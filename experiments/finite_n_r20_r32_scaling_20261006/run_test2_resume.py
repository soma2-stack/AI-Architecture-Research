"""Resume only the unfinished final TEST 2 case and stop before TEST 3."""
import os
for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
import json, time, importlib.util
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
META_PATH=ROOT/'run_metadata.json'; RESULT_PATH=ROOT/'results.json'; PROGRESS_PATH=ROOT/'progress.json'
old_meta=json.loads(META_PATH.read_text(encoding='utf-8'))
old_start=old_meta['start_timestamp_utc']
old_results=json.loads(RESULT_PATH.read_text(encoding='utf-8'))
old_progress=json.loads(PROGRESS_PATH.read_text(encoding='utf-8'))
prior_path=ROOT.parent/'finite_n_clean_mask_scaling_20261006'/'results.json'
prior=json.loads(prior_path.read_text(encoding='utf-8')) if prior_path.exists() else {'cases':{}}
old_progress.update(status='RESUMING_TEST_2_ONLY',current_case='family_n2048_K32_R16_legacy_c2_age256',
                     stop_reason=None, note='User-directed checkpoint: finish TEST 2 only; do not start TEST 3.')
PROGRESS_PATH.write_text(json.dumps(old_progress,indent=2)+'\n',encoding='utf-8')

spec=importlib.util.spec_from_file_location('r20_scaling',ROOT/'run_scaling.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
# Restore the experiment-wide start and all checkpoints after module preflight.
metadata=json.loads(META_PATH.read_text(encoding='utf-8'))
metadata['start_timestamp_utc']=old_start
metadata['status']='RUNNING - RESUMED TEST 2 ONLY'
metadata['resume_note']='The first runner was stopped mid-case when the user narrowed scope. All completed cases were retained; only the unfinished R16 legacy case is resumed. TEST 3 and later tests are disabled.'
META_PATH.write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
m.OUT=old_results
m.COMPLETED=list(old_results.get('cases',{}).keys())
m.SKIPPED=list(old_progress.get('skipped_tests',[]))
m.FAILED=list(old_progress.get('failed_tests',[]))
# Restore donor-scaling fields for exact inherited K=32 baseline points.
for key, base in m.OUT.get('inherited_baselines',{}).items():
    src=prior.get('cases',{}).get(base.get('source_case'))
    if src:
        for field in ('combined_B_norm','individual_B_mean_abs','retention','max_trace_step_error_over_initial'):
            if field in src: base[field]=src[field]
m.START=time.perf_counter()-(datetime.now(timezone.utc)-datetime.fromisoformat(old_start)).total_seconds()
m.ref.START=m.START
m.ref.LIMIT=7180.0
m.OUT.setdefault('aborted_partial_attempts',[]).append({
    'case':'family_n2048_K32_R16_legacy_c2_age256',
    'reason':'The previous process was stopped before this case completed so no TEST 3 case could start automatically.',
    'completed_measurement_discarded':False,
    'partial_cuda_state_saved':False,
    'resume_policy':'Only this incomplete case is recomputed; all completed cases are loaded from results.json.'
})
# Record unavailable independent sets explicitly for the n=2048 family matrix.
for R in (8,12,16):
    key=f'independent_n2048_R{R}'
    if not any(x.get('case')==key for x in m.SKIPPED):
        item={'case':key,'reason':'UNAVAILABLE DUE TO MASK DIMENSION','family':'independent','n':2048,'R':R,'nd':64,'maximum_independent_R':6}
        m.SKIPPED.append(item); m.OUT.setdefault('skipped',[]).append(item)

row=m.run_case('family',2048,32,16,'legacy',2.0,256)
if row is None:
    stop='TEST 2 final legacy R16 did not complete (runtime/resource guard).'
else:
    stop='Stopped immediately after TEST 2 per user instruction; TEST 3 and later tests were not run.'
    # The prior legacy R8 baseline and this R16 case expose the intentional
    # alias-prone family; only powers-of-two R4 is alias-free and overlaps the
    # independent family.
metadata=json.loads(META_PATH.read_text(encoding='utf-8'))
import torch
torch.cuda.synchronize()
metadata.update({'start_timestamp_utc':old_start,'end_timestamp_utc':datetime.now(timezone.utc).isoformat(),
    'status':'STOPPED AFTER TEST 2','total_runtime_seconds':m.elapsed(),
    'peak_allocated_vram_bytes':torch.cuda.max_memory_allocated(0),
    'peak_reserved_vram_bytes':torch.cuda.max_memory_reserved(0),
    'peak_allocated_vram_mib':torch.cuda.max_memory_allocated(0)/2**20,
    'peak_reserved_vram_mib':torch.cuda.max_memory_reserved(0)/2**20,
    'stop_reason':stop,'scope_change':'No TEST 3 or later case was launched.'})
META_PATH.write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
m.progress(current=None,stop_reason=stop)
m.make_plots_and_summary(stop)
# Make the pending-work ledger explicit in progress.json after the summary is saved.
pr=json.loads(PROGRESS_PATH.read_text(encoding='utf-8'))
pr['status']='STOPPED AFTER TEST 2'
pr['pending_tests']=['TEST 3: n=4096 clean R=16,20,24,32','TEST 4–10: failure diagnosis, XOR comparison, width scaling, negative control, optional R=40/48/64']
pr['stop_reason']=stop
pr['completed_scope']='TEST 1 and TEST 2 only'
pr['scope_change']='User explicitly directed stop before TEST 3.'
PROGRESS_PATH.write_text(json.dumps(pr,indent=2)+'\n',encoding='utf-8')
print(f'TEST 2 ONLY COMPLETE: row={row is not None}; elapsed={m.elapsed()/60:.2f} min; stop={stop}',flush=True)
