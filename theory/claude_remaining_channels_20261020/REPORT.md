# Report — the remaining memory channels (Step 3, repaired; Step 3.5)

* **Branch:** `claude/remaining-channels-20261020`, draft PR #37.
* **Base:** PR #35 `aa47ca5`. First version: `ac759bb`.
* **Audit:** Codex's independent audit is copied verbatim to
  `theory/codex_pr37_independent_audit_20261020/` and is not edited.
* **Verification:** the Step 3.5 additions are not yet independently verified.

## 1. What Codex found, and the repairs (PROOF.md §R; `repairs_check.py`)

| Finding | Repair | Status |
|---|---|---|
| Cor. R2 compared its new budget `S'_j` with the old own-leak budget `S_j`. `S'_j` contains an extra modulated-injection term. | Restated as a budget bound. The own-leak component is `< 2.5x` the first-order upper-budget scale; the injection is bounded by its own budget. | Bound PROVED. The "no amplification beyond 2.5x" reading is **REFUTED**: Codex's legal `n = 1e8` example has `S_j = 0` and readout `5.2002e-6`, rebuilt independently. |
| Cor. D3 ignored the damping of pre-existing common content. | Subtract the damped baseline `Lambda sigma_(t1)` (or assume zero initial content). The weights `.3435` / `1.18` apply only to non-spike rows. The source content is `Y(j)`, not `O(j)`. | PROVED in corrected form |
| Theorem M_F: "`n/F_s` increasing" is false (`F_s` is a ceiling). | Replaced by the continuous envelope `f(n)`. The Lemma 2.1 quantifier now includes the negative-capture condition. | PROVED; constants unchanged |
| Ledger scope. | Prop. S2's coefficients are one-step bounds; their F-step versions are OPEN. Notation fixed (`nu_l Delta O_l`). T8 charged (`+1.3335e-4 tau`). Front gates use S4's `sqrt(k)`-exponential. Lemma R recertified (`< 2.26959` / `< 2.32957`, all `n >= 1e8`). | PROVED bookkeeping |
| "Relay refuted" was too broad. | Only the own-leak component is controlled. | Relay OPEN |

**Still standing:** Prop. 1.1 and the nine-term identities; Theorem M_F; Lemma 1.3; Lemma D;
Cor. D2; Prop. R1; Lemma R; the displayed `S'_j` inequality.

## 2. Staggered sparse resets (PROOF.md §7; `exp_resets.py`)

* *Reproduced exactly* at `n = 65536`, `P = 2048`:
  * continuous holds: readout `48.0728`, `m = 2050`;
  * one reset per 64 steps, staggered: readout `47.6801` (`99.18%`), `m = 34`, `60x` lower `mT`.
* *Real under `mT`, not a shifted cost.* Staggering is what turns the per-row saving into a
  peak-width saving. Synchronous resets keep the signal (`99.0%`) but stay at `m = 2050`
  (Lemma 7.1).
* *Mechanism.* Every undriven row drifts up at the common rate `beta ~ s^3/3` (Lemma 7.2,
  an exact identity). A reset retainer's gate deficit is `~ (beta R)^2/3`.
  * A **symmetric target** `-beta R/2` cuts the loss about `3.6x` at equal cost: `99.77%` at
    `R = 64`, `96.4%` at `R = 256`.
  * Longer retention needs a shorter period (long-gap runs in CHECKS.md).
* *Cost-aware theorems.*
  * Theorem 7.3 (PROVED, every schedule): near-exact retention over `H` steps needs
    `>= (H - eps/kappa)/(Lam+1)` drives per row.
  * Theorem 7.5 (PROVED): near-homogeneous heterogeneous retainers (gate spread `E <= 1/4`, which
    covers staggered resets with `R <~ 1/(2 beta sqrt H)`) obey the own-sized ceiling up to the
    factor `~2`.
  * Strongly heterogeneous retention is OPEN.

## 3. Does it improve the memory-capacity scaling?

* **No.** It is a genuine constant-factor efficiency gain at moderate `n`, up to `~1/(beta sqrt H)`.
* It changes no asymptotic law and no proved bound:
  * the listing theorems already price retention by protected positions (Cor. 7.4);
  * the realistic reset cost `~ beta H^(3/2)` exceeds continuous holding for `H >~ 1/beta^2`;
  * for `D = Theta(n)` the reset branch scales as `beta n^(7/4)`, against `n^(3/2)` for
    continuous holds.
* A single `99%` signal is not `D`-dimensional memory: `D` columns at `>= tau/sqrt(D)` each are
  needed, and the per-column ceiling is own-sized.

## 4. The original target (PROOF.md §8)

* There are three bottlenecks:
  * leak dilution (Theorem M(d), Cor. R2);
  * the retention ceiling (Cor. D3, Theorem 7.5);
  * the non-free retention cost (Theorem 7.3).
* Together they leave `D = Theta(n)` at `mT = Theta(n^(3/2))` for every mechanism examined.
* A counterexample would need one of: strongly heterogeneous retention, own-spread capture,
  heavy-column time profiles, cycle relays, or a full-metric channel. All are OPEN.
* The original problem remains **OPEN**.

## 5. What Codex should audit next

* A1: the repairs.
* A2: Theorem 7.3.
* A3: Theorem 7.5.
* A4: Lemma 7.2.
* E7 (decisive): strongly heterogeneous retention against `n`.
* E8 (optional): resets on PR #35's skeleton section.

Specifications are in PROOF.md §5.
