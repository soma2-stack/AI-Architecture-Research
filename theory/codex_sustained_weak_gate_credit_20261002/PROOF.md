# Fixed-feature credit: sustained dissipation and very weak late tails

2026-10-02. New Codex-derived scoped results, **independent review required**.
The whole-class linear upper remains OPEN. This is a bounded theory attempt,
not a numerical experiment, theorem re-review, or new witness search.

## 1. Accepted premises and precise scope

Keep c=1, gamma=1/n, a=1-1/n, epsilon=1/1000, n>=200, the existing dense
rotating model, one public source H=(2/5)1_l, group-RMS units, and exact
endpoint h=0. Put k=floor(n/2), l=n-k, r=k-1, d=floor(n/4). No parameter,
history, query, normalization, or error tolerance is changed.

The exact selected sensitivity for the actual model is

    delta h_t = B_t K H,
    B_t = G_t(R B_(t-1) + alpha_t E),
    alpha_1=0, alpha_t=1 for t>=2, B_0=0.

K is the selected recurrent parameter block; its columns are NOT independent
history injections. G_t=diag(1-h_t^2) comes from the ACTUAL admissible coupled
tanh trajectory. Histories use inputs in (-1/2,1/2)^n, keep the source H at
interior times, and finish by resetting the actual hidden state to zero.
Parameter derivatives hold the realized inputs fixed.

The accepted reference uses the SAME realized gates:

    M_t = G_*,t(a O_* M_(t-1) + alpha_t I_r), M_0=0,
    Bbar_t = E M_t, ||M_t||op<=n,
    ||B_t-Bbar_t||op<=e n^2, e<=4/(10^8 n^2).

O_* is the orthogonal restriction of the accepted rotation to physical
memory coordinates 2,...,k. The dense-transfer ledger, valid at all horizons
and for every permitted late query, is

    eta_n = a ||H|| e n < 2*10^-9.

For any replacement Mhat of the endpoint reference credit,

    actual selected-query error
      <= eta_n + A_n ||M_T-Mhat||op,                       (1)
    A_n = a ||H||/n <= (3/10)/sqrt(n).

This follows from w_R/beta=1/n and the accepted all-query adjoint upper
||xi||<=a/beta. It is an UPPER bound for the actual query supremum, not a
replacement of that supremum by an arbitrary-adjoint or RMS contract.

Specifically, permitted losses are the scalar head q=1_n/sqrt(n), divided
by beta=max(1,||R||F), after L>=1 future steps whose preactivations all lie
in [1/4,3/4]^n. Future inputs are otherwise unrestricted. Their gates lie
in [sech^2(3/4),sech^2(1/4)]. The past input cube is NOT a future-query
restriction. Direct future parameter contributions are computed exactly
from the supplied query and common current state, and added by the decoder.
Only the inherited past credit is approximated in (1).

Accept the reviewed moving-spike decomposition, its R1 all-length bound,
the certified chart collisions, and the joint Omega(n) lower as premises.
No chart collision is promoted to a class upper. No exact accessibility or
observability theorem is redone.

## 2. Sustained dissipation in the full selected memory block

### Theorem S1: uniformly damped tail, with all fresh credit counted

Let N be the last interior time, followed by the zero reset at N+1. Suppose
the last L interior reference gates satisfy ||G_*,t||op<=u<1. Set b=a u.
Allow ANY admissible earlier history, so ||M_(N-L)||op<=n. Iterating the
inhomogeneous recurrence, with every actual source injection included, gives

    ||M_N||op <= n b^L + u sum_(j=0)^(L-1) b^j
               <= n b^L + u/(1-b).

The reset gate is I, not a damped gate. Consequently

    ||M_(N+1)||op <= a n b^L + a u/(1-b) + 1,
    error of discarding ALL selected past credit
      <= eta_n + A_n[a n b^L + a u/(1-b) + 1].             (2)

Every term is uniform over the admitted histories and all allowed futures.
It is insufficient to keep only the old-credit term n b^L; the injection
term remains even after the old history is forgotten.

For fixed u<1 and epsilon, (2) tends to zero whenever

    L |log b| - (1/2)log n -> +infinity.

