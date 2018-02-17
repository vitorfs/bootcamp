#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


celery -A bootcamp_v_two.taskapp worker -l INFO
