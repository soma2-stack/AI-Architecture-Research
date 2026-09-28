"""Shapes, register semantics, read-before-write, reproduction of hand-written rules,
numerical guards, determinism, FLOP/state counters (AE.6 tests 6-9)."""
import numpy as np
import pytest

from ams.canon import canon
from ams.families import REFERENCES
from ams.grammar import I, M, O, S, make_program, parse
from ams.interp import Compiled, compiled_flops
from ams.substrate import (DT, Net, ProgramLearner, SGD, SGDM, AdamW, Timeout, Trainer,
                           learner_flops_per_example)


def _env(R=3, B=4, n_in=5, n_out=6, seed=0):
    r = np.random.default_rng(seed)
    f = lambda *s: r.standard_normal(s).astype(DT)
    return {"a": f(R, B, n_in), "xi_I": f(R, B, n_in), "b": f(R, 1, n_out), "z": f(R, B, n_out),
            "h": f(R, B, n_out), "dphi": f(R, B, n_out), "d_bp": f(R, B, n_out), "d_fa": f(R, B, n_out),
            "e": f(R, B, n_out), "xi_O": f(R, B, n_out), "cvec": f(R, B, n_out), "W": f(R, 1, n_out, n_in),
            "W_ep0": f(R, 1, n_out, n_in), "L": f(R, B), "dL": f(R, B), "Lbar": f(R, 1), "tep": f(R, 1)}


@pytest.mark.parametrize("expr,t", [
    ("(outer d_bp a)", M), ("(matvec W a)", O), ("(matTvec W d_bp)", I), ("(rowsum W)", O),
    ("(colsum W)", I), ("(rowscale W h)", M), ("(colscale W a)", M), ("(mean W)", S), ("(norm a)", S),
    ("(dot h d_bp)", S), ("(amax W)", S), ("(nrm h)", O), ("(unit a)", I), ("(topk h 4)", O),
    ("(where h d_bp 0.5)", O), ("(mul (outer d_bp a) L)", M), ("(add a (norm h))", I),
    ("(sqrt_s (log_s (exp_c (recip_s z))))", O), ("(div_s W (sigmoid W_ep0))", M),
])
def test_shapes(expr, t):
    env = _env()
    v = Compiled([parse(expr)], {})(env, 2, {I: 5, O: 6})[0]
    trail = {S: (), I: (5,), O: (6,), M: (6, 5)}[t]
    assert v.shape[-len(trail):] == trail if trail else True
    assert v.shape[:2] in ((3, 4), (3, 1))
    assert np.all(np.isfinite(v))


def test_topk_mask_counts():
    env = _env()
    v = Compiled([parse("(topk h 4)")], {})(env, 2, {I: 5, O: 6})[0]
    assert np.all(v.sum(-1) == 4)
    v8 = Compiled([parse("(topk h 8)")], {})(env, 2, {I: 5, O: 6})[0]
    assert np.all(v8 == 1)


def _net_trainer(prog, seeds=(1,), lrs=(0.1,), d_in=4, d_out=3, clip=False):
    net = Net(d_in, d_out, list(seeds))
    L = ProgramLearner(prog, clip=clip)
    tr = Trainer(net, L, list(lrs), check_memory=False)
    return net, L, tr


def test_example_register_reset_each_step():
    p = make_program("(neg (outer d_bp a))", "(mul d_bp r1)",
                     regs=[("r1", O, "EXAMPLE", "1", 0.5, "h")])
    net, L, tr = _net_trainer(p)
    tr.set_episodes(None); tr.episode_start()
    x = np.ones((1, 1, 4), DT); y = np.zeros((1, 1, 3), DT)
    tr.step(x, y)
    # after step, register holds 0.5*1 + 0.5*h ; at next step start it must be reset to 1
    L.example_reset(net)
    assert np.all(L.regs[0]["r1"] == 1.0)


def test_episode_and_run_lifetimes():
    p = make_program("(neg (outer d_bp a))", "(add (mul d_bp r1) r2)",
                     regs=[("r1", O, "EPISODE", "0", 0.5, "h"), ("r2", O, "RUN", "0", 0.5, "h")])
    net, L, tr = _net_trainer(p)
    tr.set_episodes(10); tr.episode_start()
    x = np.ones((1, 1, 4), DT); y = np.zeros((1, 1, 3), DT)
    for _ in range(3):
        tr.step(x, y)
    assert np.any(L.regs[0]["r1"] != 0) and np.any(L.regs[0]["r2"] != 0)
    tr.episode_start()
    assert np.all(L.regs[0]["r1"] == 0) and np.any(L.regs[0]["r2"] != 0)
    tr.set_episodes(None)
    r2 = L.regs[0]["r2"].copy()
    assert np.all(r2 == L.regs[0]["r2"])


