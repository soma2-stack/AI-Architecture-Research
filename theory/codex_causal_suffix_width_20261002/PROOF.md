# Continuous causal suffix width: partial results, not a linear encoder

2026-10-02. New Codex derivations; independent review required.

**The Cn finite-error realization is neither constructed nor robustly refuted.**
This file proves uniform prefix-error and continuous approximation lemmas.
It does not infer robust dimension from exact rank, monomial count, or an
inaccessible operator ball. No experiment, new witness or architecture is used.

## 1. Verified process and fixed error contract

Use the definitions and owner-verified results from
`theory/codex_online_gate_polynomial_20261002/` and the new Grok review.
No accepted theorem is re-audited. Keep n>=200, c=1, gamma=1/n,
epsilon=1/1000, the same dense R/W/b_model, source H=.4*1_l, normalization,
admissible input lift and common final endpoint h=0.

Let k=floor(n/2), r=k-1, a=1-1/n, and O_* be the fixed accepted orthogonal
memory transport. The local gate window has N=ceil(4n log n)+1 steps,

    z_t in [1/20,1/4]^r,
    g0=1-(3/20)/n,
    D_t=diag(3/20-z_t), ||D_t||op<=Delta=1/10,
    G_t=g0 I+D_t/n, b=a g0.

Preparation/reset exceptions and the tied source injection remain unchanged.
Degree zero and the following forcing are public:

    M_t^(0)=bO_* M_(t-1)^(0)+g0 I,
    Q_t=aO_* M_(t-1)^(0)+I,
    Z_(1,t)=bO_* Z_(1,t-1)+(D_t/n)Q_t,
    Z_(j,t)=bO_* Z_(j,t-1)+(aD_t/n)O_*Z_(j-1,t-1), j>=2. (1)

All mixed states start at zero; p=p_n is the frozen public truncation degree.
Define

    u_n=a Delta/n,
    q_n=u_n/(1-b)=a Delta/(1+a(3/20))<1/11,
    C_n=Delta/[n(1-b)^2],
    B_n=C_n/(1-q_n),
    b_max=b+u_n=a(1-1/(20n))<1,
    A_n=a||H||/n<=.3/sqrt(n),
    tau_n=A_n a C_n q_n^p/(1-q_n)<=epsilon/4.             (2)

The final inequality is part of the verified frozen ledger, not a new choice
of p or epsilon. In fact q_n<1/11 follows directly from
q_n=2a/(20+3a) and 19a<20. Keep the ACTUAL query norm

    nu_n(Y)=w_R||H|| sup_(Q legal)||Y^T E^T xi_Q||_2,
    nu_n(Y)<=A_n||Y||op.                                 (3)

Only the latter upper envelope is used for safe estimates. No arbitrary
adjoint, RMS query average or Frobenius error replaces the supremum.
The decoder adds public degree zero, reset and direct future contributions.

