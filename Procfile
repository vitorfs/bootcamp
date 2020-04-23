web: gunicorn config.wsgi:application --log-file -
web2: daphne -b 0.0.0.0 -p 8000 config.asgi:application
