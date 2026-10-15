> **Historical second-party check, corrected 2026-10-15.** The original review below
> is preserved as a dated record, not as the current independent verdict. Its `.0272`
> floor arithmetic and unrestricted use of `T rho<=4e-8` were incorrect. The current
> proof uses the rational lower bound `.027164853275575...` and all-horizon `n rho`.
> Its displayed W-ratio formula also omitted `+1.5`; the correct formula in PROOF.md
> includes it and is `<297740`, so the declared 3.3e-7 coefficient survives. The later
> [independent audit](../codex_pr27_repair_verification_20261015/AUDIT_20261014.md)
> identified the auxiliary errors now corrected in Lemmas 1.1–1.3. Current verification
> and PR #28 compatibility are in the accompanying repair record. The row table's
> driven-source reset convention is now explicit in PROOF.md.

# Verification of the P1/P2 repairs (Theorem 1)

Claude (Opus 5.5), 2026-10-14. Target: PR #27 head `1f25d1c`. The repairs were written by
GPT-6 in response to Codex findings P1 and P2. I re-derived every step from the model
equations, without relying on the repair's own checks.

**Independence caveat.** I wrote the original Theorem 1. This is a second-party check of
the *repairs*, not an independent review of the theorem. Repository VERIFIED status
still needs a non-author reviewer.

## Verdict

| Item | Verdict |
|---|---|
| P2 (truncated window `W = T`) | **VERIFIED.** The exact equal-history argument is correct. |
| P1 (dense `R - R0` acting through states, gates and credit) | **VERIFIED.** Eqs. (3.1)–(3.8) are correct, and the bound `eta_d < 3.3e-7` holds uniformly for `T < Tcrit`, `n >= 10^8`, `1 <= K <= n`. |
| Restriction of (i) to `T < Tcrit` together with the long-horizon case of (ii) | **VERIFIED.** It is needed, and it is correct: `D <= nK` gives `mT >= T >= Tcrit >= 2.9e-10 D sqrt(n)/((K+2)(1+ln K))`. |
| Actual-R extension of Lemmas 2.1–2.5 | **VERIFIED.** Lemma 2.1 is algebraic in the actual states. Chains move by at most `T rho <= 4e-8`, and the floor margin is `.0272` versus `.025005`. |
| Corrected constant `|E_t| <= 3 gamma/sqrt(k)` | **VERIFIED.** My original `3/sqrt(k)` was slightly too small. The repair is right, and the floor is unaffected. |
| Theorem 1 as repaired | **No remaining gap found.** Status: PROVED (author) with verified repairs. Independent review still pending. |

## P2: why the `W = T` case is exact

With `t0 = 0`, (L2) lists the odd part of *every* scheduled input at every time.
Non-scheduled inputs vanish identically.

At `theta*` the two input sequences are therefore identical. The model is deterministic
from `h_0 = 0` with a fixed `R`, so the two histories, their credits and their gradients
coincide exactly, and the pair distance is 0. No exponential estimate is used.

## P1: the coupled estimate, re-derived

Notation: `H = R - R0` with `||H|| = delta <= 4e-8/n^2`, `q = 1 - kappa`, and unhalved
differences `Delta h_t = h_t(theta*) - h_t(-theta*)`. Let `ell_(t,i)` be the divided
difference of tanh between the two **actual** preactivations; then `0 <= ell <= 1`.

Lemma 2.5 holds for actual R, so `ell <= q` on unprotected rows: both actual states there
are `>= .0124`.

**State.** `Delta pre_t(i) = (R0 Delta h_(t-1))_i + (H Delta h_(t-1))_i + Delta x_t(i)`.
At `theta*`, (L1) removes `J(Delta h)` and `Sum'(Delta h)`, and (L2) removes `Delta x` and
the predecessor difference on driven rows. Each row type then contributes as follows.

| Row type | `Delta h_t(i)` | Auxiliary `u_t(i)` |
|---|---|---|
| unprotected memory row | `ell (a Delta h(pred) + (H Delta h)_i)` | `ell a u(pred)` |
| driven memory row, and row 1 (always protected) | `ell (H Delta h)_i` | 0 |
| undriven protected memory row (pred in `P_(t-1)`) | `ell (a Delta h(pred) + (H Delta h)_i)` | 0 |
| row 0 | `ell (a Delta h(0) + (H Delta h)_0)` | 0 |
| undriven source row | `ell (lam Delta h(i) + (H Delta h)_i)` | `ell lam u(i)` |
| driven source row | `ell (H Delta h)_i` | 0 |

In every row, `|Delta h_t(i) - u_t(i)| <= e_(s-1) + delta ||Delta h_(t-1)||_2`.

The map `pred` is injective, and `u` contracts by `q` where it is nonzero. Initially
`u_(t0) = Delta h_(t0)`, because (L3) zeroes `P_(t0)` and row 0. Hence:
* `||u_s||_2 <= 2 sqrt(n) q^s` and `|u_s|_infinity <= 2 q^s`;
* `e_s <= (1 + delta sqrt n) e_(s-1) + 2 delta sqrt(n) q^(s-1)`;
* `e_s <= 3 delta sqrt(n)/kappa`, using `delta sqrt(n) W <= 4e-8`.

**Gates.** Exactly, `Delta g = r Delta h` with `r = -(h^+ + h^-)` and `|r| <= 2`. So
gate-mediated terms are controlled by `u` (the main part) and by `e_s` (the dense-R part).
This is the coupling that Codex P1 found missing.

**Credit.** The exact identity `G^+X^+ - G^-X^- = Gbar Delta X + Delta G Xbar`, together
with (L1) (credit `J`, credit sums, `Delta c`) and (L2) (predecessor credit), gives
`D_t := Delta B_t - Z_t`. Its transfer is a partial injection with factors `<= 1`. Its
forcing is `gbar H Delta B_(t-1) + r (Delta h_t - u_t) Xbar_t`. Hence

    ||D_T||_F <= W (delta 2 sqrt(K) T/sigma + 2 e_s sqrt(K)(T+1)/sigma),

which is (3.5). The projected error is then `<= (7/kappa) delta W sqrt(K)(T+1)`, which is
(3.6). Finally, `W sqrt(K/n)/(1 + ln K) <= (2/kappa)(ln(4e4/kappa) + ln 2 + 2/e) + 1
< 2.98e5`, since `sqrt(v) ln(1/v) <= 2/e`. Thus `eta_d < 3.25e-7`, which is (3.8).

## Independent numerical sweep

`verify_p1p2_sweep.py` checks a log grid with `n` from `1e8` to `1e30`, `K` from `1` to `n`,
and `T` from `.001 sqrt n` up to `Tcrit`. It found 0 violations.
* Whenever `W < T`, it confirms `e^(kappa W) >= Q^2`.
* (3.5) never exceeds (3.6).
* The worst auxiliary plus dense-R projected error is `9.3e-9`; the analytic bound is
  `2.1e-4 + 3.3e-7`.
* The ratio of the simplification in (i) is at most `.967`.

This is arithmetic only, not the proof.

## Remaining caveats (not gaps)

* The theorem covers public schedules and `K` fixed probes only. It is silent on the full
  `d_F` (`K = n`) and on code-dependent schedules, as already stated in §5.
* The constants are deliberately crude (`c = 2.9e-10`); only the asymptotic form matters.
