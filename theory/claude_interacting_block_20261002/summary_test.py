"""How well does a d-number summary capture the warmup part of the block credit?
C_end = a O_A (Phi_T C0 + Psi_T) + I.  Idealized (exact permutation) model: Phi_T = a^T O_A^T diag(D).
Summary c = Phi_T C0 f (f = unit O_A-fixed vector); linear decoder Gamma(c) = a^T O_A^T diag(D(c)) C0,
D(c) = (O_A^(T)... ) solved from c = m a^T O_A^T (D o f).  Measures, over random admissible latent-cycle histories:
  warm residual  E = Phi_T C0 - Gamma(c)      (what d numbers miss in the warmup part)
  fresh part     Psi_T variation
as all-query envelope distances K*||.||op  (K = a||H||/n), pairwise diameters vs 2*eps."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from block import build
torch.set_num_threads(8)
EPS = 1e-3

def histories(S, T, kind, rng, count):
    d = S['d']; alt = torch.tensor([1.0 if i % 2 == 0 else -1.0 for i in range(d)])
    out = []
    for _ in range(count):
        if kind == 'sustained':      # alternating .25 baseline + zero-sum perturbation |.|<=.11, changing every step
            Z = 0.25 * alt.repeat(T, 1) + torch.tensor(rng.uniform(-0.11, 0.11, (T, d)))
        elif kind == 'weak':          # total-budget: amplitudes scaled by 1/sqrt(T)
            Z = (0.25 * alt.repeat(T, 1) + torch.tensor(rng.uniform(-0.11, 0.11, (T, d)))) / math.sqrt(T)
        elif kind == 'random':        # arbitrary zero-sum profiles of amplitude up to .3
            Z = torch.tensor(rng.uniform(-0.3, 0.3, (T, d)))
        Z = Z - Z.mean(1, keepdim=True)
        out.append(Z)
    return out

def parts(S, Z):
    d, k, a, OA = S['d'], S['k'], S['a'], S['OA']; I = torch.eye(d)
    Phi = torch.eye(d); Psi = torch.zeros(d, d)
    for t in range(Z.shape[0]):
        x = torch.cat([torch.roll(Z[t], t), torch.zeros(k - d)]); h = S['U'] @ x; g = 1 - h ** 2
        gA = torch.cat([g[1:d], g[d:d + 1]])
        Phi = gA[:, None] * (a * OA @ Phi); Psi = gA[:, None] * (a * OA @ Psi + I)
    return Phi, Psi

def run(n, T, kind, count=60, seed=0):
    S = build(n); d, a, OA, C0 = S['d'], S['a'], S['OA'], S['C0']
    ev, evec = torch.linalg.eig(OA); i1 = int(torch.argmin((ev - 1).abs())); f = evec[:, i1].real; f = f / f.norm()
    m = float(f @ C0 @ f); OT = torch.linalg.matrix_power(OA, T)
    def decode(c):
        Df = OT @ c / (m * a ** T)            # = D o f in the idealized model (O_A^T)^(-1) = O_A^T ... use OA^T inverse = OA^T^T
        D = Df / f
        return a ** T * torch.linalg.matrix_power(OA.T, T).T @ torch.diag(D) @ C0 if False else a ** T * torch.linalg.matrix_power(OA, T) @ torch.diag(D) @ C0
    rng = np.random.default_rng(seed + n + T)
    Hs = histories(S, T, kind, rng, count)
    Es, Ps, Ws = [], [], []
    for Z in Hs:
        Phi, Psi = parts(S, Z); W = Phi @ C0
        c = W @ f
        # idealized: Phi = a^T OA^T? -> products G O G O ...: Phi = prod (a G_t OA); idealized Phi = a^T OA^T diag(D) when gates conjugate
        D_f = torch.linalg.solve(m * a ** T * torch.linalg.matrix_power(OA, T), c)      # solve c = m a^T OA^T (D o f)
        Gam = a ** T * torch.linalg.matrix_power(OA, T) @ torch.diag(D_f / f) @ C0
        Es.append(W - Gam); Ps.append(Psi); Ws.append(W)
    K = S['wRH'] * math.sqrt(S['k']) * float(S['Zq'].norm(dim=1).max()) if False else S['a'] * (0.4 * math.sqrt(S['l'])) / n
    def diam(Ms):
        best = 0.0
        for i in range(len(Ms)):
            for j in range(i + 1, len(Ms)):
                best = max(best, float(torch.linalg.matrix_norm(Ms[i] - Ms[j], 2)))
        return best
    dE, dP, dW = diam(Es), diam(Ps), diam(Ws)
    return {'n': n, 'T': T, 'kind': kind, 'K': K, 'warm_full_diam_env': K * a * dW, 'warm_residual_diam_env': K * a * dE,
            'fresh_diam_env': K * a * dP, 'residual_over_full': dE / dW, 'max_|E|op': max(float(torch.linalg.matrix_norm(E, 2)) for E in Es),
            'max_|Phi C0|op': max(float(torch.linalg.matrix_norm(W, 2)) for W in Ws)}

if __name__ == '__main__':
    res = []
    for n in [int(x) for x in sys.argv[1].split(',')]:
        for T in [int(x) for x in sys.argv[2].split(',')]:
            for kind in sys.argv[3].split(','):
                r = run(n, T, kind); res.append(r)
                print('n=%4d T=%2d %-9s | envelope diameters (vs 2eps=.002): warm full %.4f  warm RESIDUAL after d-summary %.5f  fresh %.5f | resid/full %.3f' % (
                    r['n'], r['T'], r['kind'], r['warm_full_diam_env'], r['warm_residual_diam_env'], r['fresh_diam_env'], r['residual_over_full']), flush=True)
    json.dump(res, open(f'summary_{sys.argv[1].replace(",", "-")}.json', 'w'), indent=1)
