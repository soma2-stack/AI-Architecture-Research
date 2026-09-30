import argparse,json,copy,hashlib,subprocess
from common import ROOT,Meter,append,provenance,torch,np
from data import Generator
from models import build
from train import run,probes,kill_gate,logits

def grid(control,c): return c['sgdm_lrs'] if control=='sgdm' else c['lbfgs_lrs'] if control=='lbfgs' else c['adamw_lrs']
def loss(r): return r['train_'+r['phase']+'_bce'] if r['phase']!='joint' else sum(r['train_'+p+'_bce'] for p in ['A','B','C'])/3
def scratch_pass(r,c): return r['train_'+r['phase']+'_accuracy']>=c['scratch_train_min'] and r['cf_accuracy']>=c['scratch_cf_min']

def main():
    p=argparse.ArgumentParser(); p.add_argument('--phase',choices=['dev','official'],required=True); p.add_argument('--official-unlock',action='store_true'); a=p.parse_args()
    c=json.loads((ROOT/'config.json').read_text()); meter=Meter(c,a.phase); status='ERROR'; out=ROOT/'runs'/(a.phase+'.jsonl'); scratch={}; all_selected=[]; probes_done=set()
    try:
        if out.exists(): raise RuntimeError('Preserve existing output; no automatic rerun')
        if a.phase=='official':
            v=json.loads((ROOT/'development_validity.json').read_text()); validations=[json.loads(x) for x in (ROOT/'validation.jsonl').read_text().splitlines()]
            if not a.official_unlock or not v['passed'] or not validations[-1]['passed'] or validations[-1]['skips']: raise RuntimeError('Official validity/seed lock')
            paths=['common.py','data.py','models.py','train.py','runner.py','test_experiment.py','config.json','PROTOCOL.md']
            for path in paths: subprocess.check_output(['git','ls-files','--error-unmatch',str(ROOT/path)],text=True)
            if subprocess.check_output(['git','diff','HEAD','--',*[str(ROOT/path) for path in paths]],text=True).strip(): raise RuntimeError('Uncommitted freeze')
        append(out,{'type':'provenance',**provenance(ROOT/'config.json')})
        seeds=c['development_seeds'][:1] if a.phase=='dev' else c['official_seeds']
        models=['mlp2','mlp4'] if a.phase=='dev' else ['logistic','mlp2','mlp4']
        def save(seed,kind,control,lr,mode,phase,model):
            path=ROOT/'checkpoints'/f'{a.phase}_{seed}_{kind}_{control}_{lr}_{mode}_{phase}.pt'; path.parent.mkdir(exist_ok=True)
            with path.open('xb') as f: torch.save({'state_dict':model.state_dict(),'model':kind,'control':control,'seed':seed,'phase':phase},f)
            return str(path.relative_to(ROOT))
        def fit(seed,kind,control,mode):
            results=[]
            for lr in grid(control,c):
                r=run(seed,kind,control,lr,mode,c,meter,save); append(out,{'type':'trial',**r}); results.append(r)
            selected={}
            for phase in results[0]['snapshots']:
                label=phase['phase']; best=min([q for r in results for q in r['snapshots'] if q['phase']==label],key=lambda q:(loss(q),q['lr']))
                selected[label]=best; append(out,{'type':'selected',**best}); all_selected.append(best)
                print(f"{seed} {kind} {control} {mode}/{label}: train={best.get('train_'+label+'_accuracy',0):.4f} cf={best['cf_accuracy']:.4f}",flush=True)
            return selected
        def probe_selected(record):
            key=record['checkpoint']
            if key in probes_done or a.phase=='dev': return
            saved=torch.load(ROOT/key,map_location='cpu',weights_only=True); model=build(record['seed'],record['model'],record['control'],c); model.load_state_dict(saved['state_dict'])
            r=probes(record['seed'],model,Generator(record['seed'],c),c,meter); append(out,{'type':'probes','checkpoint':key,'seed':record['seed'],'model':record['model'],'mode':record['mode'],'phase':record['phase'],'control':record['control'],'results':r}); probes_done.add(key)
        # Positive scratch controls BEFORE examining path-dependence results.
        valid=True
        for seed in seeds:
            for kind in models:
                for phase in ['B','C']:
                    r=fit(seed,kind,'continuous',phase)[phase]; scratch[seed,kind,'continuous',phase]=r
                    if kind!='logistic': valid=valid and scratch_pass(r,c)
        if a.phase=='dev':
            record={'passed':valid,'selected':all_selected,'gate':'Both MLPs scratch B/C train>=.99 and CF>=.95'}
            (ROOT/'development_validity.json').write_text(json.dumps(record,indent=2)); status='PASS' if valid else 'VALIDITY_FAILURE'; return
        if not valid:
            (ROOT/'result.json').write_text(json.dumps({'decision':'INVALID / INCOMPLETE — OWNER REVIEW REQUIRED','reason':'Official scratch learnability failed','scratch':[r for r in all_selected]},indent=2)); status='VALIDITY_FAILURE'; return
        for seed in seeds:
            for kind in models:
                joint=fit(seed,kind,'continuous','joint')['joint']; probe_selected(joint)
        # Logistic is descriptive, not an admitted nonlinear architecture residual.
        for seed in seeds:
            r=fit(seed,'logistic','continuous','warm')
            for v in r.values(): probe_selected(v)
        decisions=[]
        for control in c['controls_order']:
            killed=False
            for kind in ['mlp2','mlp4']:
                if control.startswith('reinit_') and int(control.split('_')[1])>=c['models'][kind]: continue
                pairs={}
                for seed in seeds:
                    for phase in ['B','C']:
                        if (seed,kind,control,phase) not in scratch:
                            if control in ('optimizer_reset','head_reset','last_layer') or control.startswith('reinit_'):
                                scratch[seed,kind,control,phase]=scratch[seed,kind,'continuous',phase]
                            else: scratch[seed,kind,control,phase]=fit(seed,kind,control,phase)[phase]
                    warm=fit(seed,kind,control,'warm'); pairs[seed]={p:(warm[p],scratch[seed,kind,control,p]) for p in ['B','C']}
                    for r in warm.values(): probe_selected(r)
                    for phase in ['B','C']:
                        s=scratch[seed,kind,control,phase]; probe_selected(s)
                        wm=torch.load(ROOT/warm[phase]['checkpoint'],map_location='cpu',weights_only=True); sm=torch.load(ROOT/s['checkpoint'],map_location='cpu',weights_only=True)
                        m1=build(seed,kind,control,c); m2=build(seed,kind,control,c); m1.load_state_dict(wm['state_dict']); m2.load_state_dict(sm['state_dict']); e=Generator(seed,c).evaluation()
                        disagreement=float(((logits(m1,e['cf'])>=0)!=(logits(m2,e['cf'])>=0)).float().mean()); distance=float(torch.sqrt(sum((wm['state_dict'][k]-sm['state_dict'][k]).square().sum() for k in wm['state_dict'])))
                        append(out,{'type':'paired','seed':seed,'model':kind,'control':control,'phase':phase,'warm_checkpoint':warm[phase]['checkpoint'],'scratch_checkpoint':s['checkpoint'],'gap_pp':100*(s['cf_accuracy']-warm[phase]['cf_accuracy']),'prediction_disagreement':disagreement,'raw_parameter_l2':distance,'scratch_valid':scratch_pass(s,c)})
                passed,checks=kill_gate(pairs,c)
                # A repair cannot qualify against an underfitting matched scratch variant.
                passed=passed and sum(all(scratch_pass(s,c) for _,s in phases.values()) for phases in pairs.values())>=c['kill_seeds']
                eligible=control!='continuous'
                decision={'control':control,'model':kind,'satisfies_numeric_gate':passed,'eligible_stop_repair':eligible,'killed':passed and eligible,'checks':checks}; decisions.append(decision); append(out,{'type':'gate',**decision}); killed=killed or (passed and eligible)
            if killed:
                (ROOT/'result.json').write_text(json.dumps({'decision':'TARGET KILLED — ORDINARY METHODS CLOSE THE GAP','winning_control':control,'gate_results':decisions,'not_run_controls':c['controls_order'][c['controls_order'].index(control)+1:],'expanded_models_run':False,'second_generator_justified':False},indent=2)); status='KILLED'; return
        (ROOT/'result.json').write_text(json.dumps({'decision':'INVALID / INCOMPLETE — OWNER REVIEW REQUIRED','reason':'Cheap panel requires full survival/causal audit before expanded claims','gate_results':decisions},indent=2)); status='INCOMPLETE'
    except Exception as e:
        append(ROOT/'failures.jsonl',{'phase':a.phase,'error':repr(e)}); raise
    finally: print(json.dumps(meter.finish(status)),flush=True)

if __name__=='__main__': main()
