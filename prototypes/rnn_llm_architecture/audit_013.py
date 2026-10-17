"""Experiment 013 Phase 1: mechanistic audit by code execution (no training). Read-only with respect to all earlier evidence.

Establishes, by autograd and direct evaluation of the unchanged implementation:
- which parameters receive gradient under retain_slow True/False (live vs allocated parameters);
- the initial slow-write gate and fast-retention gate distributions (they are NOT a constant sigmoid(-3));
- orthonormality of the Walsh masks (so the coefficient update is an exact per-channel convex combination);
- initialization identity between `protected` and `protected_no_retain` for the same seed;
- Experiment 012 onset / late-plateau / training-stream statistics.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from statistics import mean

import torch
import torch.nn.functional as F

from . import capacity_010 as c10
from . import capacity_012 as c12

VOCAB_GROUPS = {"PAD": [0], "unused_1": [1], "WRITE": list(range(2, 10)), "VALUE": list(range(10, 14)),
                "QUERY": list(range(14, 22)), "FILLER": list(range(22, 31)), "unused_31": [31]}
TASK_TOKENS = {"WRITE_0..3": list(range(2, 6)), "VALUE_0..1": [10, 11], "QUERY_0..3": list(range(14, 18)), "FILLER": list(range(22, 30))}


def live_parameters(name: str, seed: int = 17) -> dict:
    """Allocated vs gradient-receiving parameters on a real training batch."""
    model = c10.build(name, 4, 2, seed)
    x = c10.generator_batch(4, 2, 64, 12, seed=1)
    y = c10.replay(x, 4, 2)
    loss = F.cross_entropy(c10.predictions(model, x, 4, 2).reshape(-1, 2), y.reshape(-1))
    loss.backward()
    groups: dict[str, dict] = {}
    for n, p in model.named_parameters():
        key = ".".join(k for k in n.split(".") if not k.isdigit())
        g = groups.setdefault(key, {"allocated": 0, "live": 0})
        g["allocated"] += p.numel()
        g["live"] += p.numel() if p.grad is not None and bool(p.grad.abs().sum() > 0) else 0
    total = sum(g["allocated"] for g in groups.values())
    live = sum(g["live"] for g in groups.values())
    return {"allocated": total, "live": live, "dead": total - live, "by_group": groups}


@torch.no_grad()
def initial_gates(seed: int) -> dict:
    """Layer-0 gates are a pure function of the token embedding, so they are exact per token at initialization."""
    m = c10.build("protected", 4, 2, seed)
    cell = m.cells[0]
    emb = m.embedding.weight
    slow = torch.sigmoid(cell.slow_gate(emb))      # [vocab, channels]
    fast = torch.sigmoid(cell.fast_gate(emb))      # [vocab, width]
    rows = {}
    for g, ids in TASK_TOKENS.items():
        s = slow[ids]
        rows[g] = {"slow_mean": float(s.mean()), "slow_min": float(s.min()), "slow_max": float(s.max()),
                   "fast_retention_mean": float(fast[ids].mean())}
    return {"seed": seed, "nominal_sigmoid_bias": 1 / (1 + math.exp(3)), "layer0_by_token_group": rows,
            "layer0_all_task_tokens": {"slow_min": float(slow[sum(TASK_TOKENS.values(), [])].min()),
                                       "slow_max": float(slow[sum(TASK_TOKENS.values(), [])].max())}}


def mask_orthonormality() -> float:
    m = c10.build("protected", 4, 2, 17)
    M = m.cells[0].masks
    return float((M @ M.T - torch.eye(M.shape[0])).abs().max())


def protected_equals_no_retain_init() -> dict:
    out = {}
    for s in (17, 29, 43):
        a = c12.init_fingerprint(c10.build("protected", 4, 2, s))
        b = c12.init_fingerprint(c10.build("protected_no_retain", 4, 2, s))
        out[s] = a == b
    return out


def stream_stats(data_seed: int, steps: int = 3000) -> dict:
    """Properties of a training stream that could plausibly matter (counts only; no model)."""
    upd, varied, all_eq, initial_only = [], 0, 0, 0
    n_hist = 0
    for t in range(steps):
        x = c10.generator_batch(4, 2, 64, 12, seed=c12.training_seed(data_seed, t))
        y = c10.replay(x, 4, 2)
        pos = c12.last_write_positions(x)
        body = x[:, 8:]
        marked = ((body[:, :-1] >= 2) & (body[:, :-1] < 6) & (body[:, 1:] >= 10) & (body[:, 1:] < 12)).sum(1)
        upd += marked.tolist()
        v = y.max(1).values != y.min(1).values
        varied += int(v.sum())
        all_eq += int((~v).sum())
        initial_only += int((pos < 8).sum())
        n_hist += x.shape[0]
    return {"data_seed": data_seed, "histories": n_hist, "mean_marked_rewrites": mean(upd),
            "frac_varied": varied / n_hist, "frac_all_equal": all_eq / n_hist,
            "frac_slots_never_rewritten": initial_only / (4 * n_hist)}


def exp012_curve_facts(directory: Path) -> dict:
    from .experiment_012_report import load_runs
    runs, _ = load_runs(directory)
    rows = []
    for r in runs:
        if r["architecture"] not in ("protected", "protected_no_retain"):
            continue
        w = [x["mean_loss"] for x in r["loss_windows"]]
        rows.append({"arch": r["architecture"], "init": r["init_seed"], "data": r["data_seed"], "outcome": r["outcome"],
                     "onset": r["learning_onset_step"], "loss_at_800": w[15], "loss_at_1500": w[29], "final5": mean(w[-5:]),
                     "min_window": min(w)})
    return {"runs": rows}


def main(argv=None):
    a = argv or sys.argv[1:]
    out = {
        "live_parameters": {n: live_parameters(n) for n in ("protected", "protected_no_retain", "gru24", "gru32")},
        "mask_max_abs_deviation_from_orthonormal": mask_orthonormality(),
        "init_identical_protected_vs_no_retain": protected_equals_no_retain_init(),
        "initial_gates": [initial_gates(s) for s in (17, 29, 43)],
        "training_streams": [stream_stats(s) for s in (17, 29, 43)],
        "exp012_protected_curves": exp012_curve_facts(Path(a[0])),
    }
    Path(a[1]).write_text(json.dumps(out, indent=2), encoding="utf-8", newline="\n")
    lp = out["live_parameters"]
    print({k: (v["allocated"], v["live"], v["dead"]) for k, v in lp.items()})
    print("dead groups no_retain:", {k: v for k, v in lp["protected_no_retain"]["by_group"].items() if v["live"] < v["allocated"]})
    print("masks orthonormal dev:", out["mask_max_abs_deviation_from_orthonormal"], "init identical:", out["init_identical_protected_vs_no_retain"])
    for g in out["initial_gates"]:
        print(g["seed"], {k: (round(v["slow_min"], 4), round(v["slow_max"], 4), round(v["fast_retention_mean"], 3)) for k, v in g["layer0_by_token_group"].items()})
    for s in out["training_streams"]:
        print(s)


if __name__ == "__main__":
    main()
