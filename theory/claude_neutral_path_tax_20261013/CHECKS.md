# Checks (diagnostic only)

Environment: Python 3.11.9, numpy 2.4.6, torch 2.13.0 (CPU), float64. Runs are single
process at BelowNormal priority with at most 4 threads. Finite-n numerics do not prove
asymptotic claims; see PROOF.md for status labels.

## run_checks.py → run_checks_result.json (≈ 80 s)

| Key | What | Result |
|---|---|---|
| A | Lemma 1.1 identities (n = 2000): orthogonality, row identity, `O e0 = e0`, `O u`, broadcast `O e_(d-1)` | all errors `<= 5.8e-15`; broadcast entry `.031589` vs `1/sqrt(k) = .031623` (factor `1 - gamma^2/k`) |
| B | background and holes (n = 16000, W = 30) | hole maintenance input before window `<= 1.57e-4`; max input overall `.428`; hole credit at first broadcast `43.06` (`c_h/sqrt(k) = .481`; model `.442`) |
| C | hub, vertex code, W = 30 | n = 4000: total/control/hole `.0162/.0172/.0018`; n = 8000: `.0185/.0191/.0025`; n = 16000: `.0144/.0147/.0025`; endpoints `<= 3e-14`; inputs `< .45` |
| D | W scan, n = 16000 (hole term vs reduced model) | W = 5: `.00092/.00097`; 10: `.00156/.00153`; 15: `.00200/.00185`; 20: `.00226/.00205`; 30: `.00249/.00224`; 80: `.00255/.00245`; C/n = 4.0, 7.5, 11.1, 14.6, 21.7, 56.6 |
| E | continuous code points (M = 8, ≈ 90% saturated), n = 16000, W = 30 | hole term `.00241, .00240, .00241` |
| F | autograd end-to-end (actual tanh recurrence, R leaf, frozen inputs, legal future step) | relative error `4.4e-16` (n = 400), `3.0e-15` (n = 800) |
| G | reduced model, n → ∞ (s = .99) | W = 10, 20, 30, 80: `.00169, .00229, .00251, .00265`; ceiling `.00268` |

## scaling.json (scaling_run.py, single runs)

| n | W | total | control | hole term | C/n | notes |
|---|---|---|---|---|---|---|
| 32000 | 80 | .01131 | .01150 | .00250 | 58.6 | from exploration script (same construction) |
| 64000 | 30 | .00724 | .00730 | .00245 | 22.7 | exploration script `hub7.py` (identical code path) |
| 128000 | 30 | .00510 | .00513 | .00246 | 22.8 | 577 s; endpoint `2.2e-16`, max input `.423` |

The control term scales as `n^(-1/2)` (.0147, .0073, .0051 at 16k, 64k, 128k). The hole
term is flat (.00249, .00245, .00246).

## Exploration path (scripts in `exploration/`, provenance only)

1. `probe1.py` checks the O identities, the autonomous bath and front, and the free-hole
   drift (≈ `4e-5` per step, so holes need maintenance).
2. `hub.py` / `hub2.py` / `hub3.py` are the first design: one hole, uniform `v`, off-cycle
   writes. The separation seemed to shrink with n. This was explained by an opposite-sign
   bath term ∝ `400/sqrt(n)`. The hole-only term rose to a plateau ≈ `5.5e-5` per stage.
3. Zero-sum `v` removes the `1/sqrt(n)` bath term from the control.
4. `hub4.py` tested multi-step legal queries. They are worse: each future step's
   mean-subtraction removes common gain, and the pair contrast shrinks by the mean gate.
5. `hub5.py` holds the written rows through W consecutive broadcasts. The gain saturates,
   which the mass-equilibrium explains.
6. `hub6.py` adds co-moving cycle pairs. It also showed that the full gradient (with the
   bias group) would be about `sqrt(5)` times larger, but the contract metric d_F is the
   selected-source gradient only, so that factor is not used.
7. `hub7.py`, the final design: long holes from row 40, zero-sum `v` with its negative part
   off-cycle, pairs beyond the wake. The hole term is ≈ `.0025` and flat in n. `hubcore.py`
   is the cleaned version.
8. `hub8.py` checks continuous codes. `reduced.py` is the type-level model.
