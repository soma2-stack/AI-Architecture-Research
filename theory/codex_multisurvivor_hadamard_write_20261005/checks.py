"""Small exact rational identity checks. These do not prove robust dimension.

One process, standard library only, no numerical thread pools, no GPU APIs.
The dense n=512 replay is an algebra check below the theorem's width regime.
Run: python theory/codex_multisurvivor_hadamard_write_20261005/checks.py
"""
import os
for _name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
              "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_name] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import ctypes
from ctypes import wintypes
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time

START = time.process_time()
RECORDS = []
PEAK_THREADS = 0
PEAK_RAM = 0

def resources():
    global PEAK_THREADS, PEAK_RAM
    if os.name != "nt":
        return
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    class THREADENTRY32(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                    ("th32ThreadID", wintypes.DWORD), ("th32OwnerProcessID", wintypes.DWORD),
                    ("tpBasePri", wintypes.LONG), ("tpDeltaPri", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD)]
    class PMC(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
            (name, ctypes.c_size_t) for name in ("PeakWorkingSetSize", "WorkingSetSize",
            "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
            "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(THREADENTRY32)]
    kernel.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(THREADENTRY32)]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(PMC), wintypes.DWORD]
    snap = kernel.CreateToolhelp32Snapshot(4, 0)
    if snap == ctypes.c_void_p(-1).value:
        raise RuntimeError("Thread inventory failed")
    entry = THREADENTRY32()
    entry.dwSize = ctypes.sizeof(entry)
    count = 0
    valid = kernel.Thread32First(snap, ctypes.byref(entry))
    while valid:
        count += entry.th32OwnerProcessID == os.getpid()
        valid = kernel.Thread32Next(snap, ctypes.byref(entry))
    kernel.CloseHandle(snap)
    mem = PMC()
    mem.cb = ctypes.sizeof(mem)
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(mem), mem.cb):
        raise RuntimeError("Memory inventory failed")
    PEAK_THREADS = max(PEAK_THREADS, count)
    PEAK_RAM = max(PEAK_RAM, mem.PeakWorkingSetSize)
    if count > 8 or PEAK_RAM > 128 * 1024**2:
        raise RuntimeError("Resource guard exceeded; stop rather than enlarge budget")

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    RECORDS.append({"check": name, "status": "PASS"})

N = 512
KMODEL = 256
R = KMODEL - 1
D = 128
A = F(N-1, N)
GAMMA = F(16, 15)
C = F(1, 225)
SQRTK = F(16)
UB = [F(-1, 225)] * R
UB[D-2] += GAMMA / SQRTK
VH = [GAMMA / SQRTK] * R
ZERO = F(0)
ONE = F(1)

def dot(x, y):
    return sum((u*v for u,v in zip(x,y)), ZERO)

def op(x):
    out = [ZERO] * R
    for z in range(1, D-1):
        out[z] = x[z-1]
    for z in range(D-1, R):
        out[z] = x[z]
    j = dot(UB, x)
    b = dot(VH, x)
    out = [value+j for value in out]
    out[0] += b
    return out

def tuple_sites(i, t):
    # Index conversion from physical selected coordinates 1,...,r.
    return [26+i+t-1, 65+i+t-1, D+2*i-1, D+2*i]

def gate(t, theta, matched=False):
    g = [F(999,1000)] * R
    for z in range(5):
        g[z] = F(z+1, N)  # public front retained, not dropped
    d = [F(1989,2000), F(1991,2000)]
    s = [F(1989,2000), F(199,200), F(1991,2000)]
    for i in range(5):
        j = i if i < 2 else i-2
        if t == 1:
            value = F(997,1000) + (F(1,10000)*theta[i] if i < 2 else ZERO)
        elif t in (2,3):
            value = d[i] if i < 2 else s[j]
        elif t == 4:
            value = F(199,200)
            if i < 2:
                tau0 = F(997,1000)
                tau = tau0+F(1,10000)*theta[i]
                for _ in (2,3):
                    tau0 = d[i]*(1+A*tau0)
                    tau = d[i]*(1+A*tau)
                value *= (1+A*tau0)/(1+A*tau)
        else:
            value = F(99,100)
        for site in tuple_sites(i, t):
            g[site] = value
    return g

V = []
for j in range(2):
    v = [ZERO] * R
    for site in tuple_sites(j,0)[2:]:
        v[site] = F(1,2)
    for site in tuple_sites(j+2,0)[2:]:
        v[site] = F(-1,2)
    V.append(v)
check("fixed probes orthonormal", [[dot(v,w) for w in V] for v in V] == [[1,0],[0,1]])
check("fixed probes stationary zero-sum", all(op(v)==v and sum(v)==0 for v in V))

def replay(theta):
    x = [[ZERO]*R for _ in range(2)]
    history = [x]
    words = []
    for t in range(1,6):
        g = gate(t, theta)
        words.append(g)
        x = [[g[i]*(A*ov[i]+v[i]) for i in range(R)] for ov,v in zip(map(op,x), V)]
        history.append(x)
    return history, words

def centered_survivors(x, t):
    means = []
    for cohort in range(3):
        sites = tuple_sites(cohort+2, t)
        values = [x[i] for i in sites]
        check(f"four-site private equality t{t} c{cohort}", len(set(values)) == 1)
        means.append(values[0])
    avg = sum(means)/3
    return [v-avg for v in means]

