"""Phase-3 chart adversary: Pythagorean-refined rigorous UB objective (Theorem Q'), two-stage Adam schedule,
starts = given npy files and/or fresh random sphere points. End points re-scored exactly (UB, UB', LB_spike, LB_1step)."""
import json, math, sys, time, glob
import numpy as np, torch
from core import build, EPS
from qbounds import Bracket4 as Bracket, Chart, one_step_lower, CODEX, ub_pyth

args = dict(a.split('=') for a in sys.argv[1:])
n = int(args['n']); s1 = int(args.get('s1', 150)); s2 = int(args.get('s2', 400)); nr = int(args.get('nrand', 0))
torch.set_num_threads(int(args.get('threads', 4))); tag = args.get('tag', 'p3'); seed = int(args.get('seed', 7))
S = build(n); br = Bracket(S)
scr = np.load(CODEX + {200: 'screen_200_200_6_sustained_spread.npz', 400: 'screen_400_400_6_sustained_spread.npz',
                       1000: 'screen_1000_1000_7_sustained_spread.npz'}[n])
qmax = int(args.get('qmax', scr['Q'].shape[1]))
ch = Chart(S, scr['Q'][:, :qmax], scr['Z'])
starts = [(__import__('os').path.basename(fn)[:-4], np.load(fn)[:qmax]) for fn in args.get('files', '').split(',') if fn]
if args.get('screen'):
    for i in map(int, args['screen'].split(';')):
        starts.append((f'screen_{i}', scr['coefficients'][i]))
rng = np.random.default_rng(seed + n)
for i in range(nr):
    starts.append((f'rand{seed}_{i}', rng.normal(size=scr['coefficients'].shape[1:])))
rows = []
for name, C0 in starts:
    t0 = time.time()
    raw = torch.tensor(np.asarray(C0, float) / np.linalg.norm(C0), requires_grad=True)
    best = (float('inf'), None)
    for stage, (lr, steps) in enumerate(((0.02, s1), (0.006, s2))):
        if steps == 0: continue
        opt = torch.optim.Adam([raw], lr=lr)
        sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps, eta_min=lr / 20)
        for it in range(steps + 1):
            C = raw / raw.norm(); dC, ds = ch.diff(C)
            val = br.ub(dC, ds); v = float(val.detach())
            if v < best[0]: best = (v, C.detach().clone())
            if it == steps: break
            opt.zero_grad(); val.backward(); opt.step(); sch.step()
        with torch.no_grad():
            raw.copy_(best[1])
    C = best[1]
    with torch.no_grad():
        dC, ds = ch.diff(C); ub = float(br.ub(dC, ds)); up = float(br.ub(dC, ds)); lbs, Ls = br.lb_spike(dC)
        _, parts = br.ub(dC, ds, parts=True)
    lb1, _ = one_step_lower(S, dC.numpy(), float(ds), restarts=48)
    LB = max(float(lbs), lb1)
    row = dict(n=n, start=name, UB=ub, UB_pyth=up, UB_2eps=up / (2 * EPS), LB_spike=float(lbs), LB_spike_L=Ls,
               LB_one_step=lb1, LB=LB, LB_2eps=LB / (2 * EPS), L_star=parts['L_star'], spike_part=parts['spike_part'],
               rem_part=parts['rem_part'], op=float(torch.linalg.matrix_norm(dC, 2)), ds=float(ds),
               verdict='collision' if up < 2 * EPS else ('separation' if LB > 2 * EPS else 'unresolved'), sec=time.time() - t0)
    rows.append(row); print(json.dumps(row), flush=True)
    np.save(f'chart_{tag}_{n}_{name}.npy', C.numpy())
json.dump(rows, open(f'chart_{tag}_{n}.json', 'w'), indent=1)
