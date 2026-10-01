"""Record finalized result and append shared accounting; no numerical search."""
import json,hashlib,datetime,math
from pathlib import Path
ROOT=Path(__file__).parent;REPO=ROOT.parents[1]
summary=json.loads((ROOT/'summary.json').read_text());winners=json.loads((ROOT/'frozen_winners.json').read_text())
certs=json.loads((ROOT/'certification_results.json').read_text());conditioning=json.loads((ROOT/'conditioning_comparison.json').read_text())
jobs=[json.loads(x) for x in (ROOT/'resources.jsonl').read_text().splitlines()]
cpu=sum(row['cpu_seconds'] for row in jobs);gpu=sum(row['gpu_wall_upper_seconds'] for row in jobs);wall=sum(row['wall_seconds'] for row in jobs)
ram=max(row['peak_ram_bytes'] for row in jobs);vram=max(row['peak_global_vram_bytes'] for row in jobs);pool=max(row['peak_our_gpu_pool_bytes'] for row in jobs);temp=max(row['peak_gpu_temperature_c'] for row in jobs)
resources={'measured_cpu_seconds':cpu,'measured_cpu_minutes':cpu/60,'gpu_active_phase_wall_upper_seconds':gpu,
           'gpu_active_phase_wall_upper_minutes':gpu/60,'summed_post_import_job_wall_seconds':wall,
           'peak_ram_bytes':ram,'peak_RAM_MiB':ram/2**20,'peak_global_vram_bytes':vram,'peak_global_VRAM_MiB':vram/2**20,
           'peak_CuPy_pool_bytes':pool,'peak_CuPy_pool_MiB':pool/2**20,'peak_gpu_temperature_c':temp,
           'gpu_note':'phase wall upper bound, not kernel-only time; global VRAM includes owner/other contexts; CuPy pool excludes library/context overhead',
           'invalid_attempt_cpu_seconds':jobs[2]['cpu_seconds'],'invalid_attempt_gpu_wall_upper_seconds':jobs[2]['gpu_wall_upper_seconds'],
           'administrative_CPU_estimate_seconds':60,'gpu_preflight_estimate_seconds':2,
           'workers':1,'safety_failure':False,'CUDA_used_for_numerical_search':True,'certificate_device':'CPU'}
(ROOT/'resource_summary.json').write_text(json.dumps(resources,indent=2)+'\n',encoding='utf-8')
table='\n'.join(f"| {row['n']} | {row['case']} | {row['baseline_robust']} / {row['baseline_bits']:.3f} | {row['role']} | {row['robust']} | {row['states']} | {row['bits_exact']} |" for row in summary['comparison'] if row['role']!='runner_up')
hashes='\n'.join(f"| {w['n']} | {w['case']} | {w['role']} | {w['id']} | {w['history_sha256']} |" for w in winners)
score_rows=[];diag_rows=[];geometry=[]
for row,w,c,cond in zip(summary['comparison'],winners,certs,conditioning):
    if row['role']=='runner_up':continue
    base=next(x['baseline'] for x in json.loads((ROOT/'phase_search_results.json').read_text()) if x['n']==row['n'] and x['case']==row['case'])
    rec=w['recipe'];old=base['recipe'];d=row['diagnostics']
    score_rows.append(f"| {w['n']} | {w['case']} | {w['role']} | {base['stage1']:.4f} / {w['stage1']:.4f} | {base['stage2']:.4f} / {w['stage2']:.4f} | {old['robust']},{old['bits']:.3f} / {rec['robust']},{rec['bits']:.3f} |")
    diag_rows.append(f"| {w['n']} | {w['case']} | {w['role']} | {d['largest_gain']:.3f} | {d['baseline_effective_rank']:.3f} -> {d['effective_rank']:.3f} | {d['baseline_counts']['0.001']} -> {d['counts']['0.001']} |")
    geometry.append({'n':w['n'],'case':w['case'],'role':w['role'],
         'recipe':row['recipe'],'mu':c['result']['mu_i'],'observable':c['result']['observable_half_ranges'],
         'directional_curvature_F':c['result']['directional_curvature_F'],
         'eta_hidden':c['result']['eta_hidden'],'eta_joint':c['result']['eta_sensitivity'],
         'baseline_mu':cond['baseline_query_mu'],'baseline_curvature':cond['baseline_directional_curvature_F']})
