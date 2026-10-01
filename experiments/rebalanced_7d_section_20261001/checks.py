"""Exact post-run arithmetic and precision agreement; no tuning."""
import sys,time
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import common as c
Q=c.Q; c.verify()
data=c.json.loads((c.ROOT/'candidate.json').read_text()); result=c.json.loads((c.ROOT/'result.json').read_text())
checks=[]; faces=[]
def check(name,value):checks.append({'name':name,'passed':bool(value)})
check('exactly two precisions',[v['precision'] for v in result['attempts']]==[192,256])
check('historical evidence unchanged',result['historical_6d_unchanged'] and result['historical_antipodal_unchanged'])
K=[[Q(v) for v in row] for row in data['K_selected']]; L=[[Q(v) for v in row] for row in data['L']]
aa=list(map(Q,data['a'])); eps=Q(1,1000)
m=c.k.a.model(data['endpoint']); n=m.n
diag=[m.params[p] for i,j,p in m.layers[0]['R']]
factor_sq=n*max(Q(1),sum(v*v for v in diag))
ell=[[sum(K[i][j]*L[j][d] for j in range(7))/aa[i] for d in range(24)] for i in range(7)]
for attempt in result['attempts']:
    o=attempt['certificate']; bits=attempt['precision']
    check(f'{bits} complete hidden section',o.get('valid') and o['eta_hidden']<.75)
    check(f'{bits} domain',Q(o['radius'])<=1)
    if not o.get('valid'):continue
    check(f'{bits} hidden self-mapping',all(Q(v)<=(1-Q(o['eta_hidden']))*Q(data['ah']) for v in o['hidden_forcing_upper']))
    beta=list(map(Q,o['beta3'])); mu=list(map(Q,o['mu_tilde']))
    for i in range(7):
        total=sum(v*v/diag[owner]**2 for v,(owner,p) in zip(ell[i],m.support))
        check(f'{bits} exact support-aware query {i+1}',mu[i]>0 and mu[i]**2*factor_sq*total<=Q(7,8)**2)
        linear=mu[i]*(1-Q(o['center_rows_upper'][i])); loss=mu[i]*Q(o['M3_upper'][i])/6
        check(f'{bits} exact face {i+1} arithmetic',beta[i]==linear-loss)
        faces.append({'precision':bits,'face':i+1,'linear_margin':float(linear),
            'third_order_penalty':float(loss),'beta':float(beta[i]),'slack':float(beta[i]-eps),
            'M3':o['M3_upper'][i],'mu':float(mu[i]),'passes':beta[i]>eps})
    check(f'{bits} strict outcome matches faces',o['all_antipodal_faces_pass']==all(v>eps for v in beta))
if all(v['certificate'].get('valid') for v in result['attempts']):
    a,b=[v['certificate'] for v in result['attempts']]
    check('192/256 same face decisions',[Q(v)>eps for v in a['beta3']]==[Q(v)>eps for v in b['beta3']])
    deltas=[abs(float(Q(v)-Q(w))) for v,w in zip(a['beta3'],b['beta3'])]
    check('192/256 beta agreement below 1e-15',max(deltas)<1e-15)
else:deltas=None
out={'passed':all(v['passed'] for v in checks),'checks':checks,'faces':faces,'beta_precision_differences':deltas,
    'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
    'peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset}
c.write('checks.json',out)
print('CHECKS',out['passed'],len(checks),'maximum precision difference',max(deltas) if deltas else None)
