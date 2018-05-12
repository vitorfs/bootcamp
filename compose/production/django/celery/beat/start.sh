#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


celery -A bootcamp.taskapp beat -l INFO
