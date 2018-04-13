#!/bin/bash

echo "Running python app unit tests"
cd ${GITROOT}/app
eval ${CMD_PYTHONTEST} ./test
RES=$?
if [ ${RES} -ne 0 ]; then
  echo ""
  echo "Python app unit tests failed"
  exit 1
fi

exit 0