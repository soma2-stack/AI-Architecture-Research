# Checks — Lemma M_rest note (2026-10-16)

All scripts run on CPU with `python -I <script>` from this folder. Finite computations here
never prove universal claims; they check exact identities to floating-point accuracy, or
measure specified constructions.

| Script | What it checks | Result |
|---|---|---|
| `exp_two_stream_identity.py` (main) | Prop. S1 for random query vectors, arbitrary gates (holes, drives, row-0 deviations), `n = 64, 200`, `T = 70, 160` | relative residual `<= 5.6e-13`; (S1b) residual `<= 6.2e-15`; fitted row-0 coefficient `<= 9e-14` |
| `exp_two_stream_identity.py` (`creation_check`) | Prop. S5: `Z_t - M_t Z_(t-1) = xi_t` with the rank-`<=4` formula | relative residual `3.6e-15` (`n = 64`), `1.1e-14` (`n = 200`) |
| `constants_rest.py` | decimal certificates: `.3435(1 + 1/(e s_lo^2)) <= 203` (2.0); Lemma S4 front bound at `n = 1e8`, `m+1 = 1e-5 n` | `202.53`; `pre_1 >= 104.61`; `ln g_1 <= -207.8`; slope `.014855` |
| `exp_bath_scan.py` | free bath level versus `n` | `s ~ 0` at `n = 2048`; `.045, .0486, .0496` at `n = 16384, 65536, 262144` |
| `exp_bath_block.py` | §2 bath block and afterimage at `n = 65536` (column-restricted) | identical bus over never-driven off-cycle rows to `9e-13`; contrast gain `X = 2797`; best-query readout `8.5` (`H = 1000`) and `28.6` (`H = 4000`), about `1.3%` of the released own difference |
| `exp_retention_leak.py` | §5 excess-retention leak, `n = 65536`, `P = 0..1600`, `H = 2000, 8000`, re-drive every `1/100/300` steps | readout linear in `P` (`4.9, 18.6, 57.7`); `341.5` at `H = 8000`, about 10x the released own (`35.3`); `97%` kept at re-drive 100, `75%` at 300 |
| `colsim.py` | shared column-restricted two-history simulator (credit columns never mix, Prop. S1) | used by the three experiments above; legality `max |x| = .4500 < 1/2` |

**Self-review performed.**
* (2.0) was corrected twice during drafting (see PROOF.md §7, REFUTED rows).
* The resource-law constant in (5.2) was corrected from `3.1` to `6.2` after rechecking the
  retention cost against the re-drive experiment.
* No independent verification has been performed.
