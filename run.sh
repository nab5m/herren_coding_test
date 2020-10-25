#!/bin/sh
pipenv install

pipenv run python manage.py collectstatic --noinput
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser --noinput
pipenv run celery -A project.settings.celery worker &
pipenv run gunicorn --bind 0.0.0.0:8000 --workers 3 project.wsgi:application
