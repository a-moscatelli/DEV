
import groovy.json.JsonOutput
import groovy.json.JsonSlurper
//import groovy.json.*
import groovy.util.XmlSlurper
//import com.opencsv.CSVReader
import com.opencsv.CSVWriter

import groovy.sql.Sql
// h2-1.4.200.jar


class ESc {
	private final String url = "http://elastic:changeme@localhost:9200"
	ESc() {
		println "new client for url: "+url
	}
	def get(String uripathquery,Map jsonMap) {
		def get_ = new URL(url+uripathquery).openConnection()
		def httpstatus = get_.getResponseCode()
		if (httpstatus.equals(200)) return new JsonSlurper().parseText(get_.getInputStream().getText("UTF-8"))
		println("httpstatus: $httpstatus")
		return null
	}

	Map post(String uripath, Map jsonMap) {
		return CUD("POST", uripath, jsonMap)
	}
	Map put(String uripath, Map jsonMap) {
		return CUD("PUT", uripath, jsonMap)
	}
	Map delete(String uripath, Map jsonMap) {
		return CUD("DELETE", uripath, jsonMap)
	}
	
		
	Map CUD(String method, String uripath, Map jsonMap) {
		assert method=="POST" || method=="PUT" || method=="DELETE"
		try{
		def post_ = new URL(url+uripath).openConnection()
		String jsonText = JsonOutput.toJson(jsonMap)
		post_.setRequestMethod(method)
		post_.setDoOutput(true)
		post_.setRequestProperty("Content-Type", "application/json")
		post_.getOutputStream().write(jsonText.getBytes("UTF-8"))
		def httpstatus = post_.getResponseCode()
		if (httpstatus.equals(200)) return new JsonSlurper().parseText(post_.getInputStream().getText("UTF-8"))
		println("httpstatus: $httpstatus")
		return null
		} catch(Exception e){
			println "Exception in CUD: $e"
		}
	}		
}
	
Map create_index1_json_map_ES53 = [
	settings : [
		analysis: [
			analyzer: [
				custom_analyzer1_nGram: [
					tokenizer: "custom_tokenizer1_nGram",
					filter: [
						"lowercase",
						"asciifolding"
					]
					// https://www.elastic.co/guide/en/elasticsearch/reference/6.8/analysis-whitespace-analyzer.html
					// https://www.elastic.co/guide/en/elasticsearch/reference/6.8/analysis-ngram-tokenizer.html
				]
			],
			tokenizer: [
				custom_tokenizer1_nGram: [				
					type: "ngram",
					min_gram: 1,
					max_gram: 15,	// was 15
					//token_chars: [			"letter",			"digit" 			]
					token_chars: ["letter", "digit", "punctuation", "symbol"]
				]
			]
		]
	],
	mappings: [
		cnmatchmapping: [
			properties: [
				cn:		[ type: "text", copy_to: "allfields" ],
				capt:		[ type: "text", copy_to: "allfields" ],
				src:		[ type: "keyword" ],	// keyword means: not_analyzed
				x:			[ type: "keyword" ],	// keyword means: not_analyzed
				// location:[ type: "geo_point" ],	 // aspect_bias_search_prod_urbo
				// _all may no longer be enabled for indices created in 6.0+, use a custom field and the mapping copy_to parameter
				allfields: [
					type: "text",
					analyzer: "custom_analyzer1_nGram"
				]
			]
		]
	]
]

def get_search(String cn_, String capt_, String src_, int sz_) {
	return [
		size : sz_,
		query : [
			bool : [
				should : [
								[
									match : [
										cn : [
											query : cn_,
											boost: 1,
											fuzziness: "AUTO"
										]
									]
								],
								[
									match : [
										capt : [
											query : capt_,
											boost: 1,
											fuzziness: "AUTO"
										]
									]
								]											
							],
				minimum_should_match : 2,
				filter: [
					term : [ src : src_ ]
				]
			]
		],
		sort : [
			"_score"
		]
	]
}				
	
def es = new ESc()

def sql = Sql.newInstance("jdbc:h2:mem:test", "sa", "sa", "org.h2.Driver")
sql.execute "CREATE TABLE CC(id VARCHAR(36), cn VARCHAR(100), capt VARCHAR(100), src VARCHAR(2), outerid VARCHAR(36), score REAL)"

boolean recreate_index_mapping=true
boolean add_geonames_items=true
boolean add_worldbank_items=true
boolean test_searches=false
boolean matching=true


if(recreate_index_mapping) {
	Map rt = es.delete("/escc_idx1",create_index1_json_map_ES53)
	println "index deleted. "+rt
	
	rt = es.put("/escc_idx1",create_index1_json_map_ES53)
	println "index created. "+rt
	assert rt.acknowledged
}

