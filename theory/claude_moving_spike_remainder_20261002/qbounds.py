"""Rigorous moving-spike query bracket (Theorem Q) and legal lower bounds, plus Codex chart reconstruction.

UB(dC, ds) = scale * sup_{L>=1} [ beta0 lam^L ||dC^T theta_{p(L)}|| + R_L * max(||dC||_op, |ds|) ]
R_L        = a beta0 lam^(L-1) * sum_{t=1..L} omega_hat(p(t-1))          (Theorem R1, visible frame)
LB_spike   = scale * max_L beta0 lam^L ||dC^T theta_{p(L)}||               (exact legal constant-gate spikes)
LB_1step   = scale * max over vertices g of the exact one-step distance    (legal, optimised -> lower bound)
"""
import math
import numpy as np
import torch
from core import build, node, G_HI, G_LO, S_G, EPS

CODEX = '../codex_two_pulse_corotating_20261002/'


def omega_hat(S, p):
    k = S['k']
    return S_G * math.sqrt(1 - 1 / k) if p == 0 else 2 * S['ck'] * S_G * math.sqrt(1 - 2 / k)


def remainder_budget(S, Lmax):
    """R_L for L = 1..Lmax (triangle), capped by the trivial ||X_L|| + sigma ||theta|| <= 2 beta0 lam^L."""
    lam, a, b0, d = S['lam'], S['a'], S['beta0'], S['d']
    R = np.zeros(Lmax + 1); acc = 0.0
    for L in range(1, Lmax + 1):
        acc += omega_hat(S, node(L - 1, d))
        R[L] = min(a * b0 * lam ** (L - 1) * acc, 2 * b0 * lam ** L)
    return R


class Bracket:
    def __init__(self, S, Lmax=None):
        self.S = S; d = S['d']
        self.Lmax = Lmax or 4 * d
        self.R = torch.tensor(remainder_budget(S, self.Lmax))
        Ls = np.arange(1, self.Lmax + 1)
        self.w = torch.tensor(S['beta0'] * S['lam'] ** Ls)
        self.nodes = torch.tensor([node(L, d) for L in Ls])
        self.Th = torch.tensor(S['Theta'])
        # tail beyond Lmax: lam^L L decreasing -> bounded by L = Lmax+1 value with max row
        Lt = self.Lmax + 1
        acc = sum(omega_hat(S, node(t - 1, d)) for t in range(1, Lt + 1))
        self.tail_w = S['beta0'] * S['lam'] ** Lt
        self.tail_R = min(S['a'] * S['beta0'] * S['lam'] ** (Lt - 1) * acc, 2 * S['beta0'] * S['lam'] ** Lt)

    def rows(self, dC):
        return (dC.T @ self.Th).norm(dim=0)          # ||dC^T theta_p||, p = 0..d-1

    def ub(self, dC, ds, parts=False):
        rows = self.rows(dC)
        M = torch.maximum(torch.linalg.matrix_norm(dC, ord=2), torch.abs(torch.as_tensor(ds)))
        terms = self.w * rows[self.nodes] + self.R[1:] * M
        tail = self.tail_w * rows.max() + self.tail_R * M
        val = self.S['scale'] * torch.maximum(terms.max(), tail)
        if parts:
            i = int(torch.argmax(terms))
            return val, dict(L_star=i + 1, spike_part=float(self.S['scale'] * self.w[i] * rows[self.nodes[i]]),
                             rem_part=float(self.S['scale'] * self.R[i + 1] * M), M_opds=float(M),
                             tail=float(self.S['scale'] * tail))
        return val

    def lb_spike(self, dC):
        rows = self.rows(dC)
        v = self.w * rows[self.nodes]
        i = int(torch.argmax(v))
        return self.S['scale'] * v.max(), i + 1


