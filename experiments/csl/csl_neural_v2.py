"""
H.1d — Certified Expert Growth: CSL where every claim is a small NEURAL expert.

Stream: x ~ U[-1,1]^m, y = g_t(x) + N(0, sigma^2), g_t = sum of K Gaussian bumps; every `drift`
steps one bump is replaced; with prob. `recur` the new bump is an OLD bump returning (tests reuse).
Model: y_hat = b + sum_{e in accepted} h_e(x), each h_e a tiny MLP (m -> H -> 1, output B*tanh).
Candidate: every P steps a new expert is fitted to the residuals of the last 300 examples (past data only).
Test statistic (squared loss, residual clipped to [-R, R]):
    D_t = l(r) - l(r - h(x)),  l(u) = u^2/2      -> |D| <= |h| R + h^2/2  (bound known before y: predictable)
Policies: CSL (e-process admission + retirement), HW (windowed thresholds, tuned), ALWAYS (admit all
candidates, retire by HW rule), DENSE (one fixed MLP trained online), ORACLE (true g).
Spurious admission (ground truth): at admission, true usefulness U = E_x[(g - yhat)^2 - (g - yhat - h)^2]/2 <= 0
on a probe set (the expert does not reduce true error).
"""
import numpy as np, math, json, sys, time

LAMS = np.array([0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 0.95])


def mix_log(lw):
    m = lw.max(); return m + math.log(np.exp(lw - m).mean())


class TinyMLP:
    """local expert: B * tanh(w2 . tanh(W1 (x-c)/s + b1)) * gate(x),  gate = exp(-|x-c|^2 / (2 s^2)).
    The centre c is chosen where the recent residual is concentrated (past data only)."""
    def __init__(self, m, H, B, rng, lr, c=None, s=0.35):
        self.W1 = rng.normal(0, 1.0, (H, m)); self.b1 = rng.normal(0, 0.5, H)
        self.w2 = np.zeros(H); self.B, self.lr = B, lr
        self.c = np.zeros(m) if c is None else c; self.s = s

    def f(self, x):
        u = (x - self.c) / self.s
        self.gate = math.exp(-0.5 * float(u @ u))
        self.h = np.tanh(self.W1 @ u + self.b1)
        self.o = np.tanh(self.w2 @ self.h)
        self.u = u
        return self.B * self.o * self.gate

    def grad_step(self, x, err):          # minimise err^2/2 where err = target - f(x); call after f(x)
        g_out = -err * self.B * (1 - self.o ** 2) * self.gate
        gh = g_out * self.w2 * (1 - self.h ** 2)
        self.w2 -= self.lr * g_out * self.h
        self.W1 -= self.lr * np.outer(gh, self.u); self.b1 -= self.lr * gh

    def fit(self, X, R, epochs):
        for _ in range(epochs):
            for i in np.random.permutation(len(X)):
                p = self.f(X[i]); self.grad_step(X[i], R[i] - p)


class BumpStream:
    def __init__(self, m, K, drift, recur, rng, sigma=0.5, width=0.4):
        self.m, self.K, self.drift, self.recur, self.rng, self.sigma, self.w = m, K, drift, recur, rng, sigma, width
        self.bumps = [self._new() for _ in range(K)]
        self.retired = []
        self.t = 0

    def _new(self):
        return (self.rng.uniform(-0.8, 0.8, self.m), self.rng.uniform(1.0, 2.0) * self.rng.choice([-1, 1]))

    def g(self, x):
        return sum(a * math.exp(-np.sum((x - c) ** 2) / (2 * self.w ** 2)) for c, a in self.bumps)

    def step(self):
        if self.K > 0 and self.t > 0 and self.t % self.drift == 0:
            i = int(self.rng.integers(self.K))
            self.retired.append(self.bumps[i])
            if self.retired[:-1] and self.rng.random() < self.recur:
                self.bumps[i] = self.retired[int(self.rng.integers(len(self.retired) - 1))]
            else:
                self.bumps[i] = self._new()
        x = self.rng.uniform(-1, 1, self.m)
        gx = self.g(x)
        self.t += 1
        return x, gx + self.rng.normal(0, self.sigma), gx


