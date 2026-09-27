"""
H.1s — Hierarchical (group) CSL in the symbolic stream: certify at the level of BASE FEATURES
("feature i matters in some way"), then fit all of feature i's candidate terms (single i and pairs (i,j))
densely with online L1-SGD. Question: does coarser certification extend CSL into denser regimes?

Group test for feature i (multi-direction score test):
    Z = s * (y - p) * sum_k d_k u_k(x),   u_k = centred candidate features of group i,
    d = residual-covariance direction at proposal (past data only), normalised so sum_k |d_k| <= 1  -> |Z| <= 1.
Retirement: Shiryaev-Roberts on "the certified group's frozen contribution now hurts" (as in H.1j).
Model logit = bias + sum over candidate terms whose group (either endpoint for pairs) is certified of w_term * term.
"""
import numpy as np, math, json, time, itertools, sys
from csl_experiment import RuleStream, logloss, sigmoid, run as run_base
from multiprocessing import Pool

LAMS = np.array([0.025, 0.05, 0.1, 0.2, 0.4, 0.8])


def mix_log(lw):
    m = lw.max(); return m + math.log(np.exp(lw - m).mean())


class HierCSL:
    def __init__(self, d, lr=0.01, l1=1e-3, alpha_rate=0.1, window=10000, pe=50, maxp=10, min_life=1500,
                 patience=6000, arl=1e5, delta_r=0.001):
        self.d = d; self.iu = np.triu_indices(d, 1); self.nf = d + len(self.iu[0])
        # membership: term t belongs to groups of its base features
        self.groups = [[i] + [d + k for k in range(len(self.iu[0])) if self.iu[0][k] == i or self.iu[1][k] == i] for i in range(d)]
        self.w = np.zeros(self.nf); self.b = 0.0; self.lr, self.l1 = lr, l1
        self.active = np.zeros(self.nf, bool)            # term usable iff some group containing it is certified
        self.cert = {}; self.pend = {}
        self.alpha_c = alpha_rate / (window / pe); self.pe, self.maxp = pe, maxp
        self.minlife, self.pat, self.arl, self.dr = min_life, patience, arl, delta_r
        self.cov = np.zeros(self.nf); self.mf = np.full(self.nf, 0.3); self.decay = 0.999
        self.log = []

    def fv(self, x):
        return np.concatenate([x, (x[:, None] * x[None, :])[self.iu]])

    def _refresh_active(self):
        self.active[:] = False
        for i in self.cert:
            self.active[self.groups[i]] = True

    def step(self, t, x, y):
        f = self.fv(x); u = f - self.mf
        z = self.b + float((self.w * self.active) @ u)
        p = sigmoid(z); loss = logloss(z, y); r = y - p
        to_admit, to_drop = [], []
        for i, g in self.pend.items():
            Z = g["s"] * r * float(g["d"] @ u[self.groups[i]])
            g["lw"] += np.log1p(LAMS * Z); g["logW"] = mix_log(g["lw"])
            age = t - g["born"]
            if g["logW"] >= math.log(1 / self.alpha_c):
                to_admit.append(i)
            elif age > self.pat or (age > self.minlife and g["logW"] <= 1.0):
                to_drop.append(i)
        to_ret = []
        for i, c in self.cert.items():
            idx = self.groups[i]
            if t - c["t"] < 1000:
                continue                                   # burn-in: let the plastic group fit first
            wi = self.w[idx] * self.active[idx]
            contrib_now = float(wi @ u[idx]); bound = float(np.abs(wi).sum()) + self.dr   # predictable, x-independent
            Dr = loss - logloss(z - contrib_now, y)       # > 0: removing the group's CURRENT contribution helps
            Zr = (Dr + self.dr) / bound
            c["lwr"] = np.logaddexp(0.0, c["lwr"]) + np.log1p(LAMS * max(-1.0, min(1.0, Zr))); c["logWr"] = mix_log(c["lwr"])
            if t - c["t"] > 50 and c["logWr"] >= math.log(self.arl):
                to_ret.append(i)
        # SGD on active terms
        g_ = p - y
        self.b -= self.lr * g_
        act = self.active
        self.w[act] -= self.lr * g_ * u[act]
        self.w[act] = np.sign(self.w[act]) * np.maximum(np.abs(self.w[act]) - self.lr * self.l1, 0)
        changed = False
        for i in to_ret:
            del self.cert[i]; self.log.append((t, "retire", i)); changed = True
        if to_admit:
            i = max(to_admit, key=lambda q: self.pend[q]["logW"])
            g = self.pend.pop(i); idx = self.groups[i]
            self.w[idx] = np.where(self.active[idx], self.w[idx], 4.0 * self.cov[idx] / (self.mf[idx] * (1 - self.mf[idx]) + 1e-3))
            self.w[idx] = np.clip(self.w[idx], -3, 3)
            self.cert[i] = dict(t=t, wc=self.w[idx].copy(), lwr=np.zeros(len(LAMS)), logWr=0.0)
            self.log.append((t, "admit", i)); changed = True
        for i in to_drop:
            self.pend.pop(i, None)
        if changed:
            self._refresh_active()
        # residual mining + group proposals
        self.mf = self.decay * self.mf + (1 - self.decay) * f
        self.cov = self.decay * self.cov + (1 - self.decay) * r * u
        if t % self.pe == 0 and t > 200 and len(self.pend) < self.maxp:
            sc = [(np.linalg.norm(self.cov[self.groups[i]]), i) for i in range(self.d) if i not in self.cert and i not in self.pend]
            if sc:
                _, i = max(sc)
                v = self.cov[self.groups[i]]; dd = v / (np.abs(v).sum() + 1e-12)
                self.pend[i] = dict(d=dd, s=1.0, lw=np.zeros(len(LAMS)), logW=0.0, born=t)
        return loss


def job(args):
    d, K, seed = args
    cfg = dict(d=d, K=K, lo=0.7, hi=1.4, drift=6000)
    st = RuleStream(d, K, 0.7, 1.4, 6000, 0.5, np.random.default_rng(seed))
    m = HierCSL(d)
    tot = 0.0; tot_o = 0.0
    for t in range(30000):
        x, y, lg = st.step(); tot += m.step(t, x, y); tot_o += logloss(lg, y)
    return dict(d=d, K=K, seed=seed, regret=(tot - tot_o) / 30000, groups_certified_final=len(m.cert),
                admissions=sum(1 for e in m.log if e[1] == "admit"))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(job((20, 32, 1))); print(job((20, 4, 1))); sys.exit()
    cells = [(10, K) for K in [4, 8, 16, 24, 32]] + [(20, K) for K in [4, 16, 32, 48, 64]] + [(40, K) for K in [4, 16]]
    jobs = [(d, K, s) for (d, K) in cells for s in [1, 2, 3, 4]]
    with Pool(12) as p:
        res = p.map(job, jobs, chunksize=1)
    json.dump(res, open("hier_results.json", "w"), indent=1); print("done")
