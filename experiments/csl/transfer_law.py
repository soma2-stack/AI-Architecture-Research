"""
H.1p — Safe transfer between agents: does transferring only CERTIFIED structure avoid negative transfer?

Agent A learns 30k steps in world A (no drift) with both a dense joint learner (L1POE-REL, same 98-dim
parameterisation) and group CSL with background (which yields a certified set of contexts).
Agent B then learns 15k steps in world B, which is either the SAME as A or DIFFERENT (2 of 5 laws changed).
B's learner is always L1POE-REL, initialised as:
   T0 none       : zeros
   T1 full       : all of A's dense weights
   T3 certified  : A's dense weights only for A's certified contexts (all other rows zero)
Metric: B's average loss over its first 2k, 5k and 15k steps (lower is better).
"""
import numpy as np, math, json, time, sys
import lawworld as lw
from lawworld_group import GroupCSL
from l1poe_rel import L1POERel
from multiprocessing import Pool

LAWS_A = dict(ice=1, spring=1, mud=0.6, convX=1, convY=1)
LAWS_DIFF = dict(ice=0, spring=1, mud=0.6, convX=-1, convY=1)      # ice off, conveyor-x reversed


def make_world(seed, laws):
    w = lw.LawWorld(np.random.default_rng(seed), drift=10**9)
    w.laws = dict(laws)
    return w


def train_A(seed, N=30000):
    w = make_world(seed, LAWS_A)
    dense = L1POERel(lr=0.1, l1=1e-4)
    g = GroupCSL(background=True, bg_l1=1e-4)
    for t in range(N):
        a, ctx, o, dist = w.step()
        dense.step(t, a, ctx, o); g.step(t, a, ctx, o)
    return dense, sorted(g.acc.keys())


def run_B(args):
    seed, world_kind, mode = args
    dense_A, cert = train_A(seed)
    B = L1POERel(lr=0.1, l1=1e-4)
    if mode == "full":
        B.W = dense_A.W.copy(); B.bias = dense_A.bias.copy()
    elif mode == "certified":
        for P in cert:
            B.W[P] = dense_A.W[P]
        B.bias = dense_A.bias.copy()
    w = make_world(seed + 5000, LAWS_A if world_kind == "same" else LAWS_DIFF)
    losses = []
    for t in range(15000):
        a, ctx, o, dist = w.step()
        losses.append(B.step(t, a, ctx, o))
    L = np.array(losses)
    return dict(seed=seed, world=world_kind, mode=mode, n_certified=len(cert),
                loss_2k=float(L[:2000].mean()), loss_5k=float(L[:5000].mean()), loss_15k=float(L.mean()))


if __name__ == "__main__":
    jobs = [(s, wk, m) for s in range(1, 9) for wk in ["same", "diff"] for m in ["none", "full", "certified"]]
    t0 = time.time()
    with Pool(12) as p:
        res = p.map(run_B, jobs, chunksize=1)
    json.dump(res, open("transfer_results.json", "w"), indent=1)
    print("done", time.time() - t0)
