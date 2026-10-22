# Report — three-memory probe, second-order terms, and the original Lemma M

Claude (Opus 5.5), 2026-10-19. Proofs are in `PROOF.md`, checks in `CHECKS.md`. The owner's three
files of 2026-10-18 are archived unchanged in `external_20261018/`. Nothing here is independently
verified yet.

## PROVED (author proofs; not independently checked)

* **Locality and separation (Props. 2.1, 2.3).**
  * For balanced off-cycle memories on disjoint pairs, every first-order gather term of a
    memory's column depends only on that memory.
  * All cross-memory interaction is second order (`K_bus + L_bus`). It enters only through the
    other memories' pulse-row gates.
  * Checked: first-order mixed differences are exactly 0.
* **The uniform query reads the gather row exactly (Prop. 2.2).** For `g = HI 1`, the readout of
  an off-cycle column is `a HI sqrt(k) Z_T(d-1, c)`. The centered channel is absent. So the
  probe's measured quantity is, up to that factor, a legal readout.
* **A legal width-3 construction with a rigorous first-order bound (Lemmas 4.1, 4.2).**
  * *Construction.* Sequential off-cycle pulse memories read by one gather spike.
  * *Legality.* Every input satisfies `|x| <= .4563`; the peak support is `m = 3`; the endpoint is
    exact.
  * *First-order signal.* Each memory's signal is `>= F* Pi(theta_i)`, with `Pi(z) >= .6272 z`.
* **Second-order terms are small (Lemmas 5.1, 5.2, Cor. 5.3).**
  * `||Delta SO|| <= eps_SO ||Delta F1||`, with `eps_SO <= 1/2` for `n >= 1e18` and `-> .0066`.
  * Constants are certified on a grid; monotonicity in `n` is argued.
  * This settles mission item 1 for this mechanism. Repeated capture, feedback and leakage do not
    create or destroy directions here; they only perturb the first-order signal by a few percent.
* **Theorem 6.1.** That construction is a robust `D ~ n^(1/4)/160`-dimensional section of the
  selected `d_F,E` at `m = 3`, `mT = 1.5 n`, for every `n >= 1e18`.
* **Corollary 6.2: the original Lemma M is false for large `n`** (for `R = R0`).
  * No bus listing of size `C_0 m + C_1 (mT/n)^2 + C_2 log^2 n` can make the bus readout
    `<= tau/4` at its zeros once `n^(1/4)/161` exceeds that size.
  * PR #29's joint form with Theorem 4's `Phi` fails too, for `n >~ 1e80`.

## REFUTED

* **"Arrival timing matters more than hold duration"** as a general effect.
  * It is reproduced only at `n = 256`. There the shifted pulses end within 2 steps of `T`, so the
    second-order terms have no time to build.
  * For `n >= 1024` timing changes the readout by `<= 3%`, in the opposite direction.
  * What matters is the hold before the pulse, which builds the own scalar. In the theorem regime
    the signal is `~ s^2 H_pre H_post`.
* **"Second-order contributions grow with n"** (the 14% -> 30% trend).
  * The numbers are reproduced (`14.0%` and `29.7%` in the probe).
  * But the share peaks at `~46%` near `n = 2048` and then falls: `10.8%` (16384), `2.2%` (65536),
    `0.44%` (262144).
  * The early growth is a small-n artifact: the bath is negative there, outside the theorem
    regime.
* **Distinct readouts as evidence of capacity.** Eight distinct patterns on three columns are
  automatic, and the probe's readouts are `~2–3x` below `tau`. Robustness needs
  `H ~ 40 n^(3/4)`, which does not fit at simulable `n`.

## OPEN

* **Dense matrix.** The transfer of Theorem 6.1 and Cor. 6.2 to the prescribed dense `R`
  (Remark 6.4; expected routine).
* **Independent audit** of §4–§6. The second-order bootstrap is long; the monotonicity step
  beyond the certified grid is argued, not machine-checked.
* **Lemma M'** (`O(mT/sqrt n)` listing) and the barrier law.
* **Lemma M_rest in operator form (PR #32):** the centered channel, code-dependent schedules and
  the full metric.
* **Removing the logarithmic loss** (a separate problem).
* **The original problem:** `D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`.

## WHY IT MATTERS (plain terms)

* **The external probe.** It ran correctly and its schedules are legal, but it was run where the
  network's resting state ("bath") is unrealistic. Its main trends (growing second-order effects;
  timing over duration) do not survive at realistic sizes.
* **The mechanism it was probing is real.**
  * One "collector" unit, held still for a quarter of the network's cycle, can pick up the leaked
    traces of many different memory units, one after another.
  * Each memory stays separately readable.
  * We proved this rigorously: with only 3 units driven at a time, the network stores about
    `n^(1/4)/160` independent robust memories, for very large `n`.
* **Consequence for the research program.**
  * The original Lemma M (memory capacity `~ m + (mT/n)^2 + log^2 n`) is false.
  * The corrected target Lemma M' (`~ mT/sqrt n`) is consistent with this and remains the right
    goal.
  * The conjectured `n^(3/2)` barrier is untouched. This mechanism needs `mT ~ n` for only
    `~ n^(1/4)` memories, far from `Theta(n)` memories at `o(n^(3/2))` cost.
* **Feedback.** Repeated capture and leakage (second-order terms) provably stay a small
  perturbation in this mechanism. They neither help nor hurt capacity at scale.

## NEXT

1. Ask Codex to audit Theorem 6.1 / Cor. 6.2. Priority points:
   * Lemma 5.1(d), the out-of-window bound;
   * the pulse-source bookkeeping in Lemma 5.2;
   * the monotonicity argument for `eps_SO`.
2. Supply the dense-matrix transfer (Remark 6.4).
3. Push the construction to its limit. How many directions can sequential plus concurrent
   off-cycle leaks carry per unit `mT`? That probes how close Lemma M' (`mT/sqrt n`) is to tight.
4. Return to Lemma M_rest in operator form (PR #32 §6.4) for the centered channel.