GRID = np.stack(np.meshgrid(np.linspace(-1, 1, 21), np.linspace(-1, 1, 21)), -1).reshape(-1, 2)


class Expert:
    def __init__(self, net, t, alpha):
        self.net, self.born, self.alpha = net, t, alpha
        self.hsup = net.B                         # predictable output cap; tightened by refresh_cap()
        self.lw = np.zeros(len(LAMS)); self.logW = 0.0; self.hist = []
        self.lwr = np.zeros(len(LAMS)); self.logWr = 0.0; self.histr = []
        self.admitted_at = None

    def refresh_cap(self):
        if self.net.c.shape[0] == 2:
            self.hsup = min(self.net.B, 1.25 * max(abs(self.net.f(p)) for p in GRID) + 0.05)

    def freeze(self):                             # frozen proposal direction, normalised to |phi| <= 1
        import copy
        self.frozen = copy.deepcopy(self.net)
        self.fcap = max(1e-3, max(abs(self.frozen.f(p)) for p in GRID)) if self.net.c.shape[0] == 2 else self.net.B

    def phi(self, x):
        return float(np.clip(self.frozen.f(x) / self.fcap, -1, 1))

    def out(self, x):                             # effective output, clipped at the predictable cap
        return float(np.clip(self.net.f(x), -self.hsup, self.hsup))


