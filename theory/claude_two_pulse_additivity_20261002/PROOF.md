# Two-pulse additivity in the fixed-feature class

Claude (Opus 5.5), 2026-10-02. This is new theory, written after the hostile review of
theory/reachable_fixed_feature_width_20261002 (see theory/claude_fixed_feature_width_review_20261002/REVIEW.md). The
statements below are separated into **rigorous** results (proved here and checked numerically) and **heuristic or
numerical** findings (explicitly labelled). Nothing here changes the full-model bounds
Omega_c(n^2) <= d_rob <= O_c(n^2 log n).

## 0. Setting (unchanged accepted contract)

**Model.** The accepted rotating/dense tanh family at c = 1, n >= 200.
- a = 1 - 1/n, k = floor(n/2), l = n - k, d = floor(n/4), r = k - 1.
- O = U(P_d ⊕ I_(k-d))U^T, with U = I - 2ww^T/||w||^2 and w = e1 - 1_k/sqrt k.
- P_d e_i = e_(i+1 mod d) (1-based memory coordinates).
- R0 = diag(aO, delta I_l), and ||R - R0|| = e <= 4/(10^8 n^2).
- W = I, b = (1/20)1, epsilon = 1e-3.
- w_R/beta = 1/n.

**Fixed-feature class.** The source state equals H = 0.4·1_l at every interior step. The selected parameter group is
K = deltaR_(memory 2..k, source). Its normalized gradient for a permitted late query xi is w_R (B_T^T xi) H^T, where
B_t = G_t(R B_(t-1) + alpha_t E), with alpha_1 = 0 and alpha_t = 1 for t >= 2.

**Robust dimension.** This is the accepted continuous-encoder notion. A continuous same-endpoint section over S^(m-1)
whose antipodal pairs are more than 2 epsilon apart under some permitted query forces at least m coordinates
(Borsuk-Ulam).

**Pulse.** A pulse is a step at which the memory state is nonzero. A q-pulse family has nonzero memory state only at
q fixed times. Its trajectory is otherwise fixed: warmup with memory 0 and source H, then the pulses, separated by at
least one zero-memory step, and a final exact reset to h = 0.

**Notation.**
- NC = {d+1, ..., k} is the "stationary" (non-cycled) block of physical memory coordinates; L = k - d is its size.
- c_k = 1/(sqrt k - 1).
- s_g = (sech^2(1/4) - sech^2(1/2))/2 > 0.07678.
- g_hi = sech^2(1/4), g_lo = sech^2(1/2).

## 1. Two caps that hold for every construction (rigorous)

**Theorem A (pulse-count cap).** Every robust section inside a q-pulse family has dimension at most qk. In
particular, every two-pulse section has dimension at most 2k <= n + 1.

*Proof.*
- Inside the family, the history is determined by the q memory states (z_1, ..., z_q) in R^(qk). The realized inputs
  x_t = atanh(h_t) - R h_(t-1) - b are continuous functions of them.
- For a section X: S^(m-1) -> family with m - 1 >= qk, Borsuk-Ulam applied to u -> (z_i(X(u)))_i in R^(qk) gives u
  with X(u) = X(-u). Those histories have identical answers, so they cannot be separated. ∎

**Consequence.** Two pulses (indeed any bounded number q = O(1)) can never produce superlinear robust dimension. A
superlinear section must use an unbounded number of active steps.

**Theorem B (single-query cap).** If a section's antipodal separations are all witnessed by ONE fixed permitted query,
its dimension is at most r = k - 1.

*Proof.* For a fixed xi the selected answer w_R (B_T^T xi) H^T is determined by the r-vector B_T^T xi, which is
continuous in the history. Apply Borsuk-Ulam into R^r. ∎

**Consequence.** Exceeding r (and in particular any superlinear section) requires queries that depend on the section
point.

## 2. Exact structure of the stationary block (rigorous lemmas)

**Lemma 1 (Householder leak).** For every c in NC:

    O e_c   = e_c + ell,   ell   = c_k e_2 + c_k^2 e_1 - c_k^2 1_k,
    O^T e_c = e_c + ell',  ell'  = c_k e_d + c_k^2 e_1 - c_k^2 1_k,
    O^2 e_c = e_c + ell_2, ell_2 = c_k e_3 + c_k^2 e_1 - c_k^2 1_k.

The leak vectors are common to all c in NC. ell' has zero e1 component.

