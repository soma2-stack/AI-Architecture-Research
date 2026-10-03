# Autonomous endpoints and bounded absolute input energy

Codex, 2026-10-03. NEW THEOREMS, internally checked; independent hostile
review required. Accepted local-radius and zero-endpoint results are premises,
not re-reviewed. No architecture, learning or new gamma regime is introduced.

## 1. Frozen model, query metric, and the claimed scope

Use the same explicit hard dense family, initially h_0=0:

    k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,
    lambda=1/(100n), b0=1/20, W=I,
    U=I-2ww^T/(w^T w), w=e0-1_k/sqrt(k),
    P=P_d direct_sum I_(k-d), O=UPU,
    R0=diag(aO,lambda I_l), ||R||op=a,
    e=||R-R0||op<=4/(10^8 n^2),
    h_t=tanh(R h_(t-1)+x_t+b0 1_n).

Every R,W,b entry remains independently differentiated. Inputs in a particular
history are held fixed for those derivatives. All histories begin at zero.
Absolute history energy is the norm of ALL concatenated raw inputs:

    sum_(t=1)^T ||x_t||_2^2 <= R_abs^2.

The accepted past cube remains (-1/2,1/2)^n. Upper bounds below even hold
without that cube restriction. There is no subtracted public input center.

Future queries have L>=1 recurrent steps with each preactivation in
[1/4,3/4]^n, head q=1_n/sqrt(n), and terminal loss q^T h/beta_loss,
beta_loss=max(1,||R||F). The public normalization multiplier is
w_R=||R||F/n; beta_loss>1 here, so w_R/beta_loss=1/n. These multipliers are
held constant for parameter differentiation, exactly as in the accepted work.

Let E embed selected memory coordinates 1,...,k-1 and Pi_s project source
coordinates. Consider the TRUE coupled parameter action delta R=E K Pi_s,
K in R^(r x l). Its past sensitivity is the linear map

    B_t: K -> delta h_t,
    B_t K = G_t(R B_(t-1)K+E K h_(t-1),source),
    B_0=0, G_t=diag(1-h_t^2).                         (1)

Use ||K||F as the Euclidean parameter-group norm and the induced operator
norm for B_t. This is NOT raw sensitivity rank or an RMS query surrogate.
Bounding this entire R block bounds every one-fixed-feature restriction of
it in the unchanged units. Section 13 checks the full normalized gradient
contract in this same bounded-energy family. The general full-model worst-case
memory gap is not claimed solved.

The strongest final result is THEOREM 4 in section 12: no past credit template
is needed. Sections 7--10 retain a valid intermediate public-template bound
for derivation provenance; they are not the strongest encoder or energy bound.

## 2. Existence, uniqueness, and reference fixed-point coordinates

The map f(h)=tanh(Rh+b0 1_n) has Lipschitz constant a<1. Its iterations are
Cauchy: successive differences are bounded by a geometric sequence. Their
limit h* exists in the closed cube, satisfies f(h*)=h*, and lies in (-1,1)^n.
Two fixed points would satisfy ||h*-z*||<=a||h*-z*||, so they coincide.
Zero input maintains h* exactly. For the same reason f^p has the same unique
fixed point: there is no distinct autonomous periodic orbit.

The following quantitative reference calculation is needed, not assumed.
Put tau=1/sqrt(k), cH=1/(1-tau). O fixes physical e0. For a selected vector
v, put S=sum_(i=1)^(k-1) v_i and

    J=cH tau v_(d-1)-cH^2 tau^2 S.

Directly expanding UPU gives

    (Ov)_1 = J+cH tau S,
    (Ov)_i = v_(i-1)+J,       2<=i<=d-1,
    (Ov)_i = v_i+J,           d<=i<=k-1.               (2)

The protected coordinate has no selected-block coupling. Equation (2) is
an identity for the EXISTING rotation, not a replacement recurrence.
For clarity, extend v by physical coordinate v_0=0. Then w^T v=-tau S,
w^T P v=v_(d-1)-tau S, w^T P w=1-2tau, and the direct expansion is

    UPU v=Pv-cH Pw(w^T v)-cH w(w^T Pv)
                         +cH^2 w(1-2tau)(w^T v).

Its selected rows simplify to (2); Oe0=e0 follows from Ue0=1_k/sqrt(k).