if(add_geonames_items){
	String fileContents = new File("geonm-cn-capt.json/File_0.json").getText('UTF-8')
	def inputJson = new JsonSlurper().parseText(fileContents)
	inputJson.each {
		id=UUID.randomUUID().toString()	// 2fa81a3b-d236-4761-b303-92606586140d
		Map map = it+[src:"GN",c:"c"]
		sql.execute "INSERT INTO CC(id,cn,capt,src) VALUES (?,?,?,?)", [id,map.cn, map.capt,map.src]
		println "adding id $id : $map"
		Map rt = es.put("/escc_idx1/cnmatchmapping/$id",map)
	}
}

if(add_worldbank_items){
	// I had to remove the BOM from the UTF-8-BOM xml
	String fileContents = new File("wbcn.xml").getText('UTF-8')
	def rootNode = new XmlSlurper().parseText(fileContents)
	//		/<wb:countries><wb:country><wb:name>
	//		/<wb:countries><wb:country><wb:capitalCity>
	assert rootNode.'*'.size() == 299
	rootNode.'country'.eachWithIndex { it,i ->	// ["wb:country"]
		try {
			assert it.name() == "country"
			String cn = it."name" // better to store it as String before purring into the map
			String capt = it."capitalCity" // better to store as String before purring into the map
			Map map = [cn: cn, capt:capt] + [src:"WB",c:"c"]
			id=UUID.randomUUID().toString()		
			println "adding id $id : $map"
			sql.execute "INSERT INTO CC(id,cn,capt,src) VALUES (?,?,?,?)", [id,map.cn, map.capt,map.src]
			Map rt = es.put("/escc_idx1/cnmatchmapping/$id",map)
		} catch(Exception e){
			println "Exception $e"
		}
	}
}

if(test_searches) {
	// Albania, Tirane WB		and 	Albania, Tirana GN
	// "Yemen","Sanaa","GN"	and	"Yemen, Rep.","Sana'a","WB"
	rt = es.post("/escc_idx1/cnmatchmapping/_search", get_search("Yemen","Sanaa","GN",5))
	if(rt && rt.hits.total>0) {
		println rt.hits.hits[0]._source	//[cn:Italy, capt:Rome, src:GN, c:c]
		println "\t" + rt.hits.hits[0]._id	//7abaf166-8bff-45be-9523-5e6571c7c645
		println "\t" + "\t" + rt.hits.hits[0]._score	//14.922848
	}
	rt = es.post("/escc_idx1/cnmatchmapping/_search", get_search("Yemen, Rep.","Sana'a","WB",5))
	if(rt && rt.hits.total>0) {
		println rt.hits.hits[0]._source	//[cn:Italy, capt:Rome, src:GN, c:c]
		println "\t" + rt.hits.hits[0]._id	//7abaf166-8bff-45be-9523-5e6571c7c645
		println "\t" + "\t" + rt.hits.hits[0]._score	//14.922848
	}
}

if(matching) {
	outerclass = [ "WB":"GN", "GN":"WB"]
	outerclass.each{
		sql.eachRow("select * from CC where src=?",[it.key]) { row ->
			//println "$row.cn, $row.capt"// name.padRight(10)} ($row.url)"
			rt = es.post("/escc_idx1/cnmatchmapping/_search", get_search(row.cn,row.capt,it.value,1))
			if(rt && rt.hits.total==1) {
				println rt.hits.hits[0]._source	//[cn:Italy, capt:Rome, src:GN, c:c]
				println "\t" + rt.hits.hits[0]._id	//7abaf166-8bff-45be-9523-5e6571c7c645
				println "\t" + "\t" + rt.hits.hits[0]._score	//14.922848
				sql.executeUpdate "UPDATE CC SET outerid=?, score=? where id=?", [rt.hits.hits[0]._id, rt.hits.hits[0]._score, row.id]
			}
		}
	}
}

println "WRITING CSV ..."
def cmd = "CALL CSVWRITE('es-joined.csv', 'SELECT * FROM CC','charset=UTF-8')"
sql.execute cmd.toString()
sql.close()		
println "Done."


/*CSVReader reader = new CSVReader(new InputStreamReader(new FileInputStream("wb.csv"),  "UTF-8"))
file.withWriter { w ->
    new CSVPrinter(w, CSVFormat.DEFAULT).printRecords(data)
}*/

//new File("joined.csv").withWriter("UTF-8", { w -> new CSVWriter(w).writeAll(data.collect{ it as String[] }) })


