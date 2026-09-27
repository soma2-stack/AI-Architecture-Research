"""
Y.4 — functional symbol discovery (E2 follow-up; hypothesis-family discovery from raw observations).

Hidden world: K symbols x M styles -> K*M surface types. Each surface type has a random prototype in R^d
(appearance says nothing about which symbol or style it belongs to). Observations are noisy vectors.
Hidden relation on symbols: a random Latin square T (K x K -> K). Style propagates from the first argument.
   (x_a, x_b) -> x_c   with   sym(c) = T(sym(a), sym(b)),  sty(c) = sty(a)
Training shows only a fraction rho of the (surface_a, surface_b) pairs. Test: UNSEEN surface pairs,
20-way forced choice among one fresh candidate per surface type (chance 1/(K*M)).
To generalise, a learner must discover the two latent variables (symbol, style) of the surface alphabet
from relational behaviour alone.

Methods (same information):
  lookup      surface-level memorisation after perceptual clustering (floor)
  mlp_raw     end-to-end contrastive MLP on raw vectors (continuous learner, E2-like)
  emb_ids     contrastive embedding model on perceived surface IDs (tensor-factorisation-like; perception solved)
  search      perceptual clustering (k-means) + stochastic local search for a factorisation of the surfaces into a
              K x M grid that makes the relation functional (symbol part and style part), random restarts
              ("search within the right hypothesis family"; K and M given)
  oracle      true tables (upper bound)
Diagnostics separating failure types: perception (k-means purity); identification (do perfect-score
factorisations disagree on test predictions?); search (best found score vs the true factorisation's score);
optimisation (training loss/accuracy of neural models).
"""
import json, sys, time, itertools
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from common import seed_all, pool_run


def latin(rng, K):
    base = np.add.outer(np.arange(K), np.arange(K)) % K          # cyclic group table, randomly isotoped
    return rng.permutation(K)[base[rng.permutation(K)][:, rng.permutation(K)]]


def make_world(seed, K=5, M=4, d=16, rho=0.3, reps=10, sigma=0.3):
    rng = np.random.default_rng(seed)
    S = K * M
    proto = rng.normal(0, 1, (S, d)) * 3.0                        # random prototypes: appearance is uninformative
    T = latin(rng, K)
    sym = np.repeat(np.arange(K), M); sty = np.tile(np.arange(M), K)        # surface u -> (sym, sty)
    cell = {(sym[u], sty[u]): u for u in range(S)}
    out = lambda ua, ub: cell[(T[sym[ua], sym[ub]], sty[ua])]
    pairs = [(a, b) for a in range(S) for b in range(S)]
    # training pairs: fraction rho, but guarantee each symbol pair and each surface appears as first/second arg
    while True:
        m = rng.random(len(pairs)) < rho
        tr = [p for p, k in zip(pairs, m) if k]
        ok_sym = len({(sym[a], sym[b]) for a, b in tr}) == K * K
        ok_sur = len({a for a, b in tr}) == S and len({b for a, b in tr}) == S
        if ok_sym and ok_sur: break
    te = [p for p, k in zip(pairs, m) if not k]
    noise = lambda u, n: proto[u] + sigma * rng.normal(0, 1, (n, d))
    Xa, Xb, Xc, Ua, Ub, Uc = [], [], [], [], [], []
    for a, b in tr:
        c = out(a, b)
        Xa.append(noise(a, reps)); Xb.append(noise(b, reps)); Xc.append(noise(c, reps))
        Ua += [a] * reps; Ub += [b] * reps; Uc += [c] * reps
    W = dict(K=K, M=M, S=S, T=T, sym=sym, sty=sty, proto=proto, out=out, tr=tr, te=te, sigma=sigma, rng=rng, d=d)
    D = dict(Xa=np.concatenate(Xa).astype(np.float32), Xb=np.concatenate(Xb).astype(np.float32),
             Xc=np.concatenate(Xc).astype(np.float32), Ua=np.array(Ua), Ub=np.array(Ub), Uc=np.array(Uc))
    return W, D


def test_set(W, n_per=2):
    rng = np.random.default_rng(999)
    items = []
    for a, b in W["te"]:
        for _ in range(n_per):
            xa = W["proto"][a] + W["sigma"] * rng.normal(0, 1, W["d"])
            xb = W["proto"][b] + W["sigma"] * rng.normal(0, 1, W["d"])
            cands = W["proto"] + W["sigma"] * rng.normal(0, 1, (W["S"], W["d"]))   # one fresh candidate per surface
            items.append((xa.astype(np.float32), xb.astype(np.float32), cands.astype(np.float32), W["out"](a, b), a, b))
    return items


