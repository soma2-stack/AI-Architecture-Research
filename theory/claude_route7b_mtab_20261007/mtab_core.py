"""MTAB exact survivor-side operator and width certificates (finite computations, not proofs).

Legal survivor profiles: phi_c(t) = prod_{r>t} a*g_c(r), gates g_c(r) in [gL, gH] (public).
Protected class content per donor column (normal form):  x = C^{-1/2} P0 Phi y,
P0 = zero-sum projection on the C equal classes.  Atoms a_t = C^{-1/2} P0 phi(t).
Theorem Gamma: D - q <= (gamma * Lambda/s)^2 with gamma = ||A|| * max_t ||W a_t||_1 for
any factorisation; for an orthonormal basis Q of the zero-sum space, gamma = max_t ||Q a_t||_1.
"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(v, "8")
import numpy as np

GL, GH, A = 0.995, 1.0, 1.0 - 1e-4

def profiles_from_gates(G, a=A):
    """G: C x N gates (time r=1..N). Returns Phi: C x N with Phi[:, t-1] = prod_{r>t} a g(r), t=1..N."""
    logg = np.log(a * G)
    suffix = np.cumsum(logg[:, ::-1], axis=1)[:, ::-1]        # sum_{r>=t}
    Phi = np.exp(np.concatenate([suffix[:, 1:], np.zeros((G.shape[0], 1))], axis=1))
    return Phi

def atoms(Phi):
    C = Phi.shape[0]
    X = Phi - Phi.mean(axis=0, keepdims=True)
    return X / np.sqrt(C)                     # C x T, columns a_t (zero-sum)

def haar_basis(C):
    """Orthonormal Haar basis of the zero-sum subspace of R^C (C = 2^r), rows."""
    r = int(round(np.log2(C))); assert 2**r == C
    rows = []
    for l in range(1, r+1):
        s = 2**l
        for i in range(C // s):
            h = np.zeros(C); h[i*s:i*s+s//2] = 1; h[i*s+s//2:(i+1)*s] = -1
            rows.append(h / np.sqrt(s))
    return np.array(rows)

def gamma_basis(At, Q):
    return np.abs(Q @ At).sum(axis=0).max()

def gamma_haar_order(At, order):
    H = haar_basis(At.shape[0])
    return gamma_basis(At[order], H)

def crossing_orders(Phi, nlev=400):
    """Number of distinct level orders sigma_lambda (sort classes by first passage tau_c(lambda))."""
    lams = (np.arange(nlev) + 0.5) / nlev
    seen = []; mass = {}
    for lam in lams:
        above = Phi > lam
        tau = np.where(above.any(axis=1), above.argmax(axis=1), Phi.shape[1] + 1)
        key = tuple(np.argsort(tau, kind="stable"))
        # treat orders as the same if one is consistent with the other (ties); use ranks with ties
        ranks = tuple(np.unique(tau, return_inverse=True)[1])
        mass[ranks] = mass.get(ranks, 0) + 1.0 / nlev
    # merge level patterns that are refinements-compatible is hard; report raw count and sum mu^{2/3}
    mus = np.array(list(mass.values()))
    return len(mus), float((mus**(2/3)).sum()**3)

def optimize_basis(At, Q0, iters=600, beta=40.0, eta=1e-6, lr=0.05, seed=0):
    """Heuristic: minimise max_t ||Q a_t||_1 over orthogonal Q (rows span zero-sum space).
    Works in coordinates of Q0 (orthonormal rows); returns best rigorous value found."""
    B = Q0 @ At                                  # coords, d x T
    d = B.shape[0]; R = np.eye(d); best = np.abs(B).sum(0).max(); bestR = R.copy()
    for it in range(iters):
        Z = R @ B
        s = np.sqrt(Z**2 + eta); l1 = s.sum(0)
        w = np.exp(beta * (l1 - l1.max())); w /= w.sum()
        Gz = (Z / s) * w                         # d x T
        G = Gz @ B.T                             # dL/dR
        S = G @ R.T - R @ G.T                    # skew
        step = lr / (np.abs(S).max() + 1e-12)
        # Cayley retraction
        Iden = np.eye(d)
        R = np.linalg.solve(Iden + 0.5 * step * S, (Iden - 0.5 * step * S) @ R)
        val = np.abs(R @ B).sum(0).max()
        if val < best: best, bestR = val, R.copy()
    return best, bestR @ Q0