The homogeneous triangular transition T_p(D) is (1) with forcing removed.
For L=N-t remaining interior steps,

    d_t(Z,Z')=sup_(w admitted, length L)
        nu_n(aO_* sum_(j=1)^p [T_w(Z-Z')]_j).             (4)

Its sharp common-update Lipschitz constant 1 is an accepted premise.
The norm extends to ambient decoded jets, which need not themselves be
reachable. A decoded jet is an approximate response representation, not a
claim of an additional admissible history.

## 2. What permanent merging actually proves

Suppose a set of prefixes has pairwise d_t distance <=2delta at a common cut.
Every common admitted continuation transports that set to one whose pairwise
distance is still <=2delta. This follows by iterating nonexpansiveness.
The old discrepancy cannot later amplify in this metric, so later common
updates do not require recovering it to prevent amplification.

That statement does not provide a continuous code for all such sets, a
continuous choice of representatives, or a small update-closed quotient.
Fresh forcing in (1) still introduces new history dependence. With repeated
approximation defects delta_s, the generic proven ledger remains

    error at time t <=sum_(s<=t)delta_s.                  (5)

Sharp nonexpansiveness alone cannot replace this sum by max_s delta_s.
This is a limit of the ledger, not a lower against all encoders: an encoder
with an invariant error relation can avoid accumulating defects.

Here is an exact sufficient condition for that avoidance. Let P_t be
continuous representative maps, with explicit k-coordinate ranges and
continuous coordinate read/write maps. Assume, on reachable states and the
representative states used by the updates,

    d_t(Z,P_t Z)<=delta,
    P_(t+1) Phi_(t+1)(D) P_t Z
                  =P_(t+1) Phi_(t+1)(D) Z              (6)

for every admitted next gate. Phi includes public forcing. Start at P_0(0).
Updating the representative by P_(t+1)Phi_(t+1)(D) gives exactly P_t Z_t by
induction. Error is <=delta at EVERY time, rather than a sum of projection
errors. Continuous encoding and causal closure both follow from (6).

A dimensional label on range P_t is not itself an implementation count;
its explicit coordinate system and all adaptive factors must fit in k.
Condition (6) is sufficient, not necessary for a general approximate causal
realization. No k=Cn maps with these properties are found here.

## 3. A genuine closed degree projection -- with the wrong memory scale

Let pi_m retain degrees 1,...,m and set higher degrees to zero. Triangularity
gives exactly

    pi_m Phi(D) pi_m=pi_m Phi(D).                         (7)

Thus the first m coefficient matrices form a continuous closed online state;
they are not merely an offline fit. The decoded jet appends zeros.

For a mixed-state difference, the sum of operator norms contracts by b_max:

    sum_j ||[T_p(D)Z]_j||op<=b_max sum_j||Z_j||op.        (8)

The verified coefficient envelope ||Z_j||op<=C_n q_n^(j-1) therefore gives

    d_t(Z,pi_m Z)
      <=A_n a b_max^(N-t) C_n q_n^m/(1-q_n).            (9)

This is a one-shot ALL-suffix bound. It includes all mixed directions and
all actual permitted queries; no favorable query is substituted.

For target delta=3epsilon/4 choose the public integer

    m_n=min(p,max(0,ceil(log_+(A_n a B_n/delta)
                                            /log(1/q_n)))), (10)

where log_+(x)=max(0,log x). The inequality at m=p follows from (2), so
the cap in (10) is safe. Equations (7)--(9) prove an exact state-factor causal
encoder with m_n r^2 credit coordinates and uniform d_t error <=delta.
This is a storage count, not a lower bound. At fixed epsilon the sufficient
m_n is Theta(log n), so this implementation is O(n^2 log n), worse than
the accepted auxiliary reference state.

For a single current time, the factor b_max^(N-t) can make fewer degrees
sufficient. However the resulting degree requirement increases towards the
terminal time. An encoder cannot recover previously discarded coefficients
for free when increasing m. Equation (7) does not justify that recovery.
The following one public reset avoids needing it for the erased prefix.

## 4. An explicit public interval on which every mixed prefix is negligible

Set delta0=epsilon/8 and define, from public constants only,

    ell_n=ceil(log_+(A_n a B_n/delta0)/(-log b_max)),
    t0=max(0,N-ell_n).                                   (11)

When ell_n<=N, for every t<=t0 and EVERY admitted prefix,

    d_t(Z_t,0)<=A_n a b_max^(N-t) B_n<=delta0.            (12)

If ell_n>N then t0=0 and the initial state is exactly zero, so the same
erasure at the cut is trivial. If ell_n=0, (12) applies throughout.

Proof: sum_(j=1)^p||Z_(j,t)||op<=B_n by the verified envelope, then use
(8) across every admitted remaining word and (3). All old and fresh mixed
credit ALREADY PRESENT at time t is included in this bound. Future fresh
forcing is shared by the compared histories and cancels in the difference.

Define a shadow polynomial history with D=0 at times <=t0 and the actual
D at every later time. Its degree zero is the same public degree zero.
At the cut Z_shadow=0 and the actual-shadow distance is <=delta0. With
common admitted later updates,

    d_t(Z_actual,t,Z_shadow,t)<=delta0 for every t>=t0.   (13)

Every shadow word is inside the original cube. The admissible tanh lift and
final h=0 are unchanged. This is one permanent merge, not repeated free
projection and not a new witness search. Current actual forward h, if inputs
rather than gates are processed, is retained separately and counted.

The comparison uses common gate symbols, exactly as in (4). At the cut the
actual and shadow forward states can differ. It does NOT assert that their
inverse-lift raw input suffixes are identical; both histories are admissible
and reset to the required common endpoint. The actual forward state is not
replaced by the shadow forward state in an input-processing implementation.

For perspective, B_n=Theta(n), A_n=Theta(n^(-1/2)), and
-log b_max=(21/20)/n+O(n^(-2)). Hence, at fixed epsilon,

    ell_n=(10/21)n log n+O_epsilon(n).                   (14)

This shortens the part of the fixed N-window that must introduce fresh mixed
history dependence, but it still leaves a Theta(n log n) late segment.
Its length is not a persistent-coordinate lower. No O(n) storage follows.

## 5. Decode one reference matrix into a jet with uniform d_t error

This lemma strengthens the verified terminal-query reference upper to a
specific decoded STATE bound at every prefix. The extra proof is necessary:
matching a current summed matrix alone need not match every remaining suffix.

For a genuine admitted prefix let

    M_t=G_t(aO_* M_(t-1)+I), M_0=0,
    F_t=M_t-M_t^(0),
    Psi_t(M_t)=(F_t,0,...,0) in the degree-p mixed space.  (15)

F_t is the sum of ALL chronological mixed orders of that prefix, not just p.
Psi is a linear/affine decoder in the stored matrix; it does not need history.
Claim:

    d_t(Z_t,Psi_t(M_t))<=K_n tau_n,
    K_n=1+1/(1-q_n)<21/10,                              (16)

uniformly over every time, admitted prefix, remaining word and legal query.

### 5.1 Homogeneous continuation of the real prefix coefficients

Use the full coefficient hierarchy only as a proof device. It is finite for
each finite history and is NOT stored by the proposed encoder. At time t its
order-j coefficients obey ||Z_j||op<=C_n q_n^(j-1), including j>p.
After time t suppress new order-1 forcing: it is common in the comparison
and cancels. The remaining homogeneous hierarchy keeps this envelope.
For j>=2 its one-step upper is

    b C_n q_n^(j-1)+u_n C_n q_n^(j-2)
         =C_n q_n^(j-1)[b+u_n/q_n]
         =C_n q_n^(j-1),                                (17)

because u_n/q_n=1-b. Degree 1 shrinks by b.
Thus the real prefix carrier's discarded endpoint orders above p have total
operator norm <=C_n q_n^p/(1-q_n), under every remaining word.

### 5.2 Homogeneous continuation of the degree-one lift

The lift starts with lambda F_t in the formal generating variable. Its
untruncated carrier at lambda=1 equals the real carrier, because both start
with total matrix F_t and use the same G_s aO_* products. Their PUBLIC and
newly forced pieces are identical, so only these carriers need comparison.

For L remaining steps, a term with h degree increments has at most
binom(L,h) chronological placements and norm at most

    ||F_t||op binom(L,h) b^(L-h) u_n^h.

It is irrelevant whether the products commute. Each scalar factor satisfies

    binom(L,h)b^(L-h)u_n^h
      =q_n^h [binom(L,h)b^(L-h)(1-b)^h]<=q_n^h,          (18)

because the bracket is a binomial probability and is <=1. For h>L the term
is zero. The lift has initial degree 1, so discarded orders above p have
h>=p. Also ||F_t||op<=B_n. Their total norm is consequently at most

    B_n q_n^p/(1-q_n)=C_n q_n^p/(1-q_n)^2.              (19)

The untruncated carriers agree exactly at lambda=1. Therefore the DIFFERENCE
of their retained carriers is the difference of their discarded tails, and
is bounded by the sum of the bounds in 5.1 and (19). Multiplication by the
reset aO_* and the actual query upper (3) proves (16).

Crucially no future fresh-tail error is added: future forcing is identical
for the two mixed jets and cancels in d_t. This cancellation is needed for
the constant K_n, and does not discard any actual source injection.

Since q_n<1/11, K_n<1+11/10=21/10. Thus one reference matrix with decoder
Psi has uniform d_t error <21epsilon/40. This is NOT a linear-coordinate
encoder: its credit store has r^2 entries.

## 6. A continuous quadratic online implementation with one permanent merge

Here is an explicit counted online implementation; it receives each gate D
once and never replays it. Before t0 keep no history-dependent credit.
At the cut initialize Y_(t0)=M_(t0)^(0), computed publicly. Later update

    Y_t=(g0 I+D_t/n)(aO_*Y_(t-1)+I), t>t0.              (20)

Y_t is exactly the reference M of the shadow word in section4. Decode at
every time by Psi_t(Y_t); before the cut Y_t=M_t^(0) is public and this
decode is zero. After the cut combine (13) with (16):

    d_t(Z_actual,t,Psi_t(Y_t))
      <=delta0+K_n tau_n
      <epsilon/8+21epsilon/40
       =13epsilon/20 <3epsilon/4.                       (21)

Before the cut the sharper error is <=epsilon/8. The final polynomial-to-
actual ledger costs an additional at most epsilon/4, so (21) is also within
epsilon for the selected actual gradient contract. No full-model encoder
for other features/parameter blocks is implied.

Count: r^2 credit coordinates after the cut, zero history-dependent credit
before it, plus n actual forward h coordinates while processing raw inputs.
The schedule/clock is public under the accepted convention; a fully autonomous
implementation without that public index adds ONE clock coordinate. Model
weights, public M0/Q_t, arithmetic workspace and final output storage are not
counted as history-dependent state. Y and any replacement adaptive factors
ARE counted. Continuity holds in all gate inputs and state updates; the
public discrete change of epoch does not depend on the history.

This is a stronger explicit error theorem for the known quadratic reference
representation. It is not outcome A of the owner's Cn target.

**State-factorization caveat.** An ordinary causal implementation may carry
a counted auxiliary statistic like Y. The algorithm above is continuous in
the admitted prefix and is causal. Y uses the untruncated reference recursion,
whereas the finite jet retains only p orders. No identity Y_t=f_t(Z_t), nor
the exact update compatibility required of such an identity, is proved here.
This is NOT a proof that factorization is impossible for this family.
Section3 gives a literal finite-jet state-factor encoder with its larger
m_n r^2 implementation count. These notions must not be silently identified
when formalizing the one remaining width; the accepted ordinary reference
memory upper bound remains valid.

## 7. Offline continuous approximation does not solve causal closure

There is even a continuous OFFLINE r^2-coordinate approximation of the finite
jet set R_t={Z_t(v): v an admitted prefix}, so lack of a continuous selection
of reference M alone need not be an offline obstacle.

Let sigma=epsilon/16. Compactness of R_t and continuity of d_t give a finite
sigma/2-cover by centers Z_i. For each fixed center choose one admitted
prefix and its M_i. Define

    f_i(Z)=max(0,sigma-d_t(Z,Z_i)),
    psi_i(Z)=f_i(Z)/sum_l f_l(Z),
    e_t^off(Z)=sum_i psi_i(Z) M_i,
    P_t^off(Z)=Psi_t(e_t^off(Z)).                         (22)

The denominator is positive everywhere on R_t. These maps are continuous.
Psi_t is affine and sum_i psi_i=1, so convexity of the seminorm implies

    d_t(Z,P_t^off(Z))<=sigma+K_n tau_n
                       <47epsilon/80<3epsilon/4.        (23)

This is an abstract finite-atlas existence statement, not a computed cover
or witness search. It stores r^2 output coordinates, not all cover weights.
It gives no computational-resource guarantee and no linear-memory result.

Most importantly, (22) requires the exact current Z to evaluate the weights;
that array is not free to an online encoder. No update using only e_t^off
and the next D is derived, and the absorption identity (6) is not established.
A finite epsilon-net alone, or this continuous interpolation of a net, does
not supply the requested causal encoder. The candidate may be an offline
projection without an update-compatible observable quotient.

## 8. Robust lower unchanged

Use the already-verified one joint floor(n/8)-dimensional section, not the
discardable exact-realization family. It has the same final hidden state,
whole-section admissibility, finite physical radius and polynomial antipodal
half-margin >.00149>5epsilon/4. At t=N the suffix metric is just the permitted
query norm. If a continuous encoder had fewer than floor(n/8) coordinates,
the accepted antipodal dimension principle would force equal encodings on
some boundary antipodes. A decoder with error <=3epsilon/4 would give their
distance <=3epsilon/2=.0015, contradicting the verified distance >.00298.

Therefore floor(n/8) remains a robust coordinate lower. Nothing here constructs
an omega(n) jointly visible section. The early erasure theorem does not rule
out a later one; the exact polynomial-order lower is not used to refute one.

## 9. Algebra and representation attempts within this one problem

The forcing D_t Q_t and every subsequent left D_t O_* multiplication remain
tied to the same diagonal word. A public template generated only by O_*
does not close arbitrary such forcing. Shared column factors, low displacement
rank, balanced coordinates or dynamically selected row spaces would need
both a uniform d_t approximation and a counted continuous online update.
No such Cn representation is derived here. This is not an algebraic-size
impossibility theorem.

The concrete proved closures are the degree projection (7) and the auxiliary
reference update (20). The former has too many coordinates in the explicit
implementation; the latter has too many coordinates even though its decoder
has enough error slack. Neither coordinate count lower-bounds every alternative.
Time-dependent safe erasure (11)--(13) removes old dependence, but leaves fresh
post-cut mixed credit. No raw matrix dimension, SVD, tangent count, Frobenius
rank, inaccessible operator ball, sustained chart or other gate regime is used.

## 10. One precise remaining quantity: causal suffix width

Here is a literal formalization of the requested E_t on reachable finite-jet
states. It adds no regularity requirement on the decoder beyond the owner's
contract. Let R_t be the image of the admitted length-t gate cube under (1).
For delta=3epsilon/4, define W_delta^causal(n) as the smallest integer K for
which, simultaneously at all t=0,...,N, there exist

    e_t : R_t -> R^K, continuous,
    U_(t+1) : R^K x admitted diagonal cube -> R^K, continuous,
    rho_t : R^K -> ambient degree-p jets,

with the public initial code and the two identities/inequalities

    e_(t+1)(Phi_(t+1)(D) Z)=U_(t+1)(e_t(Z),D),
    d_t(Z,rho_t(e_t(Z)))<=delta                          (24)

for EVERY reachable Z, admitted D and time t. All history-dependent basis,
factor and auxiliary coordinates count toward K. Public constants and schedule
do not. The range is padded to K if a public epoch uses fewer coordinates.
Forward h costs another n if raw inputs rather than D are supplied.

This is an UPDATE-COMPATIBLE approximate realization width, not ordinary
offline Kolmogorov width, tangent dimension, a number of net points or a
monomial count. The metric itself accounts for every admitted remaining word
and every legal future query, including the actual worst-query supremum.

The rigorously available literal bounds are

    floor(n/8) <= W_(3epsilon/4)^causal(n) <= m_n r^2,    (25)

by section8 and the closed degree realization in section3. The upper count
is only that implementation; it is not asserted optimal. In the accepted
ordinary memory model that allows another counted continuous prefix
statistic, section6 instead gives the stronger r^2-coordinate upper with
error <13epsilon/20. Section7 even gives a pure finite-jet OFFLINE r^2
approximation. Neither fact alone establishes the exact update identity in
(24) for a pure r^2-valued finite-jet encoder.

The owner was asked explicitly which encoding convention is intended; no
unanswered clarification is treated as approval. The results above cover
the literal state-factor version and preserve the verified reference upper
in the ordinary counted-statistic version. Neither interpretation has a Cn
encoder or an omega(n) robust refutation here. This is a formalization
distinction inside the same recurrence, not a new research regime.

**The single remaining theorem is whether W_(3epsilon/4)^causal(n)=O(n).**
An explicit continuously coordinatized range satisfying (6) would suffice.
A valid refutation may use one admitted same-endpoint joint section of
dimension omega(n) with the owner's buffered polynomial antipodal half-margin
>5epsilon/4; the exact-only small prefix cannot serve this purpose. A proof
of a larger coordinate count for a particular factorization is not enough.

Fixed-feature Theta(n) is not established or refuted. The accepted ordinary
fixed-feature Omega(n)--O(n^2) and full-model
Omega_c(n^2)--O_c(n^2 log n) bounds remain unchanged. Simultaneous source
features would still need compatible counted summaries even if the one-feature
linear target were subsequently solved. Stop at this obstruction; no other
regime, new witness, numerical sweep or architecture stage follows.