*Proof.*
- **Ingredients.** U e_c = e_c + c_k w for c ≠ 1. U 1_k = sqrt(k) e_1. P_d e_1 = e_2 and P_d^T e_1 = e_d. Also
  (c_k + c_k^2)/sqrt k = c_k^2.
- **First line.** O e_c = U(P ⊕ I)(e_c + c_k w) = U(e_c + c_k e_2 - (c_k/sqrt k)1). This expands to
  e_c + c_k e_2 + (c_k + c_k^2) w - c_k e_1, which is the stated formula.
- **Second line.** The same computation with P^T.
- **Third line.** O ell = c_k O e_2 + c_k^2 e_1 - c_k^2 O 1. Here O e_2 = e_3 + c_k e_2 + (c_k + c_k^2) w - c_k e_1 and
  O 1 = sqrt(k)(e_2 + c_k w). Collecting terms with c_k^2 sqrt k = c_k + c_k^2 gives O ell = c_k e_3 - c_k e_2, hence
  ell_2 = ell + O ell. ∎

**Lemma 2 (stationary credit rows).**
- Let X_s = sum_(i<s) a^i O^i and m_s = sum_(i<s) a^i. Then X_s^T e_c = m_s e_c + Lambda_s for every c in NC, with a
  common Lambda_s.
- After gates G that equal a constant gamma on the pulsed NC coordinates, the same form persists with modified scalars
  and common vectors.

*Proof.* (O^T)^i e_c = e_c + sum_(j<i) (O^T)^j ell', by induction from Lemma 1. ∎

The common-structure claims hold numerically to <= 1e-10 in the reference (collapse_lemma_check.json). On the actual
dense model V_NC = mJ + 1 Lambda^T holds to 4.5e-9 (dense perturbation).

## 3. Theorem C: one pulse already gives about n/4 (rigorous)

**Theorem C.** Fix n >= 200. Let L' = 2 floor(L/2), and let NC' be the first L' coordinates of NC with alternating
signs s_c = (+, -, +, -, ...).

