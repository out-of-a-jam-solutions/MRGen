#####################
### GENERAL SETUP ###
#####################
# base image
FROM python:3.7-alpine3.9
# labels
LABEL maintainer=contact@sheldonw.com
# install build dependencies and create new user
RUN apk add mariadb-dev pcre pcre-dev libxml2 xmlsec-dev && \
    apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers libffi-dev libxslt-dev nodejs-npm && \
    pip install pipenv && \
    pip install uwsgi && \
    set -e && \
    adduser -S mrgen
# cd into the new user's home directory
WORKDIR /home/mrgen
# create the webroot with Django's static file directory
RUN mkdir -p webroot/static
ENV DJANGO_STATIC_DIR /home/mrgen/webroot/static/

#####################
### BACKEND SETUP ###
#####################
# create and cd to the backend directory
RUN mkdir backend
WORKDIR /home/mrgen/backend
# copy necessary Django files and directories
COPY backend/manage.py manage.py
COPY backend/Pipfile Pipfile
COPY backend/Pipfile.lock Pipfile.lock
COPY backend/uwsgi.ini uwsgi.ini
COPY backend/MRGen MRGen
COPY backend/reporter reporter
# install the dependencies and collect the static files
RUN pipenv install --system --deploy && \
    python manage.py collectstatic --noinput

######################
### FRONTEND SETUP ###
######################
# create and cd to the frontend directory
WORKDIR /home/mrgen
RUN mkdir frontend
WORKDIR /home/mrgen/frontend
# copy necessary Vue files and directories
COPY frontend/.env.production .env.production
COPY frontend/.eslintrc.js .eslintrc.js
COPY frontend/babel.config.js babel.config.js
COPY frontend/package.json package.json
COPY frontend/package-lock.json package-lock.json
COPY frontend/public public
COPY frontend/src src
# compile the frontend
RUN npm install && \
    npm run build --mode=production
# copy the compiled frontend files to the webroot
RUN mv dist /home/mrgen/webroot/mrgen
# remove the non-compiled frontend files
WORKDIR /home/mrgen
RUN rm -rf frontend

###################
### OTHER SETUP ###
###################
# cd to the backend directory
WORKDIR /home/mrgen/backend
# set docker container environment variable
ENV DOCKER_CONTAINER=1
# expose the Django server port
EXPOSE 8000
# delete the build dependencies
RUN apk del .build-deps
# change to the non-privileged user
USER mrgen
# launch the application
CMD ["uwsgi", "--ini", "/home/mrgen/backend/uwsgi.ini"]
