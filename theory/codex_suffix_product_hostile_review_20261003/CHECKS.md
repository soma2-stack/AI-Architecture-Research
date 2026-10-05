# Independent checks and resource ledger

## Execution

Run one script at a time from the repository root. Both scripts set all
common numerical pools to ONE before library imports, disable CUDA
visibility, and reject worker processes. The first script also checks
resources at every record and future-transport step. The second checks at
every tiny adversarial case. Both refuse to overwrite their evidence.

Commands used:

    python theory/codex_suffix_product_hostile_review_20261003/independent_checks.py
    python theory/codex_suffix_product_hostile_review_20261003/extreme_collisions.py

| Run | Records | CPU seconds | Wall seconds | Peak process threads | Peak working set |
|---|---:|---:|---:|---:|---:|
| Independent identities/queries | 52 PASS | 4.859375 | 5.176197 | 4 | 72,785,920 bytes |
| Extreme equal-code collisions | 6 PASS | .187500 | .200719 | 4 | 29,253,632 bytes |

Sequential total math CPU: 5.046875 seconds. Largest peak working set:
69.41 MiB. One numerical thread, observed four total process threads,
no worker processes. GPU/CUDA use: ZERO. No heavy searches or resource
failures occurred. These process measurements exclude the desktop and
other users' workloads; there were no parallel numerical jobs in this task.

The first script reports memory/process threads after loading libraries;
the reported CPU/wall values measure the diagnostic work after imports.
Full invocation overhead was small and no additional numerical process
was launched. No claim about proof-thinking CPU cost is made.

## Numerical status

256/384-bit CPU mpmath knot calculations agree in their recorded 45-digit
gate value; these are independent numerical cross-checks, not interval
certificates. Near-flat and exact-knot continuity is proved analytically
in REVIEW.md. Original 192/256-bit outputs were inspected but not reused
as independent observations.

The Householder-cycle attack uses a vector implementation at n=10^6,
never a dense matrix. Legal future gates include uniform high gates and
two greedy non-scalar sign policies. Horizons extend to 64. These attacks
cannot establish a supremum over all gate words; the analytic envelope
in REVIEW.md does establish that uniform upper bound.

Same-sign collision matrices have an exact maximizing row sign vector,
so their computed H is the actual infinity-to-2 norm, not an RMS surrogate.
The coefficient applied to H is an analytic all-future upper. The extreme
collisions change entries by as much as .944335, so the attacks are not
confined to tangent perturbations.

Exact integer square roots implement ceil arithmetic without a floating
square-root decision at a boundary. A separate arithmetic equality case
at n=16000 is explicitly outside the model theorem's n>=10^6 range and
does not constitute a new model experiment.

## Preservation

FROZEN_INPUTS.json records raw-byte hashes of every file in the target
folder and the necessary predecessor/query definitions before testing.
FINAL_AUDIT.json records end-of-review checks. No historical evidence was
edited. Codex notebook changes, if present, are additive resume notes only.

## Limitations

The uniform verdict is supplied by the independently reconstructed proof,
not by the 58 tests. No empirical dimension or memory upper is inferred
from these finite examples. No online algorithm, unpaired bound, universal
energy lower, finite-bit theorem, VRAM bound or architecture claim is made.
