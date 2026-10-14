"""Exact frozen reference model R0 = diag(aO, delta I_l) of the original contract.

Memory coordinates 0..k-1, source k..n-1.  O = U P U with
  U = I - gamma w w^T, w = e0 - 1_k/sqrt(k), gamma = 1/(1-1/sqrt(k)),
  P = P_d (+) I_(k-d), (P x)_j = x_(j-1) for 1<=j<=d-1, (P x)_0 = x_(d-1).
All operators are applied matrix-free in O(n).
"""
import math
import numpy as np


class Frozen:
    def __init__(self, n):
        self.n = n
        self.k = n // 2
        self.l = n - self.k
        self.d = n // 4
        self.r = self.k - 1
        self.a = 1.0 - 1.0 / n
        self.delta = 1.0 / (100.0 * n)
        self.b0 = 0.05
        k = self.k
        self.gamma = 1.0 / (1.0 - 1.0 / math.sqrt(k))
        self.w = -np.ones(k) / math.sqrt(k)
        self.w[0] += 1.0
        # source fixed point sigma = tanh(delta sigma + b0)
        s = 0.05
        for _ in range(200):
            s = math.tanh(self.delta * s + self.b0)
        self.sigma = s

    # --- memory operators -------------------------------------------------
    def U(self, x):
        return x - self.gamma * self.w * (self.w @ x)

    def P(self, x):
        d = self.d
        y = x.copy()
        y[1:d] = x[0:d - 1]
        y[0] = x[d - 1]
        return y

    def PT(self, x):
        d = self.d
        y = x.copy()
        y[0:d - 1] = x[1:d]
        y[d - 1] = x[0]
        return y

    def O(self, x):
        return self.U(self.P(self.U(x)))

    def OT(self, x):
        return self.U(self.PT(self.U(x)))

    # --- full reference matrix R0 ----------------------------------------
    def R0(self, h):
        k = self.k
        out = np.empty_like(h)
        out[:k] = self.a * self.O(h[:k])
        out[k:] = self.delta * h[k:]
        return out

    def R0T(self, h):
        k = self.k
        out = np.empty_like(h)
        out[:k] = self.a * self.OT(h[:k])
        out[k:] = self.delta * h[k:]
        return out

    def dense_O(self):
        k = self.k
        M = np.zeros((k, k))
        for j in range(k):
            e = np.zeros(k)
            e[j] = 1.0
            M[:, j] = self.O(e)
        return M
