"""Claude's independent hostile review of the rebalanced 7D certificate (numerical attacks + replays; evidence, not proofs).

Reads experiments/rebalanced_7d_section_20261001 read-only.
modes:
  replay BITS          fresh cache-free whole-box certificate with the LOCAL kernel; compare every field/array
  accepted             frozen candidate through the UNCHANGED accepted 6D kernel (diagnostic only, not a certificate)
  exact                exact rational re-derivation of every face inequality + independent mu / hidden self-map
  affine SEED N        instrumented local kernel: per-step preactivation / first-derivative enclosures vs truth
  majorant SEED N      autodiff 2nd/3rd derivatives of (h, s) at 11-D box points vs HH/HS/HH3/HS3
  fd SEED N            finite-difference D^3 Phi along the curved exact section vs certified selected3 bound
  core                 DPhi(0), odd remainder vs M3/3 at boundary antipodes, hidden usage, min distances
  face F [--deep]      adversarial antipodal minimisation on face F (1-based)
  confirm F            50-digit recomputation at face F's best point
  curv F               slack attribution on face F
"""
import os
for _k in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[_k] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import sys, json, math, time, hashlib, types, importlib.util
sys.dont_write_bytecode = True
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.stats import qmc

HERE = Path(__file__).resolve().parent
EXP = HERE.parent / 'rebalanced_7d_section_20261001'
ACC = HERE.parent / 'third_order_antipodal_20261001'
OUT = HERE / 'out'; OUT.mkdir(exist_ok=True)
EPS = 1e-3
mode = sys.argv[1]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(EXP / 'candidate.json') == '87895c3f3742b9a97e51eced5f9d1cf0606103290cedac4c2b0b224977c63f82'
assert sha(EXP / 'kernel.py') == '82601731da97a18934daf3d3f49722b7df3cc35017b249f9a8e26a8dfb91ef30'
assert sha(ACC / 'kernel.py') == 'c2483d3585dccb36b7dfba945c1a0cb2964a59f440161a7663c594bd4d928578'

data = json.loads((EXP / 'candidate.json').read_text())
attempts = json.loads((EXP / 'result.json').read_text())['attempts']
cert = next(a['certificate'] for a in attempts if a['precision'] == 192)
case = data['endpoint']; n = case['n']; r = data['r']; s_dim = n + r


def rational_inputs():
    B = [[Q(v) for v in row] for row in data['B']]; L = [[Q(v) for v in row] for row in data['L']]
    Kh = [[Q(v) for v in row] for row in data['K_hidden']]; K = [[Q(v) for v in row] for row in data['K_selected']]
    return B, L, Kh, K, list(map(Q, data['a'])), Q(data['ah'])


def load_kernel(path, name):
    spec = importlib.util.spec_from_file_location(name, path); mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod); return mod


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=1, default=float))


# ---------------------------------------------------------------- rigorous-path replays (kernel code, not mine)
if mode == 'replay':
    bits = int(sys.argv[2]); k = load_kernel(EXP / 'kernel.py', 'local_kernel')
    B, L, Kh, K, aa, ah = rational_inputs(); t0 = time.process_time()
    base = k.a.base_for(data['endpoint'], B, bits, JI=None)
    assert base['model'].serialize() == data['model_parameters']
    out, bounds = k.certify(base, aa, ah, L, Kh, K)
    st = next(x['certificate'] for x in attempts if x['precision'] == bits)
    fields = {key: out.get(key) == st.get(key) for key in sorted(set(out) | set(st))}
    stored = np.load(EXP / f'bounds_{bits}.npz')
    arrays = {key: bool(key in bounds and key in stored.files and np.array_equal(bounds[key], stored[key]))
              for key in sorted(set(bounds) | set(stored.files))}
    res = {'bits': bits, 'all_fields_identical': all(fields.values()), 'fields': fields,
           'all_arrays_identical': all(arrays.values()), 'arrays': arrays, 'pass': out.get('all_antipodal_faces_pass'),
           'certified_dimension': out.get('certified_dimension'), 'cpu_seconds': time.process_time() - t0}
    dump(f'replay_{bits}.json', res)
    print(f"replay {bits}: fields identical {res['all_fields_identical']} arrays identical {res['all_arrays_identical']} "
          f"pass {res['pass']} dim {res['certified_dimension']} cpu {res['cpu_seconds']:.0f}s", flush=True)
    sys.exit()

if mode == 'accepted':
    # The SAME frozen candidate through the unchanged accepted kernel: isolates what the affine tightening buys.
    k = load_kernel(ACC / 'kernel.py', 'accepted_kernel'); kl = load_kernel(EXP / 'kernel.py', 'local_kernel')
    B, L, Kh, K, aa, ah = rational_inputs(); base = k.a.base_for(data['endpoint'], B, 192, JI=None)
    out, bounds = k.certify(base, aa, ah, L, Kh, K)
    new = np.load(EXP / 'bounds_192.npz')
    ratios = {key: float(np.max(new[key] / np.maximum(bounds[key], 1e-300))) for key in ('HH', 'HH3', 'HS', 'HS3') if key in bounds}
    ratios_min = {key: float(np.min(np.where(bounds[key] > 0, new[key] / np.maximum(bounds[key], 1e-300), 1))) for key in ratios}
    res = {'accepted_kernel_result': {k2: out.get(k2) for k2 in ('valid', 'reason', 'eta_hidden', 'hidden_forcing_upper', 'M3_upper', 'certified_dimension', 'all_antipodal_faces_pass')},
           'beta_over_eps_accepted': [float(Q(b)) / EPS for b in out.get('beta3', [])],
           'beta_over_eps_local': [float(Q(b)) / EPS for b in cert['beta3']],
           'M3_local': cert['M3_upper'], 'eta_local': cert['eta_hidden'], 'forcing_local': cert['hidden_forcing_upper'],
           'max_new_over_old_bound': ratios, 'min_new_over_old_bound': ratios_min,
           'note': 'diagnostic only: the accepted kernel is a weaker but valid majorant; new<=old elementwise is expected'}
    dump('accepted_kernel_diagnostic.json', res)
    print(json.dumps(res, indent=1, default=float), flush=True)
    sys.exit()

