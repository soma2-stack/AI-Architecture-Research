"""Post-screen numerical curvature/high-precision checks, with no search feedback."""
import numerics as n
import json,time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import mpmath as mp
from scipy.stats import qmc
import psutil
HERE=Path(__file__).resolve().parent

def selected():
    primary=json.loads((HERE/'results.json').read_text(encoding='utf-8'))
    chosen={}
    for d in primary['dimensions']:
        good=[v for v in d['cases'] if v['all_numerical_lifts_valid'] and v['max_normal_usage']<=1+1e-10]
        ch=max(good or d['cases'],key=lambda v:v['minimum_found_ratio'])
        chosen[d['dimension']]={'a':ch['a'],'ah':ch['ah'],'basis':ch['basis'],'ratio':ch['minimum_found_ratio'],
            'faces':ch['faces'],'source':'primary','proxy':ch['third_order_proxy'],'normal_usage':ch['max_normal_usage']}
    refined=json.loads((HERE/'refinement_results.json').read_text(encoding='utf-8'))
    for d in refined['dimensions']:
        c=max(d['candidates'],key=lambda z:z['validated_min_ratio'])
        if c['validated_min_ratio']>chosen[d['dimension']]['ratio']:
            faces=c['fresh_faces'] if c['fresh_min_ratio']<=c['validation']['minimum_found_ratio'] else c['validation']['faces']
            chosen[d['dimension']]={'a':c['a'],'ah':c['ah'],'basis':c['basis'],'ratio':c['validated_min_ratio'],
                'faces':faces,'source':'secondary direct amplitude','proxy':c['proxy'],
                'normal_usage':max(c['fresh_normal_usage'],c['validation']['max_normal_usage'])}
    return chosen

def directional_third(m,B,a,z,kappas):
    """Signed univariate third derivative of the actual terminal fixed-h section."""
    directions=z*np.array(a)[None,:]
    v=(directions@(B[:,4:]*n.SD).T).reshape(len(z),37,4)
    v=np.repeat(v,len(kappas),axis=0);k=np.tile(kappas,len(z));batch=len(k)
    h=np.zeros((batch,4));h1=h.copy();h2=h.copy();h3=h.copy()
    S=np.zeros((batch,24));s1=S.copy();s2=S.copy();s3=S.copy();ow=m.owner
    for t,x0 in enumerate(m.X[:-1]):
        x=x0+v[:,t]*k[:,None];dx=v[:,t]
        H=np.tanh(h*m.R+x@m.W.T+m.b);g=1-H*H;f2=-2*H*g;f3=-2*g*(1-3*H*H);f4=8*H*g*(2-3*H*H)
        a1=h1*m.R+dx@m.W.T;a2=h2*m.R;a3=h3*m.R
        p=S*m.rd+np.where(m.kind==0,h[:,ow],np.where(m.kind==1,x[:,m.col],1.))
        p1=s1*m.rd+np.where(m.kind==0,h1[:,ow],np.where(m.kind==1,dx[:,m.col],0.))
        p2=s2*m.rd+(m.kind==0)*h2[:,ow];p3=s3*m.rd+(m.kind==0)*h3[:,ow]
        ao=a1[:,ow];a2o=a2[:,ow];a3o=a3[:,ow]
        ns3=g[:,ow]*p3+f2[:,ow]*(p*a3o+3*p1*a2o+3*p2*ao)+f3[:,ow]*(3*p*a2o*ao+3*p1*ao*ao)+f4[:,ow]*p*ao**3
        ns2=g[:,ow]*p2+f2[:,ow]*(p*a2o+2*p1*ao)+f3[:,ow]*p*ao**2
        ns1=g[:,ow]*p1+f2[:,ow]*p*ao;ns=g[:,ow]*p
        nh3=g*a3+3*f2*a2*a1+f3*a1**3;nh2=g*a2+f2*a1*a1;nh1=g*a1
        h,h1,h2,h3=H,nh1,nh2,nh3;S,s1,s2,s3=ns,ns1,ns2,ns3
    dx3=-(h3*m.R)@m.Winv.T
    ds3=(1-m.h0[ow]**2)*(s3*m.rd+np.where(m.kind==0,h3[:,ow],np.where(m.kind==1,dx3[:,m.col],0.)))
    return ds3*m.sw

