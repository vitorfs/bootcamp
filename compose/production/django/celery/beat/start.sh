#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A bootcamp_v_two.taskapp beat -l INFO
