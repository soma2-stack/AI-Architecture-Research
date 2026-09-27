"""
E3 — keeping latent regimes separate as new regimes appear (averaging vs separation).
Stream: x_t in {0,1}^8 uniform; regime r has rule y = x[k_r] XOR s_r (16 possible rules).
Regimes are introduced one by one; after introduction, segments (length U[40,80]) sample uniformly among
the regimes introduced so far. Learner predicts y_t from (history, x_t), then sees y_t.
Metrics: error in the first 10 steps of a segment whose regime was SEEN BEFORE (re-identification),
grouped by the number of regimes introduced so far; and steady-state error (steps >= 20 of a segment).
Learners: online logistic (single model), online MLP, kNN over a recent window, a classical expert library
(pool of online logistic experts, best-recent-likelihood selection, spawn on persistent misfit),
and meta-trained in-context learners (GRU, causal Transformer over a 128-step window) trained on streams
with R_train in {1,2} or R_train in {1..5} regimes; tested on streams with 3..8 regimes.
"""
import json, sys, time, math
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from common import seed_all, pool_run, TransformerSeq

D = 8


def make_stream(rng, R, T, intro=None, seg=(40, 80), distinct=True):
    rules = []
    while len(rules) < R:
        k, s = int(rng.integers(D)), int(rng.integers(2))
        if not distinct or all(k != q[0] for q in rules):   # distinct relevant bits -> regimes conflict
            rules.append((k, s))
    if intro is None:
        intro = [0] + sorted(rng.choice(np.arange(1, T // 150), R - 1, replace=False) * 150 // 1) if R > 1 else [0]
        intro = [int(v) for v in intro]
    X = rng.integers(0, 2, (T, D)); Y = np.zeros(T, int); reg = np.zeros(T, int); segstart = np.zeros(T, int)
    t, n_intro = 0, 0
    while t < T:
        avail = [r for r in range(R) if intro[r] <= t]
        new = [r for r in avail if r >= n_intro]
        if new:
            r = new[0]; n_intro = r + 1
        else:
            r = int(rng.choice(avail))
        L = int(rng.integers(seg[0], seg[1] + 1))
        for u in range(t, min(T, t + L)):
            reg[u] = r; segstart[u] = t
        t += L
    for u in range(T):
        k, s = rules[reg[u]]; Y[u] = X[u, k] ^ s
    return X, Y, reg, segstart, intro


def score(pred_err, reg, segstart, intro):
    """pred_err[t] in {0,1}. Returns dict: first10 error on revisited regimes by #introduced; steady error."""
    T = len(reg); out = {}
    seen_before = set(); cur_seg = -1
    firsts, changed_firsts = {}, {}
    steady = []
    for t in range(T):
        if segstart[t] != cur_seg:
            prev_reg = reg[t - 1] if t > 0 else -1
            cur_seg = segstart[t]; revisit = reg[t] in seen_before; seen_before.add(reg[t])
            changed = reg[t] != prev_reg
            nintro = sum(1 for v in intro if v <= t)
        pos = t - segstart[t]
        if revisit and pos < 10:
            firsts.setdefault(nintro, []).append(pred_err[t])
        if revisit and changed and pos < 10:
            changed_firsts.setdefault(nintro, []).append(pred_err[t])
        if pos >= 20:
            steady.append(pred_err[t])
    return {"first10_by_nregimes": {k: float(np.mean(v)) for k, v in sorted(firsts.items())},
            "first10_all": float(np.mean([e for v in firsts.values() for e in v])) if firsts else None,
            "steady": float(np.mean(steady)),
            "changed_first10_by_nregimes": {k: float(np.mean(v)) for k, v in sorted(changed_firsts.items())},
            "changed_first10_all": float(np.mean([e for v in changed_firsts.values() for e in v])) if changed_firsts else None}


# ------------------------------------------------------------------------------------- online learners
def run_online(X, Y, kind, rng):
    T = len(Y); err = np.zeros(T)
    if kind == "logistic":
        w = np.zeros(D + 1); lr = 0.5
        for t in range(T):
            f = np.append(2 * X[t] - 1, 1.0); p = 1 / (1 + np.exp(-w @ f))
            err[t] = (p > 0.5) != Y[t]; w += lr * (Y[t] - p) * f
    elif kind == "mlp":
        torch.manual_seed(int(rng.integers(1e6)))
        m = nn.Sequential(nn.Linear(D, 64), nn.Tanh(), nn.Linear(64, 1)); opt = torch.optim.SGD(m.parameters(), lr=0.1)
        for t in range(T):
            xt = torch.tensor(2 * X[t] - 1, dtype=torch.float32)[None]
            lg = m(xt)[0, 0]; err[t] = float((lg > 0) != Y[t])
            loss = F.binary_cross_entropy_with_logits(lg, torch.tensor(float(Y[t])))
            opt.zero_grad(); loss.backward(); opt.step()
    elif kind == "knn":
        W = 50
        for t in range(T):
            lo = max(0, t - W); Xs, Ys = X[lo:t], Y[lo:t]
            if len(Ys) == 0: err[t] = 0.5; continue
            d = np.abs(Xs - X[t]).sum(1); m = d.min(); votes = Ys[d == m]
            err[t] = (votes.mean() > 0.5) != Y[t]
    elif kind == "library":
        experts = [np.zeros(D + 1)]; hist = [[]]; active = 0; miss = []
        for t in range(T):
            f = np.append(2 * X[t] - 1, 1.0)
            ps = [1 / (1 + np.exp(-w @ f)) for w in experts]
            # select expert with best log-likelihood over the last 6 steps (fallback: active)
            if t >= 1:
                scores = [sum(h[-6:]) for h in hist]
                active = int(np.argmax(scores))
            p = ps[active]; err[t] = (p > 0.5) != Y[t]
            for i, pi in enumerate(ps):
                hist[i].append(math.log(max(1e-6, pi if Y[t] else 1 - pi)))
            miss.append(err[t])
            experts[active] = experts[active] + 0.5 * (Y[t] - p) * f
            # spawn if the best expert has missed >= 4 of the last 6 and no expert fits recent data
            if t > 10 and sum(miss[-6:]) >= 4 and max(sum(h[-6:]) for h in hist) < 6 * math.log(0.6):
                experts.append(np.zeros(D + 1)); hist.append([0.0] * (t + 1)); miss = []
    elif kind in ("bayes", "bayes_mem"):
        H = [(k, sgn) for k in range(D) for sgn in range(2)]
        lw = np.full(len(H), -math.log(len(H))); alpha = 1 / 60; eps = 0.01
        seen = np.zeros(len(H)); streak = np.zeros(len(H))
        for t in range(T):
            w = np.exp(lw - lw.max()); w /= w.sum()
            preds = np.array([X[t, k] ^ sg for k, sg in H])
            p1 = float(w @ preds); err[t] = (p1 > 0.5) != Y[t]
            lik = np.where(preds == Y[t], 1 - eps, eps)
            w = w * lik; w /= w.sum()
            top = int(np.argmax(w)); streak = np.where(np.arange(len(H)) == top, streak + 1, 0)
            if streak[top] >= 10: seen[top] = 1
            if kind == "bayes_mem" and seen.sum() > 0:
                share = 0.9 * seen / seen.sum() + 0.1 / len(H)
            else:
                share = np.full(len(H), 1 / len(H))
            w = (1 - alpha) * w + alpha * share
            lw = np.log(w)
    return err


# ------------------------------------------------------------------------------- meta-trained learners
class GRUIC(nn.Module):
    def __init__(self, d=128):
        super().__init__()
        self.inp = nn.Linear(D + 2, d); self.rnn = nn.GRU(d, d, batch_first=True); self.out = nn.Linear(d, 1)

    def forward(self, Xp):
        h, _ = self.rnn(self.inp(Xp)); return self.out(h)[..., 0]


class TFIC(nn.Module):
    def __init__(self, d=96, W=128):
        super().__init__()
        self.inp = nn.Linear(D + 2, d)
        self.tf = TransformerSeq(1, 1, d=d, layers=3, heads=4, pos="rope", causal=True)
        self.W = W

    def forward(self, Xp):
        x = self.inp(Xp)
        T = x.shape[1]
        i = torch.arange(T)
        mask = (i[None, :] <= i[:, None]) & (i[None, :] > i[:, None] - self.W)
        for b in self.tf.blocks:
            x = b(x, mask[None, None])
        return self.tf.out(self.tf.ln(x))[..., 0]


def encode(X, Y):
    # input at t: x_t (+-1) , y_{t-1} one-hot (2 dims; zeros at t=0)
    T = len(Y); prev = np.zeros((T, 2)); prev[1:, 0] = Y[:-1] == 0; prev[1:, 1] = Y[:-1] == 1
    return np.concatenate([2 * X - 1, prev], 1).astype(np.float32)


def meta_train(kind, Rmax, rng, steps, T=600, B=16):
    m = GRUIC() if kind == "gru" else TFIC()
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3)
    for s in range(steps):
        Xs, Ys = [], []
        for _ in range(B):
            R = int(rng.integers(1, Rmax + 1))
            intro = [0] + [int(v) for v in sorted(rng.choice(np.arange(1, T // 60), R - 1, replace=False) * 60)] if R > 1 else [0]
            X, Y, _, _, _ = make_stream(rng, R, T, intro=intro)
            Xs.append(encode(X, Y)); Ys.append(Y)
        xb = torch.tensor(np.array(Xs)); yb = torch.tensor(np.array(Ys), dtype=torch.float32)
        loss = F.binary_cross_entropy_with_logits(m(xb), yb)
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
    m.eval(); return m


def run_meta(m, X, Y):
    with torch.no_grad():
        lg = m(torch.tensor(encode(X, Y))[None])[0].numpy()
    return ((lg > 0) != Y).astype(float)


TEST_R = [3, 5, 8]


def test_streams(seed):
    rng = np.random.default_rng(seed + 777); out = []
    for R in TEST_R:
        for rep in range(4):
            T = 300 * R + 600
            intro = [0] + [300 * i for i in range(1, R)]
            out.append((R, make_stream(rng, R, T, intro=intro)))
    return out


def job(args):
    kind, seed, extra = args
    seed_all(seed); rng = np.random.default_rng(seed)
    t0 = time.time()
    if kind.startswith("meta"):
        _, arch, Rmax = kind.split("_"); m = meta_train(arch, int(Rmax), rng, steps=extra)
    res = {}
    for R, (X, Y, reg, segstart, intro) in test_streams(seed):
        err = run_meta(m, X, Y) if kind.startswith("meta") else run_online(X, Y, kind, rng)
        sc = score(err, reg, segstart, intro)
        res.setdefault(R, []).append(sc)
    agg = {R: dict(first10=float(np.mean([s["first10_all"] for s in v])), steady=float(np.mean([s["steady"] for s in v])),
                   changed_first10=float(np.mean([s["changed_first10_all"] for s in v])),
                   changed_by_n={str(k): float(np.nanmean([s["changed_first10_by_nregimes"].get(k, np.nan) for s in v]))
                                 for k in range(2, R + 1)},
                   first10_by_n={str(k): float(np.mean([s["first10_by_nregimes"].get(k, np.nan) for s in v]))
                                 for k in range(2, R + 1)}) for R, v in res.items()}
    return dict(kind=kind, seed=seed, res=agg, secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        for k in ["bayes", "bayes_mem"]:
            print(job((k, 1, 0)))
        sys.exit()
    jobs = [(k, s, 0) for k in ["logistic", "mlp", "knn", "library", "bayes", "bayes_mem"] for s in [1, 2, 3]]
    jobs += [(f"meta_{a}_{r}", s, 3000) for a in ["gru", "tf"] for r in [2, 5] for s in [1, 2, 3]]
    if len(sys.argv) > 2 and sys.argv[2] == "b":        # E3b: corrected metric; GRU meta-learners incl. longer training
        jobs = [(k, s, 0) for k in ["logistic", "mlp", "knn", "library", "bayes", "bayes_mem"] for s in [1, 2, 3]]
        jobs += [(f"meta_gru_{r}", s, st) for r in [2, 5] for s in [1, 2, 3] for st in [3000, 9000]]
    t0 = time.time()
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 10)
    json.dump(res, open("e3b_results.json" if (len(sys.argv) > 2 and sys.argv[2] == "b") else "e3_results.json", "w"), indent=1)
    print("done", round(time.time() - t0, 1))
