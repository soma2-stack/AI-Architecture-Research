"""Generate scientific plots from completed incremental data only."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'results.json').read_text())
cases=d['cases']
fig,ax=plt.subplots(figsize=(7,4))
for n in sorted({x['n'] for x in cases}):
    xs=sorted([x for x in cases if x['n']==n and x['pattern']=='random'],key=lambda x:x['W'])
    ax.loglog([x['W'] for x in xs],[max(q['best_M'] for q in x['queries']) for x in xs],'o-',label=f'n={n:,}, m={xs[0]["m"]}, R={xs[0]["R"]}')
ax.axhline(.002,color='black',ls='--',label='robust target (not certified)')
ax.set(xlabel='Window W',ylabel='Best found reference query score',title='Complete coupled response: longer window, tiny found scores')
ax.legend(fontsize=8);fig.tight_layout();fig.savefig(ROOT/'query_vs_window.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(7,4))
xs=[x for x in cases if x['n']==32768 and x['pattern']=='random']
for key,label in [('best_M','M'),('L_at_best_M','L at M-selected query'),('H_at_best_M','H at M-selected query')]:
    ax.loglog([x['W'] for x in xs],[max(q[key] for q in x['queries']) for x in xs],'o-',label=label)
ax.set(xlabel='W',ylabel='Reference query score',title='Local versus complete feedback (n=32,768)');ax.legend();fig.tight_layout();fig.savefig(ROOT/'channel_vs_window.png',dpi=170);plt.close(fig)
if d['jacobians']:
    fig,ax=plt.subplots(figsize=(7,4))
    for x in d['jacobians']:
        ax.semilogy(range(1,len(x['singular_H'])+1),x['singular_H'],'o-',label=f'W={x["W"]}')
    ax.set(xlabel='Singular value index',ylabel='Normalized local H derivative',title='Independent controls: diagnostic, not robust dimension');ax.legend();fig.tight_layout();fig.savefig(ROOT/'independent_spectrum.png',dpi=170);plt.close(fig)
print('Plots updated for',len(cases),'cases')
