"""Independent hostile numerical attack on the frozen 6D third-order certificate (own torch code; not proofs).
modes: core | face F | majorant SEED N | fd SEED N | replay"""
import sys, json, math, itertools, time
from fractions import Fraction as Q
from pathlib import Path
import numpy as np, torch
from scipy.optimize import minimize
torch.set_default_dtype(torch.float64); torch.set_num_threads(1)
EXP = Path(r"C:\Users\coler\OneDrive\Desktop\ai new\experiments\third_order_antipodal_20261001")
mode = sys.argv[1]
if mode == 'replay':
    sys.dont_write_bytecode = True; sys.path.insert(0, str(EXP))
    import kernel as k
    data = json.loads((EXP/'candidate.json').read_text())
    B = [[Q(v) for v in row] for row in data['B']]; L = [[Q(v) for v in row] for row in data['L']]
    Kh = [[Q(v) for v in row] for row in data['K_hidden']]; K = [[Q(v) for v in row] for row in data['K_selected']]
    aa = list(map(Q, data['a'])); ah = Q(data['ah'])
    stored = json.loads((EXP/'result.json').read_text())['attempts']
    bnd = np.load(EXP/'bounds_192.npz')
    for bits in (192, 256):
        t = time.time(); base = k.a.base_for(data['endpoint'], B, bits, JI=None)
        out, bounds = k.certify(base, aa, ah, L, Kh, K)
        st = next(x['certificate'] for x in stored if x['precision'] == bits)
        same = {key: out.get(key) == st.get(key) for key in ('beta3', 'M3_upper', 'center_rows_upper', 'mu_tilde', 'eta_hidden', 'radius', 'certified_dimension')}
        arrs = {key: bool(np.array_equal(bounds[key], np.load(EXP/f'bounds_{bits}.npz')[key])) for key in bounds}
        print(f'replay {bits}: fields identical {same}; arrays identical {arrs}; {time.time()-t:.0f}s', flush=True)
    sys.exit()
data = json.loads((EXP/'candidate.json').read_text()); case = data['endpoint']; n = case['n']; r = 6
res = json.loads((EXP/'result.json').read_text())['attempts'][0]['certificate']
theta = [float(Q(x)) for x in data['model_parameters']]
R = np.diag(theta[:n]); W = np.array(theta[n:n+n*n]).reshape(n, n); b = np.array(theta[n+n*n:])
meta = [('R', i, i) for i in range(n)] + [('W', i, j) for i in range(n) for j in range(n)] + [('b', i, 0) for i in range(n)]
P = len(meta); vals = [R[i, j] if g == 'R' else W[i, j] if g == 'W' else b[i] for g, i, j in meta]
rms = {g: math.sqrt(np.mean([v**2 for v, m in zip(vals, meta) if m[0] == g])) for g in 'RWb'}
support = [(i, p) for i in range(n) for p, (g, o, _) in enumerate(meta) if o == i]
wsup = torch.tensor([rms[meta[p][0]] for i, p in support])
ER = torch.zeros(n, P, n); EW = torch.zeros(n, P, n); Eb = torch.zeros(n, P)
for p, (g, i, j) in enumerate(meta):
    if g == 'R': ER[i, p, j] = 1.
    elif g == 'W': EW[i, p, j] = 1.
    else: Eb[i, p] = 1.
Rt, Wt, bt = map(torch.tensor, (R, W, b))
X0 = torch.tensor([[float(Q(v)) for v in row] for row in case['X']]); T = X0.shape[0]; SD = math.sqrt(3/32)
B = torch.tensor([[float(Q(v)) for v in row] for row in data['B']]); Lt = torch.tensor([[float(Q(v)) for v in row] for row in data['L']])
Kt = torch.tensor([[float(Q(v)) for v in row] for row in data['K_selected']])
aa = np.array([float(Q(v)) for v in data['a']]); ah = float(Q(data['ah'])); A = torch.tensor(aa)
ii = [i for i, p in support]; pp = [p for i, p in support]
def fwd(x):
    h = torch.zeros(n); S = torch.zeros(n, P)
    for t in range(T):
        direct = torch.einsum('ipj,j->ip', ER, h) + torch.einsum('ipj,j->ip', EW, x[t]) + Eb
        hn = torch.tanh(Rt @ h + Wt @ x[t] + bt); g = 1-hn*hn; S = g[:, None]*(Rt @ S + direct); h = hn
    return h, S
hist = lambda w: X0 + (SD*(B @ w)).reshape(T, n)
def G(w):
    h, S = fwd(hist(w)); return torch.cat([h, S[ii, pp]*wsup])
h0 = fwd(X0)[0]
def ysec(t):
    y = torch.zeros(n)
    Hf = lambda yy: fwd(hist(torch.cat([yy, t])))[0]-h0
    for _ in range(40):
        f = Hf(y)
        if f.abs().max() < 1e-16: break
        y = y - torch.linalg.solve(torch.autograd.functional.jacobian(Hf, y), f)
    assert float(Hf(y).abs().max()) < 1e-13
    return y
def svec(z):
    t = A*torch.as_tensor(z); y = ysec(t); w = torch.cat([y, t]); h, S = fwd(hist(w))
    return float(y.abs().max())/ah, (S[ii, pp]*wsup).detach()
Psi0 = Lt @ svec(np.zeros(r))[1]
def Phi(z):
    u, s = svec(z); return u, ((Kt @ (Lt @ s - Psi0))/A).numpy(), s.numpy()