(ROOT/'geometry_comparison.json').write_text(json.dumps(geometry,indent=2)+'\n',encoding='utf-8')
gtable='\n'.join(score_rows);dtable='\n'.join(diag_rows)
report=f'''# Robust-witness search

## Classification and direct answer

**{summary['classification']}**

At epsilon exactly1e-3, new dense width3 search witnesses certify3 jointly
nontrivial directions,8states,3bits versus the archived2directions,4states,2bits.
Its best untouched confirmation witness certifies only2directions,4states,2bits.
Dense width4 certifies3directions,8states,3bits in BOTH search and confirmation,
versus archived1direction,2states,1bit. These are improved sufficient lower
bounds, but still few directions compared with exact fixed-h dimensions63/144.
The frozen moderate/large criteria were not met; they were not changed.

Thus archived witnesses were not optimal for robust certification. This search
does NOT establish a large robust core or a global robust-dimension ceiling.
Filtering, chosen axes/prefixes, box grids and interval conservatism can miss
larger regions. The tested result supports only a modest local-witness gain.
Independent recurrence also improves, especially at width4, so this is not a
unique architectural benefit of dense interaction.

## Design and immutable inputs

Widths2/3/4, horizons11/22/37, frozen archived parameters, initial h=0,
the same dense and independent families. Dense P10/21/36 and exact supported
fixed-h sensitivity dimensions20/63/144. Independent P8/15/24, supported
dimensions8/15/24. No parameter learning, architecture change or new width.
R/W/b RMS scaling, input SD sqrt(3/32), fixed normalized head/query-frame
conventions and epsilon are unchanged. No GAS-0/server operation.

Search centers lie in[-.5,.5], the archived generator support. Certificate
history perturbations were checked coordinatewise<=1, the existing local
patch domain. Future query preactivations remain[1/4,3/4] under the accepted
fixed-head convention; future inputs may differ from past-generator support,
exactly as in the accepted prior query family. No domain enlargement.

Protocol/config/pools committed before scoring: **1aa89ef**. Implementation
repair/preserved invalid campaign: **5bb034c**. Complete valid search/objective
sealed and committed **deb3a85** before confirmation. All18 histories/axes/
recipes frozen and committed **06eccf9** before interval certification.
`pool_manifest.json`, `models.json`, `SEARCH_SEALED.json` and
`WINNERS_FROZEN.json` contain the input/code/source hashes.

## Phase A: numerical discovery

Ten thousand exogenous histories per width:4000 random,4000 scrambled Sobol,
2000 smooth low-amplitude histories. Deterministic8000/2000 search/confirmation
split. Both models receive the SAME pool/domain/horizon/normalization.
Per model/width, search adds512 Gaussian mutations plus384 spectral/SPSA
evaluations (8parents x16iterations x3evaluations). Confirmation has no
adaptive generation. Valid Phase A counts are:

- 30,000 paired exogenous histories;60,000 model-history evaluations.
- 5,376 adaptive evaluations across six model/width cells.
- **65,376 valid initial/adaptive evaluations total.** Repeated shortlist
  calculations are additional derivative work, not new proposed histories.
- Per cell:128 histories pass stage2 query screening;24 reach full mixed-
  curvature proxy recipe evaluation. Search and confirmation use the same
  shortlist limits; confirmation pool size is smaller by design.

Stage1 emphasizes many strong fixed-h singular directions, not sigma_min.
Stage2 includes accepted dual query margins. The PRIMARY objective is fixed
lexicographic `(joint nontrivial packing directions, integer packing bits,
sum observable ranges)`. A whole simultaneous-box floating curvature majorant,
implicit hidden-section calculation, query-aligned projections and all mixed
terms determine the numerical proxy. Prefixes1/2/3/4/6/8 and the three
amplitudes/two profiles/two normal factors were frozen before results.
Only one selected recipe per winner is certified; no post-failure tuning.

GPU runtime: isolated `cupy-cuda12x[ctk]==14.2.0`, CUDA12.9 component wheels,
float64, batch128. CPU/GPU derivative and curvature calculations were
cross-checked. Torch's existing CPU installation and all model servers were
left alone. Runtime package versions are in runtime_packages.txt.
Runtime installation follows [CuPy's official installation documentation](https://docs.cupy.dev/en/stable/install.html).
No GPU midpoint, SVD, proxy or exploratory output is labeled CERTIFIED.

### Baseline / selected numerical scores

Each score pair is baseline/new. Primary pairs are approximate directions,bits.

| Width | Model | Role | Stage1 | Stage2 | Primary proxy |
| --- | --- | --- | --- | --- | --- |
{gtable}

All per-history spectra and stage1 scores are preserved in compressed NPZ;
full finalist spectra/curvature/query comparisons are in
conditioning_comparison.json and geometry_comparison.json.

## Phase B: rigorous CPU certification

All18 preregistered candidates passed192bit certification AND verification
of their original product/margins at256bits. **Zero certificate failures.**
Fresh interval RTRL/input jets regenerated endpoint derivatives; no previous
Jacobian or curvature cache was used. All normal-normal, normal-tangent,
tangent-tangent and mixed selected-axis majorants were generated on the
complete simultaneous history box. Implicit normal compensation keeps h
exactly fixed; scaled contraction certifies the entire selected product.
Arbitrary unselected sensitivity differences are included in query duality.
CPU mpmath100digits initializes a rational preconditioner once, not a new
search recipe. Uniform intervals and explicit upward majorants verify it.

The integer rule is exactly
`delta_i=17epsilon/(8mu_i)`, `N_i=floor(2rho_i/delta_i)+1`.
Different product grid points have query separation>=17epsilon/8>2epsilon.
Reported log2(state counts) is the exact symbolic bit bound; decimals are
rounded views. A literal integer-width binary memory requires the ceiling.

| Width | Model | Archived directions/bits | Role | Certified directions | States | Exact bits lower bound |
| --- | --- | --- | --- | ---: | ---: | --- |
{table}

Runner-ups match the best-search direction/state counts in every cell; all
three roles and their complete certificates are in summary.csv/json and
certificates/. Dense width4 has3x the archived direction count,3x its bit
bound and4x its distinguishable-state count; width3 search gains one axis/
one bit and2x states, but confirmation does not repeat that gain. Dense width2
search gains one axis but no bits; confirmation has6states versus archived4.
Independent width4 search/confirmation improves from an archived0-bit
certificate to3/6states; a bit-ratio to zero is undefined.

## Conditioning, curvature and query interpretation

| Width | Model | Role | Largest singular-value ratio | Effective rank baseline -> new | Counts>=1e-3 baseline -> new |
| --- | --- | --- | ---: | --- | --- |
{dtable}

These are NUMERICAL tangent diagnostics, not certified memory dimensions.
In particular dense width4's count>=1e-3 decreases15->12, and effective rank
decreases8.091->about7.64 despite its better product certificate. Its largest
singular value rises only~15%; width3 rises~4%. Improving raw spectral richness
alone therefore does not explain the certified gains. Local directional/
mixed curvature and query alignment matter jointly. Raw projection mu or
curvature entries are not directly invariant under changes of L; compare
observable products mu*rho in the unchanged physical gradient metric.
No factorial causal ablation of these contributions was performed.

Every retained/discarded coordinate in each frozen recipe has its exact mu,
rho, observable range, N and bit contribution stored in the certificate;
all uniform raw Hessian tensors are compressed in curvature_*_192/256.npz.
The scalar spectra remain GPU numerical values; the product/range/query
conditions are rigorous under the accepted rounding model.

## Search versus untouched confirmation

Width3 dense loses the third certified direction on confirmation: possible
selection/adaptive-witness overfitting or rare favorable histories. Do not
report that third direction as a replicated confirmation property.
Width4 dense repeats3directions/8states, so its local gain is not confined to
adaptively optimized search histories. Width2 dense and width4 independent
have stronger confirmation packings than their search winners. No broad
distributional guarantee follows from comparing two selected extrema.

## Secondary epsilon arithmetic

Primary summary was frozen in PRIMARY_FROZEN.json before secondary counts
at1e-2/1e-4 were calculated. secondary_epsilon_curves.json uses ONLY the same
certified products/margins, not new axes or reoptimized boxes. It does not
change primary epsilon or classification and does not extrapolate outside
the certified region.

## Implementation anomalies, validation and limits

The first search attempt improperly carried dense adaptive histories into
the following independent model, breaking matched counts. It is preserved
under invalid_attempt1/; both models reran from scratch after an isolation
test was added. No confirmation primary scores had been opened, and no
objective, scientific threshold or budget-per-valid-model was changed.

An early nullspace/margin unit check used confirmation history0 at width3;
it did not inspect a robust score or tune the objective. The test now uses
dedicated development randomness. That low-level exposure is disclosed;
none of the six frozen confirmation winners is that history. Their scores
were first inspected only after the complete search/code seal.

Eight current numerical/split/parity checks pass;12 accepted interval/jet/
curvature machinery checks pass. Final artifact checks verify18 winners,
exact packing arithmetic,256bit original-target verification, frozen hashes
and preservation of all{summary['prior_files_preserved']} prior evidence files.
No search/certificate hardware safety failures, NaNs or OOMs occurred.

A bounded staged/prefix search and conservative local sufficient certificate
cannot establish that only three robust directions actually exist. No
arbitrary-width robust law, finite-precision VRAM requirement, SGD advantage,
learning result or architecture discovery is claimed.

## Resources

All attempts/tests/checks, including the invalid campaign, are charged:

- CPU **{cpu:.6f}s / {cpu/60:.6f}min** (60s administrative estimate separately).
- GPU-active-phase wall UPPER bound **{gpu:.6f}s / {gpu/60:.6f}min**;
 2s preflight estimate separately. Kernel-only GPU time was not measured.
- Sum of post-import job wall times **{wall:.6f}s**; whole interactive
  documentation/wait time not metered.
- Peak process RAM **{ram/2**20:.6f}MiB**.
- Peak GLOBAL VRAM **{vram/2**20:.3f}MiB**, including pre-existing contexts;
  peak our CuPy allocator pool **{pool/2**20:.3f}MiB**, excluding library/context
  overhead. Do not interpret the pool as complete process VRAM.
- Peak GPU temperature **{temp}C**, below the80C preferred/86C stop limits.
- Frozen neural parameters; no optimizer learning, model inference server,
  GAS-0, Stage C, AMS v10, new architecture or width5 operation.

## Frozen winner history hashes

Full histories and rationalized axes/functionals are in frozen_winners.json.
Its SHA and selection metadata are sealed in WINNERS_FROZEN.json.

| Width | Model | Role | ID | History SHA-256 |
| --- | --- | --- | --- | --- |
{hashes}

## Single recommended next step

Independent hostile review of the newly certified three-axis dense products
and the sealed search/confirmation validity. Stop here; these small local
gains do not authorize architecture invention or learning experiments.
'''
(ROOT/'REPORT.md').write_text(report,encoding='utf-8')
readme='''# Robust-witness search

See REPORT.md, config.json and PREREGISTRATION.md. Final primary verdict and
all18 candidate comparisons are in summary.json/csv. Winners are frozen in
frozen_winners.json; proof conditions are in certificates/. Original archived
evidence is never overwritten. invalid_attempt1 preserves the parity defect.

Execution order (completed; do not rerun over outputs):

1. setup.py; test_search.py in the isolated CuPy venv; test_certificate.py on CPU.
2. search.py search; seal.py search; commit before confirmation.
3. search.py confirmation; seal.py winners; commit before certification.
4. certify.py on CPU; analyze.py; finish_records.py.

The isolated .venv is ignored. Install cupy-cuda12x[ctk]==14.2.0 only there.
CPU numerical/interval dependencies are inherited from the existing CPU
Python environment. Do not operate any model server or GAS-0.

No further research is run automatically.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
# Shared cumulative accounting: preserve every old row and negative result.
ledger_path=REPO/'experiments/automated_mechanism_search/runs/cpu_ledger.json'
ledger=json.loads(ledger_path.read_text());key='robust_witness_search_20261001'
assert not any(row.get('robust_witness_entry_id','').startswith(key) for row in ledger['entries'])
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
ledger['entries'].extend([{'stage':'robust_witness_search','cpu_seconds':cpu,'wall_seconds':wall,'utc':utc,
                         'note':'GPU numerical discovery, invalid parity campaign, corrected search/confirmation, CPU certificates and checks; summed post-import job wall',
                         'robust_witness_entry_id':key+'_measured'},
                        {'stage':'robust_witness_search','cpu_seconds':60,'wall_seconds':0,'utc':utc,
                         'note':'Conservative setup/install/git/telemetry/admin CPU estimate, separate from measured Python processes',
                         'robust_witness_entry_id':key+'_estimate'}])
ledger['total_cpu_seconds']=sum(row['cpu_seconds'] for row in ledger['entries']);ledger['total_cpu_hours']=ledger['total_cpu_seconds']/3600
assert ledger['total_cpu_hours']<ledger['cap_cpu_hours']
ledger_path.write_text(json.dumps(ledger,indent=1)+'\n',encoding='utf-8')
resume=f'''### Robust-witness search resume — small local gains (2026-10-01)

