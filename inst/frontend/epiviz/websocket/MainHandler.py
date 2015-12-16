import tornado.web
import logging

class MainHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self._handler = kwargs.pop('handler')
        super(MainHandler, self).__init__(*args, **kwargs)

    def get(self):
        res = self._handler()
        logging.info("Got this: " + res)
        self.write(res)
