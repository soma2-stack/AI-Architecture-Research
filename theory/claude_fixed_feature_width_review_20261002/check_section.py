"""Claude's numerical check of reachable_fixed_feature_width_20261002 (evidence, not proof).

For each n: build the paired stationary section on the ACTUAL dense family, then
  - verify O v_j = v_j for the paired vectors (and for random combinations), orthonormality, m vs floor(n/8);
  - realize histories x_t(u)=atanh(h_t)-R h_(t-1)-b for many u in the closed unit ball (axes, spread, random sphere,
    random interior): max |x|, forward endpoint h_T, total-input L2 radius from the centre;
  - exact selected sensitivity B_T(u) by the coupled recursion (5); affineness check;
  - EXACT minimum over the whole sphere of the fixed-query antipodal half-separation:
        min_u  w_R ||H|| t0 ||V^T D(u) R^T xi_g|| = w_R||H|| t0 sigma_min(Wmat),  Wmat=[V^T P_j y]_j
    for the section-7 query, compared with the analytic lower ell_n - zeta_n and the claim .0013;
  - worst permitted box query half-separation at sampled sphere points (vertex search).
"""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, '../claude_rotating_gate_review_20261001')
sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_rotating import family, weights
from check_aperiodic import box_max, G_LO, G_HI
torch.set_num_threads(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
SG = (G_HI - G_LO) / 2; TAU0, T0 = 0.11, 0.05

def run(n, n_samples=40, seed=0):
    F = family(n, 1.0); R, b = F['R'], F['b']; k, l, a, O, e = F['k'], F['l'], F['a'], F['O'], F['e']
    d = n // 4; assert d == F['d'], (d, F['d']); r = k - 1; m = (k - d) // 2
    wR = float(weights(F)[0]); beta = max(1.0, float(R.norm())); H = torch.full((l,), 0.4)
    # paired stationary vectors, 0-based physical memory indices
    I = [d + 2 * j - 2 for j in range(1, m + 1)]; J = [d + 2 * j - 1 for j in range(1, m + 1)]
    Vp = torch.zeros(k, m)
    for c, (i, j) in enumerate(zip(I, J)): Vp[i, c] = 1 / math.sqrt(2); Vp[j, c] = -1 / math.sqrt(2)
    rng = np.random.default_rng(seed + n); comb = Vp @ torch.tensor(rng.normal(size=m))
    res = {'n': n, 'k': k, 'l': l, 'd': d, 'm': m, 'floor_n_over_8': n // 8, 'e': e,
           'max_|Ov-v|_pairs': float((O @ Vp - Vp).abs().max()), 'max_|Oc-c|_random_combination': float((O @ comb - comb).abs().max()),
           'pairs_orthonormal_err': float((Vp.T @ Vp - torch.eye(m)).abs().max()), 'w_R_over_beta_times_n': wR / beta * n}
    N = 3 * n
    def z_of(u):
        z = torch.zeros(k); s = torch.sqrt(TAU0 + T0 * u)
        z[I] = s; z[J] = -s; return z
    def history(u):
        hs = [torch.zeros(n)] + [torch.cat([torch.zeros(k), H]) for _ in range(N + 1)] + [torch.cat([z_of(u), H]), torch.zeros(n)]
        xs = [torch.atanh(hs[t]) - R @ hs[t - 1] - b for t in range(1, len(hs))]
        return hs, xs
    # samples: axes (+-), spread corners, random sphere, random interior
    us = []
    for c in range(min(m, 6)):
        for sgn in (1.0, -1.0):
            u = torch.zeros(m); u[c] = sgn; us.append(u)
    us.append(torch.ones(m) / math.sqrt(m)); us.append(-torch.ones(m) / math.sqrt(m))
    alt = torch.tensor([(-1.0) ** c for c in range(m)]) / math.sqrt(m); us += [alt, -alt]
    for _ in range(n_samples):
        g = torch.tensor(rng.normal(size=m)); us.append(g / g.norm())
    for _ in range(10):
        g = torch.tensor(rng.normal(size=m)); us.append(g / g.norm() * float(rng.uniform()) ** (1 / m))
    hs0, xs0 = history(torch.zeros(m)); X0 = torch.stack(xs0)
    maxin, maxhT, maxrad = 0.0, 0.0, 0.0
    for u in us:
        hs, xs = history(u); X = torch.stack(xs); maxin = max(maxin, float(X.abs().max()))
        h = hs[-4]
        for x in xs[-3:]: h = torch.tanh(R @ h + x + b)
        maxhT = max(maxhT, float(h.abs().max())); maxrad = max(maxrad, float((X - X0).norm()))
    # full forward from h0 for one spread sample (endpoint exactness over the whole trajectory)
    hs, xs = history(us[2 * min(m, 6)]); h = torch.zeros(n)
    for x in xs: h = torch.tanh(R @ h + x + b)
    res.update({'samples': len(us), 'max_abs_input_over_samples': maxin, 'max_|h_T|_last3_steps': maxhT,
                'max_full_forward_|h_T|_spread_sample': float(h.abs().max()), 'max_total_input_L2_radius': maxrad})
    # exact selected sensitivity: B_t = G_t (R B_(t-1) + alpha_t E)
    E = torch.zeros(n, r); E[1:k] = torch.eye(r)
    Gw = 1 - torch.cat([torch.zeros(k), H]) ** 2; B = torch.zeros(n, r)
    for t in range(1, N + 2):
        B = Gw[:, None] * (R @ B + (0.0 if t == 1 else 1.0) * E)
    V = R @ B + E
    def BT(u):
        Gp = 1 - torch.cat([z_of(u), H]) ** 2
        return R @ (Gp[:, None] * V) + E
    u1, u2 = us[-1], us[-2]
    res['affine_midpoint_err'] = float((BT((u1 + u2) / 2) - (BT(u1) + BT(u2)) / 2).abs().max() / BT(u1).abs().max())
    # section-7 fixed query
    v = torch.full((n,), 0.2); v[J] = 0.45
    g = 1 - torch.tanh(R @ torch.zeros(n) + v + b) ** 2
    xi = R.T @ g / (beta * math.sqrt(n))
    # (B_T(u)-B_T(-u))^T xi = -2 t0 V^T D(u) R^T xi,  D(u)=sum_j u_j P_j  ->  columns V^T P_j R^T xi
    Rx = R.T @ xi; cols = []
    for c in range(m):
        mask = torch.zeros(n); mask[I[c]] = 1.0; mask[J[c]] = 1.0
        cols.append(V.T @ (mask * Rx))
    Wmat = torch.stack(cols, 1)
    smin = float(torch.linalg.svdvals(Wmat)[-1])
    exact_min_half = wR * float(H.norm()) * T0 * smin
    psi_xi = torch.tensor([float((xi[I[c]] - xi[J[c]]) / math.sqrt(2)) for c in range(m)])
    mN = (1 - a ** N) / (1 - a)
    ell = T0 * a * (a * mN + 1) * float(H.norm()) / (n * math.sqrt(n)) * (a * math.sqrt(2) * SG - e * math.sqrt(n))
    zeta = T0 * a * float(H.norm()) * e * (n + 1) ** 2 / n
    res.update({'psi_j_xi_times_beta_sqrt_n_min': float(psi_xi.min()) * beta * math.sqrt(n), 'a_sqrt2_sg': a * math.sqrt(2) * SG,
                'exact_min_fixed_query_half_separation_over_sphere': exact_min_half,
                'analytic_ell_minus_zeta': ell - zeta, 'claimed': 0.0013, 'leading_constant_claimed': 0.0013034})
    # worst permitted box query at sampled sphere points
    wb = []
    for u in us[:2 * min(m, 6) + 4] + us[2 * min(m, 6) + 4: 2 * min(m, 6) + 12]:
        if float(u.norm()) < 0.999: continue
        Du = torch.zeros(n); Du[I] = u; Du[J] = u
        Y = R @ (Du[:, None] * V)                                         # (B_T(u)-B_T(-u)) = -2 t0 Y
        wb.append(T0 * wR / beta * float(H.norm()) * box_max(Y, n, starts=12))
    res['worst_box_half_separation_sampled_min'] = min(wb); res['worst_box_half_separation_sampled_max'] = max(wb)
    return res

if __name__ == '__main__':
    out = []
    for n in [int(v) for v in sys.argv[2].split(',')] if len(sys.argv) > 2 else (200, 201, 202, 203, 256, 400):
        r = run(n); out.append(r); print(json.dumps(r), flush=True)
    json.dump(out, open('section_check.json' if len(sys.argv) <= 2 else f'section_check_{sys.argv[2].replace(",", "-")}.json', 'w'), indent=1)
