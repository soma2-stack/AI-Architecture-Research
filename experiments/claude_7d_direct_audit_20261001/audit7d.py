"""Direct numerical audit of the frozen 7D fixed-h antipodal section (Claude; numerical evidence, not a proof).

Reads experiments/third_order_antipodal_7d_20261001 read-only. See PREREGISTRATION.md.
modes:
  validate                      V1-V3 checks (no face computation)
  face F [--escalate|--weakest] preregistered search on face F (1-based)
  confirm F                     50-digit mpmath recomputation of face F's best point
  curv F                        slack attribution and curvature diagnostics on face F
"""
import os
for _k in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[_k] = '1'
import sys, json, math, time, hashlib
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
import torch
from scipy.optimize import minimize, differential_evolution
from scipy.stats import qmc

torch.set_default_dtype(torch.float64)
torch.set_num_threads(1)
HERE = Path(__file__).resolve().parent
EXP = HERE.parent / 'third_order_antipodal_7d_20261001'
OUT = HERE / 'out'
OUT.mkdir(exist_ok=True)
EPS = 1e-3

data = json.loads((EXP / 'candidate.json').read_text())
attempts = json.loads((EXP / 'result.json').read_text())['attempts']
cert = next(a['certificate'] for a in attempts if a['precision'] == 192)
case = data['endpoint']; n = case['n']; r = data['r']
theta_q = [Q(x) for x in data['model_parameters']]
theta = [float(x) for x in theta_q]
R = np.diag(theta[:n]); Wm = np.array(theta[n:n + n * n]).reshape(n, n); bvec = np.array(theta[n + n * n:])
meta = [('R', i, i) for i in range(n)] + [('W', i, j) for i in range(n) for j in range(n)] + [('b', i, 0) for i in range(n)]
P = len(meta)
groups = {g: [theta[p] for p, m in enumerate(meta) if m[0] == g] for g in 'RWb'}
rms = {g: math.sqrt(np.mean(np.square(v))) for g, v in groups.items()}
support = [(i, p) for i in range(n) for p, (g, o, _) in enumerate(meta) if o == i]
ii = [i for i, p in support]; pp = [p for i, p in support]
wsup = torch.tensor([rms[meta[p][0]] for i, p in support])
ER = torch.zeros(n, P, n); EW = torch.zeros(n, P, n); Eb = torch.zeros(n, P)
for p, (g, i, j) in enumerate(meta):
    if g == 'R': ER[i, p, j] = 1.
    elif g == 'W': EW[i, p, j] = 1.
    else: Eb[i, p] = 1.
Rt, Wt, bt = (torch.tensor(v) for v in (R, Wm, bvec))
X0 = torch.tensor([[float(Q(v)) for v in row] for row in case['X']]); T = X0.shape[0]
SD = math.sqrt(3 / 32)
Bm = torch.tensor([[float(Q(v)) for v in row] for row in data['B']])
Lt = torch.tensor([[float(Q(v)) for v in row] for row in data['L']])
Kt = torch.tensor([[float(Q(v)) for v in row] for row in data['K_selected']])
aa = np.array([float(Q(v)) for v in data['a']]); ah = float(Q(data['ah']))
diag = np.array(theta[:n])
norm_factor = math.sqrt(n * max(1.0, float(np.sum(diag ** 2))))
GATE_HIGH = 1 - math.tanh(0.25) ** 2
c_high = np.array([GATE_HIGH * diag[i] / norm_factor for i, p in support])
c_78 = np.array([0.875 * diag[i] / norm_factor for i, p in support])
mu = np.array([float(Q(v)) for v in cert['mu_tilde']])
beta = np.array([float(Q(v)) for v in cert['beta3']])
M3 = np.array([float(v) for v in cert['M3_upper']])
e0 = np.array([float(v) for v in cert['center_rows_upper']])
ellt = (np.array([[float(Q(v)) for v in row] for row in data['K_selected']]) @
        np.array([[float(Q(v)) for v in row] for row in data['L']])) / aa[:, None]

STATS = {'max_lift_residual': 0.0, 'max_y_over_ah': 0.0, 'lift_evals': 0, 'newton_failures': 0}


def fwd(x):
    h = torch.zeros(n, dtype=x.dtype); S = torch.zeros(n, P, dtype=x.dtype)
    for t in range(T):
        direct = torch.einsum('ipj,j->ip', ER, h) + torch.einsum('ipj,j->ip', EW, x[t]) + Eb
        hn = torch.tanh(Rt @ h + Wt @ x[t] + bt); g = 1 - hn * hn
        S = g[:, None] * (Rt @ S + direct); h = hn
    return h, S


