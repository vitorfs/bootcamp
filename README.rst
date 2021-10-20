Django 3 Social Network
========

Web app: https://www.antisocialnetwork.live

My version of the Bootcamp social network, in which I added new functionalities and updated it to use Django 3.

.. image:: https://travis-ci.org/vitorfs/bootcamp.svg?branch=master
    :target: https://travis-ci.org/vitorfs/bootcamp
    :alt: TravisCI Status

.. image:: https://coveralls.io/repos/github/vitorfs/bootcamp/badge.svg?branch=master
    :target: https://coveralls.io/github/vitorfs/bootcamp?branch=master
    :alt: Coverage

.. image:: https://requires.io/github/vitorfs/bootcamp/requirements.svg?branch=master
    :target: https://requires.io/github/vitorfs/bootcamp/requirements/?branch=master
    :alt: Requirements

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
    :target: https://github.com/pydanny/cookiecutter-django/
    :alt: Built with Cookiecutter Django

:License: MIT

Bootcamp is an open source **social network** of open purpose, on which you can build for your own ends.

The project has the following apps:

* Feed (A Twitter-like microblog)
* Articles (A collaborative blog)
* Question & Answers (A Stack Overflow-like platform)
* Messenger (A basic chat-a-like tool for asynchronous communication.)
* Network of registered people, in which you can add, follow or remove friends.

It also includes the Sightengine API to filter innapropriate content of URL or uploaded images in the feed.
-> https://sightengine.com

Some of the new features:

- New design
- Login with Facebook
- Dark mode
- Content filtering
- Chat with your friends
- See friends login and posts activity

Technology Stack
----------------

* Python_ 3.6.x / 3.7.x
* `Django Web Framework`_ 3.x
* PostgreSQL_
* `Redis 5.0`_
* Daphne_
* Caddy_
* Docker_
* docker-compose_
* WhiteNoise_
* `Twitter Bootstrap 4`_
* `jQuery 3`_
* Django-channels_ (for WebSockets)
* Sentry_
* Mailgun_
* Cookiecutter_
* Sightengine_

.. _Python: https://www.python.org/
.. _`Django Web Framework`: https://www.djangoproject.com/
.. _PostgreSQL: https://www.postgresql.org/
.. _`Redis 5.0`: https://redis.io/documentation
.. _Daphne: https://github.com/django/daphne/
.. _Caddy: https://caddyserver.com/docs
.. _Docker: https://docs.docker.com/
.. _docker-compose: https://docs.docker.com/compose/
.. _WhiteNoise: http://whitenoise.evans.io/en/stable/
.. _`Twitter Bootstrap 4`: https://getbootstrap.com/docs/4.0/getting-started/introduction/
.. _`jQuery 3`: https://api.jquery.com/
.. _Django-channels: https://channels.readthedocs.io/en/latest/
.. _Sentry: https://docs.sentry.io/
.. _Mailgun: https://www.mailgun.com/
.. _Cookiecutter: http://cookiecutter-django.readthedocs.io/en/latest/index.html
.. _Sightengine: https://sightengine.com

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

Sentry is an error logging aggregator service. You can `sign up`_ for a free account  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

.. _`sign up`: https://sentry.io/signup/?code=cookiecutter

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
