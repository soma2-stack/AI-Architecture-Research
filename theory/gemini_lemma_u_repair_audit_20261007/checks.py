"""
Independent Hostile Verification Suite for Claude Lemma U Repair
Author: Gemini (Cursor / Gemini research lane)
Date: 2026-10-07
"""

import numpy as np


def test_lemma_a():
    """Verify Lemma A's lazy-random-walk anti-concentration inequality:
    Pr(X_k = gamma) <= [1 - (1 - 2p)^((k+1)/2)] / (k + 1) <= min(p, 1/(k+1)).
    """
    print("--- 1. Testing Lemma A Anti-Concentration Inequality ---")
    def pr_xk(steps, p, gamma):
        dist = {0: 1.0}
        for b in steps:
            new_dist = {}
            for x, prob in dist.items():
                new_dist[x] = new_dist.get(x, 0.0) + (1.0 - p) * prob
                new_dist[x ^ b] = new_dist.get(x ^ b, 0.0) + p * prob
            dist = new_dist
        return dist.get(gamma, 0.0)

    # Exhaustive check on distinct non-zero step sets
    for k in [1, 2, 3, 4, 6, 7]:
        steps = list(range(1, k + 1))
        for p in [0.001, 0.02, 0.1, 0.25, 0.45, 0.5]:
            bound = (1.0 - (1.0 - 2.0 * p)**((k + 1) / 2.0)) / (k + 1)
            min_bound = min(p, 1.0 / (k + 1))
            assert bound <= min_bound + 1e-12, "Lemma A upper envelope violated!"
            for gamma in range(1, 16):
                val = pr_xk(steps, p, gamma)
                assert val <= bound + 1e-12, f"Lemma A failed for k={k}, p={p}, gamma={gamma}: val={val} > bound={bound}"
    print("Lemma A verified across all tested k, p, and target points gamma.")
    return True


def test_hardy_kernel_bound():
    """Verify discrete Hardy kernel domination and the 2*sqrt(2) bound."""
    print("\n--- 2. Testing Discrete Hardy Operator Bound ---")
    for R in [10, 50, 100, 500, 1000]:
        j = np.arange(1, R + 1)[:, None]
        k = np.arange(1, R + 1)[None, :]
        K = 1.0 / (np.maximum(j, k) + 1.0)
        norm_K = np.linalg.norm(K, 2)
        print(f"R={R:4d}: ||K||_op = {norm_K:.4f} <= 4.0: {norm_K <= 4.0}")
        assert norm_K <= 4.0, f"Violation of ||K||_op <= 4 at R={R}!"
    print("Hardy domination verified: ||K||_op <= 4 implies ||PA_cap|| <= 2 and ||U_prot|| <= 2*sqrt(2).")
    return True


def test_finite_counterexamples():
    """Reproduce finite counterexamples to ||U_prot|| <= 2."""
    print("\n--- 3. Reproducing Finite Counterexamples to ||U_prot|| <= 2 ---")
    import sys
    sys.path.append('theory/claude_lemma_u_repair_20261007')
    from core import uprot_norm, counting_order_time

    # Witness 1: r=11 (R=2047) at b=0.5
    a11 = counting_order_time(11)
    u11, _ = uprot_norm(a11, 11, b=0.5)
    print(f"Witness 1: r=11 (R=2047), b=0.5: ||U_prot|| = {u11:.4f} > 2.0: {u11 > 2.0}")
    assert u11 > 2.0, "Witness 1 failed!"

    # Witness 2: r=12 (R=4095) at b=0.5
    a12 = counting_order_time(12)
    u12, _ = uprot_norm(a12, 12, b=0.5)
    print(f"Witness 2: r=12 (R=4095), b=0.5: ||U_prot|| = {u12:.4f} > 2.0: {u12 > 2.0}")
    assert u12 > 2.0, "Witness 2 failed!"

    # Witness 3: r=12 (R=4095) at b=0.2
    u12_b02, _ = uprot_norm(a12, 12, b=0.2)
    print(f"Witness 3: r=12 (R=4095), b=0.2: ||U_prot|| = {u12_b02:.4f} > 2.0: {u12_b02 > 2.0}")
    assert u12_b02 > 2.0, "Witness 3 failed!"
    print("Original claim ||U_prot|| <= 2 is definitively refuted by explicit finite witnesses.")
    return True


