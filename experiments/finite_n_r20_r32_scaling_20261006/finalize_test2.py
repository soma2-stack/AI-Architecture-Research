"""Regenerate TEST 1/2 plots and checkpoint report without running CUDA cases."""
import os, json, time, importlib.util
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent
META=ROOT/'run_metadata.json'; RESULTS=ROOT/'results.json'; PROGRESS=ROOT/'progress.json'
old_meta=json.loads(META.read_text(encoding='utf-8'))
old_results=json.loads(RESULTS.read_text(encoding='utf-8'))
old_progress=json.loads(PROGRESS.read_text(encoding='utf-8'))
old_start=old_meta['start_timestamp_utc']
prior_path=ROOT.parent/'finite_n_clean_mask_scaling_20261006'/'results.json'
prior=json.loads(prior_path.read_text(encoding='utf-8')) if prior_path.exists() else {'cases':{}}
spec=importlib.util.spec_from_file_location('r20_scaling_finalize',ROOT/'run_scaling.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.OUT=old_results
m.START=time.perf_counter()-(datetime.now(timezone.utc)-datetime.fromisoformat(old_start)).total_seconds()
# Restore source diagnostics and K-response fields for inherited exact baselines.
for key,base in m.OUT.get('inherited_baselines',{}).items():
    src=prior.get('cases',{}).get(base.get('source_case'))
    if src:
        # Keep the current result's complete order-2..5 alias audit. The
        # inherited source only recorded orders 2..4, so restoring it here
        # would silently drop the completed order-5 count.
        for field in ('combined_B_norm','individual_B_mean_abs','retention','max_trace_step_error_over_initial'):
            if field in src: base[field]=src[field]
RESULTS.write_text(json.dumps(m.OUT,indent=2,allow_nan=False)+'\n',encoding='utf-8')
stop='Stopped immediately after TEST 2 per user instruction; TEST 3 and later tests were not run.'
m.make_plots_and_summary(stop)
pr=json.loads(PROGRESS.read_text(encoding='utf-8'))
pr.update(status='STOPPED AFTER TEST 2',current_case=None,
    completed_scope='TEST 1 clean K sweeps plus TEST 2 n=2048 mask-family comparisons',
    pending_tests=['TEST 3: n=4096 clean R=16,20,24,32','TEST 4–10: first-failure diagnosis, higher-R alias analysis, width scaling, negative control, and extensions'],
    stop_reason=stop, scope_change='User explicitly directed stop before TEST 3.')
pr['elapsed_runtime_seconds']=m.elapsed()
pr['peak_allocated_vram_bytes']=max(pr.get('peak_allocated_vram_bytes',0),103635456)
pr['peak_reserved_vram_bytes']=max(pr.get('peak_reserved_vram_bytes',0),169869312)
try:
    import torch
    torch.cuda.synchronize()
    pr['peak_allocated_vram_bytes']=max(pr.get('peak_allocated_vram_bytes',0),torch.cuda.max_memory_allocated(0))
    pr['peak_reserved_vram_bytes']=max(pr.get('peak_reserved_vram_bytes',0),torch.cuda.max_memory_reserved(0))
except Exception: pass
PROGRESS.write_text(json.dumps(pr,indent=2)+'\n',encoding='utf-8')
# Preserve the original two-hour experiment start, cumulative runtime and peak
# from the completed runner; the plot-only import is not counted as CUDA work.
meta=json.loads(META.read_text(encoding='utf-8'))
meta.update({'start_timestamp_utc':old_start,'status':'STOPPED AFTER TEST 2',
    'stop_reason':stop,'scope_change':'No TEST 3 or later case was run.',
    'total_runtime_seconds':m.elapsed(),'end_timestamp_utc':datetime.now(timezone.utc).isoformat(),
    'peak_allocated_vram_bytes':max(meta.get('peak_allocated_vram_bytes',0),103635456),
    'peak_reserved_vram_bytes':max(meta.get('peak_reserved_vram_bytes',0),169869312),
    'peak_allocated_vram_mib':max(meta.get('peak_allocated_vram_mib',0),103635456/2**20),
    'peak_reserved_vram_mib':max(meta.get('peak_reserved_vram_mib',0),169869312/2**20)})
META.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
print('TEST 2 plots and checkpoint summary regenerated; no experiment cases run.')
