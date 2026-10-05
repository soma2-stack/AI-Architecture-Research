# Hostile review: query-weighted moment merger (commit 421544d)

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** theory/query_weighted_moment_merger_20261001/ (PROOF.md, REPORT.md, PROVENANCE.json). It comes with no
  supporting code.
- **My work:** I re-derived every lemma by hand, then ran numerical checks on the actual dense rotating family:
  - `check_merger.py`, which reuses the family and surrogate code from ../claude_rotating_gate_review_20261001 and
    `box_max` from ../claude_aperiodic_review_20261001;
  - the `*.log` files and `*_check.json` outputs in this directory.

## Verdicts

| Question | Verdict |
| --- | --- |
| **1. Centered-covariance identity** | **VERIFIED.** Exact, with every cross term and the 1/4 factor at alpha = 1/2. Numerically 1e-15. |
| **2. Horizon-uniform error ledger** | **VERIFIED as a valid upper bound.** It is NOT a sharper bound in the hard regime: on rows whose gate is 1 it is never better than the plain geometric triangle sum, for any choice of lambda. |
| **3. Memory count** | **VERIFIED.** Formulas (24) and (C8) are exact; nothing is hidden or replayed; updates are continuous; O(n^2) for fixed m. Each packet costs about 3n^2/4 coordinates, so m must truly be O(1). |
| **One-packet counterexample** | **VERIFIED**, analytically and on the actual dense model. It is stronger than stated: round-robin fails for every m = o(n). The e1 eligibility row repairs it. |
| **4. Remaining obstruction correctly reduced?** | **NO.** The ledger statement is only a sufficient condition, for this family only. For this packet algebra it is very likely false: it fails, both as a certificate and in actual error, already for constant (period-1) non-scalar gates, which the reviewed Floquet encoder handles exactly in O(n^2). |
| **5. Hidden assumptions** | The convex-Q merge algebra; the per-step scalar ledger; the storage break-even against the window encoder; the reset endpoint; Section 8 heredity; the family is specific. See the end. |

## 1. Centered-covariance identity (Section 3): verified

Hand re-derivation.

- **Residual.** (alpha Q1 + (1-alpha) Q2)(M1 + M2) - Q1 M1 - Q2 M2 = -(Q1 - Q2)[(1-alpha) M1 - alpha M2]. That is (4),
  and every cross term is accounted for. The transport-feature pairing is kept.
- **Query error.** M_v phi = sum_j O^j Psi V_j, where Psi is the k x p block of memory-row parameters. Each entry of
  Psi is one parameter coordinate. So r^T c is -B(z)V reshaped, which gives (5). Its squared Frobenius norm is
  sum_{j,l} (V_j . V_l) z^T O^j (O^l)^T z, which gives (7). The adjoint of Psi -> Psi V_j is u -> u V_j^T, so
  M_v M_v^T = K(V). Grouping by s = j - l mod d gives (8).
- **A sharper equivalent form, not stated in the note.** K(V) = sum_omega |sum_j omega^j V_j|^2 P_omega, where
  P_omega are the spectral projectors of O. So K is PSD, and its eigenvalues are the orbit power spectrum of the
  centered features. The stationary cancellation (13) is exactly the omega = 1 mode vanishing.
- **Mass bound (11)-(12).** Correct; 2 mu1 mu2/(mu1 + mu2) is the harmonic mean.
- **Numerical check** (`identity`, n = 24 and 40, 20 random packet pairs each, explicit k x kp matrices):

  | Quantity | Result |
  | --- | --- |
  | (4), (5), (7) | relative error <= 3e-15 |
  | Spectral form | max eigenvalue of K matches max over omega of the power spectrum, to 2e-15 |
  | Ratio in (12) | <= 0.43 |
  | Coherent channel (13) | K Pi = M_v^T Pi = 0, to 1e-14 |
  | Heterogeneous tuple mass | does NOT cancel (K Pi relative size 1.0), as the note's qualification says |

