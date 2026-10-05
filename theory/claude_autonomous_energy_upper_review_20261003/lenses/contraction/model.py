"""Structured O(n) implementation of the frozen hard dense family (review only).

R0 = diag(a*O, lam*I_l), O = U P U (Householder U, cyclic shift P on first d of k).
Dense archived R = (R0 + 11^T/(1e8 n^3)) * a/||.||op.  The normalisation factor
a/||R0 + c 11^T|| differs from 1 by O(c n) ~ 1e-8/n^2 (below float64 resolution
for n>=1e4), so we apply R = R0 + c 11^T (scale factor 1 in float64) when
dense=True.  Independent of the Codex scripts.
"""
import os
for k_ in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[k_] = "1"
import numpy as np


class Model:
    def __init__(self, n, dense=True):
        self.n = n
        self.k = k = n // 2
        self.l = n - k
        self.r = k - 1
        self.d = n // 4
        self.a = 1 - 1 / n
        self.lam = 1 / (100 * n)
        self.b0 = 0.05
        self.tau = 1 / np.sqrt(k)
        w = -np.full(k, self.tau)
        w[0] += 1
        self.w = w
        self.gam = 1 / (1 - self.tau)   # 2/(w^T w)
        self.c = (1 / (1e8 * n ** 3)) if dense else 0.0
        self.dense = dense

    # ---- selected-block orthogonal map and transpose
    def O(self, v):
        w, g, d = self.w, self.gam, self.d
        u = v - g * w * (w @ v)
        u[:d] = np.roll(u[:d], 1)
        return u - g * w * (w @ u)

    def OT(self, v):
        w, g, d = self.w, self.gam, self.d
        u = v - g * w * (w @ v)
        u[:d] = np.roll(u[:d], -1)
        return u - g * w * (w @ u)

    def R(self, h):
        k = self.k
        out = np.empty_like(h)
        out[:k] = self.a * self.O(h[:k])
        out[k:] = self.lam * h[k:]
        if self.c:
            out += self.c * h.sum()
        return out

    def RT(self, y):
        k = self.k
        out = np.empty_like(y)
        out[:k] = self.a * self.OT(y[:k])
        out[k:] = self.lam * y[k:]
        if self.c:
            out += self.c * y.sum()
        return out

    def step(self, h, x=None):
        p = self.R(h) + self.b0
        if x is not None:
            p += x
        return np.tanh(p)

    def fixed_point(self, tol=1e-13, maxit=200000, h0=None, verbose=False):
        h = np.full(self.n, np.tanh(0.05)) if h0 is None else h0.copy()
        for it in range(maxit):
            nh = self.step(h)
            res = np.linalg.norm(nh - h)
            h = nh
            if res < tol:
                break
            if verbose and it % 2000 == 0:
                print(it, res, flush=True)
        self.hstar = h
        self.fp_res = res
        self.fp_it = it
        return h
