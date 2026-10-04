# Checks and interpretation

Resources were set before imports: OMP/MKL/OPENBLAS/NUMEXPR/BLIS/TBB pools1,
OMP_THREAD_LIMIT1, no nested OpenMP, CUDA_VISIBLE_DEVICES empty,
NVIDIA_VISIBLE_DEVICES void. No PyTorch, GPU calls or child workers.

Run (one process only):

    python theory/codex_unpaired_corridor_sensitivity_20261003/checks.py

The script writes once and refuses to overwrite prior evidence. It stops
above8 process threads or160MiB RSS. The completed run had4 threads,
94.30MiB peak working set and.796875 CPU seconds. Import/launch overhead
is excluded from the recorded math time; no concurrent numerical run was
used. All45 checks passed.

A second, sequential standalone exact_path_checks.py uses Python Fraction
arithmetic, not NumPy. It checks12 crossover coefficients,6 same-row
collapses, and the exact short-packet threshold. All19 checks pass. Its
small auxiliary n=512 rational system is an algebra identity test only,
not an admitted large-width witness. CPU.203125s, observed threads4,
peak working set22,417,408bytes. Total64 checks, total math CPU1.000000s;
maximum RAM and threads remain94.30MiB and4. GPU use remains zero.

## Tests included

- UPU versus independent open-shift/rank-two expansion.
- Full unprojected fixed-feature recurrence versus local and feedback kernels.
- Matched positive/negative gates and all four shared feedback rows.
- Balanced output cancellation, not assumed input-column independence.
- Exact reset transmission.
- Central differences for joint R/W/b, with frozen nominal input controls.
- Coupled fixed-feature forcing versus complete full-state tangent.
- Equal local quantile code and equal scalar trace, with nonzero feedback.
- Public bath state with private differentiated credit.
- Actual permitted one-step query lower estimates, not RMS surrogates.
- 192/256-bit agreement for the accepted-width exceptional query formula.

These are supporting numerical identities, not interval certificates or
dimension claims. The new exact structural formulas and short-packet
theorem are proved in PROOF.md and await independent hostile review.

## Internal analytic audit

- Source forcing during preparation is zero for recurrent fixed-feature
  parameters; W and b preparation forcings are retained in the full ledger.
- Reset is t=N=T+1, so the fixed-source forcing count is N, not T+2.
- J_state is public and scalar; J_credit is private and vector-valued.
- All Householder insertion orders remain in (6)/(7)/(10)-(13).
- Half-margin and pair thresholds are not interchanged: robust pair distance
  must exceed.002. No new positive half-margin is proved.
- The short-packet bound uses actual ||R||op=a and actual future contraction,
  and therefore needs no dense surrogate charge.
- Exact rational paths independently check the sign, all powers of a,
  insertion-time ranges, and the same-row (T-s) product collapse. Physical
  parameter-column collisions must still be summed, as stated in the proof.
- The raw energy estimate remains an UPPER.
- Output projections, parameter projections, and actual queries are kept
  distinct; no arbitrary unit adjoint is used.
- All new threshold statements stay in fixed-feature d_F, not full-model
  memory, bits, VRAM, practical width or architecture success.
