"""Independent exact bookkeeping and downstream inequality checks, read-only."""
import sys, json, math, hashlib, difflib
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'antipodal_robust_dimension_20261001'
checks={}
screens=[json.loads(p.read_text()) for p in (SRC/'screening').glob('*.json')]
candidates=json.loads((SRC/'candidates.json').read_text())
qualify=[x for x in screens if x.get('score',-1)>=1]
expected={f"{x['name']}_{x['basis']}_r{x['r']}_s{x['seed']}":x for x in qualify}
actual={x['id']:x for x in candidates if x['id']!='control_reviewed_4D'}
checks['complete_selection']=len(screens)==288 and set(expected)==set(actual) and len(candidates)==67
checks['amplitudes_rounded_down']=all(
 all(Q(v)==Q(math.floor(float(w)*2**20),2**20) for v,w in zip(c['a'],expected[cid]['a']))
 and Q(c['ah'])==Q(math.floor(float(expected[cid]['ah'])*2**20),2**20)
 for cid,c in actual.items())
crashed=set((SRC/'results_attempt1_crashed/crashed_ids.txt').read_text().split())
results={p.stem:json.loads(p.read_text()) for p in (SRC/'results').glob('*.json')}
checks['repair_only_crashed']=crashed=={cid for cid,x in results.items() if x.get('runner')=='certify_official_repair.py'} and len(crashed)==48
checks['preserved_crashes']=all('too many values to unpack' in json.loads((SRC/f'results_attempt1_crashed/{cid}.json').read_text())['error'] for cid in crashed)
checks['no_certified_repair']=all(results[cid].get('certified_dimension') is None for cid in crashed)
delta=''.join(difflib.unified_diff((SRC/'certify_official.py').read_text().splitlines(True),(SRC/'certify_official_repair.py').read_text().splitlines(True),fromfile='certify_official.py',tofile='certify_official_repair.py'))
(ROOT/'runner_diff.txt').write_text(delta)
def full_rank(matrix):
 a=[list(map(Q,row)) for row in matrix]; n=len(a)
 for j in range(n):
  p=next((p for p in range(j,n) if a[p][j]),None)
  if p is None:return False
  a[j],a[p]=a[p],a[j]; pivot=a[j][j]
  for i in range(j+1,n):
   factor=a[i][j]/pivot
   a[i]=[x-factor*y for x,y in zip(a[i],a[j])]
 return True
for cid,row in results.items():
 if not row.get('certified_dimension'):continue
 for bits in (192,256):
  c=row[f'result_{bits}']; r=row['candidate']['r']
  checks[f'{cid}_{bits}_exact_K_nonsingular']=full_rank(c['K_selected']) and full_rank(c['K_hidden'])
  checks[f'{cid}_{bits}_strict_faces']=all(Q(mu)*(1-Q(float(rs)))==Q(beta)>Q(1,1000) for mu,rs,beta in zip(c['mu_tilde_i'],c['row_sums_upper'],c['beta_i']))
  checks[f'{cid}_{bits}_all_cross_rows']=all(sum((Q(float(v)) for v in e),Q(0))<=Q(float(rs))<1 for e,rs in zip(c['scaled_jacobian_residual_upper'],c['row_sums_upper']))
  checks[f'{cid}_{bits}_hidden_inclusion']=all(Q(float(v))<=(1-Q(c['eta_hidden']))*Q(c['a_hidden']) for v in c['hidden_forcing_upper'])
  if cid.startswith('independent'):
   chart=json.loads((SRC/f"charts/{row['candidate']['chart']}.json").read_text()); n=len(c['K_hidden']); P=n*n+2*n
   support=[(i,p) for p,i in enumerate(range(n))]+[(i,n+i*n+j) for i in range(n) for j in range(n)]+[(i,n+n*n+i) for i in range(n)]
   support=sorted(support)  # accepted model support enumerates state then parameter
   L=[[Q(v) for v in rr] for rr in chart['L'][:r]]
   K=[[Q(v) for v in rr] for rr in c['K_selected']]; a=list(map(Q,c['a_i']))
   diag=[Q(6+3*i,20) for i in range(n)]
   f2=n*max(Q(1),sum(v*v for v in diag))
   ell=[[sum(K[i][j]*L[j][d] for j in range(r))/a[i] for d in range(len(L[0]))] for i in range(r)]
   checks[f'{cid}_{bits}_query_margin_exact_squared']=all(Q(mu)**2*f2*sum(v*v/diag[i]**2 for v,(i,p) in zip(e,support))<=Q(7,8)**2 for e,mu in zip(ell,c['mu_tilde_i']))
assert all(checks.values()),[name for name,ok in checks.items() if not ok]
(ROOT/'checks.json').write_text(json.dumps({'checks':checks,'passed':len(checks)},indent=2))
print(len(checks),'checks passed')
