MRGen
-----

Local Setup
+++++++++++
1. Clone the project

2. Install project dependencies

::

  $ pipenv install

3. Migrate the database

::

  $ pipenv run python manage.py migrate

4. Start Redis

::

  $ redis-server

5. Start the celery worker process

::

  $ pipenv run celery -A MRGen worker -l info

6. Start the Beat process

::

  $ pipenv run celery -A MRGen beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
