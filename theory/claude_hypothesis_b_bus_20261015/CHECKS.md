# Checks — claude_hypothesis_b_bus_20261015

All scripts run on CPU, single process, with numpy or decimal (threads capped at 4); about
five minutes in total. They do three things: check exact identities, certify constants, and
illustrate the mechanism at small `n`.

**None of them proves a universal claim.** The theorem's regime `n >= 1.5e18` is reached only
by the proof in PROOF.md §2: Lemma E plus the decimal certificate.

| Script | What it checks | Result |
|---|---|---|
| `exp_identities_u.py` | Identities at `k = 64, 400, 2000`. **I1:** uniform one-step query `U nu = a g sqrt(k) e_(d-1)`. **I1F:** `F = 2, 3, 7` steps give `(ag)^F sqrt(k) e_(d-F)`. **I2:** structured `O`, `O^T` vs dense `UPU`. **I3:** hole-row recursion (Lemma 1.2). | `<= 1.4e-13`, `<= 4.4e-13`, `<= 1.6e-14`, `<= 4.5e-16` |
| `exp_spike_decomposition.py` | Full credit recurrence of the construction for both histories (`n = 512, 1024, 2048`). The readout equals `a HI sqrt(k) Delta Y_T(d-1,:)`; the spike-path recursion reconstructs `Delta Y_T(d-1,:)`; per-term sizes. | identity `<= 3.1e-13`; recursion `<= 7.8e-12`; the `ghat` pair cancels to `3e-11` |
| `exp_error_bounds.py` (new, round 2) | Lockstep U-coordinate simulation with own parts `O` and bus parts `Z = Y - O`, at `n = 512, 1024, 2048` and `2048` with `ell = 32`. **X1:** Lemma 1.2 for every U-row at every step. **X2:** broadcast identity (9.3). **X3:** own differences supported on rows `d-10..d-1`. **X4:** the Step-10 decomposition (main + init + arrival bus + kappa + leak + w-injection) reproduces `Delta Y_T(d-1)`. Evaluates (E1)–(E6) and (10.1) with measured sups and measured small-`n` constants. | X1 `<= 6.5e-16`; X2 `<= 8.4e-15`; X3 support exactly `d-10..d-1`, 0 violations; X4 `<= 3.4e-13`; all 7 inequalities hold, LHS/RHS `<= .71` |
| `exp_drift_capture.py` | Scaled construction (`n` up to 65536): legality, exact common endpoint, equal window states, no gate difference on any local path at `T` (so the readout is all bus), and agreement with the first-order drift-capture prediction. **Round 2:** predictor arrival set corrected (Codex P2) and rerun. | max input `.4726`; endpoint diff `<= 2.2e-16`; 0 local-path hits; prediction error `.60/.33/.165` at `ell/sqrt(k) = .35/.18/.12` (unchanged to `1e-14` by the fix) |
| `constants_check.py` | Decimal certificates (50 digits) of every constant in the proof of Theorem R, in five groups (details below). | all assertions pass; `||Gamma|| >= .11790 n >= 2.0826 tau` |

The five groups certified by `constants_check.py`:
* **(A)** bath, `beta`, wake, inputs, modulation factor;
* **(B)** front-chain sums of Lemma 1.5: `51.65`, `11.81`;
* **(C)** budgets `Sigma, Dbar <= 314`, `Oh <= 346.70`, `OD <= 258.79`;
* **(D)** the Lemma E majorant system at `k = 7.5e17`: a certified super-solution `x*` with
  `b + M x* < x*`;
* **(E)** main term `>= .11791 n`, `E_Y <= 1019`, readout error `<= 5.6e-7 n`, `tau/n`, and
  the budget threshold.

**Reading the small-`n` runs.**
* At the simulated sizes (`sqrt(k) <= 181`) the bus readout stays below `tau`
  (`Gamma/tau = .06–.11`).
* At these sizes the bus contents of arrival paths are of the same order as their own
  differences. The full bus `Z^-` (mostly w-injection) is `~ Lam/sqrt(k)`, which is not small
  here. This is why the first-order prediction is off by `16–60%`.
* Lemma E shows these contents scale like `Lam/sqrt(k)` and `Dbar/sqrt(k)`. With `ell = 120000`
  and `sqrt(k) >= 8.66e8` they are `<= 4.3e-4`, against own differences of about 259.

Reproduce, from this folder:

    python -I exp_identities_u.py
    python -I constants_check.py
    python -I exp_spike_decomposition.py 512 1024 2048
    python -I exp_error_bounds.py 512 1024 2048 2048:32
    python -I exp_drift_capture.py 4096 4096:16 16384:16 16384 65536:22
