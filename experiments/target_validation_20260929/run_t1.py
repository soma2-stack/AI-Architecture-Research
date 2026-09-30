import argparse
import json
from common import ROOT, Meter, append, provenance
from t1 import rule_control, train

def main():
    p=argparse.ArgumentParser(); p.add_argument('--phase',choices=['dev','official'],required=True)
    p.add_argument('--official-unlock',action='store_true'); args=p.parse_args()
    path=ROOT/'config_t1.json'; c=json.loads(path.read_text()); meta=provenance(path)
    if args.phase=='official':
        valid=ROOT/'dev_validity_t1.json'
        if not args.official_unlock or not valid.exists() or not json.loads(valid.read_text())['passed']:
            raise RuntimeError('Official seed lock')
        import subprocess
        dirty=subprocess.check_output(['git','diff','HEAD','--',str(path),str(ROOT/'PROTOCOL.md'),*[str(x) for x in ROOT.glob('*.py')]],text=True)
        if dirty.strip(): raise RuntimeError('Commit source/config before official seeds')
    meter=Meter(c,'t1_'+args.phase); status='ERROR'; output=ROOT/'runs'/('t1_'+args.phase+'.jsonl')
    if output.exists(): raise RuntimeError('Append-only run already exists; no silent rerun')
    try:
        append(output,{'type':'provenance',**meta})
        seeds=c['official_seeds'] if args.phase=='official' else c['development_seeds'][:1]
        results=[]
        for seed in seeds:
            r=rule_control(seed); append(output,{'type':'rule_control',**r}); results.append(r)
        arms=[(m,s,'base') for m in c['models'] for s in c['schedules']]
        if args.phase=='official':
            arms += [('mlp',s,control) for control in c['mlp_controls'] for s in ('joint','cumulative')]
        else: arms=[('mlp','joint','base')]
        for seed in seeds:
            for model,schedule,control in arms:
                grid=c['sgd_lrs'] if control=='sgd' else c['adamw_lrs']; trials=[]
                for lr in grid:
                    r=train(seed,model,schedule,control,lr,c,meter)
                    append(output,{'type':'trial',**r}); trials.append(r)
                best=min(trials,key=lambda r:(r['union_bce'],r['lr']))
                append(output,{'type':'selected',**best}); results.append(best)
                print(f"{seed} {model} {schedule} {control}: acc={best['accuracy']:.3f} fit={best['union_accuracy']:.3f}",flush=True)
        if args.phase=='dev':
            joint=results[-1]; passed=joint['accuracy']>=.95 and joint['union_accuracy']>=.99 and results[0]['zero_error_distinct_rules']==1
            (ROOT/'dev_validity_t1.json').write_text(json.dumps({'passed':passed,'result':joint,'rule':results[0]},indent=2))
            status='PASS' if passed else 'VALIDITY_FAILURE'
        else: status='COMPLETE'
    finally:
        print(json.dumps(meter.finish(status)),flush=True)

if __name__=='__main__': main()
