"""POST-HOC (not preregistered) descriptive checks on Experiment 012 raw JSON: second plateau and runs still improving."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from .experiment_012_report import load_runs


def posthoc(directory: Path) -> dict:
    runs, _ = load_runs(directory)
    partial, plateau = [], {}
    for r in runs:
        w = [x["mean_loss"] for x in r["loss_windows"]]
        last, prev = sum(w[-5:]) / 5, sum(w[-10:-5]) / 5
        if r["outcome"] == "partial":
            partial.append({"arch": r["architecture"], "init": r["init_seed"], "data": r["data_seed"], "onset": r["learning_onset_step"],
                            "final_loss": last, "prev_loss": prev, "still_descending": last - prev < -0.02})
        if r["outcome"] == "plateau_only":
            plateau.setdefault(r["data_seed"], []).append(round(last, 3))
    settled = sorted(round(p["final_loss"], 3) for p in partial if not p["still_descending"])
    return {"label": "POST-HOC, not preregistered", "partial_runs": partial,
            "partial_still_descending": sum(p["still_descending"] for p in partial), "n_partial": len(partial),
            "settled_partial_final_losses": settled, "plateau_only_final_loss_by_data_seed": {str(k): sorted(v) for k, v in sorted(plateau.items())}}


if __name__ == "__main__":
    res = posthoc(Path(sys.argv[1]))
    Path(sys.argv[2]).write_text(json.dumps(res, indent=2), encoding="utf-8", newline="\n")
    print(res["partial_still_descending"], "of", res["n_partial"], "partial runs still descending; settled:", res["settled_partial_final_losses"])