def hist(w):
    return X0 + (SD * (Bm @ w)).reshape(T, n)


def G(w):
    h, S = fwd(hist(w))
    return torch.cat([h, S[ii, pp] * wsup])


H0 = fwd(X0)[0].detach()


def h_only(y, t):
    return fwd(hist(torch.cat([y, t])))[0] - H0


def lift(t, track=True):
    """Newton for the exact fixed-h section y(t)."""
    t = torch.as_tensor(t, dtype=torch.float64); y = torch.zeros(n)
    res = math.inf
    for _ in range(30):
        f = h_only(y, t); res = float(f.abs().max())
        if res < 1e-15: break
        Hy = torch.func.jacfwd(lambda yy: h_only(yy, t))(y)
        y = y - torch.linalg.solve(Hy, f)
    res = float(h_only(y, t).abs().max())
    if track:
        STATS['lift_evals'] += 1
        STATS['max_lift_residual'] = max(STATS['max_lift_residual'], res)
        STATS['max_y_over_ah'] = max(STATS['max_y_over_ah'], float(y.abs().max()) / ah)
        if res > 1e-12: STATS['newton_failures'] += 1
    return y, res


# Fast numpy forward-mode implementation (same recurrence; cross-checked against the torch path in `validate`).
BN = Bm.numpy(); X0N = X0.numpy(); WN = Wm; DIAG = diag
OWN = np.array(ii); TYP = np.array([{'R': 0, 'W': 1, 'b': 2}[meta[p][0]] for i, p in support])
JJ = np.array([meta[p][2] for i, p in support]); WS = wsup.numpy(); H0N = H0.numpy()


def fwd_np(w):
    """h, normalized s, dh/dw (n x 11), ds/dw (24 x 11) at chart point w = (y, t)."""
    m = len(w); h = np.zeros(n); dh = np.zeros((n, m)); S = np.zeros(len(OWN)); dS = np.zeros((len(OWN), m))
    Rown = DIAG[OWN]
    for t in range(T):
        Bt = BN[t * n:(t + 1) * n]; x = X0N[t] + SD * (Bt @ w); dx = SD * Bt
        pre = DIAG * h + WN @ x + bvec; dpre = DIAG[:, None] * dh + WN @ dx
        hn = np.tanh(pre); g = 1 - hn * hn; dhn = g[:, None] * dpre; dg = -2 * hn[:, None] * dhn
        direct = np.where(TYP == 0, h[JJ], np.where(TYP == 1, x[JJ], 1.0))
        ddirect = np.where((TYP == 0)[:, None], dh[JJ], np.where((TYP == 1)[:, None], dx[JJ], 0.0))
        inner = Rown * S + direct; dinner = Rown[:, None] * dS + ddirect
        S, dS = g[OWN] * inner, dg[OWN] * inner[:, None] + g[OWN][:, None] * dinner
        h, dh = hn, dhn
    return h, S * WS, dh, dS * WS[:, None]


def lift_np(t, track=True):
    y = np.zeros(n); res = math.inf
    for _ in range(30):
        h, s, dh, ds = fwd_np(np.concatenate([y, t])); f = h - H0N; res = float(np.abs(f).max())
        if res < 1e-15: break
        y = y - np.linalg.solve(dh[:, :n], f)
    h, s, dh, ds = fwd_np(np.concatenate([y, t])); res = float(np.abs(h - H0N).max())
    if track:
        STATS['lift_evals'] += 1
        STATS['max_lift_residual'] = max(STATS['max_lift_residual'], res)
        STATS['max_y_over_ah'] = max(STATS['max_y_over_ah'], float(np.abs(y).max()) / ah)
        if res > 1e-12: STATS['newton_failures'] += 1
    return y, res, s, dh, ds


CACHE = {}


def point(z, jac=False, track=True):
    """s(x(y(Az),Az)); with jac, also ds/dt along the exact section (24 x 7)."""
    key = tuple(np.round(z, 15))
    if key in CACHE: return CACHE[key]
    t = aa * np.asarray(z, dtype=float)
    y, res, s, dh, ds = lift_np(t, track)
    Js = ds[:, n:] - ds[:, :n] @ np.linalg.solve(dh[:, :n], dh[:, n:])
    out = (s, Js, y, res)
    if len(CACHE) > 20000: CACHE.clear()
    CACHE[key] = out
    return out


