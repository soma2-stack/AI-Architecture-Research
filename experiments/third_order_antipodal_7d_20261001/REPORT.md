# 7D third-order antipodal result: FAIL

The prospectively selected 7D candidate fails the accepted sufficient certificate
at both 192 and 256 bits. The previous independently reviewed 6D lower bound
remains accepted. **This is not a proof that 7D is impossible at this endpoint.**

## Unchanged contract and prospective chronology

Only independent width-4 confirmation, horizon 37, P=24. Original endpoint,
parameters, fixed-h requirement, normalized gradient metric, support-aware
query family, continuous encoding model and epsilon=1/1000 are unchanged.
Accepted third-order kernel SHA-256:
`c2483d3585dccb36b7dfba945c1a0cb2964a59f440161a7663c594bd4d928578`.
No old kernel, proof, output, history or model was modified.

Method/rules/bases freeze **fde381a** was committed and pushed before numerical
selection. Four predeclared runs (two fixed bases, two seeds) performed 2,024
proxy evaluations; 14 were numerically invalid and preserved in JSONL traces.
Top basis best score 0.7989734252692997; skip-leading-mode best score
0.5654352753940441. Original archived r7 scores were disclosed development
baselines, not fresh holdouts. No witness search occurred.

One winner, top_271071, was selected by the frozen rule even though its proxy
score was below 1. Tangent amplitudes were rounded down to dyadic 2^-20;
equal normal amplitude was padded by 51/50 and rounded up. Fixed rational
preconditioners came from the fresh interval center. Candidate freeze
**50af2c9** was committed and pushed before official whole-box certification.
Candidate SHA-256:
`4d6ca2c2804790b55f24f4125471f322ca1f324252b3a1a173ef5bb3e2bf8c9c`.
No replacement, new amplitude, basis, epsilon or post-failure optimization.

## Hidden section succeeds

eta_h = 0.05159680737473471 < 0.75.
Equal normal half-width = 0.007782936096191406.
Hidden self-mapping allowance = 0.007381361441626349.
Maximum forcing bound = 0.0065894534486663145, below that allowance.
Maximum raw-history displacement bound = 0.062177891628609115 < 1.
Both frozen rational preconditioners are nonsingular, checked by exact inverse.
The exact fixed-h lift is therefore not the failed inequality.

## Exact failed face inequalities

The accepted test is beta_i = mu_i(1-center_row_i-M3_i/6) > epsilon.
Numbers below are decimal displays of archived exact-rational lower margins;
center residuals are included in the linear column, not dropped in certification.

| Face | Linear/query margin, no cubic penalty | Cubic penalty | Certified beta | beta-epsilon |
|---|---:|---:|---:|---:|
| 1 | 0.00210633341631 | 0.00130413920184 | 0.000802194214463 | -0.000197805785537 |
| 2 | 0.000925499564981 | 0.000125972755227 | 0.000799526809755 | -0.000200473190245 |
| 3 | 0.00119180043061 | 0.000392740668564 | 0.000799059762045 | -0.000200940237955 |
| 4 | 0.00116080687546 | 0.000361574893007 | 0.000799231982450 | -0.000200768017550 |
| 5 | 0.00108532191478 | 0.000286441214678 | **0.000798880700105** | **-0.000201119299895** |
| 6 | 0.00114639874693 | 0.000346779249766 | 0.000799619497168 | -0.000200380502832 |
| 7 | 0.00102090998063 | 0.000221995898867 | 0.000798914081766 | -0.000201085918234 |

The first failed inequality in face order is face 1. The weakest is face 5,
not face 7. All seven sufficient inequalities fail. The weakest certified
antipodal query-distance bound is 0.001597761400209132, below 2epsilon=0.002.

## Exact bottleneck and its limits

The failure is a **joint amplitude/query-range versus third-order-majorant
tradeoff**, not loss of the fixed-h section, interval precision, an isolated
seventh singular direction, or a discovered mathematical gap in the method.

- Face 2's certified linear range already lies below epsilon. Even deleting
  its cubic penalty cannot pass this frozen face. Tightening only remainder
  bounds on this box cannot establish all seven inequalities.
