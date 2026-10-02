"""Prospectively frozen broader admissible-gate diagnostic."""
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('base',ROOT/'run.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)


def save_json(path,obj):
    path.write_text(json.dumps(obj,indent=2,allow_nan=False,default=lambda x:x.item())+'\n',encoding='utf-8')


def generate(F,pattern,seed):
    rng=r.np.random.default_rng(r.np.random.SeedSequence([seed,F['n'],['driven_random','driven_coherent'].index(pattern)]))
    hs=r.np.zeros((F['H']+2,F['n']))
    hs[1:-1,F['k']:]=F['Hsrc']
    profile=rng.uniform(.1,.35,F['r'])
    cooling=0
    for t in range(1,F['H']+1):
        pre=(F['R']@hs[t-1]+.05)[F['idx']]
        if t>F['H']-8:
            if r.np.max(r.np.abs(pre))<=.48:
                hs[t,F['idx']]=0
                continue
            u=-.45*r.np.sign(pre);cooling+=1
        elif pattern=='driven_random':
            u=rng.uniform(-.4,.4,F['r'])
        else:
            u=profile*rng.uniform(.5,1)+rng.uniform(-.025,.025,F['r'])
        hs[t,F['idx']]=r.np.tanh(pre+u)
    if not r.admissible(F,hs):
        raise RuntimeError('Input-driven generator inadmissible: no replacement')
    return hs,cooling


def main():
    frozen=json.loads((ROOT/'SUPPLEMENT_FROZEN.json').read_text())
    for name,digest in frozen['inputs'].items():
        if r.sha(r.REPO/name)!=digest:
            raise RuntimeError('Supplement source changed')
    r.save_json=save_json
    outdir=ROOT/'supplement_results';outdir.mkdir(exist_ok=False)
    primary=json.loads((ROOT/'results/summary.json').read_text())
    res=r.Resources();res.cpu-=primary['resources']['cpu_seconds'];res.wall-=primary['resources']['wall_seconds']
    res.peak=max(res.peak,primary['resources']['peak_rss_bytes'])
    rows=[];finite=[];status='RUNNING'
    try:
        for n in (32,64,96):
            F=r.family(n);width_rows=[]
            for pattern in ('driven_random','driven_coherent'):
                for seed in (86101,86102):
                    res.check();hs,cooling=generate(F,pattern,seed)
                    case=f'n{n}_{pattern}_{seed}'
                    info,B=r.spectrum(F,hs,case,outdir,res)
                    info.update(strategy=pattern,seed=seed,cooling_steps=cooling,
                                max_abs_memory_h=float(r.np.max(r.np.abs(hs[:,F['idx']]))))
                    rows.append(info);width_rows.append(info)
                    save_json(outdir/'summary.json',dict(status=status,rows=rows,finite=finite,resources=res.snapshot()))
            selected=sorted(width_rows,key=lambda x:(-x['lower_tangent_count'],-x['ranking_score'],x['case']))[0]
            save_json(outdir/f'finite_selection_n{n}.json',dict(selected=selected['case'],history_sha256=selected['history_sha256']))
            finite.append(r.finite_check(F,selected,outdir,res))
        status='COMPLETE'
    except Exception as exc:
        status='STOPPED';save_json(outdir/'stop.json',dict(error=repr(exc),resources=res.snapshot()))
        raise
    finally:
        save_json(outdir/'summary.json',dict(status=status,rows=rows,finite=finite,resources=res.snapshot()))
        res.done.set()


if __name__=='__main__':
    main()
