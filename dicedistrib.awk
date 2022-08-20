# this is dicedistrib.awk
# example - approximating normal distrib


# https://www.gnu.org/software/gawk/manual/html_node/String-Functions.html

# https://www.gnu.org/software/gawk/manual/html_node/Arrays.html

BEGIN {
                FS="\t"
                OFS="\t"
}
step==2 {
                init = $0
                out = init
                for(dx=2;dx<=d;dx++) {
                                init = init/6
                                out = out FS int(init)
                }
                print out
                #when d=3: print $0, int($0/6), int($0/6/6)
}
step==3 {
                split($0, a, FS)
                out = a[1]%6 +1
                for(dx=2;dx<=d;dx++) {
                                out = out FS (a[dx]%6 +1)
                }
                print out
                #when d=3: print $1%6+1, $2%6+1, $3%6+1
}
step==4 {
                split($0, a, FS)
                cumul = a[1]
                for(dx=2;dx<=d;dx++) {
                                cumul += a[dx]
                }
                print cumul
                #when d=3: print $1 + $2 + $3
}
step==5 {
                h[$0]++
}
END {
                if(step==1) {
                                for(i=0;i< 6^d;i++) print i                               # with d=6: 0..46655
                }
                if(step==5) {
                                # for(i in h) { print i, h[i] } # ...unsorted
                                print "for scatter chart:"
                                print "sum","freq"
                                for(i in h) { hk[++x]=i }
                                n = asort(hk, dest)
                                for (i=1;i<=n;i++) { print dest[i], h[dest[i]] }
                }
}