'''
Created on Mar 12, 2014

@author: florin
'''

from threading import Lock
import threading

import tornado.httpserver
import tornado.ioloop
import tornado.web

import pyRserve
import time

from epiviz.websocket.EpiVizPyEndpoint import EpiVizPyEndpoint


def connect_to_rserve(host, port, wait_time=2, wait_loop=10):
  i = 0
  conn = None
  exception = None

  while i < wait_loop:
    i += 1
    print "Connection attempt %d of %d " % (i, wait_loop)
    try:
      conn = pyRserve.connect(host=host, port=port)
      break
    except pyRserve.rexceptions.RConnectionRefused as e:
      exception = e
    time.sleep(wait_time)
  if conn is None:
    raise exception
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
        self._handler = self._rserve_conn.r.handle_request
        self._thread = None
        self._server = None
        self._console_listener = console_listener
        self._application = tornado.web.Application([(server_path, EpiVizPyEndpoint, {
          'console_listener': console_listener,
          'handler': self._handler
        })])

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
