"""Separate post-primary numerical refinement; no primary artifact mutations."""
import run as primary
import numerics as n
import json,hashlib,math,time,itertools
from pathlib import Path
import numpy as np
from scipy.stats import qmc
from scipy.optimize import minimize
import psutil
HERE=Path(__file__).resolve().parent
START=time.process_time();WALL=time.perf_counter()
PR=json.loads((HERE/'results.json').read_text(encoding='utf-8'))
AH=.125
def write(name,data):primary.write(name,data)
def budget():
    if time.process_time()-START+PR['resources']['cpu_seconds']>880:raise TimeoutError('combined numerical budget')
def points(r,base,seed):
    pool=[]
    old=HERE/f'faces_{r}_{base}_direct.json'
    saved=json.loads(old.read_text(encoding='utf-8')) if old.exists() else None
    rng=np.random.default_rng(seed+r)
    for i in range(r):
        u=qmc.Sobol(r-1,scramble=True,seed=409000+r*100+i).random_base2(3)*2-1
        corners=rng.choice([-1.,1.],(8,r-1));u=np.vstack((np.zeros(r-1),u,corners))
        z=np.insert(u,i,1.,axis=1);pool.extend(z)
        if saved:pool.append(saved['faces'][i]['argmin'])
    return np.array(pool)
def project(m,ch,a):
    normal=abs(ch['B'][:,:4]*n.SD).sum(1)*AH
    tangent=abs(ch['B'][:,4:]*n.SD)@a
    scaling=np.min((.95-normal)/np.maximum(tangent,1e-30))
    return np.clip(a*min(1,float(scaling)),1e-6,4)
def allocation(m,ch,r,base,seed,pool):
    prev=HERE/f'faces_{r}_{base}_direct.json'
    if prev.exists():a=np.array(json.loads(prev.read_text(encoding='utf-8'))['a'])
    else:
        mu=(1-np.tanh(.25)**2)/(2*m.beta*np.linalg.norm(ch['Q']/m.rd[None,:],axis=1))
        a=np.clip(n.EPS/mu,1e-6,4)
        a*=min(1,.65/float((abs(ch['B'][:,4:]*n.SD)@a).max()))
    if seed==408002:a*=1.1
    a=project(m,ch,a);x=np.log(a);rng=np.random.default_rng(seed+r*100)
    trace=(HERE/f'refine_trace_{r}_{base}_{seed}.jsonl').open('w',encoding='utf-8')
    calls=0
    def ev(x,step,kind):
        nonlocal calls
        budget();aa=project(m,ch,np.clip(np.exp(x),1e-6,4))
        sec=n.Section(m,ch['B'],aa,AH);d,valid,y=sec.pairs(pool)
        ratio=float(d.min()/.002);usage=float(abs(y).max()/AH)
        value=2/math.pi*math.atan(ratio)-10*max(0,usage-1)
        trace.write(json.dumps({'step':step,'kind':kind,'a':aa.tolist(),'min_ratio':ratio,
                                'normal_usage':usage,'all_lifts_valid':bool(np.all(valid)),'score':value})+'\n')
        calls+=1;return value,aa,ratio,usage
    cur=ev(x,-1,'initial');best=cur
    for step in range(400):
        c=.08/(1+step/50)**.101;lr=.12/(1+step/40)**.602;sign=rng.choice([-1.,1.],r)
        plus=ev(x+c*sign,step,'plus');minus=ev(x-c*sign,step,'minus')
        g=(plus[0]-minus[0])/(2*c)*sign
        proposal=ev(np.clip(x+lr*np.clip(g,-10,10),np.log(1e-6),np.log(4)),step,'proposal')
        if proposal[0]>=cur[0]:cur=proposal;x=np.log(cur[1])
        for cand in (plus,minus,proposal):
            if cand[0]>best[0]:best=cand
    trace.close()
    result={'dimension':r,'basis':base,'seed':seed,'score':best[0],'a':best[1].tolist(),'ah':AH,
            'training_pool_min_ratio':best[2],'normal_usage':best[3],'calls':calls}
    write(f'refine_optimization_{r}_{base}_{seed}.json',result);return result

