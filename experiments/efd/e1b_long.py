"""E1b: are the S5 recurrent failures just undertraining? GRU/LSTM trained 5x longer; factorized program baseline."""
import json, sys, time, numpy as np, torch
from common import seed_all, RNNSeq, train_loop, pool_run
import e1_compose as E

def factorized_program(rng):
    # learn each token's permutation g from observed transitions s -> s' = compose(s, g): g[s[i]] = s'[i]
    votes = [dict() for _ in range(5)]
    for _ in range(50):
        tok, tgt = E.make_seq("s5", 16, rng)
        prev = tuple(range(5))
        for t, y in zip(tok, tgt):
            nxt = E.PERMS[y]; g = [None] * 5
            for i in range(5): g[prev[i]] = nxt[i]
            g = tuple(g); votes[t][g] = votes[t].get(g, 0) + 1; prev = nxt
    gens = [max(v, key=v.get) for v in votes]
    def pred(tok):
        st, out = tuple(range(5)), []
        for t in tok:
            st = E.compose(st, gens[t]); out.append(E.PIDX[st])
        return np.array(out)
    return pred

def job(args):
    kind, seed, steps = args
    seed_all(seed); rng = np.random.default_rng(seed)
    if kind == "program":
        pred = factorized_program(rng)
    else:
        m = RNNSeq(5, 120, d=128, kind=kind)
        train_loop(m, E.batch_fn_factory("s5", rng), steps=steps, lr=1e-3)
        def pred(tok):
            with torch.no_grad(): return m(torch.tensor(tok)[None])[0].argmax(-1).numpy()
    return dict(kind=kind, seed=seed, steps=steps, acc=E.eval_model(pred, "s5", np.random.default_rng(seed + 1000)))

if __name__ == "__main__":
    jobs = [("program", 1, 0)] + [(k, s, 20000) for k in ["gru", "lstm"] for s in [1, 2, 3]]
    res = pool_run(job, jobs, procs=2)
    json.dump(res, open("e1b_results.json", "w"), indent=1); print("done")
