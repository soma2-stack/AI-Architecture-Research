"""Stage-3 machinery (ams/stage3.py): condition programs, learners, hooks, statistics, labels."""
import numpy as np
import pytest

from ams import stage3 as S3
from ams.canon import canon
from ams.controls import make
from ams.families import REFERENCES
from ams.fingerprint import fingerprint
from ams.grammar import make_program
from ams.substrate import Net, ProgramLearner, Trainer

C3P = make_program("(neg (outer d_bp a))", "(neg d_bp)", regs=[("r1", "O", "RUN", "0", 0.9, "(nrm dphi)")],
                   struct=("reinit", "(tanh r1)", 0.1))
C1P = make_program("(neg (outer d_bp a))", "(neg d_bp)", regs=[("r1", "M", "RUN", "0", 0.9, "(outer z a)")],
                   w_eff="(mul (tanh r1) 0.1)")
C2P = make_program("(add (neg (outer d_bp a)) (mul (rowscale (neg (outer d_bp a)) (topk h 4)) 0.1))",
                   "(add (neg d_bp) (mul (mul (neg d_bp) (topk h 4)) 0.1))")


@pytest.mark.parametrize("p", [C1P, C2P, C3P])
def test_coupling_cut_removes_every_coupling_and_keeps_signal(p):
    c = canon(p)
    assert fingerprint(c)["couplings"]
    a1 = S3.coupling_cut(c)
    fp = fingerprint(a1)
    assert fp["couplings"] == [] and fp["learning_signal"]


def test_c2_cut_is_sgd_plus_ten_percent_ungated():
    a1 = S3.coupling_cut(canon(C2P))
    net = Net(1, 1, [0])
    assert "topk" not in str(a1.dW) and a1.struct is None and a1.w_eff is None


def test_robustness_neighbours():
    names = [n for n, _ in S3.robustness_variants(canon(C3P))]
    assert sorted(names) == sorted(["decay[r1]=0.5", "decay[r1]=0.99", "theta=0.0", "theta=0.5"])
    v = dict(S3.robustness_variants(canon(C2P)))
    assert any("topk=1" in n for n in v) and any("topk=8" in n for n in v)


def test_flip_timing():
    assert S3.flip_timing(C3P).update_every == 8 and S3.flip_timing(S3.flip_timing(C3P)).update_every == 1


@pytest.mark.parametrize("mode", ["SGDM", "AdamW"])
def test_program_through_optimizer_equals_generic_for_sgd_program(mode):
    """R1_SGD fed through SGDM / AdamW moments reproduces the generic SGDM / AdamW trajectory."""
    rng = np.random.default_rng(0)
    X = rng.normal(size=(40, 3, 16, 4)).astype(np.float32)
    Y = rng.normal(size=(40, 3, 16, 2)).astype(np.float32)
    ws = []
    for L in (make(mode)(), S3.ProgramThroughOptimizer(canon(REFERENCES["R1_SGD"]), mode)):
        net = Net(4, 2, [1, 2, 3])
        tr = Trainer(net, L, [0.01, 0.01, 0.01])
        for t in range(40):
            tr.step(X[t], Y[t])
        ws.append([w.copy() for w in net.W])
    for a, b in zip(*ws):
        assert np.allclose(a, b, rtol=1e-3, atol=1e-5)


def test_register_hook_zero_and_noise_at_events():
    from ams.tasks import TaskB
    for mode in ("zero", "noise"):
        L = ProgramLearner(canon(C3P))
        net = Net(TaskB.d_in, TaskB.d_out, [10000, 10001])
        tr = Trainer(net, L, [0.1, 0.1])
        for l in range(net.nl):
            L.regs[l]["r1"][:] = 3.0 + np.arange(L.regs[l]["r1"].shape[-1])
        h = S3.RegisterHook(mode, "B")
        h(tr, 5, "B")
        assert h.n_events == 0
        h(tr, TaskB.n1, "B")
        assert h.n_events == 1
        r = L.regs[0]["r1"]
        if mode == "zero":
            assert not r.any()
        else:
            assert r.std() > 0 and abs(r.mean()) < 3.0


def test_event_steps():
    assert S3.event_steps("B") == {500}
    assert S3.event_steps("Cstar") == {256, 320, 384}
    assert S3.event_steps("F") == {100, 200, 300, 400}


