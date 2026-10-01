# Direct audit of the frozen 7D antipodal section

Claude lane, 2026-10-01. Target: `experiments/third_order_antipodal_7d_20261001` (candidate `4d6ca2c2…`), read-only and unchanged. The procedure was fixed in advance in `PREREGISTRATION.md` (SHA-256 `f91da22f…`), and every step was run as declared.

## Classification

**7D SECTION LOOKS TOO WEAK AT EPSILON**

This classification is numerical: 50-digit point evaluation plus aggressive minimization. It is not a rigorous theorem in either direction, and it does not show that 7D is impossible at this endpoint. It concerns only this frozen box.

## Answer to the primary question

Both effects are present, but they act on different faces.

- **The certificate is very conservative.** On every face the actual minimum antipodal distance is 1.24–2.82 times the certified 2β_i. Faces 1 and 3–7 actually clear 2ε, by 9.5–126%.
- **The section really is too weak on face 2.** The best antipodal pair there has D_C = 0.0019885118384809833 (50 digits), which is **0.574% below 2ε**. It sits at the face centre z = e_2, i.e. the single-axis pair t = ±a_2 e_2. Its separation is fully explained by the linear range at the frozen amplitude a_2 = 0.023666 (scaled by the 1.0743 gate ratio):

  D_C ≈ (sech²(1/4) / (7/8)) · μ_2 · ΔΦ_2 = 1.0743 · 0.00092550 · 1.99998.

  Curvature, the third-order remainder and the Cauchy–Schwarz projection contribute essentially nothing. No tightening of the remainder, the curvature majorant or the gate could certify this box.
- **The failure is not in the seventh direction.** Face 7 (smallest query singular value, 0.0122) clears 2ε at a ratio of 1.095. The failure comes from the frozen amplitude allocation on axis 2, which has the second-largest singular value but a small width.

## Per-face results (exact allowed metric D_C, high gate)

| Face | Min D_C found | / 2ε | / certified 2β | D_7/8 at min | Minimizer | 50-digit agreement |
|---:|---:|---:|---:|---:|---|---:|
| 1 | 4.5255e-3 | 2.263 | 2.821 | 4.2125e-3 | interior/boundary | 1.3e-15 |
| **2** | **1.98851e-3** | **0.9943** | 1.244 | 1.8510e-3 | face centre e_2 | 1.1e-14 |
| 3 | 2.5607e-3 | 1.280 | 1.602 | 2.3836e-3 | | 1.6e-15 |
| 4 | 2.4941e-3 | 1.247 | 1.560 | 2.3216e-3 | | 2.9e-15 |
| 5 | 2.3318e-3 | 1.166 | 1.459 | 2.1705e-3 | | 1.1e-15 |
| 6 | 2.4634e-3 | 1.232 | 1.540 | 2.2931e-3 | | 1.8e-15 |
| 7 | 2.1906e-3 | 1.095 | 1.371 | 2.0391e-3 | | 1.1e-15 |

Search reliability:

- On every face, the local multistart, the codimension-2 boundary search and differential evolution reached the same minimum, to about 1e-16 relative.
- The preregistered extra round on the actually weakest face (face 2: new seeds, double budget) found the identical value.

Lift validity:

- All 156,656 fixed-h lifts converged, with residual ≤ 1.0e-15 and |y|_∞ ≤ 0.0134·a_h.
- The 50-digit lifts have residuals of about 1e-52.

The certified weakest face, face 5, is not the actual weakest; face 2 is.

Every link in the certified chain (D_C ≥ D_7/8 ≥ μ|ΔΦ| ≥ 2μ(1 - e0 - G/6) ≥ 2β) was nonnegative on every face. The frozen certificate is therefore valid and conservative, and no bound was violated.

## Where the certified margin loses slack (log-ratios at each face's minimizer)

| Face | Linear query range | Third-order remainder | Interval curvature | Gate 7/8 vs high | Total ln(D_C/2β) |
|---:|---:|---:|---:|---:|---:|
| 1 | 1.4e-7 | 7e-8 | **0.965** | 0.072 | 1.037 |
| 2 | 9e-11 | 1e-7 | **0.146** | 0.072 | 0.218 |
| 3 | 3e-10 | 7e-9 | **0.400** | 0.072 | 0.472 |
| 4 | 2e-10 | 3e-9 | **0.373** | 0.072 | 0.445 |
| 5 | 3e-8 | 1e-7 | **0.306** | 0.072 | 0.378 |
| 6 | 2e-8 | 2.3e-4 | **0.360** | 0.072 | 0.432 |
| 7 | 2.6e-7 | 2.8e-6 | **0.244** | 0.072 | 0.316 |

**The certified margin loses the most slack in the interval curvature term**: the whole-box third-order majorant M3. This holds on every face, including the actually weakest one.

- The true third derivative along each critical ray is 6e-6 to 6.3e-3 of M3_i.
- The sampled face-wide maximum (264 rays per face) is 0.9–2.5% of M3_i, i.e. M3 is 40–110× too large.
- The second-largest loss is the constant gate relaxation: 7.4% from using the 7/8 gate instead of the high gate.
- The linear query range (Cauchy–Schwarz with μ̃) is tight at every minimizer to ≤ 3e-7.
- The Taylor/odd-remainder step itself loses ≤ 2.3e-4.

Two separate points should not be confused:

- **Most slack lost:** interval curvature.
- **What actually causes the failure:** the linear query range on face 2, μ_2 < ε. That range is real geometry, not slack.

Oracle diagnostic (same Taylor method, true curvature, 7/8 gate; not a certificate): 2μ_i(1 - e0 - Ĝ_i/6)/2ε = 2.07, **0.92**, 1.19, 1.16, 1.08, 1.14, 1.02 for faces 1–7. A perfect curvature bound would therefore pass faces 1 and 3–7 and still fail face 2. With the high gate as well, face 2 reaches at most 0.994.

## Limits

- Numerical minimization cannot prove the face minima. The face-2 conclusion rests on one explicit witness: a 50-digit, non-interval evaluation at an exact chart point. Making that rigorous would need an interval Newton (Krawczyk) enclosure of its lift and an interval evaluation of D_C. That was not run, per the stop rule.
- This applies only to this frozen box (candidate, amplitudes, basis, endpoint, ε, metric). It is not an upper bound on robust dimension, and it says nothing about other boxes or endpoints.
- D_C is the exact allowed all-high-gate metric of `INDEPENDENT_QUERY_SLACK.md`, normalized exactly as in the accepted `structured_query`. D_7/8 is reported alongside it.

## Resources

- CPU only, single-thread processes at BelowNormal priority, at most 13 at once.
- About 2,106 CPU-seconds (35 CPU-minutes), plus a few seconds for the validate/confirm runs. Well under the 6-hour cap.
- No GPU, no 8D, no new candidate, amplitude, basis, epsilon, metric or architecture.

## Files

| File | Contents |
|---|---|
| `PREREGISTRATION.md`, `RUN_LOG.md` | Procedure and chronology |
| `audit7d.py`, `summarize.py` | Code |
| `out/validate.json` | V1–V3 checks |
| `out/face*_*.json` | Every search run |
| `out/confirm_face*.json` | 50-digit checks |
| `out/curv_face*.json` | Slack and curvature |
| `out/summary.json` | Classification |
| `logs/` | Process logs |

The audit stops here.
