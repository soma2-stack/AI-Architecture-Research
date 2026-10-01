# Direct antipodal-separation audit of the frozen 7D section (preregistration)

Claude lane, 2026-10-01. This file was written before any 7D face separation, lift on a face, or curvature sample was computed. Its SHA-256 and timestamp are recorded in `RUN_LOG.md` before the first audit run. It is not committed to Git unless the owner asks.

## Target (read-only; nothing in it is changed)

`experiments/third_order_antipodal_7d_20261001/`. The following are used exactly as frozen:

- candidate `candidate.json`, SHA-256 `4d6ca2c2804790b55f24f4125471f322ca1f324252b3a1a173ef5bb3e2bf8c9c`;
- endpoint `independent_n4_confirmation` (n=4, horizon 37, P=24) and its model parameters;
- the 11-column basis B (4 hidden-normal plus 7 tangent columns) and the 7×24 projection L;
- the preconditioners K_h and K;
- tangent half-widths a_1..a_7 and hidden half-width a_h = 8161/2^20;
- epsilon = 1/1000.

The official certificate (`result.json`) is used only for comparison: beta3_i, M3_i, mu_tilde_i and center rows e0_i.

## Primary question

On each face of the 7-cube, is the actual antipodal query distance above 2ε = 0.002? Separately, how does it compare with the certified lower bound 2β_i?

## Exact objects (unchanged definitions)

- **Chart:** history x(y,t) = X0 + sqrt(3/32)·B(y,t). The tangent is t = A z with A = diag(a), z ∈ [-1,1]^7.
- **Fixed-h lift:** y(t) solves h(x(y,t)) = h0 exactly. It is solved by Newton's method from y = 0 to a residual ≤ 1e-14 in float64, and then confirmed in 50-digit arithmetic at every reported point. The solution must satisfy |y|_∞ ≤ a_h.
- **Normalized sensitivity s:** the final-time S, restricted to the 24 owner-supported entries and multiplied by the parameter-group RMS. This is the accepted normalized gradient metric.
- **Query metric, the exact allowed one (unchanged):**
  - D_C(Δs) = sqrt(Σ_d c_d² Δs_d²) with c_d = sech²(1/4)·R_ii / sqrt(n·max(1, Σ_j R_jj²)), where i is the owner row of d.
  - This is the all-high-gate maximum from `robust_certificate_tightness_20261001/INDEPENDENT_QUERY_SLACK.md`, using the same normalization as `structured_query`.
  - The certificate's realizable relaxation D_7/8 is the same expression with sech²(1/4) replaced by 7/8. It is reported separately and is not used for classification.
- **Face i:** z_i = +1, with the other six coordinates in [-1,1]. The antipode is -z. Faces z_i = -1 are the same set of pairs.
- **Phi(z):** A^-1 K (L s(z) - L s(0)). ΔΦ_i = Φ_i(z) - Φ_i(-z).

## Validity checks (before any face search; failure leads to INCONCLUSIVE with the reason)

- **V1.** The frozen hashes verify, and nothing in the frozen folder changes during the audit.
- **V2.** My float64 mu_i reproduces `result.json` mu_tilde_i to a relative error ≤ 1e-9.
- **V3.** DΦ(0), from the exact implicit section Jacobian, satisfies max|DΦ(0) - I| ≤ 1e-6. This confirms the parameter ordering, the basis, L and K.
- **V4.** At every evaluated point the lift converges with residual ≤ 1e-12 and |y|_∞ ≤ a_h.

## Search per face (all seven faces; deterministic seeds)

Objective: f_i(u) = D_C(s(z) - s(-z)) with z = (u inserted at position i, z_i = 1), u ∈ [-1,1]^6.

- **A. Coarse screen:**
  - all 3^6 = 729 points of {-1,0,1}^6, which include all 64 corners and every lower-dimensional boundary centre;
  - plus 256 scrambled Sobol points (seed 7000+i).
