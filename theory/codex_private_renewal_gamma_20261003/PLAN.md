# Private renewal Gamma stage — protocol frozen before numerical checks

Codex, 2026-10-03. Work only in the theory repository. Historical accepted
proofs/reviews and AGENTS.md remain untouched. This is a new derivation,
pending independent review; accepted global thresholds are unchanged.

## Primary analytical candidate

Use the accepted moving corridors, the existing source feature, actual legal
queries, epsilon=.001, and public preparation/reset. For sufficiently large
n, take even m approximately sqrt(n), T approximately 10 n^(3/4), and
L=ceil(1000 log n) terminal damping steps. All survivor tuples have gate
g_H=1-n^(-2). Half the tuples are donors. History A holds donors at g_H
before the terminal tail; history B holds them at g_L=199/200. Both use
g_L in the tail. Adjust only A's last donor gate analytically to make its
compensator trace EXACTLY equal to B's. This is a prescribed construction,
not optimization after a failed official certificate.

For these parameters the accepted local quantile count has p=1. Therefore
the equal local code consists of exactly the compensator traces. Analyze
the fixed UNIT parameter probe with opposite signs on donor/survivor
compensators. No time-dependent parameter direction is substituted.

Try to prove a constant Gamma lower bound using the exact co-moving
zero-sum survivor subspace and uniform damping of its orthogonal complement.
All Householder renewals remain in the full propagator; no Born truncation.

## Checks and limits

Before importing numerical libraries set all thread pools to 1, disable
CUDA visibility, use one process, no workers, no GPU. Hard process-thread
limit 12, preferred <=4; stop above 160 MiB. Tests are algebra checks and
small counterexample probes, not robust-dimension proofs. Do not search
large parameter grids. Compare selected large-n scalar bounds at 192 and
256 bits. Preserve failed checks if any; do not tune theorem constants
against numerical results.

## Stopping point

If Gamma is proved >.002 for this equal-code family, record that the old
local code cannot close the complete corridor. A single pair does NOT
prove superlinear continuous dimension. Check a continuous 1D interpolation
only; determine why its parameter count does not establish omega(n).
Stop after the exact renewal and Gamma result, without architecture work.

## Correction carried forward

The previous printed dense-error bracket was displayed incorrectly. The
independent review reconstructs a pair bound about 1.4e-12 at n=10^6;
the accepted conservative pair charge <=8e-9 remains valid. Do not reuse
the old display. The accepted short-packet theorem does not depend on it.
