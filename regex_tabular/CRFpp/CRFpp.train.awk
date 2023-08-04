#CRFpp.train.awk
BEGIN {FS="\t"; OFS="\t"}

# input = tsv1 :
# $1			$2				$3				$4					$5
#	lineno	LN_TK_SN		tkcode			tkval					TrainingLabel
#	1			0					TT_EOL			N/P					TT_EOL
#	2			0					TT_WORD		WHEAT-SRW		/PRODUCT_NAME
#	2			1					ASCII45		-						ASCII45
#	2			2					TT_WORD		CHICAGO			TT_WORD

# REQM1 : headers must be removed
NR==1 {next}
{ curr=$3 }
# REQM2 : sequences must be separated by an empty line
# REQM4 : every sequence must start with line number = 0

curr == "TT_EOL" && prev == "TT_EOL" { print ""; BASE=$1}

{
	REL_NR=$1-BASE
	#lineno=$1
	# REQM3 : first col = the token, second col = the token semantic level 1, the token semantic level 2, etc. last column = the supervised training tag
	#old print $4, $2, $5
	print $4, $3, $2, REL_NR, $5
	# REQM2 : sequences must be separated by an empty line
	prev=$3
}


# output:
#	tkval
# tkcode
#	LN_TK_SN
# lineno
# RELNR = lineno that is re-set on every sequence
# TrainingLabel


#other example templates:

#		./basenp/
#Rockwell NNP B
#International NNP I
#Corp. NNP I

#		./seg/
#よ	h	I
#っ	h	I
#て	h	I


#	lineno	LN_TK_SN	tkcode	tkval	TrainingLabel
#	1	0	TT_EOL	N/P	TT_EOL
#	2	0	TT_WORD	WHEAT-SRW	/PRODUCT_NAME
#	2	1	ASCII45	-	ASCII45
#	2	2	TT_WORD	CHICAGO	TT_WORD

#	tkval			col 1
#	LN_TK_SN		col 2
#	TrainingLabel	col 3
