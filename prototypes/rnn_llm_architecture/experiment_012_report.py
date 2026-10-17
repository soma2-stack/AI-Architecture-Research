"""Experiment 012 analysis exactly as preregistered in EXPERIMENT_012_PLAN.md: matrices, axis summaries, variance partition,
consistency counts, seed-43 and retention comparisons, collapse/age diagnostics, Exp 011 comparison, learning curves.
Descriptive only; reads raw shard JSON, never rewrites it."""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path
from statistics import mean

from .capacity_012 import ARCHS, SEEDS, SUCCESS_WHOLE_VARIED, learning_onset

DELAYS = ("64", "128", "256", "512")
CLASSES = ("plateau_only", "partial", "success")
RANK = {c: i for i, c in enumerate(CLASSES)}


def load_runs(directory: Path):
    runs, skipped = [], []
    for f in sorted(directory.glob("*.json")):
        if f.name in ("summary.json", "run_manifest.json"):
            continue
        d = json.loads(f.read_text(encoding="utf-8-sig"))
        if d.get("experiment") != 12:
            continue
        runs += d["runs"]
        skipped += d.get("skipped", [])
    return runs, skipped


def pct(x, nd=1):
    return "n/a" if x is None else f"{100 * x:.{nd}f}%"


def final_loss(r):
    w = r["loss_windows"]
    return mean(x["mean_loss"] for x in w[-5:]) if w else None


def wv(r, d="64"):
    return r.get("eval", {}).get(d, {}).get("whole_varied")


def grid(by, arch, fn):
    return {(i, d): fn(by[(arch, i, d)]) if (arch, i, d) in by else None for i in SEEDS for d in SEEDS}


def partition(cells: dict):
    """3x3 sums of squares: init main, data main, remainder (interaction + noise; inseparable with n=1/cell)."""
    vals = [v for v in cells.values() if v is not None]
    if len(vals) != 9:
        return None
    gm = mean(vals)
    total = sum((v - gm) ** 2 for v in vals)
    s_i = 3 * sum((mean(cells[(i, d)] for d in SEEDS) - gm) ** 2 for i in SEEDS)
    s_d = 3 * sum((mean(cells[(i, d)] for i in SEEDS) - gm) ** 2 for d in SEEDS)
    return {"total": total, "init": s_i, "data": s_d, "remainder": max(total - s_i - s_d, 0.0)}


def verdict(init_share, data_share):
    if init_share >= .30 and init_share >= 2 * data_share:
        return "initialization favoured"
    if data_share >= .30 and data_share >= 2 * init_share:
        return "training data favoured"
    return "neither factor consistent / unexplained"


def shares(p):
    return None if p is None else ({k: p[k] / p["total"] for k in ("init", "data", "remainder")} if p["total"] else {"init": 0.0, "data": 0.0, "remainder": 0.0})


def pooled(parts):
    parts = [p for p in parts if p]
    tot = sum(p["total"] for p in parts)
    if tot == 0:    # every cell identical: no variance to attribute
        return {"init": 0.0, "data": 0.0, "remainder": 0.0}
    return {k: sum(p[k] for p in parts) / tot for k in ("init", "data", "remainder")}


def permutation_reference(cells_by_arch: dict, n=5000, seed=12):
    """Orientation only: relabel the 9 cells within each architecture at random; return fractions of draws whose pooled init
    (resp. data) share is at least the observed one."""
    rng = random.Random(seed)
    keys = [(i, d) for i in SEEDS for d in SEEDS]
    obs = pooled([partition(c) for c in cells_by_arch.values()])
    ge_i = ge_d = 0
    for _ in range(n):
        parts = []
        for c in cells_by_arch.values():
            v = [c[k] for k in keys]
            rng.shuffle(v)
            parts.append(partition(dict(zip(keys, v))))
        p = pooled(parts)
        ge_i += p["init"] >= obs["init"] - 1e-12
        ge_d += p["data"] >= obs["data"] - 1e-12
    return {"draws": n, "frac_init_share_ge_observed": ge_i / n, "frac_data_share_ge_observed": ge_d / n}


