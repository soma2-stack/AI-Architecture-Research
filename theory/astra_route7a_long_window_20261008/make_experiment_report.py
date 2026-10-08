"""Render completed numeric evidence without modifying theory claims."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'results.json').read_text())
extra=json.loads((ROOT/'extra_results.json').read_text())
diag=json.loads((ROOT/'feedback_diagnostics.json').read_text())
scaling=json.loads((ROOT/'scaling_results.json').read_text())
lines=['# Long-window numerical evidence','',
'Status: finite reference-model experiments; NOT a robust-dimension certificate.','',
'## Setup and reproducibility','',
'CPU NumPy float64; fixed seeds; g_H=1-n^-2 (historical W=1 regression additionally uses .99999). One fixed feature uses sigma=.05. Complete rank-two chronological feedback is retained. Capture is at the final high step, before trace compensation. Main cohorts evolve autonomously. The held-high variant is separately labeled.','',
'Run from the repository with Python and NumPy (Matplotlib for plots):','',
'```powershell',
'$env:OPENBLAS_NUM_THREADS="1"',
'python theory/astra_route7a_long_window_20261008/run_experiments.py',
'python theory/astra_route7a_long_window_20261008/extra_checks.py',
'python theory/astra_route7a_long_window_20261008/diagnose_feedback.py',
'python theory/astra_route7a_long_window_20261008/scaling_cases.py',
'python theory/astra_route7a_long_window_20261008/plot_results.py',
'python theory/astra_route7a_long_window_20261008/make_experiment_report.py',
'```','',
'The main runner resumes completed cases from results.json. For a fresh reproduction use a copy of this folder without result files; preserve the archived outputs. --quick omits million-width cases. Three starts and two vertex updates per start at small widths; two starts and one update at million width. Horizons 1,2,4 for small widths and 1,4 for million width. Only the first future gate is optimized; remaining future gates are high. This is a legal subset search, not a global optimizer.','',
'Complete matrices are evaluated through exact forward/transpose products; dense n-by-n matrices are not materialized. Query scores below are full-parameter response norms. M, L and H are separately evaluated, with H=M-L.','',
'## Main sweep','',
'| n | m | R | W | precharge | N | pair | strong geometry | best found M | L at selected query | H at selected query | seconds |',
'|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---:|']
for x in d['cases']:
    q=max(x['queries'],key=lambda q:q['best_M'])
    lines.append(f"| {x['n']} | {x['m']} | {x['R']} | {x['W']} | {x['L']} | {x['N']} | {x['pattern']} | {x['strong_geometry']} | {q['best_M']:.6g} | {q['L_at_best_M']:.6g} | {q['H_at_best_M']:.6g} | {x['elapsed_s']:.1f} |")
lines += ['', 'Random means independent R-by-m Rademacher control signs versus their negatives, seed 812. Aligned means all-positive versus all-negative. Different W changes total duration and public track geometry; ratios are schedule comparisons, not an isolated causal estimate at equal total cost. All cases obey basic no-wrap. Small widths do not meet the stronger inherited large-n/spacing regime.', '',
'## Numerical legality and regression','',
f"Maximum endpoint disagreement: {max(x['endpoint_error'] for x in d['cases']):.6g}.",
f"Maximum live trace-neutrality residual: {max(x['maxtrace'] for x in d['cases']):.6g}.",
f"Maximum measured driven/capture inverse-lift input: {max(x['maxinput'] for x in d['cases']):.6g}.",
f"Gate range over main cases: [{min(x['gate_min'] for x in d['cases']):.6g}, {max(x['gate_max'] for x in d['cases']):.17g}]. Zero gates at a saturated front are floating-point tanh rounding, not a prescribed illegal donor gate.",
'', 'Regression details:', '', '```json',json.dumps(d['regression'],indent=2),'```','',
'An initial result-reporting TypeError (abs applied to a Python list) was fixed before any main case was checkpointed. The passed regression results were reused; no superseded scientific measurement was promoted. run.log preserves this event.','',
'## Deterministic public bath/front certificate','',
'These values come from the support-bound proof in RESEARCH.md, not empirical maxima. They certify the stated reference bath/front premises for the three listed geometries; dense lifting and source/query assumptions remain separate.','',
'| n | m | N | bath-gate upper | first-front upper | certified |','|---:|---:|---:|---:|---:|---|']
for x in extra['public_certificates']:
    lines.append(f"| {x['n']} | {x['m']} | {x['N']} | {x['bath_gate_bound']:.9g} | {x['first_front_gate_bound']:.5g} | {x['certified']} |")
lines += ['', '## Same forcing versus actual coupled feedback','',
'The exact stage decomposition was tested on a stationary donor parameter column, including the actual difference in J between histories. Largest reconstruction residual: '+f"{max(y['identity_error'] for x in diag for y in x['blocks']):.5g}.",
'The common-field difference term can dominate the same-forcing filter term; it was not dropped. Full per-block values are in feedback_diagnostics.json.','',
'| W | H-targeted best component score | complete M at that legal query |','|---:|---:|---:|']
for x in diag:lines.append(f"| {x['W']} | {x['best_found_H']:.6g} | {x['M_at_H_query']:.6g} |")
lines += ['', 'H is a decomposition component, not a separately observable gradient block. The complete physical score remains M. The algebraic unmatched-initial constant-input example is not claimed to be reachable by a legal RNN history.','',
'## Independent-control spectra','',
'Central differences at zero control with step .01, n=16384,m=4,R=2,precharge=128; one fixed random legal one-step query. Each row of the saved matrix is the normalized full parameter response derivative for a different control. These are local singular values, not antipodal separation or dimension proofs.','',
'| W | M singular values | H singular values |','|---:|---|---|']
for x in d['jacobians']:
    lines.append(f"| {x['W']} | "+', '.join(f'{v:.3g}' for v in x['singular_M'])+' | '+', '.join(f'{v:.3g}' for v in x['singular_H'])+' |')
lines += ['', '## Explicit held-high public-bank alternative','',
'Same small n=32768,m=8,R=4,precharge=256, independent sign pair. Public cohorts are now held high between captures. This is the full-query theorem variant, not the autonomous prototype.','',
'| W | best found M |','|---:|---:|']
for x in extra['held_bank_cases']:lines.append(f"| {x['W']} | {max(q['best_M'] for q in x['queries']):.6g} |")
lines += ['', '## Matched width / donor-count / stage-count comparisons','',
'Additional runs hold precharge=256 and use the same random control rule. Compare n=32768 versus 65536 at m=8,R=4; m=8 versus 16 at n=32768,R=4; and R=4 versus 8 at n=65536,m=16.','',
'| n | m | R | W | best found M |','|---:|---:|---:|---:|---:|']
for x in scaling['cases']:
    lines.append(f"| {x['n']} | {x['m']} | {x['R']} | {x['W']} | {max(q['best_M'] for q in x['queries']):.6g} |")
lines += ['', 'For one independent W=64 control column, halving central-difference step .02 -> .01 -> .005 changes the H derivative by relative amounts '+str([x['relative_change_from_previous'] for x in scaling['finite_difference']])+'. This is a numerical conditioning check, not a dimension proof.','',
'## Interpretation and limitations','',
'Longer windows increased some found signals and local derivative singular values. No sampled query approached .002, and no jointly robust linear-dimensional section was constructed. Found small scores are not upper bounds on all legal queries. The small number of controls in the million-width cases does not test D=Theta(n).','',
'The exact source root (sigma in (.0499,.051)) and dense perturbed model were not reconstructed numerically. The inherited comparison is a separate conditional theorem input. Query search, local spectra and finite endpoint agreement cannot substitute for it.','',
'The mathematical recent-block donor code is uniform in W and does not rely on these small scores. The full autonomous public-cohort compression remains the principal open obligation.','',
'![Found query scores](query_vs_window.png)','',
'![Channel decomposition](channel_vs_window.png)','']
if d['jacobians']:lines+=['![Independent-control spectrum](independent_spectrum.png)','']
(ROOT/'EXPERIMENTS.md').write_text('\n'.join(lines),encoding='utf-8')
print('Wrote report for',len(d['cases']),'completed cases')
