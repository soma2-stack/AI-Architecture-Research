"""Control for H.1o: fit-all-then-prune (L1POE) with the SAME 98-dim (absolute + action-relative) outcome
parameterisation per context that certified foreground families use."""
import numpy as np, math, json, sys
import lawworld as lw
from lawworld_group import rel_vec_to_abs
from multiprocessing import Pool


class L1POERel:
    def __init__(self, lr=0.1, l1=1e-4):
        self.W = np.zeros((lw.NP, 98)); self.bias = np.zeros((4, 49)); self.lr, self.l1 = lr, l1

    def step(self, t, a, ctx, o):
        act = lw.active_preconds(ctx, a)
        z = self.bias[a] + sum(rel_vec_to_abs(self.W[P], a) for P in act)
        L = lw.lse(z); loss = L - z[o]; g = np.exp(z - L); g[o] -= 1
        self.bias[a] -= self.lr * g
        grad = np.concatenate([g, np.array([g[lw.rel_to_abs(49 + q, a)] for q in range(49)])])
        for P in act:
            self.W[P] -= self.lr * 0.5 * grad
            self.W[P] = np.sign(self.W[P]) * np.maximum(np.abs(self.W[P]) - self.lr * self.l1, 0)
        return loss


def run(args):
    seed, N, kw = args
    world = lw.LawWorld(np.random.default_rng(seed)); m = L1POERel(**kw)
    tot = tot_o = 0.0; post, post_o = [], []
    for t in range(N):
        a, ctx, o, dist = world.step()
        lo = -math.log(dist[o]); tot_o += lo
        l = m.step(t, a, ctx, o); tot += l
        if world.changes and 0 <= t - world.changes[-1][0] < 1000:
            post.append(l); post_o.append(lo)
    return dict(policy="L1POE-REL", kw=kw, seed=seed, avg_loss=tot / N, oracle=tot_o / N,
                post_change_regret=float(np.mean(post) - np.mean(post_o)))


if __name__ == "__main__":
    jobs = [(s, 30000, dict(lr=lr, l1=l1)) for s in range(1, 9) for lr in [0.05, 0.1] for l1 in [1e-4, 1e-3]]
    with Pool(12) as p:
        res = p.map(run, jobs, chunksize=1)
    json.dump(res, open("l1poe_rel.json", "w"), indent=1); print("done")
