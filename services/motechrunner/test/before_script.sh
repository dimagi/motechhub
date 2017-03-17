#!/usr/bin/env bash

python manage.py runserver 7001 &
psql -c "CREATE USER motechrunner WITH PASSWORD 'motechrunner';" -U postgres
