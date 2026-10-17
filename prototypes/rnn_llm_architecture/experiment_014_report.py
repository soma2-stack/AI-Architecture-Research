"""Experiment 014 analysis: applies the decision criteria preregistered in EXPERIMENT_014_PLAN.md mechanically to raw JSON.

Reads raw per-model JSON; never rewrites it. Produces tables.md, summary.json and figures.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean

from .intervene_014 import DELAYS, MODELS, N_BASES

ORDER = list(MODELS)
SETS = ("both", "l0", "l1")
MIN_ELIGIBLE = 50
CATS = {"protected": "protected coefficients carry usable memory (localized)",
        "outside": "memory primarily outside the protected subspace",
        "distributed": "distributed / ambiguous",
        "insufficient": "evidence insufficient to localize",
        "few": "insufficient eligible pairs"}


def load(directory: Path) -> dict:
    out = {}
    for f in sorted(directory.glob("*.json")):
        if f.name in ("summary.json", "run_manifest.json", "sham_check.json") or "repro" in f.name:
            continue
        d = json.loads(f.read_text(encoding="utf-8-sig"))
        if d.get("experiment") == 14 and d.get("stage") == "intervene":
            out[d["result"]["model"]] = d["result"]
    return out


def rates(res: dict, delay: str, mode: str, ls: str, tag: str = "eligible") -> dict:
    v = res["interventions"][delay][mode]["variants"]
    prot = res["protected_family"]
    sub = v[f"{'prot' if prot else 'walsh8'}_{ls}"][tag]
    comp = v[f"{'fast' if prot else 'walsh_comp24'}_{ls}"][tag]
    noise = v[f"noise_{'prot' if prot else 'walsh8'}_{ls}"][tag]
    r8 = [v[f"rand8_b{i}_{ls}"][tag]["switch_to_donor"] for i in range(N_BASES)]
    r24 = [v[f"rand24_b{i}_{ls}"][tag]["switch_to_donor"] for i in range(N_BASES)]
    g = lambda row, k: row.get(k)
    return {"n": sub["n"], "frac": sub["fraction_of_pairs"],
            "S_sub": g(sub, "switch_to_donor"), "I_sub": g(sub, "unchanged_slots_agree_with_original"), "sub_ci": g(sub, "switch_ci95"),
            "S_comp": g(comp, "switch_to_donor"), "I_comp": g(comp, "unchanged_slots_agree_with_original"), "comp_ci": g(comp, "switch_ci95"),
            "S_noise": g(noise, "switch_to_donor"),
            "R8": [min(r8), mean(r8), max(r8)], "R24": [min(r24), mean(r24), max(r24)],
            "S_full": v[f"full_{ls}"][tag].get("switch_to_donor"), "I_full": v[f"full_{ls}"][tag].get("unchanged_slots_agree_with_original")}


def classify(r: dict) -> tuple[str, dict]:
    """Preregistered rules. Precedence note: a transplant that meets its switch/selectivity thresholds but violates the integrity
    bound is treated as 'insufficient' (checked before the 'distributed' clauses, which otherwise overlap with it)."""
    if r["n"] < MIN_ELIGIBLE:
        return "few", {}
    Sp, Sf, R8, R24, Ip, If = r["S_sub"], r["S_comp"], r["R8"][2], r["R24"][2], r["I_sub"], r["I_comp"]
    p_switch = Sp >= .80 and Sp - R8 >= .30
    f_switch = Sf >= .80 and Sf - R24 >= .30
    psuff, fsuff = p_switch and Ip >= .90, f_switch and If >= .90
    flags = {"P_sufficient": psuff, "F_sufficient": fsuff, "P_integrity_violation": p_switch and Ip < .90,
             "F_integrity_violation": f_switch and If < .90}
    if psuff and Sf <= .30:
        return "protected", flags
    if fsuff and Sp <= .30:
        return "outside", flags
    if not psuff and not fsuff and (flags["P_integrity_violation"] or flags["F_integrity_violation"]):
        return "insufficient", {**flags, "tie_break_applied": Sp >= .30 or Sf >= .30}
    if (psuff and fsuff) or (psuff and .30 < Sf < .80) or (fsuff and .30 < Sp < .80) or (not psuff and not fsuff and (Sp >= .30 or Sf >= .30)):
        return "distributed", flags
    return "insufficient", flags


def phase5_category(p: dict, layer: int) -> dict:
    mem = p["memory_displacement_ratio"][layer][-1]
    gen = p["random_full_space_displacement_ratio"][layer][-1]
    sub = p["random_in_designated_subspace_displacement_ratio"][layer][-1]
    sep = p["memory_separation_at_end_over_natural_spread"][layer]
    contraction = gen < .10
    preserved = mem >= .25 and mem >= 10 * max(gen, 1e-12) and sep >= .10
    ip = p["interpolation"]
    near = ip["0.25"]["fraction_near_an_endpoint(|tau| or |tau-1| < 0.15)"] >= .6 and ip["0.75"]["fraction_near_an_endpoint(|tau| or |tau-1| < 0.15)"] >= .6
    basin = preserved and near and ip["0.25"]["tau_median"] < .5 < ip["0.75"]["tau_median"]
    continuum = preserved and all(abs(ip[str(a)]["tau_median"] - a) <= .15 for a in (0.25, 0.5, 0.75))
    label = "collapsing (separation not preserved)" if not preserved else "basin-like" if basin else "continuum / line-attractor-like" if continuum else "ambiguous"
    return {"memory_ratio_end": mem, "random_full_ratio_end": gen, "random_subspace_ratio_end": sub, "sep_over_spread": sep,
            "generic_contraction": contraction, "separation_preserved": preserved, "label": label,
            "sub_criteria": {"memory_ratio>=0.25": mem >= .25, "memory>=10x_random_full": mem >= 10 * max(gen, 1e-12), "separation/spread>=0.10": sep >= .10},
            "selectivity_factor_over_random_full": mem / max(gen, 1e-12),
            "frac_predicting_B": [ip[str(a)]["fraction_predicting_B_value"] for a in (0.25, 0.5, 0.75)],
            "tau_medians": [ip[str(a)]["tau_median"] for a in (0.25, 0.5, 0.75)],
            "frac_near_endpoint": [ip[str(a)]["fraction_near_an_endpoint(|tau| or |tau-1| < 0.15)"] for a in (0.25, 0.5, 0.75)]}


def analyze(models: dict) -> dict:
    out = {"models": {}}
    for m in ORDER:
        if m not in models:
            continue
        res = models[m]
        info = {"role": res["spec"]["role"], "protected_family": res["protected_family"], "archive_identical": res["archive_verification"]["all_identical"],
                "stepper_gap": res["stepper_verification"], "sham_gap": max(res["interventions"][d][c]["sham_max_abs_logit_diff"] for d in res["interventions"] for c in res["interventions"][d]),
                "pairs_valid": all(all(v for k, v in pv.items() if isinstance(v, bool)) for pv in res["pair_validation"].values()),
                "eligible_fraction": {d: res["interventions"][d]["late"]["fraction_eligible"] for d in res["interventions"]},
                "original_changed_slot_accuracy": {d: res["interventions"][d]["late"]["original_changed_slot_accuracy"] for d in res["interventions"]},
                "late": {}, "early": {}, "all_pairs_late": {}, "category": {}, "category_early": {}, "strata": {}}
        for mode, key, ckey in (("late", "late", "category"), ("early", "early", "category_early")):
            for d in map(str, DELAYS):
                info[key][d] = {ls: rates(res, d, mode, ls) for ls in SETS}
                info[ckey][d] = {ls: classify(info[key][d][ls])[0] for ls in SETS}
        for d in map(str, DELAYS):
            info["all_pairs_late"][d] = {ls: rates(res, d, "late", ls, "all") for ls in SETS}
            v = res["interventions"][d]["late"]["variants"]
            pre = "prot" if res["protected_family"] else "walsh8"
            post = "fast" if res["protected_family"] else "walsh_comp24"
            info["strata"][d] = {name: {"initial_write": v[f"{name}_both"]["eligible_initial_write"], "rewritten": v[f"{name}_both"]["eligible_rewritten"]} for name in (pre, post, "full")}
        info["model_level"] = {}
        for ls in SETS:
            cats = {info["category"][d][ls] for d in map(str, DELAYS)}
            info["model_level"][ls] = next(iter(cats)) if len(cats) == 1 else "inconsistent across delays"
        info["tie_break_cells"] = [(d, ls) for d in map(str, DELAYS) for ls in SETS if classify(info["late"][d][ls])[1].get("tie_break_applied")]
        info["phase5"] = {d: {"layer0": phase5_category(res["phase5"][d], 0), "layer1": phase5_category(res["phase5"][d], 1)} for d in map(str, DELAYS)}
        info["phase5_raw_end"] = {d: {"interp_off_axis_0.5": res["phase5"][d]["interpolation"]["0.5"]["off_axis_distance_median"],
                                      "axis_len": res["phase5"][d]["final_state_axis_length_median"], "pairs": res["phase5"][d]["pairs_used"]} for d in map(str, DELAYS)}
        out["models"][m] = info
    return out


def pct(x, nd=0):
    return "n/a" if x is None else f"{100 * x:.{nd}f}%"


def md(out: dict) -> str:
    M = out["models"]
    L = ["# Experiment 014 — generated tables", "",
         "Late cut = state read at `max(write+1, T-8)`; early cut = right after the differing write. Eligible = changed-slot prediction correct on both original histories. "
         "Switch = changed-slot prediction after the transplant equals the donor's correct value. `prot`/`fast` = protected-subspace / fast-complement transplant "
         "(for the GRU: arbitrary Walsh-8 / its complement, **no protected role**). R8/R24 = random 8-d / 24-d controls (min–max over 8 bases).", "",
         "## Validity gates", "", "| model | archive reproduced exactly | stepper vs forward (max logit gap) | chunked vs uninterrupted | sham gap (max) | pairs valid |", "|---|---|---:|---:|---:|---|"]
    for m, i in M.items():
        s = i["stepper_gap"]
        L.append(f"| `{m}` | {i['archive_identical']} | {s['max_abs_logit_diff_stepper_vs_forward']:.1e} | {s['max_abs_logit_diff_chunked_vs_uninterrupted']:.1e} | {i['sham_gap']:.1e} | {i['pairs_valid']} |")
    L += ["", "Sham deviation: the preregistered bound was 1e-5; `sham_check.json` shows the sham equals a clean run on the same batch exactly (gap 0.0) with identical "
          "predictions, and the larger gap is float32 batch-size rounding against the split-batch reference.", "",
          "## Eligible fraction (changed slot correct on both original histories)", "", "| model | role | 64 | 128 | 256 | changed-slot accuracy @64 |", "|---|---|---:|---:|---:|---:|"]
    for m, i in M.items():
        L.append(f"| `{m}` | {i['role']} | {pct(i['eligible_fraction']['64'])} | {pct(i['eligible_fraction']['128'])} | {pct(i['eligible_fraction']['256'])} | {pct(i['original_changed_slot_accuracy']['64'])} |")
    for mode, title in (("late", "Late cut (primary)"), ("early", "Early cut (persistence)")):
        for ls, lname in (("both", "both layers"), ("l0", "layer 0 only"), ("l1", "layer 1 only")):
            L += ["", f"## {title}, {lname}: switch rate toward the donor's value (eligible pairs), unchanged-slot agreement in parentheses", "",
                  "| model | delay | n elig | full | prot / Walsh8 | fast / Walsh-comp24 | R8 min–max | R24 min–max | noise (norm-matched) | category |", "|---|---:|---:|---:|---|---|---|---|---:|---|"]
            for m, i in M.items():
                for d in map(str, DELAYS):
                    r = i[mode][d][ls]
                    cat = i["category" if mode == "late" else "category_early"][d][ls]
                    L.append(f"| `{m}` | {d} | {r['n']} | {pct(r['S_full'])} | {pct(r['S_sub'])} ({pct(r['I_sub'])}) | {pct(r['S_comp'])} ({pct(r['I_comp'])}) | "
                             f"{pct(r['R8'][0])}–{pct(r['R8'][2])} | {pct(r['R24'][0])}–{pct(r['R24'][2])} | {pct(r['S_noise'])} | {CATS[cat]} |")
    L += ["", "## Model-level category (late cut; same category required at all three delays)", "", "| model | both layers | layer 0 | layer 1 |", "|---|---|---|---|"]
    for m, i in M.items():
        ml = i["model_level"]
        f = lambda c: CATS.get(c, c)
        L.append(f"| `{m}` | {f(ml['both'])} | {f(ml['l0'])} | {f(ml['l1'])} |")
    tb = {m: i["tie_break_cells"] for m, i in M.items() if i["tie_break_cells"]}
    L += ["", f"Cells where the integrity-first tie-break of overlapping preregistered clauses changed the label: {tb or 'none'}.", "",
          "## All pairs (not only eligible), late cut, both layers — nothing hidden", "", "| model | delay | n | full | prot / Walsh8 | fast / Walsh-comp24 | R8 max | R24 max |", "|---|---:|---:|---:|---|---|---:|---:|"]
    for m, i in M.items():
        for d in map(str, DELAYS):
            r = i["all_pairs_late"][d]["both"]
            L.append(f"| `{m}` | {d} | {r['n']} | {pct(r['S_full'])} | {pct(r['S_sub'])} ({pct(r['I_sub'])}) | {pct(r['S_comp'])} ({pct(r['I_comp'])}) | {pct(r['R8'][2])} | {pct(r['R24'][2])} |")
    L += ["", "## Strata (late cut, both layers, eligible): changed write in the initial prefix vs rewritten — switch rate (n)", "", "| model | delay | prot initial | prot rewritten | fast initial | fast rewritten |", "|---|---:|---|---|---|---|"]
    for m, i in M.items():
        for d in map(str, DELAYS):
            st = i["strata"][d]
            keys = list(st)
            a, b = st[keys[0]], st[keys[1]]
            fm = lambda x: f"{pct(x['switch_to_donor'])} ({x['n']})"
            L.append(f"| `{m}` | {d} | {fm(a['initial_write'])} | {fm(a['rewritten'])} | {fm(b['initial_write'])} | {fm(b['rewritten'])} |")
    L += ["", "## Phase 5: perturbation stability versus memory separation (initial-prefix pairs; ratio = displacement at end / initial displacement, median)", "",
          "| model | delay | layer | memory ratio | random full-space ratio | random in-subspace ratio | memory ÷ random-full | separation / natural spread | sub-criteria met (≥.25 / ≥10× / ≥.10) | τ median α=.25/.5/.75 | P(predict B) α=.25/.5/.75 | near-endpoint fraction | preregistered label |", "|---|---:|---|---:|---:|---:|---:|---:|---|---|---|---|---|"]
    for m, i in M.items():
        for d in map(str, DELAYS):
            for ly in ("layer0", "layer1"):
                p = i["phase5"][d][ly]
                sc = "/".join("Y" if v else "n" for v in p["sub_criteria"].values())
                L.append(f"| `{m}` | {d} | {ly[-1]} | {p['memory_ratio_end']:.3g} | {p['random_full_ratio_end']:.3g} | {p['random_subspace_ratio_end']:.3g} | {p['selectivity_factor_over_random_full']:.1f}x | {p['sep_over_spread']:.3g} | {sc} | "
                         + "/".join(f"{x:.2f}" for x in p["tau_medians"]) + " | " + "/".join(f"{x:.2f}" for x in p["frac_predicting_B"]) + " | " + "/".join(f"{x:.2f}" for x in p["frac_near_endpoint"]) + f" | {p['label']} |")
    return "\n".join(L) + "\n"


def figures(models: dict, out: dict, directory: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    directory.mkdir(parents=True, exist_ok=True)
    names = [m for m in ORDER if m in models]
    for delay in ("64", "256"):
        fig, axes = plt.subplots(1, len(names), figsize=(2.4 * len(names), 3.6), sharey=True)
        for ax, m in zip(axes, names):
            r = out["models"][m]["late"][delay]["both"]
            pr = out["models"][m]["protected_family"]
            labels = ["full", "prot" if pr else "Walsh8", "fast" if pr else "Wcomp", "R8 max", "R24 max", "noise"]
            vals = [r["S_full"], r["S_sub"], r["S_comp"], r["R8"][2], r["R24"][2], r["S_noise"]]
            cols = ["#555555", "#1a7f37", "#1f4fd8", "#d98200", "#d98200", "#999999"]
            ax.bar(range(len(vals)), [v if v is not None else 0 for v in vals], color=cols)
            ax.set_xticks(range(len(vals)))
            ax.set_xticklabels(labels, rotation=60, fontsize=7)
            ax.set_title(f"{m.replace('_success', ' OK').replace('_partial', ' part').replace('_failed', ' fail')}\nn={r['n']}", fontsize=7)
            ax.set_ylim(0, 1.02)
        axes[0].set_ylabel("switch to donor's value", fontsize=8)
        fig.suptitle(f"Late-cut transplants, both layers, {delay} tokens (eligible pairs)", fontsize=9)
        fig.tight_layout()
        fig.savefig(directory / f"transplant_switch_{delay}.png", dpi=110)
        plt.close(fig)
    fig, axes = plt.subplots(2, len(names), figsize=(2.4 * len(names), 5), sharey="row")
    for j, m in enumerate(names):
        for row, ls in enumerate(("l0", "l1")):
            r = out["models"][m]["late"]["64"][ls]
            labels = ["prot/W8", "fast/Wc", "R8", "R24"]
            vals = [r["S_sub"], r["S_comp"], r["R8"][2], r["R24"][2]]
            axes[row][j].bar(range(4), [v or 0 for v in vals], color=["#1a7f37", "#1f4fd8", "#d98200", "#d98200"])
            axes[row][j].set_xticks(range(4))
            axes[row][j].set_xticklabels(labels, rotation=60, fontsize=7)
            axes[row][j].set_ylim(0, 1.02)
            if j == 0:
                axes[row][j].set_ylabel(f"layer {row}: switch", fontsize=8)
            if row == 0:
                axes[row][j].set_title(m.replace("_success", " OK").replace("_partial", " part").replace("_failed", " fail"), fontsize=7)
    fig.suptitle("Per-layer late-cut transplants at 64 tokens (eligible pairs)", fontsize=9)
    fig.tight_layout()
    fig.savefig(directory / "transplant_switch_per_layer_64.png", dpi=110)
    plt.close(fig)
    fig, axes = plt.subplots(2, len(names), figsize=(2.6 * len(names), 5), sharey=True)
    for j, m in enumerate(names):
        p = models[m]["phase5"]["256"]
        for ly in (0, 1):
            ax = axes[ly][j]
            t = p["relative_times"]
            ax.loglog([x + 1 for x in t], [max(v, 1e-6) for v in p["memory_displacement_ratio"][ly]], "-o", ms=3, color="#1a7f37", label="memory difference")
            ax.loglog([x + 1 for x in t[1:]], [max(v, 1e-6) for v in p["random_full_space_displacement_ratio"][ly][1:]], "-s", ms=3, color="#d98200", label="random, full space")
            ax.loglog([x + 1 for x in t[1:]], [max(v, 1e-6) for v in p["random_in_designated_subspace_displacement_ratio"][ly][1:]], "-^", ms=3, color="#888888", label="random, designated subspace")
            ax.set_xlabel("tokens after the write + 1", fontsize=7)
            ax.tick_params(labelsize=6)
            if ly == 0:
                ax.set_title(m.replace("_success", " OK").replace("_partial", " part").replace("_failed", " fail"), fontsize=7)
            if j == 0:
                ax.set_ylabel(f"layer {ly}: displacement / initial", fontsize=7)
    axes[0][0].legend(fontsize=5)
    fig.suptitle("Perturbation contraction vs memory-difference persistence (256-token histories, matched initial norm; random series start after the first token, when the perturbation enters)", fontsize=8)
    fig.tight_layout()
    fig.savefig(directory / "stability_vs_memory_separation_256.png", dpi=110)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 4))
    for m in names:
        ip = models[m]["phase5"]["256"]["interpolation"]
        ax.plot([0, .25, .5, .75, 1], [0] + [ip[str(a)]["tau_median"] for a in (0.25, 0.5, 0.75)] + [1], "-o", ms=3, label=m)
    ax.plot([0, 1], [0, 1], "k--", lw=.7, label="continuum (τ = α)")
    ax.set_xlabel("mixing α between the two memory states at the cut", fontsize=8)
    ax.set_ylabel("median τ of final state on the A→B axis", fontsize=8)
    ax.legend(fontsize=5)
    fig.tight_layout()
    fig.savefig(directory / "mixture_test_256.png", dpi=110)
    plt.close(fig)


def main(argv=None):
    a = argv or sys.argv[1:]
    d = Path(a[0])
    raw = d / "raw"
    models = load(raw)
    out = analyze(models)
    (d / "tables.md").write_text(md(out), encoding="utf-8", newline="\n")
    (d / "summary.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8", newline="\n")
    try:
        figures(models, out, d / "figures")
    except ImportError:
        print("matplotlib unavailable; figures skipped")
    print(md(out))


if __name__ == "__main__":
    main()
