"""Epiviz FileServer frontend

Usage:
  frontend [--rserve-host=<hostname>] [--rserve-port=<port>]

Options:
  --rserve-host=<hostname>  Address of rserve host [default: localhost]
  --rserve-port=<port>  Port where rserve listens for connections [default: 6311]
"""

from epiviz.websocket.ConsoleListener import ConsoleListener
from epiviz.websocket.EpiVizPy import EpiVizPy
from docopt import docopt

if __name__ == '__main__':
  arguments = docopt(__doc__)
  rserve_host = arguments["--rserve-host"]
  rserve_port = int(arguments["--rserve-port"])

  epivizpy = EpiVizPy(console_listener=ConsoleListener(), rserve_host=rserve_host, rserve_port=rserve_port)
  epivizpy.start()