class Grower:
    def __init__(self, m, policy, rng, H=16, B=3.0, R=4.0, lr=0.02, P=100, max_pending=6, buf=300,
                 alpha_rate=0.1, window=10000, delta_r=0.0, beta_c=0.01, tau_a=0.01, tau_r=0.0,
                 hw_win=300, min_life=1500, patience=6000, arl=1e5, bound_mode="global", adm_mode="loss"):
        self.m, self.policy, self.rng = m, policy, rng
        self.H, self.B, self.R, self.lr, self.P, self.maxp, self.buf = H, B, R, lr, P, max_pending, buf
        self.alpha_c = alpha_rate / (window / P)
        self.dr, self.bc, self.tau_a, self.tau_r, self.hw_win = delta_r, beta_c, tau_a, tau_r, hw_win
        self.minlife, self.pat, self.arl, self.bound_mode, self.adm_mode = min_life, patience, arl, bound_mode, adm_mode
        self.bias = 0.0; self.accepted, self.pending = [], []
        self.X, self.Rs = [], []
        self.log = []

    def predict(self, x):
        return self.bias + sum(e.out(x) for e in self.accepted)

    def _bound(self, e):
        hb = e.hsup if self.bound_mode == "sup" else self.B
        return hb * self.R + hb ** 2 / 2

    def step(self, t, x, y):
        if self.bound_mode == "sup" and t % 100 == 0:
            for e in self.pending + self.accepted:
                e.refresh_cap()
        outs = [e.out(x) for e in self.accepted]
        yhat = self.bias + sum(outs)
        r = float(np.clip(y - yhat, -self.R, self.R))
        loss = (y - yhat) ** 2 / 2
        to_admit, to_drop = [], []
        for e in self.pending:
            h = e.out(x)
            # INPUT-INDEPENDENT bound (|h| <= cap): tests the null averaged over inputs.
            # (An x-dependent bound silently tests a pointwise null and admits locally-helpful, globally-harmful experts.)
            bound = self._bound(e)
            D = (r * r - (r - h) ** 2) / 2
            if self.adm_mode == "score":
                # certify the NEED: residual correlates with the frozen proposal direction phi (|phi| <= 1)
                Z = r * e.phi(x) / self.R
            else:
                Z = D / bound
            e.lw += np.log1p(LAMS * Z); e.logW = mix_log(e.lw); e.hist.append(D)
            e.net.f(x); e.net.grad_step(x, r - h)          # train shadow expert on its residual (after scoring)
            age = t - e.born
            if self._admit(e):
                to_admit.append(e)
            elif age > self.pat or (age > self.minlife and not (self.policy == "CSL" and e.logW > 1.0)):
                to_drop.append(e)
        to_retire = []
        for e, h in zip(self.accepted, outs):
            bound = self._bound(e)
            rr = float(np.clip(y - yhat + h, -self.R, self.R))   # residual without e
            Dr = (r * r - rr * rr) / 2                           # >0: removing e would help
            Zr = (Dr + self.dr) / (bound + self.dr)
            e.lwr = np.logaddexp(0.0, e.lwr) + np.log1p(LAMS * Zr); e.logWr = mix_log(e.lwr); e.histr.append(Dr)
            if t - e.admitted_at > 50 and self._retire(e):
                to_retire.append(e)
        # train admitted experts + bias on full residual
        err = float(np.clip(y - yhat, -self.R, self.R))
        self.bias += self.lr * err
        for e in self.accepted:
            e.net.f(x); e.net.grad_step(x, err)
        for e in to_retire:
            self.accepted.remove(e); self.log.append((t, "retire", id(e)))
        if to_admit and self.policy == "CSL":
            to_admit = [max(to_admit, key=lambda e: e.logW)]          # at most one admission per step
        for e in to_admit:
            self.pending.remove(e); e.admitted_at = t; self.accepted.append(e); self.log.append((t, "admit", e))
            if self.policy == "CSL":
                for p in self.pending:                                  # overlapping candidates must re-prove
                    if np.linalg.norm(p.net.c - e.net.c) < 1.5 * e.net.s:   # value vs the new model:
                        p.lw = np.minimum(p.lw, 0.0); p.logW = mix_log(p.lw)  # restart (down-scaling: valid)
        for e in to_drop:
            self.pending.remove(e)
        self.X.append(x); self.Rs.append(r)
        if len(self.X) > self.buf:
            self.X.pop(0); self.Rs.pop(0)
        if t % self.P == 0 and t >= self.buf and len(self.pending) < self.maxp:
            Xb, Rb = np.array(self.X), np.array(self.Rs)
            d2 = ((Xb[:, None, :] - Xb[None, :, :]) ** 2).sum(-1)
            K = np.exp(-d2 / (2 * 0.2 ** 2))
            sm = (K @ Rb) / K.sum(1)                                   # kernel-smoothed residual
            c = Xb[int(np.argmax(np.abs(sm)))]
            net = TinyMLP(self.m, self.H, self.B, self.rng, self.lr, c=c)
            net.fit(Xb, Rb, epochs=5)
            ex = Expert(net, t, self.alpha_c); ex.freeze()
            if self.bound_mode == "sup": ex.refresh_cap()
            self.pending.append(ex)
        return loss

    def _admit(self, e):
        if self.policy == "CSL":
            return e.logW >= math.log(1 / e.alpha)
        if self.policy == "HW":
            return len(e.hist) >= self.hw_win and np.mean(e.hist[-self.hw_win:]) > self.tau_a
        if self.policy == "ALWAYS":
            return True
        raise ValueError

    def _retire(self, e):
        if self.policy == "CSL":
            return e.logWr >= math.log(self.arl)          # Shiryaev-Roberts: ARL to false retirement >= arl
        return len(e.histr) >= self.hw_win and np.mean(-np.asarray(e.histr[-self.hw_win:])) < self.tau_r


