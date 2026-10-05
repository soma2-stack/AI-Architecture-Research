"""Claude's independent hostile review of the exact-elimination / sharp-gate / radial-Taylor 8D refinement.

Reads experiments/radial_taylor_refinement_8d_20261001 read-only (numerical attacks + replays; evidence, not proofs).
modes:
  replay BITS        their functions, fresh in my process: control, coefficients, native, 8 bands, beta vs stored
  coeff              my own 60-digit derivation of C_S / C_h from the proof's formulas vs their interval enclosures
  identity N         true fixed-h section: l.(s_T(t)-s_T(0)) vs C_S.dS_prefix + C_h.dv_prefix (no elimination assumed)
  gates N            sharp polynomial gate bounds vs 50-digit true maxima on adversarial H-intervals
  prefmaj J N        autodiff prefix 2nd/3rd derivatives in the lambda_J tangent box vs prefix_192_J bounds (+ adversarial)
  radial N           end-to-end |d^3/ds^3 Phi_i(s z)| on the TRUE section vs each band's M_used, for |s| <= lambda_J
  remainder          |Phi(z)-Phi(-z)-2DPhi(0)z|_i vs the new integrated bound 2 B_i at boundary antipodes
  cleanroom          clean-room engine jets on the 36-step prefix (zero normal width) -> my own M contraction
"""
import os
for _k in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[_k] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import sys, json, math, time, hashlib
sys.dont_write_bytecode = True
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
EXP = HERE.parent / 'radial_taylor_refinement_8d_20261001'
OLD8 = HERE.parent / 'third_order_antipodal_8d_20261001'
OUT = HERE / 'out'; OUT.mkdir(exist_ok=True)
mode = sys.argv[1]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(EXP / 'candidate.json') == 'c83a242f6de829542fcf57c7b98beae6fc90be079d479b169a624e832f27cd0c' == sha(OLD8 / 'candidate.json')
data = json.loads((EXP / 'candidate.json').read_text())
res8 = json.loads((EXP / 'result8.json').read_text())
att = {a['bits']: a for a in res8['attempts']}
case = data['endpoint']; n = case['n']; r = data['r']; s_dim = n + r
ctrl = att[192]['control']


def dump(name, obj): (OUT / name).write_text(json.dumps(obj, indent=1, default=float))


def qi(pair): return (Q(pair[0]) + Q(pair[1])) / 2


def coeff_mid(bits=192):
    c = json.loads((EXP / f'coefficients_{bits}.json').read_text())
    CS = np.array([[float(qi(x)) for x in row] for row in c['CS']]); CH = np.array([[float(qi(x)) for x in row] for row in c['CH']])
    return c, CS, CH


