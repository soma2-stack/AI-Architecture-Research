"""
H.1e — Warranted World Model (R01): CSL as the structure learner of a programmatic world model
whose physical laws CHANGE over time.

World: 9x9 grid, cell types {0 empty, 1 ice, 2 mud, 3 conveyor-x, 4 conveyor-y, 5 spring, 6 wall};
8 = out of bounds (as a context type). Agent takes random actions (N,E,S,W). Layout re-randomised every
100 steps. Laws (can change every `drift` steps):
  ice    : entering ice slides one more step (if free)            [on/off]
  spring : entering a spring moves two more steps (each if free)  [on/off]
  mud    : starting on mud, the move fails with prob. p          [p in {0, .3, .6, .9}]
  convX  : entering conveyor-x pushes by kx in x                  [kx in {-1, 0, 1}]
  convY  : entering conveyor-y pushes by ky in y                  [ky in {-1, 0, 1}]
Target: agent displacement (dx, dy) in [-3,3]^2 -> 49 classes.

Model (log-linear product of laws): logits = bias[action] + sum_{laws c} w_c * (1[P_c] - mu_c) * e_{o_c}
  precondition P = (slot in {here, ahead1, ahead2}, type) optionally AND action;  outcome o = class.
Policies: CSL (score-test admission, Shiryaev-Roberts statement retirement), HW (thresholds),
          L1POE (all 120*49 candidate laws fitted by online L1-SGD, "fit then prune" like PoE-World),
          MLP (neural world model), ORACLE (exact outcome distribution).
False law: at admission, adding the law does NOT reduce the true expected log-loss (Monte Carlo over
fresh contexts, exact expectation over outcomes).
"""
import numpy as np, math, json, sys, time

LAMS = np.array([0.025, 0.05, 0.1, 0.2, 0.4, 0.8])
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]          # N, E, S, W   (y grows downward)
NT = 9                                              # context types 0..8
NO = 49
NOL = 98          # law outcome space: 49 absolute + 49 action-relative


def rel_to_abs(ol, a):
    """map a law outcome (absolute 0..48, or action-relative 49..97 = forward f, lateral l) to an absolute class"""
    if ol < 49:
        return ol
    q = ol - 49; f, l = q // 7 - 3, q % 7 - 3           # forward, lateral (lateral = rotate forward by +90deg)
    dx, dy = DIRS[a]; lx, ly = -dy, dx
    return ocls(f * dx + l * lx, f * dy + l * ly)


def mix_log(lw):
    m = lw.max(); return m + math.log(np.exp(lw - m).mean())


def lse(z):
    m = z.max(); return m + math.log(np.exp(z - m).sum())


def ocls(dx, dy):
    return (max(-3, min(3, dy)) + 3) * 7 + (max(-3, min(3, dx)) + 3)


