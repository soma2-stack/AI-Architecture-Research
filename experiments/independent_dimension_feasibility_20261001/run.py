"""Budgeted numerical screen, with all results explicitly non-certified."""
import numerics as n
import hashlib,itertools,json,math,time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import psutil
from scipy.optimize import minimize
from scipy.stats import qmc
HERE=Path(__file__).resolve().parent
CFG=json.loads((HERE/'config.json').read_text(encoding='utf-8'))
CPU_START=time.process_time();WALL_START=time.perf_counter()
def write(path,data):
    (HERE/path).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def budget():
    if time.process_time()-CPU_START>CFG['cpu_limit_seconds']:raise TimeoutError('frozen cheap-screen CPU budget reached')
def measure():
    mem=psutil.Process().memory_info()
    return {'cpu_seconds':time.process_time()-CPU_START,'wall_seconds':time.perf_counter()-WALL_START,
            'peak_ram_bytes':getattr(mem,'peak_wset',mem.rss),'gpu_seconds':0,'device':'cpu','workers':1}
def score(res):
    if res['valid']:return 2/math.pi*math.atan(res['min_proxy_ratio'])
    violations=max(0,res['radius']-1)+max(0,res['eta_h']/.75-1)+min(100,max(0,res['inclusion_ratio']-1))
    return -2-violations
def evaluate(m,ch,a,ah):
    budget()
    try:return n.proxy(m,ch,a,ah)
    except (np.linalg.LinAlgError,FloatingPointError) as exc:
        return {'valid':False,'radius':100.,'eta_h':100.,'inclusion_ratio':100.,'a':a.tolist(),'ah':float(ah),'error':str(exc)}
def initial(m,ch,ratio):
    mu=(7/8)/(2*m.beta*np.linalg.norm(ch['Q']/m.rd[None,:],axis=1))
    a=np.clip(ratio*n.EPS/mu,1e-6,4.)
    rad=float((abs(ch['B'][:,4:]*n.SD)@a).max())
    a*=min(1,.4/max(rad,1e-20));a=np.maximum(a,1e-6)
    vals=[evaluate(m,ch,a,h) for h in CFG['initial_normal_grid']]
    best=max(vals,key=score)
    return np.log(np.r_[a,best['ah']]),best
def optimize(m,ch,r,base,seed,ratio):
    rng=np.random.default_rng(seed+r*1000+(0 if base=='query_svd' else 100000))
    x,best=initial(m,ch,ratio);cur=best;calls=7
    trace=HERE/f'trace_{r}_{base}_{seed}.jsonl'
    with trace.open('w',encoding='utf-8') as out:
        def ev(v,kind,step):
            nonlocal calls
            a=np.exp(v[:-1]);ah=np.exp(v[-1]);res=evaluate(m,ch,a,ah);calls+=1
            out.write(json.dumps({'step':step,'kind':kind,'score':score(res),'result':res},allow_nan=False)+'\n')
            return res
        bounds_lo=np.log(np.full(r+1,1e-6));bounds_hi=np.log(np.r_[np.full(r,4),1])
        for step in range(CFG['spsa_steps']):
            c=CFG['spsa_perturbation']/(1+step/50)**.101
            lr=CFG['spsa_learning_rate']/(1+step/40)**.602
            sign=rng.choice([-1.,1.],r+1)
            plus=ev(np.clip(x+c*sign,bounds_lo,bounds_hi),'plus',step)
            minus=ev(np.clip(x-c*sign,bounds_lo,bounds_hi),'minus',step)
            grad=(score(plus)-score(minus))/(2*c)*sign
            trial=np.clip(x+lr*np.clip(grad,-10,10),bounds_lo,bounds_hi)
            prop=ev(trial,'proposal',step)
            if score(prop)>=score(cur):x=trial;cur=prop
            for z in (plus,minus,prop):
                if score(z)>score(best):best=z
    best={'source':'optimized_proxy','seed':seed,'calls':calls,'score':score(best),'result':best}
    write(f'optimization_{r}_{base}_{seed}.json',best)
    return best

def quick_faces(sec,r,count=8):
    vals=[];ok=True;normal=0.;arg=[]
    for i in range(r):
        u=qmc.Sobol(r-1,scramble=True,seed=405000+r*100+i).random_base2(int(math.log2(count)))*2-1
        zz=np.insert(np.vstack((np.zeros(r-1),u)),i,1,axis=1)
        d,v,y=sec.pairs(zz)
        j=int(np.argmin(d));vals.append(float(d[j]));arg.append(zz[j].tolist());ok &=bool(np.all(v));normal=max(normal,float(abs(y).max()))
    return {'min_ratio':min(vals)/.002,'all_numerical_lifts_valid':ok,'face_minima':vals,'max_normal':normal,'worst_points':arg}