If all injected interior gates have this same bound from the start, there
is no n b^L term at all. Thus, at sufficiently large n, this fully sustained
subclass needs ZERO selected-credit coordinates at its fixed endpoint.
While reading inputs, n actual forward coordinates are still counted.
For the finitely many smaller widths, storing the r^2 reference entries
gives an O_(u,epsilon)(n) upper for that subclass. The constant can be large.
This does not include an arbitrary undamped warmup followed by a short tail.

### Scope warning

S1 requires damping of EVERY selected memory direction. Damping only some
coordinates, a time-average amplitude, or a gate at one moving node does not
satisfy its hypothesis. In particular it does not kill the accepted one-pulse
lower, whose undamped warmup builds order-n credit.

## 3. Sustained latent-cycle histories: a variable-gap extension

For zero-sum latent profiles supported on the first d cycle coordinates,
the accepted exact support decomposition is

    M_t = s_t P_Z + V C_t V^T,
    s_t = g_s(t)[a s_(t-1)+alpha_t],
    C_t = G_A(t)[a O_A C_(t-1)+alpha_t I_d].                 (3)

V=[e_2,...,e_d,1_NC/sqrt(k-d)] is orthonormal. P_Z projects onto the
zero-sum NC subspace. The NC gate is one scalar for this latent-support
class. Individually varying NC gates are NOT in this class. No scalar-NC
assumption is imposed on the general model class.

Let e_A denote the uniform-NC active coordinate, F=I-e_A e_A^T, and
q=e_A^T O_A e_A. With L_NC=k-d and c_k=1/(sqrt(k)-1), the accepted rotation
gives q=1-L_NC c_k^2. One direct way to see this is to apply U to the
uniform-NC vector: its first latent cycle coordinate differs from each other
cycle coordinate by sqrt(L_NC)c_k. The cycle shift changes two entries by
that amount, so its squared displacement is 2 L_NC c_k^2, giving the formula.
Since L_NC=ceil(k/2) and k>=100, q<1/2 and
L_NC c_k^2<=(k+1)/(2(sqrt(k)-1)^2)<=101/162. The last function decreases
with sqrt(k)>=10. Thus 61/162<=q<1/2, in particular |q|<=1/2.

Take any pair of adjacent interior gates. Suppose their cycle-coordinate
gates (the F coordinates) are bounded by u_j=1-delta_j, 0<=delta_j<=1.
Their NC gates may be arbitrarily close to one. Define

    lambda_j = sqrt(1-(1-u_j^2)/(2(2-u_j)^2)),
    b_j = a^2 lambda_j.

The following two-step estimate is the existing energy argument with a
variable u; its derivation is included because the extension depends on it.
Write Gbar=u_j F+e_A e_A^T, G_i=D_i Gbar, ||D_i||op<=1. Since these
diagonal factors commute with Gbar and O_A is orthogonal,

    ||G_2 O_A G_1 O_A||op <= ||Gbar O_A Gbar||op.

For a unit vector v,

    1-||Gbar O_A Gbar v||^2
      =(1-u_j^2)(||Fv||^2+||F O_A Gbar v||^2).

Also ||Fv||^2+||F O_A v||^2>=1-|q|>=1/2. The inequality
||F O_A v||<=||F O_A Gbar v||+(1-u_j)||Fv||, together with the Euclidean
operator-norm bound 2-u_j for the resulting two-component triangular map,
gives the displayed lambda_j. No commutation of G_i with O_A is used.

### Theorem S2: time-dependent dissipation ledger

For J such pairs, starting from any ||C_start||op<=n, define

    P_J = product_(j=1)^J b_j,
    W_J = sum_(j=1)^J product_(i=j+1)^J b_i.                (4)

The empty product is one. Each pair adds at most a+1<=2 in operator norm.
After the final zero reset,

    ||C_end||op <= a[n P_J+2 W_J]+1,
    error of retaining s exactly and discarding C
      <= eta_n+A_n{a[n P_J+2 W_J]+1}.                      (5)

This is a whole-family finite-error bound with arbitrary nonperiodic gates
satisfying the specified pair envelopes. It includes fresh injection ages;
P_J alone does not bound the answer.

