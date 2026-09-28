"""Official Stage 1 (prereg v3 sec. 17): calibration of established mechanisms and ordinary
baselines, with the frozen gates M2-M7, V1-B, V2-C*, V3-F, V-D (IMPLEMENTATION_DECISIONS
D-CAL, D-S1).  Writes runs/stage1/*.json and appends to the CPU ledger.  Exit code 0 iff all
mandatory gates pass."""
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
from ams.controls import GENERIC, init_worker, run_job  # noqa: E402
from ams.runners import LR_GRID, run_D, select_lr, summarize  # noqa: E402
from ams.tasks import TaskD, TaskF, discrete_synthesis, synthesis_predict  # noqa: E402

OUT = os.path.join(HERE, "runs", "stage1")
SEEDS = [100, 101, 102, 103, 104]
DIAG = ("SGD_noclip", "SGDM_noclip", "AdamW_noclip")
JOBS = (
    [("B", m) for m in GENERIC + ("GPM", "R17_EWC_SI", "R18_kWTA_sparse_update", "R13_fast_slow") + DIAG]
    + [("Cstar", m) for m in GENERIC + ("R12_fast_weights", "R13_fast_slow", "R15_three_factor") + DIAG]
    + [("F", m) for m in GENERIC + DIAG]
)
METRIC = {"B": "forgetting", "Cstar": "hl_censored_mean", "F": None}


def f_metric(task, s):
    if task == "F":
        return 1.0 - s["ood_acc"]
    return s[METRIC[task]]


def best_generic(summ, task):
    best, bv = None, math.inf
    for m in GENERIC:
        s = summ[task].get(m)
        if s is None or not s["stable"]:
            continue
        v = f_metric(task, s)
        if v < bv:
            best, bv = m, v
    return best


def d_select(runs, seeds):
    """D-S1-9: lr minimizing seed-mean final loss among lrs with no diverged seed."""
    best, key = None, None
    for lr in LR_GRID:
        rs = [r for r in runs if r["lr"] == lr]
        if any(r["diverged"] for r in rs):
            continue
        k = float(np.mean([r["final_loss"] for r in rs]))
        if key is None or k < key:
            best, key = lr, k
    if best is None:
        return {"lr": None, "S_tau": math.inf}
    rs = [r for r in runs if r["lr"] == best]
    st = [r["S_tau"] for r in rs]
    return {"lr": best, "S_tau": (math.inf if any(math.isinf(x) for x in st) else float(np.mean(st))),
            "final_loss": key}


