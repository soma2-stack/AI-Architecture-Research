"""Numerical-only independent signed chain rules and nonlinear fixed-h solve."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import itertools,json,time
from pathlib import Path
from fractions import Fraction as F
import mpmath as m
import numpy as np
import psutil
HERE=Path(__file__).resolve().parent
c=json.loads((HERE/'frozen_candidate.json').read_text(encoding='utf-8'))
def val(x):
    f=F(x); return m.mpf(f.numerator)/f.denominator
def initialize(dps):
    m.mp.dps=dps
    th=[val(x) for x in c['model_parameters']]
    B=[[val(x)*m.sqrt(m.mpf(3)/32) for x in row] for row in c['B']]
    X=[[val(x) for x in row] for row in c['endpoint']['X']]
    a=[val(c['ah'])]*4+[val(x) for x in c['a']]
    weights=[m.sqrt(sum(x*x for x in th[lo:hi])/(hi-lo)) for lo,hi in ((0,4),(4,20),(20,24))]
    return th,B,X,a,weights

def tight_derivatives(w,data):
    th,B,X,a,weights=data; unit=1;r=th[unit];W=th[4+4*unit:4+4*(unit+1)];b=th[20+unit]
    h=h1=h2=h3=s=s1=s2=m.mpf(0)
    for t,x0 in enumerate(X):
        bt=B[4*t:4*t+4]
        x=[x0[j]+sum(bt[j][k]*w[k] for k in range(11)) for j in range(4)]
        a0=r*h+sum(W[j]*x[j] for j in range(4))+b
        a1=r*h1+sum(W[j]*bt[j][0] for j in range(4))
        a2=r*h2;a3=r*h3
        H=m.tanh(a0);g=1-H*H;g2=-2*H*g;g3=-2*g*(1-3*H*H)
        p=r*s+1;p1=r*s1;p2=r*s2
        s2n=g*p2+2*g2*a1*p1+(g2*a2+g3*a1*a1)*p
        s1n=g*p1+g2*a1*p;sn=g*p
        h3n=g*a3+3*g2*a2*a1+g3*a1**3
        h2n=g*a2+g2*a1*a1;h1n=g*a1
        h,h1,h2,h3,s,s1,s2=H,h1n,h2n,h3n,sn,s1n,s2n
    return h3,s2*weights[2]

def full_state(w,data,normal_jac=False):
    th,B,X,a,weights=data
    h=[m.mpf(0)]*4;ds=[[m.mpf(0)]*6 for _ in range(4)];dh=[[m.mpf(0)]*4 for _ in range(4)]
    for t,x0 in enumerate(X):
        bt=B[4*t:4*t+4]
        x=[x0[j]+sum(bt[j][k]*w[k] for k in range(11)) for j in range(4)]
        hn=[];sn=[];dhn=[]
        for i in range(4):
            r=th[i];W=th[4+4*i:4+4*(i+1)]
            H=m.tanh(r*h[i]+sum(W[j]*x[j] for j in range(4))+th[20+i]);g=1-H*H
            injection=[h[i]]+x+[m.mpf(1)]
            sn.append([g*(r*ds[i][j]+injection[j]) for j in range(6)])
            hn.append(H)
            dhn.append([g*(r*dh[i][j]+sum(W[k]*bt[k][j] for k in range(4))) for j in range(4)])
        h,ds,dh=hn,sn,dhn
    support=[ds[i][j]*weights[0 if j==0 else 2 if j==5 else 1] for i in range(4) for j in range(6)]
    return m.matrix(h),m.matrix(support),m.matrix(dh)

def face_one(dps):
    data=initialize(dps);*_,amps,weights=data
    h0,_,_=full_state([m.mpf(0)]*11,data)
    endpoints=[];maxres=m.mpf(0);maxy=m.mpf(0)
    for sign in (-1,1):
        w=[m.mpf(0)]*11;w[4]=sign*amps[4]
        for k in range(20):
            h,s,J=full_state(w,data);res=h-h0
            if m.norm(res,m.inf)<m.mpf(10)**(-dps+15): break
            step=m.lu_solve(J,res)
            for i in range(4):w[i]-=step[i]
        h,s,J=full_state(w,data)
        res=m.norm(h-h0,m.inf);maxres=max(maxres,res);maxy=max(maxy,max(abs(v) for v in w[:4]))
        if res>=m.mpf(10)**(-dps+15) or maxy>amps[0]: raise RuntimeError('numerical fixed-h solve failed')
        endpoints.append(s)
    K=m.matrix([[val(x) for x in row] for row in c['K_selected']]);L=m.matrix([[val(x) for x in row] for row in c['L']])
    d=K*L*(endpoints[1]-endpoints[0]);phi=abs(d[0]/amps[4])
    ref=json.loads((HERE/'result_256.json').read_text(encoding='utf-8'))
    mu=val(ref['mu'][0]); beta=val(ref['beta'][0])
    if phi*mu<2*beta:raise RuntimeError('numerical face-1 validation contradicts bound')
    return {'dps':dps,'normal_max':m.nstr(maxy,dps),'normal_limit':c['ah'],
            'fixed_h_residual_max':m.nstr(maxres,dps),'Phi1_antipodal_difference':m.nstr(phi,dps),
            'numerical_dual_query_lower_estimate':m.nstr(mu*phi,dps),'certified_separation':ref['separation'][0]}

def main():
    start=time.perf_counter();cpu=time.process_time()
    data=initialize(90); amps=data[3]
    bs=np.load(HERE/'bounds_256.npz');limits=[bs['HH3'][1,0,0,0],bs['HS'][11,0,0]]
    best=[(m.mpf(0),None,None),(m.mpf(0),None,None)]
    for number,signs in enumerate(itertools.chain([None],itertools.product((-1,1),repeat=11))):
        w=[m.mpf(0)]*11 if signs is None else [s*a for s,a in zip(signs,amps)]
        vals=tight_derivatives(w,data)
        for k,v in enumerate(vals):
            ratio=abs(v)/m.mpf(float(limits[k]))
            if ratio>best[k][0]:best[k]=(ratio,signs,v)
            if ratio>1+m.mpf('1e-70'):raise RuntimeError('actual derivative exceeds independent bound')
        if number%512==0:print(f'sensitive corner check {number}/2048',flush=True)
    records=[]
    for k,(ratio,signs,v) in enumerate(best):
        finer=initialize(120);w=[m.mpf(0)]*11 if signs is None else [s*a for s,a in zip(signs,finer[3])]
        high=tight_derivatives(w,finer)[k]
        if abs(v-high)>m.mpf('1e-80'):raise RuntimeError('sensitive derivative precision mismatch')
        records.append({'array':'HH3' if k==0 else 'HS','index':[1,0,0,0] if k==0 else [11,0,0],
                        'point_signs':signs,'actual_abs_90dps':m.nstr(abs(v),90),
                        'actual_abs_120dps':m.nstr(abs(high),120),'bound':float(limits[k]),
                        'actual_to_bound_ratio':float(ratio),'precision_difference':m.nstr(abs(v-high),20)})
    faces=[face_one(dps) for dps in (90,120)]
    if abs(val(faces[0]['Phi1_antipodal_difference'])-val(faces[1]['Phi1_antipodal_difference']))>m.mpf('1e-70'):
        raise RuntimeError('face 1 cross-precision mismatch')
    mem=psutil.Process().memory_info()
    result={'status':'NUMERICAL SUPPORTING CHECKS PASS; NOT CERTIFICATES','sample_count':2049,
            'sensitive_entries':records,'face_one':faces,
            'resources':{'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-start,
                         'peak_ram_bytes':getattr(mem,'peak_wset',mem.rss),'gpu_seconds':0}}
    (HERE/'sensitive_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'sensitive_ratios':[x['actual_to_bound_ratio'] for x in records],
                     'face1':faces,'resources':result['resources']},indent=2),flush=True)
if __name__=='__main__':main()
