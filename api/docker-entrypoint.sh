#!/bin/bash

#
# We use arithmetic so require bash for declare.
#

WEBSITES_PORT=${WEBSITES_PORT:=80}
declare -i GUNICORN_NUM_WORKERS=$(nproc)*2

exec uvicorn main:app  --workers ${GUNICORN_NUM_WORKERS} --host "0.0.0.0" --port ${WEBSITES_PORT}
