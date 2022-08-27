
# this is based on the udemy course
# https://www.udemy.com/course/association-mining-for-machine-learning/learn/lecture/24030180#notes

# this is AKA market basket analysis

# from https://stats.stackexchange.com/questions/229523/association-rules-support-confidence-and-lift
# If I am going to order / rank my rules and pick, let say the best 10 to examine, which indicator should be chosen as the ranking variable?

# usually you want all three to be high:
#		high support: should apply to a large amount of cases
#		high confidence: the rule should be correct often
#		high lift: indicates it is not just a coincidence

# also see:
# https://en.wikipedia.org/wiki/Association_rule_learning#Useful_Concepts


import pandas as pd
import re
import itertools


#import yaml

# ################################################################### section  1 - globals and functions - loading data

do_check_every_basket_is_duplic_free = True
specialcomment = '#'

baskets_file1 = 'association_mining_baskets.txt'
baskets_file2 = 'association_mining_baskets_oranges.txt'
baskets_file = baskets_file2

#min_support_count = 2
min_support = 0.15
min_confid = 0.75
min_lift = 2.0

# ################################################################### section  1 - globals and functions - loading data


pct	= lambda f: '{:.0%}'.format(f)


def get_list_of_list_of_strings(basket_filename_txt,do_check_every_basket_is_duplic_free):				# get_ListOf_OrderedListOf_Text_Baskets
	retL = list()	# baskets
	retS = set()	# items
	
	with open(basket_filename_txt, "r", encoding='utf8') as infile:		# with will auto-close the file
		for line in infile:	#	reading (almost) line by line - 	src: https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
			line = line.split(specialcomment)[0]	# remove stuff beyond # i.e. comments
			line = line.strip()
			if(len(line)) > 0:
				L = re.split("\s+", line)	# https://pythonexamples.org/python-re-split/#2
				L.sort()
				S = set(L)
				if do_check_every_basket_is_duplic_free:
					assert len(L) == len(S)
					
				if(len(L)>0):
					retL.append(L)
					retS = retS.union(S)
	
	retO = list(retS)
	retO.sort()
	ret = { 'basketsLOT' : retL, 'itemsOT' : retO }
	return ret
	



# ###################################################################

baskets = get_list_of_list_of_strings(baskets_file, True)

print('just loaded',len(baskets['basketsLOT']),'Baskets',len(baskets['itemsOT']),'Products')


# ################################################################### section  2 - apriori starts


min_support_count = int(min_support * len(baskets['basketsLOT']))
if min_support_count==0:
	min_support_count=1
	

issubset01 = lambda ItemSet, BasketSet: int(ItemSet.issubset(BasketSet))
support_count_of_x_in_baskets =	lambda itemset, baskets: sum( [issubset01(set(itemset),set(B)) for B in baskets] )
support_of_x_in_baskets = 			lambda itemset, baskets: sum( [issubset01(set(itemset),set(B)) for B in baskets] ) / len(baskets)

Apriori_C = 					[None] * len(baskets['itemsOT'])					# List of List of Text
Apriori_support_count =	Apriori_C.copy()		# List of List of Text			doing Apriori_s = Apriori_C is a copy of pointers!!
Apriori_L = 					Apriori_C.copy()		# List of List of Text





def getJoinOf(K):

	ret = []
	assert K > 0
	# C(k) is generated from L(k-1) join L(k-1) on first k-2 items in common
	# C(6) is generated from L(5) join L(5) on first 4 items in common
	# C(2) is generated from L(1) join L(1) on first 0 items in common
	common=K-1
	for candsetLHS in Apriori_L[K]:
		#print('candsetLHS:',candsetLHS)
		assert len(candsetLHS) == K
		candsetLHS_prefix = candsetLHS[0:common]			# list[0..1] = list[0]
		#print('candsetLHS_prefix:',candsetLHS_prefix)
		for candsetRHS in Apriori_L[K]:
			#print('candsetRHS:',candsetRHS)
			assert len(candsetRHS) == K
			candsetRHS_prefix = candsetRHS[0:common]
			#print('candsetRHS_prefix:',candsetRHS_prefix)
			if candsetLHS_prefix == candsetRHS_prefix:		# [] == [] on K=1
				common_prefix = candsetLHS_prefix
				#print('common_prefix:',common_prefix)
				suffixLHS = candsetLHS[common]
				suffixRHS = candsetRHS[common]
				
				if suffixLHS < suffixRHS:
					#print('suffixLHS',suffixLHS,'suffixRHS',suffixRHS)
					ret.append(common_prefix + [suffixLHS,suffixRHS] )
	return ret
	



