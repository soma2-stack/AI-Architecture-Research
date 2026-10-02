"""Resume after a JSON serialization defect; frozen numerical code unchanged."""
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('frozen_runner',ROOT/'run.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)


def write_json(path,obj):
    # NumPy comparisons return np.bool_, which standard json cannot serialize.
    path.write_text(json.dumps(obj,indent=2,allow_nan=False,
                    default=lambda value:value.item())+'\n',encoding='utf-8')


def main():
    manifest=json.loads((ROOT/'FROZEN.json').read_text())
    for name,value in manifest['inputs'].items():
        if r.sha(r.REPO/name)!=value:
            raise RuntimeError('Frozen source changed '+name)
    r.save_json=write_json
    outdir=ROOT/'results'
    prior=json.loads((outdir/'summary.json').read_text())
    rows=prior['rows'];finite=prior['finite'];resources=r.Resources()
    resources.cpu-=prior['resources']['cpu_seconds']
    resources.wall-=prior['resources']['wall_seconds']
    resources.peak=max(resources.peak,prior['resources']['peak_rss_bytes'])
    status='RUNNING'
    try:
        for n in r.CFG['widths']:
            F=r.family(n);bases=[];width_rows=[]
            existing={row['case']:row for row in rows}
            for strategy in r.CFG['strategies']:
                for seed in r.CFG['seeds']:
                    resources.check();case=f'n{n}_{strategy}_{seed}'
                    if case in existing:
                        info=existing[case];B=r.np.load(outdir/f'{case}.npz')['B']
                    else:
                        hs,sh=r.generate(F,strategy,seed)
                        info,B=r.spectrum(F,hs,case,outdir,resources)
                        info.update(strategy=strategy,seed=seed,generator_shrink=sh)
                        rows.append(info)
                    width_rows.append(info);bases.append(B)
                    write_json(outdir/'summary.json',dict(status=status,rows=rows,finite=finite,resources=resources.snapshot()))
            case=f'n{n}_novelty'
            if case in existing:
                info=existing[case]
            else:
                hs,traces=r.novelty(F,bases,resources)
                write_json(outdir/f'novelty_n{n}.json',traces)
                info,B=r.spectrum(F,hs,case,outdir,resources)
                info.update(strategy='novelty',seed=r.CFG['novelty_seed']);rows.append(info)
            width_rows.append(info)
            if not any(x['n']==n for x in finite):
                selected=sorted(width_rows,key=lambda x:(-x['lower_tangent_count'],-x['ranking_score'],x['case']))[0]
                selection=outdir/f'finite_selection_n{n}.json'
                if not selection.exists():
                    write_json(selection,dict(selected=selected['case'],history_sha256=selected['history_sha256'],rule='lower count, log score, lexical'))
                elif json.loads(selection.read_text())['selected']!=selected['case']:
                    raise RuntimeError('Finite selection changed')
                finite.append(r.finite_check(F,selected,outdir,resources))
            write_json(outdir/'summary.json',dict(status=status,rows=rows,finite=finite,resources=resources.snapshot()))
        status='COMPLETE'
    except Exception as exc:
        status='STOPPED';write_json(outdir/'resume_stop.json',dict(error=repr(exc),resources=resources.snapshot()))
        raise
    finally:
        write_json(outdir/'summary.json',dict(status=status,rows=rows,finite=finite,resources=resources.snapshot()))
        resources.done.set()


if __name__=='__main__':
    main()
