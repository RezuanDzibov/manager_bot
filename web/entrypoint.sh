#!/bin/sh

  while ! nc -z db 5432; do
    sleep 0.1
  done

bash -c "cd web && python manage.py collectstatic --noinput"
bash -c "cd web && python manage.py makemigrations"
bash -c "cd web && python manage.py migrate"
bash -c "cd web && python manage.py loaddata initial_fixture.json"
exec "$@"