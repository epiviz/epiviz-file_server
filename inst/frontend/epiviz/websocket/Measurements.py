from flask import Flask, jsonify, request
from flask.ext.cache import Cache
import requests, json
import pandas as pd
import math
from pandas.io.json import json_normalize
import numpy as np
import websocket
from pprint import pprint

import pyRserve
import EpiVizPy as ePy

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

annotation_exclude = ['datasourceId', 'datasourceGroup', 'name']

# Support for CORS
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

app.after_request(add_cors_headers)

# get measurement data from epivizFileServer.
def getEpivizMeasurements():
    res = cache.get('measurements_raw')
    if not res:
        rserve_conn = ePy.connect_to_rserve(host='localhost', port=6311)
        rserve_conn.voidEval("""handle_request <- function(json_message)
                             {
                               message <- rjson:::fromJSON(json_message)
                               msgData <- message$data
                               action <- msgData$action
                               out <- list(type="response",
                                           requestId=message$requestId,
                                           data=NULL)
                               out$data <- epivizFileServer::handle_request(fileServer, action, msgData)
                               epivizr:::toJSON(out)
                            }""")

        response = rserve_conn.r.handle_request('{"requestId":"1","type":"request","data":{"version":"3","action":"getMeasurements"}}')
        res = response
        cache.set('measurements_raw', res, timeout=3000000)
    return res

# for testing
# @app.route("/all", methods= ['GET', 'OPTIONS'])
# def all_measurements():
#     res = getEpivizMeasurements()
#     return res



##
#  Get /dataProviders
##
@app.route("/dataProviders", methods= ['GET', 'OPTIONS'])
def get_dataProvider():
    res = {
        'success': True,
        'dataProviders': {
            'serverName': 'EpivizFileServer',
            'serverURL': 'http://localhost:8888',
            'serverType': 'Websocket' }
    }
    return jsonify(res)

##
#  Get /dataSources
##
@app.route("/dataSources", methods= ['GET', 'OPTIONS'])
def get_dataSources():
    p_json = load_df()
    u_ds = p_json.datasourceGroup.unique()
    data = []
    for i in u_ds:
        data.append({
            "name": i,
            "description": i
        })

    return json.dumps({'success': True, 'dataSources': data})

##
#  Get /annotations/<DataSourceName>
##
@app.route("/annotations/<dataSource>", methods= ['GET', 'OPTIONS'])
def get_annotations(dataSource):

    if check_dataSource(dataSource):
        p_json = load_df()
        ds = filter_df(p_json, 'datasourceGroup', str(dataSource), "equals", False)
        ds.drop(annotation_exclude, inplace=True, axis=1)

        data = []

        for col in ds:
            tp = ds[col]
            colVal = np.array(ds[col].unique())

            colVal = [x for x in colVal if str(x) != 'nan']

            if len(colVal) > 0:
                rowCount = len(ds[col])

                temp = {
                    'field': col,
                    'description': col,
                    'stats': {
                        'distinctValues': colVal
                    },
                    'filter': [{
                        'name': 'contains',
                        'operator': 'contains',
                        'description': 'contains',
                        'supportsNegate': 'true'
                    }, {
                        'name': 'equals',
                        'operator': 'equals',
                        'description': 'equals',
                        'supportsNegate': 'true'
                    }]
                }

                if col in ["maxValue", "minValue"]:
                    temp['filter'].append({
                        'name': 'range',
                        'operator': 'range',
                        'description': 'range',
                        'supportsNegate': 'true'
                    })

                data.append(temp)
        return json.dumps({'success': True, 'dataSource': dataSource, 'dataAnnotations': data})
    else:
        return jsonify({"success": False, "result": "error! DataSource does not exist"})


##
#  Get /measurements/<DataSourceName>
##
@app.route("/measurements/<dataSource>", methods= ['GET', 'POST', 'OPTIONS'])
def get_measurements(dataSource):

    if request.method == 'OPTIONS':
        return jsonify({})

    if check_dataSource(dataSource):
        data = request.get_json()
        reqId = request.args.get('requestId')
        formatRes = request.args.get('format')

        p_json = load_df()
        ds = filter_df(p_json, 'datasourceGroup', str(dataSource), "equals", False)

        if len(data['filter']) > 0:
            for filt in data['filter']:

                if 'negate' not in filt:
                    filt['negate'] = False

                ds = filter_df(ds, str(filt['filterField']), filt['filterValue'], str(filt['filterOperator']), filt['negate'])

        dataR = []

        for index, row in ds.iterrows():
            temp = {}
            for key,val in row.iteritems():
                if type(val) == float and np.isnan(val):
                    val = None
                temp[key] = val

            dataR.append(temp)

        return json.dumps({'success': True, 'dataSource': dataSource, 'dataMeasurements': dataR})
    else:
        return jsonify({'success': False, "result": "error! DataSource does not exist"})

##
#
##




##
#  check if a datasource exists
##
def check_dataSource(dataSource):
    p_json = load_df()
    u_ds = p_json.datasourceGroup.unique()
    if dataSource in u_ds:
        return True
    else:
        return False


##
#  helper function - filter dataframe
##
def filter_df(data, field, value, type, negate):
    if type == "contains":
        if negate:
            return data[~(data[field].str.contains(value))]
        else:
            return data[data[field].str.contains(value)]
        return data[data[field].str.contains(value)]
    elif type == "equals":
        if negate:
            return data[~(data[field] == value)]
        else:
            return data[data[field] == value]
    elif type == "range":
        vals = value.split(',')
        minVal = float(vals[0])
        maxVal = float(vals[1])

        if negate:
            return data[~((data[field] >= minVal) & (data[field] <= maxVal))]
        else:
            return data[(data[field] >= minVal) & (data[field] <= maxVal)]


##
#  helper function - load all measurements into a pandas data frame
##
def load_df():
    res = getEpivizMeasurements()
    j_res = json.loads(res)
    data = []
    for i in range(0, len(j_res['data']['id'])):

        tissue = None
        subtype = None
        metadata = None

        temp = {
            'id': j_res['data']['id'][i],
            'name': j_res['data']['name'][i],
            'type': j_res['data']['type'][i],
            'datasourceId': j_res['data']['datasourceId'][i],
            'datasourceGroup': j_res['data']['datasourceGroup'][i],
            'minValue': j_res['data']['minValue'][i],
            'maxValue': j_res['data']['maxValue'][i]
        }

        if j_res['data']['annotation'][i]:
            if j_res['data']['annotation'][i][0] is not None:
                for key,val in j_res['data']['annotation'][i].iteritems():
                    temp['annotation.' + key] = val

        if j_res['data']['metadata'][i]:
            if j_res['data']['annotation'][i][0] is not None:
                temp['metadata'] = ','.join(j_res['data']['metadata'][i])

        data.append(temp)
    return pd.DataFrame(data)


# if __name__ == "__main__":
#     app.run(debug=True, port=5056)
#     # app.run()

