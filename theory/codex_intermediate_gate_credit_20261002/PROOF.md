# Intermediate weak gates: a joint linear lower and an explicit mixed-word problem

2026-10-02. New Codex-derived arguments, **independent review required**.
The general intermediate O(n) versus superlinear question remains OPEN.
No numerical experiment, architecture, other contraction regime, or old-chart
re-evaluation is performed. This file separates proved scoped statements from
the missing theorem; it does not treat expansion order as memory dimension.

## 1. Fixed model, source, and actual permitted-query norm

Keep the accepted family, c=1, gamma=1/n, epsilon=1/1000, n>=200:

    a=1-1/n, k=floor(n/2), l=n-k, r=k-1, d=floor(n/4),
    O=U(P_d direct_sum I_(k-d))U^T,
    U=I-2ww^T/(w^T w), w=e1-1_k/sqrt(k),
    R0=diag(aO,I_l/(100n)), ||R||op=a,
    e_R=||R-R0||op <=4/(10^8 n^2),
    h_t=tanh(R h_(t-1)+x_t+b), h_0=0,
    W=I, b=(1/20)1_n, theta=(R,W,b), P=2n^2+n.

R is the existing fully dense model. All its parameters remain frozen and
are independently differentiated. Let E embed physical memory coordinates
2,...,k. O fixes physical e1, and R0 E=a E O_* with O_* orthogonal.

The one raw source feature is H=(2/5)1_l. Source states are H at all interior
times and zero at the final reset. The selected parameter action is K H,
not independently selectable columns or arbitrary external injections:

    delta h_t=B_t K H,
    B_t=G_t(R B_(t-1)+alpha_t E),
    alpha_1=0, alpha_t=1 for t>=2.

Using the SAME actual gates, the accepted reference recurrence is

    M_t=G_*,t(a O_* M_(t-1)+alpha_t I_r), M_0=0,
    Bbar_t=E M_t, ||M_t||op<=n,
    all-query dense error <=eta_n=a||H||e_R n<2*10^-9.        (1)

The query family is exactly the accepted one: head q=1_n/sqrt(n), loss divided
by beta=max(1,||R||F), after L>=1 future recurrent steps with preactivations
in [1/4,3/4]^n. Future inputs are otherwise unrestricted. The past cube
(-1/2,1/2)^n is NOT a future-input constraint. Normalized gradient units
retain w_R=||R||F/n and w_R/beta=1/n.
These are frozen public normalization constants for differentiation, as in
the accepted contract; their numerical units are not changed here.

Define the REFERENCE-OPERATOR norm using the ACTUAL future adjoints:

    nu_n(Y)=w_R||H|| sup_(Q permitted) ||Y^T E^T xi_Q||_2,
    ||xi_Q||<=a/beta,
    nu_n(Y)<=A_n||Y||op, A_n=a||H||/n<=.3/sqrt(n).           (2)

The last inequality is a safe UPPER, not a substitution of arbitrary queries
or RMS measurements for the supremum. Decoder answers also include the exact
direct future contributions, determined by Q and the common endpoint h=0.
Those contributions cancel in same-endpoint comparisons.

The accepted moving-spike decomposition and R1 cover every allowed query
length. The old sustained charts are dead and are not used here. The joint
whole-class Omega(n) lower, sustained-history estimates and weak-tail theorem
are accepted premises, not re-proved.

## 2. An exact intermediate regime and its admissible gate cube

For definiteness take the fixed constants

    z_minus=1/20, z_plus=1/4,
    z0=(z_minus+z_plus)/2=3/20, Delta=(z_plus-z_minus)/2=1/10,
    N_n=ceil(4n log n)+1.                                  (3)

Log is natural. The weak-gate condition is on the SELECTED MEMORY restriction
G_*,t, as in the accepted fixed-feature ledgers. The unchanged source H=.4ones
has gate .84; requiring the full n-state gate deficit to be Theta(1/n) would
contradict that fixed-source setup. Source dynamics are not altered here.

At each of the N_n interior steps require

    G_*,t=I_r-diag(z_t)/n, z_t in [z_minus,z_plus]^r.        (4)

This is deficit Theta(1/n), across a window Theta(n log n), with constants
independent of n. The final endpoint reset necessarily has G=I and is a
separate step, not falsely classified as a positive-gap step. Statements
below also describe how to handle inherited old credit from an earlier prefix.
They do not prove a class theorem for every other choice of Theta constants.

