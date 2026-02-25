#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python3 manage.py collectstatic --no-input
python3 manage.py migrate
 
# Автоматичне створення адміна, якщо його немає
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python3 manage.py createsuperuser \
    --no-input \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL || true
fi

# python3 manage.py loaddata data.json
