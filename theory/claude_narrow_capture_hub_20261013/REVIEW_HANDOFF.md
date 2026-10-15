# Review handoff — corrected narrow-capture proof

Original author: Claude. Audit-driven correction: Codex, 2026-10-15, starting from
PR #27 head 118b1e66ea327af0738249fc613208a544c4df60.

The independent audit is archived unmodified in
[AUDIT_20261014.md](../codex_pr27_repair_verification_20261015/AUDIT_20261014.md).
The correction and verification record is
[REPAIR_VERIFICATION.md](../codex_pr27_repair_verification_20261015/REPAIR_VERIFICATION.md).

## Preserved result

Theorem 1 retains 2.9e-10 D sqrt(n)/((K+2)(1+ln K)) for the specified fixed memory-probe
span, public envelope accounting and frozen model. Its fine dimension estimate still
requires T<Tcrit. Lemmas 2.1–2.5 and estimates (3.1)–(3.8) retain their imported numbers
and constants. No exact front destruction or total-hole own-only bound is used.

## Focus for a further review

1. Confirm that the own/bus decomposition is exact and the own bound is not applied
   to total credit or repeated off-cycle coordinates.
2. Check post-gate order a(UGU)P and the explicitly conditional front bound, including
   nonzero O(1/sqrt(k)) leakage.
3. Check the all-horizon scalar comparison with the same actual J field and the
   rational bath induction, including odd n and the infinite excess tail certificate.
4. Confirm the orthonormal probe basis, public support envelope, actual-input charges,
   exact initialization, and the one-step scope of Lemma 1.1.
5. Check source/row-0 cases in the auxiliary state/credit comparison and the separate
   horizon and Tcrit restrictions. The state-only estimate needs no credit listings.
6. Check compatibility with PR #28 head 3746747. Its Theorem 4 remains conditional on B
   and retains its explicit D range and logarithmic loss; this repair changes no PR #28 file.

For an independent follow-up audit, use a separate review folder and do not read or
edit lane notebooks. The owner's explicit repair instruction authorized the current
PROOF/report edits; the old handoff's read-only instruction applied to review work.
Do not prove B, train, merge or contact outside researchers as part of this handoff.

## Historical P1/P2 verification

VERIFICATION_P1_P2.md preserves the author's earlier second-party check and now has
an explicit correction notice. It is not the independent audit. Earlier finite-grid
passes did not catch the auxiliary or rounding errors identified by the later audit.
