"""Do query-dependent (demodulating) worst-case box queries make ROTATING-mode pulse directions visible?
For sections restricted to the weak (rotating) part of the cycled-block pulse parameters, compute the actual
worst permitted box-query half-separation at sampled sphere points (vertex search), for section dims m."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
exec(open('rms_capacity.py').read().rsplit("if __name__ == '__main__':", 1)[0])
sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_aperiodic import box_max

def run(n, design, ms, samples=60, seed=0):
    S = setup(n); k, d = S['k'], S['d']; t0 = tau0 = 0.08; rng = np.random.default_rng(seed + n)
    CY = list(range(2, d - 1))                      # avoid e1 (0) and coordinate 1, d-1 (Householder-adjacent)
    pl = [(CY, 0)] if design == 'single' else [(CY, 0), (CY, d // 2)]
    cols = T_blocks(S, pl, tau0); p = len(cols)
    Q = rms_gram(cols, t0); ev, U = torch.linalg.eigh(Q); U = U.flip(1)
    weak = U[:, 3:]                                  # drop the strong (cycle-average / leak) directions
    Vm = torch.stack([v for v, _ in cols]); Zm = torch.stack([z for _, z in cols])
    scale = S['wR'] * float(S['H'].norm())
    out = {'n': n, 'design': design, 'params': p}
    for m in ms:
        A = torch.tensor(rng.normal(size=(weak.shape[1], m))); Qs, _ = torch.linalg.qr(weak @ A)   # random m-dim weak subspace
        rho = t0 / float(Qs.norm(dim=1).max())                                                     # per-coordinate |delta| <= t0
        seps = []
        for _ in range(samples):
            u = torch.tensor(rng.normal(size=m)); u /= u.norm(); delta = rho * (Qs @ u)
            # T_delta = - sum_c delta_c outer(V_c, Z_c);  answer(g) = T_delta g ;  Y = T_delta^T (n x r)
            Y = -(Zm.T * delta[None, :]) @ Vm            # n x r
            seps.append(scale * math.sqrt(n) * box_max(Y, n, starts=8))
        out[f'm{m}'] = {'rho_l2': rho, 'min_half_sep': min(seps), 'median': float(np.median(seps)), 'max': max(seps)}
    return out

if __name__ == '__main__':
    for n in (200, 400):
        for design in ('single', 'two'):
            r = run(n, design, (1, 2, 5, 10, 25)); print(json.dumps(r), flush=True)
