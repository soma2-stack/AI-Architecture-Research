"""Direct old primary proxy on predetermined raw pool IDs; no adaptations."""
import json,numpy as np
import geometry as g
from resources import Monitor
def main():
  assert not (g.ROOT/'raw_history_diagnostic.json').exists()
  meter=Monitor('direct raw history proxy diagnostic',True);rows=[]
  try:
    for n in [3,4]:
      pool=np.load(g.OLD/f'pool_n{n}.npz');eligible=np.flatnonzero(pool['confirmation']==0)
      rng=np.random.default_rng(g.CFG['seed']+200+n)
      ids=rng.choice(eligible,size=g.CFG['raw_history_count_per_width'],replace=False)
      assert not np.any(pool['confirmation'][ids])
      for family in ['dense','independent']:
        m=g.legacy.model(n,family);frames=[g.legacy.frame(m,pool['X'][j]) for j in ids]
        recipes=g.legacy.best_recipes(m,frames,meter)
        saved=json.loads((g.OLD/f'result_search_{family}_n{n}.json').read_text())
        shortlisted={v['id'] for v in saved['stage3_ranking']}
        spectra=np.load(g.OLD/f'spectra_search_{family}_n{n}.npz')
        ranked=np.argsort(-spectra['stage1']);rank={str(spectra['ids'][j]):i+1 for i,j in enumerate(ranked)}
        oldwin=saved['winners'][0]['recipe']
        for j,recipe in zip(ids,recipes):
          rows.append({'n':n,'case':family,'id':int(j),'strategy':'random' if j<4000 else 'sobol' if j<8000 else 'smooth',
            'spectral_rank':rank[str(j)],'old_primary_shortlist':str(j) in shortlisted,
            'direct_primary_proxy':{k:recipe[k] for k in ['valid','robust','bits','sum_range']},
            'matches_or_beats_old_search_winner_proxy':g.legacy.rank(recipe)>=g.legacy.rank(oldwin),
            'label':'NUMERICAL diagnostic only; no candidate promotion or certification'})
        print(n,family,[(r['robust'],r['bits']) for r in recipes],flush=True)
    (g.ROOT/'raw_history_diagnostic.json').write_text(json.dumps(rows,indent=2)+'\n')
  finally:meter.finish()
if __name__=='__main__':main()
