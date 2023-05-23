# this is awk-certutil-hexdump-stats.awk
# see gox.bat

#xline	linesq	hex	dec	char	class	prev	xline	linesq	hex	dec	char	class	next	xline	linesq	hex	dec	char	class
#000000	0	20	32	 	blank	prev:	NIL						next:	000000	1	0d	13	N/P	nonPr
#000000	1	0d	13	N/P	nonPr	prev:	000000	0	20	32	 	blank	next:	000000	2	0a	10	N/P	nonPr
#...
#01dd10	2	0d	13	N/P	nonPr	prev:	01dd10	1	0a	10	N/P	nonPr	next:	01dd10	3	0a	10	N/P	nonPr
#01dd10	3	0a	10	N/P	nonPr	prev:	01dd10	2	0d	13	N/P	nonPr	next:	NIL

# the input is a tsv file, every input line is a byte, the first line is the tsv header
BEGIN {FS="\t"}
NR>1 {
	hexcode[$3]++
	chclass[$3]=$6
	chclass2[$3]=$7
	chdec[$3]=$4
	chch[$3]=$5
	classcnt[$6]++
	class2cnt[$7]++
}
END {
	print "hex"	"\t"	"dec"		"\t"	"chr"		"\t"	"class"		"\t"	"cnt"
	for(x in hexcode) {
		if(chclass[x]!="alpha" && chclass[x]!="digit" ){
			printf("%s\t%d\t%s\t%s\t%d\n", x, chdec[x], chch[x], chclass[x], hexcode[x])	# https://www.asciitable.com/
		}
	}
	print "-"
	print "total bytes [any]: " (NR-1)
	for(chc in classcnt) {
		print "total bytes class [" chc "]: " classcnt[chc]
	}
	print "-"
	for(chc in class2cnt) {
		print "total bytes class2 [" chc "]: " class2cnt[chc]
	}
	print "-"
	#print "2.1 tot [alpha]: " totAlpha
	#print "2.2 tot [digit]: " totDigit
	#print "2.3 tot [else]: " totElse
	#print "2.S tot: " (totAlpha+totDigit+totElse)
	#print "3.1 tot printable: " printable	
	#print "3.2 tot non-printable: " nonPrintable
	#print "3.S tot: " (printable+nonPrintable)
}
