# kong_ldap_login_endpoint

This flask python application creates a login endpoint that authenticates a user with an LDAP server, adds a consumer for the user to a Kong API gateway giving the caller a JWT token.
It can also add/remove Kong ACL's for that consumer depending if the user is a member of the group.

## Why not just use the Kong LDAP plugin?

The Kong LDAP plugin will not work with Kong ACL's [See kong issue](https://github.com/Kong/kong/issues/1439).

The Kong LDAP plugin can provide authentication but it is not able to only authenticate if the user is in a particular LDAP group. (Posts I made trying to get group level LDAP authentication working)[https://discuss.konghq.com/t/ldap-authentication-plugin-group/818/2]

I considered adding a group query and group whitelist option to the Kong LDAP plugin but this would not be fesiable becuase querying LDAP for a users group memberships will take too long. 

## Usage

TODO

## Process on recieving a request

 - Recieve a GET request on /login with an Authorization header: Authorization: Basic base64(username:password) (works with ldap as well as basic)
 - Verify username and password against LDAP or return 401
 - Call Kong admin API and if there is no consumer ldap_USERNAME (ldap prefix to seperate from other consumers) create one
 - Query back all ACL's for that consumer
 - For each configured LOGINEP_SYNCACL query LDAP and verify if the user is a member of that group in LDAP
 - Remove all ACL's the consumer shouldn't have
 - Add all ACL's the consumer should have
 - Generate a JWT token with exp set based on LOGINEP_JWT_TOKEN_TIMEOUT
 - Add JWT credential to consumer
 - Reply to caller passing back their JWT token
 
## Paramaters

Paramaters are read as enviroment variables

LOGINEP_LDAP_TIMEOUT ??
LOGINEP_LDAP_HOST
LOGINEP_LDAP_PORT
LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX    - ldap_
LOGINEP_USER_BASE_DN
LOGINEP_USER_ATTRIBUTE
LOGINEP_KONG_ADMINAPI_URL  - http://kong:8001
LOGINEP_SYNCACL               - gorup1,group2,group3
LOGINEP_JWT_TOKEN_TIMEOUT   - seconds login is valid for

## Deployment

This container is designed to be deployed as a docker container.

## Notes

python-ldap:
https://helpful.knobs-dials.com/index.php/Python-ldap_notes
ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, seconds) 
use ldaps:// URL then I don't need to call start_tls


TODO Check if Kong deletes old JWT credentials that have expired/failed validation - https://discuss.konghq.com/t/are-jwt-credentials-deleted/821


## Future Docker build notes

To get python-ldap working on ubuntu
````
sudo apt-get install libldap2-dev libssl-dev libsasl2-dev
````

docker apline
???apython3-dev
````
apk add build-base openldap-dev python3-dev
````
