"""Two pulses on the non-cycled (stationary) block: directions invisible to the best fixed query (collapse directions)
-- are they visible to query-dependent worst-case box queries (leak channel)? Exact actual-model answers."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
exec(open('rms_capacity.py').read().rsplit("if __name__ == '__main__':", 1)[0])
sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_aperiodic import box_max

def run(n, gap, ms, samples=40, seed=0):
    S = setup(n); k, d = S['k'], S['d']; t0 = tau0 = 0.08; rng = np.random.default_rng(seed + n + gap)
    NC = list(range(d, k)); L = len(NC)
    cols = T_blocks(S, [(NC, 0), (NC, gap)], tau0)
    Vm = torch.stack([v for v, _ in cols]); Zm = torch.stack([z for _, z in cols]); scale = S['wR'] * float(S['H'].norm())
    # fixed query (all-g_lo on NC): W = answer jacobian; collapse directions = bottom right singular vectors
    v = torch.full((n,), 0.2); v[NC] = 0.45; g = 1 - torch.tanh(v + S['F']['b']) ** 2
    W = -(Vm.T * (Zm @ g)[None, :])                     # r x 2L : column c = -V_c (Z_c . g)
    U, s, Vh = torch.linalg.svd(W, full_matrices=True); sfix = s * scale * t0
    nstrong = int((sfix > 0.1 * EPS).sum()); null = Vh[nstrong:].T          # directions with fixed-query visibility < 0.1 eps
    out = {'n': n, 'gap': gap, 'L': L, 'fixed_query_strong_dirs': nstrong, 'collapse_dim': null.shape[1]}
    def sep(delta):
        Y = -(Zm.T * delta[None, :]) @ Vm
        return scale * math.sqrt(n) * box_max(Y, n, starts=8)
    for m in ms:
        A = torch.tensor(rng.normal(size=(null.shape[1], m))); Qs, _ = torch.linalg.qr(null @ A)
        rho = t0 / float(Qs.norm(dim=1).max())
        seps = []
        for _ in range(samples):
            u = torch.tensor(rng.normal(size=m)); u /= u.norm(); seps.append(sep(rho * (Qs @ u)))
        # also the fixed-query visibility of the same section, for contrast
        fq = float(torch.linalg.svdvals(W @ Qs)[-1]) * scale * rho
        out[f'm{m}'] = {'rho': rho, 'worstquery_min': min(seps), 'worstquery_median': float(np.median(seps)), 'fixed_query_min': fq}
    return out

if __name__ == '__main__':
    for n in [int(x) for x in sys.argv[1].split(',')]:
        d = n // 4
        for gap in (1, d // 2):
            r = run(n, gap, (1, 5, 20, 45)); print(json.dumps(r), flush=True)
