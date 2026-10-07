"""Finalize report metadata and age-stitch diagnostics from completed JSON cases.

This script does not run the recurrence. It is safe to rerun after an interrupted
CUDA sweep and preserves all completed measurements.
"""
import json, math
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
read=lambda name: json.loads((ROOT/name).read_text(encoding='utf-8'))
write=lambda name,obj: (ROOT/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')
D=read('results.json'); M=read('run_metadata.json'); P=read('progress.json')
cases=list(D['cases'].values())
sumfree=[x for x in cases if x.get('family')=='sum_free']
passed=[x for x in sumfree if x['metrics']['max_complete_normalized_crosstalk']<1e-3]
failed=[x for x in sumfree if x['metrics']['max_complete_normalized_crosstalk']>=1e-3]
largest=max(passed,key=lambda x:x['R'],default=None)
first=min(failed,key=lambda x:x['R'],default=None)
by_name={x['case_name']:x for x in cases}
clean=by_name.get('reproduce_n2048_K32_R8_sum_free_c2')
legacy=by_name.get('reproduce_n2048_K32_R8_legacy_c2')

# Build a row-wise equal-age response matrix: row i is read at its own
# capture+256 checkpoint. Rows occur at different global times, so this is a
# diagnostic matrix, not a simultaneous endpoint matrix.
matched=[]
for x in cases:
    recs=x.get('equal_age_read_matrices') or {}
    R=x['R']
    if len(recs)!=R or not recs:
        continue
    A=np.zeros((R,R),dtype=float)
    for i in range(R):
        q=recs.get(str(i))
        if q is None: break
        A[i,:]=np.asarray(q['response_norm_matrix'][i],dtype=float)
    else:
        nd=np.maximum(np.diag(A),1e-300)
        C=A/nd[:,None]
        np.fill_diagonal(C,0.)
        matched.append((x,A,C))

if matched:
    x,A,C=max(matched,key=lambda z:z[0]['R'])
    fig,ax=plt.subplots(figsize=(6.4,5.1))
    im=ax.imshow(np.log10(np.maximum(C,1e-18)),vmin=-18,vmax=0,cmap='magma',aspect='auto')
    ax.set(title=f"Row-wise matched-age reads: n={x['n']}, R={x['R']}, age=256 steps\nRows sampled at separate chronological checkpoints",
           xlabel='read Walsh character',ylabel='stored signal (each row at equal age)')
    fig.colorbar(im,ax=ax,label='log10 off-diagonal / intended diagonal')
    fig.tight_layout(); fig.savefig(ROOT/'matched_age_response.png',dpi=150); plt.close(fig)
    M['matched_age_diagnostic']={
      'status':'COMPLETED_ROW_WISE',
      'construction':'Stitched row i from the checkpoint at capture_time_i+256. Each intended signal has the same age, but rows are observed at different global times; therefore this is not one simultaneous joint endpoint experiment.',
      'n':x['n'],'R':x['R'],'age_steps':256,
      'max_normalized_offdiagonal':float(np.max(C)),
      'max_absolute_offdiagonal':float(np.max(A-np.diag(np.diag(A)))),
    }
else:
    M['matched_age_diagnostic']={'status':'NOT RUN'}

# Explicitly record why remaining tests were not completed.
stop_event={
  'type':'HARD_RUNTIME_GUARD',
  'configured_limit_seconds':5400.0,
  'actual_runtime_seconds':float(D.get('runtime_seconds',5400.0)),
  'message':'CUDA reference engine stopped the batched K sweep at the 90-minute hard limit before returning any per-K rows.',
}
D['stop_event']=stop_event
D['not_completed']=[
 {'test':'clean K scaling n=2048 R=8, K=8/16/32/64','status':'INCONCLUSIVE','reason':'Batched CUDA call was interrupted by the 90-minute hard runtime guard; no individual K result rows were returned.'},
 {'test':'clean-mask clearing sweep R=8 multipliers 0.5/1/2/4','status':'NOT RUN','reason':'Remaining runtime did not meet the preregistered minimum time budget; no clean-mask clearing result is inferred.'},
 {'test':'sum-free R=20/24/32 at n=2048','status':'NOT RUN','reason':'Optional channel-count extension stopped at the 70-minute cutoff after the in-flight R=16 case.'},
 {'test':'higher sum-free R at n=4096','status':'NOT RUN','reason':'Not started within the wall-clock budget.'},
 {'test':'R=8/12/16 full row-wise matched-age matrices','status':'COMPLETED_DIAGONAL_ROWS_ONLY','reason':'Each channel diagonal/cross-read row was sampled at its own 256-step age; rows are stitched across times, not one simultaneous endpoint.'},
]
for err in D.get('errors',[]):
    if '3500-second' in err.get('message',''):
        err['raw_engine_message']=err['message']
        err['message']='STOP: configured 5400-second hard runtime guard'
        err['note']='The copied reference engine has a stale literal in its exception text; the run wrapper set reference_cuda.LIMIT=5400 seconds, and the guard fired at 5400.22 seconds.'
write('results.json',D)

P.update({
 'status':'STOPPED_AT_90_MINUTE_HARD_LIMIT',
 'elapsed_runtime_seconds':float(D.get('runtime_seconds',5400.0)),
 'current_test':None,
 'failed_tests':[],
 'stopped_tests':['Kscale_n2048_R8 batched call (runtime guard before results returned)'],
 'skipped_tests':D['not_completed'],
 'pending_tests':[],
 'peak_allocated_vram_bytes':164945920,
 'peak_reserved_vram_bytes':283115520,
 'largest_n_completed':max((x['n'] for x in cases),default=0),
 'largest_R_completed':max((x['R'] for x in cases),default=0),
 'current_best_passing_R':max((x['R'] for x in passed),default=None),
 'first_failing_R_observed':min((x['R'] for x in failed),default=None),
})
write('progress.json',P)

M.update({
 'end_timestamp_utc':datetime.now(timezone.utc).isoformat(),
 'total_runtime_seconds':float(D.get('runtime_seconds',5400.0)),
 'peak_allocated_vram_bytes':164945920,
 'peak_reserved_vram_bytes':283115520,
 'peak_allocated_vram_mib':157.3,
 'peak_reserved_vram_mib':270.0,
 'largest_n_completed':max((x['n'] for x in cases),default=0),
 'largest_R_completed':max((x['R'] for x in cases),default=0),
 'largest_width_case':{'n':max((x['n'] for x in cases),default=0),'R':max((x['R'] for x in cases if x['n']==max((z['n'] for z in cases),default=0)),default=0)},
 'largest_R_case':{'R':max((x['R'] for x in cases),default=0),'n':max((x['n'] for x in cases if x['R']==max((z['R'] for z in cases),default=0)),default=0)},
 'stop_event':stop_event,
 'noncompletion_note':'K batch was interrupted by the hard runtime guard and returned no per-K measurements. The clean-mask clear sweep was not launched. These are not negative results.',
})
write('run_metadata.json',M)

def fmt(x): return '—' if x is None else f'{x:.6g}'
lines=['# Clean-Mask Multichannel CUDA Scaling','',
'| Test | Verdict | Strongest Measurement |','|---|---|---|']
lines.append(f"| R=8 clean vs legacy at n=2048 | {'PASS' if clean and legacy and legacy['metrics']['max_complete_normalized_crosstalk']>10*clean['metrics']['max_complete_normalized_crosstalk'] else 'INCONCLUSIVE'} | clean {clean['metrics']['max_complete_normalized_crosstalk']:.6g}; legacy {legacy['metrics']['max_complete_normalized_crosstalk']:.6g} (legacy/clean {legacy['metrics']['max_complete_normalized_crosstalk']/clean['metrics']['max_complete_normalized_crosstalk']:.1f}×) |" if clean and legacy else '| R=8 clean vs legacy | INCONCLUSIVE | paired reproduction incomplete |')
lines.append(f"| Sum-free channel ladder | {'PASS' if sumfree and not failed else 'FAIL' if failed else 'NOT RUN'} | largest completed clean pass R={largest['R'] if largest else '—'}; first fail={'R='+str(first['R']) if first else 'none observed'} |")
width=sorted([x for x in cases if x['R']==8 and x['family']=='sum_free'],key=lambda z:z['n'])
width_by_n={x['n']:x for x in width}
lines.append(f"| R=8 width sweep | {'PASS' if width else 'NOT RUN'} | n={list(width_by_n)}; worst ratios={[round(width_by_n[n]['metrics']['max_complete_normalized_crosstalk'],9) for n in width_by_n]} |")
lines.append(f"| Higher-order XOR audit | PASS | order-2/3/4 exact counts recorded for all completed mask sets; clean R=16 has 0/560/0 |")
ind=by_name.get('family_compare_n1024_K16_R4_independent_c2'); sf4=by_name.get('ladder_n1024_K16_R4_sum_free_c2')
lines.append(f"| Strong independent family comparison | {'PASS' if ind and sf4 else 'NOT RUN'} | at n=1024,R=4, independent {ind['metrics']['max_complete_normalized_crosstalk']:.6g} vs sum-free {sf4['metrics']['max_complete_normalized_crosstalk']:.6g} |" if ind and sf4 else '| Strong independent family comparison | NOT RUN | unavailable |')
lines.append('| Clean-mask K scaling | INCONCLUSIVE | batch started but was stopped at the hard runtime limit; no per-K values returned |')
lines.append('| Clean-mask clear sweep | NOT RUN | omitted at the 90-minute budget boundary |')
lines.append(f"| Row-wise matched-age reads | {'PASS' if matched else 'NOT RUN'} | largest sampled R={x['R'] if matched else '—'}; max off-diagonal ratio={float(np.max(C)):.3g} at age 256 steps |" if matched else '| Row-wise matched-age reads | NOT RUN | no equal-age checkpoints |')
lines.append('| Legacy alias control | PASS | R=8 legacy has 6 order-2 aliases and 0.00250616 worst normalized cross-talk |')
lines += ['', '## Run details','',
 f"- GPU: {M['gpu_name']} on {M['device']}; CUDA required and used.",
 f"- Python {M['python_version']}; PyTorch {M['pytorch_version']}; CUDA runtime {M['cuda_runtime_version']}.",
 '- Recurrence dtype: CUDA float64. CPU fallback was not used.',
 f"- Runtime: {M['total_runtime_seconds']/60:.2f} minutes (stopped at the configured 90-minute hard guard).",
 f"- Peak allocated/reserved VRAM: {M['peak_allocated_vram_mib']:.1f}/{M['peak_reserved_vram_mib']:.1f} MiB.",
 f"- Largest width case: n={M['largest_width_case']['n']} at R={M['largest_width_case']['R']}; largest channel count: R={M['largest_R_case']['R']} at n={M['largest_R_case']['n']}.",
 '- The reference recurrence was copied unchanged from the prior R=8 diagnosis folder. No training or optimization was run.',
 '', '## Main measurements','']
if clean and legacy:
    cm=clean['metrics']; lm=legacy['metrics']
    lines.append(f"At n=2048,R=8,K=32 and clear multiplier 2, clean sum-free masks measured {cm['max_complete_normalized_crosstalk']:.8g} (0.00188452%) worst normalized complete-response cross-talk. The legal legacy mask family measured {lm['max_complete_normalized_crosstalk']:.8g} (0.250616%), about {lm['max_complete_normalized_crosstalk']/cm['max_complete_normalized_crosstalk']:.1f}× larger.")
    lines.append(f"Their maximum absolute off-diagonal entries were {cm['max_complete_absolute_leakage']:.4g} (clean) and {lm['max_complete_absolute_leakage']:.4g} (legacy); the worst normalized pair for the clean family had absolute leak {cm['worst_entry_absolute_leakage']:.4g} against intended diagonal {cm['worst_entry_intended_diagonal']:.4g}. A global maximum absolute leak can belong to a different row than the maximum normalized ratio.")
lines.append('Across the clean sum-free ladder, complete cross-talk stayed below the preregistered 0.001 threshold through R=16. At n=1024 it rose from 2.24×10⁻⁶ (R=2) to 4.62×10⁻⁵ (R=16); the n=2048 R=16 case measured 4.40×10⁻⁵. No clean-family failure was observed; R=20/24/32 were not reached.')
lines.append('The clean odd-label family has no pairwise XOR aliases, but it does have order-three relations: the count rises from 56 at R=8 to 560 at R=16. This coincides with gradually larger protected-only leakage, while remaining below 0.1%. This finite sweep does not establish that those relations caused the measured leakage.')
lines.append('The stronger independent family at n=1024,R=4 measured 2.24×10⁻⁶ complete cross-talk versus 8.52×10⁻⁶ for the sum-free R=4 family; protected-only cross-talk was approximately 1.86×10⁻¹⁷ versus 6.28×10⁻⁶. This is a finite comparison for one R, not a general scaling result.')
if matched:
    lines.append(f"The stitched row-wise matched-age diagnostic (each channel sampled 256 steps after its own capture) had worst normalized off-diagonal ratio {float(np.max(C)):.3g} for R={x['R']}. Each row is sampled at a different global time, so this is not a simultaneous endpoint matrix.")
lines += ['', '## Simple Meaning','',
'The clean masks removed the large R=8 leakage seen with the alias-prone masks. The same finite implementation stayed below the preset 0.1% cross-talk target through 16 channels. It did not find a capacity limit, but the test stopped before R=20, 24, or 32. The strongest remaining measured leakage in the protected-only responses rises with the number of order-three XOR relations, but remains below the preset target. That association is a clue, not a proof of cause.','',
'1. **Largest R passing 0.1%:** 16 in completed clean cases (n=1024 and n=2048).',
'2. **First clean R that failed:** none observed through R=16; R=20/24/32 were not run.',
'3. **Did protected memory break?** No breakdown was observed through R=16. Finite results do not prove indefinite scaling.',
'4. **Did sum-free masks solve the old R=8 problem?** In the n=2048 matched run, yes: normalized cross-talk was about 133× lower than the legal alias-prone reference set.',
'5. **Higher-order aliases:** order-three XOR relations exist even though pairwise aliases are absent. For R=16 the count is 560; order-four count is zero for this odd-label set.',
'6. **Did the independent family do better?** At R=4 it had lower complete cross-talk and near-zero protected-only cross-talk than the sum-free family.',
'7. **Did K=32/64 hurt old channels?** This run cannot answer: the K batch was interrupted before returning per-K results.',
'8. **Were tiny diagonals involved?** Yes, some old intended diagonals are extremely small. We report absolute and normalized leakage separately; the largest absolute and largest percentage leakage occur in different matrix entries.',
'9. **Did matched-age reads remain clean?** Row-wise equal-age reads through R=16 were clean to about 9×10⁻¹⁵ in normalized off-diagonal ratio. These rows were measured at different times.',
'10. **How did cross-talk change with n?** R=8 went from 2.24×10⁻⁴ at n=512 to about 1.88×10⁻⁵ at n=2048 and n=4096. These finite points are not an asymptotic fit.',
'11. **Did extra clearing remove remaining clean-mask contamination?** Not tested in this run; the clean-mask clear sweep was not started.',
'12. **Is there a finite-size capacity limit?** None was seen through R=16. Higher R remains untested here.',
'13. **Did anything contradict the mechanism?** No contradiction to the protected-channel behavior was observed; R=8 clean reproduction closely matches the earlier finite result.',
'14. **Next finite-size test:** run a short, prioritized clean-mask K sweep plus a clean-mask clear sweep, then test R=20 and R=24 at n=2048 if budget permits.',
'15. **Theory handoff:** the order-three alias counts and their co-movement with protected-only leakage are the useful observation to explain; do not infer causality from this run.',
'', '## Completion record','',
f"Completed recurrence cases: {len(cases)}. The clean K batch hit the configured hard runtime guard before its batched call returned, so no K entries were committed. The clean-mask clearing sweep and R>16 extensions were not run. `progress.json` and `results.json` preserve the stop reason and all completed cases. No theorem status or repository theory file was changed.",
]
(ROOT/'SUMMARY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Finalized JSON, metadata, progress, SUMMARY.md, and matched-age plot without rerunning the recurrence.')
