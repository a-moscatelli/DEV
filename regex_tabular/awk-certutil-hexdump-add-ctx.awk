# this is awk-certutil-hexdump-add-ctx.awk
# see gox.bat
# the purpose is to support the construction, for each char, of the list of its predecessors (char & char class) and of the list of its successors (char & char class)

#xline	linesq	hex	dec	char	class
#000000	0	20	32	 	blank
#000000	1	0d	13	N/P	nonPr
#000000	2	0a	10	N/P	nonPr

BEGIN {FS="\t";	LINE_NIL="NIL" "\t" 	"\t"	"\t"	"\t"	"\t"	"\t" }

NR==1{ HDR=$0; print HDR	"\t"	"prev"	"\t"	HDR	"\t"	"next" 	"\t"	HDR }
NR>3 {	LINE["NR-2"]=LINE["NR-1"]	}
NR>2 {	LINE["NR-1"]=LINE["NR"]	}
NR>1 {	LINE["NR"]=$0	}

NR>=4 {	print LINE["NR-1"]	"\t"	"prev:"	"\t"	LINE["NR-2"]		"\t"	"next:"	"\t"	LINE["NR"]; next}
NR==3 {	print LINE["NR-1"]	"\t"	"prev:"	"\t"	LINE_NIL			"\t"	"next:"	"\t"	LINE["NR"]; next}

END {		print LINE["NR"]		"\t"	"prev:" "\t"	LINE["NR-1"]		"\t"	"next:"	"\t"	LINE_NIL}
