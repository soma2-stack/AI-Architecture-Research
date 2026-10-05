"""Claude's numerical check of query_visible_operator_dimension_20261002 (evidence, not proof).

  1. (6a) aggregate recurrence M_j,t = a G_t O_* M_j,t-1 + f_(t,j) G_t reproduces the directly propagated surrogate
     (arbitrary aperiodic gates, all p feature channels) and is literally the block RTRL sensitivity; counts.
  2. (15) constant-source-direction recursion reproduces the K = R_(remaining,source) block exactly.
  3. (4) box-query bounds lambda_H ||T||F <= nu_box(T) <= Lambda_H ||T||op on random / rank-one / spread T, using the
     actual permitted one-step box queries and actual dense R.
  4. (7)-(8) exact constants of the ambient-ball half-margin and the packing ratio.
  5. (9)-(10) single-packet bound vs accumulated aggregate (section 6.1) at several n.
"""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, '../claude_moment_merger_review_20261001')
sys.argv += ['4']
from check_merger import family, weights, realize, surrogate_direct, box_max, consts, G_LO, G_HI
torch.set_num_threads(4)
SG = (G_HI - G_LO) / 2

def nu_box(F, T, H):
    """exact permitted one-step box-query norm of the selected-group map K -> E T K H (worst corner by vertex search)."""
    n, k = F['n'], F['k']; lam, beta, kQ, dd = consts(F); wR = float(weights(F)[0])
    E = torch.zeros(n, k - 1); E[1:k] = torch.eye(k - 1)
    Y = F['R'] @ E @ T                                   # rows indexed by future gate i after transpose: Y^T g
    # nu = w_R ||H|| max_g ||T^T E^T R^T g|| / (beta sqrt n) = ||H||/(n sqrt n) * max_g ||Y^T g||  (w_R/beta = 1/n)
    return float(H.norm()) * wR / beta * box_max(Y, n) * math.sqrt(n) / math.sqrt(n), float(H.norm()) * wR / beta

