
# https://stackoverflow.com/questions/55961615/how-to-integrate-wikidata-query-in-python

import requests


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
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()
print(data)