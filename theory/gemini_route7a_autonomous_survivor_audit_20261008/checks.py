"""Independent hostile audit checks for Route 7A autonomous survivor compression.
Auditor: Gemini (Independent Mathematical Auditor)
Date: 2026-10-08
Target: GPT-6 autonomous survivor audit & Astra long-window donor code
"""
import math
import random
import numpy as np

def test_stage_a_asymptotic_drift():
    """Verify Lemma 1 positive drift under the explicit small-bath condition e_n <= 5e-6."""
    b = 0.05
    u0 = math.tanh(b)
    e_n = 5e-6
    n_min = 1_000_000
    a = 1 - 1 / n_min
    gamma_max = 1 + e_n
    
    # Derivation of beta lower bound:
    # beta_t = 0.05 - a * gamma * u_bar - a * c * D_t
    # Worst case: a <= 1, gamma <= 1 + e_n, u_bar <= u0 + e_n, c * |D_t| <= e_n
    beta_min = b - gamma_max * (u0 + e_n) - e_n
    assert beta_min > 3e-5, f"beta_min too small: {beta_min}"
    assert abs(beta_min - 3.137523e-5) < 1e-10, f"beta mismatch: {beta_min}"
    
    # Monotone drift check:
    theta = 0.03
    margin = math.tanh(a * theta + 3e-5) - theta
    assert margin > 1e-5, f"margin too small: {margin}"
    assert abs(margin - 2.0946e-5) < 1e-7
    
    # Invariance check:
    gate_at_theta = 1 - theta**2
    assert gate_at_theta <= 0.9991 < 0.9992
    
    # Step count from worst-case reset:
    s_reset = -math.sqrt(0.005)
    s = s_reset
    steps = 0
    while s < theta and steps < 15000:
        s = math.tanh(a * s + beta_min)
        steps += 1
    
    assert s >= theta, "Failed to reach theta"
    assert steps <= 11000, f"Steps exceeded 11,000: {steps}"
    
    return {
        "status": "PASS",
        "beta_min": beta_min,
        "margin": margin,
        "empirical_steps": steps,
        "certified_upper": 11000,
        "final_gate": 1 - s**2
    }

def test_stage_a_finite_n_counterexample():
    """Demonstrate that at finite n = 10^6, beta_t is strictly NEGATIVE, falsifying Lemma 1."""
    n = 1_000_000
    k = n // 2
    gamma = 1 / (1 - 1 / math.sqrt(k))
    u0 = math.tanh(0.05)
    a = 1 - 1 / n
    
    # At n = 10^6, gamma - 1 is ~ 1.416e-3 >> 5e-6
    gamma_minus_1 = gamma - 1
    assert gamma_minus_1 > 1.4e-3, f"gamma-1 mismatch: {gamma_minus_1}"
    
    # Baseline beta with D_t = 0:
    beta_finite = 0.05 - a * gamma * u0
    assert beta_finite < 0, f"beta_finite not negative: {beta_finite}"
    assert abs(beta_finite - (-2.90768e-5)) < 1e-9
    
    # Negative drift trajectory from positive capture s0 = +sqrt(0.005)
    s = math.sqrt(0.005)
    # Track steps where gate > 0.9992
    bad_steps = 0
    for t in range(50000):
        g = 1 - s**2
        if g > 0.9992:
            bad_steps += 1
        s = math.tanh(a * s + beta_finite)
    
    # Finds fixed point s* < 0
    s_star = s
    assert s_star < -0.04, f"Unexpected fixed point: {s_star}"
    assert bad_steps > 1000, f"Bad steps too small: {bad_steps}"
    
    return {
        "status": "COUNTEREXAMPLE_VERIFIED",
        "n": n,
        "gamma_minus_1": gamma_minus_1,
        "beta_finite": beta_finite,
        "fixed_point_s": s_star,
        "bad_steps_near_zero": bad_steps
    }

def test_stage_c_product_contraction():
    """Verify analytic and worst-case bad-step counting for Lemma 2."""
    M_star = 11001
    results = []
    for W_mult in [8, 12, 16]:
        Tc = W_mult * M_star
        for K_mult in [8, 10, 16]:
            K = K_mult * M_star
            q, r = divmod(K, Tc)
            max_bad = q * M_star + min(r, M_star)
            ratio = max_bad / K
            assert ratio <= 0.25 <= 3/8, f"Ratio exceeded 3/8: {ratio}"
            good_steps = K - max_bad
            assert good_steps >= K / 2, f"Good steps under K/2: {good_steps}"
            results.append((Tc, K, max_bad, ratio))
            
    return {"status": "PASS", "cases_checked": len(results), "max_ratio": max(r[3] for r in results)}

