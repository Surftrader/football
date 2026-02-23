#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python3 manage.py collectstatic --no-input
python3 manage.py migrate

python3 create_admin.py
