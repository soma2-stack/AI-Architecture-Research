"""Exploration (guidance only): exact fixed-query linear capacities of single- and two-pulse fixed-feature families
on the ACTUAL dense model. For a fixed query xi, antipodal answer differences are EXACTLY linear in the pulse
amplitude displacements (gates are affine in squared amplitudes; two-pulse bilinear terms are even and cancel), so the
best m-dimensional linear section has exact min half-separation w_R ||H|| t0 sigma_m(W)."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, '../claude_rotating_gate_review_20261001'); sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_rotating import family, weights
from check_aperiodic import G_LO, G_HI
torch.set_num_threads(8)
EPS = 1e-3

def setup(n):
    F = family(n, 1.0); R, b = F['R'], F['b']; k, l, a = F['k'], F['l'], F['a']; d = n // 4; r = k - 1
    wR = float(weights(F)[0]); beta = max(1.0, float(R.norm())); H = torch.full((l,), 0.4)
    E = torch.zeros(n, r); E[1:k] = torch.eye(r)
    Gw = torch.cat([torch.ones(k), 1 - H ** 2])
    B = torch.zeros(n, r); N = 3 * n
    for t in range(1, N + 2): B = Gw[:, None] * (R @ B + (0.0 if t == 1 else 1.0) * E)
    return dict(F=F, R=R, k=k, l=l, a=a, d=d, r=r, n=n, wR=wR, beta=beta, H=H, E=E, Gw=Gw, Bpre=B)

def query(S, kind, rng):
    n, k, d = S['n'], S['k'], S['d']; v = torch.full((n,), 0.2)
    if kind == 'pairs':                       # theorem's pattern: 0.45 on second coordinate of each non-cycled pair
        m = (k - d) // 2; J = [d + 2 * j - 1 for j in range(1, m + 1)]; v[J] = 0.45
    elif kind == 'alt_nc':                    # alternate along non-cycled coordinates
        for c in range(d, k): v[c] = 0.45 if (c - d) % 2 else 0.2
    elif kind == 'random':
        v[:k] = torch.tensor(rng.choice([0.2, 0.45], k))
    g = 1 - torch.tanh(v + S['F']['b']) ** 2                  # h_T = 0
    return S['R'].T @ g / (S['beta'] * math.sqrt(n))

def W_single(S, coords, xi):
    V = S['R'] @ S['Bpre'] + S['E']; y = S['R'].T @ xi
    return V[coords].T * y[coords][None, :]                    # columns V^T e_c y_c

def W_two(S, coords1, coords2, xi, gap, tau0):
    R, E, Gw, n, k = S['R'], S['E'], S['Gw'], S['n'], S['k']
    V1 = R @ S['Bpre'] + E
    G1 = Gw.clone(); G1[coords1] = 1 - tau0
    B = G1[:, None] * V1
    for _ in range(gap): B = Gw[:, None] * (R @ B + E)
    V2 = R @ B + E
    G2 = Gw.clone(); G2[coords2] = 1 - tau0
    y2 = R.T @ xi; y1 = R.T @ (G2 * y2)
    for _ in range(gap): y1 = R.T @ (Gw * y1)
    W1 = V1[coords1].T * y1[coords1][None, :]; W2 = V2[coords2].T * y2[coords2][None, :]
    return torch.cat([W1, W2], 1)

def pair_cols(W, pairs):                    # combine individual columns into pair columns (same amplitude on a pair)
    return torch.stack([W[:, i] + W[:, j] for i, j in pairs], 1)

def capacity(S, W, t0):
    s = torch.linalg.svdvals(W) * S['wR'] * float(S['H'].norm()) * t0
    return {'cnt>1.0eps': int((s > EPS).sum()), 'cnt>1.2eps': int((s > 1.2 * EPS).sum()), 'cnt>2eps': int((s > 2 * EPS).sum()),
            'top': float(s[0]), 'sv_at_cols': [float(x) for x in s[[0, len(s) // 4, len(s) // 2, 3 * len(s) // 4, len(s) - 1]]]}

if __name__ == '__main__':
    rng = np.random.default_rng(1); out = []
    for n in [int(v) for v in sys.argv[1].split(',')]:
        S = setup(n); k, d = S['k'], S['d']; t0 = 0.08; tau0 = 0.08
        NC = list(range(d, k)); CY = list(range(1, d)); MEM = list(range(1, k))
        pairs = [(d + 2 * j - 2, d + 2 * j - 1) for j in range(1, (k - d) // 2 + 1)]
        stag = [(d + 2 * j - 1, d + 2 * j) for j in range(1, (k - d - 1) // 2 + 1)]
        res = {'n': n, 'k': k, 'd': d, 'L_noncycled': k - d, 'pairs': len(pairs), 'r': S['r']}
        for qk in ('pairs', 'alt_nc', 'random'):
            xi = query(S, qk, rng)
            Ws = W_single(S, NC, xi); res[f'{qk}:single_pairs'] = capacity(S, pair_cols(Ws, [(i - d, j - d) for i, j in pairs]), t0)
            res[f'{qk}:single_indiv_NC'] = capacity(S, Ws, t0)
            res[f'{qk}:single_indiv_MEM'] = capacity(S, W_single(S, MEM, xi), t0)
            for gap in (1, d // 2, d):
                Wt = W_two(S, NC, NC, xi, gap, tau0)
                L = len(NC)
                Wt_pairs = torch.cat([pair_cols(Wt[:, :L], [(i - d, j - d) for i, j in pairs]), pair_cols(Wt[:, L:], [(i - d, j - d) for i, j in stag])], 1)
                res[f'{qk}:two_staggered_pairs_gap{gap}'] = capacity(S, Wt_pairs, t0)
                res[f'{qk}:two_indiv_NC_gap{gap}'] = capacity(S, Wt, t0)
                res[f'{qk}:two_indiv_MEM_gap{gap}'] = capacity(S, W_two(S, MEM, MEM, xi, gap, tau0), t0)
        out.append(res); print(json.dumps(res), flush=True)
    json.dump(out, open('explore.json', 'w'), indent=1)