class Dense:
    def __init__(self, m, rng, H=64, lr=0.01):
        self.W1 = rng.normal(0, 1.0, (H, m)); self.b1 = rng.normal(0, 0.5, H)
        self.W2 = rng.normal(0, 1 / math.sqrt(H), (H, H)); self.b2 = np.zeros(H)
        self.w3 = np.zeros(H); self.b3 = 0.0; self.lr = lr

    def fwd(self, x):
        h1 = np.tanh(self.W1 @ x + self.b1); h2 = np.tanh(self.W2 @ h1 + self.b2)
        return float(self.w3 @ h2 + self.b3)

    def step(self, t, x, y):
        h1 = np.tanh(self.W1 @ x + self.b1); h2 = np.tanh(self.W2 @ h1 + self.b2)
        yhat = self.w3 @ h2 + self.b3
        err = float(np.clip(y - yhat, -4, 4)); loss = (y - yhat) ** 2 / 2
        g3 = -err; gh2 = g3 * self.w3 * (1 - h2 ** 2); gh1 = (self.W2.T @ gh2) * (1 - h1 ** 2)
        self.w3 -= self.lr * g3 * h2; self.b3 -= self.lr * g3
        self.W2 -= self.lr * np.outer(gh2, h1); self.b2 -= self.lr * gh2
        self.W1 -= self.lr * np.outer(gh1, x); self.b1 -= self.lr * gh1
        return loss


class Hybrid:
    """slow dense core + CSL-certified fast local experts modelling the core's residual (backfitting)"""
    def __init__(self, m, rng, core_lr=0.003, **kw):
        self.g = Grower(m, "CSL", rng, adm_mode="score", bound_mode="sup", **kw)
        self.core = Dense(m, rng, lr=core_lr)
        self.log = self.g.log; self.accepted = self.g.accepted

    @property
    def bias(self):
        return self.g.bias

    def step(self, t, x, y):
        c = self.core.fwd(x)
        gp = self.g.predict(x)
        loss = self.g.step(t, x, y - c)          # experts + bias see the core's residual
        self.core.step(t, x, y - gp)            # core fits what the experts did not explain
        self.accepted = self.g.accepted
        return loss


def run(args):
    policy, seed, N, kw, scfg = args
    rng_s = np.random.default_rng(seed)
    st = BumpStream(scfg["m"], scfg["K"], scfg["drift"], scfg["recur"], rng_s, sigma=scfg.get("sigma", 0.5),
                    width=scfg.get("width", 0.4))
    probe = np.random.default_rng(seed + 5).uniform(-1, 1, (400, scfg["m"]))
    rng_m = np.random.default_rng(seed + 99)
    if policy == "DENSE":
        model = Dense(scfg["m"], rng_m, **kw)
    elif policy == "HYBRID":
        model = Hybrid(scfg["m"], rng_m, **kw)
    elif policy == "ORACLE":
        model = None
    else:
        model = Grower(scfg["m"], policy, rng_m, **kw)
    tot = tot_o = 0.0; spur = adm = 0; sizes = []; post = []; post_o = []; last_change = -10**9
    noise_floor = 0.0
    for t in range(N):
        x, y, gx = st.step()
        tot_o += (y - gx) ** 2 / 2
        if model is None:
            continue
        nlog = len(getattr(model, "log", []))
        lt = model.step(t, x, y); tot += lt
        if st.K > 0 and t > 0 and t % st.drift == 0:
            last_change = t
        if 0 <= t - last_change < 1000:
            post.append(lt); post_o.append((y - gx) ** 2 / 2)
        if policy in ("CSL", "HW", "ALWAYS", "HYBRID"):
            for (tt, ev, e) in model.log[nlog:]:
                if ev == "admit":
                    adm += 1
                    gp = np.array([st.g(p) for p in probe])
                    others = np.array([model.bias + (model.core.fwd(p) if policy == "HYBRID" else 0.0)
                                       + sum(o.out(p) for o in model.accepted if o is not e) for p in probe])
                    he = np.array([e.out(p) for p in probe])
                    U = np.mean((gp - others) ** 2 - (gp - others - he) ** 2) / 2
                    spur += int(U <= 0)
            if t % 1000 == 999:
                sizes.append(len(model.accepted))
    res = dict(policy=policy, seed=seed, avg_loss=(tot if model else tot_o) / N, oracle=tot_o / N, kw=kw,
               post_change_regret=(float(np.mean(post) - np.mean(post_o)) if post else None))
    if policy in ("CSL", "HW", "ALWAYS", "HYBRID"):
        res.update(admissions=adm, spurious=spur, mean_size=float(np.mean(sizes)), final_size=len(model.accepted))
    return res