The identity describes one merge exactly; it says nothing about how many merges are needed.

## 2. Horizon-uniform ledger (Section 5): valid, but not sharper where it matters

**The lemma is correct.**
- p~_{t-1} = (A_t/lambda)^T p~_t gives energy drop ||D_t p~_t||^2, which telescopes to <= ||c||^2.
- Variation of constants pairs r_t with p_t = A_(t+1)^T ... A_T^T c. Inserting D_t D_t^-1 and applying Cauchy-Schwarz
  gives (16).
- Pairing r_t with the D of the same step t is legitimate: each D_t is used once in the telescoped sum.
- **Lambda is valid uniformly.** For every actual gate in (0, 1], ||a G O|| <= a < lambda = 1 - gamma/2.
- The encoder recurrence E_t = A_t E_(t-1) + r_t holds because the advance (22) and fresh packet (23) are exact. I
  checked: Q^- M_(f^-) = (G/g) O Q O^T a g O M_f = A_t Q M_f.
- **Gate history:** all of it enters through the actual A_t.
- **Every permitted late query:** covered, via ||c_q,mem|| <= ||c_q|| <= kappa_Q.
- **Other rows:** source rows and (in the hybrid) the e1 row are surrogate-exact.
- **Dense error:** delta_dense = kappa_Q e C/gamma^2 comes from the accepted, horizon-free transfer. I re-checked
  48/(5e8 c^2 sqrt k).

**Numerical check** (`exact`):
- With more slots than steps, every merge goes into an empty slot. The encoder then matches the directly propagated
  surrogate to 1e-15, for both plain and hybrid. Hybrid e1 and source rows are exact to 8e-16.
- With m = 1, 2, 5, ||E_T||op = 0.24 <= sqrt(z_T) = 1.4–1.5 at n = 16, and 0.077 <= 0.66–0.77 at n = 20.
- The random test histories there exceed the input cube (max input 0.80). That only matters for admissibility; these
  are algebraic checks.

**What the ledger does NOT buy.** On rows whose gate is 1, D_t^-1 = 1/sqrt(1 - (a/lambda)^2), which is about
sqrt(n/c). For residuals supported on such rows, Cauchy-Schwarz gives, for every lambda in (a, 1),

    sum_t a^(T-t) ||r_t||  <=  [sum_t (a/lambda)^(2(T-t))]^(1/2) [sum_t lambda^(2(T-t)) ||r_t||^2]^(1/2)  <=  sqrt(z_T).

So the plain geometric triangle sum, the "ordinary contraction sum" behind (26), is never worse than the ledger there.
- For a steady stream of residuals the two coincide to leading order: about ||r||/gamma at lambda = (1+a)/2.
- For an isolated residual the ledger is worse by a factor of about sqrt(n/c).

The loss weighting helps only for residuals created on strongly damped rows. Adversarial histories keep most memory
gates at 1 (h_row = 0), so in the hard regime the target (25) needs per-merge raw residuals of order
epsilon c/sqrt(2n) on gate-1 rows.
- **Fair part of claim 3:** the per-merge bound (12) no longer multiplies by the C/gamma old mass.
- **Overstated part:** the total ledger still pays the full n/c window factor, as (26) concedes.

**Measured looseness.** On my stress histories the certificate exceeds the actual worst-query error by about 40–100x:
for example, ledger bound 4.4 against actual 0.054 (sparse, n = 256). On the hybrid counterexample run it
over-estimates by about 30x and still certifies (9.8e-6 against actual 3.5e-7).

## 3. Memory count (Section 6.1, C8): verified

- **Every term is counted** in (24): the k^2 transport, d(2n+1) features and 1 mass per packet, the l(2n+1) source
  traces, the clock and z. (C8) moves e1 into an exact p-vector row and leaves (k-1)^2 per packet.
