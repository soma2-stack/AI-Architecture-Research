# Resume — dense transfer phase (2026-10-20)

* **Branch:** `claude/dense-transfer-20261020`, stacked on PR #34 (`f515e48`). PR #34 is not
  modified.
* Restricted lane notebooks were neither read nor edited.

## Current position

- **Lens:** does the R0 sequential-memory counterexample survive the prescribed fully dense
  matrix and the full metrics?
- **Stage:** Outcome A is reached (author proof).
  * Exact locality and endpoints hold for every rank-one field along `1`.
  * The dense credit correction is `<= 1.5e-8` per column.
  * Theorem 6.1D and Corollary 6.2D hold for the prescribed dense matrix.
  * Lower bounds pass to the full fixed-feature `d_F` and to the full `R/W/b` metric.
- **Learned:**
  * The transfer rests on zero-sum memory differences, which the prescribed dense part cannot
    see.
  * The tiny `eta` matters only for the gradient readout, not for the states.
  * Generic dense matrices would forbid local erasure (Prop. 6.1).
- **Limits:** `D ~ n^(1/4)` at `mT ~ n`. The certifying channel is capped by Theorem M at `o(n)`
  below the barrier.

## Exact next actions

1. Codex audit of Theorem 6.1D / Corollary 6.2D, Lemma 3.1D (the gate-fact list G1–G8 against
   PR #34's proofs), and Proposition 5.1.
2. Sharpen the off-cycle leak channel to a two-sided rate. The construction gives
   `D ~ mT/n^(3/4)`; Theorem M(d) gives only `(mT)^(4/3)/n`.
3. A rigorous no-go for gather-certified mechanisms needs Lemma M_rest (PR #32 §6.4).