def one_step_lower(S, dC, ds, restarts=64, iters=40, seed=0):
    """Exact one-step distance at vertices g in {g_lo,g_hi}^k, maximised by sign ascent (convex objective)."""
    n, k, d, a = S['n'], S['k'], S['d'], S['a']
    dC = np.asarray(dC); ds = float(ds)
    W = (a / math.sqrt(n)) * dC.T @ S['OA'].T @ S['V'].T          # d x k : block part dC^T z = W g
    rng = np.random.default_rng(seed)
    best = 0.0; bestg = None
    def val(g):
        z = W @ g; dN = g[d:] - g[d:].mean()
        return float(z @ z + (ds * a / math.sqrt(n)) ** 2 * (dN @ dN))
    for r in range(restarts):
        g = rng.choice([G_LO, G_HI], k)
        for it in range(iters):
            z = W @ g; dN = g[d:] - g[d:].mean()
            grad = 2 * W.T @ z
            grad[d:] += 2 * (ds * a / math.sqrt(n)) ** 2 * dN
            gn = np.where(grad > 0, G_HI, G_LO)
            if np.array_equal(gn, g):
                break
            g = gn
        v = val(g)
        if v > best:
            best, bestg = v, g
    return S['scale'] * math.sqrt(best), bestg


# ---------------- Codex chart reconstruction (sustained spread, from saved Q, Z) ----------------

