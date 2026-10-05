"""Rigorous upper bound on the EXACT one-step query distance by an SDP dual certificate (Theorem Q1').
f(g) = ||dC^T O_A^T V^T g||^2 + ds^2 ||delta_N(g)||^2 is a convex quadratic; over g = mid + s_g eps, eps in [-1,1]^k
its max is at a vertex. Homogenise with eps_0 = +-1:  f = e~^T Qt e~,  max over e~ in {+-1}^(k+1) <= min sum(mu) s.t.
diag(mu) - Qt PSD. A primal Burer-Monteiro solution gives mu_i = (Qt X)_ii; feasibility is restored by adding the
(negative part of the) smallest eigenvalue, so sum(mu) is a valid upper bound (float64 eigvalsh)."""
import math
import numpy as np
from core import G_HI, G_LO, S_G

MID = 0.5 * (G_HI + G_LO)


def one_step_Q(S, dC, ds):
    k, d, n, a = S['k'], S['d'], S['n'], S['a']
    W = dC.T @ S['OA'].T @ S['V'].T                      # d x k
    Q = W.T @ W
    PZ = np.zeros((k, k)); L = S['Lnc']
    PZ[d:, d:] = np.eye(L) - np.ones((L, L)) / L
    Q = Q + ds ** 2 * PZ
    m = np.full(k, MID)
    Qt = np.zeros((k + 1, k + 1))
    Qt[0, 0] = m @ Q @ m
    Qt[0, 1:] = Qt[1:, 0] = S_G * (Q @ m)
    Qt[1:, 1:] = S_G ** 2 * Q
    return Qt


def sdp_upper(Qt, rank=24, iters=600, seed=0):
    N = Qt.shape[0]
    rng = np.random.default_rng(seed)
    Y = rng.normal(size=(N, rank)); Y /= np.linalg.norm(Y, axis=1, keepdims=True)
    step = 1.0 / (np.abs(np.linalg.eigvalsh(Qt)).max() + 1e-30)
    for it in range(iters):
        G = Qt @ Y
        Y = Y + step * G
        Y /= np.linalg.norm(Y, axis=1, keepdims=True)
    X = Y @ Y.T
    primal = float(np.sum(Qt * X))
    mu = np.einsum('ij,ji->i', Qt, X)                     # (Qt X)_ii
    lmin = float(np.linalg.eigvalsh(np.diag(mu) - Qt)[0])
    if lmin < 0:
        mu = mu - lmin * (1 + 1e-9) - 1e-15
    lmin2 = float(np.linalg.eigvalsh(np.diag(mu) - Qt)[0])
    return float(mu.sum()), primal, lmin2


def one_step_upper(S, dC, ds):
    Qt = one_step_Q(S, np.asarray(dC), float(ds))
    best = None
    for seed in range(3):
        ub, primal, chk = sdp_upper(Qt, seed=seed)
        if chk >= -1e-12 and (best is None or ub < best[0]):
            best = (ub, primal, chk)
    return S['scale'] * (S['a'] / math.sqrt(S['n'])) * math.sqrt(best[0]), best


if __name__ == '__main__':
    import torch, json
    from core import build
    from qbounds import Bracket4, Chart, CODEX, one_step_lower, load_codex_pair
    out = []
    for n, files in ((200, ['chart_adv2_200_ub_prev_screen_0.npy']), (400, ['chart_adv2_400_ub_random_2.npy', 'chart_adv2_400_ub_random_1.npy'])):
        S = build(n); scr = np.load(CODEX + {200: 'screen_200_200_6_sustained_spread.npz', 400: 'screen_400_400_6_sustained_spread.npz'}[n])
        ch = Chart(S, scr['Q'], scr['Z'])
        for fn in files:
            with torch.no_grad():
                dC, ds = ch.diff(torch.tensor(np.load(fn)))
            up, info = one_step_upper(S, dC.numpy(), float(ds))
            lo, _ = one_step_lower(S, dC.numpy(), float(ds), restarts=128)
            r = dict(n=n, file=fn, one_step_lower=lo, one_step_sdp_upper=up, ratio=up / lo, dual_check=info[2])
            out.append(r); print(json.dumps(r), flush=True)
