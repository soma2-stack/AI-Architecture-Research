"""Tiny formula/error checks. CPU only; no dimension claim from samples."""
import os
POOL_KEYS=("OMP_NUM_THREADS","OMP_THREAD_LIMIT","MKL_NUM_THREADS",
           "OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS","BLIS_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS","TBB_NUM_THREADS")
for name in POOL_KEYS:
    os.environ[name]="1"
os.environ["OMP_DYNAMIC"]="FALSE"
os.environ["MKL_DYNAMIC"]="FALSE"
os.environ["OMP_MAX_ACTIVE_LEVELS"]="1"
os.environ["CUDA_VISIBLE_DEVICES"]=""
os.environ["NVIDIA_VISIBLE_DEVICES"]="void"

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
import time
import mpmath as mp
import numpy as np
import psutil

HERE=Path(__file__).resolve().parent
PROC=psutil.Process()
START=time.perf_counter(); CPU_START=sum(PROC.cpu_times()[:2])
PEAK_THREADS=0; PEAK_RSS=0; CHECKS=[]


def guard():
    global PEAK_THREADS,PEAK_RSS
    PEAK_THREADS=max(PEAK_THREADS,PROC.num_threads())
    PEAK_RSS=max(PEAK_RSS,PROC.memory_info().rss)
    if PEAK_THREADS>8 or PEAK_RSS>256*1024**2 or PROC.children(recursive=True):
        raise RuntimeError("Resource limit: stop; do not retry with more resources")


def require(name,condition,**values):
    guard()
    CHECKS.append(dict(name=name,passed=bool(condition),values=values))
    if not condition: raise AssertionError(name)


def rows(g,a):
    m,t=g.shape
    return a**np.arange(t-1,-1,-1)*np.exp(np.cumsum(np.log(g[:,::-1]),axis=1)[:,::-1])


def physical(local):
    m,t=local.shape
    out=np.zeros((m,m+t-1))
    for i in range(m): out[i,i:i+t]=local[i]
    return out


def quantiles(local,p):
    m,t=local.shape
    pos=np.arange(t+2,dtype=float)
    levels=np.arange(p+1,dtype=float)/p
    codes=[]; output=[]
    for row in local:
        tau=np.interp(levels,np.r_[0,row,1],pos)
        codes.append(tau[1:-1])
        output.append(np.interp(np.arange(1,t+1),tau,levels))
    return np.asarray(codes),np.asarray(output)


def exact_sign_norm(e):
    return max(float(np.linalg.norm(e.T@np.asarray(sign)))
               for sign in itertools.product((-1.,1.),repeat=e.shape[0]))


def geometry():
    rng=np.random.default_rng(20261003)
    for t in (1,2,4,16,32):
        c=np.triu(np.ones((t,t)))
        exact=1/(2*np.sin((2*np.arange(1,t+1)-1)*np.pi/(4*t+2)))
        require(f"cumulative_singular_values_T{t}",
                np.max(np.abs(np.linalg.svd(c,compute_uv=False)-exact))<2e-13)
        a=1-1/1_000_000
        g=rng.uniform(.9901,.9999,size=(1,t)); kk=rows(g,a)[0]
        recovered=np.r_[kk[:-1]/(a*kk[1:]),kk[-1]]
        jac=kk[:,None]/g[0][None,:]*c
        determinant=a**(t*(t-1)/2)*np.prod(g[0,1:]**np.arange(1,t))
        require(f"product_inverse_jacobian_T{t}",
                np.max(np.abs(recovered-g[0]))<3e-15
                and abs(np.linalg.det(jac)-determinant)<3e-13,
                determinant=float(determinant))
    for h in (1,2,4,8,16):
        norm_sq=(sum(v*v for v in range(1,h+1))+sum(v*v for v in range(1,h)))/Fraction(2*h)
        require(f"exact_Haar_h{h}",norm_sq==Fraction((2*h)**2+2,12),exact_squared_norm=str(norm_sq))


def finite_boxes():
    rng=np.random.default_rng(20261003)
    a=1-1/1_000_000
    for m,t in ((1,1),(3,5),(5,8),(6,17),(2,31),(6,4)):
        for kind in ("random","constant","pulses"):
            g=rng.uniform(.9901,.9999,size=(m,t))
            if kind=="constant": g[:]=.995
            if kind=="pulses":
                g[:]=.9999; g[:,::3]=.9902
            kk=rows(g,a)
            for p in (1,2,4,9,17):
                code,approx=quantiles(kk,p)
                e=physical(kk-approx)
                hn=exact_sign_norm(e)
                cap=math.sqrt(m*t*min(m,t))/p
                frob=float(np.linalg.norm(e))
                require(f"finite_radius_{m}_{t}_{kind}_p{p}",
                        np.max(np.abs(kk-approx))<=1/p+1e-14
                        and hn<=cap+1e-13
                        and hn>=frob-1e-13
                        and hn<=math.sqrt(min(m,t))*frob+1e-13,
                        code_coordinates=int(code.size),maximum_entry_error=float(np.max(np.abs(kk-approx))),
                        exact_worst_sign_norm=hn,analytic_uniform_cap=cap)
                # Check encoder continuity across a perturbation, including levels near knots.
                gg=np.clip(g+1e-10*np.cos(np.arange(t)),.99001,.99999)
                changed,_=quantiles(rows(gg,a),p)
                require(f"continuity_sample_{m}_{t}_{kind}_p{p}",
                        code.size==0 or np.max(np.abs(code-changed))<1e-5)


