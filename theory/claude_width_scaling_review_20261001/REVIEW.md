# Hostile review: robust width-scaling theory (THEORY.md, commit 2b109ed)

Reviewer: Claude (Opus 5.5), 2026-10-01. Target: theory/robust_width_scaling_20261001/THEORY.md (plus REPORT.md and
PROVENANCE.md). This is a mathematical review from scratch, plus one small numerical check (check_truncation.py,
truncation_check.json). Codex's files were not modified.

## Verdicts

| Claim | Verdict |
| --- | --- |
| **Theorem 1:** O(n^2) approximate state suffices under uniform contraction | **VALID AS STATED, BUT NOT TIGHT.** No counterexample exists inside its hypotheses: every permitted query is answered within e_H, with no replay and no horizon dependence. But the n x n factors are redundant. The same truncated sensitivity is recoverable from (2H+1)n coordinates, so O(n log(1/eps)) suffices in the same memory model. |
| **Theorem 2:** margin ceiling (1), cubic sections give a^(2n+O(1)) | **VALID AS STATED, BUT LOOSE.** The proof and the r = nP arithmetic are correct (exponent 2n-3 for n >= 4). Using the 2n-per-step store instead gives m <= [C_*/(1-a)] a^(ceil(r/(2n))-1). Cubic margins then decay like a^(n^2+O(n)), and even quadratic sections (r = c n^2) decay like a^(cn/2+O(1)). |
| **Interpretation:** "a uniform Omega(n^2) lower bound would give Theta(n^2) for the contractive class" | **VACUOUS: the premise is false in that class.** Robust dimension there is at most 2n H(eps) = O(n log(1/eps)), so no uniform Omega(n^2) lower bound can be proved. Section 8's "quadratic target" (a uniformly contractive family with an r >= c n^2, constant-margin section) cannot exist. |

The headline "no constant-margin cubic robust section survives in the uniformly contractive class" is TRUE, and in
fact stronger than stated.

## Theorem 1, audited point by point

1. **Injection operator.** B_t phi = G_t(w_R phi_R h + w_W phi_W x + w_b phi_b). Its adjoint gives
   B_t B_t^T = G_t^2 (w_R^2 \|h\|^2 + w_W^2 \|x\|^2 + w_b^2), which is correct. Numerically the identity holds to 2e-16.
2. **Normalization bounds.** w_R = \|R\|_F/n <= a/sqrt(n) and \|h\|^2 <= n, so w_R^2 \|h\|^2 <= a^2.
   w_W = \|W\|_F/n <= w/sqrt(n) and \|x\|^2 <= nB^2, so the W term is <= w^2 B^2. This also holds for input
   dimension m != n. Hence C_* = sqrt(a^2 + w^2 B^2 + b_*^2) is width-independent. Measured max \|B_t\|op / C_* is at
   most 0.60.
3. **Tail.** \|A_t ... A_(s+1)\| <= a^(t-s) and \|B_s\| <= C_*, so the discarded tail is <= C_* a^H/(1-a) = e_H,
   uniformly in t and history. There is no accumulation (retained terms are exact). Measured error is at most
   0.2 e_H at n = 3–24.
4. **All permitted queries.** Every future-gradient query, one-step or multi-step, has the form common part (a function
   of h and future inputs) + Z_T^T c, with \|c\| <= 1 under the beta normalisation (\|c\| <= \|R\|op/beta <= 1).
   Because Z^[H] approximates Z in OPERATOR norm, every such c, including immediate arbitrary unit adjoints, is answered
   within e_H, and any Lipschitz functional of Z is approximated too. I tried queries with \|c\| > 1, queries that
   depend nonlinearly on Z, losses at later future steps, unbounded future inputs and m != n inputs. None escapes
   within the hypotheses: future-only quantities are computed exactly from h, and the adjoint stays bounded.
5. **Replay.** Neither Codex's store nor mine re-evaluates any past transition. The accepted memory model
   (future_loss_observability PROOF section 7; 4D addendum A2) forbids only replay of DISCARDED, uncounted inputs. The
   decoder is arbitrary. Counted recent inputs and hidden states are legitimate, and THEORY.md itself stores
   v_s = h_(s-1) and x_s.
6. **Horizon and uniformity.** H depends only on C_*, a and eps. Short horizons pad. It is uniform in n under the
   stated hypotheses.
7. **Exact vs approximate.** It is approximate only: error e_H <= eps. Exact memory still needs the accepted nP.

### Why n^2 is not needed (main finding)

Q_(t,s) = A_t ... A_(s+1) G_s with A_k = diag(1 - h_k^2) R. Every h_k with s <= k <= t is either a stored v_(k+1) or
the current h_t. So each Q is a FUNCTION of the stored hidden states and is redundant.

Store only h_(t-H), ..., h_t and x_(t-H+1), ..., x_t: (2H+1)n numbers, or 2Hn on the fixed-h fiber where h_t is
supplied. The decoder then forms Z^[H] by Jacobian products (truncated BPTT). It evaluates no transition and reads no
discarded input.

