"""
H.1 — Certified Structural Learning (CSL) prototype.

Question: can a model that adds/removes structure ONLY through anytime-valid
e-process tests (a) keep spurious structure near the promised rate in every
setting without retuning, (b) still detect and retire rules fast enough to be
competitive in predictive loss, compared with:
  - HW : a windowed-threshold grower (thresholds tuned once on config A)
  - NRT: naive repeated significance testing (z-test re-checked every step)
  - L1 : a dense online L1-logistic learner over every candidate feature
  - ORACLE: the true logit (loss floor)

Stream: binary features x in {0,1}^d, label y ~ Bernoulli(sigmoid(sum_k beta_k * (phi_k(x) - E phi_k))).
phi_k is a single feature or a conjunction of two features. Every `drift` steps one rule
is replaced by a new random one.

All growers share: residual-mining proposals, online weight fitting, same budget.
Only the admission / retirement rule differs.
"""
import numpy as np, json, math, sys, time
from statistics import NormalDist

# ----------------------------------------------------------------------------- stream
class RuleStream:
    def __init__(self, d, K, beta_lo, beta_hi, drift, pair_frac, rng):
        self.d, self.K, self.lo, self.hi, self.drift, self.pf, self.rng = d, K, beta_lo, beta_hi, drift, pair_frac, rng
        self.rules = [self._new_rule() for _ in range(K)]
        self.history = [(0, r) for r in self.rules]   # (start_time, rule)
        self.ended = {}                                  # rule_id -> end_time
        self.t = 0

    def _new_rule(self):
        if self.rng.random() < self.pf:
            feats = tuple(sorted(self.rng.choice(self.d, 2, replace=False).tolist()))
        else:
            feats = (int(self.rng.integers(self.d)),)
        beta = self.rng.uniform(self.lo, self.hi) * self.rng.choice([-1, 1])
        return {"id": int(self.rng.integers(1 << 30)), "feats": feats, "beta": float(beta)}

    @staticmethod
    def phi(x, feats):
        return float(np.all(x[list(feats)] == 1))

    def step(self):
        if self.K > 0 and self.t > 0 and self.t % self.drift == 0:
            i = int(self.rng.integers(self.K))
            self.ended[self.rules[i]["id"]] = self.t
            self.rules[i] = self._new_rule()
            self.history.append((self.t, self.rules[i]))
        x = (self.rng.random(self.d) < 0.5).astype(np.float64)
        logit = 0.0
        for r in self.rules:
            e = 0.5 ** len(r["feats"])
            logit += r["beta"] * (self.phi(x, r["feats"]) - e)
        y = float(self.rng.random() < 1 / (1 + math.exp(-logit)))
        self.t += 1
        return x, y, logit

    def active_feature_sets(self, t, window):
        """feature sets of rules active at any time in [t-window, t]"""
        out = []
        for (start, r) in self.history:
            end = self.ended.get(r["id"], 10**12)
            if start <= t and end >= t - window:
                out.append(set(r["feats"]))
        return out


def logloss(z, y):
    # numerically stable log(1+exp(-s z)) with s = +-1
    s = 2 * y - 1
    m = -s * z
    return max(m, 0) + math.log1p(math.exp(-abs(m)))


def sigmoid(z):
    return 1 / (1 + math.exp(-z)) if z >= 0 else math.exp(z) / (1 + math.exp(z))


# ----------------------------------------------------------------------------- grower
LAMS = np.array([0.025, 0.05, 0.1, 0.2, 0.4, 0.8])   # mixture of fixed bets: average of e-processes is an e-process


def mix_log(lw):
    m = lw.max()
    return m + math.log(np.exp(lw - m).mean())

class Claim:
    __slots__ = ("feats", "w", "logW", "sZ", "sZ2", "n", "born", "hist", "alpha", "admitted_at",
                 "logWr", "sZr", "sZ2r", "nr", "histr", "lw", "lwr", "mu", "wc", "sgn")

    def __init__(self, feats, t, alpha):
        self.feats, self.w, self.born, self.alpha = feats, 0.0, t, alpha
        self.logW, self.sZ, self.sZ2, self.n, self.hist = 0.0, 0.0, 0.0, 0, []
        self.admitted_at = None
        self.logWr, self.sZr, self.sZ2r, self.nr, self.histr = 0.0, 0.0, 0.0, 0, []
        self.lw = np.zeros(len(LAMS)); self.lwr = np.zeros(len(LAMS))
        self.mu = 0.0   # centring constant, frozen at proposal time (predictable)
        self.wc = 0.0   # certified weight (frozen at admission) for statement-based retirement
        self.sgn = 1.0  # proposed direction (from residual mining; predictable)