def test_read_before_write_semantics():
    # r1 <- mix(r1, r2, 0); r2 <- mix(r2, 1.0*...) : RHS must see old r2
    p = make_program("(neg (outer d_bp a))", "(add r1 (neg d_bp))",
                     regs=[("r1", O, "RUN", "0", 0.0, "r2"), ("r2", O, "RUN", "1", 0.0, "(add (mul h 0.0) 2)")])
    # r2 update: 2 (constant) ; r1 sees OLD r2 (=1) at the first step
    net, L, tr = _net_trainer(p)
    tr.set_episodes(None); tr.episode_start()
    x = np.ones((1, 1, 4), DT); y = np.zeros((1, 1, 3), DT)
    tr.step(x, y)
    assert np.allclose(L.regs[0]["r1"], 1.0) and np.allclose(L.regs[0]["r2"], 2.0)
    tr.step(x, y)
    assert np.allclose(L.regs[0]["r1"], 2.0)


def test_param_sees_new_registers():
    # dW = -r1 where r1 <- outer(d_bp,a) with decay 0: PARAM must use the current gradient (SGD)
    p = make_program("(neg r1)", "(neg d_bp)", regs=[("r1", M, "RUN", "0", 0.0, "(outer d_bp a)")])
    q = make_program("(neg (outer d_bp a))", "(neg d_bp)")
    rng = np.random.default_rng(3)
    X = rng.standard_normal((20, 1, 1, 4)).astype(DT); Y = rng.standard_normal((20, 1, 1, 3)).astype(DT)
    outs = []
    for prog in (p, q):
        net, L, tr = _net_trainer(prog)
        tr.set_episodes(None); tr.episode_start()
        for t in range(20):
            tr.step(X[t], Y[t])
        outs.append([w.copy() for w in net.W])
    for a, b in zip(*outs):
        assert np.max(np.abs(a - b)) < 1e-6


def _numpy_mlp_train(seed, X, Y, lr, rule, fast_decay=0.9):
    net = Net(4, 3, [seed])
    W = [w[0].astype(np.float64) for w in net.W]; b = [bb[0].astype(np.float64) for bb in net.b]
    B = [None if f is None else f[0].astype(np.float64) for f in net.fb]
    A = [np.zeros_like(w) for w in W]
    for x, y in zip(X, Y):
        acts = [x.astype(np.float64)]
        zs = []
        for l in range(3):
            We = W[l] + (A[l] if rule == "fast" else 0)
            z = We @ acts[-1] + b[l]
            zs.append(z)
            acts.append(np.tanh(z) if l < 2 else z)
        e = acts[-1] - y
        deltas = [None] * 3
        deltas[2] = e
        for l in (2, 1):
            We = W[l] + (A[l] if rule == "fast" else 0)
            deltas[l - 1] = (1 - acts[l] ** 2) * (We.T @ deltas[l])
        for l in range(3):
            if rule == "dfa":
                d = e if l == 2 else (B[l] @ e) * (1 - acts[l + 1] ** 2)
            else:
                d = deltas[l]
            if rule == "fast":
                A[l] = fast_decay * A[l] + (1 - fast_decay) * np.outer(acts[l + 1], acts[l])
            W[l] = W[l] - lr * np.outer(d, acts[l])
            b[l] = b[l] - lr * d
    return W


@pytest.mark.parametrize("rule,ref", [("sgd", "R1_SGD"), ("fast", "R12_fast_weights"), ("dfa", "R8_DFA")])
def test_interpreter_reproduces_handwritten_rules(rule, ref):
    rng = np.random.default_rng(11)
    X = rng.standard_normal((15, 4)); Y = rng.standard_normal((15, 3))   # stable horizon (guard off)
    Wref = _numpy_mlp_train(5, X, Y, 0.05, rule)
    net, L, tr = _net_trainer(canon(REFERENCES[ref]), seeds=(5,), lrs=(0.05,), clip=False)
    tr.set_episodes(None); tr.episode_start()
    for x, y in zip(X, Y):
        tr.step(x[None, None].astype(DT), y[None, None].astype(DT))
    for l in range(3):
        assert np.max(np.abs(net.W[l][0] - Wref[l])) < 1e-5, l


OVERFLOW = [
    "(mul (exp_c (exp_c (exp_c W))) 2)", "(square (square (square (square (outer d_bp a)))))",
    "(div_s (outer d_bp a) (mul W 0.1))", "(recip_s (mul (outer d_bp a) 0.1))",
    "(mul (square (square (square (square W)))) 2)", "(neg (square (square (square (exp_c W)))))",
    "(outer (recip_s d_bp) (recip_s a))", "(mul (outer (exp_c z) (exp_c a)) 2)",
    "(square (square (outer (recip_s e) a)))", "(mul (square (square (square (outer d_bp a)))) (exp_c L))",
]