- **The c = 1 closed form checks:** for n divisible by 4, (3m/4 + 1)n^2 + (m/4 + 1/2)n + m + 2.
- **Nothing is hidden.** The decoder uses only counted state and public O powers; K, eigenvalues and decoded
  sensitivities are transient. Current h is needed both for g and D_t and for the fresh features (+n if not
  supplied). There is no replay.
- **Continuity.** Positive mu_new >= g w_b keeps alpha well defined. g = max G is continuous. The round-robin clock is
  public. Merges are convex.
- **Implemented counts** (`count` field, hybrid): n = 64, m = 1 gives 7285 coordinates; n = 256, m = 16 gives 849,571.
- **Fixed m gives O(n^2).** Correct, but each packet costs about (1/4 + 1/(2cL)) n^2, which is 3n^2/4 at c = 1. The
  reviewed window encoder needs 2Hn with H ~ (n/c) log(kappa_Q C/(epsilon gamma)). At n = 256, c = 1, the two
  storages break even near m ~ 26. Packets are worth having only if m is genuinely O(1); any m ~ log n merely ties
  the trivial window encoder.

## 4. One-packet counterexample (6.2) and the e1 repair (6.3): verified, and stronger than claimed

**Hand check.**
- On the accepted O, e1 is exactly O-invariant. Numerically O11 = 1 and the off-diagonal row/column entries are
  <= 3e-16. e2 is not an eigenvector (O22 = 0.0988).
- The interior e1 gate equals a exactly, because 1 - 1/n = a.
- Coefficients (C2) and (C3) follow from the injection and gate timing: the injection at time s+1 carries a^(2(N-s)),
  including the final reset step.
- Floor bounds: 1/2 <= a^M < 1/(2a).
- 19601/79202 > 0.24748. 1/199 + 3/4e6 < 0.00503. The constant product is 0.049896.
- Inputs stay inside the cube and h_T = 0 exactly.
- The dense transfer (C6) is below 1e-6.

**Actual dense model, n = 200, N = 40000, T = 40001** (`c1.log`; uniform permitted query (9/20)1, and worst
permitted box query):

| Encoder | Uniform-query error | Worst box query |
| --- | --- | --- |
| plain round-robin m = 1 | **0.0989** | 0.118 |
| plain round-robin m = 2 | 0.0989 | 0.118 |
| plain round-robin m = 8 | 0.0989 | 0.118 |
| plain round-robin m = 32 | 0.0984 | 0.118 |
| hybrid m = 1 | 1.7e-7 | 3.5e-7 |
| hybrid m = 4 | 1.7e-7 | 3.5e-7 |

- **Constants:** A_n/n = 0.2499, B_n/n = -0.0014, q_T = 0.48.
- **Error size:** the K block alone predicts 0.055 > 0.048. The total, 0.099, includes other row-1 blocks with the
  same sign-switch mechanism.
- **Scope is understated.** The note claims only m = 1. Round-robin slot s holds injections whose ages are all
  congruent mod m, so each slot's B^(s) nearly cancels, with |B^(s)| = O(1). The error stays about A_n·scale for every
  m = o(n), as the m = 2/8/32 rows show.
- **The repair works**, and its own ledger certifies it on this history: z_T/target = 1e-4, bound 9.8e-6.
- **Why it cannot be an Omega(n^2 log n) lower bound.** It is a single history, not an antipodal section, and its
  failure mode is fixed by p = 2n+1 counted coordinates. The note says so correctly.

## 5. Is the remaining problem reduced to the constant-packet ledger statement? No

**Logically**, the statement "some continuous policy with m = m(c, epsilon) keeps sup_T z_T <= target" is sufficient
for an O(n^2) upper bound on THIS family only. It is not necessary. It is not equivalent to d_rob = O(n^2) on the
family. It says nothing about the general dense class, and its failure gives no lower bound. The note itself states
the family and lower-bound caveats.

