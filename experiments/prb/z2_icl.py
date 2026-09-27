"""
Z.2 — in-context structural rebinding with Qwen3-VL-4B-Instruct (text-only, fp32, CPU).
Paired episodes: for each (n, seed, m) the same symbols, permutation pi and demonstration pairs are used in
every condition.
Conditions:
  D_told   digits, rule stated                      (can the model execute the rule?)
  D_untold digits, rule not stated
  S_told   symbols; told they stand for 0..n-1 in a secret order and each line is (x+y) mod n  (pure rebinding)
  S_untold symbols; no information about the rule                                          (family hidden)
  S_map    symbols with the true code listed explicitly                                     (execution given binding)
Measures per condition: accuracy on unseen pairs, on demonstrated pairs, coherence of the full n x n answer table
(max fraction explained by ONE relabelling of Z_n), mapping score of that relabelling vs the truth; for S_told
an explicit mapping probe ('X stands for the number').
Controls: CSP over pi (consistent bijections, identifiability), model-as-scorer exhaustive search over pi.
"""
import json, sys, time, itertools
import numpy as np
import prb_common as P

tok, model = P.load()
POOL = P.symbol_pool(tok)
DIG = [tok.encode(str(d), add_special_tokens=False)[0] for d in range(10)]
enc = lambda s: tok.encode(s, add_special_tokens=False)


def digit_line(a, b, c=None):
    s = f" {a} + {b} ="
    return enc(s + f" {c}\n") if c is not None else enc(s) + [220]


def sym_line(sa, sb, sc=None):
    s = f" {sa} + {sb} ="
    return enc(s + f" {sc}\n") if sc is not None else enc(s)


def run_condition(cond, n, syms, sym_ids, pi, demos, rng):
    T = P.table(n)
    pairs = [(i, j) for i in range(n) for j in range(n)]
    dset = set((i, j) for i, j, _ in demos)
    if cond in ("S_decode", "S_encode"):
        names = ", ".join(syms)
        head = (f"The symbols are: {names}.\nEach symbol stands for a different number from 0 to {n - 1}. "
                f"The code is: " + ", ".join(f"{syms[i]} = {pi[i]}" for i in range(n)) + ".\n")
        ids = enc(head)
        if cond == "S_decode":
            ids += enc(f"Each line decodes the two symbols and computes (x + y) mod {n} as a number.\n")
            for i, j, k in demos:
                ids += enc(f" {syms[i]} + {syms[j]} = {pi[k]}\n")
            sufs = [enc(f" {syms[i]} + {syms[j]} =") + [220] for i, j in pairs]
            cands = DIG[:n]
        else:
            ids += enc(f"Each line computes (x + y) mod {n} of two numbers and writes the result as its symbol.\n")
            for i, j, k in demos:
                ids += enc(f" {pi[i]} + {pi[j]} = {syms[k]}\n")
            sufs = [enc(f" {pi[i]} + {pi[j]} =") for i, j in pairs]
            cands = sym_ids
        cache, plen = P.prefix_cache(model, ids)
        lg = P.score_suffixes_batched(model, cache, plen, sufs, cands)
        pred = lg.argmax(1)
        pred_sym = np.argsort(pi)[pred] if cond == "S_decode" else pred
    elif cond.startswith("D"):
        head = f"Each line computes (x + y) mod {n}.\n" if cond == "D_told" else "Each line shows the result of a fixed operation.\n"
        ids = enc(head)
        for i, j, k in demos:
            ids += digit_line(pi[i], pi[j], pi[k])
        cands = DIG[:n]
        sufs = [digit_line(pi[i], pi[j]) for i, j in pairs]
        truth = [pi[T_inv(pi, T, i, j, n)] for i, j in pairs]
        cache, plen = P.prefix_cache(model, ids)
        lg = P.score_suffixes_batched(model, cache, plen, sufs, cands)
        pred_num = lg.argmax(1)                      # predicted NUMBER
        inv = np.argsort(pi)
        pred_sym = inv[pred_num]                     # express as symbol index for coherence
    else:
        names = ", ".join(syms)
        if cond == "S_untold":
            head = f"The symbols are: {names}.\nEach line shows the result of a fixed operation on these symbols.\n"
        else:
            head = (f"The symbols are: {names}.\nEach symbol stands for a different number from 0 to {n - 1}, "
                    f"but the assignment is secret. Each line computes (x + y) mod {n} written in this secret code.\n")
            if cond == "S_map":
                head += "The code is: " + ", ".join(f"{syms[i]} = {pi[i]}" for i in range(n)) + ".\n"
        ids = enc(head)
        for i, j, k in demos:
            ids += sym_line(syms[i], syms[j], syms[k])
        cands = sym_ids
        sufs = [sym_line(syms[i], syms[j]) for i, j in pairs]
        cache, plen = P.prefix_cache(model, ids)
        lg = P.score_suffixes_batched(model, cache, plen, sufs, cands)
        pred_sym = lg.argmax(1)
    true_sym = np.array([T_inv(pi, T, i, j, n) for i, j in pairs])
    ok = pred_sym == true_sym
    is_demo = np.array([(i, j) in dset for i, j in pairs])
    coh, sig = P.coherence(pred_sym.reshape(n, n), n)
    out = dict(acc_unseen=float(ok[~is_demo].mean()), acc_demo=float(ok[is_demo].mean()), coherence=coh,
               coherent_map_score=P.mapping_score(list(sig), list(pi), n), prefix_len=plen)
    # coherence on UNSEEN entries only: does ONE relabelling explain the model's answers on unseen pairs?
    best_u = 0.0
    Tn = P.table(n)
    for sg in itertools.permutations(range(n)):
        sg = np.array(sg); invs = np.argsort(sg)
        expl = invs[Tn[sg[:, None], sg[None, :]]].reshape(-1)
        best_u = max(best_u, float((expl[~is_demo] == pred_sym[~is_demo]).mean()))
    out["coherence_unseen"] = best_u
    if cond in ("S_told", "S_map"):
        probe = [enc(f"In this code, {syms[i]} stands for the number") + [220] for i in range(n)]
        plg = P.score_suffixes_batched(model, cache, plen, probe, DIG[:n])
        pi_hat = list(plg.argmax(1))
        out["probe_map_score"] = P.mapping_score(pi_hat, list(pi), n)
        out["probe_is_bijection"] = len(set(pi_hat)) == n
        # does the probed mapping explain the model's own answers?
        T2 = P.table(n); invh = {}
        expl = [None if len(set(pi_hat)) < n else int(np.argsort(pi_hat)[T2[pi_hat[i], pi_hat[j]]]) for i, j in pairs]
        out["probe_explains_answers"] = float(np.mean([e == p for e, p in zip(expl, pred_sym)])) if expl[0] is not None else None
    return out


