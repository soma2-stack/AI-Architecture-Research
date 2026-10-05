"""Chart adversary with the NEW objective (Theorem Q upper bound) instead of the kappa operator envelope,
on Codex's sustained spread charts (T = n, q = ceil(ln n)); exact time/space bases from Codex's saved NPZ.
Objective 'ub': minimise the rigorous UB -> a value < 2 eps would CERTIFY a collision (chart not a robust section).
Objective 'lb': minimise the exact spike lower bound (search for genuinely close pairs); then evaluate UB and the
legal one-step lower at the end point. Numerical optimisation; every reported UB/LB value is an exact evaluation."""
import json, math, sys, time
import numpy as np, torch
from core import build, EPS
from qbounds import Bracket, Chart, one_step_lower, CODEX

torch.set_num_threads(int(sys.argv[3]) if len(sys.argv) > 3 else 4)


def run(n, objective, steps, lr=0.02, nrand=2, seed=0):
    S = build(n); br = Bracket(S)
    scr = np.load(CODEX + {200: 'screen_200_200_6_sustained_spread.npz', 400: 'screen_400_400_6_sustained_spread.npz',
                           1000: 'screen_1000_1000_7_sustained_spread.npz'}[n])
    Q, Z = scr['Q'], scr['Z']; ch = Chart(S, Q, Z)
    starts = []
    if n in (200, 400):
        for st in (0, 1):
            starts.append((f'codex_kappa_opt_{st}', np.load(CODEX + f'adversary_n{n}_start{st}.npz')['C']))
    for i in range(scr['coefficients'].shape[0]):
        starts.append((f'screen_{i}', scr['coefficients'][i]))
    rng = np.random.default_rng(seed + n)
    for i in range(nrand):
        starts.append((f'random_{i}', rng.normal(size=scr['coefficients'].shape[1:])))
    rows = []
    for name, C0 in starts:
        t0 = time.time()
        raw = torch.tensor(np.asarray(C0, dtype=float) / np.linalg.norm(C0), requires_grad=True)
        opt = torch.optim.Adam([raw], lr=lr)
        best = (float('inf'), None); trace = []
        for it in range(steps + 1):
            C = raw / raw.norm()
            dC, ds = ch.diff(C)
            val = br.ub(dC, ds) if objective == 'ub' else br.lb_spike(dC)[0]
            v = float(val)
            if v < best[0]:
                best = (v, C.detach().clone())
            trace.append(v)
            if it == steps: break
            opt.zero_grad(); val.backward(); opt.step()
        C = best[1]
        with torch.no_grad():
            dC, ds = ch.diff(C)
            ub, parts = br.ub(dC, ds, parts=True); lbs, Ls = br.lb_spike(dC)
        lb1, _ = one_step_lower(S, dC.numpy(), float(ds), restarts=32)
        kappa = S['a'] * S['scale'] * max(float(torch.linalg.matrix_norm(dC, 2)), abs(float(ds)))
        LB = max(float(lbs), lb1)
        row = dict(n=n, objective=objective, start=name, steps=steps, UB=float(ub), UB_2eps=float(ub) / (2 * EPS),
                   LB_spike=float(lbs), LB_spike_L=Ls, LB_one_step=lb1, LB_2eps=LB / (2 * EPS), kappa_2eps=kappa / (2 * EPS),
                   L_star=parts['L_star'], spike_part=parts['spike_part'], rem_part=parts['rem_part'],
                   start_value=trace[0], verdict='collision' if float(ub) < 2 * EPS else ('separation' if LB > 2 * EPS else 'unresolved'),
                   sec=time.time() - t0)
        rows.append(row); print(json.dumps(row), flush=True)
        np.save(f'chart_adv_{n}_{objective}_{name}.npy', C.numpy())
    return rows


if __name__ == '__main__':
    n = int(sys.argv[1]); obj = sys.argv[2]
    steps = {200: 150, 400: 150, 1000: 60}[n]
    rows = run(n, obj, steps, nrand=2 if n < 1000 else 1)
    json.dump(rows, open(f'chart_adv_{n}_{obj}.json', 'w'), indent=1)
