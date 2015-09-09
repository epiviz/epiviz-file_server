# epivizFileServer

An Rserve-based server of data from files for the [epiviz](http://epiviz.org) visualization tool.

# Usage

## Rserve backend

To start the Rserve backend run in the `backend` directory

```{bash}
./start.sh
```

## Tornado frontend

To start the python tornado frontend run in the `frontend` directory

```{bash}
python main.py
```

## demo

Start epiviz with websocket connection to tornado front end at [http://epiviz.cbcb.umd.edu/?websocket-host[]=ws://localhost:8888/ws&settings=default&](http://epiviz.cbcb.umd.edu/?websocket-host[]=ws://localhost:8888/ws&settings=default&)