- **Lens/stage:** owner-authorized witness search/certification, not architecture invention. **{summary['classification']}** at unchanged research epsilon1e-3, model families/parameters, input-SD/RMS/query units and T11/22/37. No width5, training, Stage C or AMS.
- **Frozen search:**30,000 paired exogenous histories,80/20 split;65,376 valid model-history evaluations including5376 adaptive mutation/SPSA probes. Initial protocol1aa89ef; complete objective/search sealdeb3a85 before confirmation;18 winners/runner-ups freeze06eccf9 before CPU certification. No post-certificate search/recipe adjustment.
- **Certified result:**all18 pass192bit joint mixed-curvature/implicit fixed-h products and256bit original-target/margin replay. Dense n2 search2dirs/4states/2bits, confirmation2dirs/6states/log2(6); n3 search3/8/3, confirmation2/4/2; n4 both3/8/3. Archives dense1/2/1dirs,2/2/1bits. Independent n2/n3 both1/2/1; n4 search1/3/log2(3), confirmation2/6/log2(6), archive0bit. Exact integer counts, arbitrary residual sensitivity directions included.
- **Hostile interpretation:**width3's extra axis does not repeat on untouched confirmation. Width4 dense repeats3axes/3bits, but effective spectral rank and counts>=1e-3 decline versus archive; gains are jointly geometric/query/curvature dependent. Independent also benefits. Only small certified cores; staged filtering and sufficient certificates cannot prove a ceiling or dense architectural advantage.
- **Anomalies/resources:**initial pool-carryover campaign invalid/preserved, rerun both models after repair; no objective changes. Earlier unit history0 n3 had low-level diagnostic exposure, no robust score; selected confirmations all different/untouched.8 numerical+12 machinery checks pass; all prior evidence hashes preserved. CPU{cpu:.6f}s ({cpu/60:.6f}min),60s estimate separate; GPU-phase wall upper{gpu/60:.6f}min, peakRAM{ram/2**20:.3f}MiB, globalVRAM{vram/2**20:.3f}MiB, our pool{pool/2**20:.3f}MiB, peak{temp}C. No hardware/certificate failures. GAS-0/server/other notebooks untouched. Shared CPU total{ledger['total_cpu_hours']:.6f}h. AR-164.
- **Exact next action:**STOP. Independent hostile review of experiments/robust_witness_search_20261001/REPORT.md and new dense three-axis product certificates. No architecture or learning work follows automatically.