if mode == 'exact':
    import mpmath as mp
    mp.mp.dps = 80
    B, L, Kh, K, aa, ah = rational_inputs(); res = {}
    for att in attempts:
        c = att['certificate']; bits = att['precision']
        mu = [Q(v) for v in c['mu_tilde']]; er = [Q(float(v)) for v in c['center_rows_upper']]; M3 = [Q(float(v)) for v in c['M3_upper']]
        beta = [m * (1 - e - M / 6) for m, e, M in zip(mu, er, M3)]
        assert [str(b) for b in beta] == c['beta3'], 'beta rederivation mismatch'
        res[f'faces_{bits}'] = {'all_beta_gt_eps': all(b > Q(1, 1000) for b in beta),
                                'beta_over_eps': [float(b * 1000) for b in beta],
                                'two_beta': [float(2 * b) for b in beta], 'min_face': 1 + min(range(r), key=lambda i: beta[i]),
                                'face7_two_beta_exact_str': str(2 * beta[6]), 'face7_two_beta_minus_2eps': float(2 * beta[6] - Q(2, 1000)),
                                'cubic_underestimate_factor_to_fail': [float((1 - e - Q(1000) ** -1 / m) / (M / 6)) for m, e, M in zip(mu, er, M3)]}
        eta = Q(c['eta_hidden']); mapped = [Q(float(v)) for v in c['hidden_forcing_upper']]
        res[f'hidden_{bits}'] = {'eta_lt_3_4': eta < Q(3, 4), 'selfmap_ok': all(v <= (1 - eta) * ah for v in mapped),
                                 'max_mapped_over_allowance': float(max(mapped) / ((1 - eta) * ah)),
                                 'radius_le_1': Q(c['radius']) <= 1, 'radius': float(Q(c['radius']))}
    # Independent support-aware query margin from exact ell~ = (K L)_i / a_i (my code, 80 digits).
    theta = [Q(x) for x in data['model_parameters']]; diag = theta[:n]
    meta = [('R', i, i) for i in range(n)] + [('W', i, j) for i in range(n) for j in range(n)] + [('b', i, 0) for i in range(n)]
    support = [(i, p) for i in range(n) for p, (g, o, _) in enumerate(meta) if o == i]
    factor = mp.sqrt(n * max(1, sum(mp.mpf(d.numerator) / d.denominator for d in [x * x for x in diag])))
    mine = []
    for i in range(r):
        ell = [sum(K[i][j] * L[j][d] for j in range(r)) / aa[i] for d in range(len(L[0]))]
        tot = sum(e * e / (diag[o] ** 2) for e, (o, p) in zip(ell, support))
        mine.append(mp.mpf(7) / 8 / (factor * mp.sqrt(mp.mpf(tot.numerator) / tot.denominator)))
    stored = [Q(v) for v in cert['mu_tilde']]
    res['mu_independent_rel_diff'] = [float(abs(mp.mpf(s.numerator) / s.denominator / m - 1)) for s, m in zip(stored, mine)]
    res['mu_stored_le_exact'] = [bool(mp.mpf(s.numerator) / s.denominator <= m) for s, m in zip(stored, mine)]
    old = json.loads((HERE.parent / 'third_order_antipodal_7d_20261001/candidate.json').read_text())
    res['amplitude_ratio_new_over_old'] = [float(Q(a) / Q(b)) for a, b in zip(data['a'], old['a'])]
    res['ah_ratio'] = float(Q(data['ah']) / Q(old['ah']))
    res['B_L_endpoint_model_identical_to_failed_7d'] = (data['B'] == old['B'] and data['L'] == old['L'] and data['endpoint'] == old['endpoint']
                                                       and data['model_parameters'] == old['model_parameters'])
    six = json.loads((ACC / 'candidate.json').read_text())
    res['endpoint_model_identical_to_accepted_6d'] = data['endpoint'] == six['endpoint'] and data['model_parameters'] == six['model_parameters']
    cfg = json.loads((EXP / 'config.json').read_text()); res['config_epsilon'] = cfg['epsilon']
    dump('exact_checks.json', res); print(json.dumps(res, indent=1, default=float), flush=True)
    sys.exit()

# ---------------------------------------------------------------- my own float64 model (numerical attacks)
import torch
torch.set_default_dtype(torch.float64); torch.set_num_threads(1)
theta_q = [Q(x) for x in data['model_parameters']]; theta = [float(x) for x in theta_q]
R = np.diag(theta[:n]); Wm = np.array(theta[n:n + n * n]).reshape(n, n); bvec = np.array(theta[n + n * n:])
meta = [('R', i, i) for i in range(n)] + [('W', i, j) for i in range(n) for j in range(n)] + [('b', i, 0) for i in range(n)]
P = len(meta)
rms = {g: math.sqrt(np.mean(np.square([theta[p] for p, m in enumerate(meta) if m[0] == g]))) for g in 'RWb'}
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
amps = np.r_[np.full(n, ah), aa]
diag = np.array(theta[:n]); norm_factor = math.sqrt(n * max(1.0, float(np.sum(diag ** 2))))
GATE_HIGH = 1 - math.tanh(0.25) ** 2
c_high = np.array([GATE_HIGH * diag[i] / norm_factor for i, p in support])
c_78 = np.array([0.875 * diag[i] / norm_factor for i, p in support])
mu = np.array([float(Q(v)) for v in cert['mu_tilde']]); beta = np.array([float(Q(v)) for v in cert['beta3']])
M3 = np.array([float(v) for v in cert['M3_upper']]); e0 = np.array([float(v) for v in cert['center_rows_upper']])
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


