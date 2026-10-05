"""Independent O(n)-per-step simulator of the frozen hard dense family.

Written from the model statement only (PROOF.md section 1 + harness R recipe):
  k=n//2, l=n-k, d=n//4, a=1-1/n, lam=1/(100n), b0=1/20,
  U=I-2ww^T/(w^Tw), w=e0-1_k/sqrt(k), P=cyclic shift on coords 0..d-1, O=UPU,
  R0=diag(aO, lam I_l), R=(R0+ones/(1e8 n^3))*a/||.||op   (archived recipe).
Physical coords: 0 = protected, 1..k-1 = selected memory, k..n-1 = source.
"""
import math
import numpy as np
from scipy.optimize import brentq


class Model:
    def __init__(self, n, dense=True):
        self.n = n
        k = n // 2
        self.k, self.l, self.r, self.d = k, n - k, k - 1, n // 4
        self.a = 1.0 - 1.0 / n
        self.lam = 1.0 / (100.0 * n)
        self.b0 = 0.05
        self.tau = 1.0 / math.sqrt(k)
        self.cH = 1.0 / (1.0 - self.tau)
        self.eps = 1.0 / (1e8 * n ** 3) if dense else 0.0
        # ||R0+eps*11^T||op^2 = a^2 + eps*a*k + O(eps^2 n^2): degenerate first-order
        # perturbation of the a^2 eigenspace; verified against dense SVD at small n.
        self.c = self.a / math.sqrt(self.a ** 2 + self.eps * self.a * k) if dense else 1.0
        self.A = self.c * self.a          # effective memory scale
        self.Lam = self.c * self.lam      # effective source scale
        self.ce = self.c * self.eps       # effective rank-one coefficient

    # ---- structured orthogonal O=UPU and transpose -------------------------
    def _U(self, v):
        # acts on the LAST axis (rows of a (p,k) block are independent vectors)
        wv = v[..., 0] - self.tau * v.sum(axis=-1)
        s = self.cH * wv
        u = v + (s * self.tau)[..., None] if v.ndim > 1 else v + s * self.tau
        u[..., 0] -= s
        return u

    def O(self, v):
        d = self.d
        u = self._U(v)
        u[..., :d] = np.roll(u[..., :d], 1, axis=-1)  # (Pv)(i)=v(i-1)
        return self._U(u)

    def OT(self, v):
        d = self.d
        u = self._U(v)
        u[..., :d] = np.roll(u[..., :d], -1, axis=-1)
        return self._U(u)

    def R(self, v):
        k = self.k
        out = np.empty_like(v)
        out[..., :k] = self.A * self.O(v[..., :k])
        out[..., k:] = self.Lam * v[..., k:]
        out += (self.ce * v.sum(axis=-1))[..., None] if v.ndim > 1 else self.ce * v.sum()
        return out

    def RT(self, v):
        k = self.k
        out = np.empty_like(v)
        out[..., :k] = self.A * self.OT(v[..., :k])
        out[..., k:] = self.Lam * v[..., k:]
        out += (self.ce * v.sum(axis=-1))[..., None] if v.ndim > 1 else self.ce * v.sum()
        return out

    def dense_R(self):
        n, k, d = self.n, self.k, self.d
        w = -np.ones(k) / math.sqrt(k)
        w[0] += 1
        U = np.eye(k) - self.cH * np.outer(w, w)
        P = np.eye(k)
        P[:d, :d] = np.roll(np.eye(d), 1, axis=0)
        R0 = np.zeros((n, n))
        R0[:k, :k] = self.a * (U @ P @ U)
        R0[k:, k:] = np.eye(n - k) * self.lam
        raw = R0 + np.ones((n, n)) * self.eps
        return raw * (self.a / np.linalg.norm(raw, 2)), R0

    # ---- reduced fixed point ---------------------------------------------
    @staticmethod
    def scalar_fp(A, B):
        """unique H with H=tanh(A H+B), A<1."""
        f = lambda h: h - math.tanh(A * h + B)
        return brentq(f, -1.0, 1.0, xtol=1e-18, rtol=1e-15, maxiter=500)

    def chain(self, B, beff, H):
        """cycle coords v_1..v_{d-1} for given B via eq (3) (with A, beff)."""
        A, d = self.A, self.d
        extra = B + (beff - B) / (self.cH * self.tau)
        x = H
        for _ in range(60):
            v = np.empty(d - 1)
            cur = math.tanh(A * x + extra)
            v[0] = cur
            i = 1
            while i < d - 1:
                cur = math.tanh(A * cur + B)
                v[i] = cur
                i += 1
                if abs(cur - H) < 1e-17:
                    v[i:] = H
                    cur = H
                    break
            xn = v[-1]
            if abs(xn - x) < 1e-17:
                x = xn
                break
            x = xn
        return v

    def Phi(self, B, beff):
        A, k, d, tau, cH = self.A, self.k, self.d, self.tau, self.cH
        H = self.scalar_fp(A, B)
        v = self.chain(B, beff, H)
        S = v.sum() + (k - d) * H
        return B - beff - A * cH * tau * v[-1] + A * cH * cH * tau * tau * S, H, v

    def fixed_point(self, verbose=False):
        n, k, d = self.n, self.k, self.d
        beff = self.b0
        for it in range(4):
            g = lambda B: self.Phi(B, beff)[0]
            hi = beff
            lo = beff - 0.01
            while g(lo) > 0:
                lo -= 0.05
            Bs = brentq(g, lo, hi, xtol=1e-18, rtol=1e-15, maxiter=500)
            _, H, v = self.Phi(Bs, beff)
            z = self.scalar_fp(self.A, beff)
            s = self.scalar_fp(self.Lam, beff)
            h = np.empty(n)
            h[0] = z
            h[1:d] = v
            h[d:k] = H
            h[k:] = s
            beff_new = self.b0 + self.ce * h.sum()
            if verbose:
                print(it, Bs, H, beff_new - self.b0)
            if beff_new == beff:
                break
            beff = beff_new
        self.Bstar, self.Hstar = Bs, H
        return h

    def f(self, h, x=None):
        p = self.R(h) + self.b0
        if x is not None:
            p = p + x
        return np.tanh(p)

    def polish(self, h, iters=200):
        for _ in range(iters):
            h = self.f(h)
        return h