def score_choice(W, items, choose):
    ok, oks, okm = [], [], []
    for xa, xb, cands, c, a, b in items:
        j = choose(xa, xb, cands)
        ok.append(j == c); oks.append(W["sym"][j] == W["sym"][c]); okm.append(W["sty"][j] == W["sty"][c])
    return dict(acc=float(np.mean(ok)), sym_acc=float(np.mean(oks)), sty_acc=float(np.mean(okm)))


# ------------------------------------------------------------------------------------------------ perception
def kmeans(X, k, rng, iters=50, restarts=10):
    best = None
    for r in range(restarts):
        C = [X[rng.integers(len(X))]]
        for _ in range(k - 1):                       # k-means++ seeding
            d2 = ((X[:, None] - np.array(C)[None]) ** 2).sum(-1).min(1)
            C.append(X[rng.choice(len(X), p=d2 / d2.sum())])
        C = np.array(C)
        for _ in range(iters):
            a = ((X[:, None] - C[None]) ** 2).sum(-1).argmin(1)
            C = np.array([X[a == j].mean(0) if (a == j).any() else X[rng.integers(len(X))] for j in range(k)])
        inertia = ((X - C[a]) ** 2).sum()
        if best is None or inertia < best[0]: best = (inertia, C)
    return best[1]


def perceive(W, D):
    X = np.concatenate([D["Xa"], D["Xb"], D["Xc"]]); U = np.concatenate([D["Ua"], D["Ub"], D["Uc"]])
    C = kmeans(X, W["S"], W["rng"])
    lab = ((X[:, None] - C[None]) ** 2).sum(-1).argmin(1)
    # purity: each cluster dominated by one true surface
    pur = np.mean([np.bincount(U[lab == j]).max() / max(1, (lab == j).sum()) for j in range(W["S"]) if (lab == j).any()])
    assign = lambda x: int(((C - x) ** 2).sum(-1).argmin())
    n = len(D["Xa"])
    la, lb, lc = lab[:n], lab[n:2 * n], lab[2 * n:]
    rel = {}
    for a, b, c in zip(la, lb, lc):
        rel.setdefault((int(a), int(b)), {}).setdefault(int(c), 0); rel[(int(a), int(b))][int(c)] += 1
    rel = {k: max(v, key=v.get) for k, v in rel.items()}
    return C, assign, rel, float(pur)


# ------------------------------------------------------------------------------------------------ structured search
def fscore(cellpos, rel, K, M):
    """cellpos[u] = (k, m). Score = # relation entries consistent with a symbol function F(k_a,k_b)->k_c
    plus # consistent with a style function G(m_a,m_b)->m_c (majority per key)."""
    fs, gs = {}, {}
    for (a, b), c in rel.items():
        ka, ma = cellpos[a]; kb, mb = cellpos[b]; kc, mc = cellpos[c]
        fs.setdefault((ka, kb), {}).setdefault(kc, 0); fs[(ka, kb)][kc] += 1
        gs.setdefault((ma, mb), {}).setdefault(mc, 0); gs[(ma, mb)][mc] += 1
    sc = sum(max(v.values()) for v in fs.values()) + sum(max(v.values()) for v in gs.values())
    Fm = {k: max(v, key=v.get) for k, v in fs.items()}; Gm = {k: max(v, key=v.get) for k, v in gs.items()}
    return sc, Fm, Gm