def fresh_validation(m,ch,a,r,base):
    sec=n.Section(m,ch['B'],np.array(a),AH);records=[]
    for i in range(r):
        budget();rng=np.random.default_rng(410000+r*100+i)
        sobol=qmc.Sobol(r-1,scramble=True,seed=411000+r*100+i).random_base2(5)*2-1
        u=np.vstack((np.zeros(r-1),sobol,rng.choice([-1.,1.],(32,r-1))))
        z=np.insert(u,i,1.,axis=1);d,v,y=sec.pairs(z);ix=int(np.argmin(d))
        weakest=float(d[ix]);worst=z[ix];valid=bool(np.all(v));runs=[]
        def fg(u):
            zz=np.insert(u,i,1.);dd,vv,yy,g=sec.pairs(zz,jac=True)
            if not vv[0]:return 100+float(abs(yy).max()),np.zeros(r-1)
            return float(dd[0]),np.delete(g[0],i)
        starts=[np.zeros(r-1)]+[u[j] for j in np.argsort(d)[:2]]
        for start in starts:
            opt=minimize(fg,start,jac=True,method='L-BFGS-B',bounds=[(-1,1)]*(r-1),options={'maxiter':50,'ftol':1e-14,'gtol':1e-9})
            zz=np.insert(opt.x,i,1.);dd,vv,yy=sec.pairs(zz);valid &=bool(vv[0])
            if vv[0] and dd[0]<weakest:weakest=float(dd[0]);worst=zz
            runs.append({'distance':float(dd[0]),'valid':bool(vv[0]),'success':bool(opt.success),'z':zz.tolist()})
        records.append({'face':i+1,'minimum_found':weakest,'ratio':weakest/.002,'argmin':worst.tolist(),
                        'all_lifts_valid':valid,'runs':runs})
    ratio=min(x['ratio'] for x in records);valid=all(x['all_lifts_valid'] for x in records)
    return {'fresh_faces':records,'fresh_min_ratio':ratio,'fresh_all_lifts_valid':valid,
            'fresh_normal_usage':sec.max_normal/AH,'hidden_residual_max':sec.max_residual,'point_evaluations':sec.calls}

def dimension(m,bases,r):
    print(f'Direct amplitude refinement r{r}',flush=True);candidates=[]
    for base in ('query_svd','extend7'):
        ch=m.chart(bases[base][:,:4+r]);pool=points(r,base,408000)
        np.savez_compressed(HERE/f'refine_pool_{r}_{base}.npz',z=pool)
        fits=[allocation(m,ch,r,base,seed,pool) for seed in (408001,408002)]
        best=max(fits,key=lambda x:x['score'])
        # Freeze amplitudes before adversarial verification, with no feedback loop.
        write(f'REFINE_WINNER_{r}_{base}.json',{'candidate':best,'pool_sha256':hashlib.sha256((HERE/f'refine_pool_{r}_{base}.npz').read_bytes()).hexdigest(),
                'validation_status':'Not yet inspected'})
        geom=primary.full_faces(m,ch,best['a'],AH,r,base,'refinement')
        fresh=fresh_validation(m,ch,best['a'],r,base);best.update(fresh)
        best['validation']=geom
        best['all_validation_lifts_valid']=geom['all_numerical_lifts_valid'] and fresh['fresh_all_lifts_valid']
        best['validated_min_ratio']=min(geom['minimum_found_ratio'],fresh['fresh_min_ratio'])
        best['proxy']=n.proxy(m,ch,np.array(best['a']),AH)
        candidates.append(best)
        write(f'refined_faces_{r}_{base}.json',best)
        print(f'  {base}: search {best["training_pool_min_ratio"]:.5f}; fresh {best["validated_min_ratio"]:.5f}',flush=True)
    usable=[x for x in candidates if x['all_validation_lifts_valid']]
    best=max(usable or candidates,key=lambda x:x['validated_min_ratio'])
    status='PROMISING NUMERICALLY' if best['all_validation_lifts_valid'] and best['validated_min_ratio']>=1.05 else 'MARGINAL' if best['all_validation_lifts_valid'] and best['validated_min_ratio']>=1 else 'SCREENED SECTIONS FAIL'
    result={'dimension':r,'status':status,'best_basis':best['basis'],'best_ratio':best['validated_min_ratio'],'candidates':candidates}
    write(f'refined_dimension_{r}.json',result);return result
def main():
    freeze=json.loads((HERE/'SECONDARY_FROZEN.json').read_text(encoding='utf-8'))
    assert all(hashlib.sha256((HERE/k).read_bytes()).hexdigest()==v for k,v in freeze['source_hashes'].items())
    assert all(hashlib.sha256((HERE/k).read_bytes()).hexdigest()==v for k,v in freeze['primary_output_hashes'].items())
    m=n.Model();b=np.load(HERE/'bases.npz');bases={k:b[k] for k in b.files};res=[];failure=None
    try:
        res.append(dimension(m,bases,11));res.append(dimension(m,bases,12))
        if res[-1]['status']=='PROMISING NUMERICALLY':
            mid=dimension(m,bases,14);res.append(mid)
            res.append(dimension(m,bases,15 if mid['status']=='PROMISING NUMERICALLY' else 13))
    except TimeoutError as exc:failure=str(exc)
    mem=psutil.Process().memory_info()
    write('refinement_results.json',{'status':'SECONDARY NUMERICAL DIAGNOSTIC ONLY','dimensions':res,'failure':failure,
          'resources':{'cpu_seconds':time.process_time()-START,'wall_seconds':time.perf_counter()-WALL,
                       'peak_ram_bytes':getattr(mem,'peak_wset',mem.rss),'gpu_seconds':0}})
    print(json.dumps({'dimensions':[(x['dimension'],x['status'],x['best_ratio']) for x in res],'cpu_seconds':time.process_time()-START}),flush=True)
if __name__=='__main__':main()
