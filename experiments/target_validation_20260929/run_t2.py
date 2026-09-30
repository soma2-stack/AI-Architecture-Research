import argparse,json,subprocess
from common import ROOT,Meter,append,provenance
from t2 import run

def main():
    p=argparse.ArgumentParser(); p.add_argument('--phase',choices=['dev','official'],required=True); p.add_argument('--official-unlock',action='store_true'); a=p.parse_args()
    c=json.loads((ROOT/'config_t2.json').read_text()); m=Meter(c,'t2_'+a.phase); status='ERROR'
    out=ROOT/'runs'/('t2_'+a.phase+'.jsonl')
    try:
        if not (ROOT/'t1_result.json').exists() or not json.loads((ROOT/'t1_result.json').read_text())['verdict'].startswith('KILLED'): raise RuntimeError('T1 prerequisite')
        if a.phase=='official':
            if not a.official_unlock or not json.loads((ROOT/'dev_validity_t2.json').read_text())['passed']: raise RuntimeError('Official seed lock')
            paths=['config_t2.json','PROTOCOL_T2.md','t2.py','run_t2.py','common.py']
            if subprocess.check_output(['git','diff','HEAD','--',*[str(ROOT/p) for p in paths]],text=True).strip(): raise RuntimeError('Uncommitted protocol/source')
        if out.exists(): raise RuntimeError('Run exists; preserve it')
        append(out,{'type':'provenance',**provenance(ROOT/'config_t2.json')}); chosen=[]
        seeds=c['official_seeds'] if a.phase=='official' else c['development_seeds'][:1]
        models=c['models'] if a.phase=='official' else ['head','mlp16']
        for seed in seeds:
            for kind in models:
                for arm in (['joint'] if a.phase=='dev' else ['stream','joint','fresh']):
                    trials=[]
                    for lr in c['head_lrs'] if kind=='head' else c['neural_lrs']:
                        r=run(seed,kind,arm,lr,c,m); append(out,{'type':'trial',**r}); trials.append(r)
                    best=min(trials,key=lambda r:(r['training_selection_loss'],r['lr'])); chosen.append(best)
                    append(out,{'type':'selected',**best}); print(f"{seed} {kind} {arm}: {best['mean_accuracy']:.4f}",flush=True)
        if a.phase=='dev':
            head=chosen[0]; neural=chosen[1]
            passed=head['mean_accuracy']>=.98 and min(head['accuracy_by_task'])>=.95 and neural['mean_accuracy']>=.95
            (ROOT/'dev_validity_t2.json').write_text(json.dumps({'passed':passed,'head':head['mean_accuracy'],'neural':neural['mean_accuracy']},indent=2))
            status='PASS' if passed else 'VALIDITY_FAILURE'
        else:
            checks=[]
            for seed in seeds:
                group={r['arm']:r for r in chosen if r['seed']==seed and r['model']=='head'}
                s,j,f=group['stream'],group['joint'],group['fresh']
                ratios=[h['aulc']/max(f['history'][i]['aulc'],.001) for i,h in enumerate(s['history']) if h['first_exposure']]
                retention=max(h['max_old_inactive_loss'] for h in s['history']); ratio=max(ratios)
                passed=retention<=c['kill_max_retention_loss'] and s['mean_accuracy']>=c['kill_accuracy'] and j['mean_accuracy']-s['mean_accuracy']<=c['kill_oracle_gap'] and ratio<=c['kill_adaptation_ratio']
                checks.append({'seed':seed,'retention_loss':retention,'max_fresh_aulc_ratio':ratio,'stream_accuracy':s['mean_accuracy'],'joint_accuracy':j['mean_accuracy'],'passed':passed})
            kill=sum(x['passed'] for x in checks)>=c['kill_seeds']
            (ROOT/'t2_result.json').write_text(json.dumps({'target':2,'verdict':'KILLED — FIXED CONDITIONAL LINEAR CONTROL' if kill else 'INCOMPLETE — REMAINING HOSTILE CONTROLS REQUIRED','checks':checks,'training_runs':len(chosen)*2,'remaining_controls':'not run after sufficient known-method kill' if kill else 'must complete before survival'},indent=2))
            status='COMPLETE' if kill else 'INCOMPLETE'
    finally: print(json.dumps(m.finish(status)),flush=True)

if __name__=='__main__': main()
