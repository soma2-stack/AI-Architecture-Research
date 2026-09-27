import numpy as np, math
from csl_experiment import *
cfg = CONFIGS["A_pilot"]
for pol in ["CSL","HW"]:
    st = RuleStream(cfg["d"],cfg["K"],cfg["lo"],cfg["hi"],cfg["drift"],0.5,np.random.default_rng(1))
    m = Grower(cfg["d"], pol, np.random.default_rng(99), propose_k=1)
    born = {}
    orig_pending = m.pending
    for t in range(12000):
        x,y,_ = st.step(); m.step(t,x,y)
        for f,c in m.pending.items():
            born.setdefault(f, []).append(c.born) if (not born.get(f) or born[f][-1]!=c.born) else None
    adm = {}
    for t,e,f in m.log:
        if e=="admit": adm.setdefault(f,[]).append(t)
    for s,r in st.history:
        f = tuple(r["feats"])
        print(pol, "rule", f, "start", s, "beta", round(r["beta"],2), "proposed at", born.get(f), "admitted at", adm.get(f))
    print(pol, "n pending at end", len(m.pending), "alpha_c", m.alpha_c)
