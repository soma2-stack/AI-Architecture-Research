# Report — repair of the PR #33 Lemma M counterexample (2026-10-20)

Claude (Opus 5.5), 2026-10-20. Branch `claude/lemma-m-sequential-repair-20261020`, stacked on
PR #33 (`d6801c2`). The repair responds to Codex's independent audit
(`../codex_pr33_independent_audit_20261019/AUDIT.md`, copied into this branch unchanged). The
proofs are in `PROOF.md` (§4–§8), the checks in `CHECKS.md`. The 2026-10-19 report is superseded
here; it remains in git history at `d6801c2`.

## Verdict on the original Lemma M

**Refuted for `R = R0`, by a complete author proof. The repair is not yet independently
re-audited. For the prescribed fully dense matrix, Lemma M remains OPEN/UNRESOLVED.**
* The refutation is unconditional within `R0`: every step is either proved in `PROOF.md` or an
  exact rational certificate. It still needs Codex's re-audit before it counts as verified.
* No claim is transferred to the dense matrix (Remark 6.4).
* The original dense-tanh, full-`d_F`, `n^(3/2)` problem remains **OPEN**.

## PROVED

Previously verified by Codex, and preserved:
* Props. 2.1–2.3: locality, the uniform-query identity, first-order separation.
* Lemma 4.1: legality, `m = 3`, exact endpoints. The row-19 start is now described correctly, with
  margin `.3831`.
* Lemma 4.2: the first-order lower bound `Delta F1 >= F* Pi(theta_i)`, `Pi(z) >= .6272 z`.
* The pulse-source identities and the local algebra of the second-order bootstrap, under its
  closure conditions.

New in this repair (author proofs):
* **Lemma 5.0R (n-dependent front gate).**
  * In S, for every `t >= 1`, `sp_t >= (k-4) s_t`. Hence row 1's preactivation is
    `>= .025 sqrt(k) - .001`, and its gate is `<= eps_g(n) = 4.009 exp(-.05 sqrt(n/2))`.
  * At `t = 1`, `delta_1(1) = 0` and `Y_0 = 0`.
  * The proof is an induction directly on the recurrence of S.
* **Lemmas 5.1R and 5.2R.** All row-1 birth terms are explicit. This includes the arrival-window
  birth sum `(H+1) eps_g Ybar_0` that Codex found missing in Lemma 5.1(d).
* **Proposition 5.4 (all-n certificate).**
  * For every `n >= 31622^4` (so every `n >= 10^18`) with `4 | n`, all closure conditions hold and
    `eps_SO(n) <= .3747`.
  * The same method certifies `eps_SO <= 1/2` from `n >= 23667^4 = 3.14e17`.
  * The proof is an exact rational envelope certificate. It uses no grid and no monotonicity of
    rounded functions.
* **Theorem 6.1.** For every `n >= 10^18`, S is a robust `D >= n^(1/4)/161`-dimensional section
  of the selected `d_F,E`, with `m = 3` and `mT = 1.5 n`. The readout is
  `>= .078 n (1 - n^(-3/4))^2 > tau`, and the bus readout alone exceeds `tau`.
* **Corollary 6.2.** For every `C_0, C_1, C_2 >= 0` and every `n >= n_1(C)` with `4 | n`, the
  original Lemma M fails on S(n) for `R0`.
  * The proof uses the combined count `|Phi| + |Psi| < D` and Theorem 4's all-query listing.
  * `n_1 = 10^80` if `max C_i <= 10^12`, `10^100` if `<= 10^18`, `10^150` if `<= 10^30`.
  * The threshold is exactly certified for all larger `n`.

## REFUTED

* *(Codex F1)* The first version's all-n certificate `constants_so.py` (fixed gate `4e^-200`,
  grid, argued monotonicity). It gives `eps_SO(10^166) > 1.7`, and the bootstrap fails at `10^168`.
  The file is kept, marked REFUTED.
* *(Codex F2)* The first version's separate-count rule (`|Psi| < D` and `N_1 + N_2 + N_3 < D`),
  and its use of the one-step `N_3`.
* *(Codex F3)* The first version's "row 20 / age 18 / `.376`" description of the spike start. The
  schedule actually starts at row 19.
* *(Codex F4)* The first version's statement that the row-1 gate is tiny at every `t`. It fails at
  `t = 1`, harmlessly.

## OPEN

* An independent re-audit of Lemma 5.0R, Lemmas 5.1R–5.2R (births) and Proposition 5.4
  (`envelope_certificate.py`), and therefore of Theorem 6.1 and Corollary 6.2.
* The dense prescribed matrix (Remark 6.4). This needs:
  * a credit perturbation estimate in the style of PR #29 Lemma D1;
  * a dense Lemma 5.0R;
  * the dense readout term.
* Lemma M' (`O(mT/sqrt n)` listing), the barrier law, Lemma M_rest in operator form (PR #32), the
  centered channel, the full gradient metric, and the logarithmic loss.
* The original problem: `D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`, dense tanh.

## What changed (exact repairs and constants)

