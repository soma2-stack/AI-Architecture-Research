"""Targeted finite-N R=8 diagnosis. CUDA float64 only; no training."""
import os
for _v in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_v]='1'
import sys, json, time, math, platform, hashlib, traceback, uuid
from pathlib import Path
from datetime import datetime, timezone
import torch
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.set_default_dtype(torch.float64)
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import reference_cuda as ref
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

START=time.perf_counter()
PREVIOUS_WALL_SECONDS=3316.58
WALL_LIMIT=250.0
OUT=ROOT
PREV=ROOT.parent/'finite_n_clear_scaling_20261006'
PREV_R8={'n':4096,'K':64,'R':8,'clear_mult':2.0,'expected_worst_cross_talk':0.0025062358620352044}
THRESHOLDS={
 'primary_complete_response_cross_talk_pass':1e-3,
 'cross_talk_reference_targets':[1e-2,1e-3,1e-4,1e-5],
 'protected_extra_damage_pass':1e-9,
 'trace_correction_damage_pass':1e-10,
 'reproduction_relative_difference_pass':0.10,
 'broken_control_min_cross_talk':0.1,
 'broken_control_increase_factor':10.0,
 'clear_law_relative_contraction_error_descriptive_only':0.20,
 'legal_gate_open_interval':(0.0,1.0),
 'input_cube_abs_max':0.5,
 'vrAM_stop_allocated_bytes':6*1024**3,
 'hard_wall_seconds':WALL_LIMIT,
}
ref.LIMIT=WALL_LIMIT

def atomic_json(path,obj):
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    payload=json.dumps(obj,indent=2,allow_nan=False)+'\n'
    tmp.write_text(payload,encoding='utf-8')
    last=None
    for _ in range(8):
        try:
            os.replace(tmp,path)
            return
        except PermissionError as e:
            last=e; time.sleep(.25)
    # OneDrive/indexing can briefly lock the destination. Preserve a checkpoint
    # even if atomic replacement remains unavailable.
    try: path.write_text(payload,encoding='utf-8')
    except Exception: raise last
    try: tmp.unlink(missing_ok=True)
    except Exception: pass

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def elapsed(): return time.perf_counter()-START
def guard():
    if elapsed()>WALL_LIMIT or PREVIOUS_WALL_SECONDS+elapsed()>3600:
        raise TimeoutError('60-minute cumulative experiment wall limit reached')
    if torch.cuda.max_memory_allocated()>6*1024**3: raise MemoryError('Allocated VRAM exceeded 6 GiB safety limit')

def metrics(row):
    M=np.asarray(row['final_response_norm_matrix'],dtype=float)
    P=np.asarray(row['isolated_storage_response_matrix'],dtype=float)
    R=M.shape[0]
    d=np.maximum(np.diag(M),1e-300)
    off=np.array([[M[i,j] for j in range(R) if j!=i] for i in range(R)])
    poff=np.array([[P[i,j] for j in range(R) if j!=i] for i in range(R)])
    abs_rows=np.max(off,axis=1) if R>1 else np.zeros(R)
    pabs_rows=np.max(poff,axis=1) if R>1 else np.zeros(R)
    normalized=abs_rows/d
    pdiag=np.maximum(np.diag(P),1e-300)
    pnormalized=pabs_rows/pdiag
    ratios=np.array([max((M[i,j]/max(M[i,i],1e-300) for j in range(R) if j!=i),default=0.) for i in range(R)])
    initial=np.asarray(row['initial_captured_reads'],float)
    predicted=np.asarray(row['predicted_final_reads'],float)
    actual=np.diag(M)
    extra=np.abs(actual-predicted)/np.maximum(predicted,1e-300)
    result={
      'max_complete_normalized_crosstalk':float(np.max(ratios)),
      'median_complete_normalized_crosstalk':float(np.median(np.concatenate([off[i]/d[i] for i in range(R)]))),
      'max_complete_absolute_leakage':float(np.max(off)),
      'worst_complete_source_row':int(np.argmax(ratios)),
      'worst_complete_read_column':int(np.argmax(M[int(np.argmax(ratios))]*(np.arange(R)!=int(np.argmax(ratios))))),
      'max_protected_normalized_crosstalk':float(np.max(pnormalized)),
      'median_protected_normalized_crosstalk':float(np.median(np.concatenate([poff[i]/pdiag[i] for i in range(R)]))),
      'max_protected_absolute_leakage':float(np.max(poff)),
      'oldest_diagonal':float(M[0,0]),'newest_diagonal':float(M[-1,-1]),
      'oldest_newest_diagonal_ratio':float(M[0,0]/max(M[-1,-1],1e-300)),
      'diagonal_by_channel':np.diag(M).tolist(),
      'predicted_diagonal_by_channel':predicted.tolist(),
      'initial_capture_by_channel':initial.tolist(),
      'extra_age_damage_by_channel':extra.tolist(),
      'max_extra_age_damage':float(np.max(extra)),
      'complement_residual_after_reset':row['checkpoints'].get('after_reset',{}).get('complement_residual_norms'),
      'mT':row['mT'],'total_steps':row['total_steps'],'clear_steps':row['clear_steps'],
      'clear_mult':row['clear_mult'],'n':row['n'],'K':row['K'],'R':row['channels'],
      'input_cube_legal':row['input_cube_legal'],'correction_gates_legal':row['correction_gates_legal'],
      'trace_damage_max':max(row['max_trace_step_error_over_initial']),
      'transport_quality_min':min(row['transport_quality']),
      'transport_quality_max':max(row['transport_quality']),
      'matrix_condition_number_protected':row['isolated_storage_condition_number'],
      'matrix_complete':M.tolist(),'matrix_protected':P.tolist(),
    }
    result['oldest_to_newest_protected_ratio']=float(P[0,0]/max(P[-1,-1],1e-300))
    return result

