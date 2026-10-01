"""Documentation and append-only shared accounting; no certificate execution."""
from pathlib import Path
import json, hashlib, difflib, datetime
from fractions import Fraction as Q

ROOT=Path(__file__).parent;REPO=ROOT.parents[1]
manifest=json.loads((ROOT/'input_manifest.json').read_text())
cfg=json.loads((ROOT/'inputs.json').read_text())
A=json.loads((ROOT/'regenerated_certificate_192.json').read_text())
checks=json.loads((ROOT/'final_checks.json').read_text())
audits=[json.loads((ROOT/f'consistency_{bits}.json').read_text()) for bits in (192,256)]
jobs=[json.loads(line) for line in (ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
cpu=sum(row['cpu_seconds'] for row in jobs);wall=sum(row['wall_seconds'] for row in jobs)
peak=max(row['peak_ram_bytes'] for row in jobs)
assert cpu<600 and all(x['gpu_seconds']==0 for x in jobs)
resources={'measured_cpu_seconds':cpu,'measured_cpu_minutes':cpu/60,
           'summed_post_import_wall_seconds':wall,'whole_task_wall_time':'not metered; includes documentation and review',
           'peak_process_ram_bytes':peak,'peak_process_ram_MiB':peak/2**20,
           'gpu_seconds':0,'peak_vram_bytes':0,'gpu_temperature':'not applicable: no GPU workload launched',
           'cuda_used':False,'workers':1,'administrative_cpu_estimate_seconds':15,
           'measured_code_checkpoint':'50d566d','freeze_checkpoint':'8622551',
           'all_runs_including_failed_premeasurement_tests_accounted':True}
(ROOT/'resources.json').write_text(json.dumps(resources,indent=2)+'\n',encoding='utf-8')
sha_table='\n'.join('| '+x['snapshot']+' | '+x['sha256']+' |' for x in manifest['sources'])
slacks=[float(Q(x)) for x in audits[0]['target_box_slack']]
hidden=[float(Q(x)) for x in audits[0]['hidden_self_map_slack']]
rho=list(map(lambda x:float(Q(x)),cfg['rho_i']));mu=list(map(lambda x:float(Q(x)),cfg['mu_i']))
observable=[float(Q(x)*Q(y)) for x,y in zip(cfg['rho_i'],cfg['mu_i'])]
qdiff=[float(Q(x)) for x in checks['mu_256_minus_mu_192_exact']]
report=f'''# Independent clean replay: width-3 two-axis certificate

## Classification

**CLEAN REPLAY VERIFIED — TWO-AXIS CERTIFICATE REPRODUCED**

Source commit: `{manifest['source_commit']}`. Freeze commit `8622551`;
validated execution code commit `50d566d`. All newly generated artifacts are
in `experiments/anisotropic_robust_packing_replay_20261001/`. The original
experiment, its proof, all 54 hashed files, and the archived witness remained
unchanged. GAS-0, other notebooks, GPU, model servers, training, Stage C and
AMS v10 were not operated on.

## Inputs and clean dependency order

Dense tanh recurrence, n=3, P=21, T=22, initial h=0. Same rational parameter
values and history, input SD sqrt(3/32), R/W/b RMS sensitivity coordinates,
epsilon exactly 1/1000, frozen three normal and two tangent directions. All
five amplitudes are 1/8. The rational preconditioners, output functionals,
query frame, original rho and original mu are tested without adaptation.

`inputs.json` SHA-256:
`{manifest['inputs_sha256']}`.

1. Run the 12 pinned interval/jet/curvature machinery checks plus 5 isolation
   and fresh-derivative checks: **17/17 pass**.
2. Load only frozen model/history/constants into the runtime; cached original
   endpoint intervals and curvature arrays are absent from runtime inputs.
3. Freshly compute all 4,356 endpoint-Jacobian interval entries at 192 bits.
   Independently propagate at 100 decimal digits. Rebuild the complete QR/SVD;
   the selected rationalized history and left axes reproduce exactly.
4. Reconstruct the query-aligned output functionals from the regenerated frame;
   they reproduce exactly. The SVD basis is the only SVD intermediate needed;
   an unrelated SVD-mode packing certificate is not imported or rerun.
5. Regenerate uniform curvature on the COMPLETE simultaneous five-axis box,
   then the hidden contraction, implicit section bounds, selected mixed
   curvature, joint projection contraction and target self-map.
6. Regenerate query margins/duality, exact integer packing and all six
   pairwise strict separations.
7. Start a fresh process and repeat all interval-Jacobian and curvature
   calculations at 256 bits, using the SAME frozen K/rho/mu.
8. Perform separate scalar `mpmath.diff` cross-checks, exact algebraic artifact
   checks and preservation/hash checks. Only then compare original bounds.

This is an independent clean execution, **not a separately authored interval
library**. Pinned reviewed arithmetic/jet/curvature formulas remain shared
source. They have no original generated-bound dependency. The separately
written scalar recurrence and differentiation path provide supporting
cross-checks, not replacements for interval certification.

## Regenerated numerical certificate

| Quantity | Frozen / fresh 192-bit result | Fresh 256-bit result |
| --- | ---: | ---: |
| Hidden contraction eta_h | {A['eta_hidden']:.17g} | same |
| Joint projection contraction eta | {A['eta_sensitivity']:.17g} | same |
| rho_1 | {rho[0]:.17g} | original target verified |
| rho_2 | {rho[1]:.17g} | original target verified |
| mu_1 | {mu[0]:.17g} | original lower margin verified |
| mu_2 | {mu[1]:.17g} | original lower margin verified |
| mu_1 rho_1 | {observable[0]:.17g} | same frozen value |
| mu_2 rho_2 | {observable[1]:.17g} | same frozen value |
| N_1, N_2 | 2, 2 | 2, 2 |
| Distinguishable states / bits | 4 / 2 | 4 / 2 |

Every displayed number is a rounded view; all decisions use exact rationals
and outward interval enclosures in the stored JSON. At 192 bits all 17
compared fields, including curvature tables, K matrices, projections, radii,
margins and packing arithmetic, are exactly equal to the archived result.

At 256 bits the query-margin enclosures tighten upward by approximately
{qdiff[0]:.3g}, {qdiff[1]:.3g}. This expected precision-dependent refinement
does not change the frozen margin or packing. The complete HH/HS binary64
majorants and downstream contraction/curvature bounds are unchanged. All
4,356 256-bit endpoint intervals lie inside their fresh 192-bit counterparts.

## Full mixed-curvature regeneration

`raw_curvature_192.json` and `raw_curvature_256.json` contain all 75 hidden
and 1,575 normalized-sensitivity mixed upper entries. Each contains the
normal-normal 3x3, both normal-tangent 3x2/2x3 blocks and tangent-tangent
2x2 blocks, for every output coordinate. No curvature matrix was imported.

After implicit fixed-h compensation, the two selected projection curvature
majorants are:

```
axis/output 1:
{json.dumps(A['projected_curvature'][0])}
axis/output 2:
{json.dumps(A['projected_curvature'][1])}
```

The Frobenius fixed-section mixed upper table is:

```
{json.dumps(A['directional_curvature_F'])}
```

The hidden residual majorant is:

```
{json.dumps(A['hidden_jacobian_residual_upper'])}
```

The joint selected residual majorant is:

```
{json.dumps(A['scaled_jacobian_residual_upper'])}
```

Both contractions are below one. Hidden self-map slacks are
{hidden}; target self-map slacks are {slacks}. Exact nonzero determinants
of both rational preconditioners are saved in `consistency_192.json` and
`consistency_256.json`. These certify exact hidden-state attainment and
the entire simultaneous target rectangle, not separate one-axis segments.

## Query duality and exact packing

Each full n-by-P output functional satisfies the exact rational identity
L_i=C_tilde B_i. The regenerated coefficient matrices are stored in the
consistency records. The norm bound yields

`D_C(S1,S2) >= max_i mu_i |Delta Psi_i|`

for arbitrary full sensitivity differences, including unselected residual
coordinates. Invertible W realizes the allowed gate vectors; their interval
containment is checked. Direct future injection cancels because the histories
have exactly the same h. No residual-coordinate vanishing is assumed.

Using the frozen rational mu and rho, `delta_i=17 epsilon/(8 mu_i)` and
`N_i=floor(2 rho_i/delta_i)+1` give 2 positions on each axis. For every one of
the six distinct Cartesian pairs the certified query-distance lower bound
is **17/8000 = 0.002125 > 2 epsilon = 0.002**. Four deterministic memory
states and therefore at least 2 bits follow in the declared local model.

## Higher precision and independent numerical path

100-digit separately written scalar forward evaluation plus nested
`mpmath.diff` agrees with three regenerated endpoint mixed derivatives to
absolute error below 1e-80. Four additional scalar third-derivative checks
on this actual witness (normal-normal, normal-tangent, tangent-tangent)
lie below the regenerated complete-box majorants. These supporting checks
are HIGH-PRECISION NUMERICAL; rigorous certification comes from the outward
interval and ordered majorant paths, not midpoint comparisons.

## Documentation-only formalization patch

`FORMALIZATION_PATCH.md` and `FORMALIZATION.patch` explicitly add:

- Equal instantiated normal half-widths 1/8, justifying the unweighted
  infinity-norm self-map condition.
- The Neumann-series nonsingularity implication for the square
  preconditioners, hence exact fixed-point target attainment.
- The integral mean-value/Taylor forcing formula with all mixed terms.

Original PROOF.md is untouched; no theorem, mathematical conclusion,
certificate constant or numerical proposal was changed.

## Failures, resources and limitations

Initial pinning encountered LF/CRLF byte differences. The first test run
exposed two source-extraction/isolation wrapper bugs (missing dataclass
decorator; thread environment set after NumPy import). They were repaired
before official replay. Failed tests and compute remain recorded in
`tests.json`, `SETUP_REPAIRS.md` and the append-only replay ledger.
No official regenerated certificate inequality failed.

Measured CPU: **{cpu:.6f} seconds / {cpu/60:.6f} minutes**, including the
failed and successful tests. Sum of post-import job wall times:
{wall:.6f} seconds; whole research/documentation wall time was not metered.
Peak process RAM: **{peak/2**20:.6f} MiB**. One CPU/BLAS worker.
GPU time **0**, replay VRAM allocation **0**, CUDA unused. No GPU temperature
sample was needed because no GPU workload was launched. Administrative
CPU estimate 15 seconds is accounted separately from measured work.

This does not establish maximal robust dimension, an all-width finite-error
law, practical VRAM requirements, a learning benefit or architectural novelty.
Shared source dependence is transparent: the requested independent clean
execution is completed, but not independent authorship of the interval engine.

## Frozen source hashes

| Snapshot | SHA-256 |
| --- | --- |
{sha_table}

All original files passed byte-hash preservation checks. Runtime implementation
hashes and artifact hashes are in `output_manifest.json`.

## Single recommended next step

Owner review of this clean replay and the three documentation-only proof
clarifications. Stop here; no further experiment or architecture work is
authorized by this replay result.
'''
(ROOT/'REPORT.md').write_text(report,encoding='utf-8')
# Construct an actual proof patch without writing to the original source.
proof=(ROOT/'frozen_sources/PROOF.md').read_text(encoding='utf-8')
patchtext=(ROOT/'FORMALIZATION_PATCH.md').read_text(encoding='utf-8')
normal=patchtext.split('## Insert in “Constant-hidden-state section”, after the self-map condition\n\n')[1].split('## Insert in “Anisotropic inverse-product certificate”, before Banach conclusion')[0].rstrip()
selected=patchtext.split('## Insert in “Anisotropic inverse-product certificate”, before Banach conclusion\n\n')[1].rstrip()
patched=proof.replace('The absolute inverse is bounded by\n',normal+'\n\nThe absolute inverse is bounded by\n')
patched=patched.replace("Banach's theorem therefore gives a history attaining EVERY point of the\n",selected+"\n\nBanach's theorem therefore gives a history attaining EVERY point of the\n")
diff=''.join(difflib.unified_diff(proof.splitlines(True),patched.splitlines(True),
    fromfile='a/experiments/anisotropic_robust_packing_20260930/PROOF.md',tofile='b/experiments/anisotropic_robust_packing_20260930/PROOF.md'))
(ROOT/'FORMALIZATION.patch').write_bytes(diff.encode('utf-8'))
# Append only, retaining all pre-existing global ledger entries.
ledger_path=REPO/'experiments/automated_mechanism_search/runs/cpu_ledger.json'
ledger=json.loads(ledger_path.read_text());key='anisotropic_robust_packing_replay_20261001'
assert not any(row.get('clean_replay_entry_id','').startswith(key) for row in ledger['entries'])
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
ledger['entries'].extend([
    {'stage':'anisotropic_clean_replay','cpu_seconds':cpu,'wall_seconds':wall,'utc':stamp,
     'note':'CPU-only frozen width-3 fresh interval/curvature replay, failed/successful tests, final checks; wall sum excludes imports',
     'clean_replay_entry_id':key+'_measured'},
    {'stage':'anisotropic_clean_replay','cpu_seconds':15,'wall_seconds':0,'utc':stamp,
     'note':'Conservative source-pinning and administrative estimate, not measured certificate CPU',
     'clean_replay_entry_id':key+'_estimate'}])
ledger['total_cpu_seconds']=sum(row['cpu_seconds'] for row in ledger['entries'])
ledger['total_cpu_hours']=ledger['total_cpu_seconds']/3600
assert ledger['total_cpu_hours']<ledger['cap_cpu_hours']
ledger_path.write_text(json.dumps(ledger,indent=1)+'\n',encoding='utf-8')
# Self-contained resume and append-only research entry; preserve prior resumes.
notebook=REPO/'Codex_Research.md';text=notebook.read_text(encoding='utf-8')
resume=f'''### Clean replay resume — width-3 two-axis certificate (2026-10-01)

- **Lens/stage:** independent clean execution of source1e4bf42's frozen n3/T22 certificate. **CLEAN REPLAY VERIFIED — TWO-AXIS CERTIFICATE REPRODUCED.** No new witness, axis, epsilon, theorem, width or architecture.
- **Verified result:** all 17 normal-precision reported fields reproduce exactly; eta_h0.060253012714867084, eta0.30423690175351176. Frozen rho0.008936697672956191/0.007157274316691487 and mu0.1844230111587496/0.18515681028226835 certify the simultaneous two-axis rectangle. Exact N2/2,4states,2bits; every Cartesian pair has query separation>=17/8000>2epsilon. Arbitrary residual coordinates included.
- **Clean dependencies:** fresh 4356-entry endpoint interval Jacobian,100-digit QR/SVD axes reproduced exactly; all75 HH and1575 HS mixed majorants recomputed at192/256bits from frozen history/params. No old bound/cache used. All4356 higher-precision entries nested; raw mixed bounds unchanged. Reviewed interval/jet/kernel code is shared source, explicitly disclosed; separate scalar differentiation cross-checks support it.
- **Evidence/resources:**17/17 tests; four extra actual-witness mixed-derivative checks;54 old files preserve hashes. Freeze8622551/validated execution50d566d. Measured{cpu}CPU-s ({cpu/60:.6f}min),{peak/2**20:.6f}MiB peak;15s administrative estimate separately. CPU only/one worker; GPU0/CUDA/GAS-0/server untouched. Three formalization insertions saved separately; original PROOF unchanged. SETUP_REPAIRS preserves initial wrapper/test failures.
- **Unresolved/exact next action:**STOP. Owner review of experiments/anisotropic_robust_packing_replay_20261001/REPORT.md and documentation-only patch. Clean execution addresses the requested replay gap; it is not independent authorship of the interval library. No architecture, training, Stage C or AMS v10 follows automatically. AR-163.

'''
text=text.replace('## Guardrails and current state\n\n','## Guardrails and current state\n\n'+resume,1)
text+='\n\n## AR-163 — Independent clean replay of the width-3 two-axis certificate\n\n'+report+'\n'
notebook.write_text(text,encoding='utf-8')
shared=REPO/'SHARED_RESEARCH_MAP.md';text=shared.read_text(encoding='utf-8')
summary=f'''## Latest mathematical audit — Clean width-3 two-axis replay (2026-10-01)

**CLEAN REPLAY VERIFIED — TWO-AXIS CERTIFICATE REPRODUCED.** Source1e4bf42
preserved. Isolated experiments/anisotropic_robust_packing_replay_20261001/;
freeze8622551, validated execution50d566d; AR-163. Owner reports three prior
mathematical reviews. This execution recomputes the endpoint Jacobian and all
normal-normal/normal-tangent/tangent-tangent bounds from frozen inputs, using
shared reviewed source but no cached bounds. At192bits every reported original
field reproduces exactly;256bits verify original K/rho/mu and all4356 intervals
are nested. eta_h0.060253012714867084,eta0.30423690175351176; exact simultaneous
rectangle has N2/2,4states,2bits at unchanged diagnostic epsilon1e-3. Residual
sensitivity coordinates are included in query duality.17 tests pass; separate
100-digit scalar mixed derivatives cross-check the kernel.54 original files
unchanged; documentation-only patch addresses equal normal widths,
preconditioner nonsingularity and explicit mean-value forcing. Measured
{cpu}CPU-s, peak{peak/2**20:.6f}MiB;15s estimate separate. GPU0/CUDA/GAS-0/server
untouched. Shared CPU total{ledger['total_cpu_hours']:.6f}h. **STOP for owner
review of replay/formalization.** No new architecture or learning conclusion.

'''
text=text.replace('## Latest mathematical audit — Anisotropic robust packing (2026-09-30)',summary+'## Previous mathematical audit — Anisotropic robust packing (2026-09-30)',1)
shared.write_text(text,encoding='utf-8')
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*')
        if p.is_file() and '__pycache__' not in p.parts and p.name!='output_manifest.json'}
(ROOT/'output_manifest.json').write_text(json.dumps({'source_commit':manifest['source_commit'],'sha256':hashes},indent=2)+'\n',encoding='utf-8')
print(json.dumps(resources,indent=2))
