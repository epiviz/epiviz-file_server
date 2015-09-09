'''
Created on Mar 12, 2014

@author: florin
'''

from threading import Lock
import threading

import tornado.httpserver
import tornado.ioloop
import tornado.web

from epiviz.websocket.EpiVizPyEndpoint import EpiVizPyEndpoint


class EpiVizPy(object):
    '''
    classdocs
    '''

    def __init__(self, console_listener=None, server_path=r'/ws', rserve_host = 'localhost', rserve_port = 6311):
        '''
        Constructor
        '''
        # start Rserve connection
        self._rserve_conn = pyRserve.connect(host=rserve_host, port=rserve_port)

        # define the handler function
        self._rserve_conn.voidEval("""handle_request <- function(id, action, msgData)
                                   {
                                     out <- list(type="response",
                                                 requestId=id,
                                                 data=NULL);
                                     out$data <- mgr$handle(action, msgData);
                                     epivizr:::toJSON(out)
                                  }""")
        self._handler = self._rserve_conn.r.handle_request
        self._thread = None
        self._server = None
        self._console_listener = console_listener
        self._application = tornado.web.Application([(server_path, EpiVizPyEndpoint, {
          'console_listener': console_listener,
          'handler': self.handler
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
