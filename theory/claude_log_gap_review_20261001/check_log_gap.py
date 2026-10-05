"""Claude's numerical check of the arbitrary-horizon log-gap note (PROOF.md sections 3-7). Evidence, not proof.

Family: R0 = diag(a I_k, delta I_l), B = R0 + eta q q^T, R = a B/||B||op, W = I, b = 1/20, a = 1 - c/n.
(1) Lookback: two histories with identical last-H suffix; exact normalized late-query gradient (torch autograd through
    the real recurrence, inputs held fixed); half-separation vs formula and vs the bound sqrt(n)/(20c) a^(H+1); smallest H
    with separation <= eps vs the theorem's lower bound (6).
(2) Eligibility encoder: P = 2n^2+n diagonal-reference traces vs the exact history-dependent query part c_q^T Z on long
    random and adversarial histories; error vs eps and vs the bound kappa_Q e C / gamma^2; then larger couplings eta.
"""
import math, json, sys
import numpy as np, torch
torch.set_default_dtype(torch.float64)

def family(n, c, eta=None):
    a = 1 - c / n; delta = 1 / (100 * n); k = n // 2; l = n - k
    q = torch.full((n,), 1 / math.sqrt(n)); eta = 1 / (1e8 * n * n) if eta is None else eta
    R0 = torch.diag(torch.cat([torch.full((k,), a), torch.full((l,), delta)]))
    B = R0 + eta * torch.outer(q, q); R = a * B / torch.linalg.matrix_norm(B, 2)
    return dict(n=n, c=c, a=a, k=k, l=l, q=q, R0=R0, R=R, W=torch.eye(n), b=torch.full((n,), 1 / 20), eta=eta,
                e=float(torch.linalg.matrix_norm(R - R0, 2)))

def norm_grad(F, xs, vf, past_only=False):
    """Normalized late-query gradient (R,W,b blocks); optionally only the history-dependent part."""
    n = F['n']; R, W, b, q = F['R'], F['W'], F['b'], F['q']
    beta = max(1.0, float(R.norm())); wR, wW, wb = R.norm() / n, W.norm() / n, b.pow(2).mean().sqrt()
    Rp, Wp, bp = (v.clone().requires_grad_(True) for v in (R, W, b)); h = torch.zeros(n)
    for x in xs: h = torch.tanh(Rp @ h + Wp @ x + bp)
    hT = h
    def lossf(hh): return q @ torch.tanh(Rp @ hh + Wp @ vf + bp) / beta
    g = torch.autograd.grad(lossf(hT), (Rp, Wp, bp), retain_graph=True)
    full = torch.cat([(wR * g[0]).flatten(), (wW * g[1]).flatten(), wb * g[2]])
    if not past_only: return full, hT.detach()
    gd = torch.autograd.grad(lossf(hT.detach()), (Rp, Wp, bp))
    direct = torch.cat([(wR * gd[0]).flatten(), (wW * gd[1]).flatten(), wb * gd[2]])
    return full - direct, hT.detach()

def histories(F, H, s):
    n, k, l, c = F['n'], F['k'], F['l'], F['c']; J = math.ceil(n / c); sig = 0.4
    hs = [torch.zeros(n)] + [torch.cat([torch.zeros(k), torch.full((l,), s * sig)]) for _ in range(J)] + [torch.zeros(n)] * (H + 1)
    return [torch.atanh(hs[t]) - F['R'] @ hs[t - 1] - F['b'] for t in range(1, len(hs))], J

