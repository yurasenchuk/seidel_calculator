web: gunicorn web.wsgi:application --log-file -
worker: celery -A web worker -l info --pool=solo
