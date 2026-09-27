"""
E2 — reuse of a learned rule after a surface (symbol) change.
Rule T: a 13x13 table (Z13 addition, or a random Latin square). Phase A: learn T on tokens 0..12 (all 169 pairs).
Phase B: new tokens 13..25; token 13+i denotes element pi(i) for an unknown bijection pi. Given n_B examples of T
written in the B encoding, predict the held-out B pairs.
Methods: scratch (B examples only), FT-all, FT-embed (body frozen, learn B embeddings/unembeddings),
FT-embed-tied (B symbol has one embedding used for input and output), each for an MLP body and a Transformer body;
exact-match memory; classical constraint search over pi (majority vote over all consistent pi).
"""
import json, sys, time, itertools
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from common import seed_all, pool_run

P = 13


def latin_square(rng, n=P):
    # row-by-row with random perfect matchings (Hall guarantees extension of a Latin rectangle)
    L = np.full((n, n), -1)
    for r in range(n):
        while True:
            avail = [set(range(n)) - set(L[:r, c]) for c in range(n)]
            match = {}                     # symbol -> column
            cols = list(rng.permutation(n))
            ok = True
            for c in cols:
                seen = set()
                def aug(c):
                    for s in rng.permutation(list(avail[c])):
                        s = int(s)
                        if s in seen: continue
                        seen.add(s)
                        if s not in match or aug(match[s]):
                            match[s] = c; return True
                    return False
                if not aug(c):
                    ok = False; break
            if ok: break
        for s, c in match.items():
            L[r, c] = s
    return L


def make_table(kind, rng):
    if kind == "add":
        return np.add.outer(np.arange(P), np.arange(P)) % P
    return latin_square(rng)


class Net(nn.Module):
    """Two-token input -> logits over 26 symbols. body in {mlp, tf}. tied: logits = f(h) . E^T."""
    def __init__(self, body="mlp", d=64, h=256, tied=False):
        super().__init__()
        self.E = nn.Embedding(2 * P, d)
        self.body, self.tied = body, tied
        if body == "mlp":
            self.f = nn.Sequential(nn.Linear(2 * d, h), nn.GELU(), nn.Linear(h, h), nn.GELU(), nn.Linear(h, d))
        else:
            self.pos = nn.Parameter(torch.randn(3, d) * 0.1)
            layer = nn.TransformerEncoderLayer(d, 4, 4 * d, dropout=0.0, batch_first=True, norm_first=True)
            self.tf = nn.TransformerEncoder(layer, 2)
            self.sep = nn.Parameter(torch.randn(d) * 0.1)
            self.f = nn.Linear(d, d)
        self.U = None if tied else nn.Linear(d, 2 * P, bias=False)

    def forward(self, a, b):
        return self.forward_with(a, b, self.E.weight, None if self.tied else self.U.weight)

    def forward_with(self, a, b, Ew, Uw):
        ea, eb = Ew[a], Ew[b]
        if self.body == "mlp":
            z = self.f(torch.cat([ea, eb], -1))
        else:
            x = torch.stack([ea, eb, self.sep.expand_as(ea)], 1) + self.pos[None]
            z = self.f(self.tf(x)[:, 2])
        return z @ Ew.T if self.tied else z @ Uw.T


def fit(net, a, b, c, steps, lr, params, out_lo, out_hi):
    opt = torch.optim.Adam(params, lr=lr)
    for _ in range(steps):
        lg = net(a, b)[:, out_lo:out_hi]
        loss = F.cross_entropy(lg, c - out_lo)
        opt.zero_grad(); loss.backward(); opt.step()
    return float(loss.detach())


def sinkhorn(logits, iters=20):
    for _ in range(iters):
        logits = logits - torch.logsumexp(logits, 1, keepdim=True)
        logits = logits - torch.logsumexp(logits, 0, keepdim=True)
    return logits.exp()


