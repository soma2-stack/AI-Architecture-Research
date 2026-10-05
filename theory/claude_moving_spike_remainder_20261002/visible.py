"""Visible-frame reduction (Lemma V) and the explicit 'wake' family (Proposition W).

Lemma V: physical memory coordinate 0 is invariant under O^T and every gate, and is invisible to the query.
On its complement the adjoint is (z, zeta) in R^d x Z_NC:
    z'    = a O_A^T [ diag(g_1..g_{d-1}, gbar_N) z + e_{d-1} <delta_N, zeta>/sqrt(L) ]
    zeta' = a [ delta_N z_{d-1}/sqrt(L) + P_Z (g_N * zeta) ],     z_0 = beta0 theta_0, zeta_0 = 0.
Spike factor gamma_t = g_t[p] at a cycle node p >= 1 (physical coordinate p), mean of g over coords 1..k-1 at node 0.
"""
import json, math, sys
import numpy as np
from core import build, step_np, node, G_HI, G_LO, S_G


def visible_run(S, gates, return_parts=False):
    d, k, Lnc, a = S['d'], S['k'], S['Lnc'], S['a']
    OAT = S['OA'].T; Th = S['Theta']
    z = S['beta0'] * Th[:, 0].copy(); zeta = np.zeros(Lnc); sigma = S['beta0']
    parts = []
    for t, g in enumerate(gates, start=1):
        p = node(t - 1, d)
        gamma = float(np.mean(g[1:])) if p == 0 else float(g[p])
        gN = g[d:]; gbar = float(gN.mean()); dN = gN - gbar
        GA = np.concatenate([g[1:d], [gbar]])
        zn = GA * z; zn[d - 1] += float(dN @ zeta) / math.sqrt(Lnc)
        zeta_n = dN * z[d - 1] / math.sqrt(Lnc) + gN * zeta
        zeta_n -= zeta_n.mean()
        z = a * (OAT @ zn); zeta = a * zeta_n
        sigma *= a * gamma
        parts.append(sigma)
    p = node(len(gates), d)
    rz = z - sigma * Th[:, p]
    return z, zeta, sigma, p, rz


def latent_run(S, gates):
    y = np.zeros(S['k']); y[0] = S['beta0']
    for g in gates:
        y = step_np(S, y, g)
    m = S['U'] @ y
    return m


def wake_gates(S, L, first='hi'):
    """High window on the primary path: at step t gates g_hi on physical coords d-1..d-(t-1) (wake + primary),
    g_lo elsewhere. Step 1 (primary at node 0): all g_hi ('hi') or half/half ('half')."""
    k, d = S['k'], S['d']
    G = np.full((L, k), G_LO)
    for t in range(1, L + 1):
        if t == 1:
            G[0] = G_HI
            if first == 'half':
                G[0, 1::2] = G_LO
            continue
        for j in range(1, t):
            G[t - 1, (d - j) % d] = G_HI
    return G


if __name__ == '__main__':
    out = {}
    rng = np.random.default_rng(3)
    for n in (200, 400, 1000, 4000):
        S = build(n); d, k = S['d'], S['k']; lam = S['lam']
        rec = {}
        if n <= 1000:
            # Lemma V check: visible recursion == physical recursion restricted
            gates = rng.uniform(G_LO, G_HI, (11, k))
            z, zeta, sigma, p, rz = visible_run(S, gates)
            m = latent_run(S, gates)
            zt = S['V'].T @ m; zetat = m[d:] - m[d:].mean()
            rec['V_block_residual'] = float(np.abs(z - zt).max())
            rec['V_reservoir_residual'] = float(np.abs(zeta - zetat).max())
            # coordinate 0 decoupling: m_0 = prod(a g_0) / sqrt(n)
            rec['coord0_residual'] = float(abs(m[0] - np.prod(S['a'] * gates[:, 0]) / math.sqrt(n)))
        unit1 = S['a'] * S_G * S['beta0']
        fam = {}
        for first in ('hi', 'half'):
            rows = []
            for L in (1, 2, 4, 8, 16, 32, 48) if n <= 1000 else (1, 2, 4, 8, 16, 32, 64, 128):
                if L > d: break
                G = wake_gates(S, L, first)
                z, zeta, sigma, p, rz = visible_run(S, G)
                vis = math.sqrt(float(rz @ rz) + float(zeta @ zeta))
                F = vis / (unit1 * lam ** (L - 1))
                rows.append(dict(L=L, F_visible=F, F_block=float(np.linalg.norm(rz)) / (unit1 * lam ** (L - 1)),
                                 sigma_rel=sigma / (S['beta0'] * lam ** L),
                                 quad_pred=math.sqrt((0 if first == 'hi' else 1) + (2 * S['ck']) ** 2 * (L - 1))))
            fam[first] = rows
        rec['wake'] = fam
        rec['ck'] = S['ck']; rec['omega_hat_cyc_over_sg'] = 2 * S['ck'] * math.sqrt(1 - 2 / k)
        out[n] = rec
        print(n, json.dumps(rec), flush=True)
    json.dump(out, open('visible.json', 'w'), indent=1)
