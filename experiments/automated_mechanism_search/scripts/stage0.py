"""Official Stage 0 (prereg v3 sec. 17): implementation validity + v3 mandatory checks.

Writes runs/stage0_v3/{stage0_result.json, manifest.json, pytest.txt, taskB_gate.json,
collision_selfcheck.json, profile.json} and appends to runs/cpu_ledger.json.
Stage 0 passes only if every check passes; otherwise the run stops before Stage 1.
"""
import itertools
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np  # noqa: E402

from ams import accounting, manifest  # noqa: E402
from ams.canon import canon  # noqa: E402
from ams.families import DISGUISES, REFERENCES, FamilyLibrary  # noqa: E402
from ams.grammar import make_program, M, O  # noqa: E402
from ams.probes import (CORPUS_PATH, ProbeCorpusError, cos, git_blob_sha, load_corpus,  # noqa: E402
                        regeneration_check)
from ams.runners import V3_SEEDS, taskB_gate_v3  # noqa: E402
from ams.substrate import DT, Net, ProgramLearner, Trainer  # noqa: E402

OUT = os.path.join(HERE, "runs", "stage0_v3")
GATE_SEEDS = list(V3_SEEDS)


def main():
    os.makedirs(OUT, exist_ok=True)
    cpu0, wall0 = accounting.process_cpu_seconds(), time.time()
    git_at_start = {"commit": manifest._git("rev-parse", "HEAD"),
                    "dirty_excluding_runs": bool(manifest._git("status", "--porcelain", "--", ".", ":!runs"))}
    checks = {}

    # 1. frozen probe corpus (mandatory before behavioural deduplication)
    try:
        load_corpus()
        checks["probe_corpus"] = {"pass": True, "blob": git_blob_sha(CORPUS_PATH),
                                  "regeneration_aid": regeneration_check()}
    except ProbeCorpusError as e:
        checks["probe_corpus"] = {"pass": False, "error": str(e)}

    # 2. immutable run configuration
    checks["run_config"] = {"pass": True, "sha256": manifest.write_or_verify_config()}

    # 3. full Stage-0 test suite
    r = subprocess.run([sys.executable, "-m", "pytest", "-o", "addopts=", "-p", "no:cacheprovider", "tests"],
                       cwd=HERE, capture_output=True, text=True)
    with open(os.path.join(OUT, "pytest.txt"), "w") as f:
        f.write(r.stdout + r.stderr)
    last = [l for l in r.stdout.strip().splitlines() if l.strip()][-1] if r.stdout.strip() else ""
    checks["test_suite"] = {"pass": r.returncode == 0, "summary": last}

    # 4. v3 Task-B directional gradient-conflict gate (prereg v3 sec. 6.1; D-V3-1)
    gate = taskB_gate_v3(GATE_SEEDS)
    g_pass = gate["pass"]
    with open(os.path.join(OUT, "taskB_gate.json"), "w") as f:
        json.dump({"rule": "v3: every seed-level mean cosine < 0 AND >= 90% of all 512 paired "
                           "first-layer weight-gradient cosines < 0 (no magnitude threshold)", **gate}, f, indent=1)
    checks["taskB_gradient_conflict_gate_v3"] = {
        "pass": g_pass, "rule": "all seed means < 0; frac(cos < 0) >= 0.90",
        "per_seed_mean_cos": {g["seed"]: round(g["mean_cos"], 4) for g in gate["per_seed"]},
        "per_seed_n_negative": {g["seed"]: g["n_negative"] for g in gate["per_seed"]},
        "cond1_all_seed_means_negative": gate["cond1_all_seed_means_negative"],
        "frac_negative": round(gate["cond2_frac_negative"], 4), "n_cosines": gate["n_cosines"],
        "pooled_mean_cos": round(float(np.mean([g["mean_cos"] for g in gate["per_seed"]])), 4)}

    # 5. collision-library self-check (recall, reference collisions)
    lib = FamilyLibrary()
    recall_miss, attr_diff = [], []
    for name, p in REFERENCES.items():
        for dn, d in [("identity", lambda x: x)] + list(DISGUISES.items()):
            m = lib.match(canon(d(p)))
            if m is None:
                recall_miss.append((name, dn))
            elif m["family"] != name:
                attr_diff.append((name, dn, m["family"]))
    coll = []
    for a, b in itertools.combinations(list(lib.canon), 2):
        s = max(max(cos(x, lib.bref[b]) for x in lib.runner.beta_all(lib.canon[a])),
                max(cos(x, lib.bref[a]) for x in lib.runner.beta_all(lib.canon[b])))
        if s >= 0.99:
            coll.append((a, b, round(s, 5)))
    sc = {"n_references": len(REFERENCES), "n_variants": len(REFERENCES) * (1 + len(DISGUISES)),
          "recall_misses": recall_miss, "attribution_differs": attr_diff,
          "reference_pairs": len(lib.canon) * (len(lib.canon) - 1) // 2, "family_rule_collisions": coll,
          "known_blind_spots": ["STRUCT events are not executed by the one-step probe",
                                "topk with k >= probe dimension (I=8, O=6) is all-ones in probes",
                                "per-step scalar modulation of the whole update is scale-invariant in beta",
                                "W_ep0 is not a corpus field (D-PROBE-2 derivation)"]}
    with open(os.path.join(OUT, "collision_selfcheck.json"), "w") as f:
        json.dump(sc, f, indent=1)
    checks["detector_recall"] = {"pass": not recall_miss, "misses": len(recall_miss),
                                 "attribution_differs": len(attr_diff), "reference_collisions": len(coll)}

    # 6. profiling (random data; no benchmark generator is trained)
    p = canon(make_program("(neg (rowscale (outer d_bp a) (topk h 8)))", "(neg d_bp)", w_eff="(mul r1 0.5)",
                           regs=[("r1", M, "RUN", "0", 0.9, "(outer (sub h r2) a)"),
                                 ("r2", O, "RUN", "0", 0.99, "h")]))
    rng = np.random.default_rng(0)
    net = Net(32, 4, list(range(9)))
    tr = Trainer(net, ProgramLearner(p), [1e-2] * 9)
    tr.set_episodes(None); tr.episode_start()
    X = rng.standard_normal((9, 32, 32)).astype(DT); Y = rng.standard_normal((9, 32, 4)).astype(DT)
    t0 = time.process_time()
    for _ in range(40):
        tr.step(X, Y)
    ms_b = (time.process_time() - t0) / 40 * 1e3
    net1 = Net(1, 1, list(range(9)))
    tr1 = Trainer(net1, ProgramLearner(p), [1e-2] * 9)
    tr1.set_episodes(None); tr1.episode_start()
    t0 = time.process_time()
    for _ in range(100):
        tr1.step(rng.standard_normal((9, 1, 1)).astype(DT), rng.standard_normal((9, 1, 1)).astype(DT))
    ms_c = (time.process_time() - t0) / 100 * 1e3
    est = (1000 * ms_b + 500 * ms_b + 448 * ms_c) / 1e3 * 1.15          # +15% evaluation overhead
    prof = {"ms_per_step_batch32_9runs": round(ms_b, 3), "ms_per_step_online_9runs": round(ms_c, 3),
            "est_tier1_cpu_s_per_candidate": round(est, 2),
            "est_tier1_cpu_h_for_1200": round(est * 1200 / 3600, 2),
            "AE_stage0_exit_criterion_cpu_s": 20.0, "within_AE_estimate": bool(est <= 20.0)}
    with open(os.path.join(OUT, "profile.json"), "w") as f:
        json.dump(prof, f, indent=1)
    checks["profiling"] = {"pass": True, **prof}

    # verdict
    passed = all(c["pass"] for c in checks.values())
    stop = None if passed else "PREREGISTRATION VALIDITY FAILURE (v3): " + ", ".join(
        k for k, c in checks.items() if not c["pass"])
    cpu = accounting.process_cpu_seconds() - cpu0
    wall = time.time() - wall0
    led = accounting.record("stage0_v3", cpu, wall, "official v3 Stage-0 script (tests, v3 gate, self-check, profile)")
    result = {"stage": 0, "protocol": "v3", "pass": passed, "stop_reason": stop, "checks": checks,
              "stage1_allowed": passed, "cpu_seconds": round(cpu, 2), "wall_seconds": round(wall, 2),
              "cumulative_cpu_hours": led["total_cpu_hours"]}
    with open(os.path.join(OUT, "stage0_result.json"), "w") as f:
        json.dump(result, f, indent=1, default=str)
    man = manifest.build_manifest("stage0_v3", {"git_at_start": git_at_start, "seeds": {"taskB_gate": GATE_SEEDS},
                                             "cpu_seconds": round(cpu, 2), "stage0_pass": passed,
                                             "stop_reason": stop})
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(man, f, indent=1)
    print(json.dumps({"pass": passed, "stop_reason": stop,
                      "checks": {k: c["pass"] for k, c in checks.items()},
                      "gate": checks["taskB_gradient_conflict_gate_v3"], "profile": prof,
                      "detector": checks["detector_recall"], "cpu_s": round(cpu, 1)}, indent=1))
    return 0 if passed else 2


if __name__ == "__main__":
    sys.exit(main())
