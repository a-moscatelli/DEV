

@echo https://hub.docker.com/_/mariadb

set MARIADB_USER=example-user
set MARIADB_PASSWORD=my_cool_secret
set MARIADB_ROOT_PASSWORD=my-secret-pw


docker-compose -f docker-compose-mariadb-4-datver.yml up -d
