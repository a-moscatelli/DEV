

@echo https://hub.docker.com/_/mariadb

set MARIADB_USER=user1
set MARIADB_PASSWORD=my_cool_secret
set MARIADB_DATABASE=testdb
set MARIADB_ROOT_PASSWORD=my_cool_secret_root

set JAVA_HOME=M:\APPS\openjdk8

set GROOVY=M:\_MG_PORTABLE\_MG_STACK_Y\groovy-2.5.6\bin\groovy.bat
call %GROOVY% test_hist_mariadb.groovy