The numerical check reproduces Codex's factored Z^[H] to <= 6e-17 at n = 3, 6, 12, 24. At n = 24, H = 8 this is 408
numbers against 4,992. With an arbitrary decoder replaying only RETAINED counted inputs, (H+1)n suffices.

**Corrected Theorem 1:** n + 2Hn = O(n log(C_*/(eps(1-a)))/log(1/a)) coordinates suffice, i.e. O(n) at fixed eps.
In raw (unnormalised) units C ~ sqrt(n), giving O(n log(n/eps)).

## Theorem 2, audited

- **Proof.** Compose the section lift X with a continuous encoder E into R^k, k < r. Borsuk–Ulam gives E(u) = E(-u).
  Identical memory and the same h give identical answers. The triangle inequality then gives
  D_C(Z(u), Z(-u)) <= 2e_H, so m <= e_H. This is correct, and the strict condition H q < r is handled correctly.
- **Arithmetic.** r/q_n = (2n^3+n^2)/(n^2+2n) = 2n - 3 + 6/(n+2). H = ceil(...) - 1 = 2n-2 for n = 2, 3 and 2n-3 for
  n >= 4. So m <= [C_*/(a^3(1-a))] a^(2n): the a^(2n+O(1)) claim is correct, and the hidden constant is
  C_* a^-3/(1-a).
- **C_* growth.** Under the hypotheses C_* is fixed. Polynomial growth, for example the raw-unit sqrt(n), cannot defeat
  a^(2n). Only a_n -> 1 or exponentially growing constants can.
- **Stronger corrected ceiling** (same proof, q = 2n per retained step, h supplied):

      m <= [C_*/(1-a)] a^(ceil(r/(2n)) - 1).

  | Section | Corrected ceiling |
  | --- | --- |
  | r = nP = 2n^3 + n^2 (cubic) | a^(n^2 + ceil(n/2) - 1) |
  | r = c n^2 (quadratic) | about a^(cn/2) — quadratic constant-margin sections also collapse |
  | r = c n (linear) | constant exponent, no decay |

  The fixed-margin robust dimension in this class is at most 2n H(eps) = O(n log(1/eps)).
- **Non-uniform contraction.** With a_n = 1 - c/n, Codex's bound gives no collapse (a_n^(2n) -> e^(-2c)), as THEORY.md
  says. The corrected bound still gives cubic collapse: (n/c) C_* (1-c/n)^(n^2) ~ n e^(-cn) -> 0. Cubic collapse holds
  whenever n^2 (1 - a_n) - log(C_n/(1-a_n)) -> infinity. The exact-accessibility family with \|R\|op = 1 remains
  outside every version.

## Other sections

- **Section 6 counterfamily** (R_n = delta(I - 11^T/(n+1)), W = I, b = 1). It is correct:
  - \|A_n\|op = 1, and A_n^-1 = I + 11^T;
  - for delayed fixed-head queries \|c\| <= delta, so \|Z^T c\| <= delta C_*/(1-delta) < eps.
  It correctly shows that the qualitative hypotheses give no fixed-eps lower bound for delayed heads. It does not
  cover immediate unit adjoints, as stated.
- **Sections 7–8 need correction:**
  - the contractive-class upper bound is O(n log(1/eps)), not O(n^2 log(...));
  - the "matching quadratic lower bound" is impossible in that class;
  - the REPORT table row "H(n^2+2n)" should read "(2H+1)n".

## Distinctions requested

- **Contractive vs general dense.** Everything above needs a uniform (or slowly degrading) operator contraction. With
  \|R\|op >= 1 or a_n -> 1 fast, truncation is not uniform. Only exact nP storage and accepted width-dependent-eps
  results apply there.
- **Exact vs approximate memory.** In the contractive class, the cubic exact lower bound (k >= nP for eps < eps_n) and
  the linear approximate upper bound coexist. Necessarily eps_n <= e_(nP/2-ish) ~ a^(n^2): the "cubic" regime there is
  an exponentially small-eps phenomenon.
- **Bounded inputs and normalization** are essential to C_*. Unbounded per-coordinate inputs or growing \|W\|op
  remove uniformity.

## Answer to the final question

Formally, Omega(n^2) together with the O(n^2) upper bound would give Theta(n^2). But in the uniformly contractive,
RMS-normalised, bounded-input class at fixed eps, a uniform Omega(n^2) lower bound CANNOT be proved, because
O(n log(1/eps)) state suffices. The meaningful open question there is a uniform Omega(n) lower bound, which would give
Theta(n) at fixed eps.

Quadratic or cubic robust scaling can only arise in one of two ways:
- outside uniform contraction, which for cubic means n^2(1 - a_n) must stay bounded;
- with eps shrinking in n.

## Strongest remaining weakness of the theory (after correction)

Its whole regime is conditional on uniform operator contraction plus width-uniform W and input bounds. The accepted
exact-accessibility families (\|R\|op = 1) and near-isometric recurrences are not covered, and those are the only
places where super-linear robust memory could still live.

Evidence: check_truncation.py and truncation_check.json in this directory (n = 3–24, a = 0.5 and 0.8, two seeds each;
a few CPU-seconds; no GPU).
