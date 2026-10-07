"""Small algebra/sanity checks. NOT a certificate of robust dimension.

Python standard library only. One arithmetic thread, no workers or GPU.
The actual every-width proof is PROOF.md, not these finite samples.
"""
import os

for _name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
              "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_name] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import ctypes
import json
import math
import random
import time
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

start_cpu = time.process_time()
start_wall = time.perf_counter()
peak_threads = 0
peak_ram = 0
records = []


def resources():
    global peak_threads, peak_ram
    if os.name == "nt":
        from ctypes import wintypes as w
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)

        class ThreadEntry(ctypes.Structure):
            _fields_ = [("size", w.DWORD), ("usage", w.DWORD),
                        ("thread_id", w.DWORD), ("owner_id", w.DWORD),
                        ("base", w.LONG), ("delta", w.LONG), ("flags", w.DWORD)]

        kernel.CreateToolhelp32Snapshot.restype = w.HANDLE
        kernel.Thread32First.argtypes = [w.HANDLE, ctypes.POINTER(ThreadEntry)]
        kernel.Thread32Next.argtypes = [w.HANDLE, ctypes.POINTER(ThreadEntry)]
        kernel.CloseHandle.argtypes = [w.HANDLE]
        snapshot = kernel.CreateToolhelp32Snapshot(4, 0)
        entry = ThreadEntry()
        entry.size = ctypes.sizeof(entry)
        count = 0
        okay = kernel.Thread32First(snapshot, ctypes.byref(entry))
        while okay:
            count += entry.owner_id == os.getpid()
            okay = kernel.Thread32Next(snapshot, ctypes.byref(entry))
        kernel.CloseHandle(snapshot)

        class Memory(ctypes.Structure):
            _fields_ = [("cb", w.DWORD), ("faults", w.DWORD)] + [
                (key, ctypes.c_size_t) for key in
                ("peak_ws", "ws", "peak_paged", "paged", "peak_nonpaged",
                 "nonpaged", "pagefile", "peak_pagefile")]

        kernel.GetCurrentProcess.restype = w.HANDLE
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [w.HANDLE, ctypes.POINTER(Memory), w.DWORD]
        memory = Memory()
        memory.cb = ctypes.sizeof(memory)
        assert psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),
                                         ctypes.byref(memory), memory.cb)
        peak_ram = max(peak_ram, memory.peak_ws)
        peak_threads = max(peak_threads, count)
        assert count <= 8, "STOP: thread budget exceeded"
        assert peak_ram < 100 * 1024 * 1024, "STOP: RAM guard exceeded"
    assert time.perf_counter() - start_wall < 30, "STOP: tiny-check time budget exceeded"


def check(name, condition, detail=None):
    assert condition, name
    records.append({"name": name, "passed": True, "detail": detail})


resources()
check("exact query constant exceeds .4",
      F(499, 10000) * F(999, 1000) * F(17, 100) * F(5, 10000)
      * F(998, 1000) * 100000 > F(2, 5))
check("gate dissipative coefficient", 1 - F(9992, 10000) ** 2 > F(15, 10000))
check("rank-one energy y coefficient", F(8, 6000) < F(15, 10000))
check("frame unsaturated fraction", 1 - F(9, 16) == F(7, 16))
check("uniform net loss leaves enough full controls",
      F(1, 10000) - F(9, 4) * F(1, 1000000) > F(1, 20000))
check("frame rate below unsaturated fraction", F(1, 10**9) < F(7, 16))
check("net op Chernoff exponent", -81 / 640 + .5 * math.log(1.25) < -.01)
check("elementary Gaussian interval probability", 2 * math.exp(-8) / math.sqrt(2*math.pi) > 1/5000)
check("code failure union below one at K threshold",
      math.log(2001) / 10**9 - 1/40000 < -1/50000
      and math.log(9) / 10**9 - 1/100 < -1/200)

for K in (2, 3, 4, 16, 48, 1000):
    coefficient_sq = F(K**2, (2*K-1)**2 * 2*(K+1))
    check(f"calibration lower K={K}", coefficient_sq >= F(1, 8*K))
    check(f"frame upper K={K}", F(2*K, K+1) < 2)

