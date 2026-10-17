"""Independent audit of archived Experiment 011 raw JSON. Reads only; never rewrites originals."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from statistics import mean

from . import capacity_010 as c10
from .capacity_011 import baselines, eval_seed

ORDER = ("protected", "protected_no_retain", "gru24", "gru32")


def audit(directory: Path) -> dict:
    runs = []
    for f in sorted(directory.glob("*_*.json")):
        if f.name == "run_manifest.json":
            continue
        d = json.loads(f.read_text(encoding="utf-8-sig"))
        if d.get("experiment") == 11:
            runs += d["runs"]
    learned = [r for r in runs if not r["reference_only"]]
    out = {"n_runs": len(runs), "n_learned": len(learned), "issues": []}
    # 1. integrality: accuracies must be exact multiples of 1/(histories*slots) etc.
    bad = 0
    for r in runs:
        for dl, e in r["eval"].items():
            n, vc = e["histories"], e["varied_count"]
            for val, den in ((e["per_slot"], n * 4), (e["whole"], n)):
                if abs(val * den - round(val * den)) > 1e-4:
                    bad += 1
            if e["whole_varied"] is not None and abs(e["whole_varied"] * vc - round(e["whole_varied"] * vc)) > 1e-4:
                bad += 1
    out["non_integral_accuracy_values"] = bad
    # 2. >=70% per-slot @64: two different definitions
    chk, fin = [], []
    for r in learned:
        c = any(x["per_slot"] >= .7 for x in r["checkpoints"])
        f = r["eval"]["64"]["per_slot"] >= .7
        (chk if c else []).append((r["variant"], r["seed"]))
        (fin if f else []).append((r["variant"], r["seed"]))
    out["per_slot_ge70_checkpoint_definition"] = {"count": len(chk), "runs": chk}
    out["per_slot_ge70_final_eval_definition"] = {"count": len(fin), "runs": fin}
    out["discordant"] = sorted(set(fin) ^ set(chk))
    out["discordant_detail"] = {f"{v}:{s}": {"checkpoint_max": max(x["per_slot"] for x in next(r for r in learned if (r["variant"], r["seed"]) == (v, s))["checkpoints"]),
                                              "final_eval": next(r for r in learned if (r["variant"], r["seed"]) == (v, s))["eval"]["64"]["per_slot"]}
                                for v, s in out["discordant"]}
    out["solved_ge90_whole_varied_64"] = [(r["variant"], r["seed"]) for r in learned if (r["eval"]["64"]["whole_varied"] or 0) >= .9]
    # 3. recompute mean tables
    out["means_whole_varied_64"] = {v: mean(r["eval"]["64"]["whole_varied"] for r in learned if r["variant"] == v) for v in ORDER}
    # 4. independent guess: empirical vs theoretical, regenerated
    emp = {}
    for dl in ("64", "128", "256", "512"):
        ws = [r["eval"][dl]["baselines"]["independent_guess"]["whole"] for r in learned if r["variant"] == "gru24"]
        ps = [r["eval"][dl]["baselines"]["independent_guess"]["per_slot"] for r in learned if r["variant"] == "gru24"]
        wv = [r["eval"][dl]["baselines"]["independent_guess"]["whole_varied"] for r in learned if r["variant"] == "gru24"]
        emp[dl] = {"whole_mean_over_3_eval_sets": mean(ws), "per_slot_mean": mean(ps), "whole_varied_mean": mean(wv), "whole_per_seed": ws}
    out["independent_guess_empirical"] = emp
    n = 256
    out["independent_guess_theory"] = {"per_slot": .5, "whole": 1 / 16, "whole_varied": 1 / 16,
                                       "note": "guesses are independent of labels, so P(all 4 right)=1/16 in ANY stratum, including varied-only",
                                       "binomial_se_single_eval_set_256_histories": math.sqrt(1 / 16 * 15 / 16 / n),
                                       "binomial_se_mean_of_3_sets": math.sqrt(1 / 16 * 15 / 16 / n / 3)}
    out["independent_guess_reported_6_9_is_whole_at_64_mean_of_3_sets"] = emp["64"]["whole_mean_over_3_eval_sets"]
    # regeneration check: baselines recomputed from scratch match archived values
    regen_ok = True
    for r in learned:
        if r["variant"] != "gru24":
            continue
        for dl in ("64", "512"):
            x = c10.generator_batch(4, 2, int(dl), 256, seed=eval_seed(r["seed"], int(dl)))
            y = c10.replay(x, 4, 2)
            b = baselines(x, y, eval_seed(r["seed"], int(dl)))
            regen_ok &= b["independent_guess"]["whole"] == r["eval"][dl]["baselines"]["independent_guess"]["whole"]
            regen_ok &= b["last_write_copy"]["per_slot"] == r["eval"][dl]["baselines"]["last_write_copy"]["per_slot"]
    out["baselines_regenerated_identical"] = bool(regen_ok)
    # 5. coupling facts
    out["coupling"] = {
        "model_init_seed": "build(name,4,2,seed): config.seed -> torch.manual_seed inside fork_rng (== run seed)",
        "training_data_seed": "training_seed(seed,step)=seed*1_000_003+step*8191+4*197+2 (== run seed)",
        "evaluation_seed": "eval_seed(seed,delay)=11_000_000+seed*100_003+delay (== run seed; checkpoint stream +1)",
        "consequence": "In Exp 011 all three were the SAME number per run, so 'seed 43' confounds initialization, training stream and the evaluation histories.",
        "eval_sets_differ_by_seed": True,
    }
    # 6. stream identity
    out["stream_hashes_per_seed_unique"] = {s: len({r["training_stream_sha256"] for r in learned if r["seed"] == s}) for s in (17, 29, 43)}
    # 7. text claims check
    by = {(r["variant"], r["seed"]): r for r in learned}
    out["protected_vs_gru24_whole_varied_64"] = {s: (by[("protected", s)]["eval"]["64"]["whole_varied"], by[("gru24", s)]["eval"]["64"]["whole_varied"]) for s in (17, 29, 43)}
    return out


def main(argv=None):
    a = argv or sys.argv[1:]
    res = audit(Path(a[0]))
    Path(a[1]).write_text(json.dumps(res, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({k: res[k] for k in ("non_integral_accuracy_values", "baselines_regenerated_identical", "discordant", "solved_ge90_whole_varied_64")}, indent=1))
    print("checkpoint-def >=70%:", res["per_slot_ge70_checkpoint_definition"]["count"], " final-eval-def >=70%:", res["per_slot_ge70_final_eval_definition"]["count"])
    print("independent guess whole@64 mean:", res["independent_guess_reported_6_9_is_whole_at_64_mean_of_3_sets"])


if __name__ == "__main__":
    main()
