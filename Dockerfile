FROM epiviz/docker_rbase
MAINTAINER "Hector Corrada Bravo" hcorrada@gmail.com

# install Rserve, needed for backend
RUN install2.r --error \
  Rserve

# get python numpy which we need for the
# front end
RUN apt-get update -y &&  apt-get install python-numpy -y

# copy frontend python stuff and install requirements
COPY inst/frontend /epivizfs_frontend
RUN cd /epivizfs_frontend && \
  pip install -r requirements.txt

# copy over supervisord config
COPY inst/docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chgrp staff /etc/supervisor/conf.d/supervisord.conf


EXPOSE 8888

# install the file server package
COPY . /epivizfs_pkg/epivizFileServer
RUN installPackage.r -p /epivizfs_pkg/epivizFileServer

# copy example data to be used by file server backend
COPY inst/extdata /epivizfs_data

# run everything through supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
