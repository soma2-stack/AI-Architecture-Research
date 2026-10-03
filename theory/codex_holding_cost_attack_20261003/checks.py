"""Small independent sanity checks. These calculations are NOT certificates.

One process, one numerical compute thread; no CUDA/PyTorch/GPU imports.
Run directly from this directory. All outputs stay in this new folder.
"""
import os

POOL_KEYS = (
    "OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS",
    "OMP_THREAD_LIMIT", "TBB_NUM_THREADS",
)
for _key in POOL_KEYS:
    os.environ[_key] = "1"
os.environ["OMP_MAX_ACTIVE_LEVELS"] = "1"
os.environ["OMP_DYNAMIC"] = "FALSE"
os.environ["MKL_DYNAMIC"] = "FALSE"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["NVIDIA_VISIBLE_DEVICES"] = "void"

import hashlib
import json
import math
import pathlib
import time
from fractions import Fraction

import mpmath as mp
import numpy as np
import psutil

HERE = pathlib.Path(__file__).resolve().parent
PROC = psutil.Process()
START = time.perf_counter()
CPU_START = sum(PROC.cpu_times()[:2])
PEAK_THREADS = 0
PEAK_RSS = 0
ITEMS = []


def resources():
    global PEAK_THREADS, PEAK_RSS
    threads = PROC.num_threads()
    rss = PROC.memory_info().rss
    PEAK_THREADS = max(PEAK_THREADS, threads)
    PEAK_RSS = max(PEAK_RSS, rss)
    if threads > 8 or rss > 256 * 1024**2 or PROC.children(recursive=True):
        raise RuntimeError(f"Resource limit: threads={threads}, rss={rss}")


def check(name, condition, **values):
    resources()
    ITEMS.append(dict(name=name, passed=bool(condition), values=values))
    if not condition:
        raise AssertionError(name)


def ceil_sqrt_integer(value):
    root = math.isqrt(value)
    return root if root * root == value else root + 1


