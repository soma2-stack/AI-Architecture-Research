"""Claude's numerical check of the gamma=c/n quadratic construction (PROOF.md sections 2-7). Evidence, not proof.

Builds the actual block reference R0 = diag(a O, delta I), W = I, b = 1/20, the prescribed trajectory with exact fixed-h
inputs (4), and computes the late-query gradient by torch autograd through the real recurrence with REALIZED inputs held
fixed, normalised by frozen group RMS, loss divided by beta. Then repeats with dense couplings: R = a B/||B||op,
B = R0 + e*G (G random dense, ||G||op = 1), for e = 0 (reference), 1e-8/n^2 (proof scale), 1e-3, 1e-2, 5e-2.
Uses a random sign matrix M (not the certified one) and samples the boundary sphere.
"""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)

def build(n, c):
    a = 1 - c / n; delta = 1 / (100 * n); k = n // 2; l = n - k
    L = max(1, math.ceil(c)); d = min(k, math.floor(n / (4 * c * L))); J = L * d
    e = torch.full((k,), 1 / math.sqrt(k)); e1 = torch.zeros(k); e1[0] = 1; w = e1 - e
    U = torch.eye(k) - 2 * torch.outer(w, w) / (w @ w)
    Pd = torch.zeros(d, d)
    for i in range(d): Pd[(i + 1) % d, i] = 1
    PdI = torch.eye(k); PdI[:d, :d] = Pd
    O = U @ PdI @ U.T
    R0 = torch.zeros(n, n); R0[:k, :k] = a * O; R0[k:, k:] = delta * torch.eye(l)
    return dict(n=n, c=c, a=a, delta=delta, k=k, l=l, L=L, d=d, J=J, O=O, R0=R0)

def margins(n, c, eps_list, n_u=48, seed=0):
    p = build(n, c); n_, k, l, d, J, a = p['n'], p['k'], p['l'], p['d'], p['J'], p['a']
    rng = np.random.default_rng(seed); N = d * l; r = N // 1000
    M = torch.tensor(rng.choice([-1.0, 1.0], size=(N, r)))
    q = torch.full((n,), 1 / math.sqrt(n)); W = torch.eye(n); b = torch.full((n,), 1 / 20); vf = torch.full((n,), 9 / 20)
    G = torch.tensor(rng.normal(size=(n, n))); G /= torch.linalg.matrix_norm(G, 2)
    us = [torch.tensor(v / np.linalg.norm(v)) for v in rng.normal(size=(n_u, r))]
    # orthogonality / orbit checks
    qm = q[:k]; vecs = torch.stack([torch.linalg.matrix_power(p['O'].T, j) @ qm for j in range(1, d + 1)])
    gram = vecs @ vecs.T
    out = {'n': n, 'c': c, 'a': a, 'k': k, 'l': l, 'L': p['L'], 'd': d, 'J': J, 'T': J + 1, 'N': N, 'r': r,
           'orbit_gram_offdiag_max': float((gram - torch.diag(torch.diag(gram))).abs().max()),
           'orbit_norm_sq_vs_k_over_n': [float(gram.diag().min()), k / n],
           'orbit_returns': float((torch.linalg.matrix_power(p['O'].T, d) @ qm - qm).abs().max()), 'runs': []}
    for eps in eps_list:
        B = p['R0'] + eps * G; R = a * B / torch.linalg.matrix_norm(B, 2)
        opn = float(torch.linalg.matrix_norm(R, 2)); fro = float(R.norm()); beta = max(1.0, fro)
        wR, wW, wb = R.norm() / n, W.norm() / n, b.pow(2).mean().sqrt()
        zero_frac = float((R == 0).double().mean())
        worst = math.inf; worst_ref_bound = math.inf; maxin = 0.; maxhT = 0.; maxmem = 0.
        for u in us:
            gs = []
            for sgn in (1, -1):
                H = (0.4 * torch.tanh(M @ (sgn * u))).reshape(d, l)
                hs = [torch.zeros(n)]
                for t in range(1, J + 1):
                    h = torch.zeros(n); h[k:] = H[(t - 1) % d]; hs.append(h)
                hs.append(torch.zeros(n))                                     # h_T = 0, T = J+1
                xs = [torch.atanh(hs[t]) - R @ hs[t - 1] - b for t in range(1, J + 2)]   # exact realized inputs (4)
                Rp = R.clone().requires_grad_(True); Wp = W.clone().requires_grad_(True); bp = b.clone().requires_grad_(True)
                h = torch.zeros(n); mem = 0.
                for x in xs:
                    h = torch.tanh(Rp @ h + Wp @ x + bp); mem = max(mem, float(h[:k].abs().max()))
                maxhT = max(maxhT, float(h.abs().max())); maxmem = max(maxmem, mem)
                maxin = max(maxin, max(float(x.abs().max()) for x in xs))
                loss = q @ torch.tanh(Rp @ h + Wp @ vf + bp) / beta
                gR, gW, gb = torch.autograd.grad(loss, (Rp, Wp, bp))
                gs.append(torch.cat([(wR * gR).flatten(), (wW * gW).flatten(), wb * gb]))
                if sgn == 1: Hf = float(H.norm()) / math.sqrt(d * l)
            worst = min(worst, float((gs[0] - gs[1]).norm()) / 2)
            worst_ref_bound = min(worst_ref_bound, Hf)
        out['runs'].append({'perturbation_e': eps, 'R_opnorm': opn, 'a': a, 'R_frob': fro, 'wR_over_beta_times_n': float(wR / beta * n),
                            'fraction_zero_entries_R': zero_frac, 'max_abs_hT': maxhT, 'max_abs_memory_state': maxmem,
                            'max_abs_input': maxin, 'min_HF_over_sqrt_dl': worst_ref_bound, 'min_half_margin': worst})
    return out

if __name__ == '__main__':
    res = []
    for n, c in ((256, 1.0), (256, 0.5), (512, 1.0), (512, 2.5), (1024, 1.0)):
        out = margins(n, c, [0.0, 1e-8 / n ** 2, 1e-3, 1e-2, 5e-2], n_u=24 if n >= 1024 else 48)
        res.append(out)
        print(json.dumps({k: v for k, v in out.items() if k != 'runs'}), flush=True)
        for rr in out['runs']:
            print('   ', json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in rr.items()}), flush=True)
    json.dump(res, open('quadratic_check.json', 'w'), indent=1)
