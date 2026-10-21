# Checks — dense transfer of the sequential construction (2026-10-20)

All scripts are CPU-only and run with `python -I <script>` from this folder (BLAS threads `<= 4`).
* **[certificate]** marks an exact-rational check of the constants used in a proof.
* Every other row is NUMERICAL. It tests identities, premises and the size of terms on exact
  recurrences. It never proves a universal statement by itself.

| Script | What it checks | Result |
|---|---|---|
| `dense_tools.py` | explicit builders: R0 via the exact skeleton action; the **prescribed recipe** (power base `t`, the first `j` such that `B`, `B^-1` have no zero entry, `alpha = a/norm(B)op`); schedule S (spike from row 19, `A = .38`, parking); the actual-input simulator with dense credit `B` and R0-skeleton credit `B'` | used by all below |
| `exp_dense_S.py` | the explicit prescribed `R` at `n = 512, 1024`, five adversarial `theta` (both axes, equal coordinates, random, near-axis). E1 support and legality; E2 locality, zero-sum, `R Dh = alpha R0 Dh`, endpoint; E3 `norm(B - B')` vs the bound; E4 actual vs R0-skeleton readout, Prop. 2.2, other columns; E5 the full R-gradient by exact backprop | recipe: `t = 1`, `j = 0`, all entries of `R` and `R^-1` nonzero, `norm(R)op - a <= 1.5e-14`. E1: support 3, `max|x| = .380`. E2: off-pulse `<= 9e-16`, endpoint `<= 7e-16`, `norm(R Dh - alpha R0 Dh) <= 8e-17`. E3: `1.5e-10 / 2.8e-9` vs bound `5.2e-9 / 2.1e-8`. E4: relative difference `<= 4.1e-11`; column 0 `~1e-17`. E5: identity to `<= 7.7e-13`; `norm(dG)_F / norm(dG f_s) = 2.7–3.7` |
| `exp_dense_exact_mp.py` | explicit dense matrix in 60-digit arithmetic, `n = 256`, contract `eta` and stress `eta = 1e-2` | off-pulse differences, `1^T Dh` and endpoint **exactly 0.0**; `<= 3` nonzero inputs per step; `min abs(R_ij) = 6e-16` (contract), `3.9e-5` (stress) |
| `exp_generic_control.py` | controls with non-prescribed dense matrices (non-uniform rank-1, generic Gaussian), `n = 512`, `eps = 1e-3, 1e-6`, the same sparse actual inputs | prescribed form: endpoint `6e-16`, no spread. Non-uniform rank-1: endpoint `2.2e-7 / 2.9e-11`, spread to `255 / 236` coordinates. Generic: endpoint `3.6e-4 / 3.7e-7`, spread `511 / 255`. A one-step exact merge would need `~509` extra inputs |
| `exp_dense_large.py` | field-identity simulation at `n = 16384` and `65536`: Lemma 2.2D–2.3D facts at every `t`, legality, endpoint, credit correction vs bound, readout ratio; contract `eta` plus stress `1e-6, 1e-3` | all structural checks pass for every `eta` (support 3, endpoint 0, `min(sp - (k-4)s) = .1499`, `pre_1` margin `>= .0022`, `g_1 <= eps_g`, `h_1(1) = s_1`, bath `[.0448, .0500]`). Credit at the contract: `5.3e-11` (bound `2.0e-8`), readout ratio `1 - 2.5e-12`. Stress: `.93 / 365` per column, readout ratio `.994 / .015`. At `n = 65536` the contract run also passes (credit difference `1.3e-20`, readout identical); the stress run `eta = 1e-3` keeps the structure exact but leaves readout `4.6e-3` against `28.2` |
| `skeleton_certificate.py` **[certificate]** | Theorem 9.2. PR #34's `chain()` imported unchanged, with new exact rational primitive envelopes in `y = n^(1/12)` for `H = 250 N_3^2`, `r = 2D - 1 <= y^4/1200`, `F* ~ y^4`. Checks closure, final exponent `<= 0`, the robustness ratio `> .0567` and the fit `r(H+1) <= d - 41`; bisection for the least `y_*` | certified from `y_* = 21` (`n >= 7.36e15`): `eps_SO <= .38063`, robustness ratio `.0610`, `D >= 79` at `n_*`. Pointwise chain at `n_*, 1e24, 1e30, 1e40, 1e60, 1e100` dominated (`.0118` at `2.7e21` down to `.00657`) |
| `count_skeleton.py` **[certificate]** | Cor. 9.3: PR #34's listing polynomial (imported unchanged) against `D >= e^(u/3)/2400 - 2` | Lemma M fails for all `n >= 10^63` (`C <= 10^12`) and `10^78` (`C <= 10^18`) |
| `exp_skeleton.py` | `S_K` at `n = 65536` (`D = 3`, `r = 5`, `H = 2000`, exact `delta_*` over all 3-row subsets): saturation counts, support, endpoint, readouts, under R0, contract dense field and stress `eta = 1e-3`; random and adversarial `theta` (orthogonal to `D - 1` rows) | see the results table below |
| `constants_dense.py` **[certificate]** | dense field bound `.0763`; front-gate slack `<= .001`; per-column credit correction `<= 1.5e-8 c_*`; readout perturbation `<= 2.36e-9 n^(5/8)`; final inequality `.078 n (1 - n^-3/4)^2 - perturbations > .0567 n` for `n >= 1e18` | all pass (`.07624`, `1.6e-5`, `1.5e-8`, `2.35e-9`, `.0780 > .0567`) |

`exp_skeleton.py` (`n = 16384`, `D = 3`, `r = 5`, `H = 700`; 5 `theta` x {R0, contract dense, stress `eta = 1e-3`}):

| theta | saturated pairs (>= D = 3) | support | endpoint | skeleton readout | sqrt(#sat) x min saturated per-pair readout |
|---|---|---|---|---|---|
| random 1 | 4 | 3 | `<= 1.9e-16` | 18.02 | 16.43 |
| random 2, 3 | 5 | 3 | `<= 1.9e-16` | 19.98 | 18.37 |
| adversarial (orthogonal to rows 1–2) | 3 | 3 | `<= 1.9e-16` | 16.08 | 15.49 |
| adversarial (orthogonal to rows 4–5) | 3 | 3 | `0` | 14.87 | 14.24 |

* Contract-dense runs are identical to the R0 runs.
* Stress runs keep the same saturation, support and endpoint (exactly 0), with readouts about
  3% lower because the bath moves to `.046`.
* The readout always exceeds `sqrt(#sat)` times the smallest saturated per-pair readout, as in
  Theorem 9.2.

**Inherited and not rerun.** The R0 certificates of PR #34 (`envelope_certificate.py`,
`count_certificate.py`, `constants_seq.py`) are used unchanged. Lemma 3.1D shows that they apply to
the dense trajectory's gate sequence. They involve no matrix other than `R0`.

**Self-review.**
* *A false lead was removed.* A power-base-2 rank-one vector was first used as a "non-uniform"
  control. Its weight on the memory rows is `~2^-380`, so it tested nothing. It was replaced by a
  random positive vector.
* *An overclaim was corrected.* §7's statement that the mechanism "provably cannot" reach linear
  dimension was downgraded to ANALYSIS. Theorem M controls only the first-order gather channel.
* *The role of `eta` is stated explicitly.* The stress runs showed that the state facts do not
  need small `eta`, but the readout does.
* The large-`n` runs use the field identity, so they cannot see the contract-size dense term
  (`~1e-18`) in floating point. That term is checked by the exact-rational bound and by the
  explicit-matrix runs.

No independent verification has been performed.
