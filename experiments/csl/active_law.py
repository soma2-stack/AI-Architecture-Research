"""
H.4 — Active certification: can an agent that CHOOSES its actions to gather evidence for pending hypotheses
certify world structure faster than random exploration or count-based curiosity?  (e-processes remain valid
under adaptively collected data, so the guarantee is unaffected by the policy.)

World: LawWorld, no drift (fixed laws), layout re-randomised every 100 steps. Learner: group CSL with background.
Policies (action chosen before observing the outcome; contexts an action would activate are visible):
  random     : uniform action
  curiosity  : action whose activated contexts have the fewest visits so far (count-based novelty)
  certify    : action maximising sum over activated PENDING contexts of their current test "promise"
               (log-wealth > 0 preferred; unvisited-pending get a bonus), falling back to curiosity
Metrics every 2k steps: number of certified contexts; expected log-loss of the model on a FIXED random-context
evaluation set (exact outcome expectations), so exploration does not bias the evaluation.
"""
import numpy as np, math, json, time, sys
import lawworld as lw
from lawworld_group import GroupCSL
from multiprocessing import Pool


def eval_model(world, m, ctxs):
    tot = 0.0
    for grid, pos, a in ctxs:
        ctx = world.context(pos, a, grid); act = set(lw.active_preconds(ctx, a))
        z = m.logits(a, act); L = lw.lse(z)
        dist, _ = world.outcome_dist(pos, a, grid)
        tot += sum(pr * (L - z[k]) for k, pr in dist.items())
    return tot / len(ctxs)


def choose(policy, world, m, visits, rng):
    if policy == "random":
        return int(rng.integers(4))
    if policy == "certify2" and rng.random() < 0.5:        # epsilon-greedy: 50% random steps for coverage
        return int(rng.integers(4))
    scores = []
    for a in range(4):
        act = lw.active_preconds(world.context(world.pos, a), a)
        if policy == "curiosity":
            s = -sum(visits[P] for P in act) / len(act)
        elif policy == "certify2":   # greedy half: PROMISING pending hypotheses only
            s = 0.0
            for P in act:
                if P in m.pend and m.pend[P].logW > 0.5:
                    s += m.pend[P].logW / math.sqrt(1.0 + visits[P])
        else:  # certify
            s = 0.0
            for P in act:
                if P in m.pend:
                    s += 1.0 + max(m.pend[P].logW, 0.0)
                elif P not in m.acc:
                    s += 0.5 / (1.0 + visits[P])          # not yet proposed: small novelty bonus
        scores.append(s + 1e-6 * rng.random())
    return int(np.argmax(scores))


def run(args):
    policy, seed, N = args
    world = lw.LawWorld(np.random.default_rng(seed), drift=10**9)
    m = GroupCSL(background=True, bg_l1=1e-4)
    rng = np.random.default_rng(seed + 31)
    ev = world.sample_contexts(800, np.random.default_rng(seed + 999))
    visits = np.zeros(lw.NP)
    curve = []
    for t in range(N):
        if t % 100 == 0:
            world.new_layout()
        a = choose(policy, world, m, visits, rng)
        ctx = world.context(world.pos, a)
        dist, _ = world.outcome_dist(world.pos, a)
        keys = list(dist.keys()); pr = np.array([dist[k] for k in keys])
        o = keys[int(world.rng.choice(len(keys), p=pr / pr.sum()))]
        dy, dx = o // 7 - 3, o % 7 - 3
        world.pos = (world.pos[0] + dx, world.pos[1] + dy); world.t += 1
        for P in lw.active_preconds(ctx, a):
            visits[P] += 1
        m.step(t, a, ctx, o)
        if t % 2000 == 1999:
            curve.append(dict(t=t + 1, certified=len(m.acc), eval_loss=eval_model(world, m, ev)))
    return dict(policy=policy, seed=seed, curve=curve)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        for p in ["random", "certify2"]:
            t0 = time.time(); r = run((p, 1, 6000)); print(p, r["curve"], round(time.time() - t0, 1))
        sys.exit()
    jobs = [(p, s, 20000) for p in ["random", "curiosity", "certify", "certify2"] for s in range(1, 9)]
    with Pool(12) as pool:
        res = pool.map(run, jobs, chunksize=1)
    json.dump(res, open("active_results.json", "w"), indent=1)
    print("done")
