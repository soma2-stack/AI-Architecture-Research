import numpy as np, math
from csl_experiment import *
cfg = CONFIGS["A_pilot"]
for pol in ["CSL","HW"]:
    rng_s = np.random.default_rng(1); st = RuleStream(cfg["d"],cfg["K"],cfg["lo"],cfg["hi"],cfg["drift"],0.5,rng_s)
    m = Grower(cfg["d"], pol, np.random.default_rng(99))
    trace = {}
    for t in range(12000):
        x,y,_ = st.step(); m.step(t,x,y)
        if t % 500 == 0:
            for f,c in m.pending.items():
                trace.setdefault(f, []).append((t, round(c.logW,2), round(c.w,2)))
    print(pol, "rules:", [(s, r["feats"], round(r["beta"],2)) for s,r in st.history])
    print(pol, "admit/retire log:", [(t,e,f) for t,e,f in m.log][:40])
    if pol=="CSL":
        for s,r in st.history:
            f = tuple(r["feats"])
            print("  trace", f, trace.get(f, [])[:12])
    print("threshold", math.log(1/m.alpha_c))
