"""Aggregate raw Experiment 011 shard JSON files into summary.json and tables.md (no re-analysis choices)."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean

ORDER = ("protected", "protected_no_retain", "gru24", "gru32", "delta_rule")
DELAYS = ("64", "128", "256", "512")


def load_runs(directory: Path) -> tuple[list[dict], list[dict]]:
    runs, skipped = [], []
    for f in sorted(directory.glob("*.json")):
        if f.name in ("summary.json", "run_manifest.json"):
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        if data.get("experiment") != 11:
            continue
        runs += data["runs"]
        skipped += data.get("skipped", [])
    runs.sort(key=lambda r: (ORDER.index(r["variant"]), r["seed"]))
    return runs, skipped


def pct(x) -> str:
    return "n/a" if x is None else f"{100 * x:.1f}%"


def plateau_exit(run: dict, threshold: float = .7):
    for c in run["checkpoints"]:
        if c["per_slot"] >= threshold:
            return c["step"]
    return None


def tables(runs: list[dict], skipped: list[dict]) -> str:
    out = ["# Experiment 011 — generated tables", "",
           f"{len(runs)} runs recorded, {len(skipped)} skipped. Held-out histories; `whole_varied` = all 4 slots correct on histories "
           "whose final values are not all equal. `delta_rule` is an explicit-address REFERENCE, not a fair learned comparison.", ""]
    out += ["## Every run", "", "| model | seed | status | updates | params | per-slot@64 | whole@64 | whole-varied@64 | @128 | @256 | @512 | "
            "final train loss | plateau exit (per-slot ≥70%) | wall s |", "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in runs:
        e = r.get("eval", {})
        last = r["loss_windows"][-1]["mean_loss"] if r["loss_windows"] else None
        out.append(f"| {r['variant']}{' (ref)' if r['reference_only'] else ''} | {r['seed']} | {r['status']} | {r['steps']} | {r['parameters']} | "
                   f"{pct(e.get('64', {}).get('per_slot'))} | {pct(e.get('64', {}).get('whole'))} | {pct(e.get('64', {}).get('whole_varied'))} | "
                   f"{pct(e.get('128', {}).get('whole_varied'))} | {pct(e.get('256', {}).get('whole_varied'))} | {pct(e.get('512', {}).get('whole_varied'))} | "
                   f"{'n/a' if last is None else f'{last:.3f}'} | {plateau_exit(r) or 'none'} | {r['total_wall_s']:.0f} |")
    out += ["", "## Mean over seeds (per-slot / whole / whole-varied)", "",
            "| model | seeds | " + " | ".join(f"@{d}" for d in DELAYS) + " |", "|---|---:|" + "---|" * len(DELAYS)]
    for v in ORDER:
        rs = [r for r in runs if r["variant"] == v and r.get("eval")]
        if not rs:
            continue
        cells = []
        for d in DELAYS:
            es = [r["eval"][d] for r in rs if d in r["eval"]]
            cells.append(" / ".join(pct(mean(e[k] for e in es)) for k in ("per_slot", "whole", "whole_varied")))
        out.append(f"| {v}{' (ref)' if v == 'delta_rule' else ''} | {len(rs)} | " + " | ".join(cells) + " |")
    out += ["", "## Ordinary baselines on the same histories (seed mean; per-slot / whole / whole-varied)", "",
            "| baseline | " + " | ".join(f"@{d}" for d in DELAYS) + " |", "|---|" + "---|" * len(DELAYS)]
    for key in ("independent_guess", "last_write_copy"):
        cells = []
        for d in DELAYS:
            es = [r["eval"][d]["baselines"][key] for r in runs if d in r.get("eval", {}) and r["variant"] == "gru24"]
            cells.append(" / ".join(pct(mean(e[k] for e in es)) for k in ("per_slot", "whole", "whole_varied")) if es else "n/a")
        out.append(f"| {key} | " + " | ".join(cells) + " |")
    out += ["", "Analytic independent guess: per-slot 50.0 %, whole 6.25 %.", "",
            "## Held-out delay-64 per-slot accuracy at checkpoints (every 250 updates)", "",
            "| model | seed | " + " | ".join(str(c["step"]) for c in runs[0]["checkpoints"]) + " | final |" if runs and runs[0]["checkpoints"] else "",
            "|---|---:|" + "---:|" * (len(runs[0]["checkpoints"]) + 1) if runs and runs[0]["checkpoints"] else ""]
    for r in runs:
        out.append(f"| {r['variant']} | {r['seed']} | " + " | ".join(pct(c["per_slot"]) for c in r["checkpoints"]) +
                   f" | {pct(r.get('eval', {}).get('64', {}).get('per_slot'))} |")
    out += ["", "## Compute", "", "| model | params | mean train wall s | mean train CPU s | training token positions |", "|---|---:|---:|---:|---:|"]
    for v in ORDER:
        rs = [r for r in runs if r["variant"] == v]
        if rs:
            out.append(f"| {v} | {rs[0]['parameters']} | {mean(r['train_wall_s'] for r in rs):.0f} | {mean(r['train_cpu_s'] for r in rs):.0f} | {rs[0]['train_token_positions']:,} |")
    hashes = {}
    for r in runs:
        hashes.setdefault(r["seed"], set()).add(r["training_stream_sha256"])
    out += ["", "## Training-stream identity", "", "| seed | distinct stream hashes across models (must be 1) |", "|---:|---:|"]
    out += [f"| {s} | {len(h)} |" for s, h in sorted(hashes.items())]
    if skipped:
        out += ["", "## Skipped", ""] + [f"- {s}" for s in skipped]
    return "\n".join(x for x in out if x is not None) + "\n"


def main(argv=None):
    d = Path((argv or sys.argv[1:])[0])
    runs, skipped = load_runs(d)
    (d / "tables.md").write_text(tables(runs, skipped), encoding="utf-8", newline="\n")
    summary = [{k: r.get(k) for k in ("variant", "seed", "status", "steps", "parameters", "training_stream_sha256")} |
               {"eval": {dl: {m: r["eval"][dl][m] for m in ("per_slot", "whole", "whole_varied")} for dl in r.get("eval", {})}} for r in runs]
    (d / "summary.json").write_text(json.dumps({"runs": summary, "skipped": skipped}, indent=2), encoding="utf-8", newline="\n")
    print(f"{len(runs)} runs, {len(skipped)} skipped -> {d / 'tables.md'}")


if __name__ == "__main__":
    main()
