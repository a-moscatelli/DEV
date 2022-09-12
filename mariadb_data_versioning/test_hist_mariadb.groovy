// https://mvnrepository.com/artifact/mysql/mysql-connector-java
@Grab( 'mysql:mysql-connector-java:5.1.27' )
@GrabConfig(systemClassLoader=true)

/*
@Grapes(
	@Grab(group='mysql', module='mysql-connector-java', version='8.0.30')
)
*/


// https://docs.groovy-lang.org/latest/html/api/groovy/sql/Sql.html

import groovy.sql.Sql

// Grab('org.hsqldb:hsqldb:2.6.1:jdk8')
// GrabConfig(systemClassLoader=true)

// https://dbschema.com/jdbc-driver/MariaDb.html


thedb = System.env.MARIADB_DATABASE
def db = [
	url:"jdbc:mysql://localhost:3306/$thedb",
	user:System.env.MARIADB_USER,
	password:System.env.MARIADB_PASSWORD,
	driver:'com.mysql.jdbc.Driver'
]

def sql = Sql.newInstance(db.url, db.user, db.password, db.driver)

sql.execute "drop table IF EXISTS PROJECT"

	// https://docs.groovy-lang.org/latest/html/api/groovy/sql/Sql.html
	sql.execute """
		 create table PROJECT (
			 id integer not null,
			 name varchar(50),
			 url varchar(100)
		 )
		WITH SYSTEM VERSIONING
	"""

println "data population ..."
def params = [10, 'Groovy', 'http://groovy.codehaus.org']
sql.execute 'insert into PROJECT (id, name, url) values (?, ?, ?)', params

sql.eachRow( "select * from PROJECT" ){ row -> println "$row.id -> $row.name , $row.url" }

println "pausing for 3s ..."
Thread.sleep(3000)

println "taking the current timestamp ..."
past=new Date().format("yyyy-MM-dd HH:mm:ss",TimeZone.getTimeZone('UTC')) // '2018-05-03 07:22:33' 
		// https://rmr.fandom.com/wiki/Groovy_Date_Parsing_and_Formatting
		// https://stackoverflow.com/questions/20923364/groovy-date-format-for-utc-with-milliseconds
		
println past
println "---"
println "pausing for 3s ..."
Thread.sleep(3000)

println "updating ..."
newUrl="https://groovy-lang.org/"
sql.executeUpdate "update PROJECT set url=$newUrl"

println "pausing for 3s ..."
Thread.sleep(3000)

println "show current table ..."
sql.eachRow( "select * from PROJECT" ){ row -> println "$row.id -> $row.name , $row.url" }
println "---"
assert sql.firstRow( "select * from PROJECT" )?.url?.contains("-lang")

println "show table as of 3s ago = before the last update ..."
sql.eachRow( "select * from PROJECT FOR SYSTEM_TIME AS OF TIMESTAMP '"+past+"'" ){ row -> println "$row.id -> $row.name , $row.url" }
println "---"
assert sql.firstRow( "select * from PROJECT FOR SYSTEM_TIME AS OF TIMESTAMP '"+past+"'" )?.url?.contains(".codehaus")

println "show table with full history..."
sql.eachRow( "select *, ROW_START, ROW_END from PROJECT FOR SYSTEM_TIME ALL" ){ row -> println row } // "$row.id -> $row.name , $row.url" }
println "---"

