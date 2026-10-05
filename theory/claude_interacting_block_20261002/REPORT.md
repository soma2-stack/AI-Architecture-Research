# Interacting-block review and attack: report

Claude (Opus 5.5), 2026-10-02. Details are in REVIEW_PHASE1.md and THEORY_PHASE2.md. Scripts, JSON and logs are in
this folder. Labels: **[R]** rigorous, **[S]** scoped rigorous, **[N]** numerical, **[H]** heuristic.

## A. Which Codex claims independently verify?

All seven, within their stated scopes:
1. **One-pulse lower bound** floor(n/4)-2 with half-margin > 0.00161. [R]
2. **Bounded fixed-time pulses: Theta(n).** Upper qk; lower only when the one-pulse configuration is in the family.
   [S]
3. **One fixed co-rotating profile: Theta(n).** Lower from T = 1. [S]
4. **Latent-cycle reduction to one scalar plus a d x d block.** Re-derived; my own implementation matches the full
   recursion to <= 7.5e-12. [S]
5. **d^2 + 1 finite-error upper** for the latent-cycle class. [S]
6. **Long sustained windows.** The two-step contraction lambda = sqrt(1-199/20402) and the 412 bound both check. The
   result is robust dimension <= 1 eventually, for n ≳ 1.5e10 and T ≳ 409(6.4 + 0.5 ln n). [S, asymptotic]
7. **Loopholes** (short windows, weakening gates): correctly scoped.

Codex's adversarial numbers reproduce exactly from its saved coefficients, using my independent code.

## B. What fails or needs correction?

Nothing substantive in Codex's work.

Codex's five corrections to MY earlier write-up are valid; none changes a conclusion:
1. a <= 0.995 was misused.
2. The rounded product is 0.0016177, not 0.0016181.
3. "Exact" means to displayed precision.
4. Co-rotating stationarity is false as a literal identity; Lemma B3 gives the exact replacement.
5. "Rotating channels are necessary" was a hypothesis.

One addition: the accepted contract permits future preactivations up to 3/4 (inputs outside the past cube). Using it
roughly doubles the one-pulse margin to > 0.0032 (exact 0.0050 / 0.0046 / 0.0043 at n = 200 / 400 / 1000;
full_box_margin.json). [R, contract-conditional]

## C. Strongest rigorous lower bound

| Class | Lower bound |
| --- | --- |
| One fixed feature | floor(n/4) - 2, half-margin > 0.00161, or > 0.0032 with the full permitted box |
| Full model | Omega_c(n^2), unchanged |

## D. Strongest rigorous upper bounds

| Class | Upper bound |
| --- | --- |
| General fixed feature | (floor(n/2) - 1)^2 |
| Latent-cycle class | d^2 + 1 |
| q fixed-time pulses | qk |
| One fixed co-rotating profile | r + 1 |
| Long sustained latent-cycle windows | 1, asymptotically |
| Full model | O_c(n^2 log n) |

**New [R] (Lemmas B2–B4):** in the latent-cycle class, everything beyond one d-vector of stationary information
enters through ONE rank-<=2 twist per active step, plus fresh credit (<= T). For the idealized twist-free block this
gives <= d + 1 when T + 1 < 0.0035 sqrt n. That is a structural localization, not an O(d) theorem for the actual
block.

## E. Does the interacting block admit any proven omega(n) section?

**No.**
- No section of dimension above about d survives even legal-query evidence.
- The best FIXED one-step query sees only 1–2 block directions above epsilon (n = 200–800) [N].
- Codex's large charts fail adversarially at the 1–3 epsilon level under one-step queries. Optimized two-step queries
  do not help [N].

## F. Is any meaningful fixed-feature class now proved Theta(n)?

Yes, but only scoped classes (all [S]):
- bounded fixed-time pulses whose family contains the one-pulse configuration;
- the union over T of single fixed co-rotating profiles.

Long sustained latent-cycle windows are even O(1) asymptotically. No unrestricted-profile class is closed.

## G. Short-window profiles

**Rigorous.** Only d^2 + 1, plus the localization of Lemma B4: one rank-<=2 twist per step, fresh credit <= T, which
is envelope-negligible when T ≪ 0.0035 sqrt n.

**Numerical.** The tail's one-step visibility falls with n under sustained gates (T = 6: 3.5 epsilon → 1.2 epsilon →
0.4 epsilon at n = 200 → 800), and fixed-query capacity is 1–2.

**Heuristic.** The twists' right factors are near-collinear shifts of a smooth bump, which favors O(d).

## H. Weakening-gate profiles

This is where the residual persists. The tail's one-step visibility is about 1.2–1.9 epsilon per direction, flat in
n and T, and there is no dissipation to kill fresh credit. No omega(n) section was found, and no O(d) proof exists.
This is the surviving loophole, as Codex said.

## I. Strongest remaining loophole

Weakening-gate (non-dissipative) long windows, in which undamped fresh credit accumulates and the per-step node-1
twist acts on it, combined with the uncertified gap between the κ-envelope and actual permitted-query reach (5–40x).

## J. Recommended next theorem

**Permitted-adjoint reach lemma.**
- **Statement:** at h = 0, every permitted adjoint (any future length L, preactivations in [1/4, 3/4]^n) has block
  part = moving spike (|·| <= 0.94^L sqrt(k/n)/beta at node d-1-L) + one demodulation pattern
  (|·| <= 0.153·0.94^(L-1)/(beta sqrt n) per entry) + Householder spread of explicit O(c_k) size.
- **Corollary:** sup_permitted ||X^T zeta|| <= (1/beta)[C1 max_i ||X^T b_i|| + C2 ||X^T||_(∞→2)/sqrt n + C3 c_k ||X||].
  This is about 10x sharper than the κ-envelope, and computable.
- **Use 1:** rigorously certify (or refute) collisions in Codex-type charts.
- **Use 2:** combined with Lemma B4, attempt an O(d) bound for short windows, where the twist right factors are
  near-collinear.
- **Use 3:** then test the weakening-gate long-window loophole with the sharpened metric. A cheap numerical pre-check
  is exact spike-query sweeps over L.

## Resources and files

- **Files:** block.py, jac_spectra.py, summary_test.py, codex_pairs.py, tail_visibility.py, structure_checks.py and
  their JSON/log outputs.
- **Compute:** about 1 CPU-hour (at most 8 threads). No GPU.
- **Not modified:** Codex's files. Nothing was committed.
