from pathlib import Path
import json,math,hashlib,statistics
ROOT=Path(__file__).parent;REPO=ROOT.parents[1]
def read(f):return json.loads((ROOT/f).read_text())
def write(f,obj):(ROOT/f).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def main():
  summary=read('summary.json');rows=read('results.json');same={v['name']:v for v in read('same_product_results.json')}
  cases={v['name']:v for v in read('inputs.json')['cases']}
  structured={v['name']:v for v in read('structured_margins.json')};hp=read('high_precision_checks.json')
  resources=[json.loads(v) for v in (ROOT/'resources.jsonl').read_text().splitlines()]
  resource=read('resource_summary.json')
  resource.update(cpu_seconds=sum(v['cpu_seconds'] for v in resources),cpu_minutes=sum(v['cpu_seconds'] for v in resources)/60,
    summed_post_import_job_wall_seconds=sum(v['wall_seconds'] for v in resources))
  write('resource_summary.json',resource)
  checks=read('final_checks.json');checks['result_tests']=read('result_tests.json');checks['test_total']=8+6+1
  write('final_checks.json',checks)
  table=[];curvature=[];rigorous=[]
  for row in rows:
    s=same[row['name']];best=row['products']['best'];kind=row['kind']
    table.append(f"| {row['case']} | {row['n']} | {kind} | {row['certified_dimension']} / {row['certified_bits']:.3f} | {best['r']} / {best['points']} / {best['r']} | {s['states']} / {s['bits']:.3f} |")
    curv=row['curvature']
    curvature.append(f"| {row['name']} | {curv['raw_ratio_max']:.6f} | {curv['projected_curvature_ratio_max']:.6f} | {row['accepted_grid']['query_slack_ratio']:.3f} | {curv['actual_preconditioned_jacobian_variation']:.6f} / {curv['certified_eta']:.6f} |")
    if row['name'] in structured:
      st=structured[row['name']]
      rigorous.append(f"| {row['name']} | {int(cases[row['name']]['certificate']['states'])} | {st['states']} | {st['bits']:.6f} | {min(st['margin_gain']):.3f}--{max(st['margin_gain']):.3f} |")
  raw=read('raw_history_diagnostic.json');rawtable=[]
  for n in [3,4]:
    for family in ['dense','independent']:
      rr=[v for v in raw if v['n']==n and v['case']==family]
      rawtable.append(f"| {family} | {n} | 32 | {max(v['direct_primary_proxy']['robust'] for v in rr)} | {max(v['direct_primary_proxy']['bits'] for v in rr):.3f} | {sum(v['matches_or_beats_old_search_winner_proxy'] for v in rr)} |")
  testdiff=max(v.get('absolute_difference',0) for row in hp for v in row['checks'])
  maxupper=max(read(f"upper_{row['name']}.json")['bits_upper'] for row in rows)
  minupper=min(read(f"upper_{row['name']}.json")['bits_upper'] for row in rows)
  report=f'''# Robust-certificate tightness / true-dimension gap

## Classification and architecture gate

**{summary['classification']}**

**MORE ROBUST-DIMENSION WORK NEEDED.** The tested machinery misses substantial
finite-error separation. However, a large binary grid is not a proof of an
equally large intrinsic continuous robust dimension, and no useful tight upper
bound was found. No architecture, learning experiment, or AMS is justified here.

## Procedural cleanup and freeze

Documentation-only cleanup commit **1e17cb8** precedes the new experiment.
ROBUST_WITNESS_SEARCH_AUDIT_ADDENDUM_20261001.md records both readings of the
ambiguous Moderate sentence. The historical Small label remains for provenance;
dense width 4 satisfies the less-strict width-local Moderate reading. All 144
expensive search finalists were SPSA descendants concentrated in few tracks;
the 10,000-history pools did not receive uniform expensive primary evaluation.
Winner/runner-up agreement within a track is weak evidence of independence.

Protocol, eight fixed endpoints, code and development tests frozen at **a218388**.
Implementation of declared CPU/raw checks: **7009d6d**. Same-product finer-grid
supplement declared before its measurement: **b081224**. Structural query and
precision diagnostic derivations: **cbe9b0d**. No old output is modified. The
source result remains 7cb9f3d. Frozen input/code hashes are in FROZEN_SETUP.json.

## Models, domain, epsilon and levels

Dense and independent recurrence at widths 3/4 and horizons 22/37, each with its
archived and frozen best-confirmation center. Same parameters, initial h=0,
parameter counts (dense 21/36; independent 15/24), input SD sqrt(3/32),
parameter-group RMS, normalized q=ones/sqrt(n), beta=max(1,||R||F), and future
preactivations [1/4,3/4]^n. **Primary epsilon = 1e-3** is a research diagnostic.
No secondary epsilon was used; the primary result is sealed in PRIMARY_FROZEN.json.

- Level A: accepted existing interval products; separately, a newly derived
  support-aware query margin on the SAME independent boxes.
- Level B: directly solved finite numerical grids and pairwise query distances.
  Critical pairs were checked at 60/100 decimal digits on CPU.
- Level C: failures of particular grids, sampled maxima, and a very loose
  rigorous covering upper bound. Numerical failure is not impossibility.

The larger-domain analysis uses fixed centers, normal correction coordinates
within [-1,1], tangent half-amplitudes 1/8, 1/4, 1/2, 1, and raw history
coordinates within +/-1 of each frozen center. These are local perturbations,
not new central witness searches. The finest successful grids used amplitude 1,
4--8 times the old tangent amplitude. This increase MUST NOT be counted entirely
as proof slack. A separate experiment uses only the EXACT old projection boxes.

## Certified versus numerical comparisons

The large-grid column gives binary-grid coordinates / states / bits. The
same-product column gives states / bits in the exact accepted projection box.
All numerical counts are finite lower estimates; none is a maximum.

| Model | Width | Witness | Historical certified directions / bits | Larger-domain numerical grid | SAME-product numerical packing |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(table)}

Both width-3 dense endpoints yield 4,096 separated points; independent width 3
yields 512. All four width-4 endpoints yield 4,096. Five basis methods were
tested: SVD, query-weighted SVD, center-curvature reordering and two seeded
rotations. For every tested prefix the COMPLETE binary grid was evaluated,
not a sampled subset. Root residuals are <=2e-12 and all declared domain checks
pass for winning grids. Rotations can distribute strong directions among many
binary choices: log2(point count) is a packing bit bound, not an intrinsic
dimension theorem or certificate of the intervening continuous product.

Farthest-point packing on Sobol/local-grid candidates hit the 512-state cap at
all eight endpoints, with three restarts. It gives at least nine numerical bits
but is censored; the complete 4,096-point grids supply the stronger 12-bit
estimate where available. No maximum is claimed. Every retained finite set and
closest pair is saved in compressed NPZ, with all-pair distance checks.

## Same-box query bias: a rigorous improvement for the control

The actual permitted-query supremum is computed over all 2^n gate-box vertices,
by convexity of the vector norm. This is the SAME allowed future family; the
old certificate used an interior finite frame only as a lower-bound device.
In independent recurrence, each parameter column is supported in one state row.
The query norm becomes a weighted Euclidean norm on the supported coordinates.
The all-equal permitted 7/8 gate supplies a stronger joint dual inequality.
INDEPENDENT_QUERY_SLACK.md derives it; 256-bit outward intervals and rational
packing arithmetic verify the following new lower calculations without changing
old rho, axes, boxes, epsilon or results:

| Independent endpoint | Historical states | New support-aware lower states | New log2(states) | Margin gain |
| --- | ---: | ---: | ---: | --- |
{chr(10).join(rigorous)}

In particular independent width-4 confirmation improves rigorously from 6 to
84 states, or log2(84) = 6.392317 bits (at least seven fixed-width binary bits).
Its numerical greedy same-box packing found 67 states; this is entirely
consistent because that search was not a maximum. The old dense 3-bit versus
independent 2.585-bit comparison cannot support a dense advantage.

The support-aware inequality includes every LEGALLY SUPPORTED residual
sensitivity coordinate; it excludes only mathematically impossible off-owner
entries. This new short derivation needs independent review, unlike the already
accepted old product geometry. No unrestricted dense claim is inferred.

## Actual versus majorant curvature and query distance

Each entry of the raw h_yy/S_yy tensors has its maximum found over 512 Sobol
points, corners, center and a bounded adversarial scan saved against its outward
majorant. The adversarial objective maximized the largest component ratio; it
did not individually globally optimize every tensor entry. Full normal-normal,
normal-tangent and tangent-tangent arrays are saved in curvature_ratios_*.npz.
The projected column is the actual implicit-section Hessian sampled over the
section divided by the selected rigorous projected bound.

| Endpoint | Raw maximum found / bound | Projected maximum found / bound | Actual query / old dual at closest accepted corner pair | Actual sampled eta / certified eta |
| --- | ---: | ---: | ---: | --- |
{chr(10).join(curvature)}

The prior independent width-4 confirmation observation is reproduced: the raw
ratio is about **0.997921**, yet its projected ratio is only about **0.219813**
and direct-query separation is about **5.795 times** its generic dual lower
value at the selected corner pair. A nearly attained raw tensor entry does not
imply a tight final product/packing certificate. Dense projected majorants are
even more conservative (roughly 2--9 percent attained in sampled sections).
All maxima found are LOWER estimates of the true supremum, not upper bounds.

## Slack decomposition and extra-direction failures

slack_decomposition.json and axis_slack.json give per-endpoint/component and
per-SVD-direction data, with explicit scope limitations:

A. Tangent strength: full available spectra, center permitted-query gain and
   directional curvature; tiny binary64 tails remain unresolved.
B. Hidden compensation: actual normal half-width use fractions are much below
   the allocated normal boxes; all implicit normal/tangent couplings were measured.
C/D. Raw and projected/mixed majorants: sampled ratios above; signed cancellation
   and thin-section geometry differ from componentwise absolute full-box bounds.
E. Contraction cap 3/4 and sampled preconditioned variation; the separate 9/10
   target fraction alone costs at most a factor 10/9 in target half-range.
F. Amplitude restriction: larger products use up to 4--8 times old amplitude;
   this is separated from same-box slack.
G. Query duality: a demonstrated control-specific loss of about 4.6--5.5 in
   projection margins, with no removal of supported residuals.
H. 17/8 versus collision threshold 2: spacing factor 17/16 = 1.0625. This small
   factor cannot explain the larger observed gaps.
I. Prefix: up to 16 directions were used for local packing; complete grids
   tested through 12. Remaining exact coordinates are explicitly untested.
J. Interval precision: increasing 192 to 256 bits gives identical binary64
   raw majorants in all eight cases. Precision-width inflation is not the main
   measured loss; dependency/absolute majorants remain conservative.
K. Basis coding, finite sampling, greedy choices and state cap can affect
   estimates. Components interact, so no factorial causal decomposition is claimed.

Dense width-4 confirmation's fourth through twelfth candidate directions were
tested across multiple bases and amplitudes. Failed grids usually have a close
query pair, not failed fitting or a demonstrated unreachable direction; later
bases often succeed. Specific first failures and closest pairs remain in every
product-trial record. They are Level C failure evidence only. No extra direction
is ruled out globally. Center diagonal Hessians for EVERY available SVD axis
were computed with a signed-jet cross-check; no center derivative is called a
finite-domain bound.

## Upper bound attempt and raw filtering diagnostic

QUERY_AND_COVER.md gives a valid sensitivity coordinate cover on the entire
declared raw-history cube. Exact recurrence majorants, upward RMS factors and
integer ceilings bound every strictly separated packing. The upper logs range
from **{minupper:.3f} to {maxupper:.3f} bits**, far above these lower estimates.
**NO USEFUL UPPER BOUND FOUND.** It cannot prove the true robust core small.

The direct raw-history diagnostic uses the same 32 frozen SEARCH IDs per width
for both models, no mutations, no spectral prefilter, and the old primary proxy:

| Model | Width | Raw histories | Max proxy directions | Max proxy bits | Meets/exceeds old search winner lexicographically |
| --- | --- | ---: | ---: | ---: | ---: |
{chr(10).join(rawtable)}

No sampled raw history materially beat the main dense winners; one independent
width-3 raw proxy matched/exceeded its old search winner lexicographically.
Raw width-4 dense included a three-direction/three-bit proxy missed by the old
expensive shortlist. This is evidence that spectral filtering excludes some
comparable raw histories, not proof that no better raw history exists. None of
these diagnostic centers was promoted or certified. Only 32 per width were
sampled, not the full 10,000-pool primary objective.

## Validation, failures and epistemic separation

Eight development tests, a signed-diagonal/full-jet test, and six final result
tests pass: **15 checks**. Forty closest-pair checks across accepted boxes,
large grids and greedy packings passed at 60/100 digits, with fixed-h gaps
below1e-50 and maximum binary64/decimal distance difference **{testdiff:.3e}**.
Eight scalar higher-precision mixed-derivative checks support the curvature
measurements. These are independent numerical paths, not interval proofs of
the new large grids. All {summary['preserved_prior_files']} prior files match
their saved hashes; frozen primary code/config remained unchanged.

Two ordinary implementation defects were repaired and charged: uint8 flag
inversion in the raw diagnostic (confirmation recipes were computed before a
metadata lookup stopped it; no valid diagnostic result or new winner followed),
and numpy integer indexing rejected by mpmath. Failed logs/code are preserved;
only affected phases repeated. The primary eight-endpoint analysis never reran.
See IMPLEMENTATION_REPAIRS.md. No validity, OOM or thermal failure occurred.

Rigorous: old accepted lower products, exact query-vertex reduction, independent
support-aware dual inequalities/counts and conservative cover upper bounds.
Numerical: all new large-grid packings, maximum-found curvature/variation,
basis comparisons, raw proxies and closest-pair decimal checks. Heuristic:
any inference from sampled maxima or rotated grids to intrinsic maximum robust
dimension. No practical memory, SGD, architecture superiority or width scaling
claim follows.

## Resources, files and stop

Measured CPU **{resource['cpu_seconds']:.6f} seconds / {resource['cpu_minutes']:.6f}
minutes**, including failed attempts; 60 administrative seconds estimated
separately. GPU-active-phase wall UPPER bound **{resource['gpu_active_wall_upper_seconds']/60:.6f}
minutes**, not kernel-only GPU time. Summed post-import job wall
**{resource['summed_post_import_job_wall_seconds']:.6f} seconds**. Peak process RAM
**{resource['peak_RAM_bytes']/2**20:.3f} MiB**, global VRAM
**{resource['peak_global_VRAM_bytes']/2**20:.3f} MiB** including existing contexts,
our allocator pool **{resource['peak_own_GPU_pool_bytes']/2**20:.3f} MiB** excluding
driver/library overhead, GPU temperature **{resource['peak_GPU_temperature_c']} C**.
CPU/high precision/intervals supplied trusted checks; GPU supplied numerical
geometry only. Parameters stayed frozen. No GAS-0/server operation, width 5,
training, Stage C, AMS v10 or architecture invention occurred.

All source, hashes, per-trial negatives, complete retained point sets, matrices,
decimal cross-checks and resources are in this isolated directory. Research
state updates are Codex_Research.md, SHARED_RESEARCH_MAP.md and the shared CPU
ledger only. No other lane notebook or old result was edited.

**Single next step:** independently review the support-aware query bound and
then tighten a certificate at THESE fixed endpoints using the observed thin
fixed-h section and model-specific dual norm. No new witness search or
architecture design. Stop after this stage.
'''
  (ROOT/'REPORT.md').write_text(report,encoding='utf-8')
  (ROOT/'README.md').write_text('# Robust-certificate tightness\n\nSee REPORT.md, PREREGISTRATION.md, summary.json, QUERY_AND_COVER.md and INDEPENDENT_QUERY_SLACK.md.\n\nOld artifacts are read-only. Large finite grids are numerical lower estimates, not intrinsic dimension certificates. Stop after this stage.\n',encoding='utf-8')
  # Append project CPU accounting once; do not rewrite past measurements.
  ledger=REPO/'experiments/automated_mechanism_search/runs/cpu_ledger.json';data=json.loads(ledger.read_text())
  key='robust_certificate_tightness_20261001'
  assert not any(v.get('tightness_entry_id','').startswith(key) for v in data['entries'])
  for suffix,seconds,note in [('measured',resource['cpu_seconds'],'All phases including failed raw/CPU attempts, diagnostics and final tests'),('estimate',60,'Conservative setup/git/documentation administrative CPU estimate')]:
    data['entries'].append({'stage':'robust_certificate_tightness','cpu_seconds':seconds,'wall_seconds':resource['summed_post_import_job_wall_seconds'] if suffix=='measured' else 0,
      'utc':'2026-10-01','tightness_entry_id':key+'_'+suffix,'note':note})
    data['total_cpu_seconds']+=seconds
  data['total_cpu_hours']=data['total_cpu_seconds']/3600
  ledger.write_text(json.dumps(data,indent=1)+'\n',encoding='utf-8')
  resume=f'''### Robust-certificate tightness resume (2026-10-01)

- **Stage/verdict:** {summary['classification']}. Primary epsilon 1e-3, existing dense/independent n=3/4, T=22/37, archived and frozen confirmation endpoints only. MORE ROBUST-DIMENSION WORK NEEDED.
- **Verified lower evidence:** numerical grids give dense 12 binary coordinates / 4,096 states at both widths, independent 9 / 512 at n=3 and 12 / 4,096 at n=4. This is finite coding dimension, not certified intrinsic continuous robust dimension. All critical pairs pass 60/100-digit fixed-h checks.
- **Same-box bias:** dense n4 confirmation old 8 states versus numerical 13; independent old 6 versus numerical 67. An outward support-aware query calculation on the unchanged independent box proves 84 states / log2(84)=6.392317 bits, still two axes. New short proof needs independent review. Generic margins lost about 4.6--5.5x for independent support.
- **Tightness:** independent n4 raw curvature 0.997921 of a bound reproduced, but projected bounds attain only 0.219813 in samples. Dense projected bounds attain about 0.021--0.086. Precision inflation 192->256 gives identical raw bounds. No useful upper bound; a cover yields 158--1514 bits. Numerical grid failures cannot prove a ceiling.
- **Cleanup:** 1e17cb8 documents both Moderate readings (n4 satisfies width-local reading), SPSA shortlist concentration and weak within-lineage runner-ups. Old history/results unchanged. Freeze a218388. 32 raw search IDs per width directly screened with the old primary proxy; no new promotion.
- **Validation/resources:** 15 checks, 40 numerical high-precision pair checks; {summary['preserved_prior_files']} old files preserved. Two metadata/library compatibility failures documented and charged. CPU {resource['cpu_minutes']:.6f} min plus 60s estimate; GPU-active wall upper {resource['gpu_active_wall_upper_seconds']/60:.6f} min; peak RAM {resource['peak_RAM_bytes']/2**20:.3f} MiB, global VRAM {resource['peak_global_VRAM_bytes']/2**20:.3f} MiB, pool {resource['peak_own_GPU_pool_bytes']/2**20:.3f} MiB, temperature50C. GAS-0, other notebooks, parameters and AGENTS untouched. CPU ledger {data['total_cpu_hours']:.6f}h.
- **Next action:** STOP. Independent review of the support-aware query bound, then targeted certificate tightening using the thin fixed-h section at these same endpoints. No architecture, training, Stage C, AMS or width5.

'''
  book=REPO/'Codex_Research.md';text=book.read_text(encoding='utf-8');assert '## AR-165' not in text
  text=text.replace('## Guardrails and current state\n\n','## Guardrails and current state\n\n'+resume,1)
  text+='\n\n## AR-165 — Robust-certificate tightness / true-dimension gap\n\n'+report+'\n'
  book.write_text(text,encoding='utf-8')
  shared=REPO/'SHARED_RESEARCH_MAP.md';text=shared.read_text(encoding='utf-8')
  prefix=f'''## Latest mathematical audit — Robust-certificate tightness (2026-10-01)

**{summary['classification']}. MORE ROBUST-DIMENSION WORK NEEDED.** Existing
n=3/4 endpoints only, epsilon1e-3, no training or architecture changes. Dense
numerical complete binary grids: 4,096 states; independent n3:512, n4:4,096.
Coding dimensions are not intrinsic continuous robust dimensions. At the SAME
accepted width4 confirmation boxes, numerical states are dense13 versus old8,
independent67 versus old6. A separate support-aware rigorous query calculation
proves independent84 states/log2(84)=6.392317bits with unchanged axes/rho/epsilon;
needs independent review. Old products remain accepted and unmodified. Raw
independent curvature ratio0.997921 reproduced, projected ratio0.219813; dense
projected ratios0.021--0.086. No useful upper bound. 15 tests,40 high-precision
pair checks. Procedural cleanup1e17cb8 preserves historical Small classification
while recording width-local Moderate eligibility/SPSA lineage limitations.
CPU{resource['cpu_minutes']:.6f}min plus60s estimate; GPU wall upper{resource['gpu_active_wall_upper_seconds']/60:.6f}min,
peak50C. GAS-0/AGENTS/other lane notebooks untouched. AR-165 and
experiments/robust_certificate_tightness_20261001/REPORT.md. **STOP** for independent
review and targeted same-endpoint certificate tightening; no architecture/AMS.

'''
  pos=text.index('## Latest mathematical audit');text=text[:pos]+prefix+text[pos:].replace('## Latest mathematical audit','## Previous mathematical audit',1)
  shared.write_text(text,encoding='utf-8')
  manifest={f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in ROOT.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='output_manifest.json'}
  write('output_manifest.json',{'sha256':manifest})
  print('Records finalized; CPU ledger hours',data['total_cpu_hours'])
if __name__=='__main__':main()
