# Future-loss observability and a continuous exact-state lower bound

2026-09-30. The arbitrary-width accessibility theorem at commit0cbe1a8 is an
accepted premise. The owner reports two independent reviews against its actual
proof. That theorem is not reproved here. This document studies exact gradient
queries at frozen parameters. It does not propose an architecture or a learning
experiment. The new arguments still warrant independent mathematical review.

## 1. Objects and four distinct loss contracts

Fix theta=(R,W,b) and h'=tanh(Rh+Wx+b), with P=2n²+n. A past input history
ends at h in R^n and S=D_theta h in R^(n x P). All parameters are fixed along
both the past and future computation. The accepted theorem supplies a reachable
open set O of (h,S), of dimension n+nP, at a fixed finite horizon. Locally it
contains a product U_h x U_S. Fixing h=h* in U_h leaves an open nP-dimensional
set U_S of reachable sensitivities. This fiber, not the rank of one S matrix,
is the information family considered below.

A query is chosen AFTER the past has been encoded/discarded. It specifies a
future input history v=(v1,...,vL), possibly L=0, and a terminal scalar loss
ell on the future hidden state. The future inputs are held fixed when taking
parameter derivatives. A feedback controller, differentiated input-selection
rule, or parameter-dependent loss would require extra terms; none is implicit.

Four contracts must be distinguished:

A. Immediate arbitrary linear loss: ell_c(h)=c^T h, c any vector in R^n.
   The gradient is S^T c.
B. Loss only after L>=1 future recurrent steps. Terminal losses may either be
   arbitrary linear losses or a separately specified restricted family.
C. A fixed low-dimensional output head H: y=Hh, ell=phi(y). H is known and
   theta-independent. For immediate losses the adjoint lies in im(H^T).
   Allowing future inputs/dynamics changes the observable space and must be
   stated separately. Output dimension alone is not the observable dimension.
D. Unrestricted smooth local immediate losses. Their derivatives at h* include
   every c, since linear losses are a subfamily. Thus their sensitivity query
   space agrees with A. Values are a separate output contract.

If only one fixed loss or a finite data distribution is permitted, these
contracts need not apply. The result below quantifies over all allowed late
queries, not over the errors of a particular training dataset.

## 2. Exact sensitivity distinguishability

For any adjoint family C at a fixed h, let Q=span(C), r=dim Q. The query family
maps S to {S^T c : c in C}. Two sensitivities are indistinguishable exactly when

    DeltaS^T c=0 for every c in C,

equivalently every parameter column of DeltaS belongs to Q-perp. The invisible
linear subspace is

    K_Q = {DeltaS : im(DeltaS) subset Q-perp},
    dim K_Q=(n-r)P.

Choose an orthonormal basis B for Q. The quotient can be represented by B^T S,
with rP real coordinates. The linear query map has rank rP; this is sharp on
an open full S-family. A single nonzero c has r=1 and returns P numbers. A
family whose span is R^n separates all nP coordinates: if DeltaS is nonzero,
choose a nonzero column d and c=d, giving its query component d^T d>0.
Equivalently n basis-vector queries return all rows of S. Many alternative
query families also separate S; the individual queries need not equal basis
vectors, be issued jointly, or lie in a neighborhood of zero.

The weakest linear condition for full separation on an open S-family is
span(C)=R^n. If r<n, a small nonzero member of K_Q can be added inside that
open fiber, giving genuinely reachable invisible differences. For a restricted
sensitivity manifold M, the exact weaker condition is

    (M-M) intersection K_Q = {0};

the ambient rP count must not replace the dimension of M automatically.

## 3. Future recursion: include the parameter injection

Let Phi_v(h;theta) denote L future steps. Set

    J_v=D_h Phi_v,  B_v=D_theta Phi_v with the starting h held fixed.

The full future sensitivity is

    S_future = J_v S + B_v.