def hist(w): return X0 + (SD * (Bm @ w)).reshape(T, n)


def G(w):
    h, S = fwd(hist(w)); return torch.cat([h, S[ii, pp] * wsup])


BN = Bm.numpy(); X0N = X0.numpy(); DIAG = diag
OWN = np.array(ii); TYP = np.array([{'R': 0, 'W': 1, 'b': 2}[meta[p][0]] for i, p in support])
JJ = np.array([meta[p][2] for i, p in support]); WS = wsup.numpy()


def fwd_np(w, traj=False):
    m = len(w); h = np.zeros(n); dh = np.zeros((n, m)); S = np.zeros(len(OWN)); dS = np.zeros((len(OWN), m)); Rown = DIAG[OWN]; tr = []
    for t in range(T):
        Bt = BN[t * n:(t + 1) * n]; x = X0N[t] + SD * (Bt @ w); dx = SD * Bt
        pre = DIAG * h + Wm @ x + bvec; dpre = DIAG[:, None] * dh + Wm @ dx
        hn = np.tanh(pre); g = 1 - hn * hn; dhn = g[:, None] * dpre; dg = -2 * hn[:, None] * dhn
        direct = np.where(TYP == 0, h[JJ], np.where(TYP == 1, x[JJ], 1.0))
        ddirect = np.where((TYP == 0)[:, None], dh[JJ], np.where((TYP == 1)[:, None], dx[JJ], 0.0))
        inner = Rown * S + direct; dinner = Rown[:, None] * dS + ddirect
        S, dS = g[OWN] * inner, dg[OWN] * inner[:, None] + g[OWN][:, None] * dinner
        if traj: tr.append((pre, dpre, hn, dhn))
        h, dh = hn, dhn
    if traj: return tr
    return h, S * WS, dh, dS * WS[:, None]


H0N = fwd_np(np.zeros(s_dim))[0]


def lift_np(t, track=True):
    y = np.zeros(n)
    for _ in range(30):
        h, s, dh, ds = fwd_np(np.concatenate([y, t])); f = h - H0N
        if np.abs(f).max() < 1e-15: break
        y = y - np.linalg.solve(dh[:, :n], f)
    h, s, dh, ds = fwd_np(np.concatenate([y, t])); res = float(np.abs(h - H0N).max())
    if track:
        STATS['lift_evals'] += 1; STATS['max_lift_residual'] = max(STATS['max_lift_residual'], res)
        STATS['max_y_over_ah'] = max(STATS['max_y_over_ah'], float(np.abs(y).max()) / ah)
        if res > 1e-12: STATS['newton_failures'] += 1
    return y, res, s, dh, ds


CACHE = {}


def point(z, track=True):
    key = tuple(np.round(z, 15))
    if key in CACHE: return CACHE[key]
    y, res, s, dh, ds = lift_np(aa * np.asarray(z, dtype=float), track)
    Js = ds[:, n:] - ds[:, :n] @ np.linalg.solve(dh[:, :n], dh[:, n:])
    out = (s, Js, y, res)
    if len(CACHE) > 20000: CACHE.clear()
    CACHE[key] = out; return out


S0 = point(np.zeros(r), track=False)[0]; Psi0 = Lt.numpy() @ S0; KL = Kt.numpy() @ Lt.numpy()


def Phi(z, track=True): return (Kt.numpy() @ (Lt.numpy() @ point(z, track=track)[0] - Psi0)) / aa


def dphi0(): return (KL @ point(np.zeros(r), track=False)[1]) * aa[None, :] / aa[:, None]


def DC(d, c=c_high): return float(np.sqrt(np.sum((c * d) ** 2)))


class Face:
    def __init__(self, face): self.i = face - 1
    def z(self, u): return np.insert(np.asarray(u, dtype=float), self.i, 1.0)
    def f(self, u):
        z = self.z(u); return DC(point(z)[0] - point(-z)[0])
    def fg(self, u):
        z = self.z(u); s1, J1, _, _ = point(z); s2, J2, _, _ = point(-z); d = s1 - s2; val = DC(d)
        gz = ((c_high ** 2) * d) @ ((J1 + J2) * aa[None, :]) / val
        return val, np.delete(gz, self.i)
    def dphi(self, u):
        z = self.z(u); s1, J1, _, _ = point(z); s2, J2, _, _ = point(-z); row = ellt[self.i]
        return float(row @ (s1 - s2)), np.delete(row @ ((J1 + J2) * aa[None, :]), self.i)


def local(fobj, x0, bounds):
    rr = minimize(fobj, x0, jac=True, method='L-BFGS-B', bounds=bounds, options={'gtol': 1e-10, 'ftol': 1e-15, 'maxiter': 400})
    return float(rr.fun), np.asarray(rr.x), int(rr.nit)


