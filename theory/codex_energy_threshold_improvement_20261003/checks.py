"""Independent CPU checks, not numerical substitutes for the analytic proof.

Run: python theory/codex_energy_threshold_improvement_20261003/checks.py
Writes only this new folder; refuses to overwrite an existing checks_result.json.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import ctypes
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import platform
import sys
import time

import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "checks_result.json"
ROOT = HERE.parent.parent


def peak_ram():
    if os.name != "nt":
        return None
    from ctypes import wintypes
    class Counters(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
            (name, ctypes.c_size_t) for name in (
                "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
                "PagefileUsage", "PeakPagefileUsage")]
    get_current = ctypes.windll.kernel32.GetCurrentProcess
    get_current.restype = wintypes.HANDLE
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    get_memory = ctypes.windll.psapi.GetProcessMemoryInfo
    get_memory.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
    get_memory.restype = wintypes.BOOL
    assert get_memory(get_current(), ctypes.byref(counters), counters.cb)
    return int(counters.PeakWorkingSetSize)


def check_exact_constants():
    A = Fraction(1, 10**8)
    assert A*A*5*(50*65536)**2 < 1
    assert Fraction(1, 1) - Fraction(2, 10000) - Fraction(4, 10**9) > Fraction(9997, 10000)
    assert Fraction(3, 4) + Fraction(9, 4)*Fraction(1, 45) == Fraction(4, 5)
    assert Fraction(3, 4) + Fraction(9, 4)*Fraction(1, 27) == Fraction(5, 6)
    assert Fraction(3, 4) + Fraction(9, 4)*Fraction(1, 20) == Fraction(69, 80)
    return {"signal_constant_squared_check": True, "power_arithmetic": True,
            "coefficient_A": "1/100000000", "epsilon": "1/1000"}


def parameters(n, F, dps):
    with mp.workdps(dps):
        C = 10**14
        # EXACT integer ceil of C sqrt(n F^9); no floating-point ceil.
        radicand = C*C*n*F**9
        root = math.isqrt(radicand)
        T = root if root*root == radicand else root+1
        nn, ff, tt = mp.mpf(n), mp.mpf(F), mp.mpf(T)
        eta, A = mp.mpf("1e-6"), mp.mpf("1e-8")
        delta = eta*nn/(tt*ff**mp.mpf("1.5"))
        zeta = mp.mpf(".15")+2*delta
        d = n//4
        beta = mp.sqrt((zeta+delta)/nn)
        leading = A*delta*tt**2/(nn**mp.mpf("1.5")*ff**3)
        twist = 100*delta*tt**2/nn**2
        tail = delta**3*tt**4/nn**mp.mpf("3.5")
        margin = leading-twist-tail-mp.mpf("4e-9")
        assert T >= 4 and T <= d//2 and 2*F < T-1
        assert ff*tt/nn <= mp.mpf(".005")
        assert (1+zeta)*tt/nn <= mp.mpf(1)/3
        assert beta <= mp.mpf(".1")
        assert delta*tt/nn <= mp.mpf(".5")
        assert (2*F+1)*mp.log(1+512*mp.sqrt(d)) <= mp.mpf(d)/200
        assert d//10**6 >= nn/10**7
        assert margin > mp.mpf(".9997")
        assert 2*mp.sqrt(nn*(tt+2)) <= 4*10**7*nn**mp.mpf(".75")*ff**mp.mpf("2.25")
        return {"n": str(n), "F": F, "T": str(T), "precision_decimal_digits": dps,
                **{k: mp.nstr(v, 65) for k, v in {
                    "delta": delta, "zeta": zeta, "beta_max": beta,
                    "accumulated_defect": delta*tt/nn,
                    "baseline_duration_loss": (1+zeta)*tt/nn,
                    "leading_signal": leading, "twist_upper": twist,
                    "odd_tail_upper": tail, "margin_lower_expression": margin}.items()}}


def rotations(n):
    k, d = n//2, n//4
    tau = 1/math.sqrt(k)
    gamma = 1/(1-tau)
    w = np.full(k, -tau)
    w[0] += 1
    def U(v):
        if v.ndim == 1:
            return v-gamma*w*np.dot(w, v)
        return v-gamma*w[:, None]*(w@v)[None, :]
    def P(v):
        out = v.copy()
        out[:d] = np.roll(v[:d], 1, axis=0)
        return out
    def O(v):
        return U(P(U(v)))
    return k, d, tau, gamma, U, P, O


def check_rows():
    rng = np.random.default_rng(731)
    outputs = []
    for n in [200, 256, 401, 601, 1000]:
        k, d, tau, gamma, U, P, O = rotations(n)
        errors, maxima = [], []
        for _ in range(16):
            cycle = rng.uniform(.02, .1, size=d-1)
            v = np.zeros(k)
            v[1:d] = cycle
            v[d:2*d-1] = -cycle
            if k-2*d+1 == 1:
                v[-1] = .07
            else:
                v[-2:] = [.07, -.07]
            S = v[1:].sum()
            J = gamma*tau*v[d-1]-gamma**2*tau**2*S
            manual = np.zeros(k)
            manual[1] = J+gamma*tau*S
            manual[2:d] = v[1:d-1]+J
            manual[d:] = v[d:]+J
            err = float(np.max(np.abs(O(v)-manual)))
            errors.append(err)
            maxima.append(float(np.max(np.abs(O(v)))/.1))
            assert err < 2e-14 and abs(S) <= .1+1e-14
            assert max(abs(O(v))) < 1.5*.1
            # Exact inverse lift at R0, with source H and zero endpoint.
            state = np.r_[v, np.full(n-k, .4)]
            recurrence = np.r_[(1-1/n)*O(v), np.full(n-k, .4/(100*n))]
            hold = np.arctanh(state)-recurrence-.05
            reset = -recurrence-.05
            prep = np.r_[np.full(k, -.05), np.full(n-k, np.arctanh(.4)-.05)]
            assert max(np.max(abs(hold)), np.max(abs(reset)), np.max(abs(prep))) < .5
        outputs.append({"n": n, "max_row_identity_error": max(errors),
                        "max_rotation_infinity_ratio": max(maxima)})
    return outputs


def check_joint_kernel_and_mirror():
    n, F, T, delta = 50000, 2, 73, 20.
    k, d, tau, gamma, U, P, O = rotations(n)
    zeta = .15+2*delta
    a = 1-1/n
    g0 = 1-zeta/n
    b = a*g0
    nu = 2*np.pi*np.arange(1, F+1)/T
    f = np.floor(d*np.arange(1, F+1)/T+.5).astype(int)
    omega = 2*np.pi*f/d
    xx = np.arange(d)
    V = np.zeros((k, F), dtype=complex)
    V[:d] = np.exp(1j*xx[:, None]*omega[None, :])/math.sqrt(d)
    probes = U(V)
    assert np.max(abs(probes[0])) < 1e-14
    eig = np.exp(-1j*omega)
    assert np.max(abs(O(probes)-probes*eig[None, :])) < 2e-14
    rng = np.random.default_rng(863)
    profiles = rng.normal(size=(d, F))
    basis = [np.ones(d)/math.sqrt(d)]
    for wj in omega:
        basis.extend([np.cos(wj*xx)*math.sqrt(2/d), np.sin(wj*xx)*math.sqrt(2/d)])
    basis = np.array(basis).T
    profiles -= basis@(basis.T@profiles)
    profiles /= 2*np.max(abs(profiles), axis=0)[None, :]
    assert np.max(abs(basis.T@profiles)) < 2e-12
    plus = np.zeros_like(probes)
    minus = np.zeros_like(probes)
    Z1 = np.zeros_like(probes)
    public = np.zeros_like(probes)
    injection_errors = []
    largest_input = 0.
    for t in range(1, T+1):
        age = T-t
        c = delta/F*np.sum(profiles[(xx+age)%d]*np.cos(nu*age)[None, :], axis=1)
        D = np.zeros(k)
        D[1:d] = c[1:]
        D[d:2*d-1] = c[1:]
        virtual = np.zeros_like(probes)
        virtual[:d] = c[:, None]*V[:d]
        injection = U(D[:, None]*probes)
        err = np.linalg.norm(injection-virtual, axis=0)
        injection_errors.extend(err.tolist())
        assert max(err) <= 10*delta/math.sqrt(d)
        Q = a*O(public)+probes
        Z1 = b*O(Z1)+D[:, None]*Q/n
        public = g0*Q
        plus = (g0+D/n)[:, None]*(a*O(plus)+probes)
        minus = (g0-D/n)[:, None]*(a*O(minus)+probes)
        v = np.zeros(k)
        v[1:d] = np.sqrt((zeta-c[1:])/n)
        v[d:2*d-1] = -v[1:d]
        if k-2*d+1 == 1:
            v[-1] = math.sqrt(zeta/n)
        else:
            v[-2:] = [math.sqrt(zeta/n), -math.sqrt(zeta/n)]
        largest_input = max(largest_input, float(max(abs(np.arctanh(v)-a*O(v)-.05))))
    ages = np.arange(T)
    K = np.array([[np.sum(b**ages*np.exp(-1j*wj*ages)*np.cos(vg*ages))
                   for vg in nu] for wj in omega])
    sv = np.linalg.svd(K, compute_uv=False)
    assert min(sv) >= T/4
    assert np.max(abs(np.cos(ages[:, None]*nu).sum(axis=0))) < 2e-13
    ideal = np.zeros_like(probes)
    ideal[:d] = (delta*np.exp(1j*xx[:, None]*omega)/(n*math.sqrt(d)*F)
                *(profiles@K.T)/(1-b*np.exp(-1j*omega))[None, :])
    total_err = np.linalg.norm(Z1-U(ideal), axis=0)
    assert max(total_err) <= 10*delta*T*T/(n*math.sqrt(d))
    dressed_err = np.sum(abs(O(O(Z1))-U(P(P(ideal)))), axis=0)
    assert max(dressed_err) <= 18*delta*T*T/n
    odd_tail = np.linalg.norm((plus-minus)/2-Z1, axis=0)
    kappa = delta*T/n
    upper = (delta*T*T/n)*kappa**2/(1-kappa**2)
    assert max(odd_tail) <= upper
    assert largest_input < .5
    return {"n": n, "F": F, "T": T, "delta": delta,
            "kernel_sigma_min": float(min(sv)), "required_kernel_min": T/4,
            "max_injection_error": max(injection_errors),
            "max_accumulated_first_order_error": float(max(total_err)),
            "max_dressed_L1_error": float(max(dressed_err)),
            "max_odd_tail": float(max(odd_tail)), "odd_tail_majorant": upper,
            "max_raw_memory_input": largest_input}


def check_entropy_profile():
    # A small analytic example: multiples of frequency 3 exclude modes 1,2.
    # This checks the exact stationarity and oddness, not the Gaussian existence.
    d, F = 192, 2
    with mp.workdps(100):
        L = 128*mp.sqrt(d*F)
        B = [mp.sqrt(mp.mpf(2)/d)*mp.sin(2*mp.pi*3*i/d) for i in range(d)]
        outcomes = []
        for y in [mp.mpf(".0001"), mp.mpf(".001")]:
            s = [mp.tanh(L*z*y) for z in B]
            mean = abs(mp.fsum(s))
            excluded = []
            for f in [1, 2]:
                excluded.extend([abs(mp.fsum(s[i]*mp.cos(2*mp.pi*f*i/d) for i in range(d))),
                                 abs(mp.fsum(s[i]*mp.sin(2*mp.pi*f*i/d) for i in range(d)))])
            stationarity = max(abs(mp.atanh(si)-L*zi*y) for si, zi in zip(s, B))
            assert max([mean, *excluded, stationarity]) < mp.mpf("1e-70")
            assert all(abs(si) < 1 for si in s)
            assert all(mp.tanh(-L*zi*y) == -si for si, zi in zip(s, B))
            outcomes.append({"y": str(y), "stationarity_error": mp.nstr(stationarity, 10),
                             "max_excluded_mode": mp.nstr(max(excluded), 10)})
        return outcomes


def main():
    if OUT.exists():
        raise SystemExit("Refusing to overwrite checks_result.json")
    start, cpu = time.perf_counter(), time.process_time()
    constants = check_exact_constants()
    precision_results = []
    for exponent in [200, 240]:
        n = 10**exponent
        for F in [2, math.floor(exponent*math.log(10)), 10**(exponent//20)]:
            r1, r2 = parameters(n, F, 240), parameters(n, F, 320)
            for key in r1:
                if key != "precision_decimal_digits":
                    assert r1[key] == r2[key], (key, r1[key], r2[key])
            precision_results.append({"lower_precision": r1, "higher_precision": r2,
                                      "65_digit_agreement": True})
    results = {
        "status": "PASS", "scope": "internal analytic/algebraic checks; not an interval certificate",
        "exact_constants": constants, "explicit_parameter_checks": precision_results,
        "balanced_row_checks": check_rows(), "mirror_kernel_parity": check_joint_kernel_and_mirror(),
        "entropy_stationarity": check_entropy_profile(),
        "versions": {"python": sys.version, "numpy": np.__version__, "mpmath": mp.__version__,
                     "platform": platform.platform()},
        "GPU_used": False, "training_runs": 0,
        "CPU_seconds": time.process_time()-cpu, "wall_seconds": time.perf_counter()-start,
        "peak_process_working_set_bytes": peak_ram(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    OUT.write_text(json.dumps(results, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k: results[k] for k in ["status", "CPU_seconds", "wall_seconds",
                                             "peak_process_working_set_bytes", "GPU_used"]}))


if __name__ == "__main__":
    main()
