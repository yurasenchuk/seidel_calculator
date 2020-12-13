web: gunicorn web.wsgi:application --log-file -
celery: celery worker -A forum -l info -c 4
