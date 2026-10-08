"""Certified lower bound (Prop. L2 of PROOF.md) for the counting family at contrast b=p, a=gH=1:
||P A_cap|| >= ||M_[i0,r]||^{1/2} - eta(i0,r),  eta^2 = 2 sum_{j=i0}^r [2^-j q^2/(1-q^2) + 2^(j-1) q^(2^(j-1))],
M_ii' = 1/2 2^{-|i-i'|/2}(1-2^{-min(i,i')}).  Reports the smallest r with sqrt2*bound > 2."""
import numpy as np
def Mnorm(i0, r):
    i = np.arange(i0, r+1); I, J = np.meshgrid(i, i, indexing='ij')
    return np.linalg.eigvalsh(0.5*2.0**(-np.abs(I-J)/2)*(1-2.0**(-np.minimum(I, J))))[-1]
def eta(p, i0, r):
    q = 1-2*p; j = np.arange(i0, r+1)
    with np.errstate(under='ignore'):
        t2 = np.exp(2.0**(j-1)*np.log(q)) if q > 0 else np.zeros_like(j, dtype=float)
    return np.sqrt(2*np.sum(2.0**(-j)*q*q/(1-q*q) + 2.0**(j-1)*t2))
for p in [0.2, 0.05, 0.0025]:
    found = None
    for r in range(4, 80):
        best = max((np.sqrt(Mnorm(i0, r)) - eta(p, i0, r), i0) for i0 in range(2, r+1))
        if np.sqrt(2)*best[0] > 2: found = (r, best); break
    r, (v, i0) = found
    print(f"b=p={p}: certified at r={r} (R=2^{r}-1), i0={i0}: ||P A_cap|| >= {v:.4f}, ||U_prot|| >= {np.sqrt(2)*v:.4f} > 2")
