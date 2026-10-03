# Online realization of the chronological weak-gate polynomial

2026-10-02. New Codex theory; independent verification required.

**Finite-error status: OPEN.** No O(n) approximate realization and no jointly
robust superlinear section are proved here. A new exact-realization obstruction
is proved, with an explicit warning against using it as a finite-error lower
bound. No experiment or theorem about another gate regime is performed.

## 1. Accepted inputs and scope

Use the owner-verified definitions and lemmas in
`theory/codex_intermediate_gate_credit_20261002/PROOF.md` and its Grok review.
They are premises, not re-proved here. For n>=200, keep

    a=1-1/n, k=floor(n/2), l=n-k, r=k-1, d=floor(n/4),
    O=U(P_d direct_sum I_(k-d))U^T,
    U=I-2ww^T/(w^T w), w=e1-1_k/sqrt(k),
    R0=diag(aO,I_l/(100n)), ||R||op=a,
    ||R-R0||op=e_R<=4/(10^8 n^2), W=I, b_model=.05*1_n.

R is the existing fixed fully dense tanh model, not a new architecture.
E embeds physical memory coordinates 2,...,k; R0 E=a E O_* with O_* orthogonal.
The ONE public source is H=.4*1_l. The parameter injection is K H for the
selected recurrent block K; source columns are not independently chosen.

The actual common endpoint is h=0. The accepted query family has head
q=1_n/sqrt(n), loss divided by beta=max(1,||R||F), at least one future step,
and all future preactivations in [1/4,3/4]^n. Keep public group-RMS weight
w_R=||R||F/n and w_R/beta=1/n. For the actual effective future adjoint xi_Q,

    nu_n(Y)=w_R ||H|| sup_(Q legal) ||Y^T E^T xi_Q||_2,
    ||xi_Q||<=a/beta,
    nu_n(Y)<=A_n ||Y||op, A_n=a||H||/n<=.3/sqrt(n).       (1)

This is the actual worst-query pseudometric. Its operator-norm upper envelope
is used only for safe error bounds, never as an assumed attainable query.
The decoder adds the exact direct future contribution for the selected
parameter block, computed from the common h=0 and supplied query. This term
cancels in comparisons. Other source features and R/W/b blocks are not
silently summarized by a fixed-feature encoder.

The fixed window, after public source preparation, is

    N=ceil(4n log n)+1,
    G_t=I-diag(z_t)/n=g0 I+D_t/n,
    z_t in [.05,.25]^r,
    z0=.15, Delta=.1, g0=1-z0/n,
    D_t=diag(z0-z_t), ||D_t||op<=Delta.                  (2)

All N local steps have source injection alpha=1. The final zero reset has
gate I and gives endpoint M_end=aO_* M_N+I. Preparation/reset are explicit
exceptions to (2). Every simultaneous word in this cube has the accepted
coupled tanh realization, with inputs held fixed for parameter derivatives.
They are not independent artificial sensitivity injections.

Let b=a g0 (distinct from b_model) and

    q_n=a Delta/[n(1-b)]=a Delta/(1+a z0)<.087,
    C_n=Delta/[n(1-b)^2].

The accepted public p=p_n is chosen so that dense transfer, faded old credit
and the chronological tail jointly cost at most epsilon/4, epsilon=1/1000:

    eta_n+delta_old+A_n a C_n q_n^p/(1-q_n)<=epsilon/4.    (3)

Here eta_n<2e-9, delta_old<4e-8 for n>=200, and delta_old=0 for the
zero-credit preparation. Keep the original p rule and all constants unchanged.

## 2. The smallest explicit exact recurrence obtained

Introduce a FORMAL scalar lambda, with arithmetic modulo lambda^(p+1).
It is not a selectable input or a parameter of the actual tanh model:

    F_t(lambda)=(g0 I+lambda D_t/n)(aO_* F_(t-1)(lambda)+I)
                                      mod lambda^(p+1),
    F_0=0, F_t=sum_(j=0)^p lambda^j M_t^(j).             (4)

Multiplication order in (4) is essential. This is an exact, compact algebraic
description of the truncated polynomial, not a compact persistent store.