'''
p=REPO/'Codex_Research.md';text=p.read_text(encoding='utf-8')
text=text.replace('## Guardrails and current state\n\n','## Guardrails and current state\n\n'+resume,1)
text+='\n\n## AR-164 — Robust-witness search and frozen joint certification\n\n'+report
p.write_text(text.rstrip()+'\n',encoding='utf-8')
p=REPO/'SHARED_RESEARCH_MAP.md';text=p.read_text(encoding='utf-8')
entry=f'''## Latest mathematical audit — Robust-witness search (2026-10-01)

**{summary['classification']}.** Same n2/3/4,T11/22/37,
model/parameter/normalization/query families,epsilon1e-3. Frozen paired pools:
10,000 histories per width,80/20 split;65,376 valid model-history evaluations
includingmutation/SPSA. Protocol1aa89ef/search sealeddeb3a85;18 winners frozen
06eccf9 before fresh CPU certification. All18 pass192bits and256bit original
product/margin checks. Dense search dirs2/3/3,bits2/3/3; confirmation dirs2/2/3,
bitslog2(6)/2/3. Archive dirs1/2/1,bits2/2/1. Width4 repeats3axes/8states/3bits;
width3 extra search axis does not repeat in confirmation. Independent n2/n3
remain1axis/1bit; n4 search1axis/log2(3),confirmation2axes/log2(6),from0 archived
bits. Gains not unique to dense; exact dimensions are not robust dimensions.
Initial pool-carryover campaign invalid/preserved and rerun; objective unchanged.
Unit diagnostic exposure of one confirmation history disclosed; none selected.
8 numerical/12 machinery checks pass; original evidence preserved. Measured
CPU{cpu:.6f}s plus60s estimate; GPU-phase wall upper{gpu/60:.6f}min,peak{temp}C,
RAM{ram/2**20:.3f}MiB; no safety failures. Global ledger{ledger['total_cpu_hours']:.6f}h.
GAS-0/server/training/Stage C/AMS untouched. AR-164 and
experiments/robust_witness_search_20261001/REPORT.md. **STOP: independent review
of new three-axis products/search validity.** No global ceiling or new architecture.

'''
text=text.replace('## Latest mathematical audit — Clean width-3 two-axis replay (2026-10-01)',entry+'## Previous mathematical audit — Clean width-3 two-axis replay (2026-10-01)',1)
p.write_text(text,encoding='utf-8')
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*')
        if p.is_file() and '.venv' not in p.parts and '__pycache__' not in p.parts and p.name!='output_manifest.json'}
(ROOT/'output_manifest.json').write_text(json.dumps({'sha256':hashes},indent=2)+'\n',encoding='utf-8')
print(json.dumps(resources,indent=2))
