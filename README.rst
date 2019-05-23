MRGen
=====
|Build Status|
|Codacy Quality Badge|

MRGen is a monitoring and reporting tool. It is used to keep historical records
based on Watchman Monitoring and RepairShopr services. It also generates
reports for clients based on this historical data.

Developed and maintained by `Sheldon Woodward
<https://github.com/sheldonkwoodward>`_ for `Out of a Jam Solutions
<http://www.outofajam.net/>`_.

Local Setup
-----------
Following are steps to setup the local development environemt. First clone the
project and follow the steps to setup the front-end and back-end.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^
Environment variables are handled differently in devlopment and production. For
development, you can copy the ``.env.sample`` file in the ``backend/`` folder
and rename it to ``.env``. The environment variables that Django needs will be
set by Pipenv.

For the Django dev server, the only required environemnt variables are:

- ``DJANGO_ENV`` - Set to ``prod`` for production or ``dev`` to run in debug mode
- ``DJANGO_RDS`` - Set to ``prod`` to use MySQL or ``dev`` to use SQLite
- ``WATCHMAN_API_KEY`` - The Watchman Monitoring API key
- ``REPAIRSHOPR_API_KEY`` - The RepairShopr API key

If you set ``DJANGO_RDS`` to ``prod`` then you will need to specify MySQL
connection details with the follwing environemt variables if they are not
the default values.

- ``RDS_HOSTNAME`` - ``127.0.0.1`` - The MySQL server hostname
- ``RDS_PORT`` - ``3306`` - The MySQL server port
- ``RDS_DB_NAME`` - ``mrgen`` - The MySQL server database name
- ``RDS_USERNAME`` - ``root`` - The MySQL server user
- ``RDS_PASSWORD1`` - ``password`` - The MySQL server user's password

Also, you can speicify the host that Redis runs on if necessarry:

- ``REDIS_HOSTNAME`` - ``localhost`` - The Redis server hostname

See the environment variables section below in the deployment
section for details on production environment variables.

Django Setup
^^^^^^^^^^^^
1. Install the project dependencies

::

  $ pipenv install

Sometimes installing the mysqlclient dependency will raise an error, use the
following commands to get past this.

::

  $ export LDFLAGS="-L/usr/local/opt/openssl/lib"
  $ export CPPFLAGS="-I/usr/local/opt/openssl/include"

2. Migrate the database

::

  $ pipenv run python manage.py migrate

3. Start Redis

::

  $ redis-server

4. Start the celery worker process

::

  $ pipenv run celery -A MRGen worker -l info

5. Start the Beat process

::

  $ pipenv run celery -A MRGen beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

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

Deployment
----------
Following are steps to setup the production deployment environemt. First clone
the project and follow the steps to deploy the application.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^
Environemnt variables for production deployment should be defined in a ``.env``
in the project root. Docker Compose will use this centralized ``.env`` file to
distribute the proper configuration to each part of the application.

The only environment variables that must be set are:

- ``DJANGO_SECRET_KEY`` - The secret key to prevent CSRF
- ``DJANGO_HOST_DOMAIN`` - The domain name the site is running on
- ``DJANGO_URL`` - The base url for the Django server used by Vue
- ``VUE_URL`` - The base url for the Vue server used by Django
- ``RDS_PASSWORD`` - The password to use for the MySQL database
- ``WATCHMAN_API_KEY`` - The Watchman Monitoring API key
- ``REPAIRSHOPR_API_KEY`` - The RepairShopr API key

Optionally, these other environemnt variables can be set but provide no real
use excpet for custom setups or debugging:

- ``IMAGE_TAG`` - ``latest`` - The tag for the MRGen Docker image
- ``DJANGO_ENV`` - ``prod`` - Either ``prod`` for production or anything else for non-production
- ``DJANGO_RDS`` - ``prod`` - Either ``prod`` for MySQL or anything else SQLite
- ``RDS_DB_NAME`` - ``mrgen`` - The MRGen database name
- ``RDS_USERNAME`` - ``mrgen`` - The database's non-root superuser


Docker Compose
^^^^^^^^^^^^^^
After setting up the ``.env`` file, the container can be deployed with the
following command:

::

  $ docker-compose up -d

Migrations and Static Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Before the application is ready to be used, the database must be migrated. You
can run the migrations with the following command:

::

  $ docker-compose exec backend python manage.py migrate

If you already have an existing database, this command does not need to be run
again unless the MRGen database configuration has changed.


.. |Build Status| image:: https://travis-ci.org/out-of-a-jam-solutions/MRGen.svg?branch=develop
    :target: https://travis-ci.org/out-of-a-jam-solutions/MRGen

.. |Codacy Quality Badge| image:: https://api.codacy.com/project/badge/Grade/10655399a0d44d3bb24ed2fd10d0b8b0
    :target: https://www.codacy.com/app/sheldonkwoodward/MRGen?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=out-of-a-jam-solutions/MRGen&amp;utm_campaign=Badge_Grade
