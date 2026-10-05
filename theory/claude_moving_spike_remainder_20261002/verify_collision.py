"""Cross-checks for the certified-collision antipodes found by chart_adv2 (n = 200).

1. Endpoint difference dC, ds from THREE implementations: mine (Chart, reduced block, torch), Grok's
   endpoint_from_coeffs (numpy, eigen geometric sum), and Codex's independent.py Family/profiles/Difference
   (FULL k x r reference credit, physical states, its own warm sum). Codex/Grok code is imported read-only.
2. Past-input admissibility with Codex's history_check on the ACTUAL dense R (inputs must lie in (-1/2,1/2)^n).
3. Attack: maximise the exact legal distance over (a) all constant-gate spikes, (b) one-step vertices,
   (c) L-step projected sign-gradient ascent on gates, L = 1..24, many starts, (d) wake/structured gates.
   Every value must stay <= UB (consistency); the max is the best legal lower bound.
4. UB recomputed in plain numpy (independent of the torch Bracket).
"""
import json, math, os, sys
import numpy as np, torch
from core import build, node, G_HI, G_LO, S_G, EPS
from qbounds import Bracket, Bracket4, Chart, CODEX, remainder_budget, one_step_lower
from sdp1 import one_step_upper

torch.set_num_threads(4)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'codex_two_pulse_corotating_20261002'))
sys.path.insert(0, os.path.join(HERE, '..', 'grok_permitted_query_reach_20261002'))
import independent as cx          # Codex (read-only)
import study as gk                # Grok (read-only)


def ub_numpy(S, dC, ds):
    R = remainder_budget(S, 4 * S['d'])
    rows = np.linalg.norm(dC.T @ S['Theta'], axis=0)
    M = max(np.linalg.norm(dC, 2), abs(ds))
    best = 0.0
    for L in range(1, 4 * S['d'] + 1):
        best = max(best, S['beta0'] * S['lam'] ** L * rows[node(L, S['d'])] + R[L] * M)
    Lt = 4 * S['d'] + 1
    acc = sum((S_G * math.sqrt(1 - 1 / S['k']) if node(t - 1, S['d']) == 0 else 2 * S['ck'] * S_G * math.sqrt(1 - 2 / S['k']))
              for t in range(1, Lt + 1))
    tail = S['beta0'] * S['lam'] ** Lt * rows.max() + min(S['a'] * S['beta0'] * S['lam'] ** (Lt - 1) * acc, 2 * S['beta0'] * S['lam'] ** Lt) * M
    return S['scale'] * max(best, tail)


def distance_from_gates(S, dC, ds, G):
    """exact legal distance for gate sequence G (L, k) (torch, differentiable). G[0] nearest the loss."""
    T = S['t']; U, Pi, a = T['U'], T['Pi'], S['a']
    y = torch.zeros(S['k']); y[0] = S['beta0']
    for g in G:
        y = a * (((g * (U @ y)) @ U) @ Pi.T)
    m = U @ y
    z = torch.tensor(S['V']).T @ m
    nc = m[S['d']:]; zeta = nc - nc.mean()
    return S['scale'] * torch.sqrt(((dC.T @ z) ** 2).sum() + (ds ** 2) * (zeta ** 2).sum())