def direct_allocations(m,ch,r,base):
    mu=(1-np.tanh(.25)**2)/(2*m.beta*np.linalg.norm(ch['Q']/m.rd[None,:],axis=1))
    aa=np.clip(n.EPS/mu,1e-6,4.)
    records=[]
    for scale in CFG['direct_scales']:
        a=np.clip(aa*scale,1e-6,4);rad=float((abs(ch['B'][:,4:]*n.SD)@a).max())
        a*=min(1,.65/max(rad,1e-20));ah=1.
        sec=n.Section(m,ch['B'],a,ah);geom=quick_faces(sec,r)
        proxies=[evaluate(m,ch,a,h) for h in CFG['initial_normal_grid']]
        bestproxy=max(proxies,key=score)
        records.append({'source':'balanced_direct','scale':scale,'a':a.tolist(),'ah':ah,'quick_geometry':geom,
                        'best_normal_grid_proxy':bestproxy})
    best=max(records,key=lambda z:z['quick_geometry']['min_ratio'] if z['quick_geometry']['all_numerical_lifts_valid'] else -10-z['quick_geometry']['max_normal'])
    write(f'direct_allocations_{r}_{base}.json',{'candidates':records,'selected_scale':best['scale']})
    return best

def full_faces(m,ch,a,ah,r,base,style):
    sec=n.Section(m,ch['B'],np.asarray(a),ah);faces=[];rng=np.random.default_rng(406000+r)
    for i in range(r):
        budget()
        if r<=8:
            corners=np.array(list(itertools.product((-1.,1.),repeat=r-1)))
        else:corners=rng.choice([-1.,1.],(CFG['face_random_corners'],r-1))
        sobol=qmc.Sobol(r-1,scramble=True,seed=407000+r*100+i).random_base2(5)*2-1
        u=np.vstack((np.zeros(r-1),corners,sobol));zz=np.insert(u,i,1.,axis=1)
        d,valid,y=sec.pairs(zz);sample_invalid=int((~valid).sum());normal_max=float(abs(y).max())
        order=np.argsort(np.where(valid,d,np.inf),kind='stable')
        starts=[np.zeros(r-1)]+[u[j] for j in order[:2]]
        rr=[];allvalid=bool(np.all(valid));minvalue=float(np.min(d));arg=zz[int(np.argmin(d))].tolist()
        def fg(v):
            budget();z=np.insert(v,i,1.)
            dist,vv,yy,grad=sec.pairs(z,jac=True)
            if not vv[0]:return 100+float(abs(yy).max()),np.zeros(r-1)
            return float(dist[0]),np.delete(grad[0],i)
        for start in starts:
            opt=minimize(fg,start,jac=True,method='L-BFGS-B',bounds=[(-1,1)]*(r-1),
                options={'maxiter':CFG['face_maxiter_large'] if r>=16 else CFG['face_maxiter_small'],
                         'ftol':1e-14,'gtol':1e-9})
            z=np.insert(opt.x,i,1.);dv,vv,yy=sec.pairs(z)
            allvalid &=bool(vv[0]);normal_max=max(normal_max,float(abs(yy).max()))
            if vv[0] and dv[0]<minvalue:minvalue=float(dv[0]);arg=z.tolist()
            rr.append({'distance':float(dv[0]),'fixed_h_valid':bool(vv[0]),'success':bool(opt.success),
                       'status':str(opt.message),'evaluations':int(opt.nfev),'z':z.tolist()})
        faces.append({'face':i+1,'minimum_found':minvalue,'ratio':minvalue/.002,'argmin':arg,
                      'sample_invalid_lifts':sample_invalid,'all_numerical_lifts_valid':allvalid,
                      'normal_usage_max':normal_max/ah,'runs':rr})
        if i%4==0:print(f'  r{r} {base}/{style} face{i+1}/{r}; CPU {time.process_time()-CPU_START:.1f}s',flush=True)
    ratio=min(v['ratio'] for v in faces);allvalid=all(v['all_numerical_lifts_valid'] for v in faces)
    result={'dimension':r,'basis':base,'style':style,'a':list(a),'ah':float(ah),'faces':faces,
            'weakest_face':min(faces,key=lambda z:z['ratio'])['face'],'minimum_found_ratio':ratio,
            'minimum_found_separation':ratio*.002,'all_numerical_lifts_valid':allvalid,
            'max_normal_usage':sec.max_normal/ah,'max_hidden_residual':sec.max_residual,
            'point_evaluations':sec.calls,'label':'NUMERICAL; found minimum is not a certified lower bound'}
    write(f'faces_{r}_{base}_{style}.json',result)
    return result

