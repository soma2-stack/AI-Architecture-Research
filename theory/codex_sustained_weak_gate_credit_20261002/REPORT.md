# Fixed-feature whole-class attempt: partial bounds, still open

2026-10-02. New scoped derivations for independent review. No experiments,
new witnesses, training, GPU work, architecture, or other contraction regime.
PROOF.md contains the full hypotheses, constants, counts and arguments.

## 1. Strongest theorem for sustained histories

Two actual worst-query finite-error bounds now have explicit credit-side
fresh-injection accounting:

* **Full selected-block damping:** for a last interior L-step tail with all
  selected gates <=u<1, followed by the exact zero reset,

      error <= eta_n + A_n[a n(au)^L + au/(1-au) + 1].

  If damping holds from the first injected interior step, the old-credit term
  is absent. This subclass admits O_(u,epsilon)(n) online coordinates at every
  horizon, and eventually zero endpoint credit coordinates as n increases.
  An arbitrary short sustained tail after an undamped warmup is not covered
  by that last asymptotic statement.

* **Sustained latent-cycle active block:** all pair gaps delta_j are allowed
  to vary aperiodically. Write b_j=a^2 sqrt(1-(1-u_j^2)/(2(2-u_j)^2)),
  u_j=1-delta_j, P=product b_j, W=sum of suffix products. Retain the exact
  NC scalar. The uniform error is

      eta_n + A_n{a[n P+2 W]+1}.

  For a common gap delta_n the active block vanishes in query units if
  delta_n sqrt(n)->infinity and enough damping has accumulated to make
  sqrt(n) product b_j->0. One endpoint credit scalar then suffices; n forward
  coordinates are counted while streaming. This extends the earlier specific
  sustained-chart argument; it is not a whole-class cap.

No old chart is revived or re-evaluated. The accepted n200/400/1000 collisions
are recorded as chart failures, not whole-class results.

## 2. Strongest theorem for weakening-gate histories

For ANY admissible selected-feature history, if the last L steps have gate
defect <=delta, its reference endpoint is close to the PUBLIC undamped
resolvent M_infinity=(I-a O_*)^(-1):

    error <= eta_n + A_n[2n a^L+delta n^2],
    A_n=a||H||/n <= .3/sqrt(n).

Thus L of order n log(sqrt(n)/epsilon) and tail defect of order
epsilon n^(-3/2) suffice for ZERO history-dependent credit coordinates at the
fixed endpoint. This is a norm bound on the full finite gate variation,
including every fresh injection and all allowed future queries.

In particular, arbitrary aperiodic non-scalar gates satisfying
||I-G_*,t||op<=K/t have error at most

    eta_n + .6 sqrt(n) exp[-floor(T/2)/n] + .6 K n^(3/2)/T.

At the explicit sufficiently late threshold in PROOF.md (12), that meets
epsilon=1e-3. This closes the very-late harmonic-weakening subclass. It does
NOT close the same histories at earlier T, every weakening rate, or arbitrary
aperiodic gates. The large norm of accumulated credit need not be encoded if
its large component has become public and history-independent.

## 3. Best whole-class bounds

| Class at the same fixed endpoint | Lower / upper currently justified |
|---|---|
| Arbitrary admissible fixed-feature histories | accepted Omega(n); upper r^2=O(n^2) |
| Latent-cycle arbitrary histories | upper d^2+1; no universal linear upper |
| Fully sustained selected-block subclass | O_(u,epsilon)(n) online; eventually zero endpoint credit |
| Long dissipative latent-cycle tails meeting (5) | one endpoint credit scalar; n forward while streaming |
| Very weak tails meeting (8) | zero endpoint credit; n forward while streaming |
| Complete model | accepted Omega_c(n^2) to O_c(n^2 log n), unchanged |

The accepted one-pulse lower can be written as
2floor((floor(n/2)-floor(n/4))/2)-1 >= floor(n/4)-2.
It remains outside the uniformly sustained and nearly ungated small-error
conditions that would contradict it. The lower is not re-proved here.

## 4. Is whole-class Theta(n) proved?

**NO. It is neither proved nor refuted.** No jointly admissible omega(n)
finite-radius section is constructed. No O(n) whole-class encoder is supplied.
The simple estimates above are sufficient tests, not converses or exact
dimension formulas. A bound exceeding epsilon is not a lower certificate.

## 5. Smallest remaining obstruction

The intermediate gate regime remains uncovered: enough recent non-scalar
loss to keep the public-resolvent error above epsilon, but too little active
dissipation to bound fresh credit by o(sqrt(n)). Order-1/n gate gaps across
an order-n-log-n window are an example not decided by these tests. Harmonic
weakening near that horizon also escapes the sufficiently late collapse.

The missing theorem is a finite-radius worst-query bound for the **reachable
mixed credit**, with a continuous counted O(n) representation, in that regime.
Even the latent-cycle d-by-d recurrence is unresolved; arbitrary nonuniform
NC gates make the whole class larger. Query row geometry alone does not
bound how much independent information those rows contain. No joint gate-
innovation conservation law or robust superlinear countersection was found.

## 6. Consequence for the full model

The n^2 versus n^2 log n gap is unchanged. The new results remove particular
dissipation/weakening subclasses as routes to a universal superlinear
fixed-feature lower; they do not combine into an arbitrary-history encoder.
Even a future fixed-feature Theta(n) theorem must establish simultaneous
feature compatibility and count all shared structure before implying the
full quadratic upper. Different same-endpoint lower sections cannot simply
be added or multiplied.

## 7. Recommended next theorem

Prove or refute an O(n) finite-error continuous width bound for the reachable
intermediate weak-gate active block, retaining the ACTUAL all-query norm and
coupled source injections. The proof should control the fresh-credit suffix
sum, not only old-history fading. A counterexample must be ONE admissible
same-h continuous section with every antipodal half-margin>epsilon.

No further experiment or new research stage is started.

## Evidence, resources and records

* New arguments: algebraic finite-error scoped theorems; independent hostile
  review still required. Accepted moving-spike results remain premises.
* Manual checks: CHECKS.md. No automated tests or numerical experiments were
  added or run in this theory-only attempt. No numerical outputs are cited as
  a new proof, and no R3/R4 computation is needed.
* Experimental CPU time: 0. GPU/CUDA time: 0; no ML runtime/model server was
  launched. Shell/documentation/Git overhead and whole-turn peak RAM were not
  instrumented. No claim of measured total process CPU or peak RAM is made.
* Source checkpoint, read-only handoff hashes and local tracking status:
  PROVENANCE.json. Accepted handoffs that were locally untracked remain so;
  they are not represented as already committed remote evidence.
* Own files only, plus the Codex resume and shared research pointer, are
  changed. AGENTS, Claude evidence/notebook, previous outputs and GAS-0 are
  preserved. The final task report identifies the completed documentation
  commit; PROVENANCE.json records the starting checkpoint.
