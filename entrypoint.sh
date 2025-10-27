#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

python manage.py shell <<EOF
from django.contrib.auth.models import User
import os
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
EOF

gunicorn blx_inventory.wsgi:application --bind 0.0.0.0:8000