def point_torch(z):
    t = torch.tensor(aa * np.asarray(z, dtype=float)); y, res = lift(t, track=False); w = torch.cat([y, t])
    J = torch.func.jacfwd(G)(w); Hy, Ht = J[:n, :n], J[:n, n:]
    Js = J[n:, n:] - J[n:, :n] @ torch.linalg.solve(Hy, Ht)
    return G(w)[n:].detach().numpy(), Js.detach().numpy(), y.numpy()


S0 = point(np.zeros(r), track=False)[0]
Psi0 = Lt.numpy() @ S0


def Phi(z, track=True):
    return (Kt.numpy() @ (Lt.numpy() @ point(z, track=track)[0] - Psi0)) / aa


def dphi0_matrix():
    _, J0, _, _ = point(np.zeros(r), jac=True, track=False)
    return (Kt.numpy() @ Lt.numpy() @ J0) * aa[None, :] / aa[:, None]


def DC(d, c=c_high):
    return float(np.sqrt(np.sum((c * d) ** 2)))


class Face:
    def __init__(self, face):
        self.i = face - 1

    def z(self, u):
        return np.insert(np.asarray(u, dtype=float), self.i, 1.0)

    def f(self, u):
        z = self.z(u)
        return DC(point(z)[0] - point(-z)[0])

    def fg(self, u):
        z = self.z(u)
        s1, J1, _, _ = point(z, jac=True); s2, J2, _, _ = point(-z, jac=True)
        d = s1 - s2; val = DC(d)
        gz = ((c_high ** 2) * d) @ ((J1 + J2) * aa[None, :]) / val
        return val, np.delete(gz, self.i)

    def dphi(self, u):
        z = self.z(u)
        s1, J1, _, _ = point(z, jac=True); s2, J2, _, _ = point(-z, jac=True)
        row = ellt[self.i]
        return float(row @ (s1 - s2)), np.delete(row @ ((J1 + J2) * aa[None, :]), self.i)


def local(fobj, x0, bounds):
    rr = minimize(fobj, x0, jac=True, method='L-BFGS-B', bounds=bounds,
                  options={'gtol': 1e-10, 'ftol': 1e-15, 'maxiter': 400})
    return float(rr.fun), np.asarray(rr.x), int(rr.nit)


def run_face(face, escalate=False, weakest=False):
    t0 = time.process_time(); F = Face(face); k = face - 1; m = r - 1
    double = (face == 5) or weakest
    seed_shift = (100 if escalate else 0) + (50 if weakest else 0)
    log = {'face': face, 'escalate': escalate, 'weakest_round': weakest, 'runs': []}
    # A: coarse screen
    grid = np.array(np.meshgrid(*[[-1., 0., 1.]] * m, indexing='ij')).reshape(m, -1).T
    sob = qmc.Sobol(m, scramble=True, seed=7000 + face + seed_shift).random(512 if double else 256) * 2 - 1
    pts = np.vstack([grid, sob])
    vals = np.array([F.f(u) for u in pts])
    order = np.argsort(vals)
    log['A'] = {'n': len(pts), 'best': float(vals[order[0]]), 'best_u': pts[order[0]].tolist()}
    bounds = [(-1., 1.)] * m
    # B: local multistart
    nb = 40 * (2 if double else 1) * (3 if escalate else 1)
    rng = np.random.default_rng(7100 + face + seed_shift)
    starts = [pts[j] for j in order[:nb]] + list(rng.uniform(-1, 1, (nb, m)))
    bestB = (math.inf, None)
    for x0 in starts:
        v, x, it = local(F.fg, x0, bounds); log['runs'].append(('B', v, x.tolist(), it))
        if v < bestB[0]: bestB = (v, x)
    # D: boundary search on codimension-2 sub-faces
    bestD = (math.inf, None)
    if not escalate:
        nd = 10 if double else 5
        for kk in range(m):
            for sg in (-1., 1.):
                sel = [j for j in order if pts[j][kk] == sg][:nd]
                bnd = [(sg, sg) if q == kk else (-1., 1.) for q in range(m)]
                for j in sel:
                    v, x, it = local(F.fg, pts[j], bnd); log['runs'].append(('D', v, x.tolist(), it))
                    if v < bestD[0]: bestD = (v, x)
    # C: differential evolution, then exact-gradient polish
    de = differential_evolution(F.f, bounds, popsize=(30 if (double or escalate) else 15), maxiter=60,
                                seed=7200 + face + seed_shift, tol=1e-12, atol=0, polish=False)
    vC, xC, itC = local(F.fg, de.x, bounds); log['runs'].append(('C', vC, xC.tolist(), itC))
    log['C'] = {'de_fun': float(de.fun), 'nfev': int(de.nfev), 'polished': vC, 'u': xC.tolist()}
    cands = [('B', *bestB), ('D', *bestD), ('C', vC, xC)]
    best = min((c for c in cands if c[2] is not None), key=lambda c: c[1])
    bd = min(bestB[0], bestD[0])
    log.update(best_value=best[1], best_method=best[0], best_u=best[2].tolist(), best_z=F.z(best[2]).tolist(),
               best_BD=bd, best_C=vC, reliable_BD_vs_C=abs(bd - vC) <= 0.01 * min(bd, vC),
               ratio_to_2eps=best[1] / (2 * EPS), ratio_to_2beta=best[1] / (2 * beta[k]),
               D78_at_best=DC(point(F.z(best[2]))[0] - point(-F.z(best[2]))[0], c_78),
               certified_2beta=2 * beta[k], stats=dict(STATS), cpu_seconds=time.process_time() - t0)
    tag = 'escalate' if escalate else 'weakest' if weakest else 'base'
    (OUT / f'face{face}_{tag}.json').write_text(json.dumps(log, indent=1))
    print(f"face {face} [{tag}]: best D_C {best[1]:.9e} ({best[0]}), /2eps {best[1]/2e-3:.4f}, /2beta {best[1]/(2*beta[k]):.4f}, "
          f"B/D {bd:.9e} C {vC:.9e}, reliable {log['reliable_BD_vs_C']}, max|y|/ah {STATS['max_y_over_ah']:.4f}, "
          f"max res {STATS['max_lift_residual']:.1e}, cpu {log['cpu_seconds']:.0f}s", flush=True)


