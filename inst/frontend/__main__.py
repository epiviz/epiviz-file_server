"""Epiviz FileServer frontend

Usage:
  frontend [--rserve-host=<hostname>] [--rserve-port=<port>] [--log=<loglevel>]

Options:
  --rserve-host=<hostname>  Address of rserve host [default: localhost]
  --rserve-port=<port>  Port where rserve listens for connections [default: 6311]
  --log=<loglevel> Logging level [default: WARNING]
"""

from epiviz.websocket.EpiVizPy import EpiVizPy
from docopt import docopt
import logging

if __name__ == '__main__':
  arguments = docopt(__doc__)
  rserve_host = arguments["--rserve-host"]
  rserve_port = int(arguments["--rserve-port"])
  loglevel = arguments["--log"]

  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
      raise ValueError('Invalid log level: %s' % loglevel)

  logging.basicConfig(level=numeric_level)
  epivizpy = EpiVizPy(console_listener=None, rserve_host=rserve_host, rserve_port=rserve_port)
  epivizpy.start()