def analyze(runs, skipped, exp11_dir: Path | None = None) -> dict:
    by = {(r["architecture"], r["init_seed"], r["data_seed"]): r for r in runs}
    out = {"n_runs": len(runs), "n_skipped": len(skipped), "incomplete": [k for k, r in by.items() if r["status"] != "complete"]}
    done = {k: r for k, r in by.items() if r["status"] == "complete" and "eval" in r}
    learned = lambda r: r["learning_onset_step"] is not None
    # per-architecture matrices and axis summaries
    out["arch"] = {}
    cells_wv, cells_loss = {}, {}
    for a in ARCHS:
        rs = {k: r for k, r in done.items() if k[0] == a}
        info = {"runs": len(rs)}
        wvg = grid(done, a, lambda r: wv(r))
        lg = grid(done, a, final_loss)
        info["whole_varied_64"] = {f"{i}:{d}": v for (i, d), v in wvg.items()}
        info["outcome"] = {f"{i}:{d}": done[(a, i, d)]["outcome"] if (a, i, d) in done else None for i in SEEDS for d in SEEDS}
        info["onset"] = {f"{i}:{d}": done[(a, i, d)]["learning_onset_step"] if (a, i, d) in done else None for i in SEEDS for d in SEEDS}
        info["final_loss"] = {f"{i}:{d}": v for (i, d), v in lg.items()}
        if len(rs) == 9:
            info["init_means_wv"] = {i: mean(wvg[(i, d)] for d in SEEDS) for i in SEEDS}
            info["data_means_wv"] = {d: mean(wvg[(i, d)] for i in SEEDS) for d in SEEDS}
            info["init_means_loss"] = {i: mean(lg[(i, d)] for d in SEEDS) for i in SEEDS}
            info["data_means_loss"] = {d: mean(lg[(i, d)] for i in SEEDS) for d in SEEDS}
            info["partition_wv"] = shares(partition(wvg))
            info["partition_loss"] = shares(partition(lg))
            L = {(i, d): learned(done[(a, i, d)]) for i in SEEDS for d in SEEDS}
            info["consistent_init_rows"] = sum(len({L[(i, d)] for d in SEEDS}) == 1 for i in SEEDS)
            info["consistent_data_columns"] = sum(len({L[(i, d)] for i in SEEDS}) == 1 for d in SEEDS)
            info["learned_cells"] = sum(L.values())
            info["success_cells"] = sum(done[k]["outcome"] == "success" for k in rs)
            cells_wv[a], cells_loss[a] = wvg, lg
        out["arch"][a] = info
    # pooled variance partition (within architecture) + between-architecture share
    if len(cells_wv) == 4:
        for name, cells in (("whole_varied_64", cells_wv), ("final_loss", cells_loss)):
            p = pooled([partition(c) for c in cells.values()])
            allv = [v for c in cells.values() for v in c.values()]
            gm = mean(allv)
            tot = sum((v - gm) ** 2 for v in allv)
            between = 9 * sum((mean(c.values()) - gm) ** 2 for c in cells.values())
            out[f"pooled_partition_{name}"] = {**p, "verdict": verdict(p["init"], p["data"]),
                                               "between_architecture_share_of_total": between / tot if tot else None,
                                               "permutation_reference": permutation_reference(cells)}
    # cross-architecture learned / success rates per seed, seed-43 question
    if len(done) == 36:
        out["rate_by_init_seed"] = {i: {"learned": sum(learned(done[k]) for k in done if k[1] == i), "success": sum(done[k]["outcome"] == "success" for k in done if k[1] == i), "n": 12} for i in SEEDS}
        out["rate_by_data_seed"] = {d: {"learned": sum(learned(done[k]) for k in done if k[2] == d), "success": sum(done[k]["outcome"] == "success" for k in done if k[2] == d), "n": 12} for d in SEEDS}
        out["seed43"] = {"init43_success": sum(done[k]["outcome"] == "success" for k in done if k[1] == 43), "init43_n": 12,
                         "data43_success": sum(done[k]["outcome"] == "success" for k in done if k[2] == 43), "data43_n": 12,
                         "both43_success": [k[0] for k in done if k[1] == 43 and k[2] == 43 and done[k]["outcome"] == "success"],
                         "init43_not_data43_success": sum(done[k]["outcome"] == "success" for k in done if k[1] == 43 and k[2] != 43),
                         "data43_not_init43_success": sum(done[k]["outcome"] == "success" for k in done if k[2] == 43 and k[1] != 43)}
        # retention pairing
        pairs = []
        for i in SEEDS:
            for d in SEEDS:
                p, n = done[("protected", i, d)], done[("protected_no_retain", i, d)]
                pairs.append({"init": i, "data": d, "protected": p["outcome"], "no_retain": n["outcome"],
                              "delta_rank": RANK[n["outcome"]] - RANK[p["outcome"]], "wv_protected": wv(p), "wv_no_retain": wv(n)})
        worse = sum(x["delta_rank"] < 0 for x in pairs)
        better = sum(x["delta_rank"] > 0 for x in pairs)
        out["retention"] = {"pairs": pairs, "no_retain_worse_cells": worse, "no_retain_better_cells": better,
                            "equal_cells": 9 - worse - better, "consistently_worse": bool(better == 0 and worse >= 5)}
    # reliability
    out["reliability"] = {}
    for a in ARCHS:
        rs = [r for k, r in done.items() if k[0] == a]
        if rs:
            ons = [r["learning_onset_step"] for r in rs if r["learning_onset_step"] is not None]
            out["reliability"][a] = {"runs": len(rs), "learned": len(ons), "success": sum(r["outcome"] == "success" for r in rs),
                                     "mean_whole_varied_64": mean(wv(r) for r in rs), "onset_min": min(ons) if ons else None,
                                     "onset_max": max(ons) if ons else None, "mean_final_loss": mean(final_loss(r) for r in rs),
                                     "parameters": rs[0]["parameters"], "mean_wall_s": mean(r["train_wall_s"] for r in rs)}
    # diagnostics pooled by outcome class at delay 64
    diag = {}
    for c in CLASSES:
        rs = [r for r in done.values() if r["outcome"] == c]
        if not rs:
            continue
        ev = [r["eval"]["64"] for r in rs]
        ages: dict[str, list[int]] = {}
        for e in ev:
            for k, v in e["by_last_write_age"].items():
                t = ages.setdefault(k, [0, 0])
                t[0] += v["n"]
                t[1] += v["correct"]
        diag[c] = {"runs": len(rs), "per_slot": mean(e["per_slot"] for e in ev),
                   "all_slots_same_prediction": mean(e["collapse"]["all_slots_same_prediction"] for e in ev),
                   "predicts_last_write_everywhere": mean(e["collapse"]["predicts_last_write_everywhere"] for e in ev),
                   "most_recent_slot_acc": sum(e["most_recently_written_slot"]["correct"] for e in ev) / sum(e["most_recently_written_slot"]["n"] for e in ev),
                   "other_slots_acc": sum(e["other_slots"]["correct"] for e in ev) / sum(e["other_slots"]["n"] for e in ev),
                   "by_age": {k: {"n": v[0], "acc": v[1] / v[0]} for k, v in sorted(ages.items(), key=lambda kv: (kv[0] != "initial_only", int(kv[0].split("-")[0].rstrip("+")) if kv[0] != "initial_only" else 0))},
                   "wv_by_delay": {d: mean(e2 for e2 in [r["eval"][d]["whole_varied"] for r in rs if r["eval"][d]["whole_varied"] is not None]) for d in DELAYS if d in rs[0]["eval"]}}
    out["diagnostics_by_outcome_class"] = diag
    if done:
        any_run = next(iter(done.values()))
        out["baselines"] = {d: {k: {m: any_run["eval"][d]["baselines"][k][m] for m in ("per_slot", "whole", "whole_varied")} for k in ("independent_guess", "last_write_copy")} |
                            {"analytic_independent_guess": {"per_slot": .5, "whole": .0625, "whole_varied": .0625}} for d in DELAYS if d in any_run["eval"]}
        out["same_eval_set_all_runs"] = len({json.dumps(r["eval"]["64"]["true_pattern_counts"]) for r in done.values()}) == 1
    # stream identity checks
    out["stream_hash_per_data_seed"] = {d: len({r["training_stream_sha256"] for r in runs if r["data_seed"] == d}) for d in SEEDS}
    out["init_fingerprint_per_arch_init"] = {f"{a}:{i}": len({r["init_fingerprint_sha256"] for r in runs if r["architecture"] == a and r["init_seed"] == i}) for a in ARCHS for i in SEEDS}
    # comparison with Experiment 011
    if exp11_dir is not None and exp11_dir.exists():
        cmp = []
        for f in sorted(exp11_dir.glob("*_*.json")):
            if f.name in ("run_manifest.json", "summary.json"):
                continue
            d11 = json.loads(f.read_text(encoding="utf-8-sig"))
            if d11.get("experiment") != 11:
                continue
            for r11 in d11["runs"]:
                if r11["reference_only"]:
                    continue
                r12 = done.get((r11["variant"], r11["seed"], r11["seed"]))
                if r12 is None:
                    continue
                n = min(len(r11["loss_windows"]), len(r12["loss_windows"]))
                cmp.append({"arch": r11["variant"], "seed": r11["seed"],
                            "loss_windows_identical": [x["mean_loss"] for x in r11["loss_windows"][:n]] == [x["mean_loss"] for x in r12["loss_windows"][:n]],
                            "stream_hash_identical": r11["training_stream_sha256"] == r12["training_stream_sha256"],
                            "wv64_exp011": r11["eval"]["64"]["whole_varied"], "wv64_exp012": wv(r12),
                            "outcome_exp011": ("plateau_only" if learning_onset(r11["loss_windows"]) is None else
                                               "success" if (r11["eval"]["64"]["whole_varied"] or 0) >= SUCCESS_WHOLE_VARIED else "partial"),
                            "outcome_exp012": r12["outcome"]})
        out["comparison_exp011_diagonal"] = cmp
    return out