def test_stage_d_survivor_query_bound():
    """Verify operator norm and ordinary-row query dilution for survivor cohort (Eq 9)."""
    # nu_S <= (sigma * sqrt(l) / n) * ||c_{Q,S}||_2 * ||Delta M_S||_op
    # sigma = 0.05, l = n/2
    # c_{Q,S} has |c_Q(i)| <= 100 / sqrt(n) over 4m rows -> ||c_{Q,S}||_2 <= 200 * sqrt(m/n)
    # ||Delta M_S||_op <= 2N * q_*^{K/2}
    sigma = 0.05
    # (sigma * sqrt(n/2) / n) = 0.05 / (sqrt(2) * sqrt(n)) = 0.035355339 / sqrt(n)
    # Product: (0.035355339 / sqrt(n)) * (200 * sqrt(m) / sqrt(n)) * (2N * q_*^{K/2})
    # = (0.035355339 * 200 * 2) * (N * sqrt(m) / n) * q_*^{K/2}
    coeff = (sigma / math.sqrt(2)) * 200 * 2
    assert coeff < 14.15 < 32.0, f"Coefficient exceeded 32: {coeff}"
    
    # Check K value for delta = 1e-4 with C_T = 1.0, q_* = 0.9992:
    q_star = 0.9992
    A0 = 1.0
    delta = 1e-4
    K_req = 2 * math.log(32 * A0 / delta) / (-math.log(q_star))
    assert K_req < 32000 < 88008
    K_chosen = 88008
    contraction = q_star ** (K_chosen / 2)
    assert contraction < 1e-15, f"Contraction not small enough: {contraction}"
    
    return {
        "status": "PASS",
        "exact_coefficient": coeff,
        "claimed_coefficient": 32.0,
        "K_required": K_req,
        "K_chosen": K_chosen,
        "contraction_at_K": contraction
    }

def test_stage_e_long_window_donor_aggregate():
    """Verify Astra's exact 2-aggregate identity on full rank-2 long-window block."""
    rng = random.Random(42)
    n = 1_000_000
    a = 1 - 1/n
    gH = 1 - n**-2
    gstar = 0.9975
    eps = 1e-4
    
    for W in [1, 4, 16, 64, 256]:
        tau = 55.3
        d = gstar + eps * rng.uniform(-1, 1)
        alpha = a * gH
        tw = gH * sum(alpha**j for j in range(W))
        AW = 1 + a * tw
        BW = a * alpha**W * (1 + a * tau)
        dlast = gstar * (AW + BW * gstar) / (AW + BW * d)
        
        # Verify multiplier rho
        Ai = a**2 * alpha**W * d * dlast
        rho = (gstar + eps) * gstar**2 / (gstar - eps)
        assert Ai <= rho < 0.995206, f"Ai exceeded rho: {Ai} vs {rho}"
        
        # Verify recurrence identity
        Js = [rng.uniform(-2, 2) for _ in range(W + 2)]
        V0 = rng.uniform(-5, 5)
        V = V0
        for gate, J in zip([d] + [gH]*W + [dlast], Js):
            V = a * gate * (V + J)
            
        U = Js[0]
        Qr = sum(alpha**(W + 1 - k) * Js[k] for k in range(1, W + 2))
        V_agg = Ai * (V0 + U) + a * dlast * Qr
        assert abs(V - V_agg) < 1e-11, f"Mismatch: {V} vs {V_agg}"
        
    return {"status": "PASS", "rho_bound": rho, "max_mismatch": "< 1e-11"}

def test_stage_e_code_dimension_and_scaling():
    """Verify code dimension scaling q_code = o(n) vs D = Omega(n) and compute onset R."""
    # At Route scaling:
    # m = n / R, N = C_T * sqrt(n * R), W = R
    # q_code <= h*m + (2h + K + 2)*P where P <= 4m + 4N, h = O(log R), K = O(1)
    C_T = 1.0
    results = []
    # Because K = 88008, q_code/n < 1 strictly requires R >= 4*K ~ 350,000
    for R in [500_000, 1_000_000, 5_000_000, 10_000_000]:
        n = 10**20
        m = n // R
        N = int(C_T * math.sqrt(n * R))
        P = 4 * m + 4 * N
        h = int(math.ceil(math.log(R) / (-math.log(0.995206)))) + 10
        K = 88008
        q_code = h * m + (2 * h + K + 2) * P
        ratio = q_code / n
        assert ratio < 1.0, f"q_code exceeded n at R={R}: ratio={ratio}"
        results.append((R, ratio))
            
    return {"status": "PASS", "asymptotic_ratios": results}

if __name__ == "__main__":
    print("Testing Stage A asymptotic drift:", test_stage_a_asymptotic_drift())
    print("Testing Stage A finite-n counterexample:", test_stage_a_finite_n_counterexample())
    print("Testing Stage C product contraction:", test_stage_c_product_contraction())
    print("Testing Stage D survivor query bound:", test_stage_d_survivor_query_bound())
    print("Testing Stage E Astra donor aggregate:", test_stage_e_long_window_donor_aggregate())
    print("Testing Stage E code dimension scaling:", test_stage_e_code_dimension_and_scaling())
    print("\nALL REPRODUCIBLE TESTS PASSED.")