For a theta-independent terminal loss with q=D ell at Phi_v(h), the actual
gradient is

    g_v,ell(h,S)=S^T J_v^T q + B_v^T q.

Thus c=J_v^T q is the effective current-state adjoint. It is incorrect to call
S^T c the WHOLE future gradient without the direct B_v term. However, for two
endpoints with the same h and theta and the same future query, J_v,B_v,q agree,
so the gradient difference is exactly

    g(h,S1)-g(h,S2)=(S1-S2)^T c.

For future steps A_s=G_s R,

    J_v=A_L ... A_1,
    c=A_1^T ... A_L^T q.

An explicit theta-dependence of ell would add another common term at equal h;
it is excluded from the main contract. These formulas do not differentiate
through updates to theta or through adaptive selection of future inputs.

If R is invertible, every G_s is positive diagonal and J_v is invertible.
Therefore, for ANY one fixed admissible continuation, arbitrary terminal linear
losses q give C=J_v^T R^n=R^n. No hidden-state controllability theorem is needed.
The same conclusion holds for unrestricted smooth terminal local losses.

## 4. Restricted heads: genuine quotients and a stronger ordinary case

For immediate head losses phi(Hh) whose output derivatives range over all
R^(output dimension), C=im(H^T), r=rank H and observable dimension rP. If the
loss derivatives range over a smaller set, use the span of their actual
pullbacks. For example, a constant loss sees nothing. Softmax/cross-entropy
derivatives obey a sum-zero constraint; one must compute their actual span
rather than equate output count with adjoint rank.

For a FIXED continuation and arbitrary head-output losses, C=J_v^T im(H^T)
still has dimension rank H. But varying future continuations can increase its
span. It is therefore wrong to conclude that a scalar head always observes
only P sensitivity coordinates across future queries.

One-step full-span lemma. Suppose R,W are invertible, admissible next inputs
form a nonempty open set, and the fixed scalar terminal loss is q^T h_next,
where every q_i is nonzero. At fixed current h,

    c(v)=R^T G(v) q.

Choose a next-input point with all next preactivations nonzero; such points
exist in every open input set because W is invertible. The map from v to the
diagonal gamma of G=diag(sech²(Rh+Wv+b)) has derivative

    diag(-2 sech²(a_i)tanh(a_i)) W,

which is invertible there. It maps a neighborhood onto an open gamma set.
The map gamma -> R^T diag(q) gamma is invertible. Therefore C contains an open
subset of R^n and spans R^n. It need not equal all R^n or contain zero; its
linear span is what separates sensitivity differences. This yields full
observability using one fixed scalar linear head and one chosen future input.
The additional inverse-entry condition is used by accessibility, not this
one-step lemma.

For q with exactly s nonzero entries, this one-step C has local dimension s
and span dimension s, given by R^T span{e_i:q_i!=0}. More steps may enlarge it.
For contrast, fully actuated diagonal recurrence with head e1 observes only
state1 at every future horizon. Hidden-state controllability by W does not
by itself prove adjoint observability.

## 5. Optional stronger separation for any nonzero scalar head

The same accepted assumptions actually suffice for span separation even if q
has zeros, when query horizons1,...,n and arbitrary admissible future inputs
are allowed. The following is a span claim; an open n-dimensional C at one
specific horizon is not needed or claimed here.

First R^(-1) is a polynomial in R by Cayley--Hamilton. If there were no directed
walk from j to i in the nonzero-entry graph of R, every (R^k)_ij would vanish,
and so would (R^(-1))_ij. Every inverse entry nonzero therefore implies that
this graph is strongly connected; its transpose is strongly connected as well.

For any fixed finite L, future gates G1,...,GL vary independently over a small
product open set. Indeed the map from future inputs to preactivations is block
triangular with W on its diagonal; composing with coordinatewise sech² keeps
it locally invertible wherever every preactivation is nonzero. Such a point
can be chosen successively from the open allowed input set.

