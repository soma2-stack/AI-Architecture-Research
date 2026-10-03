"""Independent scalar and tiny transport checks for the new radius proof.

Fixed diagnostic cases, no witness search and no robust small-width claim.
Whole-section/all-width certification is the written analytic proof.
"""
import os
for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[name] = "1"
from pathlib import Path
from fractions import Fraction as Q
import ctypes
import hashlib
import json
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
started_cpu, started_wall = time.process_time(), time.perf_counter()
scalar = []


def exact(name, predicate, detail):
    assert predicate, name
    scalar.append({"name": name, "pass": True, "detail": detail})


eta = Q(1, 10**4)
eps = Q(1, 1000)
ledger = eps/4 + Q(2, 10**9)
radius = 97*eta+48*eta**2
margin = 1000-eta-eta**3-ledger
exact("constant radius", radius < Q(1, 50), str(radius))
exact("strict final margin", margin > 9, str(margin))
exact("Taylor remainder constant", Q(1) < 32**2*Q(1, 10)**3,
      "1/[8(1/10)^(3/2)]<4, checked by squaring positive quantities")
exact("sqrt5 upper", Q(5) < 3**2, "sqrt(5)<3")
exact("phi first derivative upper", Q(1) < 16*Q(1, 10), "1/[2sqrt(1/10)]<2")
exact("Householder first coefficient", Q(10, 9)*Q(3, 2) < 2, "gamma*||w||<2")
exact("Householder cubic coefficient", Q(10, 9)**2*Q(3, 2)*2 < 4,
      "gamma^2*||w||*|w^T P w|<4")
exact("small n term absorbed", Q(32)**2 < 3**2*200, "32/sqrt(n)<3 for n>=200")
exact("co-moving cosine constant", (Q(22, 7)*Q(5, 2)) < 8,
      "pi*sqrt(5)<8, using pi<22/7 and sqrt5<5/2")
exact("radius power", Q(1, 18)-Q(1, 4)+Q(1, 8) == Q(-5, 72),
      "node term after log n<=sqrt n")
exact("signal power", Q(1, 4)-4*Q(1, 18) == Q(1, 36), "degree-one power")
exact("tail power", 3*Q(1, 18)-Q(1, 4) == Q(-1, 12), "odd tail decays")
exact("signal monotonicity", Q(1, 36)-Q(1, 4*10) > 0,
      "positive when log n>9; n0 is much larger")
exact("n0 logarithm", 900*3 < 10**4,
      "log(10)<3 gives log(10^900)<2700<10000")
exact("n0 leading signal", Q(10**25, 10**21*10) == 1000,
      "n0^(1/36)=10^25, (log n0)^(1/4)<10; actual leading term strictly >1000")
exact("spreading threshold", 10**850 > 61440, "n0^(17/18)=10^850")
exact("dimension floor denominator", 5*2_000_000*2 == 20_000_000,
      "d>=n/5, q>=d/(2e6), F>=n^(1/18)/2")


