"""Rigorous instance LOWER bounds ||P A_cap|| >= ||P A w||/||w|| (Rayleigh, any w) for the
counting-order family at contrast b=p (a=gH=1), streaming the atoms (no storage).
Test vector: level-constant weights from the Perron vector of the p=1/2 level matrix
M_ii' = 1/2 2^{-|i-i'|/2}(1-2^{-min}), restricted to levels >= i0."""
import os
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"): os.environ[v]="8"
import numpy as np, sys, time
def perron(r, i0):
    i = np.arange(1, r+1); I, J = np.meshgrid(i, i, indexing='ij')
    M = 0.5*2.0**(-np.abs(I-J)/2)*(1-2.0**(-np.minimum(I, J)))
    M[:i0-1, :] = 0; M[:, :i0-1] = 0
    ev, V = np.linalg.eigh(M); return np.abs(V[:, -1])
def lb(r, p, i0, B=128):
    N = 2**r; R = N-1; x = np.arange(N, dtype=np.int64); phi = perron(r, i0)
    y = np.zeros(N); carry = np.ones(N); w2 = 0.0
    for s in range(1, R+1, B):
        l = np.arange(s, min(s+B, R+1), dtype=np.int64)
        lev = np.floor(np.log2(l)).astype(int) + 1            # level of walk index k=l
        w = phi[lev-1]/np.sqrt(2.0**(lev-1)); w2 += (w*w).sum()
        chi = 1.0 - 2.0*(np.bitwise_count(np.bitwise_and.outer(l, x)) & 1)
        U = np.cumprod((1-p) + p*chi, axis=0)*carry; carry = U[-1].copy()
        y += w @ U
    y -= y.mean()
    return np.sqrt((y*y).mean()/w2)
for arg in sys.argv[1:]:
    r, p, i0 = arg.split(':'); r, p, i0 = int(r), float(p), int(i0)
    t = time.time(); v = lb(r, p, i0)
    print(f"r={r} R={2**r-1} b=p={p} i0={i0}: ||P A_cap|| >= {v:.5f}  ||U_prot|| >= {np.sqrt(2)*v:.5f}  ({time.time()-t:.0f}s)", flush=True)
