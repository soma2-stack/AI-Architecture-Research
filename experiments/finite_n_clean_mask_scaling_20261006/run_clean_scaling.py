"""Finite-N clean Walsh mask scaling. CUDA float64 only; no training."""
import os
for _v in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_v] = '1'

import sys, json, time, math, platform, hashlib, uuid, itertools, traceback
from pathlib import Path
from datetime import datetime, timezone

import torch
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.set_default_dtype(torch.float64)

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import reference_cuda as ref

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

START = time.perf_counter()
WALL_LIMIT = 5400.0
OPTIONAL_STOP = 4200.0
VRAM_LIMIT = 6 * 1024**3
ref.LIMIT = WALL_LIMIT
OUT = ROOT
THRESHOLD = 1e-3
NUMERICAL_FLOOR = 1e-300

DATA = {
    'description': 'Finite-size CUDA float64 stress test of clean Walsh mask families; not a proof.',
    'cases': {}, 'mask_diagnostics': {}, 'test_verdicts': {},
    'runtime_seconds': 0.0, 'errors': [], 'skipped': [],
}
COMPLETED, FAILED, SKIPPED = [], [], []
PLANNED = []

def elapsed():
    return time.perf_counter() - START

def atomic_json(path, obj):
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    payload = json.dumps(obj, indent=2, allow_nan=False) + '\n'
    tmp.write_text(payload, encoding='utf-8')
    last = None
    for _ in range(8):
        try:
            os.replace(tmp, path)
            return
        except PermissionError as exc:
            last = exc
            time.sleep(.2)
    try:
        path.write_text(payload, encoding='utf-8')
    except Exception:
        raise last
    try:
        tmp.unlink(missing_ok=True)
    except Exception:
        pass

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save_state(current=None):
    DATA['runtime_seconds'] = elapsed()
    atomic_json(OUT/'results.json', DATA)
    peak_a = int(torch.cuda.max_memory_allocated())
    peak_r = int(torch.cuda.max_memory_reserved())
    completed_cases = list(DATA['cases'])
    clean_pass = [x for x in DATA['cases'].values()
                  if x['family'] != 'legacy' and x['metrics']['max_complete_normalized_crosstalk'] < THRESHOLD]
    first_fail = None
    for R in sorted(set(x['R'] for x in DATA['cases'].values() if x['family'] != 'legacy')):
        group = [x for x in DATA['cases'].values() if x['family'] != 'legacy' and x['R'] == R]
        if group and any(x['metrics']['max_complete_normalized_crosstalk'] >= THRESHOLD for x in group):
            first_fail = R
            break
    prog = {
        'status': 'RUNNING', 'completed_tests': COMPLETED, 'failed_tests': FAILED,
        'skipped_tests': SKIPPED, 'pending_tests': [p for p in PLANNED if p not in COMPLETED and p not in FAILED and p not in SKIPPED],
        'elapsed_runtime_seconds': elapsed(), 'current_test': current,
        'peak_allocated_vram_bytes': peak_a, 'peak_reserved_vram_bytes': peak_r,
        'largest_n_completed': max((x['n'] for x in DATA['cases'].values()), default=0),
        'largest_R_completed': max((x['R'] for x in DATA['cases'].values()), default=0),
        'current_best_passing_R': max((x['R'] for x in clean_pass), default=None),
        'first_failing_R_observed': first_fail,
    }
    atomic_json(OUT/'progress.json', prog)

def family_masks(family, R, nd):
    if family == 'sum_free':
        if R > nd//2:
            return None
        return list(range(1, 2*R, 2))
    if family == 'independent':
        q = int(math.log2(nd))
        if 2**q != nd or R > q:
            return None
        return [1 << j for j in range(R)]
    if family == 'legacy':
        if R == 8 and nd == 128:
            return [1,2,4,8,16,32,64,3]
        if R == 8 and nd == 64:
            return [1,2,4,8,16,32,3,5]
        vals = [1 << j for j in range(min(R, max(1, int(math.log2(nd)))))]
        # Add low composite labels that create known XOR aliases.
        for v in (3,5,6,9,10,12,17,18,20,24,33,34):
            if len(vals) >= R: break
            if v < nd and v not in vals: vals.append(v)
        for v in range(1, nd):
            if len(vals) >= R: break
            if v not in vals: vals.append(v)
        return vals[:R]
    raise ValueError(family)

def alias_audit(masks, nd):
    chosen = set(masks)
    counts = {str(p): 0 for p in (2,3,4)}
    rels = {str(p): [] for p in (2,3,4)}
    for p in (2,3,4):
        for subset in itertools.combinations(masks, p):
            x = 0
            for a in subset: x ^= a
            if x in chosen and x not in subset:
                counts[str(p)] += 1
                if len(rels[str(p)]) < 80:
                    rels[str(p)].append({'sources': list(subset), 'target': x})
    # Exact finite Walsh table checks, independent of the CUDA kernel.
    x = np.arange(nd, dtype=np.int64)
    chars = np.stack([1 - 2*((np.bitwise_count(x & np.int64(mask)) if hasattr(np, 'bitwise_count') else np.array([int((int(v)&mask).bit_count()) for v in x])) % 2) for mask in masks]).astype(np.float64)
    gram = chars @ chars.T / nd
    return {
        'masks': masks, 'nd': nd, 'balanced': [int(v.sum()) == 0 for v in chars],
        'normalized_l2': [float(np.linalg.norm(v)/math.sqrt(nd)) for v in chars],
        'pairwise_gram_max_error': float(np.max(np.abs(gram-np.eye(len(masks))))) if len(masks) else 0.0,
        'duplicates': len(set(masks)) != len(masks), 'alias_counts_by_order': counts,
        'alias_relations_by_order': rels,
        'status': 'AVAILABLE',
    }

