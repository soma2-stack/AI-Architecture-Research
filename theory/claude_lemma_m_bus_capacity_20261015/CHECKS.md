# Checks — claude_lemma_m_bus_capacity_20261015

CPU only, numpy/decimal, threads capped at 8; about two minutes in total. The scripts do three
things: certify constants, check exact identities, and test structural claims on small random
adversarial histories.

**None of them proves a universal claim.** The theorems rest on PROOF.md.

| Script | What it checks | Result |
|---|---|---|
| `constants_check.py` | Lemma B: below-bath comparison sequence (8887 steps, outward margins), `Sigma_neg <= 506`, ceiling `.1009` self-consistent, `C_chain <= 558`. Theorem M: near residual with `b = 2`, far-long coefficient, `lam*` floor `1.8e6`, far-short cutoff, `K_neg`, BV constant, off-cycle coefficient, ledger. | all assertions pass: `Sigma_neg = 505.69`; ceiling map `.10082 <= .1009`; coefficients `7.6e14`, `2.03e14`, `1.32e8`; ledger `30/256` |
| `exp_two_channel_identity.py` | Prop. M1 on random `B'`, `O`, `g` (`k = 32, 200, 1000`) | residual `<= 5.8e-15`; `max |eps| = .20 <= .3404`; `max |w^T nu| = .93 <= 1.29` |
| `exp_gather_structure.py` | Random adversarial histories (`n = 256..1024`, `m = 12..40`): holes on random diagonals, a gather spike with 3% gaps, off-cycle holes, random large drives. **S1:** eight-part decomposition (4.1). **S2:** monotonicity of `K_pos`. **S3:** TV of cycle-row own profiles; TV bound for `K_uni + L_cyc + W`; off-cycle scalars. **S4:** Lemma B's ceiling and mass inequalities. | S1 `<= 8.6e-15`; S2 violation `0`; S3 cycle-profile TV `= 2.0`, TV ratio `<= .040`, off-cycle scalars up to `446` (hence part (d)); S4 no violation |
| `exp_offcycle_leak.py` | Two-history illustration of off-cycle leak capture (§5.2) at `n = 1024`, `H = 25..200` | exact endpoint; reconstruction `<= 4e-15`; dominant part is `L_off` on the modulated column (`.370 -> .478`, growing with `H`); the theorem-scale `H^2` law is NOT tested at this `n` |

**History of the checks.**
* A first version of S3 claimed `TV <= 4 c_max` for **every** own profile. It failed: off-cycle
  self-loops accumulate a single-column scalar of up to `~1/(1 - a ghat)` (bath) or the hold
  length (holes).
* That failure is why Theorem M treats off-cycle leak sources separately (part (d)). It also led
  to the off-cycle leak mechanism of §5.2.

Reproduce from this folder:

    python -I constants_check.py
    python -I exp_two_channel_identity.py
    python -I exp_gather_structure.py
    python -I exp_offcycle_leak.py
