"""Bounded preregistered numerical selection; not interval certification."""
import os,sys,time
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import common as c
import math,traceback
from scipy.optimize import minimize
from concurrent.futures import ProcessPoolExecutor

class BudgetStop(Exception):pass

def worker(job):
    cpu=CPU; wall=WALL; c.verify()
    kind,seed=job; cid=f'{kind}_{seed}'
    cfg=c.json.loads((c.ROOT/'config.json').read_text()); chart=c.json.loads((c.ROOT/'bases.json').read_text())[kind]
    ep=c.Endpoint('independent_n4_confirmation')
    B=c.np.array([[float(c.Q(v)) for v in row] for row in chart['B']])
    L=c.np.array([[float(c.Q(v)) for v in row] for row in chart['L']]); sigma=c.np.array(chart['sigma'])
    prior=c.json.loads((c.OLD/'stage2_proxy/outputs/independent_n4_confirmation_query_r7_s2.json').read_text())
    rng=c.np.random.default_rng(seed)
    start=c.np.array(prior['a']) if kind=='top' else c.np.clip(1.4e-3/(ep.margins(L)*sigma),.001,1.)
    if seed==271072:start*=c.np.exp(rng.normal(0,.15,7))
    best={'score':-math.inf}; count=0; invalid=0
    path=c.ROOT/f'trace_{cid}.jsonl'
    assert not path.exists()
    trace=path.open('w',encoding='utf-8',newline='\n')
    def evaluate(th):
        nonlocal count,invalid,best
        if time.process_time()-cpu>=cfg['worker_cpu_limit']:raise BudgetStop()
        aa=c.np.exp(th[:7]); ah=math.exp(th[7]); count+=1
        reason=None; o={}; score=-1e9
        if max(aa)>4 or ah>4:reason='amplitude search guard'
        else:
            try:
                o=c.evaluate3(ep,B,L,aa,ah)
                if o['valid']:
                    score=float(min(o['beta3']))/1e-3
                    if not math.isfinite(score):raise FloatingPointError('nonfinite proxy score')
                    if score>best['score']:
                        best={'score':score,'a':aa.tolist(),'ah':ah,'beta3':o['beta3'].tolist(),
                              'M3':o['M3'].tolist(),'eta_h':o['eta_h'],'radius':o['radius'],
                              'kind':kind,'seed':seed,'id':cid,'eval':count}
                else:reason=o['reason']
            except (c.np.linalg.LinAlgError,FloatingPointError,OverflowError) as e:reason=repr(e)
        invalid+=int(reason is not None)
        trace.write(c.json.dumps({'eval':count,'score':score,'reason':reason,'a':aa.tolist(),'ah':ah,'cpu':time.process_time()-cpu})+'\n')
        if count%100==0:trace.flush(); print(cid,count,'best',best['score'],flush=True)
        return -score if reason is None else 100+float(o.get('eta_h',1))
    status='complete'
    try:
        choices=[]
        for ah in cfg['initial_hidden_grid']:
            th=c.np.r_[c.np.log(start),math.log(ah)]; val=evaluate(th)
            choices.append((val,ah,th))
        valid=[v for v in choices if v[0]<100]
        init=min(valid,key=lambda x:(x[0],x[1]))[2] if valid else choices[-1][2]
        minimize(evaluate,init,method='Nelder-Mead',options={'maxfev':cfg['maxfev'],'adaptive':True,'xatol':1e-3,'fatol':1e-8})
    except BudgetStop:status='preregistered CPU cap'
    except Exception:status='worker defect: '+traceback.format_exc()
    finally:trace.close()
    out={'job':cid,'status':status,'best':best,'evals':count,'invalid':invalid,
         'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-wall,
         'peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset}
    c.write(f'search_{cid}.json',out);return out

if __name__=='__main__':
    c.verify(); c.k.a.c.hardware()
    assert not (c.ROOT/'search_summary.json').exists()
    jobs=[(kind,seed) for kind in ('top','skip') for seed in (271071,271072)]
    with ProcessPoolExecutor(max_workers=2,max_tasks_per_child=1) as pool:results=list(pool.map(worker,jobs))
    c.write('search_summary.json',{'results':results,'parent_cpu_seconds':time.process_time()-CPU,
        'worker_cpu_seconds':sum(v['cpu_seconds'] for v in results),'wall_seconds':time.perf_counter()-WALL,
        'parent_peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset,'gpu_used':False})
    print('Selection search finished; no rigorous certificate executed',flush=True)
