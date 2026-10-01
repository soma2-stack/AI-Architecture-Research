import sys,time,subprocess
sys.dont_write_bytecode=True
CPU=time.process_time();WALL=time.perf_counter()
import common as c
from geometry import Geometry
k=c.k;Q=c.Q;c.verify();k.a.c.hardware();assert not (c.ROOT/'candidate.json').exists()
s=c.json.loads((c.ROOT/'search_summary.json').read_text());assert all(not x['status'].startswith('worker defect') for x in s['results'])
rows=[x['best'] for x in s['results'] if 'a' in x['best']];assert rows
win=sorted(rows,key=lambda v:(-v['score'],v['id']))[0];chart=c.json.loads((c.ROOT/'bases.json').read_text())[win['kind']]
B=[[Q(v) for v in row] for row in chart['B']];L=[[Q(v) for v in row] for row in chart['L']]
aa=list(map(Q,win['a']));ah=Q(win['ah']);n=4;r=7
old=c.json.loads((c.CONTROL/'candidate.json').read_text());case=old['endpoint']
base=k.a.base_for(case,B,192,JI=None);assert base['model'].serialize()==old['model_parameters']
J=base['reduced'];H0=[row[:n] for row in J[:n]];Ht=[row[n:] for row in J[:n]]
cross=k.matmul([row[:n] for row in J[n:]],k.matmul(k.inverse(H0),Ht))
C0=k.matmul([[k.I(v) for v in row] for row in L],[[J[n+i][n+j]-cross[i][j] for j in range(r)] for i in range(24)])
Kh=k.a.mpinverse(H0);K=k.a.mpinverse(C0)
c.write('candidate.json',{'endpoint':case,'model_parameters':base['model'].serialize(),'r':7,
    'selection':win,'B':chart['B'],'L':chart['L'],'a':win['a'],'ah':win['ah'],
    'K_hidden':[[str(v) for v in row] for row in Kh],'K_selected':[[str(v) for v in row] for row in K]})
g=Geometry(c.np.array([[float(v) for v in row] for row in B]),list(map(float,aa)))
faces=[]
for i in range(7):faces.append(g.face(i));print('Numerical face',i+1,faces[-1]['ratio_to_2epsilon'],flush=True)
c.write('numerical_faces.json',{'faces':faces,'failed_lifts':g.failures,'max_lift_residual':g.max_residual,
    'max_normal_width_used':g.max_normal,'feedback_used_for_selection':False})
assert g.failures==0,'Preserve failure and stop: invalid numerical lift diagnostic'
c.write('selection_resources.json',{'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
    'peak_working_set_bytes':k.a.c.psutil.Process().memory_info().peak_wset})
c.write('CANDIDATE_FROZEN.json',{'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.REPO,text=True).strip(),
    'method_sha256':c.sha(c.ROOT/'METHOD_FROZEN.json'),'sha256':{p:c.sha(c.ROOT/p) for p in ('candidate.json','numerical_faces.json','selection_resources.json','search_summary.json')},
    'prospective':'No official whole-box interval certificate yet; no fallback or retuning'})
print('Frozen winner',win['id'],win['score'],flush=True)
