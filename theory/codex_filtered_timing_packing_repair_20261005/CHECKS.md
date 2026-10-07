# Internal checks and provenance

Author algebra checks only; not independent verification or acceptance.

## Analytic checks

1. Unrolled w includes a^{T-j+1}. No extra a is paid in the V=sum w J formula.
2. Reset cancels J_T in V-Z, not in complete M.
3. Midpoint difference is exact even though the average state does not obey
   the midpoint recurrence. Only its individual-norm bound is used.
4. Backward adjoint order is R^T bar G, not bar G R^T.
5. The dissipation inequality holds for arbitrary fixed ||R||<=a; orthogonality
   of the actual dense recurrent matrix is NOT assumed.
6. Interval telescoping ends at ||p_e||, yielding a^{N-e}, not a^{N-s}.
7. d_t=0 for equal unit gates; there is no undefined infinite charge.
8. l<=n supplies conservative decimal constants for odd as well as even n.
9. Spatial leverage is limited to changed ordinary corridor sites whose
   bare characteristic never reaches the terminal. The terminal has
   exceptional legal leverage and is not included for free.
10. Expansion at FIRST departure is an exact telescope. All subsequent
    Householder renewals are included in the contractive remainder.
11. h in the gate-window bound counts changed physical gates; h in the
    output-localized bound counts final output support. They are different.
12. Any final trace correction must enter Delta G and the interval I.
13. Dense charge is needed for reference spatial bounds; exact dense
    midpoint/time bounds have no such additive charge.
14. A count of P packets only equals D for the explicit scalar section.
15. The T=1 localization counterexample does not match compensator traces.
    No stronger scope is assigned to it.
16. D=2 is not re-reviewed; historical pending labels are preserved.

## Small numerical replay

checks.py sets all common math pools to one thread before NumPy import;
CUDA_VISIBLE_DEVICES=-1. It imports no GPU library, starts no workers,
and runs no extra monitoring thread. Process thread snapshots must stay <=8.

Run from the repository root after setting the same environment limits:

    python theory/codex_filtered_timing_packing_repair_20261005/checks.py

checks_result.json records seed, samples, residuals and resources. The
n=256 replay intentionally checks algebra rather than pretending to meet
the canonical large-width geometric/lift assumptions. At n=256 the
spatial min bound uses its global-contraction branch; these numerical
samples do not validate the sharper large-width spatial branch. Finite query samples
do not certify an all-query supremum: PROOF.md supplies that proof.

Windows peak working set: 43,520,000 bytes; observed peak threads4;
CPU .484375s; GPU0. No caches or large outputs are required.

## Protected evidence

Historical proofs, independent reviews, AGENTS.md and CURRENT_THEORY.md
are unchanged. source_hashes.json records the exact read dependency files.
The original dirty repository checkout is left on its original branch;
all work is in a separate worktree/branch based on repair commit
44c9e0e9090e8243f0f0030865e263cc7b21798e.
