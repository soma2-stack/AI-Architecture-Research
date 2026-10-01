"""Phase B: one frozen recipe per preregistered winner, no feedback search."""
import os
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import json,hashlib,traceback
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import mpmath as mp
import cpu_jets as c
import certificate_kernel as e
from resources import Monitor,ROOT,CFG

def model(n,case):
    m=c.Model(case,n);saved=json.loads((ROOT/'models.json').read_text())['dense_parameters'][str(n)]
    full=list(map(Q,saved))
    if case=='dense':m.params=full
    else:m.params=[Q(6+3*i,20) for i in range(n)]+full[n*n:]
    assert m.P==(2*n*n+n if case=='dense' else n*n+2*n)
    return m

def base_for(w,bits,meter):
    mp.mp.dps=100;e.I.precision(bits);c.ACTIVE_METER=meter
    n=w['n'];m=model(n,w['case']);X=[[Q(x) for x in row] for row in w['X']]
    original=m.serialize();_,JI,_=c.jets(m,X,'interval');assert m.serialize()==original
    scales={g:e.I(sum(m.params[p]**2 for p,(_,_,name,_) in enumerate(m.meta) if name==g)/
                    sum(name==g for _,_,name,_ in m.meta)).sqrt() for g in ('R','W','b')}
    sd=e.I(Q(3,32)).sqrt();B=[[Q(x) for x in row] for row in w['B']];BI=[[e.I(x)*sd for x in row] for row in B]
    reduced=e.matmul(JI.tolist(),BI)
    for j,(_,p) in enumerate(m.support):reduced[n+j]=[x*scales[m.meta[p][2]] for x in reduced[n+j]]
    base={'n':n,'model':m,'X':X,'D':len(m.support),'U':[[Q(x) for x in row] for row in w['U']],
          'B':B,'BI':BI,'JI':JI.tolist(),'reduced':reduced,'scaleI':scales,
          'sigma':[e.dyadic(mp.mpf(x)) for x in w['singular_values']]}
    return base

def run_one(w,index,meter):
    recipe=w['recipe'];n=w['n'];r=recipe['r'];L=[[Q(x) for x in row] for row in w['L']]
    args=(r,Q(float(recipe['a0'])),recipe['profile'],Q(float(recipe['hidden_factor'])),L,True)
    base=base_for(w,192,meter);captured={};fn=e.curvature
    def wrapped(*a):
        HH,HS=fn(*a);captured.update(HH=HH,HS=HS);return HH,HS
    e.curvature=wrapped
    try:result=e.certify(base,*args)
    finally:e.curvature=fn
    directory=ROOT/'certificates';directory.mkdir(exist_ok=True)
    np.savez_compressed(directory/f'curvature_{index}_192.npz',**captured)
    row={'index':index,'n':n,'case':w['case'],'role':w['role'],'history_sha256':w['history_sha256'],
         'recipe_frozen':{k:recipe[k] for k in ('r','a0','profile','hidden_factor')},'result':result,'verified_256':False}
    (directory/f'candidate_{index}_192.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
    if result['valid'] and int(result['states'])>1:
        high=base_for(w,256,meter)
        Kh=[[Q(x) for x in line] for line in result['K_hidden']];K=[[Q(x) for x in line] for line in result['K_selected']]
        J=[line[:n+r] for line in high['reduced']];H0=[line[:n] for line in J[:n]];Ht=[line[n:] for line in J[:n]]
        Jp=e.matmul([[e.I(x) for x in line] for line in L],J[n:]);cross=e.matmul([line[:n] for line in Jp],e.matmul(e.inverse(H0),Ht))
        C0=[[Jp[i][n+j]-cross[i][j] for j in range(r)] for i in range(r)]
        mu,_=e.query_margins(high,L);key=(256,r,tuple(tuple(line) for line in L))
        high['_center_cache']={key:(Kh,e.abs_array(Kh),e.residual(Kh,H0),K,e.residual(K,C0),mu)}
        more={}
        def capture_high(*a):
            HH,HS=fn(*a);more.update(HH=HH,HS=HS);return HH,HS
        e.curvature=capture_high
        try:verified=e.certify(high,*args)
        finally:e.curvature=fn
        np.savez_compressed(directory/f'curvature_{index}_256.npz',**more)
        assert verified['valid'],'256-bit validity failure'
        rho=list(map(Q,result['rho_i']));old_mu=list(map(Q,result['mu_i']));aa=list(map(Q,result['a_i']))
        assert all(sum(abs(K[j][i])*rho[i] for i in range(r))<=(1-Q(verified['eta_sensitivity']))*aa[j] for j in range(r))
        assert all(x<=y for x,y in zip(old_mu,mu))
        N=[int(2*x*y//(Q(17,8)*Q(1,1000)))+1 for x,y in zip(rho,old_mu)]
        assert N==result['N_i']
        assert all(Q(17,8)*Q(1,1000)>2*Q(1,1000) for x in N)
        row['verified_256']=True;row['high_precision_result']=verified
        (directory/f'candidate_{index}_256.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
    return row

def main():
    frozen=json.loads((ROOT/'WINNERS_FROZEN.json').read_text());assert len(frozen['candidates'])==18
    assert not (ROOT/'certification_results.json').exists()
    assert hashlib.sha256((ROOT/'frozen_winners.json').read_bytes()).hexdigest()==frozen['winners_sha256']
    winners=json.loads((ROOT/'frozen_winners.json').read_text());meter=Monitor('CPU rigorous certification',gpu=False)
    outputs=[]
    try:
        c.hardware()
        for index,w in enumerate(winners):
            meter.check();print('Certifying frozen',index,w['n'],w['case'],w['role'],flush=True)
            row=run_one(w,index,meter);outputs.append(row)
            print('Result',row['result'].get('reason',(row['result'].get('robust_dimension'),row['result'].get('bits'))),flush=True)
        (ROOT/'certification_results.json').write_text(json.dumps(outputs,indent=2)+'\n',encoding='utf-8')
    except Exception:
        (ROOT/'CERTIFICATION_FAILURE.json').write_text(json.dumps({'traceback':traceback.format_exc(),'partial':outputs},indent=2)+'\n',encoding='utf-8')
        raise
    finally:meter.finish()

if __name__=='__main__':main()