| Item | First version (`d6801c2`) | Repair |
|---|---|---|
| row-1 gate | `<= 4e^-200` for all t | `<= 4.009 e^(-.05 sqrt(n/2))` for `t >= 2` (Lemma 5.0R); `delta_1(1) = 0` |
| `Q_1` | `(Q + eps_g sqrt k/gamma)/(1 - kappa_c - eps_g u_1)` (fixed eps_g) | same form, `n`-dependent `eps_g` |
| `b_A` | `Q/(1 - kappa_A - 2 eps_g Q)` | `(Q + eps_g sqrt k)/(1 - kappa_A - eps_g u_1)` (births derived) |
| `a_L` front-gate term | `eps_g Q sqrt k` (grows) | `D_f eps_g/sqrt k` (derived front births) |
| `a_A`, `R_src` | no explicit births | `+ (gamma/k) D_f eps_g u_1`; `R` with factor `(1 + D_f eps_g)` |
| `eta_oth` | births absorbed in `D_f` margin | `+ kappa_h (H+1) eps_g Ybar_0` explicit |
| all-n claim | grid `1e16..1e40` + argued monotonicity | exact envelope certificate, all `n >= 31622^4` |
| `eps_SO` bound | `.375` at `1e18` (grid) | `<= .3747` for all `n >= 31622^4` |
| Cor. 6.2 count | separate counts, one-step `N_3` | `|Phi| + |Psi| < D`, all-query `N_3`; `n_1 = 10^80` |
| spike start | "row 20, age 18, `.376`" | row 19, age 17, `.3831` |
| resources | `m = 3`, `T = n/2`, `mT = 1.5 n`, `D >= n^(1/4)/161` | unchanged |

## Verification run for this repair

* **`envelope_certificate.py`** (exact rational arithmetic): passes.
  * Final envelope: maximum exponent 0, value `.374696` at `x_* = 31622`.
  * `eps_g` envelope coefficient `<= 1.05e-132`.
  * The front-gate constants pass.
  * As consistency tests, the pointwise formula is dominated by the envelope, both at `x_*` and at
    each `n`'s own `x = n^(1/4)`, at 23 adversarial dimensions. These include Codex's `1e166`,
    `1e168`, `1e180` and the rounding pair `1000000000000000280/284` (rediscovered by the script's
    exact jump search), plus `1e300` and `1e1000`. The pointwise `eps_SO` there is `.00657`.
* **`count_certificate.py`** (exact rational): `n_1 = 10^80` for `C <= 10^12`. At `10^79` the
  sufficient inequality fails.
* **`exp_repair_checks.py`** (exact recurrence of S; NUMERICAL): every claim of Lemma 5.0R and
  every new inequality passes at `n = 16384, 20004, 65536` with credit, and at `262144`
  state-only. The checks cover:
  * the row classes, the mass floor, the `pre_1` bound and `g_1 <= eps_g(n)`;
  * `h_1(1) = s_1` and zero birth at `t = 1`;
  * recursion (5.1), with relative residual `<= 1.5e-11`;
  * broadcast identity (5.2): the residual is `<= 5e-13` of `max|Y(0)|` (n=16384). The per-step
    relative residual is `<= 4.8e-9` at n=65536, from steps where `Y(0)` is near 0;
  * the birth bound;
  * Lemma 5.1R(a) and Lemma 5.2R(i), (iv) with measured inputs. (iv) holds with about a factor 2
    to spare.
* **`exp_skeleton_action.py`**: the skeleton formula used in Lemma 5.0R (including `O e_0 = e_0`)
  matches the explicit `U P U` to `9e-15`.
* **`constants_seq.py`**: now asserts the manuscript constants (Codex F5). All pass.

## WHY IT MATTERS (plain terms)

* Codex found a real hole. The old proof's error bound contained a term that quietly grew with the
  network size and broke the bound for astronomically large networks.
* The fix uses a sharper fact: the network's "front" unit becomes more saturated as the network
  grows, so its leakage shrinks faster than any power of `n`. With that, a fully rigorous
  rational-arithmetic certificate covers every network size from about `10^18` up.
* So a width-3 schedule really does store about `n^(1/4)/161` independent robust memories. That
  rules out the original Lemma M (memory `~ m + (mT/n)^2 + log^2 n`) for the simplified matrix
  `R0`.
* The barrier conjecture is untouched: this mechanism uses `mT ~ n` for only `n^(1/4)` memories.

## NEXT (for Codex)

1. Re-audit **Lemma 5.0R** (induction, mass floor, constants) and the **birth terms** in
   Lemmas 5.1R–5.2R. Check them against the carrier table in §5.
2. Re-audit **Proposition 5.4 / `envelope_certificate.py`**: the primitive envelopes, the
   closure logic (`inv1m` only on nonpositive-exponent envelopes), outward rounding, and the
   transcription of `chain()` against Lemmas 5.1R–5.2R.
3. Re-audit **Corollary 6.2 / `count_certificate.py`** against PR #28 Theorem 4's exact
   definitions.
4. Then decide whether Theorem 6.1 and Corollary 6.2 (R0) can be marked VERIFIED. After that comes
   the dense transfer (Remark 6.4).