def md(out: dict, runs: list[dict], skipped: list[dict]) -> str:
    L = [f"# Experiment 012 — generated tables", "",
         f"{out['n_runs']} runs recorded, {out['n_skipped']} skipped, incomplete: {out['incomplete'] or 'none'}. Rows = initialization seed, "
         "columns = training-data seed. `whole-varied@64` on the fixed evaluation set (512 histories). Outcome classes: P = plateau_only, "
         "Pa = partial, S = success. Descriptive only; 9 runs per architecture.", ""]
    abbr = {"plateau_only": "P", "partial": "Pa", "success": "S"}
    for a in ARCHS:
        info = out["arch"][a]
        L += [f"## {a} — 3 × 3 matrices", "", "Whole-varied@64 (outcome, onset step), row mean | column means below", "",
              "| init \\ data | " + " | ".join(str(d) for d in SEEDS) + " | row mean |", "|---|---|---|---|---:|"]
        for i in SEEDS:
            cells = []
            for d in SEEDS:
                k = f"{i}:{d}"
                v = info["whole_varied_64"][k]
                cells.append("n/a" if v is None else f"{pct(v)} ({abbr.get(info['outcome'][k], info['outcome'][k])}, {info['onset'][k] if info['onset'][k] is not None else '—'})")
            rm = info.get("init_means_wv", {}).get(i)
            L.append(f"| **{i}** | " + " | ".join(cells) + f" | {pct(rm)} |")
        L.append("| column mean | " + " | ".join(pct(info.get("data_means_wv", {}).get(d)) for d in SEEDS) + " | |")
        L += ["", "Final training loss (mean of last five 50-update windows)", "", "| init \\ data | " + " | ".join(str(d) for d in SEEDS) + " | row mean |", "|---|---|---|---|---:|"]
        for i in SEEDS:
            rm = info.get("init_means_loss", {}).get(i)
            L.append(f"| **{i}** | " + " | ".join("n/a" if info['final_loss'][f'{i}:{d}'] is None else f"{info['final_loss'][f'{i}:{d}']:.3f}" for d in SEEDS) + f" | {'n/a' if rm is None else f'{rm:.3f}'} |")
        L.append("| column mean | " + " | ".join("n/a" if info.get("data_means_loss", {}).get(d) is None else f"{info['data_means_loss'][d]:.3f}" for d in SEEDS) + " | |")
        if "partition_wv" in info and info["partition_wv"]:
            p, q = info["partition_wv"], info.get("partition_loss") or {}
            L += ["", f"Sum-of-squares shares (whole-varied): init {pct(p['init'], 0)}, data {pct(p['data'], 0)}, remainder (interaction + noise) {pct(p['remainder'], 0)}; "
                  f"(final loss): init {pct(q.get('init'), 0)}, data {pct(q.get('data'), 0)}, remainder {pct(q.get('remainder'), 0)}. "
                  f"Rows with identical learned/not-learned status across data seeds: {info['consistent_init_rows']}/3; columns: {info['consistent_data_columns']}/3. "
                  f"Learned cells {info['learned_cells']}/9, success cells {info['success_cells']}/9."]
        L.append("")
    if "pooled_partition_whole_varied_64" in out:
        L += ["## Pooled variance partition (within architecture)", "", "| outcome | init share | data share | remainder (interaction + noise) | between-architecture share of total | orientation rule |", "|---|---:|---:|---:|---:|---|"]
        for n in ("whole_varied_64", "final_loss"):
            p = out[f"pooled_partition_{n}"]
            L.append(f"| {n} | {pct(p['init'], 0)} | {pct(p['data'], 0)} | {pct(p['remainder'], 0)} | {pct(p['between_architecture_share_of_total'], 0)} | {p['verdict']} |")
        for n in ("whole_varied_64", "final_loss"):
            pr = out[f"pooled_partition_{n}"]["permutation_reference"]
            L.append(f"\nPermutation reference ({n}, orientation only, NOT a significance test): in {pr['draws']} random relabelings of the 9 cells per architecture, "
                     f"{pct(pr['frac_init_share_ge_observed'])} reach an init share ≥ observed and {pct(pr['frac_data_share_ge_observed'])} a data share ≥ observed.")
        L.append("")
    if "rate_by_init_seed" in out:
        L += ["## Per-axis summaries across all four architectures (12 runs per seed)", "", "| seed | learned as init seed | success as init seed | learned as data seed | success as data seed |", "|---:|---:|---:|---:|---:|"]
        for s in SEEDS:
            ri, rd = out["rate_by_init_seed"][s], out["rate_by_data_seed"][s]
            L.append(f"| {s} | {ri['learned']}/12 | {ri['success']}/12 | {rd['learned']}/12 | {rd['success']}/12 |")
        s43 = out["seed43"]
        L += ["", f"Seed 43: successes with init=43: {s43['init43_success']}/12 (of which with data≠43: {s43['init43_not_data43_success']}/8); with data=43: "
              f"{s43['data43_success']}/12 (of which with init≠43: {s43['data43_not_init43_success']}/8); diagonal (43,43) successes: {s43['both43_success'] or 'none'}.", ""]
        r = out["retention"]
        L += ["## Retention: `protected_no_retain` vs `protected`, paired by (init, data)", "", "| init | data | protected | no_retain | wv protected | wv no_retain |", "|---:|---:|---|---|---:|---:|"]
        L += [f"| {x['init']} | {x['data']} | {x['protected']} | {x['no_retain']} | {pct(x['wv_protected'])} | {pct(x['wv_no_retain'])} |" for x in r["pairs"]]
        L += ["", f"No-retain worse in {r['no_retain_worse_cells']}/9 cells, better in {r['no_retain_better_cells']}/9, equal class in {r['equal_cells']}/9 → "
              f"preregistered 'consistently worse' = **{r['consistently_worse']}**.", ""]
    L += ["## Reliability by architecture", "", "| architecture | params | runs | learned (onset) | success | mean whole-varied@64 | onset range | mean final loss | mean train s |", "|---|---:|---:|---:|---:|---:|---|---:|---:|"]
    for a, r in out["reliability"].items():
        onset_range = "—" if r["onset_min"] is None else str(r["onset_min"]) + "–" + str(r["onset_max"])
        L.append(f"| {a} | {r['parameters']} | {r['runs']} | {r['learned']}/{r['runs']} | {r['success']}/{r['runs']} | {pct(r['mean_whole_varied_64'])} | "
                 f"{onset_range} | {r['mean_final_loss']:.3f} | {r['mean_wall_s']:.0f} |")
    L += ["", "## Diagnostics at delay 64 pooled by outcome class", "", "| class | runs | per-slot | all-slots-same prediction | predicts last write everywhere | most-recent slot acc | other slots acc | whole-varied by delay (64/128/256/512) |", "|---|---:|---:|---:|---:|---:|---:|---|"]
    for c, d in out["diagnostics_by_outcome_class"].items():
        L.append(f"| {c} | {d['runs']} | {pct(d['per_slot'])} | {pct(d['all_slots_same_prediction'])} | {pct(d['predicts_last_write_everywhere'])} | {pct(d['most_recent_slot_acc'])} | {pct(d['other_slots_acc'])} | "
                 + " / ".join(pct(d['wv_by_delay'].get(x)) for x in DELAYS) + " |")
    ages = sorted({k for d in out["diagnostics_by_outcome_class"].values() for k in d["by_age"]}, key=lambda k: (k != "initial_only", 0 if k == "initial_only" else int(k.split("-")[0].rstrip("+"))))
    L += ["", "Per-slot accuracy by age of the slot's last write (queried slots pooled over runs; n in parentheses)", "", "| class | " + " | ".join(ages) + " |", "|---|" + "---:|" * len(ages)]
    for c, d in out["diagnostics_by_outcome_class"].items():
        L.append(f"| {c} | " + " | ".join(f"{pct(d['by_age'][k]['acc'])} ({d['by_age'][k]['n']})" if k in d["by_age"] else "—" for k in ages) + " |")
    if "baselines" in out:
        L += ["", "## Baselines on the fixed evaluation set (empirical; analytic shown separately)", "", "| delay | independent guess (per-slot / whole / whole-varied) | analytic guess | last-write copy |", "|---|---|---|---|"]
        for dly, b in out["baselines"].items():
            f = lambda x: " / ".join(pct(x[m]) for m in ("per_slot", "whole", "whole_varied"))
            L.append(f"| {dly} | {f(b['independent_guess'])} | {f(b['analytic_independent_guess'])} | {f(b['last_write_copy'])} |")
    L += ["", "## Stream / initialization identity checks", "", f"Distinct training-stream hashes per data seed (must be 1): {out['stream_hash_per_data_seed']}.",
          f"Distinct init fingerprints per (architecture, init seed) (must be 1): {set(out['init_fingerprint_per_arch_init'].values())}. Same evaluation set for all runs: {out.get('same_eval_set_all_runs')}.", ""]
    if out.get("comparison_exp011_diagonal"):
        L += ["## Diagonal cells vs Experiment 011 (same init and data seed)", "", "| architecture | seed | loss windows identical | stream identical | wv@64 Exp 011 (seed-specific eval) | wv@64 Exp 012 (fixed eval) | outcome 011 → 012 |", "|---|---:|---|---|---:|---:|---|"]
        L += [f"| {x['arch']} | {x['seed']} | {x['loss_windows_identical']} | {x['stream_hash_identical']} | {pct(x['wv64_exp011'])} | {pct(x['wv64_exp012'])} | {x['outcome_exp011']} → {x['outcome_exp012']} |" for x in out["comparison_exp011_diagonal"]]
    bad = [r for r in runs if r["status"] != "complete"]
    if bad or skipped:
        L += ["", "## Failures / incomplete", ""] + [f"- {r['architecture']} init {r['init_seed']} data {r['data_seed']}: {r['status']} after {r['steps']} updates" for r in bad] + [f"- skipped: {s}" for s in skipped]
    return "\n".join(L) + "\n"


