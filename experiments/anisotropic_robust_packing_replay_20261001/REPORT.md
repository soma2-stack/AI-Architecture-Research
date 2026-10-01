# Independent clean replay: width-3 two-axis certificate

## Classification

**CLEAN REPLAY VERIFIED — TWO-AXIS CERTIFICATE REPRODUCED**

Source commit: `1e4bf42dfa9f1a312d23b4a752738280d5861a4b`. Freeze commit `8622551`;
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
`04f137b6e4f45c9d4f18cde40accf8e40c4834832f66cf9b4b799d7c1a8b1dab`.

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
| Hidden contraction eta_h | 0.060253012714867084 | same |
| Joint projection contraction eta | 0.30423690175351176 | same |
| rho_1 | 0.0089366976729561912 | original target verified |
| rho_2 | 0.0071572743166914872 | original target verified |
| mu_1 | 0.18442301115874959 | original lower margin verified |
| mu_2 | 0.18515681028226835 | original lower margin verified |
| mu_1 rho_1 | 0.0016481326946619715 | same frozen value |
| mu_2 rho_2 | 0.0013252180827937976 | same frozen value |
| N_1, N_2 | 2, 2 | 2, 2 |
| Distinguishable states / bits | 4 / 2 | 4 / 2 |

Every displayed number is a rounded view; all decisions use exact rationals
and outward interval enclosures in the stored JSON. At 192 bits all 17
compared fields, including curvature tables, K matrices, projections, radii,
margins and packing arithmetic, are exactly equal to the archived result.

At 256 bits the query-margin enclosures tighten upward by approximately
1.1e-58, 1.17e-58. This expected precision-dependent refinement
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
[[0.058142017507301476, 0.05864907617587782], [0.05864907617587779, 0.061569637643521524]]
axis/output 2:
[[0.05407161431561628, 0.055107347885724745], [0.05510734788572471, 0.058267803503032206]]
```

The Frobenius fixed-section mixed upper table is:

```
[[0.07849794684699765, 0.07324251992749369], [0.07324251992749364, 0.07233238828172664]]
```

The hidden residual majorant is:

```
[[0.023510842988811766, 0.015494533752837825, 0.010683311888244833], [0.014739004940587493, 0.02322845898378914, 0.005424399585293384], [0.01943234135013652, 0.017018630436860117, 0.023802040927870426]]
```

The joint selected residual majorant is:

```
[[0.12786644348759282, 0.1316191063202043], [0.14925030439103798, 0.15498659736247372]]
```

Both contractions are below one. Hidden self-map slacks are
[0.11587522728103407, 0.1157863789599682, 0.11601047231488812]; target self-map slacks are [0.008697038728081103, 0.008697038728081103]. Exact nonzero determinants
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

Measured CPU: **29.156250 seconds / 0.485938 minutes**, including the
failed and successful tests. Sum of post-import job wall times:
12.093122 seconds; whole research/documentation wall time was not metered.
Peak process RAM: **284.191406 MiB**. One CPU/BLAS worker.
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
| frozen_sources\engine.py | fce5400b587b7efc49be735bceb4a3291fe1b3a8254a1105be66597189511a2a |
| frozen_sources\interval.py | 34ac4a8aacd2eae3c5890c32030e0e568096058320acb1e5dacae2f7024b7f8c |
| frozen_sources\test_engine.py | 4a4b3f042f91f8915dcfefed6294787cec5500277df86ce6f54061f368a6cd8d |
| frozen_sources\config.json | 1650770817920c00fc155ac1aec3bdcf5195fde9a1a6484ea9eb35dd67fd7c39 |
| frozen_sources\PROOF.md | b2a3b227ed61585770c5d2119779d09cc6f4f9b1416c790f1a600666d0d6f4bf |
| frozen_sources\basis_dense_n3.json | b047e2a6ab386854badb45a07f82fe6f44ea9802cfe0658c1287755e8b29f97b |
| frozen_sources\certificate_frame_dense_n3.json | 5199bb8c40ccc6616340e3f0dbb0faadbc9433b1406fac5e04e470d429334cca |
| frozen_sources\certificate_dense_n3_9602100_full.json | 805c15717cab9195ae6631e8b696e91aca0ab6c8054e8f58b0a881504e4a9cf1 |
| frozen_sources\width_core.py | 2cd3e06abd5dd72e2b0e20d485993df2aaee6547d82d482c4df96b1816ce9e70 |

All original files passed byte-hash preservation checks. Runtime implementation
hashes and artifact hashes are in `output_manifest.json`.

## Single recommended next step

Owner review of this clean replay and the three documentation-only proof
clarifications. Stop here; no further experiment or architecture work is
authorized by this replay result.
