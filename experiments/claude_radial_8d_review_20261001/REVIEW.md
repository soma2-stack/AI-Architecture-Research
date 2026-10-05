# Hostile review: exact-elimination / sharp-gate / radial-Taylor refinement of the frozen 8D certificate

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** experiments/radial_taylor_refinement_8d_20261001.
- **Commits:** preregistration and freeze 902d449 (pushed 17:41:30); result b230aed.
- **Claim:** the SAME accepted 8D section (candidate c83a242f…) is re-certified at epsilon = 1e-3 with weakest
  guaranteed separation 0.0022943344 (face 7), instead of 0.0020489061. The endpoint, candidate, metric, query family,
  epsilon and fixed-h contract are unchanged.

## Verdict

**REFINEMENT VERIFIED.** The 8D certificate stands with weakest guaranteed separation 2beta_7 = 0.0022943344 > 0.002
(14.72% relative slack).

The 54.8–67.6% cubic-penalty reduction comes from valid mathematics:
- an exact algebraic identity on the exact fixed-h section;
- provably sharp tanh-derivative maxima;
- a correct integral-remainder weighting.

It does not come from a changed domain, metric, epsilon, query family or candidate. No eliminated term can re-enter.

## The three refinements

| Component | Mathematics (re-derived) | Implementation / numerical attack |
| --- | --- | --- |
| **Exact final-input elimination** | Normals are exactly the last input (B rows 144–147 = I; earlier normal rows zero). On the exact section h_T = h*, so x_T = W^-1(atanh h* - Dv - b) for every t. This holds however the tangent's own last-row entries are compensated. RTRL at fixed realized inputs gives s_T = g*(r s_{T-1} + direct). The final gate is the constant g* = 1 - h*^2. The W-injection x_T depends on t only through v = h_{T-1}. Hence l.s_T = C_S.s_{T-1} + C_h.v + const exactly. I re-derived C_S = l g* r, and C_h with the R-term l w_R g* and the W-term -r_z sum l w_W g* (W^-1)_{l z}, by hand; bias contributes only a constant. | My own 60-digit computation of C_S and C_h from scratch lies inside their interval enclosures (relative 9e-55). On the TRUE section (my Newton lifts; no elimination assumed), Phi(t) - Phi(0) equals C_S dS_{T-1} + C_h dv to 6.5e-15 (relative 5.8e-15) at 60 points, including corners. The prefix is verified independent of the normals. |
| **Sharp gate bounds** | p1..p4 = 1-H^2, -2H+2H^3, -2+8H^2-6H^4, 16H-40H^3+24H^5 are the tanh derivatives in H. Their critical-point lists are complete (0; +/-sqrt(1/3); 0, +/-sqrt(2/3); +/-sqrt((15 +/- sqrt105)/30)). The max of \|p\| on an interval is at an endpoint or a critical point; root enclosures are outward and included when intersecting; min with the natural bound is valid. | 12,000 exact rational comparisons against 50-digit true maxima on adversarial intervals (straddling, touching or just missing every critical point; 192 and 256 bits): 0 violations. Sharp <= natural, elementwise, on all saved arrays. |
| **Radial Taylor integration** | g(1) - g(-1) = 2g'(0) + int_0^1 (1-s)^2/2 [g'''(s) + g'''(-s)] ds, hence the bound int (1-s)^2 M(\|s\|) ds. Bands [(j-1)/8, j/8] with M(j/8) valid on the symmetric box \|t\| <= (j/8)a. Weights ((1-l)^3 - (1-u)^3)/3 sum to 1/3, B = (1/2) sum w M, constant M gives M/6, and the face bound is 2mu(1 - e0 - B). No missing factor 2. Capping by the old M3 is valid. | Contraction uses the original a (direction Az, \|z\| <= 1); the sub-box only bounds where the derivative is evaluated. M is monotone in lambda. Odd remainder at 528 boundary antipodes: at most 0.279 x (2B) (face 2), and at most 0.094 x on faces 3–8. |

## Bounds against reality and second implementation

- **Prefix majorants, all 8 radial bands:** autodiff 2nd/3rd derivatives of (v, s_{T-1}) in each lambda-box, plus
  adversarial maximisation. At most 0.99972 of the bound; never exceeded. Small boxes make some entries near-exact.
- **End-to-end:** the true |d^3/ds^3 Phi_i(s z)| on the exact section, at 1,500 (z, s) samples, reaches at most 0.29 of
  the relevant band's M(lambda) (face 2). That is at least 3.4x slack on every face and band.
- **Clean-room engine** (separate mpmath directed rounding and Taylor jets; my copy, unmodified) on the 36-step prefix
  with zero normal width:
  - it reproduces their eliminated whole-box bound exactly (M ratio 1.000000; HH3/HS3 within 1.4e-14);
  - sharp-gate bands are only 0.003–1% tighter than this independent natural-gate result.
- **Fresh replays in my process (192 and 256 bits):** control arrays and fields, coefficients, native arrays and M,
  all 8 bands, and every beta are identical to stored. 192/256 beta differ by 2.3e-58; prefix arrays are bitwise equal.

## Unchanged contract (checked)

- The candidate is byte-identical (c83a242f…).
- mu and e0 are taken from the regenerated control and equal the accepted 8D values.
- The control (hidden contraction, forcing and inclusion over the FULL normal box) regenerates bit-identically, so the
  exact section still exists with |y| <= a_h.
- The zero normal width in the prefix is not a domain change: the prefix provably does not depend on the normals.
- The tangent amplitudes are unchanged (sub-boxes only bound derivatives).
- epsilon is 1/1000, with the same 7/8-gate query dual and the same Borsuk–Ulam step (S^7, k >= 8).

## All eight faces (7/8-gate metric; true minima from my 8D review, 50-digit confirmed)

| Face | New certified 2beta | True minimum | True / 2beta | Linear ceiling 2mu | Remainder understatement needed to fail |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.0030293635 | 0.0034537 | 1.140 | 0.0034538 | 3.43x |
| 2 | 0.0027767870 | 0.0032421 | 1.168 | 0.0032422 | **2.67x** |
| 3 | 0.0029694214 | 0.0032422 | 1.092 | 0.0032422 | 4.55x |
| 4 | 0.0026452179 | 0.0029376 | 1.111 | 0.0029376 | 3.21x |
| 5 | 0.0027208788 | 0.0028912 | 1.063 | 0.0028914 | 5.23x |
| 6 | 0.0024665399 | 0.0026937 | 1.092 | 0.0026933 | 3.06x |
| 7 | **0.0022943344** | 0.0024073 | **1.049** | 0.0024119 | 3.51x |
| 8 | 0.0026038810 | 0.0029529 | 1.134 | 0.0029379 | 2.81x |

Every certified value lies below the true minimum, which is a necessary consistency check, now within 5–17%. The
earlier 8D certificate failed if M3 was understated by 5.5%. Now every face tolerates a >= 2.67x error in the
integrated remainder.

The true minima essentially equal the linear Cauchy–Schwarz ceiling 2mu_i. For this section, therefore, no further
curvature refinement can gain more than about 5% on face 7.

## Provenance and repairs

- The method, code and frozen hashes were pushed at 17:41:30; the first official output was written at 17:41:52.
- 45 pre-tests and 140 final checks pass.
- The only repair is the publication checker: the initial version matched the digit 9 inside "192", and the fix uses
  an exact filename list. This is packaging only.
- The improvement criterion (>= 2x slack) was frozen beforehand. The achieved slack multiplier is 6.02x.

## Numerical 9D screen (inspected; not a theorem either way)

It is correctly labelled numerical-only: no interval kernel is called. The float refined proxy reproduces the official
8D beta to 3e-18.

**Its negative result is weak even as a screen.** In both winners, faces 7–9 fail already at the linear level
(mu_7..9 = 0.59–0.90 eps), with a_7 = 0.12–0.13, about half its 8D value. Yet no constraint was active: hidden
inclusion was at 11–30%, eta at 0.05–0.07, and the raw radius at 0.15. So the 80-step, two-start SPSA did not find a
good allocation. The sampled actual minima below 2eps condemn only those two specific boxes.

The earlier screen's 10D direct section found no pair below 1.89x 2eps (screen metric), and its 9-axis sub-cube faces are subsets of
its faces. That is numerical evidence that suitable 9D sections exist. The 9D screen must not be read as a 9D
impossibility or ceiling. It also has a recordkeeping gap (disclosed): the 14 initial normal-grid scores were not
saved.

## Strongest remaining weakness

**The new formal step is chart-specific and unmechanized.**
- The exact elimination needs the normals to be exactly the final input, and W to be invertible. It will not transfer
  automatically to other charts or architectures.
- Its two new code pieces (elimination.py, exact_gate.py) are short and hand- and numerically verified. Of these, only
  the coefficients have an independent re-derivation (mine). There is no mechanized proof.

The margin risk itself is now small. A >= 2.67x understatement of the remainder bound would be needed, and true
curvature is at most 29% of the band bounds.

**The certificate now sits near the section's true geometry.** The binding limit is the linear query range (2mu), not
curvature. So higher dimensions need better sections and amplitude allocations, with the hidden-inclusion guards
intact, rather than further remainder tightening.

The scope is unchanged:
- one section and endpoint;
- continuous encoders;
- the accepted query metric;
- no upper bound.

Evidence: review_radial.py, cleanroom/ (unmodified copy of the clean-room engine), logs/ and out/ in this directory.
About 1 CPU-hour in at most 17 single-thread BelowNormal workers; no GPU. No reviewed file was modified, and no
9D/10D search was run.
