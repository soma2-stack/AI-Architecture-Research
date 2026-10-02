# Aperiodic credit aggregation: finite gate events and a visible-credit obstruction

2026-10-01. Theory only. New author-derived lemmas require independent review.
The accepted rotating-gate results are premises; their proof is not redone.

## 1. Status and unchanged computational contract

The general arbitrary-aperiodic problem remains OPEN:

    Omega_c(n^2) <= d_rob(n,1e-3) <= O_c(n^2 log n), gamma=c/n.

This note does NOT prove a universal quadratic encoder or a logarithmic
memory lower bound. It proves two narrower facts:

1. A fixed number b of non-scalar memory-gate events at public declared
   times, with arbitrary scalar gating between them, admits an arbitrary-
   horizon O_b(n^2) continuous encoder on the SAME hard rotating family.
   Gates at the exceptional times need not commute or recur periodically.
2. On that same family, replacing even ONE non-scalar memory gate by its
   mean scalar can lose more than epsilon in an actual permitted normalized
   future gradient. This remains true when the new injection is supplied
   exactly. Query-visible old-credit gain can be Omega_c(n), not O_c(1).
   Thus a width-independent old-credit estimate cannot be inserted into
   the previous gate-defect proof solely on account of query normalization.

The second is an obstruction to an estimate/aggregation shortcut, NOT to
all quadratic encoders. The first explicitly compresses its history class.

Keep the actual predictor and all independently differentiated parameters:

    h_t=tanh(R h_(t-1)+W x_t+b), h0=S0=0,
    theta=(R,W,b), P=2n^2+n, S_t=D_theta h_t,
    Z_t=S_t D_theta.

Realized inputs are held fixed when differentiating. Frozen group-RMS
weights are w_R=||R||F/n, w_W=||W||F/n, w_b=RMS(b). The future head is
q=1/sqrt(n)*1 divided by beta=max(1,||R||F). For large widths here
beta=||R||F, so w_R/beta=1/n EXACTLY. The allowed input cube remains
(-1/2,1/2)^n and epsilon remains 1/1000.

Current h is either supplied or costs n additional coordinates. The memory
model is continuous finite-dimensional exact-real state, causal updates,
no uncounted tape/replay, public fixed model constants, unrestricted decoder
work. All future direct parameter injections are computed exactly using
the actual current state and continuation. Only past sensitivity is encoded.
No finite-precision, bits, runtime, learning or architecture claim follows.

## 2. Accepted rotating family and transfer premise

Use the accepted family without reselecting its parameters:

    a=1-c/n, k=floor(n/2), l=n-k,
    L=max(1,ceil c), d=min(k,floor(n/(4cL))),
    delta=1/(100n), R0=diag(a O,delta I_l),
    O=U(P_d direct_sum I_(k-d))U^T, O^d=I_k,
    W=I, b=(1/20)*1.

The accepted n0(c) is ceil(max(64,8cL,200 sqrt(cL),2c)).

U is the accepted Householder matrix. The actual fully dense R satisfies

    ||R||op=a, ||R-R0||op=e<=4/(10^8 n^2),

with no zero entries in R or R^-1. Nothing is tied when differentiating.
Let G_t=diag(1-h_t^2) on the ACTUAL forward trajectory and

    F_t phi=w_R phi_R h_(t-1)+w_W phi_W x_t+w_b phi_b.

The accepted transfer lemma, applied with actual features and gates, gives

    Zbar_t=G_t R0 Zbar_(t-1)+G_t F_t,
    ||Z_t-Zbar_t||op<=e C/gamma^2, C<6/5.

For every permitted future continuation ||c_q||<=a/beta<=2/sqrt(k), hence
the actual gradient error from this surrogate is at most

    kappa_Q e C/gamma^2 <=48/(5*10^8 c^2 sqrt(k)).       (1)

At fixed c and sufficiently large n this is less than epsilon uniformly
in history length. The surrogate does not replace the actual forward model.

