"""Independent numerical attack on an antipodal face certificate (own torch implementation; not a proof).
Usage: python antipodal_attack.py <candidate-id> [--faces f:s,...] [--starts k] [--hs N] [--seed s]"""
import sys, json, math, itertools, argparse
from fractions import Fraction as Q
from pathlib import Path
import numpy as np, torch
from scipy.optimize import minimize
torch.set_default_dtype(torch.float64); torch.set_num_threads(1)
EXP = Path(r"C:\Users\coler\OneDrive\Desktop\ai new\experiments\antipodal_robust_dimension_20261001")
INP = json.loads((EXP.parent/'robust_certificate_tightness_20261001/inputs.json').read_text())
ap = argparse.ArgumentParser(); ap.add_argument('cid'); ap.add_argument('--faces', default=''); ap.add_argument('--starts', type=int, default=3)
ap.add_argument('--hs', type=int, default=0); ap.add_argument('--seed', type=int, default=7); ap.add_argument('--mode', default='all')
A = ap.parse_args(); rng = np.random.default_rng(A.seed)
row = json.loads((EXP/f'results/{A.cid}.json').read_text()); cand = row['candidate']; res = row['result_192']
chart = json.loads((EXP/f"charts/{cand['chart']}.json").read_text()); case = next(c for c in INP['cases'] if c['name'] == cand['name'])
n = case['n']; r = cand['r']; fam = case['case']
theta = [float(Q(x)) for x in INP['models']['dense_parameters'][str(n)]]
R = np.array(theta[:n*n]).reshape(n, n); W = np.array(theta[n*n:2*n*n]).reshape(n, n); b = np.array(theta[2*n*n:])
if fam == 'independent': R = np.diag((6+3*np.arange(n))/20)
meta = [('R', i, j) for i in range(n) for j in range(n) if fam == 'dense' or i == j] + [('W', i, j) for i in range(n) for j in range(n)] + [('b', i, 0) for i in range(n)]
P = len(meta); vals = [R[i, j] if g == 'R' else W[i, j] if g == 'W' else b[i] for g, i, j in meta]
rms = {g: math.sqrt(np.mean([v**2 for v, m in zip(vals, meta) if m[0] == g])) for g in 'RWb'}
support = [(i, p) for i in range(n) for p, (g, o, _) in enumerate(meta) if fam == 'dense' or o == i]
wts = torch.tensor([rms[g] for g, _, _ in meta])
ER = torch.zeros(n, P, n); EW = torch.zeros(n, P, n); Eb = torch.zeros(n, P)
for p, (g, i, j) in enumerate(meta):
    if g == 'R': ER[i, p, j] = 1.
    elif g == 'W': EW[i, p, j] = 1.
    else: Eb[i, p] = 1.
Rt, Wt, bt = map(torch.tensor, (R, W, b))
X0 = torch.tensor([[float(Q(v)) for v in rw] for rw in case['X']]); T = X0.shape[0]; SD = math.sqrt(3/32)
B = torch.tensor([[float(Q(v)) for v in rw[:n+r]] for rw in chart['B']])
aa = np.array([float(Q(v)) for v in cand['a']]); ah = float(Q(cand['ah']))
def fwd(x):
    h = torch.zeros(n); S = torch.zeros(n, P)
    for t in range(T):
        direct = torch.einsum('ipj,j->ip', ER, h) + torch.einsum('ipj,j->ip', EW, x[t]) + Eb
        hn = torch.tanh(Rt @ h + Wt @ x[t] + bt); g = 1-hn*hn; S = g[:, None]*(Rt @ S + direct); h = hn
    return h, S
hist = lambda y: X0 + (SD*(B @ y)).reshape(T, n)
h0 = fwd(X0)[0]
def section(z):
    t = torch.tensor(aa*z); y = torch.zeros(n)
    Hf = lambda yy: fwd(hist(torch.cat([yy, t])))[0]-h0
    for _ in range(30):
        f = Hf(y)
        if f.abs().max() < 1e-15: break
        y = y - torch.linalg.solve(torch.autograd.functional.jacobian(Hf, y), f)
    assert float(Hf(y).abs().max()) < 1e-13
    full = torch.cat([y, t]); h, S = fwd(hist(full))
    return float(y.abs().max())/ah, np.array([float((S*wts)[i, p]) for i, p in support])
