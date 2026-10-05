"""Rigorous LOWER-bound capacities with query-dependent separation, via the box sign-corner RMS
(max over permitted box queries >= RMS over sign corners), for single vs two pulses. Exact on the actual model.
half-sep(u) >= w_R ||H|| sqrt(Q(u)),  Q(u) = g_mid^2 ||T_u 1||^2 + s_g^2 ||T_u||_F^2,  T_u = d(answer)/d(future gates)."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
exec(open('explore.py').read().split("if __name__ == '__main__':")[0])
GM = (G_HI + G_LO) / 2; SGv = (G_HI - G_LO) / 2

def T_blocks(S, pulses, tau0):
    """pulses: list of (coords, gap_after_previous). Returns list of per-parameter T matrices (r x n),
    T_c = -t0 V_i^T e_c (left_c)^T / (beta sqrt n) where left_c = transport of e_c to the end, applied to the query map."""
    R, E, Gw, n = S['R'], S['E'], S['Gw'], S['n']
    Vs, Gs, B = [], [], None
    for i, (coords, gap) in enumerate(pulses):
        if i == 0:
            V = R @ S['Bpre'] + E
        else:
            for _ in range(gap): B = Gw[:, None] * (R @ B + E)
            V = R @ B + E
        G = Gw.clone(); G[coords] = 1 - tau0; B = G[:, None] * V; Vs.append(V); Gs.append(G)
    # adjoint maps: answer(g) = sum_i -t0 V_i^T D_i Z_i g, Z_last = R^T R^T / (beta sqrt n)
    Z = R.T @ R.T / (S['beta'] * math.sqrt(n)); Zs = [None] * len(pulses); Zs[-1] = Z
    for i in range(len(pulses) - 2, -1, -1):
        gap = pulses[i + 1][1]; Zi = R.T @ (Gs[i + 1][:, None] * Zs[i + 1])
        for _ in range(gap): Zi = R.T @ (Gw[:, None] * Zi)
        Zs[i] = Zi
    cols = []
    for (coords, _), V, Zi in zip(pulses, Vs, Zs):
        for c in coords: cols.append((V[c], Zi[c]))           # T_c = - t0 * outer(V[c], Zi[c])
    return cols

def rms_gram(cols, t0):
    Vm = torch.stack([v for v, _ in cols]); Zm = torch.stack([z for _, z in cols])
    GF = (Vm @ Vm.T) * (Zm @ Zm.T)                           # <outer(v_i,z_i), outer(v_j,z_j)>_F
    z1 = Zm @ torch.ones(Zm.shape[1]); G1 = (Vm @ Vm.T) * torch.outer(z1, z1)
    return t0 ** 2 * (GM ** 2 * G1 + SGv ** 2 * GF)

def counts(S, Q, scale_thr=(1.0, 1.2, 2.0)):
    ev = torch.linalg.eigvalsh(Q).clamp(min=0).flip(0); s = ev.sqrt() * S['wR'] * float(S['H'].norm())
    return {f'>{t}eps': int((s > t * EPS).sum()) for t in scale_thr}, s

if __name__ == '__main__':
    out = []
    for n in [int(v) for v in sys.argv[1].split(',')]:
        S = setup(n); k, d = S['k'], S['d']; t0 = tau0 = 0.08
        NC = list(range(d, k)); CY = list(range(1, d)); MEM = list(range(1, k))
        res = {'n': n, 'L': k - d, 'k': k, 'd': d}
        designs = {'single_NC': [(NC, 0)], 'single_MEM': [(MEM, 0)], 'single_CY': [(CY, 0)]}
        for gap in (1, d // 2, d, 2 * d):
            designs[f'two_NC_gap{gap}'] = [(NC, 0), (NC, gap)]
            designs[f'two_MEM_gap{gap}'] = [(MEM, 0), (MEM, gap)]
            designs[f'two_CY_gap{gap}'] = [(CY, 0), (CY, gap)]
        for name, pl in designs.items():
            c, s = counts(S, rms_gram(T_blocks(S, pl, tau0), t0))
            res[name] = dict(c, params=sum(len(p[0]) for p in pl), sv_quartiles=[float(s[i]) for i in (0, len(s)//4, len(s)//2, len(s)-1)])
        out.append(res); print(json.dumps(res), flush=True)
    json.dump(out, open('rms_capacity.json', 'w'), indent=1)
