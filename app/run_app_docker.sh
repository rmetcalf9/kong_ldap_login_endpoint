#!/bin/bash

#Hardcoded here

export LOGINEP_MODE=DOCKER
export LOGINEP_VERSION=
if [ -f ${APP_DIR}/../VERSION ]; then
  LOGINEP_VERSION=$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  LOGINEP_VERSION=$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${LOGINEP_VERSION} = 'E' ]; then
  echo 'Can not find version file in standard locations'
  exit 1
fi

_term() { 
  echo "run_app_docker.sh - Caught SIGTERM signal!" 
  kill -TERM "$child" 2>/dev/null
}

trap _term SIGTERM

python3 -u "${APP_DIR}/app.py" &

child=$! 
wait "$child"


exit 0