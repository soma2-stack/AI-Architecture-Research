"""Statistics for Stage 3 (AE.4 gate 3; Cursor Tier 2)."""
from __future__ import annotations

from typing import Dict, List, Sequence

import numpy as np
from scipy import stats


def wilcoxon_greater(a: Sequence[float], b: Sequence[float]) -> float:
    """One-sided paired Wilcoxon signed-rank p-value for a > b."""
    d = np.asarray(a, float) - np.asarray(b, float)
    if np.allclose(d, 0):
        return 1.0
    return float(stats.wilcoxon(d, alternative="greater", zero_method="wilcox").pvalue)


def holm(pvals: Dict[str, float], alpha: float = 0.05) -> Dict[str, bool]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, stop = {}, False
    for i, (k, p) in enumerate(items):
        if stop or p > alpha / (m - i):
            stop = True
            out[k] = False
        else:
            out[k] = True
    return out


def bootstrap_ci(diffs: Sequence[float], n: int = 10000, seed: int = 0, level: float = 0.95):
    d = np.asarray(diffs, float)
    rng = np.random.default_rng(seed)
    means = rng.choice(d, (n, d.size), replace=True).mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(lo), float(hi)


def welch_p(a: Sequence[float], b: Sequence[float]) -> float:
    return float(stats.ttest_ind(a, b, equal_var=False).pvalue)
