# base image
FROM node:lts-alpine
# install simple http server for serving static content and add the non-privileged user
RUN npm install -g http-server && \
    adduser -S mrgen
# cd into the user's home directory
WORKDIR /home/mrgen
# install project dependencies
COPY frontend/package.json package.json
COPY frontend/package-lock.json package-lock.json
RUN npm install
# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY frontend/.eslintrc.js .eslintrc.js
COPY frontend/babel.config.js babel.config.js
COPY frontend/public public
COPY frontend/src src
# build app for production with minification
ARG VUE_APP_BACKEND_URL
RUN echo "VUE_APP_BACKEND_URL=$VUE_APP_BACKEND_URL" > .env.production && \
    npm run build --mode=production
# set docker container environment variable
ENV DOCKER_CONTAINER=1
# expose the web server port
EXPOSE 8080
# change to the non-privileged user
USER mrgen
# launch the application
CMD ["http-server", "--cors", "dist"]
