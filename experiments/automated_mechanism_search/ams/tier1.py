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

TIER1_SEEDS = [1000, 1001, 1002]                 # v5-v7 fast Tier-1 seeds
V8_TIER1_SEEDS = [5000, 5001, 5002]              # prereg v8 fast discovery seeds
TASKS = ("B", "Cstar", "F")
CSTAR_METRICS = ("hl", "aulc")                   # v5-v7: censored half-life; v8: normalized AULC


def seed_metrics(task: str, summ: Dict, cm: str = "hl") -> List[float]:
    """Per-seed lower-is-better metric (D-T1-3; C* per prereg v8 when cm='aulc')."""
    if task == "B":
        return list(summ["forgetting_seeds"])
    if task == "Cstar":
        return list(summ["aulc_seeds"] if cm == "aulc" else summ["hl_censored_seeds"])
    return list(summ["ood_err_seeds"])


def mean_metric(task: str, summ: Dict, cm: str = "hl") -> float:
    return float(np.mean(seed_metrics(task, summ, cm)))


def effect(task: str, g: float, mP: float, cm: str = "hl") -> float:
    """Task effect vs the best generic (D-S2-2; C* per prereg v8 when cm='aulc')."""
    if task == "B":
        return (g - mP) / max(g, 1.0)
    if task == "Cstar":
        return (g - mP) / (max(g, 1e-8) if cm == "aulc" else max(g, 4.0))
    return (g - mP) / max(g, 0.01)


def compute_baselines(results: Dict[str, Dict], cm: str = "hl", seeds=None) -> Dict:
    """results[f'{task}:{method}'] = runner output on the Tier-1 seeds."""
    seeds = TIER1_SEEDS if seeds is None else list(seeds)
    out = {"seeds": seeds, "cstar_metric": cm, "summaries": {}, "best_generic": {}, "adamw": {}}
    for t in TASKS:
        out["summaries"][t] = {}
        for m in GENERIC:
            s = summarize(t, select_lr(results[f"{t}:{m}"], seeds))
            out["summaries"][t][m] = s
        best, bv = None, math.inf
        for m in GENERIC:
            s = out["summaries"][t][m]
            if s["stable"] and mean_metric(t, s, cm) < bv:
                best, bv = m, mean_metric(t, s, cm)
        if best is None:
            raise RuntimeError(f"no stable generic baseline on {t} (Tier-1 seeds)")
        g = out["summaries"][t][best]
        out["best_generic"][t] = {"method": best, "metric": bv,
                                  "T2_final_mse": g.get("T2_final_mse"),
                                  "train_acc": g.get("train_acc")}
        a = out["summaries"][t]["AdamW"]
        if not a["stable"]:
            raise RuntimeError(f"AdamW unstable on {t} (Tier-1 seeds)")
        sm = seed_metrics(t, a, cm)
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


def score(prog: Program, task_results: Dict[str, Dict], base: Dict, cm: str = "hl", seeds=None) -> Dict:
    """Effects, constraints, q and Tier-1 gate from per-task runner outputs (D-S2-2/3)."""
    seeds = TIER1_SEEDS if seeds is None else list(seeds)
    effects, cons, gates, summ, metr = {}, {}, {}, {}, {}
    for t in TASKS:
        r = task_results[t]
        if r.get("error"):
            s = {"stable": False, "error": r["error"]}
        else:
            s = summarize(t, select_lr(r, seeds))
        summ[t] = s
        if not s["stable"]:
            effects[t] = -math.inf
            cons[t] = False
            gates[t] = False
            continue
        g = base["best_generic"][t]
        mP = mean_metric(t, s, cm)
        metr[t] = mP
        e = effect(t, g["metric"], mP, cm)
        if t == "B":
            ok = s["T2_final_mse"] <= 1.25 * g["T2_final_mse"]
        elif t == "Cstar":
            ok = s["return_ok_count"] >= 2
        else:
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


def evaluate(prog: Program, base: Dict, pool, cm: str = "hl", seeds=None) -> Dict:
    """Run the three tasks for a candidate (in the pool) and score them."""
    seeds = TIER1_SEEDS if seeds is None else list(seeds)
    d = program_to_dict(prog)
    jobs = [{"task": t, "learner": "P", "program": d, "seeds": seeds} for t in TASKS]
    res = pool.map(run_job, jobs, chunksize=1)
    tr = {t: r for t, r in zip(TASKS, res)}
    out = score(prog, tr, base, cm, seeds)
    out["cpu_s_workers"] = float(sum(r.get("cpu_s", 0.0) for r in res))
    out["lr"] = {t: (out["summaries"][t].get("lr") if out["summaries"][t].get("stable") else None) for t in TASKS}
    return out
