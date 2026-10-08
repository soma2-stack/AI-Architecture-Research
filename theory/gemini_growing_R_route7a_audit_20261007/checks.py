"""Independent Hostile Verification Suite for GPT-6 Growing-R Route 7A
Author: Gemini (Cursor / Gemini Research Lane)
Date: 2026-10-07
"""

import math
import numpy as np


def test_algebra_and_trace_matching():
    """Verify exact 3-step row response and trace matching formula."""
    print("--- 1. Testing Exact 3-Step Row Response & Trace Matching ---")
    G = 0.9975
    E = 1e-4
    GH = 0.99999
    a = 1.0 - 1.0 / 1024

    for tau in [0.0, 0.1, 1.0, 10.0, 100.0]:
        for x in [-1.0, -0.5, 0.0, 0.5, 1.0]:
            d1 = G + E * x
            trgt = G * (1 + a * GH * (1 + a * G * (1 + a * tau)))
            mid = GH * (1 + a * d1 * (1 + a * tau))
            d3 = trgt / (1 + a * mid)

            # Update trace manually
            tau1 = d1 * (1 + a * tau)
            tau2 = GH * (1 + a * tau1)
            tau3 = d3 * (1 + a * tau2)

            gap = abs(tau3 - trgt)
            assert gap < 1e-13, f"Trace matching failed at tau={tau}, x={x}: gap={gap}"

    print("Trace matching verified: tau3 == trgt to machine precision.")
    return True


def test_stationary_compensator_zero_difference():
    """Verify stationary compensator rows cancel identically."""
    print("\n--- 2. Testing Stationary Compensator Row Cancellation ---")
    G = 0.9975
    E = 1e-4
    GH = 0.99999
    a = 1.0 - 1.0 / 1024
    tau = 2.5

    for x in [-1.0, 0.7]:
        for y in [0.2, -0.9]:
            # For stationary compensator, e1 = e2 = e3 = e_c
            # Initial row is tau * e_c
            d1_x = G + E * x
            d1_y = G + E * y

            trgt = G * (1 + a * GH * (1 + a * G * (1 + a * tau)))
            d3_x = trgt / (1 + a * GH * (1 + a * d1_x * (1 + a * tau)))
            d3_y = trgt / (1 + a * GH * (1 + a * d1_y * (1 + a * tau)))

            # Scalar row coefficient
            c_x = a**3 * GH * d1_x * d3_x * tau + a**2 * GH * d1_x * d3_x + a * GH * d3_x + d3_x
            c_y = a**3 * GH * d1_y * d3_y * tau + a**2 * GH * d1_y * d3_y + a * GH * d3_y + d3_y

            gap = abs(c_x - c_y)
            assert gap < 1e-13, f"Compensator row difference non-zero: gap={gap}"
            assert abs(c_x - trgt) < 1e-13

    print("Stationary compensator cancellation verified: Delta ell_comp == 0 identically.")
    return True


