# Final cross-PR audit addendum — 2026-10-15

Audited base: PR #27 a67be6da53a539198fc82264606b88d74de67a00.
Companion base: PR #28 3746747137bb681ceda9c0f21b19e66d264165d1.

**PASS after the additional exact-identity correction below, in the stated scopes.**
Theorem 1 and the bath/protected/state foundations retain their assumptions and
constants. This does not certify the full-gradient original problem, which is OPEN.

## Newly demonstrated error: the injection must be gated

The previous repair corrected the homogeneous ordering but still printed
`btilde_t=a(UGU)P btilde_(t-1)+c_t U Ev`. Its additive term is false.
For post-gate reference credit, exactly

```
b_t=G_t(aO b_(t-1)+c_t Ev),
U b_t=a(U G_t U)P U b_(t-1)+c_t U G_t Ev.
```

For a unit coordinate probe v=e_d, zero raw inputs, and T=2, B1=0 and c2>0.
The omitted-gate formula errs by `c2 U(G2-I)e_d`, of norm `c2(1-g2[d])>0`.
At theorem-scale n=100000000 its value is about .002495:
`c2*tanh(.05-a*gamma*tanh(.05)/sqrt(k))^2`. This uses the reference R0 and
the prescribed zero initialization; no robust common-endpoint section is claimed.

The original (0.1), own/bus recurrences and Theorem 1's proof already include G_t
on the injection. Theorem 4 does not import Lemma 1.3. Thus this is an auxiliary
identity error, not a failure of the K-probe bound or the conditional Theorem 4.
No new assumptions were introduced.

## Verification and compatibility

Run `python -I theory/codex_pr27_repair_verification_20261015/check_full_post_gate.py`.
The new checker imports no author code. It checks the full recurrence for 160 steps
over odd/even small sizes and a scalar theorem-scale zero-input counterexample.
The corrected maximum residual is below 1.8e-14; the old formula fails.
Results and the proof's byte hash are in `full_post_gate_results.json`.

The previous independent foundation and repair suites were rerun without replacing
their historical outputs. The final companion record is on PR #28 in
`theory/codex_cross_pr_final_audit_20261015/`: exact bath/excess certificates,
fresh-source resets, coupled-state comparisons, K-probe accounting, weighted block
checks, legal-query bounds, release cases and resource constants all pass in scope.

PR #28's remaining `5.9e-4` intermediate is corrected there to `1/1700`, preserving
its final coefficient `1.9e-10`. Its older total-credit unrolling also receives
the missing front delivery. Neither changes the foundations imported from this PR.
Theorem 4 remains conditional on OPEN Hypothesis B, restricted to d_F,E and
`2N3<=D<=n` for its resource conversion, with its logarithmic loss.

Historical audit/results files are preserved. No restricted notebook was read or
modified; AGENTS.md was read and left unchanged. No training, GPU, merge or external
researcher contact occurred.
