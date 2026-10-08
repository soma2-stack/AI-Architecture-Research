"""Pins the numerical claims of CANDIDATE1_FALSIFICATION.md (fast, deterministic)."""
import numpy as np

from prototypes.rnn_llm_architecture import candidate1_checks as c1


def test_superposition_indistinguishability_theorem_A():
    rows = c1.check_A()
    d = [r["state_distance"] for r in rows]
    assert all(a > b for a, b in zip(d, d[1:])) and d[-1] < 1e-3
    assert all(r["answer_difference"] == 2.0 for r in rows)
    # linear shrinkage: distance ratio ~ delta ratio
    assert abs(rows[3]["state_distance"] / rows[2]["state_distance"] - 0.1) < 0.01


def test_grid_keys_reduce_to_dft_of_slot_table():
    r = c1.check_C()
    assert r["max_abs_S_minus_M_times_IDFT_of_table"] < 1e-12 and r["max_abs_DFT_read_minus_table"] < 1e-12


def test_exact_recovery_when_separated_and_esprit_correct():
    rng = np.random.default_rng(3)
    z = np.exp(1j * np.array([0.3, 1.9, 4.0]))
    v = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))
    zh, vh = c1.esprit(c1.moments(z, v, 12), 3)
    order = [int(np.argmin(np.abs(zh - t))) for t in z]
    assert np.abs(vh[order] - v).max() < 1e-10


def test_cluster_error_grows_and_fails_under_float32_noise():
    rows = [r for r in c1.check_B() if r["relative_noise"] > 0]
    errs = [r["median_relative_value_error"] for r in rows]
    assert all(b > a for a, b in zip(errs[2:], errs[3:]))           # monotone growth once below ~1/(2M)
    assert errs[-1] > 1e-2 and rows[-1]["fraction_failed_or_error_gt_1pct"] >= 0.5


def test_edit_cost_scales_with_K():
    rows = c1.check_D()
    for r in rows:
        assert r["min_M_for_identifiability"] >= r["K"] + 1 and r["scalar_ops_per_insert"] >= r["K"] * r["d"]
