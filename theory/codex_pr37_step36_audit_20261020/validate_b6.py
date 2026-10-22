"""Full-vector cross-check of B6, using U P U rather than class transport.
No imports of author code. Deliberately small n: identity/implementation tests.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import numpy as np
import math,json
from pathlib import Path
import importlib.util
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('b6_independent',HERE/'b6_legal.py')
red=importlib.util.module_from_spec(spec);spec.loader.exec_module(red)

def full(n,P,kind,H=90,gap=130,warm=25,source='bipolar'):
    k=n//2;d=n//4;a=1-1/n;ga=1/(1-1/math.sqrt(k));sk=math.sqrt(k);q=ga/sk
    w=-np.ones(k)/sk;w[0]+=1
    def U(z):return z-ga*np.multiply.outer(z@w,w)
    def Op(z):
        zz=U(z);p=zz.copy();p[:,1:d]=zz[:,:d-1];p[:,0]=zz[:,d-1];return U(p)
    G=min(P,16);counts=np.full(G,P//G,int);counts[:P%G]+=1;ids=np.repeat(np.arange(G),counts)
    rows=np.arange(d+2,d+2+P);j=k-3;jp=k-2;assert rows[-1]<j
    T=warm+H+gap;h=np.zeros((2,k));B=h.copy();own=np.zeros(2);src=0.;sig=.05;lam=1/(100*n)
    for _ in range(100):sig=math.tanh(lam*sig+.05)
    pulses=[(warm+H//3,0),(warm+2*H//3,1)] if source!='autonomous' else []
    Fs=[];Ext=[];gates_all=[];yrall=[];xmax=0.;peakwidth=total=0;peakown=peakY=0.
    for t in range(1,T+1):
        pre=a*Op(h)+.05;hn=np.tanh(pre)
        mask,tg=red.policy(t,warm,H,gap,kind,ids);mnow=0
        if mask.any():
            r=rows[mask];x=np.arctanh(tg[mask])[None,:]-pre[:,r]
            xmax=max(xmax,float(abs(x).max()));hn[:,r]=tg[mask];mnow+=int(np.count_nonzero(x[0]))
        if source!='autonomous' and warm<=t<warm+H:
            target=np.zeros((2,2))
            for st,hi in pulses:
                if st<=t<st+7:target[hi]=[math.tanh(.38),-math.tanh(.38)]
            x=np.arctanh(target)-pre[:,[j,jp]];xmax=max(xmax,float(abs(x).max()));mnow+=2
            hn[:,[j,jp]]=target
        peakwidth=max(peakwidth,mnow);total+=mnow
        g=1-hn*hn;gb=g[:,d-1].copy();delta=g-gb[:,None];delta[:,0]=0
        prev=U(B);p=prev.copy();p[:,1:d]=prev[:,:d-1];p[:,0]=prev[:,d-1];v=a*p
        c=src/sig;nb=a*Op(B);nb[:,j]+=c;Bnew=g*nb;yn=U(Bnew)
        S=delta[:,1:].sum(1);cap=q*(delta[:,rows]-ga*S[:,None]/k)*v[:,0,None]
        # Infer F directly from the *full* post-gate U P U result.
        probes=yn[:,rows]-a*g[:,rows]*prev[:,rows]-cap
        F=probes.mean(1);ext=F+ga*a/k*(delta[:,rows]*prev[:,rows]).sum(1)
        assert np.max(abs(probes-F[:,None]))<1e-11
        Fs.append(F.tolist());Ext.append(ext.tolist());gates_all.append(g[:,rows].tolist());yrall.append(yn[:,rows].tolist())
        own=g[:,j]*(a*own+c);peakown=max(peakown,abs(float(own[0]-own[1])))
        peakY=max(peakY,abs(float(yn[0,j]-yn[1,j])))
        h=hn;B=Bnew;src=math.tanh(lam*src+.05)
    z=U(B[0:1]-B[1:2]);z[0,j]-=own[0]-own[1];z[0,d-1]=0
    p=z.copy();p[:,1:d]=z[:,:d-1];p[:,0]=z[:,d-1];coef=a*U(p)
    read=max(abs(float(np.maximum(red.LO*coef,red.HI*coef).sum())),abs(float(np.minimum(red.LO*coef,red.HI*coef).sum())))
    return {'F':np.array(Fs),'ext':np.array(Ext),'readout':read,'xmax':xmax,'m':peakwidth,
            'additive':total,'endpoint_gap':float(abs(h[0]-h[1]).max()),'peakown':peakown,'peakY':peakY}

if __name__=='__main__':
    cases=[]
    for fam,source in [('none','autonomous'),('hold','bipolar'),('anti_switch','bipolar'),('delayed_switch','bipolar'),('mixed_ages','bipolar'),('anti_hold','bipolar')]:
        n=4096;P=32
        f=full(n,P,fam,source=source);r=red.run(n,P,fam,H=90,gap=130,warm=25,source=source,trace=True)
        FF=np.array([t['F'] for t in r['trace']]);XX=np.array([t['ext'] for t in r['trace']])
        errF=float(abs(f['F']-FF).max());errX=float(abs(f['ext']-XX).max());errRead=abs(f['readout']-r['centered_query_optimum'])
        assert max(errF,errX,errRead)<1e-9
        assert f['m']==r['peak_actual_width_m'] and f['additive']==r['actual_additive_support']
        assert abs(f['xmax']-r['max_input'])<1e-12 and f['endpoint_gap']<1e-14
        cases.append({'family':fam,'source':source,'n':n,'P':P,'max_F_error':errF,'max_Fext_error':errX,
                      'readout_error':errRead,'endpoint_gap_full':f['endpoint_gap'],'m':f['m'],'max_input':f['xmax']})
    (HERE/'b6_validation.json').write_text(json.dumps(cases,indent=2));print(json.dumps(cases,indent=2))
