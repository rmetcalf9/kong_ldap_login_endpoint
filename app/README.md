# App Development

## TDD - Continous tests

````
continous_test.sh
````

## Run a development instance

Copy run_app_developer.sh to run_app_developer_private.sh - This private file will not be pushed to git
Edit the private file and change the params to connect to your LDAP server
Run a test Kong instnace. (You can use /utils/runTestKongInstance.yml docker compose file.)
Run run_app_developer_private.sh

You should be able to call the instance on 127.0.0.1:80/login
and access the konga instance on 127.0.0.1:1337/#!/dashboard
you can call a test hello world service on 127.0.0.1:79/helloworldservice
