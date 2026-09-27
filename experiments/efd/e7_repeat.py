"""
E7 — deciding what computation to repeat (and how often): reachability in random grids.
Input: N x N grid, walls with density 0.42 (near percolation, so reachability is long-range), one start cell. Target: per-cell "reachable from start" (4-connectivity).
Train N=9; test N=9,15,21,31 (longer shortest paths need more propagation steps).
Models: fixed-depth CNN (12 conv layers); weight-tied recurrent CNN with input recall ("deep thinking" style,
Bansal et al. 2022), trained with 20 iterations, tested with 20 / 60 / 200 iterations and with halting at a fixed
point; small Transformer over cells (4 layers, 2D learned-free: row/col sinusoidal); classical BFS.
Metric: fraction of grids solved exactly, and per-cell accuracy on open cells.
"""
import json, sys, time
from collections import deque
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from common import seed_all, pool_run, Block


def make_grid(rng, N, dens=0.42):
    W = (rng.random((N, N)) < dens).astype(np.float32)
    open_ = np.argwhere(W == 0)
    s = open_[rng.integers(len(open_))]
    S = np.zeros((N, N), np.float32); S[s[0], s[1]] = 1
    R = np.zeros((N, N), np.float32); q = deque([tuple(s)]); R[s[0], s[1]] = 1
    while q:
        a, b = q.popleft()
        for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = a + da, b + db
            if 0 <= x < N and 0 <= y < N and W[x, y] == 0 and R[x, y] == 0:
                R[x, y] = 1; q.append((x, y))
    return np.stack([W, S]), R


def batch(rng, B, N):
    xs, ys = zip(*[make_grid(rng, N) for _ in range(B)])
    return torch.tensor(np.array(xs)), torch.tensor(np.array(ys))


class FixedCNN(nn.Module):
    def __init__(self, w=64, depth=12):
        super().__init__()
        layers = [nn.Conv2d(2, w, 3, padding=1), nn.ReLU()]
        for _ in range(depth - 2):
            layers += [nn.Conv2d(w, w, 3, padding=1), nn.ReLU()]
        layers += [nn.Conv2d(w, 1, 3, padding=1)]
        self.net = nn.Sequential(*layers)

    def forward(self, x, iters=None):
        return self.net(x)[:, 0]


class RecurCNN(nn.Module):
    def __init__(self, w=64):
        super().__init__()
        self.inp = nn.Conv2d(2, w, 3, padding=1)
        self.block = nn.Sequential(nn.Conv2d(w + 2, w, 3, padding=1), nn.ReLU(), nn.Conv2d(w, w, 3, padding=1), nn.ReLU())
        self.head = nn.Conv2d(w, 1, 3, padding=1)

    def forward(self, x, iters=20, halt=False):
        h = F.relu(self.inp(x))
        for t in range(iters):
            h_new = self.block(torch.cat([h, x], 1))
            if halt and t > 5:
                if (self.head(h_new) > 0).eq(self.head(h) > 0).all():
                    h = h_new; break
            h = h_new
        return self.head(h)[:, 0]


class CellTF(nn.Module):
    def __init__(self, d=64, layers=4):
        super().__init__()
        self.inp = nn.Linear(2 + 16, d)
        self.blocks = nn.ModuleList([Block(d, 4, "none", causal=False) for _ in range(layers)])
        self.ln = nn.LayerNorm(d); self.out = nn.Linear(d, 1)

    def forward(self, x, iters=None):
        B, _, N, _ = x.shape
        r = torch.arange(N, dtype=torch.float32)
        fr = torch.stack([torch.sin(r / (10 ** (i / 4))) if i % 2 == 0 else torch.cos(r / (10 ** (i / 4))) for i in range(8)], -1)
        pe = torch.cat([fr[:, None, :].expand(N, N, 8), fr[None, :, :].expand(N, N, 8)], -1)
        z = torch.cat([x.permute(0, 2, 3, 1), pe[None].expand(B, -1, -1, -1)], -1).reshape(B, N * N, -1)
        z = self.inp(z)
        for b in self.blocks:
            z = b(z)
        return self.out(self.ln(z))[..., 0].reshape(B, N, N)


def evaluate(pred_fn, seed, Ns=(9, 15, 21, 31), n=60):
    rng = np.random.default_rng(seed + 321); out = {}
    for N in Ns:
        x, y = batch(rng, n, N)
        with torch.no_grad():
            p = (pred_fn(x) > 0).float()
        openm = (x[:, 0] == 0)
        solved = ((p == y) | ~openm).all(-1).all(-1).float().mean()
        cell = ((p == y) & openm).sum() / openm.sum()
        out[N] = dict(solved=float(solved), cell=float(cell))
    return out


def job(args):
    kind, seed = args
    seed_all(seed); rng = np.random.default_rng(seed); t0 = time.time()
    if kind == "bfs":
        return dict(kind=kind, seed=seed, res={N: dict(solved=1.0, cell=1.0) for N in (9, 15, 21, 31)})
    m = {"cnn": FixedCNN, "recur": RecurCNN, "tf": CellTF}[kind]()
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    steps = 3000
    for s in range(steps):
        x, y = batch(rng, 32, 9)
        loss = F.binary_cross_entropy_with_logits(m(x), y, weight=(x[:, 0] == 0).float())
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
    m.eval()
    res = {}
    if kind == "recur":
        for it in (20, 60, 200):
            res[f"iters{it}"] = evaluate(lambda x: m(x, iters=it), seed)
        res["halt_max300"] = evaluate(lambda x: m(x, iters=300, halt=True), seed)
    else:
        res["fixed"] = evaluate(lambda x: m(x), seed)
    return dict(kind=kind, seed=seed, res=res, secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        seed_all(0); rng = np.random.default_rng(0); x, y = make_grid(rng, 9); print(x[0], "\n", y); sys.exit()
    jobs = [("bfs", 1)] + [(k, s) for k in ["cnn", "recur", "tf"] for s in [1, 2, 3]]
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 10)
    json.dump(res, open("e7_results.json", "w"), indent=1)
    print("done")
