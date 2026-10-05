"""Large, legal equal-code collisions, not infinitesimal perturbations."""
import os
for key in ('OMP_NUM_THREADS','OMP_THREAD_LIMIT','MKL_NUM_THREADS',
            'OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS',
            'TBB_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['NVIDIA_VISIBLE_DEVICES']='void'
from pathlib import Path
import hashlib
import json
import math
import time
import mpmath as mp
import psutil

process=psutil.Process()
start=time.perf_counter()
cpu_start=sum(process.cpu_times()[:2])
checks=[]
peak_threads=0
peak_rss=0
with mp.workprec(256):
    n=10**6
    a=1-mp.mpf(1)/n
    for m,t in ((1,2400),(2,900),(4,240),(16,15),(40,2),(64,64)):
        radicand=16000**2*m*t*min(m,t)
        root=math.isqrt(radicand)
        p=max(1,(root+(root*root!=radicand)+n-1)//n)
        if p==1:
            x=[a**(t-j-1)*mp.mpf('.9901')**(t-j) for j in range(t)]
            y=[a**(t-j-1)*mp.mpf('.9999')**(t-j) for j in range(t)]
            code_equal=True
        else:
            # Same product, radically different order. All .ell/p levels
            # are crossed before the first row node, determined by that product.
            low=mp.mpf('.9901')
            high=mp.mpf('.9999')
            x=[]
            y=[]
            for j in range(t):
                low_first=max(0,3-j)
                low_last=min(3,t-j)
                x.append(a**(t-j-1)*low**low_first*high**(t-j-low_first))
                y.append(a**(t-j-1)*low**low_last*high**(t-j-low_last))
            code_equal=abs(x[0]-y[0])<mp.mpf('1e-65') and min(x+y)>1-mp.mpf(1)/p
        differences=[v-w for v,w in zip(x,y)]
        same_sign=all(v>=0 for v in differences) or all(v<=0 for v in differences)
        columns=[mp.mpf(0)]*(m+t-1)
        for i in range(m):
            for j in range(t):
                columns[i+j]+=differences[j]
        # Same-sign matrix makes the all-ones row signs an EXACT maximizer.
        H=mp.sqrt(mp.fsum(v*v for v in columns))
        upper=8*H/n+mp.mpf('8e-9')
        passed=code_equal and same_sign and H<=2*mp.sqrt(m*t*min(m,t))/p and upper<mp.mpf('.002')
        peak_threads=max(peak_threads,process.num_threads())
        peak_rss=max(peak_rss,process.memory_info().rss)
        checks.append(dict(m=m,T=t,p=p,passed=bool(passed),
                           maximum_entry_difference=mp.nstr(max(abs(v) for v in differences),40),
                           exact_H=mp.nstr(H,40),controlled_all_future_upper=mp.nstr(upper,40)))
        if not passed or peak_threads>8 or peak_rss>192*1024**2 or process.children():
            raise AssertionError('Extreme collision or resource check failed; stop')
report=dict(outcome='PASS',checks=checks,precision_bits=256,gpu_usage=0,
            peak_threads=peak_threads,peak_rss_bytes=peak_rss,
            peak_working_set_bytes=getattr(process.memory_info(),'peak_wset',peak_rss),
            cpu_seconds=sum(process.cpu_times()[:2])-cpu_start,
            wall_seconds=time.perf_counter()-start,
            script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            status='NUMERICAL ADVERSARIAL EXAMPLES; uniform proof is separate')
target=Path(__file__).with_name('extreme_results.json')
if target.exists():
    raise RuntimeError('Do not overwrite evidence')
target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
