"""Summary/provenance checks only; does not optimize or certify anything."""
from pathlib import Path
import hashlib,json,math
from fractions import Fraction as F
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    f=json.loads((HERE/'METHOD_FROZEN.json').read_text(encoding='utf-8'))
    g=json.loads((HERE/'SECONDARY_FROZEN.json').read_text(encoding='utf-8'))
    checks=[]
    def check(name,ok):
        checks.append({'name':name,'passed':bool(ok)})
        if not ok:raise RuntimeError(name)
    check('primary_methods_unchanged',all(sha(HERE/k)==v for k,v in f['method_hashes'].items()))
    check('historical_7D_evidence_unchanged',all(sha(ROOT/k)==v for k,v in f['original_preservation'].items()))
    check('secondary_methods_unchanged',all(sha(HERE/k)==v for k,v in g['source_hashes'].items()))
    check('all_111_primary_records_unchanged',all(sha(HERE/k)==v for k,v in g['primary_output_hashes'].items()))
    p=json.loads((HERE/'results.json').read_text(encoding='utf-8'));r=json.loads((HERE/'refinement_results.json').read_text(encoding='utf-8'))
    d=json.loads((HERE/'diagnostics.json').read_text(encoding='utf-8'));sanity=json.loads((HERE/'sanity.json').read_text(encoding='utf-8'))
    check('requested_dimensions_complete',all(n in [v['dimension'] for v in p['dimensions']] for n in (8,10,12,16,20,24)))
    check('one_primary_binary_refinement_only',set(v['dimension'] for v in p['dimensions'])=={8,10,11,12,16,20,24})
    check('no_rigorous_engine_imports',all('from arithmetic' not in (HERE/s).read_text() and 'import kernel' not in (HERE/s).read_text() for s in ('numerics.py','run.py','refine.py','diagnostics.py')))
    check('high_precision_selected_pairs_agree',max(v['float64_hp_abs_difference'] for v in d['rows'])<1e-10)
    check('all_selected_section_samples_valid',all(v['hidden_usage']<=1+1e-10 for v in d['rows']))
    npz=np.load(HERE/'bases.npz');overlap=abs(npz['query_svd'][:,4:].T@npz['extend7'][:,4:])
    diag=float(np.diag(overlap).min());off=overlap-np.diag(np.diag(overlap));offmax=float(off.max())
    cpu=p['resources']['cpu_seconds']+r['resources']['cpu_seconds']+d['resources']['cpu_seconds']+sanity['cpu_seconds']
    wall=p['resources']['wall_seconds']+r['resources']['wall_seconds']+d['resources']['wall_seconds']+sanity['wall_seconds']
    peak=max(v['resources']['peak_ram_bytes'] for v in (p,r,d))
    check('cheap_resource_budget',cpu+15<900)
    promising=[v['dimension'] for v in d['rows'] if v['minimum_found_ratio']>=1.05]
    highest=max(promising);failed=[v['dimension'] for v in d['rows'] if v['dimension']>highest and v['minimum_found_ratio']<1];lowest=min(failed)
    lines=[]
    for v in d['rows']:
        status='promising' if v['minimum_found_ratio']>=1.05 else 'below threshold'
        normal=v['hidden_usage']*v['ah']
        lines.append(f"| {v['dimension']} | {v['minimum_found_separation']:.10g} | {v['minimum_found_ratio']:.6g} | {normal:.5g} / {v['ah']:.5g} ({100*v['hidden_usage']:.3g}%) | {max(v['sampled_third_penalty']):.5g} | {status} |")
    table='\n'.join(lines)
    proxyrows=[]
    for case in sorted(p['dimensions'],key=lambda z:z['dimension']):
        cand=max([x for x in case['cases'] if x['style']=='proxy'],key=lambda z:z['third_order_proxy'].get('min_proxy_ratio',-1e99))
        pr=cand['third_order_proxy'];i=int(np.argmin(pr['beta']))
        proxyrows.append({'dimension':case['dimension'],'basis':cand['basis'],'ratio':pr['min_proxy_ratio'],
                          'weakest_face':i+1,'mu':pr['mu'][i],'penalty':pr['penalties'][i],'M3':pr['M3'][i],
                          'actual_ratio_same_section':cand['minimum_found_ratio']})
    pt='\n'.join(f"| {v['dimension']} | {v['ratio']:.6g} | {v['mu']:.6g} | {v['penalty']:.6g} | {v['actual_ratio_same_section']:.6g} |" for v in proxyrows)
    counts={'primary_amplitude_runs':len(list(HERE.glob('optimization_*.json'))),
            'primary_proxy_evaluations':sum(json.loads(v.read_text())['calls'] for v in HERE.glob('optimization_*.json')),
            'secondary_amplitude_runs':len(list(HERE.glob('refine_optimization_*.json'))),
            'secondary_objective_evaluations':sum(json.loads(v.read_text())['calls'] for v in HERE.glob('refine_optimization_*.json'))}
    summary={'label':'NUMERICAL FEASIBILITY ONLY; NO NEW DIMENSION PROVED','highest_promising_dimension':highest,
        'lowest_failing_screened_dimension':lowest,'approximate_transition':[highest,lowest],
        'global_upper_bound':False,'rows':d['rows'],'proxy_rows':proxyrows,'checks':checks,'counts':counts,
        'basis_overlap':{'minimum_absolute_diagonal':diag,'maximum_absolute_off_diagonal':offmax,
                         'limitation':'These two bases are effectively sign-equivalent; not independent geometric alternatives'},
        'resources':{'measured_cpu_seconds':cpu,'measured_cpu_minutes':cpu/60,'summed_compute_wall_seconds':wall,
                    'peak_ram_bytes':peak,'setup_import_git_cpu_allowance_seconds':15,'gpu_seconds':0,'own_VRAM_bytes':0,'workers':1}}
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    report=f'''# Cheap numerical feasibility screen: fixed independent width 4

## Result

Highest promising screened joint dimension: **{highest}D**.
Lowest clearly failing tested joint dimension: **{lowest}D**.
The approximate transition is **{highest}–{lowest}D for these screened Cartesian sections**.
This is NOT a true robust-dimension ceiling or an upper bound for the model.
The previous rigorously certified7D result remains unchanged. No higher
dimension was proved and no rigorous certificate was attempted.

Same central endpoint/history/parameters, n=4, T=37, P=24, epsilon=1e-3,
original parameter-RMS/input-SD gradient units, permitted scalar-head queries.
All sampled selected sections enforce the same final hidden state; residuals
are near floating-point rounding. Full fixed-h sensitivity dimension remains24.

## Main table

These are found actual minima, hence UPPER numerical estimates of the unknown
all-face infima. Positive sampled minima do not prove uniform separation.
The cubic column is a sampled worst penalty mu_i*|Phi_i^(3)|/6, over joint
directions/path points; it is NOT a uniform third-order bound. Units are the
same normalized gradient units as epsilon. Normal usage gives actual sampled
compensation relative to that candidate's declared normal allowance.

| Joint dimension | Weakest actual separation found | Ratio to 2epsilon | Normal used / allowance | Max sampled cubic penalty | Numerical assessment |
|---|---:|---:|---:|---:|---|
{table}

11D is the one primary binary refinement. The table includes its separate
direct-amplitude improvement and the analogous secondary12D improvement;
all primary values remain preserved in results.json and dimension_*.json.

## Fixed-h construction and physical domain

Higher-D screening uses last-input normal coordinates, enabling explicit
x_T=W^-1(atanh(h0)-R h_(T-1)-b). This is a different local section chart at
the SAME endpoint, not a new recurrence or a new physical error metric.
Realized input histories are held fixed for parameter sensitivities; the
input compensator is never differentiated with respect to theta. Section
derivatives with respect to tangent variables include compensation correctly.
Numerical checks compare them with finite differences (maxerror
{sanity['fixed_h_jacobian_finite_difference_max_abs_error']:.5g}).

All amplitude optimizations obey raw-history chart radius<=1, a_i<=4,
a_h<=1. Primary direct sections used radius cap0.65/normal allowance1;
secondary uses allowance0.125 and radius<=0.95, inside those SAME domain rules.
These cap choices influence the approximate transition; no global range claim.

## Query metric

Disjoint independent support makes the permitted-query supremum
D_C=sech^2(1/4)*||diag(R_owner)Delta_s||_2/(sqrt(4)*max(1,||R||_F)).
Here Delta_s is the vector of all 24 normalized supported sensitivity
coordinates. R_owner repeats each diagonal recurrent weight on its six
parameter-sensitivity coordinates; it is not a new normalization.
The same accepted future gate family realizes/approaches this maximum.
The third-order dual proxy retains the conservative7/8 gate. Fixed h cancels
the future direct-parameter injection. Full supported sensitivities are used,
not selected projections alone; arbitrary residual coordinates are retained.

## Reviewed third-order method plausibility

Ordinary float64 positive majorants, all mixed terms, implicit derivatives,
and both affine tightenings were used ONLY as numerical proxies. Aggregate
third contractions avoid a large third tensor. The known7D calibration differs
from accepted beta values by at most{sanity['7d_calibration_max_abs_beta_difference']:.5g}.
No interval arithmetic was invoked in the screen.

For the BEST small proxy-oriented section at each dimension, the table below
reports the weakest proxy face. These are DIFFERENT candidates from the larger
direct-geometry winners in the main table. Proxy penalty is mu*M3/6, with
whole-box NUMERICAL majorants; it is not a rigorous lower certificate.

| Dimension | Proxy beta/epsilon | Linear mu at weak face | Cubic penalty at weak face | Actual sampled ratio on SAME proxy section |
|---|---:|---:|---:|---:|
{pt}

**8D is plausible for the existing certificate method**, but its best proxy
margin is only~2.45%; prospective exact rounding/bounds would still need proof.
**10D is geometrically promising but the reviewed global bound does not pass**.
Its large direct section fails the majorant hidden guards before a full M3
bound is formed. This must not be misreported as a nonexistent section.
For11D and12D the selected secondary sections also fail global majorant guards,
yet actual fixed-h solves remain valid. Their decisive negative evidence is
an ACTUAL below-threshold antipodal pair, not proxy failure alone.

| Dimension | Strongest observed bottleneck | Plausibility of certification |
|---|---|---|
| 8D | Small proxy margin after the third-order penalty | Plausible; numerical proxy has only 2.45% slack |
| 10D | Global hidden/curvature majorants on the larger section | Actual geometry promising; present proxy does not pass |
| 11D | Face 1 loses separation under joint amplitude competition | Selected boxes fail; no impossibility statement |
| 12D | Face 1 loses separation despite a stronger new direction | Selected boxes fail |
| 16D | Weak tail, face 16 | Not promising in screened sections |
| 20D | Much weaker tail, face 20 | Not promising in screened sections |
| 24D | Very weak tail, face 22 | Not promising in screened sections |

## Bottlenecks and refinement provenance

At11D the added eleventh face itself passes strongly; face1 fails from joint
nonlinear interference/amplitude competition. After rebalancing, its ratio is
~0.874865; the eleventh face ratio is~2.943. At12D face1 remains the limiter,
~0.689274; the new twelfth face is~1.329. Thus the failure cannot be described
as simple disappearance of the newest direction.

At16D,20D,24D the weak tail becomes the limiter (faces16,20,22 respectively).
Query-weighted tangent condition numbers rise from~34 at8D to~2.45million at24D.
Fixed-h numerical formation succeeds throughout; it is the query separation
and joint nonlinear geometry that fail in the tested products.

Primary method frozen/pushedbc7bc61 before scores. All6 requested dimensions
ran, then one11D binary refinement. The first bracket was10D/11D; its11D
failure was on an old strong axis. Secondary direct-amplitude rules were
explicitly frozen AFTER those observations in4c10ea5, BEFORE secondary scores.
This is disclosed as an adaptive diagnostic, not retrospective preregistration.
All111 primary records are unchanged. It remains cheap numerical research.

Secondary winners were hashed/saved before validation. Search-pool ratios
11D~2.738 and12D~1.209 collapsed under independent fresh face attacks to
~0.875 and~0.689. This is concrete optimization-pool overfitting; no validation
counterexample was fed back into search. As12D failed, further14/15 refinement
was not run. All failed proposals are preserved.

## Checks and limits

Selected worst pairs were independently recomputed at60/90 decimal digits,
using original rational model/history and binary-frozen numerical axes/amplitudes.
Maximum float/high-precision separation difference is
{max(x['float64_hp_abs_difference'] for x in d['rows']):.5g}. This is numerical
validation, NOT an interval proof. Sampled third derivatives include terminal
compensation and actual parameter injections; diagnostics.json stores every
axis penalty, spectrum and high-precision pair.

Basis overlap: minimum absolute diagonal{diag:.12g}, maximum off-diagonal
{offmax:.5g}. The two proposed bases are effectively sign-equivalent.
Their agreement is weak evidence; this did NOT broadly test unrelated bases.
Other bases, ellipsoids or non-Cartesian sections could improve11D or more.
No useful global robust-dimension upper bound has been established.

The strongest remaining uncertainty is whether a different joint geometry
avoids the strong first-axis collapse. This screen locates an approximate
failure region for its charts, not the model's intrinsic maximum dimension.

## Resources and files

{counts['primary_amplitude_runs']} primary amplitude runs /
{counts['primary_proxy_evaluations']} numerical proxy evaluations;
{counts['secondary_amplitude_runs']} secondary runs /
{counts['secondary_objective_evaluations']} numerical objective evaluations.
One CPU worker/thread; measuredCPU{cpu/60:.6f}minutes, summed computation
wall{wall:.6f}s, peakRAM{peak/2**20:.5f}MiB. Setup/import/Git allowance15CPU-s
separately. The900CPU-s cap was respected. GPU/CUDA/ownVRAM0. No model server,
GAS-0, training, width5, Stage C, AMS or architecture work.

Sanity, frozen-source, original-evidence, primary-record, query-pair precision,
section-usage and resource checks pass. New source/results live only in this
directory; shared map and Codex resume are updated append-only. No old negative
results or7D artifacts were overwritten. OUTPUT_MANIFEST.json records hashes.
A report-string syntax error prevented the first summary export; it was fixed
without running or changing any scientific computation. The failed export
and repair are recorded in summary_export_failure.json.

## Stop

Stop here. No certification is authorized by this task. Current method's
strongest practical certificate prospect is8D;10D needs tighter geometric
control before a serious certificate attempt. A new owner task must select
the next step. No11D impossibility, architecture superiority or discovery claim.
'''
    # Improve readable spacing without touching frozen scientific evidence.
    for a,b in {'certified7D':'certified 7D','dimension24':'dimension 24','known7D':'known 7D',
                'at11D':'at 11D','At11D':'At 11D','At12D':'At 12D','At16D':'At 16D',
                'face1':'face 1','faces16':'faces 16','from~34':'from ~34','at8D':'at 8D','at24D':'at 24D',
                'pushedbc7bc61':'pushed bc7bc61','in4c10ea5':'in 4c10ea5','All6':'All 6',
                'one11D':'one 11D','All111':'All 111','at60/90':'at 60/90','measuredCPU':'measured CPU ',
                'wall{':'wall {','peakRAM':'peak RAM ','allowance15CPU-s':'allowance 15 CPU-s',
                'The900CPU-s':'The 900 CPU-s','results or7D':'results or 7D','prospect is8D':'prospect is 8D',
                ';10D':'; 10D','No11D':'No 11D', 'remains24':'remains 24',
                'secondary12D':'secondary 12D', 'maxerror':'max error',
                'cap0.65':'cap 0.65', 'allowance1':'allowance 1', 'allowance0.125':'allowance 0.125',
                'conservative7/8':'conservative 7/8', 'at most3.':'at most 3.',
                'only~':'only ~', 'For11D and12D':'For 11D and 12D',
                'was10D/11D; its11D':'was 10D/11D; its 11D', 'As12D':'As 12D',
                'further14/15':'further 14/15', 'diagonal1':'diagonal 1',
                'improve11D':'improve 11D', '2.431510minutes':'2.431510 minutes',
                'wall147':'wall 147', '104.30469MiB':'104.30469 MiB',
                'GPU/CUDA/ownVRAM0':'GPU/CUDA/own VRAM 0', 'width5':'width 5',
                'to~2.45million':'to ~2.45 million', 'at16D':'at 16D'}.items():report=report.replace(a,b)
    (HERE/'REPORT.md').write_text(report,encoding='utf-8')
    manifest={p.name:sha(p) for p in HERE.iterdir() if p.is_file() and p.name!='OUTPUT_MANIFEST.json'}
    (HERE/'OUTPUT_MANIFEST.json').write_text(json.dumps({'sha256':manifest},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'highest_promising':highest,'lowest_screened_failure':lowest,'resources':summary['resources'],
                      'checks':len(checks),'basis_overlap':summary['basis_overlap']},indent=2))
if __name__=='__main__':main()
