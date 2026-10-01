# Post-review documentation clarifications

Date: 2026-10-01. Added by Codex under explicit owner authorization after hostile
review b7e1e45. Original PROOF.md, REPORT.md, outputs and old freezes are preserved.
These clarifications accompany those documents; none changes a bound or theorem.

## Contraction wording

Replace the interpretation of PROOF's sentence "No global contraction eta =
max_i r_i < 1 ... is required" with:

No separate sensitivity contraction cap eta < 3/4 or exact projection-product
self-map is imposed. However, mu_i>0 and beta_i=mu_i(1-r_i)>epsilon>0 imply
each r_i<1, hence max_i r_i<1 for a passing certificate. The antipodal proof avoids
the old range-shrinking/product-attainment step, not this implied inequality.

The fixed-h boundary mean-value step can be read as a limit of interior segments:
replace both cube endpoints by (1-delta) times those endpoints, apply the uniform
derivative inequality, and send delta down to zero using the Lipschitz section.

## Chronology and selection

Numerical development/screening preceded PREREGISTRATION.md. This is a
post-screen, pre-certification content freeze, not fully prospective discovery
preregistration. The historical "confirmation" endpoint label does not imply an
untouched holdout for this subsequent chart/amplitude optimization. Certificates
are deterministic existence statements, not an unbiased success-rate estimate.

FROZEN.json and REPAIR_FROZEN.json hashes establish consistency of archived
content; their self-recorded timestamps do not authenticate execution order.
The evidence is being committed after certification and review. Preserve the
original records and their stated order without inventing an earlier git freeze.
The original resource ledger is incomplete; no new estimate repairs that history.

## Numerical attack scope

Dense width-4 numerical attacks covered frob_r4_s1, while the strongest table
entry uses frob_r4_s2. The independent Codex interval replay covers s2; do not
attribute the s1 numerical attack to s2. Adversarial minima are values FOUND,
not rigorous global minima. Hessian samples do not certify whole-box suprema.

## Dimension and upper-bound scope

The theorem certifies epsilon-essential continuous encoding-coordinate lower
bounds under the continuous, no-external-history, late-query model. It does not
prove a uniform bi-Lipschitz inequality for every nearby pair or a hardware-byte
bound. Finite grid counts are separate.

REPORT's statement that an upper bound near current lower bounds is not expected
is conjectural. Twelve binary grid coordinates and numerical query slack do not
prove twelve continuous robust dimensions or disprove such an upper bound.
No useful robust-dimension upper bound has been found.

## Subsequent work

The stage-2 proxy remains numerical development. A new third-order experiment
requires its own frozen method, candidate, validity checks and official results.
No stage-1 failures, arrays, constants or recorded classifications are replaced.