class Grower:
    """policy in {'CSL','NRT','HW'}"""

    def __init__(self, d, policy, rng, alpha_rate=0.1, window=10000, propose_every=50, propose_k=2,
                 max_pending=40, patience=6000, min_life=1500, lr=0.05, wmax=3.0, delta_r=0.001, beta_c=0.01,
                 tau_a=0.003, tau_r=0.001, hw_win=300, lam_cap=0.9, bet="mix", dedup=False, warm=True, ret_mode="refit", ret_detector="martingale", arl=1e5, adm_mode="loss"):
        self.d, self.policy, self.rng = d, policy, rng
        self.iu = np.triu_indices(d, 1)
        self.nfeat = d + len(self.iu[0])
        self.alpha_c = alpha_rate / (window / propose_every * propose_k)  # per-candidate budget
        self.pe, self.pk, self.maxp, self.pat, self.minlife = propose_every, propose_k, max_pending, patience, min_life
        self.lr, self.wmax, self.dr, self.bc = lr, wmax, delta_r, beta_c
        self.tau_a, self.tau_r, self.hw_win, self.cap = tau_a, tau_r, hw_win, lam_cap
        self.bet, self.dedup, self.warm, self.ret_mode = bet, dedup, warm, ret_mode
        self.ret_detector, self.arl, self.adm_mode = ret_detector, arl, adm_mode
        self.z_adm = NormalDist().inv_cdf(1 - self.alpha_c)
        self.z_ret = NormalDist().inv_cdf(1 - beta_c)
        self.bias = 0.0
        self.accepted, self.pending = {}, {}
        self.cov = np.zeros(self.nfeat)      # EW mean of r * (phi - mean phi)
        self.mphi = np.full(self.nfeat, 0.3)
        self.decay = 0.999
        self.log = []                         # (t, event, feats)
        self.born_log = []                    # (admit_t, feats, proposal_t)

    def feat_vec(self, x):
        return np.concatenate([x, (x[:, None] * x[None, :])[self.iu]])

    def index_to_feats(self, i):
        if i < self.d:
            return (int(i),)
        j = i - self.d
        return (int(self.iu[0][j]), int(self.iu[1][j]))

    @staticmethod
    def phi(x, feats):
        return float(np.all(x[list(feats)] == 1))

    def logit(self, x, exclude=None):
        z = self.bias
        for f, c in self.accepted.items():
            if f != exclude:
                z += c.w * (self.phi(x, f) - c.mu)
        return z

    def _bet(self, sZ, sZ2):
        lam = sZ / (sZ2 + 0.25)
        return min(max(lam, 0.0), self.cap)

    def step(self, t, x, y):
        z = self.logit(x)
        p = sigmoid(z)
        loss = logloss(z, y)
        # ---------------- admission tests for pending candidates (predictable w)
        to_admit, to_drop = [], []
        for f, c in self.pending.items():
            u = self.phi(x, f) - c.mu            # centred feature, |u| <= 1
            if self.adm_mode == "score":
                # sequential score test: residual (y - p) correlates with u in the proposed direction
                D = loss - logloss(z + c.w * u, y)
                Z = c.sgn * (y - p) * u            # |Z| <= 1; mean <= 0 if no unexplained signal along u
            elif abs(c.w) > 1e-9:
                D = loss - logloss(z + c.w * u, y)  # |D| <= |w u| <= |w|
                Z = D / abs(c.w)
            else:
                D, Z = 0.0, 0.0
            if self.bet == "mix":
                c.lw += np.log1p(LAMS * Z); c.logW = mix_log(c.lw)
            else:
                lam = self._bet(c.sZ, c.sZ2)
                c.logW += math.log1p(lam * Z)
            c.sZ += Z; c.sZ2 += Z * Z; c.n += 1
            c.hist.append(D)
            # fit candidate weight on shadow model (after using it)
            g = sigmoid(z + c.w * u) - y
            c.w = float(np.clip(c.w - self.lr * g * u, -self.wmax, self.wmax))
            age = t - c.born
            if self._admit(c):
                to_admit.append(f)
            elif age > self.pat or (age > self.minlife and not self._promising(c)):
                to_drop.append(f)   # stopping a test never creates a false admission
        # ---------------- retirement tests for accepted claims
        to_retire = []
        for f, c in self.accepted.items():
            u = self.phi(x, f) - c.mu
            if self.ret_mode == "statement":
                # test the CERTIFIED statement (f, wc): does adding it to the model-without-c still help?
                z0 = z - c.w * u
                Dr = -(logloss(z0, y) - logloss(z0 + c.wc * u, y))   # >0 means the statement hurts
                Zr = (Dr + self.dr) / (abs(c.wc) + self.dr)
            else:
                Dr = loss - logloss(z - c.w * u, y)   # >0 means removing c would help; |Dr| <= |w|
                Zr = (Dr + self.dr) / (abs(c.w) + self.dr)
            if self.ret_detector == "sr":
                # Shiryaev-Roberts e-detector per bet size: R <- (1 + R)(1 + lam Z); mean over bets.
                # R_t - t is a supermartingale while c stays useful  =>  average run length to a false retirement >= arl
                c.lwr = np.logaddexp(0.0, c.lwr) + np.log1p(LAMS * Zr); c.logWr = mix_log(c.lwr)
            elif self.bet == "mix":
                c.lwr += np.log1p(LAMS * Zr); c.logWr = mix_log(c.lwr)
            else:
                lam = self._bet(c.sZr, c.sZ2r)
                c.logWr += math.log1p(lam * Zr)
            c.sZr += Zr; c.sZ2r += Zr * Zr; c.nr += 1
            c.histr.append(Dr)
            if t - c.admitted_at > 50 and self._retire(c):
                to_retire.append(f)
        # ---------------- update main model weights (SGD on log loss)
        g = p - y
        self.bias -= self.lr * g
        for f, c in self.accepted.items():
            u = self.phi(x, f) - c.mu
            c.w = float(np.clip(c.w - self.lr * g * u, -self.wmax, self.wmax))
        # ---------------- apply structural changes
        for f in to_retire:
            del self.accepted[f]; self.log.append((t, "retire", f))
        for f in to_admit:
            c = self.pending.pop(f)
            c.admitted_at = t
            c.wc = c.w
            self.born_log.append((t, f, c.born))
            self.accepted[f] = c
            self.log.append((t, "admit", f))
            # duplicate suppression: down-scale wealth of overlapping pending claims (always valid)
            for g2, c2 in (self.pending.items() if self.dedup else []):
                if set(g2) & set(f):
                    c2.logW = min(c2.logW, 0.0); c2.sZ = min(c2.sZ, 0.0)
        for f in to_drop:
            self.pending.pop(f, None)
        # ---------------- residual mining + proposals
        fv = self.feat_vec(x)
        self.mphi = self.decay * self.mphi + (1 - self.decay) * fv
        r = y - p
        self.cov = self.decay * self.cov + (1 - self.decay) * r * (fv - self.mphi)
        if t % self.pe == 0 and t > 200 and len(self.pending) < self.maxp:
            score = np.abs(self.cov) / np.sqrt(self.mphi * (1 - self.mphi) + 1e-6)
            order = np.argsort(-score)
            added = 0
            for i in order[:200]:
                f = self.index_to_feats(i)
                if f in self.accepted or f in self.pending:
                    continue
                cl = Claim(f, t, self.alpha_c)
                cl.mu = float(self.mphi[i])
                cl.sgn = 1.0 if self.cov[i] >= 0 else -1.0
                v = self.mphi[i] * (1 - self.mphi[i]) + 1e-6
                cl.w = float(np.clip(4.0 * self.cov[i] / v, -self.wmax, self.wmax)) if self.warm else 0.0
                self.pending[f] = cl
                added += 1
                if added >= self.pk:
                    break
        return loss

    def _promising(self, c):
        if self.policy == "CSL":
            return c.logW > 1.0
        if self.policy == "LR":
            return sum(c.hist) > 1.0
        return False          # HW / NRT admit early if at all; drop after min_life

    def _admit(self, c):
        if self.policy == "CSL":
            return c.logW >= math.log(1 / c.alpha)
        if self.policy == "LR":
            # plug-in likelihood-ratio "wealth" exp(sum D): the Bayes-factor-style rule. NOT a valid e-process
            # for the composite null (current model misspecified), included to show why betting matters.
            return sum(c.hist) >= math.log(1 / c.alpha)
        if self.policy == "NRT":
            if c.n < 50:
                return False
            h = np.asarray(c.hist); m = h.mean(); s = h.std() + 1e-12
            return m / (s / math.sqrt(len(h))) > self.z_adm
        if self.policy == "HW":
            if c.n < self.hw_win:
                return False
            return float(np.mean(c.hist[-self.hw_win:])) > self.tau_a
        raise ValueError

    def _retire(self, c):
        if self.policy in ("CSL", "LR"):
            if self.ret_detector == "sr":
                return c.logWr >= math.log(self.arl)
            return c.logWr >= math.log(1 / self.bc)
        if self.policy == "NRT":
            if c.nr < 50:
                return False
            h = -np.asarray(c.histr[-5000:]); m = h.mean(); s = h.std() + 1e-12   # usefulness
            return (self.dr - m) / (s / math.sqrt(len(h))) > self.z_ret
        if self.policy == "HW":
            if c.nr < self.hw_win:
                return False
            return float(np.mean(-np.asarray(c.histr[-self.hw_win:]))) < self.tau_r
        raise ValueError


