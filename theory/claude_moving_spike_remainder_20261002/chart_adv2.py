"""Second-phase chart adversary: small-step Adam (lr schedule) from many starts, two objectives:
 'ub'  : rigorous Theorem-Q upper bound (collision certificate if < 2 eps);
 'lbs' : smooth rigorous LOWER bound max(LB_spike, LB_rms1), LB_rms1 = scale*sqrt(E_vertex one-step distance^2)
         (an exact average over the vertex cube, so some legal vertex attains at least it) -> searches for the
         hardest-to-separate antipodes. End points are re-scored exactly (UB, LB_spike, optimised LB_one_step)."""
import json, math, sys, time
import numpy as np, torch
from core import build, EPS, G_HI, G_LO, S_G
from qbounds import Bracket, Chart, one_step_lower, CODEX

torch.set_num_threads(int(sys.argv[3]) if len(sys.argv) > 3 else 4)
MID = 0.5 * (G_HI + G_LO)


def lb_rms1(S, dC, ds):
    n, k, d, a = S['n'], S['k'], S['d'], S['a']
    W = (a / math.sqrt(n)) * dC.T @ torch.tensor(S['OA'].T @ S['V'].T)          # d x k
    mid = W.sum(dim=1) * MID
    val = mid @ mid + S_G ** 2 * (W ** 2).sum() + (ds * a / math.sqrt(n)) ** 2 * S_G ** 2 * (S['Lnc'] - 1)
    return S['scale'] * torch.sqrt(val)


def run(n, objective, steps, starts_extra, seed=1):
    S = build(n); br = Bracket(S)
    scr = np.load(CODEX + {200: 'screen_200_200_6_sustained_spread.npz', 400: 'screen_400_400_6_sustained_spread.npz',
                           1000: 'screen_1000_1000_7_sustained_spread.npz'}[n])
    ch = Chart(S, scr['Q'], scr['Z'])
    starts = []
    for fn in sorted(__import__('glob').glob(f'chart_adv_{n}_ub_*.npy')):
        starts.append(('prev_' + fn[len(f'chart_adv_{n}_ub_'):-4], np.load(fn)))
    if not starts:
        for i in range(scr['coefficients'].shape[0]):
            starts.append((f'screen_{i}', scr['coefficients'][i]))
    rng = np.random.default_rng(seed + n)
    for i in range(starts_extra):
        starts.append((f'random_{i}', rng.normal(size=scr['coefficients'].shape[1:])))
    rows = []
    for name, C0 in starts:
        t0 = time.time()
        raw = torch.tensor(np.asarray(C0, dtype=float) / np.linalg.norm(C0), requires_grad=True)
        opt = torch.optim.Adam([raw], lr=0.006)
        sched = torch.optim.lr_scheduler.StepLR(opt, step_size=max(1, steps // 3), gamma=0.4)
        best = (float('inf'), None)
        for it in range(steps + 1):
            C = raw / raw.norm()
            dC, ds = ch.diff(C)
            if objective == 'ub':
                val = br.ub(dC, ds)
            else:
                val = torch.maximum(br.lb_spike(dC)[0], lb_rms1(S, dC, ds))
            v = float(val.detach())
            if v < best[0]:
                best = (v, C.detach().clone())
            if it == steps: break
            opt.zero_grad(); val.backward(); opt.step(); sched.step()
        C = best[1]
        with torch.no_grad():
            dC, ds = ch.diff(C)
            ub, parts = br.ub(dC, ds, parts=True); lbs, Ls = br.lb_spike(dC); lr1 = float(lb_rms1(S, dC, ds))
        lb1, _ = one_step_lower(S, dC.numpy(), float(ds), restarts=48)
        LB = max(float(lbs), lb1, lr1)
        row = dict(n=n, objective=objective, start=name, steps=steps, objective_value=best[0],
                   UB=float(ub), UB_2eps=float(ub) / (2 * EPS), LB_spike=float(lbs), LB_spike_L=Ls, LB_one_step=lb1,
                   LB_rms1=lr1, LB=LB, LB_2eps=LB / (2 * EPS), L_star=parts['L_star'], spike_part=parts['spike_part'],
                   rem_part=parts['rem_part'],
                   verdict='collision' if float(ub) < 2 * EPS else ('separation' if LB > 2 * EPS else 'unresolved'),
                   sec=time.time() - t0)
        rows.append(row); print(json.dumps(row), flush=True)
        np.save(f'chart_adv2_{n}_{objective}_{name}.npy', C.numpy())
    return rows


if __name__ == '__main__':
    n = int(sys.argv[1]); obj = sys.argv[2]
    steps = {200: 400, 400: 300, 1000: 80}[n]
    rows = run(n, obj, steps, starts_extra={200: 6, 400: 3, 1000: 2}[n])
    json.dump(rows, open(f'chart_adv2_{n}_{obj}.json', 'w'), indent=1)
