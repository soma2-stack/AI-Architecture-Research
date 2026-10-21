# PR34 current provenance and status — 2026-10-21

## Owner freeze — 2026-10-21

New mathematical research, experiments, training, and automatic follow-up work are frozen.
Read the [canonical claim register in consolidation PR38](https://github.com/soma2-stack/AI-Architecture-Research/blob/codex/claim-register-20261021/docs/CLAIM_REGISTER.md) before proposing work.
Historical next-action lists below are inactive provenance, not authorization. OPEN and
PENDING describe evidence gaps; they do not assign another task. Only explicit owner
authorization can reopen a retired direction. This update preserves evidence and does not
merge a scientific PR or claim that PR38 is already on main.

## Current review coverage

| Evidence | Exact revision and scope |
|---|---|
| [Original independent hostile audit](../codex_pr34_independent_audit_20261019/AUDIT.md) | b47eb08a281b26dc2273ee0e23ad745238e9ad2b; the audit's own claim-by-claim verdicts, including checker defects, are preserved verbatim. |
| [Fresh independent audit](../codex_pr34_fresh_audit_20261020/AUDIT.md) | 39af3a97dab0c20628c837e2b72da8c7e70a4e3d; existing R0-scoped review and independent certificate evidence. |
| Task 3 final-commit comparison | Comparing 39af3a97dab0c20628c837e2b72da8c7e70a4e3d with f515e48ed84f31f525d6b583cc4d9fb9ff8bbeeb resolves the narrow gap for **Lemma 5.0R and Proposition 5.4: VERIFIED (within scope)**, including the .3747 assertion and positive front-gate bound. This is separate from the earlier audits, not a standalone new audit of every final PR34 result. |

The three changed files in that final comparison are CHECKS.md, PROOF.md, and
envelope_certificate.py in this folder. Task 3's conclusion was established before this
cleanup; no proof review was repeated here. The preservation manifest records this
comparison separately without inventing a pre-existing permanent Task 3 report.

The R0/selected-metric theorem and original Lemma M refutation retain the exact scopes of
the preserved audits. Dense transfer is a separate PR35 result. The central robust
D=Omega(n), mT=o(n^(3/2)) problem remains **OPEN**.

The original reports and all necessary source snapshots, independent scripts and saved
outputs are now preserved in the two linked audit directories. Each PRESERVATION.json
records byte hashes and a hash-only comparison against immutable Git source; no audit
scripts were executed in this cleanup.

<details>
<summary>Historical author status at f515e48 (preserved; superseded for current review coverage)</summary>

# Status — claude_lemma_m_three_memory_20261019 (repaired 2026-10-20)

| Item | Status | Independent check |
|---|---|---|
| External probe results; schedules legal but outside (H) | NUMERICAL, exact | Codex reran (2026-10-19) |
| Second-order share trend and "timing beats duration" | trends REFUTED as general effects (small-n artifacts) | — |
| Prop. 2.1 locality; Prop. 2.2 uniform-query exactness; Prop. 2.3 first-order separation | PROVED (R0) | **Codex: PROVED** |
| Lemma 4.1 legality / support / exactness | PROVED; row-19 / age-17 bound `.3831` | **Codex: PROVED** (with that correction) |
| Lemma 4.2 first-order bound, `Pi(z) >= .6272 z` | PROVED | **Codex: PROVED**, rational certificate |
| First-version all-n certificate (`constants_so.py`) | **REFUTED** | Codex F1 |
| First-version separate-count rule for Cor. 6.2 | **REFUTED** | Codex F2 |
| Lemma 5.0R (`n`-dependent front gate; `t = 1` exception) | PROVED (author, 2026-10-20) | pending |
| Lemmas 5.1R, 5.2R with explicit births | PROVED (author); first-version local algebra Codex-verified under closure | pending (births) |
| Prop. 5.4: closure and `eps_SO <= .3747` for all `n >= 31622^4` | PROVED (author); exact rational envelope certificate | **pending — main audit target** |
| Theorem 6.1 (R0): robust `D >= n^(1/4)/161` section, `m = 3`, `mT = 1.5 n`, `n >= 1e18` | PROVED (author) | pending |
| Cor. 6.2 (R0): original Lemma M false for every constant, all `n >= n_1(C)` (`10^80` for `C <= 10^12`) | PROVED (author) | pending |
| Dense prescribed matrix | OPEN (Remark 6.4) | — |
| Lemma M', Lemma M_rest (operator form), centered channel, full metric, log loss, original problem | OPEN | — |

PRs #31, #32 and #33 are unchanged; this repair lives on a separate branch stacked on #33. No
merge was performed. AGENTS.md and the restricted notebooks were neither read nor edited.

</details>
