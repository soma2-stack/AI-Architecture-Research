"""Claude's numerical check of query_weighted_moment_merger_20261001 (evidence, not proof).

modes:
  identity - eqs (4)-(8), (11)-(13) on explicit k x kp matrices: merger residual, exact query error, K = M_v M_v^T,
             spectral form of K, mass bound, coherent-channel cancellation.
  exact    - the encoder (22)-(23) with more slots than steps (every merge into an empty slot) is exact against the directly
             propagated surrogate; with m=1,2 the ledger inequality ||E_T||op <= sqrt(z_T) holds; hybrid row-1 split.
  c1       - section 6.2 counterhistory at n=200 (T=n^2+1) on the actual dense model: round-robin m=1,2,8,32 and hybrid m=1,4.
  stress   - hybrid round-robin encoder on simple non-scalar histories (period-1, sparse aperiodic, dense small) at
             n=64,128,256: actual worst permitted box-query error and the certified ledger bound.
  greedy   - same histories, m=8, merging at every step the pair (among m+1 packets) with the smallest loss-scaled
             residual nu (a discontinuous oracle, used only to probe whether ANY merge choice meets the ledger target).
"""
import sys, json, math, time
import numpy as np, torch
torch.set_default_dtype(torch.float64)
torch.set_num_threads(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
sys.path.insert(0, '../claude_rotating_gate_review_20261001')
sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_rotating import family, weights, realize, surrogate_direct
from check_aperiodic import box_max, G_LO, G_HI

EPS = 1e-3

def consts(F):
    n, c, k = F['n'], F['c'], F['k']; a = F['a']; lam = (1 + a) / 2
    beta = max(1.0, float(F['R'].norm())); kQ = a / beta; Cc = 6 / 5
    ddense = kQ * F['e'] * Cc / (c / n) ** 2
    return lam, beta, kQ, ddense

def kmat(V, Opow):
    """K(V) = sum_s b_s O^s with b_s = sum_j V_j . V_(j-s) (eq. 8) via FFT over the orbit index."""
    Vh = torch.fft.fft(V, dim=0); b = torch.fft.ifft((Vh.abs() ** 2).sum(1)).real
    return torch.einsum('s,sij->ij', b, Opow)

class Encoder:
    def __init__(self, F, m, hybrid, policy='rr', ledger=True):
        self.F = F; n, k, l, d, O = F['n'], F['k'], F['l'], F['d'], F['O']
        self.B = list(range(1, k)) if hybrid else list(range(k)); self.hybrid = hybrid
        Ob = O[1:, 1:] if hybrid else O; self.Ob = Ob; kb = len(self.B); self.kb = kb; p = 2 * n + 1; self.p = p
        P = [torch.eye(kb)]
        for _ in range(d - 1): P.append(Ob @ P[-1])
        self.Opow = torch.stack(P)
        self.m = m; self.Q = torch.zeros(m, kb, kb); self.f = torch.zeros(m, d, p); self.mu = torch.zeros(m)
        self.E1 = torch.zeros(p); self.Es = torch.zeros(l, p); self.h = torch.zeros(n); self.t = 0
        self.lam = (1 + F['a']) / 2; self.z = 0.0; self.nus = []; self.policy = policy; self.ledger = ledger
        self.wR, self.wW, self.wb = (float(v) for v in weights(F))

    def nu2(self, Q1, f1, mu1, Q2, f2, mu2, Dinv):
        al = mu1 / (mu1 + mu2); V = (1 - al) * f1 - al * f2
        K = kmat(V, self.Opow); X = Dinv[:, None] * (Q1 - Q2)
        return float(torch.linalg.eigvalsh(X @ K @ X.T).max().clamp(min=0)), al

    def step(self, x):
        F = self.F; n, k, a, delta = F['n'], F['k'], F['a'], F['delta']; R, W, b = F['R'], F['W'], F['b']
        h = self.h; hn = torch.tanh(R @ h + W @ x + b); G = 1 - hn ** 2; Gb = G[self.B]; g = float(Gb.max())
        vraw = torch.cat([self.wR * h, self.wW * x, torch.tensor([self.wb])])
        self.Q = (Gb / g)[None, :, None] * (self.Ob @ self.Q @ self.Ob.T)
        self.f = a * g * torch.roll(self.f, 1, 1); self.mu = a * g * self.mu
        Qn = torch.diag(Gb / g); fn = torch.zeros_like(self.f[0]); fn[0] = g * vraw; mun = float(fn[0].norm())
        Dinv = 1 / torch.sqrt(1 - (a / self.lam) ** 2 * Gb ** 2)
        if self.policy == 'rr':
            s = self.t % self.m; mu_s = float(self.mu[s])
            if self.ledger:
                nu2, al = self.nu2(self.Q[s], self.f[s], mu_s, Qn, fn, mun, Dinv)
            else:
                nu2, al = 0.0, mu_s / (mu_s + mun)
            self.Q[s] = al * self.Q[s] + (1 - al) * Qn; self.f[s] = self.f[s] + fn; self.mu[s] = mu_s + mun
        else:  # greedy: best pair among the m advanced packets and the fresh one
            Qs = torch.cat([self.Q, Qn[None]]); fs = torch.cat([self.f, fn[None]]); mus = torch.cat([self.mu, torch.tensor([mun])])
            best = None
            for i in range(self.m + 1):
                for j in range(i + 1, self.m + 1):
                    if float(mus[i]) == 0.0 or float(mus[j]) == 0.0:
                        tot = float(mus[i] + mus[j]); v, al = 0.0, (float(mus[i]) / tot if tot > 0 else 0.5)
                    else:
                        v, al = self.nu2(Qs[i], fs[i], float(mus[i]), Qs[j], fs[j], float(mus[j]), Dinv)
                    if best is None or v < best[0]: best = (v, al, i, j)
            nu2, al, i, j = best
            Qs[i] = al * Qs[i] + (1 - al) * Qs[j]; fs[i] = fs[i] + fs[j]; mus[i] = mus[i] + mus[j]
            keep = [r for r in range(self.m + 1) if r != j]
            self.Q, self.f, self.mu = Qs[keep].clone(), fs[keep].clone(), mus[keep].clone()
        self.z = self.lam ** 2 * self.z + nu2; self.nus.append(math.sqrt(nu2))
        if self.hybrid: self.E1 = float(G[0]) * (a * self.E1 + vraw)
        self.Es = G[k:, None] * (delta * self.Es + vraw[None, :])
        self.h = hn; self.t += 1

    def grads(self, C):
        """decoded normalized past gradients Zhat^T c for the columns c of C (n x A); returns A x P."""
        F = self.F; n, k = F['n'], F['k']; A = C.shape[1]
        Psi = torch.zeros(A, n, self.p); CB = C[self.B]
        for s in range(self.m):
            y = self.Q[s].T @ CB                                        # kb x A
            Yj = torch.einsum('jab,aA->jbA', self.Opow, y)              # (O^j)^T y
            Psi[:, self.B, :] += torch.einsum('jbA,jp->Abp', Yj, self.f[s])
        if self.hybrid: Psi[:, 0, :] = C[0][:, None] * self.E1[None, :]
        Psi[:, k:, :] = C[k:].T[:, :, None] * self.Es[None]
        return torch.cat([Psi[:, :, :n].reshape(A, -1), Psi[:, :, n:2 * n].reshape(A, -1), Psi[:, :, 2 * n]], 1)

    def count(self):
        F = self.F; n, k, l, d = F['n'], F['k'], F['l'], F['d']; p = 2 * n + 1
        return self.m * (self.kb ** 2 + d * p + 1) + (l + (1 if self.hybrid else 0)) * p + 2

def actual_grads(F, xs, C, chunk=256):
    """exact normalized past gradients Z_T^T c of the ACTUAL dense model (inputs held fixed), columns of C; A x P."""
    R, W, b = F['R'], F['W'], F['b']; n = F['n']; wR, wW, wb = weights(F); A = C.shape[1]
    hs = [torch.zeros(n)]
    for x in xs: hs.append(torch.tanh(R @ hs[-1] + W @ x + b))
    gR = torch.zeros(A, n, n); gW = torch.zeros(A, n, n); gb = torch.zeros(A, n); Pm = C.clone(); T = len(xs)
    buf_s, buf_h, buf_x = [], [], []
    for t in range(T, 0, -1):
        S = (1 - hs[t] ** 2)[:, None] * Pm; buf_s.append(S); buf_h.append(hs[t - 1]); buf_x.append(xs[t - 1])
        Pm = R.T @ S
        if len(buf_s) == chunk or t == 1:
            Ss = torch.stack(buf_s); Hs = torch.stack(buf_h); Xs = torch.stack(buf_x)
            gR += torch.einsum('tiA,tj->Aij', Ss, Hs); gW += torch.einsum('tiA,tj->Aij', Ss, Xs); gb += Ss.sum(0).T
            buf_s, buf_h, buf_x = [], [], []
    return torch.cat([wR * gR.reshape(A, -1), wW * gW.reshape(A, -1), wb * gb], 1), hs[-1]

def query_basis(F, hT, beta):
    """columns R^T e_i * sech^2(pre_i) / beta pieces: a box query is c(g) = R^T diag(g) q / beta; we return R^T / beta and
    evaluate gates separately (box_max works on Y = R dZ / beta)."""
    return F['R'].T / beta

def run_history(F, xs, encs, box=True):
    """advance all encoders, then compare against the actual dense model on all box queries at the endpoint."""
    lam, beta, kQ, dd = consts(F); n = F['n']
    t0 = time.time()
    for x in xs:
        for e in encs: e.step(x)
    Cb = F['R'].T / beta                                                # column i: R^T e_i / beta
    act, hT = actual_grads(F, xs, Cb)
    vf = 0.45 - F['R'] @ hT                                          # future input giving preactivation 1/2 exactly
    pre = F['R'] @ hT + F['W'] @ vf + F['b']
    ok_endpoint = float(hT.abs().max())
    out = []
    for e in encs:
        dec = e.grads(Cb); Y = (dec - act)                              # row i: dZ^T R^T e_i / beta
        gu = (1 - torch.tanh(pre) ** 2) / math.sqrt(n)
        uni = float((Y.T @ gu).norm())
        worst = box_max(Y, n) if box else None
        nus = np.array(e.nus)
        out.append({'m': e.m, 'hybrid': e.hybrid, 'policy': e.policy, 'count': e.count(), 'uniform_query_error': uni,
                    'worst_box_query_error': worst, 'ledger_bound': dd + kQ * math.sqrt(e.z) if e.ledger else None,
                    'ledger_target_z': ((EPS - dd) / kQ) ** 2, 'z_T': e.z, 'nu_median': float(np.median(nus)) if len(nus) else None,
                    'nu_mean_sq_root': float(np.sqrt((nus ** 2).mean())) if len(nus) else None,
                    'eta_star': (EPS / 2) * math.sqrt(3 * F['c'] / 40)})
    return out, {'max_abs_input': max(float(x.abs().max()) for x in xs), 'endpoint_max_abs_h': ok_endpoint,
                 'future_input_range_for_box': [float((0.2 - F['R'] @ hT).min()), float((0.45 - F['R'] @ hT).max())],
                 'kappa_Q': kQ, 'delta_dense': dd, 'T': len(xs), 'seconds': time.time() - t0}

# ---------------------------------------------------------------------------------------------------------------- modes
def mode_identity():
    out = []
    for n, c in ((24, 1.0), (40, 2.0)):
        F = family(n, c); k, d, O = F['k'], F['d'], F['O']; p = 2 * n + 1; rng = np.random.default_rng(n)
        P = [torch.eye(k)]
        for _ in range(d - 1): P.append(O @ P[-1])
        Opow = torch.stack(P)
        Mf = lambda V: sum(torch.kron(Opow[j], V[j][None, :]) for j in range(d))      # k x (k p), eq. (2)
        res = {'n': n, 'c': c, 'k': k, 'd': d}
        worst = {}
        for trial in range(20):
            Q1 = torch.tensor(rng.normal(size=(k, k))); Q2 = torch.tensor(rng.normal(size=(k, k)))
            f1 = torch.tensor(rng.normal(size=(d, p))) * torch.tensor(rng.uniform(size=(d, 1)))
            f2 = torch.tensor(rng.normal(size=(d, p))) * torch.tensor(rng.uniform(size=(d, 1)))
            mu1 = float(f1.norm(dim=1).sum()) * 1.3; mu2 = float(f2.norm(dim=1).sum()) * 1.1
            al = mu1 / (mu1 + mu2); Qs = al * Q1 + (1 - al) * Q2
            r = Qs @ Mf(f1 + f2) - Q1 @ Mf(f1) - Q2 @ Mf(f2)
            v = (1 - al) * f1 - al * f2; dQ = Q1 - Q2
            e4 = float((r + dQ @ Mf(v)).abs().max()) / float(r.abs().max())
            K = kmat(v, Opow); MvMvT = Mf(v) @ Mf(v).T
            e7 = float((K - MvMvT).abs().max()) / float(K.abs().max())
            cq = torch.tensor(rng.normal(size=k)); lhs = float((r.T @ cq).norm()); rhs = math.sqrt(float(cq @ dQ @ K @ dQ.T @ cq))
            # spectral form: eigenvalues of K on O-eigenspaces are |sum_j w^j V_j|^2
            Vh = torch.fft.fft(v, dim=0); spec = (Vh.abs() ** 2).sum(1)
            ev = torch.linalg.eigvalsh(K); e_spec = float(ev.max()) / float(spec.max())
            Mn = float(torch.linalg.matrix_norm(Mf(v), 2)); mass = float(v.norm(dim=1).sum())
            rn = float(torch.linalg.matrix_norm(r, 2)); b12 = 2 * min(mu1, mu2) * float(torch.linalg.matrix_norm(dQ, 2))
            for key, val in (('eq4_rel', e4), ('eq7_K_vs_MvMvT_rel', e7), ('eq5_query_rel', abs(lhs - rhs) / rhs),
                             ('Kmax_over_spectral_max_minus1', abs(e_spec - 1)), ('Mv_op_over_featuremass', Mn / mass),
                             ('eq12_ratio', rn / b12)):
                worst[key] = max(worst.get(key, 0.0), val)
        # coherent single channel, eq. (13)
        f0 = torch.tensor(rng.normal(size=p)); b1 = torch.tensor(rng.uniform(size=d)); b2 = torch.tensor(rng.uniform(size=d))
        F1 = b1[:, None] * f0[None]; F2 = b2[:, None] * f0[None]
        m1 = float(f0.norm() * b1.sum()); m2 = float(f0.norm() * b2.sum()); al = m1 / (m1 + m2); v = (1 - al) * F1 - al * F2
        Pi = Opow.mean(0); K = kmat(v, Opow)
        worst['eq13_KPi'] = float((K @ Pi).abs().max()) / float(K.abs().max())
        worst['eq13_MvT_Pi'] = float((Mf(v).T @ Pi).abs().max()) / float(Mf(v).abs().max())
        # heterogeneous tuple mass does NOT cancel a subchannel
        g0 = torch.tensor(rng.normal(size=p)); F1h = F1.clone(); F1h[:, n:] = b1[:, None] * g0[None, n:] * 3
        m1h = float(F1h.norm(dim=1).sum()); al = m1h / (m1h + m2); vh = (1 - al) * F1h - al * F2
        worst['heterogeneous_KPi_rel'] = float((kmat(vh, Opow) @ Pi).abs().max()) / float(kmat(vh, Opow).abs().max())
        res.update(worst); out.append(res); print(json.dumps(res), flush=True)
    return out

def mode_exact():
    out = []
    for n, c, T in ((16, 1.0, 60), (20, 2.0, 50)):
        F = family(n, c); k, l = F['k'], F['l']; rng = np.random.default_rng(7 + n)
        hs = [torch.zeros(n)] + [torch.tensor(rng.uniform(-0.35, 0.35, n)) for _ in range(T - 1)] + [torch.zeros(n)]
        xs = realize(F, hs)
        Zd = surrogate_direct(F, xs)
        res = {'n': n, 'c': c, 'T': len(xs), 'max_abs_input': max(float(x.abs().max()) for x in xs)}
        for hyb in (False, True):
            for m in (len(xs) + 1, 1, 2, 5):
                e = Encoder(F, m, hyb)
                for x in xs: e.step(x)
                # decode full Zhat (n x P) from grads against identity
                Zh = e.grads(torch.eye(n))                           # row i = Zhat^T e_i
                E = Zh - Zd; rows = e.B
                tag = f"{'hyb' if hyb else 'plain'}_m{m if m <= 5 else 'T+1'}"
                res[tag + '_maxabs_vs_surrogate'] = float(E.abs().max())
                res[tag + '_Eop_block'] = float(torch.linalg.matrix_norm(E[rows], 2))
                res[tag + '_sqrt_zT'] = math.sqrt(e.z)
                res[tag + '_other_rows_maxabs'] = float(E[[r for r in range(n) if r not in rows]].abs().max())
        out.append(res); print(json.dumps(res), flush=True)
    F = family(200, 1.0); O = F['O']
    out.append({'n': 200, 'O_row1_offdiag_max': float(O[0, 1:].abs().max()), 'O_col1_offdiag_max': float(O[1:, 0].abs().max()),
                'O11': float(O[0, 0]), 'O_e2_dot_e2': float(O[1, 1]), 'Oe2_minus_proj': float((O[:, 1] - O[1, 1] * torch.eye(F['k'])[:, 1]).norm())})
    print(json.dumps(out[-1]), flush=True)
    return out

def c1_history(F):
    n, k, l = F['n'], F['k'], F['l']; a = F['a']; N = n * n; M = math.floor(math.log(0.5) / math.log(a)); sig = 0.4
    hs = [torch.zeros(n)]
    for s in range(1, N + 1):
        mem = torch.zeros(k); mem[0] = 1 / math.sqrt(n); mem[1] = s / (10 * n * (N + 1))
        eta = 1.0 if s >= N - M + 1 else -1.0
        hs.append(torch.cat([mem, torch.full((l,), eta * sig)]))
    hs.append(torch.zeros(n)); return hs, M

def mode_c1():
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    F = family(n, 1.0); a = F['a']; N = n * n; hs, M = c1_history(F); xs = realize(F, hs)
    A_n = sum(a ** (2 * j) for j in range(M)) - sum(a ** (2 * j) for j in range(M, N))
    B_n = sum(a ** j for j in range(M)) - sum(a ** j for j in range(M, N))
    encs = [Encoder(F, m, False) for m in (1, 2, 8, 32)] + [Encoder(F, m, True) for m in (1, 4)]
    out, meta = run_history(F, xs, encs, box=True)
    # K-block (row 1, source R columns) error for the uniform query, plus the m=1 transport eigenvalue q_T on e1
    lam, beta, kQ, dd = consts(F)
    meta.update({'n': n, 'N': N, 'M': M, 'A_n_over_n': A_n / n, 'B_n_over_n': B_n / n,
                 'q_T_m1': float(encs[0].Q[0][0, 0]), 'claimed_D0_lb': 0.049896, 'claimed_actual_lb': 0.048})
    res = {'meta': meta, 'encoders': out}; print(json.dumps(res), flush=True); return res

def stress_histories(F, kind, T, seed):
    n, k, l, d = F['n'], F['k'], F['l'], F['d']; rng = np.random.default_rng(seed); hs = [torch.zeros(n)]
    for t in range(1, T):
        mem = torch.zeros(k)
        if kind.startswith('period1') and not kind.startswith('period1_signsrc'):                       # constant non-scalar gate on memory row 3 (cycled block), constant source
            mem[2] = 0.4; src = torch.full((l,), 0.4)
        elif kind == 'period1_signsrc':             # same constant gate, aperiodic random source signs (features vary)
            mem[2] = 0.4; src = torch.tensor(rng.choice([-0.4, 0.4], l))
        elif kind.startswith('sparse'):                      # one random row in 2..d with +-0.35 each step (rank-one gate deviation)
            r = int(rng.integers(1, d)); prev = float((F['R'] @ hs[-1])[r])   # sign matched to R h_prev keeps x in the cube
            mem[r] = 0.35 * (math.copysign(1.0, prev) if abs(prev) > 0.05 else float(rng.choice([-1.0, 1.0])))
            src = torch.tensor(rng.choice([-0.4, 0.4], l))
        elif kind == 'dense':                       # all memory rows random small: strongly contracting normalized products
            mem = torch.tensor(rng.uniform(-0.2, 0.2, k)); src = torch.tensor(rng.uniform(-0.4, 0.4, l))
            for _ in range(40):                     # shrink until the realized input stays inside the cube
                hc = torch.cat([mem, src]); x = torch.atanh(hc) - F['R'] @ hs[-1] - F['b']
                if float(x.abs().max()) < 0.49: break
                mem = 0.85 * mem
        elif kind == 'scalar':                      # sanity: scalar memory gate (equal |h| on every memory row)
            s = float(rng.uniform(0, 0.1)); mem = s * torch.sign(torch.tensor(rng.normal(size=k))); src = torch.tensor(rng.uniform(-0.4, 0.4, l))
        hs.append(torch.cat([mem, src]))
    if not kind.endswith('_noreset'): hs.append(torch.zeros(n))
    return hs

def mode_stress():
    kinds = sys.argv[3].split(',') if len(sys.argv) > 3 else ['scalar', 'period1', 'period1_signsrc', 'sparse', 'dense']
    ns = [int(v) for v in sys.argv[4].split(',')] if len(sys.argv) > 4 else [64, 128, 256]
    out = []
    for kind in kinds:
        for n in ns:
            F = family(n, 1.0); T = 8 * n; hs = stress_histories(F, kind, T, seed=1000 + n); xs = realize(F, hs)
            encs = [Encoder(F, m, True) for m in (1, 4, 16)]
            res, meta = run_history(F, xs, encs, box=True); meta.update({'kind': kind, 'n': n})
            r = {'meta': meta, 'encoders': res}; out.append(r); print(json.dumps(r), flush=True)
    return out

def mode_greedy():
    kinds = sys.argv[3].split(',') if len(sys.argv) > 3 else ['period1', 'sparse']
    ns = [int(v) for v in sys.argv[4].split(',')] if len(sys.argv) > 4 else [64, 128, 256]
    out = []
    for kind in kinds:
        for n in ns:
            F = family(n, 1.0); T = 8 * n; hs = stress_histories(F, kind, T, seed=1000 + n); xs = realize(F, hs)
            ms = [int(v) for v in sys.argv[5].split(',')] if len(sys.argv) > 5 else [8]
            encs = [Encoder(F, m, True, policy='greedy') for m in ms] + [Encoder(F, ms[-1], True, policy='rr')]
            res, meta = run_history(F, xs, encs, box=True); meta.update({'kind': kind, 'n': n})
            r = {'meta': meta, 'encoders': res}; out.append(r); print(json.dumps(r), flush=True)
    return out

if __name__ == '__main__':
    mode = sys.argv[1]
    res = {'identity': mode_identity, 'exact': mode_exact, 'c1': mode_c1, 'stress': mode_stress, 'greedy': mode_greedy}[mode]()
    tag = mode if len(sys.argv) <= 3 else mode + '_' + '_'.join(a.replace(',', '-') for a in sys.argv[3:])
    json.dump(res, open(f'{tag}_check.json', 'w'), indent=1)
