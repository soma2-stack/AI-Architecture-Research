"""
Z.4 — gradient (embedding-level) adaptation to a relabelled interface in Qwen3-VL-4B (fp32, CPU); the E2 analogue at scale.
Format (no spaces, one token per operand): 'a+b=c\\n'. Frozen prefix: instruction + 5 digit examples (KV-cached, no grad).
Relabelled training lines use n symbol tokens (single tokens without leading space). Only the n symbol embedding rows
are adapted; embeddings are TIED, so the same rows are used as inputs and as output (unembedding) rows.
  free      rows = E0[sym] + scale * delta     (delta trained)                     — E2 'ft_embed_tied'
  sinkhorn  rows = Sinkhorn(S / tau) @ E0[digits] (S trained, tau annealed; hardened by Hungarian) — E2/Y.4b relaxation
Measures: training accuracy, unseen-pair accuracy, recovered mapping (nearest digit row / hardened assignment) scored
modulo automorphisms, coherence of the full predicted table.
Control: model-as-scorer exhaustive search over pi using the model's own digit log-prob table (same prefix).
"""
import json, sys, time, copy
import numpy as np
import torch, torch.nn.functional as F
from scipy.optimize import linear_sum_assignment
import prb_common as P

tok, model = P.load(threads=int(sys.argv[4]) if len(sys.argv) > 4 else 12)
for p_ in model.parameters():
    p_.requires_grad_(False)
enc = lambda s: tok.encode(s, add_special_tokens=False)
DIG = [enc(str(d))[0] for d in range(10)]
PLUS, EQ, NL = enc("+")[0], enc("=")[0], enc("\n")[0]
E0 = model.get_input_embeddings().weight          # tied with lm_head
NOSPACE = [(w, enc(w)[0]) for w, _ in P.symbol_pool(tok) if len(enc(w)) == 1]


RULE = {}


def latin(n, seed):
    """a random Latin square that is NOT isotopic-in-an-obvious-way to Z_n: start from Z_n, apply random row, column
    and symbol permutations, then random intercalate-free 'cycle switches' are not needed for our purpose; we instead
    reject squares with a non-trivial automorphism (checked exhaustively for n <= 7)."""
    import itertools
    rng = np.random.default_rng(424242 + seed)
    base = np.add.outer(np.arange(n), np.arange(n)) % n
    while True:
        L = rng.permutation(n)[base[rng.permutation(n)][:, rng.permutation(n)]]
        auts = sum(1 for c in itertools.permutations(range(n))
                   if all(L[c[a], c[b]] == c[L[a, b]] for a in range(n) for b in range(n)))
        if auts == 1:
            return L


def prefix_ids(n):
    L = RULE["L"]
    ids = enc("Each line gives the value of a fixed operation on two digits. Here is the complete table.\n")
    for a in range(n):
        for b in range(n):
            ids += [DIG[a], PLUS, DIG[b], EQ, DIG[int(L[a, b])], NL]
    return ids


def exact_map_score(pi_hat, pi, n):
    return float(np.mean([pi_hat[i] == pi[i] for i in range(n)]))


def lm_hidden(inputs_embeds, cache):
    """final (normed) hidden state at the last position, via the text decoder with a replicated prefix cache."""
    B = inputs_embeds.shape[0]
    c = copy.deepcopy(cache); c.batch_repeat_interleave(B)
    out = model(inputs_embeds=inputs_embeds, past_key_values=c, use_cache=True, output_hidden_states=True)
    return out.hidden_states[-1][:, -1], out.logits[:, -1]


def line_embeds(pairs, rows, sym_tok):
    """embeddings for 'x+y=' with x, y symbol indices; symbol rows are differentiable."""
    plus, eq = E0[PLUS], E0[EQ]
    xs = torch.stack([torch.stack([rows[i], plus, rows[j], eq]) for i, j in pairs])
    return xs


def cand_logits(h, rows):
    return h @ rows.T


def T_inv(pi, i, j, n):
    return int(np.argsort(pi)[int(RULE["L"][pi[i], pi[j]])])