# ------------------------------------------------------------------ replay of their pipeline (their code, my process)
if mode == 'replay':
    bits = int(sys.argv[2]); sys.path.insert(0, str(EXP))
    import common as c
    from elimination import coefficients, prefix_bound
    c.verify(); t0 = time.process_time()
    aa = list(map(Q, data['a'])); ah = Q(data['ah']); B, L, Kh, K = [c.rows(data[v]) for v in ('B', 'L', 'K_hidden', 'K_selected')]
    ell = [[sum(K[i][j] * L[j][p] for j in range(8)) / aa[i] for p in range(24)] for i in range(8)]
    base = c.ref.a.base_for(data['endpoint'], B, bits, JI=None)
    ctrl_out, arrays = c.ref.certify(base, aa, ah, L, Kh, K)
    st = att[bits]; out = {'bits': bits}
    cb = np.load(EXP / f'control_bounds_{bits}.npz'); out['control_arrays_identical'] = all(np.array_equal(arrays[k2], cb[k2]) for k2 in cb.files)
    out['control_fields_identical'] = all(ctrl_out.get(k2) == st['control'].get(k2) for k2 in st['control'])
    CS, CH, meta = coefficients(base, ell); cj = json.loads((EXP / f'coefficients_{bits}.json').read_text())
    sc = c.ref.I.scale
    out['coefficients_identical'] = ([[[str(Q(x.lo, sc)), str(Q(x.hi, sc))] for x in row] for row in CS] == cj['CS'] and
                                     [[[str(Q(x.lo, sc)), str(Q(x.hi, sc))] for x in row] for row in CH] == cj['CH'])
    native, arr = prefix_bound(base, aa, Q(1), CS, CH, c.ref); nb = np.load(EXP / f'elimination_native_{bits}.npz')
    out['native_arrays_identical'] = all(np.array_equal(arr[k2], nb[k2]) for k2 in nb.files)
    out['native_M_identical'] = list(map(str, native)) == st['native_elimination_M3']
    bands_ok = []; Ms = []
    for j in range(1, 9):
        M, arr = prefix_bound(base, aa, Q(j, 8), CS, CH, c.tight); pb = np.load(EXP / f'prefix_{bits}_{j}.npz')
        bands_ok.append(all(np.array_equal(arr[k2], pb[k2]) for k2 in pb.files) and list(map(str, M)) == st['bands'][j - 1]['M3_original_direction'])
        Ms.append(M)
    out['bands_identical'] = bands_ok
    e = list(map(Q, ctrl_out['center_rows_upper'])); mu = list(map(Q, ctrl_out['mu_tilde']))
    pen = [sum(((1 - Q(j, 8)) ** 3 - (1 - Q(j + 1, 8)) ** 3) / 3 * min(Ms[j][i], Q(ctrl_out['M3_upper'][i])) / 2 for j in range(8)) for i in range(8)]
    beta = [mu[i] * (1 - e[i] - pen[i]) for i in range(8)]
    out['beta_identical_to_stored'] = list(map(str, beta)) == st['beta']
    out['all_beta_gt_eps'] = all(b > Q(1, 1000) for b in beta); out['two_beta'] = [float(2 * b) for b in beta]
    out['cpu_seconds'] = time.process_time() - t0
    dump(f'replay_{bits}.json', out); print(json.dumps(out), flush=True); sys.exit()

if mode == 'precision':
    a, b = att[192], att[256]
    d = max(abs(Q(x) - Q(y)) for x, y in zip(a['beta'], b['beta']))
    same_bands = all(x['M3_original_direction'] == y['M3_original_direction'] for x, y in zip(a['bands'], b['bands']))
    arrays = all(np.array_equal(np.load(EXP / f'prefix_192_{j}.npz')[k2], np.load(EXP / f'prefix_256_{j}.npz')[k2])
                 for j in range(1, 9) for k2 in np.load(EXP / f'prefix_192_{j}.npz').files)
    w = [((1 - Q(j - 1, 8)) ** 3 - (1 - Q(j, 8)) ** 3) / 3 for j in range(1, 9)]
    weights_ok = [str(x) for x in w] == [bb['weight'] for bb in a['bands']] and sum(w) == Q(1, 3)
    # Sharp gates must never exceed natural gates: band 8 (lambda=1, sharp) <= native (lambda=1, natural), elementwise.
    nat = np.load(EXP / 'elimination_native_192.npz'); sh8 = np.load(EXP / 'prefix_192_8.npz')
    le = {k2: bool(np.all(sh8[k2] <= nat[k2])) for k2 in nat.files}
    mono = all(Q(a['bands'][j]['M3_original_direction'][i]) <= Q(a['bands'][j + 1]['M3_original_direction'][i]) for j in range(7) for i in range(8))
    out = {'max_beta_192_256_diff': float(d), 'bands_identical_192_256': same_bands, 'prefix_arrays_bitwise_192_256': arrays,
           'weights_exact_and_sum_1_3': weights_ok, 'sharp_le_natural_elementwise': le, 'M_monotone_in_lambda': mono,
           'mu_e0_from_unchanged_control': [a['control']['mu_tilde'] == json.loads((OLD8 / 'result.json').read_text())['attempts'][0]['certificate']['mu_tilde'],
                                            a['control']['center_rows_upper'] == json.loads((OLD8 / 'result.json').read_text())['attempts'][0]['certificate']['center_rows_upper']]}
    dump('precision_checks.json', out); print(json.dumps(out), flush=True); sys.exit()