def metrics(row):
    M = np.asarray(row['final_response_norm_matrix'], dtype=float)
    P = np.asarray(row['isolated_storage_response_matrix'], dtype=float)
    R = M.shape[0]
    diag = np.maximum(np.diag(M), NUMERICAL_FLOOR)
    pdiag = np.maximum(np.diag(P), NUMERICAL_FLOOR)
    norm = np.zeros((R,R)); pnorm = np.zeros((R,R))
    for i in range(R):
        norm[i,:] = M[i,:] / diag[i]
        pnorm[i,:] = P[i,:] / pdiag[i]
    np.fill_diagonal(norm, 0.0); np.fill_diagonal(pnorm, 0.0)
    off = M.copy(); np.fill_diagonal(off, 0.0)
    poff = P.copy(); np.fill_diagonal(poff, 0.0)
    predicted = np.asarray(row['predicted_final_reads'], dtype=float)
    captured = np.asarray(row['initial_captured_reads'], dtype=float)
    ages = np.asarray(row['channel_ages'], dtype=float)
    extra = np.abs(np.diag(M)-predicted) / np.maximum(np.abs(predicted), NUMERICAL_FLOOR)
    worst_flat = int(np.argmax(norm)) if norm.size else 0
    wi, wj = np.unravel_index(worst_flat, norm.shape) if norm.size else (0,0)
    vals = norm[~np.eye(R,dtype=bool)]
    pvals = pnorm[~np.eye(R,dtype=bool)]
    return {
        'max_complete_normalized_crosstalk': float(np.max(norm)) if R>1 else 0.0,
        'median_complete_normalized_crosstalk': float(np.median(vals)) if vals.size else 0.0,
        'max_complete_absolute_leakage': float(np.max(off)) if R>1 else 0.0,
        'median_complete_absolute_leakage': float(np.median(off[~np.eye(R,dtype=bool)])) if R>1 else 0.0,
        'worst_source_channel': int(wi), 'worst_read_channel': int(wj),
        'worst_entry_intended_diagonal': float(M[wi,wi]),
        'worst_entry_absolute_leakage': float(M[wi,wj]),
        'max_protected_normalized_crosstalk': float(np.max(pnorm)) if R>1 else 0.0,
        'median_protected_normalized_crosstalk': float(np.median(pvals)) if pvals.size else 0.0,
        'max_protected_absolute_leakage': float(np.max(poff)) if R>1 else 0.0,
        'diagonal_by_channel': np.diag(M).tolist(),
        'protected_diagonal_by_channel': np.diag(P).tolist(),
        'predicted_diagonal_by_channel': predicted.tolist(),
        'initial_capture_by_channel': captured.tolist(),
        'channel_ages': ages.tolist(),
        'raw_retention_by_channel': (np.diag(M)/np.maximum(captured, NUMERICAL_FLOOR)).tolist(),
        'extra_damage_beyond_expected_age_by_channel': extra.tolist(),
        'max_extra_age_damage': float(np.max(extra)),
        'oldest_newest_diagonal_ratio': float(M[0,0]/max(M[-1,-1],NUMERICAL_FLOOR)),
        'complete_normalized_matrix': norm.tolist(),
        'protected_normalized_matrix': pnorm.tolist(),
        'absolute_complete_matrix': M.tolist(),
        'absolute_protected_matrix': P.tolist(),
        'numerical_floor_used': NUMERICAL_FLOOR,
    }

def classify(row):
    m = row['metrics']
    return 'PASS' if (m['max_complete_normalized_crosstalk'] < THRESHOLD and
                      row['input_cube_legal'] and row['correction_gates_legal'] and
                      row['walsh_orthogonality_error'] < 1e-12) else 'FAIL'

def compact_row(row):
    # Keep exact matrix evidence and checkpoints but drop dense trajectories.
    row.pop('trace', None)
    for stage in row.get('corrections', []):
        stage.pop('g_last', None)
    return row

