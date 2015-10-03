# epivizFileServer

An Rserve-based server of data from files for the [epiviz](http://epiviz.org) visualization tool.

See the [wiki](https://github.com/epiviz/epivizFileServer/wiki) for more information

# Usage

## Install package

```{r}
devtools::install_github("epiviz/epivizFileServer")
```

## Rserve backend

To start the Rserve backend run after installation (e.g.)

```{bash}
Rscript -e "epivizFileServer::startBackend()" --args metadata.yml
```

See [wiki](https://github.com/epiviz/epivizFileServer/wiki) for information on the `metadata.yml` argument.

## Tornado frontend

To start the python tornado frontend run

```{bash}
Rscript -e "epivizFileServer::startFrontend()"
```

This requires python with tornado installed.

## demo

Start epiviz with websocket connection to tornado front end at [http://epiviz.cbcb.umd.edu/?websocket-host[]=ws://localhost:8888/ws&settings=default&](http://epiviz.cbcb.umd.edu/?websocket-host[]=ws://localhost:8888/ws&settings=default&)
