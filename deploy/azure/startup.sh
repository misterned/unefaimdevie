#!/usr/bin/env bash
set -e
python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn croisicwebzine.wsgi:application --bind=0.0.0.0:$PORT
