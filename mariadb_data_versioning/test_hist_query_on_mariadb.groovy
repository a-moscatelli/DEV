
@Grab( 'mysql:mysql-connector-java:5.1.27' )		// https://mvnrepository.com/artifact/mysql/mysql-connector-java
@GrabConfig(systemClassLoader=true)

/*
@Grapes(
	@Grab(group='mysql', module='mysql-connector-java', version='8.0.30')
)
*/


// https://docs.groovy-lang.org/latest/html/api/groovy/sql/Sql.html

import groovy.sql.Sql





thedb = System.env.MARIADB_DATABASE

def db = [
	url:"jdbc:mysql://localhost:3306/$thedb",
	user:System.env.MARIADB_USER,
	password:System.env.MARIADB_PASSWORD,
	driver:'com.mysql.jdbc.Driver'
]

def sql = Sql.newInstance(db.url, db.user, db.password, db.driver)

println "dropping all tables - if any ..."

sql.execute "alter table IF EXISTS KIMBALL_FACT DROP CONSTRAINT fk_city"
sql.execute "alter table IF EXISTS KIMBALL_FACT DROP CONSTRAINT fk_degree"

"KIMBALL_FACT,KIMBALL_CITYDIM_NOHIST,KIMBALL_DEGREEDIM_HIST".split(",").each { table ->
	sql.execute "drop table IF EXISTS $table".toString()	
}

println "creating all tables ..."

sql.execute """
	create OR REPLACE table KIMBALL_CITYDIM_NOHIST (
		id			MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		name		varchar(50) UNIQUE KEY
	)
"""

sql.execute """
	create OR REPLACE table KIMBALL_DEGREEDIM_HIST (
		id			MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		name		varchar(50) UNIQUE KEY
	)
	WITH SYSTEM VERSIONING
"""

sql.execute """
	create OR REPLACE table KIMBALL_FACT (
		id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		name varchar(50),
		city_id MEDIUMINT,
		degree_id MEDIUMINT,
		email varchar(50)
	)
	
	WITH SYSTEM VERSIONING
"""

sql.execute """
	ALTER TABLE KIMBALL_FACT
	ADD CONSTRAINT fk_city FOREIGN KEY (city_id) REFERENCES KIMBALL_CITYDIM_NOHIST(id),
	ADD CONSTRAINT fk_degree FOREIGN KEY (degree_id) REFERENCES KIMBALL_DEGREEDIM_HIST(id)
"""


def CRUD_C(sql,Map params) {
	sql.execute 'insert into KIMBALL_CITYDIM_NOHIST (name) values (?.c)	ON DUPLICATE KEY UPDATE name= ?.c', params
	sql.execute 'insert into KIMBALL_DEGREEDIM_HIST (name) values (?.d)	ON DUPLICATE KEY UPDATE name= ?.d', params
	sql.withTransaction {
		sql.execute "SELECT id into @c_id		FROM KIMBALL_CITYDIM_NOHIST WHERE name = ?.c", params
		sql.execute "SELECT id into @d_id		FROM KIMBALL_DEGREEDIM_HIST WHERE name = ?.d", params
		sql.execute "insert into KIMBALL_FACT (name, city_id, degree_id, email) values (?.p, @c_id, @d_id, ?.e)", params
	}
}

println "populating ..."
CRUD_C(sql,	 [p:'Alberto',c:'Milan',d:'MSc',e:'a@b.com']	)
CRUD_C(sql,	 [p:'Barbara',c:'chicago',d:'MSc',e:'a@b.com']	)
CRUD_C(sql,	 [p:'Carl',c:'Munich',d:'Phd',e:'a@b.com']	)
CRUD_C(sql,	 [p:'Darwin',c:'chicago',d:'MSc',e:'a@b.com']	)


def queryt1 = """
select
F.id as pid,
F.name as pname,
F.email as email,
C.name as cname,
D.name as dname
from
KIMBALL_CITYDIM_NOHIST C,
KIMBALL_DEGREEDIM_HIST D,
KIMBALL_FACT F
where F.degree_id = D.id and F.city_id = C.id
"""

def queryt2 = """
select
F.id as pid,
F.name as pname,
F.email as email,
C.name as cname,
D.name as dname
from
KIMBALL_CITYDIM_NOHIST as C,
KIMBALL_DEGREEDIM_HIST FOR SYSTEM_TIME AS OF TIMESTAMP ?.ts D,
KIMBALL_FACT FOR SYSTEM_TIME AS OF TIMESTAMP ?.ts as F
where F.degree_id = D.id and F.city_id = C.id
"""

def queryt3 = """
select
F.id as pid,
F.name as pname,
F.email as email,
C.id as cid,
C.name as cname,
D.name as dname,
D.id as did,
D.ROW_START D_ROW_START,
D.ROW_END D_ROW_END,
F.ROW_START F_ROW_START,
F.ROW_END F_ROW_END
from
KIMBALL_CITYDIM_NOHIST as C,
KIMBALL_DEGREEDIM_HIST				FOR SYSTEM_TIME ALL as D,
KIMBALL_FACT								FOR SYSTEM_TIME ALL as F
where F.degree_id = D.id and F.city_id = C.id
"""


sql.eachRow( queryt1 ){ row -> println "$row.pid -> $row.pname, $row.cname, $row.dname, $row.email" }

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
newparams = [
	pname : "Alberto",
	newpmail : "alberto@b.it (amended)",
	newdname : "M.Sc. (amended)",
	olddname : "MSc",
	newcname : "Chicago (amended)",
	oldcname : "chicago"
]

sql.executeUpdate "update KIMBALL_FACT set email=?.newpmail where name = ?.pname", newparams	// FACT is going to have 4+1 records
sql.executeUpdate "update KIMBALL_CITYDIM_NOHIST set name=?.newcname where name = ?.oldcname", newparams // CITY is going to have 3+2 records
sql.executeUpdate "update KIMBALL_DEGREEDIM_HIST set name=?.newdname where name = ?.olddname", newparams // DEGREE is going to have 2 records


println "pausing for 3s ..."
Thread.sleep(3000)

println "=" * 80
println "showing table as of now..."
sql.eachRow( queryt1 ){ row -> println "$row.pid -> $row.pname, $row.cname, $row.dname, $row.email" }

println "=" * 80
row1 =sql.firstRow( queryt1 )
assert row1?.email?.contains("(amended)")

println "=" * 80
println "showing table as of 3s ago i.e. before the last update ..."




sql.eachRow(queryt2, [ts:past]){ row -> println "$row.pid -> $row.pname, $row.cname, $row.dname, $row.email" }
println "=" * 80
row2 = sql.firstRow( queryt2 + " and F.name ='Barbara'", [ts:past] )
print row2
assert row2?.cname?.contains("(amended)")
print "I can only see the latest city name because the city table is not defined as historical"
assert ! row2?.dname?.contains("(amended)")
print "I can see the historical degree name because the degree table is defined as historical"

println "showing table with full history..."
println "=" * 80
sql.eachRow( queryt3 ){ row -> println "$row.pid, $row.pname, $row.email, $row.cname, $row.dname" }
println "=" * 80
int NR = sql.rows(queryt3).size()
println NR + " (nonsense)"
assert NR == 17


println ""
println "all good!"

// https://dbschema.com/jdbc-driver/MariaDb.html
// https://docs.groovy-lang.org/latest/html/api/groovy/sql/Sql.html
// https://mariadb.com/kb/en/auto_increment/
// https://www.tutorialspoint.com/mariadb/mariadb_transactions.htm
// https://www.educba.com/mariadb-transaction/
