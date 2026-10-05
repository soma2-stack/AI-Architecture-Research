# Negative success: a finite-radius suffix-product channel barrier

2026-10-03. NEW internally checked theorem, pending independent hostile
review. Accepted holding-cost results and all historical evidence unchanged.

## Answer to the primary question

**No section of the requested type can exist in the accepted paired
suffix-product query channel.** This is a new finite-radius theorem, not
another failure of harmonic certification:

    D <16000 mT/sqrt(n), epsilon=.001.

Therefore D=omega(n) requires mT=omega(n^(3/2)). In particular the goal
D=omega(n), mT=o(n^(3/2)) is impossible for this channel. This is LEVEL4
negative success, with a useful LEVEL3 geometry theorem.

It is NOT a general impossibility theorem for the frozen RNN, other
private parameter directions, full fixed-feature gradients, or causal
memory over arbitrary subsequent admitted past gates.

No positive lower bound or exponent below3/4 is newly proved. The best
accepted construction remains D=Omega(n log n) at
R_abs=O(n^(3/4)(log n)^(3/2)). General threshold bracket[1/4,3/4] and
full-model Omega_c(n^2)--O_c(n^2 log n) remain unchanged.

## Mechanism of the proof

Each row is STRICTLY increasing and takes values in(0,1):

    k_j=a g_j k_(j+1), k_T=g_T.

Log-suffix coordinates are exactly cumulative sums and invert by adjacent
differences. The product map has full Jacobian rank; that does not imply
finite-error robust dimension.

The nonharmonic representation stores inverse level positions, rather than
time samples or harmonic coefficients. Append public row endpoints(0,0)
and(T+1,1), interpolate the row monotonically, and store where it crosses
ell/p for ell=1,...,p-1. This is a continuous map. Decode by interpolating
those same level/position knots. Entry error is <=1/p over the WHOLE row,
including all nonlinear product effects.

Because the physical row supports are shifted by one coordinate, each
column has at most s=min(m,T) nonzeros. The actual sign supremum obeys

    H(E)=max_(||xi||infinity<=1)||E^Txi||2
         <=sqrt(s)||E||F.

This is a direct worst-query upper, not RMS substitution. With entry
error1/p, H(E)<=sqrt(mT s)/p. We also prove ||E||F<=H(E) by allowed sign
witnesses, and give exact norm duality to rowwise absolute unit-probe sums.

All permitted future adjoints on the distant paired rows have component
size<=100/sqrt(n). Including the autonomous source and reset gives a
normalized projected upper coefficient<8/n. Dense pair error is charged
separately as8e-9. This explicitly covers every legal future horizon under
the accepted [.25,.75] preactivation contract, not only a finite query frame.

Take

    p=max(1,ceil(16000 sqrt(mT min(m,T))/n)),
    k_quant=m(p-1).

Two equal codes have projected legal query distance at most .001+8e-9,
strictly below .002. Borsuk-Ulam then forbids a robust antipodal D-ball
with D>k_quant. Finally

    k_quant<16000 m sqrt(mT min(m,T))/n
           <=16000 mT/sqrt(n).

All constants are independent of width. Integer ceilings do not introduce
an uncounted m-coordinate term. No finite packing or visible-axis count
substitutes for the continuous dimension argument.

## Haar, block codes, and exponent optimization

A unit Haar vector on an interval of length b has exact squared cumulative
norm(b^2+2)/12. Coarse blocks gain O(b); fine blocks do not. Regardless of
which nonlinear joint Haar, Walsh, ramp, sign-coded or saturated section
is attempted, its resulting product rows lie in the monotone family and
are covered by the finite-radius theorem. This is not a rejection based
only on poor Euclidean conditioning of one candidate.

For m=n^mu,T=n^tau,r=n^rho,D~mr, robust sections must satisfy

    mu+rho <=(3mu+tau+min(mu,tau))/2-1.

Together with mu<=1 this excludes the region

    mu+rho>1, mu+tau<3/2.

The non-power statement D/n<=16000 mT/n^(3/2) also rules out slowly
diverging dimensions such as n log log n at a subcritical coordinate-time
budget. The upper count is not claimed achievable.

## Energy and endpoint scope

Every admitted new nonharmonic word still uses the accepted exact lift:
two moving positive states and two stationary negative compensators per
track, source sigma, autonomous public bath, and simultaneous public reset.
The same exact NONZERO endpoint is preserved for all combinations.

Reference preparation is <m+1 squared norm, interior<=mT, reset<=m.
Actual dense correction adds at most e sqrt(n(T+2)) to the full norm.
Hence the complete accepted upper remains

    ||X||2<=2sqrt(m(T+2)+1).

This includes the source preparation and every actually used input; no
public center is subtracted. However this inequality is an UPPER. A lower
on mT is not by itself a lower on actual input energy. Only for the accepted
near-zero schedules with actual squared cost Theta(mT) does our theorem
force energy omega(n^(3/4)) when D=omega(n), in this channel.

In that scoped family, D=Omega(nF) needs at least squared holding cost
Omega(n^(3/2)F), hence energy Omega(n^(3/4)sqrt(F)). This is a necessary
factor, not a constructive improvement of the existing F^(3/2) bound.

The quantile code is a STATIC finite-error width representation. It does
not establish a causal online update with the same coordinate count.
That distinction prevents a new generic compressor claim.

## Checks, resources, files and next action

204 recorded checks PASS: exact inverse/Jacobian determinant; cumulative
singular-value and Haar formulas; whole-row finite-error bounds with exact
worst sign choices for tiny matrices; continuity samples; exact integer
coordinate counts;192/256-bit constants and a distinct-row equal-code
example. The proof supplies the uniform theorem; samples do not.

One numerical process, numerical pools1, observed peak process threads4,
no workers. CPU math2.53125s (.04219 CPU-minutes), peak working set
41,168,896 bytes (39.26MiB), GPU/CUDA0. No resource-limit failure or heavy
search. Original sources and prior unrelated dirty files preserved.

New evidence is entirely in this folder; Codex resume is additive. Theorems
ready for hostile review are PROOF.md sections1-5 (especially the all-future
coefficient, continuous inverse-level map and topological width step).

Next attack, AFTER independent review: characterize the unpaired private
sensitivity channels of the same low-cost corridors. The paired suffix
channel is now ruled out at the requested budget, but no such upper was
proved for those other channels. Stop this task; no new research begins.
