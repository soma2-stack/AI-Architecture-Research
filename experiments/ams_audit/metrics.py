"""
Mathematical Metric Implementations for Automated Mechanism Search (AMS) Audit.
Directly implements Section 10 of AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md
and Part 4 of Cursor_Research.md.
"""

import numpy as np
from typing import List, Optional, Union


def area_under_learning_curve(accuracies: Union[List[float], np.ndarray]) -> float:
    """
    AULC = (1 / T_max) * sum_{t=1}^{T_max} Acc(t)
    Normalized integral of performance over the training horizon. Range in [0, 1].
    """
    accs = np.asarray(accuracies, dtype=np.float64)
    if len(accs) == 0:
        return 0.0
    return float(np.mean(accs))


def steps_to_threshold(losses: Union[List[float], np.ndarray], threshold: float) -> int:
    """
    S_tau = min { t | L(t) <= tau }, or inf (represented as -1 or max_int) if not reached.
    """
    for step, loss in enumerate(losses):
        if loss <= threshold:
            return step + 1
    return 10**9  # Not reached


def forgetting_percentage(task1_peak_acc: float, task1_post_acc: float) -> float:
    """
    F = ((Peak_Acc_1 - Post_Acc_1) / Peak_Acc_1) * 100%
    Relative loss of performance on Task 1 after training on Task 2.
    """
    if task1_peak_acc <= 1e-7:
        return 0.0
    forgetting = (task1_peak_acc - task1_post_acc) / task1_peak_acc
    return float(np.clip(forgetting * 100.0, 0.0, 100.0))


def backward_transfer(task1_initial: float, task1_final: float) -> float:
    """
    BWT = Acc_1(final) - Acc_1(initial)
    """
    return float(task1_final - task1_initial)


def forward_transfer(task2_initial: float, random_baseline: float) -> float:
    """
    FWT = Acc_2(0) - Acc_2_random(0)
    """
    return float(task2_initial - random_baseline)


def adaptation_half_life(losses: Union[List[float], np.ndarray], target_loss: float) -> int:
    """
    t_{1/2}^adapt = min { t | L_new(t) <= L_new(0) - 0.5 * (L_new(0) - target_loss) }
    Steps required to halve the error gap on a new distribution.
    """
    losses_arr = np.asarray(losses, dtype=np.float64)
    if len(losses_arr) == 0:
        return 10**9
    l0 = losses_arr[0]
    target_cutoff = l0 - 0.5 * (l0 - target_loss)
    for step, l in enumerate(losses_arr):
        if l <= target_cutoff:
            return step + 1
    return len(losses_arr)  # Did not reach half-life within window


def retention_half_life(retained_accs: Union[List[float], np.ndarray], initial_acc: float) -> int:
    """
    t_{1/2}^ret = min { t | Acc_1(t) <= 0.5 * Acc_1(0) }
    Steps of interfering task training before Task 1 drops to half its peak.
    """
    cutoff = 0.5 * initial_acc
    for step, acc in enumerate(retained_accs):
        if acc <= cutoff:
            return step + 1
    return 10**9  # Retained above half throughout


def compute_efficiency(delta_acc: float, gflops: float) -> float:
    """
    Eff_FLOP = delta_Acc / GFLOPs_cumulative
    """
    if gflops <= 1e-9:
        return 0.0
    return float(delta_acc / gflops)


def update_efficiency(loss_start: float, loss_end: float, n_updates: int) -> float:
    """
    Eff_update = (L(0) - L(K)) / K
    """
    if n_updates <= 0:
        return 0.0
    return float((loss_start - loss_end) / n_updates)


def stability_variance(losses: Union[List[float], np.ndarray], window_size: int = 10) -> float:
    """
    sigma_eval^2 across sliding evaluation windows under stationary conditions.
    """
    losses_arr = np.asarray(losses, dtype=np.float64)
    if len(losses_arr) < window_size:
        return float(np.var(losses_arr)) if len(losses_arr) > 0 else 0.0
    # Sliding window means
    window_means = [
        np.mean(losses_arr[i : i + window_size])
        for i in range(len(losses_arr) - window_size + 1)
    ]
    return float(np.var(window_means))


def structural_generalization_gap(train_acc: float, ood_acc: float) -> float:
    """
    SGG = Acc_train - Acc_OOD (in percentage points)
    Discrepancy between in-distribution shortcut fitting and out-of-distribution invariant generalization.
    """
    return float((train_acc - ood_acc) * 100.0)
