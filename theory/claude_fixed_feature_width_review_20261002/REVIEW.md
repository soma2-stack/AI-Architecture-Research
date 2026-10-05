# Hostile review: reachable fixed-feature width (commit 4a8a2dc)

Reviewer: Claude (Opus 5.5), 2026-10-02.

- **Target:** theory/reachable_fixed_feature_width_20261002/ (PROOF.md, REPORT.md, CHECKS.md). It has no supporting
  code.
- **My work:** I re-derived every step by hand, then ran `check_section.py` (logs `section.log`,
  `section_check_*.json`) on the ACTUAL dense family at n = 200, 201, 202, 203, 256, 400, 601 and 1000. Total time is
  about 2 CPU-minutes.
- **Also compared:** experiments/fixed_feature_reachable_operator_20261002/REPORT.md (the diagnostic).

## Verdicts

| # | Question | Verdict |
| --- | --- | --- |
| 1 | floor(n/8) section | **VERIFIED.** One joint continuous section over the closed unit ball of R^m, with m = floor((k-d)/2) >= floor(n/8). It is exactly floor(n/8) at every n tested. |
| 2 | Margin | **> 0.0013 for every n >= 200 (proof).** Exact constants give 0.00145–0.00146. The exact whole-sphere minimum for the section's own query is 0.00177–0.00216. |
| 3 | Admissibility, endpoint, radius | **VERIFIED over the whole ball,** not just the axes. Max input 0.4736; h_T = 0 exactly; radius < 0.19 (analytic), 0.181 measured. |
| 4 | Borsuk-Ulam step | **VERIFIED.** No off-by-one: encoders with fewer than m coordinates collide on S^(m-1). |
| 5 | Omega(n) fixed-feature dimension | **ESTABLISHED,** for selected-source queries in the constant-source-feature class. This is not a full-model statement. |
| 6 | Evidence for superlinear growth | **None rigorous.** The theorem's mechanism is commutative and capped near n/4. The diagnostic's tangent fit (n ln n slightly better) is weak, small-width evidence only. |
| 7 | Mixed-tail bound (26) | **Valid amplitude/stability bound, NOT a dimension bound.** Codex's "tail uncontrolled" is correct. |

## 1. Construction and continuity

**Paired vectors.**
- v_j = (e_(d+2j-1) - e_(d+2j))/sqrt 2 has zero coordinate sum and no e1 component, so w^T v_j = 0 and U v_j = v_j.
- Its support lies beyond the first d (cycled) coordinates, so (P_d ⊕ I) v_j = v_j.
- Hence O v_j = v_j, and EVERY combination is O-fixed. Numerically |Ov - v| <= 3e-15 for the pairs and for random
  combinations.
- Orthonormality holds to 2e-16.

**Count.** k - d >= floor(n/4) for every residue of n mod 4, so m >= floor(floor(n/4)/2) = floor(n/8).

**Section.**
- z(u) = sum_j sqrt(0.11 + 0.05 u_j) sqrt2 v_j, with every square root in [0.245, 0.40] on the closed ball.
- u -> z(u) is smooth on a neighborhood of the ball. The single map u -> history is continuous on the whole ball.
- It is one joint section, not separate axes.

## 2–3. Fixed endpoint, admissibility, radius

The trajectory is prescribed: h0 = 0, h_t = (0, H) for t = 1..N+1 (N = 3n), h_(N+2) = (z(u), H), h_(N+3) = 0. Inputs
are x_t = atanh(h_t) - R h_(t-1) - b with ACTUAL R, so the endpoint is exactly 0 for every u. The full forward replay
gives |h_T| <= 1e-17.

**Bounds at R0.**

| Step | Coordinates | Bound |
| --- | --- | --- |
| Warmup | Memory | -0.05 |
| Warmup | Source | atanh(.4) - 0.05 - delta(.4) < 0.374 |
| Pulse | Memory | atanh(z) - 0.05, so |.| <= 0.4736 |
| Reset | Memory | -a O z - 0.05 = -a z - 0.05, so |.| <= 0.45 |
| Reset | Source | -delta(.4) - 0.05 |

The reset bound is exactly where O z = z is needed: without stationarity, (O z)_i could exceed 0.4. The dense
correction is <= e ||h|| < 1e-9.

**Measured over 66 section points per width** (axes, the uniform and alternating spread corners, random sphere and
random interior points): max |x| = 0.4736 at every n.