**Section.** u ranges over the closed unit ball of the zero-sum subspace Z = {u in R^(L'): 1^T u = 0}, which has
dimension L' - 1. Prescribe

    h_0 = 0;  h_t = (0_k, H) for t = 1..N+1 with N = 3n;
    h_(N+2) = (z(u), H),  z_c(u) = s_c sqrt(0.08(1 + u_c)) on NC', 0 elsewhere;
    h_(N+3) = 0,

and realize inputs x_t = atanh(h_t) - R h_(t-1) - b with the actual R.

**Query.** One permitted future input: v = 0.45 on NC and 0.2 elsewhere, at h = 0.

**Conclusion.** Every history is admissible, ends exactly at h = 0, and every antipodal pair has permitted-query
half-separation

    >= 0.4 · t0 · a^2 · (m/n) · sqrt(l/n) · |E| - 1e-10 >= 0.00161 > epsilon,   t0 = 0.08,

with m = n(1 - a^(3n+1)) and E defined in step 3. Hence the fixed-feature robust dimension is
>= L' - 1 >= floor(n/4) - 2, about twice the reviewed floor(n/8).

*Proof.*

1. **Admissibility over the whole ball.**
   - Since |u_c| <= ||u|| <= 1, z_c^2 lies in [0, 0.16].
   - Pulse-step memory inputs: |atanh z_c - 0.05| <= atanh(0.4) + 0.05 < 0.4737.
   - Final step: memory input -(aOz) - 0.05 - (dense). By Lemma 1, O z = z + (1^T z) ell.
   - Bound on 1^T z: with alternating signs and L' even,
     |1^T z| = |sum s_c (sqrt(0.08(1+u_c)) - sqrt 0.08)| <= sqrt(0.08) ||u||_1 <= sqrt(0.08 L') <= sqrt(0.04k + 0.08).
   - Coordinate 2: |(Oz)_2| <= c_k sqrt(0.04k + 0.08) <= 0.225 (k >= 100).
   - NC coordinates: |(Oz)_c| <= 0.4 + c_k^2 sqrt(0.04k + 0.08) <= 0.425, so the input is <= 0.995(0.425) + 0.05 + tiny
     < 0.473.
   - Coordinate e1: ell_1 = 0. Other coordinates: <= 0.025.
   - Source and warmup inputs are as in the accepted construction (< 0.4737).
   - **Endpoint:** h = 0 exactly, by construction.

2. **Exact affine sensitivity.**
   - Only the pulse gate depends on u: G_p(u) = G_p(0) - t0 diag(u) on NC'.
   - Therefore B_T(u) = R G_p(u) V + E with V = R B_(N+1) + E. Antipodal answers differ by exactly
     -2 t0 V^T (u ∘ y), with y = R^T xi = (R^T)^2 g/(beta sqrt n).

3. **Reference structure.**
   - V0 = E X_(N+1), so by Lemma 2 its NC rows are m ê_c + Lambda. The reference answer is
     V0^T (y0 ∘ u) = sum_c u_c y0_c (m ê_c + Lambda).
   - By Lemma 1, ((O^T)^2 g)_c = g_c + ell_2^T g for c in NC, so y0 is CONSTANT on NC:

         y0_c = a^2 E/(beta sqrt n),
         E = g_lo + (c_k + c_k^2) g_hi - (1 + c_k)^2 (f g_lo + (1 - f) g_hi),   f = L/k,

     using k c_k^2 = (1 + c_k)^2.
   - For zero-sum u the answer is therefore exactly y0 m û, with norm |y0| m ||u||. The Lambda term cancels because
     1^T u = 0.

4. **Lower bound on |E|.**
   - E'(c) = (1 + 2c) g_hi - 2(1 + c)(f g_lo + (1 - f) g_hi) < 0 on [0, 1/9], since 1.149 < 1.573.
   - Hence E(c_k) <= E(0) = -2(1 - f) s_g, so |E| >= 2(1 - f) s_g.
   - 1 - f = d/k >= 0.495 for n >= 200, so |E| >= 0.0760.

5. **Dense transfer.** ||V - V0|| <= e n + a e n^2 (accepted), ||y - y0|| <= 2e/beta and ||y|| <= 1/beta. The
   normalized query error is therefore <= 0.032 e n^1.5 < 1e-10.

6. **Constants.**
   - Half-separation for unit u: w_R ||H|| t0 m |y0| = 0.4 t0 a^2 (m/n) sqrt(l/n) |E|.
   - Bounds: a^2 >= 0.990025, m/n >= 1 - e^-3 >= 0.9502, sqrt(l/n) >= 0.70710.
   - Value: 0.4(0.08)(0.990025)(0.9502)(0.70710)(0.0760) >= 0.0016181.

7. **Topology.** Apply Borsuk-Ulam on the boundary sphere of Z (dimension L' - 2 sphere, L' - 1 coordinates). ∎

**Numerical verification** (verify_single.json; actual dense model, exact whole-sphere minimum = w_R||H|| t0
sigma_min(W) on Z):

| n | Section dim | floor(n/8) | Exact min half-sep | Analytic formula | Uniform bound |
| --- | --- | --- | --- | --- | --- |
| 200 | 49 | 25 | 0.00348 | 0.00348 | 0.00162 |
| 201 | 49 | 25 | 0.00349 | 0.00349 | 0.00162 |
| 202 | 49 | 25 | 0.00345 | 0.00345 | 0.00162 |
| 203 | 49 | 25 | 0.00346 | 0.00346 | 0.00162 |
| 256 | 63 | 32 | 0.00325 | 0.00325 | 0.00162 |
| 400 | 99 | 50 | 0.00291 | 0.00291 | 0.00162 |
| 601 | 149 | 75 | 0.00267 | 0.00267 | 0.00162 |
| 1000 | 249 | 125 | 0.00243 | 0.00243 | 0.00162 |

- The closed form E matches the measured query weights exactly, and y is constant on NC to 1e-12.
- Max input 0.438 on sampled points; the analytic bound is 0.4737.
- |h_T| <= 4e-16.
- Physical input radius about 0.23 (analytic <= 0.44).

The analytic and exact values coincide because the reference answer is exactly |y0| m ||u|| on Z.

**Why the reviewed theorem got only n/8.** Its pairs were built to be exactly O-fixed, so that its admissibility and
projection arguments were simple. Lemma 1 shows that single stationary coordinates leak only along ONE common vector.
The zero-sum constraint on amplitudes cancels that leak in the answer, and alternating signs control it at the reset.

## 4. Two pulses collapse in the strong channel (rigorous lemma)

**Setup.** Two pulses on NC' at times tau_1 < tau_2 = tau_1 + Delta + 1 (Delta >= 1 zero-memory steps between), each
with gate G_i = I - (tau_0 I + t0 diag(u_i)) on NC', followed by the exact reset.

**Lemma C (two-pulse collapse, reference model, any query).** For any permitted future gate vector g, the part of the
selected answer that is linear in (u_1, u_2) is exactly

    -t0 [ (alpha m1 u1 + m2 u2) ∘ ŷ  +  beta(g) m1 u1  +  alpha (u1·ŷ) Lambda1  +  beta(g)(1^T u1) Lambda1  +  (u2·ŷ) Lambda2 ],

where:
- ŷ is the query propagated to pulse 2 and restricted to NC';
- alpha = a^(Delta+1)(1 - tau_0), m1 = m_(N+1), m2 = alpha m1 + m_(Delta+1);
- Lambda1 and Lambda2 are fixed vectors (Lemma 2);
- the scalar leak coefficient is beta(g) = a^(Delta+1) lambda_(Delta+1)^T G_2(0) ŷ_full, with
  lambda_s = O^s e_c - e_c common (Lemma 1).

The bilinear term in (u1, u2) is even, so antipodal differences are exactly twice this linear part.

*Proof.*
- Write M_T = aO G_2 X_2 + I, with X_2 = (aO)^(Delta+1) G_1 X_1 + X_(Delta+1) and X_1 = X_(N+1).
- Differentiate in u_i, apply Lemma 2 to the rows of X_1 and X_2(0), and use
  (O^T)^(Delta+1)-transport e_c -> e_c + lambda for c in NC'.
- This yields ŷ_1 = alpha ŷ + beta 1 on NC', and the formula follows.
- Checked to relative error <= 1.1e-12 for random queries at n = 64–200 and gaps 1–25 (collapse_lemma_check.json). ∎

**Consequences.**
- The strong (gain about m ~ n) channel sees ONLY the combination w = alpha m1 u1 + m2 u2 in R^(L'). The second
  pulse's information collapses onto the first's.
- Information beyond w can travel only through:
  - the single scalar leak beta(g), which multiplies u1;
  - two rank-one terms along the fixed vectors Lambda1 and Lambda2.

  All of these are artifacts of the Householder coupling. ||lambda_(Delta+1)|| is 0.30 / 0.20 / 0.157 at
  n = 64 / 128 / 200, about c_k. On difference directions (w = 0) the Lambda terms combine into
  alpha(Lambda1 - (m1/m2)Lambda2), which nearly cancels: ||Lambda1|| = 20.86 and ||Lambda2|| = 19.54 at n = 200, with
  m1/m2 = 1.068.
- Under any fixed query (Theorem B), and more generally under any query family with beta ≡ 0, two stationary pulses
  supply no additional dimension beyond the L' coordinates of w plus O(1).

## 5. Do the weak channels add dimension? (numerical, actual dense model)

Answers below are exact on the actual dense model. A "worst query" is a vertex search over the permitted box (a lower
estimate of the supremum). Sampled minima over sections are NOT whole-sphere certificates; they are used here only to
show FAILURE of additivity.

**Fixed-query capacities** (explore.log; exact best m-dimensional linear sections, t0 = 0.08, n = 200). Directions
with half-separation > epsilon:

| Design | Directions above epsilon |
| --- | --- |
| Single pulse, NC pairs | 25 |
| Single pulse, NC individual | 49 = L - 1 |
| Single pulse, all memory | 50 |
| Two pulses, NC individual, gaps 1 / 25 / 50 | 50 |
| Two pulses, all memory | 50–51 |
| Two pulses, staggered pairs | 37–39 |

There is no additivity.

**Query-dependent RMS capacities** (rms_capacity.log). The max over box queries is at least the RMS over sign
corners, so these are valid lower bounds. Directions above 2 epsilon:

| Design | n = 200 | n = 400 |
| --- | --- | --- |
| Single pulse, NC | 50 | 99 |
| Two pulses, NC (all gaps) | 50 | 100 |
| Two pulses, all memory | 50–52 | 100–102 |
| Rotating (cycled) coordinates, any number of pulses | 1–2 | 1–2 |

The second pulse's extra 50/100 singular values sit at 0.1–0.2 epsilon.

**Worst-query tests of the collapse directions** (leak_test.log). These are the directions invisible to the best
fixed query (fixed-query visibility about 1e-17):

| Section dimension | Worst-query half-separation |
| --- | --- |
| 1 | 1.0–1.3 epsilon |
| 5 | about 0.75 epsilon |
| 20 | about 0.5 epsilon |
| 45 | about 0.35–0.4 epsilon |

This holds for n = 200 and 400 and gaps 1 and d/2, and does not grow with n. The leak channel can carry at most a
handful of marginal directions at epsilon = 1e-3.

**Cycled block** (demod_test.log, cycle_collapse_test.log).
- A single pulse on rotating coordinates IS visible through worst-case queries. The strong cycle-average credit
  (about n) is read through the query's ±pattern, which is ℓ1 demodulation. Random 20–25-dimensional sections have
  sampled minima of 1.06–1.8 epsilon.
- Two pulses collapse there too. In the frequency-0 channel the two pulses enter only through their rotation-shifted
  sum. Sections inside the two-pulse weak subspace, which holds every cancellation direction, give sampled minima of
  0.15–1.0 epsilon (0.15–0.24 epsilon for dimension >= 5).
- The genuinely separating channels are rotating frequencies j >= 1. Their credit gain is |c(omega_j)| ≈ d/(2 pi j),
  i.e. about 1/(8 pi j) ≈ 0.04/j of the stationary gain. That ratio is width-independent.

## 6. Rotation, mixing, gate values, spacing, dissipation

| Factor | Effect |
| --- | --- |
| Rotation | On NC, O acts as the identity up to one common leak (Lemma 1). Pulses at different times differ only by the scalar alpha, so they collapse. On the cycle, a time gap is a phase shift: frequency 0 sees the shifted sum (collapse); frequency j sees phase-weighted combinations, but only at relative gain about 0.04/j. |
| Mixing (Householder) | Produces the leak channels (beta, Lambda). These are exact, family-specific and weak (Section 5). |
| Gate values | The deviation is bounded by z^2 <= 0.16 (input cube). The section amplitude t0 needs a baseline tau_0 >= t0, so every pulse dissipates at least t0 of its coordinates' credit. Margins scale with t0. |
| Spacing | At least one zero step is needed for admissibility. Spacing changes only alpha = a^(Delta+1)(1 - tau_0) on the strong channel, so it cannot separate stationary pulses. |
| Dissipation | q pulses inside the visible window multiply pulsed credit by (1 - tau_0)^q. Keeping credit visible needs sum tau_0 = O(1) per relaxation time, which caps the per-pulse amplitude near 1/q and erodes every margin. (Heuristic budget.) |

## 7. Strongest supportable dimension, and what superlinear growth would need

**Two-pulse families (rigorous).** floor(n/4) - 2 <= robust dimension <= 2k ≤ n + 1. The lower bound comes from
Theorem C, since a two-pulse family contains single-pulse sections by fixing the other pulse. So it is Theta(n).
Numerically the two-pulse excess over one pulse is O(1) at epsilon = 1e-3 (Sections 4–5).

**What a superlinear construction would need**, all necessary by Theorems A–B, Lemma C and Section 5:
1. **An unbounded number of active steps.** By Theorem A, a bounded number of pulses is O(n).
2. **Section-dependent queries.** By Theorem B, a single query caps at r.
3. **Separation outside the strong channels.** The new information must avoid both collapses: stationary/NC (Lemma C)
   and cycle frequency 0 (shifted sums). It must therefore live in channels that distinguish TIMES, namely rotating
   phases.
4. **Rotating credit at near-stationary scale.** Under pulse-sparse histories the rotating gain is only about 0.04/j
   of stationary, and the dissipation budget prevents brute-force amplitude.
5. **The one loophole visible here: rotation-locked (co-rotating) gate modulation.** Heuristic, not verified.
   - Memory states that co-rotate with O (h_t = O h_(t-1)) cost almost no input (x ≈ atanh(h) - a h - b).
   - Their gates are stationary in the rotating frame, which turns cycle credit into a stationary-like profile at gain
     about n.
   - In that frame each coordinate's credit row records its own age-weight profile, about d^2 numbers in total, so
     O(n^2) information is present in principle.
   - Per gate event, however, its query-visible size appears to be about sqrt(n), not n, since parameter-side columns
     cannot be demodulated.
   - Whether coherent multi-step modulation can amplify those age profiles to visible scale is exactly the open
     question.

## 8. Status

- **Rigorous:** Theorems A, B, C; Lemmas 1, 2, C.
- **Numerical, exact model, sampled for worst queries:** no two-pulse additivity at epsilon = 1e-3 for n = 200 and
  400.
- **Open:** superlinear fixed-feature growth via unboundedly many co-rotating (phase-locked) innovations.
