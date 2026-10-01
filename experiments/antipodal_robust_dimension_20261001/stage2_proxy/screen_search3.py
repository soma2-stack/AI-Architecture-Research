"""Screening search (numerical proxy only) over per-axis amplitudes for one endpoint/basis/r."""
import sys, json, math, time
import numpy as np
from scipy.optimize import minimize
from screen_proxy import Endpoint, EPS
from screen_proxy3 import evaluate3
name, kind, r, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
ep = Endpoint(name)
rmax = min(r, ep.Aproj.shape[0], ep.L - ep.n)
B, U, s = ep.basis(kind, r); L = ep.projection(U); mu0 = ep.margins(L)
rng = np.random.default_rng(seed); best = {'score': -1e9}; evals = [0]
def unpack(th): return np.exp(th[:r]), math.exp(th[r])
def score(th):
    evals[0] += 1
    a, ah = unpack(th)
    if np.any(a > 4) or ah > 4: return 1e3
    try: o = evaluate3(ep, B, L, a, ah)
    except np.linalg.LinAlgError: return 1e3
    if not o['valid']: return 1e2 + o.get('eta_h', 1.)
    v = float(np.min(o['beta3']))/EPS
    if v > best['score']:
        best.update(score=v, a=a.tolist(), ah=ah, beta3=o['beta3'].tolist(), M3=o['M3'].tolist(), eta_h=o['eta_h'], radius=o['radius'])
    return -v
t0 = time.time()
# starts: equalize first-order beta ~ mu*sigma*a with target 2*eps, small hidden amplitude
warm = Path_ = __import__('pathlib').Path(f'search_out/{name}_{kind}_r{r}_s{seed}.json')
if warm.exists():
    w = json.load(open(warm))
    if w.get('a') and min(w['a']) > 0:
        for sc in (1., 1.5, 2.):
            th0 = np.r_[np.log(np.array(w['a'])*sc), math.log(max(w['ah'], 1e-5)*sc*sc)]
            minimize(score, th0, method='Nelder-Mead', options={'maxfev': 400 + 60*r, 'xatol': 1e-3, 'fatol': 1e-6, 'adaptive': True})
for k in range(1):
    a0 = np.clip(2*EPS/(np.maximum(mu0*s, 1e-9))*np.exp(rng.normal(0, .4, r))*(0.6+0.8*rng.random()), 1e-3, 2)
    th0 = np.r_[np.log(a0), math.log(np.clip(np.median(a0)*np.exp(rng.normal(-1, .7)), 1e-4, 2))]
    minimize(score, th0, method='Nelder-Mead', options={'maxfev': 400 + 60*r, 'xatol': 1e-3, 'fatol': 1e-6, 'adaptive': True})
out = {'name': name, 'basis': kind, 'r': r, 'seed': seed, 'sigma': s.tolist(), 'mu': mu0.tolist(), 'evals': evals[0], 'seconds': time.time()-t0, **best}
print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in out.items() if k in ('name', 'basis', 'r', 'score', 'eta_h', 'radius', 'evals', 'seconds')}), flush=True)
Path = __import__('pathlib').Path; Path('search3_out').mkdir(exist_ok=True)
Path(f'search3_out/{name}_{kind}_r{r}_s{seed}.json').write_text(json.dumps(out))
