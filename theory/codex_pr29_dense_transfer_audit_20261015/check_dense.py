"""Independent dense-transfer checks; no author imports; CPU only."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'): os.environ[key]='1'
import json
from pathlib import Path
import mpmath as mp

HERE=Path(__file__).resolve().parent

def schedule(n,ell,tail):
    d=n//4; T=d+ell+tail+32; start=ell+tail+40
    end=T-tail-16
    if (end-start)%2: end-=1
    events={}
    for t in range(start,T+1): events.setdefault(t,{})[7+t-start]=0
    for first in range(start+1,end,2):
        for arrival,sg in ((first,1),(first+1,-1)):
            for t in range(arrival-ell+1,arrival+1):
                i=d-1-arrival+t
                assert i not in events.setdefault(t,{})
                events[t][i]=sg if first-8<=t<=first-2 else 0
    return T,events

def run(n=256,precision=90,perturb='uniform'):
    mp.mp.dps=precision
    k=n//2; d=n//4; a=1-mp.mpf(1)/n; lam=mp.mpf(1)/(100*n)
    gamma=1/(1-1/mp.sqrt(k)); w=[-1/mp.sqrt(k)]*k; w[0]+=1
    def reflect(v):
        dot=mp.fdot(w,v)
        return [x-gamma*wi*dot for x,wi in zip(v,w)]
    def base(v):
        u=reflect(v[:k]); p=u.copy(); p[0]=u[d-1]; p[1:d]=u[:d-1]
        return [a*x for x in reflect(p)]+[lam*x for x in v[k:]]
    eta=mp.mpf(1)/(10**8*n*n)
    q=mp.matrix([mp.sqrt(mp.mpf(k)/n),0,mp.sqrt(mp.mpf(n-k)/n)])
    r=mp.matrix([0,a*mp.sqrt(mp.mpf(k)/n),lam*mp.sqrt(mp.mpf(n-k)/n)])
    H=mp.diag([a*a,a*a,lam*lam])+eta*(r*q.T+q*r.T)+eta**2*q*q.T
    eig=mp.eigsy(H,eigvals_only=True)
    alpha=a/mp.sqrt(eig[2])
    # Actual prescribed alpha in the uniform case. The altered right factor
    # is an out-of-contract cancellation test, with the same harmless scalar.
    right=[mp.mpf(1)]*n
    if perturb=='altered': right[d-6]=mp.mpf(2)
    denom=mp.sqrt(n)*mp.sqrt(mp.fdot(right,right))
    def actual(v):
        field=eta*mp.fdot(right,v)/denom
        return [alpha*(x+field) for x in base(v)]
    sigma=mp.mpf('.05')
    for _ in range(30): sigma=mp.tanh(lam*sigma+mp.mpf('.05'))
    T,events=schedule(n,16,12)
    hs=[[mp.mpf(0)]*n for _ in range(2)]
    credits=[[mp.mpf(0)]*n for _ in range(2)]
    endpoint=mp.mpf(0); off=mp.mpf(0); sums=mp.mpf(0); maxinput=mp.mpf(0)
    maximum_support=0; history=[]
    for t in range(1,T+1):
        current=[]
        for idx,theta in enumerate((1,-1)):
            old=hs[idx]; pre=[x+mp.mpf('.05') for x in actual(old)]
            hn=[mp.tanh(x) for x in pre]; inputs=[mp.mpf(0)]*n
            for i,sg in events.get(t,{}).items():
                targetpre=sg*mp.mpf('.45')*(1+theta)/2
                hn[i]=mp.tanh(targetpre); inputs[i]=targetpre-pre[i]
            maximum_support=max(maximum_support,sum(x!=0 for x in inputs))
            maxinput=max(maxinput,*map(abs,inputs))
            c=mp.fsum(old[k:])/(sigma*(n-k))
            precredit=actual(credits[idx]); precredit[0]+=c
            credits[idx]=[(1-x*x)*b for x,b in zip(hn,precredit)]
            hs[idx]=hn; current.append(hn)
        mods={i for i,sg in events.get(t,{}).items() if sg}
        diff=[x-y for x,y in zip(*current)]
        off=max(off,*[abs(x) for i,x in enumerate(diff) if i not in mods])
        sums=max(sums,abs(mp.fsum(diff)))
        history.append(credits[0][0]-credits[1][0])
    endpoint=max(abs(x-y) for x,y in zip(*hs))
    result=dict(n=n,precision=precision,perturbation=perturb,eta=str(eta),alpha=str(alpha),
                T=T,peak_support=maximum_support,max_input=str(maxinput),
                off_modulation_difference=str(off),sum_difference=str(sums),endpoint_difference=str(endpoint),
                actual_full_group_B00_difference=str(credits[0][0]-credits[1][0]),
                largest_B00_difference=str(max(map(abs,history))))
    if perturb=='uniform':
        assert endpoint<mp.mpf(10)**(-precision+10)
        assert off<mp.mpf(10)**(-precision+10)
        assert maximum_support<=17
        assert abs(credits[0][0]-credits[1][0])>mp.mpf(10)**(-precision/2)
    return result

if __name__=='__main__':
    results=[run(256,80),run(256,110),run(256,80,'altered')]
    (HERE/'dense_results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))
