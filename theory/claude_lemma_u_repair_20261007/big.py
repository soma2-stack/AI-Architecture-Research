"""Counting-order family (all nonzero characters of F_2^r), a=gH=1, contrast b=p.
Cached float32 atoms; top singular value of the protected capture block by Lanczos (svds)."""
import os
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"): os.environ[v]="8"
import numpy as np, sys, time
from scipy.sparse.linalg import svds
def prot_atoms(r, p, B=256):
    N = 2**r; R = N-1; x = np.arange(N, dtype=np.int64)
    A = np.empty((R, N), dtype=np.float32); carry = np.ones(N)
    for s in range(1, R+1, B):
        l = np.arange(s, min(s+B, R+1), dtype=np.int64)
        chi = 1.0 - 2.0*(np.bitwise_count(np.bitwise_and.outer(l, x)) & 1)
        U = np.cumprod((1-p) + p*chi, axis=0) * carry
        carry = U[-1].copy()
        A[s-1:s-1+len(l)] = (U - U.mean(axis=1, keepdims=True)) / np.sqrt(N)
    return A
for r, p in [(int(a), float(b)) for a, b in (arg.split(':') for arg in sys.argv[1:])]:
    t = time.time(); A = prot_atoms(r, p)
    s = svds(A, k=1, return_singular_vectors=False, tol=1e-6)[0]
    print(f"r={r} R={2**r-1} b=p={p}: ||P A_cap|| = {s:.5f}  ||U_prot|| (a gH=1) = {np.sqrt(2)*s:.5f}  ({time.time()-t:.0f}s)", flush=True)
    del A
