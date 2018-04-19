# kong_ldap_login_endpoint

This flask python application creates a login endpoint that authenticates a user with an LDAP server, adds a consumer for the user to a Kong API gateway giving the caller a JWT token.
It can also add/remove Kong ACL's for that consumer depending if the user is a member of the group.

[Deployed in docker hub](https://hub.docker.com/r/metcarob/kong_ldap_login_endpoint/)

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
 - Add JWT credential to consumer
 - Generate a JWT token with exp set based on LOGINEP_JWT_TOKEN_TIMEOUT
 - Reply to caller passing back their JWT token
 
## Paramaters

Paramaters are read as enviroment variables

 | Enviroment Variable Name | Example Value | Meaning |
 | ------------------------ | ------------- | ------- |
 | LOGINEP_LDAP_TIMEOUT | 60 | Seconds to wait for LDAP connection timeout |
 | LOGINEP_LDAP_HOST | unixldap.somehost.com | Host of LDAP Server |
 | LOGINEP_LDAP_PORT | 123 | Posrt of LDAP Server |
 | LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX | ldap_ | Prefix to add to ldap username when creating kong consumer |
 | LOGINEP_USER_BASE_DN | ou=People,ou=everyone,dc=somehost,dc=com | Base DN for LDAP search query used when finding a user |
 | LOGINEP_USER_ATTRIBUTE | uid | User identfying attribute for search query used when finding a user |
 | LOGINEP_GROUP_BASE_DN | ou=Group,ou=everyone,dc=somehost,dc=com | Base DN for LDAP search query used when finding a group |
 | LOGINEP_GROUP_ATTRIBUTE | cn | Group identfying attribute for search query used when finding a group |
 | LOGINEP_GROUP_MEMBER_FIELD | memberUid | Group member identifier which matches the username |
 | LOGINEP_KONG_ADMINAPI_URL | http://kong:8001 | Location of kong admin api endpoint |
 | LOGINEP_SYNCACL | gorup1,group2,group3 | comma seperated list of groups to query in LDAP. If a consumer has these groups they are added to their acl |
 | LOGINEP_JWT_TOKEN_TIMEOUT | 120 | Seconds produced JWT token is valid for. Once it is expired users will have to get another one. |

## Deployment

This container is designed to be deployed as a docker container.

## My Release Proces

 - Check all issues in the next milestone are closed
 - Run the [build process](./dockerImageBuildProcess/README.md) to create an image on my local machine
 - Run the container and make sure it comes up healthy (docker run metcarob/kong_ldap_login_endpoint:VERSION)
 - Run docker login and log in to my docker hub account
 - Run docker push metcarob/kong_ldap_login_endpoint:VERSION (Replace VERSION with version number that was just built)
 - Run docker push metcarob/kong_ldap_login_endpoint:latest
 - Rename next milestone to release number and close milestone
 - Update RELEASE.md (pointing at the milestone)
 - Create a new next milestone

## Ubuntu development enviroment setup notes

To get python-ldap working on ubuntu
````
sudo apt-get install libldap2-dev libssl-dev libsasl2-dev
````