class FTRL:
    """FTRL-Proximal (McMahan et al. 2013): per-coordinate adaptive L1/L2 online logistic regression over all candidates."""
    def __init__(self, d, alpha=0.1, beta=1.0, l1=1.0, l2=1.0, thr=0.2, gamma=1.0):
        self.gamma = gamma                                # <1: exponential forgetting (tracks drift)
        self.iu = np.triu_indices(d, 1); self.d = d
        n = d + len(self.iu[0]) + 1                       # +1 bias
        self.z = np.zeros(n); self.nn = np.zeros(n)
        self.a, self.b, self.l1, self.l2, self.thr = alpha, beta, l1, l2, thr

    def _w(self, idx):
        z, n = self.z[idx], self.nn[idx]
        w = -(z - np.sign(z) * self.l1) / ((self.b + np.sqrt(n)) / self.a + self.l2)
        w[np.abs(z) <= self.l1] = 0.0
        return w

    def step(self, t, x, y):
        fv = np.concatenate([x, (x[:, None] * x[None, :])[self.iu], [1.0]])
        idx = np.nonzero(fv)[0]
        w = self._w(idx)
        zlog = float(w @ fv[idx])
        loss = logloss(zlog, y)
        g = (sigmoid(zlog) - y) * fv[idx]
        sig = (np.sqrt(self.nn[idx] + g * g) - np.sqrt(self.nn[idx])) / self.a
        self.z[idx] += g - sig * w
        self.nn[idx] += g * g
        if self.gamma < 1.0:
            self.z *= self.gamma; self.nn *= self.gamma
        return loss

    def structure(self):
        w = self._w(np.arange(len(self.z) - 1))
        out = []
        for i in np.nonzero(np.abs(w) > self.thr)[0]:
            out.append((int(i),) if i < self.d else (int(self.iu[0][i - self.d]), int(self.iu[1][i - self.d])))
        return out