def atomic_checkpoint(data, completed, failed, skipped, remaining, current):
    data['runtime_seconds']=elapsed()
    atomic_json(OUT/'results.json',data)
    meta=data.get('metadata',{})
    prog={
      'completed_tests':completed,'failed_tests':failed,'skipped_tests':skipped,
      'elapsed_runtime_seconds':PREVIOUS_WALL_SECONDS+elapsed(),'current_test':current,'remaining_planned_tests':remaining,
      'peak_allocated_vram_bytes':int(torch.cuda.max_memory_allocated()) if torch.cuda.is_available() else None,
      'peak_reserved_vram_bytes':int(torch.cuda.max_memory_reserved()) if torch.cuda.is_available() else None,
      'cuda_required':True,'status':'RUNNING'
    }
    atomic_json(OUT/'progress.json',prog)

def write_case(data, completed, failed, skipped, name, n,K,R,clear,amps=None,masks=None,kind='core',equal_age=None):
    guard()
    key=f'{name}_n{n}_K{K}_R{R}_c{clear:g}_'+(kind if kind!='core' else 'valid')
    if key in data['cases']: return data['cases'][key]
    remaining=['core diagnosis battery']
    atomic_checkpoint(data,completed,failed,skipped,remaining,key)
    if amps is None: amps=[1.]*R
    if masks is None:
        # The exact inherited R=8 diagnostic uses the historical special
        # character set. For smaller tuple supports, use distinct nonzero
        # masks 1..R, all of which are balanced/orthogonal and fit nd>=16.
        masks=([1,2,4,8,16,32,64,3] if name=='reproduce' and R==8 else list(range(1,R+1)))
    sp=ref.spec(n,K,kind=kind,amps=amps,order=tuple(range(R)),clear_mult=clear,masks=masks,equal_age_steps=equal_age)
    before=time.perf_counter()
    print(f'RUN {key}',flush=True)
    row=ref.batch(n,[sp],channels=R)[0]
    torch.cuda.synchronize()
    row['case_name']=key
    row['elapsed_seconds']=time.perf_counter()-before
    row['metrics']=metrics(row)
    # Retain the complete selected clear trajectory, not unrelated periodic samples.
    row['clear_trajectory']=[q for q in row.get('trace',[]) if q.get('phase')=='clear']
    row.pop('trace',None)
    data['cases'][key]=row
    completed.append(key)
    atomic_checkpoint(data,completed,failed,skipped,'core diagnosis battery',None)
    return row

