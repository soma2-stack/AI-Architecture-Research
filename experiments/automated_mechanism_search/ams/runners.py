"""Task runners: vectorized training of (seed x learning-rate) configurations, metric
extraction and training-side learning-rate selection (IMPLEMENTATION_DECISIONS D-LR)."""
from __future__ import annotations

import math
import time
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import metrics as MX
from .substrate import (DT, AdamW, Learner, Net, OutOfMemory, SGD, SGDM, Timeout, Trainer,
                        learner_flops_per_example)
from .tasks import TaskB, TaskCstar, TaskD, TaskF, TaskT0

LR_GRID = (1e-3, 1e-2, 1e-1)
TIME_PER_SEED = 120.0


def _runs(seeds: Sequence[int], lrs: Sequence[float]) -> List[Tuple[int, float]]:
    return [(int(s), float(lr)) for s in seeds for lr in lrs]


def _stack(batches: Dict[int, Tuple[np.ndarray, np.ndarray]], runs) -> Tuple[np.ndarray, np.ndarray]:
    X = np.stack([batches[s][0] for s, _ in runs])
    Y = np.stack([batches[s][1] for s, _ in runs])
    return X, Y


def _mse_eval(tr: Trainer, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    with np.errstate(all="ignore"):
        out = tr.predict(X)
        return np.mean((out - Y) ** 2, axis=(1, 2)).astype(np.float64)


def _fail_record(runs, reason: str) -> Dict:
    return {"runs": runs, "error": reason, "unstable": [True] * len(runs), "reason": [reason] * len(runs)}


# ---------------------------------------------------------------------------
# Task B
# ---------------------------------------------------------------------------

def run_B(make_learner: Callable[[], Learner], seeds: Sequence[int], lrs=LR_GRID,
          hook: Optional[Callable] = None, inner: int = 1, hidden: int = 32,
          time_limit: Optional[float] = None) -> Dict:
    runs = _runs(seeds, lrs)
    tasks = {s: TaskB(s) for s in seeds}
    net = Net(TaskB.d_in, TaskB.d_out, [s for s, _ in runs], hidden=hidden)
    L = make_learner()
    tl = TIME_PER_SEED * len(seeds) * inner if time_limit is None else time_limit
    tr = Trainer(net, L, [lr for _, lr in runs], kind="reg", time_limit=tl)
    tr.set_episodes(TaskB.n1)
    tr.episode_start()
    X1 = np.stack([tasks[s].X1_eval for s, _ in runs]); Y1 = np.stack([tasks[s].Y1_eval for s, _ in runs])
    X2 = np.stack([tasks[s].X2_eval for s, _ in runs]); Y2 = np.stack([tasks[s].Y2_eval for s, _ in runs])
    ev_steps, L1c, L2c = [0], [_mse_eval(tr, X1, Y1)], [_mse_eval(tr, X2, Y2)]
    train_mse = np.zeros((TaskB.n1 + TaskB.n2, len(runs)))
    try:
        for t in range(TaskB.n1 + TaskB.n2):
            if t == TaskB.n1:
                tr.episode_start()
            if hook is not None:
                hook(tr, t, "B")
            batches = {s: tasks[s].train_batch(t) for s in seeds}
            X, Y = _stack(batches, runs)
            for _ in range(inner):
                _, _, e = tr.step(X, Y)
            train_mse[t] = np.mean(e.astype(np.float64) ** 2, axis=(1, 2))
            if (t + 1) % TaskB.eval_every == 0:
                ev_steps.append(t + 1)
                L1c.append(_mse_eval(tr, X1, Y1))
                L2c.append(_mse_eval(tr, X2, Y2))
    except (Timeout, OutOfMemory) as ex:
        return _fail_record(runs, type(ex).__name__.upper())
    L1c, L2c = np.stack(L1c), np.stack(L2c)
    i_pre, i_post = ev_steps.index(TaskB.n1), len(ev_steps) - 1
    res = {"task": "B", "runs": runs, "eval_steps": ev_steps, "L1": L1c.T.tolist(), "L2": L2c.T.tolist(),
           "unstable": (~tr.alive).tolist(), "reason": tr.reason, "updates_applied": tr.updates_applied}
    per = []
    for r in range(len(runs)):
        Li, Lp, Lq = L1c[0, r], L1c[i_pre, r], L1c[i_post, r]
        per.append({
            "L1_init": float(Li), "L1_pre": float(Lp), "L1_post": float(Lq),
            "retention": MX.retention_B(Li, Lp, Lq), "forgetting": MX.forgetting_B(Li, Lp, Lq),
            "T2_final_mse": float(L2c[i_post, r]), "T2_init_mse": float(L2c[i_pre, r]),
            "train_select": float(train_mse[TaskB.n1 - 50:TaskB.n1, r].mean() + train_mse[-50:, r].mean()),
            "stability_var_T1": MX.stability_variance(L1c[:i_pre + 1, r]),
            "eff_update_T1": MX.eff_update(Li, Lp, TaskB.n1),
        })
    res["per_run"] = per
    return res


# ---------------------------------------------------------------------------
# Task C*
# ---------------------------------------------------------------------------

def run_C(make_learner: Callable[[], Learner], seeds: Sequence[int], lrs=LR_GRID,
          hook: Optional[Callable] = None, inner: int = 1, hidden: int = 32,
          time_limit: Optional[float] = None) -> Dict:
    runs = _runs(seeds, lrs)
    tasks = {s: TaskCstar(s) for s in seeds}
    net = Net(1, 1, [s for s, _ in runs], hidden=hidden)
    L = make_learner()
    tl = TIME_PER_SEED * len(seeds) * inner if time_limit is None else time_limit
    tr = Trainer(net, L, [lr for _, lr in runs], kind="reg", time_limit=tl)
    tr.set_episodes(None)
    tr.episode_start()
    G = np.stack([tasks[s].grid for s, _ in runs])
    Y0 = np.stack([tasks[s].Y_grid["R0"] for s, _ in runs])
    Y1 = np.stack([tasks[s].Y_grid["R1"] for s, _ in runs])
    n = TaskCstar(seeds[0]).n_steps
    ev, m0, m1 = [0], [_mse_eval(tr, G, Y0)], [_mse_eval(tr, G, Y1)]
    sq = np.zeros((n, len(runs)))
    try:
        for t in range(n):
            if hook is not None:
                hook(tr, t, "Cstar")
            batches = {s: tasks[s].train_batch(t) for s in seeds}
            X, Y = _stack(batches, runs)
            for _ in range(inner):
                _, _, e = tr.step(X, Y)
            sq[t] = np.mean(e.astype(np.float64) ** 2, axis=(1, 2))
            if (t + 1) % TaskCstar.eval_every == 0:
                ev.append(t + 1)
                m0.append(_mse_eval(tr, G, Y0))
                m1.append(_mse_eval(tr, G, Y1))
    except (Timeout, OutOfMemory) as ex:
        return _fail_record(runs, type(ex).__name__.upper())
    m0, m1 = np.stack(m0), np.stack(m1)
    entries = [t for r, t in TaskCstar(seeds[0]).entries if r == "R1"]     # [256, 384]
    per = []
    for r in range(len(runs)):
        hls = [MX.half_life(ev, m1[:, r], e, TaskCstar.tau) for e in entries]
        pre = float(m0[ev.index(256), r])
        after = float(m0[ev.index(384), r])
        per.append({
            "half_lives": hls, "median_hl": MX.median_hl(hls),
            "median_hl_censored": MX.median_hl([MX.censor(h) for h in hls]),
            "R1_entry_mse": [float(m1[ev.index(e), r]) for e in entries],
            "R0_pre_shift": pre, "R0_after_return": after, "return_ok": MX.return_ok(pre, after),
            "train_select": float(sq[:, r].mean()),
        })
    return {"task": "Cstar", "runs": runs, "eval_steps": ev, "R0": m0.T.tolist(), "R1": m1.T.tolist(),
            "unstable": (~tr.alive).tolist(), "reason": tr.reason, "per_run": per,
            "omega_phi": {s: (tasks[s].omega1, tasks[s].phi1) for s in seeds},
            "updates_applied": tr.updates_applied}


# ---------------------------------------------------------------------------
# Task F
# ---------------------------------------------------------------------------

def _cls_eval(tr: Trainer, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    with np.errstate(all="ignore"):
        out = tr.predict(X).astype(np.float64)
        acc = (out.argmax(-1) == y).mean(axis=1)
        z = out - out.max(-1, keepdims=True)
        lp = z - np.log(np.exp(z).sum(-1, keepdims=True))
        ce = -np.take_along_axis(lp, y[..., None], -1)[..., 0].mean(axis=1)
    return acc, ce


def run_F(make_learner: Callable[[], Learner], seeds: Sequence[int], lrs=LR_GRID,
          hook: Optional[Callable] = None, inner: int = 1, hidden: int = 32,
          time_limit: Optional[float] = None) -> Dict:
    runs = _runs(seeds, lrs)
    tasks = {s: TaskF(s) for s in seeds}
    net = Net(20, 2, [s for s, _ in runs], hidden=hidden)
    L = make_learner()
    tl = TIME_PER_SEED * len(seeds) * inner if time_limit is None else time_limit
    tr = Trainer(net, L, [lr for _, lr in runs], kind="cls", time_limit=tl)
    tr.set_episodes(None)
    tr.episode_start()
    Xtr = np.stack([tasks[s].Xtr for s, _ in runs]); ytr = np.stack([tasks[s].ytr for s, _ in runs])
    Xo = np.stack([tasks[s].Xood for s, _ in runs]); yo = np.stack([tasks[s].yood for s, _ in runs])
    a, c = _cls_eval(tr, Xtr, ytr)
    ao, _ = _cls_eval(tr, Xo, yo)
    ev, acc_tr, ce_tr, acc_o = [0], [a], [c], [ao]
    try:
        for t in range(TaskF.n_updates):
            if hook is not None:
                hook(tr, t, "F")
            batches = {s: tasks[s].train_batch(t) for s in seeds}
            X, Y = _stack(batches, runs)
            for _ in range(inner):
                tr.step(X, Y)
            if (t + 1) % TaskF.eval_every == 0:
                a, c = _cls_eval(tr, Xtr, ytr)
                ao, _ = _cls_eval(tr, Xo, yo)
                ev.append(t + 1); acc_tr.append(a); ce_tr.append(c); acc_o.append(ao)
    except (Timeout, OutOfMemory) as ex:
        return _fail_record(runs, type(ex).__name__.upper())
    acc_tr, ce_tr, acc_o = np.stack(acc_tr), np.stack(ce_tr), np.stack(acc_o)
    per = []
    for r in range(len(runs)):
        per.append({"train_acc": float(acc_tr[-1, r]), "ood_acc": float(acc_o[-1, r]),
                    "sgg": MX.sgg(acc_tr[-1, r], acc_o[-1, r]), "train_ce": float(ce_tr[-1, r]),
                    "aulc_train": MX.aulc(acc_tr[:, r]), "aulc_ood": MX.aulc(acc_o[:, r]),
                    "train_select": float(acc_tr[-1, r]), "train_select_tie": float(ce_tr[-1, r])})
    return {"task": "F", "runs": runs, "eval_steps": ev, "train_acc": acc_tr.T.tolist(),
            "ood_acc": acc_o.T.tolist(), "unstable": (~tr.alive).tolist(), "reason": tr.reason,
            "per_run": per, "updates_applied": tr.updates_applied}


# ---------------------------------------------------------------------------
# Task T0 sanity filter
# ---------------------------------------------------------------------------

def run_T0(make_learner: Callable[[], Learner], seed: int = 500, lrs=LR_GRID,
           time_limit: float = TIME_PER_SEED) -> Dict:
    runs = _runs([seed], lrs)
    task = TaskT0(seed)
    net = Net(8, 2, [seed] * len(lrs))
    tr = Trainer(net, make_learner(), list(lrs), kind="reg", time_limit=time_limit)
    tr.set_episodes(None)
    tr.episode_start()
    n = TaskT0.n_steps
    sq = np.zeros((n, len(lrs)))
    triv = np.zeros(n)
    ymean = np.zeros(2)
    try:
        for t in range(n):
            x, y = task.train_batch(t)
            triv[t] = float(np.mean((y[0] - ymean) ** 2))
            ymean = ymean + (y[0] - ymean) / (t + 1)
            X = np.repeat(x[None], len(lrs), 0); Y = np.repeat(y[None], len(lrs), 0)
            _, _, e = tr.step(X, Y)
            sq[t] = np.mean(e.astype(np.float64) ** 2, axis=(1, 2))
            if t + 1 == n // 2:
                # AE.3.6 early stop (T0 only): loss still >= trivial at 50% of steps
                recent = sq[max(0, t - 49):t + 1].mean(0)
                if np.all((recent >= triv[max(0, t - 49):t + 1].mean()) | ~tr.alive):
                    return {"pass": False, "reason": "no_learning_early_stop", "runs": runs}
    except (Timeout, OutOfMemory) as ex:
        return {"pass": False, "reason": type(ex).__name__.upper(), "runs": runs}
    fin = sq[-50:].mean(0)
    tv = triv[-50:].mean()
    ok = [(bool(tr.alive[k]) and fin[k] <= 0.5 * tv) for k in range(len(lrs))]
    return {"pass": any(ok), "final_mse": fin.tolist(), "trivial": float(tv), "alive": tr.alive.tolist(),
            "reason": "" if any(ok) else ("unstable" if not tr.alive.any() else "no_learning"), "runs": runs}


# ---------------------------------------------------------------------------
# Task D (baseline-only)
# ---------------------------------------------------------------------------

def run_D(method: str, seeds: Sequence[int], kappa: float, lrs=LR_GRID) -> Dict:
    out = []
    for s in seeds:
        task = TaskD(s, kappa)
        L0 = task.loss(task.theta0)
        for lr in lrs:
            th = task.theta0.copy()
            m = np.zeros_like(th); v = np.zeros_like(th); vel = np.zeros_like(th)
            Hinv = np.linalg.inv(task.H + 1e-3 * np.eye(task.d)) if method == "natgrad" else None
            s_tau, diverged, losses = math.inf, False, []
            for t in range(1, TaskD.n_steps + 1):
                g = task.grad(th)
                if method == "SGD":
                    th = th - lr * g
                elif method == "SGDM":
                    vel = 0.9 * vel + g
                    th = th - lr * vel
                elif method == "AdamW":
                    m = 0.9 * m + 0.1 * g
                    v = 0.999 * v + 0.001 * g * g
                    th = th - lr * ((m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8) + 0.01 * th)
                elif method == "natgrad":
                    th = th - lr * (Hinv @ g)
                else:
                    raise ValueError(method)
                Lt = task.loss(th)
                losses.append(Lt)
                if not np.isfinite(Lt) or Lt > 10 * L0:
                    diverged = True
                    break
                if Lt <= TaskD.tau and not np.isfinite(s_tau):
                    s_tau = float(t)
            out.append({"seed": s, "lr": lr, "S_tau": s_tau, "diverged": diverged,
                        "final_loss": float(losses[-1]) if losses else float("nan"), "L0": L0})
    return {"task": "D", "method": method, "kappa": kappa, "runs": out}


# ---------------------------------------------------------------------------
# learning-rate selection
# ---------------------------------------------------------------------------

def select_lr(res: Dict, seeds: Sequence[int], lrs=LR_GRID) -> Dict:
    """Training-side selection (D-LR-1).  Returns the chosen lr, its per-seed records, and
    whether every configuration was unstable."""
    if res.get("error"):
        return {"lr": None, "per_seed": [], "all_unstable": True, "error": res["error"]}
    runs = res["runs"]
    idx = {(s, lr): k for k, (s, lr) in enumerate(runs)}
    task = res["task"]
    best, best_key = None, None
    table = {}
    for lr in lrs:
        ks = [idx[(s, lr)] for s in seeds]
        if any(res["unstable"][k] for k in ks):
            table[lr] = None
            continue
        vals = [res["per_run"][k]["train_select"] for k in ks]
        if task == "F":
            ties = [res["per_run"][k]["train_select_tie"] for k in ks]
            key = (-float(np.mean(vals)), float(np.mean(ties)))
        else:
            key = (float(np.mean(vals)), 0.0)
        table[lr] = key
        if best_key is None or key < best_key:
            best, best_key = lr, key
    if best is None:
        return {"lr": None, "per_seed": [], "all_unstable": True, "table": {str(k): v for k, v in table.items()}}
    per_seed = [res["per_run"][idx[(s, best)]] for s in seeds]
    return {"lr": best, "per_seed": per_seed, "all_unstable": False,
            "table": {str(k): v for k, v in table.items()}}


def summarize(task: str, sel: Dict) -> Dict:
    """Seed-mean task metrics at the selected learning rate."""
    if sel["all_unstable"]:
        return {"stable": False}
    ps = sel["per_seed"]
    if task == "B":
        return {"stable": True, "lr": sel["lr"],
                "forgetting": float(np.mean([p["forgetting"] for p in ps])),
                "retention": float(np.mean([p["retention"] for p in ps])),
                "T2_final_mse": float(np.mean([p["T2_final_mse"] for p in ps])),
                "L1_pre": float(np.mean([p["L1_pre"] for p in ps])),
                "L1_post": float(np.mean([p["L1_post"] for p in ps])),
                "L1_init": float(np.mean([p["L1_init"] for p in ps])),
                "forgetting_seeds": [p["forgetting"] for p in ps],
                "L1_post_gt_pre_all": all(p["L1_post"] > p["L1_pre"] for p in ps)}
    if task == "Cstar":
        return {"stable": True, "lr": sel["lr"],
                "hl_censored_mean": float(np.mean([p["median_hl_censored"] for p in ps])),
                "hl_seeds": [p["median_hl"] for p in ps],
                "hl_censored_seeds": [p["median_hl_censored"] for p in ps],
                "return_ok_count": int(sum(p["return_ok"] for p in ps)),
                "R0_pre_shift": float(np.mean([p["R0_pre_shift"] for p in ps])),
                "R1_entry_mse_min": float(np.min([min(p["R1_entry_mse"]) for p in ps])),
                "R1_entry_mse": [p["R1_entry_mse"] for p in ps]}
    if task == "F":
        return {"stable": True, "lr": sel["lr"],
                "train_acc": float(np.mean([p["train_acc"] for p in ps])),
                "ood_acc": float(np.mean([p["ood_acc"] for p in ps])),
                "sgg": float(np.mean([p["sgg"] for p in ps])),
                "ood_err_seeds": [1 - p["ood_acc"] for p in ps],
                "train_acc_seeds": [p["train_acc"] for p in ps]}
    raise ValueError(task)


RUNNERS = {"B": run_B, "Cstar": run_C, "F": run_F}


def first_layer_grad(net: Net, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Gradient of the batch-mean 1/2||e||^2 loss w.r.t. the first-layer weight matrix of
    run 0 of `net` (plain MLP backprop, float64)."""
    Ws = [w[0].astype(np.float64) for w in net.W]
    bs = [b[0].astype(np.float64) for b in net.b]
    a = [X.astype(np.float64)]
    for l in range(len(Ws)):
        z = a[-1] @ Ws[l].T + bs[l]
        a.append(np.tanh(z) if l < len(Ws) - 1 else z)
    d = (a[-1] - Y) / X.shape[0]
    for l in range(len(Ws) - 1, 0, -1):
        d = (d @ Ws[l]) * (1 - a[l] ** 2)
    return d.T @ a[0]


def taskB_gate(seed: int) -> Dict:
    """Stage-0 v2 Task-B gradient-conflict gate (D-TASK-B-GATE)."""
    task = TaskB(seed)
    net = Net(TaskB.d_in, TaskB.d_out, [seed])
    cs = []
    for X1, Y1, X2, Y2 in task.gate_pairs():
        g1 = first_layer_grad(net, X1, Y1).ravel()
        g2 = first_layer_grad(net, X2, Y2).ravel()
        cs.append(float(g1 @ g2 / (np.linalg.norm(g1) * np.linalg.norm(g2))))
    return {"seed": seed, "n_pairs": len(cs), "mean_cos": float(np.mean(cs)),
            "min_cos": float(np.min(cs)), "max_cos": float(np.max(cs)), "cosines": cs,
            "pass": bool(np.mean(cs) <= -0.50)}
