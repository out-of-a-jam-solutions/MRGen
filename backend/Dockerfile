# base image
FROM python:3.7-alpine
# labels
LABEL maintainer contact@sheldonw.com
# install build dependencies and create new user
RUN apk add mariadb-dev pcre pcre-dev libxml2 xmlsec-dev cairo-dev pango-dev gdk-pixbuf && \
    apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers libffi-dev libxslt-dev nodejs-npm musl-dev jpeg-dev zlib-dev && \
    pip install pipenv==2018.11.26 uwsgi~=2.0 && \
    set -e && \
    adduser -S mrgen
# create the webroot with Django's static file directory
ENV DJANGO_STATIC_DIR /home/mrgen/static/
# cd to the user's home directory
WORKDIR /home/mrgen
# copy necessary Django files and directories
COPY manage.py manage.py
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY uwsgi.ini uwsgi.ini
COPY MRGen MRGen
COPY reporter reporter
# install the dependencies and collect the static files
RUN pipenv install --system --deploy && \
    python manage.py collectstatic --noinput
# set docker container environment variable
ENV DOCKER_CONTAINER=1
# expose the Django server port
EXPOSE 8000
# delete the build dependencies
RUN apk del .build-deps
# change to the non-privileged user
USER mrgen
# launch the application
CMD ["uwsgi", "--ini", "/home/mrgen/uwsgi.ini"]
