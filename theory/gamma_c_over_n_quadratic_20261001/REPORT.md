# Quadratic robustness survives the normalized c/n contract

**New theorem for independent review:** for every fixed c>0 and sufficiently
large width n, a specified dense standard tanh family at contraction gap c/n
has a joint exact-fixed-h section of dimension Omega_c(n^2), with uniform
antipodal half-margin >0.002 at unchanged epsilon=0.001.

This is an existential worst-case lower, not a statement about every model.
The accepted constant-gap theorem is not revisited. No other contraction-gap
regime, width-4 section search or architecture is pursued.

## Bounds

| Scope at gamma=c/n | Lower | Upper | Status |
|---|---|---|---|
| Arbitrary permitted history lengths | Omega_c(n^2), new proof | O_c(n^2 log n), accepted window encoder | Logarithmic gap open |
| Constructed family, horizon T=O_c(n) | Omega_c(n^2) | O_c(n^2), exact counted finite-history encoding | Matching quadratic bound |

The same-gap margin ceiling still excludes cubic fixed-margin sections.
A universal subquadratic obstruction cannot hold under the present contract
if the new proof survives review.

## Exact construction

Let k=floor(n/2), l=n-k, L=max(1,ceil(c)), d=min(k,floor(n/(4cL))).
An orthogonal memory rotation has d independent temporal adjoint directions;
the k memory modes have magnitude a=1-c/n. The l source coordinates are driven
through a d by l bounded history matrix, repeated L times. An exact realized
input compensator holds all memory states and the final complete hidden state
at zero. Source tanh gates may be nonlinear; they do not attenuate the reference
memory orbit. Every parameter remains independently differentiated.

The accepted bounded-spread lemma gives

    r=floor(d l/1000)
      >=min(1/10000,1/(32000 cL)) n^2.

The real R memory/source injection and one permitted late query give orthogonal
gradient rows. Crucially, the accepted normalization obeys

    w_R/beta=1/n,

so the Theta(n) Frobenius source-history range offsets the remaining dilution.
The block-reference half-margin is >=1323/640000=0.0020671875. A fully specified
dense perturbation and exact norm rescaling change each normalized R-gradient
by <1e-6 over the entire section. The final half-margin therefore exceeds 0.002.

This is genuinely joint: EVERY antipode on the r-ball boundary is separated.
It does not infer continuous dimension from packing-state count or tangent rank.
The final R and its inverse have no zero entries, but some couplings are small.
The result uses accepted group-RMS units, not a per-entry relative metric.

## Remaining uncertainty

The proof is new and unaudited. The density/normalization transfer, held-input
compensation and temporal-adjoint grouping are the main independent-review
targets. Auxiliary sign-matrix selection is computable/exhaustive, not efficient;
no recipe was executed. For rational c all finite algebraic selections are
computably specified; the general-real statement is an existence result.

The remaining log n is not proved necessary. It disappears for this O(n)-horizon
construction. The general tail bound may overcount independently useful old
credit, but that does not supply an arbitrary-horizon O(n^2) theorem.

**Next theorem:** remove the log with a uniform arbitrary-horizon O_c(n^2)
counted continuous encoder, or refute that target with an Omega(n^2 log n)
joint robust section. Review this proof before treating quadratic existence
as a working premise. No architecture inference follows.

No experiments, GPU/CUDA, training, width-4 chasing or GAS-0 work occurred.
