# this is awk-certutil-hexdump-extract.awk
# from
# M:\DEV\A-MOSCATELLI-WIKI\regex-tabulardata
# run:
# certutil "CFTC Commitments of Traders Long Report - AG (Combined) - Copy.txt" | gawk.exe -f awk-certutil-hexdump-extract.awk > awk-certutil-hexdump-extract.out.tsv


# certutil output:
#---BEGIN---
#  000000  ...
#  01dd14
#    000000  20 0d 0a 57 48 45 41 54  2d 53 52 57 20 2d 20 43    ..WHEAT-SRW - C
#    000010  48 49 43 41 47 4f 20 42  4f 41 52 44 20 4f 46 20   HICAGO BOARD OF
#	...
#
#    01dd10  0d 0a 0d 0a                                        ....
#CertUtil: -dump command completed successfully.
#---END---

function isAlpha(ch) { return match(ch, /[[:alpha:]]/) != 0}
function isDigit(ch) { return match(ch, /[[:digit:]]/) != 0}
function isBlank(ch) { return match(ch, /[[:blank:]]/) != 0}
function isPunct(ch) { return match(ch, /[[:punct:]]/) != 0}
BEGIN {	print "xline" 		"\t"	"linesq"		"\t"	"hex"	 "\t"		"dec"	 	"\t"		"char" 	"\t"	"class"	}
NR>=3 && $1 != "CertUtil:" {
	S0b = substr($0,13,16*3)
	n=split(S0b, a)
	xline=$1
	for(i=1;i<=n;i++) {
		x=a[i]
		dec = strtonum("0x" x)
		ch = sprintf("%c",dec)
		if(isAlpha(ch)) class="alpha"; else 
			if(isDigit(ch)) class="digit"; else
				if(isBlank(ch)) class="blank"; else	# 32
					if(isPunct(ch)) class="punct"; else
						if(dec<32) class="nonPr"; else
							class="other"
		printf("%s\t%d\t%s\t%d\t%s\t%s\n", xline, i-1, x, dec, dec<32? "N/P" : ch, class)
	}
}
