# Hostile review: frozen 8D third-order antipodal certificate

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** experiments/third_order_antipodal_8d_20261001.
- **Commits:** preregistration and freeze dd70f48 (pushed 16:04:26); result 093c1e7.
- **Claim:** independent width-4 confirmation has a rigorously certified joint 8D continuous robust section at
  epsilon = 1e-3, so a continuous encoder needs k >= 8.

## Verdict

**8D CERTIFICATE VERIFIED.** No margin, third-order, joint-section, interval/rounding, topology, contract or provenance
gap was found. Face 8's certified separation 2beta_8 = 0.0020489061058 > 0.002 is confirmed by:
- two independent interval implementations;
- every numerical attack.

The true separation on every face is well above the certified value.

The lower bound k >= 8 holds under the unchanged contract:
- a continuous no-replay encoder;
- permitted late one-step queries, with the support-aware 7/8 gate;
- uniform error epsilon in the unchanged normalized metric;
- one fixed-h section of one endpoint.

It separates antipodal pairs only. It is not an 8-bit or 256-state claim.

## What was checked

| Item | Finding |
| --- | --- |
| **Contract unchanged** | Endpoint (central history) and model parameters are identical to the accepted 6D and 7D candidates. epsilon is 1/1000 (candidate, config, and kernel literal). The query/metric code is hash-verified unchanged. My own 80-digit mu~ matches the stored values to 2e-55, and the stored values are lower bounds. The encoder and topology step are unchanged. |
| **New chart** | The normal coordinates are exactly the four last-input coordinates (B rows 144–147 = identity); the screen calls this a different local chart at the same endpoint. The tangent B is query_svd columns 4–11 as exact binary64 rationals. K_selected = I and L is a numerical left inverse; their inexactness is charged as center residuals e0 <= 4.1e-14 (included). |
| **Kernel** | reviewed_kernel.py is byte-identical to the 7D affine-tightened kernel I reviewed (sha 82601731…). |
| **Second interval implementation** | I ran the clean-room engine (separate mpmath directed rounding and Taylor jets; its only edit is the expected-hash line) on the frozen 8D candidate. PASS at 192 and 256 bits. beta agrees to 2.5e-14 relative, M3 to 6e-14, mu to 1e-55, all eight derivative arrays to 2.5e-13 with identical zero patterns. Clean-room 2beta_8 = 0.002048906105769439. |
| **Fresh replays** | 192 and 256 bits, cache-free: all eight bound arrays are bit-identical and every numeric field is identical. Only `reason` differs, which run.py relabels from the copied '6D certified' string, as disclosed. |
| **Affine tightening** | 60-digit trajectories at every sign corner of every C_t,i plus 40 random corners: preactivations stay inside the enclosures (worst excess -4.6e-58) and \|dpre\| <= ax everywhere. 800 float points plus adversarial extremisation show contacts at rounding level only. |
| **Tightening is load-bearing** | The untightened accepted kernel fails the hidden self-map on this box (forcing 0.0332). |
| **Mixed 2nd/3rd derivatives** | 72 sampled points of the 12-D box plus adversarial maximisation (two seeds) give max actual / bound 0.9999947 (third order) and 0.99985 (second order). Never exceeded. The near-1 entries are h_4's final-step derivatives along the last-input normal coordinates. There the bound is sup\|tanh'''\| over a narrow preactivation interval times an exact coefficient, so it is near-exact by construction, and interval containment makes it rigorous. |
| **Implicit y''' end to end** | Finite-difference D^3 Phi along the curved exact section (120 points and directions): at most 14.7% of the certified bound. |
| **Third-order remainder** | At 528 boundary antipodes (all 128 corner pairs plus 400 face points), \|Phi(z) - Phi(-z) - 2DPhi(0)z\| <= 0.112 x (M3/3). Max \|DPhi(0) - I\| = 2.6e-14. The face-wide true third derivative is 2.2–12% of M3 (face 2 12.0%, face 6 2.6%, face 7 2.2%, face 8 2.8%). |
| **Fixed-h lift, contraction, forcing** | Exact: eta_h = 0.0275 < 3/4, forcing at most 0.810 of the allowance, radius 0.0914 <= 1. Measured: true forcing at most 12% of the certified bound (9.9% of the allowance), true contraction 0.00047, lifts use at most 9.7% of a_h, residuals <= 3e-17 (float) and 2e-52 (mp), zero Newton failures. |
| **All 8 faces** | Screen, multistart L-BFGS-B, sub-face and differential-evolution searches (3x deep on faces 2, 6, 7, 8, with 451 local runs each, all converging to one minimum), plus 12–20k-point brute-force sampling on 2, 6, 7, 8. All 50-digit confirmed. Minima are at or near the face centres. |
| **Joint 8D** | One 12-D box (4 normal + 8 tangent). The hidden section is solved simultaneously over the closed 8D box, and every M3_i sums all mixed cubic terms over all eight amplitudes. |
| **Chronology** | The candidate was extracted mechanically from the committed screen (c057e4e; query_svd/proxy, exact binary amplitudes, no rounding). The freeze was pushed at 16:04:26, before the bounds and result (16:05). All FROZEN hashes verify (12 local, 14 source, 239 historical). |
| **Repairs** | Pre-official: a synthetic-test shape typo; the candidate, kernel and sources are unchanged between FROZEN_INITIAL and FROZEN. Post-official: finalize_fixed.py differs from the frozen finalize.py by one report-text notation line (plus CRLF). Both are packaging only. |
| **Borsuk–Ulam** | The cube boundary is homeomorphic to S^7, and z -> E(x(y(Az), Az)) is continuous. An encoder into R^7 must identify some antipodal pair, so k >= 8. No off-by-one. |

## Narrow faces: certified versus true (7/8-gate metric, 50-digit confirmed)

| Face | Certified 2beta | Breaks if M3 understated by | True minimum D78 | / 2eps | / 2beta |
|---:|---:|---:|---:|---:|---:|
| 2 | 0.0020699 | 6.0% | 0.0032421 | 1.621 | 1.566 |
| 6 | 0.0020581 | 9.2% | 0.0026937 | 1.347 | 1.309 |
| 7 | 0.0020491 | 13.5% | **0.0024073** | **1.204** | 1.175 |
| 8 | **0.0020489** | **5.5%** | 0.0029529 | 1.477 | 1.441 |

The other faces are 1.45–1.73x 2eps (true). The certified weakest face is 8. The true weakest is 7, at about 2mu_7. On
every face the gap between true and certified is almost entirely the M3 majorant: log 0.16–0.45, while the query range
contributes at most 2e-5.

## Notes (no effect on validity)

1. The REPORT title has a mojibake em dash, which is cosmetic.
2. The float proxy at screen c057e4e (beta/eps 1.02445) predicted this interval result before the freeze. The
   prospective freeze protects against post-result tuning, not against prior knowledge. That is irrelevant to a proof.
3. The clean-room engine is Codex-authored software; its independence is at implementation level, not authorship
   (disclosed in its REPORT). My numerical attacks are the independent check of the bounds against reality.

## Strongest remaining weakness

**The formal margins are thin.** Face 8 breaks if M3_8 is understated by 5.5%, face 2 at 6.0%, face 6 at 9.2%, face 7
at 13.5%. That risk is now well defended:
- two separately written interval engines agree to 2.5e-13;
- true curvature is 8–45x below M3;
- true minima are 1.17–1.57x the certified 2beta.

What remains is a conceptual error shared by both engines, which derive from the same PROOF.md. The numerical tests
check the bounds against the true dynamics independently of that derivation, and none found one.

**Hidden inclusion uses 81% of its certified allowance.** The true usage is about 10%.

**The scope is narrow:**
- one section and endpoint;
- continuous encoders;
- the accepted query family and metric;
- no nontrivial upper bound.

## Is going directly to rigorous 10D sensible?

**No.**
1. The same kernel cannot certify 10D. Codex's own screen gives the best 10D proxy section beta/eps = 0.038, and the
   10D direct section fails the hidden majorant guards before M3 can even be formed. The actual 10D geometry looks
   promising (about 1.89x 2eps sampled), but the obstacle is the method's conservativeness: here M3 is 8–45x the true
   curvature.
2. 8D passes with only 2.4% formal slack, so there is no headroom to absorb two more axes.
3. 9D was not screened at all; going straight to 10D skips it.

A sensible order would be:
1. a method upgrade that removes the whole-box M3 conservativeness, for example face subdivision with branch-and-bound
   interval evaluation of Phi(z) - Phi(-z), or Taylor-model enclosures;
2. demonstrate that upgrade by re-certifying 8D with a much larger margin;
3. a cheap 9D float screen;
4. only then 9D or 10D intervals.

Alternatively, pursue the upper-bound question, which the screen suggests lies near 10–11 for these sections but which
is unproved.

Evidence: review8d.py, cleanroom_8d/ (my run of the clean-room engine), logs/ and out/ in this directory. About 1.5–2
CPU-hours in at most 18 single-thread workers at BelowNormal priority; no GPU. No file in any reviewed directory was
modified.