def run(n, seed, m, steps=100):
    RULE["L"] = latin(n, seed)
    rng = np.random.default_rng(7000 + 100 * n + seed)
    idx = rng.choice(len(NOSPACE), n, replace=False)
    syms = [NOSPACE[i][0] for i in idx]; sym_tok = [NOSPACE[i][1] for i in idx]
    pi = [int(v) for v in rng.permutation(n)]
    pairs = [(i, j) for i in range(n) for j in range(n)]
    sel = set(int(v) for v in rng.choice(len(pairs), m, replace=False))
    demo = [pairs[k] for k in sorted(sel)]; unseen = [pairs[k] for k in range(len(pairs)) if k not in sel]
    y_demo = torch.tensor([T_inv(pi, i, j, n) for i, j in demo]); y_uns = np.array([T_inv(pi, i, j, n) for i, j in unseen])
    cache, plen = P.prefix_cache(model, prefix_ids(n))
    import itertools
    Lr = RULE["L"]
    nsol = sum(1 for c in itertools.permutations(range(n)) if all(Lr[c[i], c[j]] == c[T_inv(pi, i, j, n)] for i, j in demo))
    rec = dict(n=n, seed=seed, m=m, syms=syms, pi=pi, csp_n_solutions=nsol, rule="latin")
    # --- control: digit interface accuracy with this prefix, and model-as-scorer search
    with torch.no_grad():
        sufs = [[DIG[a], PLUS, DIG[b], EQ] for a in range(n) for b in range(n)]
        lg = P.score_suffixes_batched(model, cache, plen, sufs, DIG[:n])
        rec["digit_interface_acc"] = float((lg.argmax(1) == RULE["L"].reshape(-1)).mean())
        lp = lg - np.log(np.exp(lg - lg.max(1, keepdims=True)).sum(1, keepdims=True)) - lg.max(1, keepdims=True)
        L = lp.reshape(n, n, n)
        import itertools
        best, arg = -1e18, None
        for cand in itertools.permutations(range(n)):
            sc = sum(L[cand[i], cand[j], cand[T_inv(pi, i, j, n)]] for i, j in demo)
            if sc > best: best, arg = sc, cand
        rec["scorer_search_unseen_acc"] = float(np.mean([T_inv(list(arg), i, j, n) == T_inv(pi, i, j, n) for i, j in unseen]))
        rec["scorer_search_map_score"] = exact_map_score(list(arg), pi, n)
    Dg = E0[DIG[:n]].detach()
    Es = E0[sym_tok].detach()
    scale = float(E0.detach().std())
    for method in ["free", "sinkhorn"]:
        torch.manual_seed(seed)
        if method == "free":
            delta = torch.zeros(n, E0.shape[1], requires_grad=True)
            params = [delta]; lr = 0.05
            rows_fn = lambda tau=None: Es + scale * delta
        else:
            S = (0.01 * torch.randn(n, n)).requires_grad_(True)
            params = [S]; lr = 0.1
            def rows_fn(tau=1.0):
                Lg = S / tau
                for _ in range(20):
                    Lg = Lg - torch.logsumexp(Lg, 1, keepdim=True); Lg = Lg - torch.logsumexp(Lg, 0, keepdim=True)
                return Lg.exp() @ Dg
        opt = torch.optim.Adam(params, lr=lr)
        t0 = time.time(); losses = []
        for s in range(steps):
            tau = max(0.05, 0.05 ** (s / steps))
            rows = rows_fn(tau)
            h, _ = lm_hidden(line_embeds(demo, rows, sym_tok), cache)
            loss = F.cross_entropy(cand_logits(h, rows), y_demo)
            opt.zero_grad(); loss.backward(); opt.step(); losses.append(float(loss))
        with torch.no_grad():
            if method == "free":
                rows = rows_fn()
                cos = F.normalize(rows, dim=1) @ F.normalize(Dg, dim=1).T
                pi_hat = list(cos.argmax(1).numpy())
            else:
                Lg = S.detach()
                r_, c_ = linear_sum_assignment(-Lg.numpy())
                pi_hat = [0] * n
                for a, b in zip(r_, c_): pi_hat[a] = int(b)
                rows = Dg[pi_hat]
            h_d, _ = lm_hidden(line_embeds(demo, rows, sym_tok), cache)
            tr_acc = float((cand_logits(h_d, rows).argmax(1) == y_demo).float().mean())
            h_u, _ = lm_hidden(line_embeds(unseen, rows, sym_tok), cache)
            pred_u = cand_logits(h_u, rows).argmax(1).numpy()
            h_all, _ = lm_hidden(line_embeds(pairs, rows, sym_tok), cache)
            pred_all = cand_logits(h_all, rows).argmax(1).numpy()
        coh = float("nan")
        rec[method] = dict(train_acc=tr_acc, unseen_acc=float((pred_u == y_uns).mean()), map_score=exact_map_score(pi_hat, pi, n),
                           map_is_bijection=len(set(pi_hat)) == n, coherence=coh, final_loss=losses[-1],
                           loss_curve=[round(x, 3) for x in losses[::10]], secs=round(time.time() - t0, 1))
    return rec


if __name__ == "__main__":
    n = int(sys.argv[1]); ms = [int(x) for x in sys.argv[2].split(",")]; seeds = [int(x) for x in sys.argv[3].split(",")]
    out = open(f"z4c_latin_n{n}.jsonl", "a")
    for seed in seeds:
        for m in ms:
            rec = run(n, seed, m)
            out.write(json.dumps(rec) + "\n"); out.flush()
            print(n, seed, m, "digit", rec["digit_interface_acc"], "scorer", rec["scorer_search_unseen_acc"],
                  {k: {kk: rec[k][kk] for kk in ("train_acc", "unseen_acc", "map_score", "coherence", "secs")} for k in ("free", "sinkhorn")}, flush=True)