**Radius.**
- Only the pulse and reset inputs change.
- Per pair, |sqrt(0.11 + 0.05u) - sqrt(0.11)| <= 0.05|u|/(sqrt(.06) + sqrt(.11)), so ||z(u) - z(0)|| <= 0.1226 ||u||.
- Lipschitz factors: atanh on [-.4, .4] is 25/21-Lipschitz; the reset factor is a.
- Total L2 bound: 0.1226 sqrt((25/21)^2 + a^2) = 0.190 < 0.2. Measured maximum 0.1811–0.1815.

## 4. Query, normalization and margin

**Sensitivity is exactly affine.**
- The only u-dependent gate is the pulse: G_p(u) = G_p(0) - 0.05 sum_j u_j P_j.
- The reset gate is I, and alpha = 1 at both late steps. So B_T(u) = R G_p(u) V + E with V = R B_(N+1) + E, exactly,
  with all n state rows and dense R.
- The midpoint test confirms affineness to 1e-15.

**Reference.** Mpre vbar_j = m_N vbar_j with m_N = (1 - a^(3n))/(1 - a) > 0.95 n. Then
(Bbar(u) - Bbar(v)) vbar_j = -t0 a(a m_N + 1)(u_j - v_j) psi_j.

**Query.**
- Future input 1/5 everywhere except 9/20 on the j_j coordinates. That is inside the accepted box [1/5, 9/20] at h = 0,
  giving gates g_hi and g_lo, so psi_j^T g = sqrt2 s_g.
- The actual adjoint is xi = R^T g/(beta sqrt n). It uses actual R and frozen beta, with w_R/beta = 1/n (measured
  1.0000).
- Measured psi_j^T xi · beta sqrt n = 0.108045 = a sqrt2 s_g, so |d_j| ~ 3e-13.
- The projection onto orthonormal Phi_j = vbar_j H^T/||H|| inside the selected R-group is legitimate. No stronger
  adjoint is used: one fixed, physically permitted query serves every section point.

**Constants.** Leading term t0(.4)(.98)(.95)(.07) = 0.0013034. The corrections are -e sqrt n (inside the bracket) and
zeta_n; both are < 1e-9. So ell_n - zeta_n > 0.0013 > epsilon.

**My exact recomputation.**
- The antipodal difference is linear: (B_T(u) - B_T(-u))^T xi = -2 t0 V^T D(u) R^T xi = -2 t0 Wmat u, where
  Wmat = [V^T P_j R^T xi]_j.
- So the exact minimum over the WHOLE sphere of the selected-block half-separation for this query is
  w_R ||H|| t0 sigma_min(Wmat).

| n | m | Proof's bound (exact constants) | Exact whole-sphere min, this query | Worst box query, sampled sphere points |
| --- | --- | --- | --- | --- |
| 200 | 25 | 0.001446 | 0.00214 | 0.00233–0.00504 |
| 201 | 25 | 0.00145 | 0.00215 | 0.00234–0.00505 |
| 203 | 25 | 0.00145 | 0.00216 | 0.00235–0.00504 |
| 256 | 32 | 0.00145 | 0.00206 | 0.00223–0.00479 |
| 400 | 50 | 0.00145 | 0.00194 | 0.00207–0.00441 |
| 601 | 75 | 0.00146 | 0.00185 | 0.00196–0.00414 |
| 1000 | 125 | 0.00146 | 0.00177 | 0.00186–0.00386 |

The exact minimum is computed directly on the actual dense model, so no transfer is needed. It decreases slowly toward
the projected bound, about 1.46 epsilon, which is width-uniform. The margin over epsilon is thin but genuine.

**Dense transfer.**
- ||B - Bbar|| <= e n^2 and ||V - V0|| <= e n + a e n^2, which give (20): t0 e (n+1)^2 ||u - v||. I re-derived this,
  including the a^2 n^2 + 2an + 1 <= (n+1)^2 step.
- zeta_n < 1e-9.
- The margin after every allowance is >= 0.00145.

## 5. Borsuk-Ulam

- The composite S^(m-1) -> section -> encoder -> R^q with q <= m - 1 has an antipodal coincidence.
- The same endpoint h = 0 and the same length T make the current state and clock useless as discriminators.
- The decoder's answer to the fixed query is identical for u and -u, while the truths differ by > 0.0026 > 2 epsilon.
- So q >= m. This uses continuity of the section only (the history embedding need not be odd), as the proof says.

## 6. Scope: what is fixed, what varies, what is established

| Fixed | Varies |
| --- | --- |
| Source state H = 0.4·1 at every interior step | ONLY the pulse amplitudes on the m stationary pairs |
| e1 = 0 | Hence the pulse gate diag(1 - z^2) on those coordinates |
| Memory zero during the 3n warmup | The pulse and reset inputs |
| Warmup length, pulse time, reset, endpoint 0 | |
| Selected group R_(memory 2..k, source) | |

