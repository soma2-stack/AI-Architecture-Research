import argparse,json,subprocess,hashlib,time
from common import ROOT,Meter,append,provenance
from t3 import data,labels,infer,exact_audit,evaluate,graph,neural

def main():
    p=argparse.ArgumentParser(); p.add_argument('--phase',choices=['dev','official'],required=True); p.add_argument('--official-unlock',action='store_true'); a=p.parse_args()
    c=json.loads((ROOT/'config_t3.json').read_text()); m=Meter(c,'t3_'+a.phase); status='ERROR'; out=ROOT/'runs'/('t3_'+a.phase+'.jsonl')
    try:
        if not json.loads((ROOT/'t2_result.json').read_text())['verdict'].startswith('KILLED'): raise RuntimeError('T2 prerequisite')
        if a.phase=='official':
            if not a.official_unlock or not json.loads((ROOT/'dev_validity_t3.json').read_text())['passed']: raise RuntimeError('Official seed lock')
            paths=['config_t3.json','PROTOCOL_T3.md','t3.py','run_t3.py','common.py']
            if subprocess.check_output(['git','diff','HEAD','--',*[str(ROOT/p) for p in paths]],text=True).strip(): raise RuntimeError('Uncommitted freeze')
        if out.exists(): raise RuntimeError('Preserve existing run')
        package_hash={str(p.relative_to(ROOT/'vendor')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'vendor'/'aalpy').rglob('*.py')}
        append(out,{'type':'provenance',**provenance(ROOT/'config_t3.json'),'package_source_sha256':package_hash}); results=[]
        seeds=c['official_seeds'] if a.phase=='official' else c['development_seeds'][:1]
        for seed in seeds:
            for task in c['tasks']:
                m.check(); train,tests,hashes=data(seed,task,c)
                if hashes['minimum_transition_count']<c['minimum_transition_count']: raise RuntimeError('Transition coverage validity failure')
                started=time.process_time(); model=infer(train,[labels(task,w) for w in train]); table=graph(model)
                scores=evaluate(model,task,tests); exact=exact_audit(model,task); transitions=sum(len(x) for x in table.values())
                r={'type':'known_control','seed':seed,'task':task,'model':'GSM_RPNI','exact_by_length':scores,'exact_product_equivalence':exact,'states':len(table),'transitions':transitions,'numeric_table_bytes':transitions*12,'python_object_overhead_not_in_table_bytes':True,'parameters':0,'updates':0,'training_words':len(train),'training_prefixes':sum(map(len,train)),'training_fit':all(v==1.0 for v in evaluate(model,task,{0:train}).values()),'cpu_seconds':time.process_time()-started,'learned_graph':table,**hashes}
                append(out,r); results.append(r); print(f"{seed} {task}: length64={scores['64']:.4f} exact={exact} states={len(table)}",flush=True)
        if a.phase=='dev':
            passed=all(r['exact_product_equivalence'] and r['training_fit'] for r in results)
            (ROOT/'dev_validity_t3.json').write_text(json.dumps({'passed':passed,'results':results},indent=2)); status='PASS' if passed else 'VALIDITY_FAILURE'
        else:
            successes=[all(r['exact_by_length']['64']>=c['kill_exact_accuracy'] for r in results if r['seed']==s) for s in seeds]
            kill=sum(successes)>=c['kill_seeds']
            # Fixed first-seed neural diagnostics; never select the successful seed.
            for task in c['tasks']:
                for kind in c['neural_models']:
                    trials=[]
                    for lr in c['neural_lrs']:
                        r=neural(seeds[0],task,kind,lr,c,m); append(out,{'type':'neural_trial',**r}); trials.append(r)
                    best=min(trials,key=lambda r:(r['training_loss'],r['lr'])); append(out,{'type':'neural_selected',**best}); print(f"neural {task} {kind}: train={best['training_exact']:.4f} length64={best['exact_by_length']['64']:.4f}",flush=True)
            (ROOT/'t3_result.json').write_text(json.dumps({'target':3,'verdict':'KILLED — KNOWN FINITE-STATE RULE INDUCTION' if kill else 'INCOMPLETE — ADDITIONAL CONTROLS REQUIRED','cross_task_successes':sum(successes),'official_seeds':seeds,'all_lengths_min_accuracy':min(v for r in results for v in r['exact_by_length'].values()),'exact_equivalence_count':sum(r['exact_product_equivalence'] for r in results),'known_runs':len(results),'neural_training_runs':len(c['tasks'])*len(c['neural_models'])*len(c['neural_lrs']),'scope':'Finite-state transductions with prefix supervision; no claim about unrestricted algorithm induction.'},indent=2)); status='COMPLETE' if kill else 'INCOMPLETE'
    finally: print(json.dumps(m.finish(status)),flush=True)

if __name__=='__main__': main()

