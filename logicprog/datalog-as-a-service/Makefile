# Makefile

# winstone with abcdatalog

thecp = .;./servlet-api-2.5.jar;./AbcDatalog-0.6.0.jar;./org.json-chargebee-1.0.jar
javahome = M:\APPS\openjdk8

# all: clean build run

run: WebApplication.war
	@echo === running:
	@echo open: http://localhost:8080/HelloWorldu
	$(javahome)\bin\java.exe -jar winstone-0.9.10.jar --warfile=WebApplication.war


WebApplication.war: web.xml HelloWorld.class
	@echo === building the war
	-mkdir webapp1\WEB-INF\classes
	-mkdir webapp1\WEB-INF\lib
	-copy web.xml webapp1\WEB-INF\web.xml
	-copy HelloWorld.class webapp1\WEB-INF\classes\HelloWorld.class
	-copy AbcDatalog-0.6.0.jar webapp1\WEB-INF\lib\AbcDatalog-0.6.0.jar
	-copy org.json-chargebee-1.0.jar webapp1\WEB-INF\lib\org.json-chargebee-1.0.jar

	-cd webapp1 && $(javahome)\bin\jar.exe -cvf ..\WebApplication.war *
	@echo === building the war

HelloWorld.class: HelloWorld.java
	@echo === compiling the servlet
	$(javahome)\bin\javac.exe -source 8 -target 8 -cp $(thecp) HelloWorld.java
	@echo === servlet is compiled

clean:
	@echo === clean starts
	-del /Q HelloWorld.class
	-del /q /s webapp1
	-rmdir /S /Q webapp1
	-del /Q WebApplication.war
	-rmdir /S /Q C:\Users\moscatea\AppData\Local\Temp\1\winstone\moscatea\WebApplication.war
	@echo === clean completed


use: load query

load:
		@echo load a KB - do not use double quotes as percent sign is preprocessed
		curl 'http://localhost:8080/HelloWorldu?uc=learn&kb=edge(a,%20b).%20edge(b,%20c).%20edge(c,%20d).%20edge(d,%20c).%20tc(X,%20Y)%20:-%20edge(X,%20Y).%20tc(X,%20Y)%20:-%20tc(X,%20Z),%20tc(Z,%20Y).'

query:
	@echo query the KB - do not use double quotes as percent sign is preprocessed
	curl 'http://localhost:8080/HelloWorldu?uc=query&qs=tc(X,%20Y)?'
