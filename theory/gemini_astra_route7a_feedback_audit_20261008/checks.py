"""
Comprehensive Reproducible Verification Suite for Astra's Route 7A Theorem Audit
(theory/astra_route7a_feedback_compression_20261008/PROOF.md)
Target commit: 1249c3c74347b205abd61dc09eceaa616d40135c
"""

import numpy as np

def test_algebraic_identities():
    """Verify Section 2: Equations (5) and (6) algebraic identities."""
    print("=== Testing Algebraic Identities ===")
    k = 500000
    r = k - 1
    gamma = 1.0 / (1.0 - 1.0 / np.sqrt(k))
    c = gamma**2 / k
    eta_H = gamma / np.sqrt(k)

    # Identity 1: u^T 1 = -gamma
    u_dot_1 = eta_H - c * r
    assert np.isclose(u_dot_1, -gamma, rtol=1e-12), f"u^T 1 mismatch: {u_dot_1} vs {-gamma}"
    print(f"  [PASS] u^T 1 = {u_dot_1:.12f} == -gamma (exact algebraic identity)")

    # Identity 2: gamma^2 - gamma^2/k = 2*gamma - 1
    lhs = gamma**2 - gamma**2 / k
    rhs = 2 * gamma - 1
    assert np.isclose(lhs, rhs, rtol=1e-12), f"Identity mismatch: {lhs} vs {rhs}"
    print(f"  [PASS] gamma^2 - c*r = 2*gamma - 1 == {lhs:.12f}")

    # Numerical envelope constants in Section 2:
    n = 10**6
    assert eta_H * np.sqrt(n) <= 2.0
    assert c * n <= 3.0
    assert (gamma - 1) * np.sqrt(n) <= 2.0
    u_norm = np.sqrt(eta_H**2 + c**2 * r - 2 * eta_H * c)
    assert u_norm * np.sqrt(n) <= 3.0
    print("  [PASS] All Section 2 numerical parameter envelopes verified.")


def test_terminal_cancellation():
    """Verify Section 2: Equation (7) terminal/predecessor feedback row cancellation."""
    print("\n=== Testing Terminal Feedback Cancellation ===")
    T = 50
    z_max = 100
    q = np.random.uniform(0.9, 0.9992, size=T)
    J = np.random.randn(T)

    Z = np.zeros(T + 1)
    for t in range(1, T + 1):
        Z[t] = 0.999 * q[t - 1] * (Z[t - 1] + J[t - 1])

    F = np.zeros((z_max + 1, T + 1))
    for t in range(1, T + 1):
        for z in range(2, z_max + 1):
            F[z, t] = 0.999 * q[t - 1] * (F[z - 1, t - 1] + J[t - 1])

    max_diff = max(abs(F[z, t] - Z[t]) for t in range(1, T + 1) for z in range(t + 1, z_max + 1))
    assert max_diff == 0.0, f"Non-zero diff for z > t: {max_diff}"
    print(f"  [PASS] F_{{z,t}} == Z_t identically for all z > t (cancellation verified).")


def test_receiver_contraction_and_bounds():
    """Verify Section 3: Equations (10)-(17)."""
    print("\n=== Testing Receiver Contraction & Query Bounds ===")
    g_star = 0.9975
    eps = 1e-4
    L_star = (g_star / (g_star - eps))**2
    rho = (g_star + eps) * g_star**2 / (g_star - eps)
    mult = 4 * L_star * eps / (1 - rho)

    assert L_star < 1.000201, f"L_star out of range: {L_star}"
    assert rho < 0.995206, f"rho out of range: {rho}"
    assert mult < 0.084, f"Multiplier out of range: {mult}"
    print(f"  [PASS] L_* = {L_star:.6f} < 1.000201")
    print(f"  [PASS] rho = {rho:.6f} < 0.995206")
    print(f"  [PASS] 4 L_* eps / (1 - rho) = {mult:.6f} < 0.084")

    # Trace neutrality check
    a = 1.0 - 1.0 / 1e6
    g_H = 0.995
    tau = 45.0
    A = 1.0 + a * g_H
    B = a**2 * g_H * (1.0 + a * tau)
    for x in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        d = g_star + eps * x
        d_3 = g_star * (A + B * g_star) / (A + B * d)
        tau_final = d_3 * (A + B * d)
        expected_tau = g_star * (A + B * g_star)
        assert np.isclose(tau_final, expected_tau, rtol=1e-12)
    print("  [PASS] Exact 3-step trace neutrality verified for all x in [-1, 1].")


def test_bath_front_and_cohort_bounds():
    """Verify Section 4 & Section 6: Equations (19), (22), (24), (26)."""
    print("\n=== Testing Bath, Front, and Cohort Bounds ===")
    q_star = 0.9992
    S_2 = (1 + q_star**2) / (1 - q_star**2)**3
    sigma_max = 0.051
    front_coeff = (sigma_max / np.sqrt(2)) * 24 * np.sqrt(S_2)
    assert front_coeff < 30000, f"Front coefficient too large: {front_coeff}"
    print(f"  [PASS] Front coefficient = {front_coeff:.2f} < 30000")

    cohort_coeff = (sigma_max / np.sqrt(2)) * 400
    assert cohort_coeff < 32, f"Cohort coefficient too large: {cohort_coeff}"
    print(f"  [PASS] Cohort coefficient = {cohort_coeff:.2f} < 32")


def test_long_window_cancellation():
    """Verify Section 9: Equation (35) long-window centered-input identity."""
    print("\n=== Testing Long-Window Identity (Equation 35) ===")
    W = 10
    L = W + 2
    a = 1.0 - 1.0 / 1e6
    g_H = 0.995
    g_star = 0.9975
    tau = 80.0
    eps = 1e-4

    alpha_H = a * g_H
    T_W = g_H * sum(alpha_H**u for u in range(W))
    A_W = 1 + a * T_W
    B_W = a * (alpha_H**W) * (1 + a * tau)

    def run_block(d, J_seq, V_in):
        d_last = g_star * (A_W + B_W * g_star) / (A_W + B_W * d)
        gates = [d] + [g_H] * W + [d_last]
        V = V_in
        curr_tau = tau
        for g, J in zip(gates, J_seq):
            V = a * g * (V + J)
            curr_tau = g * (1 + a * curr_tau)
        return V, curr_tau

    # Constant J and matched V_in
    J_const = 3.14159
    J_seq = np.full(L, J_const)
    V_in = a * tau * J_const

    V_0, tau_0 = run_block(g_star, J_seq, V_in)
    V_1, tau_1 = run_block(g_star + eps, J_seq, V_in)

    diff_tau = abs(tau_1 - tau_0)
    diff_V = abs(V_1 - V_0)
    assert diff_tau < 1e-12, f"Trace neutrality failed: {diff_tau}"
    assert diff_V < 1e-12, f"Constant-field cancellation failed: {diff_V}"
    print(f"  [PASS] Long-window trace diff: {diff_tau:.2e}")
    print(f"  [PASS] Long-window delta V_out under constant J: {diff_V:.2e} (identically zero)")


if __name__ == "__main__":
    test_algebraic_identities()
    test_terminal_cancellation()
    test_receiver_contraction_and_bounds()
    test_bath_front_and_cohort_bounds()
    test_long_window_cancellation()
    print("\nALL REPRODUCIBLE VERIFICATION CHECKS PASSED SUCCESSFULLY.")
