"""Numerical discovery with a sealed confirmation split and fixed objective."""
import json,sys,hashlib,itertools
from fractions import Fraction as Q
import numpy as np
import numerics as a
from resources import Monitor,ROOT,CFG

def evaluate_spectra(m,X,meter):
    out=[]
    for start in range(0,len(X),CFG['batch_size']):
        meter.check();out.append(a.spectrum_batch(m,X[start:start+CFG['batch_size']]))
    return np.concatenate(out)

def stage1(s):return np.log1p(s[:,:8]/(17/8*.001)).sum(axis=1)

def initial_pool(pool,phase):
    mask=pool['confirmation']==(phase=='confirmation')
    return pool['X'][mask].copy(),np.flatnonzero(mask).astype(str)

def screen(m,X,ids,s,meter,stage):
    limit=CFG['stage2_search_shortlist' if stage=='search' else 'stage2_confirmation_shortlist']
    idx=np.argsort(-stage1(s),kind='stable')[:limit]
    # Fixed stage2 query test; do not use confirmation to choose it.
    frames=[];records=[]
    for j in idx:
        meter.check();f=a.frame(m,X[j]);mu=a.margins(m,f['U'][:8]);qscore=float(np.log1p(f['sigma'][:8]*mu/(17/8*.001)).sum())
        frames.append(f);records.append({'id':str(ids[j]),'stage1':float(stage1(s[j:j+1])[0]),'stage2':qscore,'query_mu_svd':mu.tolist()})
    idx2=np.argsort([-x['stage2'] for x in records],kind='stable')[:CFG['stage3_search_shortlist' if stage=='search' else 'stage3_confirmation_shortlist']]
    chosen=[frames[j] for j in idx2];details=[records[j] for j in idx2]
    recipes=a.best_recipes(m,chosen,meter)
    ranked=sorted(zip(chosen,details,recipes),key=lambda row:a.rank(row[2]),reverse=True)
    return ranked,[{**rec,'recipe':recipe} for _,rec,recipe in ranked]

def serialize(m,record):
    f,details,recipe=record;n=m['n'];r=recipe['r']
    L=recipe.get('L',a.query_projection(m,f['U'][:r]).tolist())
    return {'label':'NUMERICAL ONLY — FROZEN FOR CERTIFICATION','n':n,'case':m['case'],**details,
            'X':[[str(Q(float(x))) for x in row] for row in f['X']],
            'B':[[str(Q(float(x))) for x in row[:n+r]] for row in f['B']],
            'U':[[str(Q(float(x))) for x in row] for row in f['U'][:r]],
            'L':[[str(Q(float(x))) for x in row] for row in L],
            'singular_values':[str(float(x)) for x in f['sigma']],
            'recipe':recipe,'history_sha256':hashlib.sha256(f['X'].tobytes()).hexdigest()}

def main(phase):
    assert phase in ('search','confirmation')
    if phase=='confirmation':assert (ROOT/'SEARCH_SEALED.json').exists(),'Seal complete search/code before confirmation'
    assert not (ROOT/f'phase_{phase}_results.json').exists()
    meter=Monitor('phase '+phase,gpu=True);outputs=[]
    try:
        for n in CFG['widths']:
            pool=np.load(ROOT/f'pool_n{n}.npz')
            for case in CFG['models']:
                X,ids=initial_pool(pool,phase)
                print('screening',phase,n,case,len(X),flush=True);m=a.model(n,case)
                s=evaluate_spectra(m,X,meter);initial_count=len(X)
                if phase=='search':
                    rng=np.random.default_rng(CFG['pool_seed'][str(n)]+1000+(case=='independent'))
                    parents=np.argsort(-stage1(s),kind='stable')[:16]
                    mutated=np.clip(X[parents[np.arange(512)%16]]+rng.normal(0,CFG['mutation_scale'],(512,*X.shape[1:])),*CFG['candidate_domain'])
                    sm=evaluate_spectra(m,mutated,meter)
                    X=np.concatenate([X,mutated]);s=np.concatenate([s,sm]);ids=np.r_[ids,[f'mutation_{i}' for i in range(512)]]
                    selected=np.argsort(-stage1(s),kind='stable')[:8];current=X[selected].copy();proposals=[];spectra=[];probe_ids=[]
                    for iteration in range(16):
                        sign=rng.choice([-1.,1.],current.shape);probe=CFG['spsa_probe_scale']
                        plus=np.clip(current+probe*sign,-.5,.5);minus=np.clip(current-probe*sign,-.5,.5)
                        pair=np.concatenate([plus,minus]);ss=evaluate_spectra(m,pair,meter)
                        gain=(stage1(ss[:8])-stage1(ss[8:]))/(2*probe)
                        grad=gain[:,None,None]*sign;grad/=np.maximum(np.linalg.norm(grad.reshape(8,-1),axis=1),1e-12)[:,None,None]
                        current=np.clip(current+CFG['spsa_step']*grad,-.5,.5);updated=evaluate_spectra(m,current,meter)
                        proposals.extend([pair,current.copy()]);spectra.extend([ss,updated]);probe_ids.extend([f'spsa_{iteration}_{j}' for j in range(24)])
                    X=np.concatenate([X,*proposals]);s=np.concatenate([s,*spectra]);ids=np.r_[ids,probe_ids]
                np.savez_compressed(ROOT/f'spectra_{phase}_{case}_n{n}.npz',ids=ids,singular_values=s,stage1=stage1(s))
                ranked,records=screen(m,X,ids,s,meter,phase)
                winners=[serialize(m,row) for row in ranked[:(2 if phase=='search' else 1)]]
                if phase=='search':
                    baseline=np.array([[float(Q(v)) for v in row] for row in a.SAVED['baseline_histories'][str(n)]])
                    bf=a.frame(m,baseline);bre=a.best_recipes(m,[bf],meter)[0]
                    baseline_record=serialize(m,(bf,{'id':'archived_baseline','stage1':float(stage1(bf['sigma'][None])[0]),'stage2':float(np.log1p(bf['sigma'][:8]*a.margins(m,bf['U'][:8])/(17/8*.001)).sum())},bre))
                else:baseline_record=None
                row={'n':n,'case':case,'initial_evaluated':initial_count,'adaptive_evaluated':len(X)-initial_count,
                     'stage2_evaluated':len(np.argsort(-stage1(s))[:128]),'stage3_evaluated':len(records),
                     'stage3_ranking':records,'winners':winners,'baseline':baseline_record}
                outputs.append(row);(ROOT/f'result_{phase}_{case}_n{n}.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
                print('finished',phase,n,case,[(w['recipe']['robust'],w['recipe']['bits']) for w in winners],flush=True)
        (ROOT/f'phase_{phase}_results.json').write_text(json.dumps(outputs,indent=2)+'\n',encoding='utf-8')
    finally:meter.finish()

if __name__=='__main__':main(sys.argv[1])
