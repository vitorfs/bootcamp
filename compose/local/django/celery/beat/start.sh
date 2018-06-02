#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


rm -f './celerybeat.pid'
celery -A bootcamp.taskapp beat -l INFO