For small or variable gaps it is useful that

    lambda_j <= exp(-delta_j/16),
    product_(i=p)^q b_i
      <= a^(2(q-p+1)) exp[-sum_(i=p)^q delta_i/16].         (6)

Indeed (1-u^2)/(2(2-u)^2)=delta(2-delta)/(2(1+delta)^2)>=delta/8,
and sqrt(1-x)<=exp(-x/2). These safe constants require no numerical scan.

For a common delta_n>0, put b=a^2 lambda(delta_n). The identity
1-sqrt(1-x)=x/(1+sqrt(1-x))>=x/2, with x>=delta_n/8, gives
1-b>=1-lambda>=delta_n/16. Thus W_J<=16/delta_n, and (5) is at most

    eta_n + (3/10)[sqrt(n) b^J
                   +(32/delta_n+1)/sqrt(n)].             (7)

In particular, if delta_n sqrt(n)->infinity and
J |log b|-(1/2)log n->infinity, the active query error tends to zero.
One scalar s suffices at the endpoint once (5) is below epsilon; n forward
coordinates are counted while streaming. Every jointly robust section of
dimension greater than one then has an antipodal collision through that
continuous scalar encoder, by the accepted topological error argument.

This extends the prior fixed-amplitude/even-d chart lemma to every admitted
latent-cycle history satisfying the pair bounds, including changing gaps.
It does NOT establish the whole-class O(n) result. At gaps of order 1/n,
the fresh-credit bound in (7) is of order sqrt(n) in query units and useless.
An overlarge upper bound is not evidence of a robust lower.

## 4. Very weak long tails: large fresh credit can become public

This next theorem applies to the GENERAL selected reference recurrence, not
only the latent-cycle invariant support. It does not use convex transport
averaging, basis renewal, or a numerical spectrum.

Define the PUBLIC resolvent

    M_infinity = (I_r-a O_*)^(-1).

It exists because ||a O_*||op=a<1, satisfies
M_infinity=a O_* M_infinity+I_r, and ||M_infinity||op<=n. It need not be
the endpoint of a finite actual history; it is an approximation target.
All its entries depend only on public frozen model constants, not history.

### Theorem W1: finite-error nearly ungated tail

Suppose the last L steps before the endpoint (including the reset if present)
have alpha_t=1 and ||I_r-G_*,t||op<=delta. Assume T-L>=1 so the first
zero-feature step is outside this tail. Set E_t=M_t-M_infinity. EXACTLY,

    E_t = G_*,t a O_* E_(t-1)+(G_*,t-I_r)M_infinity.

Therefore, allowing arbitrary admissible pre-tail histories,

    ||M_T-M_infinity||op <= 2n a^L+delta n^2,
    error using the public M_infinity alone
      <= eta_n+A_n[2n a^L+delta n^2].                     (8)

The initial 2n counts both true and reference credit. Each fresh discrepancy
is at most delta n, and its geometric sum is at most delta n^2. This controls
all finite gate-history variations satisfying the envelope, not just a
tangent perturbation. No source column or past gate is independently selected.

