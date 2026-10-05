"""Claude's numerical check of the near-critical linear construction (PROOF.md section 5-6). Evidence, not proof.

Builds the ACTUAL family (R = delta I + (a-delta) q q^T, W = I, b = 1/20) at width n, a random sign matrix M
(NOT the certified one), the two-step fixed-h history, and computes the late-query gradient by torch autograd through
the real recurrence with inputs held fixed. Normalizes by frozen group RMS and divides the loss by beta.
Measures the antipodal normalized-gradient distance on the boundary sphere and compares with 2*83/40000.
Also checks the lemma quantities for that M: ||M||op/sqrt(N) and min over the sphere of ||tanh(M u)||/sqrt(N).
"""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)

def run(n, a, n_u=64, seed=0):
    torch.manual_seed(seed); rng = np.random.default_rng(seed)
    N = n // 2; r = N // 1000; assert r >= 1
    q = torch.full((n,), 1 / math.sqrt(n)); delta = 1 / (100 * n)
    R = delta * torch.eye(n) + (a - delta) * torch.outer(q, q)
    W = torch.eye(n); b = torch.full((n,), 1 / 20)
    wR = R.norm() / n; wW = W.norm() / n; wb = b.pow(2).mean().sqrt(); beta = max(1.0, float(R.norm()))
    M = torch.tensor(rng.choice([-1.0, 1.0], size=(N, r)))
    Mop = float(torch.linalg.matrix_norm(M, 2)) / math.sqrt(N)
    # minimum of ||tanh(M u)||/sqrt(N) over the sphere (r small: dense grid + local refinement)
    if r == 1: us = [torch.tensor([1.0])]
    else:
        g = rng.normal(size=(20000, r)); us = [torch.tensor(v / np.linalg.norm(v)) for v in g]
    spread = min(float(torch.tanh(M @ u).norm()) / math.sqrt(N) for u in us)
    def z_of(u):
        v = torch.tanh(M @ u); z = torch.zeros(n); z[:N] = 0.4 * v; z[N:2 * N] = -0.4 * v; return z
    vf = torch.full((n,), 9 / 20)
    def grad(z):
        x1 = z - b; h1 = torch.tanh(z); x2 = -R @ h1 - b          # realized history (constants for differentiation)
        Rp = R.clone().requires_grad_(True); Wp = W.clone().requires_grad_(True); bp = b.clone().requires_grad_(True)
        h = torch.zeros(n)
        for x in (x1, x2): h = torch.tanh(Rp @ h + Wp @ x + bp)
        h2 = h.detach()
        loss = q @ torch.tanh(Rp @ h + Wp @ vf + bp) / beta     # late scalar head, future preactivation 1/2
        gR, gW, gb = torch.autograd.grad(loss, (Rp, Wp, bp))
        return h2, torch.cat([(wR * gR).flatten(), (wW * gW).flatten(), (wb * gb)]), x1, x2
    worst = math.inf; maxh2 = 0.; maxin = 0.
    sphere = [torch.tensor([1.0])] if r == 1 else [torch.tensor(v / np.linalg.norm(v)) for v in rng.normal(size=(n_u, r))]
    for u in sphere:
        h2p, gp, x1, x2 = grad(z_of(u)); h2m, gm, _, _ = grad(z_of(-u))
        maxh2 = max(maxh2, float(h2p.abs().max()), float(h2m.abs().max()))
        maxin = max(maxin, float(x1.abs().max()), float(x2.abs().max()))
        worst = min(worst, float((gp - gm).norm()) / 2)
    return {'n': n, 'a': a, 'N': N, 'r': r, 'Mop_over_sqrtN': Mop, 'min_tanh_spread_over_sqrtN': spread,
            'lemma_requires': [9, 1 / 16], 'max_abs_h2': maxh2, 'max_abs_input': maxin, 'beta': beta,
            'min_half_margin': worst, 'claimed_lower': 83 / 40000, 'ratio': worst / (83 / 40000)}

if __name__ == '__main__':
    out = []
    for n, a in ((2000, 0.5), (2000, 1 - 1 / (2 * 2000 ** 2)), (2001, 0.5), (4000, 0.5), (4000, 1 - 1 / 8000), (6000, 0.75)):
        res = run(n, a); out.append(res); print(json.dumps(res), flush=True)
    json.dump(out, open('construction_check.json', 'w'), indent=1)
