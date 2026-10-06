"""Tiny exact arithmetic/identity checks; not proof of asymptotic dimension.

No historical checks are executed. One arithmetic thread, no workers,
no NumPy/BLAS/PyTorch and no GPU. Guarded Windows resource measurements.
"""
import os
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
            "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import ctypes
import json
import math
import time
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

start_cpu, start_wall = time.process_time(), time.perf_counter()
peak_threads, peak_ram, records = 0, 0, []


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
        assert count <= 8, "STOP: thread guard exceeded"
        assert peak_ram < 100 * 1024 * 1024, "STOP: RAM guard exceeded"
    assert time.perf_counter() - start_wall < 30, "STOP: tiny-check duration exceeded"


def check(name, condition, detail=None):
    assert condition, name
    records.append({"name": name, "passed": True, "detail": detail})


resources()
check("exact query constant >1.69",
      F(499, 10000)*F(999, 1000)*F(17, 100)*F(2, 10**6)*F(998, 1000)*10**8
      > F(169, 100))
check("single contrast gives >4.2e-6 protected row",
      F(249, 100000)*F(172, 100000) > F(42, 10**7))
check("retention/reset slack >2e-6",
      F(42, 10**7)*F(999, 1000)*F(997, 1000)*F(98, 100) > F(2, 10**6))
check("full short-packet necessary time", F(2, 1000)/F(95982, 10**6) > F(20837, 10**6))
check("finite-stage dimension coefficient", F(1, 1)/F(4, 100) == 25)
check("raw norm coefficient", 4*4*10**8 < 50000**2)
check("loglog specialization cost coefficient", F(4*10**8, 10**20) == F(4, 10**12))
check("loglog specialization norm coefficient", F(50000, 10**10) == F(5, 10**6))

# Exact complete rank-two transport at k=64 (sqrt(k)=8), selected r=63.
# This tests an algebraic identity, not legal-corridor feasibility at width 64.
k, d, r = 64, 32, 63
gamma, cc = F(8, 7), F(1, 49)
aa, gh, gl = F(99, 100), F(999, 1000), F(995, 1000)
surv = [40, 41, 42, 43]
donor = [44, 45, 46, 47]
chi1, chi2 = [1, 1, -1, -1], [1, -1, 1, -1]


def transport(x):
    mass = sum(x)
    jj = gamma*x[d-2]/8-cc*mass  # physical terminal index d-1
    bb = gamma*mass/8
    y = [jj+bb]
    for physical in range(2, k):
        predecessor = x[physical-2] if physical < d else x[physical-1]
        y.append(predecessor+jj)
    return y, jj


def read(x, signs):
    return sum(F(sign, 2)*x[physical-1] for physical, sign in zip(surv, signs))


x = [F((j % 7)-3, 19) for j in range(r)]
for physical in surv:
    x[physical-1] = F(3, 17)
ox, jj = transport(x)
check("complete rank-two transport preserves norm exactly",
      sum(y*y for y in ox) == sum(y*y for y in x))
check("private renewal term in example is nonzero", jj != 0)
gate = [F(997, 1000)]*r
for physical, sign in zip(surv, chi1):
    gate[physical-1] = gh if sign > 0 else gl
captured = [aa*g*y for g, y in zip(gate, ox)]
common_read = sum(x[physical-1] for physical in surv)/2
check("exact full-renewal one-step capture",
      read(captured, chi1) == (gh-gl)/2 * aa*(common_read+2*jj))

# Arbitrary varying donor/front/bath gates during a common survivor-high tail.
previous = captured
for step in range(12):
    gates = [F(991+(step % 8), 1000)]*r
    gates[0] = F(1, 1000+step)
    for physical in donor:
        gates[physical-1] = F(994+(step % 3), 1000)
    for physical in surv:
        gates[physical-1] = gh
    oo, _ = transport(previous)
    current = [aa*g*z for g, z in zip(gates, oo)]
    check(f"protected row during changing complete tail step {step}",
          read(current, chi1) == aa*gh*read(previous, chi1))
    previous = current
resources()

# Exact Walsh old-character mixing and zero next singleton read.
old = [F(sign, 2) for sign in chi1]
masked = [(gh if bit > 0 else gl)*val for bit, val in zip(chi2, old)]
A, B = (gh+gl)/2, (gh-gl)/2
check("one-step old-character identity",
      all(masked[i] == (A*chi1[i]+B*chi1[i]*chi2[i])/2 for i in range(4)))
check("old character keeps zero total mass", sum(masked) == 0)
check("old character cannot mimic later singleton",
      sum(F(sign, 2)*val for sign, val in zip(chi2, masked)) == 0)

for stages in (2, 10, 200, 1000):
    # Gate contrast .005/R with high gate ideal limit 1.
    Aweak = 1-F(25, 10000*stages)
    check(f"weak multirow mask survival R={stages}",
          Aweak**(stages-1) >= 1-F(25, 10000))

# Arithmetic envelopes at onset. Written monotonicity proves larger widths.
with localcontext() as ctx:
    ctx.prec = 70
    n = Decimal(10)**3000
    L = n.ln()
    root4 = Decimal(10)**750
    check("onset geometry", Decimal(401)*(Decimal('1e-40')+Decimal('5e8')/root4+4/n)<1)
    check("onset front relative error", Decimal('4e20')/root4<Decimal('1e-100'))
    check("constant-width capture renewal loss", Decimal(13)*Decimal('1e-20')<Decimal('1e-12'))
    check("onset loglog M above sqrt(n)", Decimal('1e-40')*n/L.ln()>n.sqrt())
    check("onset code has K>=1e10", Decimal('1e-20')*n.sqrt()/2>Decimal('1e10'))
    check("trace-tail exponential bound", (Decimal(995)/1000).ln()*1000<-5)

resources()
result = {"checks": records, "passed": len(records),
          "scope": "Tiny exact algebra and onset arithmetic; no actual RNN or full-sphere sampling",
          "resources": {"arithmetic_threads": 1, "worker_processes": 0,
                        "observed_peak_process_threads": peak_threads,
                        "peak_working_set_bytes": peak_ram,
                        "cpu_seconds": time.process_time()-start_cpu,
                        "wall_seconds": time.perf_counter()-start_wall,
                        "gpu_cuda_usage": 0,
                        "guards": "<=8 process threads; <100MiB; <30s"}}
Path(__file__).with_name("checks_result.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"passed": result["passed"], "resources": result["resources"]}, indent=2))