def validate():
    out = {}
    exp_hash = hashlib.sha256((EXP / 'candidate.json').read_bytes()).hexdigest()
    out['V1_candidate_sha256_ok'] = exp_hash == '4d6ca2c2804790b55f24f4125471f322ca1f324252b3a1a173ef5bb3e2bf8c9c'
    mine = np.array([0.875 / (norm_factor * math.sqrt(sum(ellt[q, d] ** 2 / diag[i] ** 2 for d, (i, p) in enumerate(support))))
                     for q in range(r)])
    out['V2_mu_max_rel_err'] = float(np.max(np.abs(mine / mu - 1)))
    _, J0, y0, res0 = point(np.zeros(r), jac=True, track=False)
    DPhi0 = (Kt.numpy() @ Lt.numpy() @ J0) * aa[None, :] / aa[:, None]
    out['V3_max_abs_DPhi0_minus_I'] = float(np.max(np.abs(DPhi0 - np.eye(r))))
    out['center_lift_residual'] = res0
    rng = np.random.default_rng(1)
    xs = []
    for zz in [np.full(r, 0.3), np.full(r, -0.3)] + list(rng.uniform(-0.6, 0.6, (4, r))):
        s_np, J_np, y_np, _ = point(zz, track=False); s_t, J_t, y_t = point_torch(zz)
        xs.append(max(np.abs(s_np - s_t).max() / np.abs(s_t).max(), np.abs(J_np - J_t).max() / np.abs(J_t).max(), np.abs(y_np - y_t).max() / ah))
    out['numpy_vs_torch_max_rel_diff_interior'] = float(max(xs))
    CACHE.clear(); t = time.process_time()
    for zz in rng.uniform(-0.6, 0.6, (20, r)): point(zz, track=False)
    out['seconds_per_lift'] = (time.process_time() - t) / 20
    out['gate_ratio_DC_over_D78'] = GATE_HIGH / 0.875
    out['pass'] = (out['V1_candidate_sha256_ok'] and out['V2_mu_max_rel_err'] <= 1e-9 and out['V3_max_abs_DPhi0_minus_I'] <= 1e-6
                   and out['numpy_vs_torch_max_rel_diff_interior'] <= 1e-10)
    (OUT / 'validate.json').write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