The local window index t=1,...,N starts after a public source-establishment
step h=(0_k,H) from h0=0. That step has zero selected credit (previous source
was zero). Thus M_start=0 and alpha_t=1 throughout the window. An arbitrary
earlier fixed-source prefix instead supplies M_start with norm<=n. The
preparation and final reset are the two explicitly exempt steps; neither is
silently called a positive-gap gate. Full history length is N+2 in the
zero-credit preparation case, still Theta(n log n).

### Lemma I: every gate word in (4) has a simultaneous coupled tanh lift

Prescribe selected memory states

    h_(t,i)=s_i sqrt(z_(t,i)/n), s_i in {-1,1} fixed publicly,

and protected memory h_(t,1)=sqrt(z0/n). Keep the source H, start at zero,
perform the preparation just stated, and end at zero. Define actual inputs

    x_t=atanh(h_t)-R h_(t-1)-b.                            (5)

Substitution into the ACTUAL recurrence realizes the history exactly. These
inputs are held fixed for parameter derivatives; (5) is not differentiated
through theta. In particular the propagation/injection coupling is preserved.

Every memory state has |h_i|<=1/(2sqrt(n)) and
||h_memory||<=sqrt(k/(4n))<=1/(2sqrt(2)). For n>=200, its atanh coordinate
is less than .036. The R0 memory contribution is bounded by
a||h_memory||<=1/(2sqrt(2)); the source-to-memory reference contribution
is zero. The actual dense correction is <=e_R sqrt(k/(4n)+4l/25), below
10^-8. Adding bias .05 leaves every memory input below .445 in magnitude.
Source inputs have magnitude below atanh(.4)+.05+.4/(100n)+10^-8<.475,
including initial/reset cases. Thus the WHOLE product of gate arrays is
admissible with |x_i|<.48<.5; no single-axis restriction is used.

Any fixed-sign continuous gate section lifts continuously. At the fixed
endpoint all histories have h=0. With L_atanh<=1/(1-1/(4n))<1.002,
two gate words of the same length obey the useful radius estimate

    ||X(z)-X(ztilde)||_(history L2)
      <=(L_atanh+a)/(2sqrt(n z_minus)) ||z-ztilde||F.        (6)

Here the one-step shift of the hidden difference has norm at most one,
including the final reset. Equation (6) is a lift/radius estimate, not a
query separation or a dimension count. Signs varying between histories
are unnecessary for the lower; arbitrary admitted signs in the larger
class still have the same reference gate operator, up to the ledger (1).

### Old credit, fresh ages, and accumulated contraction

Put b_max=a(1-z_minus/n). Every chronological j-step transport in the window
has operator norm at most b_max^j<=exp[-(1+z_minus)j/n]. Unrolling gives

    M_N=Phi_(N,0) M_start
          +sum_(s=1)^N Phi_(N,s) alpha_s G_*,s,
    Phi_(N,s)=A_N ... A_(s+1), A_t=a G_*,t O_*.            (7)

The contribution injected at s has age N-s; after the reset it receives
one further factor aO_*, and the reset itself injects I_r. If ||M_start||<=n,
discarding inherited credit costs at most

    delta_old=A_n a n b_max^N
      <=.3 n^(1/2-4(1+z_minus))=.3 n^(-37/10).             (8)

For n>=200 this is below .3/200^3<4*10^-8. The fresh sum remains potentially
order n; (8) is not permission to discard it. For the zero-credit preparation,
delta_old is actually zero. For an earlier admissible prefix, the zero-start
fresh construction also uses alpha=1 through the weak window; (8) controls
the omitted prefix. The window start/schedule is public in this finite-window
formulation; no free adaptive history-dependent trigger is used.

## 3. A genuine Omega(n) section INSIDE the intermediate regime

This is new scope: the accepted one-pulse lower had an order-one gate deficit.
Here EVERY interior selected gate stays within (4), and the physical radius
is uniform in width. It is NOT a superlinear lower.

Let m=floor((k-d)/2)>=floor(n/8). Choose m pairs i_j,j_j in the physical NC
coordinates {d+1,...,k}. Define p_j=(e_(i_j)^k-e_(j_j)^k)/sqrt(2),
v_j=E^T(p_j,0_l) in R^r, and psi_j=E v_j in R^n. Every such pair vector
v_j is fixed by O_*. Each equal-pair diagonal gate preserves both its line and its
orthogonal complement. Therefore its selected eligibility is an exact scalar,
even though the rest of the reference operator is not diagonal.

Let u run over the CLOSED Euclidean unit ball in R^m. Use J=12n final interior
steps with pair gate deficit

    z_(i_j)=z_(j_j)=z0+Delta u_j,
    h_(i_j)=+sqrt((z0+Delta u_j)/n),
    h_(j_j)=-sqrt((z0+Delta u_j)/n).                       (9)

