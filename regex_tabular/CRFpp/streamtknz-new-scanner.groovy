// create after reading https://stackoverflow.com/questions/1187704/java-io-streamtokenizer-tt-number-floating-or-integer
// "StreamTokenizer is too old".

assert args.size()==1

String infilename= args[0]

class Xscanner {
	
	Scanner sc
	int inline_token_sn
	int lineno
	
	Xscanner(String line, int lineno_) {
		inline_token_sn=0
		lineno=lineno_
		sc= new Scanner(line)	//https://docs.oracle.com/javase/1.5.0/docs/api/java/util/Scanner.html
	}
	Xscanner() {}
	
	String safeprint(String scnext) {
		int stkzttype = (int)scnext[0]
		return stkzttype>=32 && stkzttype<255 ? sprintf("%c",stkzttype) : "N/P"
	}
	void xprint(List L) {
		if(L==null) { println(["lineno","LN_TK_SN","tkcode","tkval"].join("\t")); return }		// print headers
		assert L.size()==2
		println( ([lineno, inline_token_sn]+L).join("\t"))
	}
	void consume() {
		/*if(sc.hasNextLong()) {			String scnext = sc.nextLong()			xprint(["TT_NUM",	scnext])} else */
		if(sc.hasNextDouble()) {
			xprint(["TT_NUM",	sc.nextDouble()])
		} else {
			String scnext = sc.next()
			if(scnext.size()>1) {
				xprint(["TT_WORD",	scnext])
			} else {
				int stkzttype = (int)scnext[0]
				xprint(["ASCII"+stkzttype,	safeprint(scnext)])
			}
		}
		inline_token_sn++
	}
}

new Xscanner().xprint()
int lineno
new File(infilename).eachLine("UTF-8") { line ->
	Xscanner p = new Xscanner(line,lineno++)
	while(p.sc.hasNext())
		p.consume()
	p.xprint(["TT_EOL",		"N/P"])
}
