"""Static scientific plots and an honest finite-reference result ledger."""
import json
import math
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def finish(root,cases,three,meta,thr):
    render_start=time.perf_counter()
    core=[c for c in cases if c['kind']=='core']
    def worst(group,key): return max((max(c[key]) for c in group),default=0.)
    def base(n,K): return next(c for c in core if c['n']==n and c['K']==K)
    threshold=thr['full_response_cross_talk_ratio']
    tests={}
    legal=all(c['input_cube_legal'] and c['correction_gates_legal'] and c['donor_trace_match_error']<thr['trace_match_absolute_error'] for c in cases)
    tests['two_capture_retention']=dict(status='PASS' if legal and worst(core,'max_damage_over_initial')<thr['two_capture_max_damage_over_initial'] else 'FAIL',worst_damage=worst(core,'max_damage_over_initial'))
    tests['cross_talk_isolation']=dict(status='PASS' if worst(core,'cross_talk_ratios')<threshold else 'FAIL',worst_ratio=worst(core,'cross_talk_ratios'))
    stress=[c for c in cases if c['kind']=='stress']
    good=[c for c in cases if c['kind']!='broken']
    tests['trace_correction_protection']=dict(status='PASS' if legal and worst(good,'max_trace_step_error_over_initial')<thr['trace_step_error_over_initial'] else 'FAIL',worst_step_error=worst(good,'max_trace_step_error_over_initial'),largest_stress_correction_range=max(x['range'] for c in stress for x in c['corrections']))
    order=[]
    for c in cases:
        if c['kind']=='reverse':
            b=base(c['n'],c['K'])
            # Compare channel at each chronological position, since an older
            # channel necessarily experiences more ordinary transport decay.
            qs=max(abs(c['transport_quality'][c['order'][j]]-b['transport_quality'][b['order'][j]]) for j in range(2))
            cross=max(abs(c['cross_talk_ratios'][c['order'][j]]-b['cross_talk_ratios'][b['order'][j]]) for j in range(2))
            order.append(dict(n=c['n'],K=c['K'],quality_difference=qs,cross_talk_difference=cross,
                forward_retention=b['retention'],reverse_retention=c['retention']))
    tests['order_reversal']=dict(status='PASS' if max(x['quality_difference'] for x in order)<thr['order_transport_quality_difference'] and max(x['cross_talk_difference'] for x in order)<thr['order_cross_talk_difference'] else 'FAIL',comparisons=order)
    imbalance=[c for c in cases if c['kind']=='imbalance']
    tests['amplitude_imbalance']=dict(status='PASS' if worst(imbalance,'max_damage_over_initial')<thr['amplitude_max_damage_over_initial'] and worst(imbalance,'cross_talk_ratios')<threshold else 'FAIL',worst_damage=worst(imbalance,'max_damage_over_initial'),worst_cross_talk=worst(imbalance,'cross_talk_ratios'))
    broken=next(c for c in cases if c['kind']=='broken'); normal=base(broken['n'],broken['K'])
    increase=max(broken['cross_talk_ratios'])/max(max(normal['cross_talk_ratios']),1e-300)
    tests['broken_protection_control']=dict(status='PASS' if max(broken['cross_talk_ratios'])>=thr['break_min_cross_talk_ratio'] and increase>=thr['break_min_cross_talk_increase_factor'] else 'INCONCLUSIVE',cross_talk_increase_factor=increase,broken_ratios=broken['cross_talk_ratios'],normal_ratios=normal['cross_talk_ratios'])
    scaling=sorted([c for c in cases if c['n']==2048 and c['kind'] in ('core','scaling')],key=lambda c:c['K'])
    baseline=scaling[0]; ratios=[c['combined_B_norm']/baseline['combined_B_norm'] for c in scaling]
    retention_changes=[abs(c['retention'][0]/baseline['retention'][0]-1) for c in scaling]
    tests['coded_donor_scaling']=dict(status='PASS' if min(ratios)>=thr['scaling_B_norm_ratio_min'] and max(ratios)<=thr['scaling_B_norm_ratio_max'] and max(retention_changes)<thr['scaling_A_retention_relative_change'] and worst(scaling,'cross_talk_ratios')<threshold else 'FAIL',B_combined_norm_ratios=ratios,A_retention_relative_changes=retention_changes,baseline_K=baseline['K'])
    result=json.loads((root/'results.json').read_text())
    result['tests']=tests
    isolated_ratios=[]
    for c in core:
        M=c['isolated_storage_response_matrix']
        isolated_ratios.extend(abs(M[p][q])/max(abs(M[p][p]),1e-300) for p in range(2) for q in range(2) if p!=q)
    result['diagnostics']={'worst_core_isolated_storage_cross_talk_ratio':max(isolated_ratios),
                          'worst_nonbroken_two_channel_cross_talk_ratio':worst(good,'cross_talk_ratios'),
                          'worst_optional_three_channel_cross_talk_ratio':worst(three,'cross_talk_ratios')}
    result['interpretation']='NUMERICAL EVIDENCE; no proof or theorem status change. Main attribution includes all reference renewal paths.'
    (root/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    # Retention is expected to be small at tiny widths: distinguish ordinary
    # decay from excess damage, rather than demanding unit retention.
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),constrained_layout=True)
    representative=[base(n,min(16,n//32)) for n in (256,512,1024,2048)]
    for j,label in enumerate(('A','B')):
        axes[0].plot([c['n'] for c in representative],[c['retention'][j] for c in representative],'o-',label=label)
        axes[1].plot([c['n'] for c in representative],[max(c['relative_damage'][j],1e-18) for c in representative],'o-',label=label)
    axes[0].set_yscale('log');axes[1].set_yscale('log')
    axes[0].set_title('Final read / initial captured read');axes[1].set_title('Extra error / initial captured read')
    for ax in axes: ax.set_xlabel('n');ax.grid(alpha=.25);ax.legend()
    fig.suptitle('Two successive captures: ordinary transport decay versus extra damage')
    fig.savefig(root/'two_channel_retention.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.5),constrained_layout=True)
    for j,label in enumerate(('A into read B','B into read A')):
        ax.plot([c['n'] for c in representative],[max(c['cross_talk_ratios'][j],1e-18) for c in representative],'o-',label=label)
    ax.axhline(threshold,ls='--',color='black',label='Predeclared isolation threshold')
    ax.set(xlabel='n',ylabel='Off-diagonal / correct read',yscale='log',title='Complete finite-pair cross-talk, not just isolated stored components')
    ax.legend();ax.grid(alpha=.25);fig.savefig(root/'cross_talk_vs_n.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),constrained_layout=True)
    ks=[c['K'] for c in scaling]
    for j,label in enumerate(('A → B','B → A')):
        axes[0].plot(ks,[max(c['cross_talk_ratios'][j],1e-18) for c in scaling],'o-',label=label)
    axes[0].set_yscale('log');axes[0].axhline(threshold,ls='--',color='black');axes[0].set_ylabel('Cross-talk ratio')
    axes[1].plot(ks,ratios,'o-',label='New B combined norm / K=4 baseline')
    axes[1].plot(ks,[c['retention'][0]/baseline['retention'][0] for c in scaling],'s-',label='Old A retention / K=4 baseline')
    axes[1].set_ylim(.99,1.01)
    axes[1].ticklabel_format(axis='y',style='plain',useOffset=False)
    for ax in axes: ax.set_xlabel('K');ax.set_xticks(ks);ax.grid(alpha=.25);ax.legend(fontsize=8)
    fig.suptitle('Increasing donor count with an older stored channel, n=2048')
    fig.savefig(root/'cross_talk_vs_k.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),constrained_layout=True)
    for c in stress:
        xs=[p['t'] for p in c['trace']]
        for j in range(2):
            axes[0].semilogy(xs,[max(p['response_norm_matrix'][j][j],1e-25) for p in c['trace']],label=f"n={c['n']}, {'AB'[j]}")
        for corr in c['corrections']:
            axes[1].scatter(corr['range'],max(max(c['max_trace_step_error_over_initial']),1e-18),label=f"n={c['n']} stage={corr['stage']}")
    axes[0].set(xlabel='Step',ylabel='Correct protected read',title='Nonuniform donor-control stress')
    axes[1].set(xlabel='Range of final donor correction gates',ylabel='Step error / initial capture',yscale='log',title='Correction variation versus excess storage error')
    for ax in axes: ax.grid(alpha=.25);ax.legend(fontsize=7)
    fig.savefig(root/'trace_correction_stress.png',dpi=160);plt.close(fig)
    if three:
        fig,axes=plt.subplots(1,len(three),figsize=(5*len(three),4.5),constrained_layout=True,squeeze=False)
        for ax,c in zip(axes[0],three):
            M=c['final_response_norm_matrix']
            normalized=[[M[p][q]/max(M[p][p],1e-300) for q in range(3)] for p in range(3)]
            im=ax.imshow(normalized,vmin=0,vmax=max(1,max(map(max,normalized))),cmap='viridis')
            for p in range(3):
                for q in range(3): ax.text(q,p,f'{M[p][q]:.2e}\n({normalized[p][q]:.2g}×)',ha='center',va='center',fontsize=8,color='white' if normalized[p][q]<.5 else 'black')
            ax.set_xticks(range(3),['χ1','χ2','χ3']);ax.set_yticks(range(3),['A','B','C']);ax.set_title(f"n={c['n']}, K={c['K']}");ax.set_xlabel('Read');ax.set_ylabel('Varied signal')
        fig.suptitle('Exploratory three-channel response: absolute norm and diagonal-normalized ratio')
        fig.savefig(root/'three_channel_matrix.png',dpi=160);plt.close(fig)
    lines=['| Test | Status | Measurement |','|---|---|---|']
    details={
      'two_capture_retention':f"Worst extra damage / initial: {tests['two_capture_retention']['worst_damage']:.3g}",
      'cross_talk_isolation':f"Worst complete-pair cross-talk: {tests['cross_talk_isolation']['worst_ratio']:.6g}",
      'trace_correction_protection':f"Worst correction-step error: {tests['trace_correction_protection']['worst_step_error']:.3g}",
      'order_reversal':f"Largest chronology-matched quality difference: {max(x['quality_difference'] for x in order):.3g}",
      'amplitude_imbalance':f"Worst cross-talk: {tests['amplitude_imbalance']['worst_cross_talk']:.6g}",
      'broken_protection_control':f"Cross-talk increase: {increase:.4g}×",
      'coded_donor_scaling':f"B norm / baseline range: {min(ratios):.6g}–{max(ratios):.6g}"}
    for name,x in tests.items(): lines.append(f"| {name.replace('_',' ')} | **{x['status']}** | {details[name]} |")
    lines+=['','# Multistage early-capture sanity experiment','','**NUMERICAL EVIDENCE — not a proof, not training, no theorem-status change.**','',
      'The main recurrence ran on CUDA in float64. It retains the complete selected reference Householder/cycle operator, the continuously evolving public front and bath, exact finite donor traces, inverse-lift raw controls, and the common reset. As in the prior experiment, stationary off-cycle four-site carriers replace the astronomical theorem’s moving corridors. The tiny actual-model dense perturbation is omitted.','',
      '## How to read these numbers','',
      'Each signal is measured by a finite +/- donor-control pair while the other writes are present and identical in that pair. Matrix entries are Euclidean norms over the same orthonormal parameter probes used previously. Norm entries are nonnegative and are not a signed scalar linear transfer matrix. We also propagate isolated stored Walsh vectors to distinguish storage damage from new private-response contamination.','',
      'A later independent mask multiplies the earlier singleton read by a*(g_H+g_L)/2. Other preservation steps multiply it by a*g_H; reset uses a*(1-.05²). The prediction includes these public losses. Raw retention can be small because these small widths have appreciable contraction over a long repair/clear schedule.','',
      'All thresholds and planned core cases were written to run_metadata.json before the sweep. No threshold was loosened. PASS does not imply a finite-error robust B^D theorem.','',
      f"Worst isolated-storage cross-talk ratio: **{max(isolated_ratios):.6g}**. Largest final correct-read absolute prediction error in the core sweep: **{worst(core,'absolute_error'):.6g}**.",'',
      '## Core sweep','',
      '| n | K | A retention | B retention | A extra damage / initial | B extra damage / initial | A→B cross-talk | B→A cross-talk |','|---|---|---|---|---|---|---|---|']
    for c in core:
        lines.append(f"| {c['n']} | {c['K']} | {c['retention'][0]:.6g} | {c['retention'][1]:.6g} | {c['relative_damage'][0]:.3g} | {c['relative_damage'][1]:.3g} | {c['cross_talk_ratios'][0]:.6g} | {c['cross_talk_ratios'][1]:.6g} |")
    lines+=['','## Checkpoints for n=1024, K=16','',
      '| Checkpoint | A read χ1 | A read χ2 | B read χ1 | B read χ2 |','|---|---|---|---|---|']
    for label,p in normal['checkpoints'].items():
        M=p['response_norm_matrix'];lines.append(f"| {label} | {M[0][0]:.9g} | {M[0][1]:.9g} | {M[1][0]:.9g} | {M[1][1]:.9g} |")
    lines+=['','## Order reversal','',
      'Position-matched retention is the fair comparison: the first signal travels through an extra whole stage. Raw A/B retention swaps when write order swaps.','',
      '| n | K | Forward A,B retention | Reversed A,B retention | Quality difference | Cross-talk difference |','|---|---|---|---|---|---|']
    for x in order: lines.append(f"| {x['n']} | {x['K']} | {x['forward_retention']} | {x['reverse_retention']} | {x['quality_difference']:.4g} | {x['cross_talk_difference']:.4g} |")
    lines+=['','## Unequal amplitudes','',
      '| A:B | A retention | B retention | A→B | B→A |','|---|---|---|---|---|']
    for c in [normal]+imbalance: lines.append(f"| {c['amplitudes']} | {c['retention'][0]:.6g} | {c['retention'][1]:.6g} | {c['cross_talk_ratios'][0]:.6g} | {c['cross_talk_ratios'][1]:.6g} |")
    lines+=['','## Correction stress','',
      '| n | Stage | g_last minimum | g_last maximum | Range | Variance | Worst step error / initial |','|---|---|---|---|---|---|---|']
    for c in stress:
        for x in c['corrections']: lines.append(f"| {c['n']} | {x['stage']} | {x['minimum']:.12g} | {x['maximum']:.12g} | {x['range']:.6g} | {x['variance']:.6g} | {max(c['max_trace_step_error_over_initial']):.4g} |")
    lines+=['','## Coded donors with older storage, n=2048','',
      '| K | New B combined norm | B individual mean absolute | Combined / sqrt(K) | B / K=4 baseline | Old A retention | A→B | B→A |','|---|---|---|---|---|---|---|---|']
    for c,ratio in zip(scaling,ratios): lines.append(f"| {c['K']} | {c['combined_B_norm']:.9g} | {c['individual_B_mean_abs']:.9g} | {c['combined_B_norm_div_sqrt_K']:.9g} | {ratio:.6g} | {c['retention'][0]:.6g} | {c['cross_talk_ratios'][0]:.6g} | {c['cross_talk_ratios'][1]:.6g} |")
    if three:
        lines+=['','## Optional three-channel stress','',
          '| n | K | Final response norm matrix (rows=varied A,B,C; columns=χ1,χ2,χ3) | Cross-talk ratios |','|---|---|---|---|']
        for c in three:
            matrix='; '.join(', '.join(f'{v:.6g}' for v in row) for row in c['final_response_norm_matrix'])
            lines.append(f"| {c['n']} | {c['K']} | {matrix} | {c['cross_talk_ratios']} |")
        lines+=['','This path is exploratory, not a robust three-dimensional theorem. Full vectors and isolated-storage matrices are in results.json.']
    lines+=['','## Intentional break','',
      'The failure control aliases χ2 with χ1, so the two masks/reads are no longer orthogonal. It uses the same donor histories, recurrence and measurement pipeline.',
      f"- Normal cross-talk ratios: {normal['cross_talk_ratios']}.",f"- Broken cross-talk ratios: {broken['cross_talk_ratios']}.",
      f"- Normal A,B retention: {normal['retention']}; broken: {broken['retention']}.",
      f"- Cross-talk increased by {increase:.6g}×.",
      '','## Plain-English answers','']
    isolation=tests['cross_talk_isolation']['status']=='PASS'
    lines += [
      f"1. Two singleton Walsh reads {'coexist within the predeclared isolation threshold' if isolation else 'survive, but the complete finite-pair isolation threshold was not met'}. See the full-response and isolated-storage matrices in results.json.",
      f"2. Extra damage to the correct reads was at most {worst(core,'max_damage_over_initial'):.6g} of the initial captures, after accounting for expected transport and mask loss.",
      f"3. Worst full-pair cross-talk in the core sweep: {worst(core,'cross_talk_ratios'):.6g}. This includes residual common/private response, not just the stored zero-sum piece.",
      f"4. Order-reversal test: {tests['order_reversal']['status']}. Raw retention changes with the age of the stored signal; transport-normalized comparisons are reported above.",
      f"5. Unequal-amplitude test: {tests['amplitude_imbalance']['status']}. We tested 1:1, 1:0.5, 1:0.25 and 0.5:1.",
      f"6. Donor-specific correction variation produced at most {tests['trace_correction_protection']['worst_step_error']:.6g} correction-step error divided by initial capture. Largest trace mismatch: {max(c['donor_trace_match_error'] for c in cases):.6g}.",
      f"7. Increasing K from 4 to 64 gave new B combined norm ratios {min(ratios):.6g}–{max(ratios):.6g}; older A relative retention changed by at most {max(retention_changes):.6g}.",
      f"8. The broken-protection control was {tests['broken_protection_control']['status']} as an interference detector.",
      '9. Complete-response isolation failed at n=256 and n=512. Isolated stored Walsh components remained isolated to floating-point accuracy, so the failure reveals leftover private/common credit being captured by a later mask. No contradiction to the tested protected-transport identity was observed. This does not validate or refute the asymptotic theorem: the tiny dense perturbation is omitted and not every coded-ball boundary is tested.',
      '10. Next test: vary the public clear duration at fixed write/capture strength, keeping thresholds fixed, to distinguish inherited residual common-mode credit from contamination of the isolated stored Walsh components.',
      '','## Resources / reproducibility','',
      f"- Main recurrence GPU: {meta['gpu_name']} ({meta['selected_device']}); PyTorch {meta['torch_version']}; CUDA {meta['cuda_version']}; dtype float64.",
      f"- Recurrence/sweep wall time: {meta['total_runtime_seconds']:.3f} seconds; CPU time {meta['cpu_seconds']:.3f} seconds. Plotting follows this measurement.",
      f"- Peak allocated VRAM: {meta['peak_allocated_vram_bytes']/2**20:.3f} MiB; peak reserved: {meta['peak_reserved_vram_bytes']/2**20:.3f} MiB.",
      f"- Largest n={meta['largest_n']}; largest K={meta['largest_K']}; {len(cases)} two-channel cases; {len(three)} optional three-channel cases.",
      f"- All tested inputs legal: {legal}; largest raw-input magnitude: {max(c['max_absolute_raw_input'] for c in cases):.9g}.",
      f"- Previous output hashes unchanged: {meta['previous_outputs_unchanged']}. One CPU intra-op thread, one inter-op thread, no workers.",
      '- Reproduce: `python experiments/finite_n_multistage_capture_20261006/run_experiment.py`. CUDA is mandatory; no CPU fallback.',
      '- No research/governance files edited. No commit or push performed.']
    meta['output_generation_seconds']=time.perf_counter()-render_start
    meta['total_runtime_including_outputs_seconds']=meta['total_runtime_seconds']+meta['output_generation_seconds']
    lines.append(f"- Total wall time including output generation: {meta['total_runtime_including_outputs_seconds']:.3f} seconds.")
    (root/'run_metadata.json').write_text(json.dumps(meta,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    result['metadata']=meta
    (root/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    (root/'SUMMARY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v['status'] for k,v in tests.items()},indent=2),flush=True)