All earlier interior steps use z0 on every memory coordinate, with the same
fixed pair signs. Unpaired coordinates always use z0. Since log n>3 for
n>=200, N_n>12n+1, so there is a nonempty public baseline prefix. All
combinations are admissible by Lemma I, and all endpoints equal zero.

### Uniform finite physical radius

Only the final J states and the reset depend on u. For their paired memory
vector z_hidden(u), the square-root difference identity gives

    ||z_hidden(u)-z_hidden(0)||
      <= sqrt(2) Delta/[sqrt(n)(sqrt(z0-Delta)+sqrt(z0))]
      < (.24/sqrt(n)) ||u||.                             (10)

The entering input has atanh difference only, the following J-1 inputs have
atanh and R differences, and the reset has an R difference. Hence

    ||X(u)-X(0)||^2
      <= (.24^2/n)[1.002^2+(J-1)(1.002+a)^2+a^2] ||u||^2
      < 4 ||u||^2.                                      (11)

Thus the whole joint section has history-input L2 radius <2, independent of n.
This is a finite section, not a tangent statement. Epsilon is unchanged.

### Exact eligibility and a finite derivative bound

Let p_pre>=0 be the public pair eligibility before the J-step tail. For
z in [1/20,1/4], put g(z)=1-z/n and b(z)=a g(z). The tail and reset give

    p_J(z)=b(z)^J p_pre+g(z) sum_(j=0)^(J-1) b(z)^j,
    c_end(z)=a p_J(z)+1.                                 (12)

The negative derivative of the old term is nonnegative. The fresh derivative
is exactly (1/n) sum_(j=0)^(J-1)(j+1)b^j. Since 1-b<=5/(4n) and b<=a,

    -p_J'(z)
      >= [1-b^J(1+J(1-b))]/[n(1-b)^2]
      >= (16/25)n[1-16 exp(-12)]
      > (63/100)n.                                      (13)

The last strict bound needs no numerical certificate: e>5/2 implies
16 exp(-12)<1/1000 because (5/2)^12>16000. With J=12n, the entire interval
of z is controlled. The mean-value theorem gives, for ANY u,v in the ball,

    |c_end(z0+Delta u_j)-c_end(z0+Delta v_j)|
      >= a Delta (63/100)n |u_j-v_j|.                    (14)

No early credit, new injection, or gate-product coupling is omitted.

### One actual permitted query, no RMS replacement

Use one future step with preactivation 1/4 at the positive member of every
pair and 1/2 at the negative member; all other preactivations are 1/4. At
h=0 this means inputs .2 and .45, permitted by the accepted future contract.
Let s_g=[sech^2(1/4)-sech^2(1/2)]/2>7/100, the accepted lower inequality.
Its ACTUAL adjoint is xi=R^T g_future/(beta sqrt(n)). For every pair,

    psi_j^T xi
      >=[a sqrt(2)s_g-e_R sqrt(n)]/(beta sqrt(n)).         (15)

Project the queried selected gradient onto the orthonormal parameter vectors
Phi_j=v_j H^T/||H||. The reference eligibility differences in (14) then
give the corresponding projected answer. Other parameter coordinates or
residual state rows cannot cancel that projection.

For boundary antipodes u,-u, the reference half-distance using the principal
term of (15) is at least

    Delta (63/100) a^2 (2/5) sqrt(2l/n) s_g
      > (1/10)(63/100)(99/100)(2/5)(7/100)
      = .00174636.                                      (16)

The future-R correction in the half-distance is at most e_R||H||<2*10^-9,
using ||M(u)-M(-u)||op<=2n. The actual past dense-transfer half-loss is at
most eta_n<2*10^-9. Therefore EVERY antipodal pair obeys

    ACTUAL permitted-query half-distance > .00174 > epsilon. (17)

The section is continuous, jointly admissible, radius <2, and has exact same
endpoint h=0. The accepted antipodal argument implies at least m continuous
credit coordinates. This proves Omega(n) **within** the specified intermediate
regime. It neither improves the stronger accepted whole-class one-pulse
constant nor proves an omega(n) bound.

### Matching upper for this constant-tail subclass only

Its entire history is determined by u and public N,J. Store u (m coordinates),
an optional counted age clock (one), and actual current h (n while streaming).
The full ACTUAL B is decoded by affine powers for the public baseline and
the constant tail G(u):

    B_tail=(G(u)R)^J B_pre
             +sum_(j=0)^(J-1)(G(u)R)^j G(u)E,
    B_end=R B_tail+E.

