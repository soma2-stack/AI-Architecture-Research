"""Descriptive summaries and compact archival of existing measurements only."""
import hashlib
import json
import math
import shutil
import time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent


def main():
    cpu=time.process_time();wall=time.perf_counter()
    data=json.loads((ROOT/'results/summary.json').read_text())
    archive=ROOT/'archive';archive.mkdir(exist_ok=False)
    selections={x['selected_case'] for x in data['finite']}
    raw_manifest={}
    for path in sorted((ROOT/'results').glob('*.npz')):
        raw_manifest[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
        if path.stem in selections or path.stem.startswith('finite_queries'):
            shutil.copyfile(path,archive/path.name)
        else:
            z=np.load(path)
            np.savez_compressed(archive/path.name,**{key:z[key] for key in ('hs','xs','B','lower_spectrum','upper_spectrum')})
    (archive/'RAW_BANK_MANIFEST.json').write_text(json.dumps(raw_manifest,indent=2)+'\n',encoding='utf-8')
    for name in ('execution.log','resume_execution.log','crosscheck_execution.log','crosscheck_execution_v2.log'):
        shutil.copyfile(ROOT/name,archive/(name+'.txt'))
    best=[];spectra=[];strategies=[]
    for n in sorted({x['n'] for x in data['rows']}):
        rows=[x for x in data['rows'] if x['n']==n]
        chosen=sorted(rows,key=lambda x:(-x['lower_tangent_count'],-x['ranking_score'],x['case']))[0]
        best.append(chosen)
        for pattern in ('random','sparse','dense','novelty'):
            subset=[x for x in rows if x['strategy']==pattern]
            strategies.append(dict(n=n,strategy=pattern,
                  lower_counts=[x['lower_tangent_count'] for x in subset],
                  upper_counts=[x['upper_envelope_count'] for x in subset],
                  mean_gate_damage=[x['mean_gate_damage'] for x in subset]))
        z=np.load(archive/(chosen['case']+'.npz'))
        s=z['lower_spectrum'];u=z['upper_spectrum']
        positions=sorted(set([1,n//2,n,n*2,chosen['lower_tangent_count'],len(s)]))
        spectra.append(dict(n=n,case=chosen['case'],points=[dict(index=i,box_lower=float(s[i-1]),all_query_envelope=float(u[i-1])) for i in positions if i<=len(s)],
                            min_positive=float(s[s>0].min()),number_of_modes=len(s)))
    ns=np.array([x['n'] for x in best],dtype=float)
    counts=np.array([x['lower_tangent_count'] for x in best],dtype=float)
    def fits(ns,y):
        result=[]
        for label,f in [('n',ns),('n log n',ns*np.log(ns)),('n^1.5',ns**1.5),('n^2',ns**2)]:
            coeff=float(f@y/(f@f));pred=coeff*f
            result.append(dict(law=label,coefficient=coeff,rmse=float(np.sqrt(np.mean((y-pred)**2)))))
        return result
    fit=fits(ns,counts)
    finite_fits=fits(ns,np.array([x['radii'][0]['passing_axes'] for x in data['finite']],float))
    payload=dict(best=best,strategies=strategies,spectra=spectra,all_width_tangent_fits=fit,
                 finite_radius005_axis_fits=finite_fits,
                 loglog_exponent_all=float(np.polyfit(np.log(ns),np.log(counts),1)[0]),
                 loglog_exponent_largest_three=float(np.polyfit(np.log(ns[1:]),np.log(counts[1:]),1)[0]),
                 finite=data['finite'],cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall)
    (ROOT/'analysis.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    lines=['# Machine-generated descriptive tables','',
           'Counts below are tangent diagnostics, not certified continuous dimensions.','',
           '| n | H / T | Strongest box-lower count | count/n | count/(n ln n) | upper-envelope count | finite .05 passing axes |',
           '|---|---|---:|---:|---:|---:|---:|']
    for row,fin in zip(best,data['finite']):
        lines.append(f"| {row['n']} | {row['H']} / {row['T']} | {row['lower_tangent_count']} | {row['count_over_n']:.4f} | {row['count_over_nlogn']:.4f} | {row['upper_envelope_count']} | {fin['radii'][0]['passing_axes']} |")
    lines+=['','## Pattern counts','', '| n | Pattern | Lower counts | Envelope counts |','|---|---|---|---|']
    for x in strategies:
        lines.append(f"| {x['n']} | {x['strategy']} | {x['lower_counts']} | {x['upper_counts']} |")
    lines+=['','## Through-origin scaling fits','', '| Law | Tangent RMSE | Finite .05 axis RMSE |','|---|---:|---:|']
    for f,g in zip(fit,finite_fits):
        lines.append(f"| {f['law']} | {f['rmse']:.4f} | {g['rmse']:.4f} |")
    lines+=['','## Full spectral landmark values','', '| n | mode index | Box lower | All-query envelope |','|---|---:|---:|---:|']
    for x in spectra:
        for p in x['points']:
            lines.append(f"| {x['n']} | {p['index']} | {p['box_lower']:.9g} | {p['all_query_envelope']:.9g} |")
    (ROOT/'TABLES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,axes=plt.subplots(2,2,figsize=(10,7))
        for ax,row in zip(axes.ravel(),best):
            z=np.load(archive/(row['case']+'.npz'))
            ax.semilogy(np.arange(1,len(z['lower_spectrum'])+1),np.maximum(z['lower_spectrum'],1e-15),label='permitted-box lower norm')
            ax.semilogy(np.arange(1,len(z['upper_spectrum'])+1),np.maximum(z['upper_spectrum'],1e-15),label='all-query envelope')
            ax.axhline(.001,color='black',linestyle='--',linewidth=.8,label='epsilon')
            ax.set_title(f"n={row['n']} ({row['case']})");ax.set_xlabel('mode index');ax.set_ylabel('unit-input tangent scale')
        axes[0,0].legend(fontsize=7);fig.tight_layout();fig.savefig(ROOT/'spectra.png',dpi=160);plt.close(fig)
    except ImportError:
        pass
    print(json.dumps(dict(fit=fit,finite_fit=finite_fits,loglog_all=payload['loglog_exponent_all'],loglog_last_three=payload['loglog_exponent_largest_three'],cpu_seconds=payload['cpu_seconds']),indent=2))


if __name__=='__main__':
    main()