if mode == 'validate':
    out = {}
    mine = np.array([0.875 / (norm_factor * math.sqrt(sum(ellt[q, d] ** 2 / diag[i] ** 2 for d, (i, p) in enumerate(support)))) for q in range(r)])
    out['mu_float_rel_err'] = float(np.max(np.abs(mine / mu - 1)))
    out['max_abs_DPhi0_minus_I'] = float(np.max(np.abs(dphi0() - np.eye(r))))
    rng = np.random.default_rng(1); xs = []
    for zz in rng.uniform(-0.7, 0.7, (5, r)):
        t = torch.tensor(aa * zz); y, _, s_np, _, _ = lift_np(aa * zz, track=False)
        w = torch.cat([torch.tensor(y), t]); xs.append(float(np.abs(G(w)[n:].detach().numpy() - s_np).max() / np.abs(s_np).max()))
    out['numpy_vs_torch_rel'] = max(xs); dump('validate.json', out); print(out, flush=True); sys.exit()

# ---------------------------------------------------------------- affine-substitution containment attack
if mode == 'affine':
    seed, N = int(sys.argv[2]), int(sys.argv[3]); rng = np.random.default_rng(seed)
    src = (EXP / 'kernel.py').read_text()
    anchor = "        S,Sx,S2,S3=S_new,Sx_new,S2_new,S3_new"; assert src.count(anchor) == 1
    src = src.replace(anchor, "        CAPTURE.append((t,[(v.lo,v.hi) for v in pre],ax.copy(),hx_new.copy(),[(v.lo,v.hi) for v in hn],upadd(left(R,hx),left(W,u))))\n" + anchor)
    mod = types.ModuleType('kernel_instr'); mod.__file__ = str(EXP / 'kernel.py'); mod.CAPTURE = []
    exec(compile(src, str(EXP / 'kernel.py'), 'exec'), mod.__dict__)
    B, L, Kh, K, aaq, ahq = rational_inputs(); base = mod.a.base_for(data['endpoint'], B, 192, JI=None)
    h2, h3, HS, HS3 = mod.third_majorants(base, r, [ahq] * n + aaq)
    stored = np.load(EXP / 'bounds_192.npz')
    same = bool(np.array_equal(h2, stored['HH']) and np.array_equal(h3, stored['HH3']) and np.array_equal(HS, stored['HS']) and np.array_equal(HS3, stored['HS3']))
    sc = float(2 ** 192)
    cap = [(t, np.array([[lo / sc, hi / sc] for lo, hi in pre]), ax, hx, np.array([[lo / sc, hi / sc] for lo, hi in hn]), axold)
           for t, pre, ax, hx, hn, axold in mod.CAPTURE]
    assert len(cap) == T
    Cs = [Wm @ (SD * BN[t * n:(t + 1) * n]) for t in range(T)]
    pts = []
    for q in range(N):
        kind = q % 4
        if kind == 0: w = amps * rng.choice([-1., 1.], s_dim)
        elif kind == 1:
            t = rng.integers(T); i = rng.integers(n); w = amps * np.sign(Cs[t][i]) * rng.choice([-1., 1.])
        elif kind == 2: w = amps * rng.uniform(-1, 1, s_dim)
        else:
            w = amps * rng.choice([-1., 1.], s_dim); w[rng.integers(s_dim)] *= rng.uniform(-1, 1)
        pts.append(w)
    worst = {'pre_excess': -math.inf, 'h_excess': -math.inf, 'dpre_ratio': 0., 'dh_ratio': 0., 'pre_fill': 0.}
    for w in pts:
        for (t, pre, ax, hx, hn, _), (a_, da, hv, dhv) in zip(cap, fwd_np(w, traj=True)):
            width = pre[:, 1] - pre[:, 0]
            worst['pre_excess'] = max(worst['pre_excess'], float(np.max(np.maximum(a_ - pre[:, 1], pre[:, 0] - a_) / width)))
            worst['pre_fill'] = max(worst['pre_fill'], float(np.max(np.abs(a_ - (pre[:, 0] + pre[:, 1]) / 2) / (width / 2))))
            worst['h_excess'] = max(worst['h_excess'], float(np.max(np.maximum(hv - hn[:, 1], hn[:, 0] - hv) / (hn[:, 1] - hn[:, 0]))))
            worst['dpre_ratio'] = max(worst['dpre_ratio'], float(np.max(np.abs(da) / np.maximum(ax, 1e-300))))
            worst['dh_ratio'] = max(worst['dh_ratio'], float(np.max(np.abs(dhv) / np.maximum(hx, 1e-300))))
    # Adversarial: push each preactivation to its extremes over the closed 11-D box (exact float gradients).
    adv = -math.inf; advfill = 0.
    for t in rng.choice(T, 10, replace=False):
        for i in range(n):
            for sgn in (1., -1.):
                def obj(w, t=t, i=i, sgn=sgn):
                    a_, da, _, _ = fwd_np(w, traj=True)[t]; return -sgn * a_[i], -sgn * da[i]
                w0 = amps * np.sign(Cs[t][i]) * sgn
                rr = minimize(obj, w0, jac=True, method='L-BFGS-B', bounds=list(zip(-amps, amps)), options={'maxiter': 200})
                pre = cap[t][1]; val = -sgn * rr.fun; width = pre[i, 1] - pre[i, 0]
                adv = max(adv, float(max(val - pre[i, 1], pre[i, 0] - val) / width))
                advfill = max(advfill, float(abs(val - pre[i].mean()) / (width / 2)))
    tight = {'ax_new_over_old_min': float(min(np.min(c[2] / np.maximum(c[5], 1e-300)) for c in cap)),
             'ax_new_over_old_max': float(max(np.max(c[2] / np.maximum(c[5], 1e-300)) for c in cap))}
    res = {'seed': seed, 'points': N, 'kernel_arrays_identical_to_stored': same, **worst,
           'adversarial_pre_excess': adv, 'adversarial_pre_fill': advfill, **tight,
           'reading': 'excess<=0 means truth inside enclosure; ratios<=1 required; fill = |a-mid|/halfwidth'}
    dump(f'affine_{seed}.json', res); print(json.dumps(res, default=float), flush=True); sys.exit()