B_pre is public affine baseline computation, not a saved history tape. Future
direct injections are exact. Decoder transient work is not bounded. Thus
this particular intermediate subclass is Theta(n), at unchanged units.
This is NOT an encoder for changing aperiodic weak gates.

## 4. Arbitrary weak gates: uniformly convergent ordered-word expansion

Write all selected gates in (4) as

    G_*,t=g0 I_r+D_t/n,
    g0=1-z0/n, ||D_t||op<=Delta,
    b=a g0, q_n=a Delta/[n(1-b)]=a Delta/(1+a z0)<1.       (18)

D_t is diagonal but need not commute with O_* or other transported D's.
Define the exact homogeneous coefficient recursion, starting every array at0:

    M_t^(0)=b O_* M_(t-1)^(0)+alpha_t g0 I_r,
    M_t^(1)=b O_* M_(t-1)^(1)
                  +(D_t/n)[a O_* M_(t-1)^(0)+alpha_t I_r],
    M_t^(j)=b O_* M_(t-1)^(j)
                  +(a D_t/n) O_* M_(t-1)^(j-1), j>=2.     (19)

For each finite t, M_t=sum_(j=0)^t M_t^(j), exactly; terms beyond the finite
degree vanish. The injection perturbation occurs explicitly in order1. Higher
orders contain chronological, noncommuting gate words, never an average of
transport packets.

### Lemma II: all-horizon finite-error truncation

Set

    C_n=Delta/[n(1-b)^2]=Delta n/(1+a z0)^2.

Geometric summation in (19) gives, uniformly in ALL admitted weak gate words,

    ||M_t^(0)||op<=g0/(1-b),
    ||M_t^(1)||op<=C_n,
    ||M_t^(j)||op<=C_n q_n^(j-1), j>=1,
    ||M_t-sum_(j=0)^p M_t^(j)||op
                        <=C_n q_n^p/(1-q_n).              (20)

For order1 the forcing is at most
(Delta/n)[a g0/(1-b)+1]=Delta/[n(1-b)], including direct injections.
For higher orders, division by 1-b multiplies the previous bound by q_n.
That proves (20) without commuting any gate and rotation.

After the zero reset define the EXPLICIT polynomial endpoint map

    P_(n,N,p)(D)=a O_* sum_(j=0)^p M_N^(j)(D)+I_r.         (21)

It is evaluated on the REACHABLE gate-word cube from Lemma I. Its homogeneous
mixed residual is H_(n,N,p)(D)=a O_* sum_(j=1)^p M_N^(j)(D).
It is not an arbitrary ambient operator ball.

The actual all-query error, allowing an earlier prefix bounded as in (8), is

    eta_n+delta_old+A_n a C_n q_n^p/(1-q_n).               (22)

Let epsilon_star=epsilon/4-eta_n-delta_old>0. Choose the public integer

    p_n=max(0, ceil{log[A_n a C_n/((1-q_n)epsilon_star)]
                                      /log(1/q_n)}).      (23)

If the logarithm is nonpositive, p_n=0 already suffices. Then (22)<=epsilon/4
uniformly over the window. For zero initial credit, omit delta_old. Since
q_n tends to Delta/(1+z0)<1, (23) is O(log n+log(1/epsilon)).

This is an ERROR theorem, not an O(n) encoder. The literal hierarchy stores
(p_n+1)r^2 history-dependent numbers, plus forward h and a clock if required;
the existing exact r^2 reference is cheaper. Those arrays cannot be made free.
The logarithmic sufficient expansion order neither proves a logarithmic
memory lower nor proves constant orders are impossible. It only supplies a
controlled, explicit object whose finite-error continuous width is unresolved.

## 5. The smallest explicit remaining statement

The fresh mixed residual in (21), with recursion (19), is the unresolved
object. Its domain is the diagonal gate cube (4), its radius is translated
to physical histories by (6), and its norm is the ACTUAL nu_n in (2).
Public degree0, window schedule, and model constants may be recomputed;
the ordered mixed residual and any history-dependent basis may not be free.

Already its first-order term is the explicit age/source kernel

    H_1(D)=(a O_*/n) sum_(s=1)^N b^(N-s) O_*^(N-s) D_s Q_s,
    Q_s=a O_* M_(s-1)^(0)+alpha_s I_r.                    (24)

Q_s is public. D_s is the actual weak gate variation; the age transport and
Q_s are tied to the same time s. The higher terms in (19) cannot presently
be discarded at fixed epsilon uniformly in n. Thus a first-order-only width
result would still need an all-order remainder/composition theorem.

