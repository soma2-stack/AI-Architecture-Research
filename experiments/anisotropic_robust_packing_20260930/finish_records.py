"""Write the final descriptive report and append charged resource accounting."""
import json,time,math,hashlib,datetime
from fractions import Fraction as Q
from pathlib import Path
import psutil
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
rows=json.loads((ROOT/'summary.json').read_text());weak=json.loads((ROOT/'weak_axis_certificates.json').read_text())

def table(header,records):
    return '| '+' | '.join(header)+' |\n| '+' | '.join(['---']*len(header))+' |\n'+''.join('| '+' | '.join(map(str,row))+' |\n' for row in records)
def fmt(x):return f'{float(x):.6g}'
comparison=table(['Case','n','T','P','Exact fiber D','Primary robust D / bits','Secondary robust D / bits','Old bits'],[
    [r['case'],r['n'],r['T'],r['P'],r['D_exact'],f"{r['primary_D_robust']} / {r['primary_bits']:g}",
     f"{r['secondary_D_robust']} / {r['secondary_bits']:g}",r['old_isotropic']['old_bits']] for r in rows])
axes=table(['Case','n','Chosen chart','rho_i','mu_i','mu_i rho_i','N_i','Bits/axis'],[
    [r['case'],r['n'],r['selected_mode'],', '.join(map(fmt,r['rho_i'])),', '.join(map(fmt,r['mu_i'])),
     ', '.join(map(fmt,r['observable_half_ranges'])),str(r['N_i']),str(r['bits_per_axis'])] for r in rows])
