"""Scalar cross-checks of the stronger final zero-credit bound.

Preserves the earlier ARITHMETIC.json. No reference trajectory is re-run.
Written inequalities, not these numerical scalars, prove the all-width result.
"""
from pathlib import Path
from fractions import Fraction as Q
import ctypes
import json
import time
import mpmath as mp

HERE=Path(__file__).resolve().parent
cpu, wall=time.process_time(),time.perf_counter()
checks=[]


def check(name, ok, detail):
    if not ok:
        raise ArithmeticError(name)
    checks.append({"name":name,"pass":True,"detail":detail})


check("log inverse constant", Q(1,10001)<=Q(1,10000)/(1+Q(1,10000)),
      "log(1+u)>=u/(1+u); L<=10002 log n for n>=10^6")
check("log exponent", Q(1,20)-Q(1,2)==Q(-9,20), "n^(-9/20)")
check("first onset coefficient",4*10002==40008,"allocate epsilon/4 to L term")
check("geometric sum",1+Q(9999,10000)/(1-Q(9999,10000))==10000,
      "B initial unit terms plus geometric tail gives H=B+10000")
check("energy exponent", Q(1,2)*Q(1,2)==Q(1,4), "quadratic bad-step budget versus sqrt(n)")


def values(n, radius, precision):
    with mp.workdps(precision):
        nn=mp.mpf(n); rr=mp.mpf(str(radius)); eps=mp.mpf(1)/1000
        L=int(mp.ceil(mp.log(100*mp.sqrt(nn))/mp.log(mp.mpf(10001)/10000)))
        B=int(mp.ceil(10000*(1+10000*rr)**2)); H=B+10000
        actual=mp.sqrt(n-n//2)/nn*(L+H)
        coarse=(L+H)/mp.sqrt(nn)
        required_energy=mp.mpf(0)
        inner=(eps*mp.sqrt(nn)-10002*mp.log(nn)-10001)/10000
        if inner>1:
            required_energy=(mp.sqrt(inner)-1)/10000
        safe=max(mp.mpf(10)**80,(40008/eps)**(mp.mpf(20)/9),(4*H/eps)**2)
        return {"n":str(n),"R_abs":str(radius),"L":L,"H_R":H,
                "selected_group_query_error_upper":mp.nstr(actual,45),
                "coarse_query_error_upper":mp.nstr(coarse,45),
                "epsilon_half":str(eps/2),
                "necessary_energy_for_robust_margin":mp.nstr(required_energy,45),
                "explicit_sufficient_onset":mp.nstr(safe,45)}


rows=[]
for n,radius in ((10**6,.25),(10**80,1),(10**900,1)):
    lo,hi=values(n,radius,80),values(n,radius,120)
    check(f"80/120 decimal agreement n=10^{len(str(n))-1}",lo==hi,
          "45-digit bounds and integer burn-in/transport counts agree")
    rows.append(hi)
    if n>=10**80:
        with mp.workdps(80):
            check(f"epsilon gate n=10^{len(str(n))-1}",
                  mp.mpf(hi["selected_group_query_error_upper"])<mp.mpf(1)/2000,
                  "scalar corroboration of analytic sufficient-onset bound")

class Counters(ctypes.Structure):
    _fields_=[("cb",ctypes.c_ulong),("PageFaultCount",ctypes.c_ulong),
              ("PeakWorkingSetSize",ctypes.c_size_t),("WorkingSetSize",ctypes.c_size_t),
              ("QuotaPeakPagedPoolUsage",ctypes.c_size_t),("QuotaPagedPoolUsage",ctypes.c_size_t),
              ("QuotaPeakNonPagedPoolUsage",ctypes.c_size_t),("QuotaNonPagedPoolUsage",ctypes.c_size_t),
              ("PagefileUsage",ctypes.c_size_t),("PeakPagefileUsage",ctypes.c_size_t)]
c=Counters();c.cb=ctypes.sizeof(c)
ctypes.windll.kernel32.GetCurrentProcess.restype=ctypes.c_void_p
handle=ctypes.windll.kernel32.GetCurrentProcess()
ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_ulong]
ctypes.windll.psapi.GetProcessMemoryInfo(handle,ctypes.byref(c),c.cb)
result={"count":len(checks),"checks":checks,"values":rows,
        "CPU_seconds":time.process_time()-cpu,"wall_seconds":time.perf_counter()-wall,
        "peak_RAM_bytes":c.PeakWorkingSetSize,"GPU_seconds":0,"CUDA_used":False,
        "scope":"final theorem scalar check, no moderate-width robust claim"}
path=HERE/"ZERO_DECODER_ARITHMETIC.json"
if path.exists():
    raise FileExistsError("Preserve the old output")
path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"checks_passed":len(checks),"CPU_seconds":result["CPU_seconds"],
                  "peak_RAM_bytes":result["peak_RAM_bytes"],
                  "bounds":[{k:r[k] for k in ("R_abs","selected_group_query_error_upper","explicit_sufficient_onset")} for r in rows]},indent=2))