## 3. Theorem: finitely many aperiodic gate events use quadratic state

Fix b>=0 independent of n and horizon. Declare a public finite schedule
t_1<...<t_b BEFORE the history. At each such time, the actual memory gate
D_t=G_mem,t may be an arbitrary diagonal gate. At all other times assume

    G_mem,t=g_t I_k.

The common scalar g_t may vary arbitrarily. Source gates are unrestricted.
The exceptional times need not be equally spaced, periodic, or repeated.
This is a RESTRICTED history class. The schedule is an encoder clock rule,
not a phase/task input to the predictor. We do not claim that a continuous
encoder can detect arbitrary history-dependent exceptional times for free.

### 3.1 Active scalar-segment moments

Use the accepted scalar-gate moment lemma as a building block. An active
segment has d slots f_j^R,f_j^W in R^n and f_j^b in R, j=0,...,d-1, and
represents

    M_active phi=sum_j O^j [w_R phi_R,mem f_j^R
                         +w_W phi_W,mem f_j^W
                         +w_b phi_b,mem f_j^b].        (2)

At a nonexceptional step, cyclically shift the slots, multiply by a g_t,
and add at slot 0 the vectors g_t h_(t-1), g_t x_t and scalar g_t.
This is exact because O^d=I. Empty active segments start at zero.

### 3.2 Completed segments and exceptional injections

A completed segment s stores its frozen moments and a history-dependent
k by k transport matrix Q_s. Its contribution is Q_s M_s phi.

An exceptional injection e stores ONE feature tuple

    v_e=(h_(t_e-1),x_(t_e),1),

of size 2n+1 and a k by k transport matrix Q_e. Its contribution is

    Q_e [w_R phi_R,mem h_(t_e-1)
        +w_W phi_W,mem x_(t_e)+w_b phi_b,mem].          (3)

At each new transition, multiply EVERY already stored Q on the left by
the actual surrogate memory propagation A_t=G_mem,t a O. At an exceptional
time:

* freeze the current active segment and attach Q_s=D_t a O;
* attach the new injection tuple with Q_e=D_t;
* start a fresh zero active segment.

At ordinary scalar steps, update the active moments using (2). The completed
segment/injection transports receive A_t as above. This inductively represents
the full memory action as the sum of the active term (2), all Q_s M_s terms,
and all (3) terms. It keeps the actual order of noncommuting matrices. No
discarded gate or input is reconstructed from a hidden history tape.

The l source states retain their own 2n+1 eligibility entries, as in the
accepted scalar theorem. Their gates and feature coordinates remain actual.

### 3.3 Complete coordinate count, continuity and scope

Preallocate at most b completed scalar segments, one active segment, and
b exceptional injections. Count ALL transport matrices, not only features:

    [(b+1)d+l](2n+1) + 2b k^2 + b(2n+1) + 1           (4)

persistent credit/buffer coordinates suffice. The last coordinate can store
the public clock. Add n for actual h if it is not supplied. Decoder output
and workspace may be dense but are transient, not persistent uncounted state.
Model powers O^j are public; every Q is history-dependent and counted.

The clock determines scheduled transitions independently of input values.
For fixed times each state update is linear/polynomial in the continuous
features/gates; scalar g can be read from the first memory coordinate's gate.
These formulas extend continuously off the restricted history class without
an equality/membership test. Accuracy off that class is NOT promised.

Equation (4) is O_b(n^2) when b is fixed. It is uniform over arbitrary
lengths, including arbitrarily long gaps between exceptional events. Combining
the exact surrogate representation with (1) answers every permitted actual
late query within epsilon for fixed c and large n. Query adjoints are actual;
future gates need not obey the past restriction.

This is not a computationally cheap-update theorem: multiplying all Q matrices
may be expensive, and real-arithmetic conditioning is not certified. It is
a counted continuous-state theorem. If b grows like log n, (4) grows like
n^2 log n. That is an UPPER for this representation, not a lower for any
encoder. Arbitrarily many non-scalar events are not covered quadratically.