# ------------------------------------------------------------------ own float64 model (independent of their code)
import torch
torch.set_default_dtype(torch.float64); torch.set_num_threads(1)
theta_q = [Q(x) for x in data['model_parameters']]; theta = [float(x) for x in theta_q]
Rd = np.array(theta[:n]); Wm = np.array(theta[n:n + n * n]).reshape(n, n); bvec = np.array(theta[n + n * n:])
meta = [('R', i, i) for i in range(n)] + [('W', i, j) for i in range(n) for j in range(n)] + [('b', i, 0) for i in range(n)]
P = len(meta)
rms = {g: math.sqrt(np.mean(np.square([theta[p] for p, m in enumerate(meta) if m[0] == g]))) for g in 'RWb'}
support = [(i, p) for i in range(n) for p, (g, o, _) in enumerate(meta) if o == i]
ii = [i for i, p in support]; pp = [p for i, p in support]
OWN = np.array(ii); TYP = np.array([{'R': 0, 'W': 1, 'b': 2}[meta[p][0]] for i, p in support]); JJ = np.array([meta[p][2] for i, p in support])
WS = np.array([rms[meta[p][0]] for i, p in support])
X0N = np.array([[float(Q(v)) for v in row] for row in case['X']]); T = X0N.shape[0]; SD = math.sqrt(3 / 32)
BN = np.array([[float(Q(v)) for v in row] for row in data['B']]); LN = np.array([[float(Q(v)) for v in row] for row in data['L']])
KN = np.array([[float(Q(v)) for v in row] for row in data['K_selected']])
aa = np.array([float(Q(v)) for v in data['a']]); ah = float(Q(data['ah']))
ellN = (KN @ LN) / aa[:, None]
mu = np.array([float(Q(v)) for v in ctrl['mu_tilde']]); e0 = np.array([float(v) for v in ctrl['center_rows_upper']])
beta_new = np.array([float(Q(v)) for v in att[192]['beta']]); B_half = np.array([float(Q(v)) for v in att[192]['integrated_half_remainder']])
lams = [j / 8 for j in range(1, 9)]
M_used = np.array([[float(Q(v)) for v in b['M3_used']] for b in att[192]['bands']])   # band x face
STATS = {'max_lift_residual': 0.0, 'max_y_over_ah': 0.0, 'newton_failures': 0}


def run_np(w, steps=None):
    """h, normalized support s, dh/dw, ds/dw after `steps` steps (default all T)."""
    steps = T if steps is None else steps; m = len(w)
    h = np.zeros(n); dh = np.zeros((n, m)); S = np.zeros(len(OWN)); dS = np.zeros((len(OWN), m)); Rown = Rd[OWN]
    for t in range(steps):
        Bt = BN[t * n:(t + 1) * n]; x = X0N[t] + SD * (Bt @ w); dx = SD * Bt
        pre = Rd * h + Wm @ x + bvec; dpre = Rd[:, None] * dh + Wm @ dx
        hn = np.tanh(pre); g = 1 - hn * hn; dhn = g[:, None] * dpre; dg = -2 * hn[:, None] * dhn
        direct = np.where(TYP == 0, h[JJ], np.where(TYP == 1, x[JJ], 1.0))
        ddirect = np.where((TYP == 0)[:, None], dh[JJ], np.where((TYP == 1)[:, None], dx[JJ], 0.0))
        inner = Rown * S + direct; dinner = Rown[:, None] * dS + ddirect
        S, dS = g[OWN] * inner, dg[OWN] * inner[:, None] + g[OWN][:, None] * dinner
        h, dh = hn, dhn
    return h, S * WS, dh, dS * WS[:, None]


H0N = run_np(np.zeros(s_dim))[0]


def lift(t, track=True):
    y = np.zeros(n)
    for _ in range(30):
        h, s, dh, ds = run_np(np.concatenate([y, t])); f = h - H0N
        if np.abs(f).max() < 1e-15: break
        y = y - np.linalg.solve(dh[:, :n], f)
    h, s, dh, ds = run_np(np.concatenate([y, t])); res = float(np.abs(h - H0N).max())
    if track:
        STATS['max_lift_residual'] = max(STATS['max_lift_residual'], res); STATS['max_y_over_ah'] = max(STATS['max_y_over_ah'], float(np.abs(y).max()) / ah)
        if res > 1e-12: STATS['newton_failures'] += 1
    return y, s, dh, ds


S0 = lift(np.zeros(r), track=False)[1]


def Phi(z): return ellN @ (lift(aa * np.asarray(z, float))[1] - S0)


