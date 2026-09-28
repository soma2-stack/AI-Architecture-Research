"""Prereg v8 Stage-2 confirmation funnel (ams/confirm.py).

Usage: python3 scripts/stage2_confirm.py <stage2_run> <confirm_run>       e.g. stage2_v8 stage2_v8_confirm
Reads runs/<stage2_run>/archive.json (every occupied cell's current elite, at most 56), computes the
generic confirmation baselines once per task on seeds 6000-6007, evaluates each elite on its frozen
fast best_task on the same seeds, and writes runs/<confirm_run>/{baselines_confirm.json,
confirmation.json, promotions.json, jobs.jsonl.gz, manifest.json}.  promotions.json has the same
record fields as the v7 promotions file (plus q_fast and the confirmation record) and is the only
input to the v8 Stage 3.  CPU only; the shared 30 CPU-h cap is checked before each batch."""
import gzip
import json
import math
import multiprocessing as mp
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np  # noqa: E402

from ams import accounting, manifest  # noqa: E402
from ams import confirm as CF  # noqa: E402
from ams.controls import GENERIC, init_worker, run_job  # noqa: E402
from ams.tier1 import TASKS  # noqa: E402

STAGE2 = sys.argv[1] if len(sys.argv) > 1 else "stage2_v8"
RUN_NAME = sys.argv[2] if len(sys.argv) > 2 else "stage2_v8_confirm"
OUT = os.path.join(HERE, "runs", RUN_NAME)
assert not os.path.exists(os.path.join(OUT, "manifest.json")), f"{OUT} already holds a run; refusing to overwrite"


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


def main():
    assert manifest.RUN_CONFIG["protocol"] == "AMS-prereg-v8"
    s2 = json.load(open(os.path.join(HERE, "runs", STAGE2, "manifest.json")))
    assert s2.get("initial_constructor") == "v8" and s2.get("cstar_metric") == "aulc", "not an official v8 Stage-2 run"
    arch = json.load(open(os.path.join(HERE, "runs", STAGE2, "archive.json")))
    assert len(arch) <= CF.MAX_CANDIDATES
    seeds = CF.CONFIRM_SEEDS
    assert set(seeds).isdisjoint({500, 5000, 5001, 5002, *range(30000, 30010)})
    os.makedirs(OUT, exist_ok=True)
    git_at_start = {"commit": manifest._git("rev-parse", "HEAD"),
                    "dirty_excluding_runs": bool(manifest._git("status", "--porcelain", "--", ".", ":!runs"))}
    manifest.write_or_verify_config()
    parent0 = accounting.self_cpu_seconds()
    state = {"workers": 0.0}
    joblog = gzip.open(os.path.join(OUT, "jobs.jsonl.gz"), "wt", 9)
    workers = max(1, min(3, (os.cpu_count() or 2) - 1))

    def run(jobs, note):
        accounting.check_cap(accounting.self_cpu_seconds() - parent0 + state["workers"] + 60.0 * len(jobs))
        with mp.get_context("fork").Pool(workers, initializer=init_worker) as pool:
            res = pool.map(run_job, jobs, chunksize=1)
        for j, r in zip(jobs, res):
            state["workers"] += r.get("cpu_s", 0.0)
            joblog.write(json.dumps({"job": j, "result": r}, default=_json) + "\n")
        print(f"{note}: {len(jobs)} jobs", flush=True)
        return res

    # generic confirmation baselines, once per task (not counted toward the 56-candidate cap)
    gjobs = [{"task": t, "learner": m, "seeds": seeds} for t in TASKS for m in GENERIC]
    gres = run(gjobs, "generic confirmation baselines")
    base = CF.baselines({f"{j['task']}:{j['learner']}": r for j, r in zip(gjobs, gres)}, seeds)
    with open(os.path.join(OUT, "baselines_confirm.json"), "w") as f:
        json.dump(base, f, indent=1, default=_json)

    # one confirmation per occupied cell's current elite, on its frozen fast best_task
    cells = sorted(arch.items(), key=lambda kv: kv[1]["pid"])
    cjobs = [{"task": rec["tier1"]["best_task"], "learner": "P", "program": rec["canonical"], "seeds": seeds}
             for _, rec in cells]
    cres = run(cjobs, "candidate confirmations")
    joblog.close()

    records = []
    for (cell, rec), j, r in zip(cells, cjobs, cres):
        s = CF.summary(j["task"], r, seeds)
        a = CF.assess(j["task"], s, base, rec["tier1"]["cost"]["penalty"])
        a.update(pid=rec["pid"], cell=cell, descriptor=rec["descriptor"], q_fast=rec["quality"],
                 fast_tier1_pass_on_best=rec["tier1"].get("tier1_pass_on_best"),
                 family_sim=(rec.get("family_nearest") or {}).get("sim"),
                 family=(rec.get("family_nearest") or {}).get("family"), lr=s.get("lr"),
                 diagnostic_half_life=(float(np.mean(s["hl_censored_seeds"]))
                                       if s.get("stable") and j["task"] == "Cstar" else None))
        records.append(a)
    promoted = CF.select(records)
    by_pid = {rec["pid"]: rec for _, rec in cells}
    promo_out = []
    for c in promoted:
        rec = by_pid[c["pid"]]
        promo_out.append({"pid": rec["pid"], "quality": c["q_confirm"], "q_confirm": c["q_confirm"],
                          "q_fast": rec["quality"], "best_task": c["task"], "descriptor": rec["descriptor"],
                          "canonical": rec["canonical"], "raw": rec["raw"], "fingerprint": rec["fingerprint"],
                          "family_nearest": rec["family_nearest"], "tier1": rec["tier1"], "confirmation": c})
    cpu = accounting.self_cpu_seconds() - parent0 + state["workers"]
    accounting.record(RUN_NAME, cpu, 0.0, f"v8 Stage-2 confirmation funnel on {STAGE2} ({len(cells)} elites, seeds 6000-6007)")
    out = {"stage2_run": STAGE2, "seeds": seeds, "n_candidates": len(cells), "git_at_start": git_at_start,
           "n_eligible": sum(r["eligible"] for r in records), "promoted": [c["pid"] for c in promoted],
           "promoted_by_task": {t: sum(c["task"] == t for c in promoted) for t in TASKS},
           "records": records, "cpu_seconds": cpu,
           "cumulative_cpu_hours": accounting.load_ledger()["total_cpu_hours"]}
    with open(os.path.join(OUT, "confirmation.json"), "w") as f:
        json.dump(out, f, indent=1, default=_json)
    with open(os.path.join(OUT, "promotions.json"), "w") as f:
        json.dump(promo_out, f, indent=1, default=_json)
    man = manifest.build_manifest(RUN_NAME, {"git_at_start": git_at_start, "stage2_run": STAGE2, "seeds": seeds,
                                             "n_candidates": len(cells), "promoted": out["promoted"],
                                             "cpu_seconds": cpu})
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(man, f, indent=1, default=_json)
    print(json.dumps({k: out[k] for k in ("n_candidates", "n_eligible", "promoted", "promoted_by_task",
                                          "cpu_seconds", "cumulative_cpu_hours")}, indent=1, default=_json))
    return 0


if __name__ == "__main__":
    sys.exit(main())