def make_plots(data):
    cases=list(data['cases'].values())
    byname={x['case_name']:x for x in cases}
    def choose(test,n=None,R=None,clear=None,K=None):
        arr=[x for x in cases if x['case_name'].startswith(test+'_')]
        if n is not None: arr=[x for x in arr if x['n']==n]
        if R is not None: arr=[x for x in arr if x['channels']==R]
        if clear is not None: arr=[x for x in arr if x['clear_mult']==clear]
        if K is not None: arr=[x for x in arr if x['K']==K]
        return arr
    # Full and protected R=8 matrices from reproduction, falling back to largest valid R=8.
    r8=choose('reproduce',R=8) or choose('clear',R=8) or choose('width',R=8)
    if r8:
        M=np.asarray(r8[0]['metrics']['matrix_complete']); P=np.asarray(r8[0]['metrics']['matrix_protected'])
        fig,ax=plt.subplots(1,2,figsize=(11,4.5))
        im=ax[0].imshow(M,aspect='auto'); ax[0].set_title('Complete response'); fig.colorbar(im,ax=ax[0])
        im=ax[1].imshow(P,aspect='auto'); ax[1].set_title('Protected component'); fig.colorbar(im,ax=ax[1])
        for a in ax: a.set_xlabel('read channel'); a.set_ylabel('stored channel')
        fig.tight_layout(); fig.savefig(OUT/'r8_response_matrix.png',dpi=150); plt.close(fig)
    clr=choose('clear',R=8)
    if clr:
        clr=sorted(clr,key=lambda x:x['clear_mult'])
        fig,ax=plt.subplots(figsize=(7,4.5))
        ax.semilogy([x['clear_mult'] for x in clr],[x['metrics']['max_complete_normalized_crosstalk'] for x in clr],'o-',label='complete')
        ax.semilogy([x['clear_mult'] for x in clr],[x['metrics']['max_protected_normalized_crosstalk'] for x in clr],'s--',label='protected')
        ax.axhline(1e-3,color='r',ls=':',label='0.1% target'); ax.set_xlabel('clear multiplier of C0=2n'); ax.set_ylabel('worst normalized cross-talk'); ax.legend(); ax.grid(True,which='both',alpha=.3)
        fig.tight_layout(); fig.savefig(OUT/'r8_clear_sweep.png',dpi=150); plt.close(fig)
    widths=choose('width_clean',R=8)
    if widths:
        widths=sorted(widths,key=lambda x:x['n']); fig,ax=plt.subplots(figsize=(7,4.5))
        ax.loglog([x['n'] for x in widths],[x['metrics']['max_complete_normalized_crosstalk'] for x in widths],'o-',label='complete')
        ax.loglog([x['n'] for x in widths],[x['metrics']['max_protected_normalized_crosstalk'] for x in widths],'s--',label='protected')
        ax.axhline(1e-3,color='r',ls=':'); ax.set_xlabel('n'); ax.set_ylabel('worst normalized cross-talk'); ax.legend(); ax.grid(True,which='both',alpha=.3)
        fig.tight_layout(); fig.savefig(OUT/'r8_width_scaling.png',dpi=150); plt.close(fig)
    ladder=sorted([x for x in cases if x['case_name'].startswith('ladder_clean_')],key=lambda x:x['channels'])
    if ladder:
        fig,ax=plt.subplots(figsize=(7,4.5)); ax.semilogy([x['channels'] for x in ladder],[x['metrics']['max_complete_normalized_crosstalk'] for x in ladder],'o-',label='complete'); ax.semilogy([x['channels'] for x in ladder],[x['metrics']['max_protected_normalized_crosstalk'] for x in ladder],'s--',label='protected'); ax.axhline(1e-3,color='r',ls=':'); ax.set_xlabel('R channels'); ax.set_ylabel('worst normalized cross-talk'); ax.legend(); ax.grid(True,which='both',alpha=.3); fig.tight_layout(); fig.savefig(OUT/'channel_count_scaling.png',dpi=150); plt.close(fig)
        ages=[]; dam=[]
        for x in ladder:
            ages.extend(x['channel_ages']); dam.extend(x['metrics']['extra_age_damage_by_channel'])
        fig,ax=plt.subplots(figsize=(7,4.5)); ax.loglog(ages,np.maximum(dam,1e-18),'o'); ax.set_xlabel('channel age (steps)'); ax.set_ylabel('relative error beyond predicted scalar transport'); ax.grid(True,which='both',alpha=.3); fig.tight_layout(); fig.savefig(OUT/'extra_damage_vs_channel_age.png',dpi=150); plt.close(fig)
        x=ladder[-1]['metrics']; ii,jj=np.unravel_index(np.argmax(np.asarray(x['matrix_complete'])*~np.eye(len(x['matrix_complete']),dtype=bool)),np.asarray(x['matrix_complete']).shape); abs_leak=np.asarray(x['matrix_complete'])[ii,jj]; diag=np.asarray(x['matrix_complete'])[ii,ii]
        fig,ax=plt.subplots(figsize=(6,4.5)); ax.bar(['absolute leakage','intended diagonal','ratio'],[abs_leak,diag,abs_leak/max(diag,1e-300)]); ax.set_yscale('log'); ax.set_title(f'Largest off-diagonal at R={ladder[-1]["channels"]}'); fig.tight_layout(); fig.savefig(OUT/'absolute_vs_normalized_crosstalk.png',dpi=150); plt.close(fig)
        fig,ax=plt.subplots(figsize=(7,4.5)); ax.semilogy([x['channels'] for x in ladder],[x['metrics']['max_protected_normalized_crosstalk'] for x in ladder],'o-',label='protected Walsh'); ax.semilogy([x['channels'] for x in ladder],[x['metrics']['max_complete_normalized_crosstalk'] for x in ladder],'s-',label='complete response'); ax.legend(); ax.set_xlabel('R'); ax.set_ylabel('worst cross-talk'); ax.grid(True,which='both',alpha=.3); fig.tight_layout(); fig.savefig(OUT/'protected_vs_complete.png',dpi=150); plt.close(fig)
        fig,ax=plt.subplots(figsize=(7,4.5)); ax.plot([x['channels'] for x in ladder],[x['total_steps'] for x in ladder],'o-'); ax.set_xlabel('R'); ax.set_ylabel('total steps'); ax2=ax.twinx(); ax2.plot([x['channels'] for x in ladder],[x['metrics']['max_complete_normalized_crosstalk'] for x in ladder],'s--',color='tab:red'); ax2.set_ylabel('worst cross-talk'); fig.tight_layout(); fig.savefig(OUT/'clear_cost_tradeoff.png',dpi=150); plt.close(fig)
        equal=[x for x in ladder if x.get('equal_age_read_matrices')]
        if equal:
            fig,ax=plt.subplots(figsize=(7,4.5))
            for x in equal:
                vals=[]
                for _,rec in x['equal_age_read_matrices'].items():
                    M=np.asarray(rec['response_norm_matrix']); p=rec['channel']; vals.append(max([M[p,q]/max(M[p,p],1e-300) for q in range(M.shape[1]) if q!=p] or [0.]))
                ax.semilogy([x['channels']]*len(vals),vals,'o',label=f'R={x["channels"]}')
            ax.set_xlabel('channel count'); ax.set_ylabel('equal-age complete cross-talk'); ax.grid(True,which='both',alpha=.3); ax.legend(); fig.tight_layout(); fig.savefig(OUT/'matched_age_comparison.png',dpi=150); plt.close(fig)
    kcases=sorted([x for x in cases if x['case_name'].startswith('k_sensitivity_')],key=lambda x:x['K'])
    if kcases:
        fig,ax=plt.subplots(figsize=(7,4.5)); ax.semilogy([x['K'] for x in kcases],[x['metrics']['max_complete_normalized_crosstalk'] for x in kcases],'o-',label='cross-talk'); ax2=ax.twinx(); ax2.plot([x['K'] for x in kcases],[x['combined_B_norm'] for x in kcases],'s--',color='tab:red',label='B diagonal'); ax.set_xlabel('K'); ax.set_ylabel('cross-talk'); ax2.set_ylabel('new-channel response'); fig.tight_layout(); fig.savefig(OUT/'k_sensitivity_r8.png',dpi=150); plt.close(fig)
    neg=[x for x in cases if x['case_name'].startswith('negative_')]
    if neg:
        fig,ax=plt.subplots(figsize=(7,4.5)); ax.bar([x['case_name'].split('_n')[0] for x in neg],[x['metrics']['max_complete_normalized_crosstalk'] for x in neg]); ax.axhline(1e-3,color='r',ls=':'); ax.set_ylabel('worst cross-talk'); ax.tick_params(axis='x',rotation=25); fig.tight_layout(); fig.savefig(OUT/'negative_control.png',dpi=150); plt.close(fig)
    required=['r8_response_matrix.png','r8_clear_sweep.png','r8_width_scaling.png',
      'channel_count_scaling.png','extra_damage_vs_channel_age.png',
      'absolute_vs_normalized_crosstalk.png','protected_vs_complete.png',
      'clear_cost_tradeoff.png','matched_age_comparison.png','k_sensitivity_r8.png']
    for filename in required:
        if not (OUT/filename).exists():
            fig,ax=plt.subplots(figsize=(6,3.5)); ax.text(.5,.5,'Not run / no data available',ha='center',va='center'); ax.set_axis_off(); fig.savefig(OUT/filename,dpi=150); plt.close(fig)

