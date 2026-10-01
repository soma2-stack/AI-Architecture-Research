"""Freeze one numerically selected candidate before any whole-box certification."""
import sys,time,math,subprocess
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import common as c
Q=c.Q; k=c.k
c.verify(); k.a.c.hardware()
assert not (c.ROOT/'candidate.json').exists()
summary=c.json.loads((c.ROOT/'search_summary.json').read_text())
assert all(not row['status'].startswith('worker defect') for row in summary['results'])
choices=[row['best'] for row in summary['results'] if 'a' in row['best']]
for s in (1,2):
    p=c.json.loads((c.OLD/f'stage2_proxy/outputs/independent_n4_confirmation_query_r7_s{s}.json').read_text())
    choices.append(dict(p,id=f'baseline_s{s}',kind='top'))
winner=sorted(choices,key=lambda x:(-x['score'],x['id']))[0]
chart=c.json.loads((c.ROOT/'bases.json').read_text())[winner['kind']]
B=[[Q(v) for v in row] for row in chart['B']]; L=[[Q(v) for v in row] for row in chart['L']]
aa=[Q(math.floor(float(v)*2**20),2**20) for v in winner['a']]
x=Q(float(winner['ah']))*Q(51,50)*2**20
ah=Q(-((-x.numerator)//x.denominator),2**20)
assert all(v>0 for v in aa) and ah>0
case=next(d for d in k.a.INPUT['cases'] if d['name']=='independent_n4_confirmation')
base=k.a.base_for(case,B,192,JI=None); n=4; r=7
J=base['reduced']; H0=[row[:n] for row in J[:n]]; Ht=[row[n:n+r] for row in J[:n]]
Jp=k.matmul([[k.I(v) for v in row] for row in L],[row[:n+r] for row in J[n:]])
cross=k.matmul([row[:n] for row in Jp],k.matmul(k.inverse(H0),Ht))
C0=[[Jp[i][n+j]-cross[i][j] for j in range(r)] for i in range(r)]
Kh=k.a.mpinverse(H0); K=k.a.mpinverse(C0)
candidate={'endpoint':case,'selection':winner,'r':r,'B':chart['B'],'L':chart['L'],
    'a':list(map(str,aa)),'ah':str(ah),'K_hidden':[[str(v) for v in row] for row in Kh],
    'K_selected':[[str(v) for v in row] for row in K],
    'model_parameters':base['model'].serialize(),'selected_sigma':chart['sigma']}
c.write('candidate.json',candidate)
# Four fixed 8D numerical probes, completed before the official 7D result.
ep,B8,L8,s8,full=c.basis(winner['kind'],8)
dy=lambda v:Q(round(float(v)*2**128),2**128)
B8q=[[dy(v) for v in row] for row in B8]; L8q=[[dy(v) for v in row] for row in L8]
B8=c.np.array([[float(v) for v in row] for row in B8q]); L8=c.np.array([[float(v) for v in row] for row in L8q])
a8=c.np.r_[winner['a'],winner['a'][-1]*s8[-2]/s8[-1]]
rows=[]
for scale in (.5,.75,1.,1.25):
    out=c.evaluate3(ep,B8,L8,a8*scale,winner['ah']*scale**2)
    rows.append({'scale':scale,'valid':bool(out['valid']),'reason':out.get('reason'),
        'beta3':out['beta3'].tolist() if out['valid'] else None,
        'minimum_over_epsilon':float(min(out['beta3']))/1e-3 if out['valid'] else None})
c.write('8d_numerical_diagnostic.json',{'label':'NUMERICAL ONLY; no interval certificate',
    'kind':winner['kind'],'sigma':s8.tolist(),'base_a':a8.tolist(),'base_ah':winner['ah'],
    'B':[[str(v) for v in row] for row in B8q],'L':[[str(v) for v in row] for row in L8q],
    'attempts':rows,'selection_feedback_used':False})
c.write('selection_resources.json',{'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
    'peak_working_set_bytes':k.a.c.psutil.Process().memory_info().peak_wset,'gpu_used':False})
c.write('CANDIDATE_FROZEN.json',{'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.REPO,text=True).strip(),
    'method_sha256':c.sha(c.ROOT/'METHOD_FROZEN.json'),
    'sha256':{p:c.sha(c.ROOT/p) for p in ('candidate.json','8d_numerical_diagnostic.json','search_summary.json','selection_resources.json')},
    'winner':winner['id'],'prospective':'No whole-box official result computed; no replacement allowed'})
print('FROZEN',winner['id'],'numerical score',winner['score'],flush=True)
