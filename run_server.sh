#!/bin/sh

python manage.py makemigrations
python manage.py migrate

python -R manage.py runserver 0.0.0.0:8000
