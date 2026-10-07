# Filtered-timing packing audit

Codex, 2026-10-05. THEORY ONLY. Independent review pending.

## Verdict

**STILL OPEN.** The historical inference is invalid. Its numerical rate can
be recovered for a more restrictive, explicitly localized scalar-packet
class, but those extra premises have not been established for complete
moving-corridor credit. No unconditional D=o(sqrt(n)) theorem is obtained.
D=2 remains accepted and is not reopened.

The useful repair is a set of genuine COMPLETE all-query upper bounds.
They include older credit, private Householder renewal, arbitrary permitted
future horizons, frozen-input differentiation, common endpoint and dense
transport. No first-crossover truncation is used.

## Strongest new correct bounds

Let N=T+1, b_t=(1-a^t)/(1-a)<=min(t,n), q_f=sech^2(.25),
and suppose two actual histories differ in gates only during [s,e].
Include the final trace-correction steps in that interval.

Write bar g=(g+g')/2 and
d_t=max_z (g-g')^2/(1-bar g^2), with 0/0=0.
Then the complete ACTUAL pair distance is bounded above by the minimum of

    2 sigma sqrt(l) q_f b_N/n,
    (sigma sqrt(l) q_f/n) sum_{t=s}^e a^{N-t} b_t max_z|g-g'|,
    (sigma sqrt(l) q_f/n) a^{N-e}
                       sqrt(sum_{t=s}^e b_t^2 d_t).

These are finite-error upper bounds on the actual legal-query supremum,
not upper bounds on just a chosen witness. They need no dense-comparison
charge. The midpoint adjoint dissipates squared norm against
I-bar G_t^2; this controls all renewal paths without taking absolute
values of every Householder insertion.

A robust pair therefore needs

    sum_{t=s}^e b_t^2 d_t > .001736 n a^{-2(N-e)}.

The factor b_t is essential: a late gate change can alter accumulated
older credit. A short gate-write window is not a short credit-injection
window.

For h CHANGED physical sites per time, there is also a reference spatial
bound, plus <=8e-9 actual pair charge:

    distance <= (.051 sqrt(h)/n) W_I +8e-9,
    W_I=sum_{t in I} b_t delta_t a^{N-t}
                              (100+6 q_f(N-t)).

This follows by expanding transport at its first departure from an ordinary
characteristic and then retaining full nonperturbative transport.
It is an honest support/time restriction, but for long gate windows
W_I can be O(T^3), not O(T). h here is changed-gate support, which is
NOT automatically the size of a designated survivor cohort.

For a packet defined instead by its fresh-injection ages I, its complete
transported contribution has pair distance <.095982 |I|/sqrt(n).
If no other age contribution changes, a >.002 pair requires
|I|>.020837 sqrt(n). This gives a conditional time-packing count
P<47.991 N/sqrt(n) for disjoint, separately attributed scalar packets.
A donor gate change need not satisfy that attribution premise.

## Exactly how the old support-packing law can be salvaged

IF the complete reference difference has output support only on h ordinary
rows, all-legal-query distance is <=10.2 b_N sqrt(h)/n+8e-9.
This genuinely implies a necessary h of order n^2/b_N^2.

IF, additionally, one joint section has P scalar packets with disjoint final
supports totaling <=4m and each coordinate-axis pair differs only on its
own support, then P=O(m(T+1)^2/n^2). For T=O(n) and mT=o(n^(3/2)),
this yields P=o(sqrt(n)). D=P only in that specified scalar parameterization.

Neither IF is supplied by the old filtered-timing note. Spatially disjoint
survivor blocks do not make complete differentiated dynamics independent.
A flat filter retains one parameter-space vector; it is not automatically
one scalar. Counting blocks is not a proof about arbitrary B^D sections.

## First precise obstruction

At T=1, a changed tuple gate produces, after the public reset,

    (Delta M_2)_{z,w}=-a q_2 (gamma^2/k) Delta g_{1,w}

on a far bath row z outside the driven support. Thus public state
cancellation does not provide sensitivity localization.

This elementary example does NOT impose equal final compensator traces,
and is not claimed as a counterexample inside the trace-matched filtered
subclass. That subclass still needs its own complete localization or
query-leverage proof. The accepted long-packet equal-local-code,
equal-trace private-renewal counterexample shows that omitting private
feedback can also fail at finite epsilon. It is not itself a counterexample
to every possible support-packing bound.

No >.002 counterexample to a fully specified, stronger complete packing
theorem is proved here. We identify why the inherited derivation does not
establish one, rather than declaring all packing impossible.

## What is proved / conditional / failed

PROVED in this author derivation: exact suffix identities; actual midpoint
Duhamel and dissipative all-query bounds; nonperturbative ordinary-support
leverage bound; complete fresh-injection-window bound; output-localized
support upper bound with its explicit premises.

CONDITIONAL: support-packing o(sqrt(n)) for the stated scalar/localized
subclass; time-packing for separately attributed injection-age packets.

FAILED: lower visibility plus upper timing amplitude implies necessary
support; filter flatness implies one scalar; gate epochs can be identified
with fresh-credit epochs; disjoint forward sites imply disjoint sensitivity.

OPEN: an unconditional continuous-dimension packing theorem for the complete
trace-matched filtered-timing corridor family.

No historical file or CURRENT_THEORY.md is changed. No spatial-write
result is read or used as a premise. The accepted D=2 result is a separate
checkpoint, not evidence for any packing theorem.

## Checks and resources

Eight small algebra replays at n=256, 56 reference legal-form future adjoint
samples across horizons 1--7. These check formulas, not large-width lift
legality or asymptotic packing. Maximum midpoint residual 1.07e-14;
coupled suffix residual 6.60e-14. All sampled upper-bound assertions pass.
An explicit outside-support bath entry is 2.803640377e-5.

CPU time about .484 seconds; observed peak 4 process threads including
Windows loader threads; all numerical pools set to 1; peak Windows working
set 43,520,000 bytes (about 41.5 MiB); GPU/CUDA use zero.
No training, brute-force search, or GPU library was used.

## Next independent-review target

Attack PROOF.md (11)--(16): midpoint identity, telescoping adjoint
dissipation, the constant-source forcing premise, and the sup over ALL
permitted future horizons. Then attack (20)--(23): ordinary-characteristic
geometry and the first-departure expansion retaining all later renewals.

The most valuable next mathematical target is a stronger history-uniform
bound on Lambda(t,S)=sup_legal Q ||P_S Phi_bar(N,t)^T c_Q|| for actual
corridor midpoint trajectories, or a legal counterexample requiring its
age-dependent leakage term. That is the missing complete-query ingredient,
before any packet count can be turned into a continuous-dimension bound.

## Project consequence

No part of the complete LONG corridor is closed by the historical packing
argument. The already accepted short-packet obstruction remains intact;
the new estimates close additional explicitly small gate-dissipation
windows, not the long family as a whole. Best superlinear construction
and exponent bracket [1/4,3/4] are unchanged. No energy upper is reversed
into a lower, and no full-model/finite-bit/VRAM inference is made.
