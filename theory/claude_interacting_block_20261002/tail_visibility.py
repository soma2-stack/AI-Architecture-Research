"""One-step permitted-box visibility (actual legal queries, lower estimate) vs kappa-envelope (rigorous upper) of the
first-order STRONG (top d) and TAIL (beyond d) Jacobian directions of the interacting block, per latent amplitude rho."""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from block import build, run_block
sys.path.insert(0, '../claude_aperiodic_review_20261001')
from check_aperiodic import box_max
torch.set_num_threads(8)
EPS = 1e-3

def run(n, T, baseline, rho=0.11, ntail=8):
    S = build(n); d, k = S['d'], S['k']
    Qz = torch.linalg.svd(torch.eye(d) - torch.ones(d, d) / d)[0][:, :d - 1]
    alt = torch.tensor([1.0 if i % 2 == 0 else -1.0 for i in range(d)])
    B = 0.25 if baseline == 'sustained' else 0.25 / math.sqrt(T)
    Z0 = (B * alt).repeat(T, 1)
    f = lambda th: run_block(S, Z0 + th.reshape(T, d - 1) @ Qz.T)
    J = torch.func.jacfwd(f)(torch.zeros(T * (d - 1))).reshape(d * d, -1)
    U, s, Vh = torch.linalg.svd(J, full_matrices=False)
    K = S['a'] * 0.4 * math.sqrt(S['l']) / n
    def vis(j):
        dC = (J @ Vh[j]).reshape(d, d) * rho
        one = S['wRH'] * math.sqrt(k) * box_max(S['Zq'].T @ dC, k, starts=8)
        env = K * float(torch.linalg.matrix_norm(dC, 2))
        return one, env
    strong = [vis(j) for j in (0, d // 2, d - 2)]
    tail = [vis(j) for j in range(d - 1, min(d - 1 + ntail, len(s)))]
    return {'n': n, 'T': T, 'baseline': baseline, 'strong_one_step': [x[0] for x in strong], 'strong_env': [x[1] for x in strong],
            'tail_one_step_max': max(x[0] for x in tail), 'tail_env_max': max(x[1] for x in tail), 'tail_one_step': [x[0] for x in tail]}

if __name__ == '__main__':
    out = []
    for n in [int(x) for x in sys.argv[1].split(',')]:
        for T in [int(x) for x in sys.argv[2].split(',')]:
            for bl in ('sustained', 'weak'):
                r = run(n, T, bl); out.append(r)
                print('n=%4d T=%2d %-9s | strong dirs one-step %s env %s | TAIL max one-step %.5f  env %.5f   (eps=.001)' % (
                    n, T, bl, ['%.4f' % x for x in r['strong_one_step']], ['%.4f' % x for x in r['strong_env']], r['tail_one_step_max'], r['tail_env_max']), flush=True)
    json.dump(out, open(f'tail_visibility_{sys.argv[1].replace(",", "-")}.json', 'w'), indent=1)