def dphi0():
    y, s, dh, ds = lift(np.zeros(r), track=False)
    Js = ds[:, n:] - ds[:, :n] @ np.linalg.solve(dh[:, :n], dh[:, n:])
    return (ellN @ Js) * aa[None, :]


if mode == 'coeff':
    import mpmath as mp
    mp.mp.dps = 60
    c, CS, CH = coeff_mid(192)
    mq = lambda x: mp.mpf(x.numerator) / x.denominator
    th = [mq(x) for x in theta_q]; Rq = th[:n]; Wq = mp.matrix([[th[n + i * n + j] for j in range(n)] for i in range(n)]); bq = th[n + n * n:]
    h = [mp.mpf(0)] * n
    for row in case['X']:
        x = [mq(Q(v)) for v in row]; h = [mp.tanh(Rq[i] * h[i] + mp.fsum(Wq[i, j] * x[j] for j in range(n)) + bq[i]) for i in range(n)]
    g = [1 - v * v for v in h]; Wi = Wq ** -1
    rmsq = {gname: mp.sqrt(mp.fsum(th[p] ** 2 for p, m in enumerate(meta) if m[0] == gname) / sum(1 for m in meta if m[0] == gname)) for gname in 'RWb'}
    Kq = [[Q(v) for v in row] for row in data['K_selected']]; Lq = [[Q(v) for v in row] for row in data['L']]; aq = [Q(v) for v in data['a']]
    worst_out = 0; worst_rel = 0.
    for a_ in range(r):
        ell = [mq(sum(Kq[a_][j] * Lq[j][q] for j in range(r)) / aq[a_]) for q in range(24)]
        mine_S = [ell[q] * g[o] * Rq[o] for q, (o, p) in enumerate(support)]
        mine_H = [mp.mpf(0)] * n
        for q, (o, p) in enumerate(support):
            gname, i, j = meta[p]
            if gname == 'R': mine_H[j] += ell[q] * rmsq['R'] * g[o]                      # direct term v_j (j == o)
            elif gname == 'W':
                for kk in range(n): mine_H[kk] -= ell[q] * rmsq['W'] * g[o] * Wi[j, kk] * Rq[kk]   # x_T,j = c - (W^-1 D v)_j
        for q in range(24):
            lo, hi = (mq(Q(v)) for v in c['CS'][a_][q]); worst_out = max(worst_out, float(max(lo - mine_S[q], mine_S[q] - hi, 0)))
            worst_rel = max(worst_rel, float(abs(mine_S[q] - (lo + hi) / 2) / max(abs(mine_S[q]), mp.mpf(10) ** -40)))
        for kk in range(n):
            lo, hi = (mq(Q(v)) for v in c['CH'][a_][kk]); worst_out = max(worst_out, float(max(lo - mine_H[kk], mine_H[kk] - hi, 0)))
            worst_rel = max(worst_rel, float(abs(mine_H[kk] - (lo + hi) / 2) / max(abs(mine_H[kk]), mp.mpf(10) ** -40)))
    out = {'my_60digit_values_outside_their_intervals_by': worst_out, 'max_rel_diff_to_interval_mid': worst_rel,
           'contained': worst_out == 0, 'max_abs_CS': float(np.abs(CS).max()), 'max_abs_CH': float(np.abs(CH).max())}
    dump('coeff_check.json', out); print(json.dumps(out), flush=True); sys.exit()

if mode == 'identity':
    N = int(sys.argv[2]); rng = np.random.default_rng(31); c, CS, CH = coeff_mid(192)
    hP0, sP0, _, _ = run_np(np.zeros(s_dim), steps=T - 1)
    worst = 0.; scale = 0.; pts = []
    for q in range(N):
        z = rng.choice([-1., 1.], r) if q % 3 == 0 else rng.uniform(-1, 1, r)
        if q % 3 == 1: z[rng.integers(r)] = rng.choice([-1., 1.])
        pts.append(z)
    for z in pts:
        t = aa * z; y, s, _, _ = lift(t)
        hP, sP, _, _ = run_np(np.concatenate([y, t]), steps=T - 1)     # prefix (does not depend on y)
        hP2, sP2, _, _ = run_np(np.concatenate([np.zeros(n), t]), steps=T - 1)
        assert np.allclose(hP, hP2, atol=0, rtol=0) and np.allclose(sP, sP2, atol=0, rtol=0)
        lhs = ellN @ (s - S0); rhs = CS @ (sP - sP0) + CH @ (hP - hP0)
        worst = max(worst, float(np.abs(lhs - rhs).max())); scale = max(scale, float(np.abs(lhs).max()))
    out = {'points': N, 'max_abs_identity_error': worst, 'max_abs_Phi_change': scale, 'relative': worst / scale,
           'prefix_independent_of_normals': True, 'stats': dict(STATS)}
    dump('identity_check.json', out); print(json.dumps(out), flush=True); sys.exit()

