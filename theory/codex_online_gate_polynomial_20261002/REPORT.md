# Online query-width of the intermediate mixed polynomial

2026-10-02. **FINITE-ERROR QUESTION STILL OPEN.** New analytic results require
independent review. The accepted earlier results and their evidence are intact.

## Answers to the owner's eight questions

1. **Smallest explicit exact online recurrence obtained:** a switched affine
   triangular cascade of degree-1 through degree-p coefficient matrices.
   Degree 0 and the forcing Q_t are public. Equation (6) in PROOF.md gives
   the complete update, including the tied injection. Its explicit store is
   p r^2 credit coordinates, rather than (p+1)r^2. This is not claimed globally
   minimal. A single Horner value lacks the highest-order boundary term (9).
2. **Best counted finite-error upper:** r^2=(floor(n/2)-1)^2 endpoint credit
   coordinates using the exact reference recursion M<-G(aO_*M+I), plus n
   forward hidden coordinates while inputs arrive. Its output differs from
   the truncated polynomial by <=epsilon/4, uniformly over every admitted
   word and actual permitted query. Public weights/schedule and temporary
   arithmetic/output storage are uncounted; no history tape or free basis.
3. **O(n) approximate realization proved?** No.
4. **Strongest robust lower:** the accepted joint floor(n/8) section persists
   after truncation. Its polynomial half-margin is >.00149, versus the
   requested encoder error .00075 and buffered lower threshold .00125.
   The actual accepted half-margin remains >.00174; it was not re-certified.
5. **omega(n) robust lower proved?** No. The new Omega(n log n) statement is
   an EXACT-realization obstruction for the artificial polynomial and is
   explicitly not a finite-error credit-memory lower.
6. **Fixed-feature Theta(n)?** Still open, neither established nor refuted.
7. **Smallest remaining theorem:** finite-error continuous causal realization
   of the explicit triangular system in the future-suffix query metric (19),
   using C n counted coordinates and terminal error <=3epsilon/4 on every
   diagonal word. The nonexpansive lemma (20) gives a rigorous sufficient
   construction route (21). Exact realization has an obstruction; the
   finite-error quotient has no established size bound.
8. **Full-model consequence:** none closes the gap. Fixed-feature bounds
   stay Omega(n)--O(n^2); full bounds stay Omega_c(n^2)--O_c(n^2 log n).
   Compatible simultaneous feature summaries would still be needed.

## Strongest new theorem: exact realization can be misleading

Theorem E proves a counted lower m p, m=floor((k-d)/2), for EXACT online
reproduction of the chosen polynomial. It uses the actual paired stationary
channels of the accepted rotation, not an ambient matrix ball:

- p independently perturbed chronological gates on each channel generate
  an open p-dimensional scalar coefficient family. The exact Jacobian
  determinant is n^(-p)(a Delta/(2n))^[p(p-1)/2], before a public baseline
  step that multiplies it by b^p.
- That public step fixes the current actual h across all prefixes.
- A common admitted remaining suffix separates every nonzero coefficient
  difference; a legal one-step query with the original head observes it.
- Continuous exact state must distinguish that open m p family.
- The frozen p_n is Theta(log n), giving an exact Omega(n log n) obstruction.

This does NOT count monomials as robust dimensions, and it does NOT declare
the determinant well-conditioned. The positive determinant and the suffix
signal can be exceptionally small.

Theorem F then directly kills this particular route to a robust lower:
ALL such short prefixes, even arbitrary first-p gate words, lie within
less than .000113<epsilon/8 of the public zero mixed state under EVERY
remaining admitted gate suffix and legal future query. This is a finite-error
query bound, not an SVD/RMS proxy. The polynomial's exact extra coordinates
are dispensable at the prescribed error scale at that prefix cut.

The scalar projected-output subsystem can also be approximated with ordinary
scalar traces. This observation is restricted to those outputs; it does not
solve the complement or arbitrary gate words of the entire operator.

## What the new online metric changes

The relevant state distance is not only the current terminal gradient
distance. It must cover every remaining admitted gate suffix BEFORE the reset,
and then every legal future loss query AFTER the reset. Equation (19) makes
both roles explicit without changing the future preactivation contract.

The metric is nonexpansive under a common next admitted gate. An explicit
degree/age weighting (22) bounds each coefficient's future-query influence.
This supplies a precise finite-error realization problem; it does not show
that every continually injected mixed component fits in a small quotient.

## Representation attempts and limits

- Public degree 0 is removed from the counted cascade.
- Horner summation fails to close exactly because of its top-order boundary.
- Exact companion/Hankel-style minimization cannot prove the desired O(n)
  exact collapse: Theorem E rules that out for the frozen growing degree.
  It does not rule out approximate realizations, as Theorem F demonstrates.
- Public Krylov/rotation powers are not a common closed invariant space under
  arbitrary D O_* forcing. No uniform query-norm closure is established.
- Shared factors, displacement, quasiseparable or tensor forms need bounded
  counted adaptive cores AND online updates. No such bound was proved.
- Separate visible axes, coefficient counts and exact rank do not establish
  any superlinear joint robust section. No such claim is made.

**The exact bottleneck:** construct or refute a finite-error causal quotient
of (6) in (19), with all degrees, coupled forcing and fresh injections retained.
Theorem F resolves only the negligible short prefix; it does not eliminate
the later history-dependent forcing.

## Evidence and resources

Rigorous analytic derivations: PROOF.md, with manual audit in CHECKS.md.
Supporting exact-rational arithmetic: arithmetic.py and ARITHMETIC.json,
verifying the elementary log brackets and strict .000113/epsilon/8 ledger.
Those scalar calculations are not a neural experiment or dimension screen.
No numerical evidence or conjectural asymptotic fit is used as a theorem.
No automated implementation test suite was added or run.

No GPU/CUDA, training, model server, benchmark, new witness, sustained chart,
architecture or other contraction regime was used. GAS-0 files/runtime and
other lanes' evidence were not modified. Exact arithmetic CPU/wall and peak
process RAM are recorded in ARITHMETIC.json; file/Git administration is
unprofiled. PROVENANCE.json records source hashes and the verified checkpoint.

Automatic approval review rejected the proposed shared-map update because
the new lemmas have not received independent review. SHARED_RESEARCH_MAP.md
was left unchanged; this isolated record and the Codex resume contain the
new, explicitly unreviewed derivations. Historical evidence was not rewritten.

## Single recommended next theorem

Prove or refute a C n-dimensional FINITE-ERROR causal simulation of (6) under
the explicit all-suffix metric (19). A concrete sufficient approach is a
continuous lifted approximation satisfying (21) with a total error budget
<=3epsilon/4. Do not use an exact-realization/Hankel lower as a substitute for
a joint robust antipodal section. Stop this stage; no new research begins here.
