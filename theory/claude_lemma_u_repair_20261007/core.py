"""Shared exact model for the Lemma U repair (finite computations, not proofs).
Sites x in F_2^r with uniform probability; inner product = mean over sites.
Capture e (time order e=1..R) has distinct nonzero Walsh label alpha_e and pointwise
multiplier a*(gbar + b*chi_e), gbar = gH - b.  Atoms (Theorem B Lemma 2):
  capture-step atom  cap_e = a(gbar+b chi_e) * prod_{e'>e} [dec * a(gbar+b chi_e')]
  ordinary atom before capture e = a*gH*cap_e ; last interval = common mode (protected part 0).
U_prot = P [cap | a gH cap]  (P = remove site mean)."""
import os
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"): os.environ.setdefault(v,"8")
import numpy as np

def chi(alpha, r):
    x = np.arange(2**r, dtype=np.int64)
    return 1.0 - 2.0*(np.bitwise_count(np.int64(alpha) & x) & 1)

def cap_atoms(alphas, r, a=1.0, gH=1.0, b=0.5, dec=1.0):
    """Columns cap_e (e in time order), scaled so Euclidean norm = mean-norm."""
    R = len(alphas); gbar = gH - b
    cols = [None]*R
    tail = np.ones(2**r)                       # prod over later captures
    for e in range(R-1, -1, -1):
        m = a*(gbar + b*chi(alphas[e], r))
        cols[e] = m*tail
        tail = dec*m*tail
    A = np.array(cols).T / np.sqrt(2**r)
    return A

def protect(A):
    return A - A.mean(axis=0, keepdims=True)

def opnorm(M):
    if min(M.shape) <= 2500:
        return np.linalg.norm(M, 2)
    G = M.T @ M if M.shape[1] <= M.shape[0] else M @ M.T
    return float(np.sqrt(np.linalg.eigvalsh(G)[-1]))

def uprot_norm(alphas, r, a=1.0, gH=1.0, b=0.5, dec=1.0):
    A = protect(cap_atoms(alphas, r, a, gH, b, dec))
    nA = opnorm(A)
    return nA*np.sqrt(1 + (a*gH)**2), nA

def counting_order_time(r):
    """Walk order (reverse time) = binary counting 1,2,3,...,2^r-1; return time order."""
    return list(range(2**r - 1, 0, -1))
