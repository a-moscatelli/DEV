BEGIN {	FS="\t"; print "class2" 	"\t"	"class2succ"	"\t"	"count"; sep=":"	}
# xline	linesq	hex	dec	char	class	class2	prev	xline	linesq	hex	dec	char	class	class2	next	xline	linesq	hex	dec	char	class	class2
# 000000	0	20	32	 	blank	0x20	prev:	NIL							next:	000000	1	0d	13	N/P	cntrl	0x0d
NR==2 {
	predecessor_and_curr_class2["START" sep $7] ++
}
NR>=3 {
	curr=$7
	predecessor_and_curr_class2[$15 sep $7] ++
}
END {
	predecessor_and_curr_class2[curr sep "END"] ++
	for(c in predecessor_and_curr_class2) {
		split(c,a,sep)
		printf("%s\t%s\t%d\n",a[1],a[2],predecessor_and_curr_class2[c])
	}
}
