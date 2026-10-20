# Report — dense transfer of the sequential memory construction (2026-10-20)

Claude (Opus 5.5). Proofs are in `PROOF.md`, checks in `CHECKS.md`. The PR #34 result is used
unchanged and not edited. Nothing here is independently audited yet.

## Milestone verdict: Outcome A (transfer possible)

* **What happened.** The memory construction S of PR #34 was run on the repository's exact
  prescribed matrix, `R = alpha (R0 + eta 1 1^T/n)`, `eta <= 1e-8/n^2`, every entry nonzero. Inputs
  were accounted as the actual nonzero inputs. Its robustness theorem and the refutation of
  Lemma M were then re-derived for that matrix.
* **Did it work?** **PROVED** (author; audit pending):
  * **Theorem 6.1D.** For every `n >= 10^18`, the same schedule has 3 active input coordinates,
    horizon `n/2`, exactly common endpoints, and `D >= n^(1/4)/161` robust memory directions in
    the actual dense selected metric.
  * **Corollary 6.2D.** The original Lemma M is false for the prescribed dense matrix, with the
    same thresholds as for `R0`.
  * **Proposition 5.1.** The section is also robust in the full fixed-feature metric `d_F` and in
    the full `R/W/b` gradient metric. These are lower bounds only.
* **What did we learn?**
  * The memories are written in balanced pairs (`+v` on one unit, `-v` on another). The dense
    part of the prescribed matrix only ever sees the *sum* of all states, and the two histories
    always have the same sum.
  * So dense mixing is literally invisible to the memory differences. Separation, sparse inputs
    and exact endpoints survive *exactly*, not approximately.
  * The only new effect is a tiny correction in the learning credit, at most `1.5e-8` per memory,
    against a signal of order `n`.
* **What's next?** A Codex audit of the transfer (focus: the list of gate facts G1–G8 in
  Lemma 3.1D).

## Second development: a better memory code (`n^(1/4)` -> `n^(1/3)`)

* **What happened.** In S each memory has its own pair, so every pair must be held long enough to
  pass the threshold alone (`~40 n^(3/4)` steps). Instead, spread `D` memories over `2D - 1` pairs
  with a *saturation code*: each pair's amplitude is a clipped linear combination
  `clip(L (M theta))` of the memory vector, with `M` a Vandermonde matrix.
  * Any `D` rows of `M` are independent, so every memory direction drives at least `D` pairs to
    full amplitude (Lemma 9.1).
  * The readout then grows like `sqrt(D)`, and each pair needs only `~250 n^(2/3)` steps.
* **Did it work?** **PROVED** (author; exact rational certificate; audit pending), Theorem 9.2:
  * dimension `D = floor(floor(n^(1/3))/2400)` with the same 3 active inputs and cost `mT = 1.5 n`;
  * this holds for every `n >= 10^16`, for `R0` and for the prescribed dense matrix;
  * the second-order part is `<= .381` of the first-order signal, and the robustness ratio is
    `.0610 > .0567`.
* **What did we learn?**
  * (a) The first-order off-cycle channel's capacity at constant width is `Theta(n^(1/3))`.
    Theorem M(d)'s upper listing `(mT)^(4/3)/n` is sharp in order (Cor. 9.4). The old
    one-memory-per-pair code wasted a factor `n^(1/12)`.
  * (b) The Lemma M failure threshold improves from `10^80` to `10^63` (Cor. 9.3).
  * (c) Even with this code, linear dimension would need `mT ~ n^(3/2)` (Remark 9.5, ANALYSIS):
    the barrier scale, not below it.
* **What's next?**
  * Write the second-order analysis with several concurrent pairs, to turn Remark 9.5 into a
    theorem.
  * That would show the gather channel reaches `D = Theta(n)` exactly at the barrier scale.

## Answers to the five questions

