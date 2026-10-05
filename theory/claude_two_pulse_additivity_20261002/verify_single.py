"""Verification of Theorem L (single pulse, individual stationary coordinates, zero-sum amplitude section) on the ACTUAL
dense family. Exact whole-sphere minimum of the fixed-query antipodal half-separation (sigma_min on the zero-sum
subspace), analytic bound, admissibility over sampled section points, endpoint, radius."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, '../claude_rotating_gate_review_20261001'); sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_rotating import family, weights
from check_aperiodic import G_LO, G_HI
torch.set_num_threads(8)
SG = (G_HI - G_LO) / 2; TAU0 = T0 = 0.08

def run(n, samples=40, seed=0):
    F = family(n, 1.0); R, b = F['R'], F['b']; k, l, a, e = F['k'], F['l'], F['a'], F['e']; d = n // 4; r = k - 1
    assert d == F['d']
    wR = float(weights(F)[0]); beta = max(1.0, float(R.norm())); H = torch.full((l,), 0.4)
    L = k - d; Lp = 2 * (L // 2); NCp = list(range(d, d + Lp))           # 0-based physical stationary coordinates used
    s = torch.tensor([1.0 if i % 2 == 0 else -1.0 for i in range(Lp)])
    E = torch.zeros(n, r); E[1:k] = torch.eye(r); N = 3 * n
    Gw = torch.cat([torch.ones(k), 1 - H ** 2]); B = torch.zeros(n, r)
    for t in range(1, N + 2): B = Gw[:, None] * (R @ B + (0.0 if t == 1 else 1.0) * E)
    V = R @ B + E
    v = torch.full((n,), 0.2); v[d:k] = 0.45                                   # query: g_lo on ALL stationary coords
    g = 1 - torch.tanh(v + b) ** 2; xi = R.T @ g / (beta * math.sqrt(n)); y = R.T @ xi
    W = V[NCp].T * y[NCp][None, :]                                             # r x Lp
    Zs = torch.eye(Lp) - torch.ones(Lp, Lp) / Lp; Uz, _, _ = torch.linalg.svd(Zs); Qz = Uz[:, :Lp - 1]   # zero-sum basis
    smin = float(torch.linalg.svdvals(W @ Qz)[-1])
    exact_min_half = wR * float(H.norm()) * T0 * smin
    ck = 1 / (math.sqrt(k) - 1); f = L / k; m = (1 - a ** (N + 1)) / (1 - a)
    Ec = G_LO + (ck + ck * ck) * G_HI - (1 + ck) ** 2 * (f * G_LO + (1 - f) * G_HI)
    yscaled = float(y[d] * beta * math.sqrt(n) / a ** 2)
    analytic = 0.4 * T0 * a * a * (m / n) * math.sqrt(l / n) * abs(Ec)
    conservative = 0.4 * T0 * 0.990025 * 0.9502 * 0.70710 * 2 * 0.495 * 0.076783
    # admissibility over sampled section points
    rng = np.random.default_rng(seed + n)
    def hist(u):
        z = torch.zeros(k); z[NCp] = s * torch.sqrt(TAU0 + T0 * u)
        hs = [torch.zeros(n)] + [torch.cat([torch.zeros(k), H]) for _ in range(N + 1)] + [torch.cat([z, H]), torch.zeros(n)]
        return hs, [torch.atanh(hs[t]) - R @ hs[t - 1] - b for t in range(1, len(hs))]
    us = [torch.zeros(Lp)]
    for c in range(3):                                                        # zero-sum axis-like and extreme points
        u = torch.zeros(Lp); u[2 * c] = 1 / math.sqrt(2); u[2 * c + 1] = -1 / math.sqrt(2); us += [u, -u]
    u = s / s.norm(); us += [u, -u]                                           # alternating pattern (max |sum z| stress)
    blk = torch.cat([torch.ones(Lp // 2), -torch.ones(Lp - Lp // 2)]); blk -= blk.mean(); us += [blk / blk.norm(), -blk / blk.norm()]
    for _ in range(samples):
        w = torch.tensor(rng.normal(size=Lp)); w -= w.mean(); us.append(w / w.norm())
    _, xs0 = hist(torch.zeros(Lp)); X0 = torch.stack(xs0); maxin = 0.0; maxrad = 0.0; maxhT = 0.0
    for u in us[1:]:
        hs, xs = hist(u); X = torch.stack(xs); maxin = max(maxin, float(X.abs().max())); maxrad = max(maxrad, float((X - X0).norm()))
        h = hs[-3]
        for x in xs[-2:]: h = torch.tanh(R @ h + x + b)
        maxhT = max(maxhT, float(h.abs().max()))
    return {'n': n, 'k': k, 'd': d, 'L': L, 'section_dim': Lp - 1, 'floor_n4_minus2': n // 4 - 2, 'floor_n8': n // 8,
            'exact_min_half_sep': exact_min_half, 'analytic_bound_exact_consts': analytic, 'conservative_bound': conservative,
            'E_formula': Ec, 'y_c_scaled_measured': yscaled, 'y_constant_on_NC_spread': float((y[d:k].max() - y[d:k].min()) / y[d:k].abs().max()),
            'max_abs_input': maxin, 'max_radius': maxrad, 'max_|h_T|': maxhT, 'samples': len(us)}

if __name__ == '__main__':
    out = []
    for n in [int(v) for v in sys.argv[1].split(',')]:
        rr = run(n); out.append(rr); print(json.dumps(rr), flush=True)
    json.dump(out, open('verify_single.json', 'w'), indent=1)