def exact_parameter_checks():
    eta, constant, signal_a = Fraction(1, 10**6), 10**14, Fraction(1, 10**8)
    for exponent in (200, 240):
        n = 10**exponent
        for f in (2, int(exponent * math.log(10)), 10**(exponent // 16)):
            t = ceil_sqrt_integer(constant**2 * n * f**6)
            delta = eta * n / (t * f)
            zeta = Fraction(3, 20) + 2 * delta
            # Compare rational squares to avoid any ordinary floating rank/error test.
            leading_sq = (signal_a * delta * t**2)**2 / (n**3 * f**4)
            tail_sq = (delta**3 * t**4)**2 / n**7
            twist = 100 * delta * t**2 / n**2
            row_bound = eta + Fraction(9 * f * t, n)
            check(f"exact_parameters_n10^{exponent}_F{f}",
                  leading_sq >= 1 and tail_sq <= Fraction(1, 5000)**2
                  and twist < Fraction(1, 10**60)
                  and row_bound < Fraction(1, 4096)
                  and (1 + zeta) * t / n < Fraction(1, 3)
                  and (zeta + delta) / n < Fraction(1, 100)
                  and t <= (n // 4) // 2 and 2 * f < t - 1,
                  T=str(t), delta=str(delta), row_bound=str(row_bound))
            numerical = []
            for bits in (240, 320):
                with mp.workprec(bits):
                    nn, tt, ff = mp.mpf(n), mp.mpf(t), mp.mpf(f)
                    dd = mp.mpf(delta.numerator) / delta.denominator
                    leading = mp.mpf("1e-8") * dd * tt**2 / (nn**mp.mpf("1.5") * ff**2)
                    tail = dd**3 * tt**4 / nn**mp.mpf("3.5")
                    margin = leading - tail - 100 * dd * tt**2 / nn**2 - mp.mpf("4e-9")
                    numerical.append(mp.nstr(margin, 55))
            with mp.workprec(200):
                agreement = abs(mp.mpf(numerical[0]) - mp.mpf(numerical[1])) < mp.mpf("1e-45")
            check(f"precision_agreement_n10^{exponent}_F{f}", agreement,
                  precisions_bits=[240, 320], margins=numerical)


def source_checks():
    with mp.workprec(300):
        old = ((mp.atanh(mp.mpf(".4")) - mp.mpf(".05"))**2 + mp.mpf(".05")**2) / 2
        source_fraction = 1 - mp.mpf(".00125") / old
        ratio = mp.sqrt(mp.mpf(".00125") / old)
        check("energy_coefficients", old > mp.mpf(".07"),
              old_squared_coefficient=mp.nstr(old, 50),
              old_source_fraction=mp.nstr(source_fraction, 50),
              autonomous_squared_coefficient=".00125",
              new_to_old_norm_ratio=mp.nstr(ratio, 50))
        for n in (200, 8192, 10**200):
            lam = 1 / (100 * mp.mpf(n))
            sigma = mp.findroot(lambda s: s - mp.tanh(lam * s + mp.mpf(".05")), mp.mpf(".05"))
            check(f"autonomous_source_n{n}",
                  mp.mpf(".0499") < sigma < mp.mpf(".05") + lam
                  and abs(mp.atanh(sigma) - mp.mpf(".05") - lam * sigma) < mp.mpf("1e-75"),
                  sigma=mp.nstr(sigma, 60))


def temporal_kernel_check():
    # A small toy parameter check of the exact kernel formula, not a new witness.
    f, t, d, b = 3, 64, 4096, 1 - 1e-7
    tau = np.arange(t)
    nu = 2 * np.pi * np.arange(1, f + 1) / t
    omega = 2 * np.pi * np.rint(d * np.arange(1, f + 1) / t) / d
    ideal = np.exp(-1j * nu[:, None] * tau) @ np.cos(nu[:, None] * tau).T
    actual = (b**tau * np.exp(-1j * omega[:, None] * tau)) @ np.cos(nu[:, None] * tau).T
    cap = ((1 - b) + np.pi / d) * t * (t - 1) / 2
    check("temporal_diagonal_dominance", np.max(np.abs(ideal - t/2 * np.eye(f))) < 1e-12
          and np.max(np.abs(actual - ideal)) <= cap,
          maximum_entry_error=float(np.max(np.abs(actual - ideal))), analytic_cap=float(cap))


def corridor_checks():
    # n is deliberately much smaller than the analytic theorem threshold. This
    # is a cheap identity check, not a certificate for this width.
    n, m, tmax, f = 8192, 8, 32, 2
    k, l, d = n//2, n-n//2, n//4
    a, lam = 1 - 1/n, 1/(100*n)
    span = m + tmax + 4
    aa, bb = 2 * span, 5 * span
    gamma = 1 / (1 - 1 / np.sqrt(k))
    w = np.full(k, -1 / np.sqrt(k)); w[0] += 1
    with mp.workprec(160):
        sigma = float(mp.findroot(lambda s: s - mp.tanh(mp.mpf(lam)*s + mp.mpf(".05")), .05))

    def house(v):
        return v - gamma * w[:, None] * (w @ v)[None, :] if v.ndim == 2 else v - gamma * w * (w @ v)

    def rotate(v):
        z = house(v)
        z = z.copy()
        z[:d] = np.roll(z[:d], 1, axis=0)
        return house(z)

    z_indices = np.arange(aa + 2, aa + m + tmax + 1)
    ll = len(z_indices)
    frame = np.zeros((k, ll))
    frame[z_indices, np.arange(ll)] = 1/np.sqrt(2)
    frame[z_indices + 3*span, np.arange(ll)] = -1/np.sqrt(2)
    profiles = np.array([np.cos(np.arange(m)), np.sin(2 * np.arange(m) + .2)])
    delta, zeta = .3, .75
    histories = []
    for parameter in (-.7, 0., .7):
        prev = np.zeros(k)
        initial_beta = np.full(m, np.sqrt(zeta/n))
        idx0 = aa + np.arange(1, m+1)
        prev[idx0] = initial_beta
        prev[idx0 + 3*span] = initial_beta
        prev[d:d+2*m] = -np.tile(initial_beta, 2)
        prep = np.arctanh(prev) - .05
        energy = float(prep @ prep) + l * (lam*sigma)**2
        credit = np.zeros((k, ll))
        gates = np.empty((m, tmax))
        path, maximum_input = [prev.copy()], float(np.max(np.abs(prep)))
        for t in range(1, tmax+1):
            prior_rot = rotate(prev)
            current = np.tanh(a*prior_rot + .05)
            cosines = np.cos(2*np.pi*np.arange(1,f+1)*(tmax-t)/tmax)
            modulation = parameter * delta/f * (cosines @ profiles)
            beta = np.sqrt((zeta-modulation)/n)
            idx = aa + np.arange(1,m+1) + t
            driven = np.concatenate([idx, idx+3*span, np.arange(d,d+2*m)])
            current[idx] = beta; current[idx+3*span] = beta
            current[d:d+2*m] = -np.tile(beta, 2)
            # Outside input is exactly zero: do not invert saturated autonomous states.
            xx = np.arctanh(current[driven]) - a*prior_rot[driven] - .05
            energy += float(xx @ xx)
            maximum_input = max(maximum_input, float(np.max(np.abs(xx))))
            credit = (1-current**2)[:, None] * (a*rotate(credit) + frame)
            gates[:,t-1] = 1-beta**2
            prev = current; path.append(prev.copy()); resources()
        idx = aa + np.arange(1,m+1) + tmax
        paired_rows = (credit[idx] - credit[idx+3*span]) / np.sqrt(2)
        kernel = np.zeros((m,ll))
        for i in range(1,m+1):
            for j in range(1,tmax+1):
                z = aa+i+j
                kernel[i-1,z-z_indices[0]] = a**(tmax-j) * np.prod(gates[i-1,j-1:])
        error = float(np.max(np.abs(paired_rows-kernel)))
        check(f"coupled_kernel_parameter_{parameter}", error < 2e-12, maximum_error=error)
        prior_rot = rotate(prev)
        endpoint = np.tanh(a*prior_rot+.05)
        bulk = float(endpoint[2*span-1])
        resetidx = idx+1
        driven = np.concatenate([resetidx,resetidx+3*span,np.arange(d,d+2*m)])
        endpoint[driven] = bulk
        reset_inputs = np.arctanh(endpoint[driven])-a*prior_rot[driven]-.05
        energy += float(reset_inputs @ reset_inputs)
        maximum_input = max(maximum_input,float(np.max(np.abs(reset_inputs))))
        credit_reset = (1-endpoint**2)[:,None] * (a*rotate(credit)+frame)
        check(f"corridor_admissibility_parameter_{parameter}", maximum_input < .5
              and energy < 4*(n+2*m*(tmax+1)),
              maximum_reference_raw_input=maximum_input, reference_total_energy_squared=energy,
              endpoint_bulk=bulk)
        histories.append(dict(path=path, endpoint=endpoint, kernel=kernel,
                              reset_credit=credit_reset, final_credit=credit, energy=energy))
    left, right = histories[0],histories[2]
    endpoint_error = float(np.max(np.abs(left["endpoint"]-right["endpoint"])))
    check("exact_common_endpoint_numeric", endpoint_error < 2e-14, maximum_error=endpoint_error)
    for t in range(tmax+1):
        idx = aa+np.arange(1,m+1)+t
        mask = np.ones(k,dtype=bool)
        mask[np.concatenate([idx,idx+3*span,np.arange(d,d+2*m)])] = False
        error = float(np.max(np.abs(left["path"][t][mask]-right["path"][t][mask])))
        check(f"public_bath_step_{t}", error < 2e-14, maximum_error=error)
    dcredit = left["final_credit"]-right["final_credit"]
    idx = aa+np.arange(1,m+1)+tmax
    mask = np.ones(k,dtype=bool); mask[np.concatenate([idx,idx+3*span])] = False
    check("private_credit_support", np.max(np.abs(dcredit[mask])) < 2e-12,
          maximum_off_support=float(np.max(np.abs(dcredit[mask]))))
    xi = np.where(np.arange(m)%2, -1., 1.)
    ghi,glo = 1/np.cosh(.25)**2,1/np.cosh(.75)**2
    sgate = (ghi-glo)/2
    gf = np.full(k,(ghi+glo)/2)
    gf[idx+2] = (ghi+glo)/2+sgate*xi
    gf[idx+2+3*span] = (ghi+glo)/2-sgate*xi
    ds = left["reset_credit"]-right["reset_credit"]
    actual = sigma*np.sqrt(l)/(n*np.sqrt(n)) * (a*rotate(ds)).T @ gf
    gr = 1-left["endpoint"][idx[0]+1]**2
    coefficient = sigma*a*a*gr*sgate*np.sqrt(2*l/n)/n
    predicted = coefficient*(left["kernel"]-right["kernel"]).T @ xi
    qerror = float(np.max(np.abs(actual-predicted)))
    check("legal_projected_query_duality", qerror < 1e-16,
          maximum_error=qerror, coefficient=coefficient, one_query_distance=float(np.linalg.norm(actual)))
    max_col = 0.
    for i in (1,2,d//2,d-2):
        v = np.zeros(k); v[i] = 1
        expected = np.zeros(k); expected[i+1] = 1
        max_col = max(max_col, float(np.linalg.norm(rotate(v)-expected)))
    check("ordinary_column_leak", max_col <= 6/np.sqrt(n),
          maximum_leak=max_col, claimed_cap=6/np.sqrt(n))
    ITEMS.append(dict(name="corridor_metadata", passed=True, values=dict(
        n=n,m=m,T=tmax,F=f,frame_columns=ll,
        status="DOUBLE-PRECISION IDENTITY CHECK ONLY; no robust dimension inferred")))


def main():
    resources()
    exact_parameter_checks()
    source_checks()
    temporal_kernel_check()
    corridor_checks()


if __name__ == "__main__":
    outcome = "PASS"
    try:
        main()
    except Exception as exc:
        outcome = "FAIL"
        ITEMS.append(dict(name="first_failure", passed=False, values=dict(error=repr(exc))))
    resources()
    report = dict(outcome=outcome, checks=ITEMS,
                  resource_settings={key:os.environ[key] for key in POOL_KEYS},
                  cuda_visible_devices=os.environ["CUDA_VISIBLE_DEVICES"],
                  gpu_used=False, worker_processes=0,
                  peak_process_threads=PEAK_THREADS, peak_rss_bytes=PEAK_RSS,
                  process_peak_working_set_bytes=PROC.memory_info().peak_wset,
                  cpu_seconds=sum(PROC.cpu_times()[:2])-CPU_START,
                  wall_seconds=time.perf_counter()-START,
                  script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
                  numpy_version=np.__version__, mpmath_version=mp.__version__)
    target = HERE / "checks_result.json"
    if target.exists():
        raise RuntimeError("Preserve prior output; choose a new execution log name before rerunning")
    target.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({key:report[key] for key in ["outcome","peak_process_threads","peak_rss_bytes","cpu_seconds","wall_seconds"]}))
    raise SystemExit(0 if outcome == "PASS" else 1)
