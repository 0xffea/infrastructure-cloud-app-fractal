#!/bin/bash

#
# We use arithmetic so require bash for declare.
#

WEBSITES_PORT=${WEBSITES_PORT:=80}
declare -i GUNICORN_NUM_WORKERS=$(nproc)*2

exec python main.py
