"""Prereg v7 static validation of the detector-aligned anchored constructor (before any v7 search).

Structural-validation seed 70707 (non-official).  Constructs requested proposals until exactly
1,000 proposals are emitted, and checks them structurally only.  Nothing is trained: no T0, no
probe run, no B / C* / F, no FamilyLibrary.
Writes runs/v7_static_validation/{validation.json, proposals.jsonl.gz}.

Pass criteria (prereg v7 "v7 static validation"; fixed here before the run):
  1. 1,000 / 1,000 emitted proposals type-valid and within node / depth / register limits;
  2. every emitted proposal: update_every = 1, no cvec, backprop learning signal in dW, exact SGD
     backbone, exact class template (v6 C1 / C3; v7 C2 incl. residual scale 0.1, selector depth
     0-1 with an activity leaf, topk k in {1,4,8} or where(selector, 1.0, (sub 1.0 1.0)));
  3. unchanged fingerprint on every emitted (raw) proposal: learning signal present and the
     intended primary class present -- C1 as C1, C2 as C2 (unchanged Analysis.c2), C3 as C3;
  4. unchanged fingerprint on the canonical form: learning signal present; the intended class may
     be absent only where canonicalization makes the drawn expression vacuous (its simplified
     form reads no required leaf) -- reported as a count, any other loss fails;
  5. primary-class sampling consistent with uniform: chi-square p > 0.01 over requested proposals;
     sub-choices (C1 type / decay, C3 decay / kind / theta, C2 route / k / selector depth) reported;
  6. invalid instantiated attempts recorded separately (label, code, class, attempt number);
     conditional activity redraws recorded separately and not counted;
  7. no task / probe / benchmark / evaluation module imported during construction (sys.modules
     measured right after construction, before any check).
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
from ams.grammar import program_to_dict, reads, sexpr  # noqa: E402
from ams.v7gen import V7_CLASSES, DetectorAlignedGen, v7_invariants  # noqa: E402

OUT = os.path.join(HERE, "runs", "v7_static_validation")
CFG = manifest.RUN_CONFIG["stage2_v7"]["static_validation"]
SEED, N = CFG["seed"], CFG["n_emitted"]
FORBIDDEN = ("ams.tasks", "ams.runners", "ams.tier1", "ams.substrate", "ams.probes", "ams.controls",
             "ams.families", "ams.metrics", "ams.interp", "ams.search")


def _p(x):
    x = [v for v in x]
    return float(chisquare(x).pvalue) if sum(x) and len(x) > 1 else None


def _drawn(p, meta):
    """The conditionally drawn expression, its type environment and the leaves it must read."""
    from ams.fingerprint import DATA_LEAVES
    from ams.v7gen import V7_ACT_C2
    if meta["v6_class"] == "C2":
        return p.dW.args[1].args[0].args[1].args[0], {}, V7_ACT_C2
    return p.reg_updates[0], p.reg_types(), DATA_LEAVES


def main():
    assert SEED == 70707 and SEED != manifest.RUN_CONFIG["stage2_v7"]["search_seed"]
    os.makedirs(OUT, exist_ok=True)
    git = {"commit": manifest._git("rev-parse", "HEAD"),
           "dirty_excluding_runs": bool(manifest._git("status", "--porcelain", "--", ".", ":!runs"))}
    gen = DetectorAlignedGen(random.Random(SEED))
    built, n_emitted = [], 0
    while n_emitted < N:
        att = list(gen.v6_attempts())
        built.append(att)
        n_emitted += att[-1][2] is None
    leaked = sorted(m for m in FORBIDDEN if m in sys.modules)       # construction phase only
    from ams.canon import canon, simplify
    from ams.fingerprint import fingerprint

    rows, slots = [], []
    for s, att in enumerate(built):
        slots.append({"slot": s, "class": att[0][1]["v6_class"], "attempts": len(att), "emitted": att[-1][2] is None})
        for p, meta, code in att:
            row = {"slot": s, **meta, "invalid_code": code, "raw": program_to_dict(p)}
            if code is None:
                row["invariants"] = v7_invariants(p, meta)
                fr, c = fingerprint(p), canon(p)
                fc = fingerprint(c)
                e, rt, need = _drawn(p, meta)
                row.update(raw_couplings=fr["couplings"], raw_learning_signal=fr["learning_signal"],
                           canon_couplings=fc["couplings"], canon_learning_signal=fc["learning_signal"],
                           canon_descriptor=fc["descriptor"], canonical=program_to_dict(c),
                           drawn_simplified=sexpr(simplify(e, rt)),
                           drawn_vacuous=not (reads(simplify(e, rt)) & need))
            rows.append(row)

    em = [r for r in rows if r["invalid_code"] is None]
    inv_names = sorted({k for r in em for k in r["invariants"]})
    inv_fail = {k: sum(not r["invariants"].get(k, True) for r in em) for k in inv_names}
    inv_fail["missing_check"] = sum(any(k not in r["invariants"] for k in
                                        ("type_valid", "within_node_depth_limits", "register_limits",
                                         "backbone_exact", "class_template_exact", "backprop_signal_in_dW"))
                                    for r in em)
    by = collections.defaultdict(list)
    for r in em:
        by[r["v6_class"]].append(r)
    per_class = {}
    for c in V7_CLASSES:
        rs = by[c]
        per_class[c] = {
            "requested": sum(s["class"] == c for s in slots),
            "attempts": sum(r["v6_class"] == c for r in rows),
            "invalid_attempts": dict(collections.Counter(r["invalid_code"] for r in rows
                                                         if r["v6_class"] == c and r["invalid_code"])),
            "emitted": len(rs),
            "raw_intended_detected": sum(c in r["raw_couplings"] for r in rs),
            "canon_intended_detected": sum(c in r["canon_couplings"] for r in rs),
            "canon_loss_vacuous": sum(c not in r["canon_couplings"] and r["drawn_vacuous"] for r in rs),
            "canon_loss_non_vacuous": sum(c not in r["canon_couplings"] and not r["drawn_vacuous"] for r in rs),
            "raw_learning_signal": sum(r["raw_learning_signal"] for r in rs),
            "canon_learning_signal": sum(r["canon_learning_signal"] for r in rs),
            "conditional_redraws_not_counted": sum(r["redraws"] for r in rows if r["v6_class"] == c),
            "drawn_expr_depth": dict(collections.Counter(r["expr_depth"] for r in rs)),
        }
    sub = {
        "C1_reg_type": collections.Counter(r["reg_type"] for r in by["C1"]),
        "C1_decay": collections.Counter(r["decay"] for r in by["C1"]),
        "C3_decay": collections.Counter(r["decay"] for r in by["C3"]),
        "C3_kind": collections.Counter(r["kind"] for r in by["C3"]),
        "C3_theta": collections.Counter(r["theta"] for r in by["C3"]),
        "C2_route": collections.Counter(r["route"] for r in by["C2"]),
        "C2_topk_k": collections.Counter(r["k"] for r in by["C2"] if r["route"] == "topk"),
        "C2_selector_depth": collections.Counter(r["expr_depth"] for r in by["C2"]),
    }
    requested = [per_class[c]["requested"] for c in V7_CLASSES]
    uniform = {"requested": requested, "p_requested": _p(requested),
               "emitted": [per_class[c]["emitted"] for c in V7_CLASSES],
               **{f"p_{k}": _p(list(v.values())) for k, v in sub.items()}}
    invalid_rows = [{"slot": r["slot"], "class": r["v6_class"], "attempt": r["attempt"], "code": r["invalid_code"]}
                    for r in rows if r["invalid_code"]]
    checks = {
        "1_emitted_1000_type_valid_within_limits":
            len(em) == N and all(r["invariants"].get("type_valid") and r["invariants"].get("within_node_depth_limits")
                                 and r["invariants"].get("register_limits") for r in em),
        "2_constructor_invariants_backbone_templates": all(v == 0 for v in inv_fail.values()),
        "3a_raw_learning_signal": all(r["raw_learning_signal"] for r in em),
        "3b_raw_intended_class_recognized": all(r["v6_class"] in r["raw_couplings"] for r in em),
        "4a_canon_learning_signal": all(r["canon_learning_signal"] for r in em),
        "4b_canon_class_loss_only_vacuous": all(r["v6_class"] in r["canon_couplings"] or r["drawn_vacuous"] for r in em),
        "5_uniform_primary_class": uniform["p_requested"] is not None and uniform["p_requested"] > 0.01,
        "6_invalid_attempts_recorded_separately": len(invalid_rows) == len(rows) - len(em),
        "7_no_evaluation_modules_imported_during_construction": not leaked,
    }
    res = {
        "protocol": manifest.RUN_CONFIG["protocol"], "seed": SEED, "n_emitted_target": N, "git_at_start": git,
        "pass": all(checks.values()), "checks": checks,
        "requested_proposals": len(slots), "instantiated_attempts": len(rows), "emitted": len(em),
        "invalid_attempts": invalid_rows, "skipped_requests": sum(not s["emitted"] for s in slots),
        "invariant_failures": inv_fail, "per_class": per_class, "sub_choices": sub, "uniformity": uniform,
        "evaluation_modules_imported_during_construction": leaked,
        "no_task_evaluation": "no T0, probe, B, C* or F run; no FamilyLibrary; structural checks only",
    }
    with open(os.path.join(OUT, "validation.json"), "w") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=str)
    with gzip.open(os.path.join(OUT, "proposals.jsonl.gz"), "wt", 9) as f:
        for r in rows:
            f.write(json.dumps(r, default=str) + "\n")
    print(json.dumps({k: res[k] for k in ("pass", "checks", "requested_proposals", "instantiated_attempts",
                                          "emitted", "uniformity")}, indent=1, default=str))
    for c in V7_CLASSES:
        print(c, json.dumps(per_class[c], default=str))
    return 0 if res["pass"] else 5


if __name__ == "__main__":
    sys.exit(main())
