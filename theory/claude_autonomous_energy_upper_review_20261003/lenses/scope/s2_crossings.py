"""Locate widths where reference min coordinate H(B*) crosses 0, enters the accepted
weak-gate deficit window n*H^2 in [1/20,1/4], and reaches m=1/50. Diagnostics only."""
import time
from s1_hstar_scan import reference
t0=time.process_time()
cache={}
def H(n):
    if n not in cache: cache[n]=reference(n)[1]
    return cache[n]
def first(pred, lo, hi):
    # smallest n in (lo,hi] with pred true, assuming monotone
    while hi-lo>1:
        mid=(lo+hi)//2
        if pred(mid): hi=mid
        else: lo=mid
    return hi
n0=first(lambda n: H(n)>0, 2000, 2500)
print("first n with H(B*)>0:", n0, H(n0-1), H(n0))
for n in range(n0-3, n0+4):
    print(n, H(n), "deficit n*H^2 =", n*H(n)**2)
nw_lo=first(lambda n: n*H(n)**2>=1/20, n0, 3000)
nw_hi=first(lambda n: n*H(n)**2>1/4, n0, 4000)
print("positive side weak-gate window (n*H^2 in [1/20,1/4]) for n in [%d,%d)"%(nw_lo,nw_hi), H(nw_lo), H(nw_hi))
nm=first(lambda n: H(n)>=1/50, 3000, 4000)
print("first n with H>=1/50:", nm, H(nm-1), H(nm))
print("CPU",time.process_time()-t0)
