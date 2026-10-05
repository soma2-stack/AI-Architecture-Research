# Internal checks and resource ledger

## Policy before tests

PLAN.md was written before numerical execution. All OMP/MKL/OpenBLAS/
NumExpr/BLIS/Accelerate/TBB pools were set to1 before imports. OMP dynamic
and nested work disabled. CUDA visibility disabled; no GPU runtime imported.
One process at a time, workers0, hard process-thread stop12, RAM stop160 MiB.
Preferred <=4 process threads met. No brute-force or history optimization.

## Executions

| Script | PASS records | CPU s | wall s | peak process threads | peak working set |
|---|---:|---:|---:|---:|---:|
| checks.py | 58 | .890625 | .906614 | 4 | 43,843,584 bytes |
| corollary_checks.py | 19 | .156250 | .148893 | 4 | 25,530,368 bytes |

Aggregate mathematical CPU1.046875s, sequential max RAM41.813 MiB.
Thread counts are observed live process counts at check/guard boundaries;
numerical execution pools are1, with no child processes. GPU/CUDA calls0.
No NaN, crash, OOM, mathematical failure or resource guard failure occurred.

An initial provenance command referred to a nonexistent historical review
PROOF.md; that review actually uses REVIEW.md. The new manifest was corrected
to the existing filename, without modifying historical files or rerunning/
changing any mathematical check. Windows sandbox launch initially failed;
the read/run commands used approved escalation. A notebook insertion guard
also stopped on an incorrect expected heading; the actual heading was read
and used before any notebook write. These were not mathematical failures.

## Analytical audit checklist

1. O_* is orthogonal because O fixes node0; omitted node0 is not a leak.
2. Co-moving subspaces are OUTPUT spaces; v is a fixed physical parameter probe.
3. Uniform outside gate cap follows from public front/bath positivity, not a
   guessed stationary bath. Donors also meet the cap. No front is discarded.
4. Two-step damping includes all signed paths and time-varying outside gates.
5. Exact slow-mode response, full forced complement bound and all errors are
   compared before final margin; no inaccessible ambient matrix is used.
6. The terminal correction matches traces exactly and stays inside(.99,1).
7. p=1 is proved analytically only in the asymptotic constructions; the small
   reference test has p=3 and is explicitly NOT an equal-quantile example.
8. Delta L_N v=0 is a proved parameter projection, not deletion of full residuals.
9. Two permitted query patterns eliminate arbitrary common residual offsets;
   the same query is used on both histories. The actual query normalization
   and source multiplier are retained.
10. Reset is public, positive and transmitted; preparation source credit0
    and reset injection cancel exactly. All absolute input costs are counted.
11. Corrected dense display has division by n explicit; only the conservative
    accepted8e-9 charge is used. The short-packet theorem is unaffected.
12. One pair gives only1D. No omega(n), finite-bit, VRAM or architecture claim.

Numerical results are in checks_result.json and corollary_result.json, with
script hashes. Frozen source hashes and final audit verify historical evidence
is preserved. All NEW theorems still require independent hostile review.
