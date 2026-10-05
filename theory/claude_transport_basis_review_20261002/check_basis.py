"""Claude's numerical check of age_preserving_transport_basis_20261002 (evidence, not proof).

modes:
  identity - small n: companion-coefficient encoders (section 3 fixed shape, section 7 co-moving) against an exact tensor
             emulation and against the directly propagated surrogate; identities (7), (F2), (F5); ledger inequality;
             3-step (F10) leakage; delayed decoder with a terminal reset.
  f11      - section 7.4 counterhistory at n=200 on the actual dense model, several N and ridge xi; frame collapse b_t.
  stress   - co-moving fixed-anchor encoder (tensor emulation, one-step delay) on the hostile histories that defeated the
             convex merger (same seeds), plus a two-phase profile switch: actual worst permitted box-query error, ledger,
             frame conditioning.
"""
import sys, json, math, time, copy
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.argv += [] if len(sys.argv) > 2 else ['4']
sys.path.insert(0, '../claude_moment_merger_review_20261001')
from check_merger import family, weights, realize, surrogate_direct, box_max, actual_grads, consts, stress_histories
torch.set_num_threads(int(sys.argv[2]))
EPS = 1e-3

# ------------------------------------------------------------------------------------------------- encoders
class Base:
    """exact e1 / source eligibilities (2) + current h; subclasses implement the r-block core."""
    def __init__(self, F, delay=True):
        self.F = F; n, k, l = F['n'], F['k'], F['l']; self.n, self.k, self.l = n, k, l; self.r = k - 1; self.p = 2 * n + 1
        self.a = F['a']; self.delta = F['delta']; self.Ob = F['O'][1:, 1:]; self.lam = (1 + self.a) / 2
        self.wR, self.wW, self.wb = (float(v) for v in weights(F))
        self.E1 = torch.zeros(self.p); self.Es = torch.zeros(l, self.p); self.h = torch.zeros(n); self.t = 0
        self.delay = delay; self.pending = None; self.z = 0.0; self.zs = []; self.nus = []

    def step(self, x):
        F = self.F; k = self.k
        hn = torch.tanh(F['R'] @ self.h + F['W'] @ x + F['b']); G = 1 - hn ** 2; Gb = G[1:k]
        f = torch.cat([self.wR * self.h, self.wW * x, torch.tensor([self.wb])])
        if self.t == 0: self.init_profile(Gb)
        if self.delay:
            if self.pending is not None: self.core(*self.pending)
            self.pending = (Gb, f)
        else:
            self.core(Gb, f)
        self.E1 = float(G[0]) * (self.a * self.E1 + f); self.Es = G[k:, None] * (self.delta * self.Es + f[None, :])
        self.h = hn; self.t += 1; self.zs.append(self.z)

    def grads(self, C):
        """decoded normalized past gradients Zhat^T c for columns c of C (n x A): A x P."""
        n, k, p = self.n, self.k, self.p; A = C.shape[1]; Psi = torch.zeros(A, n, p); Cb = C[1:k]
        if self.delay:
            Gl, fl = self.pending; gc = Gl[:, None] * Cb
            Psi[:, 1:k, :] += gc.T[:, :, None] * fl[None, None, :]
            adj = self.a * self.Ob.T @ gc
        else:
            adj = Cb
        Psi[:, 1:k, :] += self.core_grad(adj)
        Psi[:, 0, :] = C[0][:, None] * self.E1[None, :]; Psi[:, k:, :] = C[k:].T[:, :, None] * self.Es[None]
        return torch.cat([Psi[:, :, :n].reshape(A, -1), Psi[:, :, n:2 * n].reshape(A, -1), Psi[:, :, 2 * n]], 1)

def charpoly(B):
    """chi_0..chi_(r-1) of det(zI-B) (float64 via eigenvalues; only used at small r)."""
    c = np.poly(B.numpy()).real            # highest first: [1, c_(r-1), ..., c_0]
    return torch.tensor(c[::-1][:-1].copy())

