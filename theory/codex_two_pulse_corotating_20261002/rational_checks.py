"""Exact rational scalar enclosure replay; not a matrix interval certificate."""
from fractions import Fraction as F
from math import factorial
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def cosh_bounds(x, N=24):
    lower = sum((x ** (2 * j) / factorial(2 * j) for j in range(N + 1)), F(0))
    first = x ** (2 * N + 2) / factorial(2 * N + 2)
    ratio = x ** 2 / ((2 * N + 3) * (2 * N + 4))
    return lower, lower + first / (1 - ratio)


def sech_squared_bounds(x):
    lo, hi = cosh_bounds(x)
    return 1 / hi ** 2, 1 / lo ** 2


def atanh_upper(x, N=40):
    partial = sum((x ** (2 * j + 1) / (2 * j + 1) for j in range(N + 1)), F(0))
    tail = x ** (2 * N + 3) / ((2 * N + 3) * (1 - x ** 2))
    return partial + tail


def run():
    gl = sech_squared_bounds(F(1, 2))
    gh = sech_squared_bounds(F(1, 4))
    sglo = (gh[0] - gl[1]) / 2
    exp3lo = sum((F(3) ** j / factorial(j) for j in range(40)), F(0))
    margin = F(32, 1000) * F(39601, 40000) * F(4751, 5000) * F(70710, 100000) * F(76, 1000)
    tests = {
        "sg_exceeds_076783": sglo > F(76783, 1000000),
        "derivative_positive_term_below_115": F(11, 9) * gh[1] < F(115, 100),
        "derivative_subtracted_term_above_157": 2 * gl[0] > F(157, 100),
        "m_over_n_exceeds_09502": 1 - 1 / exp3lo > F(4751, 5000),
        "sqrt_half_exceeds_070710": F(70710, 100000) ** 2 < F(1, 2),
        "uniform_reference_margin_exceeds_00161": margin > F(161, 100000),
        "atanh_pulse_plus_bias_below_04737": atanh_upper(F(2, 5)) + F(1, 20) < F(4737, 10000),
        "physical_radius_below_044": F(2, 25) * (F(25, 21) ** 2 + 1) < F(11, 25) ** 2,
        "reset_common_leak_below_0025": F(408, 100) < F(1, 40) ** 2 * 9 ** 4,
        "cycle_leak_below_0225": F(408, 100) < F(9, 40) ** 2 * 9 ** 2,
        "dense_error_bound_below_1e10": F(200) > F(64, 5) ** 2,
    }
    assert all(tests.values()), tests
    result = {"arithmetic": "Exact Python fractions plus explicit positive-series/tail bounds",
              "tests": tests, "count": len(tests), "sg_lower": str(sglo), "sg_lower_decimal": float(sglo),
              "reference_uniform_margin_lower": str(margin), "reference_uniform_margin_decimal": float(margin),
              "rejected_literal_handoff_claims": {
                  "displayed_rounded_product_is_at_least_0016181": bool(margin >= F(16181, 10000000)),
                  "a_at_n1000_is_at_most_0995": bool(1 - F(1, 1000) <= F(995, 1000))},
              "scope": "Scalar inequalities only; full-matrix numerics are separately labelled"}
    (HERE / "RATIONAL_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "sg_lower"}))


if __name__ == "__main__":
    run()