The accepted Omega_c(n^2) section, with memory gates I, lies in this class.
Therefore the class has arbitrary-horizon Theta_(c,b)(n^2) worst-case credit
memory, for fixed b, under the accepted lower theorem. In particular,
aperiodicity by itself is not a logarithmic-memory obstruction.

## 4. Counterexample to suppressing non-scalar damage by query normalization

This is an analytic history on the SAME family, not a numerical search.
Take fixed c>=1 and

    n>=max(n0(c),200c,200), N=ceil(n/c), sigma=2/5,
    tau=sigma^2=4/25, H=sigma*1_l.

Let Pi be the orthogonal projector onto the stationary space ker(I-O);
equivalently Pi=(1/d)sum_(j=0)^(d-1)O^j. Its rank is

    r0=k-d+1 >= k/2+1,

because d<=floor(n/4) for c>=1. Here d>=2 by n>=n0(c)>=8cL.
Use the explicit index i=k>d and L_i=E_ii-I_k/k. This choice avoids
the exactly stationary coordinate e1, and is not seed/outcome selection.

For w=e1-1/sqrt(k)*1 and the accepted Householder U, the first d entries
of U e_k equal alpha times the first d entries of w, where

    alpha=1/[sqrt(k)(1-1/sqrt(k))].

Subtracting their common mean leaves alpha*(e1-1/d*1_d). Therefore

    1-Pi_kk=alpha^2(1-1/d)
       <=1/[k(1-1/sqrt(k))^2] <=1/81 <1/50,
    Pi_kk>49/50.

Also

    ||L_i Pi||F^2=(1-2/k)Pi_kk+r0/k^2>(49/50)^2,
    ||L_i Pi||F>49/50>7/10.                           (5)

The nonstationary component is nonzero because d>=2. Since Pi_kk>0,
e_k is neither a +1 nor a -1 eigenvector of O. A rank-one coordinate
projection commutes with a real orthogonal O only if its line is invariant,
which would make e_k a +/-1 eigenvector. Thus [E_kk,O]!=0: the reference
pulse genuinely does not commute with the rotation. Its large surviving
stationary component supplies the old-credit gain; this is not a claim
that the pulse introduces a new high-dimensional independent section.

Prescribe the hidden history:

    h_t=(0_k,H), t=1,...,N+1,
    h_(N+2)=(sigma e_i,H),
    h_(N+3)=0.

Its memory gates are I except for the pulse

    D=I_k-tau E_ii, at t=N+2.

This finite isolated pulse is not a recurring periodic pattern. Endpoint
h_T=0 holds EXACTLY at T=N+3. Source gates are retained as generated, not
replaced by one. Use the actual fixed-h compensation

    x_t=atanh(h_t)-R h_(t-1)-b.                         (6)

At R0, source inputs have magnitude at most atanh(.4)+delta*.4+.05<.477.
The pulse memory inputs have magnitude at most atanh(.4)+.05<.477; the
reset has magnitude at most a*.4+.05<=.45. Other memory inputs equal -.05.
The dense correction is <=e*.4*sqrt(l+1), leaving strict input-cube slack.
The trajectory is therefore admissible in the original domain. Parameter
derivatives hold every realized x_t fixed; differentiating (6) would be wrong.

### 4.1 A deliberately favorable scalarized comparison

Replace only the pulse's MEMORY PROPAGATOR by its mean scalar:

    g=1-tau/k, D a O -> g a O.

Keep the injection D F_(N+2) EXACT, as well as all other injections, features
and gates. Thus no missing new injection can explain the comparison error.
This is a sensitivity surrogate used to test an estimate. We do not assert
that it is the original scalar encoder or that this comparison needs small
storage. Keeping the new injection exact makes the test more favorable.

Analyze the selected parameter block K=delta R_mem,source. At R0 its source
output sensitivities are zero. At time N+1 its raw memory sensitivity is

    T_pre K=M_N K H,
    M_N=sum_(j=0)^(N-1) a^j O^j.

