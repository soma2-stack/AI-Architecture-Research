"""Numerical check of Theorems R1/R3 for the VISIBLE-frame decomposition actually used in Theorem Q:
X_L = m restricted to physical coords 1..k-1;  spike sigma_L x_{p(L)},  sigma_L = beta0 prod a gamma_t,
gamma_t = g_t[p] (p != 0) or mean(g_t[1:]) (p = 0);  x_p = e_p - (c_k/sqrt k) 1_X,  x_0 = 1_X / sqrt k.
Adversarial maximisation of ||X_L - sigma_L x_p|| (sign ascent + structured starts); must stay <= min(R1, R3)."""
import json, math, sys
import numpy as np, torch
from core import build, node, G_HI, G_LO, S_G
from qbounds import remainder_budget, remainder_budget_R3
torch.set_num_threads(4)

def vis_rem(S, G):
    T = S['t']; U, Pi, a, k, d = T['U'], T['Pi'], S['a'], S['k'], S['d']
    R_, L, _ = G.shape
    y = torch.zeros(R_, k); y[:, 0] = S['beta0']; sig = torch.full((R_,), S['beta0'])
    for t in range(1, L + 1):
        g = G[:, t - 1]; p = node(t - 1, d)
        gam = g[:, 1:].mean(dim=1) if p == 0 else g[:, p]
        sig = sig * a * gam
        y = a * ((g * (y @ U)) @ U) @ Pi.T
    m = y @ U; X = m[:, 1:]
    p = node(L, d); c = S['ck'] / math.sqrt(k)
    xp = torch.full((k - 1,), 1 / math.sqrt(k)) if p == 0 else -c * torch.ones(k - 1)
    if p != 0: xp[p - 1] += 1.0
    return (X - sig[:, None] * xp[None, :]).norm(dim=1)

def structured(S, L):
    k, d = S['k'], S['d']; out = []
    g = np.full((L, k), G_HI); g[0, 1::2] = G_LO; out.append(g)                       # half/half then high
    g = np.full((L, k), G_HI); g[0, 1::2] = G_LO
    for t in range(2, L + 1): g[t - 1, node(t - 1, d)] = G_LO                         # kill spike, keep rest
    out.append(g)
    g = np.full((L, k), G_LO); g[0] = G_HI; g[0, 1::2] = G_LO
    for t in range(2, L + 1):
        for j in range(1, t): g[t - 1, (d - j) % d] = G_HI                            # wake window
    out.append(g)
    return np.stack(out)

out = []
for n in [int(x) for x in (sys.argv[1] if len(sys.argv) > 1 else '200,400').split(',')]:
    S = build(n); d = S['d']; Rt = remainder_budget(S, d); R3 = remainder_budget_R3(S, d)
    rng = np.random.default_rng(5)
    for L in [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48]:
        if L > d: break
        G0 = np.concatenate([structured(S, L), rng.choice([G_LO, G_HI], size=(40, L, S['k']))])
        G = torch.tensor(G0, requires_grad=True); step = 0.25 * (G_HI - G_LO); best = 0.0
        for it in range(200):
            v = vis_rem(S, G); best = max(best, float(v.max()))
            gr, = torch.autograd.grad(v.sum(), G)
            with torch.no_grad():
                G += step * torch.sign(gr); G.clamp_(G_LO, G_HI)
            if it % 50 == 49: step *= 0.6
        with torch.no_grad():
            Gv = torch.where(G > 0.5 * (G_HI + G_LO), torch.tensor(G_HI), torch.tensor(G_LO))
            best = max(best, float(vis_rem(S, Gv).max()), float(vis_rem(S, torch.tensor(G0[:3])).max()))
        unit = S['a'] * S_G * S['beta0'] * S['lam'] ** (L - 1)
        row = dict(n=n, L=L, F_adv=best / unit, F_R1=Rt[L] / unit, F_R3=R3[L] / unit, ok=bool(best <= R3[L] * (1 + 1e-12)))
        out.append(row); print(json.dumps(row), flush=True)
json.dump(out, open('r3_check.json', 'w'), indent=1)
