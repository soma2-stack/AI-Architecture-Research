"""History simulator + exact past-credit operator for the selected R block.

Exact reduction used (verified in run): every history here applies UNIFORM (or zero)
input to the source block, so h_src,t = sigma_t 1_l exactly (bitwise). Then
  B_T K = sum_s sigma_{s-1} Phi(T,s) G_s E (K 1_l),
  ||B_T||op (Frobenius->l2) = sqrt(l) * ||M_T||op,
  M_T v = sum_s sigma_{s-1} Phi(T,s) G_s E v,   v in R^(k-1) (selected rows 1..k-1),
  Phi(T,s) = G_T R ... G_{s+1} R.
Normalized worst-case past credit (PROOF eq. 13): C = (a/n) sqrt(l) ||M_T||op.
Concrete legal query credit: C_Q = (1/n) sqrt(l) ||M_T^* (A_1^T...A_L^T q)||,
  A_j = G_fut,j R, q = 1/sqrt(n)  (w_R/beta_loss = 1/n).
"""
import math
import numpy as np


class Sim:
    def __init__(self, M, hstar, policy, T, ckpt=400, track_probes=None):
        self.M, self.hstar, self.policy, self.T, self.C = M, hstar, policy, T, ckpt
        n, k = M.n, M.k
        self.sig = np.zeros(T + 1)
        self.maxg = np.zeros(T + 1)
        self.maxg_sel = np.zeros(T + 1)
        self.dev = np.zeros(T + 1)       # ||h_t - h*||
        self.xnorm2 = np.zeros(T + 1)
        self.ck = {}
        h = np.zeros(n)
        self.ck[0] = h.copy()
        self.dev[0] = np.linalg.norm(hstar)
        src_spread = 0.0
        for t in range(1, T + 1):
            h, x2 = self._step(t, h)
            self.xnorm2[t] = x2
            self.sig[t] = h[k]
            if t % 997 == 0 or t == T:
                src_spread = max(src_spread, float(h[k:].max() - h[k:].min()))
            g = 1.0 - h * h
            self.maxg[t] = g.max()
            self.maxg_sel[t] = g[1:k].max()
            self.dev[t] = np.linalg.norm(h - hstar)
            if t % ckpt == 0:
                self.ck[t] = h.copy()
        self.hT = h
        self.energy = float(self.xnorm2.sum())
        self.src_spread = src_spread
        # analytic upper bound: ||M_T|| <= sum_s |sig_{s-1}| maxg_sel_s prod_{t>s} a*maxg_t
        Ub = 0.0
        for t in range(1, T + 1):
            Ub = M.a * self.maxg[t] * Ub + abs(self.sig[t - 1]) * self.maxg_sel[t]
        self.upper_M = Ub

    def _step(self, t, h):
        M = self.M
        pre = M.R(h) + M.b0
        x = self.policy(t, h, pre)
        if x is None:
            return np.tanh(pre), 0.0
        if isinstance(x, tuple):
            idx, vals = x
            pre[idx] += vals
            return np.tanh(pre), float(np.dot(vals, vals))
        return np.tanh(pre + x), float(x @ x)

    def _segment(self, j):
        """states h_t for t in (jC, min((j+1)C,T)], recomputed from checkpoint."""
        t0 = j * self.C
        t1 = min(t0 + self.C, self.T)
        h = self.ck[t0].copy()
        out = np.empty((t1 - t0, self.M.n))
        for i, t in enumerate(range(t0 + 1, t1 + 1)):
            h, _ = self._step(t, h)
            out[i] = h
        return t0, t1, out

    def forward(self, V):
        """M_T V for V of shape (p, k-1) -> (p, n)."""
        M = self.M
        k = M.k
        V = np.atleast_2d(V)
        Z = np.zeros((V.shape[0], M.n))
        nseg = (self.T + self.C - 1) // self.C
        for j in range(nseg):
            t0, t1, H = self._segment(j)
            for i, t in enumerate(range(t0 + 1, t1 + 1)):
                g = 1.0 - H[i] * H[i]
                Z = M.R(Z)
                Z[:, 1:k] += self.sig[t - 1] * V
                Z *= g
        return Z

    def adjoint(self, Y):
        """M_T^* Y for Y of shape (p, n) -> (p, k-1)."""
        M = self.M
        k = M.k
        Y = np.atleast_2d(Y)
        mu = Y.copy()
        out = np.zeros((Y.shape[0], k - 1))
        nseg = (self.T + self.C - 1) // self.C
        for j in reversed(range(nseg)):
            t0, t1, H = self._segment(j)
            for i in reversed(range(t1 - t0)):
                t = t0 + 1 + i
                g = 1.0 - H[i] * H[i]
                gm = mu * g
                out += self.sig[t - 1] * gm[:, 1:k]
                mu = M.RT(gm)
        return out

    def opnorm(self, v0=None, iters=30, tol=1e-7, block=2, seed=0):
        """||M_T||op by block power iteration on M^*M (Rayleigh-Ritz on the block)."""
        rng = np.random.default_rng(seed)
        k = self.M.k
        V = rng.normal(size=(block, k - 1))
        if v0 is not None:
            V[0] = v0
        V, _ = np.linalg.qr(V.T)
        V = V.T
        prev = 0.0
        hist = []
        for it in range(iters):
            Z = self.forward(V)
            W = self.adjoint(Z)                     # rows = M^*M v_i
            # Rayleigh-Ritz
            Gm = V @ W.T
            Gm = 0.5 * (Gm + Gm.T)
            ev, evec = np.linalg.eigh(Gm)
            top = math.sqrt(max(ev[-1], 0.0))
            hist.append(top)
            Q, _ = np.linalg.qr(W.T)
            V = (Q @ np.eye(Q.shape[1])).T
            # rotate so first row is best Ritz vector direction next time
            if abs(top - prev) <= tol * top:
                break
            prev = top
        # final lower bound from best Ritz vector
        return top, hist

    # ---------------- legal queries -------------------------------------
    def query_adjoint(self, gates):
        """xi*beta_loss = A_1^T ... A_L^T q, A_j = G_j R, gates[j-1]=diag of G_j."""
        M = self.M
        lam = np.full(M.n, 1.0 / math.sqrt(M.n))
        for g in reversed(gates):
            lam = M.RT(g * lam)
        return lam

    def query_credit(self, gates):
        M = self.M
        y = self.query_adjoint(gates)
        w = self.adjoint(y)[0]
        return math.sqrt(M.l) / M.n * np.linalg.norm(w), y


GLO = 1.0 - math.tanh(0.75) ** 2     # gate at preactivation 3/4
GHI = 1.0 - math.tanh(0.25) ** 2     # gate at preactivation 1/4


def credit_from_M(M, normM):
    return M.a / M.n * math.sqrt(M.l) * normM
