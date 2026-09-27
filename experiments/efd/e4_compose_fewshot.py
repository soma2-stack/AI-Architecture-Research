"""
E4 — reusable decomposition vs memorised solutions; reuse of a new primitive learned from few examples.
Domain: digit strings of length 6. Primitives: R reverse, S add-1 mod 10, W rotate-left, M x->3x mod 10.
Episode (in-context): K=4 demonstrations (input -> output) of a hidden program, then a query input.
Meta-train: programs of depth 2, EXCLUDING 4 held-out ordered pairs.
Tests: (a) train-distribution depth-2 pairs, (b) held-out depth-2 pairs (systematicity),
(c) depth 3, (d) depth 4, (e) NEW primitive N (random position permutation) shown via 2 extra demos of N alone,
    then 3 demos of N∘P and a query of N∘P (composition with an in-context-learned primitive).
Learners: meta-trained Transformer (bidirectional over the episode), meta-trained GRU, program search
(enumerate compositions up to depth 4 over the primitives; with (e) the search may also induce N as a position
permutation from its demos, i.e. a DSL extended by one induced primitive).
Metric: exact-match accuracy of the 6-digit output.
"""
import json, sys, time, itertools
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from common import seed_all, pool_run, Block

import os
L = int(os.environ.get("E4L", "6"))
PRIMS = {
    "R": lambda x: x[::-1],
    "S": lambda x: [(v + 1) % 10 for v in x],
    "W": lambda x: x[1:] + x[:1],
    "M": lambda x: [(3 * v) % 10 for v in x],
}
NAMES = list(PRIMS)
HELD = [("S", "R"), ("M", "W"), ("W", "M"), ("R", "S")]          # held-out ordered pairs (apply first, then second)
PAIRS = [p for p in itertools.product(NAMES, repeat=2) if p not in HELD]


def run_prog(prog, x):
    for op in prog:
        x = PRIMS[op](x) if isinstance(op, str) else [x[i] for i in op]
    return x


def rand_x(rng):
    return [int(v) for v in rng.integers(0, 10, L)]


# token layout: digits 0..9, SEP=10 (between in/out), EOE=11 (end of example), Q=12 (query marker), PAD=13
SEP, EOE, Q, V = 10, 11, 12, 14


def episode(prog, rng, K=4, pre=None):
    toks = []
    if pre is not None:                      # extra demos of a new primitive alone
        for _ in range(2):
            x = rand_x(rng); toks += x + [SEP] + run_prog(pre, x) + [EOE]
    for _ in range(K if pre is None else 3):
        x = rand_x(rng); toks += x + [SEP] + run_prog(prog, x) + [EOE]
    xq = rand_x(rng); toks += [Q] + xq + [SEP]
    return toks, run_prog(prog, xq)


class TFModel(nn.Module):
    def __init__(self, d=int(os.environ.get("E4D", "128")), layers=4, maxlen=160):
        super().__init__()
        self.emb = nn.Embedding(V, d); self.pos = nn.Embedding(maxlen, d)
        self.blocks = nn.ModuleList([Block(d, 4, "learned", causal=False) for _ in range(layers)])
        self.ln = nn.LayerNorm(d); self.qry = nn.Parameter(torch.randn(L, d) * 0.1); self.out = nn.Linear(d, 10)

    def forward(self, tok):
        B, T = tok.shape
        x = torch.cat([self.emb(tok) + self.pos(torch.arange(T))[None], self.qry[None].expand(B, -1, -1)], 1)
        for b in self.blocks:
            x = b(x)
        return self.out(self.ln(x[:, -L:]))


class GRUModel(nn.Module):
    def __init__(self, d=256):
        super().__init__()
        self.emb = nn.Embedding(V, d); self.rnn = nn.GRU(d, d, num_layers=2, batch_first=True)
        self.dec = nn.GRU(d, d, batch_first=True); self.qry = nn.Parameter(torch.randn(L, d) * 0.1); self.out = nn.Linear(d, 10)

    def forward(self, tok):
        _, h = self.rnn(self.emb(tok))
        y, _ = self.dec(self.qry[None].expand(tok.shape[0], -1, -1), h[-1:].contiguous())
        return self.out(y)


def batch(rng, B, mode="train"):
    toks, tgts = [], []
    for _ in range(B):
        if mode == "train":
            # depth-2 programs from PAIRS; also 25% episodes with a random NEW position permutation primitive
            if rng.random() < 0.25:
                N = tuple(int(v) for v in rng.permutation(L)); P = NAMES[int(rng.integers(4))]
                t, y = episode((N, P), rng, pre=(N,))
            else:
                t, y = episode(PAIRS[int(rng.integers(len(PAIRS)))], rng)
        toks.append(t); tgts.append(y)
    T = max(len(t) for t in toks)
    toks = [t + [13] * (T - len(t)) for t in toks]
    return torch.tensor(toks), torch.tensor(tgts)


