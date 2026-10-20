# Step 3 report — the remaining memory channels (2026-10-20)

* **Base:** PR #35 at `aa47ca5` (Codex-corrected).
* **Branch:** `claude/remaining-channels-20261020`.
* **Folder:** `theory/claude_remaining_channels_20261020/`. PRs #34 and #35 are unchanged.
* **Verification:** nothing here has been independently verified.

## 1. What happened?

* **Phase A.** I rebuilt the complete readout decomposition. It combines:
  * Theorem 4's Step 3;
  * Prop. M1, extended to F-step queries through `chi = U nu`;
  * the nine-term identity on every spike row;
  * PR #32's two-stream split of the centered rows.

  This gives a 19-term ledger (PROOF.md Table 1.2), with every term marked bounded,
  conditionally bounded or uncontrolled, and its source.
* **Route 1.** I proved four new statements about the uncontrolled set: one closes a gap, one
  removes a term, and two bound mechanisms.
* **Route 2.** I tested a new candidate mechanism, the second-order relay through held arrival
  rows, by analysis and by an exact `n = 65536` simulation. I also re-examined the other levers
  (anti-holes, queries, codes, F-step, sources).
* **Checks.** Three numerical scripts and one exact certificate, all CPU-only. One experiment
  design error was caught and corrected; it is kept on record in `CHECKS.md`.

## 2. What did we discover?

* **The exact uncontrolled set** (Table 1.2):
  * U1: second-order gather (`K_bus`, `L_bus`);
  * U2: the centered channel (deviating-position capture, bath-coherent retention, excess
    retention);
  * the scope gaps: code-dependent schedules, driven sources in Theorem M, full-metric groups.
  * First-order gather bounds are *not* full-metric bounds. The ledger marks this explicitly.
* **Theorem M_F** (PROVED, certified). The first-order gather channel is listable for **all**
  legal queries, at polylogarithmic extra cost:
  `F_s^2 (mT/n)^2 + F_s^(4/3) (mT)^(4/3)/n` coordinates, residual `14/256 tau`, `n >= 1e10`.
  This closes the F-step part of the old Lemma M_rest.
* **Lemma 1.3** (PROVED, reduction). The own-type correction of Prop. M1 is `<= 1.4e-4 tau` at
  zeros of Theorem 4's listing, so it leaves Lemma M_rest.
* **Lemma D + Cors. D2–D3** (PROVED).
  * Rows held together damp their *common* content at rate `gamma s^2 |H|/k`.
  * A homogeneous retention set never holds more than the leaking row's peak own content.
  * This is a rigorous ceiling on the strongest centered mechanism found so far (PR #32's
    excess-retention leak).
* **Prop. R1 + Lemma R + Cor. R2** (PROVED).
  * For an off-cycle source, at **every order and for every legal query**, the source's own leak
    reaches the readout with at most `2.5x` its first-order gather scale.
  * No relay, feedback or query choice amplifies it.
  * The proof propagates with the true U-map, which is a contraction, instead of Lemma 1.2's
    row formula, which is exact but not contracting on the bus alone.
* **The relay** (ANALYSIS + NUMERICAL).
  * Undamped, it would be cubic in hold lengths, the only candidate found that could beat the
    first-order law.
  * Common-mode damping makes it own-sized instead. At `n = 65536` it peaks at `3.41`, which is
    22% of the direct first-order readout of the same pair, then collapses as damping sets in.
  * Its two terms (`K_bus`, `L_bus`) cancel near `H_g ~ 2 sqrt(k)`.

## 3. Did it work?

| Claim | Status |
|---|---|
| Complete ledger (Prop. 1.1, Table 1.2) | **PROVED** (bookkeeping; identities checked to `1e-14`) |
| Theorem M_F (first-order gather, all legal queries) | **PROVED** (author proof, exact certificate; unaudited) |
| Lemma 1.3 (own-type correction) | **PROVED** (reduction; linearity reading flagged for audit) |
| Lemma D, Cors. D2–D3; Prop. R1, Lemma R, Cor. R2 | **PROVED** (author proofs; identities checked) |
| The relay beats the first-order gather | **REFUTED** as a beating mechanism by Cor. R2's bound and the measured `22%` (its source-specific part is proved `<= 2.5x`) |
| Lemma M_rest: listings for U1 and U2 | **OPEN** (now narrowed to heavy off-cycle columns, cycle-column relays, and the own-spread capture term) |
| Conjecture C3: sub-barrier robust dimension `Theta((mT)^(4/3)/n)` | **CONJECTURE** (internal) |
| Original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`) | **OPEN** |

## 4. What does this mean for the linear-memory goal?

* Every mechanism examined is at most:
  * the first-order gather law, `D ~ (mT)^(4/3)/n` (sharp at constant width by PR #35); or
  * a quadratic law, `D ~ (mT/(c n))^2`.

  Both reach `D = Theta(n)` only at `mT = Theta(n^(3/2))`.
* The one candidate with super-quadratic per-column growth (the relay) is provably not amplifying
  in its source-specific part, and is measured to be weaker than first order.
* So the evidence continues to point to the barrier in the selected metric. It is **not a proof**.
  The listing obligations that remain are:
  * heavy off-cycle columns read through query-dependent time profiles (the excess-retention
    channel in general);
  * cycle-column relays, whose capture kernels are signed;
  * the own-spread capture term `U Delta w`.

  These are where a counterexample would have to live. The most concrete open test is
  inhomogeneous retention (E4).
* For the full fixed-feature metric, constructions transfer upward (PR #35 Prop. 5.1), but none
  of these upper bounds does.

## 5. What should Codex test or audit next?

* **Audit E1:** Lemma 1.3's reading of PR #28's Lemma 3.4, Lemma 7.3(c) and Step 4 as bounds
  that are linear in the weight cap.
* **Audit E2:** Theorem M_F. Check Lemma 2.1's three changes to Theorem M's proof and rerun
  `constants_mf.py`.
* **Audit E3:** Lemma D, Cors. D2–D3, Prop. R1, Lemma R, Cor. R2. Check the telescoping, the
  homogeneity claim, and `U e_1 = e_1 + (gamma/sqrt k) w`.
* **Experiment E4 (decisive):** inhomogeneous retention search. Staggered or duty-cycled
  retainers and anti-holes; measure the centered readout over peak own content against `n`
  and the number of retainers. Growth would be the first sign of a centered mechanism beating
  the quadratic law.
* **Experiment E5:** the relay at `n = 262144`.
* **E6 (sanity check):** the F-step channel split on PR #35's construction.

Full specifications are in PROOF.md §5.