def dimension(m,bases,r):
    print(f'Start dimension {r}',flush=True);cases=[]
    for base in CFG['bases']:
        B=bases[base][:,:4+r];ch=m.chart(B)
        winners=[optimize(m,ch,r,base,seed,ratio) for seed,ratio in zip(CFG['seeds'],CFG['balanced_start_ratios'])]
        win=max(winners,key=lambda v:v['score']);pr=win['result']
        direct=direct_allocations(m,ch,r,base)
        for style,a,ah,pp in [('proxy',pr['a'],pr['ah'],pr),('direct',direct['a'],direct['ah'],direct['best_normal_grid_proxy'])]:
            geom=full_faces(m,ch,a,ah,r,base,style)
            geom['third_order_proxy']=pp
            geom['weighted_singular_values']=ch['sv'].tolist()
            geom['numerical_tangent_condition']=float(ch['sv'][0]/ch['sv'][-1])
            geom['certification_plausibility']=('FLOAT64 THIRD-ORDER PROXY PROMISING' if pp.get('valid') and pp['min_proxy_ratio']>1.05 and geom['all_numerical_lifts_valid'] and geom['minimum_found_ratio']>1.05 else
                'ACTUAL SAMPLES PROMISING; REVIEWED PROXY DOES NOT PASS' if geom['all_numerical_lifts_valid'] and geom['minimum_found_ratio']>1.05 else 'NOT PROMISING IN THIS SCREEN')
            if not geom['all_numerical_lifts_valid']:bottleneck='sampled hidden-section inclusion'
            elif geom['minimum_found_ratio']<1:bottleneck='actual numerical query separation below threshold'
            elif not pp.get('valid'):bottleneck='numerical hidden/domain majorant guards'
            elif pp['min_proxy_ratio']<1:bottleneck='third-order/query-margin proxy'
            else:bottleneck='no tested bottleneck at epsilon'
            geom['bottleneck']=bottleneck;cases.append(geom)
            write(f'faces_{r}_{base}_{style}.json',geom)
    promising=[x for x in cases if x['all_numerical_lifts_valid'] and x['minimum_found_ratio']>=1.05]
    passing=[x for x in cases if x['all_numerical_lifts_valid'] and x['minimum_found_ratio']>=1]
    status='PROMISING NUMERICALLY' if promising else 'MARGINAL' if passing else 'SCREENED SECTIONS FAIL'
    best=max(cases,key=lambda z:z['minimum_found_ratio'] if z['all_numerical_lifts_valid'] else -10-z['max_normal_usage'])
    result={'dimension':r,'status':status,'best_case':{'basis':best['basis'],'style':best['style'],
        'ratio':best['minimum_found_ratio'],'separation':best['minimum_found_separation'],
        'hidden_usage':best['max_normal_usage'],'proxy':best['third_order_proxy'],'bottleneck':best['bottleneck'],
        'certification_plausibility':best['certification_plausibility']},'cases':cases}
    write(f'dimension_{r}.json',result)
    print(f'Finished r{r}: {status}; best actual ratio {best["minimum_found_ratio"]:.6g}; CPU {time.process_time()-CPU_START:.1f}s',flush=True)
    return result

def main():
    frozen=json.loads((HERE/'METHOD_FROZEN.json').read_text(encoding='utf-8'))
    assert all(hashlib.sha256((HERE/k).read_bytes()).hexdigest()==v for k,v in frozen['method_hashes'].items())
    m=n.Model();basis=np.load(HERE/'bases.npz');bases={k:basis[k] for k in CFG['bases']}
    results=[];failure=None
    try:
        for r in CFG['dimensions']:results.append(dimension(m,bases,r));write('progress.json',{'dimensions':results,'resources':measure()})
        positives=[x['dimension'] for x in results if x['status']=='PROMISING NUMERICALLY']
        negatives=[x['dimension'] for x in results if x['status']=='SCREENED SECTIONS FAIL']
        if positives:
            lo=max(positives);upper=[x for x in negatives if x>lo]
            if upper:
                hi=min(upper)
                for _ in range(CFG['max_binary_refinements']):
                    if hi-lo<=1:break
                    mid=(lo+hi)//2;v=dimension(m,bases,mid);results.append(v)
                    if v['status']=='PROMISING NUMERICALLY':lo=mid
                    elif v['status']=='SCREENED SECTIONS FAIL':hi=mid
                    else:break
                    write('progress.json',{'dimensions':results,'resources':measure()})
    except TimeoutError as exc:failure=str(exc)
    final={'status':'NUMERICAL DIAGNOSTIC ONLY','dimensions':results,'failure':failure,'resources':measure()}
    write('results.json',final);print(json.dumps({'resource_summary':final['resources'],'failure':failure}),flush=True)
if __name__=='__main__':main()
