#!/usr/bin/env bash
set -e

./manage.py test
./node_modules/.bin/jasmine-node spec/