if mode == 'gates':
    import mpmath as mp
    mp.mp.dps = 50
    N = int(sys.argv[2]); sys.path.insert(0, str(EXP)); sys.path.insert(0, str(HERE.parent / 'antipodal_robust_dimension_20261001'))
    from exact_gate import gate_majorants, POLYS
    from antipodal_kernel import I
    rng = np.random.default_rng(41); worst = [math.inf] * 4; vs_nat = [0.] * 4; cases = 0
    crit = [[mp.mpf(0)], [mp.sqrt(mp.mpf(1) / 3), -mp.sqrt(mp.mpf(1) / 3)], [mp.mpf(0), mp.sqrt(mp.mpf(2) / 3), -mp.sqrt(mp.mpf(2) / 3)],
            [s * mp.sqrt((15 + e * mp.sqrt(105)) / 30) for s in (1, -1) for e in (1, -1)]]
    special = [float(v) for row in crit for v in row]
    for bits in (192, 256):
        I.precision(bits)
        for q in range(N):
            kind = q % 4
            if kind == 0: lo, hi = sorted(rng.uniform(-0.999, 0.999, 2))
            elif kind == 1: cpt = rng.choice(special); w = 10 ** rng.uniform(-12, -2); lo, hi = cpt - w * rng.uniform(), cpt + w * rng.uniform()
            elif kind == 2: cpt = rng.choice(special); w = 10 ** rng.uniform(-14, -4); lo, hi = (cpt + w, cpt + 2 * w) if rng.uniform() < .5 else (cpt - 2 * w, cpt - w)
            else: x = rng.uniform(-0.999, 0.999); w = 10 ** rng.uniform(-15, -1); lo, hi = x, min(x + w, 0.9999)
            lo_r = math.floor(lo * 2 ** 60); hi_r = math.ceil(hi * 2 ** 60)
            H = I(lo_r << (bits - 60), hi_r << (bits - 60), True)
            bounds = gate_majorants([H]); L_, U_ = mp.mpf(lo_r) / 2 ** 60, mp.mpf(hi_r) / 2 ** 60
            g = I(1) - H.square()
            nat = (Q(g.hi, I.scale), (2 * H * g).absq(), (-2 * g * (I(1) - 3 * H.square())).absq(), (8 * H * g * (I(2) - 3 * H.square())).absq())
            for j in range(4):
                pts = [L_, U_] + [v for v in crit[j] if L_ <= v <= U_]
                true = max(abs(mp.polyval(list(reversed(POLYS[j])), v)) for v in pts)
                if true > 0: worst[j] = min(worst[j], float(mp.mpf(float(bounds[j][0])) / true))
                vs_nat[j] = max(vs_nat[j], float(Q(float(bounds[j][0])) / max(nat[j], Q(1, 10 ** 300))))
            cases += 1
    out = {'intervals': cases, 'min_bound_over_true_max': worst, 'max_bound_over_natural': vs_nat,
           'reading': 'min ratio must be >= 1 (valid); max_bound_over_natural <= 1 + ulp (never looser)'}
    dump('gates_check.json', out); print(json.dumps(out), flush=True); sys.exit()

# prefix map in torch: tangent t (8) -> (v = h_{T-1}, normalized support s_{T-1})
ER = torch.zeros(n, P, n); EW = torch.zeros(n, P, n); Eb = torch.zeros(n, P)
for p, (g_, i, j) in enumerate(meta):
    if g_ == 'R': ER[i, p, j] = 1.
    elif g_ == 'W': EW[i, p, j] = 1.
    else: Eb[i, p] = 1.
