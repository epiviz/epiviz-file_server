'''
Created on Mar 12, 2014

@author: florin
'''

from threading import Lock
import threading
import logging

import tornado.httpserver
import tornado.wsgi
import tornado.ioloop
import tornado.web

import pyRserve
import time

from pprint import pprint

from epiviz.websocket.EpiVizPyEndpoint import EpiVizPyEndpoint
from epiviz.websocket.MainHandler import MainHandler
from epiviz.websocket.Measurements import app

def connect_to_rserve(host, port, wait_time=2, wait_loop=10):
  logging.info("Connecting to Rserve at %s:%d" % (host, port))
  i = 0
  conn = None
  exception = None

  while i < wait_loop:
    i += 1
    logging.info("Connection attempt %d of %d " % (i, wait_loop))
    try:
      conn = pyRserve.connect(host=host, port=port)
      break
    except pyRserve.rexceptions.RConnectionRefused as e:
      exception = e
    time.sleep(wait_time)
  if conn is None:
    raise exception

  logging.info("Connection to Rserve successful.")
  return conn

class EpiVizPy(object):
    '''
    classdocs
    '''

    def __init__(self, console_listener=None, server_path=r'/ws', rserve_host = 'localhost', rserve_port = 6311):
        '''
        Constructor
        '''
        # start Rserve connection
        self._rserve_conn = connect_to_rserve(host=rserve_host, port=rserve_port)

        # define the handler function
        self._rserve_conn.voidEval("""handle_request <- function(json_message)
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
        self._rserve_conn.voidEval("""show_server <- function()
                                   {
                                        conn <- textConnection("out", open="w")
                                        capture.output(show(fileServer), file=conn)
                                        close(conn)
                                        paste(out, collapse="\n")
                                   }""")

        self._handler = self._rserve_conn.r.handle_request

        self._main_handler = self._rserve_conn.r.show_server

        tr = tornado.wsgi.WSGIContainer(app)

        self._thread = None
        self._server = None
        self._console_listener = console_listener
        self._application = tornado.web.Application([
            (server_path, EpiVizPyEndpoint, {
                'console_listener': console_listener,
                'handler': self._handler}),
            (r"/", MainHandler, {
                'handler': self._main_handler
            }),
            (r".*", tornado.web.FallbackHandler, dict(fallback=tr))
            ], debug=True)

    def start(self, port=8888):
        self.stop()

        self._thread = threading.Thread(target=lambda: self._listen(port)).start()
        if not self._console_listener is None:
            self._console_listener.listen()
            self.stop()

    def stop(self):
        if self._server != None:
            # self._server.stop()
            tornado.ioloop.IOLoop.instance().stop()
            self._server = None
            self._thread = None

    def _listen(self, port):
        self._server = tornado.httpserver.HTTPServer(self._application)
        self._server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
