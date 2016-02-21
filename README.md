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
python `Rscript -e "epivizFileServer::frontendPath()"`
```

This requires python with tornado installed.

## demo

Start epiviz with websocket connection to tornado front end at [http://epiviz.cbcb.umd.edu/?websocket-host[]=ws://localhost:8888/ws&settings=default&](http://epiviz.cbcb.umd.edu/?websocket-host[]=ws://localhost:8888/ws&settings=default&)

## Docker

This package defines a Docker image that may be used to run an instance of the file server.
It is registered in DockerHub. You can run the server with data included in the package by using

```{bash}
docker run -d --name epivizfs -p 8888:8888 epiviz/file_server
```

After the container starts running, you can run the epiviz app against the docker container:

[http://epiviz.cbcb.umd.edu/?websocket-host[]=ws://192.168.99.100:8888/ws&settings=default&](http://epiviz.cbcb.umd.edu/?websocket-host[]=ws://192.168.99.100:8888/ws&settings=default&)

You should use the result of `docker-machine ip <machine>` to get the fileserve address.

To use your own data with this container, there are a few options.

1. Mount data from host machine into default directory used in container

    ```{bash}
    # have to use absolute path
    HOST_VOLUME=${PWD}/datadir
    
    # assumes directory has a metadata.yml file
    docker run -d --name epivizfs -p 8888:8888 -v ${HOST_VOLUME}:/epivizfs_data epiviz/file_server
    ```

2. Mount data from host machine into a different volume used in container

    ```{bash}
    # have to use absolute paths
    HOST_VOLUME=${PWD}/datadir
    VM_VOLUME=/epivizfs_mydata
    METADATA_FILE=metadata.yml
    
    # environment variable overrides defaults
    docker run -d --name epivizfs -p 8888:8888 -v ${HOST_VOLUME}:${VM_VOLUME} -e "EPIVIZFS_BACKEND_PATH=${VM_VOLUME}/${METADATA_FILE}" epiviz/file_server
    ```

3. Use a Dockerfile and copy data to container

    All of these can be used in a new Dockerfile as well:
    
    ```{dockerfile}
    FROM epiviz/file_server
    COPY ./datadir /epivizfs_data
    VOLUME /epivizfs_data
    ```
    
    ```{bash}
    docker build -t my_epivizfs .
    docker run -d --name epivizfs -p 8888:8888 my_epivizfs
    ```

If you are using other docker containers but would like to use the data served by the epivizFileServer, use the --volumes-from option.

For example to run a simple ubuntu docker image with the data from epivizFileServer mapped to it,

```{bash}
docker run -t -i --volumes-from epivizfs ubuntu /bin/bash
```

After docker loads the ubuntu image, if you list files in the current directory, you should be able to see the mounted epiviz data directory. Any changes made to the data directory from any container should be persistent.