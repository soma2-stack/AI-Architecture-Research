"""Two pulses on the CYCLED block: separate the strong cycle-average (frequency-0) channel, where pulses collapse to a
phase-shifted sum, from 'difference' directions. Worst-case box-query visibility of sections inside the subspace where
the single-pulse-equivalent channel cancels (two-pulse null directions of the strongest worst-query structure).
Difference directions are taken as delta2 = -P delta1 with P the relative shift found numerically by maximizing
cancellation in the RMS Gram (generic version: bottom eigen-directions of RMS Gram restricted to large-norm params)."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
exec(open('rms_capacity.py').read().rsplit("if __name__ == '__main__':", 1)[0])
sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_aperiodic import box_max

def run(n, gap, ms, samples=40, seed=0):
    S = setup(n); k, d = S['k'], S['d']; t0 = tau0 = 0.08; rng = np.random.default_rng(seed + n + gap)
    CY = list(range(2, d - 1)); p1 = len(CY)
    scale = S['wR'] * float(S['H'].norm())
    c1 = T_blocks(S, [(CY, 0)], tau0); c2 = T_blocks(S, [(CY, 0), (CY, gap)], tau0)
    V1 = torch.stack([v for v, _ in c1]); Z1 = torch.stack([z for _, z in c1])
    V2 = torch.stack([v for v, _ in c2]); Z2 = torch.stack([z for _, z in c2])
    def sep(Vm, Zm, delta):
        return scale * math.sqrt(n) * box_max(-(Zm.T * delta[None, :]) @ Vm, n, starts=8)
    # 'difference' subspace: pairs (delta, -delta') where single-pulse worst-query image matches -> construct via the
    # frequency-0 functional: f(delta) = sum over pulse of (shifted) delta_c * (cycle-average credit). Null space of the
    # 2p x 1 averaged-credit functional per shifted coordinate: use RMS-Gram eigenvectors of the two-pulse design with the
    # SMALLEST eigenvalues as candidates (these include all cancellation directions).
    Q = rms_gram(c2, t0); ev, U = torch.linalg.eigh(Q)
    out = {'n': n, 'gap': gap, 'params_two': 2 * p1}
    # single-pulse reference sections of same dims (random spread in CY params, weak part)
    for m in ms:
        A = torch.tensor(rng.normal(size=(p1 + 1, m))); Qs, _ = torch.linalg.qr(U[:, :p1 + 1] @ A)   # bottom p1+1 RMS directions
        rho = t0 / float(Qs.norm(dim=1).max()); seps = []
        for _ in range(samples):
            u = torch.tensor(rng.normal(size=m)); u /= u.norm(); seps.append(sep(V2, Z2, rho * (Qs @ u)))
        A1 = torch.tensor(rng.normal(size=(p1, m))); Q1, _ = torch.linalg.qr(A1); rho1 = t0 / float(Q1.norm(dim=1).max()); seps1 = []
        for _ in range(samples):
            u = torch.tensor(rng.normal(size=m)); u /= u.norm(); seps1.append(sep(V1, Z1, rho1 * (Q1 @ u)))
        out[f'm{m}'] = {'two_bottom_rms_subspace_min': min(seps), 'two_median': float(np.median(seps)),
                        'single_random_min': min(seps1), 'single_median': float(np.median(seps1))}
    return out

if __name__ == '__main__':
    for n in [int(x) for x in sys.argv[1].split(',')]:
        d = n // 4
        for gap in (d // 2,):
            r = run(n, gap, (1, 5, 20)); print(json.dumps(r), flush=True)
