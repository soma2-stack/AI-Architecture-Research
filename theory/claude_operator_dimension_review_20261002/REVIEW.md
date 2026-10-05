# Hostile review: query-visible operator dimension (commit cece652)

Reviewer: Claude (Opus 5.5), 2026-10-02.

- **Target:** theory/query_visible_operator_dimension_20261002/ (PROOF.md, REPORT.md). It has no supporting code.
- **My work:** I re-derived every claim by hand and ran cheap numerical checks: `check_operator.py` and
  `operator_check.json`, a few CPU-seconds in total.
- **Reachability context consulted:** the accepted Omega_c(n^2) construction, the augmented-accessibility proof, the
  future-loss and approximate-observability stages, and PERPLEXITY_PROOF_PACKET.txt. I read the packet only to identify
  which theorem was sent out. It is the exact accessibility theorem.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Exact coupled aggregate recurrence (6a) | **VERIFIED.** It is block RTRL indexed by feature, not a compression. |
| 2 | Storage count | **VERIFIED.** (2n+1) r^2 + (l+1)(2n+1) (+n). This is Theta(n^3), about n^3/2, despite there being only p = O(r) operators. |
| 3 | Physical query norm nu_H | **VERIFIED.** It is the exact all-query norm of one parameter group (R remaining-rows x source-columns) for ONE shared raw feature H. The lower bound uses only permitted queries. |
| 4 | Ambient r^2 ball, half-margin > 0.004851 | **VERIFIED, and ONLY ambient.** The exact half-margin is 0.00540–0.00543. No admissible lift is claimed or shown. |
| 5 | Reachability gap | **REAL.** No repository result supplies it. But at the r^2 scale it is the wrong question for the log gap; see section 5. |
| 6 | An r^2 operator section is only quadratic | **CORRECT.** The log needs more than P = 2n^2 + n coordinates, which forces query-dependent transport structure across non-aggregable age bands. |
| 7 | Accumulation example (Section 6.1) | **VERIFIED.** It shows coherent accumulation only and adds no dimension. |
| 8 | Perplexity convergence | **Same bottleneck**, once stated as widths of the reachable fixed-endpoint answer set. See section 7. |

## 1–2. Exact aggregate recurrence and its cost

**Recurrence.** Write Phi f_s = sum_j f_(s,j) Phi e_j. Then
Zbar_*,T Phi = sum_j (sum_s f_(s,j) Q_(T,s)) Phi e_j, and M_(j,t) = A_t M_(j,t-1) + f_(t,j) G_t, since
Q_(t,s) = A_t Q_(t-1,s) and Q_(t,t) = G_t.

- **It is exactly RTRL.** (M_j)_(a,b) = d h_a / d Phi_(b,j). The recursion is the block RTRL update
  S_t = A_t S_(t-1) + G_t (x) f_t^T, read by feature index.
- **Coverage.** It allows arbitrary aperiodic gates and arbitrary horizons, and covers all p feature channels. The e1
  and l source rows use exact p-vector traces. Nothing is replayed.
- **Numerical check.** The p r^2 aggregates reproduce the directly propagated surrogate block to 6e-16 at n = 16 and 24,
  with random gates.

**Cost.**
- p r^2 + (l+1)p, plus n for current h. For example, 1,914 coordinates at n = 16; about n^3/2 asymptotically.
- The pseudoinverse claim q_joint(X, 0) <= p is correct but vacuous: it is the dimension of a history-dependent subspace
  whose basis costs r^2 per element.
- Codex's own wording ("an arrangement of exact reference RTRL, not a new small encoder") is accurate.

## 3. The physical query norm (eqs. 2–4)

**Derivation.**
- Z = S D, so a normalized perturbation of K = R_(remaining,source) maps to E T (w_R K) H. The selected-group gradient
  is w_R (T^T E^T c) H^T.
- Its Frobenius norm is w_R ||H|| ||T^T E^T c||, which gives nu_H(T) = w_R ||H|| nu_0(T) with the supremum over
  ACTUAL permitted adjoints.
- **Normalization.** w_R/beta = 1/n exactly once ||R||_F > 1. The group-RMS factor is not rescaled.
- **Lower bound.** It uses only the permitted box at h = 0 (v in [1/5, 9/20]) and the sign-corner average
  E||Y^T g||^2 = g_mid^2 ||Y^T 1||^2 + s_g^2 ||Y||_F^2. The maximum is at least the RMS. ||R E T||_F >= (a - e)||T||_F.
- **Upper bound.** It uses the accepted envelope kappa_Q = a/beta. No stronger adjoint is substituted.

**Numerical check** (actual dense R, worst box corner by vertex search, n = 64 and 128): every tested operator obeys
lambda_H ||T||_F <= nu_box <= Lambda_H ||T||_op.

| Operator (Frobenius-unit) | nu_box / lambda_H |
| --- | --- |
| Gaussian, identity, rank-one | 9–16 |
| Rotation sum sum_j a^j O^j | 3.4–4.2 |

So lambda_H is conservative. It is attained only for directions with Y^T 1 ≈ 0.

