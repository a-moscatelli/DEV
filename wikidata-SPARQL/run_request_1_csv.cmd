
rem https://softwarerecs.stackexchange.com/questions/36188/command-line-tool-to-query-wikidata-or-another-sparql-endpoint

rem https://wdtaxonomy.readthedocs.io/en/latest/README.html


..\..\..\repositories\tools\curl -X POST https://query.wikidata.org/sparql -H "Accept: text/csv" --ssl-no-revoke --data-urlencode query@query.sparql
