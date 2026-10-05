"""Adversarial maximisation of the remainder r_L = y_L - sigma_L e_{p(L)} over legal gate sequences.
Reports F_L = ||r_L|| / (a s_g beta0 lam^(L-1)), lam = a g_hi, and the same for the block-visible part ||V^T U r_L||,
against the rigorous triangle bound F_L <= N0(L) + (omega_cyc/s_g)(L - N0(L)) (Theorem R1).
Numerical lower bounds only (sign-gradient ascent on a convex-per-step objective + structured starts)."""
import json, math, sys, time
import numpy as np, torch
from core import build, run_torch, node, G_HI, G_LO, S_G

torch.set_num_threads(8)


def objective(S, G, which):
    y, sigma, p = run_torch(S, G)
    r = y.clone(); r[:, p] = r[:, p] - sigma
    if which == 'latent':
        return r.norm(dim=1)
    if which == 'block':
        return (r @ S['t']['B'].T).norm(dim=1)
    if which == 'orth':                       # orthogonal remainder (decomposition A)
        r2 = y.clone(); r2[:, p] = 0
        return r2.norm(dim=1)


def structured(S, L):
    k, d = S['k'], S['d']; out = []
    hi, lo = G_HI, G_LO
    # (a) half/half at node-0 step, then g_hi
    g = np.full((L, k), hi); g[0, ::2] = lo; out.append(g)
    # (b) NC-accumulation: physical 0 at g_lo, everything else g_hi
    g = np.full((L, k), hi); g[:, 0] = lo; out.append(g)
    # (c) b with half/half first step
    g = np.full((L, k), hi); g[:, 0] = lo; g[0, ::2] = lo; g[0, 0] = lo; out.append(g)
    # (d) spike-node high, all others low (max single-step leak)
    g = np.full((L, k), lo)
    for t in range(1, L + 1):
        p = node(t - 1, d)
        g[t - 1, p] = hi
    out.append(g)
    # (e) cycle low, NC high
    g = np.full((L, k), hi); g[:, :d] = lo; out.append(g)
    # (f) cycle high, NC low
    g = np.full((L, k), lo); g[:, :d] = hi; out.append(g)
    return np.stack(out)


def maximise(S, L, which, restarts=48, iters=250, seed=0):
    rng = np.random.default_rng(seed + 1000 * L)
    st = structured(S, L)
    rnd = rng.choice([G_LO, G_HI], size=(restarts, L, S['k']))
    rnd[: restarts // 3] = rng.uniform(G_LO, G_HI, size=(restarts // 3, L, S['k']))
    G0 = np.concatenate([st, rnd])
    G = torch.tensor(G0, requires_grad=True)
    step = 0.25 * (G_HI - G_LO)
    for it in range(iters):
        val = objective(S, G, which)
        gr, = torch.autograd.grad(val.sum(), G)
        with torch.no_grad():
            G += step * torch.sign(gr)
            G.clamp_(G_LO, G_HI)
        if it % 50 == 49:
            step *= 0.6
    with torch.no_grad():
        # round to vertices (objective convex per step -> vertex at least as good along coordinate lines; re-evaluate)
        Gv = torch.where(G > 0.5 * (G_HI + G_LO), torch.tensor(G_HI), torch.tensor(G_LO))
        v1 = objective(S, G, which); v2 = objective(S, Gv, which)
        best = torch.maximum(v1, v2)
        i = int(torch.argmax(best))
    return float(best[i]), int(i), float(objective(S, torch.tensor(st), which).max())


if __name__ == '__main__':
    ns = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [200, 400, 1000]
    Ls = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48]
    res = []
    for n in ns:
        S = build(n); lam = S['lam']
        for L in Ls:
            t0 = time.time()
            unit = S['a'] * S_G * S['beta0'] * lam ** (L - 1)
            N0 = sum(1 for t in range(1, L + 1) if node(t - 1, S['d']) == 0)
            tri = N0 + (S['omega_cyc'] / S_G) * (L - N0)
            triv = G_HI / S_G                         # ||r|| <= ||y|| <= beta0 lam^L
            row = dict(n=n, L=L, F_triangle=tri, F_trivial=triv, F_bound=min(tri, triv))
            for which in ('latent', 'block', 'orth'):
                best, idx, stbest = maximise(S, L, which)
                row[f'F_{which}'] = best / unit
                row[f'F_{which}_structured'] = stbest / unit
                row[f'argmax_{which}'] = idx
            row['sec'] = time.time() - t0
            res.append(row)
            print(json.dumps(row), flush=True)
        json.dump(res, open(f'remainder_adv_{"_".join(map(str, ns))}.json', 'w'), indent=1)
