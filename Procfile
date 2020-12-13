web: gunicorn web.wsgi:application --log-file -
worker: celery -A web worker -B --loglevel=info
