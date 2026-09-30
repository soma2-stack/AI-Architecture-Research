"""Stored-results analysis and preservation; no predictor fitting."""
import json,statistics,hashlib,tarfile
from collections import defaultdict
from common import ROOT,Meter

def mean(values): return statistics.mean(values)
def main():
    c=json.loads((ROOT/'config.json').read_text()); meter=Meter(c,'stored_result_analysis_and_archiving'); status='ERROR'
    try:
        result=json.loads((ROOT/'result.json').read_text()); rows=[json.loads(x) for x in (ROOT/'runs/official.jsonl').read_text().splitlines()]
        selected=[r for r in rows if r['type']=='selected']; groups=defaultdict(list)
        for r in selected: groups[r['model'],r['control'],r['mode'],r['phase']].append(r)
        aggregates={'/'.join(key):{'runs':len(rs),'cf_mean':mean(r['cf_accuracy'] for r in rs),'cf_min':min(r['cf_accuracy'] for r in rs),
            'anti_mean':mean(r['anti_accuracy'] for r in rs),'shortcut_flip_mean':mean(r['bayes_relative_shortcut_reliance'] for r in rs),
            'current_train_mean':mean(r['train_'+r['phase']+'_accuracy'] if r['phase']!='joint' else sum(r['train_'+p+'_accuracy'] for p in ['A','B','C'])/3 for r in rs),
            'accuracy_auc_mean':mean(r['correction_accuracy_auc'] for r in rs),'sample_exposures_to_95_upper':[r['samples_to_exceed_95_upper'] for r in rs],
            'parameters':sorted({r['parameters'] for r in rs}),'persistent_tensor_bytes':sorted({r['persistent_tensor_bytes'] for r in rs})} for key,rs in groups.items()}
        pairing=[r for r in rows if r['type']=='paired']; pair_groups=defaultdict(list)
        for r in pairing: pair_groups[r['model'],r['control'],r['phase']].append(r)
        gaps={'/'.join(key):{'mean_gap_pp':mean(r['gap_pp'] for r in rs),'max_gap_pp':max(r['gap_pp'] for r in rs),
            'prediction_disagreement_mean':mean(r['prediction_disagreement'] for r in rs),'per_seed':rs} for key,rs in pair_groups.items()}
        pr=defaultdict(list)
        for r in rows:
            if r['type']=='probes':
                for p in r['results']: pr[r['model'],r['control'],r['mode'],r['phase'],p['layer'],p['type']].append(p['test_accuracy'])
        probe_summary={'/'.join(map(str,key)):{'mean_accuracy':mean(xs),'min_accuracy':min(xs),'runs':len(xs)} for key,xs in pr.items()}
        manifest=[]
        for path in sorted((ROOT/'checkpoints').glob('*.pt')):
            manifest.append({'path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        archive=ROOT/'model_checkpoints.tar.gz'
        if archive.exists(): raise RuntimeError('Preserve existing archive')
        with tarfile.open(archive,'w:gz',compresslevel=3) as tar:
            for item in manifest: meter.check(); tar.add(ROOT/item['path'],arcname=item['path'])
        (ROOT/'checkpoint_manifest.json').write_text(json.dumps({'files':manifest,'archive':archive.name,'archive_bytes':archive.stat().st_size,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))
        trials=[r for r in rows if r['type']=='trial']; curves=[r for trial in trials for r in trial['snapshots']]
        report={'decision':result['decision'],'result':result,'aggregates':aggregates,'paired_gaps':gaps,'probe_summaries':probe_summary,
            'selected_snapshots':len(selected),'official_optimization_trials':len(trials),'official_predictor_updates':sum(r['updates'] for r in trials),
            'official_predictor_sample_exposures':sum(r['sample_exposures'] for r in curves),'probe_fits':sum(len(r['results']) for r in rows if r['type']=='probes'),
            'provenance':rows[0],'interpretation_limits':['Only one bounded generator; no architecture novelty claim.','High logistic accuracy means nonlinear embedding did not enforce nonlinear decoding necessity.','Probe information is not evidence of causal predictor use; no causal test needed after kill.','Unrun repair arms are not failures; mandatory early stop.'],
            'readout_only_repair_tested':False,'expanded_models_run':False,'ams_v10_prepared':False,'second_generator_justified':result.get('second_generator_justified',False)}
        (ROOT/'summary.json').write_text(json.dumps(report,indent=2)); status='COMPLETE'
    finally: meter.finish(status)
    ledger=[json.loads(x) for x in (ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
    measured=[r for r in ledger if 'accounting' not in r]; reservations=[r for r in ledger if 'accounting' in r]
    resources={'measured_cpu_seconds':sum(r['cpu_seconds'] for r in measured),'unmeasured_cpu_reservation_seconds':sum(r['cpu_seconds'] for r in reservations),
        'charged_cpu_seconds':sum(r['cpu_seconds'] for r in ledger),'metered_job_wall_seconds':sum(r['wall_seconds'] for r in measured),'peak_rss_bytes':max(r['peak_rss_bytes'] or 0 for r in ledger),
        'gpu_used':False,'cuda_used':False,'workers':1,'threads':1,'wall_definition':'Sum of Python-job wall times; excludes literature/documentation elapsed time.'}
    report['resources']=resources; (ROOT/'summary.json').write_text(json.dumps(report,indent=2)); print(json.dumps(resources,indent=2))

if __name__=='__main__': main()