class LawWorld:
    def __init__(self, rng, size=9, drift=5000):
        self.rng, self.S, self.drift = rng, size, drift
        self.laws = dict(ice=1, spring=1, mud=0.6, convX=1, convY=1)
        self.t = 0; self.changes = []
        self.new_layout()

    def new_layout(self):
        p = [0.52, 0.1, 0.1, 0.06, 0.06, 0.06, 0.10]
        self.grid = self.rng.choice(7, (self.S, self.S), p=p)
        free = np.argwhere(self.grid != 6)
        self.pos = tuple(free[self.rng.integers(len(free))][::-1])  # (x, y)

    def typ(self, x, y, grid=None):
        g = self.grid if grid is None else grid
        if x < 0 or y < 0 or x >= self.S or y >= self.S:
            return 8
        return int(g[y, x])

    def free(self, x, y, grid=None):
        t = self.typ(x, y, grid); return t != 8 and t != 6

    def context(self, pos, a, grid=None):
        dx, dy = DIRS[a]; x, y = pos
        return (self.typ(x, y, grid), self.typ(x + dx, y + dy, grid), self.typ(x + 2 * dx, y + 2 * dy, grid))

    def outcome_dist(self, pos, a, grid=None, laws=None):
        """exact distribution over outcome classes (only mud is stochastic)"""
        L = self.laws if laws is None else laws
        x0, y0 = pos; dx, dy = DIRS[a]
        def det():
            x, y = x0, y0
            if not self.free(x + dx, y + dy, grid):
                return x, y
            x, y = x + dx, y + dy
            t = self.typ(x, y, grid)
            if t == 1 and L["ice"] and self.free(x + dx, y + dy, grid):
                x, y = x + dx, y + dy
            elif t == 5 and L["spring"]:
                for _ in range(2):
                    if self.free(x + dx, y + dy, grid):
                        x, y = x + dx, y + dy
            elif t == 3 and L["convX"] and self.free(x + L["convX"], y, grid):
                x += L["convX"]
            elif t == 4 and L["convY"] and self.free(x, y + L["convY"], grid):
                y += L["convY"]
            return x, y
        xf, yf = det()
        d = {}
        pf = L["mud"] if self.typ(x0, y0, grid) == 2 else 0.0
        if pf > 0:
            d[ocls(0, 0)] = d.get(ocls(0, 0), 0) + pf
        d[ocls(xf - x0, yf - y0)] = d.get(ocls(xf - x0, yf - y0), 0) + (1 - pf)
        return d, (xf, yf)

    def maybe_drift(self):
        if self.t > 0 and self.t % self.drift == 0:
            k = ["ice", "spring", "mud", "convX", "convY"][int(self.rng.integers(5))]
            if k in ("ice", "spring"):
                self.laws[k] = 1 - self.laws[k]
            elif k == "mud":
                self.laws[k] = float(self.rng.choice([v for v in [0.0, 0.3, 0.6, 0.9] if v != self.laws[k]]))
            else:
                self.laws[k] = int(self.rng.choice([v for v in [-1, 0, 1] if v != self.laws[k]]))
            self.changes.append((self.t, k, self.laws[k]))

    def step(self):
        self.maybe_drift()
        if self.t % 100 == 0:
            self.new_layout()
        a = int(self.rng.integers(4))
        ctx = self.context(self.pos, a)
        dist, _ = self.outcome_dist(self.pos, a)
        keys = list(dist.keys()); probs = np.array([dist[k] for k in keys])
        o = keys[int(self.rng.choice(len(keys), p=probs / probs.sum()))]
        # move the agent according to the realised outcome
        dy, dx = o // 7 - 3, o % 7 - 3
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        self.t += 1
        return a, ctx, o, dist

    def sample_contexts(self, n, rng):
        """fresh (grid, pos, a) samples from the current world's context distribution"""
        out = []
        for _ in range(n):
            p = [0.52, 0.1, 0.1, 0.06, 0.06, 0.06, 0.10]
            grid = rng.choice(7, (self.S, self.S), p=p)
            free = np.argwhere(grid != 6)
            pos = tuple(free[rng.integers(len(free))][::-1]); a = int(rng.integers(4))
            out.append((grid, pos, a))
        return out


# preconditions: index = slot*NT + type  (27)  and  27 + (slot*NT + type)*4 + a  (108)
NP = 3 * NT + 3 * NT * 4


def active_preconds(ctx, a):
    base = [s * NT + ctx[s] for s in range(3)]
    return base + [3 * NT + (s * NT + ctx[s]) * 4 + a for s in range(3)]


class Law:
    def __init__(self, P, o, t, alpha, mu, sgn):
        self.P, self.ol, self.born, self.alpha, self.mu, self.sgn = P, o, t, alpha, mu, sgn
        self.o = o if o < 49 else 0
        self.w = 0.0; self.wc = 0.0; self.lw = np.zeros(len(LAMS)); self.logW = 0.0; self.hist = []
        self.lwr = np.zeros(len(LAMS)); self.logWr = 0.0; self.histr = []; self.admitted_at = None


