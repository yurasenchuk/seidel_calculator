web: gunicorn web.wsgi:application --log-file -
worker: celery -A web worker --loglevel=INFO --concurrency=10 -n worker1@webdjango122020.herokuapp.com
worker: celery -A web worker --loglevel=INFO --concurrency=10 -n worker2@webdjango122020.herokuapp.com
worker: celery -A web worker --loglevel=INFO --concurrency=10 -n worker3@webdjango122020.herokuapp.com
