"""
H.1k — Recurring rules and certified hibernation ("memory as prior").
Stream: like config A, but when a rule is replaced, with prob. 0.6 the new rule is an OLD rule returning.
CSL-ARCH: retired claims go to an archive. Budget per 10k-step window (alpha = 0.1) is split:
    half for new residual-mined proposals (200 slots -> alpha_c = 0.05/200 = 2.5e-4),
    half for archived claims (at most A_max = 25 archive proposals per window -> alpha_c = 0.05/25 = 2e-3).
    Archived claims are re-proposed as soon as their feature set is among the top residual candidates,
    with their archived weight as a warm start. Union bound per window still gives <= 0.1 expected false admissions.
Compare: CSL (no archive), CSL-ARCH, HW (tuned), L1 (dense).  Metric: detection delay for RECURRING vs NEW rules.
"""
import numpy as np, json, time, math
from csl_experiment import Grower, Claim, RuleStream, CONFIGS, logloss, DenseL1
from multiprocessing import Pool


class RecurStream(RuleStream):
    def __init__(self, *a, recur=0.6, **k):
        super().__init__(*a, **k); self.recur = recur; self.pool = []; self.recurring_ids = set()

    def step(self):
        if self.K > 0 and self.t > 0 and self.t % self.drift == 0:
            i = int(self.rng.integers(self.K))
            old = self.rules[i]; self.ended[old["id"]] = self.t; self.pool.append(old)
            cands = [r for r in self.pool if all(tuple(r["feats"]) != tuple(q["feats"]) for q in self.rules)]
            if cands and self.rng.random() < self.recur:
                r = dict(cands[int(self.rng.integers(len(cands)))]); r["id"] = int(self.rng.integers(1 << 30))
                self.recurring_ids.add(r["id"])
            else:
                r = self._new_rule()
            self.rules[i] = r; self.history.append((self.t, r))
        x = (self.rng.random(self.d) < 0.5).astype(np.float64)
        logit = sum(r["beta"] * (self.phi(x, r["feats"]) - 0.5 ** len(r["feats"])) for r in self.rules)
        y = float(self.rng.random() < 1 / (1 + math.exp(-logit)))
        self.t += 1
        return x, y, logit


class ArchGrower(Grower):
    def __init__(self, d, rng, archive=True, **kw):
        super().__init__(d, "CSL", rng, **kw)
        self.use_archive = archive
        self.archive = {}                         # feats -> (weight, mu)
        self.arch_alpha = 0.05 / 25; self.arch_used = []   # timestamps of archive proposals (rate-limited per window)
        if archive:
            self.alpha_c = 0.05 / 200             # new proposals get half the window budget

    def step(self, t, x, y):
        before = set(self.accepted)
        loss = super().step(t, x, y)
        if self.use_archive:
            for f in before - set(self.accepted):          # just retired -> archive
                if f in self._last_acc:
                    c = self._last_acc[f]; self.archive[f] = (c.wc if c.wc else c.w, c.mu)
            # (a) a normal proposal made THIS step that matches an archived claim gets the archive budget and
            #     warm start (set before any evidence is collected -> still predictable/valid)
            self.arch_used = [s for s in self.arch_used if s > t - 10000]
            for f, c in self.pending.items():
                if c.born == t and f in self.archive and len(self.arch_used) < 25:
                    w, mu = self.archive.pop(f)
                    c.alpha = self.arch_alpha; c.w = w; c.sgn = 1.0 if w >= 0 else -1.0
                    self.arch_used.append(t)
            # (b) re-propose archived claims whose feature set ranks in the top residual candidates
            if t % 10 == 0 and self.archive:
                self.arch_used = [s for s in self.arch_used if s > t - 10000]
                if len(self.arch_used) < 25:
                    score = np.abs(self.cov) / np.sqrt(self.mphi * (1 - self.mphi) + 1e-6)
                    top = set(self.index_to_feats(i) for i in np.argsort(-score)[:10])
                    for f in list(self.archive):
                        if f in top and f not in self.pending and f not in self.accepted:
                            w, mu = self.archive.pop(f)
                            cl = Claim(f, t, self.arch_alpha); cl.w = w; cl.mu = mu
                            idx = f[0] if len(f) == 1 else None
                            cl.sgn = 1.0 if w >= 0 else -1.0
                            self.pending[f] = cl; self.arch_used.append(t)
                            break
        self._last_acc = dict(self.accepted)
        return loss


def job(args):
    policy, seed, N = args
    cfg = CONFIGS["A_pilot"]
    st = RecurStream(cfg["d"], cfg["K"], cfg["lo"], cfg["hi"], 4000, 0.5, np.random.default_rng(seed))
    best = dict(propose_k=1, adm_mode="score", ret_mode="statement", ret_detector="sr")
    rng = np.random.default_rng(seed + 12345)
    if policy == "CSL":
        g = ArchGrower(cfg["d"], rng, archive=False, **best)
    elif policy == "CSL-ARCH":
        g = ArchGrower(cfg["d"], rng, archive=True, **best)
    elif policy == "HW":
        g = Grower(cfg["d"], "HW", rng, propose_k=1, **json.load(open("tuned.json"))["HW"])
    else:
        g = DenseL1(cfg["d"], **json.load(open("tuned.json"))["L1"])
    g._last_acc = {}
    tot = 0.0
    for t in range(N):
        x, y, _ = st.step(); tot += g.step(t, x, y)
    out = dict(policy=policy, seed=seed, avg_loss=tot / N)
    if policy != "L1":
        dn, dr, spur = [], [], 0
        for (start, r) in st.history:
            if start == 0:
                continue
            end = st.ended.get(r["id"], N)
            evs = [(t, ev) for (t, ev, f) in g.log if tuple(f) == tuple(r["feats"])]
            held = bool([e for e in evs if e[0] < start]) and [e for e in evs if e[0] < start][-1][1] == "admit"
            hits = [t for (t, ev) in evs if ev == "admit" and t >= start]
            if held:
                dly = 0                                                   # claim still held when the rule (re)starts
            else:
                dly = (hits[0] - start) if hits and hits[0] < end else (end - start)   # censored at rule end
            (dr if r["id"] in st.recurring_ids else dn).append(dly)
        for (t, ev, f) in g.log:
            if ev == "admit" and not any(set(f) & a for a in st.active_feature_sets(t, 2000)):
                spur += 1
        out.update(delay_new=float(np.median(dn)) if dn else None, delay_recurring=float(np.median(dr)) if dr else None,
                   n_new=len(dn), n_recurring=len(dr), spurious=spur)
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        for p in ["CSL", "CSL-ARCH"]:
            print(json.dumps(job((p, 1, 20000))))
        sys.exit()
    jobs = [(p, s, 40000) for p in ["CSL", "CSL-ARCH", "HW", "L1"] for s in range(1, 9)]
    t0 = time.time()
    with Pool(12) as pool:
        res = pool.map(job, jobs, chunksize=1)
    json.dump(res, open("recur_results.json", "w"), indent=1)
    print("done", time.time() - t0)