Let epsilon'=epsilon-eta_n>0. The sufficient conditions

    L >= ceil(n log(4 A_n n/epsilon')),
    delta <= epsilon'/(2 A_n n^2)                         (9)

make the right side of (8) at most epsilon. They use a^L<=exp(-L/n).
The gate-defect scale in (9) is order epsilon n^(-3/2), NOT order 1/n.

The encoder stores zero selected-credit coordinates, plus actual h (n
coordinates) during input processing. At the fixed endpoint even h is supplied
as zero. No age counter, gate history, replay, or history-dependent public
constant is hidden. A decoder applies the inherited approximation to the
ACTUAL future adjoint and adds exact common future injections. Transient
decoder computation is not bounded by this history-memory theorem.

### Corollary W2: all sufficiently late harmonic weakening histories

Suppose every realized selected memory gate obeys

    ||I_r-G_*,t||op <= K/t,                                (10)

with public K independent of n and horizon. Gates may be non-scalar and
arbitrarily aperiodic inside this envelope. At T>=3 choose L=floor(T/2).
Every tail t>T-L has defect at most 2K/T, including the reset, whose defect
is zero. Consequently

    error <= eta_n +(3/5)sqrt(n) exp[-floor(T/2)/n]
                         +(3/5)K n^(3/2)/T.              (11)

For example the following integer-safe sufficient horizon works:

    T >= max(3,
             ceil(2+2n log((6/5)sqrt(n)/epsilon')),
             ceil((6/5)K n^(3/2)/epsilon')).             (12)

The exponential and fresh-credit terms then each use at most epsilon'/2.
The bound is uniform over the entire admitted family for all such T. The
zero-credit encoder is continuous and covers every allowed future query.

Fresh credit can have norm of order n here: M_infinity does on the eigenvalue-1
subspace of O_*. That large component is public, not independently encoded
history. Thus 'fresh credit accumulates' alone does NOT create a robust
dimension lower. Nor is the total dissipation sum over the entire past the
right criterion: (8) depends on the RECENT tail and retains its injection cost.

W2 does not bound the same class at earlier horizons, does not cover every
possible rate of weakening, and does not solve arbitrary aperiodic gates.
It is conditional on REALIZED coupled histories satisfying (10), not an
assertion that arbitrary gate arrays can be realized by the tanh/input system.

## 5. Why the class theorem still does not follow

The two rigorous sufficient tests (5) and (8) constrain opposite sides:

* Sustained active loss: repeated damping must kill old credit AND keep the
  sum of fresh transports small enough in query units.
* Extremely weak late loss: the history-dependent perturbation of the public
  ungated resolvent must be small enough, although the credit itself is large.

Each encoder is for its separately stated, publicly specified class promise.
No free history-dependent selector between these encoders is assumed, and no
continuous small-memory encoder for their unrestricted union is constructed.

They leave an intermediate regime. Pair gaps of order 1/n, or tail defects
of order 1/n through a relevant order-n-log-n window, satisfy neither useful
bound in general. No implication in the converse direction is claimed.
Even harmonic weakening around T=order(n log n) is outside W2's sufficient
order(n^(3/2)/epsilon) scale. Arbitrary nonuniform NC gates add another
uncovered part of the full fixed-feature class.

R1 remains a legal all-length QUERY upper, but its remainder is multiplied
by the reachable credit residual. Without a CREDIT-side uniform estimate,
short spike-row retention does not bound that residual. One-step gate queries
still separate all operator entries, with a width-dependent weak margin;
no exact query-invisible quotient of dimension O(n) has appeared.

Likewise, source-weighted adjoint dissipation is a per-query energy budget.
It does not bound the number of jointly robust innovations when fresh credit
and gates vary together. Summing maxima over different queries loses the
information needed here. No conservation law that supplies the desired
uniform continuous dimension cap was found.

The smallest remaining obstruction is the jointly varying, noncommuting
M_t=G_*,t(a O_* M_(t-1)+I_r) in this intermediate regime: prove a continuous
O(n)-coordinate, finite-error summary (or a whole-class width upper that
implies one), OR exhibit a single admissible finite-radius same-h section of
dimension omega(n) with every antipodal query half-margin>epsilon.
All combinations must remain admissible. The known sustained-chart collisions
do not supply this quantifier. Individually visible axes or tangent ranks do
not supply the alternative lower.

## 6. Final bounds and consequences

At unchanged c=1 and epsilon=1e-3:

    Omega(n) <= whole-class fixed-feature dimension <= (floor(n/2)-1)^2.

The lower is accepted, not re-proved. The upper is the accepted counted
reference M encoder with uniform dense error eta_n. General Theta(n) is NOT
proved and is NOT refuted. S1/S2/W1/W2 only close their stated subclasses.
No superlinear jointly robust construction was found in this theory attempt.

The complete-model gap remains Omega_c(n^2) to O_c(n^2 log n). Even a later
one-feature O(n) theorem needs compatible, counted simultaneous feature
encoders to close that gap; incompatible sections cannot be multiplied.
No architecture, training, finite-bit/VRAM, other contraction regime, or
practical-performance result follows. Stop at this stage.
