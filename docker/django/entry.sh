#!/bin/sh

# fab -f fabfile.py load_secrets
python manage.py collectstatic --noinput
python manage.py migrate

exec gunicorn backend.wsgi:application \
--workers $NUM_WORKERS \
--timeout $TIMEOUT \
--bind 0.0.0.0:8000
--log-level=debug \