Degree 0 is completely public:

    M_t^(0)=b O_* M_(t-1)^(0)+g0 I,
    M_0^(0)=0,
    Q_t=aO_* M_(t-1)^(0)+I=sum_(j=0)^(t-1)(bO_*)^j.     (5)

It may be computed from public time/model constants without a history state.
Store only Z_t=(M_t^(1),...,M_t^(p)), with

    M_t^(1)=bO_* M_(t-1)^(1)+(D_t/n) Q_t,
    M_t^(j)=bO_* M_(t-1)^(j)
                    +(aD_t/n)O_* M_(t-1)^(j-1), j>=2. (6)

This is a switched affine triangular system. Its difference transition is

    [T_p(D) Z]_1=bO_* Z_1,
    [T_p(D) Z]_j=bO_* Z_j+(aD/n)O_* Z_(j-1), j>=2.      (7)

The forcing in block 1 is (D/n)Q_t, and the other blocks have zero forcing.
The terminal output operator is

    P(D)=aO_*[M_N^(0)+sum_(j=1)^p Z_(N,j)]+I.           (8)

Count: p r^2 history-dependent credit scalars, plus n current hidden-state
coordinates while processing actual inputs. Public time, the fixed schedule,
O_*, Q_t, normalization constants and model weights are uncounted under the
accepted contract. Adaptive bases/factors and any stored gate history are
counted. Arithmetic workspace and final output storage are not persistent.

This removes the previously counted public degree-0 matrix. It does NOT
claim that p r^2 is a globally minimal realization dimension.

### Why one Horner value does not close exactly

Let V_t=sum_(j=0)^p M_t^(j). Direct summation yields

    V_t=G_t(aO_* V_(t-1)+I)
                       -(aD_t/n)O_* M_(t-1)^(p).        (9)

The last term is the discarded degree-(p+1) boundary. A single evaluation
F_t(1) omits information needed for its own next update. Evaluation at 1 is
not a ring homomorphism from the truncated algebra: lambda^(p+1)=0 there,
but 1^(p+1)=1. Noncommutative Horner notation does not remove (9).
The impossibility statement below rules out an EXACT O(n) realization of
the whole selected truncated polynomial, not just this naive update.

## 3. Best finite-error upper: one exact reference matrix

Instead store the exact reference M, with

    M_t=G_t(aO_* M_(t-1)+I), M_0=0.                    (10)

Return aO_* M_N+I to answer the queries of (8). The accepted tail estimate
gives, uniformly over every admitted word and every actual permitted query,

    nu_n(aO_* M_N+I-P(D))
                         <=A_n a C_n q_n^p/(1-q_n)
                         <=epsilon/4 <3epsilon/4.      (11)

Thus there is a continuous causal approximate encoder with EXACT count r^2
endpoint-credit coordinates, or r^2+n while processing actual inputs.
No replay, tape or history-dependent free factor is used. Actual selected
gradient queries, without the polynomial proxy, have error at most
eta_n+delta_old by the already-accepted reference ledger.

The coefficient cascade is smaller syntactically, but (10) is smaller in
persistent memory. Approximate representation is allowed to use the
untruncated recursion as a sufficient statistic for the truncated output.
This is the best general upper obtained here: O(n^2), not O(n).

## 4. A new exact-realization theorem -- explicitly NOT robust

### Theorem E: exact polynomial realization needs at least m p coordinates

Let m=floor((k-d)/2). For the public degree p>=1 and N>=2p, a continuous
online state that must answer EVERY final query of (8) EXACTLY, after every
admitted remaining gate suffix, requires at least m p real coordinates.
The prefix hidden state can be fixed in this proof, so there is no hidden
free memory. For the chosen p_n at fixed epsilon, this is Omega(n log n).

This theorem concerns zero-error reproduction of the ARTIFICIAL truncated
polynomial. It is NOT a superlinear finite-epsilon bound for the accepted
credit problem. The proof uses an actually reachable channel subsystem;
it does not count ambient matrix entries or monomials.

### 4.1 Reachable scalar channels within the given family

