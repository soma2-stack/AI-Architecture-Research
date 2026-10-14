"""End-to-end autograd check of the fixed-feature separation formula on the actual tanh
recurrence h_t = tanh(R h_(t-1) + x_t + b) with R = R0 (dense), small n.

1. Build the hub v7 histories (scaled geometry) with the matrix-free code (inputs recorded).
2. Re-run in torch with R as a leaf tensor, inputs FROZEN, one-step legal query
   (future preactivation pattern p in {.25,.75}^n), loss = q^T h_(T+1) / beta.
3. Normalized fixed-feature gradient component = w_R * <dL/dR, (E v) f_s^T>.
4. Compare the pair difference with ff_sep's formula using the same query.
"""
import math
import os
import sys
import numpy as np
import torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frozen import Frozen  # noqa: E402
import hub7  # noqa: E402

torch.set_default_dtype(torch.float64)


def histories(F, D, tc, to):
    """Return the input sequence (list of arrays) for the hub history (holes on)."""
    n, k, d = F.n, F.k, F.d
    b = F.b0 * np.ones(n)
    ts, holes0, t1, tL, T, q0, Pc, Soff = (D[x] for x in ("ts", "holes0", "t1", "tL", "T", "q0", "Pc", "Soff"))
    c, delta = 0.22, 0.22
    h = np.zeros(n)
    xs = []
    for t in range(1, T + 1):
        pre = F.R0(h) + b
        tgt = np.tanh(pre)
        drive = np.zeros(n, dtype=bool)
        if t >= ts:
            pos = holes0 + (t - ts)
            pos = pos[pos <= d - 1]
            tgt[pos] = 0.0
            drive[pos] = True
        if t1 <= t <= tL:
            j = t - t1
            if Pc > 0:
                ra = q0 + j + 2 * np.arange(Pc)
                tgt[ra] = c + delta * tc
                tgt[ra + 1] = c - delta * tc
                drive[ra] = True
                drive[ra + 1] = True
            tgt[Soff[0::2]] = c + delta * to
            tgt[Soff[1::2]] = c - delta * to
            drive[Soff] = True
        if t == T:
            if Pc > 0:
                rows = q0 + (tL - t1) + 1 + np.arange(2 * Pc)
                tgt[rows] = math.tanh(0.05)
                drive[rows] = True
            tgt[Soff] = F.b0
            drive[Soff] = True
        x = np.zeros(n)
        x[drive] = np.arctanh(tgt[drive]) - pre[drive]
        xs.append(x)
        h = np.tanh(pre + x)
    return xs, h


def torch_component(R0dense, xs, F, v, gf):
    n = F.n
    R = torch.tensor(R0dense, requires_grad=True)
    b = torch.full((n,), F.b0)
    h = torch.zeros(n)
    for x in xs:
        h = torch.tanh(R @ h + torch.as_tensor(x) + b)
    # one-step legal future: preactivation p_i = atanh-free choice: p = .25 where gf=HI, .75 where LO
    p = torch.where(torch.as_tensor(gf) > 0.9, torch.tensor(0.25), torch.tensor(0.75))
    xf = p - (R.detach() @ h.detach()) - b           # frozen future input realizing p
    h1 = torch.tanh(R @ h + xf + b)
    beta = max(1.0, float(torch.linalg.norm(R.detach())))
    L = h1.sum() / math.sqrt(n) / beta
    L.backward()
    wR = float(torch.linalg.norm(R.detach())) / n
    Ev = v.copy()
    Ev[0] = 0.0
    fs = np.zeros(n)
    fs[F.k:] = 1.0 / math.sqrt(F.l)
    return wR * float(Ev @ R.grad.numpy() @ fs)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    F = Frozen(n)
    D = hub7.design(F, W=6, p0=10, wake_skip=8)
    rng = np.random.default_rng(3)
    tc = rng.choice([-1.0, 1.0], size=D["Pc"])
    to = rng.choice([-1.0, 1.0], size=len(D["Soff"]) // 2)
    v = hub7.direction(F, D)
    # dense R0
    R0d = np.zeros((n, n))
    for j in range(n):
        e = np.zeros(n)
        e[j] = 1.0
        R0d[:, j] = F.R0(e)
    xsA, hA = histories(F, D, tc, to)
    xsB, hB = histories(F, D, -tc, -to)
    _, fA, *_ = hub7.run(F, D, tc, to, True)
    _, fB, *_ = hub7.run(F, D, -tc, -to, True)
    dB = fA - fB
    z = F.R0(dB)
    gf = np.where(z > 0, hub7.HI, hub7.LO)
    formula = F.sigma * math.sqrt(F.l) / n * (gf @ z) / math.sqrt(n)
    cA = torch_component(R0d, xsA, F, v, gf)
    cB = torch_component(R0d, xsB, F, v, gf)
    print(f"n={n} T={D['T']} Pc={D['Pc']} endpoint={np.abs(hA-hB).max():.1e} "
          f"autograd_pair_diff={cA-cB:.10f} formula={formula:.10f} rel_err={abs((cA-cB)-formula)/abs(formula):.2e}")
