"""
H.1i — R21 "fit densely, certify sparsely" in LawWorld.
Predictor: L1POE (every candidate law fitted jointly; best loss in H.1e).
Auditor:   for each law c whose |w_c| first exceeds w_min, start an anytime-valid score test of its NEED
           relative to the model WITHOUT it:  Z = s*(1[y=o] - p_o^(-c))*u,  s = sign(w_c) (predictable),
           u = 1[P_c]  (Z = 0 when the law's context is absent). Certified when mixture wealth >= 1/alpha_c.
           A Shiryaev-Roberts detector on -Z (need reversed) de-certifies laws after world changes.
Evaluation at the end (fresh held-out contexts under the final laws, exact outcome expectations):
    loss of FULL dense model  vs  PRUNED to certified laws  vs  PRUNED to top-|w| laws of equal count
    (pruning = zeroing the other law weights; biases kept).
"""
import numpy as np, math, json, time
import lawworld as lw
from multiprocessing import Pool

LAMS = np.array([0.025, 0.05, 0.1, 0.2, 0.4, 0.8])


class Auditor:
    def __init__(self, alpha_rate=0.1, window=10000, max_new_per_window=2000, w_min=0.1, arl=1e5):
        self.alpha_c = alpha_rate / max_new_per_window     # budget per audited law (union bound per window)
        self.w_min, self.arl = w_min, arl
        self.tests = {}        # (P,o) -> [lw array, sign, certified(bool), sr array]
        self.cert_log = []

    def step(self, model, t, a, ctx, o):
        act = lw.active_preconds(ctx, a)
        z = model.bias[a] + model.W[act].sum(0)
        for P in act:
            nz = np.nonzero(np.abs(model.W[P]) > self.w_min)[0]
            for oo in nz:
                key = (P, int(oo))
                if key not in self.tests:
                    self.tests[key] = [np.zeros(len(LAMS)), float(np.sign(model.W[P, oo])), False, np.zeros(len(LAMS)), t]
                T = self.tests[key]
                w = model.W[P, oo]
                z0 = z.copy(); z0[oo] -= w
                p0 = np.exp(z0 - lw.lse(z0))
                Z = T[1] * ((o == oo) - p0[oo])            # u = 1 here (context present)
                if not T[2]:
                    T[0] += np.log1p(LAMS * Z)
                    if lw.mix_log(T[0]) >= math.log(1 / self.alpha_c):
                        T[2] = True; self.cert_log.append((t, key, "cert")); T[3][:] = 0.0
                else:
                    T[3] = np.logaddexp(0.0, T[3]) + np.log1p(LAMS * (-Z))
                    if lw.mix_log(T[3]) >= math.log(self.arl):
                        T[2] = False; T[0][:] = 0.0; self.cert_log.append((t, key, "decert"))

    def certified(self):
        return [k for k, T in self.tests.items() if T[2]]


def eval_loss(world, bias, W, rng, n=3000):
    tot = 0.0
    for grid, pos, a in world.sample_contexts(n, rng):
        ctx = world.context(pos, a, grid); act = lw.active_preconds(ctx, a)
        z = bias[a] + W[act].sum(0); L = lw.lse(z)
        dist, _ = world.outcome_dist(pos, a, grid)
        tot += sum(pr * (L - z[k]) for k, pr in dist.items())
    return tot / n


def job(args):
    seed, N = args
    tuned = json.load(open("law_tuned.json"))["L1POE"]
    world = lw.LawWorld(np.random.default_rng(seed))
    model = lw.L1POE(**tuned); aud = Auditor()
    for t in range(N):
        a, ctx, o, dist = world.step()
        aud.step(model, t, a, ctx, o)          # audit uses the model BEFORE it learns from this example
        model.step(t, a, ctx, o)
    cert = aud.certified()
    rng = np.random.default_rng(seed + 999)
    full = eval_loss(world, model.bias, model.W, rng)
    Wc = np.zeros_like(model.W)
    for (P, oo) in cert:
        Wc[P, oo] = model.W[P, oo]
    pc = eval_loss(world, model.bias, Wc, np.random.default_rng(seed + 999))
    k = len(cert)
    flat = np.argsort(-np.abs(model.W), axis=None)[:k]
    Wm = np.zeros_like(model.W); Wm.flat[flat] = model.W.flat[flat]
    pm = eval_loss(world, model.bias, Wm, np.random.default_rng(seed + 999))
    nz = int((np.abs(model.W) > 0.1).sum())
    orc = np.mean([sum(pr * -math.log(pr) for pr in world.outcome_dist(pos, a, grid)[0].values())
                   for grid, pos, a in world.sample_contexts(1000, np.random.default_rng(seed + 5))])
    return dict(seed=seed, n_certified=k, n_weights_over_0_1=nz, loss_full=full, loss_certified=pc,
                loss_magnitude_same_k=pm, oracle_entropy=orc, decerts=sum(1 for c in aud.cert_log if c[2] == "decert"))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(json.dumps(job((1, 8000)))); sys.exit()
    t0 = time.time()
    with Pool(8) as p:
        res = p.map(job, [(s, 30000) for s in range(1, 9)], chunksize=1)
    json.dump(res, open("audit_results.json", "w"), indent=1)
    print("done", time.time() - t0)