def main():
    out = {}
    # ---- 1 & 2: exact recurrences at small n
    for n, T in ((16, 60), (24, 50)):
        F = family(n, 1.0); k, l = F['k'], F['l']; r = k - 1; p = 2 * n + 1; a = F['a']; Ob = F['O'][1:, 1:]
        wR, wW, wb = (float(v) for v in weights(F)); rng = np.random.default_rng(n)
        hs = [torch.zeros(n)] + [torch.tensor(rng.uniform(-0.3, 0.3, n)) for _ in range(T - 1)] + [torch.zeros(n)]
        xs = realize(F, hs); Zd = surrogate_direct(F, xs)
        M = torch.zeros(p, r, r); h = torch.zeros(n)
        for x in xs:
            hn = torch.tanh(F['R'] @ h + F['W'] @ x + F['b']); Gb = 1 - hn[1:k] ** 2
            f = torch.cat([wR * h, wW * x, torch.tensor([wb])])
            M = torch.einsum('ab,jbc->jac', a * Gb[:, None] * Ob, M) + f[:, None, None] * torch.diag(Gb)[None]
            h = hn
        # decode block rows: row a of Zbar wrt parameter (row b, feature j) = M_j[a,b]
        P = 2 * n * n + n; Zb = torch.zeros(r, P)
        for j in range(p):
            for b in range(r):
                col = (b + 1) * n + j if j < n else (n * n + (b + 1) * n + (j - n) if j < 2 * n else 2 * n * n + b + 1)
                Zb[:, col] = M[j][:, b]
        out[f'n{n}_6a_maxabs_vs_surrogate_block'] = float((Zb - Zd[1:k]).abs().max())
        out[f'n{n}_6a_count'] = p * r * r + (l + 1) * p
        # (15): constant source direction, arbitrary aperiodic memory gates
        Hdir = torch.tensor(rng.uniform(-1, 1, l)); Hdir = 0.4 * Hdir / Hdir.abs().max()
        hs2 = [torch.zeros(n)]
        for t in range(1, T):
            mem = torch.tensor(rng.uniform(-0.3, 0.3, k)); al = float(rng.uniform(-1, 1))
            hs2.append(torch.cat([mem, al * Hdir]))
        hs2.append(torch.zeros(n)); xs2 = realize(F, hs2); Zd2 = surrogate_direct(F, xs2)
        Mt = torch.zeros(r, r); h = torch.zeros(n)
        for x in xs2:
            hn = torch.tanh(F['R'] @ h + F['W'] @ x + F['b']); Gb = 1 - hn[1:k] ** 2
            alpha = float(h[k:] @ Hdir / (Hdir @ Hdir))
            Mt = a * Gb[:, None] * Ob @ Mt + alpha * torch.diag(Gb); h = hn
        # K block: Zbar rows 1..k-1, R columns of block rows b (1..k-1), source columns -> entry (a,(b,i)) = M[a,b]*w_R*H_i
        err = 0.0
        for b in range(r):
            cols = [(b + 1) * n + k + i for i in range(l)]
            pred = wR * Mt[:, b][:, None] * Hdir[None, :]
            err = max(err, float((Zd2[1:k][:, cols] - pred).abs().max()))
        out[f'n{n}_15_Kblock_maxabs_vs_surrogate'] = err
    # ---- 3: box-query bounds on actual permitted queries
    rows = []
    for n in (64, 128):
        F = family(n, 1.0); k, l = F['k'], F['l']; r = k - 1; lam, beta, kQ, dd = consts(F); a, e = F['a'], F['e']
        H = torch.full((l,), 0.4); lamH = SG * (a - e) * float(H.norm()) / (n * math.sqrt(n)); LamH = a * float(H.norm()) / n
        rng = np.random.default_rng(7)
        for kind in ('gaussian', 'rank_one', 'identity', 'O_power_sum'):
            if kind == 'gaussian': T = torch.tensor(rng.normal(size=(r, r)))
            elif kind == 'rank_one': T = torch.outer(torch.tensor(rng.normal(size=r)), torch.tensor(rng.normal(size=r)))
            elif kind == 'identity': T = torch.eye(r)
            else:
                Ob = F['O'][1:, 1:]; T = sum(a ** j * torch.linalg.matrix_power(Ob, j) for j in range(n))
            T = T / T.norm()                                     # Frobenius-unit
            nb, scale = nu_box(F, T, H)
            rows.append({'n': n, 'kind': kind, 'nu_box_unitF': nb, 'lambda_H': lamH, 'Lambda_H_times_op': LamH * float(torch.linalg.matrix_norm(T, 2)),
                         'ratio_nu_over_lambda': nb / lamH})
    out['box_bounds'] = rows
    # ---- 4: constants of (7)-(8)
    cons = []
    for n in (200, 1000, 10 ** 4, 10 ** 6):
        a = 1 - 1 / n; e = 4 / (1e8 * n * n); l = n - n // 2
        half = SG * (a - e) * 0.4 * math.sqrt(l / n) / 4
        cons.append({'n': n, 'half_margin_lambdaH_Renv': half, 'over_eps': half / 1e-3, 'packing_ratio_Renv_over_delta': half / 3e-3})
    out['ball_constants'] = cons; out['s_g'] = SG; out['claimed'] = 0.004851
    # ---- 5: single packet vs accumulated aggregate (section 6.1)
    acc = []
    for n in (64, 128, 200):
        F = family(n, 1.0); k, l = F['k'], F['l']; a = F['a']; Ob = F['O'][1:, 1:]; H = torch.full((l,), 0.4)
        N = math.ceil(n); M = torch.zeros(k - 1, k - 1); P_ = torch.eye(k - 1)
        for j in range(N + 1): M = M + a ** j * P_; P_ = Ob @ P_
        nb, _ = nu_box(F, M, H); single, _ = nu_box(F, torch.eye(k - 1), H)
        acc.append({'n': n, 'nu_box_aggregate': nb, 'claimed_lower_0.0058sqrt_n': 0.0058 * math.sqrt(n),
                    'nu_box_single_packet_age0': single, 'single_packet_upper_0.4_over_sqrt_n': 0.4 / math.sqrt(n)})
    out['accumulation'] = acc
    print(json.dumps(out, indent=1)); json.dump(out, open('operator_check.json', 'w'), indent=1)

if __name__ == '__main__':
    main()
