BEGIN { FS="\t"; sep="\t" }
# xline	linesq	hex	dec	char	class	class2	prev	xline	linesq	hex	dec	char	class	class2	next	xline	linesq	hex	dec	char	class	class2
# 000000	0	20	32	 	blank	0x20	prev:	NIL							next:	000000	1	0d	13	N/P	cntrl	0x0d
NR==2 {
	S7	= ($6  =="punct") ? ("Px" $3) : $7
	predecessor_and_curr_class2["[*]" sep S7] ++
}
NR>=3 {
	S7	= ($6  =="punct") ? ("Px" $3) : $7
	S15	= ($14=="punct") ? ("Px" $11) : $15
	curr=S7
	predecessor_and_curr_class2[S15 sep S7] ++
}
END {
	predecessor_and_curr_class2[curr sep "[*]"] ++
	print "@startuml"
	for(c in predecessor_and_curr_class2) {
		split(c,a,sep)
		printf("%s --> %s : %d\n",a[1],a[2],predecessor_and_curr_class2[c])
	}
	print "@enduml"
}