specs=[]
for r in rows:
    b=json.loads((ROOT/f"basis_{r['case']}_n{r['n']}.json").read_text());s=b['singular_values']
    specs.append([r['case'],r['n'],fmt(s[0]),fmt(s[len(s)//2]),fmt(s[-1]),
                  fmt(float(s[0])/float(s[-1])),b.get('two_precision_relative_discrepancy','not required')])
spectra=table(['Case','n','Largest','Middle sorted entry','Smallest','Tangent condition','100/160-digit discrepancy'],specs)
reasons=table(['Case','n','A small tangent','B curvature bound','C query bound','D joint failure','E conservative/untested','F interval width','G units','H other'],[
 [r['case'],r['n']]+[r['discarded_failure_counts'][x] for x in 'ABCDEFGH'] for r in rows])
curvature=table(['Case','n','Uniform fixed-h Hessian Frobenius bounds','Projection aspect ratio','Selected K condition','L condition (numerical)'],[
 [r['case'],r['n'],str(r['directional_curvature_F']),fmt(r['rho_aspect_ratio']),fmt(r['selected_preconditioner_condition']),fmt(r['output_projection_condition_numerical'])] for r in rows])
epsilon=[]
for r in rows:
    for method,curve in r['curves'].items():
        epsilon.append([r['case'],r['n'],method]+[f"{x['D_robust']} / {x['bits']:.6g}" for x in curve])
curves=table(['Case','n','Frozen chart','epsilon1e-2 D/bits','PRIMARY1e-3 D/bits','epsilon1e-4 D/bits'],epsilon)
weakrows=[]
for r in rows:
    n=r['n'];D=r['D_exact'];case=r['case'];wr=[x for x in weak if x['case']==case and x['n']==n]
    labels=[('all',D),('minus bottom1',D-1),('minus ~5%',math.ceil(.95*D)),('minus ~10%',math.ceil(.9*D)),('top1',1)]
    for label,retained in labels:
        x=next(x for x in wr if x['retained']==retained)
        weakrows.append([case,n,label,retained,fmt(x['output_common_radius']),fmt(Q(x['radius_improvement_exact'])),x['bits']])
weaktable=table(['Case','n','Kept region','Axes','Certified common half-range','Improvement vs all axes','Bits at1e-3'],weakrows)
led=[json.loads(x) for x in (ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
# Include this light reporting process. No later numerical work is planned.
m=psutil.Process().memory_info()
ledrow={'job':'final documentation/accounting','cpu_seconds':time.process_time(),'wall_seconds_post_import':0,
        'wall_seconds_process':time.time()-psutil.Process().create_time(),'peak_ram_bytes':max(m.rss,getattr(m,'peak_wset',m.rss)),
        'gpu_seconds':0,'gpu_used':False,'cuda_used':False,'workers':1}
with (ROOT/'cpu_ledger.jsonl').open('a') as f:f.write(json.dumps(ledrow)+'\n')
led.append(ledrow)
resource={'measured_cpu_seconds':sum(x['cpu_seconds'] for x in led),'measured_wall_seconds_process_sum':sum(x['wall_seconds_process'] for x in led),
          'unmetered_import_estimate_seconds':5,'administration_estimate_seconds':20,
          'peak_ram_bytes':max(x['peak_ram_bytes'] for x in led),'gpu_seconds':0,'stage_gpu_allocated_bytes':0,
          'gpu_temperature':'Not measured: this stage never launched a GPU workload','cuda_used':False,
          'workers_per_numerical_job':1,'blas_threads':1,'configured_cpu_cap_seconds':2700}
resource['measured_cpu_minutes']=resource['measured_cpu_seconds']/60
resource['charged_cpu_seconds']=resource['measured_cpu_seconds']+25
assert resource['charged_cpu_seconds']<2700
(ROOT/'resources.json').write_text(json.dumps(resource,indent=2))
report=f'''# Anisotropic robust packing / product entropy

## Classification

**ONLY A FEW ROBUST DIRECTIONS SURVIVE.**

Primary error is exactly epsilon=1e-3 in the PREVIOUS secondary normalized
gradient units. It is a research diagnostic, not a production tolerance.
Primary SVD results were frozen and pushed at86efe2f BEFORE secondary
query-frame projection and epsilon curves. No witness, horizon, epsilon,
model parameter, or metric was tuned. The accepted theorems are premises.

## 1. Dense versus independent result

{comparison}

The secondary improvement is real within this certificate: dense widths2/3/4
give1/2/1 robust directions and2/2/1 packing bits; independent gives1/1/0
directions and1/1/0 bits. This does NOT certify that the rest of the reachable
region lacks robust directions. These are LOWER certificates from a bounded
grid, not maxima or upper bounds. The same method/units/head convention and
horizons apply to both families. Independent has fewer parameters, explicitly
reported; this is a structural comparison, not a matched capability result.

Dense old raw radii4.24e-17,3.40e-29,1.36e-43 map through the smallest
parameter RMS to normalized ball guarantees1.048e-18,7.509e-31,2.815e-45.
All give zero old bits at this epsilon. The independent old-method radii are
NEW same-method comparators, not previously archived facts:1.124e-13,
3.504e-15,5.009e-18, also zero bits. The certified old effective dimension at
the declared error is zero in all six cases. Bit gains are additive; division
by an old zero-bit bound is undefined.

## 2. Coordinate convention and complete spectra

h units are unchanged. History perturbations are in input SD sqrt(3/32).
S_phi=S_theta D_theta, D_theta=archived R/W/b group RMS. Effective adjoints
use q=ones/sqrt(n), beta=max(1,Frobenius R), and the SAME future preactivation
box[1/4,3/4]^n. Error remains Euclidean in phi-gradient coordinates throughout.
No normalization is chosen to improve the answer. Exact parameter values,
input histories and their hashes are preserved in provenance; no new seed.
Widths2/3/4 use T11/22/37 and archived seeds9502100/9602100/9602100.

All raw and normalized singular values are in spectra.csv; complete100-digit
SVD axes/history frames and70-digit spectra are in basis_*.json. These are
HIGH-PRECISION NUMERICAL, not certified ranks or memory dimensions.

{spectra}

The history kernel is that of J_h at the archived point. Rationalized
directions need not be exact null vectors: normal compensation and the actual
interval center absorb their error. Selected rational-frame Gram defects and
rigorous condition upper bounds are in summary.json; they are essentially1.
Physical input SD and parameter RMS factors are accounted for separately.

## 3. Directional/mixed curvature and joint geometry

CPU interval propagation encloses all gates across each simultaneous history
box. Componentwise directional and mixed h/S second derivatives include
tanh third derivatives and the actual deltaR*h,deltaW*x,delta b injections.
All positive binary64 products/sums round upward; no BLAS reduction is used.
An implicit normal correction holds h exactly fixed. Its first and second
derivatives are bounded by an exact-rational nonnegative Neumann inverse.
These bounds feed a scaled multivariate contraction test for selected S
projections. Every mixed term is included; separate one-axis certificates
are never multiplied without the joint test. See PROOF.md and engine.py.

{curvature}

Primary uses dyadic SVD left functionals. Secondary uses a finite-head Gram
dual output projection, with the SAME SVD history directions. The physical
query norm never changes. Rational inverse preconditioners and scaled
Jacobian residuals are saved for every selected certificate. All12 original
regions/margins replay at256 bits with the ORIGINAL preconditioners/radii,
not newly fitted ones; center inverse residuals are below1e-8.

**Geometry limitation:** a Cartesian product is proved in selected sensitivity
PROJECTIONS, with an exact CURVED constant-h lift. No flat full-S tensor box
is asserted. This is sufficient because joint query-dual inequalities hold
even in the presence of unselected residual coordinates.

## 4. Every selected radius, margin and axis contribution

This table chooses the better chart at PRIMARY epsilon; ties keep primary.
All exact fractions, alternate primary/secondary radii and mixed-curvature
arrays are in certificate_*.json and results_*.json. Displayed decimals round
for readability; integer packing never uses displayed values.

{axes}

For width3 dense, bits per direction are1+1. Width2 dense has2 bits in one
direction. A one-position axis contributes0 bits, including width4 independent.
Strongest/median/weakest retained observable half-ranges are explicitly in
summary.json. For the two-axis dense3 product these are0.001648/0.001648/
0.001325; its aspect ratio is1.2486. The one-axis products have aspect1,
which says nothing about the shape of the remaining sensitivity tensor.

The full tangent spectra are extremely elongated, but the certified retained
projection products are low dimensional and not strongly elongated. The full
nonlinear reachable-region shape remains unresolved.

## 5. Sharper actual future-query inequality

Gamma=(1/4)I+(5/8)11^T gives allowed gates7/8 and5/8. At fixed h, invertible
W realizes these future inputs. Put C_tilde=R^T Gamma. For tensor functional
L_i, B_i=C_tilde^-1 L_i and
mu_i=1/[sqrt(n) beta sum_j norm2(B_i[j,:])]. Outward lower enclosures are used.
For ANY sensitivity difference, D_C>=mu_i*abs(delta projection_i).
Thus this guarantee survives changes in all the other coordinates. Direct
future parameter injection cancels because h is fixed. There is no unjustified
Frobenius/sqrt(n) replacement or independently multiplied axis assumption.

Coordinate spacing is17epsilon/(8mu_i), strictly larger than2epsilon/mu_i.
N_i=floor(2rho_i mu_i/(17epsilon/8))+1 is exact Fraction arithmetic. Product
states>=product N_i and bits>=sum log2 N_i. This is deterministic uniform
finite-state/no-replay memory, not bytes/VRAM or a stochastic average-case bound.

## 6. Why directions were discarded

{reasons}

Counts are diagnostic attributions within the DECLARED certificate/grid,
not a proof of a physical cause or global impossibility. A: tangent amplitude
too small even before this dual penalty at the largest declared half-length;
G: the SAME history direction clears that diagnostic in raw parameter units
but not declared normalized units; B: uniform curvature bounds limit the
certified range; C: finite-query dual lower margin is insufficient. D/E/F/H
were not uniquely attributed by that rule. Stronger query/curvature certificates
may rescue directions; the unsearched tail is not declared intrinsically dead.
The per-axis audit uses nontrivial positions in ANY tested joint product;
such findings from different boxes are never pooled into one robust dimension.

Multiaxis proposal failures are substantial despite zero D in this attribution
table: mixed-sensitivity-curvature failures total
{sum(r['proposal_failure_counts']['mixed_sensitivity_curvature'] for r in rows)};
normal-Jacobian failures total{sum(r['proposal_failure_counts']['hidden_jacobian_dominance'] for r in rows)};
normal-box-inclusion failures total{sum(r['proposal_failure_counts']['hidden_section_box_inclusion'] for r in rows)}.
Every rejected proposal is preserved. Zero F is consistent with successful
192/256-bit checks, not a claim that interval overestimation is absent.

## 7. Weak-direction versus curvature attack

The following are actual CERTIFIED reduced-square comparators using an
UNCHANGED global curvature majorant within each witness. No discarded axis
is silently removed from the main theorem. Additional top4/8/16 cases and
exact rational inequalities are in weak_axis_certificates.json.

{weaktable}

Removing only the weakest dense direction improves the common radius by
roughly77x/52x/206x at widths2/3/4. Removing more of the tail improves it much
further, but even TOP1 retains zero packing bits under the global majorant.
Thus the weakest direction is important but not the sole limitation. The
directional curvature enclosure and query-aligned projection also matter.
The separate sigma_min-squared counterfactuals in weak_direction_diagnostics.json
are HIGH-PRECISION NUMERICAL models, not certificates. No percentage of the
TRUE reachable geometry is inferred from these sufficient bounds.

## 8. Secondary error curve, no retuning

Each curve reuses its frozen PRIMARY-epsilon-selected chart. No radii, axes,
or normalization are reoptimized at secondary epsilon. These are diagnostic
tolerances only. D is jointly certified nontrivial coordinate count.

{curves}

At1e-2 all bounds are zero. At1e-4 the secondary dense charts give approximately
5.044/7.700/4.087 bits, still only1/2/1 directions. Exact dimension is not
replaced by this scale-dependent sufficient robust count.

## 9. Validation and evidence strength

-12 focused unit tests passed, including outward arithmetic, wide tanh
  monotonicity/range, mixed-curvature versus CPU autodiff, exact affine product
  control, joint query duality with residual coordinates, CPU/frozen parameters,
  and integer-safe spacing.
-8 final artifact checks passed. Primary hashes and all5 archived source hashes
  are unchanged. All12 original selected certificates replay at256 bits.
-Width4 spectra independently agree at100/160 digits.
-15 grid points reconstructed numerically, followed by100-digit CPU forward
  evaluation. Nontrivial pair query distances exceed2epsilon. This is
  HIGH-PRECISION NUMERICAL validation, not the rigorous existence certificate.
-One interval dependency overflow campaign was preserved and corrected before
  primary completion;172.9375CPU-s remain charged. Two output/import errors
  are documented in RUNTIME_CORRECTION.md. No result or threshold was hidden,
  erased, or tuned. Original scientific config unchanged.

CERTIFIED here means a computer-assisted enclosure under explicit IEEE,
dyadic/Taylor and exact-rational arithmetic assumptions. New fixed-h/product
proof and implementation still need independent review; no proof assistant
verification is claimed. Ordinary singular spectra, shape descriptions and
failure attributions are not mathematical certificates.

Verification background: [Rump, Verification methods, Acta Numerica2010](https://www.tuhh.de/ti3/rump/intlab/ActaNumerica2010.pdf).
Such sufficient tests establish a region when they pass; failure alone does
not exclude other regions. The cited work does not certify this implementation.

## 10. Resources, files and stop

Measured CPU:{resource['measured_cpu_seconds']:.6f}s = {resource['measured_cpu_minutes']:.6f}minutes,
including failed attempts and process imports. Process-wall sum:
{resource['measured_wall_seconds_process_sum']:.6f}s (not total human research elapsed time).
An additional5s failed-import estimate plus20s administration estimate is
charged separately, giving{resource['charged_cpu_seconds']:.6f}s total charged.
Peak process RAM:{resource['peak_ram_bytes']}bytes ({resource['peak_ram_bytes']/2**20:.6f}MiB).
Single-worker numerical jobs/one BLAS thread. Well inside45CPU-minute cap.

GPU/CUDA UNUSED. GPU time0, stage GPU allocations0bytes. Device temperature
not measured because this stage launched no GPU workload; owner's unrelated
GPU usage is not reported as zero. Tiny n<=4 matrices and required exact
interval/rational computations made CPU the appropriate resource. No model
server, GPU dependency installation or GAS-0 operation occurred.

New files are confined to this directory: preregistration/config; interval,
engine, verification, reconstruction, analysis and checking code; all raw
attempts/spectra/bases; primary freeze; exact certificates and replays;
curvature/query/radius/packing/failure metadata; resources, report and proof.
Outside it only Codex_Research.md, SHARED_RESEARCH_MAP.md and the shared CPU
ledger are updated. Prior negatives and unrelated local/staged work preserved.

Commits:72fa7aa preregistration; e41e609 implementation;86efe2f verified primary
freeze/push. The completion commit contains this report and all secondary
evidence; obtain its exact SHA from git log or the owner's final response.

**Single next step:** independent hostile replay/review of the width3 two-axis
curved fixed-h contraction and query-duality product certificate. The result
does not justify an architecture, arbitrary-width robust scaling, production
memory claim, training, Stage C or AMS v10. STOP after this stage.
'''
(ROOT/'REPORT.md').write_text(report,encoding='utf-8')
(ROOT/'README.md').write_text('''# Anisotropic robust packing

Read REPORT.md for the complete result and PROOF.md for the new joint
certificate. Classification: ONLY A FEW ROBUST DIRECTIONS SURVIVE.
No learning/model server/GPU/GAS-0 run occurs in this directory.

Primary protocol config.json is frozen at72fa7aa. PRIMARY_FROZEN.json hashes
the SVD results before secondary work. Raw proposals and the incomplete initial
campaign are append-only. Both original campaigns remain separately identified.

Files:
- results_svd.json / verification_svd.json: primary selected regions/replay.
- results_frame.json / verification_frame.json: declared secondary projection.
- certificate_*.json: exact fractions, all mixed-curvature and residual bounds.
- basis_*.json / spectra.csv: raw/scaled spectra and exact rationalized axes.
- summary.json: side-by-side packing, radii, margins and error curves.
- directional_audit.json: every axis and diagnostic failure attribution.
- weak_axis_certificates.json: rigorous weakest-tail/global-majorant removals.
- weak_direction_diagnostics.json: distinct numerical sigma-squared models.
- reconstruction_checks.json: numerical reconstruction, NOT the certificate.
- tests.json / final_checks.json / source_hashes.json: validation/provenance.
- resources.json / cpu_ledger.jsonl: all attempts and resource charges.
- RUNTIME_CORRECTION.md: preserved implementation/output failures.

For authorized reproduction, use a NEW isolated directory with the same
config/source and archived witnesses; do not delete these outputs. Order:
test_engine.py, engine.py svd, verify.py svd, freeze_primary.py, commit freeze,
engine.py frame, verify.py frame, analysis.py, reconstruct.py,
weak_certificates.py, final_checks.py. Frozen output files refuse overwrite.
No new witness or epsilon selection is permitted. End after certification.
''',encoding='utf-8')
ledgerpath=REPO/'experiments/automated_mechanism_search/runs/cpu_ledger.json'
ledger=json.loads(ledgerpath.read_text());ident='anisotropic_robust_packing_20260930'
assert not any(x.get('anisotropic_entry_id','').startswith(ident) for x in ledger['entries'])
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
ledger['entries'] += [
 {'stage':'anisotropic_robust_packing','cpu_seconds':resource['measured_cpu_seconds'],
  'wall_seconds':resource['measured_wall_seconds_process_sum'],'utc':utc,
  'note':'CPU-only primary/secondary joint certificates, failed campaign, replay and checks; process-wall sum',
  'anisotropic_entry_id':ident+'_measured'},
 {'stage':'anisotropic_robust_packing','cpu_seconds':25,'wall_seconds':0,'utc':utc,
  'note':'5s failed pre-meter import estimate +20s administrative estimate; distinct from measured CPU',
  'anisotropic_entry_id':ident+'_estimate'}]
ledger['total_cpu_seconds']+=resource['charged_cpu_seconds'];ledger['total_cpu_hours']=ledger['total_cpu_seconds']/3600
assert ledger['total_cpu_hours']<30
ledgerpath.write_text(json.dumps(ledger,indent=1)+'\n')
print(json.dumps(resource,indent=2));print('Shared cumulative CPU hours',ledger['total_cpu_hours'])
