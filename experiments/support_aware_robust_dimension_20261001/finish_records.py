"""One-time report/state update; no experiment or old artifact mutation."""
from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).parent;REPO=ROOT.parents[1]
def main():
 assert not (ROOT/'RECORDS_FINISHED.json').exists()
 s=json.loads((ROOT/'summary.json').read_text());rs=json.loads((ROOT/'resource_summary.json').read_text());rows=json.loads((ROOT/'results.json').read_text())
 assert json.loads((ROOT/'final_tests.json').read_text())['passed']
 old=json.loads((ROOT/'preservation_manifest.json').read_text())
 for name,h in old.items():assert hashlib.sha256((REPO/name).read_bytes()).hexdigest()==h,name
 tables='\n'.join(f"| {x['case']} | {x['accepted_continuous_lower']} -> {x['continuous_lower']} | {x['selected_section_states_lower']} / {__import__('math').log2(x['selected_section_states_lower']):.3f} | {x['best_known_states_lower']} / {x['best_known_bits_lower']:.3f} | {x['m']:.6g} | {x['M']:.6g} |" for x in s['records'])
 slices='\n'.join(f"| {x['case']} | {' / '.join(str(v['epsilon_essential_dimension']) for v in x['accepted_subproducts'])} | {x['certificate']['eta_hidden']:.6g} | {x['certificate']['eta_sensitivity']:.6g} |" for x in rows)
 slopes='\n'.join(f"| {x['case']} | {' / '.join(map(str,x['scale_diagnostic']['states']))} | {' / '.join(f'{v:.3f}' for v in x['scale_diagnostic']['adjacent_loglog_slopes'])} |" for x in s['records'])
 report=f'''# Support-aware robust dimension certification

## Classification and architecture gate

**{s['classification']}**

**{s['architecture_gate']}.** Maximum achieved epsilon-essential continuous
lower certificate is four. No useful ambient upper bound or uniform compression
structure is established; no architecture design follows.

## Contract, endpoints and provenance

Primary epsilon exactly **1e-3**, unchanged normalized gradient/query units:
input SD sqrt(3/32), frozen R/W/b RMS parameter scales, q=ones/sqrt(n),
beta=max(1,||R||F), future preactivation box [1/4,3/4]^n. Eight unchanged
dense/independent archived and confirmation histories, n3/T22 and n4/T37.
Parameters P_dense=21/36, P_independent=15/24 are explicitly different.
No history, model, architecture, width or error-contract search.

Preregis/code/chart freeze **f0c231e**, before official intervals. Already
preregistered numerical diagnostic implementation **1dbcdb6**. Source checkpoint
915d007, accepted support-aware result supplied by the owner as independently
audited. New dimension conversion is not a re-review of that result.

## What continuous robust dimension means

For a unique continuous curved lift of projection coordinates z in [-1,1]^r,
prove on the ENTIRE simultaneous section

    max_i b_i |z_i-z'_i| <= D_C(S(z),S(z')) <= M ||z-z'||_2,
    m=min_i(b_i)/sqrt(r) > 0, and every retained b_i > epsilon.

Thus every sufficiently separated pair is query-distinguishable. Opposite
points on the cube boundary have distance >2epsilon. Borsuk-Ulam then excludes
a continuous no-replay encoder in fewer than r real coordinates answering
every allowed query to epsilon. This finite-radius criterion is stronger than
positive midpoint rank, and is separate from discrete bits/states. The
anisotropic cube boundary avoids an unnecessary inscribed-ball sqrt(r) loss
in the antipodal test, while the displayed Euclidean m honestly retains it.
PROOF.md gives the full argument, inverse accounting and computational scope.

## Model-specific query geometry

Independent: exact full query distance is the weighted Euclidean norm of all
legally supported owner coordinates, with weights sech^2(1/4)R_ii/(sqrt(n)beta).
Certification uses the near-optimal permitted rational7/8-gate lower norm and
its reviewed dual margins. Every supported residual coordinate remains.

Dense: use the entire permitted gate-box vertex maximum numerically. The
strongest accepted certified finite-frame projection dual used here remains
valid for arbitrary full-tensor residuals. It is a lower certificate, not the
exact dense norm. No independent-only zero restriction is imposed on dense.
Both models keep the same future family and physical epsilon.

## Lower bounds: state packing versus continuous dimension

The selected-section packing uses the exact strict-collision entropy corollary
in SECTION_ENTROPY_COROLLARY.md. The frozen17/8 counts remain separately saved.
Best-known packing is max(selected, accepted), never a sum across sections.

| Endpoint | Accepted continuous r -> new r | Selected section states / bits | Best known states / bits | Euclidean m lower | Euclidean M upper |
| --- | ---: | ---: | ---: | ---: | ---: |
{tables}

Independent n4 confirmation now has a FOUR-dimensional continuous section,
with b_i approximately0.0061980,0.0025144,0.0015849,0.0015178. Its Euclidean
m>=0.00075890493 and M<=0.037920712. The original17/8 spacing gives72 states;
the strict spacing corollary gives84 on this new four-dimensional product.
The previously accepted84-state result lives on a DIFFERENT two-dimensional
product. Equal counts therefore do not determine dimension.

Dense n3 confirmation gives r3 even though its historical17/8 calculation
counts only4 states: the weakest b=0.00105208 is strictly above epsilon but
below17epsilon/16. Its eight cube corners are all rigorously separated.
This is a consequence of unchanged collision threshold2epsilon, not epsilon
tuning or alteration of old constants/results.

## Thin sections and failure reasons

1,152 scheduled interval proposals completed:417 valid geometry certificates;
604 rejected for mixed sensitivity curvature,119 for hidden Jacobian dominance,
12 for hidden-section inclusion. Many valid geometries have too little range
at epsilon. Every attempted prefix1..8, amplitude1/2..1/64, equal/spectral
profile and declared projector rule is preserved in trials_*.json. No failed
proposal is treated as a mathematical dimension ceiling.

The best achieved dimensions all use tangent amplitude1/8 and equal profiles;
seven use freshly certified fixed-center charts, while dense3 archived retains
its already accepted geometry. Equal normal half-widths justify the normal
infinity-norm self-map. Selected K/Kh preconditioners remain fixed during
256-bit regeneration of all seven new charts; complete mixed curvature,
product inclusion and dimensions pass. New selected projectors happened to
come from the accepted frame-Gram rule; the supported diagonal-Gram rule was
also tested with the same supported query metric.

For the ORIGINAL products only, shrink fractions1,3/4,1/2,1/4 give:

| Endpoint | Retained continuous r at shrink fractions | Selected eta_h | Selected eta |
| --- | --- | ---: | ---: |
{slices}

Simple shrinking sacrifices finite range. Re-certification across amplitudes
balances curvature versus usable range; arbitrarily tiny valid charts do not
qualify as robust dimensions at epsilon.

## Numerical scale diagnostics

Only selected certified sections were sampled:257 deterministic Sobol points
plus all retained corners, CPU Newton solves, full permitted query distances,
three farthest-point starts at spacings epsilon,2epsilon,4epsilon,8epsilon.
All sampled normal/tangent box checks pass; root residuals<2e-12. Sampled
pair ratios respect the rigorous m/M bounds. These are finite-sampling LOWER
packings, not maxima or upper dimension estimates.

| Endpoint | Counts at the four spacings | Adjacent log-log slopes |
| --- | --- | --- |
{slopes}

Slopes around epsilon are generally closer to1--2.4 than to four. This is
consistent with highly unequal ranges and sparse greedy sampling; it does
not establish an intrinsic ceiling. The section-specific entropy corollary
rigorously gives exponent r asymptotically as spacing tends to zero, with
explicit possibly poor constants. That asymptotic result is not a claim
that four power-law directions are numerically resolved near epsilon.

## Upper bounds and comparison

**NO USEFUL ROBUST-DIMENSION UPPER BOUND FOUND.** On a chosen r-subsection,
the whole-section bi-Lipschitz map fixes its intrinsic dimension to r and
supplies a section-specific entropy cover. It excludes all OTHER reachable
directions and is therefore not a global robust-dimension upper bound.
Structural ambient upper counts remain63/144 dense and15/24 independent.
No uniform low-rank tail/truncation estimate justifies a smaller ambient ceiling.

Independent exact support does not eliminate the observed robust credit state:
it admits moderate r4 at one fixed endpoint. Dense strongest achieved r3.
These are unequal lower certificates, not true maxima or capability/superiority
comparisons. Exact full dimension remains much larger than certified robust r.

## Rigor, tests, repairs and limits

Rigorous: accepted query identities/duals, new whole-box mixed-curvature and
contraction bounds, global section m/M, epsilon-essential coordinate lower
bounds, and strict integer packing/section entropy arithmetic under the accepted
outward arithmetic model. Numerical: fixed-center SVD initializes rational
bases; all actual basis errors enter interval checks. Sampled root solutions,
packing counts and slopes are numerical diagnostics. No slope is promoted to proof.
The NEW continuous-section proof and certificates merit independent review.

Eight development tests and19 final/accepted-machinery tests pass:27 checks.
The first development invocation failed two implementation tests: BLAS limits
were set after a NumPy import, and a test incorrectly demanded an interval
endpoint equal1 instead of enclosure. Fixed BEFORE official measurements;
failed JSON and measured resource charges preserved in DEVELOPMENT_REPAIRS.md.
Official measurements had no invalidity, source mutation or budget failure.
All{len(old)}preserved source artifacts match their hashes, including AGENTS.

Strongest remaining uncertainty: whether directions beyond these lower bounds
are genuinely too weak at epsilon or merely lost to conservative curvature
and projection certificates. No finite-width global maximum, production
epsilon, memory-byte bound, learning advantage or architecture claim follows.

## Resources, artifacts and stop

Measured CPU **{rs['measured_cpu_seconds']:.6f}s / {rs['measured_cpu_seconds']/60:.6f}min**,
including failed tests;30 administrative seconds estimated separately. Summed
post-import measured job wall{rs['measured_wall_sum_seconds']:.6f}s.
Peak process RAM{rs['peak_RAM_bytes']/2**20:.6f}MiB. One CPU/BLAS worker.
**GPU/CUDA workload0; own VRAM0; GPU temperature not applicable/unmeasured.**
Small interval matrices and CPU numerical batches made GPU unnecessary.
No GAS-0/model-server operation, parameter training, new histories, width5,
architecture invention, Stage C or AMS work occurred.

Isolated directory experiments/support_aware_robust_dimension_20261001 contains
the frozen protocol/config, chart constants, source hashes, proof, all trials,
192/256 mixed bounds, selected results, numerical sets/distances, resources
and failures. Codex research/resume, shared research map and CPU ledger updated
after final validation only. Other lane notebooks and old experiment files unchanged.

**Single next step:** independently review the new four-dimensional continuous
section proof and its lower/upper interval bounds before another research stage.
Stop here; no architecture design follows automatically.
'''
 (ROOT/'REPORT.md').write_text(report,encoding='utf-8')
 (ROOT/'README.md').write_text('# Support-aware robust continuous dimension\n\nSee REPORT.md, PROOF.md, PREREGISTRATION.md, summary.json and SECTION_ENTROPY_COROLLARY.md.\n\nCPU-only fixed-endpoint certification; no new witness, architecture or training. Stop after this stage.\n')
 notebook=REPO/'Codex_Research.md';text=notebook.read_text(encoding='utf-8');assert '## AR-166' not in text
 resume=f'''### Support-aware robust dimension resume (2026-10-01)

- **Stage/classification:** MODERATE ROBUST CONTINUOUS DIMENSION CERTIFIED. Primary epsilon1e-3 unchanged; eight fixed dense/independent n3/T22 and n4/T37 endpoints only. MORE ROBUST-DIMENSION WORK NEEDED.
- **Continuous result:** residual-safe whole-section bi-Lipschitz bounds and cube-boundary Borsuk-Ulam give epsilon-essential real-coordinate lower bounds: independent archived/confirmation n3=3/3,n4=2/4; dense n3=2/3,n4=1/3. This is NOT inferred from finite grid counts or midpoint rank.
- **Strongest certificate:** independent n4 confirmation r4, b_min0.00151780986>epsilon, Euclidean m>=0.00075890493,M<=0.037920712; full mixed/hidden/product bounds verify256bits with frozen rational inverses. The accepted prior84-state product has r2; a new r4 product separately gives84 strict-separated states. New proof needs independent review, not old support-aware re-audit.
- **Scope/failures:**1152 systematic interval proposals,417 valid; extra prefixes fail mostly mixed curvature or have b<=epsilon. These failures are NOT ambient ceilings. Numerical packing slopes near epsilon~1--2.4, not dimension proofs. No useful global upper bound/compression. Structural D63/144 dense,15/24 independent remains a loose ceiling; no superiority claim.
- **Checks/resources:**27 passed checks;192/256 regenerated selected certificates;{len(old)} prior hashes intact. Two pre-official test bugs preserved and charged; official execution valid. MeasuredCPU{rs['measured_cpu_seconds']/60:.6f}min plus30s admin estimate, peak{rs['peak_RAM_bytes']/2**20:.3f}MiB, GPU/CUDA0/ownVRAM0, one worker. Freezef0c231e; diagnostic implementation1dbcdb6. GAS-0/AGENTS/other notebooks untouched. AR-166.
- **Exact next action:**STOP. Independent review of new r4 continuous section/mixed interval m/M/epsilon-essential proof. No new witness, width5, architecture, training, Stage C or AMS.

'''
 text=text.replace('## Guardrails and current state\n','## Guardrails and current state\n\n'+resume,1)
 text=text.rstrip()+'\n\n## AR-166 — Support-aware robust continuous dimension\n\n'+report
 notebook.write_text(text,encoding='utf-8')
 shared=REPO/'SHARED_RESEARCH_MAP.md';text=shared.read_text(encoding='utf-8')
 oldtitle='## Latest mathematical audit — Robust-certificate tightness (2026-10-01)'
 new=f'''## Latest mathematical audit — Support-aware robust dimension (2026-10-01)

**MODERATE ROBUST CONTINUOUS DIMENSION CERTIFIED. MORE ROBUST-DIMENSION WORK NEEDED.**
Owner reports independent audit acceptance of the old support-aware84-state bound.
New whole-section finite-radius certificate, same epsilon1e-3/frozen histories:
independent n3 archived/confirmation r3/3,n4 r2/4; dense n3 r2/3,n4 r1/3.
The r4 independent confirmation section has b_min0.00151781>epsilon, m>=0.000758905,
M<=0.0379207, with256-bit mixed-bound replay. Its strict product has84states;
the previously accepted84-state geometry had onlyr2. Cube antipodes/Borsuk-Ulam
give continuous real-coordinate lower bounds; finite count alone never supplies r.
1152 trials/417 valid,27 checks; all{len(old)} old source hashes preserved.
No useful ambient upper bound or compression; numerical packing slopes~1--2.4
around epsilon do not prove a ceiling. CPU{rs['measured_cpu_seconds']/60:.6f}min plus30s estimate,
peak{rs['peak_RAM_bytes']/2**20:.3f}MiB; GPU/CUDA0, GAS-0/AGENTS untouched.
Freezef0c231e; AR-166 and experiments/support_aware_robust_dimension_20261001/REPORT.md.
**STOP** for independent review of the NEW dimension proof/certificate, not a
repeat review of old results. No architecture, Stage C, AMS or width5.

'''
 assert oldtitle in text;text=text.replace(oldtitle,new+oldtitle.replace('Latest','Previous'),1);shared.write_text(text,encoding='utf-8')
 ledgerfile=REPO/'experiments/automated_mechanism_search/runs/cpu_ledger.json';ledger=json.loads(ledgerfile.read_text());entries=ledger['entries']
 for label,seconds,wall in [('measured',rs['measured_cpu_seconds'],rs['measured_wall_sum_seconds']),('estimate',30,0)]:
  eid='support_aware_robust_dimension_20261001_'+label
  assert not any(e.get('dimension_entry_id')==eid for e in entries)
  entries.append({'stage':'support_aware_robust_dimension','cpu_seconds':seconds,'wall_seconds':wall,'utc':'2026-10-01','dimension_entry_id':eid,'note':'CPU-only interval, tests and numerical diagnostics; failures included' if label=='measured' else 'Conservative administrative estimate, separate from measured processes'})
 ledger['total_cpu_seconds']=sum(e['cpu_seconds'] for e in entries);ledger['total_cpu_hours']=ledger['total_cpu_seconds']/3600
 ledgerfile.write_text(json.dumps(ledger,indent=1)+'\n')
 (ROOT/'RECORDS_FINISHED.json').write_text(json.dumps({'passed':True,'source_hash_count':len(old),'tests_passed':27,'new_certificates_256_verified':7,'cpu_ledger_hours':ledger['total_cpu_hours'],'records_appended_once':True},indent=2)+'\n')
 files=[p for p in ROOT.iterdir() if p.is_file() and p.name!='output_manifest.json']
 (ROOT/'output_manifest.json').write_text(json.dumps({'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
 print('Final records and manifest written;',len(files),'new files;',len(old),'old sources unchanged')
if __name__=='__main__':main()
