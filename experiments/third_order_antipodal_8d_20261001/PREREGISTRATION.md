# Prospective rigorous certification of the frozen 8D proxy section

Owner authorizes this experiment only. No 9D/10D, new witness, candidate tuning,
architecture, learning or GAS-0 work. CPU only; one thread. Stop after result.

## Immutable selection

Select exactly dimension_8.json's query_svd / proxy case from the completed
numerical screen at c057e4e. This is the small proxy-oriented section, NOT the
larger direct-geometry candidate. No alternative or fallback is allowed.
Use bases.npz query_svd columns 0..11, and all eight a values and ah unchanged.
Convert binary64 constants to their EXACT rational values; no amplitude
rounding, inflation, shrinking, or optimization. Preserve original rational
central history and parameters from endpoint.json. Width 4, T=37, P=24.

Same epsilon=1/1000, parameter-group RMS/input-SD normalization, support-aware
permitted scalar-head queries and continuous no-replay encoder contract.
Four last-input normal coordinates are exactly those declared in the screen.
The affine history chart has 4 normal plus 8 tangent coordinates. Fixed-h
compensation is proved by the reviewed contraction machinery, not assumed
from the numerical explicit solve. Normal half-widths are all equal to ah.

L is the binary-frozen numerical chart left inverse from the screen's unchanged
chart() formula. K_selected=identity; K_hidden is the binary-frozen inverse
of its center hidden-normal derivative. They need not be exact inverses:
outward center residuals are counted, and exact rational nonsingularity is
checked. These are pre-measurement constructions, not tunable parameters.

## Unchanged reviewed mathematics

Byte-copy rebalanced_7d_section_20261001/kernel.py, including BOTH accepted
affine tightenings, all parameter injections, all second/third mixed tensors,
implicit y''/y''' and s_y y''' terms. Hash the entire dependency chain.
Use the existing accepted PROOF.md and PROOF_AFFINE.md without amendment.
The generic r-dimensional argument applies with r=8; old engine metadata
string '6D certified' is historical wording and must not be used as a dimension.

Compute fresh interval endpoint derivatives and full whole-box majorants
independently at 192 and 256 bits. Dyadic intervals use Taylor-tail enclosure
of transcendental functions. Positive majorant arrays use elementary binary64
upward arithmetic exactly as reviewed; they do NOT have 192/256-bit tensor
precision. Final inequalities use exact rational arithmetic on these bounds.
No old generated derivative/curvature arrays may be reused.

## Gates and outcome

Local physical chart radius <=1. Exact K_hidden and K_selected invertible.
Hidden contraction eta_h<3/4; every forcing component <=(1-eta_h)*ah.
Full normal/tangent and selected mixed derivative majorants finite.
All eight beta_i=mu_i*(1-e0_i-M3_i/6)>1/1000, at BOTH precisions.
Report guaranteed antipodal query separations 2beta_i, all M3/6 penalties,
hidden limits, and exact rational 192/256 differences.

PASS means a continuous no-replay encoder needs k>=8 coordinates under the
unchanged contract. It is NOT an 8-bit bound, 256 pairwise grid states, a true
maximum dimension, a hardware bound or architecture novelty.
Any failed gate means FAIL for this frozen candidate; preserve the first
failed inequality and still regenerate at the second precision for diagnosis.
Stop on invalid source hashes, arithmetic exceptions, nonfinite tensors,
parameter mutation, hardware safety, or CPU budget exhaustion. No retuning.

## Checks, resources, records

Before official certification: synthetic interval arithmetic, tensor
contraction, exact frozen-candidate parity, preconditioner invertibility,
dimension, epsilon, CPU/device and source-preservation tests.
Freeze code/candidate/config/hash manifest, commit and push BEFORE official
results. After runs: rational inequality replay, complete tensor comparison,
candidate/source/history preservation and resource audits. Run all this
experiment's tests; do not run unrelated benchmarks.

Hard limit 1,200 measured CPU-seconds including setup/tests/checks, RAM 2 GiB.
Use one CPU worker and no GPU. Preserve partial results on failure. Store raw
certificates, all derivative-bound arrays, resource metadata, exact checks,
report and output hashes only in this new directory. Never overwrite history.
