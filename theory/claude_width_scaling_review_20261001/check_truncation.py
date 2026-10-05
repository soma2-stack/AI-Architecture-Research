"""Claude's numerical check of THEORY.md Theorem 1 (evidence, not proof).

For dense h' = tanh(R h + W x + b), ||R||op = a < 1, bounded inputs and group-RMS normalised sensitivities Z = S D:
  1. exact Z_T by forward RTRL;
  2. Z^[H] from THEORY.md's factored online store (Q_{t,s}, v_s, x_s) -- H(n^2+2n) numbers;
  3. Z^[H] from a store of only the last H+1 hidden states and last H inputs (truncated BPTT; no transition is
     re-evaluated, only Jacobian products) -- (2H+1)n numbers;
then check 2 == 3, ||Z - Z^[H]||op <= e_H = C_* a^H/(1-a), ||B_t||op <= C_*, and the B B^T identity.
"""
import json, math, sys
import numpy as np

def run(n, a, H_list, T=60, seed=0, wop=1.0, B=1.0, bstar=0.5):
    rng = np.random.default_rng(seed)
    R = rng.normal(size=(n, n)); R *= a / np.linalg.norm(R, 2)
    W = rng.normal(size=(n, n)); W *= wop / np.linalg.norm(W, 2)
    b = rng.normal(size=n); b *= bstar / math.sqrt(np.mean(b ** 2))
    X = rng.uniform(-B, B, size=(T, n))
    wR, wW, wb = np.linalg.norm(R) / n, np.linalg.norm(W) / n, math.sqrt(np.mean(b ** 2))
    Cstar = math.sqrt(a ** 2 + wop ** 2 * B ** 2 + bstar ** 2)
    P = 2 * n * n + n
    # parameter order: R (row-major), W (row-major), b
    def inj(hprev, x, G):
        """Normalised injection B_t as an n x P matrix."""
        M = np.zeros((n, P))
        for i in range(n):
            M[i, i * n:(i + 1) * n] = wR * hprev
            M[i, n * n + i * n:n * n + (i + 1) * n] = wW * x
            M[i, 2 * n * n + i] = wb
        return G[:, None] * M
    h = np.zeros(n); Z = np.zeros((n, P)); hs = [h.copy()]; Bs = []; Gs = []; maxB = 0.; bbt = 0.
    store = []   # THEORY.md factored store: list of (Q, v, x)
    for t in range(T):
        hn = np.tanh(R @ h + W @ X[t] + b); G = 1 - hn ** 2
        Bt = inj(h, X[t], G); A = G[:, None] * R
        Z = A @ Z + Bt
        maxB = max(maxB, np.linalg.norm(Bt, 2))
        pred = np.diag(G ** 2) * (wR ** 2 * h @ h + wW ** 2 * X[t] @ X[t] + wb ** 2)
        bbt = max(bbt, float(np.abs(Bt @ Bt.T - pred).max()))
        store = [(A @ Q, v, x) for Q, v, x in store] + [(np.diag(G), h.copy(), X[t].copy())]
        h = hn; hs.append(h.copy()); Bs.append(Bt); Gs.append(G)
    out = {'n': n, 'a': a, 'P': P, 'C_star': Cstar, 'max_B_op': maxB, 'BBt_identity_err': bbt, 'H': []}
    for H in H_list:
        # (2) factored store, keep newest H terms
        ZF = np.zeros((n, P))
        for Q, v, x in store[-H:] if H > 0 else []:
            M = np.zeros((n, P))
            for i in range(n):
                M[i, i * n:(i + 1) * n] = wR * v; M[i, n * n + i * n:n * n + (i + 1) * n] = wW * x; M[i, 2 * n * n + i] = wb
            ZF += Q @ M
        # (3) only hidden states h_{T-H..T} and inputs x_{T-H+1..T}: rebuild G, A, B by Jacobian products
        hmem = hs[T - H:T + 1]; xmem = X[T - H:T]
        ZB = np.zeros((n, P))
        for k in range(H):                       # step s = T-H+1+k (1-based); uses h_{s-1}, h_s, x_s
            Gk = 1 - hmem[k + 1] ** 2
            term = inj(hmem[k], xmem[k], Gk)
            for j in range(k + 1, H):            # propagate through later steps with A = diag(1-h^2) R
                term = ((1 - hmem[j + 1] ** 2)[:, None] * R) @ term
            ZB += term
        eH = Cstar * a ** H / (1 - a)
        out['H'].append({'H': H, 'factored_vs_hidden_state_store_max_diff': float(np.abs(ZF - ZB).max()),
                         'trunc_err_op': float(np.linalg.norm(Z - ZF, 2)), 'e_H_bound': eH,
                         'ratio_err_to_bound': float(np.linalg.norm(Z - ZF, 2) / eH),
                         'memory_theory_H(n^2+2n)': H * (n * n + 2 * n), 'memory_hidden_store_(2H+1)n': (2 * H + 1) * n})
    return out

if __name__ == '__main__':
    res = [run(n, a, [1, 2, 4, 8, 12], seed=s) for n in (3, 6, 12, 24) for a in (0.5, 0.8) for s in (0, 1)]
    json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else 'truncation_check.json', 'w'), indent=1)
    for r in res:
        worst = max(h['ratio_err_to_bound'] for h in r['H']); diff = max(h['factored_vs_hidden_state_store_max_diff'] for h in r['H'])
        print(f"n={r['n']:2d} a={r['a']} maxB/C*={r['max_B_op']/r['C_star']:.3f} BBt_err={r['BBt_identity_err']:.1e} "
              f"max err/e_H={worst:.3f} factored-vs-(2H+1)n-store diff={diff:.1e} "
              f"mem@H=8: {r['H'][3]['memory_theory_H(n^2+2n)']} vs {r['H'][3]['memory_hidden_store_(2H+1)n']}")
