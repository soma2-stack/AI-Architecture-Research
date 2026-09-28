"""Prereg v6 static validation of the SGD-anchored initial constructor (before any v6 search).

Generates exactly 1,000 proposal slots with the non-official test seed 60606 and checks them
structurally only.  Nothing is trained: no T0, no probe run, no B / C* / F, no FamilyLibrary.
Writes runs/v6_static_validation/{validation.json, proposals.jsonl.gz}.

Pass criteria (fixed here before the run):
  1. every valid proposal: type-valid; node / depth / register limits; update_every = 1; no cvec;
     backprop signal in dW; exact SGD backbone; exact class template (C1 / C2 / C3 as in v6);
  2. every slot yields a valid proposal within 10 attempts;
  3. frozen fingerprint (unchanged) on the RAW proposal: learning signal present and the intended
     coupling class present (the constructor is responsible for these);
  4. frozen fingerprint on the CANONICAL proposal: learning signal present; the intended coupling
     may be absent only where canonicalization removed a vacuous data dependence (i.e. it is
     present on the raw proposal) -- that is the unchanged filter deciding, reported as a count;
  5. uniform primary-class choice over slots: chi-square p > 0.01; sub-choices reported;
  6. no task / probe / benchmark / evaluation module is imported by the constructor.  Measured
     on sys.modules right after all 1,000 slots are constructed and before any structural check
     runs.  (The first run, kept as validation_initial_check6_whole_process.json, measured the
     whole process instead; it flagged only ams.interp, which the unchanged canonicalizer imports
     for constant folding during the checks, not the constructor.)
"""
import collections
import gzip
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from scipy.stats import chisquare  # noqa: E402

from ams import manifest  # noqa: E402
from ams.grammar import program_to_dict  # noqa: E402
from ams.v6gen import V6_CLASSES, AnchoredGen, v6_invariants  # noqa: E402

OUT = os.path.join(HERE, "runs", "v6_static_validation")
CFG = manifest.RUN_CONFIG["stage2_v6"]["static_validation"]
SEED, N = CFG["seed"], CFG["n_proposals"]
FORBIDDEN = ("ams.tasks", "ams.runners", "ams.tier1", "ams.substrate", "ams.probes", "ams.controls",
             "ams.families", "ams.metrics", "ams.interp", "ams.search")


def _p(x):
    return float(chisquare(x).pvalue) if sum(x) else None


