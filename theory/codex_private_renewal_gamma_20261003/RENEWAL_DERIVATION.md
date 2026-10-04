# Full renewal and its nonperturbative invariant-space reduction

No accepted historical derivation is modified. PROOF.md gives the theorem
and constants; this file maps the old row ledger to the new resummation.

## Two finite-rank drivers, not two scalar memory slots

O_*=C+U2 W2, U2=[ones,e1], W2=[u^T;v_H^T]. The row vectors
J=u^T M and B=v_H^T M each have r parameter coordinates. Forcing from L
and feedback from H enter exactly the same two output shapes.

The Volterra kernel W2 Phi_C(t,s) aG_s U2 is2-by2 in output-channel indices,
but acts on TWO r-coordinate row vectors. Its temporal resolvent is finite
and strictly causal. It does not give a2-coordinate or2r-coordinate online
state without a bank for the history-dependent row filters.

The accepted row realization remains exact:

    V_i,t=ag_i,t(V_i,t-1+J_t-1),
    Z_t=aq_t(Z_t-1+J_t-1),
    F_1,t=af_1,t(J_t-1+B_t-1),
    F_z,t=af_z,t(F_z-1,t-1+J_t-1),
    S_M=S_L+(r-4m-t)Z+4sum_i V_i+sum_z F_z,
    J=gamma(L_terminal+Z)/sqrt(k)-gamma^2 S_M/k,
    B=gamma S_M/sqrt(k).

All rows here are private parameter-space vectors. Exact feedback-bank
count r(m+t+1), plus direct array mt; this is an explicit upper, not proved
minimal. Public schedules are uncounted; no private coefficients are free.

## Resummation that does not discard signs

Subtracting L from M gives

    H_t=aG_t O_* H_t-1+aG_t(O_*-C)L_t-1.

Hence the full signed propagator, including all Householder insertions,
has norm <=a. It is incorrect to replace this by exp(CmT/n) path growth.
Conversely nonexpansiveness does not make a forcing invisible: substantial
credit can be injected before the histories share a terminal gate tail.

## New exact split for the counterexample

On the high survivor support A_t, all gates are g_H. The zero-sum space
H_t={support in A_t, sum0} co-moves exactly, and O_* is orthogonal.
Therefore H_t and its orthogonal complement evolve separately. This is an
OUTPUT invariant-space decomposition, not a varying INPUT parameter probe.
The probe v is fixed on compensators for the entire history.

The high common direction w_t has compression alpha=1-gamma^2|A_t|/k.
Outside coupling has norm ell=sqrt(1-alpha^2). The public bath/front and
donors have gates <=.9992. Two-step dissipation forces the complement to
damp at least m/(8000n), with a full forced bound16000n/m. This statement
controls the ENTIRE recurrence, including the exceptional front and reset.

History A's fixed zero-sum probe remains an exact slow mode while every
tuple is high. In B, only its projection onto the survivor zero-sum space
is slow; the complement settles. Their common survivor component differs
by approximately kappa_H/2. A logarithmic donor-erasure tail equalizes the
direct traces but is much shorter than the complementary damping time n/m.
It cannot erase that common difference. A prescribed tiny last-gate change
equalizes traces EXACTLY rather than approximately.

## What is, and is not, amplified

The histories have identical final LOCAL codes, not close full prefix credit
states. Their full credit already differs before the shared tail. The shared
tail remains nonexpansive. The effect is stored chronology invisible to the
chosen final local code, not exponential instability of Householder renewal.

The construction proves a macroscopic conditional diameter and a1D section.
It does not establish a high-dimensional robust section or a minimal causal
realization dimension. It leaves open whether a different, richer code can
summarize the complete corridor in sublinear/quadratic resource regimes.