def run_case(name, n, K, R, family='sum_free', clear=2.0, equal_age=None, masks=None):
    key = f'{name}_n{n}_K{K}_R{R}_{family}_c{clear:g}' + (f'_age{equal_age}' if equal_age else '')
    if key in DATA['cases']:
        return DATA['cases'][key]
    if elapsed() > WALL_LIMIT-30:
        SKIPPED.append(key); DATA['skipped'].append({'case':key,'reason':'hard wall budget guard'})
        save_state(key); return None
    if elapsed() > OPTIONAL_STOP and name.startswith('optional'):
        SKIPPED.append(key); DATA['skipped'].append({'case':key,'reason':'80-minute optional cutoff'})
        save_state(key); return None
    nd = n//32
    if masks is None: masks = family_masks(family, R, nd)
    if masks is None:
        item={'case':key,'reason':'UNAVAILABLE DUE TO MASK DIMENSION','family':family,'n':n,'R':R,'nd':nd}
        SKIPPED.append(key); DATA['skipped'].append(item); save_state(key); return None
    if len(masks)!=R or len(set(masks))!=R or min(masks)<1 or max(masks)>=nd:
        item={'case':key,'reason':f'invalid finite Walsh labels for nd={nd}','masks':masks}
        SKIPPED.append(key); DATA['skipped'].append(item); save_state(key); return None
    if nd < K or nd % K:
        item={'case':key,'reason':f'K={K} must divide nd={nd}','family':family}
        SKIPPED.append(key); DATA['skipped'].append(item); save_state(key); return None
    PLANNED.append(key)
    DIAGKEY=f'{family}_n{n}_R{R}'
    DATA['mask_diagnostics'].setdefault(DIAGKEY, alias_audit(list(masks), nd))
    save_state(key)
    print(f'RUN {key} (elapsed {elapsed()/60:.1f} min)', flush=True)
    before=time.perf_counter()
    sp=ref.spec(n,K,kind='core',amps=[1.]*R,order=tuple(range(R)),clear_mult=clear,
                masks=list(masks),equal_age_steps=equal_age)
    row=ref.batch(n,[sp],channels=R)[0]
    torch.cuda.synchronize()
    row['case_name']=key; row['family']=family; row['n']=n; row['K']=K; row['R']=R
    row['case_elapsed_seconds']=time.perf_counter()-before
    row['alias_audit']=DATA['mask_diagnostics'][DIAGKEY]
    row['metrics']=metrics(row)
    row['verdict']=classify(row)
    row=compact_row(row)
    DATA['cases'][key]=row; COMPLETED.append(key)
    save_state()
    print(f"DONE {key}: crosstalk={row['metrics']['max_complete_normalized_crosstalk']:.6g}; "
          f"protected={row['metrics']['max_protected_normalized_crosstalk']:.6g}; "
          f"case={row['case_elapsed_seconds']/60:.1f} min; peakVRAM={torch.cuda.max_memory_allocated()/2**20:.1f} MiB",flush=True)
    return row