if mode == 'affexact':
    # Exact-arithmetic recheck of the float edge contacts: 60-digit trajectories at every sign corner of every C_t,i.
    import mpmath as mp
    mp.mp.dps = 60
    src = (EXP / 'kernel.py').read_text(); anchor = "        S,Sx,S2,S3=S_new,Sx_new,S2_new,S3_new"
    src = src.replace(anchor, "        CAPTURE.append((t,[(v.lo,v.hi) for v in pre],ax.copy(),hx_new.copy()))\n" + anchor)
    mod = types.ModuleType('kernel_instr'); mod.__file__ = str(EXP / 'kernel.py'); mod.CAPTURE = []
    exec(compile(src, str(EXP / 'kernel.py'), 'exec'), mod.__dict__)
    Bq_, L_, Kh_, K_, aaq, ahq = rational_inputs(); base = mod.a.base_for(data['endpoint'], Bq_, 192, JI=None)
    mod.third_majorants(base, r, [ahq] * n + aaq); cap = mod.CAPTURE; sc = 2 ** 192
    mpq = lambda x: mp.mpf(x.numerator) / x.denominator
    th = [mpq(x) for x in theta_q]; Rq = th[:n]; Wq = [th[n + i * n:n + (i + 1) * n] for i in range(n)]; bq = th[n + n * n:]
    Xq = [[mpq(Q(v)) for v in row] for row in case['X']]; Bq = [[mpq(Q(v)) for v in row] for row in data['B']]
    ampq = [mpq(ahq)] * n + [mpq(v) for v in aaq]; sd = mp.sqrt(mp.mpf(3) / 32)
    Cs = [Wm @ (SD * BN[t * n:(t + 1) * n]) for t in range(T)]
    worst_pre = -mp.inf; worst_d = -mp.inf; checked = 0
    corners = [(t, i, sg) for t in range(T) for i in range(n) for sg in (1, -1)]
    rng = np.random.default_rng(5); extra = [rng.choice([-1, 1], s_dim) for _ in range(40)]
    for item in corners + extra:
        signs = (np.sign(Cs[item[0]][item[1]]) * item[2]) if isinstance(item, tuple) else item
        w = [ampq[k] * int(signs[k] if signs[k] != 0 else 1) for k in range(s_dim)]
        h = [mp.mpf(0)] * n; dh = [[mp.mpf(0)] * s_dim for _ in range(n)]
        for t in range(T):
            x = [Xq[t][j] + sd * mp.fsum(Bq[t * n + j][c] * w[c] for c in range(s_dim)) for j in range(n)]
            pre = [Rq[i] * h[i] + mp.fsum(Wq[i][j] * x[j] for j in range(n)) + bq[i] for i in range(n)]
            dpre = [[Rq[i] * dh[i][c] + sd * mp.fsum(Wq[i][j] * Bq[t * n + j][c] for j in range(n)) for c in range(s_dim)] for i in range(n)]
            _, enc, ax, hx = cap[t]
            for i in range(n):
                lo, hi = mp.mpf(enc[i][0]) / sc, mp.mpf(enc[i][1]) / sc
                worst_pre = max(worst_pre, max(pre[i] - hi, lo - pre[i]))
                for c in range(s_dim): worst_d = max(worst_d, abs(dpre[i][c]) - mp.mpf(float(ax[i, c])))
            hn = [mp.tanh(v) for v in pre]; dh = [[(1 - hn[i] ** 2) * dpre[i][c] for c in range(s_dim)] for i in range(n)]; h = hn
            checked += 1
    res = {'trajectories': len(corners) + len(extra), 'max_exact_pre_excess_absolute': mp.nstr(worst_pre, 8),
           'max_exact_dpre_minus_ax': mp.nstr(worst_d, 8), 'pre_contained': bool(worst_pre <= 0), 'dpre_dominated': bool(worst_d <= 0)}
    dump('affine_exact.json', res); print(json.dumps(res), flush=True); sys.exit()

if mode == 'forcing':
    # Direct test of the fixed-h inclusion: |Kh (h(0,t)-h0)| vs certified forcing, and ||I - Kh H_y(w)||_inf vs eta_h.
    Khf = np.array([[float(Q(v)) for v in row] for row in data['K_hidden']]); mapped = np.array(cert['hidden_forcing_upper'])
    rng = np.random.default_rng(21)
    tang = [aa * np.array(c) for c in np.array(np.meshgrid(*[[-1., 1.]] * r, indexing='ij')).reshape(r, -1).T] + [aa * rng.uniform(-1, 1, r) for _ in range(200)]
    worst_force = np.zeros(n); worst_eta = 0.
    for t in tang:
        h, s, dh, ds = fwd_np(np.r_[np.zeros(n), t]); worst_force = np.maximum(worst_force, np.abs(Khf @ (h - H0N)))
        for y in (np.zeros(n), ah * rng.choice([-1., 1.], n)):
            h2_, _, dh2, _ = fwd_np(np.r_[y, t]); worst_eta = max(worst_eta, float(np.abs(np.eye(n) - Khf @ dh2[:, :n]).sum(1).max()))
    res = {'points': len(tang), 'actual_forcing': worst_force.tolist(), 'certified_forcing': mapped.tolist(),
           'actual_over_certified_forcing': (worst_force / mapped).tolist(), 'actual_contraction': worst_eta, 'certified_eta': cert['eta_hidden'],
           'allowance_(1-eta)ah': (1 - cert['eta_hidden']) * ah, 'actual_forcing_over_allowance': float(worst_force.max() / ((1 - cert['eta_hidden']) * ah))}
    dump('forcing.json', res); print(json.dumps(res), flush=True); sys.exit()

