"""
E6 — changing representation after the old one becomes inadequate (a concept must SPLIT).
Data: 8 subclasses = Gaussian clusters in R^32; subclasses (2k, 2k+1) form superclass k. Superclass centres are far
apart; the two subclasses of a superclass differ along a random direction by a margin `sep`.
Phase 1: MLP trained on the 4 superclass labels for S1 steps (short or long -> tests neural collapse).
Phase 2: 8 subclass labels, n examples per subclass. Methods:
  probe      : linear (logistic) probe on frozen penultimate features
  knn_feat   : 1-NN on frozen features
  ft_all     : fine-tune whole net (new 8-way head)
  scratch    : train the same MLP from scratch on the few examples
  knn_raw    : 1-NN on raw inputs
  cluster    : classical semi-supervised: k-means (k=8) on the unlabeled phase-1 inputs, clusters labelled by the
               few examples (majority), predict via nearest centroid
Metric: phase-2 test accuracy (8-way); also within-superclass subclass accuracy.
"""
import json, sys, time
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from common import seed_all, pool_run

D, K = 32, 8


def make_world(rng, sep):
    sup = rng.normal(0, 1, (4, D)); sup /= np.linalg.norm(sup, axis=1, keepdims=True); sup *= 6.0
    cen = np.zeros((8, D))
    for k in range(4):
        u = rng.normal(0, 1, D); u -= (u @ sup[k]) / (sup[k] @ sup[k]) * sup[k]; u /= np.linalg.norm(u)
        cen[2 * k] = sup[k] + sep / 2 * u; cen[2 * k + 1] = sup[k] - sep / 2 * u
    return cen


def sample(rng, cen, n_per):
    X = np.concatenate([cen[c] + rng.normal(0, 1, (n_per, D)) for c in range(8)])
    y = np.repeat(np.arange(8), n_per)
    return X.astype(np.float32), y


class Net(nn.Module):
    def __init__(self, h=256):
        super().__init__()
        self.f = nn.Sequential(nn.Linear(D, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU())
        self.head = nn.Linear(h, 4)

    def forward(self, x):
        return self.head(self.f(x))


def train(net, X, y, steps, lr=1e-3, wd=5e-4, params=None, bs=128):
    X, y = torch.tensor(X), torch.tensor(y)
    opt = torch.optim.AdamW(params if params is not None else net.parameters(), lr=lr, weight_decay=wd)
    for s in range(steps):
        idx = torch.randint(0, len(y), (min(bs, len(y)),))
        loss = F.cross_entropy(net(X[idx]), y[idx])
        opt.zero_grad(); loss.backward(); opt.step()
    return net


def logistic_probe(F_tr, y_tr, F_te, steps=500):
    W = nn.Linear(F_tr.shape[1], 8)
    opt = torch.optim.Adam(W.parameters(), lr=1e-2)
    a, b = torch.tensor(F_tr), torch.tensor(y_tr)
    mu, sd = a.mean(0), a.std(0) + 1e-6
    for _ in range(steps):
        loss = F.cross_entropy(W((a - mu) / sd), b) + 1e-3 * (W.weight ** 2).sum()
        opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad():
        return W((torch.tensor(F_te) - mu) / sd).argmax(-1).numpy()


def nn1(A, ya, B):
    d = ((B[:, None, :] - A[None]) ** 2).sum(-1)
    return ya[d.argmin(1)]


def kmeans(X, k, rng, iters=50):
    C = X[rng.choice(len(X), k, replace=False)]
    for _ in range(iters):
        a = ((X[:, None] - C[None]) ** 2).sum(-1).argmin(1)
        C = np.array([X[a == j].mean(0) if (a == j).any() else C[j] for j in range(k)])
    return C


def job(args):
    seed, sep, S1, n = args
    seed_all(seed); rng = np.random.default_rng(seed)
    cen = make_world(rng, sep)
    X1, y1 = sample(rng, cen, 500)                 # phase-1 pool (subclass labels hidden)
    Xte, yte = sample(rng, cen, 200)
    X2, y2 = sample(rng, cen, n)                   # phase-2 few-shot subclass labels
    net = train(Net(), X1, y1 // 2, S1)
    with torch.no_grad():
        acc1 = float((net(torch.tensor(Xte)).argmax(-1).numpy() == yte // 2).mean())
        F2, Fte = net.f(torch.tensor(X2)).numpy(), net.f(torch.tensor(Xte)).numpy()
        F1 = net.f(torch.tensor(X1)).numpy()
    res = dict(seed=seed, sep=sep, S1=S1, n=n, phase1_acc=acc1)
    # feature-space diagnostic: within-superclass subclass separability (Fisher ratio along best direction)
    res["probe"] = float((logistic_probe(F2, y2, Fte) == yte).mean())
    res["probe_full"] = float((logistic_probe(F1, y1, Fte) == yte).mean())    # oracle: probe with ALL labels
    res["knn_feat"] = float((nn1(F2, y2, Fte) == yte).mean())
    res["knn_raw"] = float((nn1(X2, y2, Xte) == yte).mean())
    ft = Net(); ft.load_state_dict(net.state_dict()); ft.head = nn.Linear(256, 8)
    res["ft_all"] = float((train(ft, X2, y2, 500, lr=1e-3, wd=0.0)(torch.tensor(Xte)).argmax(-1).numpy() == yte).mean())
    sc = Net(); sc.head = nn.Linear(256, 8)
    res["scratch"] = float((train(sc, X2, y2, 500, lr=1e-3, wd=0.0)(torch.tensor(Xte)).argmax(-1).numpy() == yte).mean())
    C = kmeans(np.concatenate([X1, X2]), 8, rng)
    lab = {}
    a2 = ((X2[:, None] - C[None]) ** 2).sum(-1).argmin(1)
    for j in range(8):
        v = y2[a2 == j]; lab[j] = int(np.bincount(v).argmax()) if len(v) else -1
    ate = ((Xte[:, None] - C[None]) ** 2).sum(-1).argmin(1)
    res["cluster"] = float((np.array([lab[j] for j in ate]) == yte).mean())
    return res


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(job((1, 3.0, 300, 5))); print(job((1, 3.0, 8000, 5))); sys.exit()
    jobs = [(s, sep, S1, n) for s in [1, 2, 3] for sep in [2.0, 3.0, 4.0] for S1 in [300, 3000, 20000] for n in [5]]
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 10)
    json.dump(res, open("e6_results.json", "w"), indent=1)
    print("done")
