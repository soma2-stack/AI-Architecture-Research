import numpy as np, math, csl_neural as cn
sc = cn.SCFG
for pol in ["CSL","HW"]:
    st = cn.BumpStream(sc["m"], sc["K"], sc["drift"], sc["recur"], np.random.default_rng(1), sigma=sc["sigma"], width=sc["width"])
    g = cn.Grower(sc["m"], pol, np.random.default_rng(100))
    probe = np.random.default_rng(6).uniform(-1, 1, (1500, 2))
    for t in range(8000):
        x,y,gx = st.step(); n0 = len(g.log); g.step(t,x,y)
        for (tt, ev, e) in g.log[n0:]:
            if ev != "admit": continue
            gp = np.array([st.g(p) for p in probe])
            others = np.array([g.bias + sum(o.net.f(p) for o in g.accepted if o is not e) for p in probe])
            he = np.array([e.net.f(p) for p in probe])
            U = np.mean((gp-others)**2 - (gp-others-he)**2)/2
            loc = np.linalg.norm(probe - e.net.c, axis=1) < e.net.s
            print(pol, t, "c", np.round(e.net.c,2).tolist(), "U %.4f" % U, "bias %.2f" % g.bias,
                  "true resid in region %.2f" % np.mean((gp-others)[loc]), "expert mean out in region %.2f" % np.mean(he[loc]))
