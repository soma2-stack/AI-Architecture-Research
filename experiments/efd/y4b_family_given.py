"""
Y.4b — gradient learning WITH the right hypothesis family (separates 'optimisation within the family'
from 'not having the family'). Same world as Y.4 (true surface IDs given: perception removed).
Model: each surface u is softly assigned to a cell (k, m) of a K x M grid by a doubly-stochastic matrix
P = Sinkhorn(logits / tau) (a relaxed bijection surfaces -> cells). Learnable tables:
   F[k_a, k_b] -> logits over K (symbol rule),  G[m_a, m_b] -> logits over M (style rule).
Predicted distribution over output cells = outer(p_sym, p_sty) marginalised over the soft cells of a and b;
likelihood of the observed output surface = sum over cells of P[c, cell] * p(cell).
Anneal tau; harden P with the Hungarian algorithm at the end; evaluate on unseen pairs (exact table prediction).
Also: capacity-limited neural embeddings (e=2,4) with weight decay (compression pressure without discreteness).
"""
import json, sys, time
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from scipy.optimize import linear_sum_assignment
from common import seed_all, pool_run
import y4_functional_symbols as Y


def sinkhorn(L, iters=30):
    for _ in range(iters):
        L = L - torch.logsumexp(L, 1, keepdim=True)
        L = L - torch.logsumexp(L, 0, keepdim=True)
    return L.exp()


def fit_family(W, steps=3000, lr=0.05, seed=0):
    K, M, S = W["K"], W["M"], W["S"]
    torch.manual_seed(seed)
    A = torch.tensor([a for a, b in W["tr"]]); B = torch.tensor([b for a, b in W["tr"]])
    Cc = torch.tensor([W["out"](a, b) for a, b in W["tr"]])
    Lg = (0.01 * torch.randn(S, S)).requires_grad_(True)
    Ft = (0.01 * torch.randn(K, K, K)).requires_grad_(True)
    Gt = (0.01 * torch.randn(M, M, M)).requires_grad_(True)
    opt = torch.optim.Adam([Lg, Ft, Gt], lr=lr)
    cell_k = torch.arange(S) // M; cell_m = torch.arange(S) % M
    Ek = F.one_hot(cell_k, K).float(); Em = F.one_hot(cell_m, M).float()      # cell -> k, cell -> m
    def loss_fn(P):
        pk = P @ Ek; pm = P @ Em                     # surface -> soft symbol / style
        ka, kb, ma, mb = pk[A], pk[B], pm[A], pm[B]
        fs = torch.softmax(Ft, -1); gs = torch.softmax(Gt, -1)
        p_sym = torch.einsum("ni,nj,ijk->nk", ka, kb, fs)            # predicted output symbol dist
        p_sty = torch.einsum("ni,nj,ijk->nk", ma, mb, gs)
        p_cell = (p_sym[:, :, None] * p_sty[:, None, :]).reshape(len(A), S)
        lik = (P[Cc] * p_cell).sum(-1)
        return -(lik + 1e-9).log().mean()
    for s in range(steps):
        tau = max(0.05, 1.0 * (0.05 ** (s / steps)))
        loss = loss_fn(sinkhorn(Lg / tau))
        opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad():
        r, c = linear_sum_assignment(-Lg.numpy())
        P = torch.zeros(S, S); P[r, c] = 1.0
        hard_loss = float(loss_fn(P))
        cellpos = {int(u): (int(c[i]) // M, int(c[i]) % M) for i, u in enumerate(r)}
    rel = {(a, b): W["out"](a, b) for a, b in W["tr"]}
    sc, Fm, Gm = Y.fscore(cellpos, rel, K, M)
    pred = Y.predictor_from((sc, cellpos, Fm, Gm), K, M, np.random.default_rng(1))
    acc = float(np.mean([pred(a, b) == W["out"](a, b) for a, b in W["te"]]))
    return dict(hard_train_consistency=sc / (2 * len(rel)), hard_nll=hard_loss, test_acc=acc)


class SmallEmb(nn.Module):
    def __init__(self, S, e, h=128):
        super().__init__()
        self.E = nn.Embedding(S, e)
        self.f = nn.Sequential(nn.Linear(2 * e, h), nn.GELU(), nn.Linear(h, S))

    def forward(self, a, b):
        return self.f(torch.cat([self.E(a), self.E(b)], -1))


def job(args):
    seed, rho = args
    seed_all(seed)
    W, D = Y.make_world(seed, rho=rho)
    res = dict(seed=seed, rho=rho)
    fams = [fit_family(W, seed=seed * 10 + r) for r in range(5)]
    best = max(fams, key=lambda z: (z["hard_train_consistency"], -z["hard_nll"]))    # select by TRAINING fit only
    res["family_grad_best"] = best
    res["family_grad_restarts_perfect"] = sum(f["hard_train_consistency"] == 1.0 for f in fams)
    res["family_grad_mean_test"] = float(np.mean([f["test_acc"] for f in fams]))
    A = torch.tensor([a for a, b in W["tr"]]); B = torch.tensor([b for a, b in W["tr"]])
    Cc = torch.tensor([W["out"](a, b) for a, b in W["tr"]])
    for e in (2, 4):
        for wd in (1e-3, 1e-2):
            torch.manual_seed(seed)
            m = SmallEmb(W["S"], e)
            opt = torch.optim.AdamW(m.parameters(), lr=3e-3, weight_decay=wd)
            for s in range(4000):
                loss = F.cross_entropy(m(A, B), Cc)
                opt.zero_grad(); loss.backward(); opt.step()
            with torch.no_grad():
                At = torch.tensor([a for a, b in W["te"]]); Bt = torch.tensor([b for a, b in W["te"]])
                yt = torch.tensor([W["out"](a, b) for a, b in W["te"]])
                res[f"smallemb_e{e}_wd{wd}"] = dict(train_loss=float(loss), test_acc=float((m(At, Bt).argmax(-1) == yt).float().mean()))
    return res


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(json.dumps(job((1, 0.3)), indent=1)); sys.exit()
    jobs = [(s, rho) for s in range(1, 6) for rho in [0.1, 0.2, 0.35, 0.6, 0.85]]
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 6)
    json.dump(res, open("y4b_results.json", "w"), indent=1)
    print("done")