Take m disjoint pairs of physical NC coordinates d+1,...,k and let

    v_j=E^T(e_(i_j)^k-e_(i'_j)^k,0_l)/sqrt(2).

Each pair difference has coordinate sum zero, so the Householder U fixes it;
the latent cycle leaves these NC coordinates fixed. Hence O_* v_j=v_j.
Choose equal defects d_(t,j) on the members of each pair, independently
across pairs and time, and public zero defects on other coordinates. Every
such word is in (2) and has the accepted simultaneous tanh lift.

For all coefficients and all times,

    M_t^(i) v_j=f_(t,j)^(i) v_j,
    f_(t,j)(lambda)=(g0+lambda d_(t,j)/n)
                         [a f_(t-1,j)(lambda)+1]
                                      mod lambda^(p+1). (12)

This follows by induction from O_* v_j=v_j, equal pair gates and M_0=0.
It does not assert that the complementary operator block has no state.
Other sensitivity coordinates cannot cancel a projected column (12).

### 4.2 Full open coefficient family on each channel

At the first p weak steps use nominal d_(s,j)=d_*=Delta/2, and allow
independent small perturbations of these m p values. All stay strictly in
[-Delta,Delta]. Put

    G(lambda)=g0+d_* lambda/n,
    b=a g0,
    t_*=a d_*/n >0.

At the nominal history, for one channel and 1<=s<=p,

    partial f_p(lambda)/partial d_s
      =(lambda/n)(aG)^(p-s) sum_(j=0)^(s-1)(aG)^j
      =(lambda/n) sum_(j=p-s)^(p-1)(b+t_* lambda)^j
                                      mod lambda^(p+1). (13)

This derivative includes the perturbation of the source injection. It is
not a free variation of unrelated coefficient columns.

Successive differences of the columns in (13) give the polynomials

    (lambda/n)(b+t_* lambda)^j, j=0,...,p-1.

In the coefficient basis lambda,...,lambda^p their matrix is triangular
when ordered by j, with diagonal entries t_*^j/n. Therefore

    |det partial(f_p^(1),...,f_p^(p))/partial(d_1,...,d_p)|
                =n^(-p) t_*^[p(p-1)/2] >0.             (14)

The cumulative-column change has determinant of absolute value 1. The
ordinary finite-dimensional inverse-function theorem supplies a locally
open p-dimensional coefficient family. No numerical rank is used.

Append one public weak step with D=0. Then the current actual hidden state
is common across the prefix family: prescribed magnitudes/signs are the
public baseline and source H. Every nonzero-order scalar coefficient is
multiplied by b, so the determinant gets factor b^p and remains nonzero.
Across m independent pairs the coefficient map is block diagonal: a locally
open m p-dimensional family results at time p+1. All histories are admitted
by the already-verified cube lift. A sufficiently small coefficient-control
ball has finite physical history radius; no uniform radius is asserted.

### 4.3 Different coefficient prefixes are distinguishable by ONE continuation

Take two such prefixes and a channel with nonzero difference

    v(lambda)=sum_(i=1)^p v_i lambda^i.

Let L=N-(p+1)>=p-1. Continue that channel with a constant admitted defect d'
for all L remaining interior steps. The source forcing is identical for the
two histories and cancels, giving difference (b+a d' lambda/n)^L v(lambda)
modulo lambda^(p+1). Its evaluation at lambda=1 is

    H_v(d')=sum_(j=0)^(p-1) binom(L,j) b^(L-j)
                         (a d'/n)^j sum_(i=1)^(p-j) v_i. (15)

All binomial coefficients in (15) are nonzero. The cumulative sums
sum_(i=1)^(p-j) v_i cannot all vanish unless v=0. Thus H_v is a nonzero
polynomial, and some d' in the admitted open interval makes it nonzero.
This is a distinguishing suffix of the SAME length and actual input history
for both prefixes: their current h is common, so the prescribed suffix
states induce the same tanh inputs. The reset multiplies this difference
by a; it does not erase it.

There is also an actual allowed final query. At one future step use
preactivation 1/4 and 1/2 on the members of every pair. Other coordinates
also have an allowed preactivation. With s_g=(sech^2(1/4)-sech^2(1/2))/2>.07,

    v_j^T E^T xi_Q
      >=[a sqrt(2) s_g/sqrt(n)-e_R]/beta >0.            (16)

For a difference H_v(d') in (12), project the normalized parameter gradient
onto the orthonormal matrix (E v_j)H^T/||H||. Its difference is

    w_R ||H|| a H_v(d') v_j^T E^T xi_Q !=0.            (17)

Residual parameter coordinates do not cancel an orthogonal projection.
The query uses the original head, loss normalization and actual dense R.
There is no choice of independently injected source columns.

### 4.4 Count by prefix distinguishability, not matrix rank

If two coefficient prefixes had the same encoder state, a deterministic
online update with their identical selected suffix inputs would keep their
encoded states equal. The final decoder with the same legal query would
then return the same answer, contradicting (17).

The prefix encoder restricted to the locally open m p coefficient family
must therefore be continuous and injective. The accepted continuous-state
dimension principle implies at least m p real coordinates. This uses one
family of compatible histories, fixed prefix h, admissible suffixes and
exact query answers, not unrelated endpoint Jacobians or finite packing.

For the frozen degree rule, p_n=Theta(log n) at fixed epsilon: A_n C_n is
Theta(sqrt(n)), q_n tends to .1/1.15 in (0,1), and epsilon_star tends to
epsilon/4. This describes the chosen sufficient degree, not a necessary
degree for every approximate method. The size condition N>=2p holds for
n>=200: from (3), p<=ceil(log(134 sqrt(n))/log(1/.087))<=n, while
N>=4n log n+1>2n. Thus m p=Omega(n log n).

## 5. Why Theorem E does not answer the finite-error task

Both the reachable determinant and suffix observation can be extremely small.
Equation (14) contains powers of t_*=a Delta/(2n); (15) contains high powers
of a d'/n as well as b^L. Nonzero is not a width-independent error margin.
The local inverse radius was not bounded below uniformly. No antipodal
half-margin >epsilon has been established in m p dimensions.

There is a stronger finite-error check: the entire short-prefix family used
in Theorem E can be discarded with error <epsilon/8 under EVERY remaining
admitted gate suffix and final legal query. See Theorem F below. The exact
superlinear prefix dimension is therefore explicitly too weak for a robust
lower, rather than merely lacking a computed margin.

In fact, the scalar OUTPUT SUBSYSTEM used in the proof is summarized at
finite error by m ordinary scalar traces,

    ftrue_(t,j)=(g0+d_(t,j)/n)[a ftrue_(t-1,j)+1].       (18)

For its projected final outputs, (18) differs from the selected truncated
polynomial by at most the same tail bound in (11). This statement is only
about those channel-projected outputs. It does not assert an m-coordinate
encoder for all complementary outputs of the paired-gate family or for the
arbitrary diagonal cube.

Consequently exact minimal realization, exact Hankel-style distinguishability
or exact order independence can overcount FINITE-ERROR state even inside a
reachable subsystem. Using (14) as a robust lower would be invalid.

The strongest accepted JOINT robust lower does survive the proxy ledger.
The verified floor(n/8) section has actual half-margin >.00174. By (3), its
polynomial half-margin is >.00174-.00025=.00149. This exceeds both
3epsilon/4=.00075 and the buffered 5epsilon/4=.00125. Thus the unchanged
Omega(n) lower applies to the target approximate realization. The old section
is used as a verified lemma; it is not searched, re-certified or extended.
No omega(n) robust section is obtained.

## 6. The actual online metric includes admissible remaining gate suffixes

An endpoint approximation subspace alone is insufficient for an online
encoder: a weak current discrepancy might be routed differently by later
admitted PAST gates before the fixed reset. Future loss queries remain the
original contract. These two continuations are distinct.

At time t let Z,Z' be coefficient states with the same public degree 0.
For a remaining interior word w=(D_(t+1),...,D_N), let T_w be the ordered
product of the homogeneous transitions (7). Define

    L_p(Z)=aO_* sum_(j=1)^p Z_j,
    d_t(Z,Z')=sup_(w in admitted cube) nu_n(L_p T_w(Z-Z')). (19)

At t=N, w is empty. Injections cancel in the difference recurrence even
though each actual history retains its coupled injections. The pseudometric
uses all ACTUAL permitted queries through nu_n, not Frobenius/RMS or raw rank.
Its restriction to the reachable prefix family is the relevant behavioral
distance for online approximation.

### Lemma B: nonexpansive future-suffix metric

Let Phi_s(D) be the affine update from time s-1 to time s. For any admitted
next gate D,

    d_(t+1)(Phi_(t+1)(D)Z,Phi_(t+1)(D)Z')<=d_t(Z,Z').   (20)

Proof: forcing cancels. Every word in the left supremum, prefixed with D,
is one of the words in the right supremum. No norm substitution is required.

An explicit sufficient approximation route is a counted continuous C n-state
encoder with continuous lifts rho_t and updates F_t for which, throughout
its relevant states and admitted gates,

    d_t(rho_t(F_t(e,D)),Phi_t(D)rho_(t-1)(e))<=delta_t,
    sum_(t=1)^N delta_t<=3epsilon/4.                    (21)

Start with exact lift 0. By (20) and the triangle inequality, the lifted
approximation at t=N is within 3epsilon/4 of the polynomial output for every
legal query. Current h is counted separately unless included in the C n.
Equation (21) is SUFFICIENT, not necessary. In particular a crude sum of
per-step errors is not a memory lower bound if no such lifts are found.

Theorem E shows that the zero-error quotient cannot generally collapse this
system to C n coordinates. It does not preclude a finite-error approximate
quotient. A history-dependent basis must be included in e; an offline basis
requiring old gates to be replayed does not satisfy (21).

### A degree-and-age weighted all-suffix bound

For L=N-t remaining steps and a difference initially in order j, expanding
the homogeneous transition (7) shows that h further degree increments have
at most binom(L,h) chronological placements. Every no-increment propagation
has norm b; every increment has norm <=a Delta/n. Therefore

    d_t(Z,Z')<=sum_(j=1)^p w_(j,L) ||Z_j-Z'_j||op,
    w_(j,L)=A_n a sum_(h=0)^min(p-j,L)
                     binom(L,h)b^(L-h)(a Delta/n)^h.    (22)

No gate products are commuted in deriving this upper. In particular the
highest order has weight w_(p,L)=A_n a b^L; it cannot feed a retained higher
degree. This explicit weighting is valid for all actual permitted queries,
not a rank count or an RMS estimate. It alone does not bound the nonlinear
width of the continually forced reachable family.

### Theorem F: the exact superlinear prefix family is below epsilon/8

Set ||Z||_sum=sum_(j=1)^p ||Z_j||op and

    b_max=b+a Delta/n=a(1-z_minus/n)<1.

From (7), ||T_p(D)Z||_sum<=b_max ||Z||_sum. The forcing in (6) is at most
Delta t/n at time t because ||Q_t||op<=t. Starting at 0, for ANY admitted
first p gates,

    ||Z_p||_sum<=Delta p(p+1)/(2n).

The public baseline step used to fix current h only multiplies the coefficient
state by b. Thus, compared with the public all-zero-defect prefix of the
same length, for t=p+1,

    d_t(Z_t,0)
      <=A_n a b_max^(N-t) ||Z_t||_sum
      <=.015 p(p+1)/n^(3/2).                            (23)

Here .015=.3 Delta/2. This comparison changes only the short prefix: both
histories receive the SAME remaining gate word and reset and then the SAME
legal future query. The common prefix h makes those remaining actual tanh
inputs identical. The bound concerns the whole mixed polynomial, not just
the scalar channel projection used in Theorem E.

For the frozen p_n rule, epsilon_star>.000249, q_n<.087, and
A_n a C_n<=.03 sqrt(n). Consequently

    p<=ceil(log(134 sqrt(n))/log(1/.087))
      <=u(n)=log(134 sqrt(n))/log(1/.087)+1.

At n=200, u(200)<4.1. The function u(n)[u(n)+1]/n^(3/2) decreases for n>=200:
its logarithmic derivative, multiplied by n, is

    [1/(2log(1/.087))][1/u+1/(u+1)]-3/2 <0.

Substitution in (23) gives

    d_t(Z_t,0)<.015*4.1*5.1/200^(3/2)
              <.000113 <epsilon/8.                    (24)

Thus every prefix of the exact m p-dimensional coefficient family in Theorem
E is uniformly approximated by a single public zero mixed state at this
cut, at the requested finite-error scale. Its pairwise diameter is <epsilon/4
in the all-suffix metric. It cannot provide the requested robust antipodal
section at this epsilon. This is a finite-error upper for THIS short-prefix
family only. Later fresh forcing is not public and is not eliminated by it;
Theorem F is not a whole-window O(n) encoder or a whole-class upper.

## 7. Compression routes checked and their precise limitations

1. **Order sharing/Horner:** (9) retains an unresolved highest-order boundary.
   The exact scalar-channel obstruction (14)--(17) rules out an exact C n
   replacement for all the chosen degree-p responses. It permits approximate
   sharing, as the projected example (18) explicitly demonstrates.
2. **Companion/minimal realization:** (6)--(7) are explicit switched affine
   transitions, not a fixed linear time-invariant transfer system. Exact
   prefix distinguishability gives Theorem E directly. It supplies no
   epsilon-scale nonlinear realization lower.
3. **Krylov/spectral templates:** the forcing (D/n)Q_t and subsequent D O_*
   products must stay in the same counted closure. Powers of public O_* alone
   do not close arbitrary diagonal defects. No uniformly accurate small
   closure in (19) has been established.
4. **Shared factors/displacement/quasiseparable/tensor forms:** factorizing an
   r-by-r array is not a count unless all adaptive factors, core/bond sizes
   and their updates are bounded. This analysis proves no such uniform size
   bound and no general impossibility of approximate factorization.
5. **Query-invisible quotient:** (19) is the precise quotient metric. The
   paired channel family has no EXACT invisible coefficient direction under
   all suffixes, by (15)--(17). This does not establish a finite-error width
   for its complement or for the general reachable cube.
6. **Lower construction:** independent word controls in (13) are jointly
   admissible but their exact independence is ill-conditioned. Coefficient
   or Hankel dimension cannot replace an entire finite-radius antipodal
   inequality. Neither extra ages nor extra orders yield an omega(n) lower
   from these calculations.

These are bounded derivations and identified limitations, not claims that
every named representation was exhaustively ruled out. No spectral proxy,
ambient operator ball, failed packet merger or fixed-anchor renewal is used.

## 8. One smallest remaining theorem and consequences

**Finite-error causal realization statement.** For the explicit switched
triangular affine system (6), started at 0 on the diagonal cube (2), with
public degree p_n and horizon N_n, does there exist a uniform C and continuous
online updates/decoders using at most C n history-dependent coordinates whose
terminal error in (19) is <=3epsilon/4 for EVERY admitted word? Current h
must be included in that count or added as n coordinates; it cannot be a
history tape. Public schedule and weights may remain free. A sufficient
constructive version is (21); failure of that version alone is not a refutation.

This is now a fully specified finite-error nonlinear realization problem,
with public forcing, a known triangular transition and an actual future-suffix
query metric. Its zero-error version has a superlinear obstruction proved
here. Its finite-error version remains unresolved.

Alternatively, a refutation needs ONE admitted same-endpoint continuous
section of dimension omega(n) whose polynomial antipodal half-distance
exceeds 5epsilon/4 under nu_n, or another correctly budgeted actual margin.
Theorem E provides no such margin. No two-history packing or axis count is
substituted for it.

Strongest finite-error bounds remain

    floor(n/8)<=fixed-feature intermediate d_rob<=r^2
                              (plus n forward while streaming),
    whole fixed-feature Omega(n)<=d<=O(n^2),
    full model Omega_c(n^2)<=d_rob<=O_c(n^2 log n).

No fixed-feature Theta(n) theorem or superlinear robust refutation is obtained.
Even a later one-feature encoder needs compatible simultaneous feature
summaries before closing the full-model gap. No architecture, learning,
other contraction regime, practical bit/VRAM or capability claim follows.
