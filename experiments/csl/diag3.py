import numpy as np, math
from csl_experiment import *
cfg = CONFIGS["A_pilot"]
st = RuleStream(cfg["d"],cfg["K"],cfg["lo"],cfg["hi"],cfg["drift"],0.5,np.random.default_rng(1))
m = Grower(cfg["d"], "CSL", np.random.default_rng(1+12345), propose_k=1, ret_mode="statement")
tr = {}
for t in range(20000):
    x,y,_ = st.step(); m.step(t,x,y)
    if t % 500 == 0:
        for f,c in m.accepted.items():
            tr.setdefault(f, []).append((t, round(c.logWr,2), round(c.w,2), round(c.wc,2)))
print("rules:", [(s, r["feats"], round(r["beta"],2), st.ended.get(r["id"])) for s,r in st.history])
print("log:", m.log)
for f, v in tr.items():
    print(f, v[:40])
