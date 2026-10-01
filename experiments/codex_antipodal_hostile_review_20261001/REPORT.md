# Independent hostile review: antipodal robust dimension

Date: 2026-10-01. Reviewer: Codex. Source directory:
`experiments/antipodal_robust_dimension_20261001/`.
Source baseline commit is 545667d; Claude's new evidence is presently untracked,
not part of that commit. The frozen file hashes identify the actual reviewed content.

## Verdict

**5D JOINT ANTIPODAL CERTIFICATE VERIFIED — SURVIVES HOSTILE REVIEW.**

The claims below hold as lower bounds on epsilon-essential continuous memory
coordinates, under the stated continuous-encoder, uniform-error, late-query,
no-external-history model. They do not establish a maximum dimension, finite-byte
requirement, learning advantage, or architecture superiority.

Primary epsilon remains exactly 1/1000 in the accepted normalized gradient units.

| Endpoint / frozen candidate | r | Minimum certified beta | Guaranteed antipodal distance | Corner states |
| --- | ---: | ---: | ---: | ---: |
| Independent n4 confirmation, query_r5_s1 | 5 | 0.0013237510769157268 | >=0.0026475021538314536 | 32 |
| Independent n4 confirmation, frob_r5_s1 | 5 | 0.001105210 approximately | >=0.002210420 approximately | 32 |
| Dense n4 confirmation, frob_r4_s2 | 4 | 0.0011933704885487 | >=0.0023867409770974 | 16 |
| Dense n3 archived, query_r3_s2 | 3 | 0.0010704016399704468 | >=0.0021408032799408936 | 8 |

All bounds strictly exceed the collision threshold 2 epsilon = 0.002.
The JSON retains exact rational margins; decimal displays are explanatory only.

## What was independently checked

Read PROOF, REPORT, preregistration/config, all relevant kernel/runner/selection
code, frozen hashes, repair records, and numerical attack code/logs. No Claude
notebook was needed. No original output was edited.

1. Verified all 355 source-freeze entries, all three repair entries, and the
   repair's hash of the original freeze manifest.
2. Independently checked all 19 passing candidates at both precisions using
   rational downstream calculations: nonsingular K/K_h, hidden self-map,
   all cross-coordinate row sums, strict beta > epsilon, and exact squared
   support-aware query-margin inequalities for independent recurrence.
3. Confirmed all 288 proxy jobs are represented in the selection rule, all 66
   qualifying jobs plus the reviewed control make 67 candidates, and amplitudes
   obey the declared downward dyadic rounding.
4. Confirmed the 48 repaired records exactly match the preserved crashed IDs;
   none was certified. The repair diff contains only return-type handling,
   conditional curvature saves, provenance labeling, and its docstring.
5. Regenerated the four table candidates at 192 and 256 bits without loading
   archived endpoint-Jacobian caches. Histories, models, chart coefficients,
   amplitudes and rational preconditioners remained frozen. Every endpoint
   interval entry, output field, and full HH/HS mixed-curvature array matched
   the original exactly at each precision.
6. A full source-directory hash snapshot before/after regeneration was identical.

179 independent bookkeeping/downstream checks passed, plus eight complete
certificate regenerations and the freeze/preservation checks.

Implementation independence is bounded: this is an independent mathematical
review and fresh execution, but regeneration reuses the previously accepted
interval/curvature engine. It is not a second implementation of interval tanh
or of the RTRL jets. Agreement at two precisions alone is not the proof; the
outward arithmetic and whole-domain inequalities are the certificate.

## Attack 1: fixed-hidden-state lift

The normal half-widths really are equal. The normal box uses an unweighted
infinity norm legitimately. Hidden residual row sums are <3/4, forcing is bounded
by (1-eta_h)a_h, and rational K_h is nonsingular. Thus the contraction maps the
entire simultaneous normal box into itself for every tangent point. Its fixed
point solves H=0, not merely K_h H=0. Uniform contraction gives a unique,
continuous/Lipschitz section. Nonzero dyadic tangent errors are included through
the actual center derivative H_t and compensation terms; exact tangent
orthogonality is not assumed.

For the strongest 5D chart eta_h=0.018406259647980656; raw perturbation radius is
about 0.07658, well inside the declared +/-1 local domain. The lift covers the
whole five-dimensional tangent cube, not independent one-axis intervals.

## Attack 2: per-face argument and mixed curvature