def populate_C_L():

	dfcols = ['K','Itemset','ItemsetK','support count','support pct','L','min_support_count','baskets']
	df = pd.DataFrame([],columns=dfcols)

	
	print('=' * 100)
	print('Cs and Ls:')

	for K in range(len(baskets['itemsOT'])):
		
		if K == 0:
			continue
			
		print('=' * 50)
		print('K:',K)
		print('=' * 50)
		
		if K == 1:
			Apriori_C[K] = [ [item] for item in baskets['itemsOT'] ]

		if K > 1:
			Apriori_C[K] = getJoinOf(K-1)
			

		# df processing:
		pp1 = [ 
					[
						itemset,
						support_count_of_x_in_baskets(itemset, baskets['basketsLOT'])
					]
					for itemset in Apriori_C[K]
		]
		
		pp2 = [ [ K, R[0], specialcomment.join(R[0]), R[1], R[1]/len(baskets['basketsLOT']), (R[1]>=min_support_count), min_support_count, len(baskets['basketsLOT']) ] for R in pp1 ]
		
		df2 = pd.DataFrame(pp2, columns = dfcols)
		
		if df2.shape[0]==0:
			break
		
		df = df.append(df2,ignore_index=True)		# ignore_index=False (default) : avrai idex = 0,1,2 for each appended set		https://code-paper.com/python/examples-ignore-index-true-in-dataframe-append


		
		Apriori_L[K] = [ itemset for itemset in Apriori_C[K] if support_of_x_in_baskets(itemset, baskets['basketsLOT']) >= min_support ]


		print('')
		print('Apriori_C',K,':')
		print(df)

		
		dfL = df[df.L]	# filter: keep only rows having L==True
		df = dfL
		print('')
		print('Apriori_L',K,':')
		print(df)

	return df




def generate_rules(df):

	dfrcols = ['K','Itemset','perm','split','rule antec','rule consec','sup itemset','sup antec', 'confid','lift']
	#dfrcols = ['K','Itemset','support count','support pct','L','min_support_count','baskets','rule antec','rule consec','confid','lift']
	dfr = pd.DataFrame([],columns=dfrcols)

	print('generating rules...')
	
	for index, row in df.iterrows():		# iterate on L(K)s		# https://code-paper.com/python/examples-for-each-row-in-dataframe
		K = row['K']
		if K > 1:
			genericL = list(range(K))
			PL = list(itertools.permutations(genericL))				# https://stackoverflow.com/questions/104420/how-to-generate-all-permutations-of-a-list
			for P in PL:
				for sh in list(range(1,K)):
					L = row['Itemset']
					iprefix=list(P[0:sh])
					isuffix=list(P[sh:K])
					vprefix = [L[index] for index in iprefix]			# https://stackoverflow.com/questions/22412509/getting-a-sublist-of-a-python-list-with-the-given-indices
					vsuffix = [L[index] for index in isuffix]

					vprefix_sorted = vprefix.copy()
					vprefix_sorted.sort()
					
					vsuffix_sorted = vsuffix.copy()
					vsuffix_sorted.sort()
					
					if vprefix_sorted == vprefix and vsuffix_sorted == vsuffix:
					
						# https://www.golinuxcloud.com/pandas-loc-vs-iloc-at-vs-iat/
						
						df_supp_itemset = df.loc[index]
						suppCount_itemset_val = df.loc[index,'support pct'] # df_supp_itemset['support count']
						
						df_supp_antec = df[df.ItemsetK == specialcomment.join(vprefix_sorted)]
						
						df_supp_consec = df[df.ItemsetK == specialcomment.join(vsuffix_sorted)]
						
						suppCount_antec_val = df_supp_antec.loc[df_supp_antec.index[0],'support pct']
						suppCount_consec_val = df_supp_consec.loc[df_supp_consec.index[0],'support pct']
						
						confidence = suppCount_itemset_val / suppCount_antec_val
						
						lift = round(confidence / suppCount_consec_val,2)
						
						# https://www.mishelper.com/data-mining/association-rules/metrics/
						
						dfr.loc[len(dfr)] = [ K, L, P, sh, vprefix, vsuffix, suppCount_itemset_val, suppCount_antec_val, confidence, lift]

	return dfr
	

df = populate_C_L()
dfr = generate_rules(df)

print('')
print('rules:')
print(dfr)
print("="* 50)
print('dfr_high_confid:')
dfr_high_confid = dfr[dfr.confid >= min_confid]
print(dfr_high_confid)
print("="* 50)
print('dfr_high_confid_high_lift:')
dfr_high_confid_high_lift = dfr_high_confid[dfr_high_confid.lift >= min_lift]
print(dfr_high_confid_high_lift)




# Consider Rule 2: {Oranges} -> {Apples}. Lift answers the question: Are customers that buy oranges more likely to buy apples than the average customer? 
# We already know that 75% of the customers who bought oranges also bought apples (this is the confidence of the rule). 
# We also know that, in general, 60% of all of the customers bought apples (this is the support of {Apples}). 
# So the answer is, yes… customers that buy oranges are more likely to buy apples than the average customer. How much more likely? 
# To figure that out you do .75 / .60 = 1.25. This is gives you the lift value of the rule: 1.25

# To calculate lift we took the confidence of the rule and divided it by the support of the RHS. If the lift value is above 1, it basically means the rule may be useful. 
# If the value is one or below, it means the rule is not very useful. 

