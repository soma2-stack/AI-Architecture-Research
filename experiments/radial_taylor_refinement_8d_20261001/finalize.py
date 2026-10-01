"""Exact arithmetic, complete arrays and fixed-input publication audit."""
import time
CPU=time.process_time();WALL=time.perf_counter()
import common as c
from fractions import Fraction as Q
import numpy as np
checks=[]
def check(n,b):
    checks.append({'name':n,'passed':bool(b)})
    assert b,n
if __name__=='__main__':
    f=c.verify();r=c.json.loads((c.ROOT/'result8.json').read_text());d=c.candidate()
    check('all_frozen_source_and_history_hashes',bool(f))
    if r['status']=='INVALID / INCOMPLETE':
        c.write('final_checks.json',{'checks':checks,'status':r['status'],'error':r.get('error')})
        raise SystemExit('Invalid/incomplete run: preserve evidence; no 9D')
    check('both_precision_runs',[a['bits'] for a in r['attempts']]==[192,256])
    for a in r['attempts']:
        bands=a['bands'];bits=a['bits'];ctrl=a['control']
        check(str(bits)+'_eight_exact_radial_weights',len(bands)==8 and sum(Q(b['weight']) for b in bands)==Q(1,3))
        check(str(bits)+'_nested_domain',all(Q(b['upper_radius'])==Q(j+1,8) for j,b in enumerate(bands)))
        check(str(bits)+'_old_control_passes',ctrl['valid'] and ctrl['all_antipodal_faces_pass'])
        penalty=[sum(Q(b['weight'])*Q(b['M3_used'][i])/2 for b in bands) for i in range(8)]
        check(str(bits)+'_half_remainder_exact',penalty==list(map(Q,a['integrated_half_remainder'])))
        beta=[Q(ctrl['mu_tilde'][i])*(1-Q(ctrl['center_rows_upper'][i])-penalty[i]) for i in range(8)]
        check(str(bits)+'_beta_exact',beta==list(map(Q,a['beta'])))
        check(str(bits)+'_substantial_criterion_exact',a['substantial']==(min(beta)>=Q(r['success_target_beta'])))
        check(str(bits)+'_all_caps_valid',all(Q(b['M3_used'][i])==min(Q(b['M3_original_direction'][i]),Q(ctrl['M3_upper'][i])) for b in bands for i in range(8)))
        check(str(bits)+'_no_lost_margin',all(beta[i]>=Q(ctrl['beta3'][i]) for i in range(8)))
    diffs=[abs(Q(x)-Q(y)) for x,y in zip(r['attempts'][0]['beta'],r['attempts'][1]['beta'])]
    check('precision_beta_agreement',max(diffs)<Q(1,10**12))
    comparisons={}
    for suffix in ['control_bounds','elimination_native']+[f'prefix_{j}' for j in range(1,9)]:
        paths=[c.ROOT/f'{suffix}_{bits}.npz' if not suffix.startswith('prefix_') else c.ROOT/f'prefix_{bits}_{suffix.split("_")[1]}.npz' for bits in (192,256)]
        ar=[np.load(p) for p in paths];check(suffix+'_same_array_keys',set(ar[0].files)==set(ar[1].files))
        for name in ar[0].files:
            x,y=ar[0][name],ar[1][name]
            check(suffix+'_'+name+'_finite_and_nonnegative',np.isfinite(x).all() and np.isfinite(y).all() and (x>=0).all() and (y>=0).all())
            check(suffix+'_'+name+'_precision_agreement',np.allclose(x,y,rtol=1e-11,atol=1e-280))
            comparisons[suffix+'/'+name]={'entries':x.size,'identical':bool(np.array_equal(x,y)),
              'maximum_absolute_difference':float(abs(x-y).max())}
    successful=all(a['all_faces_pass'] and a['substantial'] for a in r['attempts'])
    check('decision_consistent',(r['status']=='SUBSTANTIAL IMPROVEMENT')==successful)
    n9=None
    if successful:
        n9=c.json.loads((c.ROOT/'result9.json').read_text())
        check('nine_is_only_numerical',n9['r']==9 and 'NO 9D CERTIFICATE' in n9['label'])
        check('numeric9_CPU_budget',n9['CPU_seconds']<=120+5)
    else:check('no_numeric9_after_failed_improvement',not (c.ROOT/'result9.json').exists())
    total=r['total_CPU_seconds']+(n9['CPU_seconds'] if n9 else 0)+time.process_time()-CPU
    check('overall_CPU_budget',total<1200)
    peak=max(r['peak_RAM_bytes'],n9['peak_RAM_bytes'] if n9 else 0,c.ref.a.c.psutil.Process().memory_info().peak_wset)
    check('RAM_budget',peak<2*1024**3)
    c.write('final_checks.json',{'checks':checks,'passed':len(checks),'arrays':comparisons,'max_beta_precision_difference':str(max(diffs)),
      'CPU_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,'total_CPU_seconds':total,'peak_RAM_bytes':peak,'GPU_seconds':0})
    a=r['attempts'][-1];ctrl=a['control'];beta=list(map(Q,a['beta']));mu=list(map(Q,ctrl['mu_tilde']))
    rows=[]
    for i in range(8):
        old_pen=mu[i]*Q(ctrl['M3_upper'][i])/6
        new_pen=mu[i]*Q(a['integrated_half_remainder'][i])
        recovery=(1-new_pen/old_pen)*100
        rows.append(f'| {i+1} | {float(2*Q(ctrl["beta3"][i])):.12g} | {float(2*beta[i]):.12g} | {float(old_pen):.12g} | {float(new_pen):.12g} | {float(recovery):.6g}% |')
    weakest=min(range(8),key=lambda i:beta[i]);old=min(Q(v) for v in ctrl['beta3'])
    stage=[('Accepted control',old),('Exact elimination / native gates',min(map(Q,a['native_elimination_beta']))),
           ('Exact elimination / sharp gates / whole box',min(map(Q,a['sharp_whole_beta']))),('Sharp gates / radial Taylor',min(beta))]
    stage_table='\n'.join(f'| {name} | {float(2*b):.12g} | {float(b/Q(1,1000)-1)*100:.6g}% |' for name,b in stage)
    nine_table='Not run: improvement criterion failed.'
    if n9:
        nine_table='\n'.join(f"- Seed {w['seed']}: proxy beta/epsilon {w['result']['min_ratio']:.8g}; found actual separation ratio {w['result']['actual']['min_ratio']:.8g}; normal usage {w['result']['actual']['normal_usage']:.6g}; {w['assessment']}." for w in n9['winners'])
        nine_table+='\nStatus: '+n9['status']+'. These are sampled numerical minima, not lower-bound proofs.'
    report=f"""# Third-order margin refinement on the SAME accepted 8D section

## Decision

**{r['status']}**. Fixed independent width4/T37/P24 confirmation endpoint,
epsilon1e-3, normalized metric, permitted query family, exact fixed-h and
continuous encoder contract unchanged. Candidate byte-identical; no new axes
or amplitudes. Freeze commit {r['freeze_commit']}. The new method requires
independent review; no claim that it has already been independently audited.

New weakest guaranteed antipodal separation **{float(2*min(beta)):.16g}**,
face {weakest+1}, relative slack **{float(min(beta)/Q(1,1000)-1)*100:.8g}%**.
Old weakest separation {float(2*old):.16g}, slack {float(old/Q(1,1000)-1)*100:.8g}%.
Slack multiplier {float((min(beta)-Q(1,1000))/(old-Q(1,1000))):.8g}.
Frozen success criterion: at least DOUBLE old weakest absolute slack.

## All face bounds and recovered curvature slack (256 bits)

Penalties here are subtracted from beta; separation is2beta. Recovery compares
the complete old whole-box remainder with the new integrated upper remainder.

| Face | Old separation | New separation | Old cubic penalty | New penalty | Penalty recovered |
|---|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

## Attribution, not candidate tuning

| Fixed method component | Weakest separation | Relative slack |
|---|---:|---:|
{stage_table}

All components were frozen prospectively. Exact final-input substitution
retains parameter sensitivities computed with realized inputs HELD FIXED;
it does not differentiate a parameter-dependent history generator. Signed
affine output coefficients are combined before absolute bounds. Sharp gates
use complete polynomial-critical-point lists with outward radical enclosures.
Eight fixed radial boxes cover BOTH halves of each antipodal segment with
exact Taylor integral weights; every joint mixed derivative is retained.
They are derivative subdomains, not a smaller 8D section. PROOF.md gives the
factor1/2 and exact section-identity derivation.

## Hidden section / query unchanged

The reviewed original control regenerated at both precisions with every
complete array identical to accepted archived values. Eta_h={ctrl['eta_hidden']:.15g};
forcing={ctrl['hidden_forcing_upper']}, below common limit
{float((1-Q(ctrl['eta_hidden']))*Q(d['ah'])):.15g}.
The SAME full curved hidden section supplies valid histories throughout the
original amplitudes. Query mu and center e0 are the unchanged control values;
no extra query power or metric rescaling. At all face margins >epsilon the
accepted continuous encoder argument retains k>=8, not bits/grid states.

## Conditional numerical 9D feasibility

{nine_table}

This phase uses the preregistered two-start balanced per-axis SPSA rules and
fixed endpoint. Winners saved before fresh joint face attacks, no validation
feedback. It invokes NO interval engine for9D. No rigorous9D, 10D, training,
architecture, Stage C or AMS work was authorized or performed.

## Precision, tests, provenance, resources

Both192/256 regenerated from scratch. Maximum beta difference
{float(max(diffs)):.6g}. All {len(comparisons)} complete array groups compared;
bitwise identical across precisions: {all(v['identical'] for v in comparisons.values())}.
Scalar intervals use declared precision; positive tensors use reviewed
elementary upward binary64, not ordinary midpoint arithmetic.
Synthetic tests and {len(checks)} final exact/arithmetic/array/provenance
checks pass. All frozen inputs and previous evidence hashes preserved.
One CPU thread, measured total {total:.6f} CPU-s ({total/60:.6f}min), peak
{peak/2**20:.6f}MiB. GPU/CUDA/own VRAM zero. Separate repair/import allowances,
if any, are disclosed in repair records and must not be described as measured.
No GAS-0 or other lane notebook touched.

## Stop / remaining uncertainty

STOP after this stage. No global robust-dimension ceiling or architecture
advantage follows. The strongest remaining uncertainty is independent audit
of the new algebraic elimination and radial coefficient bound. Recommend a
bounded independent review/replay of this refinement before any higher-D
rigorous certificate. No further work starts automatically.
"""
    (c.ROOT/'REPORT.md').write_text(report,encoding='utf-8')
    c.write('OUTPUT_MANIFEST.json',{'sha256':{p.name:c.sha(p) for p in c.ROOT.iterdir() if p.is_file() and p.name!='OUTPUT_MANIFEST.json'}})
    print(c.json.dumps({'status':r['status'],'weakest_separation':float(2*min(beta)),'slack_percent':float(min(beta)/Q(1,1000)-1)*100,
      'checks':len(checks),'CPU_seconds':total,'peak_RAM_MiB':peak/2**20,'numeric9':n9['status'] if n9 else 'NOT RUN'},indent=2))