def figures(runs: list[dict], directory: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    directory.mkdir(parents=True, exist_ok=True)
    by = {(r["architecture"], r["init_seed"], r["data_seed"]): r for r in runs}
    colors = {"plateau_only": "#888888", "partial": "#d98200", "success": "#1a7f37"}
    for a in ARCHS:
        fig, axes = plt.subplots(3, 3, figsize=(10, 7.5), sharex=True, sharey=True)
        for ri, i in enumerate(SEEDS):
            for ci, d in enumerate(SEEDS):
                ax = axes[ri][ci]
                r = by.get((a, i, d))
                if r:
                    w = r["loss_windows"]
                    ax.plot([x["step"] for x in w], [x["mean_loss"] for x in w], color=colors.get(r["outcome"], "#b00020"), lw=1.4)
                    ax.axhline(.5, color="#bbbbbb", lw=.6, ls="--")
                    if r["learning_onset_step"] is not None:
                        ax.axvline(r["learning_onset_step"], color="#1f4fd8", lw=.9, ls=":")
                    ax.set_title(f"init {i} / data {d}: {r['outcome']}", fontsize=8)
                ax.tick_params(labelsize=7)
        fig.suptitle(f"{a}: training loss (50-update windows); dashed 0.5 = onset threshold, dotted = onset", fontsize=10)
        fig.supxlabel("optimizer updates", fontsize=8)
        fig.supylabel("training loss", fontsize=8)
        fig.tight_layout()
        fig.savefig(directory / f"learning_curves_{a}.png", dpi=110)
        plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
    for ax, ds in zip(axes, SEEDS):
        for a, ls in zip(ARCHS, ("-", "--", "-.", ":")):
            for i in SEEDS:
                r = by.get((a, i, ds))
                if r:
                    w = r["loss_windows"]
                    ax.plot([x["step"] for x in w], [x["mean_loss"] for x in w], ls=ls, lw=1, color={17: "#1f4fd8", 29: "#d98200", 43: "#1a7f37"}[i])
        ax.set_title(f"data seed {ds} (colour = init seed; style = architecture)", fontsize=8)
        ax.axhline(.5, color="#bbbbbb", lw=.6, ls="--")
    fig.tight_layout()
    fig.savefig(directory / "learning_curves_by_data_seed.png", dpi=110)
    plt.close(fig)


def main(argv=None):
    a = argv or sys.argv[1:]
    d = Path(a[0])
    exp11 = Path(a[1]) if len(a) > 1 else d.parent / "experiment_011"
    runs, skipped = load_runs(d)
    out = analyze(runs, skipped, exp11)
    (d / "tables.md").write_text(md(out, runs, skipped), encoding="utf-8", newline="\n")
    (d / "summary.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8", newline="\n")
    try:
        figures(runs, d / "figures")
    except ImportError:
        print("matplotlib unavailable; figures skipped")
    print(f"{len(runs)} runs, {len(skipped)} skipped -> {d / 'tables.md'}")


if __name__ == "__main__":
    main()
