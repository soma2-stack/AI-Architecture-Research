# A bounded-history-radius joint multiharmonic lower section

Codex, 2026-10-03. NEW derivation, internally checked;
independent hostile review required before project acceptance.
The reviewed 16/15 all-admitted-history theorem is a premise, not re-proved
or changed. This stage changes only F and delta in its existing section.

## 1. Contract and theorem

Keep the SAME hard dense tanh family, c=1, gamma=1/n, epsilon=1/1000,
group-RMS parameter-gradient units, permitted future preactivation/head
queries, fixed source H, admitted intermediate gate cube, public preparation
and exact reset endpoint h=0. Parameters are frozen; all R,W,b entries remain
independently differentiated. No new architecture or query is supplied.

Physical history radius here means the owner's declared LOCAL radius

    sup_y ||X_n(y)-X_n(0)||_2,

about the public zero-defect history X_n(0) at the SAME width and length.
The norm is the ordinary Euclidean norm of the concatenated RAW INPUTS.
It is not a gate norm or a renormalized input norm. The center depends on n.
We do NOT claim a bound on ||X_n(y)||_2 relative to the zero input history:
the public source/preparation trajectory itself is not zero.

NEW THEOREM. For EVERY integer n>=10^900, there is ONE continuous admitted
closed-ball history section with common final h=0 and

    R_history < 1/50,
    D >= n^(19/18)/20,000,000,
    every boundary antipodal permitted-query half-distance >9>epsilon.

Use the reviewed spreading matrix/profile/gate-word construction with

    d=floor(n/4), k=floor(n/2), q=floor(d/10^6),
    F=floor(n^(1/18)), eta=10^(-4),
    delta=eta F/[n^(1/4)(log n)^(1/4)],
    N=ceil(4n log n)+1, D=qF.                          (1)

Log is natural. This is a deliberately unoptimized sufficient threshold,
not a numerical experiment at that width. The ball is the SAME one joint
saturated multiharmonic section; no separate-axis or packing argument is used.
Its boundary sphere forces at least D continuous no-replay credit coordinates
by the accepted antipodal encoding principle. Thus, in this local radius
contract, universal O(n) fixed-feature memory is refuted too.

## 2. Where the old radius estimate loses information

The old calculation used ||Delta h_t||_2<delta and separately bounded
atanh(h_t)-atanh(h_t^0) and R Delta h_(t-1). It obtained at most 3delta
per step and then concatenated N+O(1) steps in Euclidean norm:

    R_history <8delta sqrt(n log n).

The sqrt(N) factor IS a legitimate history-energy accumulation. The loss
is BEFORE it: the two contributions in one raw input are subtracted,
not independent positive quantities. For co-moving profiles they largely
cancel. In addition, the orthogonal projection after saturation gives a
uniform energy bound on each profile that was not used in the old radius
estimate. Neither observation changes the accepted query-signal proof.

We now retain those cancellations. There is no cancellation between
different time slots in the concatenated Euclidean norm.

## 3. Uniform profile energy and co-moving motion

Use the reviewed notation U=I-gamma_U w w^T, w=e0-1_k/sqrt(k),
gamma_U=1/(1-1/sqrt(k)), P=P_d direct_sum I_(k-d), O=UPU,
a=1-1/n, R0=diag(aO,I_l/(100n)). For n>=200,

    gamma_U<=10/9, ||w||_2<sqrt(2)<3/2,
    k>=n/3, n/5<=d<=n/4,
    ||R||op=a<1, e_R=||R-R0||op<=4/(10^8 n^2).

Profiles are exactly those in the reviewed proof:

    s_f=P_perp tanh(16sqrt(dF) B y_f)/(4F).

Besides ||s_f||infinity<=1 and sum_i s_f(i)=0, orthogonality of P_perp
implies the previously unused whole-section bound

    ||s_f||_2 <=sqrt(d)/(4F).                           (2)

For tau=N-t define the VIRTUAL full-cycle vector, extended by zero off-cycle,

    c_t(i)=delta/F sum_(f=1)^F s_f((i+tau) mod d) cos(2pi f tau/d).

