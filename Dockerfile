FROM alpine

MAINTAINER Robert Metcalf

RUN apk add --no-cache bash python3 curl build-base openldap-dev python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip3 install --upgrade pip

ENV APP_DIR /app
ENV LOGINEP_LDAP_TIMEOUT 60
ENV LOGINEP_LDAP_HOST unixldap.somehost.com
ENV LOGINEP_LDAP_PORT 123
ENV LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX ldap_
ENV LOGINEP_USER_BASE_DN ou=People,ou=everyone,dc=somehost,dc=com
ENV LOGINEP_USER_ATTRIBUTE uid
ENV LOGINEP_GROUP_BASE_DN ou=Group,ou=everyone,dc=somehost,dc=com
ENV LOGINEP_GROUP_ATTRIBUTE cn
ENV LOGINEP_GROUP_MEMBER_FIELD memberUid
ENV LOGINEP_KONG_ADMINAPI_URL http://kong:8001
ENV LOGINEP_SYNCACL group1,group2,group3
ENV LOGINEP_JWT_TOKEN_TIMEOUT 60


# LOGINEP_VERSION is not definable here as it is read from the VERSION file inside the image

EXPOSE 80

RUN \
  mkdir ${APP_DIR}


COPY ./app/src ${APP_DIR}
RUN pip3 install -r ${APP_DIR}/requirments.txt

COPY ./VERSION /VERSION

COPY ./app/run_app_docker.sh /run_app_docker.sh

CMD ["/run_app_docker.sh"]

# Regular checks. Docker won't send traffic to container until it is healthy
#  and when it first starts it won't check the health until the interval so I can't have
#  a higher value without increasing the startup time
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://127.0.0.1:80/frontend/index.html || exit 1

##docker run --name loginc -p 80:80 -d metcarob/kong_ldap_login_endpoint:latest