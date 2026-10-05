# Hostile review: rebalanced joint 7D antipodal certificate

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** experiments/rebalanced_7d_section_20261001.
- **Commits:** preregistration and method freeze 963e44e; packaging 3685718; candidate freeze 1835b68; result 622e001.
- **Claim:** independent width-4 confirmation has a rigorously certified joint 7-dimensional continuous robust section at
  epsilon = 1e-3, so a continuous encoder needs k >= 7.

## Verdict

**7D CERTIFICATE VERIFIED.** No mathematical, implementation, replay, provenance or contract gap was found. Every
attack below either reproduced the certificate exactly or stayed inside its bounds.

The lower bound k >= 7 holds under the unchanged contract:
- a continuous encoder with no external history;
- permitted late one-step queries, with the support-aware 7/8 gate;
- uniform absolute gradient error epsilon in the unchanged normalized metric;
- one fixed-h section of one endpoint.

It separates antipodal pairs only. It is not a 7-bit or 128-state claim.

## What was checked

| Item | Finding |
| --- | --- |
| **Contract unchanged** | Endpoint and model parameters are identical to the accepted 6D candidate and the failed 7D control. B and L are byte-identical to the failed control (the 2^-128 dyadic rounding was the identity). epsilon is 1/1000 (config and kernel literal). The query code (structured_query, 7/8 gate), base_for normalization (group RMS, sqrt(3/32)) and topology step are hash-verified unchanged sources. |
| **Kernel diff** | The local kernel.py differs from the reviewed 6D kernel (sha c2483d…, the file I reviewed) in exactly the two declared lines. Both sit inside the same per-step loop, so `affine` is the current step's, never stale. The direct deltaW x (raw `xx` interval) and deltaW dx (`u` = \|Btilde\|) sensitivity injections, and every R injection, are unchanged. |
| **Affine tightening: math** | W x_t = W x0_t + (W Btilde_t) w is exact at fixed theta. Enclosing C = W Btilde and v = W x0 outward, with radius sum_k sup\|C_ik\| a_k, is a valid enclosure. D_k(W x_t) = C_ik exactly, and higher chart derivatives of W x_t vanish. Hence \|D_k a_i\| <= sum_j \|R_ij\|\|D_k h_j\| + sup\|C_ik\|. This is a valid majorant; the model and metric are not changed. |
| **Affine tightening: rounding** | I(x).hi is a ceiling and absq() is the outward max, so the raw interval [-ceil(rad), ceil(rad)] contains [-rad, rad]. The center W x0 + b uses outward interval products. `uq` rounds up. |
| **Affine tightening: exact attack** | 60-digit trajectories at every sign corner of every C_t,i (296), plus 40 random corners: the preactivation is always inside the captured 192-bit enclosure (worst excess -4.0e-58, tight at t = 0 as expected), and \|dpre\| <= ax everywhere (worst -1.3e-37). 800 float points plus adversarial L-BFGS-B extremisation: contacts only at rounding level. |
| **Tightening is load-bearing** | The same frozen candidate through the unchanged accepted kernel FAILS: hidden self-mapping, forcing 0.0304 against allowance 0.0124, eta 0.142. The 7D result therefore depends on the new substitutions; there is no fallback to the previously reviewed kernel. Elementwise the new bounds are <= the old (max ratio 0.9996). |
| **Mixed 2nd/3rd derivatives** | Autodiff at 72 points of the 11-D box (half corners): max actual / bound is 0.99896 (third order) and 0.99730 (second order). Adversarial maximisation over the box of the tightest 12 entries per order (two seeds) converges to 0.99896 and 0.99731. Never exceeded, but the tightest entry (dh_2/dy_1^3) has about 0.1% slack. |
| **Implicit y''' end to end** | Finite-difference D^3 Phi along the curved exact section (120 points and directions): at most 9.2% of the certified selected3 bound. |
| **Third-order remainder** | The 1/6 Taylor factor and the face bound 2(1 - e0 - M3/6) are as accepted in 6D, and dimension-generic. At 464 boundary antipodes (all 64 corner pairs plus 400 face points), \|Phi(z) - Phi(-z) - 2DPhi(0)z\| <= 0.084 x (M3/3) on face 1 and <= 0.032 x (M3/3) on the others. Max \|DPhi(0) - I\| = 1.2e-15. |
| **Fixed-h lift, contraction, forcing** | Exact recheck: eta_h = 0.0441 < 3/4, and every mapped forcing <= (1 - eta_h) a_h (max ratio 0.5825). Radius 0.115 <= 1. Directly measured: true forcing \|Kh(h(0,t) - h0)\| is at most 17% of the certified bound (2.1% of the allowance), true contraction 0.0037, Newton lifts use <= 2.0% of a_h, residuals <= 1e-16 (float) and 3e-52 (mp). |
| **Query margin** | My own 80-digit computation of the support-aware mu~ from exact (K L)_i / a_i reproduces the stored values to 1e-55 relative, and the stored values are lower bounds. |
| **Exact face arithmetic** | beta_i = mu_i (1 - e0_i - M3_i / 6) re-derived exactly from the stored rationals and upward floats at both precisions. All seven beta_i > 1/1000. Face 7: 2 beta_7 = 0.0026222927508 (exact rational stored), 2 beta_7 - 2 eps = 6.22e-4. |
| **Replays** | Fresh cache-free 192- and 256-bit runs of the local kernel are identical to result.json and bounds_*.npz in every field and every array. |
| **Antipodal separation, all faces** | Screen, multistart L-BFGS-B, sub-face and differential-evolution searches, base plus 3x deep on faces 1, 3, 5, 6, 7, each 50-digit confirmed. Every minimum sits at the face centre. D78 / 2 eps, faces 1–7: 2.84, 2.51, 2.04, 3.56, 1.85, 1.97, **1.61**. D78 / 2 beta: 2.16, 1.10, 1.56, 1.24, 1.41, 1.50, **1.23**. |
| **Face 7 attack** | The minimum D78 = 3.2189951636e-3 (50 digits) at z ~ e_7, against certified 2 beta_7 = 2.6222927508e-3. Of the gap log(D78 / 2 beta) = 0.205, 0.208 is the M3 majorant, while the query range is 1.6e-6 and the true remainder -0.003. The true face-wide third derivative is about 3.2% of M3_7. |
| **Joint 7D** | One cube. The hidden section is solved simultaneously over the closed 7D tangent box. M3_i sums all mixed cubic terms over all seven amplitudes, so the 2.71x axis-2 increase is charged to every face's penalty. |
| **2.71x axis-2 change** | Exactly 67241/1048576 / old a_2 = 2.7096. It lifts mu_2 out of the old linear shortfall: face 2 is now 2.29 eps with penalty 0.087. The rounding (tangent down to 2^-20; hidden x 51/50 then up) was replayed exactly. |
| **Chronology** | The method commit 963e44e was pushed at 13:37:32, before any search output (13:40+). The winner freeze 1835b68 was pushed at 13:50:47, before the bounds and result files (13:51). The winner is the highest of the six scores (original_302702, 1.31115). All METHOD_FROZEN (19 local, 65 source) and CANDIDATE_FROZEN hashes verify. |
| **Borsuk–Ulam** | The face inequalities cover every boundary point z with its antipode -z. The cube boundary is homeomorphic to S^6, and z -> E(x(y(Az), Az)) is continuous, because the fixed-h section is continuous by the contraction. An encoder into R^6 must identify some antipodal pair, so k >= 7. No off-by-one. |

## Documentation notes (no effect on validity)

1. REPORT's numerical face minima (for example face 7, 0.0034582) are in the higher sech^2(1/4) gate metric. Converted to
   the certificate's 7/8 metric they are 7.4% smaller: face 7 is 0.0032190, which is 1.61 x 2eps and 1.23 x 2beta.
2. REPORT says the run "does not isolate" allocation versus tightening. The accepted-kernel diagnostic above settles it
   for this box: without the tightening the hidden section itself cannot be certified.
3. The copied reason string "6D certified" is cosmetic, as REPORT discloses.

## Strongest remaining weakness

**The result now rests entirely on the new tightened kernel.** It is unmechanized and has had one independent review
(this one) plus numerical attack, but no second interval implementation. The tightening makes several derivative
majorants almost exact: the tightest entry reaches 0.9990 of its bound. Those entries have no slack to absorb an
implementation slip, although end-to-end slack stays large (true D^3 Phi <= 9% of bound).

**The most cubic-fragile face is face 1, not face 7.** Face 1 fails if M3_1 is underestimated by more than 1.205x;
face 7 needs more than 2.02x. The true face-1 curvature is about 8.5% of M3_1, so the risk is formal, not substantive.

**The scope is narrow:**
- one section of one endpoint;
- continuous encoders only;
- the independent model's own normalized metric;
- the accepted query family;
- no nontrivial upper bound.

## Is 8D the next sensible experiment?

**Not as the immediate next step.**

The method is near saturation:
- faces 3, 5, 6 and 7 are tied at 1.311 eps after max-min optimisation;
- hidden forcing is at 58% of the allowance;
- all slack sits in M3, about 10–30x conservative.

An 8th, smaller-singular-value axis needs larger amplitudes, which raise every row's cubic penalty. It would likely
need yet another kernel refinement, compounding the main weakness.

Higher-value next steps:
- an independent second interval implementation of the tightened kernel (for example mpmath.iv or Arb), which retires
  the main weakness;
- a nontrivial upper bound, which brackets the dimension;
- a scaling question across n or T.

If the owner still wants 8D, a float-only feasibility screen of the 8th direction's linear range under the
hidden-inclusion and domain limits should precede any preregistered interval run.

Evidence: review7d.py, logs/ and out/ in this directory. Roughly one CPU-hour in at most 14 single-thread workers at
BelowNormal priority; no GPU. No file in any reviewed directory was modified.
