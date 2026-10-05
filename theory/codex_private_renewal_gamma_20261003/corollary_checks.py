"""Stable scalar checks for the same-construction logarithmic corollary."""
import os
POOLS=('OMP_NUM_THREADS','OMP_THREAD_LIMIT','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS',
       'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','TBB_NUM_THREADS')
for k in POOLS: os.environ[k]='1'
os.environ['CUDA_VISIBLE_DEVICES']=''; os.environ['NVIDIA_VISIBLE_DEVICES']='void'
os.environ['OMP_DYNAMIC']='FALSE'; os.environ['MKL_DYNAMIC']='FALSE'
import hashlib, json, time
from pathlib import Path
import mpmath as mp
import psutil
HERE=Path(__file__).resolve().parent; P=psutil.Process()
START=time.perf_counter(); CPU=sum(P.cpu_times()[:2]); CHECKS=[]; PT=0; RAM=0
def ck(name,ok,**values):
    global PT,RAM
    PT=max(PT,P.num_threads()); RAM=max(RAM,P.memory_info().rss)
    if PT>12 or RAM>160*1024**2 or P.children(): raise RuntimeError('Resource stop')
    CHECKS.append(dict(name=name,passed=bool(ok),values=values))
    if not ok: raise AssertionError(name)
answers=[]
for bits in (192,256):
    with mp.workprec(bits):
        n=mp.mpf(10)**1000; logn=mp.log(n)
        m=2*mp.floor(logn**4/2); T=mp.ceil(10*n/logn**2); L=mp.ceil(1000*logn)
        decay=1/n+1/n**2-1/n**3
        kappa=(1-1/n**2)*(-mp.expm1((T-L)*mp.log1p(-decay)))/decay
        lower=mp.mpf('.0499')*mp.mpf('.99')*mp.mpf('.17')*mp.mpf('.48')*kappa*mp.sqrt(m)/n
        ck(f'{bits} bit logarithmic complement error',16000*n/(m*kappa)<mp.mpf('.001'),relative=mp.nstr(16000*n/(m*kappa),45))
        ck(f'{bits} bit kappa lower',kappa>=mp.mpf('.998')*T,ratio=mp.nstr(kappa/T,45))
        ck(f'{bits} bit tail drift',3*L*mp.sqrt(10*m/n)<mp.mpf('.001'))
        ck(f'{bits} bit p=1',16000*m*mp.sqrt(T)/n<1)
        ck(f'{bits} bit geometry',m+T+4<=n/400)
        ck(f'{bits} bit Gamma lower',lower>mp.mpf('.039'),lower=mp.nstr(lower,45))
        ck(f'{bits} bit coordinate-time cost',m*T<=11*n*logn**2)
        ck(f'{bits} bit full energy cost',2*mp.sqrt(m*(T+2)+1)<8*mp.sqrt(n)*logn)
        ck(f'{bits} bit input-correction legality',12*n**(-4)<mp.mpf('.001'))
        answers.append(mp.nstr(lower,40))
ck('192/256 logarithmic scalar agreement',answers[0]==answers[1],lower40=answers)
result=dict(status='PASS',checks=CHECKS,cpu_seconds=sum(P.cpu_times()[:2])-CPU,
    wall_seconds=time.perf_counter()-START,peak_process_threads=PT,peak_working_set_bytes=RAM,
    workers=0,gpu_cuda_calls=0,pool_limits={k:os.environ[k] for k in POOLS},
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(HERE/'corollary_result.json').write_text(json.dumps(result,indent=2)+'\n')