No virtual node is supplied as a legal control. The actual defect omits
physical coordinate0 exactly as in the accepted construction. For EVERY y,

    ||c_t||infinity<=delta,
    sum_i c_t(i)=0,
    ||c_t||_2<=delta sqrt(d)/(4F).                     (3)

P acts as (Pv)(i)=v(i-1) on the cycle. Hence the profile shift cancels:

    c_t(i)-(P c_(t-1))(i)
      =delta/F sum_f s_f(i+tau)
           [cos(omega_f tau)-cos(omega_f(tau+1))].

Using |cos(v+omega)-cos(v)|<=|omega| and (2),

    ||c_t-P c_(t-1)||_2
       <=delta/F * sqrt(d)/(4F) * (2pi/d)*F(F+1)/2
       <=pi delta/(2sqrt(d)).                         (4)

This calculation is joint in all profiles. It does not demand time
orthogonality of saturated profiles or independent axis movements.

## 4. The exact nonlinear lift and its small mean

Assume 0<delta<=1/20. Put z0=3/20 and

    phi(v)=sqrt(z0-v)-sqrt(z0).

For |v|<=delta, z0-v>=1/10, so

    |phi'(v)|<=2,
    |phi(v)+v/(2sqrt(z0))|<=4v^2.                      (5)

The second inequality is Taylor's theorem with
|phi''(v)|/2=1/[8(z0-v)^(3/2)]<4. No linearization replaces the lift.

Let v_t=phi(c_t)/sqrt(n) on the virtual cycle, zero elsewhere, and let

    p_t=v_t-v_t(0)e0.

p_t is the EXACT physical memory hidden-state difference from the public
zero-defect history. All fixed signs are chosen positive, an admitted choice
in the original inverse lift. Source coordinates and off-cycle coordinates
do not vary. In particular physical coordinate0 stays fixed.

Equations (3)--(5) give

    ||p_t||_2<=delta/(4F),
    |v_t(i)|<=2delta/sqrt(n),
    |sum_i v_t(i)|
       <=4||c_t||_2^2/sqrt(n)
       <=delta^2 d/(4F^2 sqrt(n)).                    (6)

The last bound is crucial: the linear contribution sums to zero EXACTLY.
The remaining nonlinear mean is quadratic and carries F^-2, not F^0.

Because coordinatewise phi commutes with P, (4) yields

    ||v_t-Pv_(t-1)||_2<=pi delta/sqrt(nd)<8delta/n.

Removing node0 at the two times adds at most 4delta/sqrt(n). Thus

    ||p_t-Pp_(t-1)||_2<=4delta/sqrt(n)+8delta/n.         (7)

All inequalities hold on the ENTIRE parameter ball, not only its boundary.

## 5. Exact rank-two transport correction

For any such physical p, p(0)=0. Let m=sum_i p(i) and beta_p=|m|/sqrt(k).
From (6), d<=n/4 and k>=n/3,

    beta_p <=delta^2/(8F^2)+4delta/n.                  (8)

Indeed d/sqrt(nk)<=1/2, while the removed virtual node contributes
at most 2delta/sqrt(nk)<4delta/n. This is an upper bound on the exact mean,
not an assumed conserved zero mean of the nonlinear hidden states.

Since P preserves sums and sends one adjacent cycle coordinate into node0,

    |w^T p|=beta_p,
    |w^T Pp|<=2delta/sqrt(n)+beta_p.

Expanding the ACTUAL O=UPU gives

    Op-Pp =-gamma_U w(w^T Pp)-gamma_U Pw(w^T p)
              +gamma_U^2 w(w^T Pw)(w^T p).            (9)

Use gamma_U||w||<2, gamma_U^2||w||*|w^T Pw|<4 and (8):

    ||(O-P)p||_2<=4delta/sqrt(n)+8beta_p
                <=4delta/sqrt(n)+delta^2/F^2+32delta/n
                <=7delta/sqrt(n)+delta^2/F^2.          (10)

