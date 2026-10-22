"""Direct-matrix simulation and frozen-input gradient finite differences.
Small sizes are OUTSIDE theorem domain; checks algebra, not asymptotic theorem.
No author/previous-audit imports. CPU, single BLAS thread.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
import math,json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def setup(n):
    k=n//2;d=n//4;root=math.sqrt(k);g=1/(1-1/root)
    w=np.eye(k)[0]-np.ones(k)/root
    U=np.eye(k)-g*np.outer(w,w)
    pred=np.arange(k);pred[0]=d-1;pred[1:d]=np.arange(d-1)
    R=(1-1/n)*U@np.eye(k)[pred]@U
    sigma=.05
    for _ in range(40):sigma=math.tanh(.05+sigma/(100*n))
    return U,R,sigma

def history(n,H,z):
    U,R,sigma=setup(n);k=n//2;d=n//4;T=n//2;ts=T-d+20
    cols=d+2*np.arange(1,len(z)+1);starts=ts+20+np.arange(len(z))*(H+1)
    assert starts[-1]+H<=T-2
    h=np.zeros(k);source=0.;B=np.zeros((k,len(z)));controls=[];cs=[]
    maximum=0.;support=0
    for t in range(1,T+1):
        pre=R@h+.05;hn=np.tanh(pre);bath=hn[-1];x=np.zeros(k)
        setting={}
        if t>=ts:setting[d-1-(T-t)]=0.
        for i,start in enumerate(starts):
            if start<=t<start+H:
                v=math.tanh(.19*(1+z[i])) if start+H//2<=t<start+H//2+7 else 0.
                setting[int(cols[i])]=v;setting[int(cols[i]+1)]=-v
            elif t==start+H:setting[int(cols[i])]=bath;setting[int(cols[i]+1)]=bath
        for j,v in setting.items():x[j]=math.atanh(v)-pre[j];hn[j]=v
        c=source/sigma;B=R@B;B[cols,np.arange(len(z))]+=c;B*=(1-hn**2)[:,None]
        controls.append(x);cs.append(c);maximum=max(maximum,float(np.max(abs(x))));support=max(support,int(np.count_nonzero(x)))
        h=hn;source=math.tanh(.05+source/(100*n))
    return dict(h=h,B=B,x=controls,cs=cs,cnext=source/sigma,cols=cols,R=R,U=U,
                max_input=maximum,peak=support)

def frozen_loss(hist,col,epsilon):
    h=np.zeros(len(hist['h']))
    for x,c in zip(hist['x'],hist['cs']):
        pre=hist['R']@h+.05+x;pre[col]+=epsilon*c;h=np.tanh(pre)
    # This query is held FIXED when differentiating, as are all past controls.
    xquery=.25-(hist['R']@hist['h']+.05)
    pre=hist['R']@h+.05+xquery;pre[col]+=epsilon*hist['cnext']
    return float(np.sum(np.tanh(pre)))

def main():
    results=[]
    cases=[(512,61,np.array([1.])),(1024,101,np.array([.6,-.8])),
           (1024,100,np.array([1e-5,math.sqrt(1-1e-10)]))]
    for n,H,z in cases:
        p,m=history(n,H,z),history(n,H,-z);k=n//2
        HI=1/math.cosh(.25)**2;row=n//4-1
        actual=(p['B']-m['B']).T@(p['R'].T@(HI*np.ones(k)))
        transformed=p['U']@(p['B']-m['B'])
        gathered=(1-1/n)*HI*math.sqrt(k)*transformed[row]
        assert np.max(abs(actual-gathered))<1e-9
        finite=[]
        eps=1e-6
        raw_errors=[]
        for i,col in enumerate(p['cols']):
            derivp=(frozen_loss(p,col,eps)-frozen_loss(p,col,-eps))/(2*eps)
            derivm=(frozen_loss(m,col,eps)-frozen_loss(m,col,-eps))/(2*eps)
            halfp=(frozen_loss(p,col,eps/2)-frozen_loss(p,col,-eps/2))/eps
            halfm=(frozen_loss(m,col,eps/2)-frozen_loss(m,col,-eps/2))/eps
            raw_errors.append(abs(derivp-derivm-actual[i]))
            finite.append((4*(halfp-halfm)-(derivp-derivm))/3)
        error=float(np.max(abs(np.array(finite)-actual)))
        assert error<2e-6
        results.append({'n':n,'H':H,'theta':z.tolist(),'query_identity_error':float(np.max(abs(actual-gathered))),
                        'fixed_input_gradient_difference_error':error,'analytic_readout':actual.tolist(),
                        'raw_central_difference_error':max(raw_errors),'step':eps,
                        'finite_difference_readout':finite,'endpoint_error':float(np.max(abs(p['h']-m['h']))),
                        'peak_actual_support':max(p['peak'],m['peak']),
                        'max_input':max(p['max_input'],m['max_input']),
                        'scope':'finite consistency checks; below theorem n and bath may violate H'})
    (HERE/'independent_frozen_query_result.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))

if __name__=='__main__':main()
