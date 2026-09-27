"""
H.1h — Adversarial: correlated proxies.  Features d0..d0+P-1 are noisy copies (flip prob q) of the
first feature of each current rule (they follow the rules through drift). A proxy is genuinely
predictive (not a statistical false positive) but makes the structure misleading.
Measure: fraction of admitted claims that are proxy-only; fraction of *final-time-averaged* structure
that is proxy-only; time from a true-rule claim's admission until overlapping proxy claims are retired.
"""
import numpy as np, json, time
from csl_experiment import Grower, RuleStream, CONFIGS, logloss
from multiprocessing import Pool


class ProxyStream(RuleStream):
    def __init__(self, d, K, lo, hi, drift, pf, rng, n_proxy=2, q=0.2):
        super().__init__(d, K, lo, hi, drift, pf, rng)
        self.n_proxy, self.q, self.d_total = n_proxy, q, d + K * n_proxy

    def step(self):
        x, y, logit = super().step()
        prox = []
        for r in self.rules:
            src = x[r["feats"][0]]
            for _ in range(self.n_proxy):
                prox.append(src if self.rng.random() > self.q else 1 - src)
        return np.concatenate([x, np.array(prox)]), y, logit

    def proxy_index_owner(self, i):
        """which rule's first feature does proxy column i currently copy? (None for real features)"""
        if i < self.d:
            return None
        j = (i - self.d) // self.n_proxy
        return self.rules[j]["feats"][0]


def job(args):
    policy, seed, N, kw = args
    cfg = CONFIGS["A_pilot"]; d = cfg["d"]
    st = ProxyStream(d, cfg["K"], cfg["lo"], cfg["hi"], cfg["drift"], 0.5, np.random.default_rng(seed))
    g = Grower(st.d_total, policy, np.random.default_rng(seed + 12345), **kw)
    tot = 0.0; proxy_share = []
    for t in range(N):
        x, y, _ = st.step(); tot += g.step(t, x, y)
        if t % 500 == 499 and g.accepted:
            pr = sum(1 for f in g.accepted if all(i >= d for i in f))
            proxy_share.append(pr / len(g.accepted))
    adm = [(t, f) for (t, ev, f) in g.log if ev == "admit"]
    proxy_adm = sum(1 for (t, f) in adm if all(i >= d for i in f))
    return dict(policy=policy, seed=seed, kw=kw, avg_loss=tot / N, admissions=len(adm), proxy_only_admissions=proxy_adm,
                mean_proxy_share_of_structure=float(np.mean(proxy_share)) if proxy_share else 0.0,
                final_size=len(g.accepted))


if __name__ == "__main__":
    tuned = json.load(open("tuned.json"))
    best = dict(propose_k=1, adm_mode="score", ret_mode="statement", ret_detector="sr")
    jobs = []
    for s in range(1, 9):
        jobs += [("CSL", s, 30000, best), ("HW", s, 30000, dict(propose_k=1, **tuned["HW"])), ("NRT", s, 30000, dict(propose_k=1))]
    t0 = time.time()
    with Pool(12) as p:
        res = p.map(job, jobs, chunksize=1)
    json.dump(res, open("proxy_results.json", "w"), indent=1)
    print("done", time.time() - t0)