**Scope of H.** The norm is a one-group, one-shared-feature slice. That is valid for lower bounds and for the
constant-feature class of Section 8. For general histories the correct finite-error object is the joint error (11),
which the note also defines.

## 4. Ambient r^2 ball (Section 5)

**Re-derivation.** For any subspace V with dim V < r^2, there is a Frobenius-unit N perpendicular to V. Then
||R_env N - B||_F >= R_env for every B in V, so the width is at least lambda_H R_env = s_g (a-e) sigma sqrt(l/n)/4.

**Constants.**

| Quantity | Value |
| --- | --- |
| s_g | 0.0767836 (claimed > 0.07) |
| Exact half-margin, n = 200 | 0.005402 |
| Exact half-margin, n = 10^3 to 10^6 | 0.005424–0.005429 |
| Claimed bound | 0.004851 (uses a - e > 0.99, so n >~ 100) |
| Margin / epsilon | 5.4 |
| Packing ratio R_env/delta | 1.80 (claimed > 1.617) |

- **Topology.** Borsuk-Ulam applies to the boundary sphere S^(r^2 - 1) of the abstract ball, with antipodal
  separation 2 lambda_H R_env > 2 epsilon.
- **Finite radius.** This is finite radius at the unchanged epsilon, not tangent rank.
- **What it is.** It is ONLY a theorem about the abstract ball, and the note says so in both files. It is an immediate
  corollary of "the exact query-invisible operator space is {0}" plus the norm equivalence (4). Its only content is
  negative: normalization alone cannot collapse the accumulated-operator envelope. Nothing is shown about admissible
  coupled histories reaching any part of it.

## 5. The reachability gap is real, and existing results do not close it

| Repository result | What it gives | Why it does not supply finite-radius operator reachability |
| --- | --- | --- |
| Exact augmented accessibility (2026-09-30) | Full Jacobian rank n + nP of (h_T, S_T) for generic R | (a) Tangent rank only: no radius, no conditioning. (b) Raw augmented state, not the query-visible accumulated operator. (c) Endpoint not fixed (only a local fiber of unknown size). (d) No group normalization. (e) Its hypothesis (all entries of R^-1 nonzero) holds on this family ONLY through the 4e-8/n^2 dense perturbation, because R0^-1 is block-diagonal. So any direction that needs cross-block coupling has scale around 1e-8. |
| Future-loss exact observability | Exact (epsilon -> 0) continuous-state lower bound nP | No finite epsilon. |
| Approximate observability; 4D–8D antipodal certificates | Finite radius | Fixed small dimensions at small n. |
| Accepted Omega_c(n^2) section | Width-uniform finite-radius section | It varies FEATURES (source states H_s over d phases) with memory gates fixed at I. The operator part is the fixed scalar transport a^j O^j. Zero operator-geometry content. |
| One-pulse obstruction (aperiodic review) | One non-scalar gate changes answers by about 7 epsilon | One direction, two histories. |

So no repository result shows multi-dimensional, finite-radius, same-endpoint reachability of operator variation. The
gap is real and must not be filled from algebraic span, accessibility rank, tangent rank or ambient visibility. The note
already avoids that.

**The r^2 scale is the wrong target for the log question.**
- With scalar gates the accumulated operator lies in span{O^j}, which has dimension d (at most k). With a fixed profile
  it lies in a Krylov module of dimension at most r. Both are O(n), and both classes are already Theta(n^2)-encodable.
- In the fixed-feature block, (15) stores ANY gate history in r^2. So an r^2 operator section there is capped at
  quadratic.
- The question that matters is therefore whether admissible gate variation can raise the robust operator dimension
  beyond the commutative/Krylov Theta(n), and do so jointly for the l feature directions that share the same gates.
- r^2 reachability is neither needed nor sufficient for that.

## 6. Why r^2 does not give n^2 log n, and what extra independence is needed

Codex's argument, via (15), is correct for the one-feature block. Two further constraints make the requirement sharper.

**1. Single-query capacity (rigorous and elementary).**
- For one fixed permitted query c*, the answer u -> Z(X(u))^T c* is a continuous map into R^P, with P = 2n^2 + n.
- Borsuk-Ulam gives an antipodal coincidence on S^(m-1) whenever m - 1 >= P.
- So any section of dimension m > P (in particular any Omega(n^2 log n) section) must be separated by queries that
  depend on u.
- The answer object is then the map Z^T restricted to span(C_0), with up to nP ~ 2n^3 entries. Its query dependence
  comes only from the transports.
- Under scalar or fixed-profile gates, that query dependence collapses to d phase (or r Krylov) aggregates: the accepted
  Theta(n^2) classes.

**2. Depth attenuation (heuristic, not proved).**
- Credit at depth D is multiplied by a^D, and gates (<= 1) can only dissipate.
- The only amplification is coherent accumulation within a band, whose length is capped near n/c.
- For spread, high-dimensional sections, per-band margins are therefore width-independent constants times a^D. The
  accepted section's margin is only 0.002 = 2 epsilon (0.00207 uniform).
