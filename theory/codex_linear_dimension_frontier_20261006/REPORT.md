# Linear-dimension frontier: exact logarithmic loss removed, target open

2026-10-06. THEORY ONLY. New author-derived results require independent
review. STATUS.md is STILL OPEN for linear dimension at mT=o(n^(3/2)).
The verified coded-donor theorem is not reopened or edited.

## Main finding

There were two separate issues. The log^12 restriction came from charging
unprotected common-row drift during a long tail and erasure mask. It was
a sufficient estimate, not a necessary law. A new one-step capture BEFORE
trace correction turns that row into exact zero-sum private credit; the
long correction and clear then cause no renewal drift in its read.

This allows M=cn for a fixed small c, and gives genuine linear robust
dimension. Its actual duration cost is Theta(n^(3/2)), however. Therefore
the requested linear dimension at the STRICT little-o budget is NOT proved.

A new scoped obstruction proves that this last failure is unavoidable
for every family with bounded donor-control stage count: topology gives
D<=RK<=Rm/2, and the complete actual short-packet theorem requires
T>.020sqrt(n). Thus D<25R mT/sqrt(n). It does not close arbitrary corridor
histories with richer temporal controls.

## New author results

For every integer n>=10^3000 and sqrt(n)<=M<=10^-40n:

    D>=M/10^30, actual pair>.3, half-margin>.15,
    mT<4*10^8 n sqrt(M),
    ||X_raw||_2<50000 sqrt(n) M^(1/4).

The section is ONE continuous injective B^D, with two simultaneous
partitioned-donor write stages, two shared one-step Walsh captures,
exact final traces, one source, one public reset and one exact endpoint.

| Choice | Proved dimension | Coordinate-time cost | Absolute raw-input norm | Meets strict budget? |
|---|---|---|---|---|
| M=10^-40n | D>=10^-70n | Theta(n^(3/2)) | <5*10^-6n^(3/4) | NO |
| M=10^-40n/(log log n) | D>=n/(10^70 log log n) | <4*10^-12n^(3/2)/sqrt(log log n) | <5*10^-6n^(3/4)/(log log n)^(1/4) | YES |
| M=n/f, 10^40<=f<=sqrt(n), f->infinity | D>=n/(10^30 f) | <4*10^8n^(3/2)/sqrt(f) | <50000n^(3/4)/f^(1/4) | YES |

The log-log specialization is valid for all n>=10^3000, not just after
a sampled width. More slowly diverging f is also possible under the
displayed range. There is no best fixed logarithmic exponent p: this
protocol permits arbitrarily slow dimension dilution, yet the strict
budget still excludes a constant dilution in a bounded-stage family.

## Six-route screen

IDEAS.md records early capture, weak fresh-bit multirow masks,
cohort-local captures, gate-only protected rotations, hierarchical coded
stages, and simultaneous temporal/spatial coding. Early capture wins
because its protected-row identity is exact. The other routes have
explicit early scaling failures or a precise missing whole-ball lemma.

Weak fresh-bit masks provide an exact new algebraic partial result:
contrast .005/R preserves old singleton coefficients by an absolute
constant instead of 2^(-R). But new capture pays 1/R; the sequential
stage-selector budget still fails. Multiple protected rows share the
same source, survivor support and reset in that algebra; an improved
general-R robust theorem is not asserted.

## Answers to the target questions

1. The old load-bearing loss is 10^8(log n+1)sqrt(m/n)<10^-6.
2. Six structurally distinct routes are in IDEAS.md; their status is explicit.
3. Early capture is the strongest completed route.
4. M=Theta(n) is achievable with legal history, traces, endpoint and margin.
5. Linear D is proved at critical cost; it is NOT proved at mT=o(n^(3/2)).
6. At the strict budget, n/(10^70 log log n), or an arbitrary slower
   divergence under the range conditions, replaces the log^12 loss.
7. Conservative actual pair>.3, half-margin>.15 survive.
8. mT is little-o only for M=o(n); the cn choice is Theta(n^(3/2)).
9. The full norm bound is <50000 sqrt(n) M^(1/4), with no excluded baseline.
10. The remaining obstruction is bounded robust controls per active donor
    group together with the necessary sqrt(n) packet duration.
11. Review early capture BEFORE trace matching, exact preservation during
    its donor-dependent last correction, whole-boundary two-stage read,
    and large-m legality. Separately check the scoped topological/time
    obstruction; do not upgrade it to complete-corridor compression.

## Recommended next exact lemma

Construct R jointly independent repeated temporal controls per donor group
in ONE write interval, with R protected rows, common traces/endpoint and
a finite-radius legal-query lower>.002. Target R=ceil(log log n),
m=Theta(n/R), T=O(n/sqrt(m)). That would give linear D and a strict
little-o cost. No mere list of epochs, singular ranks, or separately
successful directions suffices. The new early-capture algebra can protect
rows once written; it does not yet write these R channels simultaneously.

The complete corridor remains open. The global superlinear absolute-norm
threshold bracket [1/4,3/4] and the full-model bounds are unchanged.
There is no bits, VRAM, practical model-size or new architecture claim.