Rt = torch.diag(torch.tensor(Rd)); Wt = torch.tensor(Wm); bt = torch.tensor(bvec); X0 = torch.tensor(X0N); Bt_ = torch.tensor(BN); wsup = torch.tensor(WS)


def Gp(tt):
    x = X0 + (SD * (Bt_[:, n:] @ tt)).reshape(T, n); h = torch.zeros(n); S = torch.zeros(n, P)
    for t in range(T - 1):
        direct = torch.einsum('ipj,j->ip', ER, h) + torch.einsum('ipj,j->ip', EW, x[t]) + Eb
        hn = torch.tanh(Rt @ h + Wt @ x[t] + bt); g = 1 - hn * hn; S = g[:, None] * (Rt @ S + direct); h = hn
    return torch.cat([h, S[ii, pp] * wsup])


if mode == 'prefmaj':
    J, N = int(sys.argv[2]), int(sys.argv[3]); lam = J / 8; rng = np.random.default_rng(500 + J)
    bd = np.load(EXP / f'prefix_192_{J}.npz')
    M3 = np.concatenate([bd['HH3'][:, n:, n:, n:], bd['HS3'][:, n:, n:, n:]]); M2 = np.concatenate([bd['HH'][:, n:, n:], bd['HS'][:, n:, n:]])
    d2 = torch.func.jacfwd(torch.func.jacrev(Gp)); d3 = torch.func.jacfwd(d2); w2 = w3 = 0.; best = []
    for q in range(N):
        t = lam * aa * (rng.choice([-1., 1.], r) if q % 2 == 0 else rng.uniform(-1, 1, r)); tt = torch.tensor(t)
        T3 = np.abs(d3(tt).detach().numpy()) / np.maximum(M3, 1e-300); T2 = np.abs(d2(tt).detach().numpy()) / np.maximum(M2, 1e-300)
        w3 = max(w3, float(T3.max())); w2 = max(w2, float(T2.max()))
        for flat in np.argsort(T3.ravel())[-4:]: best.append((float(T3.flat[flat]), np.unravel_index(int(flat), T3.shape), t))
    E = torch.eye(r); adv = 0.
    for r0, idx, t0 in sorted(best, key=lambda v: -v[0])[:8]:
        o, dirs = idx[0], idx[1:]; f = Gp
        for dd in dirs[::-1]: f = (lambda gg, e: (lambda v: torch.func.jvp(gg, (v,), (e,))[1]))(f, E[dd])
        bound = float(M3[idx]); sg = float(np.sign(float(f(torch.tensor(t0))[o]))) or 1.

        def obj(t, f=f, o=o, sg=sg, bound=bound):
            tt = torch.tensor(t, requires_grad=True); v = sg * f(tt)[o] / bound; v.backward(); return -float(v.detach()), -tt.grad.numpy()
        rr = minimize(obj, t0, jac=True, method='L-BFGS-B', bounds=list(zip(-lam * aa, lam * aa)), options={'maxiter': 60}); adv = max(adv, -float(rr.fun))
    out = {'band': J, 'lambda': lam, 'points': N, 'max_third_over_bound': w3, 'max_second_over_bound': w2, 'adversarial_third_over_bound': adv}
    dump(f'prefmaj_{J}.json', out); print(json.dumps(out), flush=True); sys.exit()

if mode == 'radial':
    N = int(sys.argv[2]); rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 61); h = 0.01
    worst = np.zeros((8, r)); worst_any = np.zeros(r)
    for q in range(N):
        z = rng.uniform(-1, 1, r)
        if q % 2 == 0: z[rng.integers(r)] = rng.choice([-1., 1.])
        if q % 5 == 0: z = rng.choice([-1., 1.], r)
        s = rng.choice([-1., 1.]) * rng.choice(lams + [rng.uniform(0, 1)])
        g = lambda u: Phi(u * z)
        d3 = np.abs((-g(s + 3 * h) + 8 * g(s + 2 * h) - 13 * g(s + h) + 13 * g(s - h) - 8 * g(s - 2 * h) + g(s - 3 * h)) / (8 * h ** 3))
        for j, lam in enumerate(lams):
            if abs(s) <= lam + 1e-12: worst[j] = np.maximum(worst[j], d3 / M_used[j])
        worst_any = np.maximum(worst_any, d3)
    out = {'samples': N, 'max_ratio_actual_over_M_used_by_band_and_face': worst.tolist(), 'overall_max_ratio': float(worst.max()),
           'max_actual_third_derivative_by_face': worst_any.tolist(), 'stats': dict(STATS)}
    dump(f'radial_{sys.argv[3] if len(sys.argv) > 3 else 61}.json', out); print(json.dumps({k: out[k] for k in ('samples', 'overall_max_ratio')}), flush=True); sys.exit()

