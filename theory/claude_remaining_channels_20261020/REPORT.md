# Report — the remaining memory channels (Steps 3, 3.5, 3.6)

* **Branch:** `claude/remaining-channels-20261020`, draft PR #37.
* **Audits:** both Codex audits (`ac759bb`, `c48640d`) are copied verbatim and not edited.
* **Verification:** the Step 3.6 additions are not yet independently verified.

## Step 3.6: repairs (PROOF.md §R2; `repairs2_check.py`)

Every Step-3.5 counterexample was reproduced independently, by class reduction plus full-vector
cross-checks, and agrees with Codex to all printed digits.

| Claim | Outcome |
|---|---|
| Theorem 7.5, nonzero-initial readout extension | **REFUTED**: `n = 1e8`, `P = 1`, `m = 1`, `T = 3`, `E = Q = 0`, violation `1.50387`. Replaced by **Theorem 7.5'** (complete initial vector: damped mean, propagated contrast, explicit remainder), PROVED. |
| Theorem 7.3 cycle addendum | corrected: front starts counted over the expanded window (`<= 1 + floor((H+Lam-1)/d)`) |
| Cor. 7.4(b), universal finite saving factor | **REFUTED** (zero-input one-step retention); the asymptotic form is PROVED |
| Lemma 7.2 | dense forward coefficient corrected to `alpha a`. Universal positive drift **REFUTED** (`n = 1e8`, `m = 5000`: drift `-2.42e-6` with `I > 0`). Telescoped identity used for long intervals. Reset law labelled approximate, with exact discrete averages. |
| Per-column dimension condition (§7.5, §8.1) | **WITHDRAWN**; no replacement assumption |

## Step 3.6: new mathematics (PROOF.md §10; `phase2_check.py`)

* **Theorem 10.1** (PROVED).
  * *Scope:* any gates (time-varying, unequal, anti-holes), any initial vector, a nonautonomous
    bath, all captures kept.
  * *Statement:* every retainer's forced content is a **convex combination of the tail sums of
    one scalar common forcing**.
  * *Query-aware readout:* `<= A P max|Psi|`, plus explicit initial and capture terms.
* **Cor. 10.2** (PROVED, cost-aware). Forcing older than `W` reaches the readout only through
  `<~ 2(Lam+1) m_W (1 + Lam/W) + P e^(-kappa W/2)` effective rows, i.e. through
  input-maintained near-exact retainers.
* **Prop. 10.3** (PROVED). For **any time-invariant heterogeneous gates**, the stationary
  centered readout is `< A |F^ext| k/(gamma s~^2)`. For a hole-type source that is the own-sized
  ceiling `< A |Y(j)|`.
* **Prop. 10.4** (PROVED). For positive-deviation populations the cumulative forcing obeys an
  exact convex-averaging recursion. So internal feedback never amplifies: `max|Phi| <= sum(|F^ext| + |I|)`.
* **Precise obstruction (OPEN).** A **damped transient** bound (10.6) would remove the factor
  `P`. Anti-hole members are the sign problem.
* **Phase 3 decision experiment** (`exp_pump.py`, `n = 65536`). A contrast pump (switching
  retainers synchronised with the source) **saturates** (`.142` at `P_A = 4000`; `~.155` at
  `P_A = 1000` over 30 cycles). It does **not** beat plain retention by the held group alone
  (`.196`, `.213`) or the stationary ceiling (`<= .62 A`). No evading
  mechanism was found.

## Meaning for the original target

* The new theorems constrain retention mechanisms in three ways:
  * stationary heterogeneity is capped (Prop. 10.3);
  * old memory is cost-limited (Cor. 10.2);
  * positive-deviation feedback never amplifies (Prop. 10.4).
* They **do not** constrain the original target: (10.6) is unproved, anti-holes are uncontrolled,
  no dimension-counting principle is available, and everything is selected-metric only.
* The original problem remains **OPEN**.

## Earlier steps (unchanged in substance)

* Step 3: the ledger, Theorem M_F, Lemma 1.3, Lemma D, Prop. R1, Lemma R.
* Step 3.5: staggered resets are a finite-`n` constant gain. That analysis is in PROOF.md §§R, 7, 8.

## Next audit

PROOF.md §5:
* B1–B5: Theorem 7.5', Theorem 10.1, Cor. 10.2, Prop. 10.3, Prop. 10.4.
* B6: adversarial anti-hole transients against (10.6).