Expand

    c=R^T G1 R^T G2 ... R^T GL q

as a polynomial in these gate coordinates. The coefficient of the monomial
gamma_(1,i1)...gamma_(L,iL) is

    q_iL product_(a=1..L-1) (R^T)_(i_a,i_(a+1)) R^T e_i1.

Distinct monomials are independent on a product open set; finite evaluations
therefore put each coefficient vector in the span of actual adjoint vectors.
Starting at any index j with q_j!=0, strong connectivity gives a nonzero path
in R^T from j to each i of length at most n-1. At horizon one plus that path
length, the displayed coefficient is a nonzero multiple of R^T e_i. Thus
the union of C at horizons1,...,n spans every R^T e_i, hence all R^n.

These are different allowed FUTURE QUERIES on the SAME endpoint. A separating
family is allowed to use multiple hypothetical futures; no incompatible past
endpoint Jacobians are combined. This argument is independent of the prior
accessibility proof and includes the direct sensitivity injection via section3.

For a squared scalar-head loss with a selectable target, choose a target whose
residual at the common future state is nonzero. Its query is a nonzero scalar
multiple of the corresponding linear-head query, so the same separation holds.
No conclusion is drawn for a fixed restricted target distribution without
checking its permitted residual/query span.

## 6. Separation theorem

At fixed theta,h, under ANY query contract whose effective adjoints span R^n,
every nonzero reachable DeltaS is distinguished by some allowed future
gradient query. The theorem follows immediately from section2 and the
cancellation of B_v in section3. Unrestricted immediate linear losses need
no additional dynamical hypotheses. For future arbitrary linear losses,
invertible J_v suffices. For a fixed full-support scalar linear head with
variable one-step input, section4's R/W/open-control assumptions suffice.
For any nonzero scalar linear head, the accepted recurrence assumptions plus
horizons1,...,n suffice by section5.

The reachable open fiber U_S has dimension nP. Under these contracts the whole
nP-dimensional family is exactly observable. Under a restricted contract of
adjoint-span dimension r, its exact observable quotient has dimension rP.
Thus the loss contract is essential to the result. The primary classification
in this report uses the full-span contract defined in config.json, not an
unspecified realistic training loss.

## 7. Continuous encoding lower bound

Define the computational model explicitly:

1. Fixed known theta and fixed finite past horizon. The query is chosen after
   the past has been processed. All history-dependent persistent storage is
   counted as a point in R^k. Fixed model/program constants are not history.
2. Encoding is continuous in the reachable endpoint, or more generally in the
   past inputs through continuous online state updates. Nonlinear encodings
   are allowed. Decoder continuity is NOT needed.
3. From this encoded state and the future query, the algorithm answers exactly
   every allowed gradient. It has no discarded-input replay, external tape,
   retained uncounted graph, variable symbolic store, or hidden state oracle.
4. Fresh future inputs, the chosen loss, known time, and fixed parameters are
   legitimate side inputs. They cannot include the discarded past or true S.

Fix h=h* and U_S. If E:U_S->R^k has E(S1)=E(S2), every deterministic query
decoder produces the same answer. Separation implies S1=S2. Thus E is a
continuous injection on a nonempty open subset of R^(nP).

Invariance of domain implies k>=nP: if k<nP, pad E with zeros into R^(nP).
This is a continuous injection from an open nP-dimensional set to R^(nP),
so its image must be open. But it lies in a proper k-dimensional coordinate
plane with empty interior, a contradiction. This proof needs no derivative,
linear encoder, bound on decoding time, or continuous decoder.

An online history encoder need not be a function only of (h,S); it may remember
irrelevant history too. The accepted endpoint map is a submersion at its full
rank point. Choose independent input coordinates for a maximal minor and hold
the other coordinates fixed. The inverse function theorem supplies a smooth
local history section X(h,S). Composing continuous online encoding with
X(h*,S) gives the E above. Therefore redundant history in the state cannot
evade the bound. This step prevents an unjustified assumption that every
learner's memory is uniquely determined by the endpoint.

