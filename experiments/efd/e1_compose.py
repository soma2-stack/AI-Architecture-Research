"""
E1 — composition of learned operations far beyond training length (harness calibration).
S5: tokens = 5 fixed permutations of 5 items; target at each position = index of the composed permutation (120).
Z5: tokens = 0..4; target = running sum mod 5.
Train lengths 1..16 (per-position loss); test on length-256 sequences; accuracy per position bucket.
"""
import itertools, json, sys, time
import numpy as np
import torch
from common import seed_all, RNNSeq, TransformerSeq, train_loop, pool_run

PERMS = list(itertools.permutations(range(5)))
PIDX = {p: i for i, p in enumerate(PERMS)}
GENS = [(1, 0, 2, 3, 4), (1, 2, 3, 4, 0), (0, 2, 1, 3, 4), (4, 3, 2, 1, 0), (2, 0, 1, 4, 3)]   # generate S5


def compose(p, g):          # apply g after p
    return tuple(g[p[i]] for i in range(5))


def make_seq(task, T, rng):
    tok = rng.integers(0, 5, T)
    if task == "s5":
        st, out = tuple(range(5)), []
        for t in tok:
            st = compose(st, GENS[t]); out.append(PIDX[st])
        return tok, np.array(out)
    return tok, np.cumsum(tok) % 5


def batch_fn_factory(task, rng, B=64, Lmax=16):
    def fn():
        T = Lmax
        toks, tgts, msks = [], [], []
        for _ in range(B):
            L = int(rng.integers(1, Lmax + 1))
            tok, tgt = make_seq(task, T, rng)
            m = np.zeros(T); m[:L] = 1
            toks.append(tok); tgts.append(tgt); msks.append(m)
        return torch.tensor(np.array(toks)), torch.tensor(np.array(tgts)), torch.tensor(np.array(msks), dtype=torch.float32)
    return fn


BUCKETS = [(0, 16), (16, 32), (32, 64), (64, 128), (128, 256)]


def eval_model(pred_fn, task, rng, n=200, T=256):
    acc = np.zeros(T)
    for _ in range(n):
        tok, tgt = make_seq(task, T, rng)
        acc += (pred_fn(tok) == tgt)
    acc /= n
    return {f"{a+1}-{b}": float(acc[a:b].mean()) for a, b in BUCKETS}


def table_fold(task, rng):
    # estimate each token's action from short training sequences (lengths<=16), then compose exactly
    ncls = 120 if task == "s5" else 5
    counts = {}
    for _ in range(500):
        tok, tgt = make_seq(task, 16, rng)
        prev = PIDX[tuple(range(5))] if task == "s5" else 0
        for t, y in zip(tok, tgt):
            counts.setdefault((int(t), int(prev)), {}).setdefault(int(y), 0)
            counts[(int(t), int(prev))][int(y)] += 1
            prev = y
    # a "program": state-transition table learned from data; generalises if every (token,state) seen
    trans = {k: max(v, key=v.get) for k, v in counts.items()}
    def pred(tok):
        prev = PIDX[tuple(range(5))] if task == "s5" else 0
        out = []
        for t in tok:
            prev = trans.get((int(t), prev), prev); out.append(prev)
        return np.array(out)
    return pred


def job(args):
    task, model_kind, seed = args
    seed_all(seed); rng = np.random.default_rng(seed)
    ncls = 120 if task == "s5" else 5
    t0 = time.time()
    if model_kind == "table_fold":
        pred = table_fold(task, rng)
    else:
        if model_kind in ("gru", "lstm"):
            m = RNNSeq(5, ncls, d=128, kind=model_kind)
        else:
            pos = model_kind.split("_")[1]
            m = TransformerSeq(5, ncls, d=128, layers=3, heads=4, pos=pos, causal=True, max_len=300)
        train_loop(m, batch_fn_factory(task, rng), steps=4000 if task == "s5" else 2000, lr=1e-3)
        def pred(tok):
            with torch.no_grad():
                return m(torch.tensor(tok)[None])[0].argmax(-1).numpy()
    res = eval_model(pred, task, np.random.default_rng(seed + 1000))
    return dict(task=task, model=model_kind, seed=seed, acc=res, secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    kinds = ["gru", "lstm", "tf_rope", "tf_none", "tf_learned", "table_fold"]
    jobs = [(task, k, s) for task in ["z5", "s5"] for k in kinds for s in [1, 2, 3]]
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(job(("z5", "gru", 1))); print(job(("z5", "tf_rope", 1))); sys.exit()
    t0 = time.time()
    res = pool_run(job, jobs, procs=12)
    json.dump(res, open("e1_results.json", "w"), indent=1)
    print("done", round(time.time() - t0, 1))