class Grower:
    def __init__(self, policy, lr=0.1, alpha_rate=0.1, window=10000, pe=50, maxp=60, min_life=1500,
                 patience=6000, delta_r=0.0005, arl=1e5, tau_a=0.003, tau_r=0.0, hw_win=300, wmax=4.0, pk=4, center=True):
        self.policy, self.lr, self.pe, self.maxp, self.minlife, self.pat = policy, lr, pe, maxp, min_life, patience
        self.alpha_c = alpha_rate / (window / pe * pk); self.pk = pk; self.center = center
        self.dr, self.arl, self.tau_a, self.tau_r, self.hw, self.wmax = delta_r, arl, tau_a, tau_r, hw_win, wmax
        self.bias = np.zeros((4, NO)); self.accepted, self.pending = {}, {}
        self.cov = np.zeros((NP, NOL)); self.mP = np.full(NP, 0.1); self.decay = 0.999
        self.log = []

    def logits(self, a, act, exclude=None):
        z = self.bias[a].copy()
        for k, c in self.accepted.items():
            if k != exclude:
                z[rel_to_abs(c.ol, a)] += c.w * ((c.P in act) - c.mu)
        return z

    def step(self, t, a, ctx, o):
        act = set(active_preconds(ctx, a))
        z = self.logits(a, act); L = lse(z); loss = L - z[o]
        p = np.exp(z - L)
        to_admit, to_drop = [], []
        for k, c in self.pending.items():
            u = (c.P in act) - c.mu; c.o = rel_to_abs(c.ol, a)
            zc = z.copy(); zc[c.o] += c.w * u
            D = loss - (lse(zc) - zc[c.o])
            Z = c.sgn * ((o == c.o) - p[c.o]) * u           # sequential score test, |Z| <= 1
            c.lw += np.log1p(LAMS * Z); c.logW = mix_log(c.lw); c.hist.append(D)
            pc = np.exp(zc - lse(zc)); c.w = float(np.clip(c.w - self.lr * (pc[c.o] - (o == c.o)) * u, -self.wmax, self.wmax))
            age = t - c.born
            if self._admit(c):
                to_admit.append(k)
            elif age > self.pat or (age > self.minlife and not (self.policy == "CSL" and c.logW > 1.0)):
                to_drop.append(k)
        to_retire = []
        for k, c in self.accepted.items():
            u = (c.P in act) - c.mu; c.o = rel_to_abs(c.ol, a)
            z0 = z.copy(); z0[c.o] -= c.w * u
            z1 = z0.copy(); z1[c.o] += c.wc * u
            Dr = -((lse(z0) - z0[o]) - (lse(z1) - z1[o]))       # >0: the certified statement hurts
            Zr = (Dr + self.dr) / (abs(c.wc) + self.dr)
            c.lwr = np.logaddexp(0.0, c.lwr) + np.log1p(LAMS * Zr); c.logWr = mix_log(c.lwr); c.histr.append(Dr)
            if t - c.admitted_at > 50 and self._retire(c):
                to_retire.append(k)
        g = p.copy(); g[o] -= 1
        self.bias[a] -= self.lr * g
        for k, c in self.accepted.items():
            u = (c.P in act) - c.mu; c.o = rel_to_abs(c.ol, a)
            c.w = float(np.clip(c.w - self.lr * g[c.o] * u, -self.wmax, self.wmax))
        for k in to_retire:
            del self.accepted[k]; self.log.append((t, "retire", k))
        for k in to_admit:
            c = self.pending.pop(k); c.admitted_at = t; c.wc = c.w; self.accepted[k] = c; self.log.append((t, "admit", k))
        for k in to_drop:
            self.pending.pop(k, None)
        # residual mining
        ind = np.zeros(NP); ind[list(act)] = 1
        self.mP = self.decay * self.mP + (1 - self.decay) * ind
        r = -g
        rl = np.concatenate([r, np.array([r[rel_to_abs(49 + q, a)] for q in range(49)])])
        self.cov = self.decay * self.cov + (1 - self.decay) * np.outer(ind - self.mP, rl)
        if t % self.pe == 0 and t > 200 and len(self.pending) < self.maxp:
            sc = np.abs(self.cov) / np.sqrt(self.mP * (1 - self.mP) + 1e-6)[:, None]
            flat = np.argsort(-sc, axis=None)[:300]
            added = 0
            for idx in flat:
                P, oo = divmod(int(idx), NOL)
                if (P, oo) in self.accepted or (P, oo) in self.pending:
                    continue
                self.pending[(P, oo)] = Law(P, oo, t, self.alpha_c, float(self.mP[P]) if self.center else 0.0,
                                            1.0 if self.cov[P, oo] >= 0 else -1.0)
                added += 1
                if added >= self.pk or len(self.pending) >= self.maxp:
                    break
        return loss

    def _admit(self, c):
        if self.policy == "CSL":
            return c.logW >= math.log(1 / c.alpha)
        return len(c.hist) >= self.hw and np.mean(c.hist[-self.hw:]) > self.tau_a

    def _retire(self, c):
        if self.policy == "CSL":
            return c.logWr >= math.log(self.arl)
        return len(c.histr) >= self.hw and np.mean(-np.asarray(c.histr[-self.hw:])) < self.tau_r


