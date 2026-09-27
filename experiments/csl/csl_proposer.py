"""
H.1c — Prior-weighted error budgets: "proposer quality should change speed, never validity".

A proposer attaches a confidence q in (0,1] to each candidate. Budget per 10k-step window:
alpha_total = 0.1, split over 200 proposal slots, so alpha_c = 0.1 * q / 200 (union bound over the
window still gives E[spurious admissions per window] <= 0.1 for ANY proposer, even adversarial).

Proposers (simulated; 'good' and 'adversarial' peek at the true rules):
  residual    : residual mining (as in H.1), q = 1
  good        : 50%: an active true rule not yet held, q = 1 ; else random feature set, q = 0.05
  random      : random feature set, q = 1
  adversarial : random SPURIOUS feature set with q = 1 ; 10%: a true rule with q = 0.05
HW (threshold grower) is run with the same proposers, ignoring q.
"""
import numpy as np, json, sys, time
from csl_experiment import Grower, Claim, RuleStream, CONFIGS, logloss, pool_map


class ProposerGrower(Grower):
    def __init__(self, d, policy, rng, stream, proposer, **kw):
        super().__init__(d, policy, rng, **kw)
        self.pe = 10**9                                                # disable base proposals
        self.stream, self.proposer, self.prng = stream, proposer, rng
        self.slot, self.slots_per_window, self.alpha_total = 50, 200, 0.1

    def _random_feats(self, avoid_true):
        true_feats = set().union(*[set(r["feats"]) for r in self.stream.rules]) if self.stream.rules else set()
        for _ in range(100):
            if self.prng.random() < 0.5:
                f = (int(self.prng.integers(self.d)),)
            else:
                f = tuple(sorted(self.prng.choice(self.d, 2, replace=False).tolist()))
            if avoid_true and set(f) & true_feats:
                continue
            if f not in self.accepted and f not in self.pending:
                return f
        return None

    def step(self, t, x, y):
        loss = super().step(t, x, y)
        if t % self.slot == 0 and t > 200 and len(self.pending) < self.maxp:
            f, q = None, 1.0
            if self.proposer == "residual":
                score = np.abs(self.cov) / np.sqrt(self.mphi * (1 - self.mphi) + 1e-6)
                for i in np.argsort(-score)[:200]:
                    g = self.index_to_feats(i)
                    if g not in self.accepted and g not in self.pending:
                        f = g; break
            elif self.proposer == "good":
                todo = [tuple(r["feats"]) for r in self.stream.rules
                        if tuple(r["feats"]) not in self.accepted and tuple(r["feats"]) not in self.pending]
                if todo and self.prng.random() < 0.5:
                    f = todo[int(self.prng.integers(len(todo)))]; q = 1.0
                else:
                    f = self._random_feats(False); q = 0.05
            elif self.proposer == "random":
                f = self._random_feats(False); q = 1.0
            elif self.proposer == "adversarial":
                todo = [tuple(r["feats"]) for r in self.stream.rules
                        if tuple(r["feats"]) not in self.accepted and tuple(r["feats"]) not in self.pending]
                if todo and self.prng.random() < 0.1:
                    f = todo[int(self.prng.integers(len(todo)))]; q = 0.05
                else:
                    f = self._random_feats(True); q = 1.0
            if f is not None:
                cl = Claim(f, t, self.alpha_total * q / self.slots_per_window)
                cl.mu = 0.5 ** len(f)          # known design distribution; predictable
                self.pending[f] = cl
        return loss


def run_one(args):
    proposer, policy, seed, N, kw = args
    cfg = CONFIGS["A_pilot"]
    stream = RuleStream(cfg["d"], cfg["K"], cfg["lo"], cfg["hi"], cfg["drift"], 0.5, np.random.default_rng(seed))
    g = ProposerGrower(cfg["d"], policy, np.random.default_rng(seed + 777), stream, proposer, **kw)
    tot = 0.0
    for t in range(N):
        x, y, _ = stream.step()
        tot += g.step(t, x, y)
    spur = adm = 0
    for (t, ev, f) in g.log:
        if ev == "admit":
            adm += 1
            if not any(set(f) & a for a in stream.active_feature_sets(t, 2000)):
                spur += 1
    delays, missed = [], 0
    for (start, r) in stream.history:
        end = stream.ended.get(r["id"], N)
        hits = [t for (t, ev, f) in g.log if ev == "admit" and tuple(f) == tuple(r["feats"]) and t >= start]
        if hits and hits[0] < end:
            delays.append(hits[0] - start)
        else:
            missed += 1
    return dict(proposer=proposer, policy=policy, seed=seed, avg_loss=tot / N, admissions=adm, spurious=spur,
                det_delay_median=float(np.median(delays)) if delays else None, det_missed=missed)


if __name__ == "__main__":
    N = 20000
    tuned = json.load(open("tuned.json"))
    jobs = []
    for prop in ["residual", "good", "random", "adversarial"]:
        for s in range(1, 9):
            jobs.append((prop, "CSL", s, N, {}))
            jobs.append((prop, "HW", s, N, dict(tuned["HW"])))
    import multiprocessing as mp
    t0 = time.time()
    with mp.Pool(12) as p:
        res = p.map(run_one, jobs, chunksize=1)
    json.dump(res, open("proposer_results.json", "w"), indent=1)
    print("done", time.time() - t0)