For a proper query span r, restrict U_S to an affine transversal varying only
the rP observable coordinates. The same argument gives k>=rP for those
coordinates, and the abstract statistic B^T S attains rP at the endpoint.
This alone does not prove an efficient online update for that smaller
statistic; future adjoint closure must be checked separately.

## 8. Hidden state and the sharp total count

The fixed-h bound nP is sensitivity information alone. If h is supplied
externally, it is side information; n coordinates must not then be charged
again to this encoder. If an algorithm stores h explicitly in addition to
auxiliary state a in R^k, fixing h in the product neighborhood makes a(S)
injective, so k>=nP and total n+k>=n+nP.

For a general joint representation E(h,S), a total d=n+nP lower bound requires
an exact-forward contract: h must be recoverable, or the algorithm must answer
all immediate linear LOSS VALUES c^T h as well as the corresponding gradients.
Those observations separate both h and S on the reachable product open set,
so E must be injective there. The same invariance-of-domain argument gives

    total k >= n+nP = 2n³+n²+n.

No double counting occurs: full endpoint accessibility supplies genuinely
independent h and S coordinates. For immediate linear GRADIENTS ONLY, h is
invisible, so a d-dimensional bound would be unjustified; nP is the established
bound. Whether restricted future gradient outputs alone separate h as well
is not asserted. If a decoder receives h from an external source, that source
must be acknowledged in the accounting.

RTRL retaining h and S gives an exact online realization with n+nP persistent
real coordinates, up to fixed model/constants and temporary work buffers.
Thus the persistent-coordinate lower bound is sharp for this exact-forward,
all-future-query model. It is not a runtime, bit, word, or general learner bound.

## 9. Escape routes and their status

| Route | Effect on the theorem |
|---|---|
| Nonlinear continuous coordinates | Still an injection; cannot lower dimension |
| Continuous low-rank/factorized/implicit state | Every factor/history-dependent scalar counts; no compact exact code on the full open family below nP |
| Smaller sufficient statistic | Works for a restricted r-dimensional adjoint span; genuine reduction to rP at the endpoint |
| Query known before encoding | Changes the late-query quantifier; storing S^T c can suffice for that one query |
| Approximate gradients | Changes exactness; invisible/tiny directions may safely be discarded; no quantitative bound proved |
| Discontinuous encodings / digit interleaving | Outside continuity assumption; set-theoretic/infinite-precision packing is not excluded by this theorem |
| Symbolic or variable discrete storage | Must account for all bits/objects; not covered by the fixed continuous-real-state model |
| Replay / reversible history reconstruction | Uses retained/retrievable history; outside the no-replay model unless all information is encoded continuously in counted state, in which case the bound returns |
| History tape / BPTT / checkpointing | Legitimate exact methods using history and/or recomputation; do not satisfy the discarded-history model |
| Unbounded decoder time with no history | Cannot distinguish a collision in E, so alone cannot escape |
| Extra parameters / model buffers | If history-dependent, include in state; fixed theta is not an extra history channel |
| Changing parameters while learning | Different derivative objective and reachable family; not analyzed here |
| Finite/discrete or seed-generated past-input family | May admit a small generative description; the open reachable-family premise is then absent, so this is a genuine scope restriction |

The strongest genuine limitation is the permitted query family and exactness:
a narrow, known or approximate loss contract can remove the nP requirement.
The strongest exact algorithmic escape is retained-history BPTT/replay, which
lies outside the stipulated streaming information model. No practical learner
is claimed to need this full exact query interface.

## 10. Independent recurrence comparison

For h_i'=tanh(r_i h_i+w_i^T x+b_i), parameters have one recurrent output owner.
P_ind=n²+2n, and only P_ind sensitivity entries can be nonzero. Each parameter p
has one trace e_p in its owner row. The exact scalar recurrence is

    e_p'=g_i(r_i e_p + direct source_p),