def test_sets(rng, n=300):
    sets = {}
    sets["depth2_train"] = [episode(PAIRS[int(rng.integers(len(PAIRS)))], rng) for _ in range(n)]
    sets["depth2_heldout"] = [episode(HELD[int(rng.integers(len(HELD)))], rng) for _ in range(n)]
    # deep programs are kept only if NOT equivalent to any program of depth <= 2 (the primitives are bijections and
    # partly commute, so many deep compositions collapse; see E8 lesson)
    probe = [rand_x(np.random.default_rng(12345 + i)) for i in range(40)]
    shallow = {tuple(tuple(run_prog(p, x)) for x in probe) for d in (1, 2) for p in itertools.product(NAMES, repeat=d)}
    def deep(d):
        while True:
            prog = tuple(NAMES[int(i)] for i in rng.integers(0, 4, d))
            if tuple(tuple(run_prog(prog, x)) for x in probe) not in shallow:
                return prog
    sets["depth3"] = [episode(deep(3), rng) for _ in range(n)]
    sets["depth4"] = [episode(deep(4), rng) for _ in range(n)]
    ne = []
    for _ in range(n):
        N = tuple(int(v) for v in rng.permutation(L)); P = NAMES[int(rng.integers(4))]
        ne.append(episode((N, P), rng, pre=(N,)))
    sets["new_prim"] = ne
    return sets


def parse(t):
    # returns list of (x, y) demos and the query x
    demos, cur = [], []
    i = 0
    while i < len(t) and t[i] != Q:
        seg = t[i:i + 2 * L + 2]; demos.append((seg[:L], seg[L + 1:2 * L + 1])); i += 2 * L + 2
    return demos, t[i + 1:i + 1 + L]


def program_search(t, max_depth=4, induce=True):
    demos, xq = parse(t)
    cands = []
    prim_list = list(NAMES)
    if induce and len(demos) >= 5:
        # induce a position-permutation primitive from the first two demos (the "new primitive alone" demos)
        for perm in itertools.permutations(range(L)):
            if all([x[i] for i in perm] == y for x, y in demos[:2]):
                prim_list.append(perm); break
        demos = demos[2:]
    for d in range(1, max_depth + 1):
        for prog in itertools.product(prim_list, repeat=d):
            if all(run_prog(prog, list(x)) == list(y) for x, y in demos):
                return run_prog(prog, list(xq))
    return None


def job(args):
    kind, seed, steps = args
    seed_all(seed); rng = np.random.default_rng(seed)
    t0 = time.time()
    sets = test_sets(np.random.default_rng(seed + 99))
    if kind == "search":
        res = {k: float(np.mean([program_search(t) == y for t, y in v])) for k, v in sets.items()}
        return dict(kind=kind, seed=seed, acc=res, secs=round(time.time() - t0, 1))
    m = TFModel() if kind == "tf" else GRUModel()
    opt = torch.optim.AdamW(m.parameters(), lr=5e-4, weight_decay=0.01)
    sch = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1, (s + 1) / 300) * max(0.05, 1 - s / steps))
    for s in range(steps):
        tok, tgt = batch(rng, int(os.environ.get("E4B", "48")))
        loss = F.cross_entropy(m(tok).reshape(-1, 10), tgt.reshape(-1))
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step(); sch.step()
    m.eval(); res = {}
    with torch.no_grad():
        for k, v in sets.items():
            T = max(len(t) for t, _ in v)
            tok = torch.tensor([t + [13] * (T - len(t)) for t, _ in v]); y = torch.tensor([y for _, y in v])
            res[k] = float((m(tok).argmax(-1) == y).all(-1).float().mean())
    return dict(kind=kind, seed=seed, steps=steps, acc=res, secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(job(("search", 1, 0))); print(job(("tf", 1, 300))); sys.exit()
    jobs = [("search", 1, 0)] + [(k, s, 6000) for k in ["tf", "gru"] for s in [1, 2, 3]]
    out = "e4_results.json"
    if len(sys.argv) > 2 and sys.argv[2] == "b":        # E4b: easier (L from env), smaller TF, 20k steps
        jobs = [("search", 1, 0)] + [("tf", s, 20000) for s in [1, 2, 3]]
        out = "e4b_results.json"
    t0 = time.time()
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 7)
    json.dump(res, open(out, "w"), indent=1)
    print("done", round(time.time() - t0, 1))
