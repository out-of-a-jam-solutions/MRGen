MRGen
-----
|Build Status|
|Codacy Quality Badge|

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

.. |Build Status| image:: https://travis-ci.org/out-of-a-jam-solutions/MRGen.svg?branch=develop
    :target: https://travis-ci.org/out-of-a-jam-solutions/MRGen

.. |Codacy Quality Badge| image:: https://api.codacy.com/project/badge/Grade/10655399a0d44d3bb24ed2fd10d0b8b0
    :target: https://www.codacy.com/app/sheldonkwoodward/MRGen?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=out-of-a-jam-solutions/MRGen&amp;utm_campaign=Badge_Grade
