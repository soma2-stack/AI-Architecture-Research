"""(1) exact cyclic basis theta_i = P_block U e_i^lat with O_A theta_i = theta_(i+1);
(2) gates in theta-basis = diagonal + rank-one (node 1) + small tilt;
(3) exact f-channel decomposition C_end = c f^T + R, R f = 0 for random histories;
(4) best FIXED one-step query capacity of the latent-cycle block (first order, exact sigma_m)."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from block import build, run_block
sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_aperiodic import G_LO, G_HI
torch.set_num_threads(8)
EPS = 1e-3
out = []
for n in (200, 400, 800):
    S = build(n); d, k, U, V, OA = S['d'], S['k'], S['U'], S['V'], S['OA']
    # (1) theta basis: block coordinates of U e_i (latent i = 0..d-1), projected (drop e1 = physical row 0)
    Theta = torch.stack([V.T @ U[:, i] for i in range(d)], 1)                     # d x d, columns theta_i
    cyc_err = float((OA @ Theta - torch.roll(Theta, -1, dims=1) @ torch.eye(d)).abs().max()) if False else \
              float(max((OA @ Theta[:, i] - Theta[:, (i + 1) % d]).abs().max() for i in range(d)))
    gram = Theta.T @ Theta; gram_ev = torch.linalg.eigvalsh(gram)
    # (2) a random admissible gate: block gate diag; in theta basis Ti = Theta^-1 G Theta
    rng = np.random.default_rng(n); gA = torch.tensor(rng.uniform(0.84, 1.0, d))
    Tg = torch.linalg.solve(Theta, gA[:, None] * Theta)
    Dg = torch.diag(torch.diagonal(Tg)); Rres = Tg - Dg
    sv = torch.linalg.svdvals(Rres)
    # (3) f-channel decomposition
    ev, evec = torch.linalg.eig(OA); f = evec[:, int(torch.argmin((ev - 1).abs()))].real; f = f / f.norm()
    Z = torch.tensor(rng.uniform(-0.3, 0.3, (6, d))); Z = Z - Z.mean(1, keepdim=True)
    C = run_block(S, Z); c = C @ f; Rm = C - torch.outer(c, f)
    # (4) fixed one-step query capacity, first order, T=6 sustained, best of several sign patterns
    T = 6; Qz = torch.linalg.svd(torch.eye(d) - torch.ones(d, d) / d)[0][:, :d - 1]
    alt = torch.tensor([1.0 if i % 2 == 0 else -1.0 for i in range(d)]); Z0 = (0.25 * alt).repeat(T, 1)
    J = torch.func.jacfwd(lambda th: run_block(S, Z0 + th.reshape(T, d - 1) @ Qz.T))(torch.zeros(T * (d - 1))).reshape(d, d, -1)
    best = (0, None)
    for trial in range(12):
        g = torch.tensor(rng.choice([G_LO, G_HI], k)) if trial else torch.full((k,), G_LO)
        zeta = S['Zq'] @ g
        Wq = torch.einsum('ijp,i->jp', J, zeta)                                  # d x p : d(C^T zeta)/dtheta
        s = torch.linalg.svdvals(Wq) * S['wRH'] * 0.11
        cnt = int((s > EPS).sum())
        if cnt > best[0]: best = (cnt, [float(x) for x in s[:6]])
    r = {'n': n, 'd': d, 'theta_cycle_err': cyc_err, 'theta_gram_eig_min_max': [float(gram_ev[0]), float(gram_ev[-1])],
         'theta_node1_norm': float(Theta[:, 0].norm()), 'gate_offdiag_in_theta_basis_sv': [float(x) for x in sv[:4]],
         'f_channel_Rf_norm': float((Rm @ f).norm()), 'f_channel_|c|': float(c.norm()), 'f_channel_|R|op': float(torch.linalg.matrix_norm(Rm, 2)),
         'fixed_query_capacity_T6_rho.11': best[0], 'fixed_query_top_sv': best[1]}
    out.append(r); print(json.dumps(r), flush=True)
json.dump(out, open('structure_checks.json', 'w'), indent=1)