def fit_assign(net, ta, tb, tc, ea, eb, ec, mode, steps=1500, lr=0.05):
    """B embeddings (and unembeddings) are soft assignments over the frozen A rows: EB = M EA, UB = M UA."""
    from scipy.optimize import linear_sum_assignment
    for q in net.parameters(): q.requires_grad_(False)
    EA = net.E.weight[:P].detach(); UA = None if net.tied else net.U.weight[:P].detach()
    S = torch.zeros(P, P, requires_grad=True)
    with torch.no_grad(): S += 0.01 * torch.randn(P, P)
    opt = torch.optim.Adam([S], lr=lr)
    def mats(M):
        Ew = torch.cat([EA, M @ EA]); Uw = None if net.tied else torch.cat([UA, M @ UA])
        return Ew, Uw
    for step in range(steps):
        tau = max(0.05, 1.0 * (0.05 ** (step / steps)))
        M = torch.softmax(S / tau, 1) if mode == "soft" else sinkhorn(S / tau)
        Ew, Uw = mats(M)
        loss = F.cross_entropy(net.forward_with(ta, tb, Ew, Uw)[:, P:], tc - P)
        opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad():
        r, c = linear_sum_assignment(-S.numpy())
        Mh = torch.zeros(P, P); Mh[r, c] = 1.0
        Ew, Uw = mats(Mh)
        acc_hard = float((net.forward_with(ea, eb, Ew, Uw)[:, P:].argmax(-1).numpy() == ec).mean())
        trl = float(F.cross_entropy(net.forward_with(ta, tb, Ew, Uw)[:, P:], tc - P))
    return acc_hard, trl, c


def csp_predict(T, ex, test_pairs, cap=20000):
    # variables: pi(i) for B symbols i in 0..12 ; constraint T[pi(a), pi(b)] = pi(c)
    sols = []
    assign = [-1] * P; used = [False] * P
    order = sorted(range(P), key=lambda i: -sum((i in e) for e in ex))
    def consistent():
        for (x, y, z) in ex:
            px, py, pz = assign[x], assign[y], assign[z]
            if px >= 0 and py >= 0:
                t = T[px, py]
                if pz >= 0 and pz != t: return False
                if pz < 0 and used[t]:
                    # t already taken by another symbol -> z must map to t, impossible
                    return False
        return True
    def rec(k):
        if len(sols) >= cap: return
        if k == P:
            sols.append(list(assign)); return
        i = order[k]
        for v in range(P):
            if used[v]: continue
            assign[i] = v; used[v] = True
            if consistent(): rec(k + 1)
            assign[i] = -1; used[v] = False
    rec(0)
    preds = []
    for (x, y) in test_pairs:
        votes = {}
        for s in sols:
            inv = {v: i for i, v in enumerate(s)}
            z = inv[T[s[x], s[y]]]; votes[z] = votes.get(z, 0) + 1
        preds.append(max(votes, key=votes.get) if votes else -1)
    return np.array(preds), len(sols)