The last step uses n>=200, hence 32/sqrt(n)<3. This treats the missing
node, Householder twist and nonlinear mean jointly and exactly. It does
not grant an inaccessible latent transport or query.

## 6. Raw input energy: sharper whole-section radius bound

For an interior transition, the raw-input difference is exactly

    Delta x_t =atanh(h_t)-atanh(h_t^0)-R Delta h_(t-1).

Only the memory difference p_t varies. At each varying coordinate the
squared hidden value is at most (z0+delta)/n<=1/(4n). Therefore

    ||atanh(h_t)-atanh(h_t^0)-p_t||_2
       <=||p_t||_2/(4n-1)<=delta/n.                   (11)

Combining (7), (10), the factor 1-a=1/n, and the actual dense perturbation,

    ||p_t-aOp_(t-1)||_2
       <=11delta/sqrt(n)+delta^2/F^2+9delta/n.

The dense residual costs at most e_R||p_(t-1)||<=delta/n, and (11)
costs at most delta/n. Consequently the following simpler simultaneous
majorant is valid:

    ||Delta x_t||_2<=16[delta/sqrt(n)+delta^2/F^2+delta/n]. (12)

The first varying transition has a public previous hidden state and costs
at most 2||p_1||<=delta/(2F). The final exact reset costs at most
||R p_N||<=delta/(4F). Preparation inputs are identical across the section.
The Euclidean contribution of these two boundary steps is
at most sqrt(5)delta/(4F)<delta/F. Summing the squared interior norms and
then using sqrt(A+B)<=sqrt(A)+sqrt(B), we obtain

    R_history <=delta/F
        +16sqrt(N)[delta/sqrt(n)+delta^2/F^2+delta/n].  (13)

This is the sharpest uniform bound proved in this stage; it is not claimed
optimal. It counts every raw-input transition, including reset, and does
not hide compensation energy. For the accepted N<=5n log n it gives

    R_history <=delta/F
        +16sqrt(5log n)[delta+delta^2 sqrt(n)/F^2+delta/sqrt(n)]. (14)

For the OLD reviewed 16/15 parameter choice, F~n^(1/15)/10^4 and
delta=10^(-10)F^(-5/2), the dominant term in THIS improved majorant grows
only like n^(1/30)sqrt(log n), versus the old n^(1/3)sqrt(log n).
Neither diverging majorant proves that the actual minimum radius diverges.
We do not attempt to improve the old growing-radius theorem's exponent.

## 7. Uniform constant radius for the new balance

Use (1). For n>=200, log n>=1, log n<=sqrt(n), F<=n^(1/18).

For the logarithm bound, log(x)/sqrt(x) has maximum 2/e<1 on x>=1,
by differentiation and e>2. This inequality is uniform, not an asymptotic
substitution. Also N<=4n log n+2<=5n log n here.

Consequently

    delta<=eta<=1/20,
    delta/F<=eta,
    sqrt(N)*delta/sqrt(n)
       <=sqrt(5)eta F n^(-1/4)(log n)^(1/4)<=3eta,
    sqrt(N)*delta^2/F^2<=sqrt(5)eta^2<3eta^2,
    sqrt(N)*delta/n<=3eta.

The third line follows from F<=n^(1/18), (log n)^(1/4)<=n^(1/8), and
1/18-1/4+1/8=-5/72<0. The fifth line has another 1/sqrt(n) factor.
Therefore (13) yields the rational bound

    R_history <=97eta+48eta^2
               =0.00970048<1/50.                    (15)

This is a WIDTH-INDEPENDENT bound for every point of ONE entire section,
not a bound on independent axes. No shorter window is needed: the existing
N~n log n now fits the fixed radius. We have not asserted that this N is
necessary. Formula (13) also shows explicitly how a different N would enter;
the accepted signal kernel/transfer ledger would need to hold for that N.

## 8. Same accepted query ledger, new amplitude

