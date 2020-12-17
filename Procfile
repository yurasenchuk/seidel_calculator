web: gunicorn web.wsgi:application --log-file -
worker: celery -A proj worker --loglevel=INFO --concurrency=10
