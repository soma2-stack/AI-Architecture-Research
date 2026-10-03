# Joint harmonic lower section: new proof, independent review required

Codex, 2026-10-02. Bounded takeover of Claude's unfinished harmonic sketch.
No architecture, training, new contraction regime or generic compressor.
Claude/Grok files and all historical evidence are preserved.

## Outcome

**A conservative omega(n) robust lower is derived:**

    d_fixed-feature >= floor(d/1,000,000) floor(n^(1/18))
                    >= n^(19/18)/20,000,000,

for n>=10^504, c=1, epsilon=.001, under the unchanged normalized legal-query
and continuous-encoding contract. This refutes a universal O(n) encoder if
the new proof survives independent review. It does NOT establish Claude's
proposed n^(7/6) exponent or a moderate-width improvement.

The new proof is internally checked, not an independently accepted checkpoint.
The accepted historical floor(n/8) lower remains preserved in its original files.

## Requested answers

1. **Construction.** Use d=floor(n/4) cycle nodes and harmonics 1,...,F,
   F=floor(n^(1/18)). Each harmonic has q=floor(d/1,000,000) parameters.
   A fixed public Gaussian/net existence construction gives a spreading matrix
   B with image orthogonal to the constant and all selected Fourier modes.
   One y=(y_1,...,y_F) ranges over the CLOSED unit ball in R^(qF).
   Profiles are

       s_f=P_perp tanh(16sqrt(dF) B y_f)/(4F).

   The co-moving physical gate word is

       D_t(i)=delta/F sum_f s_f((i+N-t) mod d) cos(2pi f(N-t)/d)

   for physical i=1,...,d-1, with zero defects elsewhere. Its entire ball is
   admitted; preparation is public and the unchanged reset gives h=0.
2. **Degree-one signal.** For one harmonic with a profile of L1>=rho d,
   after explicit node/twist corrections,

       signal_f >=rho delta sqrt(n)/(200000 f)-delta.

   For sqrt(n)>=400000f/rho this gives
   `signal_f >=rho delta sqrt(n)/(400000 f)` in the ACTUAL legal-query norm.
   Joint cross-talk is treated by a damped cosine Gram kernel, not assumed
   negligible: its real quadratic form has a lower bound n/40.
3. **Joint section.** The ball-to-history map is continuous and injective.
   Tanh is odd; projection preserves oddness and restores the exact zero
   Fourier moments needed by the twist estimate. The proof addresses every
   UNIT-BOUNDARY antipodal direction, not separately visible axes. Interior
   points arbitrarily close to the center are not asserted epsilon-separated.
4. **Dimension.** qF=Omega(n^(19/18)). This is a Borsuk-Ulam continuous-credit
   memory lower, not a tangent rank, monomial count, bit count or global
   bi-Lipschitz endpoint chart.
5. **Amplitude.** delta=10^(-10)/F^3 is the full gate-defect bound; each
   harmonic receives delta/F before the profile coefficient. Epsilon does
   not change. All nonlinear corrections are paid at this same amplitude.
6. **Threshold.** A deliberately sufficient n0=10^504. The proof is an
   arbitrary-width analytic/existence argument beyond this threshold; no
   execution at that width is claimed. All required floor/projection/cycle
   inequalities are explicit in PROOF.md.
7. **Complete ledger.** For EVERY boundary antipode pair the conservative
   half-margin is

       H_n >=10^(-17)delta sqrt(n)/F^5
                   -delta-delta^3 sqrt(n)-epsilon/4-2*10^(-9).

   The delta loss includes virtual node0, rank-two/twist and final physical
   dressing. The delta^3 sqrt(n) bound covers degree3 and all higher odd,
   cross-harmonic and chronological noncommuting corrections. Even orders
   cancel exactly. Finite-window/early-Q effects are explicitly in the
   harmonic kernel. Reset constants cancel and its a^2/O^2 factors are
   retained. The original dense/polynomial ledger and a conservative extra
   actual-R query perturbation are charged separately. No source or query
   normalization change is hidden.
8. **Final half-margin.** H_n>9 for all n>=n0. This is much greater than
   epsilon and the buffered 5epsilon/4 polynomial threshold. It is a crude
   sufficient mathematical bound, not a production tolerance claim.