def integer_width_counts():
    for n,m,t in ((10**6,100,1000),(10**12,10**8,10**5),
                  (10**24,10**21,10**9),(10**24,10**21,10**12)):
        num=16000**2*m*t*min(m,t)
        floor=math.isqrt(num)//n
        p=max(1,floor if floor*floor*n*n==num else floor+1)
        k=m*(p-1)
        require(f"exact_quantile_count_n{n}_m{m}_T{t}",
                (p*n)**2>=num
                and ((p-1)*n)**2<num
                and Fraction(k,1)<Fraction(16000*m*t,math.isqrt(n)),
                p=p,code_coordinates=k,coordinate_time_budget=m*t)


def precision_checks():
    records=[]
    for bits in (192,256):
        with mp.workprec(bits):
            q=1/mp.cosh(mp.mpf(".25"))**2
            alpha_cap=100*mp.sqrt(2)*mp.mpf(".051")
            require(f"all_future_constant_{bits}",q<mp.mpf(".941") and alpha_cap<8
                    and 1+6/(mp.mpf(".06")*mp.e)<100,
                    q_f=mp.nstr(q,50),coefficient_cap=mp.nstr(alpha_cap,50))
            n=10**6; a=1-mp.mpf(1)/n; base=mp.mpf(".995"); t=8
            # Two DISTINCT admitted rows with EXACTLY the same product. With p=2
            # every .5 crossing occurs on the first interpolation segment and
            # depends only on that shared product. This is a code-collision test,
            # not a proposed lower section or a theorem proved by sampling.
            g1=[base]*t; g2=[base]*t
            g1[0]*=mp.exp(mp.mpf(".0007")); g1[-1]*=mp.exp(mp.mpf("-.0007"))
            g2[0]*=mp.exp(mp.mpf("-.0007")); g2[-1]*=mp.exp(mp.mpf(".0007"))
            kk1=[a**(t-j-1)*mp.fprod(g1[j:]) for j in range(t)]
            kk2=[a**(t-j-1)*mp.fprod(g2[j:]) for j in range(t)]
            tau1=mp.mpf(".5")/kk1[0]; tau2=mp.mpf(".5")/kk2[0]
            tolerance=mp.mpf(2)**(-bits+12)
            require(f"continuous_code_collision_{bits}",
                    abs(tau1-tau2)<tolerance
                    and min(kk1+kk2)>mp.mpf(".5")
                    and max(abs(x-z) for x,z in zip(kk1,kk2))>mp.mpf(".0001"),
                    code_difference=mp.nstr(abs(tau1-tau2),15),
                    maximum_entry_difference=mp.nstr(max(abs(x-z) for x,z in zip(kk1,kk2)),40))
            records.append([mp.nstr(q,50),mp.nstr(alpha_cap,50),mp.nstr(tau1,50)])
    require("192_256_agreement",records[0]==records[1],values=records)


status="PASS"
try:
    guard(); geometry(); finite_boxes(); integer_width_counts(); precision_checks()
except Exception as exc:
    status="FAIL"; CHECKS.append(dict(name="first_failure",passed=False,values=dict(error=repr(exc))))
guard()
report=dict(outcome=status,checks=CHECKS,seed=20261003,resource_settings={x:os.environ[x] for x in POOL_KEYS},
            gpu_used=False,worker_processes=0,peak_process_threads=PEAK_THREADS,peak_rss_bytes=PEAK_RSS,
            process_peak_working_set_bytes=PROC.memory_info().peak_wset,
            cpu_seconds=sum(PROC.cpu_times()[:2])-CPU_START,wall_seconds=time.perf_counter()-START,
            precisions_bits=[192,256],script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            evidence_status="NUMERICAL IDENTITIES/ERROR CHECKS; written proof supplies all-region certificate")
target=HERE/'checks_result.json'
if target.exists(): raise RuntimeError("Do not overwrite prior evidence")
target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:report[key] for key in ('outcome','peak_process_threads','cpu_seconds','wall_seconds','process_peak_working_set_bytes')}))
raise SystemExit(0 if status=='PASS' else 1)