def search_factorisation(rel, S, K, M, rng, restarts=40, iters=250, noise=0.1):
    sols = []
    for r in range(restarts):
        perm = rng.permutation(S)
        cellpos = {u: (int(perm[u]) // M, int(perm[u]) % M) for u in range(S)}
        sc, _, _ = fscore(cellpos, rel, K, M)
        for it in range(iters):
            u = int(rng.integers(S))
            if rng.random() < noise * (1 - it / iters):          # random swap (exploration, annealed)
                v = int(rng.integers(S))
                cellpos[u], cellpos[v] = cellpos[v], cellpos[u]
                sc, _, _ = fscore(cellpos, rel, K, M); continue
            best_v, best_sc = None, sc
            for v in range(S):
                if v == u: continue
                cellpos[u], cellpos[v] = cellpos[v], cellpos[u]
                s2, _, _ = fscore(cellpos, rel, K, M)
                if s2 > best_sc: best_v, best_sc = v, s2
                cellpos[u], cellpos[v] = cellpos[v], cellpos[u]
            if best_v is not None:
                cellpos[u], cellpos[best_v] = cellpos[best_v], cellpos[u]; sc = best_sc
        sc, Fm, Gm = fscore(cellpos, rel, K, M)
        sols.append((sc, dict(cellpos), Fm, Gm))
    return sols


def mdl_select(rel, S, rng, restarts=20):
    """Unknown K, M: try every factorisation K*M = S, fit by search, score by description length (bits):
    cell assignment + symbol table + style table + exceptions. Returns (K, M, best solution, table of bits)."""
    import math
    out = []
    for K in [k for k in range(1, S + 1) if S % k == 0]:
        M = S // K
        if K == 1 or M == 1:
            cellpos = {u: ((u, 0) if M == 1 else (0, u)) for u in range(S)}
            sols = [(fscore(cellpos, rel, K, M)[0], cellpos) + fscore(cellpos, rel, K, M)[1:]]
        else:
            sols = search_factorisation(rel, S, K, M, rng, restarts=restarts)
        best = max(sols, key=lambda z: z[0])
        exc = 2 * len(rel) - best[0]
        bits = S * math.log2(S) * (K > 1 and M > 1) + len(best[2]) * math.log2(max(K, 2)) +                len(best[3]) * math.log2(max(M, 2)) + exc * math.log2(S * S)
        out.append((bits, K, M, best))
    out.sort(key=lambda z: z[0])
    return out[0][1], out[0][2], out[0][3], [(round(b, 1), K, M) for b, K, M, _ in out]


def predictor_from(sol, K, M, rng):
    sc, cellpos, Fm, Gm = sol
    inv = {v: u for u, v in cellpos.items()}
    def pred(a, b):
        ka, ma = cellpos[a]; kb, mb = cellpos[b]
        k = Fm.get((ka, kb), int(rng.integers(K))); m = Gm.get((ma, mb), int(rng.integers(M)))
        return inv[(k, m)]
    return pred


# ------------------------------------------------------------------------------------------------ neural
class RawReg(nn.Module):
    """continuous end-to-end learner: (x_a, x_b) -> predicted x_c (MSE); choose nearest candidate."""
    def __init__(self, d, h=256):
        super().__init__()
        self.f = nn.Sequential(nn.Linear(2 * d, h), nn.GELU(), nn.Linear(h, h), nn.GELU(), nn.Linear(h, d))

    def forward(self, xa, xb):
        return self.f(torch.cat([xa, xb], -1))


class IdCls(nn.Module):
    """embedding model on surface IDs (perception solved): (id_a, id_b) -> distribution over output IDs."""
    def __init__(self, S, e=32, h=256):
        super().__init__()
        self.E = nn.Embedding(S, e)
        self.f = nn.Sequential(nn.Linear(2 * e, h), nn.GELU(), nn.Linear(h, h), nn.GELU(), nn.Linear(h, S))

    def forward(self, a, b):
        return self.f(torch.cat([self.E(a), self.E(b)], -1))


def train_nn(model, X, Y, loss_fn, steps=4000, bs=256, lr=1e-3, wd=1e-4):
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    n = len(Y)
    for s in range(steps):
        idx = torch.randint(0, n, (bs,))
        loss = loss_fn(model(*[x[idx] for x in X]), Y[idx])
        opt.zero_grad(); loss.backward(); opt.step()
    model.eval()
    return float(loss.detach())


def job(args):
    seed, rho = args
    seed_all(seed)
    W, D = make_world(seed, rho=rho)
    items = test_set(W)
    K, M, S = W["K"], W["M"], W["S"]
    res = dict(seed=seed, rho=rho, n_train_pairs=len(W["tr"]), n_test_pairs=len(W["te"]))
    t0 = time.time()
    # perception
    C, assign, rel, purity = perceive(W, D)
    res["perception_purity"] = purity
    # map clusters -> true surfaces (for evaluation only)
    cl2true = {j: int(((W["proto"] - C[j]) ** 2).sum(-1).argmin()) for j in range(S)}
    # lookup floor
    def ch_lookup(xa, xb, cands):
        k = rel.get((assign(xa), assign(xb)))
        if k is None: return int(W["rng"].integers(S))
        return int(((cands - C[k]) ** 2).sum(-1).argmin())
    res["lookup"] = score_choice(W, items, ch_lookup)
    # oracle
    res["oracle"] = score_choice(W, items, lambda xa, xb, cands: W["out"](int(((W["proto"] - xa) ** 2).sum(-1).argmin()),
                                                                              int(((W["proto"] - xb) ** 2).sum(-1).argmin())))
    # structured search on perceived relation
    rng = np.random.default_rng(seed + 7)
    sols = search_factorisation(rel, S, K, M, rng)
    maxscore = 2 * len(rel)
    best = max(s[0] for s in sols)
    perfect = [s for s in sols if s[0] == maxscore]
    # true factorisation score on the perceived relation
    true_cell = {j: (int(W["sym"][cl2true[j]]), int(W["sty"][cl2true[j]])) for j in range(S)}
    true_sc, _, _ = fscore(true_cell, rel, K, M)
    res["search_best_score_frac"] = best / maxscore
    res["true_score_frac"] = true_sc / maxscore
    res["n_restarts_perfect"] = len(perfect)
    bestsol = max(sols, key=lambda s: s[0])
    pred = predictor_from(bestsol, K, M, rng)
    def ch_search(xa, xb, cands):
        k = pred(assign(xa), assign(xb))
        return int(((cands - C[k]) ** 2).sum(-1).argmin())
    res["search"] = score_choice(W, items, ch_search)
    # search with UNKNOWN K and M (family size chosen by MDL)
    Km, Mm, solm, table = mdl_select(rel, S, np.random.default_rng(seed + 13))
    res["mdl_choice"] = [Km, Mm]; res["mdl_table"] = table
    pm = predictor_from(solm, Km, Mm, rng)
    res["search_mdl"] = score_choice(W, items, lambda xa, xb, cands: int(((cands - C[pm(assign(xa), assign(xb))]) ** 2).sum(-1).argmin()))
    # identification: do perfect-score solutions disagree on test predictions?
    if len(perfect) >= 2:
        te_keys = sorted({(assign(xa), assign(xb)) for xa, xb, _, _, _, _ in items})
        preds = [tuple(predictor_from(p, K, M, np.random.default_rng(1))(a, b) for a, b in te_keys) for p in perfect]
        res["perfect_solutions_distinct_test_predictions"] = len(set(preds))
    # neural: raw vectors (regression)
    A, B, Cc = (torch.tensor(D[k]) for k in ("Xa", "Xb", "Xc"))
    torch.manual_seed(seed)
    m_raw = RawReg(W["d"])
    res["mlp_raw_train_mse"] = train_nn(m_raw, (A, B), Cc, F.mse_loss)
    def ch_raw(xa, xb, cands):
        with torch.no_grad():
            y = m_raw(torch.tensor(xa)[None], torch.tensor(xb)[None])[0].numpy()
        return int(((cands - y) ** 2).sum(-1).argmin())
    res["mlp_raw"] = score_choice(W, items, ch_raw)
    # neural: perceived IDs and true IDs (classification)
    for tag, idmap in [("emb_ids", lambda X, U: torch.tensor([assign(x) for x in X])),
                       ("emb_true_ids", lambda X, U: torch.tensor(U))]:
        Ai, Bi, Ci = idmap(D["Xa"], D["Ua"]), idmap(D["Xb"], D["Ub"]), idmap(D["Xc"], D["Uc"])
        torch.manual_seed(seed)
        m_id = IdCls(S)
        res[tag + "_train_loss"] = train_nn(m_id, (Ai, Bi), Ci, F.cross_entropy)
        true_mode = tag == "emb_true_ids"
        def ch_id(xa, xb, cands, m_id=m_id, true_mode=true_mode):
            if true_mode:
                a = int(((W["proto"] - xa) ** 2).sum(-1).argmin()); b = int(((W["proto"] - xb) ** 2).sum(-1).argmin())
                cid = [int(((W["proto"] - c) ** 2).sum(-1).argmin()) for c in cands]
            else:
                a, b = assign(xa), assign(xb); cid = [assign(c) for c in cands]
            with torch.no_grad():
                p = m_id(torch.tensor([a]), torch.tensor([b]))[0]
            return int(np.argmax([float(p[c]) for c in cid]))
        res[tag] = score_choice(W, items, ch_id)
    # identification check with perception solved exactly: search on the TRUE surface relation
    true_rel = {(a, b): W["out"](a, b) for a, b in W["tr"]}
    sols_t = search_factorisation(true_rel, S, K, M, np.random.default_rng(seed + 11))
    perf_t = [s_ for s_ in sols_t if s_[0] == 2 * len(true_rel)]
    res["truerel_search_best_frac"] = max(s_[0] for s_ in sols_t) / (2 * len(true_rel))
    res["truerel_n_perfect"] = len(perf_t)
    if perf_t:
        te_pairs = W["te"]
        preds = [tuple(predictor_from(p_, K, M, np.random.default_rng(1))(a, b) for a, b in te_pairs) for p_ in perf_t]
        res["truerel_distinct_perfect_predictions"] = len(set(preds))
        best_t = perf_t[0]
        pt = predictor_from(best_t, K, M, np.random.default_rng(2))
        res["truerel_search_test_acc"] = float(np.mean([pt(a, b) == W["out"](a, b) for a, b in te_pairs]))
    res["secs"] = round(time.time() - t0, 1)
    return res


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        r = job((1, 0.3)); print(json.dumps(r, indent=1, default=float)); sys.exit()
    jobs = [(s, rho) for s in range(1, 6) for rho in [0.1, 0.2, 0.35, 0.6, 0.85]]
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 10)
    json.dump(res, open("y4_results.json", "w"), indent=1, default=float)
    print("done")
