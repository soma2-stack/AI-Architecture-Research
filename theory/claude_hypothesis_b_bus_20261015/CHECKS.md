# Checks — claude_hypothesis_b_bus_20261015

All scripts run on CPU in under ten minutes in total, single process, numpy or decimal.
They check exact identities, certify constants, and illustrate the mechanism at small `n`.
**None of them proves a universal claim**; the theorem's regime `n >= 1.5e18` is reached
only by the proof in PROOF.md §2.

| Script | What it checks | Result |
|---|---|---|
| `exp_identities_u.py` | I1: uniform one-step query `U nu = a g sqrt(k) e_(d-1)`; I1F: `F = 2, 3, 7` steps give `(ag)^F sqrt(k) e_(d-F)`; I2: structured `O`, `O^T` vs dense `UPU`; I3: hole row recursion (Lemma 1.2) | `<= 1.4e-13`, `<= 4.4e-13`, `<= 1.6e-14`, `<= 4.5e-16` (`k = 64, 400, 2000`) |
| `exp_spike_decomposition.py` | Full credit recurrence of the construction for both histories (`n = 512, 1024, 2048`): the readout equals `a HI sqrt(k) Delta Y_T(d-1,:)`; the spike-path recursion reconstructs `Delta Y_T(d-1,:)`; per-term sizes | identity `<= 3.1e-13`; recursion `<= 7.8e-12`; the `ghat` pair cancels to `3e-11` |
| `exp_drift_capture.py` | Scaled construction (`n` up to 65536): legality, exact common endpoint, equal window states, no gate difference on any local path at `T` (so the readout is all bus), and agreement with the first-order drift-capture prediction | max input `.4726`; endpoint diff `<= 2.2e-16`; 0 local-path hits; prediction error `.60/.33/.165` at `ell/sqrt(k) = .35/.18/.12` |
| `constants_check.py` | Decimal certificates (50 digits) of every constant used in the proof of Theorem R: bath and `beta` ranges, wake bounds, input bounds, modulation factor, main coefficient, `tau/n`, budget threshold | all assertions pass; `||Gamma||/tau >= 2.082` |

At the simulated sizes the bus readout stays below `tau` (`Gamma/tau = .06–.11`), and the
1/k leak competes with capture when `ell` is comparable to `sqrt(k)`. Both effects are
consistent with the proof, which uses `ell = 120000` and `sqrt(k) >= 8.6e8`.

Reproduce, from this folder:

    python -I exp_identities_u.py
    python -I constants_check.py
    python -I exp_spike_decomposition.py 512 1024 2048
    python -I exp_drift_capture.py 4096 4096:16 16384:16 16384 65536:22
