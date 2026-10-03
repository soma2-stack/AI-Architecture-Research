"""Independent arithmetic/identity checks of the NEW autonomous-energy proof.

No old-proof replay, witness optimization, SVD, training or GPU. Small
reference fixed points are numerical evidence only; all-width certification
is by the explicit analytic proof, not their floating-point minima.
"""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"
from pathlib import Path
from fractions import Fraction as Q
import ctypes
import json
import time
import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
started_cpu, started_wall = time.process_time(), time.perf_counter()
checks, numerical = [], []


def check(name, predicate, detail):
    if not predicate:
        raise ArithmeticError(name)
    checks.append({"name": name, "pass": bool(predicate), "detail": detail})


m0, m = Q(1, 40), Q(1, 50)
kappa = Q(10000, 10001)
qg = Q(9999, 10000)
bm_upper = m0**3/(3*(1-m0*m0))+m0/10**6
check("reference B_m bound", bm_upper < Q(1, 100000), str(bm_upper))
check("reference gamma square", Q(700, 699)**2 < Q(201, 200), "tau<1/700")
phi_upper = Q(1, 100000)-Q(1,20)+Q(201,200)*(m0+Q(1600,500000))
check("Phi(B_m) negative", phi_upper == Q(-21649,1000000), str(phi_upper))
check("source/protected positive", m0+m0**3/(3*(1-m0*m0)) < Q(1,20),
      "atanh(1/40)<1/20")
check("dense fixed-point transfer", m0-Q(4,10**11) > m, "n>=10^6")
check("radial contraction", kappa == 1/(1+m*m/4), str(kappa))
check("public tail time-l2 constant", (m/2)**2/(1-kappa*kappa) < 1,
      str((m/2)**2/(1-kappa*kappa)))
check("radial time-l2 gain", kappa/(1-kappa) == 10000, "exact")
check("radial pointwise gain", kappa*kappa/(1-kappa*kappa) < 71**2, "10000/sqrt(20001)<71")
check("good transport sum", 1/(1-qg) == 10000, "exact")
check("source gain", (1+Q(4,10**8*200))/(1-Q(1,20000)) < 2, "n>=200")
check("local second derivative", Q(16,27) < 1, "(4/(3sqrt(3)))^2<1")
check("coarse C_R coefficients", 2*101**5+40008*72*2*10**12+2*(101+2*10**6) < 10**19,
      "bounds C_R/(1+R)^3, every R>=0")
check("logarithm sufficient onset", 80*3 < 10**4, "log(10^80)<240<10^4")