# The new auxiliary complementary inequality, tested on its exact 3D quotient.
# These floating checks attack the algebra; the written energy argument proves it.
rng = random.Random(71417)
worst_loss_ratio = 1.0
for _ in range(1000):
    high_weight = .001 + .04*rng.random()
    gamma = 1.00001
    outside_weight = gamma - high_weight
    partition = .1 + .8*rng.random()
    rr = [math.sqrt(high_weight), math.sqrt(outside_weight*partition),
          math.sqrt(outside_weight*(1-partition))]
    xx = [rng.uniform(-1, 1) for _ in range(3)]
    dot = sum(x*r for x, r in zip(xx, rr))
    rx = [x-r*dot for x, r in zip(xx, rr)]
    gates = [.999999, .995, .99 + .0092*rng.random()]
    yy = [g*x for g, x in zip(gates, rx)]
    norm = sum(x*x for x in xx)
    loss = norm - sum(y*y for y in yy)
    worst_loss_ratio = min(worst_loss_ratio, loss/norm/high_weight)
check("exploratory auxiliary quotient dissipates", worst_loss_ratio >= 1/6000,
      {"samples": 1000, "minimum_ratio": worst_loss_ratio})
resources()

# Small public clipped-code example. Sphere sampling is evidence only.
toy_K, toy_q = 512, 2
BB = [[rng.gauss(0, 1) for _ in range(toy_q)] for _ in range(toy_K)]
min_full = toy_K
max_norm_squared = 0.0
for sample in range(256):
    angle = 2*math.pi*sample/256
    yy = [math.cos(angle), math.sin(angle)]
    values = [sum(b*y for b, y in zip(row, yy)) for row in BB]
    min_full = min(min_full, sum(abs(value) >= 2 for value in values))
    max_norm_squared = max(max_norm_squared, sum(value*value for value in values))
check("exploratory clipped-code sphere example", min_full > 0,
      {"K": toy_K, "q": toy_q, "directions": 256, "minimum_full_entries": min_full,
       "max_sample_norm_squared_over_K": max_norm_squared/toy_K,
       "not_a_uniform_certificate": True})

# Exact Walsh mask identity and preservation of the earlier bit.
labels = [(b1, b2) for b1 in (0, 1) for b2 in (0, 1)]
def character(bits):
    return [(-1) ** sum(label[j] for j in bits) for label in labels]
aa, bb = F(3, 4), F(1, 8)
chi1, chi2, chi12 = character((0,)), character((1,)), character((0, 1))
mask = [aa + bb*x for x in chi2]
written = [x*g for x, g in zip(chi1, mask)]
check("exact fresh-bit Walsh identity",
      written == [aa*x+bb*z for x, z in zip(chi1, chi12)])
check("later singleton annihilates earlier write",
      sum(x*y for x, y in zip(written, chi2)) == 0)

with localcontext() as context:
    context.prec = 70
    LL = Decimal(3000) * Decimal(10).ln()
    mask_envelope = Decimal(2*10**8) / LL**5
    check("worst-range mask envelope at threshold", mask_envelope < Decimal(".000001"),
          str(mask_envelope))
    for beta in (Decimal(".5"), Decimal(".75"), Decimal(".875"), Decimal(".99")):
        onset = max(Decimal(3000), Decimal(200)/(1-beta)**2)
        logarithm = onset*Decimal(10).ln()
        check(f"power specialization beta={beta}",
              (1-beta)*logarithm >= 12*logarithm.ln())

resources()
payload = {
    "role": "small algebra checks; not proof of robust dimension",
    "all_passed": all(r["passed"] for r in records),
    "check_count": len(records), "checks": records,
    "resources": {"arithmetic_threads": 1, "worker_processes": 0,
                  "observed_peak_process_threads": peak_threads,
                  "peak_working_set_bytes": peak_ram,
                  "cpu_seconds": time.process_time()-start_cpu,
                  "wall_seconds": time.perf_counter()-start_wall,
                  "gpu_cuda_usage": 0, "numpy_blas_torch_imports": 0,
                  "thread_pool_environment": {key: os.environ[key] for key in
                      ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS")}},
}
output = Path(__file__).with_name("checks_result.json")
output.write_text(json.dumps(payload, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"passed": payload["check_count"], "resources": payload["resources"]}, indent=2))
