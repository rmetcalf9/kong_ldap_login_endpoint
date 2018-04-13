#!/bin/bash

APP_DIR=.

export LOGINEP_VERSION=
if [ -f ${APP_DIR}/../VERSION ]; then
  LOGINEP_VERSION=${0}-$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  LOGINEP_VERSION=${0}-$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${LOGINEP_VERSION} = 'E' ]; then
  echo "Can not find version file in standard locations APPDIR=${APP_DIR}"
  exit 1
fi

export LOGINEP_LDAP_TIMEOUT=60
export LOGINEP_LDAP_HOST=unixldap.somehost.com
export LOGINEP_LDAP_PORT=123
export LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX=ldap_
export LOGINEP_USER_BASE_DN=ou=People,ou=everyone,dc=somehost,dc=com
export LOGINEP_USER_ATTRIBUTE=uid
export LOGINEP_GROUP_BASE_DN=ou=Group,ou=everyone,dc=somehost,dc=com
export LOGINEP_GROUP_ATTRIBUTE=cn
export LOGINEP_GROUP_MEMBER_FIELD=memberUid
export LOGINEP_KONG_ADMINAPI_URL=http://kong:8001
export LOGINEP_SYNCACL=group1,group2,group3
export LOGINEP_JWT_TOKEN_TIMEOUT=60

python3 ./src/app.py

exit 0