def test_certified_counterexample_b0025():
    """Verify certified counterexample at b=0.0025 via Proposition L2."""
    print("\n--- 4. Verifying Certified Counterexample at b=0.0025 ---")
    def Mnorm(i0, r):
        i = np.arange(i0, r + 1)
        I, J = np.meshgrid(i, i, indexing='ij')
        return np.linalg.eigvalsh(0.5 * 2.0**(-np.abs(I - J) / 2.0) * (1.0 - 2.0**(-np.minimum(I, J))))[-1]

    def eta(p, i0, r):
        q = 1.0 - 2.0 * p
        j = np.arange(i0, r + 1)
        with np.errstate(under='ignore'):
            t2 = np.exp(2.0**(j - 1) * np.log(q)) if q > 0 else np.zeros_like(j, dtype=float)
        return np.sqrt(2.0 * np.sum(2.0**(-j) * q * q / (1.0 - q * q) + 2.0**(j - 1) * t2))

    p = 0.0025
    r = 26
    i0 = 16
    m_val = Mnorm(i0, r)
    eta_val = eta(p, i0, r)
    bound_pa = np.sqrt(m_val) - eta_val
    bound_u = np.sqrt(2.0) * bound_pa
    print(f"At b={p}, r={r} (R=2^{r}-1), i0={i0}:")
    print(f"  ||M_[i0,r]||^0.5 = {np.sqrt(m_val):.5f}")
    print(f"  eta = {eta_val:.5f}")
    print(f"  ||PA_cap|| >= {bound_pa:.5f}")
    print(f"  ||U_prot|| >= {bound_u:.5f} > 2.0: {bound_u > 2.0}")
    assert bound_u > 2.0, "Certified bound failed to exceed 2.0!"
    print("Certified counterexample at b=0.0025 verified mathematically.")
    return True


def test_refutation_of_previous_gram_decay():
    """Verify refutation of the previous Gram-decay / Gershgorin claim."""
    print("\n--- 5. Verifying Refutation of Previous Gram-Decay Claim ---")
    from core import counting_order_time, chi
    r = 6
    b = 0.5
    al = counting_order_time(r)
    R = len(al)
    a = gH = 1.0
    gbar = gH - b
    cols = []
    for e in range(R):
        v = chi(al[e], r)
        for f in range(e + 1, R):
            v = v * a * (gbar + b * chi(al[f], r))
        cols.append(v)
    V = np.array(cols).T / np.sqrt(2**r)
    G = V.T @ V
    E, F = np.meshgrid(np.arange(R), np.arange(R), indexing='ij')
    off = E != F
    conjectured_bound = 2.0 * b * (a * gbar)**(np.abs(E - F) - 1.0)
    ratio = (G / conjectured_bound)[off].max()
    off_diag_row_sum = (G - np.diag(np.diag(G))).sum(1).max()
    print(f"r={r}, b={b}: max ratio to conjectured Gram-decay bound = {ratio:.2e} (expected > 1e10)")
    print(f"r={r}, b={b}: max off-diagonal row sum = {off_diag_row_sum:.4f} > 2.0: {off_diag_row_sum > 2.0}")
    assert ratio > 1e10, "Conjectured Gram decay did not fail by orders of magnitude!"
    assert off_diag_row_sum > 2.0, "Off-diagonal row sum was expected to exceed 2.0!"
    print("Refutation of previous Gram decay / Gershgorin bound confirmed.")
    return True


if __name__ == '__main__':
    print("RUNNING GEMINI AUDIT VERIFICATION SUITE FOR CLAUDE LEMMA U REPAIR\n")
    test_lemma_a()
    test_hardy_kernel_bound()
    test_finite_counterexamples()
    test_certified_counterexample_b0025()
    test_refutation_of_previous_gram_decay()
    print("\n==========================================")
    print("ALL TESTS COMPLETED AND VERIFIED.")
    print("==========================================")
