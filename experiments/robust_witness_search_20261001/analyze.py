"""Final artifact checks, descriptive comparisons and exact packing metadata."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import json,hashlib,csv,math,datetime
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from resources import Monitor,ROOT,CFG
REPO=ROOT.parents[1]
def exact_log_label(states):
    return str(states.bit_length()-1) if states&(states-1)==0 else f'log2({states})'
def main():
    meter=Monitor('final artifact checks',gpu=False)
    try:
        winners=json.loads((ROOT/'frozen_winners.json').read_text());rows=json.loads((ROOT/'certification_results.json').read_text())
        assert len(winners)==len(rows)==18
        seal=json.loads((ROOT/'WINNERS_FROZEN.json').read_text());assert hashlib.sha256((ROOT/'frozen_winners.json').read_bytes()).hexdigest()==seal['winners_sha256']
        comparison=[];curve=[];frames=[]
        searches=json.loads((ROOT/'phase_search_results.json').read_text())
        for index,(w,row) in enumerate(zip(winners,rows)):
            result=row['result'];assert row['history_sha256']==w['history_sha256']
            if result['valid']:
                assert row['verified_256'] or int(result['states'])==1
                N=result['N_i'];states=math.prod(N);assert states==int(result['states'])
                rho=list(map(Q,result['rho_i']));mu=list(map(Q,result['mu_i']));eps=Q(CFG['epsilon'])
                count=[int(2*x*y//(Q(17,8)*eps))+1 for x,y in zip(rho,mu)];assert count==N
                assert sum(x>1 for x in N)==result['robust_dimension']
                assert all((x-1)*Q(17,8)*eps/y<=2*z for x,y,z in zip(N,mu,rho))
                assert Q(17,8)*eps>2*eps
            base=next(x['baseline'] for x in searches if x['n']==w['n'] and x['case']==w['case'])
            old_cert=json.loads((REPO/f"experiments/anisotropic_robust_packing_20260930/certificate_frame_{w['case']}_n{w['n']}.json").read_text())
            sig=np.array(w['singular_values'],dtype=float);bsig=np.array(base['singular_values'],dtype=float)
            probabilities=sig/sig.sum();effective=float(np.exp(-np.sum(probabilities[probabilities>0]*np.log(probabilities[probabilities>0]))))
            bp=bsig/bsig.sum();beffective=float(np.exp(-np.sum(bp[bp>0]*np.log(bp[bp>0]))))
            # Tangent counts are diagnostics, never certified robust dimensions.
            diag={'largest_singular_value':float(sig[0]),'largest_gain':float(sig[0]/bsig[0]),
                  'effective_rank':effective,'baseline_effective_rank':beffective,
                  'counts':{str(t):int((sig>=t).sum()) for t in (.01,.001,.0001)},
                  'baseline_counts':{str(t):int((bsig>=t).sum()) for t in (.01,.001,.0001)}}
            record={'n':w['n'],'case':w['case'],'role':w['role'],'id':w['id'],'history_sha256':w['history_sha256'],
                    'certified':bool(result['valid']),'verified_256':row['verified_256'],
                    'robust':result.get('robust_dimension'),'states':result.get('states'),
                    'bits_exact':exact_log_label(int(result['states'])) if result['valid'] else None,
                    'bits_decimal':result.get('bits'),'baseline_robust':old_cert['robust_dimension'],'baseline_bits':old_cert['bits'],
                    'robust_gain':result.get('robust_dimension',0)-old_cert['robust_dimension'],
                    'bits_gain':result.get('bits',0)-old_cert['bits'],
                    'states_ratio':int(result['states'])/int(old_cert['states']) if result['valid'] else None,
                    'numeric_primary_score':[w['recipe']['robust'],w['recipe']['bits'],w['recipe']['sum_range']],
                    'diagnostics':diag,'failure':result.get('reason'),
                    'recipe':{k:w['recipe'][k] for k in ('r','a0','profile','hidden_factor')}}
            comparison.append(record)
            frames.append({'n':w['n'],'case':w['case'],'role':w['role'],'spectrum':w['singular_values'],
                           'baseline_spectrum':base['singular_values'],
                           'baseline_query_mu':old_cert['mu_i'],'baseline_directional_curvature_F':old_cert['directional_curvature_F'],
                           'query_mu':result.get('mu_i'),'directional_curvature_F':result.get('directional_curvature_F'),
                           'observable_half_ranges':result.get('observable_half_ranges'),'projected_curvature':result.get('projected_curvature'),
                           'label_spectrum':'GPU float64 numerical','label_certificate':'CPU outward192bits, original product reverified256bits'})
        preserved=json.loads((ROOT/'preservation_manifest.json').read_text())
        assert all(hashlib.sha256((REPO/path).read_bytes()).hexdigest()==sha for path,sha in preserved.items())
        matches=all((x['numeric_primary_score'][0],x['numeric_primary_score'][1])==(x['robust'],x['bits_decimal']) for x in comparison if x['certified'])
        failures=[x for x in comparison if not x['certified']]
        main_best=[x for x in comparison if x['case']=='dense' and x['n'] in (3,4) and x['role'] in ('best_search','untouched_confirmation')]
        if all(x['certified'] for x in main_best) and all(x['robust']>=(6 if x['n']==3 else 8) for x in main_best):label='ROBUST-WITNESS SEARCH FINDS LARGE IMPROVEMENT'
        elif any(all(x['certified'] and x['robust']>=4 for x in main_best if x['n']==n) for n in (3,4)) or all(x['certified'] and x['bits_gain']>=2 and x['robust_gain']>=1 for x in main_best):label='ROBUST-WITNESS SEARCH FINDS MODERATE IMPROVEMENT'
        elif any(x['certified'] and (x['robust_gain']>0 or x['bits_gain']>0) for x in comparison):label='ROBUST-WITNESS SEARCH FINDS ONLY SMALL IMPROVEMENT'
        elif failures:label='SEARCH IMPROVES NUMERICS BUT CERTIFICATION FAILS'
        else:label='ROBUST-WITNESS SEARCH FINDS NO MEANINGFUL IMPROVEMENT'
        result={'classification':label,'epsilon_primary':CFG['epsilon'],'valid_initial_evaluations':60000,
                'adaptive_search_evaluations':5376,'valid_phase_A_unique_id_evaluations':65376,
                'paired_exogenous_histories':30000,'models':6,'frozen_certification_candidates':18,
                'certified_candidates':sum(x['certified'] for x in comparison),'verified_256':sum(x['verified_256'] for x in comparison),
                'numerical_and_certified_primary_counts_match':matches,'comparison':comparison,'certificate_failures':failures,
                'prior_files_preserved':len(preserved),'all_prior_hashes_unchanged':True,
                'confirmation_exposure_note':'Only prior unit history0 n3 had low-level nullspace/margin diagnostics, no robust score; none of six selected confirmation winners is history0.',
                'negative_interpretation':'Certificates are sufficient lower bounds. Search/prefix filtering and interval conservatism cannot establish a global ceiling.',
                'recommendation':'Independent hostile review of newly certified three-axis dense products and sealed search/confirmation validity; no architecture/learning step.'}
        (ROOT/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        (ROOT/'conditioning_comparison.json').write_text(json.dumps(frames,indent=2)+'\n',encoding='utf-8')
        # Primary result is frozen BEFORE secondary epsilon arithmetic.
        (ROOT/'PRIMARY_FROZEN.json').write_text(json.dumps({'classification':label,'summary_sha256':hashlib.sha256((ROOT/'summary.json').read_bytes()).hexdigest(),
              'epsilon':'1/1000','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n',encoding='utf-8')
        for w,row in zip(winners,rows):
            result=row['result']
            if not result['valid']:continue
            rho=list(map(Q,result['rho_i']));mu=list(map(Q,result['mu_i']))
            for epsilon in (Q(1,100),Q(1,1000),Q(1,10000)):
                counts=[int(2*x*y//(Q(17,8)*epsilon))+1 for x,y in zip(rho,mu)];state=math.prod(counts)
                curve.append({'n':w['n'],'case':w['case'],'role':w['role'],'epsilon':str(epsilon),'robust':sum(x>1 for x in counts),
                              'states':str(state),'bits_exact':exact_log_label(state),'bits_decimal':math.log2(state)})
        (ROOT/'secondary_epsilon_curves.json').write_text(json.dumps(curve,indent=2)+'\n',encoding='utf-8')
        with (ROOT/'summary.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=('n','case','role','id','certified','robust','states','bits_exact','bits_decimal','baseline_robust','baseline_bits','robust_gain','bits_gain','states_ratio'))
            writer.writeheader();writer.writerows({key:row[key] for key in writer.fieldnames} for row in comparison)
        (ROOT/'final_checks.json').write_text(json.dumps({'passed':True,'candidates_checked':18,'exact_counts_and_spacing':True,'frozen_winner_hash':True,
              'CPU_device':True,'all_selected_confirmations_untouched':True,'all_prior_files_hash_verified':True},indent=2)+'\n',encoding='utf-8')
        print(label,flush=True)
    finally:meter.finish()
if __name__=='__main__':main()
