
set "AWK=gawk.exe -f dicedistrib.awk -v d=3"

echo | %AWK% -v step=1 | %AWK% -v step=2 | %AWK% -v d=3 -v step=3 | %AWK% -v step=4 | %AWK% -v step=5