class L1POE:
    """every candidate law (P, o) has a weight; online L1-SGD (sparse: only active preconditions)"""
    def __init__(self, lr=0.05, l1=1e-3, thr=0.2):
        self.W = np.zeros((NP, NO)); self.bias = np.zeros((4, NO)); self.lr, self.l1, self.thr = lr, l1, thr

    def step(self, t, a, ctx, o):
        act = active_preconds(ctx, a)
        z = self.bias[a] + self.W[act].sum(0); L = lse(z); loss = L - z[o]
        g = np.exp(z - L); g[o] -= 1
        self.bias[a] -= self.lr * g
        self.W[act] -= self.lr * g
        self.W[act] = np.sign(self.W[act]) * np.maximum(np.abs(self.W[act]) - self.lr * self.l1, 0)
        return loss

    def size(self):
        return int((np.abs(self.W) > self.thr).sum())


class MLPWM:
    def __init__(self, rng, H=64, lr=0.05):
        din = 3 * NT + 4
        self.W1 = rng.normal(0, 1 / math.sqrt(din), (H, din)); self.b1 = np.zeros(H)
        self.W2 = np.zeros((NO, H)); self.b2 = np.zeros(NO); self.lr = lr

    def step(self, t, a, ctx, o):
        x = np.zeros(3 * NT + 4); x[[s * NT + ctx[s] for s in range(3)]] = 1; x[3 * NT + a] = 1
        h = np.tanh(self.W1 @ x + self.b1); z = self.W2 @ h + self.b2
        L = lse(z); loss = L - z[o]; g = np.exp(z - L); g[o] -= 1
        gh = (self.W2.T @ g) * (1 - h ** 2)
        self.W2 -= self.lr * np.outer(g, h); self.b2 -= self.lr * g
        self.W1 -= self.lr * np.outer(gh, x); self.b1 -= self.lr * gh
        return loss


def true_scores(world, model, key, rng, n=600):
    """under TRUE dynamics, for the model WITHOUT law `key`: (expected score s*(1[y=o]-p_o)*u, expected loss
    reduction from adding the law with its current weight).  score <= 0  <=>  the certified 'need' was false."""
    c = model.accepted[key]; sc = us = 0.0
    for grid, pos, a in world.sample_contexts(n, rng):
        ctx = world.context(pos, a, grid); act = set(active_preconds(ctx, a))
        dist, _ = world.outcome_dist(pos, a, grid)
        zw = model.logits(a, act); z0 = model.logits(a, act, exclude=key)
        Lw, L0 = lse(zw), lse(z0); p0 = np.exp(z0 - L0)
        o = rel_to_abs(c.ol, a); u = (c.P in act) - c.mu
        sc += c.sgn * u * (dist.get(o, 0.0) - p0[o])
        us += sum(pr * ((L0 - z0[k]) - (Lw - zw[k])) for k, pr in dist.items())
    return sc / n, us / n


