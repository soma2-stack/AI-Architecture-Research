"""Theorem Q bracket on the four saved Codex antipodes (already legally separated per Grok): how much of the
upper bound is the remainder, how close the legal one-step query gets to the L=1 remainder budget,
and what the stationary-channel split gives."""
import json, math
import numpy as np, torch
from core import build, S_G, EPS
from qbounds import Bracket, Chart, load_codex_pair, one_step_lower

torch.set_num_threads(4)
out = []
for n, start in ((200, 0), (200, 1), (400, 0), (400, 1)):
    S = build(n); C, Q, Z = load_codex_pair(n, start)
    ch = Chart(S, Q, Z); br = Bracket(S)
    with torch.no_grad():
        dC, ds = ch.diff(torch.tensor(C))
        ub, parts = br.ub(dC, ds, parts=True)
        lbs, Ls = br.lb_spike(dC)
    lb1, g1 = one_step_lower(S, dC.numpy(), float(ds))
    op = float(torch.linalg.matrix_norm(dC, 2)); fro = float(dC.norm())
    kappa = S['a'] * S['scale'] * max(op, abs(float(ds)))
    rem1 = S['scale'] * S['a'] * S['beta0'] * S_G * math.sqrt(1 - 1 / S['k']) * max(op, abs(float(ds)))
    # stationary split
    f = torch.tensor(S['f']); dc = dC @ f; dR = dC - torch.outer(dc, f)
    row = dict(n=n, start=start, kappa=kappa, UB=float(ub), UB_over_2eps=float(ub) / (2 * EPS), **parts,
               LB_spike=float(lbs), LB_spike_L=Ls, LB_one_step=lb1, LB=max(float(lbs), lb1),
               LB_over_2eps=max(float(lbs), lb1) / (2 * EPS),
               remainder_L1=rem1, one_step_over_rem_L1=lb1 / rem1,
               op=op, frob=fro, dc_norm=float(dc.norm()), dR_op=float(torch.linalg.matrix_norm(dR, 2)),
               ds=float(ds), verdict=('collision' if float(ub) < 2 * EPS else 'separation' if max(float(lbs), lb1) > 2 * EPS else 'unresolved'))
    out.append(row); print(json.dumps(row), flush=True)
json.dump(out, open('pairs_bracket.json', 'w'), indent=1)
