"""Prereg v8 Stage-2 confirmation funnel.

After the MAP-Elites search stops, every occupied archive cell's current elite is evaluated on its
frozen fast `best_task` over the 8 confirmation seeds 6000-6007 (same LR grid, training-side LR
selection).  Generic baselines (SGD / SGDM / AdamW) are computed once per task on the same seeds.

    e_confirm   = task effect vs the best confirmation generic (Tier-1 formula; C* uses AULC)
    q_confirm   = e_confirm - (already recorded fast cost penalty)

Confirmation-eligible iff: stable after LR selection; task constraint passes (B: T2 <= 1.25 * T2_G;
C*: R0 return condition on >= 6/8 seeds; F: train accuracy >= 0.98); q_confirm >= 0.15; improvement
over the confirmation AdamW mean >= 2 * AdamW sample SD; beats the best generic on >= 6/8 paired
seeds (strictly lower metric).  Promotion: eligible elites only, by descending q_confirm (ties toward
lower library similarity), at most 8 per task and 20 in total."""
from __future__ import annotations

from typing import Dict, List, Sequence

import numpy as np

from .controls import GENERIC
from .runners import select_lr, summarize
from .tier1 import TASKS, effect, mean_metric, seed_metrics

CONFIRM_SEEDS = [6000, 6001, 6002, 6003, 6004, 6005, 6006, 6007]
Q_MIN = 0.15
MIN_WINS = 6
MIN_RETURN_C = 6
MAX_CANDIDATES = 56
PER_TASK_MAX = 8
N_PROMOTE_MAX = 20
CM = "aulc"


def summary(task: str, res: Dict, seeds: Sequence[int] = CONFIRM_SEEDS) -> Dict:
    if res.get("error"):
        return {"stable": False, "error": res["error"]}
    s = summarize(task, select_lr(res, list(seeds)))
    if s["stable"]:
        s["seed_metric"] = seed_metrics(task, s, CM)
        s["metric"] = mean_metric(task, s, CM)
    return s


def baselines(results: Dict[str, Dict], seeds: Sequence[int] = CONFIRM_SEEDS) -> Dict:
    """results[f'{task}:{method}'] -> per-task best generic and AdamW statistics on the seeds."""
    out = {"seeds": list(seeds), "cstar_metric": CM, "summaries": {}, "best_generic": {}, "adamw": {}}
    for t in TASKS:
        S = {m: summary(t, results[f"{t}:{m}"], seeds) for m in GENERIC}
        out["summaries"][t] = S
        stable = {m: S[m] for m in GENERIC if S[m].get("stable")}
        if not stable:
            raise RuntimeError(f"no stable generic on {t} (confirmation seeds)")
        G = min(stable, key=lambda m: stable[m]["metric"])
        out["best_generic"][t] = {"method": G, "metric": stable[G]["metric"], "seed_metric": stable[G]["seed_metric"],
                                  "T2_final_mse": stable[G].get("T2_final_mse")}
        if not S["AdamW"].get("stable"):
            raise RuntimeError(f"AdamW unstable on {t} (confirmation seeds)")
        sm = S["AdamW"]["seed_metric"]
        out["adamw"][t] = {"mean": float(np.mean(sm)), "sd": max(float(np.std(sm, ddof=1)), 1e-9), "seeds": sm}
    return out


def assess(task: str, s: Dict, base: Dict, penalty: float) -> Dict:
    """Confirmation effect, q_confirm and eligibility for one candidate on its frozen task."""
    out: Dict = {"task": task, "stable": bool(s.get("stable")), "penalty": penalty}
    if not out["stable"]:
        out.update(eligible=False, q_confirm=None, reason="unstable")
        return out
    g = base["best_generic"][task]
    mP = s["metric"]
    e = effect(task, g["metric"], mP, CM)
    if task == "B":
        ok = s["T2_final_mse"] <= 1.25 * g["T2_final_mse"]
    elif task == "Cstar":
        ok = s["return_ok_count"] >= MIN_RETURN_C
    else:
        ok = s["train_acc"] >= 0.98
    if not ok:
        e = min(e, 0.0)
    q = e - penalty
    A = base["adamw"][task]
    adamw_ok = (A["mean"] - mP) >= 2.0 * A["sd"]
    wins = int(sum(p < gg for p, gg in zip(s["seed_metric"], g["seed_metric"])))
    out.update(m_P=mP, m_G=g["metric"], G=g["method"], e_confirm=float(e), q_confirm=float(q),
               constraint_ok=bool(ok), adamw_gate=bool(adamw_ok), paired_wins=wins,
               seed_metric=s["seed_metric"], G_seed_metric=g["seed_metric"])
    if task == "Cstar":
        out["return_ok_count"] = s["return_ok_count"]
    out["eligible"] = bool(ok and q >= Q_MIN and adamw_ok and wins >= MIN_WINS)
    return out


def select(cands: List[Dict]) -> List[Dict]:
    """cands: dicts with pid, task, eligible, q_confirm, family_sim.  Promotion order per v8."""
    elig = [c for c in cands if c["eligible"]]
    elig.sort(key=lambda c: (-c["q_confirm"], c.get("family_sim") or 0.0, c["pid"]))
    out, per_task = [], {}
    for c in elig:
        if per_task.get(c["task"], 0) >= PER_TASK_MAX:
            continue
        out.append(c)
        per_task[c["task"]] = per_task.get(c["task"], 0) + 1
        if len(out) >= N_PROMOTE_MAX:
            break
    return out
