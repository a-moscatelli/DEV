@rem cd Z:\AWS_CLI\analysis_of_resources_by_tag
@set F=temp.out.json
@set C=temp.res_tags.csv
@cls
goto go1
:go1
del /Q /F %F%
aws resourcegroupstaggingapi  get-resources > %F%
del /Q /F %C%
python json-parse.py %F% aws-get-resources %C% res-tag-csv
:go2
python json-parse.py %C% res-tag-csv - res-tag-stats-print

@rem aws resourcegroupstaggingapi get-tag-keys
@rem aws resourcegroupstaggingapi get-tag-values --key project

