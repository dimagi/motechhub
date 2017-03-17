#!/usr/bin/env bash
set -e

./manage.py test
jasmine-node spec/
