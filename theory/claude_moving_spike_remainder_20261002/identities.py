"""Float64 checks of the exact identities used in THEORY.md (Lemmas S1-S4)."""
import json, math
import numpy as np
from core import build, step_np, decompose_np, Mdiag, node, G_HI, G_LO, S_G

out = {}
rng = np.random.default_rng(7)
for n in (200, 400, 1000):
    S = build(n); k, d, U, w, sig = S['k'], S['d'], S['U'], S['w'], S['sig']
    r = {}
    # S1: U diag(g) U = diag(g) - sig (w v^T + v w^T),  v = (g - ghat) * w,  ghat = sum g w^2 / ||w||^2
    worst = 0.0
    for _ in range(5):
        g = rng.uniform(G_LO, G_HI, k)
        ghat = float(g @ w ** 2) / S['ww']; v = (g - ghat) * w
        M = U @ np.diag(g) @ U
        worst = max(worst, float(np.abs(M - (np.diag(g) - sig * (np.outer(w, v) + np.outer(v, w)))).max()))
    r['S1_rank2_identity_residual'] = worst
    # S2: column leaks. sup ||K e_p|| over vertices and random gates vs omega bounds
    lk0, lkc = 0.0, 0.0
    for trial in range(400):
        g = rng.choice([G_LO, G_HI], k) if trial % 2 else rng.uniform(G_LO, G_HI, k)
        M = U @ np.diag(g) @ U
        c0 = M[:, 0].copy(); c0[0] = 0; lk0 = max(lk0, float(np.linalg.norm(c0)))
        p = int(rng.integers(1, d)); cp = M[:, p].copy(); cp[p] = 0; lkc = max(lkc, float(np.linalg.norm(cp)))
    # extremal configurations
    g = np.full(k, G_LO); g[: k // 2] = G_HI
    M = U @ np.diag(g) @ U; c0 = M[:, 0].copy(); c0[0] = 0
    r['S2_leak0_halfhalf'] = float(np.linalg.norm(c0))
    g = np.full(k, G_LO); g[5] = G_HI
    M = U @ np.diag(g) @ U; cp = M[:, 5].copy(); cp[5] = 0
    r['S2_leakcyc_extremal_vertex'] = float(np.linalg.norm(cp))
    r['S2_leak0_sampled_max'] = lk0; r['S2_leakcyc_sampled_max'] = lkc
    r['S2_omega0_bound'] = S['omega_0']; r['S2_omegacyc_bound'] = S['omega_cyc']
    # S3: constant gates -> exact spike; block image theta_p
    for gam in (G_LO, G_HI):
        gates = np.full((7, k), gam)
        y, sigma, s, p = decompose_np(S, gates)
        e = np.zeros(k); e[p] = sigma
        r[f'S3_const_{gam:.3f}_spike_residual'] = float(np.abs(y - e).max())
        r[f'S3_const_{gam:.3f}_block_residual'] = float(np.abs(S['B'] @ y - sigma * S['Theta'][:, p]).max())
    # S4: Duhamel formula for the remainder r_L = sum_t sigma_{t-1} Phi(L,t) a Pi K_t e_{p_{t-1}}
    L = 9
    gates = rng.uniform(G_LO, G_HI, (L, k))
    y, sigma, s, p = decompose_np(S, gates)
    rem = y.copy(); rem[p] -= sigma
    acc = np.zeros(k); sig_t = S['beta0']
    for t in range(1, L + 1):
        g = gates[t - 1]; q = node(t - 1, d)
        M = U @ np.diag(g) @ U
        col = M[:, q].copy(); col[q] = 0
        x = S['a'] * (S['Pi'] @ col) * sig_t
        for tau in range(t + 1, L + 1):
            x = step_np(S, x, gates[tau - 1])
        acc += x
        sig_t *= S['a'] * M[q, q]
    r['S4_duhamel_residual'] = float(np.abs(acc - rem).max())
    # co-isometry of the one-step block map and Pythagoras
    A = (S['a'] / math.sqrt(n)) * (S['V'].T @ S['O'].T)
    r['coisometry_residual'] = float(np.abs(A @ A.T - (S['a'] ** 2 / n) * np.eye(d)).max())
    # stationary vector
    r['f_fixed_residual'] = float(np.abs(S['OA'] @ S['f'] - S['f']).max())
    out[n] = r
    print(n, json.dumps(r), flush=True)
json.dump(out, open('identities.json', 'w'), indent=1)
