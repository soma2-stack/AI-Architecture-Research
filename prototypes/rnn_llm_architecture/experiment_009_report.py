"""Render Experiment 009 tables and preregistered hypothesis decisions from raw JSON.

Read-only: never trains, never edits the results file. Decision rules are the
ones fixed in EXPERIMENT_009_PLAN.md section 4.
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

SOLVED = 0.90
LEARNED = ("protected_w32", "protected_no_retain_w32", "protected_shift_w32", "protected_hard_w32",
           "protected_hard_shift_w32", "tanh_w32", "gru_w32", "lstm_w32", "gru_w24", "lstm_w20",
           "gru_keep3_w32", "gru_hard_w32")
ORACLE = ("oracle_tag_protected_w32",)


def pct(x):
    return "—" if x is None else f"{100 * x:.1f}%"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def runs_for(report, variant, task="two_slot"):
    return [r for r in report["runs"] if r["variant"] == variant and r.get("train_task") == task]


def unequal(r, delay, key="two_slot"):
    v = r.get(key, {}).get(str(delay))
    return None if v is None else v["paired_on_unequal"]


def mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.fmean(xs) if xs else None


def primary_table(report, variants, delays) -> list[str]:
    seeds = report["config"]["seeds"]
    lines = ["| Arm | Params | State floats | " + " | ".join(f"{d}" for d in delays) + " |",
             "|---|---:|---:|" + "---:|" * len(delays)]
    for v in variants:
        rs = runs_for(report, v)
        if not rs:
            continue
        cells = []
        for d in delays:
            vals = [unequal(r, d) for r in rs]
            solved = sum(1 for x in vals if x is not None and x >= SOLVED)
            cells.append(f"{pct(mean(vals))} ({solved}/{len(seeds)})")
        cells_ok = all(r.get("complete") for r in rs) and len(rs) == len(seeds)
        name = v if cells_ok else f"{v} (incomplete: {[r['status'] for r in rs if not r.get('complete')]})"
        lines.append(f"| `{name}` | {rs[0].get('parameters', '—'):,} | {rs[0].get('recurrent_state_floats', '—')} | "
                     + " | ".join(cells) + " |")
    return lines


def seed_table(report, variants, delays) -> list[str]:
    seeds = report["config"]["seeds"]
    lines = ["| Arm | Delay | " + " | ".join(str(s) for s in seeds) + " |", "|---|---:|" + "---:|" * len(seeds)]
    for v in variants:
        by_seed = {r["seed"]: r for r in runs_for(report, v)}
        if not by_seed:
            continue
        for d in delays:
            lines.append(f"| `{v}` | {d} | " + " | ".join(pct(unequal(by_seed[s], d)) if s in by_seed else "missing"
                                                         for s in seeds) + " |")
    return lines


def learning_table(report, variants) -> list[str]:
    seeds = report["config"]["seeds"]
    lines = ["| Arm | A≠B at 250 updates (per seed) | First checkpoint ≥90% (per seed) | Median | Final loss (mean) | Max pre-clip grad norm |",
             "|---|---|---|---:|---:|---:|"]
    for v in variants:
        by_seed = {r["seed"]: r for r in runs_for(report, v)}
        if not by_seed:
            continue
        at250, first = [], []
        for s in seeds:
            r = by_seed.get(s)
            cp = (r or {}).get("checkpoints", [])
            at250.append(pct(cp[0]["paired_on_unequal"]) if cp else "—")
            first.append((r or {}).get("first_checkpoint_unequal_ge_0.9"))
        hit = [f for f in first if f is not None]
        med = statistics.median(hit) if len(hit) * 2 > len(seeds) else None
        losses = mean([r.get("loss_last") for r in by_seed.values()])
        grad = max((r.get("max_grad_norm_preclip") or 0) for r in by_seed.values()) if by_seed else None
        lines.append(f"| `{v}` | {' / '.join(at250)} | {' / '.join('never' if f is None else str(f) for f in first)} | "
                     f"{'—' if med is None else med} | {'—' if losses is None else f'{losses:.4f}'} | "
                     f"{'—' if grad is None else f'{grad:.3g}'} |")
    return lines


def curve_table(report, variants) -> list[str]:
    """Mean held-out A≠B both-correct per checkpoint, and how often both queries get the same answer."""
    steps = [c["step"] for c in runs_for(report, variants[0])[0]["checkpoints"]]
    lines = ["| Arm | " + " | ".join(str(s) for s in steps) + " | same answer to A and B at 250 → final |",
             "|---|" + "---:|" * len(steps) + "---|"]
    for v in variants:
        rs = [r for r in runs_for(report, v) if r.get("checkpoints")]
        if not rs:
            continue
        means = [pct(mean([r["checkpoints"][i]["paired_on_unequal"] for r in rs if len(r["checkpoints"]) > i]))
                 for i in range(len(steps))]
        same0 = mean([r["checkpoints"][0]["predicts_same_for_both"] for r in rs])
        same1 = mean([r["checkpoints"][-1]["predicts_same_for_both"] for r in rs])
        lines.append(f"| `{v}` | " + " | ".join(means) + f" | {pct(same0)} → {pct(same1)} |")
    return lines


def legacy_table(report) -> list[str]:
    seeds = report["config"]["seeds"]
    delays = report["config"]["legacy_delays"]
    lines = ["| Model | Trained on | " + " | ".join(f"legacy {d}" for d in delays) + " | two-slot 64 | two-slot 256 |",
             "|---|---|" + "---:|" * (len(delays) + 2)]
    for v in report["config"]["legacy_variants"]:
        for task in ("two_slot", "legacy"):
            rs = runs_for(report, v, task)
            if not rs:
                continue
            cells = [pct(mean([unequal(r, d, "legacy") for r in rs])) for d in delays]
            cells += [pct(mean([unequal(r, d) for r in rs])) for d in (64, 256)]
            lines.append(f"| `{v}` | {task} ({len(rs)}/{len(seeds)} seeds) | " + " | ".join(cells) + " |")
    return lines


def gate_table(report, variants) -> list[str]:
    lines = ["| Arm | Layer | mean gate: marked value | unmarked bit | WRITE marker | benign distractor | exact-zero fraction on distractors | implied retention after 512 non-write tokens (median over seeds) |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for v in variants:
        rs = [r for r in runs_for(report, v) if r.get("gates")]
        if not rs:
            continue
        for layer in range(len(rs[0]["gates"]["layers"])):
            rows = [r["gates"]["layers"][layer] for r in rs]
            m = lambda k: mean([x[k]["mean"] for x in rows])
            z = mean([x["benign_distractor"]["fraction_exactly_zero"] for x in rows])
            ret = statistics.median(x["implied_retention_after_512_nonwrite_tokens"] for x in rows)
            lines.append(f"| `{v}` | {layer} | {m('marked_value'):.3f} | {m('unmarked_bit'):.3f} | {m('write_marker'):.3f} | "
                         f"{m('benign_distractor'):.3f} | {z:.2f} | {ret:.2g} |")
    return lines


def perturbation_table(report, variants) -> list[str]:
    lines = ["| Arm | Seeds solving 64 | clean, immediate | clean, +64 tail | noise 0.5, immediate | noise 0.5, +64 tail | noise 1.0, immediate | noise 1.0, +64 tail |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for v in variants:
        if not runs_for(report, v):
            continue
        rs = [r for r in runs_for(report, v) if (unequal(r, 64) or 0) >= SOLVED and r.get("perturbation")]
        if not rs:
            lines.append(f"| `{v}` | 0 | — | — | — | — | — | — |")
            continue
        p = [r["perturbation"] for r in rs]
        lines.append(f"| `{v}` | {len(rs)} | {pct(mean([x['clean_immediate'] for x in p]))} | "
                     f"{pct(mean([x['clean_after_tail'] for x in p]))} | "
                     f"{pct(mean([x['noise_0.5']['immediate'] for x in p]))} | {pct(mean([x['noise_0.5']['after_tail'] for x in p]))} | "
                     f"{pct(mean([x['noise_1.0']['immediate'] for x in p]))} | {pct(mean([x['noise_1.0']['after_tail'] for x in p]))} |")
    return lines


def probe_table(report, variants) -> list[str]:
    lines = ["| Arm | Native 64 | Probe 64 (held-out) | Native 256 | Probe fit at 64, applied at 256 | Probe features |",
             "|---|---:|---:|---:|---:|---:|"]
    for v in variants:
        rs = [r for r in runs_for(report, v) if r.get("probe")]
        if not rs:
            continue
        lines.append(f"| `{v}` | {pct(mean([unequal(r, 64) for r in rs]))} | "
                     f"{pct(mean([r['probe']['test']['paired_on_unequal'] for r in rs]))} | "
                     f"{pct(mean([unequal(r, 256) for r in rs]))} | "
                     f"{pct(mean([r['probe']['transfer']['paired_on_unequal'] for r in rs]))} | {rs[0]['probe']['features']} |")
    return lines


def baseline_table(report, delays) -> list[str]:
    rs = [r for r in report["runs"] if r.get("two_slot")]
    names = list(rs[0]["two_slot"][str(delays[0])]["baselines"]) if rs else []
    lines = ["| Rule (no learning) | " + " | ".join(str(d) for d in delays) + " |", "|---|" + "---:|" * len(delays)]
    for n in names:
        lines.append(f"| {n} | " + " | ".join(pct(mean([r["two_slot"][str(d)]["baselines"][n] for r in rs])) for d in delays) + " |")
    return lines


def resource_table(report, variants) -> list[str]:
    lines = ["| Arm | Params | State floats | Median train s | Median eval s | Statuses |", "|---|---:|---:|---:|---:|---|"]
    for v in variants:
        rs = runs_for(report, v)
        if not rs:
            continue
        st = sorted({r["status"] for r in rs})
        lines.append(f"| `{v}` | {rs[0].get('parameters', 0):,} | {rs[0].get('recurrent_state_floats')} | "
                     f"{statistics.median(r.get('train_seconds', 0) for r in rs):.0f} | "
                     f"{statistics.median(r.get('eval_seconds', 0) for r in rs):.0f} | {', '.join(st)} |")
    for v in report["config"]["legacy_variants"]:
        rs = runs_for(report, v, "legacy")
        if rs:
            lines.append(f"| `{v}` (legacy-trained) | {rs[0].get('parameters', 0):,} | {rs[0].get('recurrent_state_floats')} | "
                         f"{statistics.median(r.get('train_seconds', 0) for r in rs):.0f} | "
                         f"{statistics.median(r.get('eval_seconds', 0) for r in rs):.0f} | {', '.join(sorted({r['status'] for r in rs}))} |")
    return lines


def decisions(report) -> list[str]:
    seeds = report["config"]["seeds"]
    n = len(seeds)
    out = []
    by = lambda v, t="two_slot": {r["seed"]: r for r in runs_for(report, v, t)}
    # H1
    p = by("protected_w32")
    solved = [s for s in seeds if s in p and (unequal(p[s], 64) or 0) >= SOLVED]
    early = [p[s]["checkpoints"][0]["paired_on_unequal"] for s in seeds if s in p and p[s].get("checkpoints")]
    h1 = ("SUPPORTED" if len(solved) >= 3 and early and max(early) < .25 else
          "FALSIFIED" if len(solved) <= 1 else "INCONCLUSIVE")
    out.append(f"- **H1 (budget/plateau): {h1}.** `protected_w32` solves 64 in {len(solved)}/{n} seeds; "
               f"A≠B at 250 updates per seed: {', '.join(pct(x) for x in early)}.")
    # H2
    lt, ll = by("protected_w32"), by("protected_w32", "legacy")
    diffs = {d: [unequal(lt[s], d, "legacy") - unequal(ll[s], d, "legacy") for s in seeds if s in lt and s in ll]
             for d in (128, 256)}
    if all(diffs[d] for d in diffs):
        means = {d: statistics.fmean(v) for d, v in diffs.items()}
        signs = {d: sum(1 for x in v if x > 0) for d, v in diffs.items()}
        if all(means[d] >= .20 and signs[d] >= 4 for d in diffs):
            h2 = "SUPPORTED"
        elif any(means[d] < .10 or signs[d] <= 2 for d in diffs):
            h2 = "FALSIFIED"
        else:
            h2 = "INCONCLUSIVE"
        out.append(f"- **H2 (fixed-timing task): {h2}.** Legacy-eval A≠B, two-slot-trained minus legacy-trained "
                   f"`protected_w32`: 128 → {100 * means[128]:+.1f} pp ({signs[128]}/{len(diffs[128])} seeds positive); "
                   f"256 → {100 * means[256]:+.1f} pp ({signs[256]}/{len(diffs[256])} positive).")
    # H3
    nr = by("protected_no_retain_w32")
    nr_solved = sum(1 for s in seeds if s in nr and (unequal(nr[s], 64) or 0) >= SOLVED)
    rets = [layer["implied_retention_after_512_nonwrite_tokens"] for s in solved for layer in p[s]["gates"]["layers"]]
    h3 = "SUPPORTED" if nr_solved >= len(solved) - 1 and rets and max(rets) < .01 else "FALSIFIED"
    out.append(f"- **H3 (protected retention unused): {h3}.** no-retain solves 64 in {nr_solved}/{n} vs protected "
               f"{len(solved)}/{n}; max implied 512-token retention over solved protected runs and layers: "
               f"{max(rets) if rets else float('nan'):.2g}.")
    # H4
    for v in LEARNED + ORACLE:
        rs = [r for r in by(v).values() if (unequal(r, 64) or 0) >= SOLVED and r.get("perturbation")]
        if len(rs) < 3:
            continue
        ok = sum(1 for r in rs if r["perturbation"]["noise_0.5"]["after_tail"] >= r["perturbation"]["noise_0.5"]["immediate"]
                 and r["perturbation"]["noise_0.5"]["after_tail"] >= SOLVED)
        verdict = "SUPPORTED" if ok >= 3 else "NOT SUPPORTED"
        out.append(f"- **H4 (error-correcting memory) for `{v}`: {verdict}** ({ok}/{len(rs)} solved seeds recover from 0.5×RMS noise).")
    # H5
    orc = by("oracle_tag_protected_w32")
    of = [orc[s]["first_checkpoint_unequal_ge_0.9"] for s in seeds if s in orc and orc[s]["first_checkpoint_unequal_ge_0.9"]]
    limit = statistics.median(of) + 250 if of else None
    for v in ("protected_hard_w32", "protected_hard_shift_w32"):
        h = by(v)
        fast = sum(1 for s in seeds if s in h and limit is not None and h[s]["first_checkpoint_unequal_ge_0.9"] is not None
                   and h[s]["first_checkpoint_unequal_ge_0.9"] <= limit)
        long = sum(1 for s in seeds if s in h and (unequal(h[s], 512) or 0) >= SOLVED)
        verdict = "SUPPORTED" if fast >= 3 and long >= 3 else "FALSIFIED"
        out.append(f"- **H5 (learned exact closure ≈ oracle) for `{v}`: {verdict}.** Reached 90% by oracle median + 250 "
                   f"(= {limit}) in {fast}/{n} seeds; solves 512 in {long}/{n}.")
    # H6
    counts = {v: (sum(1 for r in runs_for(report, v) if (unequal(r, 64) or 0) >= SOLVED),
                  sum(1 for r in runs_for(report, v) if (unequal(r, 512) or 0) >= SOLVED))
              for v in LEARNED if runs_for(report, v)}
    out.append("- **H6 (descriptive) solved seeds at 64 / 512:** " +
               "; ".join(f"`{v}` {a}/{b}" for v, (a, b) in counts.items()) + ".")
    return out


def load_hosted(path: Path) -> dict:
    """Hosted per-run summary lines (two-slot A≠B by delay), keyed by (task, variant, seed)."""
    out = {}
    for line in path.read_text().splitlines():
        row = json.loads(line)
        if "variant" in row:
            out[(row["task"], row["variant"], row["seed"])] = row
    return out


def hosted_table(report, hosted: dict) -> list[str]:
    """Local versus hosted replication of the primary metric on identical code and seeds."""
    delays = [str(d) for d in report["config"]["eval_delays"]]
    lines = ["| Arm | Trained on | Seed pairs | Solved 64 local / hosted | Solved 512 local / hosted | Mean abs. diff (all delays) | Seed-runs whose solved/unsolved status differs at any delay |",
             "|---|---|---:|---:|---:|---:|---:|"]
    keys = [("two_slot", v) for v in LEARNED + ORACLE] + [("legacy", v) for v in report["config"]["legacy_variants"]]
    for task, v in keys:
        pairs = [(r, hosted[(task, v, r["seed"])]) for r in runs_for(report, v, task) if (task, v, r["seed"]) in hosted]
        if not pairs:
            continue
        loc = lambda r, d: r["two_slot"][d]["paired_on_unequal"]
        s64 = (sum(loc(r, "64") >= SOLVED for r, _ in pairs), sum(h["unequal_by_delay"]["64"] >= SOLVED for _, h in pairs))
        s512 = (sum(loc(r, "512") >= SOLVED for r, _ in pairs), sum(h["unequal_by_delay"]["512"] >= SOLVED for _, h in pairs))
        diffs = [abs(loc(r, d) - h["unequal_by_delay"][d]) for r, h in pairs for d in delays]
        flips = sum(any((loc(r, d) >= SOLVED) != (h["unequal_by_delay"][d] >= SOLVED) for d in delays) for r, h in pairs)
        lines.append(f"| `{v}` | {task} | {len(pairs)} | {s64[0]} / {s64[1]} | {s512[0]} / {s512[1]} | "
                     f"{100 * statistics.fmean(diffs):.1f} pp | {flips} |")
    return lines


def render(report: dict, hosted: dict | None = None) -> str:
    delays = report["config"]["eval_delays"]
    parts = [f"Status: **{report['status']}**; runs {len(report['runs'])}; elapsed {report['elapsed_seconds']:.0f} s; "
             f"torch {report['environment']['torch']}; Python {report['environment']['python']}; "
             f"{report['environment']['workers']} workers × 1 thread.", "",
             "### Primary: A≠B both-correct, mean over seeds (solved seeds ≥90%)", "",
             *primary_table(report, LEARNED, delays), "", "Oracle upper-bound diagnostic (not an architecture):", "",
             *primary_table(report, ORACLE, delays), "", "### Rule baselines on the same held-out histories (A≠B both-correct)", "",
             *baseline_table(report, delays), "", "### Per-seed A≠B both-correct", "",
             *seed_table(report, LEARNED + ORACLE, (64, 256, 512)), "", "### Learning speed and stability", "",
             *learning_table(report, LEARNED + ORACLE), "",
             "Mean held-out A≠B both-correct at the training length by update (checkpoint histories):", "",
             *curve_table(report, LEARNED + ORACLE), "", "### Legacy task (Experiments 004–008 generator)", "",
             *legacy_table(report), "", "### Gate usage", "", *gate_table(report, LEARNED + ORACLE), "",
             "### State-perturbation recovery (seeds that solve 64)", "", *perturbation_table(report, LEARNED + ORACLE), "",
             "### Frozen-state linear probe", "", *probe_table(report, LEARNED + ORACLE), "",
             "### Resources", "", *resource_table(report, LEARNED + ORACLE), "",
             "### Preregistered decisions", "", *decisions(report)]
    if hosted:
        parts += ["", "### Hosted GitHub Actions replication (torch 2.14.1+cpu wheel)", "", *hosted_table(report, hosted)]
    return "\n".join(parts) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("results", type=Path)
    p.add_argument("--hosted", type=Path, help="JSONL of hosted per-run summary lines")
    p.add_argument("--output", type=Path)
    a = p.parse_args(argv)
    text = render(load(a.results), load_hosted(a.hosted) if a.hosted else None)
    if a.output:
        if a.output.exists():
            raise FileExistsError(a.output)
        a.output.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
