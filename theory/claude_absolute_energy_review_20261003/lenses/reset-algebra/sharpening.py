import mpmath as mp
mp.mp.dps = 40
def parts(n):
    n_ = mp.mpf(n); k = n//2; l = n-k
    a = 1-1/n_; lam = 1/(100*n_); en = 4/(mp.mpf(10)**8*n_**2); b0 = mp.mpf(1)/20
    cstar = mp.sqrt(k) - 1/(mp.sqrt(k)-1)
    mem = max(mp.mpf(0), b0*cstar - a)
    L = (b0-lam)*mp.sqrt(l) - en*mp.sqrt(n_)
    Ls = mp.sqrt(l*(b0-lam)**2 + mem**2) - en*mp.sqrt(n_)
    return L, Ls, mem
onset = next(n for n in range(200, 5000) if parts(n)[2] > 0)
print("first n with memory-block contribution (b0*c* > a):", onset)
for n in (200, 256, 400, 806, 1000, 2000, 10**6, 10**9):
    L, Ls, mem = parts(n)
    print(n, "L_n=", mp.nstr(L, 12), " sharpened=", mp.nstr(Ls, 12), " b0sqrt(n)-1/sqrt2=", mp.nstr(mp.sqrt(n)/20-1/mp.sqrt(2), 12),
          " b0 sqrt(n)=", mp.nstr(mp.sqrt(n)/20, 12), " ratio sharpened/L_n=", mp.nstr(Ls/L, 8))
# sharp emptiness threshold vs claimed for some R
for Rb in (1, 10, 100, 1000):
    # smallest n with sharpened bound > R  (class empty), and largest n with b0 sqrt(n) <= R (class nonempty via T=1)
    lo, hi = 200, 10**12
    while lo < hi:
        mid = (lo+hi)//2
        if parts(mid)[1] > Rb: hi = mid
        else: lo = mid+1
    print(f"R={Rb}: claimed empty for n>={mp.nstr(mp.mpf(200000000)/249001*Rb**2, 12)}; sharpened empty for n>={lo}; "
          f"nonempty (x_1=-b) for n<={int(400*Rb**2)}; ratio claimed/sharp={mp.nstr(mp.mpf(200000000)/249001*Rb**2/lo, 6)}")
