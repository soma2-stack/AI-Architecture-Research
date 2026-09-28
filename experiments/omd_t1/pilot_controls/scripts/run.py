"""OMD-PILOT-1 orchestration. Subcommands (run in order; each refuses to start unless the previous
gate passed):

  phaseA_train    train 12 controllers (4 controls x seeds 101-103), held-out imitation gate
  phaseA_blind    closed-loop rollouts on training streams -> blinded trajectory files + sealed key
  phaseA_extract  blinded extraction (never reads the key); hashes all outputs
  phaseA_judge    unblind and judge each extraction against the planted quotient semantics
  phaseB          causal intervention gate
  phaseC          plain-code transplant gate
  all             run the above in sequence as separate processes, stopping at the first failed gate
"""
import glob
import hashlib
import json
import os
import secrets
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

from omdp import ledger  # noqa: E402
from omdp.config import CONFIG, EVENT_EVICT  # noqa: E402

DEV = os.environ.get("OMD_DEV_RESULTS")  # dev dry run: scratch output, dev seeds, 2 passes, no gating
if DEV:
    CONFIG.update({"train_seeds": [9701, 9702, 9703], "heldout_seeds": [9801, 9802, 9803],
                   "train_len": 3000, "heldout_len": 5000})
    CONFIG["training"]["max_passes"] = 2
RES = DEV or os.path.join(HERE, "results")
PA = os.path.join(RES, "phaseA")
CTRL_DIR = os.path.join(PA, "controllers")
BLIND = os.path.join(PA, "blinded")
EXTR = os.path.join(PA, "extracted")
KEY = os.path.join(PA, "blinding_key.json")
PB = os.path.join(RES, "phaseB")
PC = os.path.join(RES, "phaseC")


