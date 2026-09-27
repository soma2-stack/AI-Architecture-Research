"""
H.1j — Group CSL in LawWorld: certify CONTEXTS (preconditions), fit their effects densely.

Unit of certification = a precondition P (one of 120 contexts). Proposal: residual-covariance norm of P.
Admission test (multi-outcome score test along a frozen direction d, |d| <= 1/2):
    Z = u * sum_o d_o (1[y=o] - p_o) = u * (d_y - <p, d>),   u = 1[P]   ->  |Z| <= 1,
    mean <= 0 if there is no unexplained signal along d in context P.
    d (98-dim, absolute + action-relative outcome directions, mapped to absolute classes by the action)
    is the normalised residual covariance of P at proposal time (past data only).
After admission: P gets a dense 98-dim weight vector trained jointly with all admitted contexts (like L1POE
restricted to certified contexts, no L1).
Retirement: Shiryaev-Roberts on "the frozen admitted weight vector now hurts":
    Dr = -(l(z0) - l(z0 + a)),  a = the family's frozen logit shift, |Dr| <= 2 max|a|.
"""
import numpy as np, math, json, time, sys
import lawworld as lw
from multiprocessing import Pool

LAMS = lw.LAMS


def rel_vec_to_abs(vec98, a):
    """map a 98-dim law-outcome vector (49 abs + 49 relative) to a 49-dim absolute logit shift for action a"""
    out = vec98[:49].copy()
    for q in range(49):
        if vec98[49 + q] != 0.0:
            out[lw.rel_to_abs(49 + q, a)] += vec98[49 + q]
    return out


class Family:
    def __init__(self, P, t, alpha, d):
        self.P, self.born, self.alpha, self.d = P, t, alpha, d
        self.lw = np.zeros(len(LAMS)); self.logW = 0.0
        self.W = np.zeros(98); self.Wc = None
        self.lwr = np.zeros(len(LAMS)); self.logWr = 0.0; self.admitted_at = None


