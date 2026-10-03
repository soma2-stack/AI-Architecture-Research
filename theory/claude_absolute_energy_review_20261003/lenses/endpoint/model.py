"""Independent rebuild of the frozen dense family (from PROOF.md text and the
accepted harness convention). Diagnostic only."""
import os
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(key, "4")
import numpy as np

B0 = 0.05


def build(n):
    k, d, ell = n // 2, n // 4, n - n // 2
    a = 1 - 1 / n
    lam = 1 / (100 * n)
    w = -np.ones(k) / np.sqrt(k)
    w[0] += 1
    U = np.eye(k) - 2 * np.outer(w, w) / (w @ w)
    P = np.eye(k)
    P[:d, :d] = np.roll(np.eye(d), 1, axis=0)  # (Pv)(i)=v(i-1)
    O = U @ P @ U
    R0 = np.zeros((n, n))
    R0[:k, :k] = a * O
    R0[k:, k:] = lam * np.eye(ell)
    raw = R0 + np.ones((n, n)) / (1e8 * n ** 3)
    R = raw * (a / np.linalg.norm(raw, 2))
    return dict(n=n, k=k, d=d, ell=ell, r=k - 1, a=a, lam=lam, U=U, P=P, O=O,
                R0=R0, R=R, en=4 / (1e8 * n * n), w=w)


def fixed_point(R, b, tol=1e-15, maxit=200):
    """Newton for G(h)=h-tanh(Rh+b)=0, started from damped Picard."""
    n = R.shape[0]
    h = np.zeros(n)
    for _ in range(200):
        h = np.tanh(R @ h + b)
    for it in range(maxit):
        y = R @ h + b
        t = np.tanh(y)
        G = h - t
        if np.linalg.norm(G) < tol:
            break
        J = np.eye(n) - (1 - t ** 2)[:, None] * R
        h = h - np.linalg.solve(J, G)
    res = np.linalg.norm(h - np.tanh(R @ h + b))
    return h, res
