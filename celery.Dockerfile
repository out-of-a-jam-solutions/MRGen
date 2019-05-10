# base image
FROM python:3.6-alpine
# lablels
LABEL maintainer contact@sheldonw.com
# install pipenv and create the celery user
RUN apk add mariadb-dev pcre pcre-dev libxml2 xmlsec-dev && \
    apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers libffi-dev libxslt-dev nodejs-npm && \
    pip install pipenv==2018.11.26 && \
    adduser -S celery
# cd into the user's home directory
WORKDIR /home/celery
# copy necessary Django files and directories
COPY backend/Pipfile Pipfile
COPY backend/Pipfile.lock Pipfile.lock
COPY backend/MRGen MRGen
COPY backend/reporter reporter
# install the dependencies
RUN pipenv install --system --deploy
# set docker container environment variable
ENV DOCKER_CONTAINER=1
# delete the build dependencies
RUN apk del .build-deps
# change to the non-privileged user
USER celery
# launch the application
ENTRYPOINT ["celery", "-A", "MRGen"]