class ShapeCoef(Base):
    """section 3: fixed saved profile D, companion coefficients T (r x p), update (6); delayed decoder (8a)."""
    def init_profile(self, Gb):
        self.D = Gb / Gb.max(); self.B = self.a * self.D[:, None] * self.Ob; self.chi = charpoly(self.B)
        self.T = torch.zeros(self.r, self.p)
    def companion(self, T):
        Tn = torch.zeros_like(T); Tn[0] = -self.chi[0] * T[-1]; Tn[1:] = T[:-1] - self.chi[1:, None] * T[-1][None, :]; return Tn
    def core(self, Gb, f):
        g = float(Gb.max()); self.T = g * self.companion(self.T); self.T[0] += g * f
    def core_grad(self, y):                # sum_j (B^j D)^T y  (x)  T_j
        out = 0; yj = y
        for j in range(self.r):
            out = out + (self.D[:, None] * yj).T[:, :, None] * self.T[j][None, None, :]; yj = self.B.T @ yj
        return out
    def count(self):
        return self.r * self.p + (self.l + 1) * self.p + self.r + 1 + (self.p if self.delay else 0)

class CoMoving(Base):
    """section 7: co-moving Q, fixed anchor D/B, fresh-injector ridge refit (F3). If coef=True the coefficient array T is
    kept (companion action J_B); otherwise the decoded map S = L_D(T) (r x r x p) is emulated exactly (no char poly)."""
    def __init__(self, F, xi, delay=True, coef=False):
        super().__init__(F, delay); self.xi = xi; self.coef = coef; self.frame = []; self.res = []
    def init_profile(self, Gb):
        r = self.r; self.D = Gb / Gb.max(); self.B = self.a * self.D[:, None] * self.Ob; self.Binv = torch.linalg.inv(self.B)
        self.Q = torch.eye(r); self.logb = 0.0
        if self.coef: self.chi = charpoly(self.B); self.T = torch.zeros(r, self.p)
        else: self.Z = torch.zeros(r, r, self.p)      # decoded map Q L_D(T), propagated stably (identical in exact arithmetic)
    def core(self, Gb, f):
        a, r = self.a, self.r
        A = a * Gb[:, None] * self.Ob
        Qraw = A @ self.Q @ self.Binv; s = float(torch.linalg.matrix_norm(Qraw, 2)); self.Q = Qraw / s; self.logb += math.log(s)
        if self.coef:
            T = self.T; Tn = torch.zeros_like(T); Tn[0] = -self.chi[0] * T[-1]; Tn[1:] = T[:-1] - self.chi[1:, None] * T[-1][None, :]
            self.T = s * Tn
        else:
            self.Z = torch.einsum('ab,bcp->acp', A, self.Z)                       # (F2): Q_t L_D(Tprop) = A_t Q_(t-1) L_D(T_(t-1))
        W = 1 / (1 - (a / self.lam) ** 2 * Gb ** 2); sw = W.sqrt()[:, None]
        BjD = [self.D.diag()]
        for _ in range(r - 1): BjD.append(self.B @ BjD[-1])
        BjD = torch.stack(BjD); C = torch.einsum('ab,jbc->jac', self.Q, BjD)          # C_j = Q B^j D
        Gm = torch.diag(Gb); C0 = C[0]
        ell = float((C0 * W[:, None] * Gm).sum() / (C0 * W[:, None] * C0).sum()); Enew = Gm - ell * C0
        X = (C * sw[None]).reshape(r, -1); H = X @ X.T; bb = X @ (Enew * sw).reshape(-1)
        alpha = torch.linalg.solve(H + self.xi * torch.eye(r), bb)
        coef = alpha.clone(); coef[0] += ell
        if self.coef: self.T = self.T + coef[:, None] * f[None, :]
        else: self.Z = self.Z + torch.einsum('j,jab,p->abp', coef, C, f)   # fresh part Q (ell D + sum alpha_j B^j D) (x) f
        Rnew = ell * C0 + torch.einsum('j,jab->ab', alpha, C) - Gm
        nu = float(f.norm()) * float(torch.linalg.matrix_norm(sw * Rnew, 2))
        self.z = self.lam ** 2 * self.z + nu ** 2; self.nus.append(nu); self.res.append(float(torch.linalg.matrix_norm(Rnew, 2)))
        sv = torch.linalg.svdvals(self.Q); self.frame.append(float(sv[-1] / sv[0]))
    def core_grad(self, y):
        if self.coef:
            y = self.Q.T @ y
            out = 0; yj = y
            for j in range(self.r):
                out = out + (self.D[:, None] * yj).T[:, :, None] * self.T[j][None, None, :]; yj = self.B.T @ yj
            return out
        return torch.einsum('bA,baq->Aaq', y, self.Z)
    def count(self):
        r, p = self.r, self.p
        return r * r + r * p + (self.l + 1) * p + r + 2 + (p if self.delay else 0)

