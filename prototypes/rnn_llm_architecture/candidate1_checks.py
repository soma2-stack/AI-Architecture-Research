"""Candidate 1 (additive moment memory with algebraic recovery): small deterministic numerical checks. No training.

S_j = sum_i v_i z_i^j, j = 0..M-1, z_i on the unit circle. Checks:
  A. superposition indistinguishability: {(z,a),(z',b)} and {(z,b),(z',a)} have states that converge as z' -> z, while lookup answers differ;
  B. float64 ESPRIT recovery error for a 2-key cluster versus separation (expected amplitude-error growth ~ (M*delta)^-3);
  C. grid-key reduction: with keys at M-th roots of unity, S is the (unnormalised) DFT of an M-slot table and the inverse DFT reads it exactly;
  D. scalar work of one value-carrying insert grows linearly with M (and M >= K + ceil(K/d) for identifiability).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


def moments(z: np.ndarray, v: np.ndarray, M: int) -> np.ndarray:
    """S[j, :] = sum_i v[i, :] * z[i]**j  (v: [K, d])."""
    j = np.arange(M)[:, None]
    return (z[None, :] ** j) @ v


def esprit(S: np.ndarray, K: int):
    """Stable subspace (ESPRIT) recovery of K nodes and values from moments S [M, d]."""
    M, d = S.shape
    L = M // 2
    H = np.concatenate([np.stack([S[i:i + L, c] for i in range(M - L + 1)], 1) for c in range(d)], 1)   # [L, (M-L+1)*d]
    U, _, _ = np.linalg.svd(H, full_matrices=False)
    Us = U[:, :K]
    Phi = np.linalg.pinv(Us[:-1]) @ Us[1:]
    z = np.linalg.eigvals(Phi)
    V = z[None, :] ** np.arange(M)[:, None]
    v = np.linalg.lstsq(V, S, rcond=None)[0]
    return z, v


def check_A(M=32):
    z = np.exp(1j * 0.7)
    a, b = np.array([[1.0]]), np.array([[-1.0]])
    rows = []
    for delta in (1e-1, 1e-2, 1e-3, 1e-4, 1e-6):
        z2 = z * np.exp(1j * delta)
        S1 = moments(np.array([z, z2]), np.vstack([a, b]), M)
        S2 = moments(np.array([z, z2]), np.vstack([b, a]), M)
        rows.append({"delta": delta, "state_distance": float(np.linalg.norm(S1 - S2)), "answer_difference": float(abs(a - b).max())})
    return rows


def check_B(M=32, K=2, seed=0):
    """Relative value error of ESPRIT for a 2-key cluster vs separation, exact float64 moments and moments with float32-level relative noise."""
    rows = []
    for noise in (0.0, 6e-8):
        rng = np.random.default_rng(seed)
        for msep in (2.0, 1.0, 0.5, 0.25, 0.125, 1 / 16, 1 / 32, 1 / 64, 1 / 128):   # separation in units of 1/M
            errs = []
            for _ in range(20):
                th0 = rng.uniform(0, 2 * np.pi)
                th = np.array([th0, th0 + 2 * np.pi * msep / M])
                v = rng.normal(size=(K, 1)) + 1j * rng.normal(size=(K, 1))
                S = moments(np.exp(1j * th), v, M)
                S = S + noise * np.abs(S).max() * (rng.normal(size=S.shape) + 1j * rng.normal(size=S.shape))
                zh, vh = esprit(S, K)
                order = [int(np.argmin(np.abs(zh - np.exp(1j * t)))) for t in th]
                errs.append(np.inf if len(set(order)) < K else float(np.max(np.abs(vh[order] - v)) / np.max(np.abs(v))))
            rows.append({"relative_noise": noise, "separation_times_M": msep, "median_relative_value_error": float(np.median(errs)),
                         "fraction_failed_or_error_gt_1pct": float(np.mean([e > 1e-2 for e in errs]))})
    return rows


def check_C(M=16, d=3, seed=1):
    """Keys restricted to M-th roots of unity: S = M * IDFT(slot table), and the DFT reads every slot exactly."""
    rng = np.random.default_rng(seed)
    table = np.zeros((M, d), dtype=complex)
    slots = rng.choice(M, size=5, replace=False)
    table[slots] = rng.normal(size=(5, d))
    S = moments(np.exp(2j * np.pi * slots / M), table[slots], M)
    return {"max_abs_S_minus_M_times_IDFT_of_table": float(np.abs(S - M * np.fft.ifft(table, axis=0)).max()),
            "max_abs_DFT_read_minus_table": float(np.abs(np.fft.fft(S, axis=0) / M - table).max())}


def check_D():
    """Scalar complex multiply-adds for one value-carrying insert: (M-1) powers + M*d updates; M >= K + ceil(K/d)."""
    rows = []
    for K in (8, 64, 512):
        for d in (1, 32):
            M = K + -(-K // d)
            rows.append({"K": K, "d": d, "min_M_for_identifiability": M, "scalar_ops_per_insert": (M - 1) + M * d,
                         "slot_or_hash_value_copy": d})
    return rows


def main(argv=None):
    out = {"A_indistinguishability": check_A(), "B_esprit_cluster_error_float64": check_B(), "C_grid_reduction": check_C(), "D_edit_cost": check_D()}
    p = Path((argv or sys.argv[1:])[0])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