def run(args):
    policy, seed, N, kw = args
    world = LawWorld(np.random.default_rng(seed))
    rng_m = np.random.default_rng(seed + 50)
    if policy in ("CSL", "HW"):
        model = Grower(policy, **kw)
    elif policy == "L1POE":
        model = L1POE(**kw)
    elif policy == "MLP":
        model = MLPWM(rng_m, **kw)
    else:
        model = None
    tot, tot_o, post, post_o = 0.0, 0.0, [], []
    false_adm, adm, harmful = 0, 0, 0
    for t in range(N):
        a, ctx, o, dist = world.step()
        lo = -math.log(dist[o]); tot_o += lo
        if model is None:
            continue
        n0 = len(getattr(model, "log", []))
        l = model.step(t, a, ctx, o); tot += l
        if world.changes and 0 <= t - world.changes[-1][0] < 1000:
            post.append(l); post_o.append(lo)
        if policy in ("CSL", "HW"):
            for (tt, ev, k) in model.log[n0:]:
                if ev == "admit":
                    adm += 1
                    s_, u_ = true_scores(world, model, k, np.random.default_rng(seed * 1000 + tt))
                    false_adm += int(s_ <= 0); harmful += int(u_ <= 0)
    res = dict(policy=policy, seed=seed, kw=kw, avg_loss=(tot if model else tot_o) / N, oracle=tot_o / N,
               post_change_regret=(float(np.mean(post) - np.mean(post_o)) if post else None), n_changes=len(world.changes))
    if policy in ("CSL", "HW"):
        res.update(admissions=adm, false_admissions=false_adm, harmful_at_admission=harmful, final_size=len(model.accepted))
    if policy == "L1POE":
        res.update(final_size=model.size())
    return res


if __name__ == "__main__":
    mode = sys.argv[1]
    import multiprocessing as mp
    N = 30000
    if mode == "quick":
        for pol, kw in [("CSL", {}), ("HW", {}), ("L1POE", {}), ("MLP", {}), ("ORACLE", {})]:
            t0 = time.time(); print(json.dumps(run((pol, 1, 8000, kw))), round(time.time() - t0, 1), flush=True)
    if mode == "tune":
        jobs = [("HW", s, N, dict(tau_a=ta, tau_r=tr)) for ta in [0.0, 0.001, 0.003, 0.01] for tr in [0.0, 0.0005] for s in [101, 102]]
        jobs += [("L1POE", s, N, dict(lr=lr, l1=l1)) for lr in [0.02, 0.05, 0.1] for l1 in [1e-4, 1e-3, 1e-2] for s in [101, 102]]
        jobs += [("MLP", s, N, dict(lr=lr)) for lr in [0.01, 0.03, 0.1] for s in [101, 102]]
        with mp.Pool(12) as p:
            res = p.map(run, jobs, chunksize=1)
        json.dump(res, open("law_tune.json", "w"), indent=1)
        import collections
        agg = collections.defaultdict(list)
        for r in res: agg[(r["policy"], json.dumps(r["kw"], sort_keys=True))].append(r["avg_loss"])
        best = {}
        for (pp, k), v in sorted(agg.items(), key=lambda kv: np.mean(kv[1])):
            print(pp, k, "%.4f" % np.mean(v)); best.setdefault(pp, json.loads(k))
        json.dump(best, open("law_tuned.json", "w")); print("tuned", best)
    if mode == "eval_uncentered":
        tuned = json.load(open("law_tuned.json"))
        jobs = []
        for s in range(1, 9):
            jobs.append(("CSL", s, N, dict(center=False)))
            jobs.append(("HW", s, N, dict(center=False, **tuned["HW"])))
        with mp.Pool(12) as p:
            res = p.map(run, jobs, chunksize=1)
        json.dump(res, open("law_eval_uncentered.json", "w"), indent=1)
    if mode == "eval":
        tuned = json.load(open("law_tuned.json"))
        jobs = []
        for s in range(1, 9):
            for pol, kw in [("CSL", {}), ("HW", tuned["HW"]), ("L1POE", tuned["L1POE"]), ("MLP", tuned["MLP"]), ("ORACLE", {})]:
                jobs.append((pol, s, N, kw))
        with mp.Pool(12) as p:
            res = p.map(run, jobs, chunksize=1)
        json.dump(res, open("law_eval.json", "w"), indent=1)