def attack(S, dC, ds, seed=0):
    dCt, dst = torch.tensor(dC), torch.tensor(ds)
    best = (0.0, None)
    rng = np.random.default_rng(seed)
    for L in list(range(1, 13)) + [16, 20, 24]:
        starts = [np.full((L, S['k']), G_HI)]
        for j in range(10):
            starts.append(rng.choice([G_LO, G_HI], size=(L, S['k'])))
        for G0 in starts:
            G = torch.tensor(G0, requires_grad=True)
            step = 0.25 * (G_HI - G_LO)
            for it in range(120):
                v = distance_from_gates(S, dCt, dst, G)
                if float(v) > best[0]:
                    best = (float(v), L)
                gr, = torch.autograd.grad(v, G)
                with torch.no_grad():
                    G += step * torch.sign(gr); G.clamp_(G_LO, G_HI)
                if it % 40 == 39: step *= 0.5
            with torch.no_grad():
                Gv = torch.where(G > 0.5 * (G_HI + G_LO), torch.tensor(G_HI), torch.tensor(G_LO))
                v = float(distance_from_gates(S, dCt, dst, Gv))
                if v > best[0]: best = (v, L)
    return best


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1].isdigit():
        n = int(sys.argv[1]); files = sys.argv[2:]
    else:
        n = 200; files = [f'chart_adv2_200_ub_{nm}.npy' for nm in (sys.argv[1:] or ['prev_screen_0', 'prev_random_0', 'random_5', 'prev_screen_3'])]
    S = build(n); br = Bracket(S); br4 = Bracket4(S)
    scr = np.load(CODEX + {200: 'screen_200_200_6_sustained_spread.npz', 400: 'screen_400_400_6_sustained_spread.npz', 1000: 'screen_1000_1000_7_sustained_spread.npz'}[n]); Q, Z = scr['Q'], scr['Z']
    ch = Chart(S, Q, Z)
    old = os.getcwd(); os.chdir(os.path.join(HERE, '..', 'codex_two_pulse_corotating_20261002'))
    f = cx.Family(n)
    os.chdir(old)
    Sg = gk.build(n)
    out = []
    for name in files:
        C = np.load(name)
        rec = dict(name=name, coeff_norm=float(np.linalg.norm(C)))
        # (1a) mine
        with torch.no_grad():
            dC, ds = ch.diff(torch.tensor(C)); dC = dC.numpy(); ds = float(ds)
        # (1b) Grok
        Cp, sp, _ = gk.endpoint_from_coeffs(Sg, C, Q, Z); Cm, sm, _ = gk.endpoint_from_coeffs(Sg, -C, Q, Z)
        rec['grok_dC_maxdiff'] = float(np.abs((Cp - Cm) - dC).max()); rec['grok_ds_diff'] = float(abs((sp - sm) - ds))
        # (1c) Codex full reference credit
        plus, _ = cx.profiles(f, Q, Z, C, 'sustained', 'spread'); minus, _ = cx.profiles(f, Q, Z, -C, 'sustained', 'spread')
        D = cx.Difference(f, plus, minus)
        V = S['V']; Vx = V[1:, :]                       # V restricted to coords 1..k-1 (parameter space index)
        Mt_V = np.column_stack([D.rmatvec(V[:, i]) for i in range(S['d'])])   # r x d : M^T b_i
        dC_codex_T = Vx.T @ Mt_V                         # = dC^T  (d x d)
        rec['codex_dC_maxdiff'] = float(np.abs(dC_codex_T.T - dC).max())
        u = np.zeros(S['k']); u[S['d']] = 1; u[S['d'] + 1] = -1; u /= math.sqrt(2)
        Mu = D.rmatvec(u)
        rec['codex_ds_diff'] = float(abs(Mu[S['d'] - 1] / u[S['d']] - ds))
        rec['codex_offblock_leak'] = float(np.linalg.norm(Mt_V - Vx @ dC_codex_T))
        rec['dC_scale_max_abs'] = float(np.abs(dC).max())
        # (2) admissibility of both antipodal histories on the ACTUAL dense R
        for sgn, prof in (('plus', plus), ('minus', minus)):
            mx, endh, _ = f.history_check(prof)
            rec[f'max_input_{sgn}'] = mx; rec[f'endpoint_max_{sgn}'] = endh
        # (3) bracket and attack
        UB = float(br.ub(torch.tensor(dC), ds)); UBn = ub_numpy(S, dC, ds); UB4 = float(br4.ub(torch.tensor(dC), ds)); sdpU1, _ = one_step_upper(S, dC, ds)
        lbs, Ls = br.lb_spike(torch.tensor(dC))
        lb1, _ = one_step_lower(S, dC, ds, restarts=128)
        att, attL = attack(S, dC, ds)
        rec.update(UB=UB, UB_numpy=UBn, UB_2eps=UB / (2 * EPS), UB4=UB4, UB4_2eps=UB4 / (2 * EPS), one_step_sdp_upper=sdpU1, LB_spike=float(lbs), LB_spike_L=Ls, LB_one_step=lb1,
                   attack_best=att, attack_L=attL, LB=max(float(lbs), lb1, att),
                   dense_transfer_2eta=2 * f.eta, UB_actual=UB + 2 * f.eta,
                   kappa=S['a'] * S['scale'] * max(np.linalg.norm(dC, 2), abs(ds)),
                   consistent=bool(max(float(lbs), lb1, att) <= UB + 1e-12),
                   certified_collision_R1=bool(UB + 2 * f.eta < 2 * EPS), certified_collision_R4=bool(UB4 + 2 * f.eta < 2 * EPS), consistent4=bool(max(float(lbs), lb1, att) <= UB4 + 1e-12))
        out.append(rec); print(json.dumps(rec), flush=True)
    json.dump(out, open(f'verify_collision_{n}.json', 'w'), indent=1)
