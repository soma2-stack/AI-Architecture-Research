"""Hash phase boundaries. No scoring or certification in this program."""
from pathlib import Path
import json,hashlib,sys,subprocess
ROOT=Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(mode):
    if mode=='search':
        results=json.loads((ROOT/'phase_search_results.json').read_text())
        assert len(results)==6
        assert all(row['initial_evaluated']==8000 and row['adaptive_evaluated']==896 for row in results)
        files=['config.json','numerics.py','search.py','pool_manifest.json','phase_search_results.json']
        (ROOT/'SEARCH_SEALED.json').write_text(json.dumps({'stage':'search complete; confirmation not scored',
          'implementation_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
          'sha256':{name:sha(ROOT/name) for name in files},'primary_objective_unchanged':True},indent=2)+'\n',encoding='utf-8')
        print('Search and objective sealed; confirmation remains unopened')
    else:
        assert mode=='winners';lock=json.loads((ROOT/'SEARCH_SEALED.json').read_text())
        assert all(sha(ROOT/name)==hash_value for name,hash_value in lock['sha256'].items())
        search=json.loads((ROOT/'phase_search_results.json').read_text());confirmation=json.loads((ROOT/'phase_confirmation_results.json').read_text())
        assert all(row['initial_evaluated']==2000 and row['adaptive_evaluated']==0 for row in confirmation)
        winners=[]
        for row in search:
            for role,candidate in zip(('best_search','runner_up'),row['winners']):winners.append({**candidate,'role':role})
            partner=next(x for x in confirmation if x['n']==row['n'] and x['case']==row['case'])
            for candidate in partner['winners']:
                assert not (candidate['n']==3 and candidate['id']=='0'),'Prior unit-check history selected: cannot call untouched; stop'
                winners.append({**candidate,'role':'untouched_confirmation'})
        assert len(winners)==18
        target=ROOT/'frozen_winners.json';assert not target.exists()
        target.write_text(json.dumps(winners,indent=2)+'\n',encoding='utf-8')
        meta={'source_search_seal':lock,'winners_sha256':sha(target),
              'confirmation_results_sha256':sha(ROOT/'phase_confirmation_results.json'),
              'candidates':[{'n':w['n'],'case':w['case'],'role':w['role'],'id':w['id'],'history_sha256':w['history_sha256'],
                             'recipe':{k:w['recipe'][k] for k in ('r','a0','profile','hidden_factor')}} for w in winners],
              'confirmation_winners_had_no_prior_score_or_diagnostic_exposure':True,
              'no_more_search_or_recipe_selection_allowed':True}
        (ROOT/'WINNERS_FROZEN.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
        print('All18 histories/axes/recipes frozen before CPU certification')
if __name__=='__main__':main(sys.argv[1])
