
# https://stackoverflow.com/questions/55961615/how-to-integrate-wikidata-query-in-python

url = 'https://query.wikidata.org/sparql'
query = '''
SELECT ?item ?itemLabel ?linkcount WHERE {
    ?item wdt:P31/wdt:P279* wd:Q35666 .
    ?item wikibase:sitelinks ?linkcount .
FILTER (?linkcount >= 1) .
SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" . }
}
GROUP BY ?item ?itemLabel ?linkcount
ORDER BY DESC(?linkcount)
limit 50
'''

# https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv

import csv
import requests

#CSV_URL = 'http://samplecsvs.s3.amazonaws.com/Sacramentorealestatetransactions.csv'

headers = {"Accept": "text/csv; charset=utf-8"}

with requests.Session() as s:
    download = s.get(url,params = {'query': query},headers=headers)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)
		