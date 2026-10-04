"""Exact rational one-Householder path checks, no numerical libraries."""
import os
for key in ('OMP_NUM_THREADS','OMP_THREAD_LIMIT','MKL_NUM_THREADS',
            'OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key]='1'
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['NVIDIA_VISIBLE_DEVICES']='void'
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import time
import psutil

proc=psutil.Process(); start=time.perf_counter(); cpu_start=sum(proc.cpu_times()[:2])
checks=[]; peak_threads=0; peak_rss=0
n=512; k=256; r=255; d=128; a=Q(511,512); gamma=Q(16,15)
m=2; T=7; S=m+T+4; A=2*S; B=5*S
gates=[[Q(9930+7*((i+2*j)%8),10000) for j in range(T)] for i in range(m)]
G=[]
for t in range(1,T+1):
    diagonal=[Q(997,1000)]*r
    for i in range(m):
        for physical in (A+i+1+t,B+i+1+t,d+4+2*i,d+5+2*i):
            diagonal[physical-1]=gates[i][t-1]
    G.append(diagonal)

def C(x):
    out=x.copy(); out[0]=Q(0); out[1:d-1]=x[:d-2]
    return out

def R2(x):
    total=sum(x,Q(0))
    j=gamma/Q(16)*x[d-2]-gamma**2/Q(k)*total
    out=[j]*r; out[0]+=gamma/Q(16)*total
    return out

def product(values):
    result=Q(1)
    for value in values: result*=value
    return result

def record(name,ok,**data):
    global peak_threads,peak_rss
    peak_threads=max(peak_threads,proc.num_threads()); peak_rss=max(peak_rss,proc.memory_info().rss)
    checks.append(dict(name=name,passed=bool(ok),data=data))
    if not ok or peak_threads>8 or peak_rss>160*1024**2 or proc.children():
        raise AssertionError('Exact check or resource failure: stop')

status='PASS'
try:
    for source_row in range(m):
        for s in (1,3,7):
            local=[Q(0)]*r; local[A+source_row+s]=gates[source_row][s-1]
            first=[Q(0)]*r
            for t in range(s+1,T+1):
                old_first=C(first); insertion=R2(local)
                first=[a*G[t-1][z]*(old_first[z]+insertion[z]) for z in range(r)]
                shifted=C(local)
                local=[a*G[t-1][z]*shifted[z] for z in range(r)]
            for target_row in range(m):
                formula=-gamma**2/Q(k)*a**(T-s)*sum(
                    (product(gates[target_row][j-1:T])*product(gates[source_row][s-1:j-1])
                     for j in range(s+1,T+1)),Q(0))
                observed=first[A+target_row+T]
                record(f'prefix_suffix_i{target_row}_h{source_row}_s{s}',observed==formula,
                       exact_coefficient=str(formula),scope='n=512 rational algebra, not a model certificate')
                if target_row==source_row:
                    collapsed=-gamma**2/Q(k)*(T-s)*a**(T-s)*product(gates[source_row][s-1:T])
                    record(f'same_row_age_times_product_h{source_row}_s{s}',formula==collapsed)
    margin=2*Q(51,1000)*Q(941,1000)*Q(1,50)
    record('complete_actual_short_packet_threshold',margin<Q(2,1000),
           pair_upper=str(margin),decimal=float(margin),constant_N_over_sqrt_n='1/50')
except Exception as exc:
    status='FAIL'; checks.append(dict(name='first_failure',passed=False,data=dict(error=repr(exc))))
report=dict(outcome=status,checks=checks,gpu_used=False,workers=0,arithmetic='exact Python Fraction',
            peak_process_threads=peak_threads,peak_rss_bytes=peak_rss,
            peak_working_set_bytes=getattr(proc.memory_info(),'peak_wset',peak_rss),
            cpu_seconds=sum(proc.cpu_times()[:2])-cpu_start,wall_seconds=time.perf_counter()-start,
            script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
target=Path(__file__).with_name('exact_path_result.json')
if target.exists(): raise RuntimeError('Preserve previous evidence')
target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:report[key] for key in ('outcome','cpu_seconds','wall_seconds','peak_process_threads','peak_working_set_bytes')}))
raise SystemExit(0 if status=='PASS' else 1)