* **A. Does dense mixing destroy separation?** No, for the prescribed matrix.
  * Memory differences sum to zero, so `R Delta h = alpha R0 Delta h` exactly (Lemma 2.1D).
  * Checked exactly at 60 digits, and at `1e-16` on the explicit matrix.
  * For a *generic* dense matrix (a different problem) local erasure is impossible in one step
    (Prop. 6.1). Controls spread the differences to 236–511 of 512 coordinates.
* **B. Can the inputs stay sparse?** Yes: the physical input support is 3 at every step.
  * Internal state activity is all `n` coordinates: the dense field and the bath move every unit,
    but these are not inputs.
  * The "reference" input `x + (R - R0)h` is dense, but it is not the contract's measure.
  * The public support envelope is the 3 driven rows.
* **C. Exact endpoints?** Yes, exactly, for every `alpha` and `eta` (Lemma 2.1D). This is
  verified as exactly 0 at 60 digits.
* **D. Additional interference?**
  * The dense credit term obeys `||B - B'|| <= T ||R - R0|| c n <= 1.5e-8` per column
    (Lemma 3.2D; measured `3e-9`).
  * The front-gate and second-order bounds of PR #34 transfer verbatim (Lemmas 2.3D, 3.1D).
  * *Caution* (stress tests): the state facts hold for any `eta`, but at an off-contract
    `eta = 1e-3` the credit term destroys the readout (1.5% left). The contract's tiny `eta` is
    what protects the gradient memory.
* **E. Full readout?** Lower bounds pass upward.
  * The full fixed-feature readout contains the selected columns.
  * The full R-gradient's Frobenius norm dominates its fixed-feature projection.
  * Exact backpropagation confirms the identity to `1e-12`; the full gradient difference is
    2.7–3.7 times larger.
  * This does not bound the full metric's dimension from above (it is `Omega(n^2)` in the full
    model).

## PROVED / REFUTED / OPEN

* **PROVED (author):**
  * Lemmas 1.1, 2.1D, 2.2D, 2.3D, 3.1D, 3.2D;
  * Theorem 6.1D and Corollary 6.2D (prescribed dense matrix);
  * Prop. 5.1 (full metrics, lower bounds);
  * Prop. 6.1 (one-step merge obstruction for m-generic matrices);
  * Prop. 7.2 (a reusable dense-transfer principle for balanced constructions);
  * Lemma 9.1, Theorem 9.2, Corollaries 9.3 and 9.4 (saturation code, `n^(1/3)`, sharpness of
    Theorem M(d)).
* **REFUTED:**
  * "Dense mixing forces dense inputs": refuted for the prescribed matrix (support 3).
  * My own draft control with a power-base-2 vector: it tested nothing (weight `2^-380` on memory
    rows) and was replaced.
* **OPEN:**
  * A rigorous statement that this mechanism family cannot reach linear dimension below the
    barrier. Theorem M gives the ANALYSIS; the full no-go needs Lemma M_rest.
  * Constructions for generic dense matrices.
  * The original problem: `D = Omega(n)` at `mT = o(n^(3/2))` in the full `d_F`.

## Plain-English significance

* The counterexample to our old memory-counting rule was not an artifact of the simplified
  matrix. It holds in the actual dense architecture we committed to.
* Writing memories in balanced pairs is a structural trick that makes them immune to this kind
  of global mixing.
* But the mechanism stores only about `n^(1/4)` memories (`n^(1/3)` with the better code) for a
  cost of about `n`. Linear memory at less than `n^(3/2)` cost would need a different channel.

## Next research steps

1. **Codex audit:** Theorem 6.1D, Lemma 3.1D (G1–G8 against PR #34), Prop. 5.1.
2. **Tight rate of this channel: done at constant width** (§9). The saturation code matches
   Theorem M(d)'s `(mT)^(4/3)/n`. The remaining work is the general-width second-order analysis
   (Remark 9.5).
3. **Rigorous no-go for gather-certified mechanisms below the barrier:** this requires
   Lemma M_rest (centered channel, second-order terms) at the listing zeros.