def test_analytical_constants_and_inequalities():
    """Verify contraction factor rho, discriminant inequality, and fresh perturbation bound."""
    print("\n--- 3. Testing Analytical Constants & Bounds ---")
    G = 0.9975
    E = 1e-4
    dmin = G - E
    LSTAR = (G / dmin) ** 2
    rho = (G + E) * (G**2) / (G - E)
    expected_rho = 0.995205770102266
    print(f"Computed rho = {rho:.12f}, Expected = {expected_rho:.12f}")
    assert abs(rho - expected_rho) < 1e-9
    assert rho < 1.0, "Contraction factor rho must be strictly < 1!"

    # Test quadratic inequality (1 + sqrt(tau)) / (1 + 0.99 tau) <= 5/4
    # Discriminant of 1.2375 v^2 - v + 0.25 is 1 - 4(1.2375)(0.25) = -0.2375 < 0
    disc = (-1.0)**2 - 4 * (1.25 * 0.99) * 0.25
    print(f"Quadratic discriminant = {disc:.6f} < 0")
    assert disc < 0.0

    # Numerical grid test over tau in [0, 1e8]
    tau_vals = np.logspace(-6, 8, 1000)
    ratios = (1.0 + np.sqrt(tau_vals)) / (1.0 + 0.99 * tau_vals)
    max_ratio = np.max(ratios)
    print(f"Max ratio over grid: {max_ratio:.8f} <= 1.25")
    assert max_ratio <= 1.25 + 1e-12

    # Fresh perturbation coefficient: LSTAR * ( (2 / 0.99^3) * 1.25 + sqrt(2) )
    fresh_coeff = LSTAR * ( (2.0 / (0.99**3)) * 1.25 + math.sqrt(2) )
    print(f"Fresh perturbation coefficient = {fresh_coeff:.8f} < 4.0: {fresh_coeff < 4.0}")
    assert fresh_coeff < 4.0

    # Uniform row bound: 8 * E / (1 - rho)
    row_bound = 8.0 * E / (1.0 - rho)
    print(f"Uniform row bound = {row_bound:.8f} < 0.16687: {row_bound < 0.16687}")
    assert row_bound < 0.16687

    # Query coefficient: sigma * row_bound
    sigma = 0.051
    query_coeff = sigma * row_bound
    print(f"Query coefficient = {query_coeff:.8f} < 0.00852: {query_coeff < 0.00852}")
    assert query_coeff < 0.00852

    # R >= 19 threshold
    # 0.00852 / sqrt(R) < 0.002 <=> sqrt(R) > 4.26 <=> R > 18.1476 <=> R >= 19
    r_thresh = (query_coeff / 0.002) ** 2
    print(f"Exact critical R threshold = {r_thresh:.6f} => integer ceiling = {math.ceil(r_thresh)}")
    assert math.ceil(r_thresh) <= 19
    assert query_coeff / math.sqrt(19) < 0.002
    assert query_coeff / math.sqrt(18) > 0.002

    print("Analytical constants and thresholds VERIFIED.")
    return True


def test_adversarial_control_simulations():
    """Stress test moving row differences with adversarial alternating controls and waits."""
    print("\n--- 4. Stress Testing Adversarial Controls & Long Waits ---")
    G = 0.9975
    E = 1e-4
    GH = 0.99999
    a = 1.0 - 1.0 / 1000000
    rho = (G + E) * (G**2) / (G - E)
    row_bound = 8.0 * E / (1.0 - rho)

    def run_sim(ctrls, waits):
        R = len(ctrls)
        row = []
        tau = 0.0
        def step(d):
            nonlocal tau
            row[:] = [val * a * d for val in row] + [d]
            tau = d * (1.0 + a * tau)

        # Precharge
        for _ in range(200):
            step(GH)

        for j in range(R):
            for _ in range(waits[j]):
                step(GH)
            incoming = tau
            d1 = G + E * ctrls[j]
            trgt = G * (1 + a * GH * (1 + a * G * (1 + a * incoming)))
            mid = GH * (1 + a * d1 * (1 + a * incoming))
            d3 = trgt / (1 + a * mid)
            step(d1)
            step(GH)
            step(d3)
        return np.array(row), tau

    rng = np.random.default_rng(20261007)
    for R in [1, 10, 50, 100, 200]:
        # Adversarial alternating signs
        cx = np.array([1.0 if i % 2 == 0 else -1.0 for i in range(R)])
        cy = -cx
        waits = rng.integers(0, 10, size=R)
        rx, tx = run_sim(cx, waits)
        ry, ty = run_sim(cy, waits)
        norm = np.linalg.norm(rx - ry)
        assert abs(tx - ty) < 1e-8
        assert norm < row_bound
        print(f"R={R:3d}: norm={norm:.6f} < bound={row_bound:.6f}")

    print("Adversarial simulations VERIFIED: all norms remain strictly bounded.")
    return True


if __name__ == '__main__':
    print("RUNNING GEMINI VERIFICATION SUITE FOR GPT-6 GROWING-R ROUTE 7A\n")
    test_algebra_and_trace_matching()
    test_stationary_compensator_zero_difference()
    test_analytical_constants_and_inequalities()
    test_adversarial_control_simulations()
    print("\n==========================================")
    print("ALL TESTS COMPLETED AND VERIFIED.")
    print("==========================================")
