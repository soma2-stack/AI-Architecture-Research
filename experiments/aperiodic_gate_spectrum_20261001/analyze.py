"""Post-measurement descriptive analysis; never selects or reruns histories."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '4'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import time
import json
import csv
import hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import psutil

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
OUT = ROOT/'analysis'

def load(folder):
    return [json.loads(p.read_text()) for p in sorted(folder.glob('n*.json'))]

def csv_save(name, rows):
    with (OUT/name).open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def fits(ns, ys):
    ns, ys=np.array(ns,dtype=float), np.array(ys,dtype=float)
    result={}
    for label,x in [('n2',ns**2),('n2logn',ns**2*np.log(ns))]:
        b=float(x@ys/(x@x)); pred=b*x
        loo=[]
        for i in range(len(ns)):
            keep=np.arange(len(ns))!=i
            coef=x[keep]@ys[keep]/(x[keep]@x[keep])
            loo.append((coef*x[i]-ys[i])/ys[i])
        result[label]=dict(coefficient=b, relative_rmse=float(np.sqrt(np.mean(((pred-ys)/ys)**2))),
                           absolute_rmse=float(np.sqrt(np.mean((pred-ys)**2))),
                           leave_one_width_out_relative_rmse=float(np.sqrt(np.mean(np.square(loo)))))
    result['loglog_exponent']=float(np.polyfit(np.log(ns),np.log(ys),1)[0])
    return result

def main():
    start_c,start_w=time.process_time(),time.perf_counter()
    OUT.mkdir(exist_ok=False)
    primary=load(ROOT/'results'); full=load(ROOT/'full_history_results')
    assert len(primary)==70 and len(full)==24
    rows=[]
    for rec in primary:
        for metric,m in rec['metrics'].items():
            rows.append(dict(map='source',n=rec['n'],H=rec['relevant_window'],strategy=rec['strategy'],seed=rec['seed'],
                             metric=metric,count=m['visible_count'],count_n2=m['count_over_n2'],count_n2logn=m['count_over_n2logn'],
                             input_sd_count=m['input_sd_visible_count'],radius_005_count=m['radius_005_linear_visible_count'],
                             top=m['top'],tail_energy=m['tail_energy_below_epsilon'],epsilon_gap=m['epsilon_gap']))
    for r in full:
        s=np.load(ROOT/'full_history_results'/f"n{r['n']:03d}_{r['strategy']}_s{r['seed']}_spectra.npz")['box_rms']
        cnt=r['visible_count']; gap=float(s[cnt-1]/s[cnt]) if cnt and s[cnt]>0 else None
        rows.append(dict(map='complete',n=r['n'],H=r['H'],strategy=r['strategy'],seed=r['seed'],metric='box_rms',
                         count=cnt,count_n2=r['count_over_n2'],count_n2logn=r['count_over_n2logn'],
                         input_sd_count=r['input_sd_visible_count'],radius_005_count=r['radius_005_linear_count'],
                         top=r['top'],tail_energy=r['tail_energy_below_epsilon'],epsilon_gap=gap))
    csv_save('per_case.csv',rows)
    groups={}
    for r in rows:
        key=(r['map'],r['metric'],r['strategy'],r['n'])
        groups.setdefault(key,[]).append(r)
    means=[]
    for (which,metric,strategy,n),vals in sorted(groups.items()):
        counts=[v['count'] for v in vals]
        means.append(dict(map=which,metric=metric,strategy=strategy,n=n,H=vals[0]['H'],
                          mean_count=float(np.mean(counts)),min_count=min(counts),max_count=max(counts),
                          mean_n2=float(np.mean(counts)/n**2),mean_n2logn=float(np.mean(counts)/(n**2*np.log(n))),
                          mean_input_sd_count=float(np.mean([v['input_sd_count'] for v in vals])),
                          mean_radius_005_count=float(np.mean([v['radius_005_count'] for v in vals]))))
    csv_save('by_width_strategy.csv',means)
    fitrows={}
    keys=sorted(set((v['map'],v['metric'],v['strategy']) for v in means))
    for key in keys:
        vals=[v for v in means if (v['map'],v['metric'],v['strategy'])==key]
        fitrows['/'.join(key)]=fits([v['n'] for v in vals],[v['mean_count'] for v in vals])
        if key[0]=='source':
            large=[v for v in vals if v['n']>=64]
            fitrows['/'.join(key)+'/n_ge_64']=fits([v['n'] for v in large],[v['mean_count'] for v in large])
    checks={}
    frozen=json.loads((ROOT/'FROZEN.json').read_text())
    checks['primary_and_accepted_hashes']={name:hashlib.sha256((REPO/name).read_bytes()).hexdigest()==h for name,h in frozen['inputs'].items()}
    frozen2=json.loads((ROOT/'FULL_HISTORY_FROZEN.json').read_text())
    checks['supplement_hashes']={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h for name,h in frozen2['inputs'].items()}
    assert all(checks['primary_and_accepted_hashes'].values()) and all(checks['supplement_hashes'].values())
    fd=[v for r in primary for ck in r['full_dense_crosschecks'] for v in ck['finite_difference']]
    fd2=[v for r in full for v in r['checks']['finite_differences']]
    checks.update(primary_fd_checks=len(fd),complete_fd_checks=len(fd2),
                  max_primary_full_gradient_error=max(v['full_gradient_derivative_error'] for v in fd),
                  max_complete_full_gradient_error=max(v['full_gradient_derivative_error'] for v in fd2),
                  max_fixed_h_forward_error=max([v['fixed_h_forward_error'] for v in fd]+[v['forward_endpoint_error'] for v in fd2]),
                  max_complete_input_norm_error=max(abs(r['checks']['input_direction_norm']-1) for r in full),
                  max_input_abs=max(r['history']['max_abs_input'] for r in primary+full),
                  complete_max_gram_roundoff_abs=max(abs(r['negative_gram_eigenvalue']) for r in full),
                  min_complete_epsilon_gap=min(r['epsilon_gap'] for r in rows if r['map']=='complete'))
    optimized=[(r,m) for r in primary if r['strategy']!='scalar_control' for m in r['metrics']['box_rms']['query_optimized_modes']]
    checks['optimized_tail_modes_exceed_epsilon']=[dict(case=r['case'],**m) for r,m in optimized if m['rms_singular_value']<=.001 and m['optimized_box_distance']>.001]
    correlations=[]
    for r in primary:
        for metric,m in r['metrics'].items():
            for lag,v in m['correlations_by_lag'].items():
                correlations.append(dict(n=r['n'],strategy=r['strategy'],seed=r['seed'],metric=metric,lag=int(lag),**v))
    csv_save('temporal_correlations.csv',correlations)
    resources=[json.loads((ROOT/p/'resource_summary.json').read_text()) for p in ('development','results','full_history_results')]
    plt.rcParams.update({'font.size':9})
    fig,axs=plt.subplots(1,3,figsize=(12,3.8))
    for strategy,marker in [('diffuse','o'),('random_pulse','s'),('query_adversarial_pulse','^')]:
        v=[r for r in means if r['map']=='source' and r['metric']=='box_rms' and r['strategy']==strategy]
        axs[0].plot([r['n'] for r in v],[r['mean_n2'] for r in v],marker=marker,label=strategy)
        v=[r for r in means if r['map']=='complete' and r['strategy']==strategy]
        axs[1].plot([r['n'] for r in v],[r['mean_n2'] for r in v],marker=marker,label=strategy)
    for n in [64,128,256]:
        path=ROOT/'results'/f'n{n:03d}_query_adversarial_pulse_s62101_spectra.npz'
        s=np.load(path)['box_rms']
        axs[2].semilogy(np.arange(1,len(s)+1)/n,np.maximum(s,1e-12),label=f'n={n}')
    axs[0].set(title='Source-only query-visible count / n²',xlabel='width n',ylabel='count / n²')
    axs[1].set(title='Complete-history count / n² (secondary)',xlabel='width n',ylabel='count / n²')
    axs[2].axhline(.001,color='k',linestyle='--',label='epsilon')
    axs[2].set(xlim=(0,2),ylim=(1e-8,1),title='Source temporal spectrum',xlabel='temporal index / n',ylabel='singular value')
    for ax in axs: ax.legend(fontsize=7); ax.grid(alpha=.25)
    fig.tight_layout(); fig.savefig(OUT/'diagnostic.png',dpi=170); plt.close(fig)
    result=dict(fits=fitrows,checks=checks,
                resources=dict(measurement_cpu_seconds=sum(r['cpu_seconds'] for r in resources),
                               measurement_wall_seconds=sum(r['wall_seconds'] for r in resources),
                               peak_measurement_rss_bytes=max(r['peak_rss_bytes'] for r in resources),gpu_seconds=0),
                analysis_cpu_seconds=time.process_time()-start_c,analysis_wall_seconds=time.perf_counter()-start_w,
                analysis_peak_working_set_bytes=psutil.Process().memory_info().peak_wset)
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
