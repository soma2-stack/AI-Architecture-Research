# Status — claude_lemma_m_bus_capacity_20261015

**Type:** author theory, with decimal certificates, exact-identity checks and small-n
structural tests. **Repository status:** PENDING INDEPENDENT AUDIT. This note builds on:
* PR #29 (`bd166b2`): Lemma 1.2, the own/bus split, Theorems R and R_D, all independently
  verified;
* PR #27 (`c987408`), §2;
* PR #28 (`0cc0a23`): Theorem 4 and Hypothesis B.

| Item | Status |
|---|---|
| Prop. M1: exact two-channel decomposition of the one-step bus readout (gather `a sqrt(k) gbar Delta Z_T(d-1)` + centered `|eps| <= .3404` + own-type correction) | PROVED; checked to `5.8e-15` |
| (4.1): exact eight-part decomposition of the gather row's bus | PROVED; checked to `8.6e-15` |
| Lemma B: bath ceiling `s_t <= .1009`, below-bath gap sum `<= 506` (sub-barrier domain) | PROVED; constants certified |
| Lemma C: deviation budget `Sigma_P <= 2(1 + 558) mT` | PROVED |
| **Theorem M: first-order gather channel listable** — size `9.1e5 + 9.7e14 (mT/n)^2 + 1.4e8 (mT)^(4/3)/n + 4`, residual `<= 30 tau/256`; `R0` or the prescribed dense `R`, undriven source, one-step queries; part (d) for public schedules | **PROVED** (author); independent audit requested |
| Prop. M2: a bus listing of size `O(mT/sqrt n + (m+1) W)` (Lemma M') suffices for the barrier law | PROVED |
| Lemma M in its original form (`C_0 m + C_1 (mT/n)^2 + C_2 log^2 n`) | likely FALSE for astronomically large `n` [ANALYSIS, §5.2: off-cycle leak capture, `D ~ m n^(1/4)/108` at `mT ~ 27 D n^(3/4)`] |
| Magnitude bound for the centered channel at listing zeros | heuristically false for `n >~ 1e20` [ANALYSIS, §5.3] |
| Lemma M_rest: second-order gather, entry, centered channel, F-step queries, code-dependent (d) | **OPEN** |
| Original problem (`D = Omega(n)`, `mT = o(n^(3/2))`, full `d_F`) | **OPEN** |

**Exact next action.** Prove the second-order gather part of Lemma M_rest by a Lemma-E-style
a priori fixed point for general sections in the regime `m <= epsilon sqrt(k)`. Then design a
time-grid listing for the centered channel.
