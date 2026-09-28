"""Official Stage 2 (prereg v5): frozen MAP-Elites search (AE.3.4; D-S2-*, D-T1-*, D-S2-v4).

Budgets: 6,000 generated / 3,000 sanity-evaluated / 1,200 Tier-1 / 20 promoted; CPU only; the
shared 30 CPU-h cap is checked before every Tier-1 evaluation.  Writes runs/stage2/*."""
import json
import math
import multiprocessing as mp
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np  # noqa: E402

from ams import accounting, manifest, search, tier1  # noqa: E402
from ams.controls import GENERIC, init_worker, make, run_job  # noqa: E402
from ams.families import FamilyLibrary  # noqa: E402
from ams.grammar import program_to_dict  # noqa: E402
from ams.runners import run_T0  # noqa: E402

RUN_NAME = sys.argv[1] if len(sys.argv) > 1 else "stage2"      # official repaired rerun: stage2_repair1
OUT = os.path.join(HERE, "runs", RUN_NAME)
assert not os.path.exists(os.path.join(OUT, "manifest.json")), f"{OUT} already holds a run; refusing to overwrite"
SEARCH_SEED = 20260928
SANITY_SEED = 500
CHECKPOINT_EVERY = 25


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
    os.makedirs(OUT, exist_ok=True)
    git_at_start = {"commit": manifest._git("rev-parse", "HEAD"),
                    "dirty_excluding_runs": bool(manifest._git("status", "--porcelain", "--", ".", ":!runs"))}
    s1 = json.load(open(os.path.join(HERE, "runs", "stage1_v5", "stage1_result.json")))
    if not s1["pass"]:
        print("v5 Stage 1 did not pass; Stage 2 not allowed.")
        return 3
    manifest.write_or_verify_config()
    accounting.check_cap()
    assert max(tier1.TIER1_SEEDS + [SANITY_SEED]) < 10000, "confirmation-seed leakage"
    wall0 = time.time()
    state = {"parent0": accounting.self_cpu_seconds(), "workers": 0.0, "ledgered": 0.0, "n_t1": 0}
    log = open(os.path.join(OUT, "records.jsonl"), "w")
    prog_log = open(os.path.join(OUT, "progress.log"), "w")

    def progress(msg):
        prog_log.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
        prog_log.flush()

    def total_cpu():
        return accounting.self_cpu_seconds() - state["parent0"] + state["workers"]

    def checkpoint(note):
        tot = total_cpu()
        delta = tot - state["ledgered"]
        if delta > 0:
            accounting.record(RUN_NAME, delta, 0.0, note)
            state["ledgered"] = tot

    workers = max(1, min(3, (os.cpu_count() or 2) - 1))
    with mp.get_context("fork").Pool(workers, initializer=init_worker) as pool:
        # D-T1-1: Tier-1 generic baselines, once, before any candidate
        jobs = [{"task": t, "learner": m, "seeds": tier1.TIER1_SEEDS} for t in tier1.TASKS for m in GENERIC]
        res = pool.map(run_job, jobs, chunksize=1)
        state["workers"] += sum(r["cpu_s"] for r in res)
        base = tier1.compute_baselines({f"{j['task']}:{j['learner']}": r for j, r in zip(jobs, res)})
        with open(os.path.join(OUT, "baselines_tier1.json"), "w") as f:
            json.dump(base, f, indent=1, default=_json)
        progress(f"baselines: { {t: base['best_generic'][t] for t in tier1.TASKS} }")
        checkpoint("Stage-2 Tier-1 baselines")

        lib = FamilyLibrary()

        def sanity(c):
            return run_T0(make("P", program_to_dict(c)), seed=SANITY_SEED)

        def t1(c):
            accounting.check_cap(total_cpu() - state["ledgered"])
            out = tier1.evaluate(c, base, pool)
            state["workers"] += out.pop("cpu_s_workers")
            state["n_t1"] += 1
            if state["n_t1"] % CHECKPOINT_EVERY == 0:
                checkpoint(f"Stage-2 through Tier-1 #{state['n_t1']}")
                progress(f"tier1={state['n_t1']} counts={pipe.counts} cells={len(pipe.archive)} "
                         f"cum_cpu_h={accounting.load_ledger()['total_cpu_hours']:.3f}")
            return out

        def emit(rec):
            log.write(rec.to_json() + "\n")

        pipe = search.Pipeline(lib, sanity, t1, log=emit)

        class Cap(Exception):
            pass

        try:
            outcome = search.map_elites(pipe, random.Random(SEARCH_SEED), progress)
        except accounting.CPUCapExceeded as e:
            outcome = {"stop": f"CPU_CAP: {e}", "generations": []}
        log.close()
    checkpoint("Stage-2 final")

    promo = search.select_promotions(pipe)
    arch = {str(k): {"pid": r.pid, "quality": r.quality, "descriptor": r.descriptor, "canonical": r.canonical,
                     "raw": r.raw, "fingerprint": r.fingerprint, "family_nearest": r.family,
                     "tier1": r.tier1} for k, r in pipe.archive.items()}
    with open(os.path.join(OUT, "archive.json"), "w") as f:
        json.dump(arch, f, indent=1, default=_json)
    c = dict(pipe.counts)
    n = max(c["generated"], 1)
    evald = c["tier1_evaluated"]
    q_pass = sum(1 for r in pipe.records if r.quality is not None and r.quality >= search.Q_MIN)
    summary = {
        "stop": outcome["stop"], "generations": outcome["generations"], "counts": c,
        "rediscovery_by_family": pipe.rediscovery_by_family,
        "rates_over_generated": {k: v / n for k, v in c.items() if k != "generated"},
        "rediscovery_total": c["REDISCOVERY"] + c["REDISCOVERY_inert"] + c["pure_rule"],
        "rediscovery_rate_over_screened": (c["REDISCOVERY"] + c["REDISCOVERY_inert"] + c["pure_rule"]) /
        max(1, n - c["invalid"] - c["dup_syntactic"] - c["dup_behavioral"] - c["probe_nonfinite"] - c["defect"]),
        "archive_occupancy": f"{len(pipe.archive)}/{search.N_CELLS}",
        "tier1_q_ge_0.15": q_pass,
        "tier1_negative": evald - len(promo),
        "promoted": [r.pid for r in promo],
        "cpu_seconds": total_cpu(), "wall_seconds": time.time() - wall0,
        "cumulative_cpu_hours": accounting.load_ledger()["total_cpu_hours"],
    }
    with open(os.path.join(OUT, "counts.json"), "w") as f:
        json.dump(summary, f, indent=1, default=_json)
    with open(os.path.join(OUT, "promotions.json"), "w") as f:
        json.dump([{"pid": r.pid, "quality": r.quality, "best_task": r.tier1["best_task"],
                    "descriptor": r.descriptor, "canonical": r.canonical, "raw": r.raw,
                    "fingerprint": r.fingerprint, "family_nearest": r.family, "beta_hash": r.beta_hash,
                    "struct_hash": r.struct_hash, "tier1": r.tier1, "K": r.detail.get("K"),
                    "K_info": r.detail.get("K_info"), "cos_P_KP": r.detail.get("cos_P_KP")} for r in promo],
                  f, indent=1, default=_json)
    man = manifest.build_manifest(RUN_NAME, {"git_at_start": git_at_start, "search_seed": SEARCH_SEED,
                                             "tier1_seeds": tier1.TIER1_SEEDS, "sanity_seed": SANITY_SEED,
                                             "stop": outcome["stop"], "counts": c,
                                             "cpu_seconds": total_cpu(), "n_promoted": len(promo)})
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(man, f, indent=1, default=_json)
    progress(f"DONE stop={outcome['stop']} promoted={len(promo)}")
    import gzip
    import shutil
    with open(os.path.join(OUT, "records.jsonl"), "rb") as fi, gzip.open(os.path.join(OUT, "records.jsonl.gz"), "wb", 9) as fo:
        shutil.copyfileobj(fi, fo)
    os.remove(os.path.join(OUT, "records.jsonl"))
    print(json.dumps({k: summary[k] for k in ("stop", "counts", "archive_occupancy", "promoted",
                                             "rediscovery_total", "cumulative_cpu_hours")}, indent=1, default=_json))
    return 0


if __name__ == "__main__":
    sys.exit(main())
