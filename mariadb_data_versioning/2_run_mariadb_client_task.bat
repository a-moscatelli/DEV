

call setenv.bat

set JAVA_HOME=M:\APPS\openjdk8

set GROOVY=M:\_MG_PORTABLE\_MG_STACK_Y\groovy-2.5.6\bin\groovy.bat
call %GROOVY% test_hist_query_on_mariadb.groovy
