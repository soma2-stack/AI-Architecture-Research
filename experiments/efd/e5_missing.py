"""
E5 — knowing what information is missing before answering.
Facts over variables v0..v15 (mod-10 arithmetic): "v_i = c" and "v_i = v_j + d". Query "v_q = ?".
Answer: the value (0..9) if determined by the facts, else UNKNOWN (class 10).
Facts form random acyclic constraint forests; a component is determined iff it contains a constant fact.
Train: <= 6 variables, query hop-distance to the constant <= 2. Test: up to 14 variables, hop distance 1..7.
Balanced determined / undetermined. Learners: Transformer encoder over fact tokens (set-structured: per-fact
position only), GRU over the serialised facts, classical union-find with offsets.
"""
import json, sys, time
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from common import seed_all, pool_run, Block

NV = 16
# tokens: vars 0..15, digits 16..25, EQC 26, EQV 27, QRY 28, PAD 29
DIG, EQC, EQV, QRY, PAD, VOC = 16, 26, 27, 28, 29, 30
UNK = 10
import os
NO_OFFSET = os.environ.get("E5B") == "1"          # E5b: facts are pure equalities v_i = v_j (no arithmetic), isolating multi-hop determinacy


def gen(rng, nvar, hop, determined):
    """Build a chain from the query variable of length `hop` to a constant (if determined) plus distractor
    components; returns facts list, query var, answer, true hop."""
    vars_ = list(rng.permutation(NV)[:nvar])
    q = vars_[0]
    chain = vars_[:hop + 1] if hop + 1 <= nvar else vars_
    facts, val = [], {}
    # chain: v_chain[k] = v_chain[k+1] + d
    for k in range(len(chain) - 1):
        facts.append(("v", chain[k], chain[k + 1], 0 if NO_OFFSET else int(rng.integers(10))))
    last = chain[-1]
    rest = [v for v in vars_ if v not in chain]
    if determined:
        facts.append(("c", last, int(rng.integers(10))))
    # distractors: other variables in separate components; some determined, some not
    while rest:
        size = int(rng.integers(1, min(3, len(rest)) + 1))
        comp, rest = rest[:size], rest[size:]
        for k in range(len(comp) - 1):
            facts.append(("v", comp[k], comp[k + 1], 0 if NO_OFFSET else int(rng.integers(10))))
        if rng.random() < 0.6:
            facts.append(("c", comp[-1], int(rng.integers(10))))
    # distractor attached to the chain but not providing a constant path (side branches without constants)
    order = rng.permutation(len(facts))
    facts = [facts[i] for i in order]
    return facts, q, solve(facts, q)


def solve(facts, q):
    # union-find with offsets: value(v) = value(root) + off(v)
    parent, off = {}, {}
    def find(v):
        if parent.setdefault(v, v) == v:
            off.setdefault(v, 0); return v, 0
        r, o = find(parent[v]); parent[v] = r; off[v] = (off[v] + o) % 10
        return r, off[v]
    const = {}
    for f in facts:
        if f[0] == "v":
            _, a, b, d = f          # a = b + d
            ra, oa = find(a); rb, ob = find(b)
            if ra != rb:
                parent[ra] = rb; off[ra] = (ob + d - oa) % 10
    for f in facts:
        if f[0] == "c":
            r, o = find(f[1]); const[r] = (f[2] - o) % 10
    r, o = find(q)
    return (const[r] + o) % 10 if r in const else UNK


def encode(facts, q):
    toks, fpos = [], []
    for f in facts:
        if f[0] == "c":
            t = [f[1], EQC, DIG + f[2], PAD]
        else:
            t = [f[1], EQV, f[2], DIG + f[3]]
        toks += t; fpos += [0, 1, 2, 3]
    toks += [QRY, q, PAD, PAD]; fpos += [0, 1, 2, 3]
    return toks, fpos


