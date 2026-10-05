import mpmath as mp
from fractions import Fraction as Q
mp.mp.dps=60
eps=mp.mpf(1)/1000
def Rreq39(n):
    n=mp.mpf(n); I=(eps*mp.sqrt(n)-10002*mp.log(n)-10001)/10000
    return (mp.sqrt(I)-1)/10000 if I>1 else mp.mpf(0)
def Rreq34(n):
    n=mp.mpf(n); v=(eps*mp.sqrt(n)/(mp.mpf(10)**19*mp.log(n)**mp.mpf(2.5)))**(mp.mpf(1)/3)-1
    return max(v,0)
print("sqrt(eps)/1e6 =",mp.nstr(mp.sqrt(eps)/10**6,12))
for e in [20,30,40,60,80,200,900]:
    n=mp.mpf(10)**e
    r=Rreq39(n)
    print(f"n=1e{e}: (39) R_req={mp.nstr(r,10)}  ratio R_req/n^(1/4)={mp.nstr(r/n**0.25,12)}  (34) R_req={mp.nstr(Rreq34(n),6)}  ratio34/(n^(1/6)/log^(5/6))={mp.nstr(Rreq34(n)/(n**(mp.mpf(1)/6)/mp.log(n)**(mp.mpf(5)/6)),8)}")
# where (39) becomes non-vacuous (I>1)
f=lambda x: (eps*mp.sqrt(mp.e**x)-10002*x-10001)/10000-1
x0=mp.findroot(f,60)
print("(39) non-vacuous from log n >",mp.nstr(x0,10)," n ~",mp.nstr(mp.e**x0,8))
# exact check (39) derivation: L+H > eps sqrt n with H <= X+10001 where X=10000(1+10000R)^2
# Self-consistency: at R exactly = Rreq39(n), the coarse bound bound (10002 log n + X + 10001)/sqrt n equals eps
for e in [40,80]:
    n=mp.mpf(10)**e; R=Rreq39(n); X=10000*(1+10000*R)**2
    print(f"n=1e{e}: (10002 log n + X+10001)/sqrt n / eps = {mp.nstr((10002*mp.log(n)+X+10001)/mp.sqrt(n)/eps,20)}")
# C_R <= 1e19 (1+R)^3 over a grid of R (exact-ish)
worst=0
for R in [mp.mpf(x)/100 for x in range(0,1000)]+[mp.mpf(10)**k for k in range(1,12)]:
    chi=mp.mpf(1)/50+71*R; H=mp.ceil(10000*(1+10000*R)**2)+10000
    C=2*R*101**5+40008*chi*H+2*R*(101+mp.sqrt(H))
    worst=max(worst,C/(1+R)**3)
print("max C_R/(1+R)^3 over grid =",mp.nstr(worst,10)," < 1e19:",worst<mp.mpf(10)**19)
# 2*10002^(5/2) <= 2*101^5 (term-by-term in C_R)
print("10002^2.5 =",mp.nstr(mp.mpf(10002)**2.5,12)," 101^5 =",101**5)
# sqrt(10002 log n) <= 101 (log n)^(5/2) for n>=1e6 ; trivially since log n>=13.8
# (33) onset R=1 eps=1e-3
print("(33) second term R=1:",mp.nstr((2*mp.mpf(10)**19*8/eps)**(mp.mpf(8)/3),8))