For a scalar B, let H(B) be the unique solution H=tanh(aH+B). Define the
selected cycle v(B) as the unique fixed point of

    v_1=tanh(a v_(d-1)+B+(b0-B)/(cH tau)),
    v_i=tanh(a v_(i-1)+B),       2<=i<=d-1.           (3)

This auxiliary spatial cycle map is a contraction with constant a. The
off-cycle selected coordinates are H(B). Let S(B) be their total sum with
the coordinates in (3), and define

    Phi(B)=B-b0-a cH tau v_(d-1)(B)
                    +a cH^2 tau^2 S(B).              (4)

Both H(B) and v(B) depend continuously on B, by their contraction equations.
If Phi(B)=0, equations (2)--(4) give precisely the selected fixed point of
the reference R0. For example, (4) implies

    a cH tau S=(b0-B)/(cH tau)+a v_(d-1),

which turns the first equation in (3) into the special row in (2).

## 3. A width-uniform positive lower bound on h*

THEOREM 1. For every integer n>=10^6, every coordinate of the ACTUAL dense
autonomous fixed point satisfies

    h*_i >= m:=1/50.                                 (5)

Proof. First work with R0. Set m0=1/40 and

    B_m=atanh(m0)-a m0.

The series bound atanh(m0)-m0<=m0^3/[3(1-m0^2)] gives, for n>=10^6,

    0<B_m<1/100000<b0.

At B=B_m the normal scalar map fixes m0. Since the extra first-row forcing
in (3) is positive, its cycle fixed point lies in [m0,1]^(d-1). Furthermore

    0<=v_i-m0<=(1-m0^2)^(i-1)(1-m0),
    S(B_m)<=r m0+1600.                               (6)

This follows by the derivative bound on tanh between two outputs >=m0 and
the geometric sum; off-cycle coordinates equal m0.

Here k>=500000, tau<1/700 and cH^2<(700/699)^2<201/200. Dropping the negative
last-cycle term in (4), equations (6) give

    Phi(B_m)
      < 1/100000-1/20+(201/200)(1/40+1600/500000)
      = -0.021649 <0.                                (7)

At B=b0 the extra forcing in (3) vanishes; all selected coordinates equal
H(b0)>0. Since cH tau^2 r=1+tau,

    Phi(b0)=a cH H(b0)>0.                            (8)

Continuity gives a root B* in (B_m,b0). H(B) is increasing: either its scalar
fixed-point comparison or H'(B)=(1-H^2)/(1-a(1-H^2))>0 proves this. At this
root (3) preserves [H(B*),1]^(d-1); hence every selected coordinate is >m0.
The protected coordinate solves z=tanh(az+b0); source coordinates solve
s=tanh(lambda s+b0). Both are >tanh(b0)>m0. Uniqueness identifies this
constructed vector as the reference autonomous fixed point h*_0.

The actual dense fixed point is within

    ||h*-h*_0||_2 <= e||h*_0||_2/(1-a)
                   <=4/(10^8 sqrt(n)).                (9)

This follows by comparing the two fixed-point equations with tanh Lipschitz
constant one. For n>=10^6, m0-4/(10^8 sqrt(n))>m. Equations (5) follow. QED.

In particular m sqrt(n)<=||h*||_2<sqrt(n). Its hidden norm is Theta(sqrt(n)),
but zero input holds it; hidden-state norm is NOT raw-input energy.
The old weak selected gate cube has |h_i|<=1/(2sqrt(n)), so h* lies outside
it for these widths. At h*,

    ||G* R||op <=a(1-m^2), G*=diag(1-(h*)^2),          (10)

a contraction gap bounded away from zero. Exact rotating eigenvectors of O
do not give the old near-critical harmonic resolvent: its norm is bounded
by 1/[1-a(1-m^2)]<=1/m^2, rather than a growing n/f bound. This does not
re-review the old driven weak-gate construction, which used other states.

## 4. Query legality at the new common endpoint

From any current h and desired permitted future preactivation v, take

    x_future=v-Rh-b0 1_n.                             (11)

Then the next actual state is tanh(v). Iterating (11) realizes every allowed
future box sequence. The permitted contract constrains preactivations, NOT
raw future input size. Some future inputs in (11) can grow with width; they
are not part of the past-history budget. Nothing silently restricts them.
The nominally selected future raw inputs are then held fixed for parameter
derivatives, as in the accepted query construction; (11) is not differentiated
through the parameter-dependent control choice.

