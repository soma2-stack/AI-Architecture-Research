# Holding-cost attack, 2026-10-03

New Codex theory folder. The owner's accepted 3/4 theorem is a premise, not
a review target. Historical sources and reviews remain untouched.

Work in order: full energy decomposition; autonomous source; exact paired
moving corridors; duty-cycle forcing; parameter optimization; temporal
kernel refinement; scoped and general obstruction analysis.

Numerical checks are frozen sanity checks of derived identities. No witness
search or parameter tuning against numerical results. No training or GPU.

Before any numerical imports: one process, all numerical thread pools set
to ONE, no worker pools, CUDA_VISIBLE_DEVICES empty, no GPU libraries loaded.
Observe process thread count and peak working set. Abort if process threads
exceed 8 or working set exceeds 256 MiB. No automatic higher-resource retry.
Shell/administrative steps and checks run sequentially. Max numerical compute
threads planned: 1, below the owner's global eight-thread limit.

Fixed sanity cases: paired corridor at n=8192,m=8,T=32,F=2; source equilibrium
scalar checks at n=200,8192; exact parameter arithmetic at n=10^200 and
10^240, F=2,floor(log n),n^(1/16). Use 240/320 binary precision bits. No numerical
dimension claim from these checks. Any failure is preserved before repair.