def diagnostic(n, F, seed):
    rng = np.random.default_rng(seed)
    k, d, ell = n//2, n//4, n-n//2
    N = int(np.ceil(4*n*np.log(n)))+1
    a, delta, z0 = 1-1/n, .03, .15
    ids = np.arange(d)
    modes = [np.ones(d)/np.sqrt(d)]
    for f in range(1, F+1):
        modes.extend([np.sqrt(2/d)*np.cos(2*np.pi*f*ids/d),
                      np.sqrt(2/d)*np.sin(2*np.pi*f*ids/d)])
    A = np.column_stack(modes)
    perp = np.eye(d)-A@A.T
    B = perp@rng.normal(size=(d, 3))/np.sqrt(d)
    y = rng.normal(size=(F, 3))
    y /= np.linalg.norm(y)
    profiles = (perp@np.tanh(16*np.sqrt(d*F)*(B@y.T))).T/(4*F)
    assert np.max(np.abs(profiles)) <= 1+1e-14
    assert np.max(np.linalg.norm(profiles, axis=1)) <= np.sqrt(d)/(4*F)+1e-14
    w = -np.ones(k)/np.sqrt(k)
    w[0] += 1
    gamma = 1/(1-1/np.sqrt(k))
    U = np.eye(k)-gamma*np.outer(w,w)
    P = np.eye(k)
    P[:d,:d] = np.roll(np.eye(d), 1, axis=0)
    O = U@P@U
    R0 = np.zeros((n,n))
    R0[:k,:k] = a*O
    R0[k:,k:] = np.eye(ell)/(100*n)
    raw = R0+np.ones((n,n))/(10**8*n**3)
    R = raw*(a/np.linalg.norm(raw, 2))
    eR = np.linalg.norm(R-R0, 2)
    assert eR <= 4/(10**8*n**2)+1e-14
    base = np.r_[np.full(k,np.sqrt(z0/n)), np.full(ell,.4)]
    base[0] = 0
    virtual, states = [], []
    for tau in range(d):
        c = delta/F*np.sum(profiles[:,(ids+tau)%d]*
            np.cos(2*np.pi*np.arange(1,F+1)*tau/d)[:,None],axis=0)
        c = np.r_[c,np.zeros(k-d)]
        v = (np.sqrt(z0-c)-np.sqrt(z0))/np.sqrt(n)
        v[d:] = 0
        p = v.copy()
        p[0] = 0
        virtual.append((c,v))
        states.append(np.r_[p,np.zeros(ell)])
    interior_sq = []
    max_ratio = 0.
    mean_ratio = 0.
    rank_two_error = 0.
    cosine_error = 0.
    majorant = 16*(delta/np.sqrt(n)+delta**2/F**2+delta/n)
    for tau in range(d):
        c,v = virtual[tau]
        cold,_ = virtual[(tau+1)%d]
        now,prev = states[tau],states[(tau+1)%d]
        cpred = delta/F*np.sum(profiles[:,(ids+tau)%d]*(
            np.cos(2*np.pi*np.arange(1,F+1)*tau/d)-
            np.cos(2*np.pi*np.arange(1,F+1)*(tau+1)/d))[:,None],axis=0)
        cosine_error = max(cosine_error,float(np.max(np.abs(c-P@cold-np.r_[cpred,np.zeros(k-d)]))))
        pp = prev[:k]
        formula = (-gamma*w*(w@(P@pp))-gamma*(P@w)*(w@pp)
                   +gamma**2*w*(w@(P@w))*(w@pp))
        rank_two_error=max(rank_two_error,float(np.linalg.norm((O-P)@pp-formula)))
        mean_bound = delta**2*d/(4*F**2*np.sqrt(n))
        mean_ratio=max(mean_ratio,float(abs(v.sum())/mean_bound))
        step = np.arctanh(base+now)-np.arctanh(base)-R@prev
        sn = np.linalg.norm(step)
        max_ratio=max(max_ratio,float(sn/majorant))
        interior_sq.append(sn**2)
        assert np.linalg.norm(now) <= delta/(4*F)+1e-14
        assert abs(v.sum()) <= mean_bound+1e-14
        assert sn <= majorant+1e-14
    assert cosine_error < 1e-13
    assert rank_two_error < 1e-13
    count,rem=divmod(N-1,d)
    interior_energy=count*sum(interior_sq)+sum(interior_sq[:rem])
    first=states[(N-1)%d]
    first_norm=np.linalg.norm(np.arctanh(base+first)-np.arctanh(base))
    reset_norm=np.linalg.norm(R@states[0])
    radius_actual=np.sqrt(interior_energy+first_norm**2+reset_norm**2)
    radius_bound=delta/F+np.sqrt(N)*majorant
    assert radius_actual <= radius_bound
    # Check same endpoint independently by inverse-lift reset: h_final=0.
    reset=-R@(base+states[0])-.05*np.ones(n)
    assert np.max(np.abs(np.tanh(R@(base+states[0])+reset+.05)))<1e-14
    return {"n":n,"F":F,"seed":seed,"N":N,"diagnostic_delta":delta,
            "cosine_identity_error":cosine_error,"rank_two_identity_error":rank_two_error,
            "actual_mean_over_bound":mean_ratio,"max_interior_norm_over_bound":max_ratio,
            "exactly_accumulated_numeric_radius":float(radius_actual),
            "new_radius_majorant":float(radius_bound),"old_radius_majorant":float(8*delta*np.sqrt(n*np.log(n))),
            "scope":"float64 algebra check only, not a robust certificate or witness search"}


numerical=[diagnostic(*case) for case in [(200,2,610301),(256,3,610302),(400,4,610303)]]


class Counters(ctypes.Structure):
    _fields_=[("cb",ctypes.c_ulong),("PageFaultCount",ctypes.c_ulong)]+[
        (name,ctypes.c_size_t) for name in ["PeakWorkingSetSize","WorkingSetSize",
        "QuotaPeakPagedPoolUsage","QuotaPagedPoolUsage","QuotaPeakNonPagedPoolUsage",
        "QuotaNonPagedPoolUsage","PagefileUsage","PeakPagefileUsage"]]
counters=Counters()
counters.cb=ctypes.sizeof(counters)
kernel=ctypes.WinDLL("kernel32",use_last_error=True)
kernel.GetCurrentProcess.restype=ctypes.c_void_p
psapi=ctypes.WinDLL("psapi",use_last_error=True)
psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.POINTER(Counters),ctypes.c_ulong]
assert psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),ctypes.byref(counters),counters.cb)
output={"status":"PASS","exact_checks":scalar,"numerical_checks":numerical,
        "cpu_seconds":time.process_time()-started_cpu,"wall_seconds":time.perf_counter()-started_wall,
        "peak_ram_bytes":counters.PeakWorkingSetSize,"gpu_seconds":0,"cuda_used":False,
        "proof_basis":"written analytic whole-section bounds, not numerical checks"}
i=1
while (HERE/f"CHECK_RESULTS_{i}.json").exists():
    i+=1
target=HERE/f"CHECK_RESULTS_{i}.json"
with target.open("x",encoding="utf-8") as handle:
    json.dump(output,handle,indent=2)
print(json.dumps({"status":"PASS","exact_checks":len(scalar),"numerical":numerical,
                  "cpu_seconds":output["cpu_seconds"],"wall_seconds":output["wall_seconds"],
                  "peak_ram_bytes":output["peak_ram_bytes"],"output":str(target)},indent=2))
