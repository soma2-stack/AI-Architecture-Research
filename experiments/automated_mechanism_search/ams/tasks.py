"""Benchmark generators, frozen by prereg v2 sec. 6 (and IMPLEMENTATION_DECISIONS D-TASK-*).

Every generator is a deterministic function of its seed.  Streams use
Generator(PCG64(SeedSequence([seed, stream]))) except the Task-B target matrices,
which follow the literal v2 text Generator(PCG64(seed)).
"""
from __future__ import annotations

import hashlib
from typing import Dict, List, Tuple

import numpy as np

from .substrate import rng_for

DT = np.float32


def _rownorm(A: np.ndarray) -> np.ndarray:
    return A / np.linalg.norm(A, axis=1, keepdims=True)


# ---------------------------------------------------------------------------
# Task B (v2 overlapping shared/private construction)
# ---------------------------------------------------------------------------

class TaskB:
    name = "B"
    D, NC, NP = 32, 8, 12
    C = slice(0, 8)
    P1 = slice(8, 20)
    P2 = slice(20, 32)
    d_in, d_out, kind = 32, 4, "reg"
    batch = 32
    n1 = n2 = 500
    eval_every = 25
    n_eval = 256
    n_gate_pairs = 64
    boundaries = True

    def __init__(self, seed: int):
        self.seed = int(seed)
        g = np.random.Generator(np.random.PCG64(self.seed))
        self.A_c = _rownorm(g.standard_normal((4, 8)))
        self.A_1 = _rownorm(g.standard_normal((4, 12)))
        self.A_2 = _rownorm(g.standard_normal((4, 12)))
        self.train_rng = rng_for(self.seed, 1)
        self.X1_eval, self.Y1_eval = self._sample(1, 256, rng_for(self.seed, 2))
        self.X2_eval, self.Y2_eval = self._sample(2, 256, rng_for(self.seed, 3))

    def make(self, task: int, c: np.ndarray, p: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        n = c.shape[0]
        X = np.zeros((n, self.D))
        X[:, self.C] = c
        if task == 1:
            X[:, self.P1] = p
            Y = c @ self.A_c.T + 0.10 * p @ self.A_1.T
        else:
            X[:, self.P2] = p
            Y = -c @ self.A_c.T + 0.10 * p @ self.A_2.T
        return X.astype(DT), Y.astype(DT)

    def _sample(self, task: int, n: int, rng) -> Tuple[np.ndarray, np.ndarray]:
        c = rng.standard_normal((n, 8))
        p = rng.standard_normal((n, 12))
        return self.make(task, c, p)

    def train_batch(self, step: int) -> Tuple[np.ndarray, np.ndarray]:
        task = 1 if step < self.n1 else 2
        return self._sample(task, self.batch, self.train_rng)

    def gate_pairs(self) -> List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
        rng = rng_for(self.seed, 4)
        out = []
        for _ in range(self.n_gate_pairs):
            c = rng.standard_normal((self.batch, 8))
            p1 = rng.standard_normal((self.batch, 12))
            p2 = rng.standard_normal((self.batch, 12))
            X1, Y1 = self.make(1, c, p1)
            X2, Y2 = self.make(2, c, p2)
            out.append((X1, Y1, X2, Y2))
        return out

    @property
    def n_steps(self) -> int:
        return self.n1 + self.n2


# ---------------------------------------------------------------------------
# Task C* (v2 recurring regimes, no boundary signal)
# ---------------------------------------------------------------------------

class TaskCstar:
    name = "Cstar"
    d_in, d_out, kind = 1, 1, "reg"
    batch = 1
    schedule = (("R0", 256), ("R1", 64), ("R0", 64), ("R1", 64))
    eval_every = 4
    tau = 0.05
    boundaries = False

    def __init__(self, seed: int):
        self.seed = int(seed)
        g = rng_for(self.seed, 5)
        self.omega1 = float(g.uniform(1.4, 1.8))
        self.phi1 = float(g.uniform(np.pi / 3, 2 * np.pi / 3))
        self.train_rng = rng_for(self.seed, 1)
        self.grid = np.linspace(-np.pi, np.pi, 128).astype(DT)[:, None]
        self.Y_grid = {"R0": self.f("R0", self.grid), "R1": self.f("R1", self.grid)}
        self.regime_at = []
        for r, n in self.schedule:
            self.regime_at += [r] * n
        self.entries = []
        t = 0
        for r, n in self.schedule:
            self.entries.append((r, t))
            t += n

    def f(self, regime: str, x: np.ndarray) -> np.ndarray:
        if regime == "R0":
            return np.sin(x).astype(DT)
        return np.sin(self.omega1 * x + self.phi1).astype(DT)

    def train_batch(self, step: int) -> Tuple[np.ndarray, np.ndarray]:
        x = self.train_rng.uniform(-np.pi, np.pi, (1, 1)).astype(DT)
        return x, self.f(self.regime_at[step], x)

    @property
    def n_steps(self) -> int:
        return sum(n for _, n in self.schedule)


# ---------------------------------------------------------------------------
# Task F (v2 fixed 500-update budget)
# ---------------------------------------------------------------------------

class TaskF:
    name = "F"
    d_in, d_out, kind = 20, 2, "cls"
    batch = 32
    n_train, n_ood = 100, 1000
    n_agree_train, n_agree_ood = 90, 100
    n_updates = 500
    eval_every = 25
    boundaries = False

    def __init__(self, seed: int):
        self.seed = int(seed)
        self.Xtr, self.ytr = self._make(self.n_train, self.n_agree_train, rng_for(self.seed, 1))
        self.Xood, self.yood = self._make(self.n_ood, self.n_agree_ood, rng_for(self.seed, 2))
        self.batch_rng = rng_for(self.seed, 3)

    @staticmethod
    def _make(n: int, n_agree: int, rng) -> Tuple[np.ndarray, np.ndarray]:
        X = rng.integers(0, 2, (n, 20))
        y = X[:, 0] ^ X[:, 1] ^ X[:, 2]
        agree = np.zeros(n, bool)
        agree[rng.permutation(n)[:n_agree]] = True
        X[:, 3] = np.where(agree, y, 1 - y)
        return X.astype(DT), y.astype(np.int64)

    def train_batch(self, step: int) -> Tuple[np.ndarray, np.ndarray]:
        idx = self.batch_rng.integers(0, self.n_train, self.batch)
        return self.Xtr[idx], self.ytr[idx]

    @property
    def n_steps(self) -> int:
        return self.n_updates


def discrete_synthesis(X: np.ndarray, y: np.ndarray, max_k: int = 3):
    """Minimal XOR-of-k-bits hypothesis (k = 1..max_k, optionally negated) consistent with
    all training examples; ties -> lexicographically smallest index tuple."""
    import itertools
    Xi = X.astype(np.int64)
    for k in range(1, max_k + 1):
        for idx in itertools.combinations(range(Xi.shape[1]), k):
            par = np.bitwise_xor.reduce(Xi[:, idx], axis=1)
            if np.all(par == y):
                return idx, 0
            if np.all(1 - par == y):
                return idx, 1
    return None, None


def synthesis_predict(X: np.ndarray, idx, neg) -> np.ndarray:
    par = np.bitwise_xor.reduce(X.astype(np.int64)[:, idx], axis=1)
    return par if neg == 0 else 1 - par


# ---------------------------------------------------------------------------
# Task D (baseline-only diagnostic)
# ---------------------------------------------------------------------------

class TaskD:
    name = "D"
    d = 32
    kappas = (1e2, 1e4, 1e6)
    n_steps = 1000
    tau = 1e-4

    def __init__(self, seed: int, kappa: float):
        self.seed, self.kappa = int(seed), float(kappa)
        g = rng_for(self.seed, 6)
        A = g.standard_normal((self.d, self.d))
        Q, R = np.linalg.qr(A)
        Q = Q * np.sign(np.diag(R))[None, :]
        self.Q = Q
        self.lam = np.geomspace(1.0, self.kappa, self.d)
        self.H = (Q * self.lam) @ Q.T
        self.theta0 = rng_for(self.seed, 7).standard_normal(self.d)

    def loss(self, th: np.ndarray) -> float:
        return float(0.5 * th @ self.H @ th)

    def grad(self, th: np.ndarray) -> np.ndarray:
        return self.H @ th


# ---------------------------------------------------------------------------
# Task T0 (sanity filter, AE Stage 1b)
# ---------------------------------------------------------------------------

class TaskT0:
    name = "T0"
    d_in, d_out, kind = 8, 2, "reg"
    batch = 1
    n_steps = 300
    noise = 0.1
    boundaries = False

    def __init__(self, seed: int):
        self.seed = int(seed)
        g = rng_for(self.seed, 8)
        self.Wt = g.normal(0, 1 / np.sqrt(8), (2, 8))
        self.train_rng = rng_for(self.seed, 1)

    def train_batch(self, step: int):
        x = self.train_rng.standard_normal((1, 8))
        y = x @ self.Wt.T + self.noise * self.train_rng.standard_normal((1, 2))
        return x.astype(DT), y.astype(DT)


# ---------------------------------------------------------------------------
# Reserved Tasks A and E (finalists only)
# ---------------------------------------------------------------------------

class TaskA:
    name = "A"
    d, k = 16, 4
    horizons = (100, 250, 500, 1000)

    def __init__(self, seed: int, T: int):
        self.seed, self.T = int(seed), int(T)
        self.rng = rng_for(self.seed, 9)

    def episode(self):
        T = self.T
        X = self.rng.standard_normal((T, self.d)).astype(DT)
        X[:, 0] = 0.0
        X[:, 1] = 0.0
        t1 = int(self.rng.integers(1, 11)) - 1
        s = self.rng.choice([-1.0, 1.0], self.k)
        X[t1, :] = 0.0
        X[t1, 0] = 1.0
        X[t1, 2:2 + self.k] = s
        X[T - 1, :] = 0.0
        X[T - 1, 1] = 1.0
        return X, s.astype(DT), t1


class TaskE:
    name = "E"
    n_states = 5
    lengths = (10, 50, 200)
    n_episodes = 128
    d_in = 5 + 5 + 3 + 5
    d_out = 5

    def __init__(self, seed: int, L: int):
        self.seed, self.L = int(seed), int(L)
        self.rng = rng_for(self.seed, 9)

    @staticmethod
    def succ(s: int) -> int:
        return (s + 1) % 5

    def _x(self, sym=None, state=None, flag=0, noise=None):
        x = np.zeros(self.d_in, DT)
        if sym is not None:
            x[sym] = 1.0
        if state is not None:
            x[5 + state] = 1.0
        x[10 + flag] = 1.0
        if noise is not None:
            x[13:] = noise
        return x

    def episodes(self):
        """Yields (X steps, y targets, is_query mask) per episode; query states balanced."""
        qs = np.tile(np.arange(5), self.n_episodes // 5 + 1)[:self.n_episodes]
        self.rng.shuffle(qs)
        for e in range(self.n_episodes):
            perm = self.rng.permutation(5)         # symbol -> latent state
            sym_of_state = np.argsort(perm)
            X, Y, Q = [], [], []
            for sym in self.rng.permutation(5):
                X.append(self._x(sym=sym, state=int(perm[sym]), flag=0))
                Y.append(sym)
                Q.append(False)
            for _ in range(self.L):
                X.append(self._x(flag=1, noise=self.rng.standard_normal(5)))
                Y.append(int(self.rng.integers(0, 5)))
                Q.append(False)
            s = int(qs[e])
            qsym = int(sym_of_state[s])
            X.append(self._x(sym=qsym, flag=2))
            Y.append(int(sym_of_state[self.succ(s)]))
            Q.append(True)
            yield np.stack(X), np.asarray(Y), np.asarray(Q)


def generator_fingerprint(seed: int = 100) -> Dict[str, str]:
    """sha256 of representative generated data, recorded in the run manifest."""
    h = {}
    b = TaskB(seed)
    h["B"] = hashlib.sha256(b.A_c.tobytes() + b.A_1.tobytes() + b.A_2.tobytes() +
                            b.X1_eval.tobytes() + b.Y2_eval.tobytes()).hexdigest()
    c = TaskCstar(seed)
    h["Cstar"] = hashlib.sha256(np.array([c.omega1, c.phi1]).tobytes() + c.Y_grid["R1"].tobytes()).hexdigest()
    f = TaskF(seed)
    h["F"] = hashlib.sha256(f.Xtr.tobytes() + f.ytr.tobytes() + f.Xood.tobytes()).hexdigest()
    d = TaskD(seed, 1e4)
    h["D"] = hashlib.sha256(d.H.tobytes() + d.theta0.tobytes()).hexdigest()
    e = TaskE(seed, 10)
    X, Y, Q = next(e.episodes())
    h["E"] = hashlib.sha256(X.tobytes() + Y.tobytes()).hexdigest()
    a = TaskA(seed, 100)
    X, s, t1 = a.episode()
    h["A"] = hashlib.sha256(X.tobytes() + s.tobytes()).hexdigest()
    t0 = TaskT0(seed)
    h["T0"] = hashlib.sha256(t0.Wt.tobytes()).hexdigest()
    return h