def surrogate_block_rows(F, Zh, Zd):
    return float((Zh - Zd).abs().max())

# ------------------------------------------------------------------------------------------------- modes
def shape_history(F, kind, T, seed):
    """histories inside (4): fixed memory profile from t=1 with scalar modulation g_t, then (optionally) a reset."""
    n, k, l = F['n'], F['k'], F['l']; rng = np.random.default_rng(seed); hs = [torch.zeros(n)]
    Dm = torch.ones(k); Dm[2] = 0.86; Dm[3] = 0.93                         # memory profile (row 0 = e1 is free anyway)
    for t in range(1, T):
        g = 1.0 if kind == 'const' else float(rng.uniform(0.985, 1.0))
        hm = torch.sqrt(torch.clamp(1 - g * Dm, min=0)) * torch.tensor(rng.choice([-1.0, 1.0], k))
        hm[0] = float(rng.uniform(-0.3, 0.3))                               # e1 row unrestricted
        hs.append(torch.cat([hm, torch.tensor(rng.uniform(-0.4, 0.4, l))]))
    hs.append(torch.zeros(n)); return hs

def mode_identity():
    out = []
    for n, c, T in ((16, 1.0, 70), (24, 1.0, 60), (20, 2.0, 60)):
        F = family(n, c); res = {'n': n, 'c': c, 'T': T}
        for kind in ('const', 'modulated'):
            hs = shape_history(F, kind, T, seed=n); xs = realize(F, hs); Zd = surrogate_direct(F, xs)
            res[f'{kind}_max_abs_input'] = max(float(x.abs().max()) for x in xs)
            for name, enc in (('shapecoef_delay', ShapeCoef(F, True)), ('comoving_coef_delay', CoMoving(F, 1e-3, True, True)),
                              ('comoving_tensor_delay', CoMoving(F, 1e-3, True, False))):
                for x in xs: enc.step(x)
                Zh = enc.grads(torch.eye(n)); res[f'{kind}_{name}_maxabs_vs_surrogate'] = float((Zh - Zd).abs().max())
                if isinstance(enc, CoMoving): res[f'{kind}_{name}_zT'] = enc.z
            res[f'{kind}_surrogate_maxabs'] = float(Zd.abs().max())
        # general random history: coefficient vs tensor co-moving agree; ledger inequality ||E||op <= a sqrt(z_(T-1))
        rng = np.random.default_rng(5 + n)
        hs = [torch.zeros(n)] + [torch.tensor(rng.uniform(-0.3, 0.3, n)) for _ in range(T - 1)] + [torch.zeros(n)]
        xs = realize(F, hs); Zd = surrogate_direct(F, xs)
        e1, e2 = CoMoving(F, 1e-3, True, True), CoMoving(F, 1e-3, True, False)
        for x in xs: e1.step(x); e2.step(x)
        Z1 = e1.grads(torch.eye(n)); Z2 = e2.grads(torch.eye(n)); E = (Z2 - Zd)[1:F['k']]
        res['random_coef_vs_tensor_maxabs'] = float((Z1 - Z2).abs().max()); res['random_decoded_maxabs'] = float(Z2.abs().max())
        res['random_Eop_block'] = float(torch.linalg.matrix_norm(E, 2)); res['random_a_sqrt_z_Tminus1'] = F['a'] * math.sqrt(e2.zs[-1])
        res['random_other_rows_maxabs'] = float(torch.cat([(Z2 - Zd)[:1], (Z2 - Zd)[F['k']:]]).abs().max())
        res['random_max_abs_input'] = max(float(x.abs().max()) for x in xs)
        # (F2): one transport step without fresh injection preserves decoded credit exactly (coefficient encoder e1)
        enc = copy.deepcopy(e1); Gb = 1 - torch.tanh(torch.tensor(rng.uniform(-0.6, 0.6, F['k'] - 1))) ** 2
        def decoded(en, Qm, Tm):
            out = torch.zeros(en.r, en.r, en.p); P_ = Qm.clone()
            for j in range(en.r): out += torch.einsum('ab,p->abp', P_ * en.D[None, :], Tm[j]); P_ = P_ @ en.B
            return out
        A = enc.a * Gb[:, None] * enc.Ob
        before = torch.einsum('ab,bcp->acp', A, decoded(enc, enc.Q, enc.T))
        Qraw = A @ enc.Q @ enc.Binv; s = float(torch.linalg.matrix_norm(Qraw, 2)); T = enc.T
        Tn = torch.zeros_like(T); Tn[0] = -enc.chi[0] * T[-1]; Tn[1:] = T[:-1] - enc.chi[1:, None] * T[-1][None, :]
        after = decoded(enc, Qraw / s, s * Tn)
        res['F2_transport_rel'] = float((before - after).abs().max() / before.abs().max())
        # (F10) three-step leakage: D=I, noncommuting middle gate, scalar end
        r = F['k'] - 1; Ob = F['O'][1:, 1:]; G2 = torch.ones(r); G2[2] = 0.8
        Q3 = Ob @ torch.diag(G2) @ Ob.T; X = torch.linalg.inv(Q3); B = F['a'] * Ob
        res['F10_commutator_norm'] = float(torch.linalg.matrix_norm(X @ B - B @ X, 2))
        out.append(res); print(json.dumps(res), flush=True)
    return out