if mode == 'majorant':
    seed, N = int(sys.argv[2]), int(sys.argv[3]); rng = np.random.default_rng(seed)
    bd = np.load(EXP / 'bounds_192.npz'); M2 = np.concatenate([bd['HH'], bd['HS']]); Mt3 = np.concatenate([bd['HH3'], bd['HS3']])
    d2 = torch.func.jacfwd(torch.func.jacrev(G)); d3 = torch.func.jacfwd(d2); w2 = w3 = 0.; arg = None
    for q in range(N):
        y = amps * (rng.choice([-1., 1.], s_dim) if q % 2 == 0 else rng.uniform(-1, 1, s_dim))
        yt = torch.tensor(y); T3 = d3(yt).detach().numpy(); T2 = d2(yt).detach().numpy()
        r3 = float((np.abs(T3) / np.maximum(Mt3, 1e-300)).max()); r2 = float((np.abs(T2) / np.maximum(M2, 1e-300)).max())
        if r3 > w3: w3 = r3; arg = np.unravel_index(int(np.argmax(np.abs(T3) / np.maximum(Mt3, 1e-300))), T3.shape)
        w2 = max(w2, r2)
    res = {'seed': seed, 'points': N, 'max_third_over_bound': w3, 'argmax_third': [int(v) for v in arg], 'max_second_over_bound': w2}
    dump(f'majorant_{seed}.json', res); print(json.dumps(res), flush=True); sys.exit()

if mode == 'majadv':
    # Adversarial: maximise |entry| / bound over the closed 11-D box for the tightest 2nd/3rd-derivative entries.
    seed, K = int(sys.argv[2]), int(sys.argv[3]); rng = np.random.default_rng(seed)
    bd = np.load(EXP / 'bounds_192.npz'); M2 = np.concatenate([bd['HH'], bd['HS']]); Mt3 = np.concatenate([bd['HH3'], bd['HS3']])
    d2 = torch.func.jacfwd(torch.func.jacrev(G)); d3 = torch.func.jacfwd(d2)
    starts = [np.zeros(s_dim)] + [amps * rng.choice([-1., 1.], s_dim) for _ in range(5)]
    cand3, cand2 = {}, {}
    for y in starts:
        yt = torch.tensor(y); R3 = np.abs(d3(yt).detach().numpy()) / np.maximum(Mt3, 1e-300); R2 = np.abs(d2(yt).detach().numpy()) / np.maximum(M2, 1e-300)
        for cand, Rr in ((cand3, R3), (cand2, R2)):
            for flat in np.argsort(Rr.ravel())[-K:]:
                idx = np.unravel_index(int(flat), Rr.shape)
                if Rr[idx] > cand.get(idx, (0, None))[0]: cand[idx] = (float(Rr[idx]), y)
    E = torch.eye(s_dim)

    def entry(w, idx):
        o, dirs = idx[0], idx[1:]; f = lambda v: G(v)
        for d in dirs[::-1]:
            f = (lambda g, e: (lambda v: torch.func.jvp(g, (v,), (e,))[1]))(f, E[d])
        return f(w)[o]
    out = {'seed': seed, 'K': K}
    for label, cand, M in (('third', cand3, Mt3), ('second', cand2, M2)):
        best = 0.; arg = None
        for idx, (r0, y0) in sorted(cand.items(), key=lambda kv: -kv[1][0])[:K]:
            sgn = float(np.sign(float(entry(torch.tensor(y0), idx)))) or 1.; bound = float(M[idx])

            def obj(w, idx=idx, sgn=sgn, bound=bound):
                wt = torch.tensor(w, requires_grad=True); v = sgn * entry(wt, idx) / bound; v.backward()
                return -float(v), -wt.grad.numpy()
            rr = minimize(obj, y0, jac=True, method='L-BFGS-B', bounds=list(zip(-amps, amps)), options={'maxiter': 60})
            val = -float(rr.fun)
            if val > best: best, arg = val, ([int(v) for v in idx], r0)
        out[f'max_{label}_over_bound_adversarial'] = best; out[f'argmax_{label}'] = arg
    dump(f'majadv_{seed}.json', out); print(json.dumps(out), flush=True); sys.exit()

if mode == 'fd':
    seed, N = int(sys.argv[2]), int(sys.argv[3]); rng = np.random.default_rng(seed)
    sel3 = np.load(EXP / 'bounds_192.npz')['selected3']; absK = np.abs(Kt.numpy()); worst = 0.
    for q in range(N):
        z0 = rng.uniform(-.85, .85, r); u = rng.normal(size=r); u /= np.abs(u).max(); hs = 0.04
        g = lambda s: Phi(z0 + s * u, track=False)
        f = [g(m * hs) for m in (-2, -1, 1, 2)]
        d3fd = (f[3] - 2 * f[2] + 2 * f[1] - f[0]) / (2 * hs ** 3)
        bound = np.einsum('im,mabc,a,b,c->i', absK, sel3, aa * np.abs(u), aa * np.abs(u), aa * np.abs(u)) / aa
        worst = max(worst, float((np.abs(d3fd) / bound).max()))
    res = {'seed': seed, 'points': N, 'max_fd_third_over_certified': worst}
    dump(f'fd_{seed}.json', res); print(json.dumps(res), flush=True); sys.exit()