def tensor(v):
    S = np.zeros((n, P))
    for x, (i, p) in zip(v, support): S[i, p] = x
    return S
beta_n = math.sqrt(n)*max(1., np.linalg.norm(R))
if fam == 'independent': Qs = [R.T @ np.full(n, 7/8)/beta_n]
else: Qs = list((R.T @ (.25*np.eye(n)+.625*np.ones((n, n)))).T/beta_n)
sech2 = lambda x: 1/math.cosh(x)**2
Qv = [R.T @ np.array(g)/beta_n for g in itertools.product((sech2(.75), sech2(.25)), repeat=n)]
Dlow = lambda d: max(np.linalg.norm(c @ tensor(d)) for c in Qs)
Dsup = lambda d: max(np.linalg.norm(c @ tensor(d)) for c in Qv)
beta = np.array([float(Q(x)) for x in res['beta_i']]); bmin = beta.min()
print(f"== {A.cid} {cand['name']} r={r} certified={row.get('certified_dimension')} beta_min={bmin:.6e} 2beta_min={2*bmin:.6e} a={np.round(aa,4)} ah={ah:.5f}", flush=True)
if A.mode in ('all', 'corners'):
    corners = list(itertools.product((-1., 1.), repeat=r)); secs = {}; worsty = 0
    for z in corners:
        u, s = section(np.array(z)); secs[z] = s; worsty = max(worsty, u)
    mind = min(Dlow(secs[za]-secs[zb]) for za, zb in itertools.combinations(corners, 2))
    print(f" corners {len(corners)}: max |y|/a_h {worsty:.4f} (<=1 required); min pairwise D_lowquery {mind:.6e} vs 2eps 2e-3 ratio {mind/2e-3:.4f}; vs 2beta_min ratio {mind/(2*bmin):.4f}", flush=True)
if A.mode in ('all', 'antipodal'):
    faces = [tuple(map(float, f.split(':'))) for f in A.faces.split(',')] if A.faces else [(f, s) for f in range(r) for s in (1.,)]
    best = math.inf; arg = None
    for face, sign in faces:
        face = int(face)
        def obj(u):
            z = np.insert(np.tanh(u), face, sign); _, s1 = section(z); _, s2 = section(-z); return Dlow(s1-s2)
        if r == 1: v = obj(np.zeros(0)); best = min(best, v); arg = (face, sign); continue
        grid = list(itertools.product(np.linspace(-.95, .95, 3), repeat=r-1))
        vals = sorted((obj(np.arctanh(np.array(g))), g) for g in grid)
        inits = [np.arctanh(np.array(g)) for _, g in vals[:A.starts]] + [rng.normal(size=r-1) for _ in range(A.starts)]
        for u0 in inits:
            rr = minimize(obj, u0, method='Nelder-Mead', options={'maxiter': 120, 'xatol': 1e-4, 'fatol': 1e-12})
            if rr.fun < best: best, arg = rr.fun, (face, sign, np.round(np.tanh(rr.x), 3))
        print(f"  face {face}: running min antipodal D_lowquery {best:.6e}", flush=True)
    print(f" adversarial antipodal min D_lowquery = {best:.6e} at {arg}; ratio to 2eps {best/2e-3:.4f}; ratio to 2beta_min {best/(2*bmin):.4f}", flush=True)
if A.hs:
    cv = np.load(EXP/f'results/curvature_{A.cid}_192.npz'); HH, HS = cv['HH'], cv['HS']
    amps = np.r_[np.full(n, ah), aa]; Mj = torch.tensor(np.concatenate([HH, HS]))
    def G(y):
        h, S = fwd(hist(y)); return torch.cat([h, torch.stack([(S*wts)[i, p] for i, p in support])])
    hess = lambda y: torch.func.jacfwd(torch.func.jacrev(G))(y)
    pts = [torch.tensor(amps*np.array(c)) for c in itertools.product((-1., 1.), repeat=n+r)]
    pts = [pts[i] for i in rng.choice(len(pts), min(len(pts), A.hs//2), replace=False)] + [torch.tensor(amps*rng.uniform(-1, 1, n+r)) for _ in range(A.hs//2)]
    w = max(float((hess(y).abs()/Mj).max()) for y in pts)
    print(f" Hessian majorant check over {len(pts)} points of the {n+r}-D box: max actual/bound {w:.5f} (<=1 required)", flush=True)
