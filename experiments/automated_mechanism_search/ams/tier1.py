"""Stage-2 Tier-1 evaluation (IMPLEMENTATION_DECISIONS D-S2-2, D-S2-3, D-T1-1..6).

Baselines: SGD / SGDM / AdamW on Tier-1 seeds 1000-1002 (computed once before the search).
Candidate: B, C*, F each with 3 seeds x 3 learning rates; learning rate selected per task by
training-side metrics (D-LR-1); effects vs the best generic; quality q (AE.3.3); Tier-1 minimum
effect vs AdamW (2 sigma)."""
from __future__ import annotations

import math
from typing import Dict, List, Optional

import numpy as np

from .controls import GENERIC, make, run_job
from .runners import select_lr, summarize
from .substrate import Net, ProgramLearner, learner_flops_per_example
from .canon import canon
from .families import REFERENCES
from .grammar import Program, program_to_dict

TIER1_SEEDS = [1000, 1001, 1002]
TASKS = ("B", "Cstar", "F")


def seed_metrics(task: str, summ: Dict) -> List[float]:
    """Per-seed lower-is-better metric (D-T1-3)."""
    if task == "B":
        return list(summ["forgetting_seeds"])
    if task == "Cstar":
        return list(summ["hl_censored_seeds"])
    return list(summ["ood_err_seeds"])


def mean_metric(task: str, summ: Dict) -> float:
    return float(np.mean(seed_metrics(task, summ)))


def compute_baselines(results: Dict[str, Dict]) -> Dict:
    """results[f'{task}:{method}'] = runner output on TIER1_SEEDS."""
    out = {"seeds": TIER1_SEEDS, "summaries": {}, "best_generic": {}, "adamw": {}}
    for t in TASKS:
        out["summaries"][t] = {}
        for m in GENERIC:
            s = summarize(t, select_lr(results[f"{t}:{m}"], TIER1_SEEDS))
            out["summaries"][t][m] = s
        best, bv = None, math.inf
        for m in GENERIC:
            s = out["summaries"][t][m]
            if s["stable"] and mean_metric(t, s) < bv:
                best, bv = m, mean_metric(t, s)
        if best is None:
            raise RuntimeError(f"no stable generic baseline on {t} (Tier-1 seeds)")
        g = out["summaries"][t][best]
        out["best_generic"][t] = {"method": best, "metric": bv,
                                  "T2_final_mse": g.get("T2_final_mse"),
                                  "train_acc": g.get("train_acc")}
        a = out["summaries"][t]["AdamW"]
        if not a["stable"]:
            raise RuntimeError(f"AdamW unstable on {t} (Tier-1 seeds)")
        sm = seed_metrics(t, a)
        out["adamw"][t] = {"mean": float(np.mean(sm)), "sd": max(float(np.std(sm, ddof=1)), 1e-9), "seeds": sm}
    return out


def _cost_terms(prog: Program) -> Dict:
    net = Net(32, 4, [0])
    L = ProgramLearner(prog)
    sgd = ProgramLearner(canon(REFERENCES["R1_SGD"]))
    f_p = learner_flops_per_example(net, L)
    f_s = learner_flops_per_example(net, sgd)
    st = L.state_floats(net)
    params = net.n_params()
    return {"flops": f_p, "flops_sgd": f_s, "flops_ratio": f_p / f_s, "state_floats": st, "params": params,
            "penalty": 0.05 * math.log2(f_p / f_s) + 0.05 * math.log2(1 + st / params)}


def score(prog: Program, task_results: Dict[str, Dict], base: Dict) -> Dict:
    """Effects, constraints, q and Tier-1 gate from per-task runner outputs (D-S2-2/3)."""
    effects, cons, gates, summ, metr = {}, {}, {}, {}, {}
    for t in TASKS:
        r = task_results[t]
        if r.get("error"):
            s = {"stable": False, "error": r["error"]}
        else:
            s = summarize(t, select_lr(r, TIER1_SEEDS))
        summ[t] = s
        if not s["stable"]:
            effects[t] = -math.inf
            cons[t] = False
            gates[t] = False
            continue
        g = base["best_generic"][t]
        mP = mean_metric(t, s)
        metr[t] = mP
        if t == "B":
            e = (g["metric"] - mP) / max(g["metric"], 1.0)
            ok = s["T2_final_mse"] <= 1.25 * g["T2_final_mse"]
        elif t == "Cstar":
            e = (g["metric"] - mP) / max(g["metric"], 4.0)
            ok = s["return_ok_count"] >= 2
        else:
            e = (g["metric"] - mP) / max(g["metric"], 0.01)
            ok = s["train_acc"] >= 0.98
        if not ok:
            e = min(e, 0.0)
        effects[t] = float(e)
        cons[t] = bool(ok)
        A = base["adamw"][t]
        gates[t] = bool(ok and (A["mean"] - mP) >= 2.0 * A["sd"])
    cost = _cost_terms(prog)
    finite = [e for e in effects.values() if math.isfinite(e)]
    if not finite:
        return {"q": None, "effects": effects, "summaries": summ, "cost": cost, "reason": "unstable_all_tasks"}
    best_task = max(TASKS, key=lambda t: (effects[t], -TASKS.index(t)))
    q = max(finite) - cost["penalty"]
    return {"q": float(q), "effects": effects, "constraints": cons, "tier1_gate": gates,
            "best_task": best_task, "tier1_pass_on_best": gates[best_task],
            "metrics": metr, "summaries": summ, "cost": cost}


def evaluate(prog: Program, base: Dict, pool) -> Dict:
    """Run the three tasks for a candidate (in the pool) and score them."""
    d = program_to_dict(prog)
    jobs = [{"task": t, "learner": "P", "program": d, "seeds": TIER1_SEEDS} for t in TASKS]
    res = pool.map(run_job, jobs, chunksize=1)
    tr = {t: r for t, r in zip(TASKS, res)}
    out = score(prog, tr, base)
    out["cpu_s_workers"] = float(sum(r.get("cpu_s", 0.0) for r in res))
    out["lr"] = {t: (out["summaries"][t].get("lr") if out["summaries"][t].get("stable") else None) for t in TASKS}
    return out
