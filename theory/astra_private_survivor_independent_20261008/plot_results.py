"""Static figures from archived data; no experiment reruns."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'comparison_results.json').read_text())['cases']
fig,axes=plt.subplots(1,2,figsize=(13,5),constrained_layout=True)
for ax,n in zip(axes,[32768,1048576]):
    rows=[x for x in data if x['n']==n and x['W']==16 and not x['raw_competitor']]
    labels=[x['variant'].replace('astra_','A: ').replace('gpt_','G: ').replace('_',' ') for x in rows]
    values=[max(q['best_M'] for q in x['queries']) for x in rows]
    ax.barh(labels,values)
    ax.set_xscale('log');ax.set_xlabel('Found complete M query score (lower bound)')
    ax.set_title(f'n={n:,}; m=8, R=4, W=16')
    ax.grid(axis='x',alpha=.25)
fig.suptitle('Matched chronology and query budget; controls/contrast differ as documented')
fig.savefig(ROOT/'comparison_scores.png',dpi=160);plt.close(fig)
data=json.loads((ROOT/'independent_results.json').read_text())['spectra']
fig,ax=plt.subplots(figsize=(7,4),constrained_layout=True)
for x in data:
    ax.semilogy(range(1,len(x['singular_M'])+1),x['singular_M'],'o-',label=x['mode'])
ax.set_xlabel('Singular-value index');ax.set_ylabel('Complete M response singular value')
ax.set_title('Eight independent controls at one fixed query; not robust dimension')
ax.legend();ax.grid(alpha=.25)
fig.savefig(ROOT/'independent_spectrum.png',dpi=160)
