"""Independent rebuild of the frozen dense tanh family (archived construction).

Written from PROOF.md section 1 and the multiharmonic PROOF.md section 2.
R = (R0 + ones/(1e8 n^3)) * a/||R0 + ones/(1e8 n^3)||_op.
"""
import numpy as np

B0 = 0.05


def build(n):
    k, d = n // 2, n // 4
    ell = n - k
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
    eR = np.linalg.norm(R - R0, 2)
    en = 4 / (1e8 * n ** 2)
    return dict(n=n, k=k, ell=ell, d=d, a=a, lam=lam, U=U, P=P, O=O, R0=R0, R=R,
                eR=eR, en=en, b=B0 * np.ones(n))


def claimed_bound(n):
    k = n // 2
    ell = n - k
    lam = 1 / (100 * n)
    en = 4 / (1e8 * n ** 2)
    return (B0 - lam) * np.sqrt(ell) - en * np.sqrt(n)


def analytic_box_R0(n):
    """Exact min over h in [-1,1]^n of ||R0 h + b0 1_n||_2 (separable after O^T)."""
    k = n // 2
    ell = n - k
    a = 1 - 1 / n
    lam = 1 / (100 * n)
    s = np.sqrt(k)
    c_big = s - 1 / (s - 1)          # entry d-1 of O^T 1_k
    c_zero = 1.0                     # entry 0
    c_rest = 1 / (s - 1)             # |entries| elsewhere (k-2 of them)
    mem2 = (max(0.0, B0 * c_big - a) ** 2 + max(0.0, B0 * c_zero - a) ** 2
            + (k - 2) * max(0.0, B0 * c_rest - a) ** 2)
    src2 = ell * (B0 - lam) ** 2
    return np.sqrt(mem2 + src2), np.sqrt(mem2), np.sqrt(src2)
