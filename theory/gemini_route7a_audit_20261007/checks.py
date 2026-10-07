"""
Independent Mathematical Verification Script for Astra Route 7A Audit
Author: Gemini (Cursor / Gemini research lane)
Date: 2026-10-07
"""

import math
import numpy as np
import sympy as sp


def check_constant_32():
    sigma = 0.051
    C_Q = 100.0
    # Legal query bound: 4 * C_Q * sigma * (N/n) * sqrt(l * h_S / n) * sqrt(F_ell)
    # With l <= n and h_S = 2m:
    # 4 * C_Q * sigma * sqrt(2) * (N * sqrt(m) / n)
    c_18 = 4 * C_Q * sigma * math.sqrt(2)
    print(f"Constant in Eq (18): {c_18:.4f} <= 32: {c_18 <= 32}")
    assert c_18 <= 32, "Constant 32 violated!"
    return True


def check_two_step_clear_constants():
    # In Section 6:
    # g_H > 0.99, |eta| >= sqrt(1 - p/16) > 0.99 for p < 0.01
    # sqrt(2p - p^2) >= sqrt(p * (2 - 0.01)) = sqrt(1.99) * sqrt(p)
    # Component outside S_{t+1}:
    # g_H * |eta| * sqrt(2p - p^2) - ||v||
    # With ||v|| < sqrt(p)/4 = 0.25 * sqrt(p):
    c_outside = 0.99 * 0.99 * math.sqrt(1.99) - 0.25
    print(f"Outside component factor: {c_outside:.4f} > 0.73: {c_outside > 0.73}")
    assert c_outside > 0.73, "Outside component factor too small!"

    # Loss at step 2 is delta * (c_outside * sqrt(p))^2 = delta * p * c_outside^2
    loss_factor = c_outside**2
    target_loss = 1.0 / 16.0  # delta * p / 16
    print(f"Step 2 loss factor: {loss_factor:.4f} >= 1/16 ({target_loss:.4f}): {loss_factor >= target_loss}")
    assert loss_factor >= target_loss, "Step 2 loss factor violated!"
    return True


def check_trace_neutral_algebra():
    tau, a, g_H, g_star, eps, x = sp.symbols('tau a g_H g_star eps x')
    d1 = g_star + eps * x
    d2 = g_H

    tau_target = g_star * (1 + a * g_H * (1 + a * g_star * (1 + a * tau)))
    d3 = tau_target / (1 + a * g_H * (1 + a * d1 * (1 + a * tau)))

    tau1 = d1 * (1 + a * tau)
    tau2 = d2 * (1 + a * tau1)
    tau3 = d3 * (1 + a * tau2)

    diff = sp.simplify(tau3 - tau_target)
    print(f"Trace-neutral algebraic error: {diff}")
    assert diff == 0, "Trace-neutral algebra did not cancel!"

    # Check bounds on d3
    g_star_val = 0.9975
    eps_val = 1e-4
    bound_d3 = g_star_val * eps_val / (g_star_val - eps_val)
    print(f"Max |d3 - g_*| = {bound_d3:.8f} < 0.000101: {bound_d3 < 0.000101}")
    assert bound_d3 < 0.000101, "d3 bound violated!"
    return True


def check_walsh_pairwise_independence():
    k = 7
    h_S = 2**k  # 128
    sites = np.arange(h_S)

    def walsh_char(alpha):
        bits = (sites[:, None] & (1 << np.arange(k))) > 0
        alpha_bits = (alpha & (1 << np.arange(k))) > 0
        dot = (bits * alpha_bits).sum(axis=1) % 2
        return 1 - 2 * dot  # in {-1, +1}

    alphas = list(range(1, h_S))
    np.random.seed(42)
    selected = np.random.choice(alphas, size=20, replace=False)

    for i in range(len(selected)):
        w_i = walsh_char(selected[i])
        assert np.isclose(np.mean(w_i), 0.0)
        for j in range(i + 1, len(selected)):
            w_j = walsh_char(selected[j])
            assert np.isclose(np.mean(w_i * w_j), 0.0)
            p_both = np.mean((w_i == -1) & (w_j == -1))
            assert np.isclose(p_both, 0.25)
    print("Walsh character pairwise independence verified for all test pairs.")
    return True


def check_right_space_induction():
    np.random.seed(42)
    r = 24
    N = 8
    u = np.random.randn(r)
    v_H = np.random.randn(r)

    I_exc = [2, 3, 4, 5, 6, 7]
    L0 = [np.random.randn(r, r) for _ in range(N + 1)]
    L0[0] = np.zeros((r, r))

    basis_vectors = []
    for c in I_exc:
        e_c = np.zeros(r)
        e_c[c] = 1.0
        basis_vectors.append(e_c)
    for t in range(1, N + 1):
        basis_vectors.append(L0[t].T @ u)
        basis_vectors.append(L0[t].T @ v_H)

    E_mat = np.column_stack(basis_vectors)
    U, S, _ = np.linalg.svd(E_mat, full_matrices=False)
    U_basis = U[:, S > 1e-10]
    P_E = U_basis @ U_basis.T

    Delta_L = [np.zeros((r, r)) for _ in range(N + 1)]
    for t in range(1, N + 1):
        for c in I_exc:
            Delta_L[t][:, c] = np.random.randn(r)
    L = [L0[t] + Delta_L[t] for t in range(N + 1)]

    one_r = np.ones(r)
    e_1 = np.zeros(r)
    e_1[0] = 1.0

    H = [np.zeros((r, r)) for _ in range(N + 1)]
    J = [np.zeros(r) for _ in range(N + 1)]
    B = [np.zeros(r) for _ in range(N + 1)]

    for t in range(1, N + 1):
        H_t = np.zeros((r, r))
        for s in range(1, t + 1):
            A_ts = np.random.randn(r, r)
            H_t += (A_ts @ one_r)[:, None] @ J[s-1][None, :] + (A_ts @ e_1)[:, None] @ B[s-1][None, :]
        H[t] = H_t
        J[t] = (L[t] + H[t]).T @ u
        B[t] = (L[t] + H[t]).T @ v_H

        err_J = np.linalg.norm(J[t] - P_E @ J[t]) / (np.linalg.norm(J[t]) + 1e-12)
        err_B = np.linalg.norm(B[t] - P_E @ B[t]) / (np.linalg.norm(B[t]) + 1e-12)
        assert err_J < 1e-10, f"J[{t}] failed: {err_J}"
        assert err_B < 1e-10, f"B[{t}] failed: {err_B}"

    print(f"Right space induction verified: all J_t, B_t in E_par (dim <= {len(basis_vectors)}).")
    return True


if __name__ == '__main__':
    print("Running mathematical checks for Astra Route 7A Audit...")
    check_constant_32()
    check_two_step_clear_constants()
    check_trace_neutral_algebra()
    check_walsh_pairwise_independence()
    check_right_space_induction()
    print("ALL CHECKS PASSED.")
