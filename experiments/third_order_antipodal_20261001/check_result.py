"""Post-result verification only: no candidate changes or new certification."""
import os,sys,time
CPU=time.process_time(); WALL=time.perf_counter()
sys.dont_write_bytecode=True
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,hashlib,subprocess
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import sympy as sp
import psutil
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[1]
data=json.loads((ROOT/'candidate.json').read_text()); result=json.loads((ROOT/'result.json').read_text())
freeze=json.loads((ROOT/'FROZEN.json').read_text()); checks={}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks['setup_frozen']=all(sha(ROOT/p)==h for p,h in freeze['local_sha256'].items())
checks['sources_frozen']=all(sha(REPO/p)==h for p,h in freeze['source_sha256'].items())
checks['two_precision_pass']=len(result['attempts'])==2 and all(x['certificate']['certified_dimension']==6 for x in result['attempts'])
a=list(map(Q,data['a'])); K=[[Q(v) for v in row] for row in data['K_selected']]
L=[[Q(v) for v in row] for row in data['L']]; ah=Q(data['ah']); n=4;r=6
ell=[[sum(K[i][j]*L[j][d] for j in range(r))/a[i] for d in range(24)] for i in range(r)]
diag=[Q(6+3*i,20) for i in range(n)]; factor2=n*max(Q(1),sum(v*v for v in diag))
support=sorted([(i,i) for i in range(n)]+[(i,n+i*n+j) for i in range(n) for j in range(n)]+[(i,n+n*n+i) for i in range(n)])
for row in result['attempts']:
    bits=row['precision']; c=row['certificate']; cap=np.load(ROOT/f'bounds_{bits}.npz')
    checks[f'{bits}_finite_all_tensors']=all(np.isfinite(cap[key]).all() and (cap[key]>=0).all() for key in cap.files)
    checks[f'{bits}_full_mixed_shapes']=cap['HH3'].shape==(4,10,10,10) and cap['HS3'].shape==(24,10,10,10)
    checks[f'{bits}_hidden_section']=c['eta_hidden']<.75 and all(Q(float(v))<=(1-Q(c['eta_hidden']))*ah for v in c['hidden_forcing_upper'])
    checks[f'{bits}_face_arithmetic']=all(Q(mu)*(1-Q(float(e))-Q(float(m))/6)==Q(beta)>Q(1,1000) for mu,e,m,beta in zip(c['mu_tilde'],c['center_rows_upper'],c['M3_upper'],c['beta3']))
    checks[f'{bits}_residual_safe_queries']=all(Q(mu)**2*factor2*sum(v*v/diag[i]**2 for v,(i,p) in zip(e,support))<=Q(7,8)**2 for e,mu in zip(ell,c['mu_tilde']))
    T3=cap['selected3']
    exact=[sum((abs(K[i][j])*Q(float(T3[j,k,l,m]))*a[k]*a[l]*a[m]/a[i]
                for j in range(r) for k in range(r) for l in range(r) for m in range(r)),Q(0)) for i in range(r)]
    checks[f'{bits}_outward_cubic_contraction']=all(v<=Q(float(bound)) for v,bound in zip(exact,c['M3_upper']))
# Independent symbolic derivations, not another empirical model run.
t=sp.symbols('t'); x=sp.symbols('x'); aa=sp.Function('a')(t); p=sp.Function('p')(t); f=sp.Function('f')
fj=[None]+[sp.diff(f(x),x,j).subs(x,aa) for j in range(1,5)]
ap=sp.diff(aa,t); a2=sp.diff(aa,t,2); a3=sp.diff(aa,t,3)
pp=sp.diff(p,t); p2=sp.diff(p,t,2); p3=sp.diff(p,t,3)
expected=fj[1]*p3+fj[2]*(p*a3+3*pp*a2+3*p2*ap)+fj[3]*(3*p*a2*ap+3*pp*ap**2)+fj[4]*p*ap**3
checks['symbolic_S_third_product_chain']=sp.simplify(sp.diff(fj[1]*p,t,3)-expected)==0
h=sp.tanh(x)
checks['symbolic_tanh_fourth']=sp.simplify(sp.diff(h,x,4)-8*h*(1-h*h)*(2-3*h*h))==0
checks['symbolic_constant_linear_control']=sp.diff(3*(2*t+1),t,3)==0
checks['symbolic_implicit_third']=sp.diff((t*t+t**3)*(1+t),t,3).subs(t,0)==12
# Verify archive bytes in Git, not just the working tree; newline preservation.
old=ROOT.parent/'antipodal_robust_dimension_20261001'
archive=json.loads((old/'BYTE_EXACT_ARCHIVE.json').read_text())
paths=list(archive['sha256']); prefix='experiments/antipodal_robust_dimension_20261001/'
archive_commit='c482a73'
requests=''.join(archive_commit+':'+prefix+p.replace('\\','/')+'\n' for p in paths).encode()
blob=subprocess.run(['git','cat-file','--batch'],input=requests,stdout=subprocess.PIPE,check=True,cwd=REPO).stdout
pos=0; good=True
for name in paths:
    end=blob.index(b'\n',pos); header=blob[pos:end].split()
    assert len(header)==3,('Git archive lookup failed',name,header)
    size=int(header[2]); pos=end+1
    content=blob[pos:pos+size]; pos+=size+1
    good=good and hashlib.sha256(content).hexdigest()==archive['sha256'][name]
checks['archive_git_blobs_match_raw_hashes']=good
checks['archive_working_files_unchanged']=all(sha(old/p)==h for p,h in archive['sha256'].items())
assert all(checks.values()),[name for name,v in checks.items() if not v]
delta=max(abs(Q(x)-Q(y)) for x,y in zip(result['attempts'][0]['certificate']['beta3'],result['attempts'][1]['certificate']['beta3']))
out={'checks':checks,'passed':len(checks),'archive_verified_commit':archive_commit,'maximum_exact_beta_precision_difference':str(delta),
     'maximum_beta_precision_difference_float':float(delta),
     'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
     'peak_working_set_bytes':psutil.Process().memory_info().peak_wset,
     'gpu_used':False,'timing_note':'Additional to immutable result.json; includes imports and symbolic checks'}
(ROOT/'final_checks.json').write_text(json.dumps(out,indent=2))
print(len(checks),'checks pass',out['cpu_seconds'],'CPU seconds; beta precision difference',float(delta))
