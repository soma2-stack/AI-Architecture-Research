"""Benchmark determinism, exact v2 schedules, metric correctness, Task-B gate implementation."""
import math

import numpy as np
import pytest

from ams import metrics as MX
from ams.runners import first_layer_grad, taskB_gate
from ams.substrate import Net
from ams.tasks import (TaskA, TaskB, TaskCstar, TaskD, TaskE, TaskF, TaskT0, discrete_synthesis,
                       generator_fingerprint, synthesis_predict)


# ---------------------------------------------------------------- determinism

def test_generators_deterministic_and_seed_dependent():
    assert generator_fingerprint(100) == generator_fingerprint(100)
    a, b = generator_fingerprint(100), generator_fingerprint(101)
    assert all(a[k] != b[k] for k in a)


def test_train_streams_deterministic():
    for T in (TaskB, TaskCstar, TaskF, TaskT0):
        t1 = T(3)
        x1 = [t1.train_batch(t)[0] for t in range(5)]
        t2 = T(3)
        x2 = [t2.train_batch(t)[0] for t in range(5)]
        assert all(np.array_equal(u, v) for u, v in zip(x1, x2))


# ---------------------------------------------------------------- Task B (v2)

def test_taskB_v2_construction():
    t = TaskB(123)
    g = np.random.Generator(np.random.PCG64(123))
    Ac = g.standard_normal((4, 8)); Ac /= np.linalg.norm(Ac, axis=1, keepdims=True)
    assert np.allclose(t.A_c, Ac)
    for A in (t.A_c, t.A_1, t.A_2):
        assert np.allclose(np.linalg.norm(A, axis=1), 1.0)
    X, Y = t.train_batch(0)
    assert X.shape == (32, 32) and Y.shape == (32, 4)
    assert np.all(X[:, 20:] == 0) and np.any(X[:, 8:20] != 0)
    X2, Y2 = t.train_batch(500)
    assert np.all(X2[:, 8:20] == 0) and np.any(X2[:, 20:] != 0)
    c, p1 = X[:, :8].astype(float), X[:, 8:20].astype(float)
    assert np.allclose(Y, c @ t.A_c.T + 0.10 * p1 @ t.A_1.T, atol=1e-5)
    c2, p2 = X2[:, :8].astype(float), X2[:, 20:].astype(float)
    assert np.allclose(Y2, -c2 @ t.A_c.T + 0.10 * p2 @ t.A_2.T, atol=1e-5)
    assert t.X1_eval.shape == (256, 32) and t.X2_eval.shape == (256, 32)
    assert not np.array_equal(t.X1_eval[:, :8], t.X2_eval[:, :8])     # separate streams
    assert TaskB.n1 == 500 and TaskB.n2 == 500 and TaskB.eval_every == 25 and TaskB.batch == 32


def test_taskB_gate_pairs_share_c():
    pairs = TaskB(5).gate_pairs()
    assert len(pairs) == 64
    for X1, Y1, X2, Y2 in pairs[:3]:
        assert np.array_equal(X1[:, :8], X2[:, :8]) and X1.shape == (32, 32)


def test_taskB_gate_gradient_numeric():
    t = TaskB(9)
    net = Net(32, 4, [9])
    X, Y, _, _ = t.gate_pairs()[0]
    g = first_layer_grad(net, X, Y)
    Ws = [w[0].astype(float) for w in net.W]
    def loss(W0):
        a = X.astype(float)
        for l, W in enumerate([W0] + Ws[1:]):
            z = a @ W.T
            a = np.tanh(z) if l < 2 else z
        return 0.5 * np.mean(np.sum((a - Y) ** 2, 1))
    eps = 1e-6
    for (i, j) in [(0, 0), (5, 3), (31, 31)]:
        Wp = Ws[0].copy(); Wp[i, j] += eps
        Wm = Ws[0].copy(); Wm[i, j] -= eps
        assert abs((loss(Wp) - loss(Wm)) / (2 * eps) - g[i, j]) < 1e-6


def test_taskB_gate_deterministic():
    a, b = taskB_gate(100), taskB_gate(100)
    assert a["mean_cos"] == b["mean_cos"] and a["n_pairs"] == 64


# ---------------------------------------------------------------- Task C* (v2)

def test_taskC_v2_schedule():
    t = TaskCstar(7)
    assert [n for _, n in t.schedule] == [256, 64, 64, 64] and [r for r, _ in t.schedule] == ["R0", "R1", "R0", "R1"]
    assert t.n_steps == 448 and TaskCstar.eval_every == 4 and TaskCstar.tau == 0.05
    assert 1.4 <= t.omega1 <= 1.8 and np.pi / 3 <= t.phi1 <= 2 * np.pi / 3
    assert t.grid.shape == (128, 1) and np.isclose(t.grid[0, 0], -np.pi) and np.isclose(t.grid[-1, 0], np.pi)
    x, y = t.train_batch(0)
    assert x.shape == (1, 1) and TaskCstar.d_in == 1                   # no regime/boundary input
    assert not TaskCstar.boundaries
    assert t.regime_at[255] == "R0" and t.regime_at[256] == "R1" and t.regime_at[320] == "R0" and t.regime_at[384] == "R1"
    xs = np.array([t.train_batch(k)[0][0, 0] for k in range(300)])
    assert xs.min() >= -np.pi and xs.max() <= np.pi


