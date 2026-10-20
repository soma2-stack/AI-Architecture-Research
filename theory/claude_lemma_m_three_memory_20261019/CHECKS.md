# Checks — three-memory probe verification and the sequential construction (2026-10-19, repaired 2026-10-20)

All scripts run on CPU with `python -I <script>` from this folder (BLAS threads `<= 4`). Finite
computations here check exact identities to floating-point accuracy, measure specified
constructions, or certify constants. The two exact-rational certificates are marked
**[certificate]**. Every other row is a check: it never proves a universal claim by itself.

## Repair of 2026-10-20 (after Codex's audit `../codex_pr33_independent_audit_20261019/`)

| Script | What it checks | Result |
|---|---|---|
| `envelope_certificate.py` **[certificate]** | Prop. 5.4. An exact rational envelope of every quantity in Lemmas 5.1R–5.2R, valid for all `x = n^(1/4) >= x_* = 31622`. It asserts all closure conditions, a final maximum exponent `<= 0`, and the theorem's `eps_SO <= .3747`. It also checks the Lemma 5.0R constants. | passes: `eps_SO <= .374696` for all `n >= 31622^4`; components `.00830 / .36451 / .00189`; `e <= .006422`; `c_g <= 1.05e-132`. Bisection: `eps_SO <= 1/2` certified from `x_* = 23667` |
| `envelope_certificate.py` (consistency part, not proof) | conservative pointwise high-precision upper-bound evaluation of the same chain, with exact integer `H, D`, high-precision approximations for `gamma, a^-d, F*`, and a positive rational upper bound for the tiny front gate, at 23 adversarial `n`: Codex's `1e166, 1e168, 1e180`, the rounding pair `1000000000000000280/284` (found by exact jump search), jumps near `1e30, 1e60, 1e166`, and `1e300, 1e1000` | dominated by the envelope at `x_*` **and** at each `n`'s own `x`; pointwise `.37468` at `1e18`, `.006570` from `1e60` on |
| `count_certificate.py` **[certificate]** | Cor. 6.2R. A rational quadratic `P_C(ln n) >= N_1 + N_2 + N_3 + 3C_0 + 2.25C_1 + C_2 ln^2 n` (PR #28 Theorem 4, all queries, `m = 3`, `T = n/2`), and `g, g', g'' > 0` at `u_1`, so that `n^(1/4)/161 > P_C` for all `n >= n_1` | `n_1 = 10^80` for `max C <= 10^12`; `10^100` for `<= 10^18`; `10^150` for `<= 10^30`. At `10^79` the inequality fails (`g < 0`) |
| `exp_repair_checks.py` | exact recurrence of S (row-19 spike, `A = .38`, parking) with `D = 5`. State: Lemma 5.0R(a)–(d) at every `t`. Credit (one memory column, both histories): (5.1), (5.2), births, Lemma 5.1R(a), Lemma 5.2R(i), (iv) with measured inputs | all pass at `n = 16384 (H=700), 20004 (H=700), 65536 (H=3000)`, two `theta` each. Results below |
| `exp_skeleton_action.py` | the exact skeleton action used in Lemma 5.0R (`O e_0 = e_0`; `(Ox)_1 = J + gamma sp/sqrt k`, ...) for `x_0 != 0`, versus explicit `U P U` | `<= 8.9e-15` |
| `constants_seq.py` (updated) | now asserts the manuscript constants (Codex F5) and the corrected row-19 / age-17 legality bound | `.3830 <= .3831`, `pi_0 = .627283 >= .6272`, `c_s = .333007 <= .3331`, front mass `39.7223 <= 39.73`, `c_R = .00049885 >= .0004988`, `h = 38.073 <= 38.1` |
| `constants_so.py` | first-version grid certificate | **REFUTED** (Codex F1); kept as a negative result with a header note |

`exp_repair_checks.py` results (rounded):

| n | sp_t - (k-4)s_t (min) | pre_1 - bound (min) | eps_g - g_1 (min, t>=2) | bath min | (5.1) rel. resid. | births / bound | Lemma 5.2R(iv): `|dSO|` vs rhs | dSO/dF1 |
|---|---|---|---|---|---|---|---|---|
| 16384 | .1499 | .0022 | .0429 | .0448 | 3.4e-12 | 6.0e-4 / 5.5e-2 | .0105 <= .0214 | .121 |
| 20004 | .1499 | .0020 | .0268 | .0458 | 4.2e-12 | 2.1e-4 / 3.0e-2 | .0065 <= .0138 | .093 |
| 65536 | .1499 | .0011 | 4.7e-4 | .0486 | 1.5e-11 | 7.9e-8 / 6.6e-4 | .0030 <= .0077 | .022 |
| 262144 (state only) | .1499 | .00055 | 5.5e-8 (eps_g = 5.51e-8) | .0496 | — | — | — | — |

In all runs:
* `h_1(1) = s_1` exactly, and the birth at `t = 1` is exactly 0;
* undriven cycle rows are `>= s_t`, and inactive off-cycle rows equal `s_t` (to `0`);
* the front mass is `<= 8.93 <= 39.73`, and active-pair `|delta|` is `<= .1295 <= .1316`;
* (5.2) holds to `<= 5e-13` of `max|Y(0)|` (the per-step relative value is `<= 4.8e-9`, from steps
  with `Y(0)` near 0).

## Original checks of 2026-10-19 (unchanged)

| Script | What it checks | Result |
|---|---|---|
| `external_20261018/lemma_m_three_memory_probe.py` (owner's file, run from a scratch copy) | rerun of the external probe | identical to `lemma_m_three_memory_results.txt` except the last float digit |
| `m3sim.py` | independent column-restricted simulator with the nine-term split of PR #31 (4.1), legality, peak support, bath, deviation mass, optional L_bus attribution and parking | used by every experiment below; the nine terms reconstruct `Z_T(d-1)` to `< 1e-14` |
| `exp_verify_probe.py` | the probe's eight bit patterns at `n = 256, 512`, three offset patterns | all reported metrics reproduced to every printed digit; `max|x| = .4511`, `m = 7`, endpoint `< 4e-16`; bath `-.09 .. -.11` (n=256), `-.065 .. -.073` (n=512) |
| `exp_exact_checks.py` | (a) Prop. 2.2 identity; (b) Prop. 2.3 first-order separation in the probe | (a) `3.2e-15`; (b) first-order mixed differences exactly `0.0`; interaction = second-order part to `9e-16` |
| `exp_second_order_scaling.py` | single-memory second-order share, `n = 256 .. 262144`, `H = 25, 100` | `15.7, 30.6, 39.7, 45.5, 38.2, 10.8, 2.21, 0.44%`; `H`-independent for `n >= 16384` |
| `exp_timing.py` | timing vs duration variants A–D at `n = 256, 1024, 4096` | n=256 drop `.619 -> .508` from horizon truncation; n >= 1024 shifts change the readout `<= 3.1%` (increase) |
| `exp_so_attrib.py` | L_bus by carrier row (row 1, front, spike, pair), `n = 16384, 65536` | total `12.1%` -> `2.26%`; row 1 `5.5%` -> `.75%`; front `4.9%` -> `1.0%`; spike `~ -s^2/2` |
| `exp_sequential.py` | exploratory sequential geometry (row-7 spike, amplitude .4, release) | separation exact; interaction `3e-4`; `SO/F1 = 11–12%` at n=16384 |
| `exp_S_check.py` | the exact construction S of §4 (spike from **row 19**, `A = .38`, parking), `n = 16384 (H=700), 65536 (H=3000)`, `D = 5` | `max|x| = .380`, `m = 3`, exact endpoint, parked rows = bath to `5e-16`, separation exactly 0, `Delta F1 >= 7.7x / 2.2x` the Lemma 4.2 bound, `SO/F1 = 12% / 2.3%` |

**Self-review (2026-10-19, kept).**
* *Pulse amplitude lowered.* `.45` (probe) / `.4` (exploratory) -> `.38`. This makes every
  pulse-step leak term provably nonnegative, since `tanh^2(.38) < 1/7`.
* *Release replaced by parking.*
* *Interaction bound reworked* (window / out-of-window split).
* The 2026-10-19 note that "the spike starts at row 20" was wrong (it is row 19; Codex F3).
* The "monotonicity in n argued, not machine-checked" caveat was itself the failure point
  (Codex F1). It is now replaced by the envelope certificate.

**Self-review (2026-10-20).**
* Every bound in the chain was re-derived against the carrier table of Lemma 5.2R, including all
  row-1 births.
* The pointwise and envelope evaluations share one transcription (`chain()`). An error in that
  transcription would therefore not be caught by their agreement. It is caught only by checking
  `chain()` against PROOF.md §5, which is the audit target.
* The simulations test the lemma premises and the measured-input inequalities on exact
  recurrences. They cannot test closure, which fails at simulable `n`.
