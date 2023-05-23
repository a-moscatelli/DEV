# from	M:\DEV\A-MOSCATELLI-WIKI\regex-tabulardata
# run	M:\dev\sh\make all

CFTC_COT_infile = CFTC\ Commitments\ of\ Traders\ Long\ Report\ -\ AG\ (Combined).txt
CERTUTIL_EXE = C:\Windows\System32\certutil.exe
.PHONY: all
.PHONY: clean

all: temp-cot.stats.txt temp-cot.succpreds.tsv
clean:
	del temp-cot.*

temp-cot.certutil.txt : $(CFTC_COT_infile)
	$(CERTUTIL_EXE)  "$<"  >  $@

temp-cot.extract.tsv : temp-cot.certutil.txt  awk-certutil-hexdump-extract.awk
	gawk.exe -f awk-certutil-hexdump-extract.awk  $<  >  $@

temp-cot.context.tsv : temp-cot.extract.tsv  awk-certutil-hexdump-add-ctx.awk
	gawk.exe -f awk-certutil-hexdump-add-ctx.awk  $<  >  $@

temp-cot.stats.txt : temp-cot.context.tsv  awk-certutil-hexdump-stats.awk
	gawk.exe -f awk-certutil-hexdump-stats.awk  $<  >  $@

temp-cot.succpreds.tsv : temp-cot.context.tsv  awk-certutil-hexdump-prec-succ.awk
	gawk.exe -f awk-certutil-hexdump-prec-succ.awk  $<  >  $@

# recipes are re-executed also when the awk script is updated.
