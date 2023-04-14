# I am on github
import json
# also available: https://pypi.org/project/jsonpath-python/
import sys
import sqlite3 as sql
import pandas as pd

# aws resourcegroupstaggingapi  get-resources > resourcegroupstaggingapi-get-resources.out.txt

assert len(sys.argv) == 1+2+2

this_script, in_file, in_file_format, out_file, out_file_format = sys.argv


#if in_file_format == 'aws-get-resources' and out_file_format == 'res-tag-csv':
	#pass

if in_file_format == 'aws-get-resources' and out_file_format == 'res-tag-csv':

	data = json.load(open(in_file, 'r'))
	res_list = data['ResourceTagMappingList']
	records = []
	for res in res_list:
		arn=res["ResourceARN"]
		kv_list = res["Tags"]
		for kv in kv_list:
				k = kv["Key"]
				v = kv["Value"]
				entry = { 'res' : arn,	'key' : k, 'val' : v}
				records.append(entry)
				
	df = pd.DataFrame(records)
	df.to_csv(out_file, encoding='utf-8', header=True, index=True, index_label="id")	# sep='\t', 

if in_file_format == 'res-tag-csv' and out_file_format == 'res-tag-stats-print':
	# https://towardsdatascience.com/python-pandas-and-sqlite-a0e2c052456f
	df = pd.read_csv(in_file,encoding='utf-8') #, index_col='id')
	df.set_index('id')
	conn = sql.connect(':memory:')
	df.to_sql('restag', con=conn)
	
	pd.options.display.max_rows = None
	pd.options.display.max_colwidth = None
	
	sql='''
	select * from restag
	'''
	dfq = pd.read_sql(sql, conn)
	#print(dfq)
	
	hr="=" * 80
	eol="\n"
	
	print(hr,eol,"count of key, values","(None) can be shown")
	sql="select key,val,count(*) as countof from restag group by key,val"

	dfq = pd.read_sql_query(sql, conn)
	print(dfq)


	conn.close()