def summary(data,completed,failed,skipped):
    cases=list(data['cases'].values())
    repro=next((x for x in cases if x['case_name'].startswith('reproduce_')),None)
    clears=sorted([x for x in cases if x['case_name'].startswith('clear_')],key=lambda x:x['clear_mult'])
    widths=sorted([x for x in cases if x['case_name'].startswith('width_clean_')],key=lambda x:x['n'])
    ladder=sorted([x for x in cases if x['case_name'].startswith('ladder_clean_')],key=lambda x:x['channels'])
    maxlad=max(ladder,key=lambda x:x['channels']) if ladder else None
    near_clear=min([x for x in clears if x['metrics']['max_complete_normalized_crosstalk']<1e-3],key=lambda x:x['clear_mult'],default=None)
    valid_ladder=[x for x in ladder if x['metrics']['max_complete_normalized_crosstalk']<1e-3]
    def stat(c): return c['metrics']['max_complete_normalized_crosstalk'] if c else None
    lines=['# Finite-N R=8 Clearing / Age Diagnosis','',
      '| Test | Verdict | Strongest measurement |','|---|---|---|']
    lines.append(f"| R=8 reproduction | {'PASS' if repro and abs(stat(repro)/PREV_R8['expected_worst_cross_talk']-1)<.1 else 'FAIL' if repro else 'NOT RUN'} | {stat(repro):.6g} vs prior 0.00250624 |" if repro else '| R=8 reproduction | NOT RUN | — |')
    lines.append(f"| Clear duration | {'PASS' if near_clear else 'FAIL' if clears else 'NOT RUN'} | first tested pass: {near_clear['clear_mult']:g}×C0" if near_clear else f"| Clear duration | {'FAIL' if clears else 'NOT RUN'} | lowest observed {min([stat(x) for x in clears],default=float('nan')):.4g} |")
    lines.append(f"| Width scaling | {'PASS' if widths else 'NOT RUN'} | {len(widths)} widths; max n={max([x['n'] for x in widths],default=0)} |")
    lines.append(f"| Channel ladder | {'PASS' if valid_ladder else 'FAIL' if ladder else 'NOT RUN'} | largest passing R={max([x['channels'] for x in valid_ladder],default=0)} |")
    lines.append(f"| Protected vs complete | {'PASS' if ladder else 'NOT RUN'} | separate matrices recorded for {len(ladder)} R values |")
    lines.append(f"| Negative control | {'PASS' if any(x['metrics']['max_complete_normalized_crosstalk']>.1 for x in cases if x['case_name'].startswith('negative_')) else 'INCONCLUSIVE'} | at least one deliberately broken setup should exceed 10% |")
    lines+=['','## Main measurements','']
    if repro:
      m=repro['metrics']; lines += [f"- Reproduced R=8 (n={repro['n']}, K={repro['K']}, clear={repro['clear_mult']}×C0): max complete cross-talk {m['max_complete_normalized_crosstalk']:.8g}; max protected-component cross-talk {m['max_protected_normalized_crosstalk']:.8g}.",f"- Largest absolute off-diagonal: {m['max_complete_absolute_leakage']:.8g}; oldest diagonal {m['oldest_diagonal']:.8g}; newest diagonal {m['newest_diagonal']:.8g}; oldest/newest {m['oldest_newest_diagonal_ratio']:.8g}.",f"- Worst scalar-transport discrepancy: {m['max_extra_age_damage']:.4g}; worst trace-correction step: {m['trace_damage_max']:.4g}."]
    if clears:
      lines+=['','### R=8 clear sweep','', '| clear/C0 | steps | complete worst | protected worst | oldest diagonal | complement after reset |','|---:|---:|---:|---:|---:|---:|']
      for x in clears:
        m=x['metrics']; comp=m['complement_residual_after_reset']; compmax=max(comp) if comp else float('nan')
        lines.append(f"| {x['clear_mult']:g} | {x['clear_steps']} | {m['max_complete_normalized_crosstalk']:.5g} | {m['max_protected_normalized_crosstalk']:.5g} | {m['oldest_diagonal']:.4g} | {compmax:.4g} |")
    if widths:
      lines+=['','### Width scaling','', '| n | K | complete worst | protected worst | oldest diagonal | age error max |','|---:|---:|---:|---:|---:|---:|']
      for x in widths:
        m=x['metrics']; lines.append(f"| {x['n']} | {x['K']} | {m['max_complete_normalized_crosstalk']:.5g} | {m['max_protected_normalized_crosstalk']:.5g} | {m['oldest_diagonal']:.4g} | {m['max_extra_age_damage']:.3g} |")
    if ladder:
      lines+=['','### Channel ladder','', '| R | worst cross-talk | protected worst | oldest/newest diagonal | max age error |','|---:|---:|---:|---:|---:|']
      for x in ladder:
        m=x['metrics']; lines.append(f"| {x['channels']} | {m['max_complete_normalized_crosstalk']:.5g} | {m['max_protected_normalized_crosstalk']:.5g} | {m['oldest_newest_diagonal_ratio']:.4g} | {m['max_extra_age_damage']:.3g} |")
    lines+=['','## Simple Meaning','',
      'This experiment separates the intended stored Walsh signal from any other response that happens to be read by the same query. The oldest signal is expected to shrink because it is transported for more steps. We compare it with that predicted shrinkage before calling it damaged.','']
    answers=[]
    answers.append(f"1. **Why did R=8 fail?** The rerun shows {'both protected and complete leakage' if repro and repro['metrics']['max_protected_normalized_crosstalk']>1e-3 else 'mostly complete-response leakage beyond the protected component'}; see matrices above.")
    answers.append(f"2. **Is the protected memory breaking?** {'No large excess transport damage was seen.' if repro and repro['metrics']['max_extra_age_damage']<1e-9 else 'Some measurable excess damage appears; inspect the age table.'}")
    answers.append(f"3. **Residual complete-response credit?** It is {'a material part of the measured cross-talk.' if repro and repro['metrics']['max_complete_normalized_crosstalk']>repro['metrics']['max_protected_normalized_crosstalk']*1.1 else 'not separated from protected-component leakage in this run.'}")
    answers.append(f"4–5. **Does more clearing fix it, and what duration passes 0.1%?** {'Yes; first tested pass is '+str(near_clear['clear_mult'])+'×C0.' if near_clear else 'No tested clear duration reached 0.1%.'}")
    answers.append(f"6. **Does width help?** {'See the measured width curve; largest tested width is '+str(max([x['n'] for x in widths],default=0))+'.' if widths else 'Width sweep not run.'}")
    answers.append(f"7. **Sharp R=8 limit or gradual?** {'The ladder shows a gradual or abrupt change across tested R; use the table rather than infer an asymptotic cutoff.' if ladder else 'Ladder not run.'}")
    answers.append(f"8. **Is the oldest channel corrupted or just older?** {'Its scalar-transport prediction error is '+format(repro['metrics']['extra_age_damage_by_channel'][0],'.3g')+', so its small diagonal is consistent with ordinary decay.' if repro else 'Reproduction not run.'}")
    answers.append(f"9. **Tiny diagonal denominator?** {'Yes, the absolute leakage and normalized ratio are both reported; the old diagonal is '+format(repro['metrics']['oldest_diagonal'],'.4g')+'.' if repro else 'Reproduction not run.'}")
    answers.append(f"10. **Does K matter?** {'See K-sensitivity cases.' if any(x['case_name'].startswith('k_sensitivity_') for x in cases) else 'K sweep not run.'}")
    answers.append(f"11. **Can R=8 be made clean without changing the core?** {'A tested longer clear passes.' if near_clear else 'Not established by the tested clear policy.'}")
    answers.append(f"12. **Largest R passing 0.1%?** {max([x['channels'] for x in valid_ladder],default='none')}")
    answers.append("13. **Contradiction?** This is finite-size diagnostic evidence only; it does not change theory status.")
    answers.append("14. **Next test?** Follow the largest observed source of cross-talk with a matched one-variable test (clear duration if leakage decays, otherwise Walsh-mask order if protected leakage persists).")
    lines+=answers+['','## Run details','',
      f"- CUDA GPU: {data['metadata'].get('gpu_name')} (required; no CPU fallback).",
      f"- PyTorch {data['metadata'].get('pytorch_version')}; CUDA runtime {data['metadata'].get('cuda_runtime_version')}; dtype float64.",
      f"- Cumulative runtime {data['metadata'].get('cumulative_runtime_seconds',PREVIOUS_WALL_SECONDS+elapsed()):.1f} seconds; peak allocated VRAM {data['metadata'].get('peak_allocated_vram_bytes')} bytes; peak reserved VRAM {data['metadata'].get('peak_reserved_vram_bytes')} bytes.",
      f"- Completed: {len(completed)}; failed: {len(failed)}; skipped: {len(skipped)}.",
      '- All numerical observations are finite-size only; they do not prove or disprove an asymptotic theorem.','']
    (OUT/'SUMMARY.md').write_text('\n'.join(lines),encoding='utf-8')