There are exactly N injections: the first transition from h0 gives zero,
and transitions 2,...,N+1 give H. On Pi,

    M_N Pi=m_N Pi, m_N=(1-a^N)/gamma>3n/(5c).          (7)

Indeed a^N<=exp(-1)<2/5; exp(1)>1+1+1/2+1/6>5/2.

Both comparisons use identical pulse and reset injections. Subtracting
their final raw sensitivities gives the exact coupled formula

    Delta T K=-tau a^2 O L_i O M_N K H.                (8)

All K columns are coupled through the same H. No parameter columns have
been selected as independently controllable inputs.

### 4.2 Actual allowed queries see a width-independent loss

Use only the accepted one-step future inputs v_j in [1/5,9/20]. From h_T=0
their preactivations are [1/4,1/2], so the future gates range over
[g_lo,g_hi]^n. Let s_g=(g_hi-g_lo)/2>7/100 as accepted.

For any normalized sensitivity error, write Y=R Delta Z/beta. The accepted
sign-averaging bound applies to the WHOLE error and to any parameter block:

    D_box>=s_g ||Y||F/sqrt(n).

For the R block w_R/beta=1/n, so at the reference the query-composed
selected-block difference is Y0=R0 Delta T/n. Orthogonal left factors in
(8) and ||H||=sigma sqrt(l) give

    ||Y0||F =tau a^3 sigma sqrt(l)/n * ||L_i O M_N||F
              >=tau a^3 sigma sqrt(l)/n *m_N||L_i Pi||F.

The inequality projects onto Pi on the right; O M_N Pi=m_N Pi. It does
not assert that L_i commutes with O or with Pi. With a^3>49/50,
sqrt(l/n)>7/10, (5), and (7),

    D_box(reference error)
      > (7/100)(4/25)(49/50)(2/5)(7/10)(3/(5c))(7/10)
      =403368/(312500000 c)
      =0.0012907776/c.                                (9)

For c=1 this exceeds epsilon, even before accounting for the full future
query family. Gradient errors in other parameter blocks cannot cancel a
Euclidean norm in this block. The direct future R injection is zero at h_T=0;
other direct terms are supplied identically by the comparison.

### 4.3 Transfer to the actual fully dense predictor

Let T be the actual raw selected-block sensitivity, T0 the reference raw
sensitivity with the actual prescribed gates, and That0 the scalarized
comparison in 4.1. All injections have norm <=sigma sqrt(l). Both reference
propagators are contractions of norm <=a, hence

    ||T-T0||op<=e sigma sqrt(l)/gamma^2,
    ||T0||op,||That0||op<=sigma sqrt(l)/gamma.

The comparison answers with the ACTUAL future adjoint and normalized
surrogate w_R That0. Therefore its actual error matrix is

    Y=R(T-That0)/n,

while the reference (9) uses Y0=R0(T0-That0)/n. Thus

    ||Y-Y0||op
       <=e sigma sqrt(l)/n *(a/gamma^2+2/gamma)
       <=4sigma/(10^8 sqrt(n))*(a/c^2+2/(cn)).         (10)

The box-query distance changes by at most g_hi||Y-Y0||op. At c=1,n>=200
this is less than 1e-6. Consequently the ACTUAL allowed-query error is

    >0.0012897776 > epsilon=0.001.                     (11)

For each other fixed c>=1, the reference loss remains bounded below by
a positive constant of order 1/c, and (10) vanishes with n. We claim
an epsilon violation specifically at c=1; (9) does NOT exceed .001 for
all c. This specialization is inside the unchanged gamma=c/n class.

### 4.4 Two actual reachable endpoints, without matched-injection artifice

There is also a two-real-history version. Keep the entire prefix unchanged,
but compare the coordinate pulse h_mem=sigma e_k with the balanced pulse
h_mem=(sigma/sqrt(k))*1_k. Keep its source state H and the next exact reset
to h_T=0. The second actual memory gate is precisely g I with the SAME
g=1-tau/k. Its hidden vector has norm sigma; its realized pulse/reset inputs
obey the same strict domain bounds and dense compensation as (6).

