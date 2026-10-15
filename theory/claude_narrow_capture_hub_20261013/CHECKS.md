# Verification — narrow-capture foundation repairs

Updated 2026-10-15. Proofs and exact certificates are distinguished from finite diagnostics.

## Independent verification

From the repository root:

    python -I theory/codex_pr27_repair_verification_20261015/check_foundations.py
    python -I theory/codex_pr27_repair_verification_20261015/check_repairs.py

These scripts import no author implementation. They preserve the audit's counterexamples
and check the repaired own/bus decomposition, post-gate order, contrast identity, explicit
front condition, exact scalar gate functional, finite-size bounds and PR #28 compatibility.

The excess certificate rounds integer operations upward through 20000 iterates and
bounds the entire remaining geometric tail. Its start-1 upper bound is
221.021047106976...<223; the larger 1.06-start upper bound is 222.531626600977...<223.
The corrected rational floor preactivation lower bound is .027164853275575...,
greater than the rational upper bound .025005211590577... for atanh(.025).
The lifetime and theorem coefficients are preserved. Full results and limitations are
in the separate [verification record](../codex_pr27_repair_verification_20261015/REPAIR_VERIFICATION.md).

## Original author diagnostics

    python -I theory/claude_narrow_capture_hub_20261013/checks.py
    python -I theory/claude_narrow_capture_hub_20261013/verify_p1p2_sweep.py

checks.py writes checks_result.json next to itself. Its bath-identity examples use
n=8000,32000, below the bath theorem's n>=1e8 threshold, and its random drives exceed
the theorem's narrow-width fraction. These are identity diagnostics, not tests of the
floor theorem in its range. The constant sweep is also finite diagnostic evidence.
The exact infinite-sum/floor certificates above provide the stronger arithmetic evidence.

The retained coupled dense-error bound is eta<3.3e-7 only in its stated short-budget
branch. For W=T, equality of all inputs proves equality of the histories exactly.
For W<T, the auxiliary remainder has an analytic upper bound <1.46e-11, comfortably
below the retained loose 2.1e-4 budget. No finite grid is used to infer a uniform proof.