c78 = R.T @ np.full(n, 7/8)/(math.sqrt(n)*max(1., np.linalg.norm(R)))
cw = np.array([c78[i] for i, p in support])
D78 = lambda d: float(np.linalg.norm(cw*d))
beta = np.array([float(Q(x)) for x in res['beta3']]); M3 = np.array(res['M3_upper']); bmin = beta.min()
print(f'== mode {mode}; beta3 min {bmin:.6e}; 2beta_min {2*bmin:.6e}; M3 {np.round(M3,4)}', flush=True)
if mode == 'core':
    # DPhi(0) by central differences along the exact section (h small)
    hstep = 1e-4; Dphi = np.zeros((r, r))
    for j in range(r):
        e = np.zeros(r); e[j] = hstep; Dphi[:, j] = (Phi(e)[1]-Phi(-e)[1])/(2*hstep)
    print(' |DPhi(0)-I| max', float(np.abs(Dphi-np.eye(r)).max()), flush=True)
    rng = np.random.default_rng(11); worst = np.zeros(r); worstu = 0; mind = math.inf
    pts = [np.array(c) for c in itertools.product((-1., 1.), repeat=r)][:32]
    for _ in range(160):
        z = rng.uniform(-1, 1, r); z[rng.integers(r)] = rng.choice([-1., 1.]); pts.append(z)
    for z in pts:
        u1, p1, s1 = Phi(z); u2, p2, s2 = Phi(-z); worstu = max(worstu, u1, u2)
        rem = np.abs(p1-p2-2*(Dphi @ z)); worst = np.maximum(worst, rem/(M3/3))
        mind = min(mind, D78(s1-s2))
    print(f' {len(pts)} boundary antipodes (32 corner pairs + 160 random face points): max |y|/a_h {worstu:.4f}', flush=True)
    print(f' odd remainder |Phi(z)-Phi(-z)-2DPhi(0)z|_i / (M3_i/3): max per face {np.round(worst,4)} (<=1 required)', flush=True)
    print(f' min antipodal D_7/8 {mind:.6e}; /2eps {mind/2e-3:.4f}; /2beta_min {mind/(2*bmin):.4f}', flush=True)
if mode == 'face':
    face = int(sys.argv[2]); rng = np.random.default_rng(100+face)
    def obj(u):
        z = np.insert(np.tanh(u), face, 1.); _, _, s1 = Phi(z); _, _, s2 = Phi(-z); return D78(s1-s2)
    grid = list(itertools.product((-.9, 0., .9), repeat=r-1)); grid = [grid[i] for i in rng.choice(len(grid), 40, replace=False)] + [tuple([0.]*(r-1))]
    vals = sorted((obj(np.arctanh(np.array(g))), g) for g in grid); best = vals[0][0]; arg = vals[0][1]
    for _, g in vals[:3]:
        rr = minimize(obj, np.arctanh(np.array(g)), method='Nelder-Mead', options={'maxiter': 150, 'xatol': 1e-4, 'fatol': 1e-12})
        if rr.fun < best: best, arg = rr.fun, np.round(np.tanh(rr.x), 3)
    print(f' face {face}: adversarial min antipodal D_7/8 {best:.6e} at {arg}; /2eps {best/2e-3:.4f}; /2beta_face {best/(2*beta[face]):.4f}; /2beta_min {best/(2*bmin):.4f}', flush=True)
if mode == 'majorant':
    seed, N = int(sys.argv[2]), int(sys.argv[3]); rng = np.random.default_rng(seed)
    bd = np.load(EXP/'bounds_192.npz'); M2 = np.concatenate([bd['HH'], bd['HS']]); Mt3 = np.concatenate([bd['HH3'], bd['HS3']])
    amps = np.r_[np.full(n, ah), aa]
    d2 = torch.func.jacfwd(torch.func.jacrev(G)); d3 = torch.func.jacfwd(d2)
    w2 = w3 = 0.
    for k in range(N):
        y = amps*(rng.choice([-1., 1.], n+r) if k % 2 == 0 else rng.uniform(-1, 1, n+r))
        yt = torch.tensor(y); T3 = d3(yt).detach().numpy(); T2 = d2(yt).detach().numpy()
        w3 = max(w3, float((np.abs(T3)/np.maximum(Mt3, 1e-300)).max())); w2 = max(w2, float((np.abs(T2)/np.maximum(M2, 1e-300)).max()))
    print(f' majorant seed {seed}: {N} points of the 10-D box (half corners): max |3rd|/HH3,HS3 {w3:.5f}; max |2nd|/HH,HS {w2:.5f} (<=1 required)', flush=True)
if mode == 'fd':
    # End-to-end: directional third derivatives of Phi along the CURVED fixed-h section (implicit y''') vs bound
    seed, N = int(sys.argv[2]), int(sys.argv[3]); rng = np.random.default_rng(seed)
    sel3 = np.load(EXP/'bounds_192.npz')['selected3']  # r x r x r x r bound on |D^3 Psi| (t coords)
    absK = np.abs(Kt.numpy()); worst = 0.
    for k in range(N):
        z0 = rng.uniform(-.8, .8, r); u = rng.normal(size=r); u /= np.abs(u).max()
        hs = 0.04; g = lambda s: Phi(z0+s*u)[1]
        f = [g(m*hs) for m in (-2, -1, 1, 2)]
        d3fd = (f[3]-2*f[2]+2*f[1]-f[0])/(2*hs**3)
        bound = np.einsum('im,mabc,a,b,c->i', absK, sel3, aa*np.abs(u), aa*np.abs(u), aa*np.abs(u))/aa
        worst = max(worst, float((np.abs(d3fd)/bound).max()))
    print(f' fd seed {seed}: {N} interior points/directions: max |D^3 Phi_i[u,u,u]| (finite diff) / certified bound = {worst:.5f} (<=1 required)', flush=True)