def confirm(face):
    import mpmath as mp
    mp.mp.dps = 50
    best = min((json.loads(p.read_text()) for p in OUT.glob(f'face{face}_*.json')), key=lambda d: d['best_value'])
    z = np.array(best['best_z'])
    th = [mp.mpf(x.numerator) / x.denominator for x in theta_q]
    Rm = th[:n]; Wq = [th[n + i * n:n + (i + 1) * n] for i in range(n)]; bq = th[n + n * n:]
    X = [[mp.mpf(Q(v).numerator) / Q(v).denominator for v in row] for row in case['X']]
    Bq = [[mp.mpf(Q(v).numerator) / Q(v).denominator for v in row] for row in data['B']]
    a_q = [mp.mpf(Q(v).numerator) / Q(v).denominator for v in data['a']]
    sd = mp.sqrt(mp.mpf(3) / 32)
    rmsq = {g: mp.sqrt(sum(th[p] ** 2 for p, m in enumerate(meta) if m[0] == g) / sum(1 for m in meta if m[0] == g)) for g in 'RWb'}

    def run(w, want_dy):
        h = [mp.mpf(0)] * n; S = [[mp.mpf(0)] * P for _ in range(n)]; dh = [[mp.mpf(0)] * n for _ in range(n)]
        for t in range(T):
            x = [X[t][j] + sd * mp.fsum(Bq[t * n + j][c] * w[c] for c in range(n + r)) for j in range(n)]
            dx = [[sd * Bq[t * n + j][c] for c in range(n)] for j in range(n)]
            pre = [Rm[i] * h[i] + mp.fsum(Wq[i][j] * x[j] for j in range(n)) + bq[i] for i in range(n)]
            hn = [mp.tanh(v) for v in pre]; g = [1 - v * v for v in hn]
            Sn = [[mp.mpf(0)] * P for _ in range(n)]
            for p, (gr, i, j) in enumerate(meta):
                direct = h[j] if gr == 'R' else x[j] if gr == 'W' else mp.mpf(1)
                Sn[i][p] = g[i] * (Rm[i] * S[i][p] + direct)
                for i2 in range(n):
                    if i2 != i: Sn[i2][p] = g[i2] * Rm[i2] * S[i2][p]
            if want_dy:
                dh = [[g[i] * (Rm[i] * dh[i][c] + mp.fsum(Wq[i][j] * dx[j][c] for j in range(n))) for c in range(n)] for i in range(n)]
            h, S = hn, Sn
        return h, S, dh
    h0q = run([mp.mpf(0)] * (n + r), False)[0]

    def svec(zz):
        tq = [a_q[c] * mp.mpf(float(zz[c])) for c in range(r)]
        y = [mp.mpf(float(v)) for v in lift_np(aa * zz, track=False)[0]]
        for _ in range(8):
            h, S, dh = run(y + tq, True)
            f = mp.matrix([h[i] - h0q[i] for i in range(n)])
            if max(abs(v) for v in f) < mp.mpf(10) ** -45: break
            step = mp.lu_solve(mp.matrix(dh), f); y = [y[i] - step[i] for i in range(n)]
        h, S, _ = run(y + tq, False)
        resid = max(abs(h[i] - h0q[i]) for i in range(n))
        s = [S[i][p] * rmsq[meta[p][0]] for i, p in support]
        return s, resid, max(abs(v) for v in y)
    s1, r1, y1 = svec(z); s2, r2, y2 = svec(-z)
    d = [s1[q] - s2[q] for q in range(len(support))]
    gh = 1 - mp.tanh(mp.mpf(1) / 4) ** 2; nf = mp.sqrt(n * max(mp.mpf(1), sum(v ** 2 for v in Rm)))
    DCq = mp.sqrt(mp.fsum((gh * Rm[i] / nf * d[q]) ** 2 for q, (i, p) in enumerate(support)))
    D78q = DCq * mp.mpf(7) / 8 / gh
    k = face - 1
    dphi = mp.fsum(mp.mpf(float(ellt[k, q])) * d[q] for q in range(len(support)))  # ellt rounded to float: diagnostic only
    out = {'face': face, 'z': z.tolist(), 'DC_mp50': mp.nstr(DCq, 20), 'D78_mp50': mp.nstr(D78q, 20),
           'DC_float64': best['best_value'], 'rel_diff': float(abs(DCq / best['best_value'] - 1)),
           'lift_residual_mp': mp.nstr(max(r1, r2), 5), 'max_y_over_ah_mp': float(max(y1, y2) / ah),
           'dphi_i_mp_approx': mp.nstr(dphi, 12), 'ratio_to_2eps': float(DCq / (2 * EPS))}
    (OUT / f'confirm_face{face}.json').write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


