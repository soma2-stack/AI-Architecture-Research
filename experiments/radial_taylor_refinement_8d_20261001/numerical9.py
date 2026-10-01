"""Conditional float64 9D feasibility ONLY. Never calls a rigorous kernel."""
import os,sys,time,json,inspect,math
from pathlib import Path
for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[name]='1'
os.environ['CUDA_VISIBLE_DEVICES']='-1';sys.dont_write_bytecode=True
CPU=time.process_time();WALL=time.perf_counter();ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
SCREEN=REPO/'experiments/independent_dimension_feasibility_20261001'
import numpy as np
from fractions import Fraction as Q
from scipy.stats import qmc
from scipy.optimize import minimize
import psutil
sys.path.insert(0,str(SCREEN));import numerics as n
def write(name,obj):(ROOT/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def budget():
    if time.process_time()-CPU>120:raise TimeoutError('120 CPU-second numerical9 limit')
def gate_bounds(lo,hi):
    amin=np.where(lo*hi<=0,0,np.minimum(lo*lo,hi*hi));amax=np.maximum(lo*lo,hi*hi);hm=np.maximum(abs(lo),abs(hi))
    g=1-amin;old=[g,2*hm*g,2*g*np.maximum(abs(1-3*amin),abs(1-3*amax)),8*hm*g*np.maximum(abs(2-3*amin),abs(2-3*amax))]
    pol=((1,0,-1),(0,-2,0,2),(-2,0,8,0,-6),(0,16,0,-40,0,24))
    rr=((0,),(-np.sqrt(1/3),np.sqrt(1/3)),(0,-np.sqrt(2/3),np.sqrt(2/3)),
        tuple(s*np.sqrt((15+t*np.sqrt(105))/30) for s in (-1,1) for t in (-1,1)))
    out=[]
    for j in range(4):
        points=np.vstack([lo,hi]+[np.clip(v,lo,hi) for v in rr[j]])
        sharp=np.max(abs(np.polynomial.polynomial.polyval(points,pol[j])),axis=0)
        out.append(np.minimum(old[j],sharp))
    return tuple(out)
def install():
    n.__dict__['original_box2']=n.box2
    src=inspect.getsource(n.box2)
    old='        g=1-amin;f2=2*hm*g;f3=2*g*np.maximum(abs(1-3*amin),abs(1-3*amax));f4=8*hm*g*np.maximum(abs(2-3*amin),abs(2-3*amax))'
    assert src.count(old)==1
    n.__dict__['gate_bounds']=gate_bounds
    exec(src.replace(old,'        g,f2,f3,f4=gate_bounds(nl,nh)'),n.__dict__)
def refined_proxy(m,ch,a,ah):
    budget();r=len(a);B=ch['B'];amps=np.r_[np.full(4,ah),a]
    HH,HS,_,radius=n.box2(m,B,amps);H=ch['Jh'];Kh=np.linalg.inv(H[:,:4])
    Eh=abs(np.eye(4)-Kh@H[:,:4])+abs(Kh)@np.einsum('ijk,k->ij',HH[:,:4],amps)
    eta=float(Eh.sum(1).max());force=abs(Kh)@(abs(H[:,4:])@a+.5*np.einsum('ijk,j,k->i',HH[:,4:,4:],a,a))
    inc=float(force.max()/max((1-eta)*ah,1e-15))
    out={'valid':False,'radius':radius,'eta_h':eta,'inclusion_ratio':inc,'forcing':force.tolist(),'a':a.tolist(),'ah':float(ah)}
    if radius>1 or eta>=.75 or inc>1 or not np.isfinite(inc):return out
    ell=ch['Q']/a[:,None];g0=1-m.h0**2
    CS=ell*(g0[m.owner]*m.rd)[None,:];CH=np.zeros((r,4))
    for p in range(24):
        v=ell[:,p]*m.sw[p]*g0[m.owner[p]]
        if m.kind[p]==0:CH[:,m.owner[p]]+=v
        elif m.kind[p]==1:CH-=v[:,None]*(m.Winv[m.col[p]]*m.R)[None,:]
    sharp_box=n.box2
    try:
        n.box2=n.original_box2
        old_control=n.proxy(m,ch,a,ah)
    finally:n.box2=sharp_box
    orig=m.X;M=[]
    try:
        m.X=orig[:-1]
        for j in range(1,9):
            lam=j/8;_,_,gg,_=n.box2(m,B,np.r_[np.zeros(4),lam*a])
            h3,s3=n.box3_contracted(m,B,np.r_[np.zeros(4),a],gg)
            row=abs(CS)@s3+abs(CH)@h3
            if old_control['valid']:row=np.minimum(row,np.array(old_control['M3']))
            M.append(row)
    finally:m.X=orig
    weights=np.array([((1-j/8)**3-(1-(j+1)/8)**3)/3 for j in range(8)])
    half=np.array(M).T@weights/2
    e=(abs(np.eye(r)-ch['Q']@ch['A'])*a[None,:]/a[:,None]).sum(1)
    mu=(7/8)/(2*m.beta*np.linalg.norm(ell/m.rd[None,:],axis=1));beta=mu*(1-e-half)
    out.update(valid=True,beta=beta.tolist(),mu=mu.tolist(),half_remainder=half.tolist(),cubic_penalty=(mu*half).tolist(),old_control_valid=old_control['valid'],
               min_ratio=float(beta.min()/.001),bands_M3=np.array(M).tolist())
    return out
def score(v):
    if v['valid']:return 2/math.pi*math.atan(v['min_ratio'])
    return -2-max(0,v['radius']-1)-max(0,v['eta_h']/.75-1)-min(100,max(0,v['inclusion_ratio']-1))
def optimize(m,ch,seed,target):
    linear=(7/8)/(2*m.beta*np.linalg.norm(ch['Q']/m.rd[None,:],axis=1))
    aa=np.clip(target*.001/linear,1e-6,4);rad=float((abs(ch['B'][:,4:]*n.SD)@aa).max());aa*=min(1,.4/max(rad,1e-20))
    initials=[refined_proxy(m,ch,aa,h) for h in (1e-4,1e-3,.004,.016,.064,.256,1)]
    best=max(initials,key=score);x=np.log(np.r_[aa,best['ah']]);cur=best;rng=np.random.default_rng(seed);calls=7
    low=np.log(np.full(10,1e-6));high=np.log(np.r_[np.full(9,4),1])
    with (ROOT/f'trace9_{seed}.jsonl').open('w',encoding='utf-8') as log:
        def ev(v,kind,step):
            nonlocal calls
            rr=refined_proxy(m,ch,np.exp(v[:9]),np.exp(v[9]));calls+=1
            log.write(json.dumps({'step':step,'kind':kind,'result':rr},allow_nan=False)+'\n');return rr
        for step in range(80):
            delta=.08/(1+step/50)**.101;lr=.12/(1+step/40)**.602;sgn=rng.choice([-1.,1.],10)
            pp=ev(np.clip(x+delta*sgn,low,high),'plus',step);mm=ev(np.clip(x-delta*sgn,low,high),'minus',step)
            grad=(score(pp)-score(mm))/(2*delta)*sgn;trial=np.clip(x+lr*np.clip(grad,-10,10),low,high)
            prop=ev(trial,'proposal',step)
            if score(prop)>=score(cur):x=trial;cur=prop
            for rr in (pp,mm,prop):
                if score(rr)>score(best):best=rr
    winner={'seed':seed,'calls':calls,'result':best,'label':'NUMERICAL ONLY; selected before face attacks'}
    write(f'winner9_{seed}.json',winner);return winner
def attack(m,ch,a,ah,seed):
    sec=n.Section(m,ch['B'],np.array(a),ah);faces=[];rng=np.random.default_rng(seed)
    for i in range(9):
        budget();sob=qmc.Sobol(8,scramble=True,seed=seed+i).random_base2(6)*2-1
        u=np.vstack((np.zeros(8),sob,rng.choice([-1.,1.],(64,8))));z=np.insert(u,i,1,axis=1)
        dist,valid,y=sec.pairs(z);order=np.argsort(dist);found=float(dist.min());arg=z[int(np.argmin(dist))].tolist()
        results=[]
        def fg(v):
            budget();value,ok,yy,grad=sec.pairs(np.insert(v,i,1),jac=True)
            if not ok[0]:return 100+float(abs(yy).max()),np.zeros(8)
            return float(value[0]),np.delete(grad[0],i)
        for start in [np.zeros(8)]+[u[j] for j in order[:2]]:
            opt=minimize(fg,start,jac=True,method='L-BFGS-B',bounds=[(-1,1)]*8,
                         options={'maxiter':60,'ftol':1e-14,'gtol':1e-9})
            zz=np.insert(opt.x,i,1);dd,ok,yy=sec.pairs(zz)
            results.append({'distance':float(dd[0]),'valid':bool(ok[0]),'point':zz.tolist(),'success':bool(opt.success)})
            if ok[0] and dd[0]<found:found=float(dd[0]);arg=zz.tolist()
        faces.append({'face':i+1,'minimum_found':found,'ratio_to_2epsilon':found/.002,
                      'all_sampled_lifts_valid':bool(np.all(valid)),'point':arg,'optimizer_runs':results})
    return {'faces':faces,'min_ratio':min(v['ratio_to_2epsilon'] for v in faces),
      'max_normal':sec.max_normal,'normal_allowance':ah,'normal_usage':sec.max_normal/ah,
      'max_hidden_residual':sec.max_residual,'all_sampled_lifts_valid':all(v['all_sampled_lifts_valid'] for v in faces),
      'label':'Found minima UPPER-estimate true infima, NOT certified lower bounds'}
if __name__=='__main__':
    result8=json.loads((ROOT/'result8.json').read_text());assert result8['status']=='SUBSTANTIAL IMPROVEMENT'
    assert not (ROOT/'result9.json').exists();install();m=n.Model()
    d=json.loads((ROOT/'candidate.json').read_text());B8=np.array([[float(Q(v)) for v in row] for row in d['B']]);ch8=m.chart(B8)
    ch8['Q']=np.array([[float(Q(v)) for v in row] for row in d['L']])
    calibration=refined_proxy(m,ch8,np.array([float(Q(v)) for v in d['a']]),float(Q(d['ah'])))
    official=np.array([float(Q(v)) for v in result8['attempts'][-1]['beta']])
    # Numerical proof cap may make the official bound more conservative; do not force equality.
    discrepancy=float(max(abs(np.array(calibration['beta'])-official)))
    write('numerical8_calibration.json',{'result':calibration,'max_beta_discrepancy':discrepancy,
      'label':'ordinary float64 check only; no refined official result changed'})
    assert discrepancy<1e-9
    B9=np.load(SCREEN/'bases.npz')['query_svd'][:,:13];ch=m.chart(B9)
    out={'r':9,'epsilon':.001,'label':'NUMERICAL FEASIBILITY ONLY; NO 9D CERTIFICATE','winners':[],'status':'INCOMPLETE'}
    try:
        winners=[optimize(m,ch,s,t) for s,t in ((410901,1.0),(410902,1.5))]
        for winner in winners:
            v=winner['result'];v['actual']=attack(m,ch,v['a'],v['ah'],winner['seed']+1000)
            winner['assessment']='PROMISING NUMERICALLY' if v['valid'] and v['min_ratio']>=1.05 and v['actual']['min_ratio']>=1.05 and v['actual']['all_sampled_lifts_valid'] else 'NOT PROMISING IN SCREENED SECTION'
            out['winners'].append(winner);write('result9.json',out)
        out['status']='COMPLETE'
    except TimeoutError as e:out['status']='CPU LIMIT / PARTIAL';out['error']=str(e)
    finally:
        out.update(CPU_seconds=time.process_time()-CPU,wall_seconds=time.perf_counter()-WALL,
          peak_RAM_bytes=psutil.Process().memory_info().peak_wset,GPU_seconds=0)
        write('result9.json',out);print(out['status'],[(v['result']['min_ratio'],v['result']['actual']['min_ratio']) for v in out['winners']],flush=True)
