"""Analyze stored results only; never trains or alters frozen protocols."""
import json,statistics,hashlib,os
from collections import defaultdict
from common import ROOT,Meter,append

def rows(name): return [json.loads(x) for x in (ROOT/'runs'/name).read_text(encoding='utf-8-sig').splitlines()]
def mean(xs): return statistics.mean(xs)

def main():
    c=json.loads((ROOT/'config_t3.json').read_text()); meter=Meter(c,'final_stored_result_analysis')
    results=[json.loads((ROOT/f't{i}_result.json').read_text()) for i in (1,2,3)]
    if not all(r['verdict'].startswith('KILLED') for r in results): raise RuntimeError('No all-killed conclusion')
    data={i:rows(f't{i}_official.jsonl') for i in (1,2,3)}; aggregates={}
    for i in (1,2):
        selected=[r for r in data[i] if r['type']=='selected']; groups=defaultdict(list)
        for r in selected: groups[(r['model'],r.get('control','base'),r.get('schedule',r.get('arm')))].append(r)
        aggregates[str(i)]={'/'.join(k):{'mean_accuracy':mean(r.get('accuracy',r.get('mean_accuracy')) for r in rs),
            'min_accuracy':min(r.get('accuracy',r.get('mean_accuracy')) for r in rs),
            'parameters':sorted({r['parameters'] for r in rs}),
            'persistent_bytes':sorted({r['persistent_bytes'] for r in rs}),
            'seeds':len(rs)} for k,rs in groups.items()}
    selected=[r for r in data[3] if r['type']=='neural_selected']
    aggregates['3']={r['task']+'/'+r['model']:{'training_exact':r['training_exact'],'id_exact':r['exact_by_length']['16'],
        'length64_exact':r['exact_by_length']['64'],'parameters':r['parameters'],'persistent_bytes':r['persistent_tensor_bytes'],
        'first_failure_length':next((int(k) for k,v in r['exact_by_length'].items() if v<.99),None),
        'endpoint_error_slope_16_to_64':(r['exact_by_length']['16']-r['exact_by_length']['64'])/48} for r in selected}
    known=[r for r in data[3] if r['type']=='known_control']
    aggregates['3_known']={task:{'runs':len([r for r in known if r['task']==task]),'states':sorted({r['states'] for r in known if r['task']==task}),
        'transitions':sorted({r['transitions'] for r in known if r['task']==task}),
        'numeric_table_bytes':sorted({r['numeric_table_bytes'] for r in known if r['task']==task})} for task in c['tasks']}
    head=[r for r in data[2] if r['type']=='selected' and r['model']=='head' and r['arm']=='stream']
    aggregates['2_head_returns']={'accuracy_before_return_mean':mean(h['active_checkpoints'][0] for r in head for h in r['history'] if not h['first_exposure']),
        'return_aulc_mean':mean(h['aulc'] for r in head for h in r['history'] if not h['first_exposure']),
        'first_exposure_aulc_mean':mean(h['aulc'] for r in head for h in r['history'] if h['first_exposure']),
        'transfer_claim':'No positive shared-feature transfer claim; fixed context isolation suffices.'}
    meter.finish('COMPLETE')
    ledger=[json.loads(x) for x in (ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
    measured=[r for r in ledger if 'accounting' not in r]; reserved=[r for r in ledger if 'accounting' in r]
    resources={'measured_cpu_seconds':sum(r['cpu_seconds'] for r in measured),'conservative_unmeasured_cpu_charge_seconds':sum(r['cpu_seconds'] for r in reserved),
        'total_charged_cpu_seconds':sum(r['cpu_seconds'] for r in ledger),'measured_job_wall_seconds_sum':sum(r['wall_seconds'] for r in measured),
        'peak_rss_bytes':max(r['peak_rss_bytes'] or 0 for r in ledger),'gpu_used':False,'cuda_used':False,'threads':1,'workers':1,
        'wall_note':'Sum of metered Python jobs, not elapsed research/literature session duration.'}
    summary={'status':'ALL TARGETS KILLED — NEW TARGET DISCOVERY REQUIRED','target_results':results,'aggregates':aggregates,'resources':resources,
        'official_neural_training_runs':280+150+40,'known_control_runs':5+40,
        'deviations':[{'target':2,'detail':'Frozen prose says GRU hidden8; committed implementation uses hidden7. Actual GRU diagnostics are nonconforming to that prose. The independently decisive 136-parameter head arm, its thresholds and all seeds are unaffected. No GRU equivalence/parameter-matching conclusion is drawn.'}],
        'interpretation':'These minimal bounded targets did not justify an architecture search. This does not close unrestricted visual confounding, unbounded continual learning or unrestricted program induction.',
        'ams_v10_prepared':False,'next_action':'Stop. A new bounded target-discovery rationale needs owner review; no fourth target or AMS search is run.'}
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(resources,indent=2))

if __name__=='__main__': main()