if mode == 'core':
    D = dphi0(); out = {'max_abs_DPhi0_minus_I': float(np.abs(D - np.eye(r)).max())}
    rng = np.random.default_rng(11)
    corners = [np.array(c) for c in np.array(np.meshgrid(*[[-1., 1.]] * r, indexing='ij')).reshape(r, -1).T if c[0] > 0]
    pts = corners + []
    for _ in range(400):
        z = rng.uniform(-1, 1, r); z[rng.integers(r)] = rng.choice([-1., 1.]); pts.append(z)
    rem = np.zeros(r); mind = math.inf; mind78 = math.inf; minratio = math.inf
    for z in pts:
        p1 = Phi(z); p2 = Phi(-z); rem = np.maximum(rem, np.abs(p1 - p2 - 2 * D @ z) / (M3 / 3))
        d = point(z)[0] - point(-z)[0]; mind = min(mind, DC(d)); d78 = DC(d, c_78); mind78 = min(mind78, d78)
        face = int(np.argmax(np.abs(z))); minratio = min(minratio, d78 / (2 * beta[face]))
    out.update(boundary_pairs=len(pts), odd_remainder_over_M3_third=rem.tolist(), min_DC_high=mind, min_D78=mind78,
               min_D78_over_2eps=mind78 / 2e-3, min_D78_over_2beta_face=minratio, stats=dict(STATS))
    dump('core.json', out); print(json.dumps(out, default=float), flush=True); sys.exit()

if mode == 'face':
    face = int(sys.argv[2]); deep = '--deep' in sys.argv; t0 = time.process_time(); F = Face(face); k = face - 1; m = r - 1
    mult = 3 if deep else 1; sh = 500 if deep else 0
    log = {'face': face, 'deep': deep, 'runs': []}
    grid = np.array(np.meshgrid(*[[-1., 0., 1.]] * m, indexing='ij')).reshape(m, -1).T
    sob = qmc.Sobol(m, scramble=True, seed=9000 + face + sh).random(256 * mult) * 2 - 1
    pts = np.vstack([grid, sob]); vals = np.array([F.f(u) for u in pts]); order = np.argsort(vals)
    log['screen'] = {'n': len(pts), 'best': float(vals[order[0]]), 'best_u': pts[order[0]].tolist()}
    bounds = [(-1., 1.)] * m; nb = 40 * mult; rng = np.random.default_rng(9100 + face + sh)
    best = (math.inf, None, '')
    for x0 in [pts[j] for j in order[:nb]] + list(rng.uniform(-1, 1, (nb, m))):
        v, x, it = local(F.fg, x0, bounds); log['runs'].append(('B', v, x.tolist()))
        if v < best[0]: best = (v, x, 'B')
    for kk in range(m):  # codimension-2 sub-faces
        for sg in (-1., 1.):
            bnd = [(sg, sg) if q == kk else (-1., 1.) for q in range(m)]
            for j in [j for j in order if pts[j][kk] == sg][:5 * mult]:
                v, x, it = local(F.fg, pts[j], bnd); log['runs'].append(('D', v, x.tolist()))
                if v < best[0]: best = (v, x, 'D')
    de = differential_evolution(F.f, bounds, popsize=15 * mult, maxiter=60 * mult, seed=9200 + face + sh, tol=1e-12, atol=0, polish=False)
    v, x, _ = local(F.fg, de.x, bounds); log['runs'].append(('C', v, x.tolist())); log['de'] = {'fun': float(de.fun), 'polished': v}
    if v < best[0]: best = (v, x, 'C')
    z = F.z(best[1]); d = point(z)[0] - point(-z)[0]; d78 = DC(d, c_78)
    log.update(best_DC_high=best[0], best_D78=d78, method=best[2], best_u=best[1].tolist(), best_z=z.tolist(),
               D78_over_2eps=d78 / 2e-3, D78_over_2beta=d78 / (2 * beta[k]), DC_high_over_2eps=best[0] / 2e-3,
               certified_2beta=2 * beta[k], stats=dict(STATS), cpu_seconds=time.process_time() - t0)
    dump(f'face{face}_{"deep" if deep else "base"}.json', log)
    print(f"face {face} [{'deep' if deep else 'base'}]: min D78 {d78:.9e} /2eps {d78/2e-3:.4f} /2beta {d78/(2*beta[k]):.4f}; "
          f"DC(high) {best[0]:.9e} /2eps {best[0]/2e-3:.4f}; via {best[2]}; z {np.round(z,3).tolist()}; max|y|/ah {STATS['max_y_over_ah']:.4f}; "
          f"cpu {log['cpu_seconds']:.0f}s", flush=True)
    sys.exit()