def test_resource_matching():
    P = canon(C3P)
    assert S3.compute_matched_k("Cstar", P, "SGD") == 2          # FLOPs_P slightly above SGD -> ceil = 2
    h, target, params = S3.capacity_matched_hidden("Cstar", P)
    assert params >= target and h >= 32
    assert Net(1, 1, [0], hidden=h - 1).n_params() < target


def test_statistics():
    assert S3.wilcoxon_greater([0.0] * 10) == 1.0
    assert S3.wilcoxon_greater([1.0] * 10) < 0.01
    lo, hi = S3.bootstrap_ci([1.0, 2.0, 3.0, 1.5, 2.5, 2.0, 1.0, 3.0, 2.0, 2.0])
    assert 0 < lo < hi
    assert S3.holm({"a": 0.001, "b": 0.04, "c": 0.02}) == {"a": True, "c": True, "b": True}
    assert S3.holm({"a": 0.001, "b": 0.03, "c": 0.04}) == {"a": True, "b": False, "c": False}


def _decision(**kw):
    d = {"gate1_stable": True, "gate2_learns": True, "threshold_ok": True, "bootstrap_excludes_0": True,
         "gate4a_K_drops_half": True, "gate4b_P_beats_K_by_half_tau": True, "gate4c_A1_drops_half": True,
         "cursor_A1_ok": True, "gate5_A5b_keeps_half": True, "gate6_beats_A6_A7": True, "gate6_flops_ok": True,
         "cursor_A7_ok": True, "known_control": {"ok": True}, "robustness_ok": True, "A2_A3_drop_half": True}
    d.update(kw)
    return d


def test_labels():
    top = "POSSIBLE ARCHITECTURE CANDIDATE — CROSS-LANE AUDIT REQUIRED"
    mid = "INTERESTING EMPIRICAL MECHANISM — NOVELTY AUDIT REQUIRED"
    assert S3.label(_decision(), True) == top
    assert S3.label(_decision(), False) == "NEGATIVE"
    assert S3.label(_decision(gate2_learns=False), True) == "NEGATIVE"
    assert S3.label(_decision(gate4a_K_drops_half=False), True) == "REDISCOVERY"
    assert S3.label(_decision(gate6_beats_A6_A7=False), True) == mid
    assert S3.label(_decision(known_control={"ok": False}), True) == mid
    assert S3.label(_decision(A2_A3_drop_half=False), True) == mid
    assert S3.label(_decision(A2_A3_drop_half=None), True) == top


def test_stage3_plumbing_smoke_on_non_official_seeds(monkeypatch):
    """End-to-end plumbing on C* with seeds 900-901 (never used by any official stage)."""
    from ams.grammar import program_to_dict
    monkeypatch.setattr(S3, "STAGE3_SEEDS", [900, 901])
    P = canon(C3P)
    spec = {"kind": "program", "program": program_to_dict(P)}
    jobs = {"P": {"spec": spec}, "A2": {"spec": spec, "hook": "zero"}, "A3": {"spec": spec, "hook": "noise"},
            "A5b": {"spec": {"kind": "opt_swap", "program": program_to_dict(P), "mode": "AdamW"}},
            "SGD": {"spec": {"kind": "named", "name": "SGD"}}, "SGDM": {"spec": {"kind": "named", "name": "SGDM"}},
            "AdamW": {"spec": {"kind": "named", "name": "AdamW"}},
            "A6": {"spec": {"kind": "named", "name": "SGD"}, "inner": 2},
            "A7": {"spec": {"kind": "named", "name": "SGD"}, "hidden": 33}}
    S = {}
    for k, j in jobs.items():
        r = S3.run_s3_job({"cid": "x", "cond": k, "task": "Cstar", "seeds": [900, 901], **j})
        assert "error" not in r, r.get("error")
        if k in ("A2", "A3"):
            assert r["hook_events"] == 3
        S[k] = S3.summary("Cstar", r)
    S["K"] = S["A1"] = S["SGD"]
    d = S3.pre_decide("Cstar", S, True, 1.03)
    assert d["best_generic"] in ("SGD", "SGDM", "AdamW") and "gate4a_K_drops_half" in d
    assert S3.label(d, False) in ("NEGATIVE", "REDISCOVERY")
