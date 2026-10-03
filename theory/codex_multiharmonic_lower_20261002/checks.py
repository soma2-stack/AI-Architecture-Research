"""Independent small-width algebra checks, not evidence for the asymptotic theorem.

No Claude implementation/import/output is used. CPU NumPy only. The actual
proof amplitude/threshold are analytic; these checks use delta=.03 to make
the identities numerically measurable at n=200,400.
"""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
import json
import math
import time
from fractions import Fraction
from pathlib import Path
import numpy as np

START_CPU = time.process_time()
START_WALL = time.perf_counter()


def verify_width(n, seed):
    k, d, F = n // 2, n // 4, 2
    a, g0 = 1 - 1 / n, 1 - .15 / n
    b = a * g0
    N = math.ceil(4 * n * math.log(n)) + 1
    delta = .03
    omega = 2 * np.pi * np.arange(1, F + 1) / d
    w = -np.ones(k) / math.sqrt(k)
    w[0] += 1
    gu = 2 / (w @ w)

    def U(v):
        return v - gu * w[:, None] * (w @ v)[None, :]

    def P(v):
        v = v.copy()
        v[:d] = np.roll(v[:d], 1, axis=0)
        return v

    def O(v):
        return U(P(U(v)))

    x = np.arange(d)
    frame = np.column_stack([np.ones(d) / math.sqrt(d)] + [
        col for f in range(F) for col in
        (math.sqrt(2 / d) * np.cos(omega[f] * x),
         math.sqrt(2 / d) * np.sin(omega[f] * x))])
    perp = np.eye(d) - frame @ frame.T
    rng = np.random.default_rng(seed)
    profiles = perp @ rng.normal(size=(d, F))
    profiles /= max(1.0, np.max(np.abs(profiles)))
    latent = np.zeros((k, F), dtype=np.complex128)
    latent[:d] = np.exp(1j * x[:, None] * omega[None, :]) / math.sqrt(d)
    physical = U(latent)
    lam = np.exp(-1j * omega)
    eigen_error = np.max(np.abs(O(physical) - physical * lam[None, :]))
    assert eigen_error < 1e-13
    assert np.max(np.abs(physical[0])) < 1e-13

    public = np.zeros_like(physical)
    coeff = np.zeros((5, k, F), dtype=np.complex128)
    plus, minus = public.copy(), public.copy()
    ideal_sum = public.copy()
    max_twist_ratio = 0.0
    max_deficit = 0.0
    tau_arr = np.arange(N)
    decay = b ** tau_arr
    cosine = np.cos(tau_arr[:, None] * omega[None, :])
    kernel = ((decay[:, None] * np.exp(-1j * tau_arr[:, None] * omega[None, :])).T
              @ cosine - (b ** N * lam ** N)[:, None] * cosine.sum(axis=0)[None, :])

    for t in range(1, N + 1):
        tau = N - t
        virtual_d = delta / F * (profiles[(x + tau) % d]
                                @ np.cos(omega * tau))
        diag = np.zeros(k)
        diag[1:d] = virtual_d[1:]
        max_deficit = max(max_deficit, float(np.max(np.abs(diag))))
        assert np.max(np.abs(diag)) <= delta * (1 + 1e-12)
        assert np.all(.15 - diag[1:] >= .05)
        assert np.all(.15 - diag[1:] <= .25)

        forcing = a * O(public) + physical
        transported = np.stack([O(coeff[j]) for j in range(5)])
        updated = b * transported
        updated[0] += (diag / n)[:, None] * forcing
        for j in range(1, 5):
            updated[j] += (a * diag / n)[:, None] * transported[j - 1]
        coeff = updated
        public = g0 * forcing
        plus = (g0 + diag / n)[:, None] * (a * O(plus) + physical)
        minus = (g0 - diag / n)[:, None] * (a * O(minus) + physical)

        # Recompute the full twist expression directly, separately from (13).
        virtual_injection = np.zeros_like(latent)
        virtual_injection[:d] = virtual_d[:, None] * latent[:d]
        exact_latent_injection = U(diag[:, None] * physical)
        difference = exact_latent_injection - virtual_injection
        norm = np.linalg.norm(difference, axis=0)
        max_twist_ratio = max(max_twist_ratio, float(np.max(norm) /
                                                    (6 * delta / math.sqrt(d))))
        assert np.max(norm) <= 6 * delta / math.sqrt(d) + 1e-12
        finite_q = (1 - (b * lam) ** t) / (1 - b * lam)
        propagated = virtual_injection.copy()
        propagated[:d] = np.roll(propagated[:d], tau % d, axis=0)
        ideal_sum += b ** tau / n * propagated * finite_q[None, :]

    ideal_formula = np.zeros_like(latent)
    ideal_formula[:d] = (delta / (n * math.sqrt(d) * F)
                        * np.exp(1j * x[:, None] * omega[None, :])
                        * (profiles @ kernel.T) / (1 - b * lam)[None, :])
    formula_error = np.max(np.abs(ideal_sum - ideal_formula))
    assert formula_error < 1e-10
    real_gram = (kernel.real + kernel.real.T) / 2
    gram_min = float(np.linalg.eigvalsh(real_gram)[0])
    assert gram_min >= n / 40
    exact_transformed = O(O(coeff[0]))
    ideal_l1 = np.sum(np.abs(ideal_formula), axis=0)
    exact_l1 = np.sum(np.abs(exact_transformed), axis=0)
    assert np.all(exact_l1 >= ideal_l1 - 32 * delta * n - 1e-10)

    odd = (plus - minus) / 2
    odd_five = coeff[0] + coeff[2] + coeff[4]
    odd_remainder = float(np.max(np.linalg.norm(odd - odd_five, axis=0)))
    tail_upper = delta ** 7 * n / (1 - delta ** 2)
    assert odd_remainder <= tail_upper + 1e-9
    assert np.max(np.linalg.norm(odd - coeff[0], axis=0)) <= delta ** 3 * n / (1-delta**2) + 1e-9

    # An actual legal one-step projection, not an RMS norm or an ambient adjoint.
    future_column = O(O(odd))
    Hnorm = .4 * math.sqrt(n-k)
    ghi, glo = 1 / math.cosh(.25)**2, 1 / math.cosh(.75)**2
    sg = (ghi-glo)/2
    assert sg > .16
    legal_lower = 0.0
    dual_lower = 0.0
    for f in range(F):
        for realpart in (future_column[:, f].real, future_column[:, f].imag):
            gates = np.where(realpart >= 0, ghi, glo)
            gates_opposite = np.where(realpart >= 0, glo, ghi)
            maximum = max(abs(gates @ realpart), abs(gates_opposite @ realpart))
            formula_maximum = (ghi+glo)/2 * abs(realpart.sum()) + sg * np.abs(realpart).sum()
            assert abs(maximum - formula_maximum) < 1e-10
            legal_lower = max(legal_lower, a*a*Hnorm/(n*math.sqrt(n))*maximum)
        dual_lower = max(dual_lower, a*a*Hnorm/(n*math.sqrt(n))*sg/2
                         * np.abs(future_column[:, f]).sum())
    assert legal_lower >= dual_lower - 1e-12
    return dict(n=n, F=F, N=N, diagnostic_delta=delta, seed=seed,
                exact_eigenvector_error=float(eigen_error),
                ideal_kernel_formula_error=float(formula_error),
                symmetric_kernel_min_eigenvalue=gram_min,
                proved_kernel_floor=n/40, max_twist_bound_ratio=max_twist_ratio,
                degree_one_physical_l1=exact_l1.tolist(), ideal_l1=ideal_l1.tolist(),
                odd_order_remainder_after_degree5=odd_remainder,
                degree7_tail_upper=tail_upper, legal_one_step_half_distance_lower=legal_lower,
                complex_column_dual_lower=dual_lower, maximum_gate_defect=max_deficit)


