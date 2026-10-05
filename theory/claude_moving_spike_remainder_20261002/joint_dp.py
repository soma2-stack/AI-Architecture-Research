"""Theorem R4: rigorous JOINT (spike, remainder) budget by an interval dynamic programme over the per-step
inequalities of Theorems R1/R3 (normalised units: Sigma_t = sigma_t/(beta0 lam^t), rho_t = ||r_t||/(beta0 lam^t)).

  t = 1 (node 0):  Sigma_1 = gbar/g_hi in [glo^, 1],  rho_1 <= sqrt((1-1/k)(1-Sigma_1)(Sigma_1-glo^))   (Bhatia-Davis)
  node-0 step:     Sigma' = u Sigma (u in [glo^,1]),   rho' <= rho + Sigma * omega0/g_hi                  (triangle)
  cycle step:      Sigma' = u Sigma,  rho' <= min( rho + Sigma*omega_c/g_hi ,
                                                   sqrt(rho^2 + A Sigma^2 + 2 c' (1-u) Sigma rho) )        (R1, R3)
  A = phi* c_k^2 (1-1/k),  c' = c_k sqrt(1-1/k).
Sigma is binned on [0,1]; u on [glo^,1]; every transition uses the conservative end of each bin and spreads
its value over all target bins it can reach, so V_L(bin) >= sup rho_L over all legal trajectories with Sigma_L in bin.
Output: for each L, arrays (Sigma_hi(bin), V_L(bin)); UB_L = scale beta0 lam^L max_bin [Sigma_hi row_p + V M]."""
import math
import numpy as np
from core import build, node, G_HI, G_LO, S_G
from qbounds import phi_star


def joint_budget(S, Lmax, nb=600, nu=60):
    k, d = S['k'], S['d']
    glo = G_LO / G_HI
    cp = S['ck'] * math.sqrt(1 - 1 / k); A = phi_star() * S['ck'] ** 2 * (1 - 1 / k)
    w0 = S_G * math.sqrt(1 - 1 / k) / G_HI; wc = 2 * S['ck'] * S_G * math.sqrt(1 - 2 / k) / G_HI
    edges = np.linspace(0.0, 1.0, nb + 1)          # Sigma bins [edges[j], edges[j+1]]
    hi = edges[1:]
    uedges = np.linspace(glo, 1.0, nu + 1)
    V = np.full(nb, -np.inf)
    # t = 1: Sigma_1 in [glo, 1]; rho_1 bound = max over the bin of the Bhatia-Davis value
    for j in range(nb):
        lo_, hi_ = edges[j], edges[j + 1]
        if hi_ < glo: continue
        a_, b_ = max(lo_, glo), hi_
        mid = 0.5 * (1 + glo)
        s = min(max(mid, a_), b_)                   # maximiser of (1-s)(s-glo) on the bin
        V[j] = math.sqrt(max(0.0, (1 - 1 / k) * (1 - s) * (s - glo)))
    out = {1: (hi.copy(), V.copy())}
    for t in range(2, Lmax + 1):
        p = node(t - 1, d)
        Vn = np.full(nb, -np.inf)
        live = np.where(np.isfinite(V))[0]
        for i in range(nu):
            u0, u1 = uedges[i], uedges[i + 1]
            Sg = hi[live]; rho = V[live]
            if p == 0:
                newrho = rho + Sg * w0
            else:
                tri = rho + Sg * wc
                en = np.sqrt(rho ** 2 + A * Sg ** 2 + 2 * cp * (1 - u0) * Sg * rho)
                newrho = np.minimum(tri, en)
            lo_t = u0 * edges[live]; hi_t = u1 * hi                                     # reachable Sigma' interval
            jlo = np.clip(np.floor(lo_t * nb).astype(int), 0, nb - 1)
            jhi = np.clip(np.ceil(u1 * edges[live + 1] * nb).astype(int) - 1, 0, nb - 1)
            for a_, b_, r_ in zip(jlo, jhi, newrho):
                if r_ > Vn[a_:b_ + 1].min():
                    Vn[a_:b_ + 1] = np.maximum(Vn[a_:b_ + 1], r_)
        V = Vn
        out[t] = (hi.copy(), V.copy())
    return out


if __name__ == '__main__':
    import json, sys
    from qbounds import remainder_budget, remainder_budget_R3
    res = {}
    for n in (200, 400, 1000):
        S = build(n); Lm = min(64, S['d'])
        jb = joint_budget(S, Lm)
        Rt = remainder_budget(S, Lm); R3 = remainder_budget_R3(S, Lm)
        rows = []
        for L in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64):
            if L > Lm: break
            hi, V = jb[L]; rmax = np.max(V[np.isfinite(V)])
            unit = S['a'] * S_G * S['beta0'] * S['lam'] ** (L - 1)
            rows.append(dict(L=L, F_R4=rmax * S['beta0'] * S['lam'] ** L / unit, F_R3=R3[L] / unit, F_R1=Rt[L] / unit))
        res[n] = rows
        print(n, [(r['L'], round(r['F_R4'], 3), round(r['F_R3'], 3)) for r in rows], flush=True)
    json.dump(res, open('joint_dp.json', 'w'), indent=1)
