# Hostile review: frozen 6D third-order antipodal certificate

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** experiments/third_order_antipodal_20261001. Freeze 914b075; result e2245ed.
- **Claim:** independent width-4 confirmation needs at least 6 continuous robust memory coordinates at epsilon = 1e-3.

## Verdict

**6D THIRD-ORDER CERTIFICATE VERIFIED.** No mathematical, implementation, provenance or replay gap was found. The
lower bound is valid under the accepted contract:
- a continuous no-external-history encoder;
- permitted late one-step queries, with the support-aware 7/8 gate;
- uniform absolute gradient error epsilon in the unchanged normalized metric;
- one fixed-h section of one frozen endpoint.

It is not a 6-bit / 64-state claim. Only antipodal pairs are separated.

## What was checked

| Item | Finding |
| --- | --- |
| Proof algebra | Every recurrence term was re-derived independently: h_ijk, S_ijk with f'..f'''' and f'''' = 8H(1-H^2)(2-3H^2); implicit y' / y'' / y''' including all three H''[w_ij, v_k] terms; composite s''' + 3 mixed s'' + s_y y'''; odd remainder \|R+\|, \|R-\| <= M3/6, so \|Phi(z) - Phi(-z) - 2DPhi(0)z\| <= M3/3 and face bound 2(1 - e0 - M3/6). Correct. |
| Kernel vs proof | Line-by-line match. Outward history box, interval gates, upward tensor algebra; R and W injection derivatives (R: h', h'', h'''; W: x' only); M3, e0 and ell~ assembly; support-aware mu~ of (KL)_i / a_i. |
| Fixed-h lift | Hidden contraction eta_h = 0.0497 < 3/4. The self-map passes with a_h = 8087/2^20. Equal hidden widths give the sup-norm contraction. Lipschitz continuity follows (addendum A1 argument). Own Newton solves: hidden use <= 2.1% of a_h at 192 boundary points. |
| Joint 6D | One cube, with every face integrated along rays through the whole simultaneous 10-D (4 normal + 6 tangent) box. Not six 1D results. |
| Majorants vs truth | Autodiff at 96 points of the 10-D box, half of them corners: max actual / bound 0.9979 for third derivatives, 0.9963 for second derivatives. Tight, never exceeded. |
| Implicit y''' end to end | Finite-difference third derivatives of Phi along the curved exact section (72 points and directions) are at most 2.3% of the certified bound. |
| Odd remainder | At 192 boundary antipodes, actual \|Phi(z) - Phi(-z) - 2DPhi(0)z\| <= 0.0085 x (M3/3). |
| Antipodal separation | Adversarial minimum per face, D(7/8) / 2eps = 3.04, 1.98, 2.43, 2.34, 2.16, 2.31. Ratio to the certified 2 beta_face >= 1.149 (face 1). |
| Replays | Fresh cache-free 192- and 256-bit replays are identical to result.json and bounds_*.npz in every field and array. |
| Freeze | Every FROZEN.json local and source hash verifies. No scientific file changed between 914b075 and e2245ed. |
| Candidate rule | The highest archived r = 6 proxy, query_r6_s2 at 1.6574 versus s1 at 1.6469, was selected. Tangent widths were rounded down, and the hidden width +2% rounded up, as declared. |
| Checker repairs | Post-result git-path and ignored-log packaging only, for the stage-1 archive. The certificate is not affected. |

## Strongest remaining weakness

**Formal rigor rests on unmechanized code.** The new third-order majorant kernel and the accepted floating-point
upward-rounding plus interval model are hand-audited and numerically attacked, not machine-checked.

**There is a margin, but only some of it is formal.** The weakest face (face 1) has beta3 / eps = 1.657 with
M3 / 6 = 0.455. A 2.2x underestimate of that one cubic bound would break it. The measured truth is about 40–100x
below the bound, so the risk is formal, not substantive.

**The claim is narrow:**
- continuous-coordinate encoders only;
- one local section and endpoint;
- the independent recurrence's own (diagonal-R) parameter metric;
- the accepted unrestricted-future-input query family.

No upper bound exists, so 6 is not the maximum.

Evidence: third_attack.py, tjobs.txt and logs/ in this directory. 20 single-thread CPU workers at BelowNormal
priority; no GPU.
