import sys,time
sys.dont_write_bytecode=True
CPU=time.process_time();WALL=time.perf_counter()
import common as c
import math,traceback
from concurrent.futures import ProcessPoolExecutor
from scipy.optimize import minimize
class BudgetStop(Exception):pass
def worker(job):
    cpu=CPU;wall=WALL;c.verify();kind,seed=job;cid=f'{kind}_{seed}'
    cfg=c.json.loads((c.ROOT/'config.json').read_text());chart=c.json.loads((c.ROOT/'bases.json').read_text())[kind]
    ep=c.Endpoint('independent_n4_confirmation')
    B=c.np.array([[float(c.Q(v)) for v in row] for row in chart['B']]);L=c.np.array([[float(c.Q(v)) for v in row] for row in chart['L']])
    old=c.json.loads((c.CONTROL/'candidate.json').read_text());start=c.np.array([float(c.Q(v)) for v in old['a']]);start[1]*=1.15
    if seed==302702:start*=c.np.exp(c.np.random.default_rng(seed).normal(0,.15,7))
    best={'score':-math.inf};count=0;invalid=0
    path=c.ROOT/f'trace_{cid}.jsonl';assert not path.exists();trace=path.open('w',encoding='utf-8',newline='\n')
    def evaluate(th):
        nonlocal best,count,invalid
        if time.process_time()-cpu>=cfg['worker_cpu_limit']:raise BudgetStop()
        raw=c.np.exp(th[:7]);rawh=math.exp(th[7]);count+=1;reason=None;out={};score=-1e9
        qa,qh=c.round_widths(raw,rawh);aa=c.np.array(list(map(float,qa)));ah=float(qh)
        if max(raw)>4 or rawh>4 or not all(v>0 for v in qa):reason='amplitude guard'
        else:
            try:
                out=c.proxy.evaluate3(ep,B,L,aa,ah)
                if out['valid']:
                    score=float(min(out['beta3']))/1e-3
                    if not math.isfinite(score):raise FloatingPointError('nonfinite score')
                    if score>best['score']:
                        best={'id':cid,'kind':kind,'seed':seed,'eval':count,'score':score,
                            'a':list(map(str,qa)),'ah':str(qh),'raw_a':raw.tolist(),'raw_ah':rawh,
                            'beta3':out['beta3'].tolist(),'M3':out['M3'].tolist(),
                            'eta_h':out['eta_h'],'radius':out['radius']}
                else:reason=out['reason']
            except (c.np.linalg.LinAlgError,FloatingPointError,OverflowError) as e:reason=repr(e)
        invalid+=int(reason is not None)
        trace.write(c.json.dumps({'eval':count,'score':score,'reason':reason,'a':list(map(str,qa)),'ah':str(qh),'cpu':time.process_time()-cpu})+'\n')
        if count%100==0:trace.flush();print(cid,count,'best',best['score'],flush=True)
        return -score if reason is None else 100+float(out.get('eta_h',1))
    status='complete'
    try:
        choices=[]
        for ah in cfg['normal_grid']:
            th=c.np.r_[c.np.log(start),math.log(ah)];value=evaluate(th);choices.append((value,ah,th))
        valid=[v for v in choices if v[0]<100];init=min(valid,key=lambda v:(v[0],v[1]))[2] if valid else choices[-1][2]
        minimize(evaluate,init,method='Nelder-Mead',options={'adaptive':True,'maxfev':cfg['maxfev'],'xatol':1e-3,'fatol':1e-8})
    except BudgetStop:status='preregistered worker CPU cap'
    except Exception:status='worker defect: '+traceback.format_exc()
    finally:trace.close()
    ans={'job':cid,'status':status,'best':best,'evals':count,'invalid':invalid,
        'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-wall,
        'peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset}
    c.write(f'search_{cid}.json',ans);return ans
if __name__=='__main__':
    c.verify();c.k.a.c.hardware();assert not (c.ROOT/'search_summary.json').exists()
    jobs=[(kind,seed) for kind in ('original','plus','minus') for seed in (302701,302702)]
    with ProcessPoolExecutor(max_workers=2,max_tasks_per_child=1) as pool:res=list(pool.map(worker,jobs))
    c.write('search_summary.json',{'results':res,'worker_cpu_seconds':sum(x['cpu_seconds'] for x in res),
        'parent_cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
        'parent_peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset,'gpu_used':False})
    print('Numerical selection complete; no official certificate executed')
