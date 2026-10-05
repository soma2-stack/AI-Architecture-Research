"""Independent reconstruction of Codex's adversarial co-rotating pairs (from their saved C,Q,Z only) and a sharper
look at their query brackets: one-step box lower, OPTIMISED TWO-STEP permitted-query lower (admissible future inputs),
and the kappa all-query envelope. Reference model (R0); dense transfer adds <= 2 eta < 4e-9."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from block import build
sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_aperiodic import G_LO, G_HI, box_max
torch.set_num_threads(8)
EPS = 1e-3
CODEX = '../codex_two_pulse_corotating_20261002/'

def gates_from(S, Q, Z, C, T):
    d, k = S['d'], S['k']; ck = S['ck']
    field = torch.tanh(math.sqrt(T * d) * (Q @ C @ Z.T))
    base = torch.tensor([0.25 if i % 2 == 0 else -0.25 for i in range(d)])
    latent = base + 0.055 * (field - field.mean(dim=1, keepdim=True))
    rot = torch.stack([torch.roll(latent[t], t) for t in range(T)])
    common = ck * rot[:, :1]; cyc = rot[:, 1:] + common
    return torch.cat([1 - cyc ** 2, 1 - common ** 2], 1), rot

def endpoint(S, G):
    a, OA, d = S['a'], S['OA'], S['d']; M = S['C0']; s = sum(a ** j for j in range(3 * S['n'])); I = torch.eye(d)
    for g in G:
        M = g[:, None] * (a * OA @ M + I); s = float(g[-1]) * (a * s + 1)
    return a * OA @ M + I, a * s + 1

def full_reference_pieces(S):
    n, k = S['n'], S['k']; a = S['a']
    R0mem = a * S['O']; delta = 1 / (100 * n)
    return R0mem, delta

def two_step_lower(S, dC, starts=6, iters=60, seed=0):
    """maximise ||dC^T zeta|| over two-step futures from h=0 with preactivations in [1/4,1/2]^n (gates in [g_lo,g_hi]),
    zeta = V^T (memory part of R^T G1 R^T G2 q / beta). Projected gradient ascent on gates; admissibility checked after."""
    n, k, d, a, V, O = S['n'], S['k'], S['d'], S['a'], S['V'], S['O']; l = n - k
    beta = math.sqrt(k * a * a + l * (1 / (100 * n)) ** 2)
    delta = 1 / (100 * n)
    q = torch.full((n,), 1 / math.sqrt(n))
    def RT(x):  # R0^T x
        return torch.cat([a * O.T @ x[:k], delta * x[k:]])
    rng = np.random.default_rng(seed); best = 0.0; bestg = None
    for st in range(starts):
        g1 = torch.tensor(rng.uniform(G_LO, G_HI, n), requires_grad=True); g2 = torch.tensor(rng.uniform(G_LO, G_HI, n), requires_grad=True)
        for it in range(iters):
            eta = RT(g1 * RT(g2 * q)) / beta; zeta = V.T @ eta[:k]
            val = (dC.T @ zeta).norm()
            gr1, gr2 = torch.autograd.grad(val, (g1, g2))
            with torch.no_grad():
                g1 += 0.02 * torch.sign(gr1); g2 += 0.02 * torch.sign(gr2)
                g1.clamp_(G_LO, G_HI); g2.clamp_(G_LO, G_HI)
        with torch.no_grad():
            eta = RT(g1 * RT(g2 * q)) / beta; zeta = V.T @ eta[:k]; val = float((dC.T @ zeta).norm())
        if val > best: best = val; bestg = (g1.detach().clone(), g2.detach().clone())
    # admissibility of the realising inputs: pre1 = atanh-inverse of gate, v1 = pre1 - b ; h1 = tanh(pre1); v2 = pre2 - R h1 - b
    g1, g2 = bestg
    pre1 = torch.atanh(torch.sqrt(1 - g1)); pre2 = torch.atanh(torch.sqrt(1 - g2))
    v1 = pre1 - 0.05; h1 = torch.tanh(pre1)
    Rh1 = torch.cat([a * O @ h1[:k], delta * h1[k:]]); v2 = pre2 - Rh1 - 0.05
    return best, float(max(v1.abs().max(), v2.abs().max()))

def run(n, start):
    S = build(n); d, k = S['d'], S['k']
    z = np.load(CODEX + f'adversary_n{n}_start{start}.npz')
    C, Q, Z = (torch.tensor(z[x]) for x in ('C', 'Q', 'Z')); T = Q.shape[0]
    Gp, rot = gates_from(S, Q, Z, C, T); Gm, _ = gates_from(S, Q, Z, -C, T)
    Mp, sp = endpoint(S, Gp); Mm, sm = endpoint(S, Gm); dC = Mp - Mm
    K = S['a'] * 0.4 * math.sqrt(S['l']) / n
    env = K * max(float(torch.linalg.matrix_norm(dC, 2)), abs(sp - sm))
    # one-step box: zeta = Zq g_mem ; full g in box over n coords but only memory part matters
    Y = (S['Zq'].T @ dC)                                                  # k x d : answer = Y^T g_mem
    one_step = S['wRH'] * math.sqrt(k) * box_max(Y, k, starts=20)
    two_step, maxv = two_step_lower(S, dC)
    two = S['wRH'] * two_step
    return {'n': n, 'start': start, 'T': T, 'chart_dim': int(C.numel()), 'kappa_envelope_halfsep': env / 2 * 2,
            'envelope_ratio_to_2eps': env / 0.002, 'codex_reported_ratio': None,
            'one_step_box_lower': one_step, 'two_step_lower': two, 'two_step_max_input': maxv,
            'scalar_diff': abs(sp - sm), 'dC_op': float(torch.linalg.matrix_norm(dC, 2)), 'dC_F': float(dC.norm())}

if __name__ == '__main__':
    rep = json.load(open(CODEX + 'ADVERSARY.json'))['rows']
    out = []
    for r in rep:
        res = run(r['n'], r['start']); res['codex_reported_ratio'] = r['independent_full_operator_upper_ratio']
        res['codex_reported_lower'] = r['actual_query_lower_distance']; out.append(res); print(json.dumps(res), flush=True)
    json.dump(out, open('codex_pairs.json', 'w'), indent=1)
