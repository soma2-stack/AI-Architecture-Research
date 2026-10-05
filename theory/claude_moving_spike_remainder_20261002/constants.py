"""Horizon-uniform remainder constants (Theorem R1 corollary) and stationary-split numbers on collision pairs."""
import json, math
import numpy as np, torch
from core import build, node, S_G, G_HI, EPS
from qbounds import remainder_budget, Bracket, Chart, CODEX
out = {}
for n in (200, 400, 1000, 4000, 10**4, 10**5, 10**6):
    S = build(n) if n <= 4000 else None
    if S is None:
        k, d = n // 2, n // 4; a = 1 - 1 / n; ck = 1 / (math.sqrt(k) - 1); lam = a * G_HI; b0 = math.sqrt(k / n)
        Sd = dict(k=k, d=d, a=a, ck=ck, lam=lam, beta0=b0)
    else:
        Sd = S
    k, d, a, ck, lam, b0 = Sd['k'], Sd['d'], Sd['a'], Sd['ck'], Sd['lam'], Sd['beta0']
    w0 = S_G * math.sqrt(1 - 1 / k); wc = 2 * ck * S_G * math.sqrt(1 - 2 / k)
    best, Lb, acc = 0, 0, 0
    for L in range(1, 4 * min(d, 2000) + 1):
        acc += w0 if node(L - 1, d) == 0 else wc
        F = min(acc / S_G, 2 * G_HI / (a * S_G))       # in units a s_g beta0 lam^(L-1)
        v = lam ** (L - 1) * F
        if v > best: best, Lb = v, L
    out[n] = dict(ck=ck, omega_c_over_sg=wc / S_G, sup_L_lamF=best, argmax_L=Lb,
                  analytic_upper=math.sqrt(1 - 1 / k) + (wc / S_G) / (math.e * math.log(1 / lam)))
    print(n, out[n])
# stationary split on the collision pairs
S = build(200); scr = np.load(CODEX + 'screen_200_200_6_sustained_spread.npz'); ch = Chart(S, scr['Q'], scr['Z'])
f = torch.tensor(S['f'])
for name in ('prev_screen_0', 'prev_random_0'):
    C = torch.tensor(np.load(f'chart_adv2_200_ub_{name}.npy'))
    with torch.no_grad():
        dC, ds = ch.diff(C)
    dc = dC @ f; dR = dC - torch.outer(dc, f)
    kap = S['a'] * S['scale'] * max(float(torch.linalg.matrix_norm(dC, 2)), abs(float(ds)))
    out['pair_' + name] = dict(dc_norm=float(dc.norm()), dR_op=float(torch.linalg.matrix_norm(dR, 2)),
                               dC_op=float(torch.linalg.matrix_norm(dC, 2)), ds=float(ds), dC_frob=float(dC.norm()),
                               kappa_2eps=kap / (2 * EPS), grok_L2_2eps=kap * G_HI * S['beta0'] / (2 * EPS))
    print(name, out['pair_' + name])
json.dump(out, open('constants.json', 'w'), indent=1)
