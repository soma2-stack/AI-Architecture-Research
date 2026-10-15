# Narrow capture through the Householder hub — corrected report

Original author: Claude, 2026-10-14. Independent audit and corrections: Codex,
2026-10-15. Frozen dense-tanh model, fixed source feature and recurrent normalization
unchanged. Current mathematics: [PROOF.md](PROOF.md). Historical audit and reproducible
checks: [repair verification](../codex_pr27_repair_verification_20261015/REPAIR_VERIFICATION.md).

## Current result and scope

Theorem 1 retains its verified coefficient. For n>=1e8, a robust public-schedule
section certified by a fixed orthonormal memory-probe span of rank K satisfies

    mT >= 2.9e-10 D sqrt(n)/((K+2)(1+ln K)).

Here m is the public envelope width. With a common exact support this is the actual
peak width; a possibly larger envelope must not be charged as a smaller pointwise
support. All actual dense inverse-lift inputs and the full preparation/reset horizon
are counted. This support-count result alone gives no absolute-input-energy bound.
The sharpened dimension bound retains its condition T<Tcrit and its ln K term:

    D <= 1e6 (K+2)(m+1)(1+ln K+ln+((T+1)/sqrt(n))).

For fixed K and D=Theta(n), the resource bound is Omega(n^(3/2)). It does not rule out
unrestricted multi-probe sections. The group here contains only memory-row directions
v f_s^T with v supported on rows 1..k-1; it is not the full R/W/b gradient.

## What the independent audit preserved

* Exact Householder row transport, with injective local predecessors and no local wrap.
* The exact bath identity, moving-bath gap inequalities and Lambda=450000.
* The bath floor s>=.025 at m<=5e-5 n and n>=1e8, with corrected finite-size arithmetic.
* Protected count (m+1)(Lambda+1), outside-state bound .0124 and kappa=1.5e-4.
* Dense state/gate/credit comparison (3.1)–(3.8), in its stated horizon/budget ranges.
* Exact equal histories when W=T and the original Theorem 1 resource coefficient.

The bath comparison now holds at every horizon: chains use the same actual J field
and their scalar error is at most rho(1-a^A)/(1-a)<=n rho<=4e-8/sqrt(n).
The separate coupled-state comparison still uses W<=T<=n^(3/2).

## Withdrawn claims and their corrections

The previous total hole-credit bound omitted incoming bus deliveries. It is now an
own-injection cycle-path bound; off-cycle own content uses its repeated-coordinate
geometric sum. A legal neutral hole with zero own injection nevertheless receives
positive bus credit. That negative result is preserved in the audit and checker.

For post-gate credit the correct U-coordinate operator is a(UGU)P. No finite tanh
transport destroys a nonzero packet exactly. Under an explicit front-mass condition,
the dominant front contribution is attenuated, with nonzero order-1/sqrt(k) leakage
retained. The exact uniform/contrast decomposition remains valid, but it is not a
universal lifetime or accumulated-bus theorem.

The one-step separation functional uses exact gate constants and tau/Dg, not an
upward-rounded .33n threshold. Borsuk–Ulam gives an antipodal zero, not the previously
asserted geometric zero subsphere. A one-step inference requires one-step certification.

## Proof mechanism

List recent scheduled inputs, predecessor state/credit values, global J/Sum/c
channels, and protected initial state/credit values. At a Borsuk–Ulam zero, the
auxiliary protected differences vanish and the ordinary unprotected part contracts.
The actual dense perturbation includes state-to-gate-to-credit feedback. For T<Tcrit
its projected error remains below 3.3e-7. Larger-horizon resource cases use D<=nK
instead of extrapolating that error estimate. The theorem does not use front
saturation, an own-only bound on total credit, or the informal hub accounting.

## Relation to PR #28

Compatibility was checked against head 3746747137bb681ceda9c0f21b19e66d264165d1.
All imported lemma/equation numbers and constants are preserved. Theorem 4 needs
only the state part of the listings and comparison, in a valid horizon range.
PR #28 separately extends fixed-K certificates to code-dependent pointwise supports.
Its inherited 5.9e-4 intermediate rounding should be read as the exact 1/1700;
its final 1.9e-10 coefficient still follows. PR #28 was not modified.

Its larger group {u f_s^T:u_0=0}, including source directions, remains distinct from
this note's memory-probe group. Its Theorem 4 is CONDITIONAL on OPEN Hypothesis B;
for 2N3<=D<=n its stated resource bound has the asymptotic logarithmic loss.
Neither that conditional result nor this repaired theorem resolves the original problem.

## Status

| Claim | Status |
|---|---|
| Theorem 1 in its stated group, schedule and resource scopes | PROVED; independently checked with these corrections |
| Own-path bound, exact operator order and contrast split | PROVED in their stated scopes |
| Front attenuation | PROVED conditional on the explicit mass condition; no exact destruction |
| Old total-hole and exact-destruction claims | REFUTED as stated; counterexamples/history retained |
| General neutral-path tax | CONJECTURAL |
| Hypothesis B | OPEN; not attempted during this repair |
| Original frozen dense-tanh strict-budget problem | OPEN |
| New primitive or architecture discovery | Not established by this result |

## Reproduction and history

Run the independent scripts from the repository root:

    python -I theory/codex_pr27_repair_verification_20261015/check_foundations.py
    python -I theory/codex_pr27_repair_verification_20261015/check_repairs.py

The original checks.py and verify_p1p2_sweep.py remain additional CPU diagnostics;
finite sweeps alone are not proofs. The independent infinite-sum and bath-margin
certificates use exact integer/rational arithmetic.

The historical 2026-10-14 P1/P2 repairs addressed omitted gate feedback and a false
truncated-window exponential argument. The subsequent audit found the separate
auxiliary and arithmetic errors corrected here. The full audit is archived unmodified
in the separate verification folder; no negative result or notebook was erased.
The current repair phase ends with verification and publishing these corrections.
No attempt to prove B, training run, merge or outside contact is authorized here.