def lookback(n, c, eps=1e-3):
    F = family(n, c); a = F['a']; kappa = 1 - math.tanh(0.5) ** 2; vf = torch.full((n,), 9 / 20)
    def sep(H):
        xp, J = histories(F, H, 1); xm, _ = histories(F, H, -1)
        suffix_equal = all(torch.equal(u, v) for u, v in zip(xp[-H:], xm[-H:])) if H > 0 else True
        gp, _ = norm_grad(F, xp, vf); gm, _ = norm_grad(F, xm, vf)
        formula = kappa * 0.4 / n * math.sqrt(F['k'] / n) * math.sqrt(F['l']) * a ** (H + 1) * (1 - a ** J) / (c / n)
        return float((gp - gm).norm()) / 2, formula, suffix_equal, max(float(v.abs().max()) for v in xp + xm)
    rows = []
    for H in [0, n // 2, n, 2 * n, 4 * n]:
        m, f, se, mi = sep(H); rows.append({'H': H, 'half_sep': m, 'Rblock_formula': f, 'bound_sqrt_n_20c': math.sqrt(n) / (20 * c) * a ** (H + 1),
                                            'suffix_identical': se, 'max_abs_input': mi})
    # smallest H with separation <= eps (bisection on the exact separation, which is monotone in H)
    lo, hi = 0, 1
    while sep(hi)[0] > eps: hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if sep(mid)[0] > eps: lo = mid
        else: hi = mid
    En = 4 * 0.4 / (1e8 * c * c * math.sqrt(n))
    H_lower = math.log(math.sqrt(n) / (20 * c * (eps + En))) / (-math.log(a)) - 1
    H_win = math.ceil(math.log((a / max(1.0, float(F['R'].norm()))) * math.sqrt(a ** 2 + 0.25 + 0.0025) / (eps * c / n)) / (-math.log(a)))
    return {'n': n, 'c': c, 'rows': rows, 'H_actual_min_for_eps': hi, 'H_theorem_lower': H_lower,
            'H_window_upper': H_win, 'lead_term_(n/2c)logn': n / (2 * c) * math.log(n)}

def eligibility(n, c, etas, T=2000, seed=0):
    out = []
    rng = np.random.default_rng(seed)
    for eta in etas:
        F = family(n, c, eta); R, R0, W, b, q, a = F['R'], F['R0'], F['W'], F['b'], F['q'], F['a']
        d = torch.diag(R0); beta = max(1.0, float(R.norm())); wR, wW, wb = R.norm() / n, W.norm() / n, b.pow(2).mean().sqrt()
        C = math.sqrt(a ** 2 + 0.25 + 0.0025); kQ = a / beta; bound = kQ * F['e'] * C / (c / n) ** 2
        worst = 0.; scale = 0.
        cases = {'random': [torch.tensor(rng.uniform(-0.5, 0.5, n)) for _ in range(T)]}
        xp, _ = histories(F, 3 * n, 1); cases['coherent_tail'] = xp
        cases['alternating'] = [torch.tensor(rng.choice([-0.45, 0.45], n)) * (1 if (t // 50) % 2 else -1) for t in range(T)]
        for name, xs in cases.items():
            ER = torch.zeros(n, n); EW = torch.zeros(n, n); Eb = torch.zeros(n); h = torch.zeros(n)
            for x in xs:                                       # streaming eligibility traces (diagonal reference)
                hn = torch.tanh(R @ h + W @ x + b); g = 1 - hn ** 2
                ER = g[:, None] * (d[:, None] * ER + wR * h[None, :]); EW = g[:, None] * (d[:, None] * EW + wW * x[None, :])
                Eb = g * (d * Eb + wb); h = hn
            for vf in (torch.full((n,), 9 / 20), torch.tensor(rng.uniform(-0.5, 0.5, n))):
                past, hT = norm_grad(F, xs, vf, past_only=True)
                cq = R.T @ ((1 - torch.tanh(R @ hT + W @ vf + b) ** 2) * q) / beta
                elig = torch.cat([(cq[:, None] * ER).flatten(), (cq[:, None] * EW).flatten(), cq * Eb])
                worst = max(worst, float((past - elig).norm())); scale = max(scale, float(past.norm()))
        out.append({'n': n, 'c': c, 'eta': eta, 'opnorm_R_minus_R0': F['e'], 'max_query_error': worst, 'max_past_part_norm': scale,
                    'bound_kQ_e_C_over_gamma2': bound, 'below_eps': worst < 1e-3, 'P_coordinates': 2 * n * n + n})
    return out

if __name__ == '__main__':
    res = {'lookback': [], 'eligibility': []}
    for n, c in ((64, 1.0), (128, 1.0), (256, 1.0), (128, 2.0)):
        r = lookback(n, c); res['lookback'].append(r); print(json.dumps(r), flush=True)
    for n in (64, 128, 256):
        for r in eligibility(n, 1.0, [1 / (1e8 * n * n), 1e-5, 1e-4, 1e-3, 1e-2]):
            res['eligibility'].append(r); print(json.dumps(r), flush=True)
    json.dump(res, open('log_gap_check.json', 'w'), indent=1)