cs2 = Fraction(3, 131072)**2
assert cs2 / (50*5120*12) > Fraction(1, 10**17)
assert Fraction(32,50) < 1
assert Fraction(3,10)/(1-Fraction(1,10)**2) < 1
assert Fraction(197,191) < Fraction(129,125)
assert Fraction(2651,2048) > Fraction(129,100)
assert Fraction(5625,33282) > Fraction(4,25)
assert Fraction(199,200)**2 > Fraction(99,100)
assert Fraction(99,100)*Fraction(4,15)*Fraction(2,25) > Fraction(1,50)
assert (Fraction(1,10**27)-Fraction(1,10**30))*10**28 - Fraction(1,10**10) - Fraction(1,4000) - Fraction(2,10**9) > 9
results = [verify_width(n, seed) for n, seed in ((200, 610201), (400, 610202))]
try:
    import psutil
    memory = psutil.Process().memory_info()
    peak_ram = getattr(memory, "peak_wset", memory.rss)
except ImportError:
    peak_ram = None
output = dict(status="all independent algebra/contract checks passed",
              proof_constant_checks="exact rational arithmetic passed",
              asymptotic_certificate="analytical proof, not established by numerical checks",
              results=results, cpu_seconds=time.process_time()-START_CPU,
              wall_seconds=time.perf_counter()-START_WALL, peak_ram_bytes=peak_ram,
              gpu_seconds=0, cuda_used=False)
outpath = Path(__file__).with_name("CHECK_RESULTS.json")
replay = 1
while outpath.exists():
    replay += 1
    outpath = Path(__file__).with_name(f"CHECK_RESULTS_REPLAY_{replay}.json")
outpath.write_text(json.dumps(output, indent=2), encoding="utf-8")
print(json.dumps(output, indent=2))