class GroupCSL:
    def __init__(self, lr=0.1, alpha_rate=0.1, window=10000, pe=50, pk=1, maxp=30, min_life=1500, patience=6000,
                 delta_r=0.0005, arl=1e5, wmax=4.0, background=False, bg_lr=0.1, bg_l1=1e-3):
        self.background, self.bg_lr, self.bg_l1 = background, bg_lr, bg_l1
        self.B = np.zeros((lw.NP, 49))          # background weights (absolute outcomes), used only for uncertified contexts
        self.lr, self.pe, self.pk, self.maxp, self.minlife, self.pat = lr, pe, pk, maxp, min_life, patience
        self.alpha_c = alpha_rate / (window / pe * pk)
        self.dr, self.arl, self.wmax = delta_r, arl, wmax
        self.bias = np.zeros((4, 49)); self.acc, self.pend = {}, {}
        self.cov = np.zeros((lw.NP, 98)); self.mP = np.full(lw.NP, 0.1); self.decay = 0.999
        self.log = []

    def logits(self, a, act, exclude=None):
        z = self.bias[a].copy()
        for P, f in self.acc.items():
            if P != exclude and P in act:
                z += rel_vec_to_abs(f.W, a)
        if self.background:
            bg = [P for P in act if P not in self.acc]
            if bg:
                z += self.B[bg].sum(0)
        return z

    def step(self, t, a, ctx, o):
        act = set(lw.active_preconds(ctx, a))
        z = self.logits(a, act); L = lw.lse(z); loss = L - z[o]; p = np.exp(z - L)
        to_admit, to_drop = [], []
        for P, f in self.pend.items():
            u = 1.0 if P in act else 0.0
            if u:
                dab = rel_vec_to_abs(f.d, a)
                Z = float(np.clip(dab[o] - p @ dab, -1, 1))       # |dab| <= 1/2 by construction, clip is inactive
                f.lw += np.log1p(LAMS * Z); f.logW = lw.mix_log(f.lw)
                # shadow-train the family's weights (used as the initial weights if admitted)
                zs = z + rel_vec_to_abs(f.W, a); ps = np.exp(zs - lw.lse(zs)); g = ps.copy(); g[o] -= 1
                self._update_W(f, g, a)
            age = t - f.born
            if f.logW >= math.log(1 / f.alpha):
                to_admit.append(P)
            elif age > self.pat or (age > self.minlife and f.logW <= 1.0):
                to_drop.append(P)
        to_retire = []
        for P, f in self.acc.items():
            if P not in act:
                continue      # detector runs on "context-present" time: absent steps carry no evidence
            shift = rel_vec_to_abs(f.W, a); z0 = z - shift
            ac = rel_vec_to_abs(f.Wc, a); z1 = z0 + ac
            Dr = -((lw.lse(z0) - z0[o]) - (lw.lse(z1) - z1[o]))
            bound = 2 * np.max(np.abs(ac)) + self.dr
            Zr = (Dr + self.dr) / bound
            f.lwr = np.logaddexp(0.0, f.lwr) + np.log1p(LAMS * Zr); f.logWr = lw.mix_log(f.lwr)
            if t - f.admitted_at > 50 and f.logWr >= math.log(self.arl):
                to_retire.append(P)
        g = p.copy(); g[o] -= 1
        self.bias[a] -= self.lr * g
        if self.background:
            bg = [P for P in act if P not in self.acc]
            if bg:
                self.B[bg] -= self.bg_lr * g
                self.B[bg] = np.sign(self.B[bg]) * np.maximum(np.abs(self.B[bg]) - self.bg_lr * self.bg_l1, 0)
        for P, f in self.acc.items():
            if P in act:
                self._update_W(f, g, a)
        for P in to_retire:
            del self.acc[P]; self.log.append((t, "retire", P))
        if to_admit:
            P = max(to_admit, key=lambda q: self.pend[q].logW)       # one admission per step
            f = self.pend.pop(P); f.admitted_at = t; f.Wc = f.W.copy(); self.acc[P] = f; self.log.append((t, "admit", P))
            if self.background:
                f.W[:49] += self.B[P]; f.Wc = f.W.copy(); self.B[P] = 0.0      # hand the background knowledge over
        for P in to_drop:
            self.pend.pop(P, None)
        # residual mining over contexts
        ind = np.zeros(lw.NP); ind[list(act)] = 1
        self.mP = self.decay * self.mP + (1 - self.decay) * ind
        r = -g
        rl = np.concatenate([r, np.array([r[lw.rel_to_abs(49 + q, a)] for q in range(49)])])
        self.cov = self.decay * self.cov + (1 - self.decay) * np.outer(ind, rl)      # uncentred: context-specific residual
        if t % self.pe == 0 and t > 200 and len(self.pend) < self.maxp:
            sc = np.linalg.norm(self.cov, axis=1) / np.sqrt(self.mP + 1e-6)
            for P in np.argsort(-sc):
                P = int(P)
                if P in self.acc or P in self.pend:
                    continue
                v = self.cov[P]; d = v / (2 * np.max(np.abs(v)) + 1e-12)       # |d| <= 1/2 (predictable)
                f = Family(P, t, self.alpha_c, d); f.W = np.clip(4.0 * v / max(self.mP[P], 1e-3), -1, 1)
                self.pend[P] = f
                break
        return loss

    def _update_W(self, f, g, a):
        # gradient of the loss wrt the 98-dim family vector: abs part g, relative part g mapped back
        grad = np.concatenate([g, np.array([g[lw.rel_to_abs(49 + q, a)] for q in range(49)])])
        f.W = np.clip(f.W - self.lr * 0.5 * grad, -self.wmax, self.wmax)


def run(args):
    seed, N = args[0], args[1]
    kw = args[2] if len(args) > 2 else {}
    world = lw.LawWorld(np.random.default_rng(seed)); m = GroupCSL(**kw)
    tot = tot_o = 0.0; post, post_o = [], []
    for t in range(N):
        a, ctx, o, dist = world.step()
        lo = -math.log(dist[o]); tot_o += lo
        l = m.step(t, a, ctx, o); tot += l
        if world.changes and 0 <= t - world.changes[-1][0] < 1000:
            post.append(l); post_o.append(lo)
    return dict(policy="GCSL", kw=kw, seed=seed, avg_loss=tot / N, oracle=tot_o / N,
                post_change_regret=float(np.mean(post) - np.mean(post_o)) if post else None,
                admissions=sum(1 for e in m.log if e[1] == "admit"), retirements=sum(1 for e in m.log if e[1] == "retire"),
                final_contexts=len(m.acc))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        t0 = time.time(); print(json.dumps(run((1, 8000))), round(time.time() - t0, 1)); sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == "bg":
        jobs = [(s, 30000, dict(background=True, bg_l1=l1)) for s in range(1, 9) for l1 in [1e-4, 1e-3, 1e-2]]
        with Pool(12) as p:
            res = p.map(run, jobs, chunksize=1)
        json.dump(res, open("law_group_bg.json", "w"), indent=1); print("done"); sys.exit()
    with Pool(8) as p:
        res = p.map(run, [(s, 30000) for s in range(1, 9)], chunksize=1)
    json.dump(res, open("law_group_results.json", "w"), indent=1)
    print("done")
