from pathlib import Path
import hashlib, json, platform, shutil, subprocess, sys
out = Path(__file__).resolve().parent
exp = out.parent
src = exp / 'run_scaling.py'
ref_src = exp / 'reference_cuda.py'
text = src.read_text(encoding='utf-8')
needle = 'if not META_PATH.exists():\n'
assert text.count(needle) == 1
scope_insert = "PREREG['authorized_scope'] = {\n  'scope': 'MAIN-25 TEST3 only; no TEST1/TEST2 rerun and no TEST4-10 or extension runs',\n  'authorized_on': '2026-10-22',\n  'conditions': [{'n':4096,'K':8,'R':R,'family':'sum_free','clear_mult':2.0,'equal_age_steps':256} for R in (16,20,24,32)],\n  'notes': 'The conditional R=40/48/64 extension is outside TEST3 and was not authorized. Scientific thresholds and recurrence are unchanged.'\n}\n" + needle
text = text.replace(needle, scope_insert, 1)
start = text.index('def run_plan():')
end = text.index('def diagnose_failure', start)
new_plan = '''def run_plan():
    # Scoped owner authorization: MAIN-25 TEST3 only. Preserve the registered
    # R order and stop at the first failure. No other protocol stages are run.
    OUT['test3_status'] = 'RUNNING'
    OUT['test3_pending_R'] = [16,20,24,32]
    for R in (16,20,24,32):
        row=run_case('main4096',4096,8,R,'sum_free',2.0,256)
        if row is None:
            OUT['test3_status'] = 'INCOMPLETE_RUN_ERROR_OR_BUDGET'
            break
        OUT['test3_pending_R'].remove(R)
        if row['verdict']=='FAIL':
            diagnose_failure(row)
            OUT['test3_status'] = 'STOPPED_AT_FIRST_FAILURE'
            break
    else:
        OUT['test3_status'] = 'COMPLETED_ALL_REGISTERED_TEST3_CASES'

'''
text = text[:start] + new_plan + text[end:]
a = text.index('    # Check whether added clearing')
b = text.index('def make_plots_and_summary', a)
text = text[:a] + "    OUT['first_failure']['followup_simulations'] = 'NOT RUN: outside the owner-authorized TEST3 scope'\n    atomic_json(RESULT_PATH,OUT)\n\n" + text[b:]
old = '    make_plots_and_summary(stop)\n'
assert text.count(old) == 1
text = text.replace(old, '    # Full-battery report generation is omitted; TEST3 report is written after verification.\n', 1)
(out / 'run_test3.py').write_text(text, encoding='utf-8')
shutil.copyfile(ref_src, out / 'reference_cuda.py')
try:
    torch_ver = subprocess.check_output([sys.executable, '-c', 'import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available())'], text=True).strip().splitlines()
except Exception as e:
    torch_ver = [f'preflight failed: {e}']
config = {
 'experiment_id':'MAIN-25 TEST3', 'date':'2026-10-22',
 'source_snapshot_commit':subprocess.check_output(['git','-C',str(exp.parents[1]),'rev-parse','HEAD'],text=True).strip(),
 'protocol_source':'../run_metadata.json and ../run_scaling.py; copied recurrence source ../reference_cuda.py',
 'registered_conditions':[{'n':4096,'K':8,'R':r,'family':'sum_free','clear_mult':2.0,'equal_age_steps':256,'labels':list(range(1,2*r,2))} for r in (16,20,24,32)],
 'thresholds_unchanged':{'max_complete_normalized_crosstalk_strictly_below':1e-3,'input_cube_legal':True,'correction_gates_legal':True,'walsh_orthogonality_error_strictly_below':1e-12,'mask_balance_abs_sum':0,'pairwise_orthogonality_max_error':1e-12,'protected_transport_relative_error_reference':1e-9,'trace_correction_relative_error_reference':1e-10},
 'controls_and_comparators':{'MAIN25_TEST1_2':'existing n=2048 results are read-only comparisons; no conditions rerun','MAIN21':'n=2048 R16/20/24/32 comparison is not width-matched and is descriptive only'},
 'scope_exclusions':['TEST4-10','R40/R48/R64 conditional extension','all MAIN21 conditions','all model training'],
 'resource_limits':{'gpu':'NVIDIA RTX 3060 CUDA float64 required','temperature_target_c':81,'stop_above_c':86,'vram_limit_mib':10240,'torch_threads':1,'inter_op_threads':1,'OMP_NUM_THREADS':1,'MKL_NUM_THREADS':1,'OPENBLAS_NUM_THREADS':1,'NUMEXPR_NUM_THREADS':1,'registered_hard_runtime_seconds':7200},
 'environment_preflight':{'python':platform.python_version(),'torch':torch_ver,'platform':platform.platform()},
 'source_sha256':{'registered_runner':hashlib.sha256(src.read_bytes()).hexdigest(),'test3_runner':hashlib.sha256((out/'run_test3.py').read_bytes()).hexdigest(),'registered_reference':hashlib.sha256(ref_src.read_bytes()).hexdigest(),'copied_reference':hashlib.sha256((out/'reference_cuda.py').read_bytes()).hexdigest()},
 'method_changes':'Only execution scope/output location changed: TEST3 R16/20/24/32 cases selected; recurrence, metrics, masks, controls, and thresholds retained. Original files are not written. The failure branch retains same-case diagnostics but suppresses extra simulations outside authorized scope.'
}
(out/'test3_config.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'config':str(out/'test3_config.json'),'test3_runner_sha256':config['source_sha256']['test3_runner'],'reference_sha256':config['source_sha256']['copied_reference'],'python':config['environment_preflight']},indent=2))
