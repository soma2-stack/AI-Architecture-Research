"""Prereg v8 pre-search implementation validation (before any v8 candidate training).

Checks (all must pass; fixed here before the run):
  1. full test suite passes (pytest, subprocess);
  2. the 155-entry reference/disguise collision golden snapshot is unchanged;
  3. the v7 C1/C2/C3 constructor is unchanged: the v8 generator reproduces all 1,000 stored v7
     static-validation proposals (seed 70707) exactly, every emitted proposal satisfies the v7
     invariants and the unchanged fingerprint recognizes its intended class;
  4. regression tests: gate-mutation zero spelling; exact N_GEN_MAX boundary;
  5. C* AULC unit tests on hand-constructed curves (no adaptation = 1, monotone < 1, worsening > 1);
  6. offline replay of the stored v7 *generic* C* curves (runs/stage3_v7 shared SGD / SGDM / AdamW
     jobs): AULC finite and bit-identical on recomputation -- no candidate outcome is read;
  7. seed separation (fast 5000-5002, confirmation 6000-6007, Stage-3 30000-30009 disjoint from
     each other and from every earlier set) and the Stage-3 lock (runners refuse 30000-30009;
     no recorded run used them);
  8. the active configuration is prereg v8 with search seed 2026092808.
No candidate is trained.  Writes runs/v8_presearch_validation/validation.json."""
import gzip
import json
import math
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from ams import manifest  # noqa: E402

OUT = os.path.join(HERE, "runs", "v8_presearch_validation")


def pytest(args):
    r = subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q", *args], cwd=HERE,
                       capture_output=True, text=True)
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    m = re.search(r"(\d+) passed", tail)
    return {"returncode": r.returncode, "summary": tail, "passed": int(m.group(1)) if m else 0,
            "failed": "failed" in tail or "error" in tail}


