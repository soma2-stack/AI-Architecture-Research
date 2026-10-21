"""Independent full-vector U P U reference replaying finite physical controls.
Replay checks transport/credit/inputs, not an independent derivation of policy.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import importlib.util,numpy as np,math,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('own_legal',HERE/'legal_class.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def verify(kw):
    r=mod.simulate(**kw,trace=True);n=kw['n'];k=n//2;d=n//4;a=1-1/n;ga=1/(1-1/math.sqrt(k));eps=ga/k
    counts=np.array(r['counts']);G=len(counts);P=int(sum(counts));classes=np.repeat(np.arange(G),counts)
    Hs=np.arange(d,d+P);j=k-2;jp=k-1;assert d+P<j
    w=-np.ones(k)/math.sqrt(k);w[0]+=1
    def U(z):return z-ga*np.multiply.outer(z@w,w)
    def O(z):
        v=U(z);p=v.copy();p[:,1:d]=v[:,:d-1];p[:,0]=v[:,d-1];return U(p)
    h=np.zeros((2,k));b=h.copy();src=0.;sig=.05;lam=1/(100*n)
    for _ in range(100):sig=math.tanh(lam*sig+.05)
    errY=errF=0.;maxin=0.;width=np.zeros(2,int);ddL1=0.;T=r['T']
    for t,ctrl in enumerate(r['trace']['controls']):
        pre=a*O(h)+.05;hn=np.tanh(pre);x=np.zeros_like(h)
        mask=np.array(ctrl['mask']);ret=np.array(ctrl['ret']);pair=np.array(ctrl['pair']);pm=np.array(ctrl['pair_mask'])
        ridx=Hs[mask[classes]]
        for hi in range(2):
            vals=ret[hi,classes[mask[classes]]];x[hi,ridx]=np.arctanh(vals)-pre[hi,ridx];hn[hi,ridx]=vals
            pidx=np.array([j,jp])[pm];pv=pair[hi,pm];x[hi,pidx]=np.arctanh(pv)-pre[hi,pidx];hn[hi,pidx]=pv
            width[hi]=max(width[hi],np.count_nonzero(x[hi]));maxin=max(maxin,float(abs(x[hi]).max()))
        ddL1+=float(abs(x[0]-x[1]).sum())
        gates=1-hn**2;c=src/sig;yy=U(b);bb=a*O(b);bb[:,j]+=c;bn=gates*bb;yn=U(bn)
        v=yy.copy();v[:,1:d]=yy[:,:d-1];v[:,0]=yy[:,d-1];v*=a
        bathrow=d-1;hat=gates[:,bathrow];delta=gates-hat[:,None];delta[:,0]=0
        F=-eps*((delta[:,1:]*v[:,1:]).sum(1)+c*gates[:,j]);ext=F+eps*np.sum(delta[:,Hs]*v[:,Hs],axis=1)
        errF=max(errF,float(abs(ext-np.array(r['trace']['Fext'][t])).max()))
        Yexpected=np.array(r['trace']['Yret'][t])[:,classes]
        errY=max(errY,float(abs(yn[:,Hs]-Yexpected).max()))
        h,b=hn,bn;src=math.tanh(lam*src+.05)
    endpoint=float(abs(h[0]-h[1]).max());yd=U(b)[0]-U(b)[1];D=float(yd[Hs].sum());l1=float(abs(yd[Hs]).sum())
    zr=np.zeros((1,k));zr[0,Hs]=yd[Hs];pv=zr.copy();pv[:,1:d]=zr[:,:d-1];pv[:,0]=zr[:,d-1]
    coef=a*U(pv)[0];actual=a*O(b[0:1]-b[1:2])[0]
    candidates=[]
    for plus in [True,False]:
        query=np.where(coef>=0,mod.HI if plus else mod.LO,mod.LO if plus else mod.HI)
        candidates.append((abs(float(coef@query)),float(actual@query)))
    retquery,fullquery=max(candidates)
    assert max(errY,errF)<1e-10 and endpoint<1e-13
    assert width.tolist()==r['m_plus_minus'] and abs(maxin-r['max_input'])<1e-10
    assert abs(l1-r['population_L1_difference'])<1e-9
    assert abs(retquery-r['legal_one_step_retainer_component_optimum'])<1e-9
    # Complementary legal gate boxes give exactly equal/opposite retainer
    # component values (its uniform-query coefficient is zero). Floating ties
    # can pick either. Require agreement with the selected query in this pair.
    fullquery_error=min(abs(v-r['legal_same_query_full_selected_readout']) for _,v in candidates)
    assert fullquery_error<1e-9,(kw,candidates,r['legal_same_query_full_selected_readout'])
    return {'kwargs':kw,'max_Y_error':errY,'max_Fext_error':errF,'endpoint_float_gap':endpoint,
            'input_max':maxin,'width':width.tolist(),'T':T,'full_population_sum':D,'full_population_L1':l1,'class_population_L1':r['population_L1_difference'],
            'legal_query_retainer_component':retquery,'legal_query_full_selected':fullquery,
            'selected_query_error_allowing_complement_tie':fullquery_error,
            'input_difference_L1_full':ddL1,'input_difference_L1_class':r['sum_input_difference_L1']}

if __name__=='__main__':
    cases=[dict(n=4096,kind='kernel',counts=[16,16],T=160),dict(n=4096,kind='cost',warm=20,u=.1,H=100),
           dict(n=8192,kind='stair',K=1,rho=3,top=.2,settle=.02,warm=30,level=1.)]
    rows=[verify(x) for x in cases];(HERE/'full_crosscheck_results.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