if mode == 'confirm':
    import mpmath as mp
    mp.mp.dps = 50; face = int(sys.argv[2])
    best = min((json.loads(p.read_text()) for p in OUT.glob(f'face{face}_*.json')), key=lambda d: d['best_D78'])
    z = np.array(best['best_z'])
    th = [mp.mpf(x.numerator) / x.denominator for x in theta_q]
    Rq = th[:n]; Wq = [th[n + i * n:n + (i + 1) * n] for i in range(n)]; bq = th[n + n * n:]
    X = [[mp.mpf(Q(v).numerator) / Q(v).denominator for v in row] for row in case['X']]
    Bq = [[mp.mpf(Q(v).numerator) / Q(v).denominator for v in row] for row in data['B']]
    a_q = [mp.mpf(Q(v).numerator) / Q(v).denominator for v in data['a']]; sd = mp.sqrt(mp.mpf(3) / 32)
    rmsq = {g: mp.sqrt(sum(th[p] ** 2 for p, mm in enumerate(meta) if mm[0] == g) / sum(1 for mm in meta if mm[0] == g)) for g in 'RWb'}

    def run(w, want):
        h = [mp.mpf(0)] * n; S = [[mp.mpf(0)] * P for _ in range(n)]; dh = [[mp.mpf(0)] * n for _ in range(n)]
        for t in range(T):
            x = [X[t][j] + sd * mp.fsum(Bq[t * n + j][c] * w[c] for c in range(s_dim)) for j in range(n)]
            dx = [[sd * Bq[t * n + j][c] for c in range(n)] for j in range(n)]
            pre = [Rq[i] * h[i] + mp.fsum(Wq[i][j] * x[j] for j in range(n)) + bq[i] for i in range(n)]
            hn = [mp.tanh(v) for v in pre]; g = [1 - v * v for v in hn]; Sn = [[mp.mpf(0)] * P for _ in range(n)]
            for p, (gr, i, j) in enumerate(meta):
                direct = h[j] if gr == 'R' else x[j] if gr == 'W' else mp.mpf(1)
                Sn[i][p] = g[i] * (Rq[i] * S[i][p] + direct)
                for i2 in range(n):
                    if i2 != i: Sn[i2][p] = g[i2] * Rq[i2] * S[i2][p]
            if want: dh = [[g[i] * (Rq[i] * dh[i][c] + mp.fsum(Wq[i][j] * dx[j][c] for j in range(n))) for c in range(n)] for i in range(n)]
            h, S = hn, Sn
        return h, S, dh
    h0q = run([mp.mpf(0)] * s_dim, False)[0]

    def svec(zz):
        tq = [a_q[c] * mp.mpf(float(zz[c])) for c in range(r)]; y = [mp.mpf(float(v)) for v in lift_np(aa * zz, track=False)[0]]
        for _ in range(8):
            h, S, dh = run(y + tq, True); f = mp.matrix([h[i] - h0q[i] for i in range(n)])
            if max(abs(v) for v in f) < mp.mpf(10) ** -45: break
            step = mp.lu_solve(mp.matrix(dh), f); y = [y[i] - step[i] for i in range(n)]
        h, S, _ = run(y + tq, False)
        return [S[i][p] * rmsq[meta[p][0]] for i, p in support], max(abs(h[i] - h0q[i]) for i in range(n)), max(abs(v) for v in y)
    s1, r1, y1 = svec(z); s2, r2, y2 = svec(-z); d = [s1[q] - s2[q] for q in range(len(support))]
    nf = mp.sqrt(n * max(mp.mpf(1), sum(v ** 2 for v in Rq)))
    D78q = mp.sqrt(mp.fsum((mp.mpf(7) / 8 * Rq[i] / nf * d[q]) ** 2 for q, (i, p) in enumerate(support)))
    out = {'face': face, 'z': z.tolist(), 'D78_mp50': mp.nstr(D78q, 20), 'D78_float64': best['best_D78'],
           'rel_diff': float(abs(D78q / best['best_D78'] - 1)), 'lift_residual_mp': mp.nstr(max(r1, r2), 5),
           'D78_over_2eps': float(D78q / (2 * EPS)), 'D78_over_2beta': float(D78q / (2 * beta[face - 1])), 'max_y_over_ah': float(max(y1, y2) / ah)}
    dump(f'confirm_face{face}.json', out); print(json.dumps(out), flush=True); sys.exit()

if mode == 'curv':
    face = int(sys.argv[2]); t0 = time.process_time(); F = Face(face); k = face - 1
    best = min((json.loads(p.read_text()) for p in OUT.glob(f'face{face}_*.json')), key=lambda d: d['best_D78'])
    z = np.array(best['best_z']); d = point(z)[0] - point(-z)[0]; D78v = DC(d, c_78); dph = float(ellt[k] @ d)

    def g3sup(zz, h):
        g = lambda s: Phi(s * zz, track=False)[k]; b = 0.
        for s in np.linspace(-1, 1, 41):
            b = max(b, abs((-g(s + 3 * h) + 8 * g(s + 2 * h) - 13 * g(s + h) + 13 * g(s - h) - 8 * g(s - 2 * h) + g(s - 3 * h)) / (8 * h ** 3)))
        return b
    rng = np.random.default_rng(9300 + face)
    rays = [F.z(u) for u in rng.uniform(-1, 1, (150, r - 1))] + [F.z(c) for c in np.array(np.meshgrid(*[[-1., 1.]] * (r - 1), indexing='ij')).reshape(r - 1, -1).T]
    Ghat = max(g3sup(zz, 0.02) for zz in rays)
    starts = [np.array(best['best_u'])] + list(rng.uniform(-1, 1, (15, r - 1)))
    mind = min(local(F.dphi, x0, [(-1., 1.)] * (r - 1))[0] for x0 in starts)
    out = {'face': face, 'D78_at_best': D78v, 'mu_dphi_at_best': mu[k] * abs(dph), 'two_beta': 2 * beta[k], 'M3': M3[k],
           'G_face_hat': Ghat, 'G_face_hat_over_M3': Ghat / M3[k], 'oracle_face_bound_true_curvature': 2 * mu[k] * (1 - e0[k] - Ghat / 6),
           'mu_min_dphi_face': mu[k] * mind,
           'log_terms': {'query_linear_range': math.log(D78v / (mu[k] * abs(dph))),
                         'actual_vs_linearised': math.log(abs(dph) / 2),
                         'curvature_majorant': math.log(1 / (1 - e0[k] - M3[k] / 6))},
           'log_total_D78_over_2beta': math.log(D78v / (2 * beta[k])), 'cpu_seconds': time.process_time() - t0}
    dump(f'curv_face{face}.json', out); print(json.dumps(out, default=float), flush=True); sys.exit()
