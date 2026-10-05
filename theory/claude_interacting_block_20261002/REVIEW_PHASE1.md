# Phase 1: independent review of Codex's two-pulse / co-rotating stage (commit ea0ebd7)

Claude (Opus 5.5), 2026-10-02.

- **Target:** theory/codex_two_pulse_corotating_20261002/ (REPORT.md, VERIFICATION.md, SCOPED_THEORY.md and code).
- **Method:** hand re-derivation, plus my own reduced-block implementation (`block.py`), which does not import Codex
  code.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | One-pulse lower bound 2floor((k-d)/2)-1 >= floor(n/4)-2, half-margin > 0.00161 | **VERIFIED.** This is my Theorem C; Codex's re-derivation agrees. With the corrected constants the rounded product is 0.0016177 > 0.00161. **Remark (new):** the accepted contract permits future preactivations up to 3/4 (inputs may leave the past cube). Using v = 0.70 on the stationary block gives exact minima 0.0050 / 0.0046 / 0.0043 (n = 200/400/1000) and a uniform analytic margin > 0.0032 (s_g' = 0.1527). |
| 2 | Bounded numbers of fixed-time pulses: Theta(n) | **VERIFIED, correctly scoped.** The upper bound qk comes from Borsuk-Ulam on the pulse states, and an exact counted encoder is also given. The lower bound holds only when the family contains the one-pulse configuration (other pulse states fixed, at least 3n warmup before one pulse). Growing q is not covered. |
| 3 | One fixed co-rotating profile: Theta(n) | **VERIFIED, scoped.** O^d = I exactly makes the gates d-periodic; the period affine map is exact; z has r = k-1 coordinates. The lower bound comes from T = 1 (one-pulse section). No lower bound is claimed for each fixed large T, and Codex says so. |
| 4 | Changing latent-cycle profiles reduce to one scalar plus a d x d block | **VERIFIED.** See below. My own implementation matches the full r-block recursion to 3e-13 (n = 64) and 7.5e-12 (n = 128). |
| 5 | Finite-error upper with d^2 + 1 credit coordinates | **VERIFIED.** The encoder stores (s, C) exactly in the reference; dense error < 2e-9. It is a quadratic cap (d^2 ≈ n^2/16), stronger than r^2 by about 4x, and decides nothing for q ≈ ln n charts (q(d-1) < d^2 + 1), as Codex states. |
| 6 | Long SUSTAINED profiles cannot keep superlinear (indeed > 1) robust dimension asymptotically | **VERIFIED, with scope made explicit.** See below. |
| 7 | Loopholes: short windows and weakening gates | **CORRECTLY IDENTIFIED.** Short means T ≲ 409(6.4 + 0.5 ln n) at large n (beyond that the warmup term dies). "Weakening" means B, P → 0 so that u → 1 and lambda → 1. |

## Detail on claims 4–6

**Claim 4: reduction.**
- For a zero-sum latent cycle vector x, the physical memory state h = Ux satisfies h_1 = 0, h_i = x_i + c_k x_1 on
  physical 2..d, and h_c = c_k x_1 on every stationary coordinate. Proof: w·x = x_1 and 2/||w||^2 = sqrt(k) c_k.
- So stationary gates are equal at each step.
- Z_NC (zero-sum stationary vectors) is pointwise O-fixed and gate-scalar. Its complement inside e1^⊥, spanned by
  V = [e_2..e_d, 1_NC/sqrt L], is invariant under O and every gate.
- The identity injection splits as P_Z + V V^T, giving M = s P_Z + V C V^T exactly.

**Claim 6: dissipation.** I re-derived each step:
- |h_i| >= 0.14 - 0.36 c_k >= 0.10;
- gates <= 0.99 on the d-1 cycle coordinates;
- q = e^T O_A e = 1 - L c_k^2 (from O 1_NC = 1_NC + L ell);
- the factorization G = D Gbar with ||D|| <= 1;
- the two-gate energy identity;
- the overlap bound 1 - |q|;
- the triangular-map norm <= 2 - u;
- 199/20402;
- the 412 bound (1 - lambda >= delta/2).

Scope:
- B = 0.25, P = 0.11, d even.
- The bound is eta + 0.3[sqrt(n) lambda^floor(T/2) + 412/sqrt n]. It is below epsilon only for n ≳ 1.5e10 (from the
  412 term) and T ≳ 409(6.4 + 0.5 ln n).
- It is an asymptotic statement with an astronomically large crossover. Codex says so.

## Corrections Codex made to my earlier write-up (all valid; no conclusion changes)

1. I misused a <= 0.995 in one admissibility bound. a < 1 gives 0.475 < 0.5.
2. The rounded product is 0.0016177, not >= 0.0016181.
3. "Exact" agreement of actual and reference numbers holds to displayed precision only.
4. "Co-rotating gates are stationary in the rotating frame" is false as a literal identity. Codex's commutator
   t^2 c_k^2 (e_3 + e_4) is correct. The exact replacement is Lemma B3 in THEORY_PHASE2.md: diagonal plus a rank-two
   twist plus a small tilt, in an explicit cyclic basis.
5. "Rotating channels are necessary" was a hypothesis, not established by sampled non-additivity.

## Reproduction of Codex's adversarial pairs

From Codex's saved coefficients only (`codex_pairs.py`, independent implementation), the numbers match exactly:

| n, start | Envelope / 2 epsilon | One-step box lower |
| --- | --- | --- |
| 200, 0 | 7.996 | 0.00115 |
| 200, 1 | 8.794 | 0.00625 |
| 400, 0 | 9.587 | 0.00216 |
| 400, 1 | 7.217 | 0.00299 |

New: optimized TWO-STEP permitted queries (preactivations in [1/4, 1/2]) give 0.00075 / 0.00264 / 0.00300 / 0.00165.
They do not approach the kappa envelope (about 0.016). Their realizing future inputs reach 2–4.9, outside the past
cube, which the contract allows for futures.
