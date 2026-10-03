"""Exact scalar consolidation checks; no numerical experiment or external imports.

The inequalities hold for all n beyond the stated thresholds by the power
comparisons documented in PROOF.md. Checking n0 alone would not prove them.
Outputs are append-only, and independent review bytes are checked unchanged.
"""
from fractions import Fraction as Q
from pathlib import Path
import ctypes
import hashlib
import json
import os
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
start_cpu, start_wall = time.process_time(), time.perf_counter()
checks = []


def check(name, predicate, details):
    if not predicate:
        raise AssertionError(name)
    checks.append({"name": name, "pass": True, "details": details})


EPS = Q(1, 1000)
LEDGER = EPS / 4 + Q(2, 10**9)
BASE_DELTA = Q(1, 10**10)
CSAT = Q(3, 131072)
check("accepted conservative signal constant", CSAT**2 / (50*5120*12) > Q(1, 10**17),
      str(CSAT**2 / (50*5120*12)))
check("joint auxiliary amplitude", Q(1, 10**17) * BASE_DELTA == Q(1, 10**27),
      "An isolated joint component uses delta/F; joint column bound already has F^-5.")


def threshold_case(name, exponent, root, cden, p, fmin, dimension_denominator):
    # n0=10^exponent, c=1/cden, theta=1/root, delta=10^-10/F^p.
    # All chosen roots and coefficient powers are exact integer powers of 10.
    check(name + ": threshold root", exponent % root == 0, str(exponent // root))
    x0 = Q(10**(exponent // root), cden)
    check(name + ": positive floor", x0 >= fmin, str(x0))
    check(name + ": floor lower", x0 >= 2,
          "For every x>=2: floor(x)>=x/2; x(n) is increasing.")
    power = 5 + p
    cden_power = len(str(cden)) - 1
    check(name + ": decimal coefficient", cden == 10**cden_power, str(cden))
    scale_power = Q(exponent, 2) - power*Q(exponent, root) + power*cden_power
    check(name + ": leading bound exponent", scale_power.denominator == 1, str(scale_power))
    leading = Q(10**scale_power.numerator, 10**27)
    # For p=3 the cubic/leading ratio is 10^-3/F. For p=5/2 it is 10^-3.
    ratio_power = 5 - 2*p
    check(name + ": cubic ratio exponent", ratio_power in (0, -1), str(ratio_power))
    ratio = Q(1, 1000) if ratio_power == 0 else Q(1, 1000*fmin)
    half = leading*(1-ratio) - BASE_DELTA - LEDGER
    check(name + ": uniform strict half-margin", half > 9,
          {"leading_lower": str(leading), "cubic_over_leading_upper": str(ratio),
           "uniform_half_margin_lower": str(half), "decimal_display_only": float(half)})
    # h=2F+1<=3F<=3 c n^theta; d>=n/5. Sufficient n^(1-theta)>=61440 c.
    growth = 10**(exponent - exponent//root)
    check(name + ": spreading dimension", growth >= Q(61440, cden),
          "n^(1-theta)>=61440*c, increasing with n; implies 2F+1<=d/4096.")
    check(name + ": cycle/non-aliasing", growth > Q(20, cden),
          "F<n/20<=d/4; h<=d/4096 also implies d-1>2F when d>=2e6.")
    check(name + ": spreading floor", 10**exponent >= 10**7,
          "d>=n/5>=2e6; floor(d/1e6)>=d/(2e6).")
    check(name + ": dimension denominator", dimension_denominator == 20_000_000*cden,
          "qF >= c*n^(1+theta)/20,000,000, with every floor retained.")
    check(name + ": gate admissibility", BASE_DELTA < Q(1, 10),
          "p>0 and F>=1 imply delta<=1e-10; all words remain in the reviewed gate box.")
    return {"name": name, "n0": "10^"+str(exponent), "theta": str(Q(1, root)),
            "c": str(Q(1, cden)), "delta_power": str(p),
            "dimension_power": str(1+Q(1, root)), "dimension_denominator": dimension_denominator,
            "uniform_half_margin_lower": str(half), "leading_lower": str(leading)}


cases = [
    threshold_case("accepted 19/18", 504, 18, 1, Q(3), 1, 20_000_000),
    threshold_case("Grok 17/16 unchanged amplitude", 80, 16, 10_000, Q(3), 10, 200_000_000_000),
    threshold_case("same-ledger amplitude-balanced 16/15", 75, 15, 10_000, Q(5, 2), 10, 200_000_000_000),
]

# General exponents: p=3 => 1/2-8theta; optimal balance p=5/2 => 1/2-(15/2)theta.
check("frozen-amplitude boundary", Q(1, 2)-8*Q(1, 16) == 0, "theta=1/16")
check("amplitude-balanced boundary", Q(1, 2)-Q(15, 2)*Q(1, 15) == 0, "theta=1/15")
check("earlier 7/6 sketch power", Q(1, 2)-8*Q(1, 6) == Q(-5, 6),
      "Even balanced amplitude has exponent 1/2-(15/2)/6=-3/4.")
check("optimized ledger coefficient squared",
      (Q(2, 3)**2 * Q(1, 3)) * Q(1, 10**51) == Q(4, 27*10**51),
      "max_delta(A*delta-B*delta^3)=2*A^(3/2)/(3*sqrt(3B)); square checked exactly.")

review_hashes = {
    "theory/grok_multiharmonic_lower_review_20261002/REPORT.md":
        "a21683015d8a1b26be2dd118588c6635add7b5f19cf9c9dc22ffb69210c326c3",
    "theory/grok_multiharmonic_lower_review_20261002/probe.py":
        "35d21fc8540d768b2d9cc9f26503da7a4f4fa26aeee3a830bd6aa6fa11fc7560",
}
for rel, expected in review_hashes.items():
    actual = hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
    check("review unchanged: " + rel, actual == expected, actual)


def peak_ram():
    if os.name != "nt":
        return None
    class Counters(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in ["PeakWorkingSetSize", "WorkingSetSize",
            "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
            "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage"]]
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(Counters), ctypes.c_ulong]
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
        raise ctypes.WinError(ctypes.get_last_error())
    return counters.PeakWorkingSetSize


ram = peak_ram()
result = {"status": "PASS", "checks": checks, "cases": cases,
          "cpu_seconds": time.process_time()-start_cpu,
          "wall_seconds": time.perf_counter()-start_wall, "peak_ram_bytes": ram,
          "gpu_used": False, "numerical_experiment": False,
          "scope": "Exact rational arithmetic plus documented symbolic all-n inequalities; not independent hostile review."}
index = 1
while (HERE/f"ARITHMETIC_{index}.json").exists():
    index += 1
target = HERE/f"ARITHMETIC_{index}.json"
with target.open("x", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2)
print(json.dumps({"status": result["status"], "checks": len(checks), "output": str(target),
                  "cases": cases, "cpu_seconds": result["cpu_seconds"],
                  "wall_seconds": result["wall_seconds"], "peak_ram_bytes": ram}, indent=2))