- **B. Local multistart:** L-BFGS-B with an exact gradient (implicit-function section Jacobian), box bounds, gtol 1e-10. It starts from the 40 best A points plus 40 uniform random starts (seed 7100+i).
- **C. Independent global method:** SciPy differential evolution on [-1,1]^6 (popsize 15, maxiter 60, seed 7200+i, polish = L-BFGS-B).
- **D. Boundary search:** for every free coordinate k and sign σ ∈ {±1}, fix u_k = σ (a codimension-2 face of the cube) and run L-BFGS-B from the 5 best A points restricted to that sub-face. That is 12 sub-faces × 5 runs.
- **Weakest face:** face 5, the certified weakest, gets doubled counts in A-random, B, C popsize and D starts. After all faces finish, if the face with the lowest actual minimum is not face 5, it receives one escalation round on the face-5 budget with new seeds (+50).
- **Reliability:** a face is reliable if the best values from B ∪ D and from C agree within 1%. Otherwise it receives one escalation round: 3× the B starts, and C with seed +100 and popsize 30. After escalation the face is reliable if the escalation best lies within 1% of the pre-escalation best.
- Each face's best point is recomputed in 50-digit arithmetic (lift, s(±z), D_C, D_7/8, ΔΦ_i) and must agree with float64 to a relative error ≤ 1e-8.

## Classification (exactly one; m = min over faces of the confirmed best D_C)

- **7D SECTION LOOKS TOO WEAK AT EPSILON:** some face has a confirmed boundary antipodal pair with D_C ≤ 2ε = 0.002, with a valid lift.
- **7D LOOKS REAL — CERTIFICATE IS TOO CONSERVATIVE:** m ≥ 1.05 × 2ε, and every face is reliable.
- **INCONCLUSIVE:** anything else, including 2ε < m < 1.05·2ε, any unreliable face, or any validity failure.

The classification is numerical. A numerical minimum is not a rigorous 7D theorem and will never be reported as one. Reaching LOOKS REAL would mean only that a sharper sufficient certificate is worth attempting.

## Slack attribution (diagnostic, fixed now)

For each face, take the D_C minimiser z*. At that point the certified chain is

D_C ≥ D_7/8 ≥ μ_i|ΔΦ_i| ≥ 2μ_i(1 - e0_i - G_i/6) ≥ 2μ_i(1 - e0_i - M3_i/6) = 2β_i.

Here G_i = max over s ∈ [-1,1] of |d³/ds³ Φ_i(s z*)|. It is estimated by fourth-order central finite differences on 41 values of s, cross-checked at step sizes 0.02 and 0.01.

The log-ratios of consecutive terms are attributed as follows; they sum to ln(D_C(z*)/2β_i):

| Term | Ratio | Attributed to |
|---|---|---|
| gate | D_C / D_7/8 | another term: the 7/8 versus high-gate relaxation; a constant |
| query | D_7/8 / (μ_i ΔΦ_i) | linear query range: the Cauchy–Schwarz projection margin μ |
| remainder | ΔΦ_i / 2(1 - e0 - G_i/6) | third-order remainder: the Taylor step given the true ray curvature |
| curvature | (1 - e0 - G_i/6) / (1 - e0 - M3_i/6) | interval curvature: the whole-box majorant versus the true third derivative |

The largest term on the actually weakest face is the primary answer to where the margin loses the most slack. The full table is reported for all faces.

Further diagnostics:

- The face-wide true-curvature estimate Ĝ_i is the maximum of G over 200 seeded random face rays plus 64 face corners. From it, the oracle bound 2μ_i(1 - e0 - Ĝ_i/6) is reported.
- min |ΔΦ_i| over the face is found by L-BFGS-B from 20 starts. The face-minimum ladder 2β ≤ oracle ≤ μ·min|ΔΦ| ≤ min D_7/8 ≤ min D_C is reported.

All of these are diagnostics. None is a certificate.

## Resources and stops

- CPU only, with OMP/MKL threads set to 1 and BelowNormal priority. At most 20 single-thread processes, with a total cap of 6 CPU-hours.
- No GPU, no 8D, no new candidate, amplitudes, basis, epsilon, metric or architecture.
- Stop after the classification and the slack table.
