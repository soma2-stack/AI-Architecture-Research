"""Experiment 015 analysis: applies the criteria preregistered in EXPERIMENT_015_PLAN.md mechanically to raw JSON."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from .necessity_015 import DELAYS, MODELS, TIMINGS

PRIMARY = ("prot_success_43_29", "prot_success_43_43")
MIN_ELIG = 50
NB = 8


def load(raw: Path) -> dict:
    out = {}
    for f in sorted(raw.glob("*.json")):
        if f.name == "run_manifest.json":
            continue
        d = json.loads(f.read_text(encoding="utf-8-sig"))
        if d.get("experiment") == 15:
            out[d["result"]["model"]] = d["result"]
    return out


def g(v, name, key="target_acc", tag="eligible"):
    return v[name][tag].get(key)


def cell(v: dict, timing: str) -> dict:
    n = v["S_mean"]["eligible"]["n"]
    A_S = g(v, "S_mean")
    r8 = [g(v, f"R8_mean_b{i}") for i in range(NB)]
    r8n = [g(v, f"R8_normrand_b{i}") for i in range(NB)]
    A_C = g(v, "C_mean")
    A_rS = g(v, "S_mean_rescue_S") if "S_mean_rescue_S" in v else None
    A_same = g(v, "S_unrelated_same")
    D_diff = g(v, "S_unrelated_diff", "donor_value_rate")
    worst_r8 = min(range(NB), key=lambda i: r8[i])
    nn_S = v["S_mean"]["eligible"] and v["S_mean"].get("off_distribution_nn_ratio")
    nn_R = v[f"R8_mean_b{worst_r8}"].get("off_distribution_nn_ratio")
    c = {"n_eligible": n, "A_S": A_S, "A_S_zero": g(v, "S_zero"), "minR8": min(r8), "meanR8": sum(r8) / NB, "minR8n": min(r8n), "A_C": A_C,
         "A_rescue_S": A_rS, "A_rescue_C_only": g(v, "S_mean_rescue_C") if "S_mean_rescue_C" in v else None,
         "A_same": A_same, "D_diff": D_diff, "D_twin": g(v, "S_twin", "donor_value_rate"),
         "C_twin_donor": g(v, "C_twin", "donor_value_rate"), "C_unrel_diff_donor": g(v, "C_unrelated_diff", "donor_value_rate"),
         "A_full_mean": g(v, "full_mean"), "A_fullspace_normrand": g(v, "fullspace_normrand"), "minR24": min(g(v, f"R24_mean_b{i}") for i in range(NB)),
         "other_acc_after_S_mean": g(v, "S_mean", "other_acc"), "other_acc_after_R8_mean_mean": sum(g(v, f"R8_mean_b{i}", "other_acc") for i in range(NB)) / NB,
         "nn_ratio_S_mean": nn_S, "nn_ratio_worst_R8": nn_R, "nn_ratio_S_unrelated_same": v["S_unrelated_same"].get("off_distribution_nn_ratio"),
         "nn_ratio_S_twin": v["S_twin"].get("off_distribution_nn_ratio"), "sham_gap": v["sham"].get("sham_max_abs_logit_gap"),
         "A_original_all": g(v, "sham", tag="all"), "A_S_all": g(v, "S_mean", tag="all")}
    if n < MIN_ELIG:
        c.update(verdict="too few eligible", N={})
        return c
    N = {"N1_destroy": A_S <= .65, "N2_selective": A_S <= min(r8) - .30 and A_S <= min(r8n) - .30, "N3_complement_dispensable": A_C >= .90,
         "N4_rescue": None if A_rS is None else A_rS >= .90, "N5_natural": A_same >= .90 and D_diff >= .80}
    supported = N["N1_destroy"] and N["N2_selective"] and N["N5_natural"] and (N["N4_rescue"] in (None, True))
    c["N"] = N
    c["off_distribution_flag"] = (nn_S or 0) > 2 * (nn_R or 1e9)
    c["verdict"] = "supported" if supported else "contradicted" if A_S >= .90 else "inconclusive"
    return c


def analyze(models: dict) -> dict:
    out = {"models": {}}
    for m in MODELS:
        if m not in models:
            continue
        r = models[m]
        cells = {d: {t: cell(r["delays"][d]["timings"][t]["variants"], t) for t in TIMINGS} for d in map(str, DELAYS)}
        verdicts = [c["verdict"] for dd in cells.values() for c in dd.values() if c["verdict"] != "too few eligible"]
        mv = "supported" if verdicts and all(v == "supported" for v in verdicts) else "contradicted" if verdicts and all(v == "contradicted" for v in verdicts) else "inconclusive" if verdicts else "too few eligible"
        val = {"archive_identical": r["archive_verification"]["all_identical"],
               "stepper_vs_014_max_gap": max(r["delays"][d]["stepper_vs_014_stepper_max_logit_gap"] for d in r["delays"]),
               "sham_max_gap": max(c["sham_gap"] for dd in cells.values() for c in dd.values()),
               "pairs_valid": all(all(v for v in pv.values() if isinstance(v, bool)) for pv in (r["delays"][d]["pair_validation"] for d in r["delays"]))}
        out["models"][m] = {"role": r["spec"]["role"], "protected_family": r["protected_family"], "validity": val, "cells": cells, "model_verdict": mv,
                            "verdict_counts": {k: verdicts.count(k) for k in ("supported", "contradicted", "inconclusive")},
                            "original": {d: r["delays"][d]["original"] for d in r["delays"]}}
    M = out["models"]
    pv = [M[p]["model_verdict"] for p in PRIMARY if p in M]
    allcells = lambda p: [c for dd in M[p]["cells"].values() for c in dd.values() if c["verdict"] != "too few eligible"]
    q = {}
    q["Q1_removal_selectively_destroys_recall"] = "supported" if pv and all(v == "supported" for v in pv) else "contradicted" if "contradicted" in pv else "inconclusive"
    q["Q2_rescue_recovers"] = "supported" if all(c["N"]["N4_rescue"] in (None, True) for p in PRIMARY for c in allcells(p)) else (
        "contradicted" if all(c["N"]["N4_rescue"] in (None, False) for p in PRIMARY for c in allcells(p)) else "inconclusive")
    q["Q3_exceeds_matched_random"] = "supported" if all(c["N"]["N2_selective"] for p in PRIMARY for c in allcells(p)) else (
        "contradicted" if not any(c["N"]["N2_selective"] for p in PRIMARY for c in allcells(p)) else "inconclusive")
    q["Q4_more_than_one_network"] = q["Q1_removal_selectively_destroys_recall"]
    fx = M.get("fixed005_success_43_43", {}).get("model_verdict")
    q["Q5_fixed_gate_counterexample_to_architectural_necessity"] = "supported" if fx == "contradicted" else "inconclusive" if fx == "inconclusive" else "contradicted"
    out["questions"] = q
    return out


def pct(x):
    return "—" if x is None else f"{100 * x:.0f}%"


def md(out: dict) -> str:
    M = out["models"]
    L = ["# Experiment 015 — generated tables", "",
         "Layer-1 edits; eligible recipients (original target prediction correct; twin donors: both twins correct). Target accuracy = target slot correct "
         "for the recipient's own history. `S` = designated 8-d subspace (GRU: arbitrary Walsh-8, no protected role), `C` = its 24-d complement.", "",
         "## Validity", "", "| model | archive exact | stepper = Exp 014 stepper (max gap) | sham gap (same batch) | pairs valid |", "|---|---|---:|---:|---|"]
    for m, i in M.items():
        v = i["validity"]
        L.append(f"| `{m}` | {v['archive_identical']} | {v['stepper_vs_014_max_gap']:.1e} | {v['sham_max_gap']:.1e} | {v['pairs_valid']} |")
    L += ["", "## Verdicts", "", "| model | role | model verdict | cells supported / contradicted / inconclusive |", "|---|---|---|---|"]
    for m, i in M.items():
        k = i["verdict_counts"]
        L.append(f"| `{m}` | {i['role']} | **{i['model_verdict']}** | {k['supported']} / {k['contradicted']} / {k['inconclusive']} |")
    L += ["", "## Answers to the preregistered questions", ""] + [f"- {k}: **{v}**" for k, v in out["questions"].items()]
    L += ["", "## Every cell (eligible recipients)", "",
          "| model | delay | timing | n | original (all) | S mean | S zero | min R8 mean | min R8 norm-matched | C mean | rescue S | rescue C only | unrel. same: acc | unrel. diff: donor | twin→S donor | twin→C donor | full mean | NN ratio S / worst R8 | N1 N2 N4 N5 (N3) | verdict |",
          "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|"]
    for m, i in M.items():
        for d in map(str, DELAYS):
            for t in TIMINGS:
                c = i["cells"][d][t]
                N = c.get("N", {})
                flags = " ".join({True: "Y", False: "n", None: "–"}[N.get(k)] for k in ("N1_destroy", "N2_selective", "N4_rescue", "N5_natural")) + f" ({ {True: 'Y', False: 'n', None: '–'}[N.get('N3_complement_dispensable')]})" if N else "—"
                nn = f"{c['nn_ratio_S_mean']:.2f} / {c['nn_ratio_worst_R8']:.2f}" if c["nn_ratio_S_mean"] is not None else "—"
                L.append(f"| `{m}` | {d} | {t} | {c['n_eligible']} | {pct(c['A_original_all'])} | {pct(c['A_S'])} | {pct(c['A_S_zero'])} | {pct(c['minR8'])} | {pct(c['minR8n'])} | {pct(c['A_C'])} | "
                         f"{pct(c['A_rescue_S'])} | {pct(c['A_rescue_C_only'])} | {pct(c['A_same'])} | {pct(c['D_diff'])} | {pct(c['D_twin'])} | {pct(c['C_twin_donor'])} | {pct(c['A_full_mean'])} | {nn} | {flags} | {c['verdict']} |")
    return "\n".join(L) + "\n"


def figures(out: dict, directory: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    directory.mkdir(parents=True, exist_ok=True)
    M = out["models"]
    names = list(M)
    for t in TIMINGS:
        fig, axes = plt.subplots(1, len(names), figsize=(2.5 * len(names), 3.8), sharey=True)
        for ax, m in zip(axes, names):
            c = M[m]["cells"]["128"][t]
            labels = ["orig (all)", "S mean", "S zero", "R8 min", "R8n min", "C mean", "rescue S", "unrel same", "full mean"]
            vals = [c["A_original_all"], c["A_S"], c["A_S_zero"], c["minR8"], c["minR8n"], c["A_C"], c["A_rescue_S"], c["A_same"], c["A_full_mean"]]
            cols = ["#555555", "#b00020", "#e06070", "#d98200", "#f0b060", "#1f4fd8", "#1a7f37", "#7fbf7f", "#999999"]
            ax.bar(range(len(vals)), [v if v is not None else 0 for v in vals], color=cols)
            ax.axhline(.5, color="#aaaaaa", lw=.6, ls="--")
            ax.set_xticks(range(len(vals)))
            ax.set_xticklabels(labels, rotation=70, fontsize=6)
            ax.set_ylim(0, 1.02)
            ax.set_title(f"{m}\n{M[m]['model_verdict']}", fontsize=6)
        axes[0].set_ylabel("target-slot accuracy (eligible)", fontsize=8)
        fig.suptitle(f"Layer-1 removals, 128 tokens, timing = {t} (dashed = chance)", fontsize=9)
        fig.tight_layout()
        fig.savefig(directory / f"removal_{t}_128.png", dpi=110)
        plt.close(fig)


def main(argv=None):
    a = argv or sys.argv[1:]
    d = Path(a[0])
    out = analyze(load(d / "raw"))
    (d / "tables.md").write_text(md(out), encoding="utf-8", newline="\n")
    (d / "summary.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8", newline="\n")
    try:
        figures(out, d / "figures")
    except ImportError:
        print("matplotlib unavailable")
    print(md(out))


if __name__ == "__main__":
    main()