Two precise sufficient next statements are:

**Upper target.** For the public p_n in (23), continuously update at most C n
counted real coordinates from the gate word (and counted actual h), with no
replay, and answer every permitted query of P_(n,N,p_n)(D) to error<=3epsilon/4.
Equation (22) then supplies the desired epsilon-correct intermediate encoder.
An offline low-dimensional fit without a counted continuous causal update
does not establish this statement.

**Lower target.** Construct ONE continuous D(u) in the same gate cube, for
u in a unit ball of dimension omega(n), with finite physical history radius
and

    nu_n(P(D(u))-P(D(-u)))/2 >5epsilon/4

for every boundary u. Lemma I supplies simultaneous admissibility and same
endpoint; (22) loses at most epsilon/4 in the half-distance, leaving an actual
robust lower at epsilon. This is a sufficient buffered criterion, not an
equivalence for sections whose margin is arbitrarily close to epsilon.

This reduction preserves finite changes, all chronological injection ages,
gate-history variation, and actual worst-case queries. It identifies a single
controlled noncommutative polynomial-width/online-realization problem, rather
than saying only 'the gates might be hard'. Neither target is proved here.

The algebraic expansion itself extends to any fixed 0<z_minus<z_plus with
z0=(z_minus+z_plus)/2, Delta=(z_plus-z_minus)/2 and n>z_plus. Then q_n<1
because z0>Delta. It applies to REALIZED admissible gate words in that wider
box. The unconditional whole-cube tanh lift, explicit lower constants and
radius in this file are only asserted for the specific box (3).

## 6. Compression and lower-construction attacks that did not close it

* Old-credit fading succeeds in (8), but the fresh operator in (7) remains.
  A long lookback is not a persistent-memory count.
* A public scalar resolvent is only degree0. The uniform omitted-order bound
  is order sqrt(n) in query units at fixed truncation order. That is a failure
  of this sufficient bound, not a lower against every resolvent encoding.
* Moving-spike rows are supplemented by a nonzero legal query remainder and
  the one-step gate zonotope. Retaining a few rows does not control H unless
  a credit-side remainder estimate is also proved. No such uniform estimate
  is established here.
* Multiscale ages or fixed polynomial moments need a finite remainder bound
  on the tied D/O words. Formula (19) does not collapse those words to powers
  of one generator under arbitrary aperiodicity. Treating it as a semigroup
  would assume away the unknown part.
* Counting separately visible ages, choosing independently controlled source
  columns, or replacing the operator family by a matrix ball would not satisfy
  the lower target. The new weak-gate construction in section3 supplies only
  m linear directions. No joint omega(n) section is obtained.

One concrete attempted larger family is D_(t,i)=lambda sum_(j=1)^q
Q_(t,j)U_(j,i), with ||U||F<=1 and an orthonormal public time basis Q.
The EXACT whole-section range condition is

    lambda max_t ||Q_(t,:)||_2 <=Delta.

For a flat time basis this bounds lambda by Delta sqrt(N/q), not the
independent-axis amplitude Delta sqrt(N). Its q*r coefficient count is not
a robust dimension. Even after satisfying this joint range constraint and
the physical radius bound (6), one must prove an infimum over the ENTIRE
coefficient sphere in the actual query norm. No such lower was obtained.
This range calculation is not a collision or a theorem ruling out that
family; it records the precise missing separation step without reviving
the old sustained charts.

These are limits of attempted proof routes, NOT impossibility theorems for
age aggregation, low-rank or nonlinear compression. No new numerical spectra,
SVD proxies, RMS queries, or unverified asymptotic fits are used.

## 7. Status and consequences

Strongest new lower: m>=floor(n/8) in the normalized intermediate regime,
with all interior deficits in [1/(20n),1/(4n)], radius<2, endpoint0, and actual
antipodal half-margin>.00174 at epsilon=.001. Constant-tail subclass upper
is O(n), so THAT subclass is Theta(n).

Arbitrary aperiodic intermediate upper: still the accepted r^2=O(n^2)
selected-credit store, plus n forward coordinates while streaming. No general
O(n) upper and no superlinear robust lower are obtained. Whole-class fixed-
feature Theta(n) is neither proved nor refuted. The whole-class accepted
Omega(n) lower stands unchanged.

The complete-model Omega_c(n^2)--O_c(n^2 log n) gap remains open. Even a later
one-feature upper needs compatible simultaneous feature summaries; a special
subclass theorem or incompatible lower sections cannot be multiplied into a
full-model result. No architecture, other gamma regime, learning or finite-bit
claim follows. Stop after this theory stage.
