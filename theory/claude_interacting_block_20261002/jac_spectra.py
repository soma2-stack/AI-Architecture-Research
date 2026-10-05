"""First-order structure of the interacting block for short co-rotating windows.
Exact Jacobian (autograd) of C_end w.r.t. all zero-sum latent profile perturbations theta (T*(d-1) params) at a
sustained alternating baseline (B=.25) or a weak baseline. Reports, per unit latent l2 amplitude:
  sF  : Frobenius singular values  -> per-direction UPPER envelope  nu <= wRH * Gmax * sF   (Gmax = sup_g ||Zq g||)
  sR  : RMS-box singular values    -> per-direction LOWER bound     nu >= wRH * sR        (sign-corner average)
and counts of directions above epsilon at latent radius rho."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from block import build, run_block
sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_aperiodic import G_LO, G_HI, box_max
GM = (G_HI + G_LO) / 2; SG = (G_HI - G_LO) / 2; EPS = 1e-3
torch.set_num_threads(8)

def analyze(n, T, baseline='sustained', B=0.25):
    S = build(n); d, k = S['d'], S['k']
    Qz = torch.linalg.svd(torch.eye(d) - torch.ones(d, d) / d)[0][:, :d - 1]        # zero-sum basis
    alt = torch.tensor([1.0 if i % 2 == 0 else -1.0 for i in range(d)])
    z0 = (B * alt) if baseline == 'sustained' else (B / math.sqrt(T) * alt)
    Z0 = z0.repeat(T, 1)
    def f(theta):
        Z = Z0 + (theta.reshape(T, d - 1) @ Qz.T)
        return run_block(S, Z)
    th0 = torch.zeros(T * (d - 1))
    J = torch.func.jacfwd(f)(th0).reshape(d * d, -1)                                 # vec(C_end) jacobian
    sF = torch.linalg.svdvals(J)
    Zq = S['Zq']; Gmax = math.sqrt(k) * box_max(Zq.T, k, starts=6)                    # sup_g ||Zq g||, g in box
    # RMS-box quadratic form: E||dC^T Zq g||^2 = gm^2 ||dC^T Zq 1||^2 + sg^2 ||dC^T Zq||_F^2
    Jm = J.T.reshape(-1, d, d)                                                          # p x d x d  (dC per param)
    A1 = torch.einsum('pij,ik->pjk', Jm, Zq).reshape(Jm.shape[0], -1)                  # vec(dC^T Zq)  (p x d*k)
    A0 = torch.einsum('pij,i->pj', Jm, Zq @ torch.ones(k))                               # dC^T Zq 1     (p x d)
    Q = GM ** 2 * A0 @ A0.T + SG ** 2 * A1 @ A1.T
    sR = torch.linalg.eigvalsh(Q).clamp(min=0).flip(0).sqrt()
    wRH = S['wRH']
    out = {'n': n, 'T': T, 'baseline': baseline, 'd': d, 'params': T * (d - 1), 'Gmax': Gmax}
    for rho in (0.11, 0.05):
        up = wRH * Gmax * sF * rho; lo = wRH * sR * rho
        out[f'rho{rho}_count_upper>eps'] = int((up > EPS).sum()); out[f'rho{rho}_count_lower>eps'] = int((lo > EPS).sum())
    out['sF_top'] = [float(x) for x in sF[:3]]
    out['sF_at'] = {str(i): float(sF[i]) for i in (d // 2, d - 1, d, 2 * d - 1, 2 * d, 3 * d) if i < len(sF)}
    out['sR_at'] = {str(i): float(sR[i]) for i in (0, d // 2, d - 1, d, 2 * d, 3 * d) if i < len(sR)}
    rel = sF / sF[0]
    out['sF_count_rel>1e-1'] = int((rel > 1e-1).sum()); out['sF_count_rel>1e-2'] = int((rel > 1e-2).sum()); out['sF_count_rel>1e-3'] = int((rel > 1e-3).sum())
    return out

if __name__ == '__main__':
    res = []
    for n in [int(x) for x in sys.argv[1].split(',')]:
        for T in [int(x) for x in sys.argv[2].split(',')]:
            for bl in sys.argv[3].split(','):
                r = analyze(n, T, bl); res.append(r); print(json.dumps(r), flush=True)
    json.dump(res, open(f'jac_spectra_{sys.argv[1].replace(",", "-")}.json', 'w'), indent=1)
