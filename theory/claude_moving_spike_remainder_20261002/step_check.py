"""Per-step check of the R1/R3 inequalities along random and adversarial-pattern legal trajectories (visible frame)."""
import json, math
import numpy as np
from core import build, node, G_HI, G_LO, S_G
from qbounds import phi_star
out = {}
rng = np.random.default_rng(11)
for n in (200, 400):
    S = build(n); k, d, U, Pi, a = S['k'], S['d'], S['U'], S['Pi'], S['a']
    lam = S['lam']; c = S['ck'] / math.sqrt(k); cp = S['ck'] * math.sqrt(1 - 1 / k); A = phi_star() * cp ** 2
    wc = 2 * S['ck'] * S_G * math.sqrt(1 - 2 / k) / G_HI
    worst_en, worst_tri, worst_t1 = -1e9, -1e9, -1e9
    for trial in range(300):
        L = int(rng.integers(2, 40)); mode = trial % 3
        y = np.zeros(k); y[0] = S['beta0']; sig = S['beta0']
        def visible(y, sig, t):
            m = U @ y; X = m[1:]; p = node(t, d)
            xp = np.full(k - 1, 1 / math.sqrt(k)) if p == 0 else -c * np.ones(k - 1)
            if p != 0: xp[p - 1] += 1
            return np.linalg.norm(X - sig * xp) / (lam ** t), sig / (lam ** t)
        rho, Sg = visible(y, sig, 0)
        for t in range(1, L + 1):
            if mode == 0: g = rng.uniform(G_LO, G_HI, k)
            elif mode == 1: g = rng.choice([G_LO, G_HI], k)
            else:
                g = np.full(k, G_HI if rng.random() < 0.5 else G_LO); g[rng.integers(0, k, k // 3)] = G_LO
            p = node(t - 1, d)
            gam = g[1:].mean() if p == 0 else g[p]
            sig = sig * a * gam; y = a * (Pi @ (U @ (g * (U @ y))))
            rho2, Sg2 = visible(y, sig, t)
            u = gam / G_HI
            if p == 0:
                if t == 1:
                    bd = math.sqrt((1 - 1 / k) * (1 - u) * (u - G_LO / G_HI))
                    worst_t1 = max(worst_t1, rho2 - bd)
            else:
                worst_tri = max(worst_tri, rho2 - (rho + Sg * wc))
                worst_en = max(worst_en, rho2 ** 2 - (rho ** 2 + A * Sg ** 2 + 2 * cp * (1 - u) * Sg * rho))
            rho, Sg = rho2, Sg2
    out[n] = dict(max_violation_energy=worst_en, max_violation_triangle=worst_tri, max_violation_t1=worst_t1)
    print(n, out[n])
json.dump(out, open('step_check.json', 'w'), indent=1)
