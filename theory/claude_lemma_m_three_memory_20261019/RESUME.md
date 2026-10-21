# Resume — sequential off-cycle construction, repaired (2026-10-20)

## Owner freeze — 2026-10-21

New mathematical research, experiments, training, and automatic follow-up work are frozen.
Read the [canonical claim register in consolidation PR38](https://github.com/soma2-stack/AI-Architecture-Research/blob/codex/claim-register-20261021/docs/CLAIM_REGISTER.md) before proposing work.
Historical next-action lists below are inactive provenance, not authorization. OPEN and
PENDING describe evidence gaps; they do not assign another task. Only explicit owner
authorization can reopen a retired direction. This update preserves evidence and does not
merge a scientific PR or claim that PR38 is already on main.

Current audit provenance is in [STATUS.md](STATUS.md); pending/next-action language below is historical.

* **Branch:** `claude/lemma-m-sequential-repair-20261020`, stacked on PR #33
  (`claude/lemma-m-three-memory-20261019`, `d6801c2`).
* **Audit:** Codex's audit of PR #33 is copied unchanged to
  `../codex_pr33_independent_audit_20261019/`.
* Restricted lane notebooks were neither read nor edited.

## Current position

- **Search lens:** robust bus capacity under the actual resource `mT` (peak width times horizon),
  in the frozen dense-tanh RNN, with the selected `d_F,E` metric.
- **Stage:** repair after the audit.
  * The `n`-dependent front-gate bound (Lemma 5.0R) is in place.
  * Every birth term is explicit.
  * An exact all-n envelope certificate (Prop. 5.4) replaces the refuted grid certificate.
  * Cor. 6.2 now uses the combined count.
- **Strongest results (author; re-audit pending):**
  * Theorem 6.1 (R0): `D >= n^(1/4)/161` robust directions at `m = 3`, `mT = 1.5 n`, for every
    `n >= 10^18`.
  * Cor. 6.2 (R0): the original Lemma M is false for every choice of constants, for all
    `n >= n_1(C)` (`10^80` if `C <= 10^12`).
- **Closed / negative:**
  * Codex F1–F4 findings on the first version: the grid certificate, the separate-count rule,
    the row-20 description, and the all-`t` gate statement.

## Open

- An independent re-audit of Lemma 5.0R, the explicit births, `envelope_certificate.py` and
  `count_certificate.py`.
- The dense transfer (Remark 6.4).
- Lemma M' tightness.
- Lemma M_rest in operator form (PR #32).
- The log loss.
- The original problem.

## Exact next action

1. Request Codex's re-audit of the repair. Focus on:
   * the transcription of `chain()` against PROOF §5;
   * the primitive envelopes;
   * Lemma 5.0R's induction.
2. If the re-audit passes, write the dense transfer:
   * a dense Lemma 5.0R;
   * a `B - B'` estimate in the style of PR #29 Lemma D1;
   * the readout term.
