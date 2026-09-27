import json, collections, numpy as np
res = json.load(open("tune_results.json"))
agg = collections.defaultdict(list)
for r in res:
    agg[(r["policy"], tuple(sorted(r["kw"].items())))].append(r)
rows = [(k[0], dict(k[1]), np.mean([x["avg_loss"] for x in v]),
         np.mean([x.get("spurious", x.get("spurious_avg_structure", 0)) for x in v])) for k, v in agg.items()]
best = {}
for pol in ["HW", "L1"]:
    rr = sorted([r for r in rows if r[0] == pol], key=lambda r: r[2])
    for r in rr[:6]: print(pol, r[1], "loss %.4f" % r[2], "spur %.2f" % r[3])
    print(pol, "worst", rr[-1][1], "%.4f" % rr[-1][2])
    best[pol] = rr[0][1]
best["HW"].pop("propose_k", None)
json.dump(best, open("tuned.json", "w")); print("tuned:", best)
