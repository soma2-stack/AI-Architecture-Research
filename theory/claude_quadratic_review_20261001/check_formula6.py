"""Check formula (6): autograd R memory-row/source-column normalized gradient block vs the closed form."""
import math, numpy as np, torch, json
torch.set_default_dtype(torch.float64)
from check_quadratic import build
out = []
for n, c in ((256, 1.0), (256, 2.5), (512, 0.5)):
    p = build(n, c); k, l, d, J, a, O, R = p['k'], p['l'], p['d'], p['J'], p['a'], p['O'], p['R0']
    rng = np.random.default_rng(3); H = torch.tensor(0.4 * np.tanh(rng.normal(size=(d, l))))
    q = torch.full((n,), 1 / math.sqrt(n)); W = torch.eye(n); b = torch.full((n,), 1 / 20); vf = torch.full((n,), 9 / 20)
    hs = [torch.zeros(n)] + [torch.cat([torch.zeros(k), H[(t - 1) % d]]) for t in range(1, J + 1)] + [torch.zeros(n)]
    xs = [torch.atanh(hs[t]) - R @ hs[t - 1] - b for t in range(1, J + 2)]
    Rp = R.clone().requires_grad_(True); h = torch.zeros(n)
    for x in xs: h = torch.tanh(Rp @ h + W @ x + b)
    beta = float(R.norm()); loss = q @ torch.tanh(Rp @ h + W @ vf + b) / beta
    gR = torch.autograd.grad(loss, Rp)[0] * (R.norm() / n)
    kappa = 1 - math.tanh(0.5) ** 2; BL = sum(a ** (j * d) for j in range(p['L'])); qm = q[:k]
    closed = sum(a ** (d + 1 - s) * torch.outer(torch.linalg.matrix_power(O.T, d + 1 - s) @ qm, H[s - 1]) for s in range(1, d + 1)) * kappa / n * BL
    blk = gR[:k, k:]
    out.append({'n': n, 'c': c, 'max_abs_diff': float((blk - closed).abs().max()), 'block_norm': float(blk.norm()),
                'rel': float((blk - closed).norm() / blk.norm())})
    print(out[-1], flush=True)
json.dump(out, open('formula6_check.json', 'w'), indent=1)