The effective current-state adjoint for a legal L-step future is

    xi_Q=(A_L...A_1)^T q/beta_loss,
    A_j=G_future,j R,
    ||xi_Q||_2<=a^L/beta_loss<=a/beta_loss.             (12)

The exact selected gradient consists of B_T^*xi_Q plus injections made
within the future. If histories have the same endpoint, those future
injections and their trajectories agree and cancel in differences. More
generally an encoder storing the true current h can compute them exactly.

For any past-sensitivity difference Delta B the ACTUAL all-legal-query norm
satisfies the upper bound

    sup_Q w_R||Delta B^*xi_Q||F <=(a/n)||Delta B||op.   (13)

Equation (13) is a uniform bound over the actual supremum, not its replacement
by arbitrary unit queries or an RMS average. The F norm is exactly the l2
gradient norm of this accepted parameter group. All query amplitudes and
epsilon remain unchanged.

## 5. Exact cheap preparation and local nonlinear equations

Let z_t=f^t(0) be the public ZERO-INPUT trajectory. At finite t it need not
equal h*. A finite cheap exact landing is obtained by using B zero-input
steps, then

    x_(B+1)=R(h*-z_B).                                (14)

The next preactivation is Rh*+b, so the endpoint is EXACTLY h*. Holding
afterwards costs zero. The full absolute norm is exactly ||R(h*-z_B)||_2;
there is no excluded preparation, source maintenance or reset input.

The radial contraction in the next section gives

    ||R(h*-z_B)||_2 <=a kappa^B sqrt(n).

Choose B so kappa^B sqrt(n)<=min(R_abs/2,1/4). This supplies, for EVERY fixed
R_abs>0, a nonempty exact-endpoint class with norm<=R_abs/2 and inputs inside
the accepted past cube. It is a zero-dimensional witness of feasibility,
not a robust lower section. Unlike h=0, this class is not eventually empty.

For deviations u_t=h_t-h*, put v_t=R u_(t-1)+x_t. Exactly,

    u_t=tanh(atanh(h*)+v_t)-h*,
    u_t=G* v_t-h* componentwise G* v_t^2+r_(3,t),
    ||r_(3,t)||_2 <=(1/3)||v_t||_6^3.                 (15)

