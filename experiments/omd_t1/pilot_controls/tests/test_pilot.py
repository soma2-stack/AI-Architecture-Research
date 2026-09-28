"""OMD-PILOT-1 infrastructure tests. No official seeds are trained here; the end-to-end checks use
synthetic oracle controllers and dev seeds >= 9000."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omdp import causal, extract as X, judge, streams, teachers, transplant  # noqa: E402
from omdp import instrument as ins  # noqa: E402
from omdp.config import CONFIG, EVENT_EVICT, EVENT_FILL, EVENT_HIT  # noqa: E402
from omdp.controller import NeuralController, generic_cl, generic_tf, np_choose  # noqa: E402

DEV = 9101


def _run(policy, seq, C):
    ids = {k: i for i, k in enumerate(sorted(set(seq)))}
    tr = teachers.simulate(policy, np.array([ids[k] for k in seq]), C)
    return tr


def _evicted_item(seq, tr, C):
    """Map eviction events to the evicted item labels."""
    items = [None] * C
    out = []
    for t, x in enumerate(seq):
        e, s = int(tr["etype"][t]), int(tr["slot"][t])
        if e == EVENT_EVICT:
            out.append(items[s])
        if e != EVENT_HIT:
            items[s] = x
    return out


# ------------------------------------------------------------------------------------ teachers
def test_lru():
    seq = list("abac")
    assert _evicted_item(seq, _run("LRU", seq, 2), 2) == ["b"]


def test_lfu():
    seq = list("abac")
    assert _evicted_item(seq, _run("LFU", seq, 2), 2) == ["b"]
    seq = list("ababbc")  # a: 1 hit, b: 2 hits
    assert _evicted_item(seq, _run("LFU", seq, 2), 2) == ["a"]
    seq = list("abcd")  # all zero counts -> LRU tie-break
    assert _evicted_item(seq, _run("LFU", seq, 3), 3) == ["a"]


def test_twoq():
    seq = list("abac")
    assert _evicted_item(seq, _run("TWOQ", seq, 2), 2) == ["b"]
    seq = list("ababc")  # both protected; a last accessed at t=2, b at t=3
    assert _evicted_item(seq, _run("TWOQ", seq, 2), 2) == ["a"]
    seq = list("abcabd")  # a, b protected; c probationary -> c evicted even though newest
    assert _evicted_item(seq, _run("TWOQ", seq, 3), 3) == ["c"]


def test_sieve():
    # C=3: a b c, hit a, d: hand at tail a (visited -> clear), b unvisited -> evict b; hand -> c
    # e: start at c (unvisited) -> evict c; hand -> d. f: start at d -> evict d; hand -> e
    seq = list("abcadef")
    assert _evicted_item(seq, _run("SIEVE", seq, 3), 3) == ["b", "c", "d"]
    # wrap-around: a b c, hit a b c, d: all visited -> clear all, wrap, evict a
    seq = list("abcabcd")
    assert _evicted_item(seq, _run("SIEVE", seq, 3), 3) == ["a"]


def test_track_matches_own_run():
    req, _, _ = streams.make_stream(DEV, 3000)
    for p in CONFIG["controls"]:
        tr = teachers.simulate(p, req, 16)
        local, own = teachers.track(p, req, 16, tr["etype"], tr["slot"])
        ev = tr["etype"] == EVENT_EVICT
        assert np.array_equal(own[ev], tr["slot"][ev]), p
        assert np.array_equal(local, tr["local"]), p


# ------------------------------------------------------------------------------------ streams
def test_stream_deterministic():
    a = streams.make_stream(DEV, 5000)
    b = streams.make_stream(DEV, 5000)
    assert np.array_equal(a[0], b[0]) and len(a[0]) == 5000
    assert a[0].min() >= 0 and a[0].max() < CONFIG["N"]
    assert {s["type"] for s in a[2]} <= set(streams.SEG_TYPES)


# ------------------------------------------------------------------------------------ instrument
def test_param_cap():
    assert ins.n_params(ins.init_params(0)) <= CONFIG["instrument"]["param_cap"]


def test_lazy_contract_and_equivariance():
    req, _, _ = streams.make_stream(DEV, 1500)
    p = ins.init_params(3)
    out = ins.to_numpy(ins.cl_rollout(p, req))
    H = out["h_pre"]
    for t in range(len(req) - 1):
        changed = np.where(np.any(H[t + 1] != H[t], axis=1))[0]
        assert set(changed) <= {int(out["slot"][t])}
    ctrl = NeuralController(p)
    rng = np.random.default_rng(0)
    for t in np.where(out["etype"] == EVENT_EVICT)[0][:50]:
        h, g, dt = H[t], out["g_pre"][t], out["dt"][t]
        pi = rng.permutation(16)
        S = ctrl.score(h, g, dt)
        assert np.array_equal(ctrl.score(h[pi], g, dt[pi]).view(np.uint32), S[pi].view(np.uint32))


def test_jit_rollout_matches_python():
    req, _, _ = streams.make_stream(DEV, 800)
    p = ins.init_params(5)
    a = ins.to_numpy(ins.cl_rollout(p, req))
    b = generic_cl(NeuralController(p), req)
    assert np.array_equal(a["etype"], b["etype"]) and np.array_equal(a["slot"], b["slot"])
    assert np.allclose(a["hs_post"], b["hs_post"], atol=1e-5)
    tr = teachers.simulate("LRU", req, 16)
    c = NeuralController(p).tf(tr["etype"], tr["slot"], tr["dt"], tr["resident"])
    d = generic_tf(NeuralController(p), tr["etype"], tr["slot"], tr["dt"], tr["resident"])
    ev = tr["etype"] == EVENT_EVICT
    assert np.array_equal(np.asarray(c["victim"])[ev], d["victim"][ev])


def test_tie_break():
    S = np.array([1.0, 0.5, 0.5, 2.0], np.float32)
    dt = np.array([3, 4, 9, 1], np.float32)
    res = np.ones(4, bool)
    assert np_choose(S, dt, res) == 2
    dt[2] = 4
    assert np_choose(S, dt, res) == 1
    import jax.numpy as jnp
    assert int(ins.choose_j(jnp.asarray(S), jnp.asarray(dt), jnp.asarray(res))) == 1


# ------------------------------------------------------------------------------------ oracle controllers
class Oracle:
    """Exact planted policy in controller form: h = (A @ [state, 0] + b), score lexicographic."""

    def __init__(self, kind, seed=0):
        self.kind = kind
        r = np.random.default_rng(seed)
        self.A = np.array([[1.3, 0.4], [-0.2, 0.9]], np.float32)
        self.b = r.standard_normal(2).astype(np.float32)

    def _state(self, h):
        return np.linalg.solve(self.A, (np.atleast_2d(h) - self.b).T).T[:, 0]

    def _enc(self, s):
        return (self.A @ np.array([s, 0.0], np.float32) + self.b).astype(np.float32)

    def score(self, h, g, dt):
        st = np.round(self._state(h))
        return (st * 10.0 - np.log1p(np.asarray(dt, np.float64)) / 8.0).astype(np.float32)

    def hit(self, hi, g, dti):
        st = np.round(self._state(hi))[0]
        nxt = st + 1 if self.kind == "LFU" else (1 if self.kind == "TWOQ" else 0)
        return self._enc(nxt)

    def ins(self, g):
        return self._enc(0)

    def glob(self, g, is_hit, is_ev, hs, dts):
        return np.asarray(g, np.float32)

    def cl(self, req):
        return generic_cl(self, req)

    def tf(self, etype, slot, dt, resident):
        return generic_tf(self, etype, slot, dt, resident)


def _blind_trajs(ctrl, seeds, length):
    trajs, reqs = [], []
    for s in seeds:
        req, _, _ = streams.make_stream(s, length)
        o = ctrl.cl(req)
        ev = o["etype"] == EVENT_EVICT
        trajs.append({"etype": o["etype"], "slot": o["slot"], "hs_post": o["hs_post"],
                      "g_pre": o["g_pre"], "g_post": o["g_post"], "S_ev": o["S"][ev]})
        reqs.append(req)
    return trajs, reqs


@pytest.mark.parametrize("kind,expect", [("LRU", 1), ("TWOQ", 2), ("LFU", None)])
def test_extract_and_judge_oracles(kind, expect):
    ctrl = Oracle(kind)
    trajs, reqs = _blind_trajs(ctrl, [9201, 9202], 2500)
    out, abstraction = X.extract([dict(t) for t in trajs])
    assert out["status"] == "COMPACT RULE", out
    if expect is not None:
        assert out["stats"]["n_classes"] == expect
    assert out["rule"]["recency"] == "oldest_first"
    teach = [teachers.simulate(kind, r, 16, record_local=False) for r in reqs]
    j = judge.judge(out, kind, trajs, reqs, teach)
    assert j["pass"], j
    # a wrong planted label must fail the judge (e.g. LRU rule judged as LFU or vice versa)
    wrong = {"LRU": "TWOQ", "TWOQ": "LRU", "LFU": "TWOQ"}[kind]
    teach_w = [teachers.simulate(wrong, r, 16, record_local=False) for r in reqs]
    assert not judge.judge(out, wrong, trajs, reqs, teach_w)["pass"]


def test_sieve_judge_fails_family_L():
    out = {"status": "COMPACT RULE", "rule": {"family": "L", "classes": [0], "rank": {0: 0}, "on_hit": {0: 0},
                                              "insert_class": 0, "recency": "oldest_first"}}
    assert not judge.judge(out, "SIEVE", [], [], [])["pass"]


def test_phase_b_c_on_oracle():
    ctrl = Oracle("LFU")
    trajs, _ = _blind_trajs(ctrl, [9301, 9302], 2500)
    out, abstraction = X.extract([dict(t) for t in trajs])
    alpha = X.Alpha(abstraction)
    req, _, segs = streams.make_stream(9401, 3000)
    cfg = dict(CONFIG)
    cfg["phaseB"] = dict(CONFIG["phaseB"], states_per_pair=40)
    summ, rec = causal.phase_b(ctrl, out["rule"], alpha, "LFU", req, 7, cfg=cfg)
    assert summ["pass"], summ
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "p.py")
        with open(path, "w") as f:
            f.write(X.plain_code(out["rule"], "TEST", out["description"]))
        plain = transplant.load_plain_code(path)
        summ_c, _ = transplant.phase_c(ctrl, plain, "LFU", req, segs, 9401)
    assert summ_c["pass"], summ_c
    assert summ_c["overall_agreement"] == 1.0


def test_phase_b_detects_broken_mechanism():
    """A controller whose score ignores its local state must fail B2 against LFU semantics."""
    class Blind(Oracle):
        def score(self, h, g, dt):
            return (-np.log1p(np.asarray(dt, np.float64)) / 8.0).astype(np.float32)
    ctrl = Blind("LFU")
    trajs, _ = _blind_trajs(ctrl, [9501], 2500)
    out, abstraction = X.extract([dict(t) for t in trajs])
    req, _, _ = streams.make_stream(9601, 3000)
    cfg = dict(CONFIG)
    cfg["phaseB"] = dict(CONFIG["phaseB"], states_per_pair=40)
    summ, _ = causal.phase_b(ctrl, out["rule"], X.Alpha(abstraction), "LFU", req, 3, cfg=cfg)
    assert not summ["B2_pass"]
