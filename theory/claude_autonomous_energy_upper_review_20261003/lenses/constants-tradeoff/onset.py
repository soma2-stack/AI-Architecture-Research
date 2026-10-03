import mpmath as mp
from fractions import Fraction as Q
mp.mp.dps = 80
H = 10000*10001**2 + 10000  # R=1
LOG = mp.log(mp.mpf(10001)/10000)
def L(n): return int(mp.ceil(mp.log(100*mp.sqrt(mp.mpf(n)))/LOG))
def d0(n, a=False, coarse=False):
    if coarse: v = (L(n)+H)/mp.sqrt(mp.mpf(n))
    else: v = mp.sqrt(n-n//2)*(L(n)+H)/mp.mpf(n)
    if a: v*= (1-mp.mpf(1)/n)
    return v
def first_cross(target, **kw):
    lo, hi = 10**6, 10**40
    assert d0(lo,**kw) > target and d0(hi,**kw) <= target
    while hi-lo>1:
        mid=(lo+hi)//2
        if d0(mid,**kw)<=target: hi=mid
        else: lo=mid
    return hi
eps = mp.mpf(1)/1000
for target,name in [(eps/2,"eps/2"),(eps,"eps")]:
    for kw in [{}, {"a":True}, {"coarse":True}]:
        n1 = first_cross(target, **kw)
        # check monotonicity issue: next L-jump after n1
        Lc = L(n1)
        nj = int(mp.ceil((mp.mpf(10001)/10000)**(2*Lc) / 10**4))  # smallest n with L(n) >= Lc+1 approx
        while L(nj) <= Lc: nj += 1
        while L(nj-1) > Lc: nj -= 1
        print(f"target {name} {kw}: first n with bound<=target = {n1} ({mp.nstr(mp.mpf(n1),12)}), L={Lc}, d0(n1)={mp.nstr(d0(n1,**kw),20)}, d0(n1-1)={mp.nstr(d0(n1-1,**kw),20)}")
        print(f"   next L jump at n={mp.nstr(mp.mpf(nj),15)}: d0(nj-1)={mp.nstr(d0(nj-1,**kw),20)} d0(nj)={mp.nstr(d0(nj,**kw),20)} (jump up: {d0(nj,**kw)>d0(nj-1,**kw)}), still <= target: {d0(nj,**kw)<=target}")
# non-monotonicity measure: at a typical L jump near 1e30, relative jump up vs relative decrease per unit n
n=10**30
Lc=L(n)
nj = int(mp.ceil((mp.mpf(10001)/10000)**(2*Lc) / 10**4))
while L(nj) <= Lc: nj += 1
while L(nj-1) > Lc: nj -= 1
print("example L-jump at n=",mp.nstr(mp.mpf(nj),15)," relative change d0(nj)/d0(nj-1)-1 =", mp.nstr(d0(nj)/d0(nj-1)-1,10))
# threshold where L-jumps start to make delta0 non-monotone: need 1/(L+H) > ~1/(2n)
print("non-monotone regime starts near n ~ (L+H)/2 =", mp.nstr(mp.mpf(H)/2,6))
n=10**11
Lc=L(n); nj = int(mp.ceil((mp.mpf(10001)/10000)**(2*Lc) / 10**4))
while L(nj) <= Lc: nj += 1
while L(nj-1) > Lc: nj -= 1
print("at n~1e11 jump:", mp.nstr(d0(nj)/d0(nj-1)-1,10))
n=10**13
Lc=L(n); nj = int(mp.ceil((mp.mpf(10001)/10000)**(2*Lc) / 10**4))
while L(nj) <= Lc: nj += 1
while L(nj-1) > Lc: nj -= 1
print("at n~1e13 jump:", mp.nstr(d0(nj)/d0(nj-1)-1,10))