**Substantively, for this packet algebra the statement looks false, and the actual encoder fails too.** All checks
below use the hybrid encoder, admissible inputs (max |x| <= 0.488, h_T = 0), the actual dense model, and the worst
permitted box query. epsilon = 0.001.

| History | n = 64 | n = 128 | n = 256 | z_T/target |
| --- | --- | --- | --- | --- |
| scalar gates (sanity) | 1.2e-11 | 4.5e-12 | 1.6e-12 | ~1e-17 |
| **period-1**: one constant non-scalar gate (h_mem = 0.4 e3), constant source | 0.024 | 0.019 | 0.020 | 2e4–1e7 |
| period-1 gate, random source signs | 0.060 | 0.062 | 0.063 | 3e6–2e7 |
| sparse aperiodic: one random memory row at ±0.35 per step | 0.070 | 0.045 | 0.056 | 4e6–2e7 |
| dense aperiodic memory h ~ U(-0.2, 0.2), shrunk into the cube | 0.047 | 0.051 | 0.054 | 1e6–2e7 |

- These are round-robin m = 1/4/16; the three agree to within a few percent, except period-1 at n = 64, m = 16 (0.0099).
- **Greedy oracle, m = 8.** At every step it merges the pair, among m+1 packets, with the smallest loss-scaled
  residual. This is discontinuous and is a probe only. Its errors are still 10–22 epsilon:

  | History | n = 64 | n = 128 | n = 256 |
  | --- | --- | --- | --- |
  | period-1 | 0.016 | 0.019 | 0.022 |
  | period-1 with random source signs | 0.012 | 0.010 | 0.010 |
  | sparse | 0.012 | 0.012 | 0.018 |

  Its z_T/target stays at 3e5–3e6.
- **No-reset variant.** Without the final reset (h_T = 0.4 e3, query input still in the cube), period-1 still fails at
  0.019–0.021 (`stress_noreset.log`). The one exception is m = d (n = 64, m = 16): there every round-robin slot holds a
  single orbit phase, constant features make every merge exact (error 3.5e-6), and the cost is d ~ n/4 packets.
- **Greedy m-sweep on sparse histories** (`msweep*.log`):

  | n | m = 4 | m = 8 | m = 16 | m = 32 |
  | --- | --- | --- | --- | --- |
  | 64 | 0.018 | 0.012 | 0.0075 | 0.0044 |
  | 128 | — | 0.012 | 0.0077 | 0.0052 |

  The error falls roughly like m^-0.7 and does not improve with n at fixed m. At m = 32 the packet state (101,091 and
  406,915 coordinates) is already larger than the reviewed window encoder's 2Hn (about 77,000 and 322,000). It still
  misses epsilon by 4–5x, even with a discontinuous oracle policy. At fixed m, z_T/target grows with n: 2.7e4 to 2.3e5
  at m = 32, and 3e5 to 2.6e6 at m = 8 from n = 64 to 256.

Two structural reasons explain this.

**(a) The merge algebra, not the policy, is the obstruction.**
- With constant gates the true transport of age j is a^j X^j G, where X = GO. The packet form normalizes this to
  Q_j = X^j G O^-j, and Q_j changes by a rank-one O(sigma^2) step with every additional unit of age. A convex
  mass-weighted average of several Q_j cannot reproduce the right transport for each member.
- With constant features, the exact single-packet representation needs the refit
  Q* = (Q1 C1 + Q2 C2)(C1 + C2)^-1, with C = sum_j F_j O^j. That is not a convex average, and it loses ||Q|| <= 1.
- The reviewed Floquet/Cayley-Hamilton encoder handles period-1 gates exactly in O(n^2) using a transport basis
  (powers of X) with feature coefficients. That is a different algebra.
- So the constant-packet statement fails on a class that already has a proven O(n^2) encoder. A positive theorem would
  need a different packet structure, not just a cleverer schedule.

