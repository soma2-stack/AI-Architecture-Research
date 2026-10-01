"""Final preservation/accounting checks and report; no new calculations."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    freeze=json.loads((HERE/'METHOD_FROZEN.json').read_text(encoding='utf-8'))
    output=json.loads((HERE/'REPLAY_OUTPUT_FROZEN.json').read_text(encoding='utf-8'))
    comparison=json.loads((HERE/'comparison.json').read_text(encoding='utf-8'))
    checks=[]
    def add(name,ok):
        checks.append({'name':name,'passed':bool(ok)})
        if not ok:raise RuntimeError(name)
    add('all_8_frozen_method_files_unchanged',all(sha(HERE/k)==v for k,v in freeze['method_hashes'].items()))
    add('all_49_original_files_unchanged',all(sha(ROOT/k)==v for k,v in freeze['original_preservation'].items()))
    add('all_6_frozen_replay_outputs_unchanged',all(sha(HERE/k)==v for k,v in output['sha256'].items()))
    add('arithmetic_library_files_unchanged',all(sha(Path(k))==v for k,v in freeze['arithmetic_library_hashes'].items()))
    for file in ('development_tests.json','final_tests.json'):
        add(file+'_passed',json.loads((HERE/file).read_text(encoding='utf-8'))['passed'])
    add('all_78_comparison_checks_pass',len(comparison['checks'])==78 and all(x['passed'] for x in comparison['checks']))
    r=json.loads((HERE/'result_256.json').read_text(encoding='utf-8'))
    add('exact_hidden_inequalities_pass',F(r['eta_h'])<F(3,4) and max(map(F,r['forcing']))<F(r['hidden_allowance']))
    add('all_7_strict_antipodal_inequalities_pass',all(F(v)>F(1,500) for v in r['separation']))
    cpu=wall=0;peak=0
    for file in ('development_tests.json','result_192.json','result_256.json','comparison.json','sensitive_checks.json','final_tests.json'):
        z=json.loads((HERE/file).read_text(encoding='utf-8'));z=z.get('resources',z)
        cpu+=z['cpu_seconds'];wall+=z['wall_seconds'];peak=max(peak,z.get('peak_ram_bytes',0))
    resources={'measured_cpu_seconds':cpu,'measured_cpu_minutes':cpu/60,'summed_computation_wall_seconds':wall,
        'comparison_export_failure_cpu_upper_charge_seconds':1,'unmeasured_setup_import_git_allowance_cpu_seconds':30,
        'peak_measured_ram_bytes':peak,'initial_development_peak_RAM':'not monitored; final identical test suite was monitored',
        'gpu_seconds':0,'own_VRAM_bytes':0,'gpu_temperature':'not sampled; no GPU work','max_worker_count':1,
        'resource_ceiling_seconds':2700,'measurement_scope':'CPU/wall excludes assistant writing and pauses; setup/import/Git allowance separate'}
    add('resource_ceiling_pass',cpu+31<2700)
    (HERE/'final_audit.json').write_text(json.dumps({'checks':checks,'resources':resources},indent=2)+'\n',encoding='utf-8')
    faces='\n'.join(f"| {i['face']} | {i['M3']:.15g} | {i['mu']:.15g} | {i['beta']:.15g} | {i['separation']:.15g} | PASS |" for i in comparison['faces'])
    arrays='\n'.join(f"| {k} | {v['entries']} | {v['max_relative_nonzero']:.4g} |" for k,v in comparison['comparisons']['256']['arrays'].items())
    sensitive=json.loads((HERE/'sensitive_checks.json').read_text(encoding='utf-8'))
    report=f'''# Clean-room second implementation of tightened 7D certificate

## SECOND INTERVAL IMPLEMENTATION AGREES

Frozen independent width-4 confirmation, horizon37/P24, epsilon1/1000,
seven unchanged axes/amplitudes/output functionals/preconditioners. Both fresh
192- and256-bit outward interval runs PASS. All original49 source/output files
remain byte-identical. GAS-0/AGENTS/other notebooks were not edited or run.
No8D, new witness, architecture, learning, Stage C or AMS work occurred.

## Independence and chronology

Author derives from the accepted PROOF.md and PROOF_AFFINE.md, using a separate
mpmath/libmp directed-rounding backend and symmetric Taylor polynomial ring.
No original kernel, interval engine, jet or contraction helper is imported or
copied. Actual deltaW*x/deltaW*dx injections remain present even under affine
cancellation. All11 coordinates and mixed implicit terms are propagated.

This is independently implemented software, not a blinded independent author:
the author knows the earlier implementation/headline results. The trusted
mpmath arithmetic library remains a dependency; its version/source hashes
are frozen. Candidate metadata not needed for the calculation is ignored.

- Accepted source commit622e001; accepted certificate first committed622e001.
- Method/candidate freeze24f0648, pushed before official execution.
- Both independent outputs frozenf8ce4dd before reading reference arrays.
- Candidate SHA-256: {freeze['source_candidate_sha256']}.
- METHOD_FROZEN.json records mathematical source/input/library/preservation hashes.
- REPLAY_OUTPUT_FROZEN.json records the fresh output hashes before comparison.

## Whole-array comparison

All52,857 entries of all8 arrays compared at BOTH precisions (105,714 entry
comparisons). Exact-zero patterns agree. New positive majorants use192/256-bit
rounding instead of per-operation binary64 nextafter rounding, so tiny numerical
differences are expected. Maximum relative difference is1.69853658783692e-13,
well below the prospectively declared1e-10 tolerance. No constants were tuned.

| Array | Entries per precision | Maximum relative difference at256bits |
|---|---:|---:|
{arrays}

The complete normal-normal, normal-tangent, tangent-tangent and selected-axis
mixed derivative arrays, implicit y2/y3, fixed3 and selected3 are included.
Exact dyadic arbitrary-precision bounds are in exact_bounds_192/256.json.gz;
NPZ binary64 upward summaries are for comparison, not primary certificates.
The192/256 NPZ summaries are bitwise identical; exact rational beta values
differ by at most {float(F(comparison['precision_max_differences']['beta'])):.8g}.

## Fixed-h section

New eta_h={float(F(r['eta_h'])):.17g}; accepted0.044064912334239315.
Equal normal half-width ah={float(F('7543/524288')):.17g}.
Forcing upper bounds: {', '.join(f'{float(F(v)):.17g}' for v in r['forcing'])}.
Hidden allowance(1-eta_h)ah={float(F(r['hidden_allowance'])):.17g}.
Maximum forcing/allowance={float(max(map(F,r['forcing']))/F(r['hidden_allowance'])):.17g}.
Raw history-coordinate radius={float(F(r['domain'])):.17g}<1.
Rational nonsingularity of K_h/K/W and nonnegative inverse of I-Eh verified.
This certifies the simultaneous curved fixed-h section, not just its tangent.

## Seven face certificates

Here mu is the amplitude-normalized query dual margin for ell=(KL)_i/a_i.
The residual-safe support metric, permitted7/8 gate and epsilon are unchanged.
Every row proves antipodal separation>2epsilon=0.002 over its ENTIRE face.

| Face | M3 upper | mu lower | beta lower | Separation >=2beta | Result |
|---|---:|---:|---:|---:|---|
{faces}

Weakest face7 separation>={min(x['separation'] for x in comparison['faces']):.17g}.
This retains continuous-encoder k>=7 under the accepted contract. It is NOT
7bits,128 pairwise-separated corners, a maximum dimension or practical memory.

## Nearly-tight entries and face1

New HH3[1,0,0,0] and HS[11,0,0] bounds match the reference to rounding-level
differences (indices and values in comparison.json). A separate signed
univariate chain-rule path scans all2,048 corners plus center, at90digits,
and rechecks the largest sampled value at120digits. Ratios actual/bound:
{sensitive['sensitive_entries'][0]['actual_to_bound_ratio']:.15g} and
{sensitive['sensitive_entries'][1]['actual_to_bound_ratio']:.15g}; no violation.
These finite numerical checks are NOT uniform certificates; the interval
induction establishes the uniform bound. They confirm the small~0.1% slack
has not been consumed by the1e-13 implementation differences.

Face1 M3: accepted3.226820573749615; independent{comparison['faces'][0]['M3']:.17g}.
Its third-order penalty is{comparison['faces'][0]['third_penalty']:.17g},
beta={comparison['faces'][0]['beta']:.17g}. Holding other terms fixed, M3
would have to increase by factor{comparison['faces'][0]['M3_failure_multiplier']:.17g}
to erase its strict margin. This is a diagnostic, not permission to change bounds.

Exact rational contraction independently verifies ALL7 M3 upper bounds from
the saved selected3 tensor. A separate100-decimal-digit Decimal path verifies
all7 query margins; exact squared inequalities and rational beta arithmetic
verify outward direction and strict separation. No ordinary floating-point
cosine or threshold argument establishes certification.

Separate90/120-digit nonlinear fixed-h face1 midpoint-antipode checks agree:
Phi1 difference={sensitive['face_one'][1]['Phi1_antipodal_difference'][:40]},
numerical dual-query lower estimate={sensitive['face_one'][1]['numerical_dual_query_lower_estimate'][:40]}.
Normal compensation~3.41304e-6 is insideah; residuals~1.53e-92/1.21e-122.
This is supporting numerical evidence at one pair, not the all-face proof.

## Validation, repairs, resources

12 synthetic tests passed before freeze,12 passed in final repeat;78 exact
comparison/consistency checks and{len(checks)} final provenance/resource checks pass.
Tests cover directed arithmetic, high-precision tanh gates, repeated/mixed
Taylor indices, signed center/autograd agreement, second/third bounds,
affine cancellation with retained parameter injections, matrix inverses,
frozen inputs, contraction indexing, CPU enforcement and forbidden imports.

One POST-RESULT comparison export bug (numpy.int64 JSON index) is preserved
in comparison_export_failure.json. Formatting conversion only was repaired;
all mathematical checks had passed. No frozen source or output was modified.
No numerical or certificate disagreement was found.

Measured CPU {cpu:.6f}s = {cpu/60:.6f}minutes.
Summed measured computation wall {wall:.6f}s, excluding assistant/Git pauses.
Failed export charged1CPU-s; unmeasured setup/import/Git allowance30CPU-s,
listed separately rather than presented as measured time.
Peak monitored process RAM {peak/2**20:.6f}MiB (final synthetic tests);
official replay peaks~62.61/64.46MiB. Initial development test RAM was not
monitored; the same test suite was monitored in the final repeat.
OneCPUprocess/thread, GPU/CUDA0, ownVRAM0; GPU temperature not sampled because
no GPU work was launched. No model server or unrelated process was touched.

## Single recommended next step

Technically ready for a separately preregistered CHEAP NUMERICAL8D–24D
feasibility screen at the SAME endpoint/metric/query contract, with fixed
candidate rules and a small budget. This means section dimensions8–24,
not new widths. It does not predict8D will pass and does not authorize new
official certificates, architecture design or learning. No such screen ran.
STOP here and obtain the next owner authorization.

## Files and scope

All new source, tests, frozen inputs, directed bounds, comparison records,
numerical supporting checks and manifests live in this isolated directory.
Only Codex_Research.md, SHARED_RESEARCH_MAP.md and the new-directory raw-byte
attribute rule were updated outside it. Preexisting changes in Claude's
notebook and GAS-0 remain unstaged and untouched. OUTPUT_MANIFEST.json lists
every new artifact and its hash.
'''
    replacements={'horizon37/P24':'horizon 37 / P24','independent width-4':'independent width-4',
        'original49':'original 49','No8D':'No 8D','All11':'All 11','All52,857':'All 52,857',
        'all8':'all 8','use192/256':'use 192/256','The192/256':'The 192/256',
        'commit622e001':'commit 622e001','committed622e001':'committed 622e001',
        'freeze24f0648':'freeze 24f0648','frozenf8ce4dd':'frozen f8ce4dd','accepted0.':'accepted 0.',
        'accepted7/8':'accepted 7/8','permitted7/8':'permitted 7/8','Face1':'Face 1','face1':'face 1',
        'ALL7':'ALL 7','all7':'all 7','at90digits':'at 90 digits','at120digits':'at 120 digits',
        'all2,048':'all 2,048','12 synthetic':'12 synthetic','freeze,12':'freeze, 12',
        ';78':'; 78','below bounds':'below bounds','charged1CPU-s':'charged 1 CPU-s',
        'allowance30CPU-s':'allowance 30 CPU-s','NUMERICAL8D':'NUMERICAL 8D',
        'dimensions8':'dimensions 8','predict8D':'predict 8D','OneCPUprocess/thread':'One CPU process/thread'}
    for a,b in replacements.items():report=report.replace(a,b)
    (HERE/'REPORT.md').write_text(report,encoding='utf-8')
    manifests={str(p.relative_to(HERE)):sha(p) for p in HERE.iterdir() if p.is_file() and p.name!='OUTPUT_MANIFEST.json'}
    (HERE/'OUTPUT_MANIFEST.json').write_text(json.dumps({'sha256':manifests,'historical_files_preserved':49,
        'current_parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'classification':comparison['classification'],'checks':len(checks),'resources':resources},indent=2))
if __name__=='__main__':main()