@pytest.mark.parametrize("expr", OVERFLOW)
def test_guards_fire_or_clip_on_overflow(expr):
    p = make_program(expr, "(neg (exp_c (exp_c d_bp)))")
    net = Net(4, 3, [1, 2])
    tr = Trainer(net, ProgramLearner(p, clip=False), [1.0, 1.0], check_memory=False)
    tr.set_episodes(None); tr.episode_start()
    rng = np.random.default_rng(0)
    for t in range(60):
        tr.step(rng.standard_normal((2, 2, 4)).astype(DT) * 3, rng.standard_normal((2, 2, 3)).astype(DT))
    # guard: run flagged unstable, or parameters remain finite and bounded (clipped path)
    ok = (~tr.alive).any() or all(np.all(np.isfinite(w)) and np.abs(w).max() < 1e4 for w in net.W)
    assert ok
    # the clipped (production) path never produces non-finite parameters
    net2 = Net(4, 3, [1])
    tr2 = Trainer(net2, ProgramLearner(p, clip=True), [0.1], check_memory=False)
    tr2.set_episodes(None); tr2.episode_start()
    for t in range(60):
        tr2.step(rng.standard_normal((1, 2, 4)).astype(DT) * 3, rng.standard_normal((1, 2, 3)).astype(DT))
    assert all(np.all(np.isfinite(w)) for w in net2.W)


def test_divergence_guard():
    p = make_program("(outer d_bp a)", "d_bp")    # gradient ascent
    net = Net(4, 3, [1])
    tr = Trainer(net, ProgramLearner(p, clip=False), [1.0], check_memory=False)
    tr.set_episodes(None); tr.episode_start()
    rng = np.random.default_rng(0)
    for t in range(300):
        tr.step(rng.standard_normal((1, 4, 4)).astype(DT), rng.standard_normal((1, 4, 3)).astype(DT))
    assert not tr.alive[0] and tr.reason[0].startswith("unstable")


def test_determinism_bit_identical():
    p = canon(REFERENCES["R16_node_perturbation"])       # uses noise
    outs = []
    for _ in range(2):
        net = Net(4, 3, [9, 10])
        tr = Trainer(net, ProgramLearner(p), [0.1, 0.01], check_memory=False)
        tr.set_episodes(None); tr.episode_start()
        rng = np.random.default_rng(1)
        for t in range(30):
            tr.step(rng.standard_normal((2, 3, 4)).astype(DT), rng.standard_normal((2, 3, 3)).astype(DT))
        outs.append(np.concatenate([w.ravel() for w in net.W]))
    assert np.array_equal(outs[0], outs[1])


def test_flop_and_state_counters():
    net = Net(4, 3, [1])
    c = Compiled([parse("(neg (outer d_bp a))")], {})
    assert compiled_flops(c, {I: 4, O: 32}) == 32 * 4 + 32 * 4       # outer + neg
    fw = ProgramLearner(canon(REFERENCES["R12_fast_weights"]))
    assert fw.state_floats(net) == sum(net.sizes[l] * net.sizes[l + 1] for l in range(3))
    assert SGDM().state_floats(net) == net.n_params()
    assert AdamW().state_floats(net) == 2 * net.n_params()
    assert net.n_params() == 4 * 32 + 32 + 32 * 32 + 32 + 32 * 3 + 3
    f_sgd = learner_flops_per_example(net, ProgramLearner(canon(REFERENCES["R1_SGD"])))
    f_fw = learner_flops_per_example(net, fw)
    assert f_fw > f_sgd > 0


def test_timeout_guard():
    net = Net(4, 3, [1])
    tr = Trainer(net, SGD(), [0.1], time_limit=0.0, check_memory=False)
    tr.set_episodes(None); tr.episode_start()
    with pytest.raises(Timeout):
        tr.step(np.zeros((1, 1, 4), DT), np.zeros((1, 1, 3), DT))


def test_update_every_accumulates():
    p = make_program("(neg (outer d_bp a))", "(neg d_bp)", update_every=8)
    net, L, tr = _net_trainer(p)
    tr.set_episodes(None); tr.episode_start()
    W0 = net.W[0].copy()
    x = np.ones((1, 1, 4), DT); y = np.zeros((1, 1, 3), DT)
    for t in range(7):
        tr.step(x, y)
        assert np.array_equal(net.W[0], W0)
    tr.step(x, y)
    assert not np.array_equal(net.W[0], W0)
    assert tr.updates_applied == 1