def main():
    assert SEED != manifest.RUN_CONFIG["stage2_v6"]["search_seed"] and SEED != 20260928
    os.makedirs(OUT, exist_ok=True)
    git = {"commit": manifest._git("rev-parse", "HEAD"),
           "dirty_excluding_runs": bool(manifest._git("status", "--porcelain", "--", ".", ":!runs"))}
    gen = AnchoredGen(random.Random(SEED))
    built = [list(gen.v6_attempts()) for _ in range(N)]
    leaked = sorted(m for m in FORBIDDEN if m in sys.modules)       # constructor phase only
    from ams.canon import canon
    from ams.fingerprint import fingerprint
    rows, slots = [], []
    for s, att in enumerate(built):
        slots.append({"slot": s, "class": att[0][1]["v6_class"], "attempts": len(att),
                      "valid": att[-1][2] is None})
        for p, meta, code in att:
            row = {"slot": s, **meta, "invalid_code": code, "raw": program_to_dict(p)}
            if code is None:
                row["invariants"] = v6_invariants(p, meta)
                fr = fingerprint(p)
                c = canon(p)
                fc = fingerprint(c)
                row.update(raw_couplings=fr["couplings"], raw_learning_signal=fr["learning_signal"],
                           canon_couplings=fc["couplings"], canon_learning_signal=fc["learning_signal"],
                           canon_descriptor=fc["descriptor"], canonical=program_to_dict(c))
            rows.append(row)
    process_modules = sorted(m for m in FORBIDDEN if m in sys.modules)

    valid = [r for r in rows if r["invalid_code"] is None]
    inv_names = sorted({k for r in valid for k in r["invariants"]})
    inv_fail = {k: sum(not r["invariants"].get(k, False) for r in valid) for k in inv_names}
    by = collections.defaultdict(list)
    for r in valid:
        by[r["v6_class"]].append(r)
    per_class = {}
    for c in V6_CLASSES:
        rs = by[c]
        per_class[c] = {
            "slots": sum(s["class"] == c for s in slots),
            "attempts": sum(r["v6_class"] == c for r in rows),
            "invalid_attempts": collections.Counter(r["invalid_code"] for r in rows
                                                    if r["v6_class"] == c and r["invalid_code"]),
            "valid": len(rs),
            "raw_intended_coupling_detected": sum(c in r["raw_couplings"] for r in rs),
            "canon_intended_coupling_detected": sum(c in r["canon_couplings"] for r in rs),
            "canon_no_coupling_at_all": sum(not r["canon_couplings"] for r in rs),
            "raw_learning_signal": sum(r["raw_learning_signal"] for r in rs),
            "canon_learning_signal": sum(r["canon_learning_signal"] for r in rs),
            "conditional_redraws": sum(r["redraws"] for r in rows if r["v6_class"] == c),
            "drawn_expr_depth_attempts": collections.Counter(r["expr_depth"] for r in rows if r["v6_class"] == c),
            "drawn_expr_depth_valid": collections.Counter(r["expr_depth"] for r in rs),
        }
    sub = {
        "C1_reg_type": collections.Counter(r["reg_type"] for r in by["C1"]),
        "C1_decay": collections.Counter(r["decay"] for r in by["C1"]),
        "C3_decay": collections.Counter(r["decay"] for r in by["C3"]),
        "C3_kind": collections.Counter(r["kind"] for r in by["C3"]),
        "C3_theta": collections.Counter(r["theta"] for r in by["C3"]),
    }
    class_slots = [per_class[c]["slots"] for c in V6_CLASSES]
    class_valid = [per_class[c]["valid"] for c in V6_CLASSES]
    uniform = {"slots": class_slots, "p_slots": _p(class_slots), "valid": class_valid,
               "p_valid": _p(class_valid), **{f"p_{k}": _p(list(v.values())) for k, v in sub.items()}}

    raw_cpl_fail = sum(r["v6_class"] not in r["raw_couplings"] for r in valid)
    canon_explained = sum(r["v6_class"] not in r["canon_couplings"] and r["v6_class"] in r["raw_couplings"]
                          for r in valid)
    checks = {
        "1_constructor_invariants": all(v == 0 for v in inv_fail.values()) and len(inv_names) >= 8,
        "2_every_slot_valid_within_10": all(s["valid"] for s in slots),
        "3a_raw_learning_signal": all(r["raw_learning_signal"] for r in valid),
        "3b_raw_intended_coupling": raw_cpl_fail == 0,
        "4a_canon_learning_signal": all(r["canon_learning_signal"] for r in valid),
        "4b_canon_coupling_loss_only_by_canonicalization":
            all(r["v6_class"] in r["canon_couplings"] or r["v6_class"] in r["raw_couplings"] for r in valid),
        "5_uniform_class_choice": uniform["p_slots"] is not None and uniform["p_slots"] > 0.01,
        "6_no_evaluation_modules_imported": not leaked,
    }
    res = {
        "protocol": manifest.RUN_CONFIG["protocol"], "seed": SEED, "n_slots": N, "git_at_start": git,
        "pass": all(checks.values()), "checks": checks,
        "attempts_total": len(rows), "valid_proposals": len(valid),
        "invariant_failures": inv_fail, "per_class": per_class, "sub_choices": sub, "uniformity": uniform,
        "raw_intended_coupling_missing": raw_cpl_fail,
        "canon_coupling_removed_by_canonicalization": canon_explained,
        "evaluation_modules_imported": leaked,
        "listed_modules_loaded_by_whole_process": process_modules,
        "no_task_evaluation": "no T0, probe, B, C* or F run; no FamilyLibrary; structural checks only",
    }
    with open(os.path.join(OUT, "validation.json"), "w") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=str)
    with gzip.open(os.path.join(OUT, "proposals.jsonl.gz"), "wt", 9) as f:
        for r in rows:
            f.write(json.dumps(r, default=str) + "\n")
    print(json.dumps({k: res[k] for k in ("pass", "checks", "attempts_total", "valid_proposals",
                                          "raw_intended_coupling_missing", "uniformity")}, indent=1, default=str))
    for c in V6_CLASSES:
        print(c, json.dumps(per_class[c], default=str))
    return 0 if res["pass"] else 5


if __name__ == "__main__":
    sys.exit(main())
