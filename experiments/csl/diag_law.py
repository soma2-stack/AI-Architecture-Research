import numpy as np, math, lawworld as lw
seed = 1
world = lw.LawWorld(np.random.default_rng(seed)); g = lw.Grower("CSL")
born = {}
rows = []
for t in range(30000):
    a, ctx, o, dist = world.step()
    n0 = len(g.log); g.step(t, a, ctx, o)
    for k, c in g.pending.items():
        born.setdefault(k, c.born)
    for (tt, ev, k) in g.log[n0:]:
        if ev != "admit": continue
        s600, _ = lw.true_scores(world, g, k, np.random.default_rng(seed * 1000 + tt), n=600)
        s4k, u4k = lw.true_scores(world, g, k, np.random.default_rng(777 + tt), n=4000)
        last_change = max([c[0] for c in world.changes if c[0] <= tt], default=-10**9)
        c = g.accepted[k]
        # overlapping admitted laws with the same outcome index (possible "need already satisfied")
        overlap = sum(1 for k2, c2 in g.accepted.items() if k2 != k and c2.ol == c.ol and c2.admitted_at >= c.born)
        rows.append((tt, k, round(s600, 5), round(s4k, 5), round(u4k, 5), tt - last_change, tt - c.born, overlap))
false600 = [r for r in rows if r[2] <= 0]
print("admissions", len(rows), "false by n=600:", len(false600), " false by n=4000:", sum(1 for r in rows if r[3] <= 0))
print("columns: t, law(P,o), score600, score4000, usefulness4000, steps_since_law_change, test_duration, overlapping_admitted_same_outcome")
for r in false600 + [r for r in rows if r[3] <= 0 and r not in false600]:
    print(r)
print("typical true score of admitted laws (median, n=4000):", np.median([r[3] for r in rows]))
