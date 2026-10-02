# Intermediate regime: new linear section, mixed-word width still unresolved

2026-10-02. New mathematical derivations for independent review. No numerical
experiment, new spectrum, training, architecture, GPU workload, other gamma
regime or old-chart re-evaluation. PROOF.md is the complete argument.

## 1. Exact regime

Keep c=1, gamma=1/n, epsilon=.001, source H=.4ones_l, the same dense tanh
model, group-RMS metric and permitted scalar-head future queries. Use

    n>=200, N=ceil(4n log n)+1,
    1-g_(t,i) in [1/(20n),1/(4n)]

on every selected memory coordinate at all N weak-window steps. A public
source-establishment step precedes the window; the exact h=0 reset follows it.
Those two steps are explicit exceptions to the weak positive gate gap.

EVERY word in this gate cube has a coupled tanh realization: hidden coordinates
are signed sqrt(z_(t,i)/n), and inputs are atanh(h_t)-R h_(t-1)-b. The whole
cube stays inside |input|<.48, without independent parameter-column injections.
Inputs are held fixed when differentiating parameters.

An arbitrary bounded inherited credit contributes at most .3 n^(-37/10) in
query units over this window. Thus old credit is not the remaining bottleneck
at this chosen length. All fresh ages are retained in the exact unrolling.

## 2. Strongest O(n) upper obtained

**No uniform O(n) encoder for arbitrary aperiodic weak gates was obtained.**
The existing general selected-feature upper remains r^2=O(n^2), plus n actual
forward coordinates. An O(n) exact encoder covers the newly constructed
constant-tail subclass only: store its m section coordinates, an optional
counted clock, and actual h, then decode public baseline/tail affine powers.
It does not store or replay discarded inputs.

New general error theorem: arbitrary weak words have a convergent chronological
gate-word expansion with ratio

    q_n=a Delta/(1+a z0)<1, z0=.15, Delta=.1.

With C_n=Delta n/(1+a z0)^2, truncation after p perturbation orders gives

    all-query error <= eta_n+delta_old+A_n a C_n q_n^p/(1-q_n).

A public p_n=O(log n+log(1/epsilon)) makes that error <=epsilon/4 uniformly.
This is a finite-error theorem, not a compression theorem: the literal
hierarchy stores (p_n+1)r^2 entries, worse than reference RTRL. Expansion order
is not memory dimension, and its bound does not prove a logarithm is necessary.

## 3. Strongest lower obtained

**No superlinear lower.** A new joint section proves

    m=floor((floor(n/2)-floor(n/4))/2)>=floor(n/8)

within the intermediate gate regime itself, for every n>=200. This is useful
because the previously accepted whole-class one-pulse lower used stronger
gate deficits and therefore did not establish this narrower statement.

The new section has:

* one unit-ball parameter u in R^m;
* paired stationary NC directions with equal deficits .15+.1u_j;
* all deficits divided by n and inside the same box for every combination;
* a public baseline, followed by a 12n-step constant weak tail and exact reset;
* physical total-input L2 radius <2, uniform in n;
* exact scalar reference eligibilities, with no tangent approximation;
* one actual permitted future query for ALL antipodes;
* actual normalized antipodal half-margin >.00174>.001 after dense errors.

The mean-value derivative bound is -p'(z)>.63n over the whole range. Together
with the permitted pair-query margin it gives the explicit lower. A continuous
encoder of fewer than m coordinates has a memory-colliding antipode, so it
cannot meet epsilon. This is a true joint continuous lower, not finite packing
or independent-axis counting. It does not improve the accepted stronger
whole-class approximately n/4 count. Its constant-tail subclass is Theta(n).

## 4. Is fixed-feature Theta(n) proved or refuted?

**Neither.** Arbitrary aperiodic intermediate gates remain Omega(n) to O(n^2).
The whole-class fixed-feature bounds and full-model bounds remain unchanged.
No numerical evidence is claimed in this stage; the general O(n) outcome is
still a conjectural possibility, not an interpretation promoted to a theorem.

## 5. Smallest remaining mathematical obstruction

The controlled object is the reachable mixed gate-word polynomial

    H_(n,N,p_n)(D)=a O_* sum_(j=1)^p_n M_N^(j)(D),

with the exact recursion in PROOF.md (19), evaluated on the simultaneously
admissible diagonal gate cube. Its norm is the ACTUAL permitted-query
supremum, not Frobenius or RMS. Its first-order age/source kernel is written
explicitly in (24); higher ordered products have a certified norm tail.

Two concrete statements would close this attempt:

1. A counted continuous online O(n) state answering all polynomial query
   outputs to error <=3epsilon/4. The uniform epsilon/4 transfer/truncation
   ledger then gives the desired intermediate encoder.
2. One jointly admissible continuous superlinear gate section whose polynomial
   antipodal half-margin exceeds 5epsilon/4. The same ledger then gives an
   actual-model robust lower at epsilon.

These are sufficient buffered statements. Offline approximation alone is not
an online encoder, and a marginal actual lower need not satisfy the buffered
polynomial criterion. No equivalence beyond those error implications is claimed.

## 6. Full-model consequence

    Omega_c(n^2) <= d_rob <= O_c(n^2 log n)

remains open. A sufficient O(log n) expansion order does NOT establish a
logarithmic memory lower. Compatible simultaneous feature summaries would
still be required after a fixed-feature upper. Incompatible lower sections
cannot be multiplied into a full-model theorem.

## 7. Recommended next theorem

Establish or refute a horizon-uniform O(n) counted continuous query-width
representation of the ordered weak-gate polynomial residual, including an
online realization and all necessary orders. The first-order kernel is a
concrete entry point, but it must be accompanied by a remainder theorem;
its tangent rank cannot settle the problem.

## Checks, resources and provenance

New rigorous derivations remain subject to independent mathematical review.
CHECKS.md records the manual algebraic audit and construction indexing.
No automated tests or numerical experiments were added/run. Experimental
CPU time0; GPU/CUDA time0; no model server was launched. Administrative
shell/Git overhead and peak RAM were not instrumented.

PROVENANCE.json records source hashes and the starting checkpoint cbc4c79.
Only this new Codex directory, Codex_Research.md and the shared resume pointer
are changed. Accepted evidence, other-lane notebooks, AGENTS and GAS-0 are
preserved. Final task output records the completed commit. Stop this stage.
