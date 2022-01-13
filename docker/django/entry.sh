#!/bin/sh

# fab -f fabfile.py load_secrets
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

NUM_WORKERS=3
TIMEOUT=120

exec gunicorn backend.wsgi:application \
--workers $NUM_WORKERS \
--timeout $TIMEOUT \
--bind 0.0.0.0:8000
--log-level=debug \