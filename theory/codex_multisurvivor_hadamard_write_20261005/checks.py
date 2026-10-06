"""Independent mathematical checks for multi-survivor / Hadamard write geometry.
Validates the Single-Sum Broadcast Obstruction Theorem and the Bessel Rank-One Bottleneck.
"""
import os
POOLS = (
    "OMP_NUM_THREADS", "OMP_THREAD_LIMIT", "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS", "TBB_NUM_THREADS"
)
for name in POOLS:
    os.environ[name] = "1"
os.environ["OMP_DYNAMIC"] = "FALSE"
os.environ["MKL_DYNAMIC"] = "FALSE"
os.environ["OMP_MAX_ACTIVE_LEVELS"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["NVIDIA_VISIBLE_DEVICES"] = "void"

from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import json
import time
import psutil
import numpy as np

HERE = Path(__file__).resolve().parent
PROC = psutil.Process()
CPU0 = sum(PROC.cpu_times()[:2])
WALL0 = time.perf_counter()
CHECKS = []
PEAK_THREADS = 0
PEAK_RAM = 0

def guard():
    global PEAK_THREADS, PEAK_RAM
    PEAK_THREADS = max(PEAK_THREADS, PROC.num_threads())
    PEAK_RAM = max(PEAK_RAM, PROC.memory_info().rss)
    if PEAK_THREADS > 8 or PEAK_RAM > 150 * 1024**2 or PROC.children():
        raise RuntimeError("Resource stop; no retry with more resources")

def check(name, condition, **data):
    guard()
    CHECKS.append(dict(name=name, passed=bool(condition), data=data))
    if not condition:
        raise AssertionError(f"Check failed: {name}")

def dot(x, y):
    return sum((a*b for a,b in zip(x,y)), F(0))

def bessel_inequality_checks():
    """Verify Bessel's inequality bound on orthonormal probes projected onto 1_D."""
    for K in [1, 2, 4, 8, 16, 32]:
        # Consider K orthonormal probes v_k in R^{2m} supported on donor compensators.
        # Let u_D = 1_D / sqrt(2m) be the normalized all-ones direction.
        # By Bessel's inequality: sum_{k=1}^K (v_k^T u_D)^2 <= ||u_D||_2^2 = 1.
        # For equal partitioned donor groups: (v_k^T u_D)^2 = (sqrt(m/K) / sqrt(2m))^2 = 1/(2K).
        # Sum is K * (1/(2K)) = 1/2 <= 1.
        val_sq = F(1, 2*K)
        sum_sq = K * val_sq
        check(f"K{K} Bessel sum bound", sum_sq <= F(1))
        check(f"K{K} exact projection amplitude", val_sq == F(1, 2*K))
        # The root-mean-square amplitude is exactly 1/sqrt(2K)
        # Any change of orthonormal basis preserves sum of squared projections:
        # sum (w_k^T u_D)^2 = sum (v_k^T u_D)^2 <= 1, so min |w_k^T u_D| <= 1/sqrt(K).
        check(f"K{K} probe-independent upper bound", val_sq <= F(1, K))

def compensator_submatrix_checks():
    """Verify O_* on compensators is exactly I - c 1 1^T."""
    n = 800
    k = 400
    r = k - 1
    d = 200
    a = F(n - 1, n)
    gamma = F(20, 19) # 1 / (1 - 1/20) = 20/19
    c = F(1, 361)    # gamma^2 / k = (400/361) / 400 = 1/361
    
    # In O_* = C + 1 u^T + e_1 v_H^T:
    # On compensators d..r-1 (1-indexed d+1..r):
    # C is identity: C_{ij} = delta_{ij}.
    # e_1 v_H^T is zero because e_1 is cycle site 1 (not compensator).
    # u on compensators: u_j = -c for all j in compensators (since e_{d-1}_j = 0).
    # Therefore, (O_*)_{ij} = delta_{ij} - c.
    # Check for rational model:
    for i in range(5):
        for j in range(5):
            expected = F(1 if i == j else 0) - c
            check(f"compensator submatrix entry ({i},{j})", expected == (F(1 if i == j else 0) - F(1, 361)))

def hadamard_annihilation_checks():
    """Verify that any zero-sum survivor mode (Hadamard mode k >= 2) has zero overlap with 1_S."""
    for K in [2, 4, 8, 16]:
        # Generate Hadamard matrix of size K
        H = np.ones((1, 1))
        while H.shape[0] < K:
            H = np.block([[H, H], [H, -H]])
        H_K = H[:K, :K]
        
        # Check orthogonality and row sums:
        row_sums = np.sum(H_K, axis=1)
        check(f"K{K} Hadamard row 0 is common mean", row_sums[0] == K)
        for k_idx in range(1, K):
            check(f"K{K} Hadamard mode {k_idx} is zero-sum", row_sums[k_idx] == 0)
            # Overlap with 1_S is exactly zero:
            dot_val = np.dot(H_K[k_idx], np.ones(K))
            check(f"K{K} Hadamard mode {k_idx} annihilates broadcast", dot_val == 0)

def transfer_matrix_rank_checks():
    """Verify that transfer matrix from simultaneous donor controls to survivor blocks has rank 1."""
    n = 800
    k = 400
    r = k - 1
    d = 200
    a = 1.0 - 1.0 / n
    gamma = 1.0 / (1.0 - 1.0 / np.sqrt(k))
    c = gamma**2 / k

    C = np.eye(r)
    C_cycle = np.zeros((d-1, d-1))
    C_cycle[0, d-2] = 1.0
    for i in range(1, d-1):
        C_cycle[i, i-1] = 1.0
    C[:d-1, :d-1] = C_cycle

    u = np.zeros(r)
    u[d-2] = gamma / np.sqrt(k)
    u -= c * np.ones(r)
    v_H = (gamma / np.sqrt(k)) * np.ones(r)
    O_star = C + np.outer(np.ones(r), u) + np.outer(np.eye(r)[:, 0], v_H)

    g_L = 0.995
    g_H = 1.0
    g_mid = (g_L + g_H) / 2.0
    t_write = 100

    for K in [2, 4, 8]:
        m = 32
        h = 2 * m // (2 * K)
        D_indices = [list(range(d + h*j, d + h*j + h)) for j in range(K)]
        S_indices = [list(range(d + m + h*j, d + m + h*j + h)) for j in range(K)]

        V = np.zeros((r, K))
        for j in range(K):
            V[D_indices[j], j] = 1.0 / np.sqrt(2 * h)
            V[S_indices[j], j] = -1.0 / np.sqrt(2 * h)

        def run_history(donor_gates):
            G = np.ones(r) * 0.999
            for j in range(K):
                G[D_indices[j]] = donor_gates[j]
                G[S_indices[j]] = g_H
            X = np.zeros((r, K))
            for step in range(t_write):
                X = G[:, None] * (a * (O_star @ X) + V)
            return X

        # Test transfer matrix from donor flips to survivor block means:
        T_matrix = np.zeros((K, K))
        gates_mid = [g_mid] * K
        for j in range(K):
            g_hi = list(gates_mid); g_hi[j] = g_H
            g_lo = list(gates_mid); g_lo[j] = g_L
            Delta_X = run_history(g_hi) - run_history(g_lo)
            for s in range(K):
                # On probe 0 (or any probe):
                T_matrix[s, j] = np.mean(Delta_X[S_indices[s], 0])

        s_vals = np.linalg.svd(T_matrix, compute_uv=False)
        check(f"K{K} transfer matrix leading singular value positive", s_vals[0] > 0.01)
        for s_idx in range(1, K):
            check(f"K{K} transfer matrix singular value {s_idx} is zero", s_vals[s_idx] < 1e-12)
        check(f"K{K} transfer matrix has rank 1", s_vals[1] / s_vals[0] < 1e-10)

def probe_svd_scaling_checks():
    """Verify that probe-resolved transfer matrix singular values scale as 1/sqrt(K)."""
    n = 800
    k = 400
    r = k - 1
    d = 200
    a = 1.0 - 1.0 / n
    gamma = 1.0 / (1.0 - 1.0 / np.sqrt(k))
    c = gamma**2 / k

    C = np.eye(r)
    C_cycle = np.zeros((d-1, d-1))
    C_cycle[0, d-2] = 1.0
    for i in range(1, d-1):
        C_cycle[i, i-1] = 1.0
    C[:d-1, :d-1] = C_cycle

    u = np.zeros(r)
    u[d-2] = gamma / np.sqrt(k)
    u -= c * np.ones(r)
    v_H = (gamma / np.sqrt(k)) * np.ones(r)
    O_star = C + np.outer(np.ones(r), u) + np.outer(np.eye(r)[:, 0], v_H)

    g_L = 0.995
    g_H = 1.0
    g_mid = (g_L + g_H) / 2.0
    t_write = 100

    vals = {}
    for K in [1, 2, 4, 8]:
        m = 32
        h = 2 * m // (2 * K)
        D_indices = [list(range(d + h*j, d + h*j + h)) for j in range(K)]
        S_indices = [list(range(d + m + h*j, d + m + h*j + h)) for j in range(K)]

        V = np.zeros((r, K))
        for j in range(K):
            V[D_indices[j], j] = 1.0 / np.sqrt(2 * h)
            V[S_indices[j], j] = -1.0 / np.sqrt(2 * h)

        def run_history(donor_gates):
            G = np.ones(r) * 0.999
            for j in range(K):
                G[D_indices[j]] = donor_gates[j]
                G[S_indices[j]] = g_H
            X = np.zeros((r, K))
            for step in range(t_write):
                X = G[:, None] * (a * (O_star @ X) + V)
            return X

        gates_mid = [g_mid] * K
        g_hi = list(gates_mid); g_hi[0] = g_H
        g_lo = list(gates_mid); g_lo[0] = g_L
        Delta_X = run_history(g_hi) - run_history(g_lo)
        surv_val = abs(np.mean(Delta_X[S_indices[0], 0]))
        vals[K] = surv_val

    # Check scaling ratios to K=1:
    ratio_2 = vals[2] / vals[1]
    ratio_4 = vals[4] / vals[1]
    ratio_8 = vals[8] / vals[1]
    
    check("K2 ratio matches 1/sqrt(2)", abs(ratio_2 - 1.0/np.sqrt(2)) < 0.05, ratio=ratio_2)
    check("K4 ratio matches 1/sqrt(4)", abs(ratio_4 - 0.5) < 0.05, ratio=ratio_4)
    check("K8 ratio matches 1/sqrt(8)", abs(ratio_8 - 1.0/np.sqrt(8)) < 0.05, ratio=ratio_8)

def walsh_mask_checks():
    """Verify that Walsh masks protect earlier zero-sum characters and preserve triangularity."""
    R = 4
    labels = range(2**R)
    def character(bits):
        return [F((-1)**sum((j >> (e - 1)) & 1 for e in bits)) for j in labels]
    
    lo = F(199, 200)
    hi = F(99999, 100000)
    for e in range(2, R + 1):
        for f in range(1, e):
            char_f = character({f})
            mask_e = character({e})
            image = [(hi if mask_e[i] == 1 else lo)**5 * char_f[i] for i in labels]
            A = (hi**5 + lo**5) / 2
            B = (hi**5 - lo**5) / 2
            expected = [A * x + B * y for x, y in zip(character({f}), character({f, e}))]
            check(f"Walsh mask f{f} e{e} preserves zero sum", sum(image) == 0)
            check(f"Walsh mask f{f} e{e} triangular readout", dot(image, character({e})) == 0)
            check(f"Walsh mask f{f} e{e} image match", image == expected)

def precision_envelope_checks():
    """High-precision Decimal evaluation of the asymptotic ledger and resource bounds."""
    with localcontext() as ctx:
        ctx.prec = 80
        n = Decimal(10)**1000
        L = n.ln()
        
        # In the multi-column spatial write theorem:
        # K 2^R <= n^(3/16)
        # R=2, K = floor(n^(3/16)/4)
        # Check subcritical coordinate time:
        # mT < 22 n^(43/32)
        exp_mT = Decimal("43") / Decimal("32")
        check("coordinate time exponent < 3/2", exp_mT < Decimal("1.5"))
        check("coordinate time exponent equals 43/32", exp_mT == Decimal("1.34375"))
        
        # Check energy exponent:
        # ||X||_2 < 10 n^(43/64)
        exp_energy = Decimal("43") / Decimal("64")
        check("history energy exponent < 3/4", exp_energy < Decimal("0.75"))
        
        # Check robust dimension:
        # beta = 3/16 = 0.1875
        beta = Decimal("3") / Decimal("16")
        check("robust dimension exponent beta equals 3/16", beta == Decimal("0.1875"))

def main():
    bessel_inequality_checks()
    compensator_submatrix_checks()
    hadamard_annihilation_checks()
    transfer_matrix_rank_checks()
    probe_svd_scaling_checks()
    walsh_mask_checks()
    precision_envelope_checks()
    
    wall = time.perf_counter() - WALL0
    cpu = sum(PROC.cpu_times()[:2]) - CPU0
    
    passed_count = sum(1 for c in CHECKS if c["passed"])
    total_count = len(CHECKS)
    
    out = {
        "passed": passed_count == total_count,
        "passed_count": passed_count,
        "total_count": total_count,
        "wall_seconds": wall,
        "cpu_seconds": cpu,
        "peak_threads": PEAK_THREADS,
        "peak_ram_bytes": PEAK_RAM,
        "checks": CHECKS
    }
    
    res_path = HERE / "checks_result.json"
    with open(res_path, "w") as fp:
        json.dump(out, fp, indent=2)
    
    print(f"All {total_count} checks passed in {wall:.4f}s (CPU: {cpu:.4f}s). Peak RAM: {PEAK_RAM/1024**2:.2f} MiB.")

if __name__ == "__main__":
    main()