def git_state():
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=HERE, text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--porcelain", "--", ".", ":(exclude)results"],
                                    cwd=HERE, text=True).strip()
    return {"commit": head, "code_dirty": bool(dirty), "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))


def load(path):
    with open(path) as f:
        return json.load(f)


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def require(path, what):
    if DEV and os.path.exists(path):
        return
    if not os.path.exists(path) or not load(path).get("pass"):
        sys.exit(f"STOP: {what} has not passed ({path}); refusing to continue")


def ctrl_name(control, seed):
    return f"{control}_s{seed}"


def M(stage, note):
    return ledger.Measured(("dev_" + stage) if DEV else stage, note)


def cpu_guard(meas):
    def g():
        ledger.check_cap(meas.elapsed_cpu(), margin_s=60.0)
    return g


# --------------------------------------------------------------------------------------------- A
def phaseA_train():
    from omdp import streams, teachers, train
    from omdp import instrument as ins
    with M("phaseA_train", "train 12 controllers + held-out imitation gate") as meas:
        start = git_state()
        dump(os.path.join(RES, "config.json"), CONFIG)
        import platform
        import jax
        import jaxlib
        import scipy
        dump(os.path.join(RES, "environment.json"), {"python": platform.python_version(), "platform": platform.platform(),
                                                     "jax": jax.__version__, "jaxlib": jaxlib.__version__,
                                                     "numpy": np.__version__, "scipy": scipy.__version__,
                                                     "devices": [str(d) for d in jax.devices()]})
        dump(os.path.join(RES, "seeds.json"), {"train": CONFIG["train_seeds"], "heldout": CONFIG["heldout_seeds"],
                                              "train_len": CONFIG["train_len"], "heldout_len": CONFIG["heldout_len"]})
        C = CONFIG["C"]
        ho = {s: streams.make_stream(s, CONFIG["heldout_len"]) for s in CONFIG["heldout_seeds"]}
        gate = {"git_at_start": start, "pairs": {}, "controllers": {}}
        for control in CONFIG["controls"]:
            for seed in CONFIG["train_seeds"]:
                req, _, segs = streams.make_stream(seed, CONFIG["train_len"])
                tr = teachers.simulate(control, req, C)
                name = ctrl_name(control, seed)
                t0 = time.time()
                params, info = train.train(tr, seed, cpu_guard=cpu_guard(meas))
                info["wall_s"] = round(time.time() - t0, 2)
                dump(os.path.join(CTRL_DIR, name + ".json"), {"control": control, "train_seed": seed,
                                                             "params": ins.params_to_lists(params), "train": info})
                np.savez_compressed(os.path.join(CTRL_DIR, name + "_train_teacher.npz"),
                                    etype=tr["etype"], slot=tr["slot"], req=req)
                gate["controllers"][name] = {"selected_pass": info["selected_pass"],
                                             "train_agreement_selected": info["history"][info["selected_pass"] - 1]["train_agreement"]
                                             if info["selected_pass"] else None, "n_params": info["n_params"]}
                for hs in CONFIG["heldout_seeds"]:
                    hreq = ho[hs][0]
                    ttr = teachers.simulate(control, hreq, C, record_local=False)
                    ev = train.evaluate_tf(params, ttr)
                    _, out = ins.tf_rollout(params, ins.init_carry(C), ttr["etype"].astype(np.int32),
                                            ttr["slot"].astype(np.int32), ttr["dt"], ttr["resident"])
                    np.savez_compressed(os.path.join(PA, "heldout_decisions", f"{name}_h{hs}.npz"),
                                        teacher_etype=ttr["etype"], teacher_slot=ttr["slot"],
                                        neural_victim_teacher_forced=np.asarray(out["victim"]).astype(np.int16))
                    ok = ev["agreement"] >= CONFIG["gates"]["phaseA_imitation_min"]
                    gate["pairs"][f"{name}_h{hs}"] = {"agreement": ev["agreement"], "n_evict": ev["n_evict"],
                                                      "ce": ev["ce"], "pass": bool(ok),
                                                      "scoring_evaluations_O_C": ev["n_evict"] * C}
                    print(f"{name} h{hs}: agreement {ev['agreement']:.5f} ({'PASS' if ok else 'FAIL'})", flush=True)
        gate["pass"] = all(p["pass"] for p in gate["pairs"].values())
        gate["failed_pairs"] = [k for k, p in gate["pairs"].items() if not p["pass"]]
        gate["failed_controls"] = sorted({k.split("_s")[0] for k in gate["failed_pairs"]})
        gate["cpu_seconds_this_step"] = round(meas.elapsed_cpu(), 2)
        dump(os.path.join(PA, "imitation_gate.json"), gate)
        print("PHASE A IMITATION GATE:", "PASS" if gate["pass"] else "FAIL " + str(gate["failed_controls"]))


def _load_params(name):
    from omdp import instrument as ins
    d = load(os.path.join(CTRL_DIR, name + ".json"))
    return ins.params_from_lists(d["params"]), d


def phaseA_blind():
    require(os.path.join(PA, "imitation_gate.json"), "Phase A imitation gate")
    from omdp import streams
    from omdp.controller import NeuralController
    with M("phaseA_blind", "closed-loop rollouts on training streams for blinded extraction"):
        start = git_state()
        key = {"git_at_start": start, "map": {}}
        reqs = {s: streams.make_stream(s, CONFIG["train_len"])[0] for s in CONFIG["train_seeds"]}
        os.makedirs(BLIND, exist_ok=True)
        for control in CONFIG["controls"]:
            for seed in CONFIG["train_seeds"]:
                name = ctrl_name(control, seed)
                p, _ = _load_params(name)
                ctrl = NeuralController(p)
                arrays = {}
                for k, s in enumerate(CONFIG["train_seeds"]):
                    o = ctrl.cl(reqs[s])
                    ev = o["etype"] == EVENT_EVICT
                    arrays.update({f"etype_{k}": o["etype"], f"slot_{k}": o["slot"], f"hs_post_{k}": o["hs_post"],
                                   f"g_pre_{k}": o["g_pre"], f"g_post_{k}": o["g_post"], f"S_ev_{k}": o["S"][ev]})
                code = secrets.token_hex(3).upper()
                while code in key["map"]:
                    code = secrets.token_hex(3).upper()
                path = os.path.join(BLIND, f"{code}.npz")
                np.savez_compressed(path, n_streams=np.int64(len(CONFIG["train_seeds"])), **arrays)
                key["map"][code] = {"controller": name, "sha256": sha(path)}
        dump(KEY, key)
        print("blinded", len(key["map"]), "trajectory files")


def phaseA_extract():
    """Blinded: reads only results/phaseA/blinded/*.npz. Never opens the key file."""
    require(os.path.join(PA, "imitation_gate.json"), "Phase A imitation gate")
    from omdp import extract as X
    with M("phaseA_extract", "blinded quotient extraction of 12 controllers"):
        start = git_state()
        os.makedirs(EXTR, exist_ok=True)
        hashes = {"git_at_start": start, "files": {}}
        for path in sorted(glob.glob(os.path.join(BLIND, "*.npz"))):
            code = os.path.basename(path)[:-4]
            z = np.load(path)
            trajs = [{"etype": z[f"etype_{k}"], "slot": z[f"slot_{k}"], "hs_post": z[f"hs_post_{k}"],
                      "g_pre": z[f"g_pre_{k}"], "g_post": z[f"g_post_{k}"], "S_ev": z[f"S_ev_{k}"]}
                     for k in range(int(z["n_streams"]))]
            out, abstraction = X.extract(trajs)
            out["codename"] = code
            jp = os.path.join(EXTR, f"{code}.json")
            dump(jp, out)
            files = {"json": jp}
            if abstraction is not None:
                ap = os.path.join(EXTR, f"{code}_abstraction.npz")
                np.savez_compressed(ap, scale=np.asarray(abstraction["scale"]), points=abstraction["points"],
                                    point_class=abstraction["point_class"])
                files["abstraction"] = ap
            if out["status"] == "COMPACT RULE":
                cp = os.path.join(EXTR, f"{code}_policy.py")
                with open(cp, "w") as f:
                    f.write(X.plain_code(out["rule"], code, out["description"]))
                files["plain_code"] = cp
            hashes["files"][code] = {k: {"path": os.path.relpath(v, HERE), "sha256": sha(v)} for k, v in files.items()}
            print(code, out["status"], "|", out["description"], flush=True)
        dump(os.path.join(EXTR, "extraction_hashes.json"), hashes)


def phaseA_judge():
    require(os.path.join(PA, "imitation_gate.json"), "Phase A imitation gate")
    from omdp import judge, streams, teachers
    with M("phaseA_judge", "unblind and judge extractions"):
        start = git_state()
        key = load(KEY)
        hashes = load(os.path.join(EXTR, "extraction_hashes.json"))
        C = CONFIG["C"]
        reqs = [streams.make_stream(s, CONFIG["train_len"])[0] for s in CONFIG["train_seeds"]]
        out = {"git_at_start": start, "controllers": {}}
        for code, meta in sorted(key["map"].items()):
            for kind, f in hashes["files"][code].items():
                assert sha(os.path.join(HERE, f["path"])) == f["sha256"], f"hash mismatch {code} {kind}"
            name = meta["controller"]
            control = name.split("_s")[0]
            z = np.load(os.path.join(BLIND, f"{code}.npz"))
            ext_trajs = [{"etype": z[f"etype_{k}"], "slot": z[f"slot_{k}"]} for k in range(int(z["n_streams"]))]
            teach = [teachers.simulate(control, r, C, record_local=False) for r in reqs]
            ex = load(os.path.join(EXTR, f"{code}.json"))
            j = judge.judge(ex, control, ext_trajs, reqs, teach)
            j.update({"codename": code, "extraction_status": ex["status"], "description": ex["description"],
                      "validation_agreement_pooled": ex["stats"].get("validation_agreement_pooled")})
            out["controllers"][name] = j
            print(name, code, "PASS" if j["pass"] else "FAIL", j.get("reason", ""), flush=True)
        out["pass"] = all(v["pass"] for v in out["controllers"].values())
        out["failed_controls"] = sorted({k.split("_s")[0] for k, v in out["controllers"].items() if not v["pass"]})
        dump(os.path.join(PA, "extraction_gate.json"), out)
        print("PHASE A EXTRACTION GATE:", "PASS" if out["pass"] else "FAIL " + str(out["failed_controls"]))


def _extraction_for(name):
    from omdp import extract as X
    key = load(KEY)
    code = [c for c, m in key["map"].items() if m["controller"] == name][0]
    ex = load(os.path.join(EXTR, f"{code}.json"))
    z = np.load(os.path.join(EXTR, f"{code}_abstraction.npz"))
    alpha = X.Alpha({"scale": z["scale"], "points": z["points"], "point_class": z["point_class"]})
    return code, ex, alpha


# --------------------------------------------------------------------------------------------- B, C
def phaseB():
    require(os.path.join(PA, "extraction_gate.json"), "Phase A extraction gate")
    from omdp import causal, streams
    from omdp.controller import NeuralController
    with M("phaseB", "causal intervention gate") as meas:
        out = {"git_at_start": git_state(), "pairs": {}}
        for control in CONFIG["controls"]:
            for seed in CONFIG["train_seeds"]:
                name = ctrl_name(control, seed)
                p, _ = _load_params(name)
                code, ex, alpha = _extraction_for(name)
                for hs in CONFIG["heldout_seeds"]:
                    req = streams.make_stream(hs, CONFIG["heldout_len"])[0]
                    summ, rec = causal.phase_b(NeuralController(p), ex["rule"], alpha, control, req, seed * 1000 + hs)
                    dump(os.path.join(PB, "records", f"{name}_h{hs}.json"), rec)
                    out["pairs"][f"{name}_h{hs}"] = summ
                    print(name, hs, "PASS" if summ["pass"] else "FAIL", flush=True)
                    ledger.check_cap(meas.elapsed_cpu(), margin_s=60.0)
        out["pass"] = all(v["pass"] for v in out["pairs"].values())
        out["failed_pairs"] = [k for k, v in out["pairs"].items() if not v["pass"]]
        dump(os.path.join(PB, "phaseB_gate.json"), out)
        print("PHASE B GATE:", "PASS" if out["pass"] else "FAIL " + str(out["failed_pairs"]))


def phaseC():
    require(os.path.join(PB, "phaseB_gate.json"), "Phase B gate")
    from omdp import streams, transplant
    from omdp.controller import NeuralController
    with M("phaseC", "plain-code transplant gate") as meas:
        out = {"git_at_start": git_state(), "pairs": {}}
        for control in CONFIG["controls"]:
            for seed in CONFIG["train_seeds"]:
                name = ctrl_name(control, seed)
                p, _ = _load_params(name)
                code, ex, _ = _extraction_for(name)
                plain = transplant.load_plain_code(os.path.join(EXTR, f"{code}_policy.py"))
                for hs in CONFIG["heldout_seeds"]:
                    req, _, segs = streams.make_stream(hs, CONFIG["heldout_len"])
                    summ, dec = transplant.phase_c(NeuralController(p), plain, control, req, segs, hs)
                    np.savez_compressed(os.path.join(PC, "decisions", f"{name}_h{hs}.npz"), **dec)
                    out["pairs"][f"{name}_h{hs}"] = summ
                    print(name, hs, "PASS" if summ["pass"] else "FAIL", flush=True)
                    ledger.check_cap(meas.elapsed_cpu(), margin_s=60.0)
        out["pass"] = all(v["pass"] for v in out["pairs"].values())
        out["failed_pairs"] = [k for k, v in out["pairs"].items() if not v["pass"]]
        dump(os.path.join(PC, "phaseC_gate.json"), out)
        print("PHASE C GATE:", "PASS" if out["pass"] else "FAIL " + str(out["failed_pairs"]))


def run_all():
    steps = [("phaseA_train", os.path.join(PA, "imitation_gate.json")),
             ("phaseA_blind", None), ("phaseA_extract", None),
             ("phaseA_judge", os.path.join(PA, "extraction_gate.json")),
             ("phaseB", os.path.join(PB, "phaseB_gate.json")),
             ("phaseC", os.path.join(PC, "phaseC_gate.json"))]
    for step, gate in steps:
        rc = subprocess.call([sys.executable, os.path.abspath(__file__), step])
        if rc != 0:
            sys.exit(f"STOP: {step} exited with {rc}")
        if gate is not None and not load(gate).get("pass") and not DEV:
            print(f"STOP after {step}: gate failed")
            return
    print("OMD-PILOT-1: all gates passed. Not continuing to OMD-1 (not authorized).")


if __name__ == "__main__":
    os.makedirs(os.path.join(PA, "heldout_decisions"), exist_ok=True)
    os.makedirs(os.path.join(PC, "decisions"), exist_ok=True)
    cmd = sys.argv[1]
    {"phaseA_train": phaseA_train, "phaseA_blind": phaseA_blind, "phaseA_extract": phaseA_extract,
     "phaseA_judge": phaseA_judge, "phaseB": phaseB, "phaseC": phaseC, "all": run_all}[cmd]()