def job(args):
    kind, seed, nBs = args
    seed_all(seed); rng = np.random.default_rng(seed)
    T = make_table(kind, rng)
    pi = rng.permutation(P)                      # B token i means element pi[i]
    inv = np.argsort(pi)
    pairs = [(x, y) for x in range(P) for y in range(P)]
    # B-encoded truth: token x,y -> token inv[T[pi[x], pi[y]]]
    truthB = {(x, y): int(inv[T[pi[x], pi[y]]]) for (x, y) in pairs}
    A_a = torch.tensor([x for x, y in pairs]); A_b = torch.tensor([y for x, y in pairs])
    A_c = torch.tensor([int(T[x, y]) for x, y in pairs])
    out = []
    # pretrain the four bodies on A
    pre = {}
    for body in ["mlp", "tf"]:
        for tied in [False, True]:
            seed_all(seed * 10 + (body == "tf") * 2 + tied)
            net = Net(body, tied=tied)
            loss = fit(net, A_a, A_b, A_c, 3000 if body == "mlp" else 4000, 3e-3, net.parameters(), 0, P)
            with torch.no_grad():
                accA = float((net(A_a, A_b)[:, :P].argmax(-1) == A_c).float().mean())
            pre[(body, tied)] = (net.state_dict(), accA)
    for nB in nBs:
        order = rng.permutation(len(pairs))
        tr = [pairs[i] for i in order[:nB]]; te = [pairs[i] for i in order[nB:]]
        ta = torch.tensor([x + P for x, y in tr]); tb = torch.tensor([y + P for x, y in tr])
        tc = torch.tensor([truthB[(x, y)] + P for x, y in tr])
        ea = torch.tensor([x + P for x, y in te]); eb = torch.tensor([y + P for x, y in te])
        ec = np.array([truthB[(x, y)] for x, y in te])
        # exact-match memory
        out.append(dict(kind=kind, seed=seed, nB=nB, method="memory", acc=0.0))
        # CSP
        ex = [(x, y, truthB[(x, y)]) for x, y in tr]
        t0 = time.time()
        pr, nsol = csp_predict(T, ex, te)
        out.append(dict(kind=kind, seed=seed, nB=nB, method="csp", acc=float((pr == ec).mean()), nsol=nsol,
                        secs=round(time.time() - t0, 2)))
        for body in ["mlp", "tf"]:
            for mode in ["assign_soft", "assign_sinkhorn"]:
                accs, losses, correct_bind = [], [], []
                for restart in range(3):
                    seed_all(seed * 1000 + nB * 7 + restart + 50)
                    net = Net(body, tied=False); net.load_state_dict(pre[(body, False)][0])
                    acc, L, col = fit_assign(net, ta, tb, tc, ea, eb, ec, "soft" if mode == "assign_soft" else "sink")
                    accs.append(acc); losses.append(L); correct_bind.append(float((col == pi).mean()))
                best = int(np.argmin(losses))
                out.append(dict(kind=kind, seed=seed, nB=nB, method=f"{body}_{mode}", acc=accs[best],
                                acc_mean=float(np.mean(accs)), train_loss=losses[best], bind_correct=correct_bind[best]))
            for mode in ["scratch", "ft_all", "ft_embed", "ft_embed_tied"]:
                tied = mode == "ft_embed_tied"
                accs, losses, diag = [], [], []
                for restart in range(3):
                    seed_all(seed * 1000 + nB * 7 + restart)
                    net = Net(body, tied=tied)
                    if mode != "scratch":
                        net.load_state_dict(pre[(body, tied)][0])
                        with torch.no_grad():   # fresh random B embeddings
                            net.E.weight[P:] = torch.randn(P, net.E.weight.shape[1]) * net.E.weight[:P].std()
                    if mode in ("ft_embed", "ft_embed_tied"):
                        for q in net.parameters(): q.requires_grad_(False)
                        net.E.weight.requires_grad_(True)
                        params = [net.E.weight]
                        if not tied:
                            net.U.weight.requires_grad_(True); params.append(net.U.weight)
                        # gradients only matter for B rows (A rows unused in phase B)
                    else:
                        params = list(net.parameters())
                    L = fit(net, ta, tb, tc, 1500, 3e-3, params, P, 2 * P)
                    with torch.no_grad():
                        acc = float((net(ea, eb)[:, P:].argmax(-1).numpy() == ec).mean())
                        # diagnostic: is each learned B embedding near the A embedding of the element it denotes?
                        EA_, EB_ = net.E.weight[:P], net.E.weight[P:]
                        dmat = torch.cdist(EB_, EA_)
                        nn_idx = dmat.argmin(1).numpy()
                        snap_ok = float((nn_idx == pi).mean())
                        dAA = torch.cdist(EA_, EA_) + 1e9 * torch.eye(P)
                        off = float(dmat.min(1).values.mean() / dAA.min(1).values.mean())
                    accs.append(acc); losses.append(L); diag.append((snap_ok, off))
                best = int(np.argmin(losses))       # restart selection by TRAINING loss only
                out.append(dict(kind=kind, seed=seed, nB=nB, method=f"{body}_{mode}", acc=accs[best],
                                acc_mean=float(np.mean(accs)), train_loss=losses[best],
                                preA=pre[(body, tied)][1] if mode != "scratch" else None,
                                nearestA_is_true=diag[best][0], offmanifold_ratio=diag[best][1]))
    return out


if __name__ == "__main__":
    nBs = [6, 10, 15, 20, 30, 45, 70, 100]
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        r = job(("add", 1, [10, 30]))
        for x in r: print(x)
        sys.exit()
    jobs = [(k, s, nBs) for k in ["add", "latin"] for s in [1, 2, 3, 4, 5]]
    t0 = time.time()
    res = pool_run(job, jobs, procs=10)
    json.dump([x for r in res for x in r], open("e2_results.json", "w"), indent=1)
    print("done", round(time.time() - t0, 1))