class EGpm:
    """Exponentiated gradient +/- (Kivinen & Warmuth 1997) over all candidates, L1 radius U, with fixed-share
    mixing gamma (Herbster & Warmuth 1998) so it can track drift. Regret ~ U * sqrt(T log n)."""
    def __init__(self, d, eta=0.05, U=8.0, gamma=1e-4, lr_b=0.02):
        self.iu = np.triu_indices(d, 1); self.d = d
        n = d + len(self.iu[0]); self.n = n
        self.wp = np.full(n, U / (2 * n)); self.wm = np.full(n, U / (2 * n))
        self.eta, self.U, self.gamma, self.b, self.lr_b = eta, U, gamma, 0.0, lr_b

    def step(self, t, x, y):
        fv = np.concatenate([x, (x[:, None] * x[None, :])[self.iu]]) - 0.5 * 0   # uncentred binary features
        w = self.wp - self.wm
        z = self.b + float(w @ fv)
        loss = logloss(z, y)
        g = (sigmoid(z) - y)
        self.b -= self.lr_b * g
        gi = g * fv
        self.wp *= np.exp(-self.eta * gi); self.wm *= np.exp(self.eta * gi)
        s = self.wp.sum() + self.wm.sum()
        self.wp *= self.U / s; self.wm *= self.U / s
        if self.gamma > 0:
            share = self.gamma * self.U / (2 * self.n)
            self.wp = (1 - self.gamma) * self.wp + share; self.wm = (1 - self.gamma) * self.wm + share
        return loss

    def structure(self):
        w = self.wp - self.wm
        out = []
        for i in np.nonzero(np.abs(w) > 0.2)[0]:
            out.append((int(i),) if i < self.d else (int(self.iu[0][i - self.d]), int(self.iu[1][i - self.d])))
        return out


