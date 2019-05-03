MRGen
=====
|Build Status|
|Codacy Quality Badge|

MRGen is a monitoring and reporting tool. It is used to keep historical records
based on Watchman Monitoring and RepairShopr services.

Local Setup
-----------
Following are steps to setup the local development environemt. First clone the
project and follow the steps to setup the front-end and back-end.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^
Before starting the development servers, you must setup a ``.env`` file in the
project root. Copy the ``.env.sample`` file and modify the key value pairs to
configure your environment.

Django Setup
^^^^^^^^^^^^
1. Install the project dependencies

::

  $ pipenv install

2. Migrate the database

::

  $ pipenv run python manage.py migrate

3. Start Redis

::

  $ redis-server

4. Start the celery worker process

::

  $ pipenv run celery -A backend worker -l info

5. Start the Beat process

::

  $ pipenv run celery -A backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

6. Start the Django server

::

  $ pipenv run python manage.py runserver

Vue Setup
^^^^^^^^^
1. Change the current directory to the ``frontend`` folder

::

  $ cd frontend

2. Install the project dependencies

::

  $ npm install

3. Start the Vue web server and compiler

::

  $ npm run serve

Local Server Access
^^^^^^^^^^^^^^^^^^^
The development Django server is available by default at http://localhost:8000. The admin panel is available on ``/admin`` and the API is available on ``/api``

The development Vue web server is available be default at http://localhost:8080. The project is served on the root domain.

.. |Build Status| image:: https://travis-ci.org/out-of-a-jam-solutions/MRGen.svg?branch=develop
    :target: https://travis-ci.org/out-of-a-jam-solutions/MRGen

.. |Codacy Quality Badge| image:: https://api.codacy.com/project/badge/Grade/10655399a0d44d3bb24ed2fd10d0b8b0
    :target: https://www.codacy.com/app/sheldonkwoodward/MRGen?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=out-of-a-jam-solutions/MRGen&amp;utm_campaign=Badge_Grade