- At fixed epsilon, only O(log(m0/epsilon)) bands of length Theta(n/c) can each carry Theta(n^2) spread coordinates.
- Deeper credit (up to the (n/2c) log n window) is visible only coherently, carrying few dimensions. That is consistent
  with the accepted "log lookback necessity, quadratic aggregation" split.

**What an Omega(n^2 log n) section would need, all in ONE continuous same-endpoint section with width-independent
margin:**
- (i) Theta(log n) age bands whose transports are mutually non-aggregable in the query metric (non-commuting, and not
  in one Krylov/commutative module);
- (ii) Theta(n^2) independently varying feature coordinates per band;
- (iii) separation witnessed by u-dependent queries;
- (iv) one shared gate sequence for every feature/source group;
- (v) margins that survive the a^D attenuation of deep bands.

Point (v) currently looks like the most serious obstacle. It suggests the log may NOT be obtainable through robust
sections, and that the gap may lie on the encoder side. This is a hypothesis.

## 7. Section 6.1 accumulation example

**Hand check.**
- Inputs are in the cube (max about 0.374 source).
- h_(N+2) = 0 exactly, and memory gates are all I.
- M = sum_(j<=N) a^j O_*^j.
- ||M||_F >= m_N sqrt(k - d) with m_N > 3n/5 and k - d = n/4.
- Lower bound 0.3 s_g (a - e) sigma sqrt(l/n) sqrt n > 0.0058 sqrt n.

**Numerical check.**

| n | Aggregate nu_box | Claimed 0.0058 sqrt(n) | Single packet nu_box | Bound 0.4/sqrt(n) |
| --- | --- | --- | --- | --- |
| 64 | 0.229 | 0.046 | 0.023 | 0.050 |
| 128 | 0.263 | 0.066 | 0.016 | 0.035 |
| 200 | 0.290 | 0.082 | 0.013 | 0.028 |

The single packet is epsilon-small only for n >~ 3.4e4 numerically (the note says >= 160000).

**Status.** One scalar-gate history. It demonstrates that per-operator thresholds must carry the 1/gamma accumulation
factor (eq. 13, tolerance about epsilon/n). It adds no lower-bound dimension, and the note says so.

## 8. Relation to the independent Perplexity ideas

Put all of them on one object: the reachable fixed-endpoint answer set A = {c -> Z(X)^T c : X admissible, h_T = h*},
with the sup-over-permitted-query norm.

| Idea | Its place relative to A |
| --- | --- |
| Query-visible continuous dimension | This is d_rob(epsilon), essentially the Urysohn (Alexandrov) width at scale about epsilon of the history -> answer map: the smallest m with a continuous m-coordinate encoder whose fibers have answer-diameter <= 2 epsilon. |
| Bernstein widths | These are the lower-bound tool. A linear m-dimensional query-norm ball of radius > epsilon INSIDE A, plus a continuous same-endpoint lift, gives a Borsuk-Ulam section. |
| Kolmogorov (linear) widths | These, which are Codex's (6), are the linear-encoder upper-bound tool. They need counted coefficients and bases (the window encoder is one). |
| Ambient r^2 operator visibility | The trivial Bernstein = Kolmogorov width of an ambient SUPERSET of A. |
| Gate-dissipation budget | A proposed mechanism bounding A's widths from above. Operator diversity needs non-scalar gates, and those dissipate the very accumulated credit that makes operators visible. |
| Missing reachability | The gap between A's Bernstein widths and the ambient ball. |

So Codex and the independent analyses do point at the same bottleneck: the finite-radius geometry of the actually
reachable, feature-coupled answer set, not algebraic or ambient dimension.

Two refinements:
- the decisive quantity for the log gap is operator diversity beyond Theta(n) per feature direction, jointly across
  features, NOT reachability of r^2;
- depth attenuation (section 6) must be confronted before investing in a log lower bound.

## 9. Smallest meaningful next theorem

**Fixed-feature reachable operator width.** In the constant-source-direction class of Section 8 (credit
K -> E M_T K H with M_T = sum_s alpha_s Q_(T,s)), at c = 1 and the fixed endpoint h_T = 0, decide whether
admissible same-endpoint sections exist whose nu_H antipodal half-margin exceeds epsilon with dimension omega(n). That
is, does gate variation create robust operator dimension beyond the commutative/Krylov Theta(n) reachable with scalar or
fixed-profile gates?

- Prove an O(n polylog n) cap via a quantitative gate-dissipation budget, or construct an omega(n) section.
- This is the reachability gap at the scale that actually matters.
- It is free of encoder questions, since storage there is r^2 by (15).
- Codex's finite-chart criterion (16)–(17) makes a numerical screen possible first.

A parallel check before any log-lower-bound attempt is a rigorous dimension–depth tradeoff: an upper bound on the
margin of m-dimensional sections supported on credit older than D.

## Evidence

- **Checks:** `check_operator.py` and `operator_check.json`.
- **Not modified:** Codex's files. Nothing was committed.