class DenseL1:
    def __init__(self, d, lr=0.02, l1=2e-4, thr=0.2):
        self.iu = np.triu_indices(d, 1)
        self.d = d
        self.w = np.zeros(d + len(self.iu[0])); self.b = 0.0
        self.lr, self.l1, self.thr = lr, l1, thr

    def step(self, t, x, y):
        fv = np.concatenate([x, (x[:, None] * x[None, :])[self.iu]])
        z = self.b + float(self.w @ fv)
        loss = logloss(z, y)
        g = sigmoid(z) - y
        self.b -= self.lr * g
        self.w -= self.lr * g * fv
        self.w = np.sign(self.w) * np.maximum(np.abs(self.w) - self.lr * self.l1, 0)   # truncated gradient
        return loss

    def structure(self):
        idx = np.nonzero(np.abs(self.w) > self.thr)[0]
        out = []
        for i in idx:
            if i < self.d:
                out.append((int(i),))
            else:
                j = i - self.d; out.append((int(self.iu[0][j]), int(self.iu[1][j])))
        return out


# ----------------------------------------------------------------------------- evaluation
def run(config, policy, seed, N, **kw):
    rng_s = np.random.default_rng(seed)
    stream = RuleStream(config["d"], config["K"], config["lo"], config["hi"], config["drift"], 0.5, rng_s)
    rng_m = np.random.default_rng(seed + 12345)
    if policy == "L1":
        model = DenseL1(config["d"], **{k: v for k, v in kw.items() if k in ("lr", "l1", "thr")})
    elif policy == "FTRL":
        model = FTRL(config["d"], **kw)
    elif policy == "EG":
        model = EGpm(config["d"], **kw)
    elif policy == "ORACLE":
        model = None
    else:
        model = Grower(config["d"], policy, rng_m, **kw)   # CSL / NRT / HW / LR
    tot, tot_oracle = 0.0, 0.0
    spurious_L1_samples = []
    for t in range(N):
        x, y, true_logit = stream.step()
        tot_oracle += logloss(true_logit, y)
        if model is None:
            continue
        tot += model.step(t, x, y)
        if policy in ("L1", "FTRL", "EG") and t % 1000 == 999:
            act = stream.active_feature_sets(t, 2000)
            sp = sum(1 for f in model.structure() if not any(set(f) & a for a in act))
            spurious_L1_samples.append(sp)
    res = {"policy": policy, "seed": seed, "avg_loss": tot / N if model else tot_oracle / N,
           "oracle_loss": tot_oracle / N}
    if policy in ("CSL", "NRT", "HW", "LR"):
        # spurious admissions: admitted claim disjoint from every rule active within 2000 steps of admission
        spur, adm = 0, 0
        for (t, ev, f) in model.log:
            if ev == "admit":
                adm += 1
                act = stream.active_feature_sets(t, 2000)
                if not any(set(f) & a for a in act):
                    spur += 1
        # detection delay: first admission of an exactly matching claim after rule start
        delays, missed = [], 0
        for (start, r) in stream.history:
            end = stream.ended.get(r["id"], N)
            hits = [t for (t, ev, f) in model.log if ev == "admit" and tuple(f) == tuple(r["feats"]) and t >= start]
            if hits and hits[0] < end:
                delays.append(hits[0] - start)
            else:
                missed += 1
        # retirement delay: claims that intersect ONLY an ended rule; time until retired
        rdel, rmiss = [], 0
        for rid, tend in stream.ended.items():
            rule = [r for (_, r) in stream.history if r["id"] == rid][0]
            fs = set(rule["feats"])
            for (t, ev, f) in model.log:
                if ev != "admit" or t > tend or not (set(f) & fs):
                    continue
                later = [t2 for (t2, ev2, f2) in model.log if ev2 == "retire" and f2 == f and t2 >= tend]
                # only count if f does not also touch a rule that is still active
                still = stream.active_feature_sets(tend + 1, 0)
                if any(set(f) & a for a in still):
                    continue
                if later:
                    rdel.append(later[0] - tend)
                else:
                    rmiss += 1
        false_ret = 0
        for (t, ev, f) in model.log:
            if ev == "retire" and any(set(f) == a for a in stream.active_feature_sets(t, 0)):
                false_ret += 1
        res.update(dict(admissions=adm, spurious=spur, final_size=len(model.accepted), false_retire=false_ret,
                        det_delay_median=float(np.median(delays)) if delays else None,
                        det_missed=missed, n_new_rules=len(delays) + missed,
                        ret_delay_median=float(np.median(rdel)) if rdel else None, ret_missed=rmiss))
    if policy in ("L1", "FTRL", "EG"):
        res.update(dict(spurious_avg_structure=float(np.mean(spurious_L1_samples)),
                        final_size=len(model.structure())))
    return res