and closes within those owner traces. There is an exact persistent upper bound
n+P_ind=n²+3n, rather than n+nP for dense interaction. A full-support immediate
head q queries gradient_p=q_owner(p) e_p; one query is already injective on
all owner traces. On an open reachable owner-trace fiber, the matching continuous
lower bound is P_ind, or n+P_ind with forward state preserved.

Prior independent certificates establish full owner-endpoint rank at n=2 and4,
so these lower bounds apply at those witnessed widths. The O(P_ind+n) upper
bound holds at every width from the explicit exact trace recurrence. No new
all-width independent accessibility proof is assumed or run here. Thus the
comparison is an exact-state organization distinction, not a capability claim.

## 11. Existing width3 two-layer cross sensitivities

The saved two-layer recurrence is

    h1'=tanh(R1 h1+W1 x+b1),
    h2'=tanh(R2 h2+W2 tanh(h1')+b2).

At width3 each layer has21 parameters, total42; global hidden state6. The saved
same-point certificates give an open reachable supported endpoint of dimension
195: h dimension6, within-layer derivatives E dimension126, and upper-state /
early-parameter cross block C dimension3x21=63. Holding (h,E) fixed in a local
product section leaves an open63-dimensional cross fiber. These certificates
are accepted/read-only premises; they are not recomputed.

An upper-layer immediate linear loss q2^T h2 queries early-parameter gradient
C^T q2. Arbitrary q2 spans R^3, so all63 cross coordinates are distinguished.
The same continuous encoding argument gives at least63 extra coordinates
conditional on fixed h,E. One fixed immediate q2 only sees21, and must not
be reported as observing63 by itself.

With one future step, differences restricted to C propagate as DeltaC'=G2 R2
DeltaC: lower-layer state and its sensitivity are identical, so all other
injections cancel. A fixed full-support upper scalar head therefore has
effective adjoint R2^T G2 q2. If R2,W2,W1 are invertible, the external input
can vary G2 over an open set: D_x q2_pre=W2 diag(sech²(h1')) G1 W1 is invertible,
and choose upper preactivations nonzero. This proves full cross separation
under that fixed-head future contract too. Exact rational determinant checks
below verify these matrix assumptions at the archived width3 point.

Arbitrary linear losses on all6 hidden coordinates distinguish every supported
sensitivity coordinate189. With exact-forward state preserved, the analogous
total bound is195 on this finite-width certified family. No arbitrary-width
deep theorem or upper-head-only195 bound is claimed.

## 12. Classification, conditioning and exact next step

**FULL EXACT OBSERVABILITY — CONTINUOUS STATE LOWER BOUND PROVED**

This classification is conditional on the explicit full-span, late exact query
contract and continuous discarded-history state model. Unrestricted losses
work; even a fixed full-support scalar head after one chosen future input works
under the stated assumptions. Restricted contracts may give a smaller quotient.

The conclusion is mathematical separation and a sharp exact-real persistent
coordinate bound, not quantitative observability. Previous tiny singular
directions may be practically irrelevant at finite precision. No bit bound,
practical memory need, learning benefit, runtime lower bound, or architecture
novelty is proved. Accepted accessibility is a premise, not rerun in this task.

Single next step: independent mathematical review of this observability/encoding
proof, especially the local history section and total-versus-auxiliary accounting.
No learning, Stage C, AMS v10 or architecture work starts from this result.

Primary mathematical reference: Allen Hatcher, *Algebraic Topology*, section2.B,
Theorem2B.3 (book p172; chapter PDF p75),
[author's chapter](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf).
It states invariance of domain for continuous injections of an open subset of
R^d into R^d. Zero-padding into R^d gives the dimensional corollary used here.
Its hypotheses match our open fiber and continuous injective encoding; no
continuity of a decoder or injectivity of a differentiation operation is assumed.