def f11_history(F, N):
    n, k, l = F['n'], F['k'], F['l']; i = k - 1; hs = [torch.zeros(n)]
    h1 = torch.zeros(n); h1[i] = 0.3; h1[k:] = 0.4; hs.append(h1)
    for _ in range(2, N + 1):
        h = torch.zeros(n); h[k:] = 0.4; hs.append(h)
    return hs

def endpoint_errors(F, enc, xs_full):
    lam, beta, kQ, dd = consts(F); n = F['n']
    Cb = F['R'].T / beta; act, hT = actual_grads(F, xs_full, Cb)
    Y = enc.grads(Cb) - act; pre = F['R'] @ hT + F['W'] @ (0.45 - F['R'] @ hT) + F['b']
    gu = (1 - torch.tanh(pre) ** 2) / math.sqrt(n)
    return {'uniform_query_error': float((Y.T @ gu).norm()), 'worst_box_query_error': box_max(Y, n),
            'certificate': dd + F['a'] * kQ * math.sqrt(enc.zs[-1]) if enc.zs else dd, 'endpoint_max_abs_h': float(hT.abs().max())}

def mode_f11():
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 200; F = family(n, 1.0); k, r = F['k'], F['k'] - 1
    Ns = [150, 400, 1000, 2000]; xis = [1e-8, 1e-4, 1.0, 1e4]
    hs = f11_history(F, max(Ns)); xs = realize(F, hs)
    x_reset = -F['R'] @ hs[-1] - F['b']
    lam, beta, kQ, dd = consts(F)
    # dimension s of W = ker(I-O_*) cap e_i^perp, and the claimed lower bound (F18)
    Ob = F['O'][1:, 1:]; ev, U = torch.linalg.eigh((Ob + Ob.T) / 2); fix = U[:, ev > 1 - 1e-9]
    ei = torch.zeros(r); ei[-1] = 1; Pfix = fix @ fix.T; v = Pfix @ ei
    s_dim = fix.shape[1] - (1 if float(v.norm()) > 1e-9 else 0)
    sg = (1 - math.tanh(0.25) ** 2 - (1 - math.tanh(0.5) ** 2)) / 2; a = F['a']; e = F['e']
    lb = sg * a * (a - e) * 0.4 * math.sqrt(F['l'] / n) * math.sqrt(s_dim) / (2 * n * (1 / n)) - dd
    meta = {'n': n, 'k': k, 'r': r, 'd': F['d'], 's_dim_W': s_dim, 'claimed_F18_bound_value': lb, 'delta_dense': dd,
            'max_abs_input': max(float(x.abs().max()) for x in xs + [x_reset]), 'Ns': Ns, 'xis': xis}
    print(json.dumps(meta), flush=True)
    encs = {xi: CoMoving(F, xi, True, False) for xi in xis}
    rows = []; t0 = time.time()
    for t, x in enumerate(xs, start=1):
        for enc in encs.values(): enc.step(x)
        if t in Ns:
            xs_full = xs[:t] + [x_reset]
            for xi, enc in encs.items():
                e2 = copy.deepcopy(enc); e2.step(x_reset)
                row = {'N': t, 'xi': xi, 'log_b_t': enc.logb, 'frame_cond_min_over_max': enc.frame[-1] if enc.frame else 1.0,
                       'fresh_residual_op_last': enc.res[-1] if enc.res else 0.0, 'seconds': time.time() - t0}
                row.update(endpoint_errors(F, e2, xs_full)); rows.append(row); print(json.dumps(row), flush=True)
    return {'meta': meta, 'rows': rows}

