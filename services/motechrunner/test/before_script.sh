#!/usr/bin/env bash

psql -c "CREATE USER motechrunner WITH PASSWORD 'motechrunner' CREATEDB;" -U postgres
createdb -U motechrunner motechrunner
python manage.py migrate
python manage.py runserver 7001 &
