from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
repo = ROOT.parents[2]
run = json.loads((ROOT / 'results.json').read_text(encoding='utf-8'))
old_main25 = json.loads((PARENT / 'results.json').read_text(encoding='utf-8'))
main21 = json.loads((repo / 'experiments/finite_n_clean_mask_scaling_20261006/continuation_20261022/results.json').read_text(encoding='utf-8'))
manifest = json.loads((ROOT / 'original_inputs_sha256.json').read_text(encoding='utf-8'))
rows=[]
for key,row in run['cases'].items():
    M=np.asarray(row['final_response_norm_matrix'],dtype=np.float64)
    P=np.asarray(row['isolated_storage_response_matrix'],dtype=np.float64)
    d=np.maximum(np.abs(np.diag(M)),1e-300)
    pd=np.maximum(np.abs(np.diag(P)),1e-300)
    NM=M/d[:,None]; NP=P/pd[:,None]
    np.fill_diagonal(NM,0.0); np.fill_diagonal(NP,0.0)
    rec_ct=float(np.max(NM)); rec_pct=float(np.max(NP))
    old=old_main25.get('inherited_baselines',{})
    baseline=None
    if row['R']==16:
        baseline=next((v for v in old.values() if v.get('n')==2048 and v.get('K')==32 and v.get('R')==16 and v.get('family')=='sum_free'),None)
        baseline_src='MAIN-25 inherited n=2048,K=32,R=16 TEST2 baseline (not rerun)'
    else:
        baseline=next((v for v in main21.get('cases',{}).values() if v.get('n')==2048 and v.get('R')==row['R'] and v.get('family')=='sum_free' and v.get('clear_mult')==2.0),None)
        baseline_src='MAIN-21 completed n=2048,K=32 comparison; not width/K matched'
    bct=baseline.get('metrics',{}).get('max_complete_normalized_crosstalk') if baseline else None
    trace_errors=row.get('max_trace_step_error_over_initial') or []
    masks=row['alias_audit']
    hashes_unchanged=True
    for name,expected in manifest.items():
        if hashlib.sha256((PARENT/name).read_bytes()).hexdigest().upper()!=expected.upper():
            hashes_unchanged=False
    rows.append({
      'case':key,'n':row['n'],'m':row['m'],'K':row['K'],'R':row['R'],'mask_family':row['family'],'clear_mult':row['clear_mult'],'equal_age_steps':row['equal_age_steps'],
      'registered_verdict':row['verdict'],'independently_recomputed_complete_ct':rec_ct,'stored_complete_ct':row['metrics']['max_complete_normalized_crosstalk'],'complete_ct_abs_difference':abs(rec_ct-row['metrics']['max_complete_normalized_crosstalk']),
      'independently_recomputed_protected_ct':rec_pct,'stored_protected_ct':row['metrics']['max_protected_normalized_crosstalk'],'protected_ct_abs_difference':abs(rec_pct-row['metrics']['max_protected_normalized_crosstalk']),
      'criterion_threshold':1e-3,'criterion_pass':rec_ct<1e-3 and row['input_cube_legal'] and row['correction_gates_legal'] and row['walsh_orthogonality_error']<1e-12,
      'absolute_complete_leakage_max':row['metrics']['max_complete_absolute_leakage'],'oldest_to_newest_diagonal_ratio':row['metrics']['oldest_newest_diagonal_ratio'],'oldest_channel_retention_fraction':row['metrics']['raw_retention_by_channel'][0],'newest_channel_retention_fraction':row['metrics']['raw_retention_by_channel'][-1],
      'matched_age_max_offdiag_ratio':row.get('matched_age_metrics',{}).get('max_offdiag_ratio'),'max_extra_age_damage':row['metrics']['max_extra_age_damage'],
      'mask_balance_all_rows':all(masks['balanced']),'mask_pairwise_gram_max_error':masks['pairwise_gram_max_error'],'xor_alias_counts_orders_2_to_5':masks['alias_counts_by_order'],
      'input_cube_legal':row['input_cube_legal'],'correction_gates_legal':row['correction_gates_legal'],'walsh_orthogonality_error':row['walsh_orthogonality_error'],'walsh_row_sum_max':row['walsh_row_sum_max'],'probe_orthogonality_error':row['probe_orthogonality_error'],'max_trace_step_error_over_initial':max(trace_errors) if trace_errors else None,'donor_trace_match_error':row['donor_trace_match_error'],'max_absolute_raw_input':row['max_absolute_raw_input'],
      'total_steps':row['total_steps'],'mT':row['mT'],'case_elapsed_seconds':row['case_elapsed_seconds'],'cuda_peak_allocated_mib_case_context':None,
      'baseline_ct':bct,'baseline_source':baseline_src,'baseline_is_matched':False,'original_files_hashes_unchanged_after_run':hashes_unchanged
    })
