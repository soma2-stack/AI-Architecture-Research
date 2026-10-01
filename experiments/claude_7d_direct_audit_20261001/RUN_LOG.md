# Run log — direct 7D audit

- 2026-10-01 12:55:41 EDT: PREREGISTRATION.md written before any face computation. SHA-256 `f91da22f08704abed27bfcb36596ef110f30fe805e81ed87ce64f4548710d449`.
- 12:59:56: Validity checks (`audit7d.py validate`, `out/validate.json`) were run before any face computation. All pass:
  - V1: candidate hash ok.
  - V2: mu_tilde reproduced to a relative error of 4.4e-16.
  - V3: max|DPhi(0)-I| = 1.0e-15.
  - Center lift residual 3e-18.
  - Implementation note: the torch lift (80 ms) was replaced by an equivalent numpy forward-mode recurrence (3 ms per lift with the section Jacobian). It matches the torch path to 1.0e-14 relative at 6 interior non-face points. The mathematics and the preregistered procedure are unchanged.
- 12:59:56: Launched the 7 preregistered face searches (`audit7d.py face 1..7`). audit7d.py SHA-256 `507cb4dfa7bf7942c497e2b59ac5673845cfc5594f342c1e4be92baf70f0060a`. Each runs as one single-thread process at BelowNormal priority.
- Base face searches finished; results are in `out/face*_base.json` and `logs/`. Every face is reliable: the B/D and C bests are identical. All lifts are valid (max|y|/a_h 0.0134; max residual 1.0e-15; no Newton failures). Best D_C per face, with ratios to 2eps and to 2beta:

  | Face | Best D_C | / 2eps | / 2beta |
  |---:|---:|---:|---:|
  | 1 | 4.5255e-3 | 2.263 | 2.821 |
  | 2 | **1.9885e-3** | **0.994** | 1.244 |
  | 3 | 2.5607e-3 | 1.280 | 1.602 |
  | 4 | 2.4941e-3 | 1.247 | 1.560 |
  | 5 | 2.3318e-3 | 1.166 | 1.459 |
  | 6 | 2.4634e-3 | 1.232 | 1.540 |
  | 7 | 2.1906e-3 | 1.095 | 1.371 |

- **Not yet classified.** Face 2, not face 5, is the actual weakest. Still to run, as preregistered:
  1. the weakest-face round (`face 2 --weakest`);
  2. 50-digit confirmation (`confirm 1..7`);
  3. slack attribution (`curv 1..7`);
  4. `summarize.py`.
- Stopped here because the usage limit was reached.
- 13:10:16: Resumed. Launched `face 2 --weakest`, plus `confirm` and `curv` for faces 1,3,4,5,6,7. audit7d.py is unchanged (SHA-256 507cb4dfa7bf7942…).
- 13:17:26: Weakest-face round (`face 2 --weakest`) reproduced the identical minimum, 1.988511838e-3 at z = e_2. 50-digit confirmations: all 7 faces agree with float64 to ≤ 1.1e-14 relative, with mp lift residuals ≤ 1.7e-52. Face 2's D_C at 50 digits is 0.0019885118384809833 (0.99426 × 2eps).
- Slack diagnostics (`curv 1..7`) are complete; every chain term is nonnegative. `summarize.py` gives the classification **7D SECTION LOOKS TOO WEAK AT EPSILON**. See REPORT.md.
- Total about 2,106 CPU-seconds. The frozen 7D folder is unchanged (git status clean for it). Nothing was committed. Audit stopped.
