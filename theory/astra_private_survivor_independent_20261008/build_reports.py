"""Render archived measurements and fair-comparison tables."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'independent_results.json').read_text())
c=json.loads((ROOT/'comparison_results.json').read_text())
p=json.loads((ROOT/'product_matched_results.json').read_text())
best=lambda x:max(x['queries'],key=lambda q:q['best_M'])
lines=['# Independent private-survivor experiments','',
'PENDING REVIEW. Frozen reference model, NumPy float64 CPU. No robust continuous section is certified.','',
'## Independent phase','',
'All cases below were completed and saved at commit 185320f before competitor inspection. Seed 812, actual complete J/B, two query starts and one vertex update, horizons 1,2,4,8. The first future gate is optimized; other future gates are high. Source scale .05 is a proxy for the inherited fixed source root. Full dense perturbation is not numerically reconstructed.','',
'| n | m | R | W | protocol | controls | N | best M | L at selected query | H at selected query |','|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|']
for x in d['cases']:
    q=best(x);lines.append(f"| {x['n']} | {x['m']} | {x['R']} | {x['W']} | {x['mode']}{' + private donors' if x['coupled'] else ''} | {x['private_controls']} | {x['N']} | {q['best_M']:.6g} | {q['L_at_best_M']:.6g} | {q['H_at_best_M']:.6g} |")
lines+=['','Small widths satisfy basic no-wrap, not the stronger inherited large-n geometry. Weak echo has larger contrast at these small R; raw improvement cannot be attributed solely to retention. Post-comparison tests match contrast explicitly.','',
f"Maximum independent endpoint error: {max(x['endpoint_error'] for x in d['cases']):.5g}; echo-product error: {max(x['echo_product_error'] for x in d['cases']):.5g}; donor live-trace error: {max(x['maxtrace'] for x in d['cases']):.5g}; measured inverse-lift input: {max(x['maxinput'] for x in d['cases']):.6g}.",
'Survivor TRACE neutrality is not asserted. Survivor PRODUCT neutrality is intentional. The final reset gives the common hidden endpoint.','',
'## Full cost','',
'For each case independent_results.json stores N, mN, mN/n^(3/2), actual driven reference input squares over every precharge/holding/write/reset step. Add initial selected-memory preparation 6m[.05^2+atanh(sqrt(1-g_H))^2], plus the inherited source preparation. No public input center is subtracted. These are reference selected-memory measurements, not a certified dense full-lift energy. Asymptotic cost is proved by schedule counting in RESEARCH.md, not inferred from finite ratios.','',
'## Independent directions','',
'Eight survivor coordinates were separately differentiated at zero (central difference .01) for each protocol, n=16384,m=4,R=2,W=16. Saved NPZ matrices contain complete parameter-coordinate derivatives.','',
'| protocol | full M singular values | H singular values |','|---|---|---|']
for x in d['spectra']:lines.append('| '+x['mode']+' | '+', '.join(f'{v:.3g}' for v in x['singular_M'])+' | '+', '.join(f'{v:.3g}' for v in x['singular_H'])+' |')
lines+=['','| protocol | unit antipodal direction | best found complete M after query search |','|---|---|---:|']
for x in d['spectra']:
    for y in x['unit_antipodes']:lines.append(f"| {x['mode']} | {y['direction']} | {best(y)['best_M']:.6g} |")
lines+=['','A weak singular vector of one fixed query is not necessarily weak for every legal query. These finite antipodal probes do not certify the minimum over a sphere, and small found scores do not upper-bound the query supremum.','',
'## Regression and identity checks','', '```json',json.dumps(d['validation'],indent=2),'```','',
'See math_validation.json for the recent-block aggregate identity, monotone local-code example, and exact shared endpoints across normalized competing protocols.','',
'## Reproduce','', '```powershell', '$env:OPENBLAS_NUM_THREADS="1"',
'python theory/astra_private_survivor_independent_20261008/run_independent.py',
'python theory/astra_private_survivor_independent_20261008/compare.py',
'python theory/astra_private_survivor_independent_20261008/product_matched.py',
'python theory/astra_private_survivor_independent_20261008/test_math.py',
'python theory/astra_private_survivor_independent_20261008/build_reports.py','```','',
'Runners resume completed JSON cases. For a fresh reproduction, use a separate copy without generated result files. Do not overwrite the archival evidence. The pinned competitor snapshot is unmodified; compare.py applies exactly two documented public preparation/reset changes in memory.']
(ROOT/'EXPERIMENTS.md').write_text('\n'.join(lines),encoding='utf-8')

lines=['# GPT-6 versus Astra: matched private-survivor comparison','',
'**Overall winner: INCONCLUSIVE.** GPT-6 wins several tested scalar M-score comparisons; neither proves robust linear memory. No main-theorem victory is claimed.','',
'## Independence and provenance','',
'Astra checkpoint 185320f predates all competitor inspection. GPT-6 source is pinned to f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c and copied byte-for-byte as competitor_snapshot.py; COMPETITOR_PROVENANCE.json records its SHA-256. No historical competitor file is edited.','',
'## Fairness controls','',
'All paired comparisons use identical n,m,R,W, precharge L, source normalization .05, complete frozen reference O, seed 812, and query budget (two starts, one update; horizons 1,2,4,8 at small widths, horizon 1 at million width). Donor private words are zero.','',
'GPT-6 originally starts survivor rows at the ordinary bath and resets them high; Astra prepares paired survivors high and resets to gate 1-tanh(.05)^2. compare.py explicitly harmonizes just these TWO PUBLIC operations in memory. With these edits all compared protocols share the same reference initial state and final hidden endpoint. Verbatim competitor replays are also included and show the size of that adjustment.','',
'Architectures still differ in pulse locations, baseline attenuation and total variable-gate exposure. These are exposed rather than silently credited as storage advantages. GPT capture uses only the Walsh-low half: active controls are mR/2, not the nominal mR array size. Astra active_half ties the other half to zero for a control-count comparison.','',
'GPT interior_independent has mR(W-1) controls. interior_tied repeats one control throughout each window and has mR controls. interior_equal_dose additionally scales the control by min(1,4/(W-1)), matching approximately the echo\'s two-pulse variable half-excursion sum. This is not a guarantee of identical energy or identical transfer operators.','',
'Astra weak_equal_contrast sets its log contrast to make the boundary gate derivative approximately 1e-4; this removes the principal small-R contrast advantage of default weak echo. That finite matching setting is NOT asserted legal for arbitrarily large R.','',
'## Results','',
'| n | m | R | W | variant | raw GPT | controls | variable excursion/site/stage | best M | L | H |','|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---:|']
for x in c['cases']:
    q=best(x);lines.append(f"| {x['n']} | {x['m']} | {x['R']} | {x['W']} | {x['variant']} | {x['raw_competitor']} | {x['active_private_controls']} | {x['variable_gate_half_excursion_sum_per_stage_site']:.6g} | {q['best_M']:.6g} | {q['L_at_best_M']:.6g} | {q['H_at_best_M']:.6g} |")
lines+=['','All values are FOUND scores, not suprema. Large H is not a separate legal readout; complete M remains the criterion. Million-width cases satisfy the stronger geometry, but exact source-root/dense lifting remain separate inherited assumptions. No million-width spectrum or linear-size control bank is claimed.','',
'## Product-matched interior falsifier (post-comparison invention)','',
'Use z=(u,0,-reverse(u)), making opposite words have exactly equal interior gate products. This removes the old local precharge difference while retaining full coupled feedback. Controls number mR(W-2)/2; endpoints still match. Different control subspaces prevent treating this as a pure causal ablation of every other effect.','',
'| n | m | R | W | controls | product error | best M | L | H |','|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for x in p:
    q=best(x);lines.append(f"| {x['n']} | {x['m']} | {x['R']} | {x['W']} | {x['controls']} | {x['product_error']:.3g} | {q['best_M']:.6g} | {q['L_at_best_M']:.6g} | {q['H_at_best_M']:.6g} |")
lines+=['','## Verdict by criterion','',
'| Criterion | Defensible conclusion |','|---|---|',
'| Mathematical rigor | Astra supplies a full fixed-gap echo code and a new arbitrary-word local monotone code; GPT supplies a private-capture code. The full-code scopes differ; both depend on inherited premises and need hostile review. |',
'| Certified robust dimension | Neither proves a jointly readable linear section. Tie at the unresolved target. |',
'| Found complete signal | GPT interior and capture variants exceed the corresponding tested echo scores, including some control-count/dose-matched cases. Numerical advantage only. |',
'| Efficiency | N and mN are matched within comparison rows; extra controls, pulse exposure and preparation/reset are explicitly recorded. No efficiency advantage for certified memory is established. |',
'| Scalability | Both have scoped obstructions and remaining near-critical/interior cases. Finite scores do not establish asymptotic capacity. |',
'| Validity | Both use the exact reference operator and complete feedback; neither independently certifies the dense source/lift or all-query optimization numerically. |','',
'The most useful scientific development is separating low-dimensional local-product effects from the unresolved H channel. Astra does not claim to win because it introduced stronger controls, and GPT is not declared to solve memory because one pair score is larger.','',
'Next: a complete H approximate-width theorem or robust counterexample after matching the local survival code, beginning with weak echo.']
(ROOT/'COMPARISON.md').write_text('\n'.join(lines),encoding='utf-8')
print('Reports generated:',len(d['cases']),'independent,',len(c['cases']),'comparison,',len(p),'product-matched cases')