def main():
    os.makedirs(OUT, exist_ok=True)
    git = {"commit": manifest._git("rev-parse", "HEAD"),
           "dirty_excluding_runs": bool(manifest._git("status", "--porcelain", "--", ".", ":!runs"))}
    checks, info = {}, {}

    suite = pytest([])
    info["full_suite"] = suite
    checks["1_full_suite"] = suite["returncode"] == 0 and suite["passed"] > 0 and not suite["failed"]

    gold = pytest(["tests/test_repair1.py::test_reference_collision_outputs_identical_to_pre_repair"])
    info["golden_snapshot"] = gold
    checks["2_golden_155_unchanged"] = gold["returncode"] == 0 and gold["passed"] == 1

    from ams.fingerprint import fingerprint
    from ams.grammar import program_to_dict
    from ams.v7gen import v7_invariants
    from ams.v8gen import V8Gen
    rows = [json.loads(l) for l in gzip.open(os.path.join(HERE, "runs", "v7_static_validation", "proposals.jsonl.gz"), "rt")]
    g = V8Gen(random.Random(70707))
    got, inv_bad, cls_bad = [], 0, 0
    while len(got) < len(rows):
        for p, meta, code in g.v6_attempts():
            got.append(program_to_dict(p))
            if code is None:
                inv_bad += not all(v7_invariants(p, meta).values())
                cls_bad += meta["v6_class"] not in fingerprint(p)["couplings"]
    info["v7_constructor"] = {"stored_proposals": len(rows), "identical": got == [r["raw"] for r in rows],
                              "invariant_failures": inv_bad, "class_not_recognized": cls_bad}
    checks["3_v7_constructor_unchanged"] = got == [r["raw"] for r in rows] and inv_bad == 0 and cls_bad == 0

    reg = pytest(["tests/test_v8.py", "-k", "gate_mutation_zero or exact_cap or uncounted_candidate"])
    info["repair_regressions"] = reg
    checks["4_repair_regressions"] = reg["returncode"] == 0 and reg["passed"] >= 4

    aulc = pytest(["tests/test_v8.py", "-k", "aulc"])
    info["aulc_unit_tests"] = aulc
    checks["5_aulc_unit_tests"] = aulc["returncode"] == 0 and aulc["passed"] >= 5

    from ams import metrics as MX
    from ams.tasks import TaskCstar
    rep = {}
    for line in gzip.open(os.path.join(HERE, "runs", "stage3_v7", "jobs.jsonl.gz"), "rt"):
        j = json.loads(line)
        if j["job"]["cid"] != "shared:Cstar" or j["job"]["cond"] not in ("SGD", "SGDM", "AdamW"):
            continue
        r = j["result"]
        vals = []
        for row, bad in zip(r["R1"], r["unstable"]):
            if bad:
                continue
            a1 = MX.adaptation_aulc(r["eval_steps"], row, [256, 384], TaskCstar.tau)
            a2 = MX.adaptation_aulc(r["eval_steps"], row, [256, 384], TaskCstar.tau)
            vals.append((a1, a1 == a2 and math.isfinite(a1)))
        rep[j["job"]["cond"]] = {"n_stable_runs": len(vals), "all_finite_deterministic": all(ok for _, ok in vals),
                                 "min": min(v for v, _ in vals), "max": max(v for v, _ in vals)}
    info["v7_generic_curve_replay"] = rep
    checks["6_v7_generic_aulc_replay"] = (set(rep) == {"SGD", "SGDM", "AdamW"}
                                          and all(v["all_finite_deterministic"] and v["n_stable_runs"] > 0
                                                  for v in rep.values()))

    from ams import confirm as CF
    from ams import tier1
    from ams.runners import LOCKED_STAGE3_SEEDS, SeedLockError, _runs
    v8 = manifest.RUN_CONFIG["stage2_v8"]
    sets = {"fast": set(v8["fast_tier1_seeds"]), "confirm": set(v8["confirm_seeds"]), "stage3": set(v8["stage3_seeds"]),
            "sanity": {500}, "stage1": set(range(100, 105)), "v5_v7_tier1": {1000, 1001, 1002},
            "v7_stage3": set(range(10000, 10010)), "tier3": set(range(20000, 20010))}
    names = list(sets)
    disjoint = all(not (sets[a] & sets[b]) for i, a in enumerate(names) for b in names[i + 1:])
    locked = True
    for s in LOCKED_STAGE3_SEEDS:
        try:
            _runs([s], (0.1,))
            locked = False
        except SeedLockError:
            pass
    used = set()
    for root, _, files in os.walk(os.path.join(HERE, "runs")):
        for fn in files:
            if fn == "manifest.json":
                m = json.load(open(os.path.join(root, fn)))
                for k in ("seeds", "tier1_seeds", "sanity_seed", "search_seed"):
                    v = m.get(k)
                    used |= set(v) if isinstance(v, list) else ({v} if isinstance(v, int) else set())
    info["seeds"] = {k: sorted(v) for k, v in sets.items()}
    info["stage3_seeds_in_recorded_manifests"] = sorted(used & LOCKED_STAGE3_SEEDS)
    checks["7_seed_separation_and_stage3_lock"] = (
        disjoint and locked and not (used & LOCKED_STAGE3_SEEDS) and set(v8["stage3_seeds"]) == set(LOCKED_STAGE3_SEEDS)
        and tier1.V8_TIER1_SEEDS == v8["fast_tier1_seeds"] and CF.CONFIRM_SEEDS == v8["confirm_seeds"]
        and not os.path.exists(os.path.join(HERE, "runs", "stage3_v8")))

    checks["8_active_protocol_v8"] = (manifest.RUN_CONFIG["protocol"] == "AMS-prereg-v8"
                                      and v8["search_seed"] == 2026092808)

    res = {"protocol": manifest.RUN_CONFIG["protocol"], "git_at_start": git, "pass": all(checks.values()),
           "checks": checks, "info": info,
           "no_candidate_training": "no v8 candidate trained; tests run only non-official seeds and fixtures"}
    with open(os.path.join(OUT, "validation.json"), "w") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=str)
    print(json.dumps({"pass": res["pass"], "checks": checks, "suite": suite["summary"]}, indent=1))
    return 0 if res["pass"] else 5


if __name__ == "__main__":
    sys.exit(main())
