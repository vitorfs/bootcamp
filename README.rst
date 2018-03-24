Bootcamp
========

An enterprise oriented social network

[![]()]() [![]()]() [![]()]()
|Build Status|
.. image:: https://travis-ci.org/vitorfs/bootcamp.svg?branch=master
    :target: https://travis-ci.org/vitorfs/bootcamp
    :alt: TravisCI Status

|Coverage Status|
.. image:: https://coveralls.io/repos/github/vitorfs/bootcamp/badge.svg?branch=master
    :target: https://coveralls.io/github/vitorfs/bootcamp?branch=master
    :alt: Coverage

|Requirements Status|
.. image:: https://requires.io/github/vitorfs/bootcamp/requirements.svg?branch=master
    :target: https://requires.io/github/vitorfs/bootcamp/requirements/?branch=master
    :alt: Requirements

|Templating|
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
    :target: https://github.com/pydanny/cookiecutter-django/
    :alt: Built with Cookiecutter Django


:License: MIT

Bootcamp is an open source **enterprise social network** built with Python_ using the `Django Web Framework`_.

The project has four basic apps:

* Feed (A Twitter-like microblog)
* Articles (A collaborative blog)
* Question & Answers (A Stack Overflow-like platform)
* Messenger (A basic chat-a-like tool for asynchronous communication.)

.. _Python: https://www.python.org/
.. _`Django Web Framework`: https://www.djangoproject.com/


Technology Stack
----------------

* Python 3.6.x and up
* Django 1.11.x / 2.0.x
* Twitter Bootstrap 4
* jQuery 3
* Redis 3.2
* WebSockets (Using django-channels for that!)

Basic Commands
--------------

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate a simplified coverage report::

    $ pytest

To generate an HTML report::

    $ coverage html
    $ open htmlcov/index.html

To check the report in console::

    $ coverage report -m

Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html


Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
