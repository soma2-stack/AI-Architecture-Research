"""Separate high-precision list-arithmetic path for the cheaper preparation.

This supports the written identities; it is not an interval certificate or
a width-400 robust-dimension claim. Original checks/log remain unchanged.
"""
import os
for _name in ("OMP_NUM_THREADS", "OMP_THREAD_LIMIT", "MKL_NUM_THREADS",
              "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS", "TBB_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_name] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["NVIDIA_VISIBLE_DEVICES"] = "void"
os.environ["OMP_DYNAMIC"] = "FALSE"
os.environ["MKL_DYNAMIC"] = "FALSE"

import hashlib
import json
import pathlib
import time
import mpmath as mp
import psutil

HERE = pathlib.Path(__file__).resolve().parent
PROC = psutil.Process()
CPU_START = sum(PROC.cpu_times()[:2])
WALL_START = time.perf_counter()
PEAK_THREADS = 0
PEAK_RSS = 0
CHECKS = []


def guard():
    global PEAK_THREADS, PEAK_RSS
    PEAK_THREADS = max(PEAK_THREADS, PROC.num_threads())
    PEAK_RSS = max(PEAK_RSS, PROC.memory_info().rss)
    if PEAK_THREADS > 8 or PEAK_RSS > 256*1024**2 or PROC.children(recursive=True):
        raise RuntimeError("Resource limit exceeded; stop without retry")


def require(name, condition, **values):
    guard()
    CHECKS.append(dict(name=name, passed=bool(condition), values=values))
    if not condition:
        raise AssertionError(name)


def run(bits):
    with mp.workprec(bits):
        n,m,tt = 400,2,6
        k,l,d = n//2,n//2,n//4
        span=m+tt+4; aa=2*span; shift=3*span
        a=1-mp.mpf(1)/n; lam=mp.mpf(1)/(100*n); bias=mp.mpf(".05")
        gamma=1/(1-1/mp.sqrt(k))
        w=[-1/mp.sqrt(k) for _ in range(k)]; w[0]+=1
        sigma=mp.findroot(lambda x:x-mp.tanh(lam*x+bias),bias)

        def rotate(v):
            dot=mp.fdot(w,v)
            u=[v[i]-gamma*w[i]*dot for i in range(k)]
            p=[u[d-1]]+u[:d-1]+u[d:]
            dot=mp.fdot(w,p)
            return [p[i]-gamma*w[i]*dot for i in range(k)]

        zs=list(range(aa+2,aa+m+tt+1))
        frames=[]
        for z in zs:
            col=[mp.mpf(0)]*k
            col[z]=1/mp.sqrt(2); col[z+shift]=-1/mp.sqrt(2)
            frames.append(col)
        histories=[]
        for y in (mp.mpf("-.7"),mp.mpf(".7")):
            v=[mp.tanh(bias)]*k
            beta0=mp.sqrt(mp.mpf(".75")/n)
            driven=list(range(aa+1,aa+m+1))+list(range(aa+shift+1,aa+shift+m+1))+list(range(d,d+2*m))
            for i in range(1,m+1):
                v[aa+i]=v[aa+shift+i]=beta0
                v[d+i-1]=v[d+m+i-1]=-beta0
            energy=mp.fsum((mp.atanh(v[i])-bias)**2 for i in driven)+l*(lam*sigma)**2
            maximum_input=max(abs(mp.atanh(v[i])-bias) for i in driven)
            cols=[[mp.mpf(0)]*k for _ in zs]
            gates=[[] for _ in range(m)]
            for t in range(1,tt+1):
                ov=rotate(v)
                new=[mp.tanh(a*z+bias) for z in ov]
                driven=[]
                for i in range(1,m+1):
                    c=y*mp.mpf(".3")*mp.cos(2*mp.pi*(tt-t)/tt)*mp.cos(i)
                    beta=mp.sqrt((mp.mpf(".75")-c)/n)
                    for pos in (aa+i+t,aa+shift+i+t):
                        new[pos]=beta; driven.append(pos)
                    for pos in (d+i-1,d+m+i-1):
                        new[pos]=-beta; driven.append(pos)
                    gates[i-1].append(1-beta**2)
                xx=[mp.atanh(new[i])-a*ov[i]-bias for i in driven]
                energy+=mp.fdot(xx,xx); maximum_input=max(maximum_input,max(map(abs,xx)))
                nextcols=[]
                for col,p in zip(cols,frames):
                    transport=rotate(col)
                    nextcols.append([(1-new[i]**2)*(a*transport[i]+p[i]) for i in range(k)])
                cols=nextcols; v=new; guard()
            kk=[[mp.mpf(0)]*len(zs) for _ in range(m)]
            error=mp.mpf(0)
            for i in range(1,m+1):
                for j in range(1,tt+1):
                    zz=aa+i+j; q=zs.index(zz)
                    kk[i-1][q]=a**(tt-j)*mp.fprod(gates[i-1][j-1:])
                for q in range(len(zs)):
                    output=(cols[q][aa+i+tt]-cols[q][aa+shift+i+tt])/mp.sqrt(2)
                    error=max(error,abs(output-kk[i-1][q]))
            ov=rotate(v)
            endpoint=[mp.tanh(a*z+bias) for z in ov]
            public_bulk=endpoint[aa-1]
            driven=[]
            for i in range(1,m+1):
                for pos in (aa+i+tt+1,aa+shift+i+tt+1,d+i-1,d+m+i-1):
                    endpoint[pos]=public_bulk; driven.append(pos)
            xx=[mp.atanh(endpoint[i])-a*ov[i]-bias for i in driven]
            energy+=mp.fdot(xx,xx); maximum_input=max(maximum_input,max(map(abs,xx)))
            resetcols=[]
            for col,p in zip(cols,frames):
                transport=rotate(col)
                resetcols.append([(1-endpoint[i]**2)*(a*transport[i]+p[i]) for i in range(k)])
            require(f"cheap_prep_kernel_{bits}_{y}",error<mp.mpf("1e-60"),
                    kernel_error=mp.nstr(error,15), energy_squared=mp.nstr(energy,50),
                    maximum_input=mp.nstr(maximum_input,35))
            require(f"cheap_prep_energy_{bits}_{y}",maximum_input<mp.mpf(".5")
                    and energy<m*(tt+2)+1)
            histories.append((endpoint,resetcols,kk,energy))
        left,right=histories
        endpoint_error=max(abs(x-z) for x,z in zip(left[0],right[0]))
        require(f"common_endpoint_{bits}",endpoint_error<mp.mpf("1e-60"),
                endpoint_error=mp.nstr(endpoint_error,15))
        ghi=1/mp.cosh(mp.mpf(".25"))**2; glo=1/mp.cosh(mp.mpf(".75"))**2
        mid=(ghi+glo)/2; sg=(ghi-glo)/2
        future=[mid]*k; xi=[mp.mpf(1),mp.mpf(-1)]
        for i in range(1,m+1):
            future[aa+i+tt+2]=mid+sg*xi[i-1]
            future[aa+shift+i+tt+2]=mid-sg*xi[i-1]
        gr=1-left[0][aa+1+tt+1]**2
        coefficient=sigma*a*a*gr*sg*mp.sqrt(2*mp.mpf(l)/n)/n
        query_error=mp.mpf(0)
        for q in range(len(zs)):
            diff=[x-z for x,z in zip(left[1][q],right[1][q])]
            observed=sigma*mp.sqrt(l)*a/(n*mp.sqrt(n))*mp.fdot(rotate(diff),future)
            predicted=coefficient*mp.fsum((left[2][i][q]-right[2][i][q])*xi[i] for i in range(m))
            query_error=max(query_error,abs(observed-predicted))
        require(f"legal_query_identity_{bits}",query_error<mp.mpf("1e-60"),
                maximum_error=mp.nstr(query_error,15),coefficient=mp.nstr(coefficient,50))
        return [mp.nstr(left[3],60),mp.nstr(right[3],60),mp.nstr(coefficient,60)]


status="PASS"
try:
    results=[run(bits) for bits in (240,320)]
    with mp.workprec(220):
        agreement=max(abs(mp.mpf(x)-mp.mpf(z)) for x,z in zip(*results))
        require("separate_path_precision_agreement",agreement<mp.mpf("1e-55"),
                difference=mp.nstr(agreement,20),values=results)
except Exception as exc:
    status="FAIL"
    CHECKS.append(dict(name="first_failure",passed=False,values=dict(error=repr(exc))))
guard()
report=dict(outcome=status,checks=CHECKS,precisions_bits=[240,320],
            CPU_seconds=sum(PROC.cpu_times()[:2])-CPU_START,
            wall_seconds=time.perf_counter()-WALL_START,
            peak_process_threads=PEAK_THREADS,peak_rss_bytes=PEAK_RSS,
            process_peak_working_set_bytes=PROC.memory_info().peak_wset,
            gpu_used=False,worker_processes=0,
            script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            status="HIGH-PRECISION NUMERICAL IDENTITIES, NOT RIGOROUS NUMERICAL CERTIFICATES")
target=HERE/"checks_autonomous_preparation_result.json"
if target.exists():
    raise RuntimeError("Do not overwrite earlier output")
target.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps({key:report[key] for key in ("outcome","CPU_seconds","wall_seconds","peak_process_threads","peak_rss_bytes")}))
raise SystemExit(0 if status=="PASS" else 1)