SCFG = dict(m=2, K=4, drift=5000, recur=0.3, sigma=0.5, width=0.35)

if __name__ == "__main__":
    mode = sys.argv[1]
    import multiprocessing as mp
    N = 25000
    if mode == "quick":
        for pol in ["CSL", "HW", "DENSE", "ORACLE"]:
            t0 = time.time(); print(json.dumps(run((pol, 1, 8000, {}, SCFG))), round(time.time() - t0, 1), flush=True)
    if mode == "tune":
        jobs = [("HW", s, N, dict(tau_a=ta, tau_r=tr), SCFG) for ta in [0.0, 0.005, 0.01, 0.02, 0.05]
                for tr in [0.0, 0.002] for s in [101, 102]]
        jobs += [("DENSE", s, N, dict(lr=lr), SCFG) for lr in [0.003, 0.01, 0.03] for s in [101, 102]]
        with mp.Pool(12) as p:
            res = p.map(run, jobs, chunksize=1)
        json.dump(res, open("neural_tune.json", "w"), indent=1)
    if mode == "tune_summary":
        import collections
        res = json.load(open("neural_tune.json")); agg = collections.defaultdict(list)
        for r in res: agg[(r["policy"], json.dumps(r["kw"], sort_keys=True))].append(r["avg_loss"])
        best = {}
        for (p, k), v in sorted(agg.items(), key=lambda kv: np.mean(kv[1])):
            print(p, k, "%.4f" % np.mean(v))
            best.setdefault(p, json.loads(k))
        json.dump(best, open("neural_tuned.json", "w")); print("tuned", best)
    if mode == "adapt":
        tuned = json.load(open("neural_tuned.json"))
        jobs = []
        for s in range(1, 9):
            for pol, kw in [("CSL", {"adm_mode": "score", "bound_mode": "sup"}), ("HW", tuned["HW"]), ("DENSE", tuned["DENSE"]),
                            ("HYBRID", {"core_lr": 0.003}), ("HYBRID", {"core_lr": 0.01}), ("DENSE", {"lr": 0.003})]:
                jobs.append((pol, s, N, kw, SCFG))
        with mp.Pool(12) as p:
            res = p.map(run, jobs, chunksize=1)
        json.dump(res, open("neural_adapt.json", "w"), indent=1)
    if mode == "hybrid":
        jobs = []
        for s in range(1, 9):
            for pol, kw in [("HYBRID", {"core_lr": 0.003}), ("HYBRID", {"core_lr": 0.01}), ("DENSE", {"lr": 0.01}),
                            ("DENSE", {"lr": 0.003}), ("CSL", {"adm_mode": "score", "bound_mode": "sup"})]:
                jobs.append((pol, s, N, kw, SCFG))
        with mp.Pool(12) as p:
            res = p.map(run, jobs, chunksize=1)
        json.dump(res, open("neural_hybrid.json", "w"), indent=1)
    if mode == "eval":
        tuned = json.load(open("neural_tuned.json"))
        cfgs = {"base": SCFG, "noisy": dict(SCFG, sigma=1.0), "null": dict(SCFG, K=0)}
        jobs = []
        for name, c in cfgs.items():
            for s in range(1, 7):
                for pol, kw in [("CSL", {}), ("CSL", {"alpha_rate": 1.0}), ("CSL", {"alpha_rate": 10.0}),
                                ("CSL", {"bound_mode": "sup"}), ("CSL", {"adm_mode": "score", "bound_mode": "sup"}),
                                ("HW", tuned["HW"]), ("DENSE", tuned["DENSE"]), ("ORACLE", {})]:
                    jobs.append((pol, s, N, kw, c))
        with mp.Pool(12) as p:
            res = p.map(run, jobs, chunksize=1)
        for r, j in zip(res, jobs):
            r["config"] = [k for k, v in cfgs.items() if v is j[4]][0]
        json.dump(res, open("neural_eval_v2.json", "w"), indent=1)