Now the new injections differ as they actually should. In the selected
R_mem,source block the two reference final sensitivities differ by

    Delta T_real K=-tau a O L_i (a O M_N+I) K H.

After multiplying by the reference future R0/n, the stationary right
projection contains (a m_N+1)L_i Pi. Thus its query separation is at least
the reference lower bound (9), with a positive additional contribution
in this projected block. No global noncancellation is assumed: the right
projection itself gives the norm lower bound.

Both trajectories have bounded injection norm sigma sqrt(l). Comparing
their actual normalized difference to the reference costs at most

    2e sigma sqrt(l)/n *(a/gamma^2+1/gamma)

in operator norm, by the same transfer calculation. At c=1,n>=200 the
permitted query distance between these two ACTUAL, SAME-h sensitivities
therefore exceeds 0.0012887776. This is a genuinely observable reachable
difference of width-independent scale, not an arbitrary tensor perturbation.

It is only TWO histories. This conservative bound is not >2epsilon;
it alone rules out neither sharing an optimally chosen approximate answer
nor any low-dimensional encoder. The sharper surrogate error (11) concerns
using the specified scalarized answer. No antipodal dimension theorem or
logarithmic lower is being inferred from either comparison.

## 5. Query-visible old-credit gain itself can be linear in n

The pulse obstruction is not just an artifact of adding an injection error.
Here is an orientation-aware version on the block reference, with actual
group multiplier w_R. It shows why the old-credit factor cannot generally
be made width independent just by restricting to permitted query directions.

Differences of two permitted future gate vectors can be chosen as
2s_g times ANY memory sign vector, with their source gate entries identical.
After the fixed reset and future transition, the corresponding reference
adjoint differences at the pulse are a nonzero common scalar times

    (O^T)^2 s, s in {-1,1}^k.

For sign averaging these vectors have covariance I_k up to that scalar.
The scalar, including beta and 1/sqrt(n), cancels in the following GAIN
ratio. It does not disappear from the actual gradient-error margin (9).

Writing z for the vector before L_i, the past-credit response to the
non-scalar defect is

    w_R a * vec( (M_N^T O^T L_i z) H^T ).

Sign averaging and (5)-(7) show that at least one query difference with
L_i z!=0 has response norm divided by ||L_i z|| at least

    w_R a sigma sqrt(l)
       * ||M_N^T O^T L_i||F / ||L_i||F
    >w_R a sigma sqrt(l) m_N *(7/10).

To verify the ratio: the averaged squared numerator is the squared
Frobenius norm of the response matrix, while the averaged squared
denominator is ||L_i||F^2=1-1/k<1. Equation (5) gives
||L_i Pi||F/||L_i||F>49/50>7/10; project M_N on its stationary space.
If every nonzero sample ratio were smaller, their weighted average would
also be smaller, a contradiction.

The accepted dense family has w_R>=a sqrt(k)/(2n). Also
sqrt(kl)/n>2/5 and a^2>49/50. Therefore this
old-credit gain is strictly larger than

    (49/50)(sigma/2)(2/5)(3n/(5c))(7/10)
      =0.032928 n/c > n/(40c).                        (12)

This is a property of query-DIFFERENCE directions on the block reference,
whose dense query-error transfer was explicitly established in (10)-(11).
It is not a license to rescale a query and pretend it remains permitted.
The actual epsilon obstruction is (11), not the gain ratio alone.

The old credit can have gain of the same ORDER as 1/gamma on directions
coming from the allowed query family. Full row support is not enough to
infer this; the accumulated stationary contribution (7) supplies the gain.
Normalization does not universally erase it. A sharper upper must exploit
which of these contributions are ALREADY represented by shared moments,
not merely replace their norm by O_c(1).

## 6. What this says about dual summaries and approximate quotients

