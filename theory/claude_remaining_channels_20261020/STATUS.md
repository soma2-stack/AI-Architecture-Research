# Status — the remaining memory channels (Step 3)

* **Branch:** `claude/remaining-channels-20261020`.
* **Base:** PR #35 `aa47ca5`.
* **Owner:** Claude.
* **Verification:** no independent verification yet.

## Current search lens

Close or refute Lemma M_rest by splitting the bus into exactly identified channels. Two tools
from this step:
* common-mode damping (Lemma D);
* the contracting true U-map (Prop. R1 / Lemma R).

## Strongest results

| Result | Status | Scope |
|---|---|---|
| Prop. 1.1 + Table 1.2: complete ledger | PROVED | every legal query |
| Theorem M_F: first-order gather, all legal queries | PROVED, certified | (H), `n >= 1e10`, public schedules for (d), undriven sources |
| Lemma 1.3: own-type correction `<= 1.4e-4 tau` | PROVED (reduction) | zeros of `Phi`; linearity reading to audit |
| Lemma D, Cors. D2–D3: common-mode damping, retention ceilings | PROVED | homogeneous hole sets |
| Prop. R1, Lemma R, Cor. R2: no amplification of off-cycle source leaks | PROVED | S4 domain (`m+1 <= 1e-5 n`), every order and query |

## Killed or closed directions

* The relay as a beating mechanism. Its source-specific part is proved `<= 2.5x` first
  order; measured at 22% of the direct readout.
* Anti-hole damping compensation: costs more than it saves (ANALYSIS).
* Codes or queries changing the per-column law (ANALYSIS).
* Experiment-design note: without a release gap, relaxation leaks fake second-order effects.

## Open

* U1 and U2 listings. Remaining pieces:
  * heavy off-cycle columns (query-dependent time profiles);
  * cycle-column relays (signed capture kernels);
  * the own-spread capture term `U Delta w`;
  * the common W-part (T15).
* Scope gaps:
  * code-dependent Theorem M(d) and M_F(d) (U4);
  * driven sources (U6);
  * the full metric (U5);
  * `F_ent` for `1e-5 n < m+1 <= 5e-5 n`.
* Lowering Theorem M_F's `F_s^2` to `F_s` needs per-row F-step weights.
* Original problem: OPEN.
* Conjecture C3: internal.

## Unresolved prior-art questions

None new. The mechanisms are internal to this model; no external literature claim is made.

## Exact next action

1. Run Codex E4 (inhomogeneous retention). If the readout-over-peak ratio stays bounded,
   attempt an ℓ1 version of Cor. D2 for gate-homogeneous sets with joins and leaves. That would
   close the retention part of U2 up to heavy columns.
2. Then attack the heavy-column problem. Express the query's time profile
   `chi^T Phi^U(T,t) w` through the window equalities at zeros of `Phi`, and test whether a
   window-length basis suffices.
