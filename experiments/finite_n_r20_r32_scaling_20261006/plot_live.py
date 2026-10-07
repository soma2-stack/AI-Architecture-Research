"""Refresh finite-size diagnostic plots whenever results.json is checkpointed."""
import json, time
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

ROOT=Path(__file__).resolve().parent
RESULT=ROOT/'results.json'
PROGRESS=ROOT/'progress.json'

def plot_once():
    if not RESULT.exists(): return 0
    try: data=json.loads(RESULT.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError): return 0
    cases=list(data.get('cases',{}).values())
    inherited=list(data.get('inherited_baselines',{}).values())
    if not cases and not inherited: return 0
    def save(name):
        plt.tight_layout(); plt.savefig(ROOT/name,dpi=135); plt.close()
    # R-specific response matrices as soon as each matching case lands.
    for R in (20,24,32,40,48,64):
        arr=[c for c in cases if c.get('family')=='sum_free' and c.get('R')==R]
        if not arr: continue
        c=max(arr,key=lambda x:x['n'])
        mat=np.asarray(c['metrics']['complete_normalized_matrix'],float)
        positive=mat[mat>0]
        if not positive.size: continue
        fig,ax=plt.subplots(figsize=(6,5)); im=ax.imshow(np.maximum(mat,1e-18),aspect='auto',norm=LogNorm(vmin=max(float(positive.min()),1e-18),vmax=max(float(positive.max()),1e-17)))
        fig.colorbar(im,ax=ax,label='normalized cross-talk'); ax.set(title=f'Complete response R={R}, n={c["n"]}',xlabel='read channel',ylabel='stored source'); save(f'response_matrix_r{R}.png')
    # K scaling uses inherited baseline points as labeled by their source.
    fig,ax=plt.subplots(figsize=(7,4.5)); plotted=False
    for R in (8,16):
        arr=[c for c in cases+inherited if c.get('n')==2048 and c.get('R')==R and c.get('family')=='sum_free']
        arr=sorted(arr,key=lambda x:x['K'])
        if arr:
            ax.plot([x['K'] for x in arr],[x['combined_B_norm'] if 'combined_B_norm' in x else x.get('individual_B_mean_abs',np.nan) for x in arr],'o-',label=f'R={R}')
            plotted=True
    if plotted:
        ax.set(xlabel='K',ylabel='combined donor response norm',title='Clean K scaling (inherited baselines included)'); ax.grid(True,alpha=.3); ax.legend(); save('clean_k_scaling.png')
    else: plt.close()
    # Cross-talk vs R and mask family comparison.
    clean=sorted([c for c in cases+inherited if c.get('family')=='sum_free'],key=lambda x:(x['n'],x['R']))
    if clean:
        fig,ax=plt.subplots(figsize=(7,4.5))
        for n in sorted(set(c['n'] for c in clean)):
            arr=[c for c in clean if c['n']==n]
            ax.plot([c['R'] for c in arr],[max(c['metrics']['max_complete_normalized_crosstalk'],1e-18) for c in arr],'o-',label=f'n={n}')
        ax.axhline(1e-3,color='red',ls='--',label='0.1%'); ax.set_yscale('log'); ax.set(xlabel='R',ylabel='worst normalized cross-talk',title='Clean cross-talk vs R'); ax.grid(True,which='both',alpha=.25); ax.legend(); save('cross_talk_vs_r.png')
    family=sorted([c for c in cases+inherited if c.get('n')==2048 and c.get('R') in (4,8,12,16)],key=lambda x:(x['family'],x['R']))
    if family:
        fig,ax=plt.subplots(figsize=(7,4.5))
        for fam in ('legacy','sum_free','independent'):
            arr=[c for c in family if c.get('family')==fam]
            if arr: ax.plot([c['R'] for c in arr],[max(c['metrics']['max_complete_normalized_crosstalk'],1e-18) for c in arr],'o-',label=fam)
        ax.axhline(1e-3,color='red',ls='--'); ax.set_yscale('log'); ax.set(xlabel='R',ylabel='worst normalized cross-talk',title='Mask family comparison, n=2048'); ax.grid(True,which='both',alpha=.25); ax.legend(); save('mask_family_comparison.png')
    clean_new=[c for c in cases if c.get('family')=='sum_free']
    if clean_new:
        fig,ax=plt.subplots(figsize=(7,4.5)); xs=[sum(c['alias_audit']['alias_counts_by_order'].values()) for c in clean_new]; ys=[c['metrics']['max_complete_normalized_crosstalk'] for c in clean_new]
        ax.scatter(xs,ys); ax.set_yscale('log'); ax.set(xlabel='XOR relations, orders 2–5',ylabel='complete cross-talk',title='Alias counts vs cross-talk'); ax.grid(True,which='both',alpha=.25); save('alias_relations_vs_crosstalk.png')
        fig,ax=plt.subplots(figsize=(7,4.5))
        for p in ('2','3','4','5'):
            arr=sorted(clean_new,key=lambda x:(x['n'],x['R']))
            ax.plot([f"{x['n']}:{x['R']}" for x in arr],[x['alias_audit']['alias_counts_by_order'].get(p,0) for x in arr],'o-',label=f'order {p}')
        ax.set(xlabel='n:R (case order)',ylabel='XOR relation count',title='Higher-order mask relations'); ax.tick_params(axis='x',rotation=70); ax.grid(True,alpha=.3); ax.legend(); save('alias_relations_vs_r.png')
    matched=[c for c in cases if c.get('matched_age_metrics')]
    if matched:
        fig,ax=plt.subplots(figsize=(7,4.5)); ax.plot([c['R'] for c in matched],[max(c['matched_age_metrics']['max_offdiag_ratio'],1e-18) for c in matched],'o-',label='row-wise matched age'); ax.plot([c['R'] for c in matched],[c['metrics']['max_complete_normalized_crosstalk'] for c in matched],'s--',label='final'); ax.axhline(1e-3,color='red',ls=':'); ax.set_yscale('log'); ax.set(xlabel='R',ylabel='worst cross-talk',title='Matched-age versus final endpoint'); ax.grid(True,which='both',alpha=.25); ax.legend(); save('matched_age_vs_final.png')
    return len(cases)

last=-1
deadline=time.time()+7300
while time.time()<deadline:
    count=plot_once()
    if count!=last:
        last=count
        print(f'LIVE_PLOTS_UPDATED cases={count}',flush=True)
    try:
        if PROGRESS.exists() and json.loads(PROGRESS.read_text(encoding='utf-8')).get('status')=='STOPPED':
            break
    except Exception: pass
    time.sleep(8)
plot_once()
print('LIVE_PLOTTER_DONE',flush=True)
