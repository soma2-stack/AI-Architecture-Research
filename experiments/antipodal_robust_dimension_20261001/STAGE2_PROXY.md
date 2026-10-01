# Stage-2 diagnostic: odd-symmetric antipodal bound (NUMERICAL ONLY — not certificates)

## Idea

For antipodal pairs the even Taylor terms cancel exactly:

    Phi(z) - Phi(-z) = 2 DPhi(0) z + R3(z),   |R3_i(z)| <= (1/3) sup_cube |D^3 Phi_i [z,z,z]|.

This holds because g(s) = Phi_i(s z) gives g(1) - g(-1) = 2 g'(0) + int_{-1}^{1} int_0^s (s-u) g'''(u) du ds, and
int s ds = 0 over [-1,1]. With K ~ DPsi(0)^-1, the per-face margin becomes

    beta3_i = mu~_i (1 - E0row_i - M3_i / 6),

where:
- E0row_i is the scaled CENTER residual |I - K C0|, which is tiny;
- M3_i bounds sum_{jkl} |D^3 Phi_i|_jkl over the cube.

Second-order curvature, the binding term in stage 1, drops out. Third-order whole-box majorants of h and S are needed,
using a tanh'''' bound 8|tanh| sech^2 |2 - 3 tanh^2|, together with the implicit third derivative of the hidden
section.

The hidden-section existence and inclusion conditions are unchanged; they still use second-order bounds. The odd
cancellation applies only to antipodal pairs. It is sufficient for the Borsuk–Ulam dimension theorem but not for the
2^r-corner finite-state statement.

## Implementation status

**Float proxy only:** `stage2_proxy/screen_proxy3.py`.
- Its third-order majorants were checked against autodiff third derivatives on the independent n3 archived endpoint.
  At 48 points (32 of the 64 box corners plus 16 random points) the maximum actual/majorant ratio was 0.994; tight,
  never exceeded.
- The second-order part is the stage-1 proxy, which reproduces the reviewed kernel exactly.
- **No rigorous (interval, outward-rounded) third-order kernel exists yet. Nothing below is certified.**

## Screen (13 jobs; Nelder–Mead on log amplitudes, warm-started from stage-1 screening; min beta3 / epsilon)

| Endpoint | r | Stage-2 proxy | Stage-1 proxy at same r | Strongest certified now |
| --- | ---: | ---: | ---: | ---: |
| independent_n4_confirmation | 6 | **1.657** (query), 0.929 (frob) | 0.592 | 5 |
| independent_n4_confirmation | 7 | 0.790 | 0.266 | 5 |
| dense_n4_confirmation | 5 | 0.947 | 0.328 | 4 |
| independent_n3_confirmation | 4 | **2.254** | 0.602 | 3 |
| independent_n3_archived | 4 | **1.691** | 0.386 | 3 |
| dense_n3_confirmation | 4 | **1.651** | 0.652 | 3 |
| dense_n3_archived | 4 | **1.351** | 0.319 | 3 |
| independent_n4_archived | 3 | **3.781** | 0.945 | 2 |
| dense_n4_archived | 3 | **2.315** | 0.591 | 1 |

In the stage-2 optima the hidden half-widths a_h are about 2–5x larger than the stage-1 optima. Hidden-section
inclusion is therefore less likely to be the failure mode.

**Interpretation (hypothesis, not a result).** A rigorous odd-symmetric kernel may certify r = 6 at
independent_n4_confirmation and add one coordinate at most other endpoints. r = 7 at independent_n4_confirmation and
r = 5 at dense_n4_confirmation are not reached by this proxy; the optimizer is lightly converged, so this is not a
ceiling.
