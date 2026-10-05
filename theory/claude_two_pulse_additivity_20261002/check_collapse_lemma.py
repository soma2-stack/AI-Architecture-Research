"""Exact check of the two-pulse collapse lemma in the reference model (R0, no dense perturbation):
answer(u1,u2;g) = -t0 [ (alpha m1 u1 + m2 u2) o y2 + beta(g) m1 u1 + alpha (u1.y2) Lam1 + beta(g)(sum u1) Lam1 + (u2.y2) Lam2 ]
on the stationary pulsed coordinates, for arbitrary queries g."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
exec(open('rms_capacity.py').read().rsplit("if __name__ == '__main__':", 1)[0])

def run(n, gap, trials=5):
    S = setup(n); S['R'] = S['F']['R0'].clone()                       # reference model
    # recompute warmup credit with R0
    R, E, Gw, k, d, a, r = S['R'], S['E'], S['Gw'], S['k'], S['d'], S['a'], S['r']; N = 3 * n
    B = torch.zeros(n, r)
    for t in range(1, N + 2): B = Gw[:, None] * (R @ B + (0.0 if t == 1 else 1.0) * E)
    S['Bpre'] = B; S['beta'] = max(1.0, float(S['F']['R'].norm()))
    t0 = tau0 = 0.08; L = k - d; Lp = 2 * (L // 2); NCp = list(range(d, d + Lp))
    cols = T_blocks(S, [(NCp, 0), (NCp, gap)], tau0)
    O = S['F']['O']; Os = O[1:, 1:]
    # independent ingredients (block coordinates: physical c -> block c-1)
    m1 = sum(a ** s for s in range(N + 1)); X1 = sum(a ** s * torch.linalg.matrix_power(Os, s) for s in range(N + 1))
    c0 = d - 1                                                          # block index of first stationary coordinate
    Lam1 = X1.T[:, c0] - m1 * torch.eye(r)[:, c0]
    G1 = torch.ones(r); G1[[c - 1 for c in NCp]] = 1 - tau0; G2 = G1.clone()
    Sg = sum(a ** s * torch.linalg.matrix_power(Os, s) for s in range(gap + 1))
    X2 = torch.linalg.matrix_power(a * Os, gap + 1) @ (G1[:, None] * X1) + Sg
    m2 = a ** (gap + 1) * (1 - tau0) * m1 + sum(a ** s for s in range(gap + 1)); Lam2 = X2.T[:, c0] - m2 * torch.eye(r)[:, c0]
    lam = torch.linalg.matrix_power(Os, gap + 1)[:, c0] - torch.eye(r)[:, c0]
    alpha = a ** (gap + 1) * (1 - tau0)
    # check common-structure claims
    struct = max(float((X1.T[:, c - 1] - m1 * torch.eye(r)[:, c - 1] - Lam1).abs().max()) for c in NCp)
    struct2 = max(float((X2.T[:, c - 1] - m2 * torch.eye(r)[:, c - 1] - Lam2).abs().max()) for c in NCp)
    rng = np.random.default_rng(n + gap); worst = 0.0
    for _ in range(trials):
        g = torch.tensor(rng.uniform(G_LO, G_HI, n)); u1 = torch.tensor(rng.normal(size=Lp)); u2 = torch.tensor(rng.normal(size=Lp))
        ans = -sum(uu * V * float(Z @ g) for uu, (V, Z) in zip(torch.cat([u1, u2]), cols))     # model answer (linear part)
        xi = R.T @ g / (S['beta'] * math.sqrt(n)); eta = xi[1:k]; y2 = a * Os.T @ eta
        beta_g = float(a ** (gap + 1) * lam @ (G2 * y2))
        idx = [c - 1 for c in NCp]
        U1 = torch.zeros(r); U1[idx] = u1; U2 = torch.zeros(r); U2[idx] = u2
        form = -( (alpha * m1 * U1 + m2 * U2) * y2 + beta_g * m1 * U1 + alpha * float(U1 @ y2) * Lam1 + beta_g * float(u1.sum()) * Lam1 + float(U2 @ y2) * Lam2 )
        worst = max(worst, float((ans - form).abs().max() / ans.abs().max()))
    return {'n': n, 'gap': gap, 'X1_common_structure_err': struct, 'X2_common_structure_err': struct2, 'lemma_rel_err': worst,
            'm1': m1, 'm2': m2, '||Lam1||': float(Lam1.norm()), '||Lam2||': float(Lam2.norm()), '||lam||': float(lam.norm()), 'alpha': alpha}

if __name__ == '__main__':
    out = []
    for n, gap in ((64, 1), (64, 7), (128, 1), (128, 16), (200, 25)):
        rr = run(n, gap); out.append(rr); print(json.dumps(rr), flush=True)
    json.dump(out, open('collapse_lemma_check.json', 'w'), indent=1)
