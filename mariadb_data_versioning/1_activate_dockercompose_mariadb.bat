

@echo from https://hub.docker.com/_/mariadb

call setenv.bat

docker-compose -f docker-compose-mariadb-4-datver.yml up -d