class Chart:
    def __init__(self, S, Q, Z, strength='sustained'):
        self.S = S; d = S['d']
        self.Q = torch.tensor(Q); self.Z = torch.tensor(Z); self.T = Q.shape[0]
        div = math.sqrt(self.T) if strength == 'total-budget' else 1.0
        self.amp = 0.055 / div
        self.base = torch.tensor([0.25 / div if i % 2 == 0 else -0.25 / div for i in range(d)])
        self.perm = torch.tensor(np.array([(np.arange(d) - t) % d for t in range(self.T)]))
        OA = torch.tensor(S['OA']); self.OA = OA; a = S['a']
        # C0 = sum_{j<3n} (a OA)^j by doubling
        def geo(N):
            if N == 1: return torch.eye(d), a * OA
            if N % 2 == 0:
                Sm, P = geo(N // 2); return Sm + P @ Sm, P @ P
            Sm, P = geo(N - 1); return Sm + P, (a * OA) @ P
        self.C0, _ = geo(3 * S['n'])
        self.s0 = (1 - a ** (3 * S['n'])) / (1 - a)
        self.ck = S['ck']

    def gates(self, C):
        field = torch.tanh(math.sqrt(self.T * self.S['d']) * (self.Q @ C @ self.Z.T))
        latent = self.base + self.amp * (field - field.mean(dim=1, keepdim=True))
        rot = torch.gather(latent, 1, self.perm)
        common = self.ck * rot[:, :1]; cyc = rot[:, 1:] + common
        return torch.cat([1 - cyc ** 2, 1 - common ** 2], dim=1)

    def endpoint(self, C):
        a = self.S['a']; M = self.C0; s = torch.tensor(self.s0); I = torch.eye(self.S['d'])
        for g in self.gates(C):
            M = g[:, None] * (a * self.OA @ M + I); s = g[-1] * (a * s + 1)
        return a * self.OA @ M + I, a * s + 1

    def diff(self, C):
        Cp, sp = self.endpoint(C); Cm, sm = self.endpoint(-C)
        return Cp - Cm, sp - sm


def load_codex_pair(n, start):
    z = np.load(CODEX + f'adversary_n{n}_start{start}.npz')
    return z['C'], z['Q'], z['Z']


def ub_pyth_terms(S, rows_sel, M, R, w):
    """Pythagorean refinement (Theorem Q'): with the ORTHOGONAL spike coefficient s', ||X_L||^2 = s'^2 c + ||r'||^2 <= N_L^2,
    c = ||theta||^2 = 1 - 1/k, N_L = beta0 lam^L sqrt(c), ||r'|| <= ||r|| <= R_L. Per-L value
    max_{0<=s<=N/sqrt(c)} s*row + M*min(R, sqrt(N^2 - c s^2)). Vectorised over L (torch)."""
    c = 1.0 - 1.0 / S['k']
    N = w * math.sqrt(c)                       # w = beta0 lam^L
    row = rows_sel
    full = N * torch.sqrt(row ** 2 / c + M ** 2)                       # unconstrained optimum (when R >= N part)
    s_star = N * row / (c * torch.sqrt(row ** 2 / c + M ** 2))
    s0 = torch.sqrt(torch.clamp(N ** 2 - R ** 2, min=0.0) / c)
    capped = s0 * row + M * R
    use_full = (R >= N) | (s_star >= s0)
    return torch.where(use_full, torch.minimum(full, w * row + R * M), torch.minimum(capped, w * row + R * M))


def ub_pyth(br, dC, ds):
    S = br.S
    rows = br.rows(dC)
    M = torch.maximum(torch.linalg.matrix_norm(dC, ord=2), torch.abs(torch.as_tensor(ds)))
    terms = ub_pyth_terms(S, rows[br.nodes], M, br.R[1:], br.w)
    tail = br.tail_w * rows.max() + br.tail_R * M
    return S['scale'] * torch.maximum(terms.max(), tail)


def phi_star(grid=4001):
    """phi* = max over x, y in [g_lo/g_hi, 1] of (1-x) x^2/(1+x) + (x-y)^2  (Theorem R3 constant)."""
    from core import G_LO, G_HI
    lo = G_LO / G_HI
    xs = np.linspace(lo, 1.0, grid)
    f1 = (1 - xs) * xs ** 2 / (1 + xs)
    return float(np.max(f1 + np.maximum((xs - lo) ** 2, (1 - xs) ** 2)))


def remainder_budget_R3(S, Lmax):
    """Theorem R3 (energy / quadrature form), valid for 1 <= L <= d (single node-0 step at t = 1):
    ||r_L|| <= beta0 lam^L [ c' + sqrt(c'^2 + (omega0/g_hi)^2 + phi* c'^2 (L-1)) ],  c' = c_k sqrt(1-1/k).
    Returned array is min(triangle, R3) for L <= d and triangle beyond."""
    from core import G_HI
    R = remainder_budget(S, Lmax)
    k, d, b0, lam = S['k'], S['d'], S['beta0'], S['lam']
    cp = S['ck'] * math.sqrt(1 - 1 / k); ph = phi_star()
    w0 = S_G * math.sqrt(1 - 1 / k) / G_HI
    for L in range(2, min(Lmax, d) + 1):
        R3 = b0 * lam ** L * (cp + math.sqrt(cp ** 2 + w0 ** 2 + ph * cp ** 2 * (L - 1)))
        R[L] = min(R[L], R3)
    return R


class Bracket3(Bracket):
    def __init__(self, S, Lmax=None):
        super().__init__(S, Lmax)
        self.R = torch.tensor(remainder_budget_R3(S, self.Lmax))


class Bracket4(Bracket):
    """Theorem Q with the JOINT interval-DP budget (Theorem R4) for L <= Ljoint, triangle R1 budget beyond."""
    def __init__(self, S, Lmax=None, Ljoint=None, nb=600, nu=60):
        super().__init__(S, Lmax)
        from joint_dp import joint_budget
        self.Lj = Ljoint or min(64, S['d'])
        jb = joint_budget(S, self.Lj, nb=nb, nu=nu)
        His, Vs = [], []
        for L in range(1, self.Lj + 1):
            hi, V = jb[L]; m = np.isfinite(V)
            His.append(torch.tensor(hi[m])); Vs.append(torch.tensor(V[m]))
        self.His, self.Vs = His, Vs

    def ub(self, dC, ds, parts=False):
        S = self.S
        rows = self.rows(dC)
        M = torch.maximum(torch.linalg.matrix_norm(dC, ord=2), torch.abs(torch.as_tensor(ds)))
        vals = []
        for L in range(1, self.Lj + 1):
            r = rows[self.nodes[L - 1]]
            vals.append(self.w[L - 1] * torch.max(self.His[L - 1] * r + self.Vs[L - 1] * M))
        vj = torch.stack(vals)
        rest = self.w[self.Lj:] * rows[self.nodes[self.Lj:]] + self.R[self.Lj + 1:] * M
        tail = self.tail_w * rows.max() + self.tail_R * M
        allv = torch.cat([vj, rest, tail.reshape(1)])
        val = S['scale'] * allv.max()
        if parts:
            i = int(torch.argmax(allv))
            L = i + 1
            if L <= self.Lj:
                r = rows[self.nodes[L - 1]]
                b = int(torch.argmax(self.His[L - 1] * r + self.Vs[L - 1] * M))
                sp = float(S['scale'] * self.w[L - 1] * self.His[L - 1][b] * r)
                rp = float(S['scale'] * self.w[L - 1] * self.Vs[L - 1][b] * M)
            else:
                sp, rp = float('nan'), float('nan')
            return val, dict(L_star=L, spike_part=sp, rem_part=rp, M_opds=float(M))
        return val