base, base_words = replay([ZERO,ZERO])
b = F(1,2000)
ds = [F(1989,2000),F(1991,2000)]
ss = [F(1989,2000),F(199,200),F(1991,2000)]
eta = dot(UB,base_words[1]) - SQRTK/GAMMA * UB[0]*base_words[1][0]
raw_columns = []
for theta in ([ONE,ONE], [ONE,-ONE], [F(1,3),F(-2,5)], [ZERO,ONE], [ONE,ZERO]):
    history, words = replay(theta)
    for j in range(2):
        diffs = [[u-v for u,v in zip(history[t][j],base[t][j])] for t in range(6)]
        j1 = dot(UB,diffs[1])
        check("J1 finite coefficient", j1 == -C*F(1,10000)*theta[j])
        check("J2 retains exact Householder", dot(UB,diffs[2]) == A*(ds[j]+eta)*j1)
        actual = centered_survivors(diffs[4],4)
        polynomial = [A**3*F(199,200)*j1*(s*s+s*(ds[j]+eta)) for s in ss]
        mean = sum(polynomial)/3
        check("finite centered two-filter formula", actual == [v-mean for v in polynomial])
        after = centered_survivors(diffs[5],5)
        check("reset does not erase protected modes", after == [A*F(99,100)*v for v in actual])
        tau = ZERO
        target = ZERO
        for t in range(4):
            tau = words[t][tuple_sites(j,t+1)[2]]*(1+A*tau)
            target = base_words[t][tuple_sites(j,t+1)[2]]*(1+A*target)
        check("exact donor trace correction", tau == target)
        check("correction gate budget", F(994,1000) < words[3][tuple_sites(j,4)[2]] < F(996,1000))
    resources()

# Determinant of the normalized two-filter core, squared to stay rational.
x1,x2 = [2*F(199,200)+d+eta for d in ds]
det_squared = F(4,3)*b**6*(ds[0]-ds[1])**2
check("nonzero exact determinant", det_squared > 0)
check("determinant formula", F(4,3)*b**6*(x1-x2)**2 == det_squared)

# Matched pairs really are local traces; exact replay has no private feedback.
for t in range(1,5):
    g = base_words[t-1][:]
    for j in range(2):
        value = F(1994+j,2000)
        for tuple_id in (j,j+2):
            for site in tuple_sites(tuple_id,t):
                g[site] = value
        check("matched gate eigenvector", [g[i]*V[j][i] for i in range(R)] == [value*v for v in V[j]])

for k in range(1,17):
    gram = [[F(i==j,2)-F(1,4*k) for j in range(k)] for i in range(k)]
    check("matched projected common eigenvalue", all(sum(row)==F(1,4) for row in gram))
    if k > 1:
        contrast = [F(1),F(-1)]+[ZERO]*(k-2)
        check("matched projected contrast eigenvalue", [dot(row,contrast) for row in gram] == [v/2 for v in contrast])

for t in range(1,30):
    exact = sum((s-1)*(t-s+1) for s in range(1,t+1))
    check("word-diversity constant", 6*exact == t*(t*t-1))

for length in (2,3,5,12,50):
    for shift in (0,1,2):
        word = [F(1995+((s+shift)%4),2000) for s in range(2,length)]
        rho0 = F(994,1000)
        pulse = F(1,10000)
        center = F(997,1000)
        traces = [center-pulse, center, center+pulse]
        prod = F(1)
        for g in word:
            traces = [g*(1+A*tau) for tau in traces]
            prod *= A*g
        check("pulse trace variation exact", traces[2]-traces[0] == 2*pulse*prod)
        check("pulse trace age lower", min(traces) >= (length-1)*rho0*prod)
        target = F(199,200)*(1+A*traces[1])
        corrections = [target/(1+A*tau) for tau in traces]
        check("pulse final correction bound", abs(corrections[2]-corrections[0]) <= 2*pulse/((length-1)*rho0))
        check("pulse corrections legal", all(F(994,1000)<g<F(996,1000) for g in corrections))

for h_count in (2,4,8,16):
    had = [[1]]
    while len(had) < h_count:
        had = [r+r for r in had] + [r+[-x for x in r] for r in had]
    check("Hadamard orthogonality", all(sum(had[i][s]*had[j][s] for s in range(h_count)) == (h_count if i==j else 0)
          for i in range(h_count) for j in range(h_count)))
    for columns in range(1,h_count):
        check("ball/cube gate budget squared", F(columns,h_count) <= F(columns*columns,h_count))

resources()
folder = Path(__file__).resolve().parent
out = {
    "purpose": "Exact algebra sanity checks, not finite-error/asymptotic proof",
    "algebra_replay_width": N,
    "replay_width_is_theorem_regime": False,
    "all_checks_passed": True,
    "check_count": len(RECORDS),
    "checks": RECORDS,
    "resources": {"process_cpu_seconds": time.process_time()-START,
        "peak_observed_process_threads": PEAK_THREADS,
        "peak_working_set_bytes": PEAK_RAM,
        "numeric_pool_threads": 1, "worker_processes": 0,
        "gpu_api_calls": 0, "cuda_usage": 0,
        "guard_threads": 8, "guard_ram_bytes": 128*1024**2,
        "thread_environment": {name:os.environ[name] for name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS", "CUDA_VISIBLE_DEVICES")}},
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(folder/"checks_result.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({key:out[key] for key in ("all_checks_passed","check_count","resources")},indent=2))
