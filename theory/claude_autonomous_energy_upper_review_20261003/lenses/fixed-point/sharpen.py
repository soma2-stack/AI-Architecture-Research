"""How far does the SAME analytic IVT argument reach? (exact-form upper bound of Phi(B_m)).
U(k,n,m0) = B_m - b0 + cH^2*( m0*(k-1)/k + (1-m0)/(m0^2 k) ), B_m = atanh(m0)-a m0.
Negative => argument proves h*_0 >= m0 on R0 at that width. mpmath, 40 digits."""
import mpmath as mp
mp.mp.dps = 40
def U(n, m0):
    k = n // 2; a = 1 - mp.mpf(1)/n; tau = 1/mp.sqrt(k); cH = 1/(1-tau)
    Bm = mp.atanh(m0) - a*m0
    return Bm - mp.mpf(1)/20 + cH**2*(m0*(k-1)/k + (1-m0)/(m0**2*k))
m0 = mp.mpf(1)/40
# smallest n (even/odd both) with U<0 for m0=1/40
lo, hi = 1000, 10**6
for n in range(1000, 10**6, 1000):
    if U(n, m0) < 0 and U(n+1, m0) < 0:
        break
first = n
for n in range(first-1000, first+1):
    if U(n, m0) < 0 and all(U(j, m0) < 0 for j in range(n, n+4)):
        first = n; break
print('m0=1/40: analytic argument closes from about n =', first, ' U there =', mp.nstr(U(first, m0), 6))
print('U(1e6,1/40)=', mp.nstr(U(10**6, m0), 8), ' vs proof bound -0.021649')
# best m0 provable at n=1e6 by the same chain
lo, hi = mp.mpf('0.02'), mp.mpf('0.0499')
for _ in range(80):
    mid = (lo+hi)/2
    if U(10**6, mid) < 0: lo = mid
    else: hi = mid
print('largest m0 provable by same argument at n=1e6:', mp.nstr(lo, 8))
for n in (10**7, 10**8, 10**10):
    lo, hi = mp.mpf('0.02'), mp.mpf('0.04996')
    for _ in range(80):
        mid = (lo+hi)/2
        if U(n, mid) < 0: lo = mid
        else: hi = mid
    print('n=%g largest provable m0:' % n, mp.nstr(lo, 8))