# ---------------------------------------------------------------- Task F (v2)

def test_taskF_v2():
    t = TaskF(11)
    assert t.Xtr.shape == (100, 20) and t.Xood.shape == (1000, 20)
    ytr = (t.Xtr[:, 0].astype(int) ^ t.Xtr[:, 1].astype(int) ^ t.Xtr[:, 2].astype(int))
    assert np.array_equal(ytr, t.ytr)
    assert int((t.Xtr[:, 3] == t.ytr).sum()) == 90
    assert int((t.Xood[:, 3] == t.yood).sum()) == 100
    assert TaskF.n_updates == 500 and TaskF.batch == 32 and TaskF.eval_every == 25
    idx, neg = discrete_synthesis(t.Xtr, t.ytr)
    assert idx == (0, 1, 2) and neg == 0
    assert np.mean(synthesis_predict(t.Xood, idx, neg) == t.yood) == 1.0


# ---------------------------------------------------------------- Task D, E, A

def test_taskD():
    for k in (1e2, 1e4, 1e6):
        d = TaskD(3, k)
        ev = np.linalg.eigvalsh(d.H)
        assert np.isclose(ev.min(), 1.0) and np.isclose(ev.max() / ev.min(), k, rtol=1e-6)
        assert np.allclose(d.Q.T @ d.Q, np.eye(32), atol=1e-10)
    assert TaskD.kappas == (1e2, 1e4, 1e6) and TaskD.n_steps == 1000


def test_taskE_protocol():
    e = TaskE(4, 10)
    eps = list(e.episodes())
    assert len(eps) == 128
    X, Y, Q = eps[0]
    assert X.shape[0] == 5 + 10 + 1 and Q.sum() == 1 and Q[-1]
    counts = np.bincount([np.argmax(ep[0][-1][:5]) for ep in eps], minlength=5)
    assert counts.sum() == 128


def test_taskA():
    a = TaskA(1, 100)
    X, s, t1 = a.episode()
    assert X.shape == (100, 16) and X[t1, 0] == 1 and X[-1, 1] == 1 and 0 <= t1 <= 9


# ---------------------------------------------------------------- metrics

def test_retention_formula():
    assert MX.retention_B(1.0, 0.0, 0.0) == 100.0
    assert MX.retention_B(1.0, 0.0, 1.0) == 0.0
    assert MX.retention_B(1.0, 0.0, 0.25) == 75.0
    assert MX.retention_B(1.0, 0.0, 5.0) == 0.0            # clipped
    assert MX.forgetting_B(1.0, 0.0, 0.25) == 25.0
    assert MX.retention_B(0.5, 0.5, 0.5) == 100.0          # denominator floor


def test_half_life():
    steps = list(range(0, 129, 4))
    mse = [1.0] * len(steps)
    entry = 64
    i = steps.index(entry)
    for k in range(i, len(steps)):
        mse[k] = 1.0 - 0.1 * (k - i)
    # midpoint (1+0.05)/2 = 0.525 -> first value <= 0.525 at 0.5 (k-i = 5) -> 20 updates
    assert MX.half_life(steps, mse, entry, 0.05) == 20.0
    assert MX.half_life(steps, [0.01] * len(steps), entry, 0.05) == 0.0
    assert math.isinf(MX.half_life(steps, [1.0] * len(steps), entry, 0.05))
    assert math.isinf(MX.median_hl([4.0, math.inf]))
    assert MX.censor(math.inf) == 128.0


def test_return_ok_and_sgg():
    assert MX.return_ok(0.1, 0.109) and not MX.return_ok(0.1, 0.12)
    assert MX.return_ok(0.001, 0.0105) and not MX.return_ok(0.001, 0.012)
    assert MX.sgg(1.0, 0.2) == pytest.approx(80.0)


def test_generic_metrics():
    assert MX.steps_to_threshold([3, 2, 1, 0.5], 1.0) == 2
    assert math.isinf(MX.steps_to_threshold([3, 2], 1.0))
    assert MX.aulc([0, 1]) == 0.5
    assert MX.forgetting_acc([0.5, 1.0, 0.8, 0.5], 1) == pytest.approx(50.0)
    assert MX.bwt(0.9, 0.6) == pytest.approx(-0.3)
    assert MX.eff_update(1.0, 0.5, 10) == pytest.approx(0.05)
    assert MX.retention_half_life([0, 1, 2, 3], [1.0, 0.9, 0.6, 0.4], 0) == 3.0
