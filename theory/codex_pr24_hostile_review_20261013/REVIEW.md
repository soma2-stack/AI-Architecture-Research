# Independent hostile review of PR #24

Reviewer: Codex. Date: 2026-10-13. This is an independent verification record,
not an amendment to or defense of the author's proof.

Target: [PR #24](https://github.com/soma2-stack/AI-Architecture-Research/pull/24),
exact commit `acb1be84c2cd4b72f399b5d3aa963e46092fa18a`.
Review base: `f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c`.
All references to the target below mean that immutable revision.

## Executive verdict

**The core modified-QSR theorem survives. The PR is not correct in every literal
claim. The original frozen dense-tanh problem remains OPEN.**

1. **VERIFIED:** Lemmas 5.1, 5.2, 5.3 and Theorem 5.4, for the explicitly modified
   QSR recurrence, its declared positive bias weight, and its own future-query
   family. The proof does give separation for every boundary point, not just
   sampled directions. There is no missing factor of R or square root in these
   arguments.
2. **REFUTED as literally written:** Corollary 5.5's claim
   `floor(n'/1001) >= n/1002` for every `n >= 10^6`.
   At `n=1,000,999`, it gives `D=999 < n/1002=999.000998...`.
   Replacing that assertion by `D >= n/1004` repairs the stated onset without
   weakening the asymptotic `Theta(n)` conclusion. The separation, time, and
   coordinate-time bounds survive.
3. **VERIFIED in the augmented model:** Corollary 5.6's projected-gradient
   formula, normalization, preparation charge, and `0.0089503135...` lower
   bound. Its `m` is a bound on simultaneously addressed input coordinates with
   a public preparation schedule. A fixed m-dimensional input map is not
   specified. The normalization is transplanted; the architecture, source
   dynamics, endpoint and legal queries are not those of the original problem.
4. **VERIFIED locally, MIS-SCOPED if used globally:** Lemma 8.1 bounds an
   unweighted sum of gate deficits at one time. It excludes the exact free
   neutral fixed point used by QSR. It does not prove a credit-weighted
   contraction, a neutral-path tax, or impossibility of another original-model
   construction.
5. **PROOF GAP:** the claimed preservation of the full uniform robust-credit
   property by the vanilla tanh ablation. Its experiment uses an idealized
   adjoint box without a realization proof and samples boundary histories.
   Familiar delay-line organization is not itself a proof of that stronger
   equivalence. Do not mark architectural equivalence VERIFIED from this test.

Recommended disposition: retain the scoped QSR result, correct the finite-size
dimension bound and resource wording, narrow the normalization claims, and
leave the tanh-equivalence claim unproved. Do not upgrade the original problem.

## Resume / status

- **Search lens:** hostile proof audit, exact coupled gradients, uniform
  antipodal quantifiers, and resource/contract preservation.
- **Stage:** complete mathematical review and independent computational checks.
- **Strongest surviving result:** QSR's continuous robust bias section, and its
  explicitly augmented fixed-source normalized variant. These are verified
  results for a modified model, not novel-architecture certifications.
- **Killed / closed directions:** the literal `D >= n/1002` rounding statement;
  any claim that matching normalization alone solves the original problem;
  treating sampled idealized tanh adjoints as a uniform equivalence proof.
- **Unresolved questions:** actual legal-query realization and all-boundary
  separation for the tanh ablation; any reduction to the frozen original model;
  the neutral-path tax conjecture. Prior-art references do not settle those
  quantitative claims.
- **Exact next action:** author can correct the enumerated statements in a
  separate revision; any re-review should pin that new SHA. No training or
  additional research search is needed to reproduce this review.

## 1. Governance, evidence and unchanged contract

`AGENTS.md` was read and left untouched. No Claude, Cursor, or Codex notebook
was opened; the PR's specific proof/report/handoff/checker artifacts were
read under the owner's express review request. No author file was modified.
The review adds only its own folder on a separate branch.

Primary sources read include the target's `PROOF.md`, `REPORT.md`,
`REVIEW_HANDOFF.md`, all of `checks.py`, `CHECKS.md`, `STATUS.md`, and
`PROVENANCE.json`. Original-contract sources read directly from the base:

- [Current contract/status](../CURRENT_THEORY.md), Scope / contract and
  authoritative hierarchy.
- [Quadratic construction](../gamma_c_over_n_quadratic_20261001/PROOF.md),
  section 1: full parameter groups, frozen normalization and future losses.
- [Fixed-feature definition](../reachable_fixed_feature_width_20261002/PROOF.md),
  sections 1–3: actual coupled injection and memory semantics.
- [Autonomous-energy contract](../codex_autonomous_absolute_energy_20261003/PROOF.md),
  section 1: actual legal futures and source projection.
- [Strict-budget fixed-feature contract](../codex_frontier_invention_20261006/PROOF.md),
  sections 1–2, and the statement of the
  [linear frontier](../codex_linear_dimension_frontier_20261006/PROOF.md).
- [Continuous-memory units](../robust_width_scaling_20261001/THEORY.md), section 1.

The unchanged original problem fixes, with total width n,

    h_t = tanh(R h_(t-1) + x_t + .05*1),    h_0 = 0,
    ||R||op = 1 - 1/n,
    R_0 = diag(a O, (100n)^(-1) I),  ||R-R_0||op <= 4/(10^8 n^2).

Past inputs lie in the OPEN cube `(-.5,.5)^n`. Future queries have at least
one step, all preactivations in `[.25,.75]^n`, fixed head `1/sqrt(n)`, and
loss divided by the frozen `beta=max(1,||R||F)`. Recurrent group multiplier
is `w_R=||R||F/n`, so `w_R/beta=1/n`. The original bias multiplier is
`RMS(b)=.05`, not an independently selected `.035/sqrt(n)`.

All entries are independently differentiated; realized past and future inputs
are held fixed. In particular, differentiating a cancellation policy or an
inverse-lift formula through its dependence on model parameters changes the
question. One fixed source feature is used. All actual persistent
history-dependent information counts. Preparation, holding, corrections and
reset are charged; there is no subtraction of a public input center from
absolute input norm. A lower section needs one exact common endpoint and
uniform separation greater than `.002` on its entire antipodal boundary.

None of the QSR computations satisfies this entire contract. In particular,
zero bias and identity/shift source dynamics cannot be silently substituted
for the frozen dense biased tanh model.

## 2. Verdict ledger

| Target | Verdict | Precise scope / issue |
|---|---|---|
| Lemma 1.2 | VERIFIED | Correct monomial transport and block index, including R=1. |
| Theorem 1.3 | VERIFIED | Exact polynomial write/cancel identity with realized inputs fixed. |
| Theorem 1.4 | VERIFIED | Correct initial-state Jacobian and post-padding rotation. |
| Proposition 3.1 | VERIFIED | Usual chain rule for the specified parameterization. |
| Lemma 3.2 | VERIFIED | Shared endpoint and identical future make direct future gradient contributions cancel. |
| Propositions 4.1–4.2 | VERIFIED | Their own initial-state parameter and query metrics; not original fixed-feature credit. |
| Proposition 4.3 | VERIFIED | Fixed-head dilution for reachable QSR queries; see the reachability detail below. |
| Theorem 4.4 | VERIFIED | Bias and initial-state bounds in the stated nonexpansive class. |
| Corollary 4.5 | VERIFIED | Its explicit bias/initial-state weights and model class; not every possible normalized parameter metric. |
| Lemma 5.1 | VERIFIED | Exact gradient difference, with correct block placement and all shared parameter injections included. |
| Lemma 5.2 | VERIFIED | Legal QSR future adjoints for `0<rho_f<=.5`; that bound should be restated locally. |
| Lemma 5.3 | VERIFIED | Existential sign-code result; constants and probabilities check. Not a certificate for every random draw. |
| Theorem 5.4 | VERIFIED | Uniform all-boundary separation in QSR under its closed input box and custom positive bias weight. |
| Corollary 5.5 | REFUTED literally | False finite-n dimension rounding; corrected asymptotic theorem is VERIFIED. |
| Corollary 5.6 | VERIFIED / MIS-SCOPED if strengthened | Inequality and normalization verified for the explicitly augmented, publicly addressed model; fixed-port and original-contract interpretations are not established. |
| Section 7.2 quantitative tanh replacement | PROOF GAP | Actual-query realization and uniform sphere separation not proved by the numerical ablation. |
| Lemma 8.1 | VERIFIED | Local reference-model norm/trace bound, with a negligible dense perturbation under the actual bounded-state assumptions. |
| Lemma 8.1 as a universal tax/obstruction | MIS-SCOPED | Does not control credit orientation or accumulated query-visible sensitivity. |
| Original frozen dense-tanh strict-budget problem | OPEN | No unchanged-contract proof or obstruction in this PR or review. |

## 3. Lemma 5.1: exact coupled gradient difference

Write `k_r = Dz^(r) * mu^(R+1-r)` (coordinatewise multiplication), and
`a=sum_r k_r`. At time `u=qR+r+1`, the only nontrivial gate for write r is
`1+z^(r)`. At terminal time `T=(q+2)R`, this gate is on block `R+1-r`:

    1 + ((T-u+1) mod R) = 1 + ((2R-r) mod R).

For r=R this is block 1; there is no block R+1. For t=qR+s, with
`1<=s<=R`, the relevant gates are exactly r>=s, because the suffix starts
at t+1. Thus the transposed transport contributes

    (S^T)^(2R-s) delta_s = (S^T)^(R-s) delta_s.

Each prefix injection t=1,...,qR sees every orbit once per revolution.
Consequently these injections give `q (J_R tensor I_m) delta_0`, not qR
copies of every coordinate. The t=qR contribution is already included
here; the window starts at qR+1, so nothing is double-counted.

An independent scalar form is especially useful for catching indexing errors.
Number OUTPUT blocks b=0,...,R-1. Then the exact difference is

    Delta_b = (q+1) a,                         b=0,
    Delta_b = q a + sum_(r=R-b+1..R) k_r,       1<=b<R.              (R1)

This follows by counting solutions of `b=(s-r) mod R`, `1<=s<=r<=R`.
It is equivalent to the PR's formula but contains no shift powers or
intermediate delta_s arrays. In particular, for R=1, `Delta=(q+1)Dz*mu`.

Independent exact checks propagated the full forward tangent
`B_t=A_t B_(t-1)+I`, then evaluated `(B_T-B'_T)^T mu`. They agree with
(R1) for 234 rational tests, including every adjoint basis direction,
signed adjoints, non-antipodal history pairs, q=0,1,3, and R=1,2,3,4,5,7.
This tests coupled shared-bias differentiation, not only a chosen terminal
Jacobian or the author's backward recurrence.

## 4. Lemma 5.2: realizability, legality and endpoints

Start at zero and write v^(1),...,v^(R), then take one zero-input step.
The port states at times 1,...,R are exactly those writes, including R=1.
There are R nontrivial derivative gates: the gate for v^(r) occurs at
step r+1. At time R+1 it is on output block
`1+((R+1-r) mod R)`. Transposing the remaining S factor moves it to
input block R+1-r. A uniform head is invariant under S. Therefore

    mu^(R+1-r) = (1+v^(r))/sqrt(n).                                 (R2)

All these choices are actual common futures, not independently assigned
adjoints. The same future input array is applied to both histories.
With `v in [-rho_f,0]` and `rho_f<=.5`, every gate used in this query
lies in `[.5,1]`; the returning final port value is also nonpositive.
Thus the sign vertices used in Theorem 5.4 are legal in Q_ne.

The definition of Q_ne mentions port states in `[-2,0]`, which algebraically
would allow negative gates. Starting from zero under the declared input
box, those negative gates are not reachable while retaining legality:
if previous legal port states lie in `[-1,0]`, their returned values
`w(u)=u+u^2/2` lie in `[-.5,0]`. Adding an input at least -.5 cannot go
below -1. The final state is not used as another gate. This induction
justifies the nonnegative-adjoint statement where it is used. Merely
saying `[-2,0] gives [0,1] gates` would be incorrect without reachability.

Independent forward initial-state tangents gave exact (R2) in 36 rational
cases. This result does not realize the original tanh future-preactivation
box `[.25,.75]` and does not realize the tanh ablation's claimed box.

## 5. Lemma 5.3: full probability and covering audit

For fixed unit y and a random sign row, X=g.y satisfies

    E X^2=1,
    E X^4=3-2 sum_j y_j^4 <=3.

Paley–Zygmund applied to X^2 at threshold 1/4 gives
`P(|X|>1/2)>=3/16`. The count has mean at least 3N/16; falling below N/8
requires a deficit of at least N/16. Hoeffding gives
`exp(-2(N/16)^2/N)=exp(-N/128)`. Row independence is sufficient.

A Euclidean 1/120-net of the unit sphere has cardinality at most 241^D.
The first union bound is therefore `241^D exp(-N/128)`. No independence
among different net points is needed.

For the norm event, 1/4-nets on the two spheres have sizes at most 9^N
and 9^D. Approximating the maximizing left and right unit vectors gives
`||G|| <= 2 max_net |u^T G v|`. Each bilinear form has independent sign
coefficients with squared sum
`sum_ij u_i^2 v_j^2=1`. Hence its two-sided tail is at most
`2 exp(-s^2/2)`. Taking

    s^2 = 2(N+D) log 9 + 2N

and union-bounding leaves probability at most `2 exp(-N)`. Under D<=N/1000,

    ||G||^2 <= 8(1.001 log 9 + 1) N = 25.5953744153... N,
    ||G|| < 5.06 sqrt(N).

If ||y-y'||<=1/120, the number of coordinates with
`|(G(y-y'))_i|>=1/4` is at most

    16 ||G||^2 / 120^2 <= .02843930491 N < N/16.

Thus at least N/16 of the net point's N/8 large coordinates remain of
magnitude at least 1/4. This is the needed UNIFORM transfer over the sphere.

Finally,

    1/128 - log(241)/1000 = .0023277030665...,
    P(failure) <= exp(-.0023277030665 N) + 2 exp(-N).

At N=520 this is approximately .29807636<1. The source's rounded exponent
.0023275 is a valid weaker bound. There are actually no allowed positive
integer D for 520<=N<1000, so the first nonvacuous case is N=1000.
There is no constant/probability gap.

Appending y makes theta injective on B^D even if clipping loses information.
Clipping is continuous and odd; differentiability is not required by the
topological argument. At each surviving row its clipped magnitude equals 1.

**Important qualification:** the result is existence, not a deterministic
certificate for the random matrices used in `checks.py`. For example an
all-ones N-by-2 sign matrix and `y=(1,-1)/sqrt(2)` give Gy=0. This matrix
is a possible draw and violates the thickness conclusion. It does not
contradict the existence theorem. Public code search/storage and dense
evaluation of Gy are also not proved to cost O(n); see section 9.

Our independent D=2 diagnostic enumerated every angular threshold and every
interval between thresholds, obtaining a minimum saturated fraction .487
for its sampled N=2000 matrix. For D=3, 230 adversarial/sample directions
gave .476. The D=2 cell enumeration is evaluated in float64; the universal
mathematical certificate remains the proof above. Neither diagnostic is
used as a replacement for that proof.

## 6. Theorem 5.4: every antipode, common query, topology

Oddness gives `Dz=-rho theta(y)`, so every unit y satisfies

    ||Dz||_1 >= rho(n-D)/16,    ||Dz||_2 <= rho sqrt(n).

For one within-block coordinate i, choose the majority sign of sum_r Dz_i^r,
breaking a zero sum in favor of +1. Let P>=N be the positive and negative
masses relative to that orientation. The legal query in Lemma 5.2 yields

    e_i sqrt(n) a_i = P-(1-rho_f)N
                   >= (rho_f/2)(P+N).

This includes zero sums, exact ties, sparse columns, and zero entries.
The query may depend discontinuously on y. That is permitted: robustness
requires `for every y, there exists a common legal query`; it does not
require a continuous query-selection map. Once selected, the same query is
used on H(y) and H(-y) and held fixed during differentiation.

Cauchy–Schwarz across m coordinates, followed by n=mR, gives

    ||q 1_R tensor a|| >= q R rho_f ||Dz||_1/(2n).

The entire window contribution, with no assumed favorable sign, is at most
`R ||Dz||_2/sqrt(n) <= R rho`. Subtraction is safe even for a worst-case
adversarial window. Hence

    ||Delta grad_b|| >= rho R [q rho_f(n-D)/(32n)-1].                (R3)

Since D<=n/1001, `(n-D)/n>=1000/1001`; 32.032 is exactly
`32*1001/1000`. With q=193 and rho=rho_f=.5 the coefficient is
`1.006306193806194`, so rounding DOWN to 1.0063 is legitimate.

The history is continuous and injective because its writes recover theta,
whose final coordinates recover y. The start and endpoint are identically
zero. Each pair is tested through true shared-bias parameter derivatives,
not an initial-state surrogate. Borsuk–Ulam then applies to any continuous
memory encoder into fewer than D real coordinates: some antipodes have
equal codes, the common future produces the same decoder answer, and the
triangle inequality contradicts pair distance greater than 2 epsilon.

This is a lower bound on continuous real memory for the query task. It is
not a bit bound, a practical learning result, or an upper bound for every
history in the architecture. The input history itself also gives the usual
topological upper restriction D<=mT for a robust section.

We exhaustively tested all nonzero ternary Dz patterns for m=1 and R<=5
under three parameter choices, including q=193 and rho_f=.125, for 1,074
cases. Every inequality survived. Full forward derivatives were used for
the small cases and the independently rational-checked scalar formula
for the others. A code in the actual theorem regime n=2002,D=2 was also
checked at threshold directions and 100 additional angles.

The sign query need not be almost optimal. An exact adversarial example is

    R=5, m=1, q=1, rho=rho_f=.5,
    Dz=(.5,0,0,0,-.5).

The specified sign query has norm `1/(2sqrt(5))`; a reversed sign query has
norm `1/sqrt(2)`, which exhaustive vertex enumeration finds optimal.
The ratio is `1/sqrt(10)=.31622776...`. This refutes any universal reading
of the report's observed near-optimality, but does not refute (R3), whose
lower bound is negative in this example. The author labels near-optimality
as a finite sample observation; it should remain one.

## 7. Corollary 5.5: exact counterexample and valid correction

The counterexample is integer arithmetic:

    n = 1,000,999
    R = floor(sqrt(n)) = 1000
    m = floor(n/R) = 1000
    n' = mR = 1,000,000
    D = floor(n'/1001) = 999
    1002 D = 1,000,998 < n.

The failure is not isolated: a scan of n=1,000,000,...,1,099,999 finds
31,931 violations. That scan is diagnostic; the displayed integers are
already an exact counterexample.

A simple universally valid replacement at the stated onset is D>=n/1004.
Indeed `n'>n-sqrt(n)` and floor(x)>x-1 give

    D > n/1001 - sqrt(n)/1001 - 1.

For u=sqrt(n)>=1000, subtracting n/1004 from this lower bound is

    3u^2/(1001*1004) - u/1001 - 1.

It is increasing for u>=1000 and exceeds .986 at u=1000. Thus D>=n/1004
throughout the stated regime. This is a proved correction, not a claim
based only on the scan.

The other numerical estimates check:

- Full-width head reduces active-coordinate adjoints by sqrt(n'/n).
- `1.0063*(R/sqrt(n))*sqrt(n'/n) >=
  1.0063*(1-.001)^(3/2)>1` at n>=10^6.
- Thus `d_b>=c>.002` still holds for fixed c>=.0021.
- T=195R and mT=195n'<=195n; m<=sqrt(n)+2.
- There are at most 2n' nonzero input coordinate-times. For z in [-.5,0],
  `z^2+w(z)^2 <= .25+.140625=25/64`, so
  `||X||_2 <= (5/8)sqrt(n') <= (5/8)sqrt(n)`.
- Inert identity coordinates have identical states and bias tangents in
  the two histories; their pair differences are zero.

Consequently the repaired asymptotic statement, for fixed c, is valid:
`D=Theta(n)`, `T=Theta(sqrt(n))`, `mT=Theta(n)=o(n^(3/2))` in QSR.
Theorem 4.4 and D<=mT prove the stated optimal orders for robust sections
of this nonexpansive class. They do not prove a global memory upper bound.

**Open versus closed input cube.** Theorem 5.4 and Corollary 5.5 allow -.5,
and saturation in the code actually attains it. They are not admissible
under the original OPEN past cube. This is harmless for their declared
QSR contract, but must not be hidden during a transplant. Taking amplitudes
strictly below .5 and increasing q if needed repairs an open-cube QSR
variant, not the dense-tanh problem.

## 8. Corollary 5.6: normalized fixed-source derivative and full preparation

Let k=n_mem=mR=l, nt=n_tot=2k, and f_s=1_l/sqrt(l). At the frozen block
matrix `W_full=diag(S,I_l)`, its Frobenius norm is sqrt(nt)>1, so

    (||W_full||F/nt)/beta = 1/nt.

For a perturbation in the one fixed source direction `delta K = u f_s^T`,
the memory injection at time t is exactly
`u (f_s^T s_(t-1))`. It is one shared trainable recurrent block, not an
independent parameter at each time or for each source coordinate. Its
projected normalized gradient is therefore

    (1/nt) sum_t c_(t-1) lambda_t^mem,
    c_(t-1)=f_s^T s_(t-1).                                      (R4)

The normalization is a FROZEN full recurrent group norm. If one instead
normalized only K by RMS(K), its frozen value is zero and the metric
would vanish. If one normalized the zero QSR bias by RMS(b), that metric
would likewise vanish. The PR avoids the first problem by explicitly
choosing the full recurrent group; the bias theorem instead explicitly
chooses a custom positive weight. These distinctions are essential.

During the R-step source preparation, s ramps from zero to sigma*1_l
and memory remains zero. The scalar c lies in [0,sigma sqrt(l)], with
c_0=0; after preparation it is constant. Since memory dynamics and source
dynamics decouple at K=0, their common future and direct future gradient
terms cancel between the pair. Source-head contributions do not secretly
differentiate through K: there is no memory-to-source coupling here.

The post-preparation part is sigma sqrt(l)/nt times Lemma 5.1, with the
head scaled to 1/sqrt(nt). The preparation difference has norm at most

    [sigma sqrt(l)/nt] R ||Dz||_2/sqrt(nt).

One window charge already appeared in Theorem 5.4, so preparation replaces
the subtractive 1 by 2. Repeating the l1 estimate gives exactly

    d_F >= [sigma/(2sqrt(nt))] rho R
                      [q rho_f/32.032 - 2].                    (R5)

For R=m, sigma=.05, rho=rho_f=.5 and q=193 this is
`.008950313574927753`, safely greater than .002. All square-root factors
in (R4)–(R5) check. The asymptotic construction chooses, for example,
`D=floor(k/1001)` and sufficiently large square k; arbitrary choices of
small D in the upper-bounded allowed range do not by themselves imply
linear dimension. REPORT's table entry `D>=n_mem/1001` is also too strong
for this integer choice; use `D>n_mem/1001-1`.

**Preparation accounting.** The past consists of R preparation steps,
193R neutral accumulation steps, R writes and R cancellations:
`T=196R`, hence `mT=196k=98nt` under the stated simultaneous-coordinate
bandwidth convention. Source preparation adds exactly k nonzero input
coordinate-times and squared norm sigma^2 k. Including the write/cancel
bound gives

    # nonzero past coordinate-times <=3k,
    ||X||_2^2 <= (sigma^2+25/64)k = .393125 k,
    ||X||_2 < .627 k^(1/2) < .63 k^(1/2).

The R+1 future query steps are separate from past-memory cost. If charged
as well, the bandwidth-time product is `m(197R+1)=197k+m`, still linear.
The common endpoint is `(0,sigma*1_l)`, not the original zero endpoint.

**Input architecture qualification.** In the written recurrence
`s_t=s_(t-1)+xi_t`, xi_t is an l-vector. The checker writes different
physical source blocks in successive preparation steps, then writes the
memory port. This proves at most m nonzero addressed coordinates per step.
To call it m scalar input channels, declare a public time-dependent routing
map `B_t` (fixed during differentiation). It is not the same assertion as
one fixed port map `E_1` driving an identity source block. No routing map
or fixed-port realization is specified in the corollary. This is a resource
scope clarification, not a counterexample to (R5).

Independent tests computed projected forward sensitivities and full-trajectory
central differences with the source schedule frozen. Maximum projection
finite-difference error was `2.85e-12`. The actual preparation term was
included. Three additional full forward-tangent tests at q=193 satisfied
strictly positive sample-specific lower bounds. These diagnostics do not
replace the uniform code proof.

## 9. Computational cost and limitations of the author's checks

`mT` here is coordinate-time, not total arithmetic for generating a section,
proving a code, forming dense parameter gradients, or training.

- The frozen QSR forward recurrence can indeed use a ring buffer and O(m)
  work per step. Public time counters/routing need to be declared.
- A dense N-by-D code with D=Theta(n) stores Theta(n^2) signs, and a generic
  evaluation Gy uses Theta(nD) arithmetic. It is a public model/section
  specification, not history-dependent decoder memory, but not an O(n)
  preprocessing theorem. The probabilistic proof provides existence, not
  a fast algorithm certifying the particular G chosen in a numerical run.
- A dense derivative with respect to W or K need not be computable in O(m)
  work per step. Cheap frozen forward execution does not imply cheap
  gradient computation or practical memory efficiency.
- The author's F/K numerical sections use empirical D near n/16, far above
  the proved D<=n/1001, and some small n admit no positive D under the theorem.
  Their large margins are sample observations, not finite-size instances
  certifying the full theorem's quantifiers.
- Several author sections record errors/rational equality flags without
  asserting all of them. A successful process exit or the phrase 'all
  internal assertions pass' is not itself a check that every recorded
  identity passed. Our separate harness asserts the identities it reports.
- The author’s sign-query experiment is a finite sample. The .3162 example
  in section 6 explains why it cannot be promoted to uniform near-optimality.
- The author’s code-thickness optimizer estimates a minimum from above;
  finding no bad point is not a sphere certificate. The proof, however,
  does supply an existential certificate.

The report's 'any normalized parameter-gradient metric' and 'every reasonable
normalization' are **MIS-SCOPED**. The actual results specify particular
groups, weights, query families and model classes. Rescaling a positive
weight rescales separation; zero group RMS can annihilate a group. No
universal claim over undefined 'reasonable' normalizations is a theorem.

One additional algebraic wording correction: the statement that W/U traces
are linear in z is false in general. At R=m=1, T=2 and immediate linear
loss with terminal adjoint 1, the frozen realization gives
`grad_W=w(z)=z+z^2/2` and `grad_U=z^2/2`. The displayed chain-rule formulas
remain correct; the later bias theorem does not use this inaccurate prose.

## 10. Lemma 8.1: verified trace deficit, no general credit obstruction

In the reference model, for a memory coordinate with x_t(i)=0,

    a(Oh_(t-1)^mem)_i = atanh(h_t(i))-.05.

For |h_t(i)|<=eta<=.01 this implies

    (Oh_(t-1)^mem)_i <= -[.05-atanh(eta)]/a < -.0399,

where the inherited a=1-1/n lies in (0,1). Squaring these coordinates and
using orthogonality proves

    ||h_(t-1)^mem||^2
      >= N_t [(.05-atanh(.01))/a]^2
      >= .00159 N_t.                                         (R6)

The exact numerator squared is `.0015999733318443434`, so .00159 is safe.
The explanatory .0016 should be treated as an approximation, not a uniform
lower constant as n tends to infinity.

For actual R=R_0+E, tanh states satisfy ||h||<=sqrt(n), so the extra
preactivation is at most `e sqrt(n)<=4/(10^8 n^(3/2))` per coordinate.
Replace `.05-atanh(.01)` by `.05-atanh(.01)-e sqrt(n)` in (R6).
For the inherited n>=200 this perturbation is below `1.42e-11` before
squaring, vastly smaller than the slack to .00159. The dense-model bound
therefore survives; using orthogonality of the dense R itself would have
been wrong, but is unnecessary.

**What (R6) does not prove.** It bounds `sum_j(1-g_j)`, not
`sum_j(1-g_j)|v_j|^2` for the credit vector v. A gate deficit can be in a
direction orthogonal to v. For example, take a reference O=I and
`h_prev=(-.05/a,0)`. With zero input on the first coordinate its next state
is exactly zero, so it supplies a positive trace deficit at the previous
time. Nevertheless `diag(1-h_prev^2)e_2=e_2`. The previous state is
reachable from zero using bounded inputs
`(atanh(-.05/a)-.05,-.05)`. This is an illustration of the missing logical
implication, not a construction refuting the conjecture in the actual
Householder-twisted dense family.

The bias makes h=0 not a zero-input fixed point; moreover the original
operator norm is strictly below 1 even at all-one gates. So the exact
QSR neutral-isometric state is unavailable. Neither fact quantifies the
full tradeoff for approximate neutrality, moving credit, mixing or another
control mechanism. No bound of the form
`sum_t #supp(x_t) >= c D sqrt(n)` follows from Lemma 8.1 alone.
The PR correctly labels that tax a conjecture. Wording suggesting all
alternative constructions must use one specific dense mechanism is also
an interpretation, not an exhaustive mathematical dichotomy.

## 11. Novelty and tanh substitution: the unresolved proof claim

The primitive-level novelty argument is modest: QSR explicitly uses cyclic
transport, a scalar quadratic map, ordinary parameter sharing and ordinary
sensitivity propagation. No new computational operation is demonstrated.
Related organizations precede the proposal; for example
[Appeltant et al. (2011)](https://www.nature.com/articles/ncomms1476) use a
single nonlinear delayed node, and
[Henaff, Szlam and LeCun (2016)](https://proceedings.mlr.press/v48/henaff16.html)
study recurrent orthogonal constructions for long memory. These are
context for a prior-art screen, not the required robust-credit equivalence
proof for this project's contract.

The stronger Section 7.2 claim changes the map to
`tanh(S h+E_1 x+b)` with zero bias. Nonlinearity now acts on all coordinates
at every time, rather than once at the port. Its sensitivity products and
bias injections differ from QSR. The numerical ablation explicitly
supplies chosen mu entries in `[.5,1]/sqrt(n)` without constructing the
corresponding future inputs. The uniform head sample is realizable as an
immediate query if that modified family allows it, but finitely many
successful samples do not prove every boundary antipode separates.

A complete equivalence proof would need: a specified legal tanh query
family and realization lemma, uniform gate-product contrast on a thick
section, bounds for the actual bias injection factors/window terms, and
the same complete resource accounting. The unproved sketch and finite
ablation do not supply all four. Thus 'existing delay-line mechanism' is
reasonable structural classification, but 'true architectural equivalence
preserves the claimed uniform property' remains a **PROOF GAP**. This
review does not promote QSR to a novel architecture either: absence of
that particular equivalence proof is not positive novelty evidence.

## 12. Reproduction, provenance and final disposition

From a checkout of this review branch:

```powershell
python -I theory/codex_pr24_hostile_review_20261013/independent_checks.py
```

Requirements: Python 3.11+ and NumPy. No torch, GPU or training framework
is used. The script imports no author code, reads no author files at
runtime, and writes only `independent_results.json` in this review folder.
It uses one numerical-library thread and BelowNormal priority on Windows.
The recorded run took approximately 1.2 seconds on CPU.

Read [independent_checks.py](independent_checks.py),
[independent_results.json](independent_results.json), and
[PROVENANCE.json](PROVENANCE.json). The test file includes exact rational
forward sensitivities, full-trajectory finite differences with fixed inputs,
exhaustive ternary sign patterns, alternate amplitudes/q, sphere threshold
directions, a deliberately bad sign matrix, source preparation, rounding
counterexamples, and audited probability constants.

The proof-level conclusions come from the derivations in this review, not
from finite tests. No counterexample was found to Lemmas 5.1–5.3,
Theorem 5.4, or the augmented-model inequality of Corollary 5.6.
The finite-n rounding claim is exactly refuted. The corrected QSR theorem
and transplanted-normalization theorem survive in their stated modified
models. The original problem remains **OPEN** under its unchanged contract.