def T_inv(pi, T, i, j, n):
    """symbol index k with pi[k] = (pi[i] + pi[j]) mod n"""
    return int(np.argsort(pi)[T[pi[i], pi[j]]])


_SCORER = {}


def model_scorer_table(n):
    """log-prob table L[x, y, z] = log p(z | 'x + y =') from the model in the digit interface (rule stated, no demos)."""
    if n in _SCORER: return _SCORER[n]
    ids = enc(f"Each line computes (x + y) mod {n}.\n")
    cache, plen = P.prefix_cache(model, ids)
    sufs = [digit_line(a, b) for a in range(n) for b in range(n)]
    lg = P.score_suffixes_batched(model, cache, plen, sufs, DIG[:n])
    lp = lg - np.log(np.exp(lg - lg.max(1, keepdims=True)).sum(1, keepdims=True)) - lg.max(1, keepdims=True)
    _SCORER[n] = lp.reshape(n, n, n)
    return _SCORER[n]


def scorer_search(n, demos):
    L = model_scorer_table(n)
    best, arg = -1e18, None
    for pi in itertools.permutations(range(n)):
        s = sum(L[pi[i], pi[j], pi[k]] for i, j, k in demos)
        if s > best: best, arg = s, pi
    return arg


def episode(n, seed, m, conds):
    rng = np.random.default_rng(1000 * n + seed)
    idx = rng.choice(len(POOL), n, replace=False)
    syms = [POOL[i][0] for i in idx]; sym_ids = [POOL[i][1] for i in idx]
    pi = [int(v) for v in rng.permutation(n)]
    T = P.table(n)
    pairs = [(i, j) for i in range(n) for j in range(n)]
    dsel = rng.choice(len(pairs), m, replace=False)
    demos = [(pairs[d][0], pairs[d][1], T_inv(pi, T, pairs[d][0], pairs[d][1], n)) for d in dsel]
    rec = dict(n=n, seed=seed, m=m, syms=syms, pi=pi)
    sols = P.csp_consistent(n, demos)
    rec["csp_n_solutions"] = len(sols)
    unseen = [p for p in pairs if p not in set((i, j) for i, j, _ in demos)]
    def acc_from(pi_c):
        return float(np.mean([T_inv(list(pi_c), T, i, j, n) == T_inv(pi, T, i, j, n) for i, j in unseen]))
    # CSP prediction: majority vote over consistent bijections
    votes = []
    for i, j in unseen:
        c = {}
        for s in sols:
            k = T_inv(list(s), T, i, j, n); c[k] = c.get(k, 0) + 1
        votes.append(max(c, key=c.get) == T_inv(pi, T, i, j, n))
    rec["csp_acc_unseen"] = float(np.mean(votes))
    rec["scorer_search_acc_unseen"] = acc_from(scorer_search(n, demos))
    for cond in conds:
        t0 = time.time()
        rec[cond] = run_condition(cond, n, syms, sym_ids, pi, demos, rng)
        rec[cond]["secs"] = round(time.time() - t0, 1)
    return rec


if __name__ == "__main__":
    conds = ["D_told", "D_untold", "S_told", "S_untold", "S_map", "S_decode", "S_encode"]
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    ms = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [10, 20, 30, 40]
    seeds = range(int(sys.argv[3]) if len(sys.argv) > 3 else 6)
    out = open(f"z2_n{n}.jsonl", "a")
    for seed in seeds:
        for m in ms:
            t0 = time.time()
            rec = episode(n, seed, m, conds)
            rec["secs"] = round(time.time() - t0, 1)
            out.write(json.dumps(rec) + "\n"); out.flush()
            print(n, seed, m, {c: round(rec[c]["acc_unseen"], 2) for c in conds}, "csp", rec["csp_acc_unseen"], "nsol", rec["csp_n_solutions"], rec["secs"], flush=True)
