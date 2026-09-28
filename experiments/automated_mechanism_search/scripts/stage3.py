"""Official Stage 3 (frozen D-S3 / D-S3-v4): matched validation of the Stage-2 promotions.

Usage: python3 scripts/stage3.py <stage2_run> <stage3_run>      e.g. stage2_v7 stage3_v7;
       prereg v8: stage2_v8_confirm stage3_v8 (locked seeds 30000-30009, C* AULC, Gate 4 on KF(P))
Reads runs/<stage2_run>/promotions.json; writes runs/<stage3_run>/{results.json, jobs.jsonl.gz,
manifest.json}.  Fresh seeds 10000-10009; CPU only; the shared 30 CPU-h cap is checked before
every batch of jobs.  Labels never exceed POSSIBLE ARCHITECTURE CANDIDATE — CROSS-LANE AUDIT REQUIRED."""
import gzip
import json
import math
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np  # noqa: E402

from ams import accounting, manifest  # noqa: E402
from ams import stage3 as S3  # noqa: E402
from ams.controls import GENERIC, init_worker, make  # noqa: E402
from ams.families import FamilyLibrary  # noqa: E402
from ams.grammar import program_from_dict, program_to_dict  # noqa: E402
from ams.substrate import ProgramLearner  # noqa: E402

STAGE2 = sys.argv[1] if len(sys.argv) > 1 else "stage2_v7"
RUN_NAME = sys.argv[2] if len(sys.argv) > 2 else "stage3_v7"
OUT = os.path.join(HERE, "runs", RUN_NAME)
assert not os.path.exists(os.path.join(OUT, "manifest.json")), f"{OUT} already holds a run; refusing to overwrite"
V8 = RUN_NAME.startswith("stage3_v8")          # prereg v8: locked seeds 30000-30009, C* AULC, Gate 4 on KF(P)
S3.configure("v8" if V8 else "v7")
if V8:
    os.environ["AMS_STAGE3_UNLOCK"] = "1"       # the official v8 Stage 3 is the only permitted user of 30000-30009


