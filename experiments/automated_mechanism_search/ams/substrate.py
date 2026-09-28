"""Fixed pilot substrate: MLP [d_in, 32, 32, d_out], tanh hidden, float32.

Many independent runs (seed x learning-rate configurations) are vectorized along
axis 0 ("R").  Each protocol step presents a mini-batch of B examples (B = 1 for
online tasks).  The same mechanism program is applied to all three layers.

Step order (AE.1.5):  FORWARD (all layers) -> loss -> backward (if d_bp is read)
-> CREDIT -> STATE -> PARAM (applied every `update_every` steps) -> STRUCT
(every 100 steps).  Batch semantics: IMPLEMENTATION_DECISIONS.md D-SUB-*.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .grammar import (GAIN_MAX, I, M, O, REG_CLIP, S, STRUCT_PERIOD, Program, reads)
from .interp import Compiled, compiled_flops

DT = np.float32
HIDDEN = 32
NOISE_STD = 0.01            # xi and "noise" register init: N(0, 0.01) read as std 0.01
LBAR_DECAY = 0.99
DIVERGENCE_FACTOR = 10.0
WNORM_MAX = 1e4
MEM_LIMIT_MB = 512.0


def seed_seq(seed: int, stream: int) -> np.random.SeedSequence:
    return np.random.SeedSequence([int(seed), int(stream)])


def rng_for(seed: int, stream: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed_seq(seed, stream)))


# RNG stream ids (IMPLEMENTATION_DECISIONS D-SEED-1)
STREAM_INIT, STREAM_FEEDBACK, STREAM_REINIT, STREAM_NOISE = 7001, 7002, 7003, 7004


def rss_mb() -> float:
    try:
        with open("/proc/self/statm") as f:
            pages = int(f.read().split()[1])
        import os
        return pages * os.sysconf("SC_PAGE_SIZE") / 2**20
    except OSError:  # pragma: no cover
        return 0.0


class Timeout(Exception):
    pass


class OutOfMemory(Exception):
    pass


class Net:
    """Parameters for R runs of the fixed MLP."""

    def __init__(self, d_in: int, d_out: int, seeds: Sequence[int], hidden: int = HIDDEN,
                 depth_hidden: int = 2):
        self.sizes = [d_in] + [hidden] * depth_hidden + [d_out]
        self.nl = len(self.sizes) - 1
        self.R = len(seeds)
        self.seeds = list(seeds)
        self.std = [np.sqrt(2.0 / (self.sizes[l] + self.sizes[l + 1])) for l in range(self.nl)]
        self.W: List[np.ndarray] = []
        self.b: List[np.ndarray] = []
        for l in range(self.nl):
            o, i = self.sizes[l + 1], self.sizes[l]
            self.W.append(np.zeros((self.R, o, i), DT))
            self.b.append(np.zeros((self.R, o), DT))
        for r, s in enumerate(self.seeds):
            g = rng_for(s, STREAM_INIT)
            for l in range(self.nl):
                o, i = self.sizes[l + 1], self.sizes[l]
                self.W[l][r] = g.normal(0.0, self.std[l], (o, i)).astype(DT)
        # fixed random feedback for hidden layers (DFA), N(0, 1/d_out)
        self.fb: List[Optional[np.ndarray]] = []
        for l in range(self.nl):
            if l == self.nl - 1:
                self.fb.append(None)
            else:
                arr = np.zeros((self.R, self.sizes[l + 1], d_out), DT)
                for r, s in enumerate(self.seeds):
                    g = rng_for(s, STREAM_FEEDBACK + 100 * l)
                    arr[r] = g.normal(0.0, np.sqrt(1.0 / d_out), (self.sizes[l + 1], d_out))
                self.fb.append(arr)
        self.reinit_rng = [rng_for(s, STREAM_REINIT) for s in self.seeds]
        self.noise_rng = [rng_for(s, STREAM_NOISE) for s in self.seeds]

    def n_params(self) -> int:
        return int(sum(self.sizes[l] * self.sizes[l + 1] + self.sizes[l + 1] for l in range(self.nl)))

    def dims(self, l: int) -> Dict[str, int]:
        return {I: self.sizes[l], O: self.sizes[l + 1]}

    def noise(self, shape_tail: Tuple[int, ...], B: int) -> np.ndarray:
        out = np.empty((self.R, B) + shape_tail, DT)
        for r in range(self.R):
            out[r] = self.noise_rng[r].normal(0.0, NOISE_STD, (B,) + shape_tail)
        return out


# ---------------------------------------------------------------------------
# Learners
# ---------------------------------------------------------------------------

class Learner:
    name = "learner"
    needs_bp = True
    needs_fa = False
    reads_noise = False
    update_every = 1
    clip = True

    def init(self, net: Net):
        pass

    def episode_start(self, net: Net, tr: "Trainer"):
        pass

    def forward_mods(self, l: int, env: Dict[str, np.ndarray], net: Net, nb: int):
        return None, None

    def updates(self, net: Net, tr: "Trainer", cache) -> List[Tuple[np.ndarray, np.ndarray]]:
        raise NotImplementedError

    def struct_event(self, net: Net, tr: "Trainer", cache):
        pass

    def post_apply(self, net: Net, tr: "Trainer", deltas):
        pass

    # accounting
    def state_floats(self, net: Net) -> int:
        return 0

    def flops_per_example(self, net: Net) -> float:
        return 0.0


def _grad(cache, l):
    d, a = cache["d_bp"][l], cache["a"][l]
    B = a.shape[1]
    gW = np.matmul(np.swapaxes(d, 1, 2), a) / B
    gb = d.mean(axis=1)
    return gW, gb


class SGD(Learner):
    name = "SGD"

    def __init__(self, clip: bool = True):
        self.clip = clip

    def updates(self, net, tr, cache):
        out = []
        for l in range(net.nl):
            gW, gb = _grad(cache, l)
            out.append((-gW, -gb))
        return out


class SGDM(Learner):
    """Polyak heavy-ball momentum, beta = 0.9: v <- beta v + g; delta = -v."""
    name = "SGDM"

    def __init__(self, beta: float = 0.9, clip: bool = True):
        self.beta = beta
        self.clip = clip

    def init(self, net):
        self.vW = [np.zeros_like(w) for w in net.W]
        self.vb = [np.zeros_like(b) for b in net.b]

    def updates(self, net, tr, cache):
        out = []
        for l in range(net.nl):
            gW, gb = _grad(cache, l)
            self.vW[l] = self.beta * self.vW[l] + gW
            self.vb[l] = self.beta * self.vb[l] + gb
            out.append((-self.vW[l], -self.vb[l]))
        return out

    def state_floats(self, net):
        return net.n_params()


class AdamW(Learner):
    """AdamW (Loshchilov & Hutter): bias-corrected moments, decoupled weight decay on W."""
    name = "AdamW"

    def __init__(self, b1=0.9, b2=0.999, eps=1e-8, wd=0.01, clip: bool = True):
        self.b1, self.b2, self.eps, self.wd = b1, b2, eps, wd
        self.clip = clip

    def init(self, net):
        self.m = [[np.zeros_like(w), np.zeros_like(b)] for w, b in zip(net.W, net.b)]
        self.v = [[np.zeros_like(w), np.zeros_like(b)] for w, b in zip(net.W, net.b)]
        self.t = 0

    def updates(self, net, tr, cache):
        self.t += 1
        c1 = 1 - self.b1 ** self.t
        c2 = 1 - self.b2 ** self.t
        out = []
        for l in range(net.nl):
            gs = _grad(cache, l)
            ds = []
            for j in range(2):
                m = self.m[l][j] = self.b1 * self.m[l][j] + (1 - self.b1) * gs[j]
                v = self.v[l][j] = self.b2 * self.v[l][j] + (1 - self.b2) * gs[j] ** 2
                ds.append(-(m / c1) / (np.sqrt(v / c2) + self.eps))
            ds[0] = ds[0] - self.wd * net.W[l]
            out.append((ds[0].astype(DT), ds[1].astype(DT)))
        return out

    def state_floats(self, net):
        return 2 * net.n_params()


class GPM(SGD):
    """Gradient Projection Memory (Saha et al. 2021) on the MLP, with SGD.

    At each task boundary after the first, the input-representation subspace of
    every layer (augmented with the constant bias input) is extracted from the
    last `n_mem` training examples of the finished task by SVD with energy
    threshold `thr`; later updates are projected onto its orthogonal complement.
    """
    name = "GPM"

    def __init__(self, thr: float = 0.97, n_mem_batches: int = 8, clip: bool = True):
        super().__init__(clip)
        self.thr = thr
        self.n_mem_batches = n_mem_batches

    def init(self, net):
        self.P = [None] * net.nl       # (R, n_in+1, n_in+1)
        self.mem: List[List[np.ndarray]] = [[] for _ in range(net.nl)]
        self.n_eps = 0

    def episode_start(self, net, tr):
        self.n_eps += 1
        if self.n_eps == 1:
            return
        for l in range(net.nl):
            A = np.concatenate(self.mem[l], axis=1)          # (R, N, n_in)
            Aa = np.concatenate([A, np.ones(A.shape[:2] + (1,), DT)], axis=2)
            n_in1 = Aa.shape[2]
            P = np.zeros((net.R, n_in1, n_in1), DT)
            for r in range(net.R):
                X = Aa[r].astype(np.float64).T              # (n_in+1, N)
                if self.P[l] is not None:                   # residual w.r.t. existing basis
                    X = X - self.P[l][r].astype(np.float64) @ X
                U, s, _ = np.linalg.svd(X, full_matrices=False)
                tot = (Aa[r].astype(np.float64) ** 2).sum()
                acc = np.cumsum(s ** 2) / max(tot, 1e-12)
                prev = 0.0 if self.P[l] is None else 0.0
                k = int(np.searchsorted(acc, self.thr - prev) + 1)
                k = min(k, U.shape[1])
                Pk = U[:, :k] @ U[:, :k].T
                P[r] = (Pk if self.P[l] is None else self.P[l][r] + Pk).astype(DT)
            self.P[l] = P
        self.mem = [[] for _ in range(net.nl)]

    def updates(self, net, tr, cache):
        for l in range(net.nl):
            self.mem[l].append(cache["a"][l].copy())
            self.mem[l] = self.mem[l][-self.n_mem_batches:]
        out = []
        for l in range(net.nl):
            gW, gb = _grad(cache, l)
            if self.P[l] is not None:
                G = np.concatenate([gW, gb[:, :, None]], axis=2)   # (R, o, i+1)
                G = G - np.matmul(G, self.P[l])
                gW, gb = G[:, :, :-1], G[:, :, -1]
            out.append((-gW, -gb))
        return out

    def state_floats(self, net):
        return int(sum((net.sizes[l] + 1) ** 2 for l in range(net.nl)))


def _init_reg(rd, shape, net: Net) -> np.ndarray:
    if rd.init == "0":
        return np.zeros(shape, DT)
    if rd.init == "1":
        return np.ones(shape, DT)
    out = np.empty(shape, DT)
    for r in range(shape[0]):
        out[r] = net.noise_rng[r].normal(0.0, NOISE_STD, shape[1:])
    return out


class ProgramLearner(Learner):
    """Executes a (canonical) grammar program on every layer."""

    def __init__(self, prog: Program, name: str = "program", clip: bool = True):
        self.prog = prog
        self.name = name
        self.clip = clip
        self.update_every = prog.update_every
        rt = prog.reg_types()
        self.rtypes = rt
        rd = reads(prog.dW) | reads(prog.db)
        allr = set()
        for _, e in prog.slot_exprs():
            allr |= reads(e)
        self.all_reads = allr
        self.needs_bp = "d_bp" in allr
        self.needs_fa = "d_fa" in allr
        self.reads_noise = bool({"xi_I", "xi_O"} & allr)
        self.fwd_exprs = [e for e in (prog.w_eff, prog.gain) if e is not None]
        self.f_fwd = Compiled(self.fwd_exprs, rt) if self.fwd_exprs else None
        self.f_cred = Compiled([prog.cvec], rt) if prog.cvec is not None else None
        self.f_state = Compiled(list(prog.reg_updates), rt) if prog.regs else None
        par = [prog.dW, prog.db]
        self.f_param = Compiled(par, rt)
        self.f_struct = Compiled([prog.struct.mask], rt) if prog.struct is not None else None

    # --- registers -----------------------------------------------------------
    def _reg_shape(self, rtype, net, l):
        o, i = net.sizes[l + 1], net.sizes[l]
        return (net.R, 1) + {I: (i,), O: (o,), M: (o, i)}[rtype]

    def init(self, net):
        self.regs = [{rd.name: _init_reg(rd, self._reg_shape(rd.type, net, l), net)
                      for rd in self.prog.regs} for l in range(net.nl)]
        self.freeze = [None] * net.nl

    def episode_start(self, net, tr):
        for l in range(net.nl):
            for rd in self.prog.regs:
                if rd.lifetime == "EPISODE":
                    self.regs[l][rd.name] = _init_reg(rd, self._reg_shape(rd.type, net, l), net)

    def example_reset(self, net):
        for l in range(net.nl):
            for rd in self.prog.regs:
                if rd.lifetime == "EXAMPLE":
                    self.regs[l][rd.name] = _init_reg(rd, self._reg_shape(rd.type, net, l), net)

    def _env_regs(self, env, l, regs=None):
        regs = self.regs[l] if regs is None else regs
        for k, v in regs.items():
            env["reg:" + k] = v

    def forward_mods(self, l, env, net, nb):
        if self.f_fwd is None:
            return None, None
        self._env_regs(env, l)
        outs = self.f_fwd(env, nb, net.dims(l))
        k = 0
        W_eff = g = None
        if self.prog.w_eff is not None:
            W_eff = env["W"] + outs[k]
            k += 1
        if self.prog.gain is not None:
            g = np.clip(outs[k], 0.0, GAIN_MAX)
        return W_eff, g

    def updates(self, net, tr, cache):
        out = []
        new_regs_all = []
        for l in range(net.nl):
            env = cache["env"][l]
            self._env_regs(env, l)
            dims = net.dims(l)
            if self.f_cred is not None:
                env["cvec"] = self.f_cred(env, 2, dims)[0]
            new_regs = dict(self.regs[l])
            if self.f_state is not None:
                vs = self.f_state(env, 2, dims)
                for rd, v in zip(self.prog.regs, vs):
                    r_old = self.regs[l][rd.name]
                    if rd.lifetime == "EXAMPLE":
                        vbar = v                             # per-example temporary
                    else:
                        vbar = v.mean(axis=1, keepdims=True)  # per-layer persistent state
                    lam = DT(rd.decay)
                    rn = lam * r_old + (DT(1) - lam) * vbar
                    new_regs[rd.name] = np.clip(rn, -REG_CLIP, REG_CLIP).astype(DT)
            self.regs[l] = new_regs
            self._env_regs(env, l)
            dW, db = self.f_param(env, 2, dims)
            dW = np.broadcast_to(dW, (net.R, dW.shape[1]) + dW.shape[2:]).mean(axis=1)
            db = np.broadcast_to(db, (net.R, db.shape[1]) + db.shape[2:]).mean(axis=1)
            if self.freeze[l] is not None:
                dW = dW * (1.0 - self.freeze[l])[:, :, None]
            out.append((dW.astype(DT), db.astype(DT)))
            new_regs_all.append(new_regs)
        return out

    def struct_event(self, net, tr, cache):
        if self.f_struct is None:
            return
        st = self.prog.struct
        for l in range(net.nl):
            env = cache["env"][l]
            self._env_regs(env, l)
            v = self.f_struct(env, 2, net.dims(l))[0]
            v = np.broadcast_to(v, (net.R, v.shape[1], net.sizes[l + 1])).mean(axis=1)
            mask = (v - st.theta > 0).astype(DT)             # (R, o)
            if st.kind == "freeze":
                self.freeze[l] = mask
            else:
                for r in range(net.R):
                    rows = np.nonzero(mask[r])[0]
                    if rows.size and tr.alive[r]:
                        net.W[l][r, rows, :] = net.reinit_rng[r].normal(
                            0.0, net.std[l], (rows.size, net.sizes[l])).astype(DT)
                tr.n_reinit[l] += int(mask.sum())

    def state_floats(self, net):
        tot = 0
        for l in range(net.nl):
            o, i = net.sizes[l + 1], net.sizes[l]
            for rd in self.prog.regs:
                if rd.lifetime != "EXAMPLE":
                    tot += {I: i, O: o, M: o * i}[rd.type]
            if "W_ep0" in self.all_reads:
                tot += o * i
        tot += sum(1 for s in ("Lbar", "dL") if s in self.all_reads)
        return tot

    def flops_per_example(self, net):
        tot = 0.0
        for l in range(net.nl):
            d = net.dims(l)
            for c in (self.f_fwd, self.f_cred, self.f_state, self.f_param, self.f_struct):
                if c is not None:
                    f = compiled_flops(c, d)
                    tot += f / STRUCT_PERIOD if c is self.f_struct else f
            o, i = d[O], d[I]
            tot += 3 * sum({I: i, O: o, M: o * i}[rd.type] for rd in self.prog.regs)
        return tot


# ---------------------------------------------------------------------------
# Trainer
# ---------------------------------------------------------------------------

@dataclass
class RunStatus:
    unstable: np.ndarray
    reason: List[str]


class Trainer:
    """Online/mini-batch training of R runs of the substrate with one learner."""

    def __init__(self, net: Net, learner: Learner, lrs: Sequence[float], kind: str = "reg",
                 time_limit: Optional[float] = None, check_memory: bool = True):
        self.net = net
        self.L = learner
        self.lr = np.asarray(lrs, DT)
        assert self.lr.shape == (net.R,)
        self.kind = kind
        self.alive = np.ones(net.R, bool)
        self.reason = [""] * net.R
        self.t = 0
        self.t_ep = 0
        self.ep_len = 1
        self.boundaries = False
        self.W_ep0 = [w.copy() for w in net.W]
        self.Lbar = None
        self.L_prev = None
        self.loss_hist: List[np.ndarray] = []
        self.loss_ref = None
        self.loss_ema = None
        self.acc = None
        self.acc_n = 0
        self.n_reinit = [0] * net.nl
        self.t0 = time.process_time()
        self.wall0 = time.time()
        self.time_limit = time_limit
        self.check_memory = check_memory
        self.updates_applied = 0
        learner.init(net)

    # --- episodes --------------------------------------------------------------
    def set_episodes(self, ep_len: Optional[int]):
        """ep_len=None: boundary-free task (tep = 0, EPISODE registers never reset)."""
        self.boundaries = ep_len is not None
        self.ep_len = ep_len or 1

    def episode_start(self):
        self.t_ep = 0
        self.W_ep0 = [w.copy() for w in self.net.W]
        self.L.episode_start(self.net, self)

    def tep(self) -> np.ndarray:
        v = (self.t_ep / self.ep_len) if self.boundaries else 0.0
        return np.full((self.net.R, 1), v, DT)

    # --- forward ------------------------------------------------------------------
    def _forward(self, x: np.ndarray, train: bool, need_env: bool = True):
        net = self.net
        R, B = x.shape[0], x.shape[1]
        a = x.astype(DT)
        cache = {"a": [], "z": [], "h": [], "dphi": [], "Weff": [], "g": [], "env": []}
        tep = self.tep()
        for l in range(net.nl):
            o, i = net.sizes[l + 1], net.sizes[l]
            env = {
                "a": a, "W": net.W[l][:, None], "b": net.b[l][:, None],
                "W_ep0": self.W_ep0[l][:, None], "tep": tep,
            }
            if self.L.reads_noise:
                if train:
                    env["xi_I"] = net.noise((i,), B)
                    env["xi_O"] = net.noise((o,), B)
                else:
                    env["xi_I"] = np.zeros((R, 1, i), DT)
                    env["xi_O"] = np.zeros((R, 1, o), DT)
            W_eff, g = self.L.forward_mods(l, env, net, 2)
            if W_eff is None:
                z = np.matmul(a, np.swapaxes(net.W[l], 1, 2))
                Weff_store = net.W[l][:, None]
            elif W_eff.shape[1] == 1:
                z = np.matmul(a, np.swapaxes(W_eff[:, 0], 1, 2))
                Weff_store = W_eff
            else:
                z = np.matmul(W_eff, a[..., None])[..., 0]
                Weff_store = W_eff
            if g is not None:
                z = g * z
            z = z + net.b[l][:, None]
            if l < net.nl - 1:
                h = np.tanh(z)
                dphi = 1.0 - h * h
            else:
                h = z
                dphi = np.ones_like(z)
            cache["a"].append(a)
            cache["z"].append(z)
            cache["h"].append(h)
            cache["dphi"].append(dphi)
            cache["Weff"].append(Weff_store)
            cache["g"].append(g)
            if need_env:
                env.update({"z": z, "h": h, "dphi": dphi})
            cache["env"].append(env)
            a = h
        return cache

    def predict(self, X: np.ndarray, chunk: int = 256) -> np.ndarray:
        outs = []
        for s in range(0, X.shape[1], chunk):
            c = self._forward(X[:, s:s + chunk], train=False, need_env=False)
            outs.append(c["z"][-1])
        return np.concatenate(outs, axis=1)

    # --- one protocol step -----------------------------------------------------------
    def step(self, x: np.ndarray, y: np.ndarray):
        net, Lr = self.net, self.L
        R, B = x.shape[0], x.shape[1]
        if isinstance(Lr, ProgramLearner):
            Lr.example_reset(net)
        with np.errstate(all="ignore"):
            cache = self._forward(x, train=True)
            out = cache["z"][-1]
            if self.kind == "reg":
                e = out - y
                Lex = 0.5 * np.sum(e * e, axis=-1)
            else:  # classification: y integer labels (R, B)
                zmax = out.max(axis=-1, keepdims=True)
                ex = np.exp(out - zmax)
                p = ex / ex.sum(axis=-1, keepdims=True)
                oh = np.zeros_like(p)
                np.put_along_axis(oh, y[..., None].astype(int), 1.0, axis=-1)
                e = p - oh
                Lex = -np.log(np.maximum(np.sum(p * oh, axis=-1), 1e-12))
            e = e.astype(DT)
            Lex = Lex.astype(DT)
            Lm = Lex.mean(axis=1)
            # backward through W_eff and g (held constant)
            if Lr.needs_bp:
                d = [None] * net.nl
                d[-1] = e
                for l in range(net.nl - 1, 0, -1):
                    gd = d[l] if cache["g"][l] is None else cache["g"][l] * d[l]
                    We = cache["Weff"][l]
                    if We.shape[1] == 1:
                        ga = np.matmul(gd, We[:, 0])
                    else:
                        ga = np.matmul(gd[..., None, :], We)[..., 0, :]
                    d[l - 1] = cache["dphi"][l - 1] * ga
                cache["d_bp"] = d
            for l in range(net.nl):
                env = cache["env"][l]
                if l == net.nl - 1:
                    env["e"] = e
                    env["d_fa"] = e
                else:
                    env["e"] = np.zeros((R, 1, net.sizes[l + 1]), DT)
                    if Lr.needs_fa:
                        env["d_fa"] = np.matmul(e, np.swapaxes(net.fb[l], 1, 2))
                if Lr.needs_bp:
                    env["d_bp"] = cache["d_bp"][l]
                env["L"] = Lex
                if self.L_prev is None:
                    env["dL"] = np.zeros_like(Lex)
                    env["Lbar"] = Lm[:, None].astype(DT)
                else:
                    env["dL"] = (Lex - self.L_prev[:, None]).astype(DT)
                    env["Lbar"] = self.Lbar[:, None].astype(DT)
            deltas = Lr.updates(net, self, cache)
            # accumulate and apply
            if self.acc is None:
                self.acc = [[dw.copy(), db.copy()] for dw, db in deltas]
            else:
                for k, (dw, db) in enumerate(deltas):
                    self.acc[k][0] += dw
                    self.acc[k][1] += db
            self.acc_n += 1
            if self.acc_n >= Lr.update_every:
                live = self.alive.astype(DT)
                for l, (dw, db) in enumerate(self.acc):
                    dw = dw / self.acc_n
                    db = db / self.acc_n
                    if Lr.clip:
                        nrm = np.sqrt(np.sum(dw.astype(np.float64) ** 2, axis=(1, 2)))
                        sc = np.where(nrm > 1.0, 1.0 / np.maximum(nrm, 1e-30), 1.0).astype(DT)
                        dw = dw * sc[:, None, None]
                        db = np.clip(db, -1.0, 1.0)
                    step_w = (self.lr * live)[:, None, None] * dw
                    step_b = (self.lr * live)[:, None] * db
                    step_w = np.where(np.isfinite(step_w), step_w, 0).astype(DT)
                    step_b = np.where(np.isfinite(step_b), step_b, 0).astype(DT)
                    net.W[l] += step_w
                    net.b[l] += step_b
                self.acc = None
                self.acc_n = 0
                self.updates_applied += 1
            self.t += 1
            self.t_ep += 1
            if self.t % STRUCT_PERIOD == 0:
                Lr.struct_event(net, self, cache)
            # loss statistics
            if self.L_prev is None:
                self.Lbar = Lm.astype(np.float64)
            else:
                self.Lbar = LBAR_DECAY * self.Lbar + (1 - LBAR_DECAY) * Lm
            self.L_prev = Lm.astype(np.float64)
        self._guards(Lm, cache)
        return cache, Lex, e

    def _guards(self, Lm: np.ndarray, cache):
        Lm = Lm.astype(np.float64)
        bad = ~np.isfinite(Lm)
        self.loss_hist.append(Lm)
        if self.t <= 10:
            self.loss_ref = np.nanmean(np.stack(self.loss_hist), axis=0)
        if self.loss_ema is None:
            self.loss_ema = np.where(np.isfinite(Lm), Lm, 0.0)
        else:
            self.loss_ema = 0.9 * self.loss_ema + 0.1 * np.where(np.isfinite(Lm), Lm, np.inf)
        if self.t > 10:
            bad |= self.loss_ema > DIVERGENCE_FACTOR * self.loss_ref
        if self.t % 50 == 0 or self.t <= 1:
            for l in range(self.net.nl):
                wn = np.sqrt(np.sum(self.net.W[l].astype(np.float64) ** 2, axis=(1, 2)))
                bad |= ~np.isfinite(wn) | (wn > WNORM_MAX)
                bad |= ~np.isfinite(self.net.b[l]).all(axis=1)
            if self.check_memory and rss_mb() > MEM_LIMIT_MB:
                raise OutOfMemory(f"RSS {rss_mb():.0f} MB")
        newly = bad & self.alive
        for r in np.nonzero(newly)[0]:
            self.reason[r] = f"unstable@{self.t}"
        self.alive &= ~bad
        if self.time_limit is not None and time.process_time() - self.t0 > self.time_limit:
            raise Timeout(f"exceeded {self.time_limit}s CPU")

    def status(self) -> RunStatus:
        return RunStatus(~self.alive, list(self.reason))


def base_flops_per_example(net: Net, needs_bp: bool) -> float:
    """Forward + (optional) backward FLOPs of the substrate per example."""
    f = 0.0
    for l in range(net.nl):
        o, i = net.sizes[l + 1], net.sizes[l]
        f += 2 * o * i + 3 * o
        if needs_bp and l > 0:
            f += 2 * o * i + 2 * o
    return f


def learner_flops_per_example(net: Net, learner: Learner) -> float:
    """Per-example FLOPs: substrate forward/backward plus the learner's own work."""
    f = base_flops_per_example(net, learner.needs_bp)
    if isinstance(learner, ProgramLearner):
        f += learner.flops_per_example(net)
        f += sum(3 * (net.sizes[l] * net.sizes[l + 1]) for l in range(net.nl))   # clip + apply
        return f
    P = net.n_params()
    extra = {"SGD": 1, "GPM": 3, "SGDM": 3, "AdamW": 12}.get(learner.name, 1)
    return f + P + extra * P
