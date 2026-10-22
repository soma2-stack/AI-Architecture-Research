# Checks — three-memory probe verification and the sequential construction (2026-10-19)

All scripts run on CPU with `python -I <script>` from this folder (BLAS threads `<= 4`). Finite
computations here check exact identities to floating-point accuracy, measure specified
constructions, or certify decimal constants. They never prove universal claims by themselves.

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
| `exp_S_check.py` | the exact construction S of §4 (row-20 spike, A = .38, parking), `n = 16384 (H=700), 65536 (H=3000)`, `D = 5` | `max|x| = .380`, `m = 3`, exact endpoint, parked rows = bath to `5e-16`, separation exactly 0, `Delta F1 >= 7.7x / 2.2x` the Lemma 4.2 bound, `SO/F1 = 12% / 2.3%` |
| `constants_seq.py` | Lemma 4.1 legality constants; `Pi(z) >= .6272 z`; `c_s = .3331`; front mass `39.73`; `c_R = 4.988e-4`; required `H > 38.07 n^(3/4) + 14` | all assertions pass |
| `constants_so.py` | Lemma 5.1/5.2 coefficients and `eps_SO` on the grid `n = 10^(16 + j/20)` up to `1e40` | `eps_SO <= 1/2` from `n = 3.2e17` on (`.375` at `1e18`, `.0066` asymptotically) |

**Self-review performed.**
* *Pulse amplitude lowered.* `.45` (probe) / `.4` (exploratory) -> `.38`. This makes every
  pulse-step leak term provably nonnegative (`tanh^2(.38) < 1/7`) and keeps `|x| <= .4563`.
* *Spike start moved.* Row 7 -> row 20, because the front chain at row 7 forces `|x| = .472`.
  The rigorous margin at row 20 is `.376`.
* *Release replaced by parking.* Parking at the bath value removes all post-hold leak terms and
  all below-bath chains.
* *Interaction bound reworked.* A first, global background bound overestimated the
  cross-memory interaction by `~200x`. It was replaced by the window/out-of-window split of
  Lemma 5.1(c)(d).
* *Monotonicity in n* of `eps_SO` beyond the grid is argued from the form of the coefficients,
  not machine-checked.

No independent verification has been performed.