def _json(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and math.isinf(o):
        return "inf" if o > 0 else "-inf"
    if hasattr(o, "tolist"):
        return o.tolist()
    return str(o)


def prog_spec(p, name):
    return {"kind": "program", "program": program_to_dict(p), "name": name}


def main():
    promos = json.load(open(os.path.join(HERE, "runs", STAGE2, "promotions.json")))
    os.makedirs(OUT, exist_ok=True)
    git_at_start = {"commit": manifest._git("rev-parse", "HEAD"),
                    "dirty_excluding_runs": bool(manifest._git("status", "--porcelain", "--", ".", ":!runs"))}
    if not promos:
        res = {"stage2_run": STAGE2, "promoted": 0, "note": "no promotions; Stage 3 not applicable"}
        json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1)
        print(res)
        return 0
    manifest.write_or_verify_config()
    accounting.check_cap()
    assert set(S3.STAGE3_SEEDS).isdisjoint({500, 1000, 1001, 1002, *range(5000, 5003), *range(6000, 6008),
                                            *range(20000, 20010)})
    if V8:
        assert S3.STAGE3_SEEDS == list(range(30000, 30010)) and S3.CM == "aulc" and S3.GATE4_REF == "KF"
    lib = FamilyLibrary()
    parent0 = accounting.self_cpu_seconds()
    state = {"workers": 0.0}
    joblog = gzip.open(os.path.join(OUT, "jobs.jsonl.gz"), "wt", 9)
    workers = max(1, min(3, (os.cpu_count() or 2) - 1))

    cands = []
    for pr in promos:
        P = program_from_dict(pr["canonical"])
        task = pr["best_task"]
        K, kinfo = lib.decompose(P)
        has_persistent = any(r.lifetime != "EXAMPLE" for r in P.regs)
        conds = {"P": prog_spec(P, "P"), "K": prog_spec(K, "K"), "A1": prog_spec(S3.coupling_cut(P), "A1"),
                 "A4": prog_spec(S3.flip_timing(P), "A4"),
                 "A5a": {"kind": "opt_swap", "program": program_to_dict(P), "mode": "SGDM"},
                 "A5b": {"kind": "opt_swap", "program": program_to_dict(P), "mode": "AdamW"}}
        hooks = {}
        if has_persistent:
            conds["A2"], hooks["A2"] = prog_spec(P, "A2"), "zero"
            conds["A3"], hooks["A3"] = prog_spec(P, "A3"), "noise"
        kf_name = None
        if V8:                                  # KF(P): exact nearest known-family reference (v8 Gate 4)
            kf_name = pr["family_nearest"]["family"]
            assert lib.nearest(P)["family"] == kf_name, "nearest family differs from the Stage-2 record"
            conds["KF"] = prog_spec(S3.nearest_family_program(kf_name), "KF")
        rob = S3.robustness_variants(P)
        for name, q in rob:
            conds["rob:" + name] = prog_spec(q, "rob")
        fl = {"flops_P": S3.flops(task, ProgramLearner(P)), "flops_SGD": S3.flops(task, make("SGD")())}
        cands.append({"pid": pr["pid"], "task": task, "P": P, "K": K, "K_info": kinfo, "conds": conds, "KF": kf_name,
                      "hooks": hooks, "has_persistent": has_persistent, "flops": fl,
                      "flops_ratio": fl["flops_P"] / fl["flops_SGD"]})

    def run(jobs, note):
        est = 60.0 * len(jobs)
        accounting.check_cap(accounting.self_cpu_seconds() - parent0 + state["workers"] + est)
        with mp.get_context("fork").Pool(workers, initializer=init_worker) as pool:
            res = pool.map(S3.run_s3_job, jobs, chunksize=1)
        for j, r in zip(jobs, res):
            state["workers"] += r.get("cpu_s", 0.0)
            joblog.write(json.dumps({"job": {k: v for k, v in j.items() if k != "spec"}, "spec": j["spec"],
                                     "result": r}, default=_json) + "\n")
        print(f"{time.strftime('%H:%M:%S')} {note}: {len(jobs)} jobs", flush=True)
        return res

    # phase 1: candidate-specific conditions + per-task generics and known controls
    shared = {}
    for t in sorted({c["task"] for c in cands}):
        for g in GENERIC + S3.KNOWN_CONTROLS[t]:
            shared[(t, g)] = {"cid": f"shared:{t}", "cond": g, "task": t,
                              "spec": {"kind": "named", "name": g}, "seeds": S3.STAGE3_SEEDS}
    jobs = list(shared.values())
    for c in cands:
        for k, spec in c["conds"].items():
            jobs.append({"cid": c["pid"], "cond": k, "task": c["task"], "spec": spec, "seeds": S3.STAGE3_SEEDS,
                         "hook": c["hooks"].get(k)})
    res1 = run(jobs, "phase 1")
    shared_S = {}
    for j, r in zip(jobs, res1):
        if j["cid"].startswith("shared:"):
            shared_S[(j["task"], j["cond"])] = S3.summary(j["task"], r)
        else:
            c = next(x for x in cands if x["pid"] == j["cid"])
            c.setdefault("S", {})[j["cond"]] = S3.summary(j["task"], r)
    # phase 2: resource-matched best generic (A6 compute, A7 capacity)
    jobs2 = []
    for c in cands:
        t = c["task"]
        for g in GENERIC:
            c["S"][g] = shared_S[(t, g)]
        for g in S3.KNOWN_CONTROLS[t]:
            c["S"][g] = shared_S[(t, g)]
        stable = {g: c["S"][g] for g in GENERIC if c["S"][g].get("stable")}
        G = min(stable, key=lambda g: stable[g]["metric"]) if stable else "SGD"
        k = S3.compute_matched_k(t, c["P"], G)
        h, target, params = S3.capacity_matched_hidden(t, c["P"])
        c["matching"] = {"G": G, "A6_k": k, "A7_hidden": h, "A7_param_target": target, "A7_params": params}
        jobs2.append({"cid": c["pid"], "cond": "A6", "task": t, "spec": {"kind": "named", "name": G},
                      "seeds": S3.STAGE3_SEEDS, "inner": k})
        jobs2.append({"cid": c["pid"], "cond": "A7", "task": t, "spec": {"kind": "named", "name": G},
                      "seeds": S3.STAGE3_SEEDS, "hidden": h})
    res2 = run(jobs2, "phase 2")
    for j, r in zip(jobs2, res2):
        c = next(x for x in cands if x["pid"] == j["cid"])
        c["S"][j["cond"]] = S3.summary(j["task"], r)
    joblog.close()

    decisions = {c["pid"]: S3.pre_decide(c["task"], c["S"], c["has_persistent"], c["flops_ratio"]) for c in cands}
    pv = {pid: d["wilcoxon_p"] for pid, d in decisions.items() if "wilcoxon_p" in d}
    hol = S3.holm(pv)
    out = {"stage2_run": STAGE2, "seeds": S3.STAGE3_SEEDS, "git_at_start": git_at_start, "candidates": [],
           "profile": {"version": "v8" if V8 else "v7", "cstar_metric": S3.CM, "gate4_reference": S3.GATE4_REF}}
    for c in cands:
        d = decisions[c["pid"]]
        d["holm_significant"] = hol.get(c["pid"], False)
        lab = S3.label(d, d["holm_significant"])
        out["candidates"].append({
            "pid": c["pid"], "task": c["task"], "label": lab, "decision": d, "matching": c.get("matching"),
            "flops": c["flops"], "K_info": c["K_info"], "KF_family": c["KF"], "program": program_to_dict(c["P"]),
            "K": program_to_dict(c["K"]), "has_persistent": c["has_persistent"],
            "summaries": {k: {kk: vv for kk, vv in v.items() if kk in ("stable", "lr", "metric", "seed_metric",
                                                                        "return_ok_count", "R0_pre_shift",
                                                                        "retention", "T2_final_mse", "train_acc",
                                                                        "sgg", "error", "hl_censored_seeds",
                                                                        "aulc_seeds")}
                          for k, v in c["S"].items()},
        })
    cpu = accounting.self_cpu_seconds() - parent0 + state["workers"]
    accounting.record(RUN_NAME, cpu, 0.0, f"Stage 3 on {STAGE2} promotions ({len(cands)} candidates), parent self + workers")
    out["cpu_seconds"] = cpu
    out["cumulative_cpu_hours"] = accounting.load_ledger()["total_cpu_hours"]
    out["labels"] = {c["pid"]: c["label"] for c in out["candidates"]}
    out["tier3_required"] = [pid for pid, l in out["labels"].items() if l.startswith("POSSIBLE ARCHITECTURE")]
    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump(out, f, indent=1, default=_json)
    man = manifest.build_manifest(RUN_NAME, {"git_at_start": git_at_start, "stage2_run": STAGE2,
                                             "seeds": S3.STAGE3_SEEDS, "labels": out["labels"], "cpu_seconds": cpu})
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(man, f, indent=1, default=_json)
    print(json.dumps({"labels": out["labels"], "cpu_seconds": cpu,
                      "cumulative_cpu_hours": out["cumulative_cpu_hours"]}, indent=1, default=_json))
    return 0


if __name__ == "__main__":
    sys.exit(main())
