import numpy as np, math, csl_neural as cn
sc = cn.SCFG
st = cn.BumpStream(sc["m"], sc["K"], sc["drift"], sc["recur"], np.random.default_rng(1), sigma=sc["sigma"], width=sc["width"])
g = cn.Grower(sc["m"], "CSL", np.random.default_rng(100))
print("bumps", [(np.round(c,2).tolist(), round(a,2)) for c,a in st.bumps])
for t in range(8000):
    x,y,gx = st.step()
    n0 = len(g.log)
    g.step(t,x,y)
    for (tt, ev, e) in g.log[n0:]:
        if ev == "admit":
            dmin = min(np.linalg.norm(e.net.c - c) for c,a in st.bumps)
            print(t, "ADMIT c=", np.round(e.net.c,2).tolist(), "dist-to-nearest-bump %.2f" % dmin, "logW %.1f" % e.logW, "size", len(g.accepted))
        else:
            print(t, "RETIRE", ev, "size", len(g.accepted))
    if t % 2000 == 1999:
        print(t, "pending", len(g.pending), [round(p.logW,1) for p in g.pending], "accepted logWr", [round(a.logWr,1) for a in g.accepted])
