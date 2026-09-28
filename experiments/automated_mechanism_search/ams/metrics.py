"""Metrics (prereg v2 sec. 6 and sec. 10; Cursor suite formulas)."""
from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence

import numpy as np

CENSOR_HL = 128.0
AULC_KS = tuple(range(4, 65, 4))          # prereg v8: k in {4, 8, ..., 64}
AULC_FLOOR = 1e-8


def adaptation_area(eval_steps: Sequence[int], mse_R1: Sequence[float], entry: int, tau: float) -> float:
    """Prereg v8 per-entry normalized adaptation area
        A_e = mean_k max(MSE_R1(e+k) - tau, 0) / max(MSE_R1(e) - tau, 1e-8),  k in {4, 8, ..., 64}.
    No clipping beyond the floor at zero in the numerator."""
    steps = list(eval_steps)
    E = float(mse_R1[steps.index(entry)])
    den = max(E - tau, AULC_FLOOR)
    return float(np.mean([max(float(mse_R1[steps.index(entry + k)]) - tau, 0.0) / den for k in AULC_KS]))


def adaptation_aulc(eval_steps: Sequence[int], mse_R1: Sequence[float], entries: Sequence[int],
                    tau: float) -> float:
    """Prereg v8 seed-level Task-C* metric A_C = 0.5 * (A_first_R1 + A_second_R1); lower is better."""
    assert len(entries) == 2
    return 0.5 * (adaptation_area(eval_steps, mse_R1, entries[0], tau)
                  + adaptation_area(eval_steps, mse_R1, entries[1], tau))


def retention_B(L1_init: float, L1_pre: float, L1_post: float) -> float:
    """v2: 100 * clip(1 - (L1_post - L1_pre) / max(L1_init - L1_pre, 1e-8), 0, 1)."""
    r = 1.0 - (L1_post - L1_pre) / max(L1_init - L1_pre, 1e-8)
    return 100.0 * float(np.clip(r, 0.0, 1.0))


def forgetting_B(L1_init: float, L1_pre: float, L1_post: float) -> float:
    return 100.0 - retention_B(L1_init, L1_pre, L1_post)


def half_life(eval_steps: Sequence[int], mse: Sequence[float], entry: int, tau: float,
              seg_len: int = 64) -> float:
    """v2 C*: first update index k in (0, seg_len] at which MSE reaches the midpoint between
    the entry MSE and tau; 0 if already <= tau; +inf if never within the segment."""
    steps = list(eval_steps)
    i0 = steps.index(entry)
    m0 = float(mse[i0])
    if m0 <= tau:
        return 0.0
    mid = 0.5 * (m0 + tau)
    for s, v in zip(steps[i0 + 1:], mse[i0 + 1:]):
        if s - entry > seg_len:
            break
        if v <= mid:
            return float(s - entry)
    return math.inf


def median_hl(hls: Sequence[float]) -> float:
    return float(np.median(np.asarray(hls, float)))


def censor(x: float) -> float:
    return CENSOR_HL if not np.isfinite(x) else float(x)


def return_ok(mse_R0_pre: float, mse_R0_after: float) -> bool:
    return bool(mse_R0_after <= max(1.10 * mse_R0_pre, mse_R0_pre + 0.01))


def sgg(acc_train: float, acc_ood: float) -> float:
    """Structural generalization gap in percentage points."""
    return 100.0 * (acc_train - acc_ood)


# --- generic Cursor metrics -----------------------------------------------------------------

def aulc(acc: Sequence[float]) -> float:
    a = np.asarray(acc, float)
    return float(a.mean()) if a.size else float("nan")


def steps_to_threshold(loss: Sequence[float], tau: float, steps: Optional[Sequence[int]] = None) -> float:
    steps = list(range(len(loss))) if steps is None else list(steps)
    for s, v in zip(steps, loss):
        if v <= tau:
            return float(s)
    return math.inf


def forgetting_acc(acc1_curve: Sequence[float], t1_index: int) -> float:
    a = np.asarray(acc1_curve, float)
    peak = a[:t1_index + 1].max()
    return float(100.0 * (peak - a[-1]) / peak) if peak > 0 else float("nan")


def bwt(acc1_T1: float, acc1_end: float) -> float:
    return float(acc1_end - acc1_T1)


def fwt(acc2_at0: float, acc2_random_at0: float) -> float:
    return float(acc2_at0 - acc2_random_at0)


def retention_half_life(eval_steps: Sequence[int], perf1: Sequence[float], t1: int) -> float:
    steps = list(eval_steps)
    i0 = steps.index(t1)
    p0 = perf1[i0]
    for s, v in zip(steps[i0:], perf1[i0:]):
        if v <= 0.5 * p0:
            return float(s - t1)
    return math.inf


def eff_flop(delta_acc: float, gflops: float) -> float:
    return float(delta_acc / gflops) if gflops > 0 else float("nan")


def eff_update(L0: float, LK: float, K: int) -> float:
    return float((L0 - LK) / K) if K > 0 else float("nan")


def stability_variance(losses: Sequence[float], window: int = 5) -> float:
    x = np.asarray(losses, float)
    if x.size < window:
        return float("nan")
    w = np.array([x[i:i + window].mean() for i in range(0, x.size - window + 1, window)])
    return float(np.mean((w - w.mean()) ** 2))


def r2_perf(mse: float, trivial: float) -> float:
    """Accuracy-like performance for regression: clip(1 - MSE/trivial, 0, 1)."""
    return float(np.clip(1.0 - mse / trivial, 0.0, 1.0)) if trivial > 0 else float("nan")
