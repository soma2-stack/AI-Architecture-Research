"""Collision onset in nested sub-charts: Codex's n = 200 sustained spread chart restricted to the first q DCT time
modes (q = 1..6; dimension q(d-1)); same exact chart map, joint rigorous UB4 objective. A certified collision
(UB4 < 2 eps) kills that sub-chart as an eps-section; failure to find one is NOT a separation certificate."""
import json, math, sys, time
import numpy as np, torch
from core import build, EPS
from qbounds import Bracket4, Chart, one_step_lower, CODEX
args = dict(a.split('=') for a in sys.argv[1:])
n = int(args.get('n', 200)); qs = [int(x) for x in args.get('qs', '1,2,3,4,5').split(',')]
nr = int(args.get('nrand', 3)); steps = int(args.get('steps', 500)); torch.set_num_threads(int(args.get('threads', 4)))
S = build(n); br = Bracket4(S)
scr = np.load(CODEX + {200: 'screen_200_200_6_sustained_spread.npz', 400: 'screen_400_400_6_sustained_spread.npz', 1000: 'screen_1000_1000_7_sustained_spread.npz'}[n])
rows = []
for q in qs:
    ch = Chart(S, scr['Q'][:, :q], scr['Z'])
    rng = np.random.default_rng(int(args.get('seed', 100)) + q)
    starts = [(f'rand_{i}', rng.normal(size=(q, S['d'] - 1))) for i in range(nr)]
    starts += [(f'screen_{i}', scr['coefficients'][i][:q]) for i in range(int(args.get('nscreen', 2)))]
    best_q = None
    for name, C0 in starts:
        t0 = time.time()
        raw = torch.tensor(C0 / np.linalg.norm(C0), requires_grad=True); best = (float('inf'), None)
        for lr, st in ((0.02, steps // 3), (0.006, steps)):
            opt = torch.optim.Adam([raw], lr=lr); sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=st, eta_min=lr / 20)
            for it in range(st + 1):
                C = raw / raw.norm(); dC, ds = ch.diff(C); val = br.ub(dC, ds); v = float(val.detach())
                if v < best[0]: best = (v, C.detach().clone())
                if it == st: break
                opt.zero_grad(); val.backward(); opt.step(); sch.step()
            with torch.no_grad(): raw.copy_(best[1])
        with torch.no_grad():
            dC, ds = ch.diff(best[1]); ub = float(br.ub(dC, ds)); lbs, Ls = br.lb_spike(dC)
        lb1, _ = one_step_lower(S, dC.numpy(), float(ds), restarts=48)
        LB = max(float(lbs), lb1)
        r = dict(n=n, q=q, dim=q * (S['d'] - 1), start=name, UB4_2eps=ub / (2 * EPS), LB_2eps=LB / (2 * EPS),
                 verdict='collision' if ub < 2 * EPS else ('separation' if LB > 2 * EPS else 'unresolved'), sec=time.time() - t0)
        rows.append(r); print(json.dumps(r), flush=True)
        np.save(f'chart_q_{n}_q{q}_s{args.get("seed", 100)}_{name}.npy', best[1].numpy())
        if r['verdict'] == 'collision': break
json.dump(rows, open(f'chart_q_{n}_{args.get("seed", 100)}.json', 'w'), indent=1)
