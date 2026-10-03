"""CPU-only arithmetic checks of NEW energy formulas, not an old-proof replay.

No witness search, sensitivity experiment, GPU or model server. Diagnostic
float/high-precision numbers supplement the written all-width inequalities.
"""
import os
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[key] = "1"
from pathlib import Path
from fractions import Fraction as F
import ctypes
import json
import time
import mpmath as mp
import numpy as np

HERE = Path("/tmp/claude-0/-home-user-AI-Architecture-Research/41f5f24e-9d59-52c8-b10d-d67473801e1c/scratchpad/wf_scope")
start_cpu, start_wall = time.process_time(), time.perf_counter()
checks = []


def record(name, ok, detail):
    if not ok:
        raise ArithmeticError(name)
    checks.append({"name": name, "pass": bool(ok), "detail": detail})


b0 = F(1, 20)
min_coefficient = b0-F(1, 20_000)-F(8, 10**8*200**2)
record("terminal coefficient all n >= 200", min_coefficient > F(499, 10_000),
       str(min_coefficient))
energy_coefficient = F(499, 10_000)**2/2
record("width-energy rational constant", energy_coefficient == F(249_001, 200_000_000),
       str(energy_coefficient))
record("frozen local radius", F(970_048, 10**8) < F(1, 50),
       "accepted 0.00970048, counted only as a local perturbation")


def scalars(n, precision):
    with mp.workdps(precision):
        nn = mp.mpf(n)
        k, ell = n//2, n-n//2
        a, lam, s, b = 1-1/nn, 1/(100*nn), mp.mpf(2)/5, mp.mpf(1)/20
        beta = mp.sqrt(mp.mpf(3)/(20*nn))
        A, B = mp.atanh(s), mp.atanh(beta)
        N = int(mp.ceil(4*nn*mp.log(nn)))+1
        mem = k*(2*b*b+N*((B-b)**2+a*a*beta*beta))
        src = ell*((A-b)**2+N*(A-b-lam*s)**2+(b+lam*s)**2)
        E0 = mp.sqrt(mem+src)
        dense = 4/(10**8*nn**2)*mp.sqrt(s*s*ell+N*(beta*beta*k+s*s*ell))
        terminal = (b-lam)*mp.sqrt(ell)-4/(10**8*nn**mp.mpf("1.5"))
        r = k-1
        Bn = b*mp.sqrt(r)-(a+1/(1-1/(4*nn)))*mp.sqrt(r/(4*nn)) - 4/(10**8*nn**mp.mpf("1.5"))
        constant = mp.sqrt(2*(b*b+(A-b)**2))
        return {
            "n": n, "N": N, "history_length": N+2,
            "E0": mp.nstr(E0, 55), "dense_norm_enclosure_radius": mp.nstr(dense, 55),
            "memory_energy": mp.nstr(mem, 55), "source_energy": mp.nstr(src, 55),
            "preparation_norm": mp.nstr(mp.sqrt(k*b*b+ell*(A-b)**2), 55),
            "terminal_lower": mp.nstr(terminal, 55),
            "weak_transition_lower": mp.nstr(Bn, 55),
            "weak_window_lower": mp.nstr(mp.sqrt(N-1)*max(mp.mpf(0), Bn), 55),
            "E0_over_n_sqrt_log_n": mp.nstr(E0/(nn*mp.sqrt(mp.log(nn))), 55),
            "C_abs": mp.nstr(constant, 55),
        }


rows = []
for n in (200, 256, 400, 1000, 2000, 10**6):
    low, high = scalars(n, 80), scalars(n, 120)
    record(f"80/120 decimal precision scalar agreement n={n}", low == high,
           "all saved 55-digit scalars and ceiling integers agree; numerical cross-check, not an interval certificate")
    rows.append(high)


def matrix_formula(n):
    k, ell, d = n//2, n-n//2, n//4
    w = -np.ones(k)/np.sqrt(k)
    w[0] += 1
    U = np.eye(k)-2*np.outer(w, w)/(w@w)
    P = np.eye(k)
    P[:d, :d] = np.roll(np.eye(d), 1, axis=0)
    O = U@P@U
    ones = np.ones(k)
    orth = abs(ones@O@ones)
    record(f"Householder center orthogonality n={n}", orth < 1e-10,
           {"absolute_error": float(orth), "expected": 0})
    R0 = np.zeros((n, n))
    R0[:k, :k] = (1-1/n)*O
    R0[k:, k:] = np.eye(ell)/(100*n)
    p = np.r_[np.zeros(k), np.full(ell, .4)]
    v = np.r_[np.full(k, np.sqrt(.15/n)), np.full(ell, .4)]
    q = np.arctanh(v)-.05
    N = int(np.ceil(4*n*np.log(n)))+1
    def energy(R):
        return (np.linalg.norm(np.arctanh(p)-.05)**2
                + np.linalg.norm(q-R@p)**2
                + (N-1)*np.linalg.norm(q-R@v)**2
                + np.linalg.norm(R@v+.05)**2)
    expected = float(scalars(n, 80)["E0"])
    err = abs(np.sqrt(energy(R0))-expected)
    record(f"direct transition formula vs closed scalar formula n={n}", err < 1e-10,
           {"norm_error": float(err), "norm": expected, "counted_steps": N+2})
    # An arbitrary bounded perturbation tests the sandwich algebra. This is
    # not a new model witness or a replacement for the archived public R.
    e = 4/(10**8*n*n)
    test_R = R0+(e/2)*np.ones((n,n))/n
    direct_diff = abs(np.sqrt(energy(test_R))-expected)
    budget = e*np.sqrt(p@p+N*(v@v))
    record(f"bounded matrix perturbation sandwich n={n}", direct_diff <= budget+1e-11,
           {"norm_change": float(direct_diff), "bound": float(budget),
            "scope": "algebra check; not the archived dense witness"})


for n in (200, 256, 400):
    matrix_formula(n)


import resource
class _MC: pass
mc=_MC(); mc.PeakWorkingSetSize=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
result = {"checks": checks, "check_count": len(checks), "rows": rows,
          "CPU_seconds": time.process_time()-start_cpu,
          "wall_seconds": time.perf_counter()-start_wall,
          "peak_RAM_bytes": mc.PeakWorkingSetSize,
          "GPU_seconds": 0, "CUDA_used": False,
          "scope": "new energy arithmetic only; accepted robust theorem not re-reviewed"}
output = HERE/"ARITHMETIC_linux_replay.json"
if output.exists():
    raise FileExistsError("Preserve historical output; choose a new explicit output name before rerun")
output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"checks_passed": len(checks), "C_abs": rows[0]["C_abs"],
                  "rows": [{k: row[k] for k in ("n", "E0", "terminal_lower", "weak_window_lower")} for row in rows],
                  "CPU_seconds": result["CPU_seconds"], "peak_RAM_bytes": result["peak_RAM_bytes"]}, indent=2))
