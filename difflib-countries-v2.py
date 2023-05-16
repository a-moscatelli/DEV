import difflib
import pandas as pd

dir='./'

countrynames_WB = set(pd.read_csv(dir+'worldbank-countries.csv',encoding='utf-8')['Country Name'].values) # world bank
countrynames_GN = set(pd.read_csv(dir+'geonames-countries-html.csv',encoding='utf-8')['Country Name'].values) # geonames

def string_similarity(str1, str2):
	result =  difflib.SequenceMatcher(a=str1.lower(), b=str2.lower())
	rt = result.ratio()
	assert rt >= 0.0 and rt <= 1.0
	return rt


countrynames_com = countrynames_WB.intersection(countrynames_GN)
countrynames_GN_only = countrynames_GN - countrynames_WB
countrynames_WB_only = countrynames_WB - countrynames_GN
print('countrynames_com',len(countrynames_com))
print('countrynames_GN_only',len(countrynames_GN_only))
print('countrynames_WB_only',len(countrynames_WB_only))

negative_float_K = -0.123
dfscores = pd.DataFrame(negative_float_K, index = list(countrynames_WB_only), columns = list(countrynames_GN_only))
# dfscores = a matrix with column names = wb, row names = gn
for c in dfscores.columns:
	for r in dfscores.index.values:
		dfscores.at[r, c] = string_similarity(r,c)

print('- perfect matches:')
print('|SN|name|')
for i, cn in enumerate(countrynames_com):
	print('|'.join(['',str(i),cn,'']))

print('- matching the rest:')
print('|SN|wb|gn|difflib.SequenceMatcher score|')
for i in range(min(dfscores.shape)):
	cols_bests = dfscores.max()
	abs_best = max(cols_bests)
	col_of_best = cols_bests.idxmax()
	row_of_best = dfscores[col_of_best].idxmax()
	print( '|'.join(['',str(i),col_of_best,row_of_best,str(round(abs_best,4)),'']))
	dfscores.drop(col_of_best,inplace=True,axis=1)
	dfscores.drop(row_of_best,inplace=True,axis=0)