def third_derivative_sup(F, z, h):
    """max over 41 s in [-1,1] of |d^3/ds^3 Phi_i(s z)|, 4th-order central differences (stencil may reach |s|<=1+3h)."""
    g = lambda s: Phi(s * z, track=False)[F.i]
    best = 0.0
    for s in np.linspace(-1, 1, 41):
        v = (-g(s + 3 * h) + 8 * g(s + 2 * h) - 13 * g(s + h) + 13 * g(s - h) - 8 * g(s - 2 * h) + g(s - 3 * h)) / (8 * h ** 3)
        best = max(best, abs(v))
    return best


def curv(face):
    t0 = time.process_time(); F = Face(face); k = face - 1
    best = min((json.loads(p.read_text()) for p in OUT.glob(f'face{face}_*.json')), key=lambda d: d['best_value'])
    z = np.array(best['best_z'])
    s1 = point(z)[0]; s2 = point(-z)[0]; d = s1 - s2
    DCv, D78v = DC(d), DC(d, c_78); dphi = float(ellt[k] @ d)
    Gs = {h: third_derivative_sup(F, z, h) for h in (0.02, 0.01)}
    Gi = max(Gs.values())
    lin_true = 2 * mu[k] * (1 - e0[k] - Gi / 6)
    lin2 = float(2 * (dphi0_matrix() @ z)[k])
    terms = {'gate': math.log(DCv / D78v), 'query_linear_range': math.log(D78v / (mu[k] * abs(dphi))),
             'third_order_remainder': math.log(abs(dphi) / (2 * (1 - e0[k] - Gi / 6))),
             'interval_curvature': math.log((1 - e0[k] - Gi / 6) / (1 - e0[k] - M3[k] / 6))}
    # Face-wide true-curvature estimate: 200 random face rays + 64 face corners
    rng = np.random.default_rng(7300 + face)
    rays = [F.z(u) for u in rng.uniform(-1, 1, (200, r - 1))]
    rays += [F.z(np.array(c, dtype=float)) for c in np.array(np.meshgrid(*[[-1., 1.]] * (r - 1), indexing='ij')).reshape(r - 1, -1).T]
    Ghat = max(third_derivative_sup(F, zz, 0.02) for zz in rays)
    # min |DeltaPhi_i| over the face (20 L-BFGS-B starts)
    starts = [np.array(best['best_u'])] + list(rng.uniform(-1, 1, (19, r - 1)))
    mins = [local(F.dphi, x0, [(-1., 1.)] * (r - 1))[0] for x0 in starts]
    out = {'face': face, 'z_star': z.tolist(), 'DC': DCv, 'D78': D78v, 'mu': mu[k], 'mu_dphi': mu[k] * abs(dphi), 'dphi': dphi,
           'G_ray_by_step': Gs, 'G_ray': Gi, 'M3': M3[k], 'G_ray_over_M3': Gi / M3[k],
           'linear_part_2DPhi0z': lin2, 'odd_remainder_actual': abs(dphi - lin2),
           'odd_remainder_over_M3_third': abs(dphi - lin2) / (M3[k] / 3), 'odd_remainder_over_Gray_third': abs(dphi - lin2) / (Gi / 3),
           'two_beta': 2 * beta[k], 'oracle_ray_bound': lin_true, 'log_terms': terms,
           'log_total': math.log(DCv / (2 * beta[k])), 'G_face_hat': Ghat, 'G_face_hat_over_M3': Ghat / M3[k],
           'oracle_face_bound': 2 * mu[k] * (1 - e0[k] - Ghat / 6), 'min_dphi_face': min(mins),
           'mu_min_dphi_face': mu[k] * min(mins), 'stats': dict(STATS), 'cpu_seconds': time.process_time() - t0}
    (OUT / f'curv_face{face}.json').write_text(json.dumps(out, indent=1))
    print(json.dumps({key: out[key] for key in ('face', 'DC', 'D78', 'mu_dphi', 'two_beta', 'G_ray', 'M3', 'G_face_hat',
                                                  'oracle_face_bound', 'mu_min_dphi_face', 'log_terms', 'log_total')}, indent=1), flush=True)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'validate': validate()
    elif mode == 'face': run_face(int(sys.argv[2]), escalate='--escalate' in sys.argv, weakest='--weakest' in sys.argv)
    elif mode == 'confirm': confirm(int(sys.argv[2]))
    elif mode == 'curv': curv(int(sys.argv[2]))