- The other six linear margins exceed epsilon but cubic penalties consume
  their slack. Face 7 has only 0.00002090998063224 linear slack, versus a
  0.00022199589886667 penalty. Its cubic majorant would have to drop by more
  than about 90.58% at unchanged amplitudes/margin to pass that face alone.
- For the weakest face 5, M3=1.5835368886032835, consisting of direct S'''
  1.1796601057953018, mixed S''/y'' 0.13533959621290662, and implicit S_y y'''
  0.2685371865950741. Fractions are about 74.50%, 8.55%, 16.96%.
- Face 7 has a larger implicit-compensation fraction: about 37.29%, versus
  56.57% direct and 6.14% mixed. Full mixed majorants were retained.

These are positive upper-majorant components, not measured actual curvature.
Nor is a failing query lower margin an upper bound on actual query separation.
The bounded numerical optimizer need not have found the best possible 7D box.
See DIAGNOSTIC_NOTES.md for a preserved diagnostic field-name clarification.

Selected query-weighted tangent singular values:
0.24124861288636146, 0.09852681260838499, 0.06317358152769108,
0.059719010610247876, 0.01614444651131574, 0.014552587774600063,
0.012199612159703069. They alone do not establish robustness.

## 192/256 agreement and tests

Both precisions regenerated the entire certificate from frozen input/model,
without reusing generated bounds. All eight saved mixed/implicit derivative
arrays (HH, HH3, HS, HS3, y2, y3, fixed3, selected3) are identical across
precisions. Maximum difference of exact beta lower bounds is
7.425926225072048e-57. Every face has the same FAIL decision.

12 pre-freeze development tests passed, including the accepted kernel's eight
tests. 40 independent exact downstream/consistency checks and 14 final frozen
input/rounding/full-array checks passed. All original antipodal archive hashes,
accepted 6D working artifacts and source hashes remain unchanged. The sole
pre-freeze setup failure (standard-library module shadowing) is recorded in
DEVELOPMENT_REPAIRS.md; no scientific rule was changed.

## 8D plausibility: numerical only

Before the official 7D run, the four predeclared 8D scale probes were completed.
At scale 0.5 the proxy hidden section was valid, but minimum beta/epsilon was
0.4033643723458844. Scales 0.75, 1 and 1.25 failed numerical hidden inclusion.
Thus this restricted diagnostic does not support 8D with the current recipe.
It does not establish impossibility. No 8D optimization or certification ran,
and these scores were not used to change 7D selection.

## Resources and files

Measured CPU: **446.921875 seconds = 7.448698 CPU-minutes**, summing development,
basis setup, all four search processes, parent overhead, selection, official
192/256 runs and final checks/summary. Separate small failed-startup/administrative
allowance: 5 CPU seconds. Both remain below the preregistered 40-minute cap.
Summed phase wall time before the last summary/audit was 267.7825 seconds;
including their short execution, about 4.6 minutes of computation wall time,
excluding Git/documentation/waiting between phases.
Largest measured process working-set peak: **330.53125 MiB**.
Conservative concurrent parent plus two largest worker-peak sum: about
980.79 MiB (an upper accounting sum, not a sampled simultaneous peak).
At most two single-thread CPU workers. Torch CPU build, CUDA disabled,
**GPU time 0, GPU/CUDA unused**. No GAS-0 or model server operation.

PREREGISTRATION.md/config.json/METHOD_FROZEN.json: prospective rules and hashes.
bases.json/candidate.json/CANDIDATE_FROZEN.json: actual fixed rational inputs.
trace_*.jsonl/search_*.json/search_summary.json: all numerical selection evidence.
result.json/bounds_192.npz/bounds_256.npz: regenerated official evidence.
remainder_decomposition_*.json/diagnostics.json: failure decomposition.
tests.json/checks.json/final_audit.json: validations.
8d_numerical_diagnostic.json: the four pre-official numerical probes.

## Stop and next step

**FAIL: no new 7D lower certificate. Accepted 6D remains the strongest result
for this endpoint.** No architecture, width 5, learning, Stage C or AMS work.
Strongest uncertainty: how much of the failure is true finite-radius geometry
versus sufficient-majorant and chosen-face conservatism.

Single recommendation: separately preregister a direct high-precision antipodal
separation audit of this frozen 7D section before attempting 8D. Do not infer
a dimension ceiling from the present failed sufficient certificate.