def high_precision(n, radius, precision):
    with mp.workdps(precision):
        nn, rr = mp.mpf(n), mp.mpf(str(radius))
        L = int(mp.ceil(mp.log(100*mp.sqrt(nn))/mp.log(mp.mpf(10001)/10000)))
        bad = int(mp.ceil(10000*(1+10000*rr)**2))
        H = bad+10000
        chi = mp.mpf(1)/50+71*rr
        C = 2*rr*101**5+40008*chi*H+2*rr*(101+mp.sqrt(H))
        delta = 2*mp.sqrt(n-n//2)/nn*(rr*L**mp.mpf("2.5")+(L+10001)*chi*H)
        delta += 2*rr/nn*(mp.sqrt(L)+mp.sqrt(H))
        return {"n": str(n), "R_abs": str(radius), "L": L, "B_R": bad, "H_R": H,
                "chi_R": mp.nstr(chi,45), "C_R": mp.nstr(C,45),
                "query_error_bound":mp.nstr(delta,45)}


for n, radius in ((10**6, .25), (10**80, 1), (10**900, 1)):
    low, high = high_precision(n, radius, 80), high_precision(n, radius, 120)
    check(f"80/120 decimal agreement n={n}", low == high,
          "saved 45-digit scalar values and ceiling counts agree; numerical cross-check only")
    numerical.append(high)


def rotate(v, n):
    k, d = n//2, n//4
    tau = 1/np.sqrt(k)
    w = -np.full(k,tau)
    w[0] += 1
    gamma = 1/(1-tau)
    u = v-gamma*w*(w@v)
    u = u.copy()
    u[:d] = np.roll(u[:d],1)
    return u-gamma*w*(w@u)


for n in (200, 2000):
    k, d = n//2, n//4
    rng = np.random.default_rng(610310+n)
    v = rng.normal(size=k)
    v[0] = 0
    direct = rotate(v,n)
    tau, gamma = 1/np.sqrt(k), 1/(1-1/np.sqrt(k))
    S = v[1:].sum()
    J = gamma*tau*v[d-1]-gamma*gamma*tau*tau*S
    closed = np.zeros(k)
    closed[1] = J+gamma*tau*S
    closed[2:d] = v[1:d-1]+J
    closed[d:] = v[d:]+J
    err = np.max(np.abs(direct-closed))
    check(f"independent selected-row identity n={n}", err < 1e-12,
          {"max_error":float(err)})

    # Reference-only zero-input iteration, fixed start and no search.
    h = np.zeros(n)
    a = 1-1/n
    steps = 0
    while steps < 100000:
        nxt = np.r_[np.tanh(a*rotate(h[:k],n)+.05),
                    np.tanh(h[k:]/(100*n)+.05)]
        residual = np.linalg.norm(nxt-h)
        h = nxt
        steps += 1
        if residual < 1e-12:
            break
        if time.process_time()-started_cpu > 60:
            raise TimeoutError("Stop tiny diagnostics at 60 CPU seconds")
    check(f"numerical reference fixed point convergence n={n}", residual < 1e-12,
          {"iterations":steps,"residual":float(residual),"min_coordinate":float(h.min()),
           "scope":"below theorem threshold; NOT an outward certificate"})


with mp.workdps(80):
    p = mp.mpf(1)/50
    for ztext in ("-.9", "-.01", "0", ".01", ".02", ".8"):
        z = mp.mpf(ztext)
        if z == p:
            ratio = 1/(1-p*p)
        else:
            ratio = (mp.atanh(z)-mp.atanh(p))/(z-p)
        check(f"global secant numeric example z={ztext}", ratio >= 1+p*p/4,
              mp.nstr(ratio,40))


class Counters(ctypes.Structure):
    _fields_=[("cb",ctypes.c_ulong),("PageFaultCount",ctypes.c_ulong),
              ("PeakWorkingSetSize",ctypes.c_size_t),("WorkingSetSize",ctypes.c_size_t),
              ("QuotaPeakPagedPoolUsage",ctypes.c_size_t),("QuotaPagedPoolUsage",ctypes.c_size_t),
              ("QuotaPeakNonPagedPoolUsage",ctypes.c_size_t),("QuotaNonPagedPoolUsage",ctypes.c_size_t),
              ("PagefileUsage",ctypes.c_size_t),("PeakPagefileUsage",ctypes.c_size_t)]
counters=Counters()
counters.cb=ctypes.sizeof(counters)
ctypes.windll.kernel32.GetCurrentProcess.restype=ctypes.c_void_p
handle=ctypes.windll.kernel32.GetCurrentProcess()
ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_ulong]
ctypes.windll.psapi.GetProcessMemoryInfo(handle,ctypes.byref(counters),counters.cb)
result={"checks":checks,"count":len(checks),"high_precision_values":numerical,
        "CPU_seconds":time.process_time()-started_cpu,"wall_seconds":time.perf_counter()-started_wall,
        "peak_RAM_bytes":counters.PeakWorkingSetSize,"GPU_seconds":0,"CUDA_used":False,
        "scope":"new analytic inequalities and tiny reference consistency checks, no witness search"}
path=HERE/"ARITHMETIC.json"
if path.exists():
    raise FileExistsError("Preserve old output; explicitly choose a new path for any rerun")
path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"checks_passed":len(checks),"CPU_seconds":result["CPU_seconds"],
                  "peak_RAM_bytes":result["peak_RAM_bytes"],
                  "high_precision_values":numerical,
                  "fixed_points":[c for c in checks if "reference fixed point" in c["name"]]},indent=2))