Let Phi=A^-1 K(Psi(Az)-Psi(0)). The whole-section derivative residual is bounded
componentwise by Ehat. Integration along a cube segment yields, when
|z_i-z'_i|=2,

    |Phi_i(z)-Phi_i(z')| >= 2 - sum_k Ehat_ik |z_k-z'_k|
                             >= 2(1-sum_k Ehat_ik).

Every changing coordinate appears in the row sum. There is no cancellation
assumption and no separate-axis-to-joint inference. HH and HS cover every
normal-normal, normal-tangent, and tangent-tangent pair. The implicit section
curvature includes both the Hessian contraction with [Dy;I] and the normal
sensitivity derivative multiplied by D2y. Omitting that latter term would be a
real defect; it is present.

For the strongest 5D chart the outward rows are
0.5325761130, 0.2502520502, 0.4074175037, 0.4129886075, 0.3416937483.
All simultaneous face margins pass. The closed-boundary segment argument can
be formalized by radially moving both endpoints into the cube interior and
taking limits; the uniform derivative bound and section continuity persist.

## Attack 3: query margins and residual cancellation

The projection is an exact rational linear functional of ALL supported
normalized sensitivity coordinates. It is not conditioned on other coordinates
being zero. For independent recurrence each parameter column has a unique state
owner, giving the weighted Cauchy-Schwarz query inequality at the permitted
7/8 gate. The squared lower-margin inequality was checked rationally for every
independent passing face. Dense recurrence uses the accepted finite-frame dual,
with an exact invertible frame. W invertibility and permitted gate inclusion
are checked by the certificate engine.

Because the hidden state is exactly fixed, the same future input realizes a
given gate for both histories. The future step's direct parameter injection is
the same and cancels in the gradient difference. It is therefore legitimate to
compare Delta S through the effective adjoint family. Residual sensitivity
coordinates cannot invalidate either query lower bound.

## Attack 4: topology and the meaning of dimension

The cube-boundary parametrization v -> v/||v||_infinity is odd and continuous.
Composing any continuous history encoder with the fixed-h history section gives
a continuous map from S^(r-1) to R^k. If k<r, Borsuk-Ulam produces identical
codes at antipodal points. At least one cube coordinate then differs by exactly
2, so the certified query distance is >2epsilon. A common decoded answer for
every same late query cannot approximate both gradients within epsilon.

This proves k>=r in this computational model. Decoder continuity is unnecessary.
Finite-state corner counting is a separate valid implication. Neither 32 corner
states nor the earlier 84/90-state product count by itself proves continuous
dimension. The proof does not establish a small global upper bound or the
maximum epsilon-essential dimension.

## Attack 5: screening, repair and provenance

The preregistration explicitly follows 288 numerical development/screening jobs.
This must be described as post-screen, pre-certification freezing, not as a
fully prospective preregistered discovery procedure or an untouched confirmation
test for the new chart optimization. The endpoint called 'confirmation' retains
its historical label; it was used in this stage's proxy optimization.

This does not invalidate a deterministic existence certificate whose complete
inputs are frozen and whose inequalities are checked. It does invalidate any
attempt to interpret selection as an unbiased population success rate.

Hashes establish current content consistency, not an independently authenticated
chronology. Self-recorded timestamps cannot alone prove the claimed execution
order. The lack of a pre-run git commit and complete resource ledger should
remain disclosed. Do not retrofit either into historical records.

The bookkeeping defect is genuine but harmless to the passing certificate:
early invalid-geometry returns were dictionaries, whereas the runner expected
a tuple. The preserved crashes and repair list are consistent. All 48 now
record hidden-section inclusion failures; none was rescued through changed
geometry. Failure here is not a dimension upper bound.

## Documentation qualifications, not certificate-breaking defects

1. PROOF's statement that no global eta<1 is required is literally misleading:
   positive mu_i and beta_i>epsilon imply every row r_i<1, hence eta<1 anyway.
   The correct distinction is that no separate 3/4 sensitivity cap or exact
   product-range/self-map certificate is imposed. REPORT mostly states this
   more carefully. Correct the wording in a separate author-owned patch.
2. The numerical attack covers dense r4_s1, whereas the strongest listed
   certificate is r4_s2. Our fresh interval replay covers s2. Do not call the
   existing s1 numerical attack an attack on s2.
3. Reported adversarial minima are smallest values FOUND, not certified global
   minima. Hessian sampling near 0.998 of a bound does not prove a supremum.
4. Twelve numerically distinguishable binary coordinates do not establish twelve
   continuous robust dimensions. The REPORT's expectation that an upper bound
   near current lower bounds is false is conjectural; those grids do not prove it.
5. The argument proves epsilon-essential continuous encoding dimension, not a
   uniform bi-Lipschitz bound for every nearby pair or a hardware-register bound.

## Resources, artifacts and preservation

Fresh certificate replay: 107.96875 CPU seconds (1.79948 CPU minutes),
109.59778 seconds wall, peak working set 328843264 bytes (313.609375 MiB).
The separate 179-check process took about 0.345 wall seconds; its CPU/RAM were
not independently metered. Reading/editing overhead is not included in replay
CPU. One CPU worker; no GPU/CUDA, model server, training, witness search, or
third-order implementation. GAS-0 and Claude's evidence were untouched.

Artifacts: replay.py, replay.json, eight freshly generated curvature NPZ files,
checks.py, checks.json, runner_diff.txt, this report. replay.json preserves all
355 frozen hashes, certificate outputs, precision and comparison checks.

## Single recommended next step

Have the author freeze/commit the accepted stage-1 evidence with the wording and
provenance clarifications above. Only then consider a separately preregistered,
owner-authorized third-order certification task. This review does not implement
or authorize the proposed 6D method. Architecture design remains premature.
