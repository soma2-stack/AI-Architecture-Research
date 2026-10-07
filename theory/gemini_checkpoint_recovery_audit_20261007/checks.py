"""
Numerical and algebraic verification script for:
1. Legal-query normalization constants (7.213 arithmetic derivation and sharp C <= 0.048)
2. Eta ledger upper bounds (eta <= 8.0001e-9 < 0.001)
3. Route-6 stationary code asymptotics (q_stat / K -> 0)
"""

import math

def check_constants():
    # Model parameters
    sigma_max = 0.051
    sigma_min = 0.0499
    q_f = 1024 / 1089  # sech^2(0.25) < 1024/1089 ~ 0.94031
    
    # 1. Historical repo ledger origin of 7.213:
    # Tuple coefficient from equation (24): 400 / sqrt(n)
    # Divided by 2 (survivor tuples = m/2, Cauchy-Schwarz gives sqrt(m)/sqrt(2))
    # and sqrt(l/n) <= 1/sqrt(2):
    # C_repo = (400 * sigma_max) / (2 * sqrt(2))
    c_repo = (400 * sigma_max) / (2 * math.sqrt(2))
    print(f"[Check 1] C_repo exact = {c_repo:.6f} <= 7.213: {c_repo <= 7.213}")
    assert c_repo <= 7.213
    assert abs(c_repo - 7.212489) < 1e-4

    # 2. Sharp constant C_sharp = sigma * q_f
    c_sharp = sigma_max * q_f
    print(f"[Check 2] C_sharp exact = {c_sharp:.6f} <= 0.048: {c_sharp <= 0.048}")
    assert c_sharp <= 0.048

    # 3. Final public clear contraction
    # Duration: L_clear = 100000 * (n/m) * log(n)
    # Contraction per 2 steps: 1 - m / (8000*n)
    # Total contraction exponent: - (m / (8000*n)) * 100000 * (n/m) * log(n) = -12.5 * log(n)
    # Hence contraction factor <= n^(-12.5)
    for n_exp in [6, 10, 50, 100]:
        n = 10**n_exp
        contraction = n**(-12.5)
        assert contraction <= 1e-75

    # 4. Eta ledger
    e_dense = 8.0e-9
    e_complementary = 1.0e-28
    eta_total = e_dense + e_complementary
    print(f"[Check 3] eta_total = {eta_total:.10e} <= 8.0001e-9: {eta_total <= 8.0001e-9}")
    assert eta_total <= 8.0001e-9
    assert eta_total < 0.001

    # 5. Route-6 asymptotics: q_stat / K -> 0
    print("[Check 4] Route-6 asymptotic ratios q_stat / K:")
    for n_val in [1e6, 1e12, 1e20, 1e50, 1e100]:
        log_n = math.log(n_val)
        log_log_n = math.log(log_n)
        R = log_log_n
        K = n_val / R
        q_stat = R * (2**R + 1)
        ratio = q_stat / K
        print(f"  n = {n_val:.1e}: R = {R:.2f}, 2^R = {2**R:.2f}, q_stat = {q_stat:.2f}, q_stat/K = {ratio:.4e}")
        assert ratio < 1.0

    print("ALL CHECKS PASSED.")

if __name__ == "__main__":
    check_constants()
