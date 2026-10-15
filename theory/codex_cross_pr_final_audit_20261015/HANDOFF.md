# Research handoff after the final cross-PR audit

2026-10-15. This document proposes future proof/counterexample targets; it proves
neither Hypothesis B nor removal of the logarithmic loss. The original frozen dense
tanh, full d_F normalization/query contract, h0=0 and complete peak-width-times-
horizon mT measure are fixed. Dense corrections, preparation and reset are charged.
The verified conditional theorem is for d_F,E, not a substitute definition of full d_F.

## A. Hypothesis B: first control the complete bus, not just rank-two X

**Most promising approach:** derive a budget-aware bound on the accumulated
standard-coordinate broadcast/capture kernels. Work with the exact own/bus split
of B', which uses actual gates/source and R0 transport. Do not equate the bus with
the U-coordinate X-transfers: U-wrap transport and the uniform injection component
remain even when X=0. Rank <=2 per step is not rank <=2 over the entire horizon.

Here is a precise coupled identity to organize that work. On memory rows define

```
L=[a 1_(>=1), a gamma e1/sqrt(k)],
R_t^pm=[ J(B'_(t-1)^pm) ; Sum'(B'_(t-1)^pm) ],
Phi_S^pm(T,t)=(G_T^pm aS)...(G_(t+1)^pm aS),
K_t^pm(nu)=nu_mem^T Phi_S^pm(T,t) G_t^pm L.
```

R_t is 2-by-(n-1) after dropping the redundant parameter column, and K_t is 1-by-2.
For the same common future query in both histories, exactly

```
nu_mem^T Delta D_T
   =sum_t [ Kbar_t(nu) Delta R_t + Delta K_t(nu) Rbar_t ].
```

This is an algebraic restatement, not a smallness estimate. Both feedback channels
must be retained, as must their code dependence. In particular, the state-only
listing makes state J and Sum' even; it does **not** make credit J or Sum' even.

**Exact missing inequality:** at the zeros theta* of Theorem 4's actual odd listing,
under its below-budget hypotheses,

```
sup_(all legal F,gates) ||sum_t [Kbar_t Delta R_t+Delta K_t Rbar_t]||2 <=tau/4.
```

Bounding the two sums by tau/8 each would suffice, but is stronger than necessary
and cancellation must not be excluded by assumption. A useful first intermediate
target is a weighted coherence/occupation bound on the sequence R_t, combined with
the suffix-product capture budget, that charges long near-neutral paths to actual
protected position-steps. A mere sum of per-step norms may lose exactly the coherence
information needed here. The capture lemma is an upper bound; its bath coefficient
does not give a positive lower bound on capture.

**Next small CPU diagnostic, if needed in the next phase:** directly unroll both
standard bus channels for admissible histories, separate the two terms above, and
compare the singular spectrum and legal-query norm of their accumulated sum.
Use sparse schedules with long off-cycle captures and staggered broadcasters;
enforce the state-listing equalities rather than testing arbitrary gate matrices.
Keep this a finite counterexample search, not training and not evidence that B is proved.

**What counts as proof:** a uniform inequality in the actual model, for the stated
continuous common-endpoint sections, all required listing zeros and all legal queries,
with the current tau/4 budget. For the contradiction alone it would also suffice
to prove existence of one suitable zero; that is a different, weaker formulation
than a statement holding at every zero and should be named explicitly.

**What counts as a counterexample:** a legal section in B's stated domain and a
listing zero where one legal query has bus norm >tau/4, with exact group normalization,
dimension, endpoint and mT accounting verified. A high bus norm on a pair that is
not a required listing zero does not refute B. A small-n example outside the theorem
range is diagnostic only. Even refuting B would not solve the original problem:
large coherent bus content can have low robust dimension. Resolving the original
question needs either a robust legal construction or a full-contract impossibility.

## B. Removing the logarithmic loss: charge information, not total old magnitude

The current release bound has the form

```
R1(w)<=C T sqrt(m) exp(-kappa w)
       <=C sqrt(mu) n sqrt(y) exp(-kappa w),    y=T/sqrt(n).
```

Making this O(tau) uniformly forces w~(log+ y)/(2kappa). The larger carrying set
p~m(Lambda+w) propagates that log into the dimension/resource bound. Optimizing
query spike constants alone cannot remove this source of loss.

**Most promising approach:** replace the uniform magnitude cutoff by a
budget-weighted approximation of old own profiles. Long, high-amplitude old profiles
must have spent time near-neutral, and maintaining many independent such profiles
should be charged to protected position-steps and their preparation. Use a continuous
soft listing for the large profiles; a hard, code-dependent truncation may destroy
the continuity needed for Borsuk–Ulam.

One precise **sufficient new lemma**, to be proved or refuted, is the following.
Choose a fixed release window w0 depending on the existing constants, not y. Add
an odd continuous listing Psi_old with pointwise nonzero-coordinate count

`<=C0 m+C1(mT/n)^2`,

such that, at a joint zero with the fixed-window state/recent-profile listings,
the remaining old own-content readout is <=tau/32 uniformly over all legal queries.
Constants may depend on the fixed kappa, Lambda and epsilon, but not on n,m,T,D.
The previous source, dense, spike and B allocations must remain valid.

Such a lemma would replace the logarithmic carrying-window cost by

`D<=C m+C(mT/n)^2+N3`.

Together with T>.001sqrt(n), 2N3<=D<=n and B, its two branches would give
mT>=c D sqrt(n), with no asymptotic log. This is a **target implication**, not a
new theorem proved in this audit. It would still require an explicit full-metric
extension before being called a solution under the unchanged original contract.

A pure magnitude bound such as old content <=C mT/sqrt(n) is an unsafe target:
a single repeatedly protected off-cycle coordinate can accumulate O(T) own credit
at cost O(T). The issue is the number of robust independent directions after a
small listing, not whether every individual old credit row is small.

**What counts as proof:** the proposed approximation/count inequality, or another
uniform argument yielding the logarithm-free resource law with continuity, actual
support, preparation costs and the current error budget intact.

**What counts as a counterexample to that strategy:** an admissible budgeted family
of old own profiles for which every listing of the proposed size leaves a legal-query
residual >tau/32. Arbitrary bounded-variation vectors not realizable by the model
are insufficient. Failure of this particular approximation lemma would not by itself
prove that the logarithmic loss in the true resource law is necessary.

## Order of work

1. Settle the complete-bus kernel inequality, or isolate a legal counterexample to B.
2. If B survives, investigate the old-profile occupation/continuous-approximation lemma.
3. Keep selected-group and original full-d_F claims separate; write any extension
   under the inherited normalization and legal-query family explicitly.

Do not resume a claim of an unconditional n^(3/2) theorem from the present records.