CONFIGS = {
    "A_pilot":   dict(d=40,  K=4, lo=1.0, hi=2.0, drift=6000),
    "B_highdim": dict(d=150, K=4, lo=1.0, hi=2.0, drift=6000),
    "C_weak":    dict(d=40,  K=4, lo=0.4, hi=0.8, drift=6000),
    "D_null":    dict(d=40,  K=0, lo=1.0, hi=2.0, drift=6000),
}

def _job(args):
    cfg_name, pol, seed, N, kw = args
    r = run(CONFIGS[cfg_name], pol, seed, N, **kw)
    r["config"] = cfg_name; r["kw"] = kw
    return r


def pool_map(jobs, procs=12):
    from multiprocessing import Pool
    with Pool(procs) as p:
        return p.map(_job, jobs, chunksize=1)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "quick"
    N = 30000
    if mode == "tune":
        jobs = []
        for ta in [0.0, 0.002, 0.005, 0.01, 0.02]:
            for tr in [0.0, 0.001, 0.003]:
                for s in [101, 102, 103]:
                    jobs.append(("A_pilot", "HW", s, N, dict(tau_a=ta, tau_r=tr, propose_k=1)))
        for lr in [0.0005, 0.002, 0.008]:
            for l1 in [1e-4, 1e-3, 5e-3]:
                for s in [101, 102, 103]:
                    jobs.append(("A_pilot", "L1", s, N, dict(lr=lr, l1=l1)))
        t0 = time.time(); res = pool_map(jobs)
        json.dump(res, open("tune_results.json", "w"), indent=1)
        print("tuning done", time.time() - t0)
    if mode == "lr":
        jobs = []
        for cfg in CONFIGS:
            for s in range(1, 9):
                jobs.append((cfg, "LR", s, N, dict(propose_k=1, ret_mode="statement", ret_detector="sr")))
        t0 = time.time(); res = pool_map(jobs)
        json.dump(res, open("eval_lr.json", "w"), indent=1)
        print("lr eval done", time.time() - t0)
    if mode == "score":
        jobs = []
        for cfg in CONFIGS:
            for s in range(1, 9):
                jobs.append((cfg, "CSL", s, N, dict(propose_k=1, ret_mode="statement", ret_detector="sr", adm_mode="score")))
        t0 = time.time(); res = pool_map(jobs)
        json.dump(res, open("eval_score.json", "w"), indent=1)
        print("score eval done", time.time() - t0)
    if mode == "retire":
        jobs = []
        for cfg in CONFIGS:
            for s in range(1, 9):
                jobs.append((cfg, "CSL", s, N, dict(propose_k=1, ret_mode="statement", ret_detector="sr")))
                jobs.append((cfg, "CSL", s, N, dict(propose_k=1, ret_mode="refit", ret_detector="sr")))
        t0 = time.time(); res = pool_map(jobs)
        json.dump(res, open("eval_statement.json", "w"), indent=1)
        print("retire eval done", time.time() - t0)
    if mode == "eval":
        tuned = json.load(open("tuned.json"))
        jobs = []
        for cfg in CONFIGS:
            for s in range(1, 9):
                jobs.append((cfg, "CSL", s, N, dict(propose_k=1)))
                jobs.append((cfg, "NRT", s, N, dict(propose_k=1)))
                jobs.append((cfg, "HW", s, N, dict(propose_k=1, **tuned["HW"])))
                jobs.append((cfg, "L1", s, N, dict(**tuned["L1"])))
                jobs.append((cfg, "ORACLE", s, N, {}))
        t0 = time.time(); res = pool_map(jobs)
        json.dump(res, open("eval_results.json", "w"), indent=1)
        print("eval done", time.time() - t0)
    if mode == "quick":
        t0 = time.time()
        for pol in ["CSL", "HW", "NRT", "ORACLE"]:
            r = run(CONFIGS["A_pilot"], pol, 1, 12000, propose_k=1)
            print(json.dumps(r))
        print("elapsed", time.time() - t0)