config=json.loads((ROOT/'test3_config.json').read_text(encoding='utf-8'))
telemetry=[]
with (ROOT/'gpu_telemetry.csv').open(encoding='utf-8') as f:
    next(f,None)
    for line in f:
        p=line.strip().split(',')
        if len(p)>=5:
            try: telemetry.append({'temperature_c':float(p[1]),'memory_used_mib':float(p[2]),'memory_total_mib':float(p[3]),'gpu_utilization_pct':float(p[4])})
            except ValueError: pass
report={
 'verification_date':'2026-10-22','run_status':run.get('test3_status'),'pending_R':run.get('test3_pending_R'),'completed_cases':len(run.get('cases',{})),'failed_or_aborted_cases':run.get('failed_cases',[]),'runner_errors':run.get('errors',[]),
 'all_complete_metric_recomputations_match':all(x['complete_ct_abs_difference']<1e-15 and x['protected_ct_abs_difference']<1e-15 for x in rows),
 'all_completed_cases_pass_registered_threshold':all(x['criterion_pass'] for x in rows),
 'original_inputs_hashes_unchanged_after_run':all(x['original_files_hashes_unchanged_after_run'] for x in rows),
 'cases':rows,'resource_summary':{
   'wall_runtime_seconds':json.loads((ROOT/'run_metadata.json').read_text(encoding='utf-8')).get('total_runtime_seconds'),
   'per_case_seconds':{x['case']:x['case_elapsed_seconds'] for x in rows},
   'runner_peak_allocated_vram_mib':json.loads((ROOT/'run_metadata.json').read_text(encoding='utf-8')).get('peak_allocated_vram_mib'),
   'runner_peak_reserved_vram_mib':json.loads((ROOT/'run_metadata.json').read_text(encoding='utf-8')).get('peak_reserved_vram_mib'),
   'torch_threads':json.loads((ROOT/'run_metadata.json').read_text(encoding='utf-8')).get('torch_num_threads'),
   'telemetry_sample_count':len(telemetry),'telemetry_max_temperature_c':max((x['temperature_c'] for x in telemetry),default=None),'telemetry_max_total_vram_used_mib':max((x['memory_used_mib'] for x in telemetry),default=None),'telemetry_max_gpu_utilization_pct':max((x['gpu_utilization_pct'] for x in telemetry),default=None)
 },
 'scope_verdict':'INCONCLUSIVE: R16/R20/R24 completed and pass; R32 was started in order but interrupted by the registered runtime guard before a complete result was saved.',
 'interpretation':'Finite float64 recurrence evidence only. The very small oldest/newest diagonal ratios mean low normalized cross-talk does not establish usable oldest-channel recall. No theorem or trained-model claim follows.'
}
(ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['run_status','pending_R','completed_cases','all_complete_metric_recomputations_match','all_completed_cases_pass_registered_threshold','original_inputs_hashes_unchanged_after_run','resource_summary','cases']},indent=2))