def make_batch(rng, B, nvar_rng, hop_rng):
    T_, P_, Y_ = [], [], []
    for _ in range(B):
        nvar = int(rng.integers(nvar_rng[0], nvar_rng[1] + 1))
        hop = int(rng.integers(hop_rng[0], min(hop_rng[1], nvar - 1) + 1))
        det = rng.random() < 0.5
        facts, q, ans = gen(rng, nvar, hop, det)
        t, p = encode(facts, q); T_.append(t); P_.append(p); Y_.append(ans)
    L = max(len(t) for t in T_)
    T_ = [t + [PAD] * (L - len(t)) for t in T_]; P_ = [p + [0] * (L - len(p)) for p in P_]
    return torch.tensor(T_), torch.tensor(P_), torch.tensor(Y_)


class TF(nn.Module):
    def __init__(self, d=128, layers=6):
        super().__init__()
        self.emb = nn.Embedding(VOC, d); self.fp = nn.Embedding(4, d)
        self.blocks = nn.ModuleList([Block(d, 4, "none", causal=False) for _ in range(layers)])
        self.ln = nn.LayerNorm(d); self.out = nn.Linear(d, 11)

    def forward(self, tok, fpos):
        x = self.emb(tok) + self.fp(fpos)
        m = (tok != PAD)
        mask = m[:, None, None, :].expand(-1, 1, tok.shape[1], -1)
        for b in self.blocks:
            x = b(x, mask)
        qpos = (tok == QRY).float().argmax(1)
        return self.out(self.ln(x[torch.arange(len(tok)), qpos + 1]))


class GRUm(nn.Module):
    def __init__(self, d=256):
        super().__init__()
        self.emb = nn.Embedding(VOC, d); self.rnn = nn.GRU(d, d, num_layers=2, batch_first=True); self.out = nn.Linear(d, 11)

    def forward(self, tok, fpos):
        h, _ = self.rnn(self.emb(tok))
        qpos = (tok == QRY).float().argmax(1)
        return self.out(h[torch.arange(len(tok)), qpos + 1])


def evaluate(pred_fn, seed):
    rng = np.random.default_rng(seed + 55); res = {}
    for hop in (1, 2):               # in-distribution: 3..6 variables
        for det in [True, False]:
            ok = []
            for _ in range(150):
                nvar = int(rng.integers(max(hop + 1, 3), 7))
                facts, q, ans = gen(rng, nvar, hop, det)
                ok.append(pred_fn(facts, q) == ans)
            res[f"ID_hop{hop}_{'det' if det else 'undet'}"] = float(np.mean(ok))
    for hop in range(1, 8):
        for det in [True, False]:
            ok = []
            for _ in range(150):
                nvar = int(rng.integers(max(hop + 1, 6), 15))
                facts, q, ans = gen(rng, nvar, hop, det)
                ok.append(pred_fn(facts, q) == ans)
            res[f"hop{hop}_{'det' if det else 'undet'}"] = float(np.mean(ok))
    return res


def job(args):
    kind, seed, steps = args
    seed_all(seed); rng = np.random.default_rng(seed); t0 = time.time()
    if kind == "unionfind":
        return dict(kind=kind, seed=seed, acc=evaluate(lambda f, q: solve(f, q), seed))
    m = TF() if kind == "tf" else GRUm()
    opt = torch.optim.AdamW(m.parameters(), lr=5e-4, weight_decay=0.01)
    sch = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1, (s + 1) / 300) * max(0.05, 1 - s / steps))
    for s in range(steps):
        tok, fp, y = make_batch(rng, 64, (3, 6), (1, 2))
        loss = F.cross_entropy(m(tok, fp), y)
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step(); sch.step()
    m.eval()
    def pred(facts, q):
        t, p = encode(facts, q)
        with torch.no_grad():
            return int(m(torch.tensor([t]), torch.tensor([p])).argmax(-1))
    return dict(kind=kind, seed=seed, steps=steps, acc=evaluate(pred, seed), secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(job(("unionfind", 1, 0))); print(job(("tf", 1, 200))); sys.exit()
    jobs = [("unionfind", 1, 0)] + [(k, s, 6000) for k in ["tf", "gru"] for s in [1, 2, 3]]
    out = "e5_results.json"
    if len(sys.argv) > 2 and sys.argv[2] == "b":
        jobs = [("unionfind", 1, 0)] + [(k, s, 12000) for k in ["tf", "gru"] for s in [1, 2]]
        out = "e5b_results.json"
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 7)
    json.dump(res, open(out, "w"), indent=1)
    print("done")