The uniform scalar bound |tanh'''|<=2 proves the remainder. Alternatively
||u_t-G*v_t||_2<=||v_t||_4^2/2, using |tanh''|<1. The quadratic term is
generally NONZERO: odd/even history parity is not inherited around h*.
In each coordinate the displayed quadratic term is
-h*_i[1-(h*_i)^2](v_t,i)^2.
The exact sensitivity equation is still (1); G_t=G*-2diag(h* u_t)-diag(u_t^2).
No derivative is taken through a history's inverse lift or endpoint choice.

The upper theorem below uses exact global inequalities, not approximation
by (15). Thus it pays ALL nonlinear interactions without a discarded Taylor
tail or the old polynomial/dense approximation ledger.

## 6. Global radial contraction about a nonzero fixed point

LEMMA 2. For any p,z in (-1,1), with |p|>=m,

    |atanh(z)-atanh(p)| >=(1+p^2/4)|z-p|.

Indeed the secant integral of atanh' is at least

    1+integral_0^1 [p+s(z-p)]^2 ds
      =1+(p^2+pz+z^2)/3 >=1+p^2/4.                  (16)

The case z=p follows by continuity. Applying (16) in each actual update
against h* gives

    ||h_t-h*||_2 <= kappa ||R(h_(t-1)-h*)+x_t||_2,
    kappa=1/(1+m^2/4)=10000/10001.                    (17)

This is a global radial bound relative to h*, not an assertion that every
Jacobian of f has norm <=kappa a. That distinction is essential.

Define the public burn-in

    L_n=ceil(log(2sqrt(n)/m)/log(1+1/10000)).           (18)

It is O(log n), with a large constant, and kappa^L_n sqrt(n)<=m/2.
After this time the zero-input trajectory has every gate <=

    q_g=1-m^2/4=9999/10000.                           (19)

For ANY history with total input norm <=R_abs, extending it by zeros if
needed, the global radial convolution gives

    ||(h_t-h*)_(t>=L_n)||_(time l2)
      <= m/[2sqrt(1-kappa^2)] + kappa R_abs/(1-kappa)
      < 1+10000 R_abs.                               (20)

This uses the l2 gain of the scalar geometric convolution (triangle
inequality for its shifted sequences). It is a STATE energy calculation,
not a substitute for future-query visibility.

Call t>=L_n bad if ||h_t-h*||_2>m/2. The number of bad time steps, at arbitrary
horizon, is at most

    B_R=ceil(10000(1+10000R_abs)^2).                   (21)

At a good step all coordinates satisfy h_t,i>=m/2, and ||G_t R||op<=q_g;
at a bad step ||G_t R||op<=a<1. Thus any length-j transport wholly after
burn-in obeys

    ||A_t...A_(t-j+1)||op <= q_g^max(0,j-B_R),
    sum_(j>=0) q_g^max(0,j-B_R)=B_R+10000=:H_R.        (22)

There is no exponential prefactor q_g^(-B_R) in this summed bound. The bad
steps can be anywhere; no periodicity, sparse scheduling or separate-axis
assumption is made.

For later use, the pointwise geometric l2 gain in (17) also gives

    ||h_t-z_t||_2 <= chi_R:=m+71R_abs, t>=L_n.         (23)

Here kappa/sqrt(1-kappa^2)=10000/sqrt(20001)<71, and both public initial
radial terms are at most m/2. Before burn-in, ordinary incremental
Lipschitzness yields ||h_t-z_t||_2<=R_abs sqrt(t).

## 7. Auxiliary source variation and public sensitivity template

Write delta h_t=h_t-z_t. Global incremental Lipschitzness gives

    ||delta h||_(time l2)<=n R_abs.

Because the reference source block is lambda I_l and its off-block
coupling is zero, actual source variations obey

    ||delta h_source,t||_2
      <=lambda||delta h_source,t-1||_2
          +||x_source,t||_2+e||delta h_(t-1)||_2.

Therefore, for arbitrary history length,

    ||delta h_source||_(time l2)
      <=(1+en)R_abs/(1-lambda) <=2R_abs.              (24)

Let B_t^0 be the EXACT actual-R sensitivity (1) of the public zero-input
history z_t, from initial sensitivity zero. It depends only on public model
constants and t, not the private history. Its bound is

    ||B_t^0||op<=sqrt(l)t,              t<=L_n,
    ||B_t^0||op<=sqrt(l)(L_n+10000),    every t.        (25)

The latter follows by retaining initial sensitivity at burn-in and summing
the reference good-step contraction (19). Source injection norm is at most
sqrt(l). Public sensitivity is NOT zero; it is answered by the decoder.

## 8. Auxiliary intermediate finite-error credit theorem

Subtract (1) from its public counterpart. With delta B_t=B_t-B_t^0, exactly

    delta B_t = G_t R delta B_(t-1)
       +(G_t-G_t^0)(R B_(t-1)^0+I_source,t-1^0)
       +G_t delta I_source,t-1.                       (26)

Here I_source K=E K h_source; its difference has operator norm
||delta h_source||_2. Gate differences satisfy
||G_t-G_t^0||op<=2||delta h_t||_2. This keeps the actual coupled injections.

Up through burn-in, (24)--(26) and ||delta h_t||<=R_abs sqrt(t) imply

    ||delta B_(min(T,L_n))||op
      <=2sqrt(l)R_abs L_n^(5/2)+2R_abs sqrt(L_n).      (27)

For example the gate-forcing sum is bounded by
2sqrt(l)R_abs sum_(t<=L_n) t^(3/2)<=2sqrt(l)R_abs L_n^(5/2);
source forcing is bounded by Cauchy using (24).

For later times, inherited (27) is not amplified. The gate-forcing bound is
2sqrt(l)(L_n+10001)chi_R per step. Sum its transports with (22).
The source-forcing sum is at most 2R_abs sqrt(H_R), because squared
transport bounds are no larger than their summed bounds. Consequently

    ||B_T-B_T^0||op <=
       2sqrt(l)R_abs L_n^(5/2) +2R_abs sqrt(L_n)
       +2sqrt(l)(L_n+10001)chi_R H_R+2R_abs sqrt(H_R)   (28)

for EVERY finite horizon, every admitted gate history produced by a bounded
raw-input history, and every endpoint. No tail has been declared invisible
merely from exact rank or one singular spectrum.

THEOREM 3 (absolute-energy finite-error upper). For n>=10^6 the public
zero-input template has uniform ACTUAL permitted-query error at most

    delta(n,R_abs) =
      (2sqrt(l)/n)[R_abs L_n^(5/2)+(L_n+10001)chi_R H_R]
           +(2R_abs/n)[sqrt(L_n)+sqrt(H_R)].           (29)

Equations (13) and (28) prove this directly. For every fixed R_abs,

    delta(n,R_abs)=O_R((log n)^(5/2)/sqrt(n)) ->0.     (30)

All dense couplings, gate-history variations, fresh source changes, nonlinear
terms, preparation and corrections are included. No old epsilon/4 ledger is
needed: these are exact actual-system estimates.

## 9. Auxiliary template encoder (superseded by section 12)

An encoder that also preserves forward state stores

    E_t=(t,h_t) in R^(n+1),
    U(E_t,x_(t+1))=(t+1,tanh(Rh_t+x_(t+1)+b)).         (31)

It is continuous and causal. For a query, compute B_t^0 from the public
zero-input schedule and the public model, propagate it through the ACTUAL
future from stored h_t, and add the exact public future injections. Equation
(29) is its error on the fixed-feature block, uniformly over all late queries.

Only the n hidden coordinates and one clock persist. There is no actual
input/gate history tape, replay or history-dependent sensitivity cache. The
decoder may use temporary arithmetic workspace to evaluate the PUBLIC zero
schedule; it does not reconstruct/replay discarded private history. This is
the accepted persistent-coordinate model, which excludes temporary workspace
and final output storage. It is not a runtime/working-RAM theorem.

If queries occur at a fixed public common endpoint h*, its h is public and
need not be retained for terminal credit queries. Then one clock suffices;
at a given public time even that clock is unnecessary. An implementation
requiring forward predictions throughout should use the counted n+1 version.

For an explicit sufficient onset, for n>=10^6 let

    C_R=2R_abs*101^5+40008 chi_R H_R
                         +2R_abs(101+sqrt(H_R)).

The inequalities L_n<=10002log n, L_n+10001<=20004log n give

    delta(n,R_abs)<=C_R(log n)^(5/2)/sqrt(n)
                    <=10^19(1+R_abs)^3(log n)^(5/2)/sqrt(n). (32)

For n>=10^80, log n<=n^(1/20); hence a deliberately unoptimized sufficient
threshold for error <=epsilon/2 is

    n >= max(10^80, [2*10^19(1+R_abs)^3/epsilon]^(8/3)). (33)

No practical-onset claim is made. Take epsilon=.001 in the accepted units.
The logarithm comparison is elementary: at 10^80, log n<240<10^4=n^(1/20),
and n^(1/20)/log n increases whenever log n>20.

At any fixed common endpoint and fixed history length, all histories in the
absolute budget are within delta of the SAME queried-gradient template.
Every antipodal half-distance is therefore <=delta. Once (33) holds it is
<=epsilon/2, so NO positive-dimensional section can meet the required
half-margin >epsilon. This is a nonvacuous metric conclusion: section 5
constructs cheap nonempty histories ending at h*. It uses no bit counting
or topology inference from finite packing.

Thus omega(n) fixed-feature robust memory does NOT survive constant absolute
energy in THIS frozen family. Indeed asymptotic fixed-feature credit needs
at most one clock; counting online forward state gives n+1. Other RNN families
or other loss/normalization contracts are not covered.

## 10. Auxiliary weaker energy tradeoff (superseded by section 12)

Packets can use zero-input gaps and a final correction, so their public input
baseline can be cheap. But (29) applies to every jointly admissible packet
allocation, any number of harmonics, any interval length, and every finite
radius construction satisfying the total absolute budget. It bounds their
FULL nonlinear query effect, not separately visible axes. A better Fourier
basis or optimized amplitudes cannot evade this upper.

The first lost old-mechanism dependency is its long near-critical harmonic
transport: (10), (17) and the finite bad-step budget replace it with a
width-independent effective transport budget after public burn-in. The
old even-order cancellation also cannot be assumed around nonzero h*, as
the quadratic term (15) shows. These observations explain the mechanism;
the rigorous impossibility is the uniform actual-query bound (29).

Any positive-dimensional robust section at epsilon requires delta>epsilon.
Equation (32) yields the explicit necessary energy condition

    R_abs > [epsilon sqrt(n)/(10^19(log n)^(5/2))]^(1/3)-1. (34)

This is a conservative necessary cost for ANY robust antipodal distinction,
not a sharp dimension-dependent lower law. In particular it forces growing
absolute energy, at least order n^(1/6)/(log n)^(5/6) in this bound. The old
accepted local-radius section supplies superlinearity at absolute cost
asymptotic 0.53312948 n sqrt(log n), with its old endpoint. The gap between
these energy scalings is open; no minimum-energy exponent is identified.

## 11. Other endpoints and interpretation

The upper theorem did not require h_T=h*: at any public common endpoint
the private credit difference has the same bound. With h stored, it also
holds without a common endpoint. Therefore changing the common endpoint
again cannot recover superlinear fixed-feature credit at fixed absolute R
inside this family and query contract.

The unique autonomous h* is best for zero-cost holding. For another endpoint
z, write u=z-h*. Lemma 2 gives a constant-holding input lower bound

    ||atanh(z)-Rz-b||_2 >=(1+m^2/4-a)||u||_2.          (35)

Holding L steps costs at least sqrt(L) times this value. Nontrivial autonomous
periodic alternatives are impossible by section 2. Nearby endpoints can still
be reached cheaply; neither (35) nor the theorem claims h* uniquely minimizes
every finite landing cost.

Accepted statements remain separate: growing LOCAL radius Omega(n^(16/15));
bounded LOCAL radius Omega(n^(19/18)); full-model Omega_c(n^2)--O_c(n^2 log n).
They concern costly driven input histories and are not contradicted. This
stage counts the full past input drive, allows a genuine nonempty autonomous
endpoint class, and derives a finite-error fixed-feature upper specifically
for constant absolute energy. No finite-bit, VRAM, practical onset, runtime,
training advantage, architecture or every-RNN statement follows.

## 12. Strongest theorem: a zero-past-credit decoder

The preceding comparison to public sensitivity can be removed entirely.
Up through burn-in every actual history has

    ||B_t||op <=sqrt(l)t,  t<=L_n.

After burn-in unroll (1), retain B_L without amplification, and bound every
fresh injection by sqrt(l). Summing (22) gives, at EVERY horizon,

    ||B_T||op <=sqrt(l)(L_n+H_R).                     (36)

This estimate concerns the entire TRUE coupled sensitivity, not just its
difference from a public template. The source state is automatically bounded
coordinatewise by tanh; no source-only variation restriction is needed.

THEOREM 4 (strongest finite-error encoder). For every fixed R_abs>0, all
n>=10^6, and every history of ANY finite length with full absolute input
norm <=R_abs, a decoder that sets PAST selected sensitivity to ZERO, preserves
the actual current hidden state, and computes the future's direct sensitivity
exactly has uniform error at most

    delta_0(n,R_abs)=sqrt(l)(L_n+H_R)/n
                    <=(L_n+H_R)/sqrt(n).              (37)

This is uniform over ALL permitted future queries, by (12)--(13) and (36).
The normalized past-gradient contribution itself has that bound. Its future
direct part need not be small and is not discarded. No actual or public past
history needs replay, no public sensitivity needs recomputation, and no clock
is needed.

The exact continuous encoder is simply

    E_t=h_t in R^n,
    U(E_t,x)=tanh(R E_t+x+b).

These n counted coordinates preserve forward state. There are ZERO persistent
credit coordinates. At terminal queries with the public common endpoint h*,
even the forward state is public and no private terminal summary is needed.
As in the accepted encoding model, computing a supplied future query may use
temporary arithmetic workspace; this is not a whole-program RAM/runtime
claim or a bound on storage for queries outside the energy promise.

For fixed R_abs, delta_0=O_R(log n/sqrt(n))->0. An explicit sufficient integer
onset for delta_0<=epsilon/2 is

    n >= ceil(max{10^80, (40008/epsilon)^(20/9),
                                      (4H_R/epsilon)^2}). (38)

Indeed L_n<=10002log n and, at n>=10^80, log n<=n^(1/20).
The second condition makes L_n/sqrt(n)<=epsilon/4; the third makes
H_R/sqrt(n)<=epsilon/4. For R_abs=1 and epsilon=.001, n>=10^80 is sufficient.
This is deliberately loose and proves no useful practical onset.

At any FIXED common endpoint and history length, a pair's future direct
contributions agree. Each past contribution has norm <=delta_0, so every
antipodal half-distance is <=delta_0. Thus once (38) holds there is NO
positive-dimensional epsilon-robust antipodal section. This is nonvacuous:
section 5 constructs nonempty cheap exact-h* histories, with every start and
correction counted. Exact sensitivity distinctions may still exist below
epsilon; no exact accessibility/observability theorem is contradicted.

A sharper necessary absolute-energy condition for ANY robust half-margin
>epsilon follows from (37), L_n<=10002log n, and

    H_R<=10000(1+10000R_abs)^2+10001:

    R_abs > (sqrt((epsilon sqrt(n)-10002log n-10001)/10000)-1)/10000, (39)

whenever the expression is real and positive; otherwise the condition is
vacuous. In particular this bound forces R_abs=Omega_epsilon(n^(1/4))
asymptotically before even one robust direction can exist in this family.
The explicit leading necessary coefficient from (39) is sqrt(epsilon)/10^6.
It is conservative, not a sharp minimum-energy theorem or a D-specific law.
Equation (39) supersedes the weaker intermediate energy bound (34).

Finally, a finite-time public endpoint z_T=f^T(0) has an EXACTLY zero-input
baseline and no landing correction. It can be preferable if one only wants
a common endpoint at a chosen public time; it is not stationary unless it is
h*. The same upper applies there and at all other endpoints. The autonomous
h* is unique for zero-cost stationary holding, not uniquely cheapest for
every finite-time landing. No endpoint choice recovers superlinear robust
fixed-feature credit under a constant absolute budget in this frozen family.

## 13. Full-gradient contract consistency, in the SAME bounded-energy family

This check avoids an ambiguity if the query decoder must return every R,W,b
coordinate, rather than only the fixed-feature projection. It does not enlarge
the model/energy class or close the accepted all-admitted-history full-model gap.

Let A_n=L_n+H_R. For the entire independently differentiated R group, its
actual coupled injection is delta R h_previous; operator norm is <=sqrt(n)
when ||delta R||F=1. Repeating (36) gives

    ||S_R,T||op<=sqrt(n)A_n.

For W, the injection is delta W x_t. Cauchy and the input energy bound give
an initial bound R_abs sqrt(L_n), and (22) gives a later bound R_abs sqrt(H_R).
For b, the injection has norm one. Thus

    ||S_W,T||op<=R_abs(sqrt(L_n)+sqrt(H_R)),
    ||S_b,T||op<=A_n.                                 (40)

The accepted weights are w_W=||I||F/n=1/sqrt(n), w_b=RMS(b)=.05.
Also beta_loss=||R||F>=a sqrt(k)-sqrt(n)e>sqrt(n)/2 for n>=200.
The actual all-query errors from dropping past sensitivity in each group obey

    delta_R<=A_n/sqrt(n),
    delta_W<=2R_abs(sqrt(L_n)+sqrt(H_R))/n,
    delta_b<=A_n/(10sqrt(n)).                         (41)

Their sum is a valid bound for the weighted Euclidean concatenation of the
groups and also for their maximum. No group units have changed. Therefore
the full normalized past-gradient error is at most

    delta_all=1.1 A_n/sqrt(n)
                       +2R_abs(sqrt(L_n)+sqrt(H_R))/n ->0. (42)

The zero-past decoder can compute ALL future direct contributions exactly
from its true stored h_t and the query, starting every parameter sensitivity
at zero at query time. Its persistent state is still only h_t in R^n.

One conservative onset for delta_all<=epsilon/2 is

    n>=ceil(max{10^80,8R_abs^2,(120024/epsilon)^(20/9),
                                            (12H_R/epsilon)^2}). (43)

Indeed the last two bounds make A_n/sqrt(n)<=epsilon/6. If n>=8R_abs^2,
delta_W<=(A_n/sqrt(n)), since sqrt(L_n)+sqrt(H_R)<=sqrt(2A_n) and A_n>=1.
Hence delta_all<=2.1epsilon/6<epsilon/2. For R_abs=1, epsilon=.001,
n>=10^80 suffices here too.

This extension is included solely to verify the query contract. It concerns
THIS positive-bias rotating dense family under constant absolute input energy,
not the full-model worst case over all admitted driven histories or all RNNs.
No stronger full-model lower or removal of its n^2--n^2 log n gap follows.
