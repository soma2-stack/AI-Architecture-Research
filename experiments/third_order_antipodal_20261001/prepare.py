"""Deterministically freeze one archived proxy candidate; no score optimization."""
import sys, json, math, time, hashlib
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
START_CPU=time.process_time(); START_WALL=time.perf_counter()
import kernel as k
ROOT=k.ROOT; OLD=k.OLD
sys.path.insert(0,str(OLD))
from screen_proxy import Endpoint
rows=[]
for p in (OLD/'stage2_proxy/outputs').glob('*.json'):
    d=json.loads(p.read_text())
    if d['name']=='independent_n4_confirmation' and d['r']==6: rows.append((d['score'],p.name,d))
score,name,proxy=sorted(rows,key=lambda row:(-row[0],row[1]))[0]
assert name=='independent_n4_confirmation_query_r6_s2.json'
ep=Endpoint(proxy['name']); B,U,s=ep.basis(proxy['basis'],6); L=ep.projection(U)
dy=lambda v: Q(round(float(v)*2**128),2**128)
B=[[dy(x) for x in row] for row in B]; L=[[dy(x) for x in row] for row in L]
aa=[Q(math.floor(float(v)*2**20),2**20) for v in proxy['a']]
x=Q(float(proxy['ah']))*Q(51,50)*2**20
ah=Q(-((-x.numerator)//x.denominator),2**20)
case=next(d for d in k.a.INPUT['cases'] if d['name']==proxy['name'])
base=k.a.base_for(case,B,192,JI=None); n=case['n']; r=6
J=base['reduced']; H0=[row[:n] for row in J[:n]]; Ht=[row[n:n+r] for row in J[:n]]
Jp=k.matmul([[k.I(v) for v in row] for row in L],[row[:n+r] for row in J[n:]])
cross=k.matmul([row[:n] for row in Jp],k.matmul(k.inverse(H0),Ht))
C0=[[Jp[i][n+j]-cross[i][j] for j in range(r)] for i in range(r)]
Kh=k.a.mpinverse(H0); K=k.a.mpinverse(C0)
candidate={'endpoint':case,'source_proxy':name,'source_proxy_score':score,'r':6,
    'B':[[str(v) for v in row] for row in B],'L':[[str(v) for v in row] for row in L],
    'a':[str(v) for v in aa],'ah':str(ah),
    'K_hidden':[[str(v) for v in row] for row in Kh],'K_selected':[[str(v) for v in row] for row in K],
    'model_parameters':base['model'].serialize(),
    'numerical_spectrum_from_setup':s.tolist()}
(ROOT/'candidate.json').write_text(json.dumps(candidate,indent=2))
config={'stage':'third-order antipodal; one 6D candidate','source_archive_commit':'1e1b141',
    'epsilon':'1/1000','n':4,'T':37,'r':6,'P':24,'precision_bits':[192,256],
    'device':'cpu','workers':1,'cpu_budget_seconds':1200,'ram_limit_bytes':2*1024**3,
    'selection':'maximum existing r6 archived proxy score; no replacement on failure',
    'hidden_padding':'51/50, rounded upward2^-20; tangent widths rounded downward2^-20',
    'normalization':'input SD sqrt(3/32), original parameter-group RMS, q=ones/sqrt(n), beta=max(1,||R||F)',
    'query':'permitted future preactivations[1/4,3/4]^n; support-aware7/8 gate',
    'torch_version':k.a.c.torch.__version__,'numpy_version':k.np.__version__,
    'mpmath_version':k.a.mp.__version__,'python_version':sys.version}
(ROOT/'config.json').write_text(json.dumps(config,indent=2))
resources={'cpu_seconds':time.process_time()-START_CPU,'wall_seconds':time.perf_counter()-START_WALL,
           'peak_working_set_bytes':k.a.c.psutil.Process().memory_info().peak_wset,'gpu_used':False,
           'stage':'setup; no whole-box third-order result computed'}
(ROOT/'setup_resources.json').write_text(json.dumps(resources,indent=2))
print(name,aa,ah,resources,flush=True)