def hp_pair(m,B,a,z,dps):
    mp.mp.dps=dps
    def val(x):
        if isinstance(x,str):f=F(x);return mp.mpf(f.numerator)/f.denominator
        return mp.mpf(float(x))
    th=list(map(val,m.c['model_parameters']));R=th[:4];W=mp.matrix([th[4+4*i:4+4*(i+1)] for i in range(4)]);b=mp.matrix(th[20:])
    Wi=W**-1;X=[[val(x) for x in row] for row in m.c['endpoint']['X']]
    weights=[mp.sqrt(sum(x*x for x in th[lo:hi])/(hi-lo)) for lo,hi in ((0,4),(4,20),(20,24))]
    h0=mp.matrix([0]*4)
    for x in X:h0=mp.matrix([mp.tanh(R[i]*h0[i]+sum(W[i,j]*x[j] for j in range(4))+b[i]) for i in range(4)])
    responses=[];maxnormal=mp.mpf(0);residual=mp.mpf(0)
    for sign in (-1,1):
        v=[sign*val(aa)*val(zz) for aa,zz in zip(a,z)];hp=[mp.mpf(0)]*4;S=[[mp.mpf(0)]*6 for _ in range(4)]
        for t in range(36):
            x=[X[t][j]+mp.sqrt(mp.mpf(3)/32)*sum(val(B[4*t+j,4+k])*v[k] for k in range(len(v))) for j in range(4)]
            hn=[];Sn=[]
            for i in range(4):
                H=mp.tanh(R[i]*hp[i]+sum(W[i,j]*x[j] for j in range(4))+b[i]);g=1-H*H
                injection=[hp[i]]+x+[mp.mpf(1)];Sn.append([g*(R[i]*S[i][j]+injection[j]) for j in range(6)]);hn.append(H)
            hp,S=hn,Sn
        x=Wi*mp.matrix([mp.atanh(h0[i])-R[i]*hp[i]-b[i] for i in range(4)])
        y=[(x[j]-X[-1][j]-mp.sqrt(mp.mpf(3)/32)*sum(val(B[144+j,4+k])*v[k] for k in range(len(v))))/mp.sqrt(mp.mpf(3)/32) for j in range(4)]
        maxnormal=max(maxnormal,max(abs(w) for w in y));sn=[]
        for i in range(4):
            injection=[hp[i]]+list(x)+[mp.mpf(1)]
            sn.extend((1-h0[i]**2)*(R[i]*S[i][j]+injection[j])*weights[0 if j==0 else 2 if j==5 else 1] for j in range(6))
            residual=max(residual,abs(mp.tanh(R[i]*hp[i]+sum(W[i,j]*x[j] for j in range(4))+b[i])-h0[i]))
        responses.append(sn)
    beta=max(mp.mpf(1),mp.sqrt(sum(r*r for r in R)));high=1-mp.tanh(mp.mpf(1)/4)**2
    D=high/(2*beta)*mp.sqrt(sum((R[p//6]*(responses[1][p]-responses[0][p]))**2 for p in range(24)))
    return {'dps':dps,'separation':mp.nstr(D,dps),'ratio':mp.nstr(D/mp.mpf('.002'),dps),
            'normal_max':mp.nstr(maxnormal,dps),'hidden_residual':mp.nstr(residual,dps)}

def main():
    start=time.perf_counter();cpu=time.process_time();m=n.Model();bases=np.load(HERE/'bases.npz');cases=selected();rows=[]
    for r,c in sorted(cases.items()):
        B=bases[c['basis']][:,:4+r];ch=m.chart(B);a=np.array(c['a'])
        Z=np.array([f['argmin'] for f in c['faces']]+list(np.eye(r))+list(qmc.Sobol(r,scramble=True,seed=412000+r).random_base2(5)*2-1))
        third=directional_third(m,B,a,Z,np.linspace(-1,1,9));Phi3=third@ch['Q'].T/a[None,:]
        M3=np.max(abs(Phi3),axis=0);mu=(7/8)*a/(2*m.beta*np.linalg.norm(ch['Q']/m.rd[None,:],axis=1));pen=mu*M3/6
        f=min(c['faces'],key=lambda v:v['ratio']);hp=[hp_pair(m,B,a,f['argmin'],dps) for dps in (60,90)]
        mismatch=abs(float(hp[-1]['separation'])-f['minimum_found'])
        if mismatch>1e-10:raise RuntimeError('selected actual separation high-precision disagreement')
        rows.append({'dimension':r,'selected_source':c['source'],'basis':c['basis'],'ah':c['ah'],'a':c['a'],
            'minimum_found_ratio':c['ratio'],'minimum_found_separation':c['ratio']*.002,'weakest_face':f['face'],
            'hidden_usage':c['normal_usage'],'proxy':c['proxy'],
            'sampled_M3':M3.tolist(),'sampled_third_penalty':pen.tolist(),
            'sampled_curvature_label':'NUMERICAL SAMPLE; neither supremum nor uniform bound',
            'path_samples':len(Z)*9,'high_precision':hp,'float64_hp_abs_difference':mismatch,
            'tangent_spectrum':ch['sv'].tolist()})
        print(f'r{r}: numerical ratio {c["ratio"]:.6f}; max sampled cubic penalty {pen.max():.6g}; HP diff {mismatch:.2g}',flush=True)
    mem=psutil.Process().memory_info()
    (HERE/'diagnostics.json').write_text(json.dumps({'label':'POST-SCREEN NUMERICAL DIAGNOSTICS ONLY; NO OPTIMIZATION FEEDBACK',
        'rows':rows,'resources':{'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-start,
        'peak_ram_bytes':getattr(mem,'peak_wset',mem.rss),'gpu_seconds':0}},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