The queried object is the selected-source gradient.

**Established:** finite-radius, fixed-endpoint, query-visible robust dimension >= floor(n/8) for the reachable
fixed-feature operator family. It is generated purely by gate variation, since the feature never changes. The
fixed-feature bounds are floor(n/8) <= d <= (floor(n/2) - 1)^2; the upper is the r^2 recursion, with error < 2e-9.

**Not established:** anything about the full model. Full bounds remain Omega_c(n^2) <= d_rob <= O_c(n^2 log n). The
new Omega(n) is far below the accepted Omega_c(n^2), which uses features.

**Mechanism is commutative.**
- On the paired subspace O acts as the identity, and the pulse is diagonal there. The realized operator variation is
  a commuting, diagonal family: each pair contributes one scalar eigenvalue.
- Repeating pulses on the same stationary directions only multiplies those scalars, so this mechanism is capped by
  dim ker(I - O_*) = k - d ≈ n/4 (n/8 with disjoint pairs).
- Every one-time pulse family is affine in at most r + 1 gate entries, so ANY single-pulse section is capped at r + 1
  ≈ n/2.

## 7. Weak mixed tail (Sections 9–10)

**Check of (24)–(26).**
- The Duhamel identity holds, given the same alpha sequence in both histories, which the class guarantees: B_s - B~_s
  = G_s R (B_(s-1) - B~_(s-1)) + DeltaG_s V~_s, and the adjoint p_s collects the transports.
- Energy (25): ||R^T G p||^2 <= a^2 ||G p||^2 = a^2 (||p||^2 - ||Gamma p||^2).
- (26) follows from block Cauchy-Schwarz.

**What it is.** It is a correct two-history amplitude/Lipschitz bound, not a dimension bound.
- A dimension upper bound needs a continuous low-dimensional summary of gate words with small L_A and L_D, which is the
  encoder problem itself.
- Gamma^dagger blows up as gates approach 1, exactly the hard regime. The kernel term pays 1/sqrt(1 - a^2) ≈ sqrt(n/2),
  as the earlier ledger did on gate-1 rows.
- Codex's conclusion that the joint mixed tail is uncontrolled is correct.

## 8. Relation to the numerical diagnostic

The diagnostic used broad irregular aperiodic, non-commuting gate words over many times. Its counts per width
(n = 16–96):

| Measure | Count |
| --- | --- |
| Tangent lower counts | about 2.3–2.4 n |
| Finite radius-0.05 single-axis passes | about 0.65 n |
| Sampled 20–32-dimensional joint spheres | Separated |

It noted that n ln n fits its tangent counts slightly better than n.

The theorem captures the ORDER (linear) with a rigorous joint section. But it uses a special, commutative,
single-pulse, stationary-subspace mechanism at about n/8, below the diagnostic's ~0.65n finite axes. It does not realize
the diagnostic's rotating-mode, multi-time directions or its weak tail. So it is a specially constructed linear subset,
not the same structural mechanism. It neither confirms nor refutes the diagnostic's possible n ln n tangent trend.

## 9. Strongest remaining obstruction

Superlinear fixed-feature growth requires:
- an unbounded number q of time-separated gate innovations (each one-time pulse is capped at r + 1);
- acting on ROTATING, non-stationary modes, because the stationary mechanism is capped near n/4;
- whose effects stay jointly separable at finite radius after rotation, mixing and dissipation. The diagnostic's
  supplement already saw stronger gates dissipating credit without gaining directions.

The obstruction is joint finite-radius control of these multigate, non-commuting innovations. No width upper (26 is
amplitude only) and no multi-pulse joint section exists.

## 10. Recommended next theorem

**Two-pulse additivity in the fixed-feature class.** Prove or refute that two time-separated pulses acting on rotating
(non-stationary) modes yield a joint continuous fixed-endpoint section of dimension greater than r + 1, the cap for any
single pulse, with a width-independent margin above epsilon.

- **Positive:** the first rigorous evidence that independent gate innovations ADD robust dimension. That is the
  necessary mechanism for superlinear growth, and it would leave a q-pulse/dissipation-budget question.
- **Negative:** a mechanism (rotation-induced collapse or dissipation) that would point toward an O(n) fixed-feature
  bound.

This is the smallest step that tests superlinearity at all. Anything within one pulse, or within the stationary
subspace, provably cannot.

## Evidence

- **Checks:** `check_section.py`, `section.log` and the JSON outputs.
- **Not modified:** Codex's files. Nothing was committed.
