# Robust-certificate tightness / true-dimension gap

## Classification and architecture gate

**CERTIFICATES ARE HIGHLY CONSERVATIVE — MANY MORE ROBUST DIRECTIONS APPEAR NUMERICALLY**

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
| dense | 3 | archived | 2 / 2.000 | 12 / 4096 / 12 | 5 / 2.322 |
| dense | 3 | confirmation | 2 / 2.000 | 12 / 4096 / 12 | 8 / 3.000 |
| independent | 3 | archived | 1 / 1.000 | 9 / 512 / 9 | 7 / 2.807 |
| independent | 3 | confirmation | 1 / 1.000 | 9 / 512 / 9 | 9 / 3.170 |
| dense | 4 | archived | 1 / 1.000 | 12 / 4096 / 12 | 3 / 1.585 |
| dense | 4 | confirmation | 3 / 3.000 | 12 / 4096 / 12 | 13 / 3.700 |
| independent | 4 | archived | 0 / 0.000 | 12 / 4096 / 12 | 5 / 2.322 |
| independent | 4 | confirmation | 2 / 2.585 | 12 / 4096 / 12 | 67 / 6.066 |

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
| independent_n3_archived | 2 | 7 | 2.807355 | 4.618--4.618 |
| independent_n3_confirmation | 2 | 9 | 3.169925 | 4.604--4.604 |
| independent_n4_archived | 1 | 4 | 2.000000 | 5.485--5.485 |
| independent_n4_confirmation | 6 | 84 | 6.392317 | 5.126--5.394 |

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
| dense_n3_archived | 0.874503 | 0.086260 | 1.309 | 0.008090 / 0.304237 |
| dense_n3_confirmation | 0.892298 | 0.058713 | 1.309 | 0.002420 / 0.146475 |
| independent_n3_archived | 0.988238 | 0.221223 | 4.961 | 0.035703 / 0.177453 |
| independent_n3_confirmation | 0.986970 | 0.172083 | 4.946 | 0.012175 / 0.095269 |
| dense_n4_archived | 0.866467 | 0.047530 | 1.355 | 0.008205 / 0.178656 |
| dense_n4_confirmation | 0.884638 | 0.021116 | 1.355 | 0.002414 / 0.407723 |
| independent_n4_archived | 0.980161 | 0.198700 | 5.892 | 0.060494 / 0.310652 |
| independent_n4_confirmation | 0.997921 | 0.219813 | 5.795 | 0.034101 / 0.330629 |

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
from **158.341 to 1513.542 bits**, far above these lower estimates.
**NO USEFUL UPPER BOUND FOUND.** It cannot prove the true robust core small.

The direct raw-history diagnostic uses the same 32 frozen SEARCH IDs per width
for both models, no mutations, no spectral prefilter, and the old primary proxy:

| Model | Width | Raw histories | Max proxy directions | Max proxy bits | Meets/exceeds old search winner lexicographically |
| --- | --- | ---: | ---: | ---: | ---: |
| dense | 3 | 32 | 2 | 2.000 | 0 |
| independent | 3 | 32 | 1 | 1.000 | 1 |
| dense | 4 | 32 | 3 | 3.000 | 0 |
| independent | 4 | 32 | 1 | 1.585 | 0 |

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
below1e-50 and maximum binary64/decimal distance difference **1.765e-14**.
Eight scalar higher-precision mixed-derivative checks support the curvature
measurements. These are independent numerical paths, not interval proofs of
the new large grids. All 214 prior files match
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

Measured CPU **1340.265625 seconds / 22.337760
minutes**, including failed attempts; 60 administrative seconds estimated
separately. GPU-active-phase wall UPPER bound **22.753797
minutes**, not kernel-only GPU time. Summed post-import job wall
**1377.946121 seconds**. Peak process RAM
**1257.434 MiB**, global VRAM
**2005.000 MiB** including existing contexts,
our allocator pool **471.291 MiB** excluding
driver/library overhead, GPU temperature **50 C**.
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