9. **omega(n).** Yes in the new derivation, pending independent hostile
   review. This is stronger than the unchanged historical rigorous checkpoint.
10. **Universal O(n).** Refuted by the new theorem under the stated continuous
    no-replay memory model if the proof is accepted: qF/n diverges. The lower
    applies at terminal time, so no special causal update can evade it.
11. **Failed lemma.** No failure was found in the final revised derivation.
    Several steps of the ORIGINAL sketch were not valid as stated and have
    been replaced, as listed below. The n^(7/6) sketch itself is not certified.

## What was repaired in taking over the sketch

- The undressed physical cosine in Claude's numerical script is not an exact
  eigenvector. The proof uses the exact Householder-dressed complex Fourier
  vector, with real/imaginary unit-norm parameter projections.
- Coordinatewise saturation does not preserve Fourier orthogonality. We
  project AFTER saturation and divide by the explicit infinity-operator
  bound 4F. The resulting F^2 spreading loss is included, not ignored.
- Individual cross-talk estimates do not certify a joint section. The exact
  finite-window kernel has an n/40 joint singular lower on real profile
  coefficients, obtained from a cosine Gram bound.
- q_n^2 is not a uniform relative correction to every harmonic signal. We
  bound the entire odd tail absolutely in the permitted query norm and
  reduce delta with F. The exponent is deliberately weakened accordingly.
- A large Frobenius norm is not used as query visibility. The algebra first
  identifies one physical harmonic column with large L1, then constructs
  an actual one-step gate/preactivation query with the fixed scalar head.

## Section geometry and radius caveat

Every gate word lies inside the original intermediate box and has the
accepted coupled tanh lift. The initial state is fixed and all endpoints
are exactly h=0. A finite physical history radius is

    ||X(y)-X(0)||2 <8delta sqrt(n log n).

It grows with width; a WIDTH-UNIFORM Euclidean history radius has not been
proved and is not part of this theorem. Individual raw inputs remain inside
the fixed accepted past cube. The proof is for the stated all-admitted-history
contract, not a newly restricted uniformly bounded-history-energy model.

The explicit witness word is period-d in age, with d growing with n. This
does not contradict fixed-period results with width-independent period.
The general admitted-word contract includes this subset; the proof does
not claim that the constructed word is genuinely aperiodic.

## Independent internal checks

checks.py was written separately, with no Claude imports or output reuse.
It independently compares direct degree-one recurrence against the exact
finite harmonic kernel at n=200 and400, and checks eigenvector dressing,
node/twist bounds, physical query duality, odd-order parity/tails and gate
admission. Delta=.03 in those checks makes identities measurable; those
diagnostic values are NOT the proof's chosen amplitude or a robust lower
at these small widths. The checker also verifies final constants and the
n0 margin using exact rational arithmetic.

- Exact kernel identity discrepancy: <=1.88e-17.
- Dressed eigenvector discrepancy: <=1.99e-16.
- Kernel symmetric-part minimum: 86.589 and173.372, versus floors5 and10.
- Odd remainder after degree5: <=1.23e-13; safe degree7 bounds are >4e-9.
- All checks passed on two clean runs. Both outputs are retained.

The asymptotic theorem is established by the written inequalities, not by
small-width numerics. No numerical rank or RMS query surrogate is used.

## Resources and stopping point

Two CPU-only algebra runs: total5.625 CPU seconds, total5.813 wall seconds,
peak working set37,007,360 bytes (about35.3 MiB). GPU/CUDA0; no framework,
model server or GAS-0 process/file was used. Administrative time is unprofiled.
The measured checking intervals exclude Python/NumPy startup and final output
serialization; these are not represented as a whole-machine resource total.

New records: PROOF.md, REPORT.md, CHECKS.md, checks.py, both check JSON files,
and PROVENANCE.json. The Codex resume is updated with provisional status.
The shared map is not promoted with an unreviewed theorem.

**Single next step:** independent hostile review of the projected saturated
section, the physical twist estimate, joint harmonic kernel and actual legal
query bound. Do not optimize the exponent or begin architecture work first.
