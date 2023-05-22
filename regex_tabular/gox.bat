rem gox.bat
# from
# M:\DEV\A-MOSCATELLI-WIKI\regex-tabulardata
# run:
set infile="CFTC Commitments of Traders Long Report - AG (Combined) - Copy.txt"
certutil %infile% | gawk.exe -f awk-certutil-hexdump-extract.awk | gawk.exe -f awk-certutil-hexdump-add-ctx.awk | gawk.exe -f awk-certutil-hexdump-stats.awk

