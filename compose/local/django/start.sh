#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


python manage.py migrate
python manage.py runserver 0.0.0.0:8000