def run_k_batch(n, Ks, R, family='sum_free', clear=2.0):
    masks=family_masks(family,R,n//32)
    eligible=[K for K in Ks if K<=n//32 and (n//32)%K==0]
    if not eligible:
        SKIPPED.append(f'Kbatch_n{n}_R{R}'); return
    specs=[]
    names=[]
    for K in eligible:
        key=f'Kscale_n{n}_K{K}_R{R}_{family}_c{clear:g}'
        if key in DATA['cases']: continue
        names.append(key); PLANNED.append(key)
        specs.append(ref.spec(n,K,kind='core',amps=[1.]*R,order=tuple(range(R)),clear_mult=clear,masks=masks))
    if not specs: return
    save_state(names[0]); print('RUN CUDA K batch: '+', '.join(names),flush=True)
    tick=time.perf_counter(); rows=ref.batch(n,specs,channels=R); torch.cuda.synchronize()
    for key,row in zip(names,rows):
        K=row['K']; row['case_name']=key; row['family']=family; row['n']=n; row['K']=K; row['R']=R
        row['case_elapsed_seconds']=time.perf_counter()-tick
        row['alias_audit']=alias_audit(masks,n//32); row['metrics']=metrics(row); row['verdict']=classify(row)
        DATA['mask_diagnostics'].setdefault(f'{family}_n{n}_R{R}',row['alias_audit'])
        DATA['cases'][key]=compact_row(row); COMPLETED.append(key)
    save_state(); print(f'K batch done in {(time.perf_counter()-tick)/60:.1f} min',flush=True)

def setup_metadata():
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA is required. Stopping without CPU fallback.')
    torch.cuda.set_device(0); torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
    props=torch.cuda.get_device_properties(0)
    env={k:os.environ.get(k) for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS')}
    meta={
      'experiment':'finite_n_clean_mask_scaling_20261006',
      'start_timestamp_utc':datetime.now(timezone.utc).isoformat(),
      'python_version':platform.python_version(),'pytorch_version':torch.__version__,
      'cuda_runtime_version':torch.version.cuda,'cuda_available':torch.cuda.is_available(),
      'device':'cuda:0','gpu_name':props.name,'gpu_total_memory_bytes':props.total_memory,
      'dtype':'torch.float64','initial_allocated_vram_bytes':int(torch.cuda.memory_allocated()),
      'initial_reserved_vram_bytes':int(torch.cuda.memory_reserved()),
      'cpu_thread_limits':env,'torch_num_threads':torch.get_num_threads(),
      'torch_num_interop_threads':torch.get_num_interop_threads(),
      'resource_limits':{'wall_hard_seconds':WALL_LIMIT,'optional_start_stop_seconds':OPTIONAL_STOP,
                         'allocated_vram_stop_bytes':VRAM_LIMIT,'CUDA_required':True,'CPU_fallback':False},
      'preregistered_thresholds':{
        'primary_complete_response_cross_talk_pass':THRESHOLD,
        'cross_talk_reference_targets':[1e-2,1e-3,1e-4,1e-5,1e-6,1e-7],
        'protected_component_transport_relative_error_pass':1e-9,
        'trace_correction_relative_error_pass':1e-10,
        'mask_balance_absolute_sum_pass':0,
        'mask_pairwise_gram_max_error_pass':1e-12,
        'legacy_clean_R8_distinction_min_factor':10.0,
      },
      'mask_family_algorithms':{
        'legacy':'historical power-of-two/composite alias-prone labels; n=2048 R8 uses [1,2,4,8,16,32,3,5] because label 64 is out of range; n=4096 R8 reproduces [1,2,4,8,16,32,64,3].',
        'sum_free':'first R odd positive integers below nd=n/32; all pairwise XORs are even, hence no pairwise alias into the selected odd labels.',
        'independent':'first R powers of two, available only for R<=log2(nd); distinct subset XORs cannot equal another selected basis label.'
      },
      'mask_family_capacity':'sum_free R<=nd/2; independent R<=log2(nd); legacy subject to distinct legal labels.',
      'measurement_conventions':'Copied validated reference_cuda.py from finite_n_r8_diagnosis_20261006. Complete response and isolated protected-component matrix use the inherited CUDA float64 recurrence, full private feedback/front/bath/Householder transport, trace correction, common reset, and normalized Walsh reads. No theorem implication.',
      'source_sha256':{
         'reference_cuda.py':digest(ROOT/'reference_cuda.py'),
         'prior_r8_reference_cuda.py':digest(ROOT.parent/'finite_n_r8_diagnosis_20261006'/'reference_cuda.py')
      },
      'planned_tests':[
        'clean-vs-legacy R8 reproduction at n2048',
        'sum-free R ladder at n1024; selected R ladder at n2048 and n4096 if within runtime',
        'clean R8 width curve n512..4096',
        'K=8,16,32,64 at n2048 R8',
        'clear multipliers .5,1,2,4 for clean R8 at n1024',
        'independent-mask comparison where available',
        'matched-age reads where runtime permits',
        'alias-relation negative control via legacy R8'
      ],
      'pass_fail_thresholds_locked_before_new_sweep':True,
    }
    atomic_json(OUT/'run_metadata.json',meta)
    DATA['metadata']={'gpu_name':props.name,'pytorch_version':torch.__version__,'cuda_runtime_version':torch.version.cuda,
                      'dtype':'torch.float64','device':'cuda:0','threshold':THRESHOLD}
    save_state('preflight complete / before new sweep')
    print(json.dumps({k:meta[k] for k in ('python_version','pytorch_version','cuda_runtime_version','gpu_name','gpu_total_memory_bytes','initial_allocated_vram_bytes')},indent=2),flush=True)
    return meta

def write_placeholder(ax, title, text='Not run in available runtime'):
    ax.text(.5,.5,text,ha='center',va='center',wrap=True); ax.set_title(title); ax.set_axis_off()

def plot_matrix(path, row, title):
    if row is None:
        fig,ax=plt.subplots(figsize=(6,4)); write_placeholder(ax,title); fig.savefig(OUT/path,dpi=130); plt.close(fig); return
    M=np.asarray(row['metrics']['absolute_complete_matrix'])
    P=np.asarray(row['metrics']['absolute_protected_matrix'])
    fig,axs=plt.subplots(1,2,figsize=(11,4.6))
    for ax,A,t in zip(axs,(M,P),('Complete response','Protected-only response')):
        im=ax.imshow(np.log10(np.maximum(A,1e-300)),aspect='auto',cmap='viridis'); ax.set_title(t+' (log10 abs)')
        ax.set_xlabel('read character'); ax.set_ylabel('stored signal'); fig.colorbar(im,ax=ax)
    fig.suptitle(title); fig.tight_layout(); fig.savefig(OUT/path,dpi=140); plt.close(fig)

def make_plots():
    cases=list(DATA['cases'].values())
    def choose(**kw):
        arr=cases
        for k,v in kw.items(): arr=[x for x in arr if x.get(k)==v]
        return arr
    # Clean R scaling
    arr=sorted([x for x in cases if x['family']=='sum_free'],key=lambda x:(x['n'],x['R']))
    fig,ax=plt.subplots(figsize=(8,4.8))
    if arr:
        for n in sorted(set(x['n'] for x in arr)):
            z=[x for x in arr if x['n']==n]; ax.semilogy([x['R'] for x in z],[max(x['metrics']['max_complete_normalized_crosstalk'],1e-16) for x in z],'-o',label=f'n={n}')
        ax.axhline(1e-3,color='r',ls=':',label='0.1% target'); ax.legend()
    else: write_placeholder(ax,'Clean-mask R scaling')
    ax.set(title='Sum-free mask scaling',xlabel='R channels',ylabel='worst normalized complete cross-talk'); ax.grid(True,which='both',alpha=.25); fig.tight_layout(); fig.savefig(OUT/'clean_mask_r_scaling.png',dpi=140); plt.close(fig)
    best=max(arr,key=lambda x:x['R'],default=None); fails=min([x for x in arr if x['metrics']['max_complete_normalized_crosstalk']>=THRESHOLD],key=lambda x:x['R'],default=None)
    plot_matrix('response_matrix_largest_pass.png',best,'Largest observed passing clean family')
    plot_matrix('response_matrix_first_fail.png',fails,'First observed failing clean family')
    def curve(fname, xs, ys, xlabel, ylabel, title, logy=True):
        fig,ax=plt.subplots(figsize=(7.5,4.5))
        if xs: (ax.semilogy if logy else ax.plot)(xs,ys,'o-')
        else: write_placeholder(ax,title)
        ax.set(xlabel=xlabel,ylabel=ylabel,title=title); ax.grid(True,which='both',alpha=.25); fig.tight_layout(); fig.savefig(OUT/fname,dpi=140); plt.close(fig)
    r_data=sorted([x for x in arr if x['n']==1024],key=lambda x:x['R'])
    curve('cross_talk_vs_r.png',[x['R'] for x in r_data],[max(x['metrics']['max_complete_normalized_crosstalk'],1e-16) for x in r_data],'R','worst complete cross-talk','Cross-talk vs channel count')
    width=sorted([x for x in cases if x['family']=='sum_free' and x['R']==8],key=lambda x:x['n'])
    curve('cross_talk_vs_width.png',[x['n'] for x in width],[max(x['metrics']['max_complete_normalized_crosstalk'],1e-16) for x in width],'n','worst complete cross-talk','Clean R=8 width scaling')
    age_x=[]; age_y=[]
    for x in cases:
        for a,b in zip(x['metrics']['channel_ages'],x['metrics']['extra_damage_beyond_expected_age_by_channel']): age_x.append(a); age_y.append(max(b,1e-18))
    curve('extra_damage_vs_age.png',age_x,age_y,'channel age (steps)','relative extra diagonal damage','Extra damage after removing expected age transport')
    failures=[x for x in cases if x['metrics']['max_complete_normalized_crosstalk']>=THRESHOLD]
    abs_x=[x['metrics']['max_complete_absolute_leakage'] for x in cases]; norm_y=[x['metrics']['max_complete_normalized_crosstalk'] for x in cases]
    fig,ax=plt.subplots(figsize=(7,4.8))
    if cases: ax.scatter(abs_x,norm_y,c=[x['R'] for x in cases],cmap='viridis'); ax.set_xscale('log'); ax.set_yscale('log'); fig.colorbar(ax.collections[0],ax=ax,label='R')
    else: write_placeholder(ax,'Absolute vs normalized cross-talk')
    ax.set(xlabel='maximum absolute leakage',ylabel='maximum normalized leakage',title='Absolute leakage vs denominator-normalized leakage'); ax.grid(True,which='both',alpha=.25); fig.tight_layout(); fig.savefig(OUT/'absolute_vs_normalized_crosstalk.png',dpi=140); plt.close(fig)
    kcases=sorted([x for x in cases if x['n']==2048 and x['R']==8 and x['family']=='sum_free' and x['case_name'].startswith('Kscale')],key=lambda x:x['K'])
    curve('clean_k_scaling.png',[x['K'] for x in kcases],[x['combined_B_norm'] for x in kcases],'K','coded donor combined norm','Clean-mask coded-donor norm vs K',False)
    clears=sorted([x for x in cases if x['R']==8 and x['family']=='sum_free' and 'clear' in x['case_name']],key=lambda x:(x['n'],x['clear_mult']))
    curve('clear_scaling_clean_masks.png',[x['clear_mult'] for x in clears],[max(x['metrics']['max_complete_normalized_crosstalk'],1e-16) for x in clears],'clear multiplier of C0','worst cross-talk','Clear scaling with clean masks')
    # Alias counts versus measured complete crosstalk (order 2/3/4 counts).
    fig,ax=plt.subplots(figsize=(7,4.8))
    if cases:
        sc=ax.scatter([x['alias_audit']['alias_counts_by_order']['2']+x['alias_audit']['alias_counts_by_order']['3']+x['alias_audit']['alias_counts_by_order']['4'] for x in cases],
                      [max(x['metrics']['max_complete_normalized_crosstalk'],1e-16) for x in cases],c=[x['R'] for x in cases],cmap='plasma'); ax.set_yscale('log'); fig.colorbar(sc,ax=ax,label='R')
    else: write_placeholder(ax,'Alias count vs cross-talk')
    ax.set(xlabel='count of XOR relations of orders 2–4',ylabel='worst complete cross-talk',title='Higher-order mask aliases vs measured cross-talk'); ax.grid(True,which='both',alpha=.25); fig.tight_layout(); fig.savefig(OUT/'alias_count_vs_crosstalk.png',dpi=140); plt.close(fig)
    fam=[x for x in cases if x['R']==8 and x['n']==2048]
    fig,ax=plt.subplots(figsize=(7,4.5))
    if fam: ax.bar([x['family'] for x in fam],[x['metrics']['max_complete_normalized_crosstalk'] for x in fam]); ax.set_yscale('log')
    else: write_placeholder(ax,'Mask family comparison')
    ax.axhline(1e-3,color='r',ls=':',label='0.1% target'); ax.legend(); ax.set(title='R=8 mask family comparison (n=2048)',ylabel='worst complete cross-talk'); fig.tight_layout(); fig.savefig(OUT/'mask_family_comparison.png',dpi=140); plt.close(fig)
    # Matched-age matrix: use R=8/12/16 cases where checkpoint was requested.
    ma=[x for x in cases if x.get('equal_age_read_matrices')]
    if ma:
        x=max(ma,key=lambda z:z['R']); # plot the first common-age record
        rec=next(iter(x['equal_age_read_matrices'].values())); A=np.asarray(rec['response_norm_matrix'],float)
        fig,ax=plt.subplots(figsize=(5.5,4.8)); im=ax.imshow(np.log10(np.maximum(A,1e-300)),aspect='auto'); ax.set(title=f"Matched-age n={x['n']} R={x['R']}",xlabel='read channel',ylabel='stored signal'); fig.colorbar(im,ax=ax,label='log10 response norm')
    else:
        fig,ax=plt.subplots(figsize=(5.5,4.8)); write_placeholder(ax,'Matched-age response')
    fig.tight_layout(); fig.savefig(OUT/'matched_age_response.png',dpi=140); plt.close(fig)
    # Legacy alias negative control and clean comparison.
    neg=[x for x in cases if x['family']=='legacy' and x['R']>=8]
    if neg: plot_matrix('negative_alias_control.png',max(neg,key=lambda x:x['R']),'Legacy alias-prone negative control')
    else: plot_matrix('negative_alias_control.png',None,'Legacy alias-prone negative control')

def make_summary():
    cases=list(DATA['cases'].values())
    sumfree=[x for x in cases if x['family']=='sum_free']
    pass_cases=[x for x in sumfree if x['verdict']=='PASS']
    fail_cases=[x for x in sumfree if x['verdict']=='FAIL']
    largest=max(pass_cases,key=lambda x:x['R'],default=None)
    first=min(fail_cases,key=lambda x:x['R'],default=None)
    lines=['# Clean-Mask Multichannel CUDA Scaling','',
           '| Test | Verdict | Strongest Measurement |','|---|---|---|']
    def verdict(group, ok=None):
        return ok if ok else ('PASS' if group else 'NOT RUN')
    c8=[x for x in cases if x['R']==8 and x['n']==2048]
    clean8=next((x for x in c8 if x['family']=='sum_free'),None)
    leg8=next((x for x in c8 if x['family']=='legacy'),None)
    lines += [
      f"| R=8 clean vs legacy | {('PASS' if clean8 and leg8 and leg8['metrics']['max_complete_normalized_crosstalk']>10*max(clean8['metrics']['max_complete_normalized_crosstalk'],1e-16) else 'INCONCLUSIVE')} | clean={clean8['metrics']['max_complete_normalized_crosstalk']:.6g}; legacy={leg8['metrics']['max_complete_normalized_crosstalk']:.6g} |" if clean8 and leg8 else '| R=8 clean vs legacy | NOT RUN | reference comparison unavailable |',
      f"| Channel-count ladder | {('PASS' if largest else 'NOT RUN')} | largest observed clean pass R={largest['R'] if largest else '—'}; first fail R={first['R'] if first else 'none observed'} |",
      f"| Width scaling | {verdict([x for x in cases if x['R']==8 and x['family']=='sum_free'])} | tested n={sorted(set(x['n'] for x in cases if x['R']==8 and x['family']=='sum_free'))} |",
      f"| K scaling | {verdict([x for x in cases if x['case_name'].startswith('Kscale')])} | K tested={[x['K'] for x in sorted(cases,key=lambda z:z['K']) if x['case_name'].startswith('Kscale')]} |",
      f"| Clearing / alias audit | {verdict([x for x in cases if x['R']==8 and x['family']=='sum_free'])} | plots and exact order-2/3/4 XOR counts included |",
    ]
    lines += ['', '## Run details', '',
      f"- GPU: {DATA.get('metadata',{}).get('gpu_name','unknown')} ({DATA.get('metadata',{}).get('device','cuda:0')})",
      f"- PyTorch/CUDA: {DATA.get('metadata',{}).get('pytorch_version','?')} / {DATA.get('metadata',{}).get('cuda_runtime_version','?')}",
      '- Main recurrence dtype: CUDA float64; no CPU fallback.',
      f"- Total runtime: {elapsed()/60:.2f} minutes.",
      f"- Peak allocated/reserved VRAM: {torch.cuda.max_memory_allocated()/2**20:.1f}/{torch.cuda.max_memory_reserved()/2**20:.1f} MiB.",
      f"- Largest completed n/R: {max((x['n'] for x in cases),default=0)} / {max((x['R'] for x in cases),default=0)}.",
      '- The recurrence is the copied, previously validated finite reference implementation. This experiment is finite-size evidence only.',
      '', '## Main observations', '']
    if clean8 and leg8:
        lines.append(f"At n=2048, R=8, the clean sum-free family measured {clean8['metrics']['max_complete_normalized_crosstalk']:.6g} worst complete-response cross-talk, while the alias-prone legacy family measured {leg8['metrics']['max_complete_normalized_crosstalk']:.6g}. The ratio is {leg8['metrics']['max_complete_normalized_crosstalk']/max(clean8['metrics']['max_complete_normalized_crosstalk'],1e-300):.3g}x.")
        lines.append(f"The clean R=8 absolute maximum leakage was {clean8['metrics']['max_complete_absolute_leakage']:.6g}; its largest normalized leak was associated with intended diagonal {clean8['metrics']['worst_entry_intended_diagonal']:.6g}.")
    lines.append(f"Largest clean configuration observed below 0.1%: {('n='+str(largest['n'])+', R='+str(largest['R'])+', K='+str(largest['K'])+', cross-talk='+format(largest['metrics']['max_complete_normalized_crosstalk'],'.6g')) if largest else 'none'}.")
    lines.append(f"First observed clean failure of the 0.1% target: {('n='+str(first['n'])+', R='+str(first['R'])+', cross-talk='+format(first['metrics']['max_complete_normalized_crosstalk'],'.6g')) if first else 'none in completed cases'}.")
    lines += ['', '## Mask algebra checks', '', 'Mask labels were generated algorithmically; Walsh balance, normalization, pairwise Gram error, duplicates, and XOR relations through order four are saved per case in `results.json` under `mask_diagnostics`. The sum-free construction uses odd labels, so pairwise XORs are even; higher-order odd-length relations may still occur and are counted rather than assumed absent.', '']
    lines += ['## Simple Meaning','',
      'This experiment checks whether stored signals stay separated when more Walsh-coded channels share the same finite corridor recurrence. A cross-talk percentage compares an unwanted read to the intended read; it can look large if the intended old signal has become very small from normal aging.', '',
      '1. **Largest R passing 0.1%:** '+(str(largest['R'])+f" (observed at n={largest['n']})" if largest else 'not determined from completed cases.'),
      '2. **First R failing:** '+(str(first['R'])+f" (n={first['n']})" if first else 'none observed in completed clean cases.'),
      '3. **Did protected memory break?** See the protected-only matrix and expected-age damage; finite outcomes do not imply a theorem.',
      '4. **Did sum-free masks address the old R=8 alias?** '+('Yes in this run.' if clean8 and leg8 and leg8['metrics']['max_complete_normalized_crosstalk']>10*max(clean8['metrics']['max_complete_normalized_crosstalk'],1e-16) else 'The paired reproduction was incomplete or did not show the preregistered factor.'),
      '5. **Higher-order aliases:** exact order 2–4 counts are listed in the mask audit; compare these with measured matrices, without treating correlation as proof of cause.',
      '6. **Stronger independent masks:** '+('available and measured where the Walsh-label dimension allowed.' if any(x['family']=='independent' for x in cases) else 'not run / unavailable.'),
      '7. **K=32/64:** '+('measurements are in results.json.' if any(x['case_name'].startswith('Kscale') and x['K']>=32 for x in cases) else 'not completed.'),
      '8. **Tiny diagonals:** absolute leakage and normalized leakage are reported separately for each case.',
      '9. **Matched-age reads:** '+('recorded for cases that include equal-age checkpoints.' if any(x.get('equal_age_read_matrices') for x in cases) else 'not completed.'),
      '10. **Width trend:** finite tested points are plotted; no asymptotic law is inferred.',
      '11. **Clearing:** selected clean-mask clear settings are compared; no general law is inferred.',
      '12. **Finite-size capacity:** this battery only identifies tested pass/fail points, not a theoretical capacity.',
      '13. **Theory contradiction:** no theorem status is changed; report any numerical anomaly as a finite-size discrepancy to investigate.',
      '14. **Next experiment:** target the first reproducible clean-mask failure and vary only its identified confound (age, higher-order alias, or residual complement).',
      '15. **For theory review:** only a stable, reproducible change in protected-only response or a measured higher-order alias/leak mapping is a useful handoff.',
      '', '## Completed / skipped work', '',
      f"Completed cases: {len(cases)}. Skipped cases: {len(DATA['skipped'])}. Failed runs: {len(DATA['errors'])}.",
      'See `progress.json` for the exact checkpoint and pending cases.', '']
    (OUT/'SUMMARY.md').write_text('\n'.join(lines),encoding='utf-8')

def main():
    meta=setup_metadata()
    # Pre-compute, validate and persist mask diagnostics before new numerical outcomes.
    for n in (512,1024,2048,4096):
        nd=n//32
        for R in sorted(set([2,4,6,8,9,10,12,16,20,24,32])):
            for fam in ('sum_free','independent'):
                mm=family_masks(fam,R,nd)
                if mm is None:
                    DATA['mask_diagnostics'][f'{fam}_n{n}_R{R}']={'status':'UNAVAILABLE DUE TO MASK DIMENSION','nd':nd,'R':R}
                else:
                    DATA['mask_diagnostics'][f'{fam}_n{n}_R{R}']=alias_audit(mm,nd)
    for n in (2048,4096):
        mm=family_masks('legacy',8,n//32)
        DATA['mask_diagnostics'][f'legacy_n{n}_R8']=alias_audit(mm,n//32)
    save_state('mask family preregistration complete')

    # Gate 1: same-path reproduction. If clean-vs-legacy does not separate, stop and diagnose.
    clean=run_case('reproduce',2048,32,8,'sum_free',2.0)
    legacy=run_case('reproduce',2048,32,8,'legacy',2.0)
    if not clean or not legacy: raise RuntimeError('Could not complete the R=8 clean/legacy gate.')
    DATA['test_verdicts']['R8_clean_legacy_gate']={
        'clean':clean['metrics']['max_complete_normalized_crosstalk'],
        'legacy':legacy['metrics']['max_complete_normalized_crosstalk'],
        'legacy_to_clean_ratio':legacy['metrics']['max_complete_normalized_crosstalk']/max(clean['metrics']['max_complete_normalized_crosstalk'],1e-300),
        'pass':legacy['metrics']['max_complete_normalized_crosstalk'] > 10*max(clean['metrics']['max_complete_normalized_crosstalk'],1e-16)
    }
    save_state('R8 reproduction gate')
    if not DATA['test_verdicts']['R8_clean_legacy_gate']['pass']:
        raise RuntimeError('Clean-vs-legacy R=8 distinction failed preregistered gate; stopping for diagnosis.')

    # Width points, including representative comparison size.
    for n,K in ((512,8),(1024,16),(4096,64)):
        run_case('width',n,K,8,'sum_free',2.0,equal_age=256 if n==1024 else None)
        if elapsed()>OPTIONAL_STOP: break

    # Broad R ladder at n=1024; dimensions permit sum-free through R=16.
    for R in (2,4,6,8,9,10,12,16):
        run_case('ladder',1024,16,R,'sum_free',2.0,equal_age=256 if R in (8,12,16) else None)
        if elapsed()>WALL_LIMIT-90: break

    # Stronger linearly-independent family comparison where it exists.
    for R in (4,5):
        run_case('family_compare',1024,16,R,'independent',2.0)
        if elapsed()>WALL_LIMIT-90: break

    # Higher-R stress at n=2048, with sum-free family available through R=32.
    for R in (12,16,20,24,32):
        if elapsed()>OPTIONAL_STOP: break
        run_case('optional_ladder',2048,32,R,'sum_free',2.0,equal_age=256 if R in (12,16) else None)

    # K scaling, all K values packed into one CUDA batch for the same recurrence.
    if elapsed()<WALL_LIMIT-300:
        run_k_batch(2048,(8,16,32,64),8,'sum_free',2.0)

    # Clearing sweep: distinct calls because the validated engine requires same clear duration per batch.
    if elapsed()<WALL_LIMIT-500:
        for clear in (.5,1.,2.,4.):
            run_case('clear',1024,16,8,'sum_free',clear)
            if elapsed()>WALL_LIMIT-300: break

    # Strong-family comparison against sum-free R=4, same n/K and recurrence.
    if elapsed()<OPTIONAL_STOP:
        run_case('family_compare',1024,16,4,'sum_free',2.0)

    DATA['test_verdicts']['main_sweep_finished']={'completed_cases':len(DATA['cases']),'wall_limit_seconds':WALL_LIMIT}
    make_plots(); make_summary()
    atomic_json(OUT/'results.json',DATA)
    p=json.loads((OUT/'progress.json').read_text(encoding='utf-8')); p.update(status='COMPLETE' if elapsed()<WALL_LIMIT else 'STOPPED_AT_WALL_LIMIT',elapsed_runtime_seconds=elapsed(),current_test=None,peak_allocated_vram_bytes=int(torch.cuda.max_memory_allocated()),peak_reserved_vram_bytes=int(torch.cuda.max_memory_reserved()),completed_tests=COMPLETED,failed_tests=FAILED,skipped_tests=SKIPPED,pending_tests=[x for x in PLANNED if x not in COMPLETED and x not in FAILED and x not in SKIPPED]); atomic_json(OUT/'progress.json',p)
    m=json.loads((OUT/'run_metadata.json').read_text(encoding='utf-8')); m['end_timestamp_utc']=datetime.now(timezone.utc).isoformat(); m['total_runtime_seconds']=elapsed(); m['peak_allocated_vram_bytes']=int(torch.cuda.max_memory_allocated()); m['peak_reserved_vram_bytes']=int(torch.cuda.max_memory_reserved()); m['largest_n_completed']=max((x['n'] for x in DATA['cases'].values()),default=0); m['largest_R_completed']=max((x['R'] for x in DATA['cases'].values()),default=0); atomic_json(OUT/'run_metadata.json',m)
    print(f"Finished: {elapsed()/60:.2f} min, cases={len(DATA['cases'])}, peak VRAM={torch.cuda.max_memory_allocated()/2**20:.1f} MiB",flush=True)

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        DATA['errors'].append({'time_seconds':elapsed(),'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()})
        FAILED.append(str(exc));
        if torch.cuda.is_available():
            try: make_plots(); make_summary()
            except Exception: pass
        try:
            save_state(str(exc))
            p=json.loads((OUT/'progress.json').read_text(encoding='utf-8')); p['status']='STOPPED_ERROR'; p['current_test']=str(exc); atomic_json(OUT/'progress.json',p)
        except Exception: pass
        print(traceback.format_exc(),file=sys.stderr,flush=True)
        raise
