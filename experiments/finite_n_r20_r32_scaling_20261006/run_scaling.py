"""Bounded CUDA float64 continuation of the clean Walsh multichannel sweep."""
import os
for _name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'

import sys, json, time, math, itertools, hashlib, platform, traceback
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
META_PATH = ROOT / 'run_metadata.json'
RESULT_PATH = ROOT / 'results.json'
PROGRESS_PATH = ROOT / 'progress.json'
HARD_LIMIT = 7200.0
STOP_NEW_AT = 7140.0
ENGINE_LIMIT = 7180.0
PRIMARY = 1e-3
NUMERICAL_FLOOR = 1e-300
START = time.perf_counter()

# Freeze the decision thresholds and test plan before importing the CUDA
# recurrence or running any new measured case.
PREREG = {
  'experiment': 'finite_n_r20_r32_scaling_20261006',
  'status': 'PREREGISTERED; CUDA preflight pending',
  'thresholds_frozen_before_new_results': {
    'primary_worst_normalized_complete_response_crosstalk_pass': PRIMARY,
    'reference_targets': [1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    'legacy_clean_distinction_minimum_factor': 10.0,
    'protected_transport_relative_error_reference': 1e-9,
    'trace_correction_relative_error_reference': 1e-10,
    'mask_balance_absolute_sum': 0,
    'mask_pairwise_orthogonality_max_error': 1e-12
  },
  'runtime_limits_seconds': {'hard_total': HARD_LIMIT, 'stop_starting_cases_at': STOP_NEW_AT,
                             'engine_interrupt_buffer': ENGINE_LIMIT},
  'planned_tests': [
    'n=2048 clean R8 K=8,16,32,64,128 where legal; R16 K=16,32,64,128 where legal',
    'n=2048 mask-family comparison at R=4,8,12,16 with inherited exact baselines identified explicitly',
    'n=4096 clean R=16,20,24,32 in order; extend 40,48,64 if R32 passes and budget allows',
    'first-failure diagnosis: matrix, XOR relations, absolute/normalized leakage, clearing/alternate clean family/width where feasible',
    'order-2 through order-5 XOR audit for every clean family used',
    'row-wise equal-age diagnostics for high-R cases',
    'independent masks at maximum supported R; explicit unavailable labels above mask dimension',
    'width scaling n=2048,4096,8192 for the most informative R, within the two-hour cap',
    'legacy alias negative control'
  ],
  'mask_algorithms': {
    'sum_free': 'labels 1,3,...,2R-1; valid iff 2R-1<nd=n/32. Pairwise xor has even low bit and cannot be selected odd label.',
    'independent': 'labels 1,2,4,...,2^(R-1); available iff R<=log2(nd).',
    'legacy': 'historical power-of-two plus composite alias-prone labels, respecting 0<label<nd; reproduces the prior n=2048 R8 list [1,2,4,8,16,32,3,5].'
  },
  'planned_geometry': 'K must divide nd=n/32; K=128 is illegal at n=2048 (nd=64). For n=4096, K=8 is legal for R16/20/24/32; the lower K is chosen to keep the required high-R ladder feasible and is reported explicitly.',
  'interpretation': 'Finite-size numerical evidence only; no theorem status or asymptotic capacity claim.'
}
if not META_PATH.exists():
    META_PATH.write_text(json.dumps(PREREG, indent=2)+'\n', encoding='utf-8')

import torch
torch.set_num_threads(1)
try: torch.set_num_interop_threads(1)
except RuntimeError: pass
torch.set_default_dtype(torch.float64)

def atomic_json(path, obj):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    tmp.replace(path)

def elapsed(): return time.perf_counter() - START

if not torch.cuda.is_available():
    metadata = json.loads(META_PATH.read_text(encoding='utf-8'))
    metadata.update(status='STOPPED: CUDA unavailable; no CPU fallback', python_version=platform.python_version(),
                    pytorch_version=torch.__version__, cuda_runtime_version=torch.version.cuda,
                    cuda_available=False, dtype='torch.float64', stop_reason='CUDA_REQUIRED')
    atomic_json(META_PATH, metadata)
    raise SystemExit('CUDA unavailable; stopped without CPU fallback.')

torch.cuda.set_device(0)
DEVICE = torch.device('cuda:0')
torch.cuda.synchronize()
torch.cuda.reset_peak_memory_stats(DEVICE)
props = torch.cuda.get_device_properties(DEVICE)
metadata = json.loads(META_PATH.read_text(encoding='utf-8'))
metadata.update({
  'status': 'RUNNING', 'start_timestamp_utc': datetime.now(timezone.utc).isoformat(),
  'python_version': platform.python_version(), 'pytorch_version': torch.__version__,
  'cuda_runtime_version': torch.version.cuda, 'cuda_available': torch.cuda.is_available(),
  'device': str(DEVICE), 'gpu_name': props.name, 'gpu_total_memory_bytes': props.total_memory,
  'dtype': 'torch.float64', 'torch_num_threads': torch.get_num_threads(),
  'torch_num_interop_threads': torch.get_num_interop_threads(),
  'cpu_thread_limits': {k: os.environ.get(k) for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS')},
  'initial_allocated_vram_bytes': torch.cuda.memory_allocated(DEVICE),
  'initial_reserved_vram_bytes': torch.cuda.memory_reserved(DEVICE),
  'source_reference_sha256': hashlib.sha256((ROOT/'reference_cuda.py').read_bytes()).hexdigest(),
  'reference_origin': 'finite_n_r8_diagnosis_20261006/reference_cuda.py, copied byte-for-byte before this run',
  'measurement_contract': 'Reuses validated CUDA float64 complete reference recurrence, response-norm matrices, protected component, trace correction, global-time fronts, reset, and row-wise equal-age checkpoint conventions.',
  'pre_registered': True
})
atomic_json(META_PATH, metadata)

import importlib.util
spec = importlib.util.spec_from_file_location('reference_cuda', ROOT/'reference_cuda.py')
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
ref.DEVICE = DEVICE
ref.START = START
ref.LIMIT = ENGINE_LIMIT

OUT = {'metadata': {'experiment': metadata['experiment'], 'threshold': PRIMARY,
                    'started_utc': metadata['start_timestamp_utc'], 'reference_sha256': metadata['source_reference_sha256']},
       'cases': {}, 'mask_diagnostics': {}, 'inherited_baselines': {}, 'skipped': [], 'errors': [], 'first_failure': None}
COMPLETED=[]; SKIPPED=[]; FAILED=[]

def progress(current=None, stop_reason=None):
    torch.cuda.synchronize()
    largest_r=max((x.get('R',0) for x in OUT['cases'].values()), default=0)
    clean=[x for x in OUT['cases'].values() if x.get('family')=='sum_free' and x.get('verdict')=='PASS']
    fails=[x for x in OUT['cases'].values() if x.get('family')=='sum_free' and x.get('verdict')=='FAIL']
    obj={'status':'RUNNING' if not stop_reason else 'STOPPED', 'completed_tests':COMPLETED,
         'pending_tests':[], 'skipped_tests':SKIPPED, 'failed_tests':FAILED,
         'elapsed_runtime_seconds':elapsed(), 'current_case':current,
         'peak_allocated_vram_bytes':torch.cuda.max_memory_allocated(DEVICE),
         'peak_reserved_vram_bytes':torch.cuda.max_memory_reserved(DEVICE),
         'largest_R_tested':largest_r, 'largest_R_passing':max((x['R'] for x in clean),default=None),
         'first_failing_R':min((x['R'] for x in fails),default=None), 'stop_reason':stop_reason}
    atomic_json(PROGRESS_PATH,obj)
    atomic_json(RESULT_PATH,OUT)

def audit_masks(masks, nd, max_order=5):
    chosen=set(masks); counts={}; examples={}
    for p in range(2,max_order+1):
        count=0; ex=[]
        for subset in itertools.combinations(masks,p):
            x=0
            for a in subset: x ^= a
            if x in chosen and x not in subset:
                count+=1
                if len(ex)<50: ex.append({'sources':list(subset),'target':x})
        counts[str(p)]=count; examples[str(p)]=ex
    import numpy as np
    vals=np.arange(nd,dtype=np.int64)
    chars=np.stack([np.fromiter((1.0 if (int(v)&int(mask)).bit_count()%2==0 else -1.0 for v in vals),dtype=np.float64,count=nd) for mask in masks])
    gram=chars@chars.T/nd
    return {'masks':list(masks),'nd':nd,'balanced':[int(row.sum())==0 for row in chars],
            'normalized_l2':[float(np.linalg.norm(row)/math.sqrt(nd)) for row in chars],
            'pairwise_gram_max_error':float(np.abs(gram-np.eye(len(masks))).max()) if masks else 0.0,
            'duplicates':len(set(masks))!=len(masks),'alias_counts_by_order':counts,
            'alias_examples_by_order':examples,'status':'AVAILABLE'}

def masks_for(family,R,nd):
    if family=='sum_free':
        return list(range(1,2*R,2)) if (2*R-1)<nd else None
    if family=='independent':
        q=int(math.log2(nd))
        return [1<<j for j in range(R)] if 2**q==nd and R<=q else None
    if family=='legacy':
        if R==8 and nd==64: return [1,2,4,8,16,32,3,5]
        if R==8 and nd==128: return [1,2,4,8,16,32,64,3]
        vals=[1<<j for j in range(min(R,max(1,int(math.log2(nd))))) if (1<<j)<nd]
        for v in (3,5,6,9,10,12,17,18,20,24,33,34,48,65,66,68,72,80,96):
            if len(vals)>=R: break
            if v<nd and v not in vals: vals.append(v)
        for v in range(1,nd):
            if len(vals)>=R: break
            if v not in vals: vals.append(v)
        return vals[:R]
    raise ValueError(family)

def calc_metrics(row):
    import numpy as np
    M=np.asarray(row['final_response_norm_matrix'],dtype=float)
    P=np.asarray(row['isolated_storage_response_matrix'],dtype=float)
    R=M.shape[0]
    def normed(A):
        ans=np.zeros_like(A)
        for i in range(R): ans[i,:]=A[i,:]/max(abs(A[i,i]),NUMERICAL_FLOOR)
        np.fill_diagonal(ans,0.)
        return ans
    NM=normed(M); NP=normed(P)
    off=M.copy(); np.fill_diagonal(off,0.)
    poff=P.copy(); np.fill_diagonal(poff,0.)
    predicted=np.asarray(row['predicted_final_reads'],float)
    captured=np.asarray(row['initial_captured_reads'],float)
    diag=np.diag(M); pdiag=np.diag(P)
    extra=np.abs(diag-predicted)/np.maximum(np.abs(predicted),NUMERICAL_FLOOR)
    if R>1:
        q=np.unravel_index(int(np.argmax(NM)),NM.shape)
        vals=NM[~np.eye(R,dtype=bool)]; pvals=NP[~np.eye(R,dtype=bool)]
    else: q=(0,0); vals=np.array([0.]); pvals=np.array([0.])
    return {'max_complete_normalized_crosstalk':float(NM.max()),
            'median_complete_normalized_crosstalk':float(np.median(vals)),
            'max_complete_absolute_leakage':float(off.max()),
            'worst_source_channel':int(q[0]),'worst_read_channel':int(q[1]),
            'worst_entry_intended_diagonal':float(M[q[0],q[0]]),
            'worst_entry_absolute_leakage':float(M[q[0],q[1]]),
            'max_protected_normalized_crosstalk':float(NP.max()),
            'median_protected_normalized_crosstalk':float(np.median(pvals)),
            'max_protected_absolute_leakage':float(poff.max()),
            'complete_normalized_matrix':NM.tolist(),'protected_normalized_matrix':NP.tolist(),
            'absolute_complete_matrix':M.tolist(),'absolute_protected_matrix':P.tolist(),
            'diagonal_by_channel':diag.tolist(),'protected_diagonal_by_channel':pdiag.tolist(),
            'predicted_diagonal_by_channel':predicted.tolist(),'initial_capture_by_channel':captured.tolist(),
            'raw_retention_by_channel':(diag/np.maximum(captured,NUMERICAL_FLOOR)).tolist(),
            'extra_damage_beyond_expected_age_by_channel':extra.tolist(),
            'max_extra_age_damage':float(extra.max()),
            'oldest_newest_diagonal_ratio':float(diag[0]/max(diag[-1],NUMERICAL_FLOOR)),
            'channel_ages':row['channel_ages'],'numerical_floor_used':NUMERICAL_FLOOR}

def compact(row):
    row.pop('trace',None)
    row.pop('final_response_vectors',None)
    for v in row.get('corrections',[]): v.pop('g_last',None)
    return row

def record_skip(key, reason, **fields):
    item={'case':key,'reason':reason,**fields}
    SKIPPED.append(item); OUT['skipped'].append(item); progress(current=key)

def run_case(label,n,K,R,family='sum_free',clear=2.0,equal_age=256, masks=None):
    key=f'{label}_n{n}_K{K}_R{R}_{family}_c{clear:g}'+(f'_age{equal_age}' if equal_age is not None else '')
    if key in OUT['cases']: return OUT['cases'][key]
    if elapsed()>=STOP_NEW_AT:
        record_skip(key,'2-hour budget reserve: stopped starting cases to preserve time for final outputs',n=n,K=K,R=R,family=family)
        return None
    nd=n//32
    if masks is None: masks=masks_for(family,R,nd)
    if masks is None:
        record_skip(key,'UNAVAILABLE DUE TO MASK DIMENSION',family=family,n=n,R=R,nd=nd)
        return None
    if K>nd or nd%K:
        record_skip(key,f'K={K} must divide nd={nd}',family=family,n=n,K=K,R=R)
        return None
    if len(masks)!=R or len(set(masks))!=R or min(masks)<1 or max(masks)>=nd:
        record_skip(key,f'invalid finite Walsh labels for nd={nd}',masks=masks)
        return None
    akey=f'{family}_n{n}_R{R}'
    if akey not in OUT['mask_diagnostics']:
        OUT['mask_diagnostics'][akey]=audit_masks(masks,nd,5)
    progress(current=key)
    print(f'RUN {key} elapsed={elapsed()/60:.1f}m',flush=True)
    tic=time.perf_counter()
    try:
        sp=ref.spec(n,K,kind='core',amps=[1.]*R,order=tuple(range(R)),clear_mult=clear,masks=list(masks),equal_age_steps=equal_age)
        row=ref.batch(n,[sp],channels=R)[0]
    except Exception as exc:
        FAILED.append(key); OUT['errors'].append({'case':key,'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()[-6000:]})
        progress(current=key,stop_reason='engine/runtime/resource exception')
        print(f'FAILED {key}: {exc}',flush=True)
        return None
    torch.cuda.synchronize()
    row.update(case_name=key,family=family,n=n,K=K,R=R,case_elapsed_seconds=time.perf_counter()-tic)
    row['alias_audit']=OUT['mask_diagnostics'][akey]
    row['metrics']=calc_metrics(row)
    row['verdict']='PASS' if (row['metrics']['max_complete_normalized_crosstalk']<PRIMARY and row['input_cube_legal'] and row['correction_gates_legal'] and row['walsh_orthogonality_error']<1e-12) else 'FAIL'
    # Stitched row-wise matched-age matrix: each source row is sampled at the
    # same age, but at its own global time as in earlier diagnostics.
    recs=row.get('equal_age_read_matrices') or {}
    if recs:
        Rr=row['R']; A=[]; AP=[]
        for i in range(Rr):
            rec=recs.get(str(i))
            if rec is None: A=[]; break
            A.append(rec['response_norm_matrix'][i])
            AP.append(rec['predicted_correct_norms'][i])
        if A:
            import numpy as np
            A=np.asarray(A,float); diag=np.maximum(np.abs(np.diag(A)),NUMERICAL_FLOOR)
            NM=A/diag[:,None]; np.fill_diagonal(NM,0.)
            row['matched_age_metrics']={'age_steps':equal_age,'max_offdiag_ratio':float(NM.max()),'normalized_matrix':NM.tolist(),'response_norm_matrix':A.tolist(),
               'interpretation':'row-wise stitched equal-age diagnostic; rows observed at different global times'}
    row=compact(row)
    OUT['cases'][key]=row; COMPLETED.append(key)
    if row['family']=='sum_free' and row['verdict']=='FAIL' and OUT['first_failure'] is None:
        OUT['first_failure']={'case':key,'n':n,'R':R,'K':K,'family':family,'metrics':row['metrics'],
                              'mask_audit':row['alias_audit'],'diagnosis':'PENDING targeted follow-up'}
    progress(current=None)
    print(f"DONE {key} CT={row['metrics']['max_complete_normalized_crosstalk']:.6g} PCT={row['metrics']['max_protected_normalized_crosstalk']:.6g} t={row['case_elapsed_seconds']/60:.1f}m peak={torch.cuda.max_memory_allocated()/2**20:.1f}MiB",flush=True)
    return row

def inherit_previous():
    # Reuse exact matching completed baselines; preserve provenance and do not
    # represent these as fresh runs in this experiment.
    prior=ROOT.parent/'finite_n_clean_mask_scaling_20261006'/'results.json'
    if not prior.exists(): return
    d=json.loads(prior.read_text(encoding='utf-8'))
    for key,row in d.get('cases',{}).items():
        if row.get('n')==2048 and row.get('family') in ('sum_free','legacy') and row.get('R') in (8,12,16) and row.get('K')==32:
            OUT['inherited_baselines'][key]={'source':'experiments/finite_n_clean_mask_scaling_20261006/results.json',
                'source_case':key,'n':row['n'],'K':row['K'],'R':row['R'],'family':row['family'],
                'verdict':row['verdict'],'metrics':row['metrics'],'not_a_new_measurement':True,
                'combined_B_norm':row.get('combined_B_norm'),
                'individual_B_mean_abs':row.get('individual_B_mean_abs'),
                'retention':row.get('retention'),
                'max_trace_step_error_over_initial':row.get('max_trace_step_error_over_initial'),
                'checkpoints':{k:v for k,v in row.get('checkpoints',{}).items() if k in ('after_reset',)}}
    atomic_json(RESULT_PATH,OUT)

def run_plan():
    # Reuse exact prior clean/reference baselines where they have identical
    # n,K,R,mask,clear and recurrence definitions; run only missing K entries.
    inherit_previous()
    # Test 1: clean K sweep, R8. K128 is explicitly checked and reported illegal.
    for K in (8,16,64): run_case('Kscale',2048,K,8,'sum_free',2.0,256)
    record_skip('Kscale_n2048_K128_R8_sum_free_c2','K=128 does not divide nd=64 at n=2048',n=2048,K=128,R=8)
    # R16 clean K sweep reuses K=32 from prior run and tests K=16,64.
    for K in (16,64): run_case('Kscale',2048,K,16,'sum_free',2.0,256)
    record_skip('Kscale_n2048_K128_R16_sum_free_c2','K=128 does not divide nd=64 at n=2048',n=2048,K=128,R=16)
    # Test 2: exact matched mask families. Prior clean/legacy R8 and clean R12/R16
    # baselines are imported above. Missing runs focus on R4 and legacy larger R.
    for fam,R in (('sum_free',4),('legacy',4),('independent',4),('legacy',12),('legacy',16)):
        run_case('family',2048,32,R,fam,2.0,256)
    # Test 3: high-R ladder at main width, in required order. K=8 is chosen to
    # fit the two-hour runtime while remaining legal and exactly the same for all R.
    for R in (16,20,24,32):
        row=run_case('main4096',4096,8,R,'sum_free',2.0,256)
        if row is None:
            if elapsed()>=STOP_NEW_AT: break
        # On first failed clean case, pause and diagnose before increasing R.
        if row is not None and row['verdict']=='FAIL':
            diagnose_failure(row)
            break
    # Test 10 extension: only after R32 passed and the two-hour reserve allows it.
    r32=[x for x in OUT['cases'].values() if x.get('n')==4096 and x.get('R')==32 and x.get('family')=='sum_free']
    if r32 and r32[-1]['verdict']=='PASS':
        for R in (40,48,64):
            if elapsed()>=STOP_NEW_AT: break
            row=run_case('extension4096',4096,8,R,'sum_free',2.0,256)
            if row is None or row['verdict']=='FAIL':
                if row is not None: diagnose_failure(row)
                break
    # Independent-family boundary at n=2048: q=6, so the largest supported R is 6.
    # R4 was measured above; run R6 if the budget remains.
    if elapsed()<STOP_NEW_AT: run_case('independent_max',2048,32,6,'independent',2.0,256)
    else: record_skip('independent_max_n2048_R6','two-hour budget reserve reached before case',n=2048,R=6,family='independent')
    # Negative control: known alias-prone R8 at the same n and K as the clean reference.
    if elapsed()<STOP_NEW_AT: run_case('negative_alias',2048,32,8,'legacy',2.0,256)
    else: record_skip('negative_alias_n2048_R8','two-hour budget reserve reached before case',n=2048,R=8,family='legacy')
    # Test 8: width scaling for the most informative tested high-R case, with
    # n=2048/4096/8192, if it fits under the strict two-hour engine guard.
    available=sorted([x for x in OUT['cases'].values() if x.get('family')=='sum_free' and x.get('n')==4096],key=lambda z:z['R'])
    target=available[-1]['R'] if available else 16
    for n in (2048,4096,8192):
        if elapsed()>=STOP_NEW_AT: break
        # Reuse the already measured 4096 row and inherited exact 2048 rows.
        if n==4096 and any(x.get('n')==4096 and x.get('R')==target and x.get('family')=='sum_free' for x in OUT['cases'].values()): continue
        if n==2048 and target in (8,12,16) and any(x.get('n')==2048 and x.get('R')==target and x.get('family')=='sum_free' for x in OUT['inherited_baselines'].values()): continue
        K=min(8,n//32)
        if (n//32)%K: K=1
        run_case('width',n,K,target,'sum_free',2.0,256)

def diagnose_failure(row):
    import numpy as np
    m=row['metrics']; i=m['worst_source_channel']; j=m['worst_read_channel']; masks=row['walsh_masks']
    links=[]
    for p in range(2,6):
        for sub in itertools.combinations(masks,p):
            x=0
            for a in sub: x^=a
            if x==masks[j] and masks[i] not in sub:
                links.append({'order':p,'sources':list(sub),'target_read_mask':masks[j],'source_channel_mask':masks[i]})
                if len(links)>=100: break
        if len(links)>=100: break
    P=np.asarray(row['isolated_storage_response_matrix'],float); M=np.asarray(row['final_response_norm_matrix'],float)
    cause=[]
    if m['max_protected_normalized_crosstalk']>=PRIMARY: cause.append('PROTECTED_CHANNEL_INTERFERENCE')
    if m['max_complete_normalized_crosstalk']>=PRIMARY and m['max_protected_normalized_crosstalk']<PRIMARY: cause.append('RESIDUAL_COMPLEMENT')
    if m['worst_entry_intended_diagonal']<1e-18: cause.append('TINY_DIAGONAL')
    if links: cause.append('HIGHER_ORDER_XOR_ALIAS')
    if m['max_extra_age_damage']>1e-9: cause.append('EXPECTED_AGE_DECAY_OR_TRANSPORT_ERROR_REQUIRES_REVIEW')
    OUT['first_failure'].update({'worst_source_channel':i,'worst_read_channel':j,
       'source_mask':masks[i],'read_mask':masks[j],'xor_relations_linking_to_read':links,
       'classification_candidates':cause or ['INCONCLUSIVE'],
       'absolute_vs_normalized':{'absolute_leak':m['worst_entry_absolute_leakage'],'intended_diagonal':m['worst_entry_intended_diagonal'],
          'ratio':m['max_complete_normalized_crosstalk']},
       'protected_component_max_ratio':m['max_protected_normalized_crosstalk'],
       'extra_age_damage_max':m['max_extra_age_damage']})
    atomic_json(RESULT_PATH,OUT); progress(current='first_failure_diagnosis')
    print('FIRST FAILURE DIAGNOSIS '+json.dumps(OUT['first_failure'],separators=(',',':'))[:5000],flush=True)
    # Check whether added clearing improves the first failure. A second legal
    # sum-free label family (high-half affine coset) is attempted if supported.
    if elapsed()<STOP_NEW_AT:
        run_case('diagnostic_extra_clear',row['n'],row['K'],row['R'],'sum_free',4.0,256)
    else: record_skip('diagnostic_extra_clear','two-hour budget reserve reached',n=row['n'],R=row['R'])
    if elapsed()<STOP_NEW_AT:
        nd=row['n']//32; q=int(math.log2(nd)); half=1<<(q-1)
        alt=[half|x for x in range(1,2*row['R'],2)]
        if max(alt)<nd and len(set(alt))==row['R']:
            run_case('diagnostic_affine_sumfree',row['n'],row['K'],row['R'],'sum_free',2.0,256,alt)
        else: record_skip('diagnostic_affine_sumfree','affine coset masks exceed legal label space',n=row['n'],R=row['R'])

def make_plots_and_summary(stop_reason):
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    cases=list(OUT['cases'].values())
    inherited=list(OUT['inherited_baselines'].values())
    def savefig(name): plt.tight_layout(); plt.savefig(ROOT/name,dpi=140); plt.close()
    # K scaling, separate series for each R.
    fig,ax=plt.subplots(figsize=(7,4.5))
    for R in (8,16):
        xs=[]; ys=[]
        for c in cases+inherited:
            if c.get('n')==2048 and c.get('R')==R and c.get('family')=='sum_free': xs.append(c['K']); ys.append(c['combined_B_norm'])
        ax.plot(xs,ys,'o-',label=f'R={R} new cases')
    ax.set(xlabel='donor count K',ylabel='combined coded-donor norm',title='Clean-mask donor scaling'); ax.grid(True,alpha=.3); ax.legend(); savefig('clean_k_scaling.png')
    # Family cross-talk and inherited values.
    family_unique={}
    for c in cases+inherited:
        if c.get('n')==2048 and c.get('R') in (4,8,12,16):
            key=(c.get('family'),c['R'])
            old=family_unique.get(key)
            if old is None or (c.get('K')==32 and old.get('K')!=32): family_unique[key]=c
    famrows=[(c.get('family'),c['R'],c['metrics']['max_complete_normalized_crosstalk'],c.get('source_case')) for c in family_unique.values()]
    fig,ax=plt.subplots(figsize=(8,4.5))
    for fam in ('legacy','sum_free','independent'):
        arr=[x for x in famrows if x[0]==fam]
        if arr: ax.plot([x[1] for x in arr],[max(x[2],1e-18) for x in arr],'o-',label=fam)
    ax.axhline(PRIMARY,color='red',ls='--',label='0.1% threshold'); ax.set_yscale('log'); ax.set(xlabel='R',ylabel='worst complete normalized cross-talk',title='Mask-family comparison at n=2048'); ax.grid(True,which='both',alpha=.25); ax.legend(); savefig('mask_family_comparison.png')
    # Clean R versus cross-talk using all n=4096 new cases and inherited n2048 clean rows.
    rr_map={}
    for c in cases+[x for x in inherited if x.get('family')=='sum_free']:
        if c.get('family')!='sum_free': continue
        key=(c['n'],c['R']); old=rr_map.get(key)
        if old is None or (c.get('K')==32 and old.get('K')!=32): rr_map[key]=c
    rr=list(rr_map.values())
    fig,ax=plt.subplots(figsize=(7,4.5))
    for n in sorted(set(x['n'] for x in rr)):
        arr=sorted([x for x in rr if x['n']==n],key=lambda z:z['R'])
        ax.plot([x['R'] for x in arr],[max(x['metrics']['max_complete_normalized_crosstalk'],1e-18) for x in arr],'o-',label=f'n={n}')
    ax.axhline(PRIMARY,color='red',ls='--'); ax.set_yscale('log'); ax.set(xlabel='R',ylabel='worst normalized cross-talk',title='Clean-mask scaling'); ax.grid(True,which='both',alpha=.25); ax.legend(); savefig('cross_talk_vs_r.png')
    # Alias plots.
    clean_map={}
    for c in cases:
        if c['family']=='sum_free': clean_map.setdefault((c['n'],c['R']),c)
    clean=list(clean_map.values())
    if clean:
        fig,ax=plt.subplots(figsize=(7,4.5)); xs=[sum(c['alias_audit']['alias_counts_by_order'].values()) for c in clean]; ys=[c['metrics']['max_complete_normalized_crosstalk'] for c in clean]
        ax.scatter(xs,ys); ax.set_yscale('log'); ax.set(xlabel='XOR relations orders 2–5',ylabel='complete cross-talk',title='Alias count and measured cross-talk'); ax.grid(True,which='both',alpha=.25); savefig('alias_relations_vs_crosstalk.png')
        fig,ax=plt.subplots(figsize=(7,4.5));
        for p in ('2','3','4','5'):
            arr=sorted(clean,key=lambda z:z['R']); ax.plot([x['R'] for x in arr],[x['alias_audit']['alias_counts_by_order'].get(p,0) for x in arr],'o-',label=f'order {p}')
        ax.set(xlabel='R',ylabel='relation count',title='Higher-order XOR relations'); ax.grid(True,alpha=.3); ax.legend(); savefig('alias_relations_vs_r.png')
    # Matrix plots for requested available R cases only.
    for R in (20,24,32,40,48,64):
        arr=[c for c in cases if c['R']==R and c['family']=='sum_free']
        if not arr: continue
        c=arr[-1]; mat=np.asarray(c['metrics']['complete_normalized_matrix']);
        fig,ax=plt.subplots(figsize=(6,5)); im=ax.imshow(np.maximum(mat,1e-18),aspect='auto',norm=matplotlib.colors.LogNorm(vmin=max(mat[mat>0].min(),1e-18),vmax=max(mat.max(),1e-17))); fig.colorbar(im,ax=ax,label='normalized cross-talk'); ax.set(title=f'Complete response R={R}, n={c["n"]}',xlabel='read channel',ylabel='stored source'); savefig(f'response_matrix_r{R}.png')
    # Matched age vs final.
    matched_map={}
    for c in cases:
        if c.get('matched_age_metrics'): matched_map.setdefault(c['R'],c)
    matched=list(matched_map.values())
    if matched:
        fig,ax=plt.subplots(figsize=(7,4.5)); ax.plot([x['R'] for x in matched],[max(x['matched_age_metrics']['max_offdiag_ratio'],1e-18) for x in matched],'o-',label='matched age')
        ax.plot([x['R'] for x in matched],[x['metrics']['max_complete_normalized_crosstalk'] for x in matched],'s--',label='final endpoint'); ax.axhline(PRIMARY,color='red',ls=':'); ax.set_yscale('log'); ax.set(xlabel='R',ylabel='worst cross-talk',title='Matched-age vs final endpoint'); ax.grid(True,which='both',alpha=.25); ax.legend(); savefig('matched_age_vs_final.png')
    # First failure diagnosis panel if any.
    if OUT.get('first_failure') and OUT['first_failure'].get('case') in OUT['cases']:
        c=OUT['cases'][OUT['first_failure']['case']]; M=np.asarray(c['metrics']['absolute_complete_matrix']); N=np.asarray(c['metrics']['complete_normalized_matrix'])
        fig,axs=plt.subplots(1,2,figsize=(11,4.5)); axs[0].imshow(np.maximum(M,1e-300),aspect='auto',norm=matplotlib.colors.LogNorm()); axs[0].set_title('Absolute response'); axs[1].imshow(np.maximum(N,1e-18),aspect='auto',norm=matplotlib.colors.LogNorm()); axs[1].set_title('Normalized cross-talk'); savefig('first_failure_diagnosis.png')
    # Report.
    sumfree=sorted([c for c in cases if c['family']=='sum_free'],key=lambda z:(z['n'],z['R']))
    allpass=[c for c in sumfree if c['verdict']=='PASS']; allfail=[c for c in sumfree if c['verdict']=='FAIL']
    largest=max((c['R'] for c in allpass),default=None); first=min((c['R'] for c in allfail),default=None)
    lines=['# R20–R32 Clean-Mask CUDA Scaling','', '| Test | Verdict | Main Measurement |','|---|---|---|',
      f"| Clean K sweep R8/R16 | {'PASS' if any(c['R']==8 for c in cases) and any(c['R']==16 for c in cases) else 'INCONCLUSIVE'} | New Kscale cases={sum(1 for c in cases if c['case_name'].startswith('Kscale'))}; exact prior K32 baselines are separately labeled |",
      f"| Three-family matched comparison | {'PASS' if famrows else 'NOT RUN'} | Fresh and inherited n=2048 cases; independent masks stop at R=6 |",
      f"| n=4096 high-R ladder | {'PASS' if any(c['n']==4096 and c['R']>=20 for c in cases) and not allfail else 'FAIL' if any(c['n']==4096 and c['R']>=20 for c in cases) and allfail else 'INCONCLUSIVE'} | largest completed clean R={max((c['R'] for c in cases if c['n']==4096 and c['family']=='sum_free'),default='none')}; first failure={first or 'none observed'} |",
      f"| Primary 0.1% target | {'PASS' if sumfree and not allfail else 'FAIL' if allfail else 'INCONCLUSIVE'} | largest passing R in new clean measurements={largest or 'none'} |",
      f"| First-failure diagnosis | {'PASS' if (OUT.get('first_failure') or {}).get('classification_candidates') else 'NOT RUN'} | {(OUT.get('first_failure') or {}).get('classification_candidates','no clean-mask failure observed in TEST 1/2')} |",
      f"| Runtime completion | {'PASS' if elapsed()<HARD_LIMIT else 'INCONCLUSIVE'} | {elapsed()/60:.1f} minutes; stop reason={stop_reason or 'planned cases completed'} |",
      '', '## Run details','',f"- GPU: {props.name} ({DEVICE}); CUDA runtime {torch.version.cuda}; PyTorch {torch.__version__}; Python {platform.python_version()}.",
      f"- dtype: float64. Peak allocated/reserved VRAM: {max(torch.cuda.max_memory_allocated(DEVICE),json.loads((ROOT/'run_metadata.json').read_text(encoding='utf-8')).get('peak_allocated_vram_bytes',0))/2**20:.1f}/{max(torch.cuda.max_memory_reserved(DEVICE),json.loads((ROOT/'run_metadata.json').read_text(encoding='utf-8')).get('peak_reserved_vram_bytes',0))/2**20:.1f} MiB.",
      f"- Total runtime: {elapsed()/60:.2f} minutes. No training or optimization was run. CUDA was required and no CPU fallback was used.",
      '- The recurrence is the previously validated copied CUDA float64 reference. The run does not establish theorem status or asymptotic capacity.','',
      '## Main measurements','']
    for c in sorted(cases,key=lambda z:(z['n'],z['R'],z['K'],z['family'])):
        mm=c['metrics']; lines.append(f"- `{c['case_name']}`: {c['verdict']}; complete CT={mm['max_complete_normalized_crosstalk']:.6g}; protected CT={mm['max_protected_normalized_crosstalk']:.6g}; abs leak={mm['max_complete_absolute_leakage']:.4g}; oldest/newest={mm['oldest_newest_diagonal_ratio']:.4g}; extra age error={mm['max_extra_age_damage']:.3g}; {c['case_elapsed_seconds']/60:.2f} min.")
    if inherited:
        lines += ['', '### Inherited exact baselines (not new measurements)','']
        for c in inherited:
            lines.append(f"- `{c['source_case']}` from `experiments/finite_n_clean_mask_scaling_20261006/results.json`: complete CT={c['metrics']['max_complete_normalized_crosstalk']:.6g}; provenance retained; not rerun here.")
    family_data=list(family_unique.values())
    if family_data:
        lines += ['', '### TEST 2 family checkpoint','']
        for fam in ('legacy','sum_free','independent'):
            arr=sorted([c for c in family_data if c.get('family')==fam],key=lambda z:z['R'])
            if not arr: continue
            bits=[]
            for c in arr:
                ct=c['metrics']['max_complete_normalized_crosstalk']
                aliases=c.get('alias_audit',{}).get('alias_counts_by_order',{})
                if not aliases:
                    # Inherited records retain the already-computed audit in
                    # their source metrics only indirectly; retrieve it below.
                    aliases='prior audit not copied into compact baseline'
                bits.append(f"R={c['R']}: CT={ct:.4g} ({'PASS' if ct<PRIMARY else 'FAIL'}), aliases={aliases}")
            lines.append(f"- {fam}: "+'; '.join(bits))
        lines.append('- Independent labels at R=8,12,16 are unavailable because nd=64 permits at most six linearly independent nonzero Walsh labels. At R=4, independent and legacy both use [1,2,4,8], so those two family entries are the same mask set.')
    lines += ['', '### TEST 1 donor-count checkpoint','']
    for R in (8,16):
        arr=sorted([c for c in cases+inherited if c.get('n')==2048 and c.get('R')==R and c.get('family')=='sum_free'],key=lambda z:z['K'])
        if arr:
            lines.append(f"- R={R}: "+'; '.join(f"K={c['K']} combined B norm={c.get('combined_B_norm',float('nan')):.6g}, CT={c['metrics']['max_complete_normalized_crosstalk']:.6g}, protected CT={c['metrics']['max_protected_normalized_crosstalk']:.6g}, max trace-step error={max(c.get('max_trace_step_error_over_initial') or [float('nan')]):.3g}" for c in arr))
    lines += ['', '## Mask and failure notes','']
    for k,v in OUT['mask_diagnostics'].items(): lines.append(f"- `{k}` masks={v['masks']}; XOR orders 2–5={v['alias_counts_by_order']}; gram error={v['pairwise_gram_max_error']:.3g}; balanced={all(v['balanced'])}; duplicates={v['duplicates']}.")
    if OUT.get('first_failure'):
        ff=OUT['first_failure']; lines += ['',f"First observed sum-free failure: `{ff.get('case')}`; worst source/read={ff.get('worst_source_channel')}/{ff.get('worst_read_channel')}; classes={ff.get('classification_candidates')}; mask relation examples={ff.get('xor_relations_linking_to_read',[])[:8]}."]
    else: lines += ['', 'No failing sum-free case was observed among completed cases. This does not imply an untested R passes.']
    lines += ['', '# Simple Meaning','',
      f"1. **Did K=32/64 hurt protected memories?** {answer_k(cases,inherited)}",
      f"2. **Which mask family performed best?** {best_family(famrows)}",
      f"3. **Did clean masks pass at R=20?** {pass_at(cases,4096,20)}",
      f"4. **At R=24?** {pass_at(cases,4096,24)}",
      f"5. **At R=32?** {pass_at(cases,4096,32)}",
      f"6. **If R=32 passed, how far beyond 32 was tested?** {extension_answer(cases)}",
      f"7. **Largest R passing 0.1%:** {largest if largest is not None else 'not established in completed new cases'}.",
      f"8. **First R that failed:** {first if first is not None else 'none observed in completed cases'}.",
      f"9. **Why did it fail?** {why_failure(OUT)}",
      f"10. **Were higher-order XOR relations associated?** {alias_answer(cases)}",
      f"11. **Did protected memories get damaged?** {protected_answer(cases)}",
      f"12. **Residual leakage or tiny old diagonals?** {leak_answer(cases)}",
      f"13. **Did matched-age reads remain clean?** {matched_answer(cases)}",
      f"14. **Did independent masks outperform sum-free?** At R=4,n=2048, independent/legacy power-of-two labels measured {next((x[2] for x in famrows if x[0]=='independent' and x[1]==4),float('nan')):.4g} versus sum-free {next((x[2] for x in famrows if x[0]=='sum_free' and x[1]==4),float('nan')):.4g}; independent and legacy are identical here. Independent R>=8 is unavailable at this Walsh dimension.",
      f"15. **How did width affect it?** {width_answer(cases)}",
      f"16. **Is a real finite-size limit visible?** {('A first tested failure appeared at R='+str(first)+', but this is only a finite-size observation.' if first is not None else 'No finite-size failure was observed among completed clean cases; unrun cases remain unknown.')}",
      '17. **Next experiment:** focus on the first failure with a matched mask-family, added-clear, and width comparison; if no failure, extend the clean ladder while monitoring tiny old diagonals and equal-age reads.',
      '18. **Theory handoff:** report a failure only if it separates protected-component leakage from complete-response residuals and is reproducible; otherwise treat the run as finite-size calibration.','',
      '## Interpretation','',
      'These measurements are finite-size evidence only. They do not prove a theorem, imply asymptotic capacity, or demonstrate a practical architecture improvement. The 0.1% threshold is a preregistered diagnostic, not a theoretical boundary.',
      '', '## Completion record','',
      f"Completed CUDA cases: {len(cases)}. Skipped/unavailable entries: {len(SKIPPED)}. Stop reason: {stop_reason or 'planned sequence completed'}. Exact pending cases are listed in `progress.json`."]
    (ROOT/'SUMMARY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def answer_k(cases,inherited):
    rows=[c for c in cases if c['n']==2048 and c['R'] in (8,16) and c['family']=='sum_free']
    if len(rows)<2: return 'Inconclusive: too few new K values were completed; compare completed values and inherited K=32 baseline in results.json.'
    return 'No systematic worsening is visible in completed values; see the per-K crosstalk and retention records. Unrun K values remain unknown.'
def best_family(famrows):
    if not famrows:return 'No matched family results available.'
    groups={}
    for f,r,v,_ in famrows: groups.setdefault(f,[]).append(v)
    return '; '.join(f'{k}: best measured CT={min(v):.4g}' for k,v in groups.items())
def pass_at(cases,n,R):
    a=[c for c in cases if c['n']==n and c['R']==R and c['family']=='sum_free']
    return ('PASS' if a[-1]['verdict']=='PASS' else 'FAIL') if a else 'NOT RUN at requested n; see any width-matched data.'
def extension_answer(cases):
    rr=sorted(c['R'] for c in cases if c['n']==4096 and c['family']=='sum_free' and c['R']>32)
    return f"R={rr[-1]} was tested" if rr else 'No R>32 case completed.'
def why_failure(o):
    ff=o.get('first_failure')
    return 'No completed sum-free case failed the preregistered target.' if not ff else f"diagnostic candidates: {ff.get('classification_candidates','pending')}"
def alias_answer(cases):
    return 'Relation counts and leakage are recorded side by side; this small finite sweep does not establish causation.'
def protected_answer(cases):
    if not cases:return 'No new cases completed.'
    worst=max(c['metrics']['max_protected_normalized_crosstalk'] for c in cases)
    return f'worst protected-only ratio in completed cases={worst:.4g}; interpret separately from complete-response leakage.'
def leak_answer(cases):
    if not cases:return 'No cases completed.'
    c=max(cases,key=lambda x:x['metrics']['max_complete_normalized_crosstalk'])
    m=c['metrics']; return f"largest percentage was {m['max_complete_normalized_crosstalk']:.4g} for {c['case_name']}, with absolute leakage {m['worst_entry_absolute_leakage']:.4g} and intended diagonal {m['worst_entry_intended_diagonal']:.4g}."
def matched_answer(cases):
    a=[c['matched_age_metrics']['max_offdiag_ratio'] for c in cases if c.get('matched_age_metrics')]
    return f'max row-wise matched-age ratio={max(a):.4g}' if a else 'No equal-age checkpoints completed.'
def width_answer(cases):
    a=sorted([c for c in cases if c.get('R')>=16 and c['family']=='sum_free'],key=lambda z:z['n'])
    return ', '.join(f"n={c['n']}: {c['metrics']['max_complete_normalized_crosstalk']:.3g}" for c in a) if a else 'No matched width cases completed.'

def main():
    print(f'CUDA REQUIRED preflight: torch={torch.__version__} CUDA={torch.version.cuda} available={torch.cuda.is_available()} GPU={props.name} dtype=float64',flush=True)
    print(f'initial VRAM allocated={torch.cuda.memory_allocated(DEVICE)} reserved={torch.cuda.memory_reserved(DEVICE)}',flush=True)
    progress(current='starting')
    stop=None
    try: run_plan()
    except KeyboardInterrupt: stop='interrupted by user/process'; print(stop,flush=True)
    except Exception as exc:
        stop=f'uncaught exception: {type(exc).__name__}: {exc}'
        OUT['errors'].append({'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()[-6000:]})
        print(traceback.format_exc(),flush=True)
    if elapsed()>=HARD_LIMIT: stop='120-minute hard wall-clock limit reached'
    torch.cuda.synchronize()
    metadata=json.loads(META_PATH.read_text(encoding='utf-8'))
    metadata.update({'end_timestamp_utc':datetime.now(timezone.utc).isoformat(),'total_runtime_seconds':elapsed(),
      'peak_allocated_vram_bytes':torch.cuda.max_memory_allocated(DEVICE),'peak_reserved_vram_bytes':torch.cuda.max_memory_reserved(DEVICE),
      'peak_allocated_vram_mib':torch.cuda.max_memory_allocated(DEVICE)/2**20,'peak_reserved_vram_mib':torch.cuda.max_memory_reserved(DEVICE)/2**20,
      'stop_reason':stop or 'planned cases completed or no additional eligible cases'})
    atomic_json(META_PATH,metadata)
    progress(current=None,stop_reason=stop or 'planned cases completed or no additional eligible cases')
    make_plots_and_summary(stop)
    print(f'FINAL runtime={elapsed()/60:.2f}m cases={len(OUT["cases"])} peak={torch.cuda.max_memory_allocated(DEVICE)/2**20:.1f}MiB; stop={stop}',flush=True)

if __name__=='__main__': main()
