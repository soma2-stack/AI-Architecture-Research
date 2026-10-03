# Joint harmonic lower section: reviewed theorem and consolidation

Codex, original 2026-10-02; consolidation 2026-10-03.
No architecture, training, new contraction regime or generic compressor.
Claude/Grok files and all historical evidence are preserved.

## Outcome

**The original 19/18 theorem is accepted after independent review:**

    d_fixed-feature >= floor(d/1,000,000) floor(n^(1/18))
                    >= n^(19/18)/20,000,000,

for n>=10^504, c=1, epsilon=.001, under the unchanged normalized legal-query
and continuous-encoding contract. This refutes a universal O(n) encoder
under the all-admitted-history contract. It does NOT establish Claude's
proposed n^(7/6) exponent or a moderate-width improvement.

The owner reports two Perplexity reviews and the saved Grok review; the
accepted JOINT proof is unchanged by the auxiliary correction below. The
Perplexity results are supplied in the owner's context, not separate saved
review documents located in this workspace. No review content is invented.
The accepted historical floor(n/8) lower remains preserved in its original files.

## Strongest results after consolidation

| status / public rule | threshold | joint dimension lower | uniform antipodal half-margin |
|---|---:|---:|---:|
| accepted original: F=floor(n^(1/18)), delta=10^(-10)/F^3 | 10^504 | n^(19/18)/20,000,000 | >9 |
| Grok corollary, independently checked here: F=floor(n^(1/16)/10^4), SAME delta | 10^80 | n^(17/16)/(2*10^11) | >=99,989.9997499979>9 |
| NEW internally checked ledger corollary: F=floor(n^(1/15)/10^4), delta=10^(-10)/F^(5/2) | 10^75 | n^(16/15)/(2*10^11) | >=998.9997499979>9 |

The second row should replace 19/18 as the strongest independently reviewed
and now independently checked choice. The third row is NOT covered by the
previous reviews: it follows from the same construction/ledger with an
explicitly rebalanced public amplitude and needs its own hostile review.
No new recurrence, witness search, query contract, metric or epsilon is used.

For the unchanged F^-3 amplitude law, the leading term is
10^(-27)sqrt(n)/F^8 and theta=1/16 is its power ceiling. It is NOT the
ceiling if amplitude may rebalance within the same ledger. Maximizing
sqrt(n)[10^(-17)delta/F^5-delta^3] gives a constant times
sqrt(n)/F^(15/2), with attainable power ceiling theta=1/15.
PROOF.md sections12A--12C give all constants, floors and size conditions.
These are ceilings of the conservative proof estimates, not impossibility
theorems for the actual reachable family.

## Original 19/18 construction: answers with auxiliary normalization corrected

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
2. **Degree-one signal.** For an ISOLATED component f of the joint word,
   with profile L1>=rho d and amplitude delta/F, after node/twist corrections,

       signal_f >=rho delta sqrt(n)/(200000 f F)-delta/F.

   For sqrt(n)>=400000f/rho this gives
   `signal_f >=rho delta sqrt(n)/(400000 f F)` in the ACTUAL legal-query norm.
   Omitting F would apply only to a DIFFERENT separately normalized single
   component of amplitude delta. It must not be substituted into the joint
   construction. Its full proof already pays delta/F through F^5; the
   accepted joint theorem is unaffected by correcting the auxiliary display.
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
9. **omega(n).** Yes, accepted for the original 19/18 theorem; the 17/16
   corollary has now been independently checked against the full ledger.
10. **Universal O(n).** Refuted under the stated continuous
    no-replay all-admitted-history model: qF/n diverges. The lower
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

The stated radius allowance is width-dependent; a WIDTH-UNIFORM Euclidean
history radius has not been proved and is not part of this theorem. A
diverging upper majorant alone does not prove the actual minimum enclosing
radius diverges. Individual raw inputs remain inside
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

Original records: PROOF.md, REPORT.md, CHECKS.md, checks.py, both check JSON
files and PROVENANCE.json. Original document bytes are preserved at commit
d2a4317; original numerical outputs, CHECKS.md and PROVENANCE.json remain
unchanged. Their hashes refer to that original version, not this edited
proof/report. New exact arithmetic, change provenance and checks are stored
separately in theory/codex_multiharmonic_consolidation_20261003/.

Updated reviewed fixed-feature bounds are Omega(n^(17/16))--O(n^2) in the
ordinary counted-history-statistic contract. The NEW internally derived
16/15 row would strengthen the lower after review. The literal finite-jet
causal-width lower also applies, without silently substituting the ordinary
reference-matrix upper for an exact finite-jet update-compatible quotient.
The full-model Omega_c(n^2)--O_c(n^2 log n) bounds are unchanged. One feature
cannot be multiplied across sources without a new JOINT proof.

**Single next step:** independently audit only the amplitude-balanced 16/15
corollary and the ledger-ceiling calculation. No new direction, experiments,
architecture invention, learning or contraction regime follows this stage.
