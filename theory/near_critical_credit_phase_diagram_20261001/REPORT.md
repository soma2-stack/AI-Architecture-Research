# Near-critical phase diagram: linear lower proved, higher transitions open

**Strongest new result:** a specified dense, invertible tanh family has an
exact two-step fixed-hidden-state section of dimension
floor(floor(n/2)/1000)=Omega(n), with uniform half-margin >=0.002075 at unchanged
epsilon=1e-3. It uses the actual normalized late scalar-head query, not an
arbitrary-unit-loss replacement. New proof requires independent review.

| Contraction gap | Existential robust lower | General sufficient-memory upper | Status |
|---|---|---|---|
| Theta(1) | Omega(n) | O(n) | Worst-case Theta(n) established by the new derivation |
| Theta(1/n) | Omega(n) | O(n^2 log n) | Quadratic lower open; cubic robust sections excluded |
| Theta(1/n^2) | Omega(n) | O(n^3) | Cubic lower open |

Upper bounds assume bounded input coordinates/W operator norm/bias RMS,
fixed group-RMS units, arbitrary decoder work and counted retained history.
Counts are on the fixed-h fiber; add n if exact h is not supplied. No claim
that every model requires linear memory is made.

The accepted recent-window improvement gives k<=min(nP,2nH), where

    H=ceil_+(log(kappa_Q C/[epsilon gamma])/[-log(1-gamma)]),
    kappa_Q=(1-gamma)/max(1,||R||F).

Every r-dimensional antipodal section has half-margin at most

    (kappa_Q C/gamma)(1-gamma)^(ceil[r/(2n)]-1).

Cubic margins therefore decay exponentially in n^2 for constant gap, and
as O(n exp(-c n)) at gap Theta(1/n). At gap Theta(1/n^2), this upper obstruction
does not decide existence. A logarithmic boundary layer prevents treating
1/n^2 as an exactly proved threshold.

**Explicit family:** R=delta I+(a-delta)qq^T, delta=1/(100n), q=1/sqrt(n)*1,
W=I, b=(1/20)*1. All recurrent entries and inverse entries are nonzero; all
parameters are independently differentiated. A deterministic finite-net/sign
matrix specification supplies bounded paired input coordinates. Joint final
input compensation gives h2=0 exactly. The full held-input sensitivity yields
the stated margin without an interval-curvature sufficient bound.

This family has only one slow collective mode, so its lower remains linear
even when gamma shrinks. It is a genuine dense existence example, not proof
of rich slow-mode scaling. Its matrix specification is computable/exhaustive,
not an efficient closed-form formula, and was not executed.

**Transitions:** linear worst-case growth is established by this new proof.
Linear-to-quadratic and quadratic-to-cubic growth are NOT yet established.
Contraction gap alone does not determine memory: normalized query strength,
slow-mode multiplicity, tanh gates and coupled injections also matter.

**Next theorem:** a jointly robust Omega(n^2) fixed-h section at gamma=c/n
under the unchanged normalized late-query contract. This is the smallest
unresolved transition with a clean cubic exclusion. Independently review the
new linear construction before treating it as an accepted premise.

No experiments, width-4 dimension chasing, new witnesses, architecture work,
GPU/CUDA or GAS-0 work occurred. Source and provenance are in PROOF.md and
PROVENANCE.md. Historical upper theorem is preserved; its redundant quadratic
store and impossible matching-quadratic recommendation are superseded here.