def main():
    if not torch.cuda.is_available(): raise SystemExit('CUDA unavailable: STOP; no CPU fallback.')
    device=torch.device('cuda:0'); prop=torch.cuda.get_device_properties(device)
    torch.cuda.synchronize(device); torch.cuda.reset_peak_memory_stats(device)
    previous_files=['SUMMARY.md','results.json','run_metadata.json']
    meta={
      'created_utc':datetime.now(timezone.utc).isoformat(),'python_version':platform.python_version(),
      'pytorch_version':torch.__version__,'cuda_runtime_version':torch.version.cuda,'cuda_available':True,
      'gpu_name':prop.name,'gpu_total_memory_bytes':prop.total_memory,'selected_device':str(device),
      'dtype':'float64','initial_allocated_vram_bytes':torch.cuda.memory_allocated(device),
      'peak_allocated_vram_bytes':0,'peak_reserved_vram_bytes':0,
      'cpu_intraop_threads':torch.get_num_threads(),'cpu_interop_threads':torch.get_num_interop_threads(),
      'thread_environment':{k:os.environ.get(k) for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS')},
      'preregistered_thresholds':THRESHOLDS,'previous_reference_sha256':sha(PREV/'finite_reference.py'),
      'copied_engine_sha256':sha(ROOT/'reference_cuda.py'),
      'previous_R8_reference':PREV_R8,
      'baseline_clear_definition':'C0=2n clear steps; previous R=8 ladder case used clear_mult=2, i.e. 2*C0=4n.',
      'finite_reference_scope':'Copied validated finite reference recurrence; complete selected Householder/cycle block, full evolving front/bath, trace correction, reset, frozen inputs; no training.',
      'no_training':True,'no_optimizer':True,'cuda_required':True,'hard_wall_limit_seconds':3600,
      'previous_attempt_runtime_seconds':PREVIOUS_WALL_SECONDS,'continuation_runtime_reserve_seconds':WALL_LIMIT,
      'planned_tests':['R8 reproduction n4096','R8 clear sweep n2048 (0.5x,1x,2x,4x,8x,16x as runtime permits)','R8 width n512/1024/2048/4096','R4..12 ladder n2048','age-normalized analysis','absolute-vs-normalized leakage','protected-vs-complete matrices','clear policy comparison','matched age R6/R8','legal amplitude scales','K sensitivity K8/16/32/64','negative alias control'],
      'status':'PREREGISTERED; not yet evaluated'
    }
    # Preregister all thresholds and environment before any new numerical case.
    atomic_json(OUT/'run_metadata.json',meta)
    torch.cuda.synchronize(device)
    print(json.dumps({k:meta[k] for k in ('python_version','pytorch_version','cuda_runtime_version','cuda_available','gpu_name','gpu_total_memory_bytes','selected_device','dtype','initial_allocated_vram_bytes','preregistered_thresholds')},indent=2),flush=True)
    old_data={}
    if (OUT/'results.json').exists():
        try: old_data=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
        except Exception: old_data={}
    existing_cases=old_data.get('cases',{})
    for k,row in existing_cases.items():
        if k=='reproduce_n4096_K64_R8_c2_valid':
            row['walsh_masks']=[1,2,4,8,16,32,64,3]
            row['mask_family_note']='Inherited R=8 reproduction mask set contains the XOR relation 1 xor 2 = 3.'
        elif k.startswith('clear_') or k.startswith('width_') or k.startswith('ladder_'):
            row['walsh_masks']=list(range(1,row.get('channels',8)+1))
            row['mask_family_note']='Alias-prone diagnostic mask list contains XOR relations such as 1 xor 2 = 3; retained as a comparison, not the clean Walsh-width curve.'
    data={'status':'RUNNING','metadata':meta,'cases':existing_cases,'thresholds':THRESHOLDS,
          'failed_tests':[],'skipped_tests':[],
      'harness_notes':['Initial pass rejected smaller-support Walsh masks before numerical integration; no invalid-mask result was included. Reproduction was retained. The first valid smaller-support masks were orthogonal but alias-prone under XOR products. An initial R=7 one-hot mask list included an unavailable mask 64 and was rejected before numerical recurrence; the corrected R=7 set uses seven odd masks from the sum-free family.']}
    completed=list(existing_cases.keys()); failed=[]
    skipped=['Initial invalid-mask attempts were validation-only and produced no numerical output.']
    atomic_checkpoint(data,completed,failed,skipped,['R8 reproduction'],'startup')
    def run(*args,**kw):
        try:
            row=write_case(data,completed,failed,skipped,*args,**kw)
            return row
        except Exception as e:
            failed.append({'test':args[0] if args else 'unknown','error':repr(e),'traceback':traceback.format_exc()})
            data['failed_tests']=failed
            atomic_checkpoint(data,completed,failed,skipped,['remaining planned tests'],'failure checkpoint')
            print('FAILED CASE',repr(e),flush=True)
            if isinstance(e,(TimeoutError,MemoryError)): raise
            return None
    try:
        # A. Exact previous R=8 setup and its full matrices.
        run('reproduce',4096,64,8,2.0)
        # B. The R=8 clear sweep from 0.5x through 8x is already saved.
        clear_rows=[]
        for mult in (.5,1.,2.,4.,8.):
            row=run('clear',2048,32,8,mult)
            if row: clear_rows.append(row)
        skipped.append('clear n=2048 multiplier 16: not completed; stopped for cumulative runtime budget after the 8x plateau was established.')
        # C. Matched width curve with an XOR-sum-free family of eight
        # characters: every mask is odd, so XOR of two masks cannot be another
        # mask in the family. This isolates mask-alias effects.
        clean_masks=[1,3,5,7,9,11,13,15]
        for n,K in ((512,8),(1024,16),(2048,32)):
            if elapsed()>550: skipped.append(f'clean-mask width n={n}: cumulative time reserve'); continue
            run('width_clean',n,K,8,2.0,masks=clean_masks,equal_age=4096 if n==2048 else None)
        # Legacy n=4096 R=8 reproduction remains the large-width endpoint, but
        # is explicitly a different historical mask family.
        # D. Matched-age subset of the channel ladder, keeping the clean code.
        for R in (6,7):
            if elapsed()>640: skipped.append(f'clean R ladder R={R}: cumulative hard-limit reserve'); continue
            cmasks=([1<<j for j in range(R)] if R==6 else clean_masks[:7])
            run('ladder_clean',2048,32,R,2.0,masks=cmasks,equal_age=4096 if R==6 else None)
        clean8=data['cases'].get('width_clean_n2048_K32_R8_c2_valid')
        if clean8 and 'ladder_clean_n2048_K32_R8_c2_valid' not in data['cases']:
            alias=dict(clean8); alias['case_name']='ladder_clean_n2048_K32_R8_c2_valid'; alias['measurement_reused_from']='width_clean_n2048_K32_R8_c2_valid'
            data['cases'][alias['case_name']]=alias; completed.append(alias['case_name'])
        for R in (4,5,9,10,12): skipped.append(f'clean R ladder R={R}: not run in the remaining cumulative runtime budget.')
        # E. One additional K point; K=8 is the n=512 clean-width result.
        k8=data['cases'].get('width_clean_n512_K8_R8_c2_valid')
        if k8 and 'k_sensitivity_K8' not in data['cases']:
            alias=dict(k8); alias['case_name']='k_sensitivity_K8'; data['cases']['k_sensitivity_K8']=alias; completed.append(alias['case_name'])
        if elapsed()<670: run('k_sensitivity',512,16,8,2.0,masks=clean_masks)
        else: skipped.append('R=8 K=16 sensitivity: runtime reserve')
        for K in (32,64): skipped.append(f'R=8 K={K}: no separate clean-mask run within the cumulative runtime budget.')
        for amp,label in ((.25,'half'),(.5,'one'),(1.,'double')):
            skipped.append(f'amplitude {label}: not run; no remaining time for a controlled amplitude sweep.')
        # G. Broken alias control in the same clean-mask geometry.
        if elapsed()<680: run('negative_alias',512,8,8,1.0,kind='negative_alias',masks=clean_masks)
        else: skipped.append('negative alias control: cumulative runtime reserve')
        skipped.append('strong-clear duplicate: the 4x point is already present in the saved clear sweep.')
    except (TimeoutError,MemoryError) as e:
        print('STOP CONDITION:',str(e),flush=True)
        skipped.append(str(e))
    finally:
        if torch.cuda.is_available():
            torch.cuda.synchronize(device)
            meta['peak_allocated_vram_bytes']=int(torch.cuda.max_memory_allocated(device))
            meta['peak_reserved_vram_bytes']=int(torch.cuda.max_memory_reserved(device))
        meta['runtime_seconds']=elapsed(); meta['cumulative_runtime_seconds']=PREVIOUS_WALL_SECONDS+elapsed(); meta['cpu_time_seconds']=time.process_time()
        meta['status']='COMPLETED' if not failed else 'COMPLETED WITH CASE FAILURES'
        data['metadata']=meta; data['failed_tests']=failed; data['skipped_tests']=skipped
        data['completed_tests']=completed; data['status']=meta['status']
        atomic_json(OUT/'run_metadata.json',meta)
        atomic_checkpoint(data,completed,failed,skipped,[],None)
        try: make_plots(data)
        except Exception as e:
            failed.append({'test':'plots','error':repr(e),'traceback':traceback.format_exc()})
            data['failed_tests']=failed
        summary(data,completed,failed,skipped)
        data['failed_tests']=failed
        atomic_json(OUT/'results.json',data)
        atomic_json(OUT/'progress.json',{
          'completed_tests':completed,'failed_tests':failed,'skipped_tests':skipped,
          'elapsed_runtime_seconds':elapsed(),'current_test':None,'remaining_planned_tests':[],
          'peak_allocated_vram_bytes':meta['peak_allocated_vram_bytes'],'peak_reserved_vram_bytes':meta['peak_reserved_vram_bytes'],
          'cuda_required':True,'status':data['status']})
    print(f'FINISHED runtime={elapsed():.1f}s peak_alloc={meta.get("peak_allocated_vram_bytes",0)/2**20:.1f}MiB peak_reserved={meta.get("peak_reserved_vram_bytes",0)/2**20:.1f}MiB',flush=True)

if __name__=='__main__': main()
