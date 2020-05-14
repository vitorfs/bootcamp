Django Social Network
=====================

A Social Network derived from the open source Bootcamp project, with new features and design.

The project has four basic apps:

* Feed (A Twitter-like microblog)
* Articles (A collaborative blog)
* Question & Answers (A Stack Overflow-like platform)
* Messenger (A basic chat-a-like tool for asynchronous communication.)

Technology Stack
----------------

* Python_ 3.6.x / 3.7.x
* `Django 3`_
* PostgreSQL_
* `Redis 5.0`_
* Daphne_
* Caddy_
* Docker_
* docker-compose_
* WhiteNoise_
* `Bootstrap 4`_
* `jQuery 3`_
* Django-channels_ (for WebSockets)
* Sentry_
* Mailgun_
* Cookiecutter_

.. _Python: https://www.python.org/
.. _`Django 3`: https://www.djangoproject.com/
.. _PostgreSQL: https://www.postgresql.org/
.. _`Redis 5.0`: https://redis.io/documentation
.. _Daphne: https://github.com/django/daphne/
.. _Caddy: https://caddyserver.com/docs
.. _Docker: https://docs.docker.com/
.. _docker-compose: https://docs.docker.com/compose/
.. _WhiteNoise: http://whitenoise.evans.io/en/stable/
.. _`Bootstrap 4`: https://getbootstrap.com/docs/4.0/getting-started/introduction/
.. _`jQuery 3`: https://api.jquery.com/
.. _Django-channels: https://channels.readthedocs.io/en/latest/
.. _Sentry: https://docs.sentry.io/
.. _Mailgun: https://www.mailgun.com/
.. _Cookiecutter: http://cookiecutter-django.readthedocs.io/en/latest/index.html

Create tables in DB
^^^^^^^^^^^^^^^^^^^

    $ python manage.py migrate

Run application
^^^^^^^^^^^^^^^

    $ python manage.py runserver

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