def main():
    os.makedirs(OUT, exist_ok=True)
    stage0 = json.load(open(os.path.join(HERE, "runs", "stage0_v3", "stage0_result.json")))
    if not stage0["pass"]:
        print("Stage 0 (v3) did not pass; Stage 1 not allowed.")
        return 3
    manifest.write_or_verify_config()
    accounting.check_cap()
    git_at_start = {"commit": manifest._git("rev-parse", "HEAD"),
                    "dirty_excluding_runs": bool(manifest._git("status", "--porcelain", "--", ".", ":!runs"))}
    cpu0, wall0 = accounting.process_cpu_seconds(), time.time()

    jobs = [{"task": t, "learner": m, "seeds": SEEDS} for t, m in JOBS]
    workers = max(1, min(3, (os.cpu_count() or 2) - 1))
    with mp.get_context("fork").Pool(workers, initializer=init_worker) as pool:
        results = pool.map(run_job, jobs, chunksize=1)
    worker_cpu = sum(r["cpu_s"] for r in results)

    raw, summ, sels = {}, {"B": {}, "Cstar": {}, "F": {}}, {}
    for (t, m), r in zip(JOBS, results):
        sel = select_lr(r, SEEDS)
        s = summarize(t, sel)
        summ[t][m] = s
        sels[f"{t}:{m}"] = {"lr": sel.get("lr"), "table": sel.get("table"), "all_unstable": sel["all_unstable"]}
        raw[f"{t}:{m}"] = r
    with open(os.path.join(OUT, "raw_runs.json"), "w") as f:
        json.dump(raw, f, default=float)

    # Task D (baseline-only)
    D = {}
    for kappa in TaskD.kappas:
        for meth in ("SGD", "SGDM", "AdamW", "natgrad"):
            res = run_D(meth, SEEDS, kappa)
            D[f"{meth}@{kappa:g}"] = {"select": d_select(res["runs"], SEEDS), "runs": res["runs"]}

    # discrete synthesis on F
    synth = []
    for s in SEEDS:
        t = TaskF(s)
        idx, neg = discrete_synthesis(t.Xtr, t.ytr)
        acc = float(np.mean(synthesis_predict(t.Xood, idx, neg) == t.yood)) if idx is not None else 0.0
        synth.append({"seed": s, "hypothesis": idx, "negated": neg, "ood_acc": acc})

    # ------------------------------------------------------------------ gates
    G = {}
    stable_all = {t: {m: summ[t][m]["stable"] for m in GENERIC} for t in summ}
    G["M6_controls_run"] = {"pass": all(all(v.values()) for v in stable_all.values()), "stable": stable_all}
    if G["M6_controls_run"]["pass"]:
        G["M2_B_fit"] = {"pass": all(summ["B"][m]["L1_pre"] < 1e-3 for m in GENERIC),
                         "L1_pre": {m: summ["B"][m]["L1_pre"] for m in GENERIC}, "threshold": 1e-3}
        G["M3_B_interference"] = {
            "pass": all(summ["B"][m]["forgetting"] >= 10.0 and summ["B"][m]["L1_post_gt_pre_all"] for m in GENERIC),
            "forgetting": {m: summ["B"][m]["forgetting"] for m in GENERIC},
            "L1_post_gt_pre_every_seed": {m: summ["B"][m]["L1_post_gt_pre_all"] for m in GENERIC}}
        G["M4_F_failure"] = {
            "pass": all(summ["F"][m]["train_acc"] >= 0.98 and summ["F"][m]["ood_acc"] <= 0.25 and summ["F"][m]["sgg"] >= 75.0
                        for m in GENERIC),
            "train_acc": {m: summ["F"][m]["train_acc"] for m in GENERIC},
            "ood_acc": {m: summ["F"][m]["ood_acc"] for m in GENERIC},
            "sgg": {m: summ["F"][m]["sgg"] for m in GENERIC}}
        bc = best_generic(summ, "Cstar")
        sc = summ["Cstar"][bc]
        e1 = float(np.mean([x[0] for x in sc["R1_entry_mse"]]))
        e2 = float(np.mean([x[1] for x in sc["R1_entry_mse"]]))
        G["M7_Cstar_sanity"] = {"pass": sc["R0_pre_shift"] < 0.25 and e1 > 0.05 and e2 > 0.05,
                                "best_generic": bc, "R0_pre_shift": sc["R0_pre_shift"],
                                "R1_entry_mse_seed_mean": [e1, e2]}
    G["M5_detector"] = {"pass": bool(stage0["checks"]["test_suite"]["pass"] and stage0["checks"]["detector_recall"]["pass"]),
                        "source": "runs/stage0_v3/stage0_result.json"}
    sgdB = summ["B"]["SGD"]
    v1 = {}
    for c in ("GPM", "R17_EWC_SI", "R18_kWTA_sparse_update", "R13_fast_slow"):
        s = summ["B"][c]
        v1[c] = None if not s["stable"] else {
            "forgetting": s["forgetting"], "T2_final_mse": s["T2_final_mse"],
            "ok": s["forgetting"] <= 0.85 * sgdB["forgetting"] and s["T2_final_mse"] <= 1.1 * sgdB["T2_final_mse"]} \
            if sgdB["stable"] else None
    G["V1_B"] = {"pass": any(v and v["ok"] for v in v1.values()), "controls": v1,
                 "SGD": {"forgetting": sgdB.get("forgetting"), "T2_final_mse": sgdB.get("T2_final_mse")}}
    sgdC = summ["Cstar"]["SGD"]
    v2 = {}
    for c in ("R12_fast_weights", "R13_fast_slow", "R15_three_factor"):
        s = summ["Cstar"][c]
        v2[c] = None if not (s["stable"] and sgdC["stable"]) else {
            "hl": s["hl_censored_mean"], "ok": s["hl_censored_mean"] <= 0.9 * sgdC["hl_censored_mean"]}
    G["V2_Cstar"] = {"pass": any(v and v["ok"] for v in v2.values()), "controls": v2,
                     "SGD_hl": sgdC.get("hl_censored_mean")}
    G["V3_F"] = {"pass": float(np.mean([x["ood_acc"] for x in synth])) >= 0.95, "synthesis": synth}
    vd = {}
    for kappa in (1e4, 1e6):
        ng = D[f"natgrad@{kappa:g}"]["select"]["S_tau"]
        base = min(D[f"SGD@{kappa:g}"]["select"]["S_tau"], D[f"SGDM@{kappa:g}"]["select"]["S_tau"])
        vd[f"{kappa:g}"] = {"natgrad": ng, "min_SGD_SGDM": base, "ok": bool(np.isfinite(ng) and ng <= base / 3)}
    G["V_D"] = {"pass": all(v["ok"] for v in vd.values()), "kappa": vd,
                "S_tau_all": {k: v["select"] for k, v in D.items()}}

    mandatory = ["M2_B_fit", "M3_B_interference", "M4_F_failure", "M5_detector", "M6_controls_run",
                 "M7_Cstar_sanity", "V1_B", "V2_Cstar", "V3_F", "V_D"]
    failed = [g for g in mandatory if not G.get(g, {"pass": False})["pass"]]
    passed = not failed

    recorded = {
        "unclipped_generic_diagnostic": {t: {m: summ[t].get(m) for m in DIAG if m in summ[t]} for t in summ},
        "AdamW_and_fast_weight_columns": {"Cstar": {m: summ["Cstar"][m] for m in ("AdamW", "R12_fast_weights", "R13_fast_slow")},
                                           "D_AdamW": {k: v["select"] for k, v in D.items() if k.startswith("AdamW")}},
        "seed_CV_under_SGD": {
            "B_forgetting": _cv(summ["B"]["SGD"].get("forgetting_seeds")),
            "Cstar_hl": _cv(summ["Cstar"]["SGD"].get("hl_censored_seeds")),
            "F_ood_err": _cv(summ["F"]["SGD"].get("ood_err_seeds"))},
        "best_generic": {t: best_generic(summ, t) for t in ("B", "Cstar", "F")},
    }
    cpu_parent = accounting.process_cpu_seconds() - cpu0
    cpu = cpu_parent + worker_cpu
    wall = time.time() - wall0
    led = accounting.record("stage1", cpu, wall, f"official Stage-1 calibration (parent {cpu_parent:.1f}s + workers {worker_cpu:.1f}s)")
    result = {"stage": 1, "protocol": "v3", "pass": passed, "failed_gates": failed,
              "stop_reason": None if passed else "STAGE-1 MANDATORY GATE FAILURE: " + ", ".join(failed),
              "stage2_allowed": passed, "gates": G, "summaries": summ, "lr_selection": sels,
              "recorded_only": recorded, "seeds": SEEDS, "cpu_seconds": round(cpu, 2),
              "wall_seconds": round(wall, 2), "cumulative_cpu_hours": led["total_cpu_hours"]}
    with open(os.path.join(OUT, "stage1_result.json"), "w") as f:
        json.dump(result, f, indent=1, default=_json)
    man = manifest.build_manifest("stage1", {"git_at_start": git_at_start, "seeds": SEEDS, "lr_grid": list(LR_GRID),
                                             "jobs": [f"{t}:{m}" for t, m in JOBS], "cpu_seconds": round(cpu, 2),
                                             "stage1_pass": passed, "failed_gates": failed})
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(man, f, indent=1)
    print(json.dumps({"pass": passed, "failed": failed,
                      "gates": {k: v["pass"] for k, v in G.items()}, "cpu_s": round(cpu, 1)}, indent=1))
    return 0 if passed else 2


def _cv(x):
    if not x:
        return None
    a = np.asarray(x, float)
    return float(a.std(ddof=1) / abs(a.mean())) if a.mean() != 0 else None


def _json(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and math.isinf(o):
        return "inf"
    return str(o)


if __name__ == "__main__":
    sys.exit(main())
