"""Experiment 013 analysis as preregistered in EXPERIMENT_013_PLAN.md (conditions A–D, paired comparison rules).

A = protected and D = protected_no_retain are read from Experiment 012's raw JSON; B and C from the Experiment 013 confirmatory
JSON. Descriptive only; reads raw files, never rewrites them.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean

from .capacity_012 import SEEDS
from .experiment_012_report import load_runs, partition, shares

COND = {"A": "protected", "B": "protected_fixed_0474", "C": "protected_fixed_005", "D": "protected_no_retain"}
LABEL = {"A": "learned gate", "B": "fixed g = sigmoid(-3) = 0.0474", "C": "fixed g = 0.005", "D": "forced overwrite (g = 1)"}
RANK = {"plateau_only": 0, "partial": 1, "success": 2}
DELAYS = ("64", "128", "256", "512")
PAIRS = (("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("B", "C"), ("A", "D"))


def collect(exp013: Path, exp012: Path) -> dict:
    r12, _ = load_runs(exp012)
    r13, sk13 = load_runs(exp013)
    cells = {}
    for k, arch in COND.items():
        src = r12 if k in ("A", "D") else r13
        rows = {(r["init_seed"], r["data_seed"]): r for r in src if r["architecture"] == arch}
        cells[k] = rows
    return {"cells": cells, "skipped": sk13}


def wv(r, d="64"):
    return r["eval"][d]["whole_varied"]


def compare(cells, x, y) -> dict:
    keys = [(i, d) for i in SEEDS for d in SEEDS]
    if any(k not in cells[x] or k not in cells[y] for k in keys):
        return {"complete": False}
    hi = sum(RANK[cells[x][k]["outcome"]] > RANK[cells[y][k]["outcome"]] for k in keys)
    lo = sum(RANK[cells[x][k]["outcome"]] < RANK[cells[y][k]["outcome"]] for k in keys)
    dwv = mean(wv(cells[x][k]) for k in keys) - mean(wv(cells[y][k]) for k in keys)
    lx = sum(cells[x][k]["learning_onset_step"] is not None for k in keys)
    ly = sum(cells[y][k]["learning_onset_step"] is not None for k in keys)
    sx = sum(cells[x][k]["outcome"] == "success" for k in keys)
    sy = sum(cells[y][k]["outcome"] == "success" for k in keys)
    x_out = hi >= 4 and lo <= 1 and dwv >= .20
    y_out = lo >= 4 and hi <= 1 and -dwv >= .20
    comparable = not x_out and not y_out and abs(lx - ly) <= 1 and abs(sx - sy) <= 1
    verdict = f"{x} outperforms {y}" if x_out else f"{y} outperforms {x}" if y_out else "comparable" if comparable else "inconclusive"
    return {"complete": True, "x_higher_class_cells": hi, "x_lower_class_cells": lo, "mean_wv64_diff_x_minus_y": dwv,
            "learned": [lx, ly], "success": [sx, sy], "verdict": verdict}


def age_accuracy(rows) -> dict:
    tot: dict[str, list[int]] = {}
    for r in rows:
        for k, v in r["eval"]["64"]["by_last_write_age"].items():
            t = tot.setdefault("initial_only" if k == "initial_only" else "rewritten", [0, 0])
            t[0] += v["n"]
            t[1] += v["correct"]
    return {k: v[1] / v[0] for k, v in tot.items()}


def analyze(data) -> dict:
    cells = data["cells"]
    out = {"conditions": {}, "pairs": {}, "skipped": data["skipped"]}
    for k, rows in cells.items():
        rs = list(rows.values())
        info = {"architecture": COND[k], "label": LABEL[k], "runs": len(rs),
                "incomplete": [f"{i}:{d}" for (i, d), r in rows.items() if r["status"] != "complete"]}
        if rs:
            info["live_parameters"] = rs[0].get("live_parameters", 7488 if k == "D" else 8016)
            info["allocated_parameters"] = rs[0]["parameters"]
            info["learned"] = sum(r["learning_onset_step"] is not None for r in rs)
            info["success"] = sum(r["outcome"] == "success" for r in rs)
            info["mean_whole_varied"] = {d: mean(wv(r, d) for r in rs) for d in DELAYS}
            info["mean_per_slot64"] = mean(r["eval"]["64"]["per_slot"] for r in rs)
            info["matrix"] = {f"{i}:{d}": {"wv64": wv(rows[(i, d)]), "outcome": rows[(i, d)]["outcome"], "onset": rows[(i, d)]["learning_onset_step"],
                                           "final_loss": mean(x["mean_loss"] for x in rows[(i, d)]["loss_windows"][-5:])}
                              for i in SEEDS for d in SEEDS if (i, d) in rows}
            if len(rows) == 9:
                info["init_means_wv"] = {i: mean(wv(rows[(i, d)]) for d in SEEDS) for i in SEEDS}
                info["data_means_wv"] = {d: mean(wv(rows[(i, d)]) for i in SEEDS) for d in SEEDS}
                info["learned_by_init"] = {i: sum(rows[(i, d)]["learning_onset_step"] is not None for d in SEEDS) for i in SEEDS}
                info["partition_wv"] = shares(partition({(i, d): wv(rows[(i, d)]) for i in SEEDS for d in SEEDS}))
            info["age_accuracy64"] = age_accuracy(rs)
            succ = [r for r in rs if r["outcome"] == "success"]
            info["success_wv_by_delay"] = {d: mean(wv(r, d) for r in succ) for d in DELAYS} if succ else None
            info["mean_train_wall_s"] = mean(r["train_wall_s"] for r in rs)
        out["conditions"][k] = info
    for x, y in PAIRS:
        out["pairs"][f"{x}_vs_{y}"] = compare(cells, x, y)
    p = out["pairs"]
    c = out["conditions"]

    def outperforms(x, y):
        return p.get(f"{x}_vs_{y}", {}).get("verdict") == f"{x} outperforms {y}" or p.get(f"{y}_vs_{x}", {}).get("verdict") == f"{x} outperforms {y}"

    def comparable(x, y):
        return p.get(f"{x}_vs_{y}", {}).get("verdict") == "comparable" or p.get(f"{y}_vs_{x}", {}).get("verdict") == "comparable"

    age_c = c.get("C", {}).get("age_accuracy64", {})
    out["preregistered_interpretation"] = {
        "1_learned_gate_necessary (A outperforms both B and C)": outperforms("A", "B") and outperforms("A", "C"),
        "2_fixed_retention_sufficient (B or C comparable to or better than A)": any(comparable("A", z) or outperforms(z, "A") for z in ("B", "C")),
        "3_retention_per_se_matters (B or C outperforms D)": outperforms("B", "D") or outperforms("C", "D"),
        "4a_stronger_retention_prevents_updating (B>C and C rewritten < initial-only)": outperforms("B", "C") and age_c.get("rewritten", 1) < age_c.get("initial_only", 0),
        "4b_stronger_retention_helps (C outperforms B)": outperforms("C", "B"),
    }
    return out


def md(out) -> str:
    c, p = out["conditions"], out["pairs"]
    ab = {"plateau_only": "P", "partial": "Pa", "success": "S"}
    L = ["# Experiment 013 — generated tables", "",
         "A and D are Experiment 012 runs (reused); B and C are new. Rows = init seed, columns = data seed. whole-varied@64 on the "
         "fixed Experiment 012 evaluation set (512 histories). P = plateau_only, Pa = partial, S = success. Descriptive; 9 runs per condition.", "",
         "## Summary", "", "| cond | model | slow-write gate | live / allocated params | learned | success | mean wv @64 / @128 / @256 / @512 | mean per-slot@64 | mean train s |",
         "|---|---|---|---:|---:|---:|---|---:|---:|"]
    for k in "ABCD":
        i = c[k]
        if not i["runs"]:
            L.append(f"| {k} | {i['architecture']} | {i['label']} | — | — | — | — | — | — |")
            continue
        L.append(f"| {k} | `{i['architecture']}` | {i['label']} | {i['live_parameters']:,} / {i['allocated_parameters']:,} | {i['learned']}/{i['runs']} | {i['success']}/{i['runs']} | "
                 + " / ".join(f"{100 * i['mean_whole_varied'][d]:.1f}%" for d in DELAYS) + f" | {100 * i['mean_per_slot64']:.1f}% | {i['mean_train_wall_s']:.0f} |")
    for k in "ABCD":
        i = c[k]
        if not i.get("matrix"):
            continue
        L += ["", f"## {k}: {i['label']} — 3 × 3 (whole-varied@64, outcome, onset)", "", "| init \\ data | 17 | 29 | 43 | row mean |", "|---|---|---|---|---:|"]
        for s in SEEDS:
            cells = []
            for d in SEEDS:
                m = i["matrix"].get(f"{s}:{d}")
                cells.append("n/a" if m is None else f"{100 * m['wv64']:.1f}% ({ab.get(m['outcome'], m['outcome'])}, {m['onset'] if m['onset'] is not None else '—'})")
            rm = i.get("init_means_wv", {}).get(s)
            L.append(f"| **{s}** | " + " | ".join(cells) + f" | {'n/a' if rm is None else f'{100 * rm:.1f}%'} |")
        if "data_means_wv" in i:
            L.append("| col mean | " + " | ".join(f"{100 * i['data_means_wv'][d]:.1f}%" for d in SEEDS) + " | |")
            pw = i["partition_wv"]
            L.append(f"\nVariance shares (whole-varied): init {100 * pw['init']:.0f}%, data {100 * pw['data']:.0f}%, remainder {100 * pw['remainder']:.0f}%. "
                     f"Learned by init seed: {i['learned_by_init']}. Accuracy@64 never-rewritten slots {100 * i['age_accuracy64'].get('initial_only', 0):.1f}%, "
                     f"rewritten slots {100 * i['age_accuracy64'].get('rewritten', 0):.1f}%.")
    L += ["", "## Paired comparisons (preregistered rule)", "", "| X vs Y | X higher class | X lower class | mean wv@64 X − Y | learned X/Y | success X/Y | verdict |", "|---|---:|---:|---:|---|---|---|"]
    for name, r in p.items():
        if not r.get("complete"):
            L.append(f"| {name} | — | — | — | — | — | incomplete data |")
            continue
        L.append(f"| {name.replace('_vs_', ' vs ')} | {r['x_higher_class_cells']} | {r['x_lower_class_cells']} | {100 * r['mean_wv64_diff_x_minus_y']:+.1f} pts | "
                 f"{r['learned'][0]}/{r['learned'][1]} | {r['success'][0]}/{r['success'][1]} | {r['verdict']} |")
    L += ["", "## Preregistered interpretation flags", ""] + [f"- {k}: **{v}**" for k, v in out["preregistered_interpretation"].items()]
    if out["skipped"]:
        L += ["", "## Skipped", ""] + [f"- {s}" for s in out["skipped"]]
    return "\n".join(L) + "\n"


def figure(data, path: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    colors = {"A": "#1a7f37", "B": "#1f4fd8", "C": "#d98200", "D": "#888888"}
    fig, axes = plt.subplots(3, 3, figsize=(11, 8), sharex=True, sharey=True)
    for ri, i in enumerate(SEEDS):
        for ci, d in enumerate(SEEDS):
            ax = axes[ri][ci]
            for k in "DCBA":
                r = data["cells"][k].get((i, d))
                if r:
                    w = r["loss_windows"]
                    ax.plot([x["step"] for x in w], [x["mean_loss"] for x in w], color=colors[k], lw=1.3 if k == "A" else 1.0,
                            label=f"{k}: {LABEL[k]}")
            ax.axhline(.5, color="#bbbbbb", lw=.6, ls="--")
            ax.set_title(f"init {i} / data {d}", fontsize=8)
            ax.tick_params(labelsize=7)
    axes[0][0].legend(fontsize=6, loc="lower left")
    fig.suptitle("Training loss (50-update windows): A learned gate, B fixed 0.0474, C fixed 0.005, D forced overwrite", fontsize=10)
    fig.supxlabel("optimizer updates", fontsize=8)
    fig.supylabel("training loss", fontsize=8)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=110)
    plt.close(fig)


def main(argv=None):
    a = argv or sys.argv[1:]
    d13, d12 = Path(a[0]), Path(a[1])
    data = collect(d13, d12)
    out = analyze(data)
    (d13 / "tables.md").write_text(md(out), encoding="utf-8", newline="\n")
    (d13 / "summary.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8", newline="\n")
    try:
        figure(data, d13 / "figures" / "learning_curves_A_B_C_D.png")
    except ImportError:
        print("matplotlib unavailable; figure skipped")
    print(md(out))


if __name__ == "__main__":
    main()