The accepted exact observability theorem already rules out a nonzero exact
query-invisible sensitivity subspace when the adjoint span is full. We do
not reprove it. On the present h=0 endpoint the accepted box metric also
has the quantitative lower s_g||R Delta Z/beta||F/sqrt(n).

One fixed adjoint, or a fixed small probe bank, is not the contract: future
inputs can choose a different gate vector after the summary is committed.
The pulse (8) acts on a shared, coherent old-credit block and remains visible
in that family. It cannot uniformly be placed in an epsilon-invisible
quotient. This does not mean ALL small directions remain visible; many may
be discarded under a correct uniform approximation argument.

An adjoint-specific gradient can be accumulated if that adjoint and its
backward history were known beforehand. For a LATE unknown query, storing
only that one accumulated gradient does not give its responses under later
non-scalar adjoint changes. A valid dual-space recursion must handle those
changes with counted state. Equation (12) blocks a gain-only shortcut,
not every recursive dual representation.

Similarly the accepted low-rank and fixed-Krylov method failures remain
method-specific. A tensor can have large query-visible row rank and still
be decoded from the shared moments in section 3. Matrix-algebra closure,
the age of old credit, and a single difficult pulse supply no logarithmic
continuous-memory lower bound.

## 7. Where the all-aperiodic argument stops

The b-event encoder transports complete old shared segments by k by k
matrices. At the next event it must preserve the association between that
transport and its source-feature moments. With an unbounded number of
events, simply retaining every pair makes (4) grow with b. Merely summing
the Q matrices loses those associations: in general

    sum_s Q_s M_s phi

cannot be replaced by (sum_s Q_s) times one common feature-moment map.
The same actual history controls both Q_s and M_s. Their dependence cannot
be declared independent to obtain a lower bound either.

The previous horizon-free adjoint gate budget remains valid. The new
obstruction proves that its coupling to old credit does not enjoy a
width-independent visible-gain bound on every admissible history. It does
NOT prove that the previous O_c(n) total-error estimate is sharp, or that
every individual gate event costs another n^2 independent robust coordinates.

The missing theorem is a uniform finite-error compression of these
TRANSPORT--FEATURE CORRELATIONS. It must either jointly merge them into
O_c(n^2) continuous state with error <=epsilon for all late queries, or
produce a single jointly robust fixed-h section proving that no such
merger is possible. The pulse example admits (4) with b=1 and T=O_c(n),
so it is expressly NOT the requested Omega_c(n^2 log n) counterfamily.

## 8. Bounded attack conclusion and mathematical checks

Strongest new sufficient-state theorem: O_b(n^2) for any fixed public finite
schedule of non-scalar gate events, arbitrary timing and arbitrary scalar
gating/source histories between events, at every horizon on the accepted
rotating family. All transport, feature, source and clock storage is counted.

Strongest new obstruction: even after removing the mean scalar gate and
retaining every new injection exactly, the one-pulse comparison violates
epsilon on the actual dense family at c=1. Query-visible old-credit gain
can be Omega_c(n). A proposed bounded visible-gain improvement is false.

Universal O_c(n^2) for arbitrary aperiodic histories: NOT established.
Joint robust Omega_c(n^2 log n) lower: NOT established.
Logarithmic necessity for general continuous memory: STILL OPEN.

Checks are mathematical: exact event updates and coordinate count; continuity
without gate-membership tests; explicit k-th coordinate choice;
stationary projector rank/Householder diagonal; injection indexing; paired
reachable pulse histories; exact fixed-h
trajectory and input slack; scalar contrast and matched injection; all-query
normalization; tensor Frobenius calculation; selected-block/dense transfer;
gain-ratio covariance; distinction between an estimate obstruction and a
memory lower bound. No automated tests or experiments were run.

This stage stops here. No gamma=Theta(1/n^2), other width, witness search,
architecture invention, training, GPU/CUDA or GAS-0 operation. The new
lemmas need independent hostile review before being treated as accepted.
