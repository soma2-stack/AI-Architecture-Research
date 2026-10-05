# Multi-column spatial writes: partial positive result

Codex, 2026-10-05. THEORY ONLY. STATUS: STILL OPEN.
All NEW claims are author-derived and require independent hostile review.
The owner-verified single-block spatial-write result and D=2 are premises,
not reopened. No historical report or CURRENT_THEORY.md was edited.

## Result in plain English

Several independent parameter probes CAN share one survivor block and the
same masks. Donors need separate simultaneous controls, rather than
separate time runs or separate survivor blocks.

The price is a smaller signal for each donor group. The gain is
proportional to 1/sqrt(K), even when all K gradient coordinates are combined.
Making the shared writes sqrt(K) longer restores a fixed finite margin.
This gives one JOINT KR-dimensional ball, substantially beyond log n.
It does not solve the requested stronger no-dilution problem.

## Proven partial theorem

For n>=10^1000,

    K>=1, 2<=R<=floor(log2(n)/8), K2^R<=n^(3/16),

one continuous same-endpoint B^(KR) section has actual boundary

    pair distance>.012, half-margin>.006, epsilon=.001,
    mT<11sqrt(K)2^R n^(5/4),
    ||X||_2<7K^(1/4)2^(R/2)n^(5/8).

There are K donor groups in the SAME original donor support, one survivor
support, R shared writes and R public spatial masks, and one public reset.
The source feature, recurrent group factor, legal query box, and head
normalization are unchanged.

Explicit choices:

| Choice | Joint dimension | Coordinate-time upper | Absolute raw-input norm |
|---|---|---|---|
| R=2, K=floor(n^(3/16)/4) | >=n^(3/16)/3 | <22n^(43/32) | <10n^(43/64) |
| R=floor(log2(n)/8), K=floor(n^(3/16)/2^R) | Theta(n^(1/16)log n) | <11n^(45/32) | <7n^(45/64) |

These are growing but SUBLINEAR dimensions. The general reviewed
Omega(n log n) superlinear result at n^(3/4)(log n)^(3/2), global threshold
bracket [1/4,3/4], and full-model gap remain unchanged.

The largest K certified by this safe parameter range is approximately
n^(3/16)/4 at R=2. This is not an optimality claim. The largest allowed R
is the inherited floor(log2(n)/8), available with K of order n^(1/16).
All these choices have mT=o(n^(3/2)).

## Mechanism and the missing mathematical step supplied here

The probes are Frobenius-orthogonal rank-one recurrent actions
(Ev_k)f_s^T, all sharing the SAME source feature. Their sensitivity columns
are X_t=G_t(aO_*X_(t-1)+V). They are not independent source features or
time-dependent parameter probes.

The new comparison lemma handles ALL simultaneous idle donor controls.
A generalized common positive cone signs their genuine chronological
auxiliary response. A uniform exceptional-front estimate then transfers
the finite read gap to the complete response. The bound has no K front
penalty because aggregate weights sum to gamma, regardless of group count.

At a boundary cube point, choose one donor coordinate at +1 versus -1.
Its matched response is exact and independent of every idle donor control.
The low response is bounded uniformly over all of them. Thus this is not
coordinate-axis evidence promoted to a joint dimension.

Telescope by R stage vectors, not KR scalar controls. Each stage writes a
private parameter-space ROW VECTOR into one protected Walsh character.
Later masks cannot convert a different write into its singleton read.
Exact scalar trace corrections make all future gates independent of the
stage being flipped. This proves the full boundary antipodal margin.

## What fails for free multiplication

PROVED, scoped: with uniform donor gates, stationary zero-sum donor
contrast probes have only a local scalar trace; matching that trace
makes their final comparison exactly zero.

PROVED, scoped: for the new partitioned donors, the leading joint
K-probe survivor common read on an axis antipode has norm

    kappa/sqrt(2(K+1)).

This formula includes orthogonalization and all K coordinates.
No change of probe basis removes the loss.
The selected-probe ALL-LEGAL-QUERY upper is correspondingly
O(kappa sqrt(m)/(n sqrt(K))) after the common mask and clear,
with the stated negligible residues.

This does NOT prove a universal 1/sqrt(K) obstruction for another gate
code or moving-cycle probe family. The no-dilution version is STILL OPEN.

## Classification

| Claim | Classification |
|---|---|
| Shared K-probe, KR-dimensional finite-radius section with compensated writes | PROVED author derivation; hostile review required |
| One-probe historical spatial-write theorem | VERIFIED premise supplied by owner |
| Several orthogonal donor contrast probes with the SAME uniform controls multiply dimension | FAILED, exact quotient |
| Literal orthogonal source features multiply autonomous-source forcing | FAILED, rank-one source forcing |
| 1/sqrt(K) loss in the partitioned-donor common-write read | PROVED, scoped |
| No-dilution shared multi-probe family in general | STILL OPEN |
| D=omega(n) or exponent below 3/4 for superlinear d_F | NOT PROVED |

The Kn final-sensitivity topological ceiling is only a ceiling for
distinction witnessed through K selected parameter actions. Our actual
new construction attains KR, not Kn.

## Next hostile-review target

Attack PROOF.md sections 4--7:

1. The multi-idle chronological comparison, including its exact source sign.
2. The K-independent exceptional-front comparison.
3. Trace independence and stage-wise telescope over the ENTIRE KR boundary.
4. The physical parameter normalization and legal two-query witness.
5. Every-width envelopes at n>=10^1000.
6. The precise scope of the axis dilution upper.

After that review, the single remaining stronger lemma is whether a
different shared donor code or moving-cycle parameter-column family has
a joint minimum gain without the sqrt(K) duration price.
Do not count probes, temporal slots, or a large rank as robust dimension.

## Scope and practical limits

These are fixed-feature continuous-coordinate theory statements.
They imply no finite-bit, VRAM, practical-width, training-efficiency, or
every-RNN claim. Their enormous onset is explicit.
The full absolute raw-input history norm is counted, and one exact
common nonzero endpoint is used.
No architecture work or large experiment was done.