**(b) Pigeonhole / Little's law (heuristic, not proved).**
- With m slots, at most m injections are unmerged, so the mean age at first merge is at most m.
- At that age the injection still has mass about mu_new e^(-cm/n) ≈ mu_new.
- For sparse or period-1 non-scalar gates its normalized transport differs from every other packet's mass-weighted
  transport by about sigma^2 in operator norm, so each step costs nu_t >= ||r_t|| ~ sigma^2 mu_new.
- That gives z_T >~ (sigma^2 mu)^2 n/c against the target epsilon^2 n/2. This fails, independently of n and m, as
  soon as the gate non-scalarity sigma^2 is well above epsilon/mu.
- The greedy numbers are consistent with this.

## 6. Hidden assumptions that could invalidate the planned theorem

1. **Convex-Q merge algebra.** See (a). Age-dependent transports inside a packet cannot be represented, even for
   period-1 gates. This is the decisive one.
2. **Scalar per-step ledger.** Section 2 shows it is never sharper than the triangle sum on gate-1 rows. It discards
   cross-merge incoherence; that is the only thing the uncountable matrix Gram in (16) keeps. Even an actually-accurate
   packet encoder could not be certified by (25) on hard histories, since the ledger over-estimates by about 30–100x
   in my runs.
3. **Storage break-even.** Packets cost about 3n^2/4 each, so m must be O(1). The target is not "some m(c, epsilon)",
   but an m small enough to beat 2Hn. The break-even is about 26 at n = 256 and grows like log n.
4. **Final steps are visible undamped.** Histories may end with a reset or any gate change. The most recent merges
   are seen almost unattenuated, so any policy must keep its youngest injections unmerged.
5. **Section 8 heredity (28) is conditional.** It maps later adjoints into C(h) only if the prepended input is itself
   a permitted FUTURE input. Accepted documents define the future family through a preactivation box ("includes
   [1/4, 3/4]^n"). Admissible PAST inputs anywhere in the cube need not qualify. So an arbitrary history step can make
   a residual that was invisible to permitted queries visible again. The REPORT's phrase "prepending an admissible
   input" overstates this.
6. **Family specificity.** Section 6.3 uses the exact O-invariance of physical e1. Merges use the public O. Any
   result covers this rotating family only (as the note says) and cannot close the general class gap.

## Bottom line

- **What is verified:**
  - the centered-covariance identity, and its spectral form;
  - a valid horizon-uniform ledger;
  - an exact O_m(n^2) storage count;
  - a correct, and in fact stronger (all m = o(n)), counterexample with a working one-row repair.
- **What is false or misleading as stated:** the ledger is not sharper than a triangle sum on undamped rows. And the
  "remaining problem" is not reduced to a constant-packet ledger theorem: that statement appears false for this
  merge algebra, already on periodic gates.
- **What remains open is unchanged.** Is the robust dimension on aperiodic non-scalar histories O(n^2) or
  Omega(n^2 log n)? Any packet route needs a non-convex transport representation, such as transport bases or refits,
  and an error certificate that keeps cross-merge incoherence.

## Evidence and resources

- **Code:** `check_merger.py`, with modes identity, exact, c1, stress and greedy (the m-sweep is greedy with an m
  list).
- **Logs:**
  - `c1.log`: the counterexample.
  - `stress.log`: scalar, period-1 and period-1 with random signs results. Its sparse/dense rows are SUPERSEDED: those
    first versions violated the input cube (max |x| 0.74–0.76 and 0.55).
  - `stress_adm.log`: admissible sparse/dense.
  - `stress_noreset.log`: its sparse_noreset rows at n = 64 also needed a future input up to 0.78 and are not used.
  - `greedy_period1.log`: use its period-1 rows only.
  - `greedy_adm.log` and `msweep*.log`.
  - JSON copies for each run.
- **Compute:** about 2.5 CPU-hours on at most about 21 threads at below-normal priority. No GPU.
- **Not modified:** Codex's files. Nothing was committed.