if mode == 'remainder':
    D = dphi0(); rng = np.random.default_rng(71)
    pts = [np.array(c) for c in np.array(np.meshgrid(*[[-1., 1.]] * r, indexing='ij')).reshape(r, -1).T if c[0] > 0]
    for _ in range(400):
        z = rng.uniform(-1, 1, r); z[rng.integers(r)] = rng.choice([-1., 1.]); pts.append(z)
    worst = np.zeros(r); worst_old = np.zeros(r); M3old = np.array(ctrl['M3_upper'])
    for z in pts:
        rem = np.abs(Phi(z) - Phi(-z) - 2 * D @ z); worst = np.maximum(worst, rem / (2 * B_half)); worst_old = np.maximum(worst_old, rem / (M3old / 3))
    out = {'pairs': len(pts), 'max_DPhi0_minus_I': float(np.abs(D - np.eye(r)).max()), 'remainder_over_new_bound_2B': worst.tolist(),
           'remainder_over_old_bound_M3_3': worst_old.tolist(), 'stats': dict(STATS)}
    dump('remainder.json', out); print(json.dumps(out), flush=True); sys.exit()

if mode == 'cleanroom':
    # Second implementation of the eliminated whole-box (lambda) bound: clean-room jets on the 36-step prefix.
    sys.path.insert(0, str(HERE / 'cleanroom'))
    from arithmetic import set_precision
    import replay as cr
    lamq = Q(sys.argv[2]) if len(sys.argv) > 2 else Q(1); set_precision(192)
    c2 = {'endpoint': dict(case, X=case['X'][:-1]), 'model_parameters': data['model_parameters'], 'B': data['B'][:-n],
          'a': [str(lamq * Q(v)) for v in data['a']], 'ah': '0', 'r': r}
    raw, dom = cr.bound_jets(c2)
    HH3 = np.vectorize(lambda x: x.float_up(), otypes=[float])(raw['HH3']); HS3 = np.vectorize(lambda x: x.float_up(), otypes=[float])(raw['HS3'])
    cj = json.loads((EXP / 'coefficients_192.json').read_text())
    absCS = np.array([[float(max(abs(Q(x[0])), abs(Q(x[1])))) for x in row] for row in cj['CS']]); absCH = np.array([[float(max(abs(Q(x[0])), abs(Q(x[1])))) for x in row] for row in cj['CH']])
    PHI3 = np.einsum('iq,qabc->iabc', absCS, HS3[:, n:, n:, n:]) + np.einsum('ik,kabc->iabc', absCH, HH3[:, n:, n:, n:])
    M = np.einsum('iabc,a,b,c->i', PHI3, aa, aa, aa) * (1 + 1e-12)
    j = int(lamq * 8)
    ref_nat = [float(Q(v)) for v in att[192]['native_elimination_M3']] if lamq == 1 else None
    ref_sharp = [float(Q(v)) for v in att[192]['bands'][j - 1]['M3_original_direction']]
    nat = np.load(EXP / 'elimination_native_192.npz') if lamq == 1 else None
    out = {'lambda': str(lamq), 'cleanroom_M': M.tolist(), 'codex_sharp_band_M': ref_sharp,
           'cleanroom_over_sharp': (M / np.array(ref_sharp)).tolist()}
    if lamq == 1:
        out['codex_native_M'] = ref_nat; out['cleanroom_over_native'] = (M / np.array(ref_nat)).tolist()
        out['HH3_rel_diff_vs_native'] = float(np.max(np.abs(HH3 - nat['HH3']) / np.maximum(nat['HH3'], 1e-300)))
        out['HS3_rel_diff_vs_native'] = float(np.max(np.abs(HS3 - nat['HS3']) / np.maximum(nat['HS3'], 1e-300)))
    dump(f'cleanroom_prefix_{j}.json', out); print(json.dumps(out), flush=True); sys.exit()