def two_phase_history(F, T, seed):
    """constant memory profile A for the first half, a different constant profile B afterwards (one profile switch)."""
    n, k, l, d = F['n'], F['k'], F['l'], F['d']; rng = np.random.default_rng(seed); hs = [torch.zeros(n)]
    for t in range(1, T):
        mem = torch.zeros(k); mem[2 if t < T // 2 else 5] = 0.4
        hs.append(torch.cat([mem, torch.tensor(rng.choice([-0.4, 0.4], l))]))
    hs.append(torch.zeros(n)); return hs

def mode_stress():
    kinds = sys.argv[3].split(',') if len(sys.argv) > 3 else ['period1', 'period1_signsrc', 'twophase', 'sparse', 'dense']
    ns = [int(v) for v in sys.argv[4].split(',')] if len(sys.argv) > 4 else [64, 128]
    xis = [float(v) for v in sys.argv[5].split(',')] if len(sys.argv) > 5 else [1e-4, 1.0]
    out = []; lamb = None
    for kind in kinds:
        for n in ns:
            F = family(n, 1.0); T = 8 * n
            hs = two_phase_history(F, T, 2000 + n) if kind == 'twophase' else stress_histories(F, kind, T, seed=1000 + n)
            xs = realize(F, hs); t0 = time.time()
            encs = [CoMoving(F, xi, True, False) for xi in xis]
            for x in xs:
                for e in encs: e.step(x)
            res = {'kind': kind, 'n': n, 'T': len(xs), 'max_abs_input': max(float(x.abs().max()) for x in xs), 'encoders': []}
            for xi, e in zip(xis, encs):
                r = endpoint_errors(F, e, xs); _, beta, kQ, dd = consts(F)
                r.update({'xi': xi, 'count': e.count(), 'zT_minus1_over_target': e.zs[-1] / (((EPS - dd) / (F['a'] * kQ)) ** 2),
                          'nu_median': float(np.median(e.nus)), 'fresh_residual_op_median': float(np.median(e.res)),
                          'frame_cond_final': e.frame[-1], 'log_b_T': e.logb})
                res['encoders'].append(r)
            res['seconds'] = time.time() - t0; out.append(res); print(json.dumps(res), flush=True)
    return out

if __name__ == '__main__':
    mode = sys.argv[1]
    res = {'identity': mode_identity, 'f11': mode_f11, 'stress': mode_stress}[mode]()
    tag = mode if len(sys.argv) <= 3 else mode + '_' + '_'.join(a.replace(',', '-') for a in sys.argv[3:])
    json.dump(res, open(f'{tag}_check.json', 'w'), indent=1)
