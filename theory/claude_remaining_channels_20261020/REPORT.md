# Report — the remaining memory channels (Steps 3, 3.5, 3.6, 3.7)

* **Branch:** `claude/remaining-channels-20261020`, draft PR #37.
* **Audits:** all three Codex audits (`ac759bb`, `c48640d`, `18f8005`) are copied verbatim and not
  edited.
* **Verification:** the Step 3.7 additions are not yet independently verified.

## Step 3.7: repairs (PROOF.md §R3; `repairs3_check.py`)

| Claim | Outcome |
|---|---|
| (10.6) unweighted-tail bound and Conjecture 10.5 | **REFUTED**, withdrawn. Exact scalar witness `200000399/79992000`. Legal zero-input family: ratio `6.533` at `n = 2^18`, `T = 5300` (limit `6.613`; Codex `6.611` at `n = 1e8`). Unweighted tails count forcing that every bath row has forgotten; the filtered content stays `~.5` of the scale. |
| §10.8 tail-listing route | withdrawn as written: it misses the kernel term (now Prop. 11.7) |
| Prop. 10.3 | frozen bath stated (necessary); `<=` at `F^ext = 0`; source specialisation for the source-leak forcing only |
| Theorem 7.5' | `.660504` (not `.6605`). Witness: initial mean plus `Acq` = total. Displayed bound `2.2762e-8`; the recorded `1.8226e-8` is the older bound. |
| Cor. 10.2 | `1 <= W <= L`, `<=` at `W = L`; explicit initial-vector norm |
| Prop. 10.4, Lemma 7.2, `phase2_check` note | first-step boundary; `a' s_t/2`; nominal `P` capped at 3000 |

## Step 3.7: new mathematics (PROOF.md §11; `filtered_check.py`)

* **Theorem 11.3 — variation ceiling** (PROVED).
  * *Scope:* any gates (holes, anti-holes, switching), nonautonomous bath, signed feedback,
    initial vector, captures, any query; `eps P <= 1`.
  * *Bound:* `|chi^T y_T| <= A V(phi) + 2A(||y_(t1)||_1 + sum_t ||c_t||_1)`, where
    `phi = k F^ext/(gamma s~^2)` and `V` is its total variation (plus the first value).
  * *Proof:* exact adjoint representation, then a **sliding-box lemma**: backward partial sums of
    `eps s~^2 pi` stay in `[min(chi,0), max(chi,0)]`. Then one Abel summation.
  * *What it removes:* the factor `P`, the horizon, and the unweighted tails.
  * *Corollary:* Prop. 10.3's ceiling holds for **every** transient with constant forcing.
* **Prop. 11.6 — tightness** (operator level, NUMERICAL + ANALYSIS).
  * *Construction:* a nested-hold staircase (holes and bath rows only) with `K` forcing
    reversals.
  * *Result:* `2.81, 4.62, 6.43, 8.23, 11.81x` the stationary ceiling for `K = 1, 2, 3, 4, 6`;
    `.91`–`.99` of the variation bound.
  * *Consequence:* any transient bound of the form "universal `C` times the stationary ceiling"
    is **REFUTED**.
  * *Within the barrier budget:* `K = O(log n)` (ANALYSIS).
* **Prop. 11.7 — cross-history split** (PROVED). The readout difference is the forcing difference
  plus the kernel difference plus initial and capture differences. The kernel term is
  `<= R_chi Gamma + V(psi)`, where `Gamma = sum |Delta r| |z|` is a gate-difference budget.
* **Legal checks** (NUMERICAL, `n = 16384`).
  * The credit reduces exactly to the population operator (residual `<= 6.9e-14`), and the
    theorem holds in all legal histories.
  * *Example (E):* equal input support, same source schedule, exact common endpoints. The kernel
    term is `-2100` of a difference of `-2039` (`.42` of the stationary scale). Tail or forcing
    listing zeros do not control it.
  * *Legal two-history staircase (F):* exact gaps `0`; it did **not** realize the operator
    amplification (`.88`–`1.19x` one sustained level).

## Meaning for the original target

* Per history, the centered memory of a column is now bounded **exactly and tightly** by the
  variation of its external forcing.
* Across histories, Lemma M_rest's centered channel reduces to (i) `V(Delta phi)` and (ii) the
  kernel term, which is controlled by `Gamma`.
* Neither is yet bounded by listable or cost quantities in the barrier regime.
* No dimension theorem and no full-metric bound. **The original problem remains OPEN.**

## Earlier steps (unchanged in substance)

* *Step 3:* the ledger, Theorem M_F, Lemma 1.3, Lemma D, Prop. R1, Lemma R.
* *Step 3.5:* staggered resets give a finite-`n` constant gain.
* *Step 3.6:* Theorem 7.5', Theorem 10.1, Cor. 10.2, Prop. 10.3 (frozen bath), Prop. 10.4, and
  the contrast-pump experiment (saturates).

## Next audit

PROOF.md §5:
* C1–C4: Lemma 11.2, Theorem 11.3, Prop. 11.6, Prop. 11.7.
* C5: legal staircase at large `n`.
* C6: `Gamma` versus cost.