The reviewed degree-one proof, odd parity, joint chronological/cross-harmonic
tail and dense/polynomial ledger depend only on the stated Fourier/spreading
size conditions and sup ||D_t||<=delta<=1/20. They therefore give for every
boundary antipode pair, in the UNCHANGED actual permitted-query norm,

    H_n >=10^(-17)delta sqrt(n)/F^5-delta-delta^3 sqrt(n)-e,
    e=epsilon/4+2*10^(-9)=0.000250002.                 (16)

Our amplitude gives

    degree-one term =10^(-21) n^(1/4)/[F^4(log n)^(1/4)]
                   >=10^(-21) n^(1/36)/(log n)^(1/4),
    odd tail       =eta^3 F^3 n^(-1/4)(log n)^(-3/4)
                   <=eta^3 n^(-1/12)(log n)^(-3/4)<=eta^3,
    structural term delta<=eta.                      (17)

This pays all mixed nonlinear terms; no relative-tail cancellation is
invented. The full original e is retained. A legal aligned future query
is supplied by the accepted proof; Euclidean norms above bounded only input
energy and transport error, NOT query visibility as a substitute metric.

For n0=10^900, n0^(1/36)=10^25 and log n0=900 log10<2700<10^4.
Hence the lower in (17) is STRICTLY greater than 1000 at n0. The ratio
n^(1/36)/(log n)^(1/4) increases when log n>9, by logarithmic differentiation.
Explicitly its logarithmic derivative is
(1/36-1/(4log n))/n>0. The elementary log10<3 can also be obtained from
the positive exponential series e^3>1+3+9/2+27/6=13>10.
Thus for EVERY n>=n0,

    H_n>1000-10^(-4)-10^(-12)-0.000250002
       =999.999649997999>9>epsilon.                  (18)

Spreading and floor conditions are unchanged: d>=2*10^6,
2F+1<=3n^(1/18)<=d/4096 follows from n^(17/18)>=61440,
F<d/4, d-1>2F, and N>=d. All hold at n0 and thereafter.
The same saturation, injectivity, legal inverse lift, preparation and common
reset apply. In particular the new delta is positive and admitted at ALL
points of the ball; it is not chosen based on certificate failures.

Finally q>=d/(2*10^6) and F>=n^(1/18)/2, so

    D=qF>=n^(19/18)/20,000,000=omega(n).                (19)

## 9. Continuous dimension conclusion and limitations

Compose a continuous K-coordinate encoder with the SINGLE joint section's
boundary sphere S^(D-1). If K<D, Borsuk-Ulam supplies an equal-code antipodal
pair. Uniform physical epsilon answers would give pair query-distance
<=2epsilon, contradicting (18). The buffered strict polynomial/causal
contract is also contradicted, since its allowed decoder error is 3epsilon/4.
No packing count, raw rank, tangent rank or separate-axis count is used.

Thus bounded LOCAL physical radius does not force O(n) in this model. The
all-admitted-history 16/15 theorem remains unchanged; our new bounded-radius
19/18 result is separately derived and awaits independent hostile review.
This does NOT bound absolute input-history energy ||X|| about zero, change
the late-query contract, establish moderate-width behavior, or prove any
finite-bit, GPU memory, learning or architectural consequence. The huge
sufficient n0 is not a practical onset guarantee. Full-model
Omega_c(n^2)--O_c(n^2 log n) bounds remain unchanged: source sections cannot
be multiplied without another joint proof.

The explicit dimension/radius/margin tradeoff of this SAME family is (13)
and (16), with D=floor(d/10^6)F and all size/admissibility constraints stated.
For the convenient radius-safe rule delta=eta F/(n log n)^(1/4), it reads

    radius <=97eta+48eta^2,
    H>=10^(-17)eta n^(1/4)/(F^4(log n)^(1/4))
           -eta F/(n log n)^(1/4)
           -eta^3 F^3 n^(-1/4)(log n)^(-3/4)-e,

in the parameter range used here. We stop at a rigorous superlinear example,
not an optimized exponent or a whole-class robust-dimension upper bound.
