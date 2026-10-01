"""Export measured spectra and conditioning summaries; no new trajectories."""
import csv
import json
import math
from pathlib import Path
import audit as a

def finalize():
    rows=json.loads((a.ROOT/'summary.json').read_text())
    with (a.ROOT/'spectra.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['case','width','P','T','coordinates','index','singular_value'])
        for r in rows:
            for key in ('endpoint_raw','fixed_h_raw','fixed_h_input_sd_relative_parameter'):
                for i,x in enumerate(r[key]['values']):
                    writer.writerow([r['case'],r['n'],r['P'],r['T'],key,i+1,x])
    combined=[]
    for r in rows:
        n=r['n']; rc=float(r['future_head']['adjoint_ball_radius_formula_value'])
        vv=[float(x)*rc/math.sqrt(n) for x in r['fixed_h_raw']['values']]
        combined.append({'case':r['case'],'n':n,'head_ball_radius':rc,
            'unit_history_radius_tangent_only':True,
            'guaranteed_query_scales_tangent':vv,
            'counts':{str(e):sum(x>=e for x in vv) for e in a.CFG['absolute_thresholds']},
            'warning':'Sufficient bound in local linearization, not finite perturbation or bit certificate.'})
    (a.ROOT/'combined_conditioning.json').write_text(json.dumps(combined,indent=2))
    resources=a.read_jsonl(a.ROOT/'cpu_ledger.jsonl')
    metered=sum(x['cpu_seconds'] for x in resources)
    result={'classification':'ROBUST DIMENSION DEPENDS STRONGLY ON SCALE/HORIZON',
        'measured_cpu_seconds_before_finalization':metered,
        'numerical_and_check_job_wall_seconds':sum(x['wall_seconds'] for x in resources),
        'peak_ram_bytes':max(x['peak_rss_bytes'] for x in resources),
        'cuda_used':False,'gpu_used':False,'new_training_runs':0,
        'numerical_cases':len(rows),'source_commit':a.CFG['source_commit'],
        'freeze_commit':'6aff41c','implementation_commit':'af999ca',
        'scope':'Conditional finite-error proof plus archived conditioning diagnostics, not arbitrary-width robust scaling.'}
    (a.ROOT/'result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
    print('combined tangent counts',[(x['case'],x['n'],x['counts']) for x in combined])

if __name__=='__main__':
    meter=a.Meter('export tables and conditioning summaries')
    try:finalize()
    finally:meter.finish()
