# A conservative joint multi-harmonic robust lower section

2026-10-02. Codex derivation, internally checked; independent review required.
This is a new theorem attempt, not a previously accepted project theorem.
Claude's files and historical results are not modified.

## 1. Statement and scope

Keep the accepted dense tanh family, c=1, gamma=1/n, epsilon=1/1000,
group-RMS normalization, legal late-query contract and intermediate gate box.
For every integer

    n >= n0 = 10^504,
    d=floor(n/4), k=floor(n/2), r=k-1, l=n-k,
    F=floor(n^(1/18)), q=floor(d/1,000,000),

the construction below gives ONE continuous closed-ball history section
with parameter dimension

    D=qF >= n^(19/18)/20,000,000.

All its gate words are admitted, all lifted inputs are in the accepted past
input domain, and all endpoints are h=0. Every boundary antipodal pair has
normalized permitted-query half-distance greater than 9, hence greater than
epsilon and also greater than the buffered 5epsilon/4 polynomial threshold.
The deliberately enormous threshold is a sufficient bound, not an optimized
onset or a practical claim. No theorem at moderate width is asserted.

Consequently the accepted continuous no-replay memory model needs at least
D coordinates. In particular its universal O(n) hypothesis is refuted if
the new derivation is correct. The same antipodal lower applies to the strict
finite-jet causal width because the frozen polynomial ledger is included.
The full-model n^2 versus n^2 log n gap is NOT settled by this one-feature lower.

The history section has a stated finite radius for each n. It does not have
a width-uniform Euclidean history radius; that stronger condition is not
claimed. Query/error units are unchanged.

## 2. Accepted model, embedding and parameter probe

Use zero-based physical memory indices 0,...,k-1. Physical index 0 is the
decoupled coordinate omitted from the r-dimensional selected memory block.
Latent cycle indices are 0,...,d-1. Let

    w=e0-1_k/sqrt(k), gamma_U=2/(w^T w)=1/(1-1/sqrt(k)),
    U=I-gamma_U w w^T,
    P=P_d direct_sum I_(k-d), O=U P U,
    a=1-1/n, R0=diag(aO,I_l/(100n)),
    ||R||op=a, e_R=||R-R0||op<=4/(10^8 n^2),
    W=I, b_model=.05*1_n, H=.4*1_l.

R is the accepted fixed dense perturbation, not a new architecture. O fixes
physical e0, and its restriction is O_*. Every sensitivity derivative keeps
the particular history's raw inputs fixed. Gate words are realized by the
accepted inverse tanh input lift; they are not artificial parameter injections.
The parameter definition remains P_n=2n^2+n for independently differentiated
R,W,b. This lower uses only the selected R-gradient block; it does not drop
other parameters or renormalize that block as a smaller model.

For 1<=f<=F define omega_f=2pi f/d and the COMPLEX latent vector

    v_f(i)=exp(i omega_f i)/sqrt(d) on the cycle, zero elsewhere.

Then P v_f=lambda_f v_f with lambda_f=exp(-i omega_f), sum_i v_f(i)=0,
||v_f||2=1, and the physical probe p_f=U v_f has physical coordinate 0 equal
to zero. Thus p_f is an actual unit parameter-side direction in the selected
block, with O p_f=lambda_f p_f. Real and imaginary parts are real permissible
parameter projections with norm at most 1; no complex-valued model is used.
The selected parameter perturbation is K H, not independently selectable
source columns. A unit real memory probe p corresponds to the unit-Frobenius
parameter direction K=p H^T/||H||.

Claude's numerical script used an undressed physical cosine with index 0
removed. That is not exactly the eigenvector above. It remains numerical
motivation only; the following proof uses the exact dressed eigenvector.

## 3. Public recursion, exact first order and parity

Set z0=3/20, g0=1-z0/n, b=a g0, N=ceil(4n log n)+1. The reference is

    M_t=(g0 I+D_t/n)(a O_* M_(t-1)+I), M_0=0.

Its public degree zero and Q_t obey the accepted recurrence. In particular

    Q_t p_f=[1-(b lambda_f)^t]/[1-b lambda_f] p_f.

For ANY word D the exact degree-one column is

    Z_(1,N) p_f = 1/n sum_(tau=0)^(N-1)
       b^tau O_*^tau D_(N-tau) Q_(N-tau) p_f.             (1)

Use a formal scalar multiplying every D_t. The chronological coefficients
are homogeneous of degree j in the WHOLE word. If D_t(-y)=-D_t(y), then

    [M_N(y)-M_N(-y)]/2 = Z_1(y)+Z_3(y)+Z_5(y)+... .     (2)

Even orders cancel exactly. This includes mixed-frequency and differently
ordered products; it is not a commuting approximation. The public final reset
adds I and left-multiplies by aO_*, so its I cancels in (2).

## 4. A fully quantitative spreading lemma

Let A be the real orthogonal projection onto the constant and cosine/sine
cycle modes 1,...,F, and P_perp=I-A on R^d. Its rank is h=2F+1 and

    ||P_perp||_(infinity->infinity)<=2F+2<=4F.

Indeed each row of A has absolute sum at most 1+2F by its Fourier formula.
For h<=d/4096 and d>=2,000,000 there exists a real d-by-q matrix B, q as in
section1, with range in ker A and, for all y in R^q,

    ||B y||2<=2||y||2,
    ||B y||1>=sqrt(d)||y||2/8.                           (3)

Here is an explicit probabilistic existence proof with all constants.
Take B=P_perp G/sqrt(d), with G having independent standard Gaussian entries.
For a fixed unit y, Gy is a standard d-dimensional Gaussian g.

* Since the Gaussian density is less than 2/5, Pr(|g_i|>=1/2)>3/5.
  Exponential Markov with exp(-t)=2/3 shows
  Pr(number of such coordinates <=d/2)<=(.8 sqrt(1.5))^d
  =(.96)^(d/2)<=exp(-d/50). Therefore ||g||1>=d/4 except
  on that event.
* ||A g||2^2 is chi-square of rank h. Its moment generating function at 1/4
  is 2^(h/2), by direct Gaussian integration. Thus
  Pr(||A g||2>sqrt(d)/16)<=2^(h/2) exp(-d/1024)
  <=exp(-d/2048).
* Consequently ||P_perp g/sqrt(d)||1>=3sqrt(d)/16 outside
  these two events, using ||A g||1<=sqrt(d)||A g||2.
* The same chi-square MGF gives
  Pr(||g/sqrt(d)||2>3/2)<=exp(-d/5):
  2^(d/2)exp(-9d/16)<exp(-d/5).

A 1/4-net of the unit sphere in R^q has size at most 9^q (the elementary
disjoint-ball volume argument). Its successful norm bound gives ||B||op<=2.
A 1/64-net has size at most 129^q. On its successful L1 bounds, extension
using ||B||op<=2 gives ||By||1>=5sqrt(d)/32>sqrt(d)/8
for every unit y. A union bound is less than

    9^q exp(-d/5)
      +129^q[exp(-d/50)+exp(-d/2048)]
    <=3 exp(-d/4096)<1.

Here q<=d/1,000,000, log 129<5 and log9<3. This proves (3).
No unknown Kashin constant is used. B can be chosen separately as a fixed
PUBLIC matrix for each n, once and for all, independent of the history.

Also, for every nonzero y, at least d/1024 coordinates of By have magnitude
at least ||y||2/(16sqrt(d)). Otherwise splitting the L1 norm into small and
large coordinates and applying Cauchy-Schwarz to the latter contradicts (3):

    sqrt(d)||y||/8 <= sqrt(d)||y||/16 +2||y|| sqrt(number_large).

## 5. One joint odd saturated section

Write y=(y_1,...,y_F) in the CLOSED unit ball of R^(qF). Define

    L_sat=16sqrt(dF),
    s_f(y)=P_perp tanh(L_sat B y_f)/(4F).                (4)

Tanh acts coordinatewise. Every s_f is continuous, odd, lies in ker A, and
has infinity norm at most 1. At a boundary point some ||y_f||>=1/sqrt(F).
Put z=B y_f/||y_f||. On at least d/1024 coordinates, |z_i|>=1/(16sqrt(d));
there |tanh(L_sat B y_f)_i|>=tanh1>3/4, with the same sign as z_i. Hence

    z^T tanh(L_sat B y_f)>=3sqrt(d)/65536.

Because z is in ker A and ||z||2<=2,

    ||P_perp tanh(L_sat B y_f)||2>=c_sat sqrt(d),
    c_sat=3/131072.

Therefore the selected block satisfies

    ||s_f||1>=||s_f||2^2/||s_f||infinity
             >=c_sat^2 d/(16F^2).                      (5)

This loss of F^2 is deliberately paid; a saturated profile is not silently
assumed to retain its original Fourier orthogonality or a constant spread.

The block map in (4) is injective: for distinct y_f,y'_f,
the inner product of B(y_f-y'_f) with the difference of their projected tanh
vectors is strictly positive, by strict monotonicity of tanh. Projection
does not change this inner product since B(y_f-y'_f) lies in ker A.
The full ball-to-history map is therefore an embedding once the injective
gate-word map in section6 is included (compact domain, Hausdorff image).

## 6. Admitted co-moving gate word and finite history radius

Choose the PUBLIC amplitude

    delta=10^(-10)/F^3.

For tau=N-t and physical cycle index i=1,...,d-1 set

    D_t(i,i)=delta/F sum_(g=1)^F s_g((i+tau) mod d;y)
                                      cos(omega_g tau). (6)

All other selected physical defects are zero. Physical coordinate 0 is not
in the selected block and is not varied. Since ||s_g||infinity<=1,
||D_t||op<=delta<1/10, so z_t=z0-diag D_t remains in [1/20,1/4] at EVERY
point of the whole ball, not merely on separate axes. D(-y)=-D(y).

This particular age pattern has period d, which GROWS with n. It is an
admitted subset of the unrestricted gate cube, not a fixed-period-p class
with p independent of width. No genuine aperiodicity is needed for a lower
against an encoder required to work on every admitted word. It is not a
constant-tail or scalar fixed-profile word.

The gate-word map is injective in the profile arrays: for any line x, one
cycle reveals the cosine polynomial at d-1 distinct phases (the missing
physical node excludes one phase). A nonzero degree-F trigonometric polynomial
has at most 2F circle zeros. Since d-1>2F, all its coefficients are determined.
Together with section5 this gives a genuine continuous history section.

Use the unchanged accepted lift: memory h_t(i)=sqrt(z_t(i)/n) with fixed signs,
source h_t=H, preparation public, and final h=0. Raw inputs are
atanh(h_t)-R h_(t-1)-b_model. The all-word lift theorem ensures admissibility;
the past cube is not confused with the independently specified future-query box.
Inputs are held fixed in the parameter derivatives.

For completeness, a radius about the public zero-defect history is finite:
only d-1 hidden coordinates vary, z0-delta>1/10, and
||h_t-h_t^0||2<delta. The atanh derivative is at most 800/799, and ||R||<=1,
so ||x_t-x_t^0||2<3delta, including the reset. Thus

    ||X(y)-X(0)||2 <=3delta sqrt(N+2)<8delta sqrt(n log n). (7)

This bound is width-dependent, as stated in section1. Every final h is EXACTLY
0; the curved-section compensation is supplied by the exact inverse input lift.

## 7. Exact harmonic kernel: cross-talk treated jointly

Temporarily include the virtual cycle node 0 in (6), and work in latent
coordinates. This is a comparison used in the following identity, not an
admitted independent node control. Let c_t(i) denote that virtual diagonal.
For each f the idealized latent degree-one column I_f has entries

    I_f(x)=delta exp(i omega_f x)/[n sqrt(d) F(1-b lambda_f)]
                         sum_g K_fg s_g(x),             (8)

where

    K_fg=sum_(tau=0)^(N-1) b^tau exp(-i omega_f tau)cos(omega_g tau)
             -b^N lambda_f^N sum_(tau=0)^(N-1)cos(omega_g tau). (9)

Equations (8)--(9) follow directly from (1) and the exact finite Q_t, not
from a stationary resolvent replacement. No harmonic is assumed isolated.

For every REAL x in R^F,

    ||K x||2 >= x^T Re(K) x/||x||2 >=(n/40)||x||2.      (10)

To prove this, the first term of Re(K) is the weighted cosine Gram matrix.
Its first d terms give b^(d-1)d/2 times I by exact cycle orthogonality.
As 1-b<=(23/20)/n and d<=n/4,

    b^(d-1)>=57/80, d>=n/5,
    b^(d-1)d/2 >=57n/800.

The second term has operator norm at most F N b^N. Since F<=n,
b^N<=n^(-4), N<=5n log n, this is <=5log n/n^2<=n/40 for n>=200.
The resulting real quadratic form is still >=n/40 times squared norm.
The inequality for the complex output Kx follows from real Cauchy-Schwarz.

Also

    |1/(1-b lambda_f)|>=d/(8f)>=d/(8F),                (11)

because |1-b lambda_f|<=23/(20n)+2pi f/d<8f/d.

Applying (10)--(11) to the real profile vector at EACH row, and then using
(5) for the largest section block, gives

    sum_x ||(I_1(x),...,I_F(x))||2
       >=delta sqrt(d)/(320F^2) sum_x ||(s_1(x),...,s_F(x))||2
       >=delta c_sat^2 d^(3/2)/(5120 F^4).

At least one f therefore satisfies

    ||I_f||1 >=delta c_sat^2 d^(3/2)/(5120F^5).          (12)

The conversion uses max column L1 >= (sum row L2)/F. It is an algebraic step,
NOT a substitution of RMS/Frobenius visibility for the permitted query norm.
The next sections exhibit the actual permitted query.

## 8. Node-0 and Householder twist corrections

These corrections are not hidden in asymptotic notation. Extend the physical
defect by zero at node0 and let D denote that k-by-k diagonal; let D_hat be
the virtual full-cycle diagonal. For a fixed time/frequency, the zero Fourier
moments of every s_g imply EXACTLY

    sum_cycle c_t(i)=0, sum_cycle c_t(i)v_f(i)=0,
    w^T D v_f=c_t(0)/sqrt(kd),
    w^T D w=-c_t(0)/k, w^T v_f=1/sqrt(d).

Consequently

    U D U v_f-D_hat v_f
      =-c_t(0)e0/sqrt(d)-gamma_U w(w^T D v_f)
        -gamma_U D w/sqrt(d)
        +gamma_U^2 w(w^T D w)/sqrt(d),
    ||U D U v_f-D_hat v_f||2<=6delta/sqrt(d).           (13)

For n>=200 use gamma_U<=10/9, ||w||2<=sqrt2,
||D w||2<=delta sqrt(d/k), k/d<=3. These inequalities directly give (13).
Propagation by the orthogonal P has no norm loss. The exact finite Q_t
factor has magnitude at most 2/|1-b lambda_f|, and
sum_tau b^tau<=1/(1-b)<=n. Therefore the accumulated error after any fixed
orthogonal output transform has L1 at most

    12delta |1/(1-b lambda_f)| sqrt(k/d) <=24delta n.   (14)

Two physical O factors appear after reset and one query. Since sum_x I_f(x)=0
by the excluded profile Fourier moments, the remaining transformation of
the ideal column is U P^2 I_f. It obeys

    ||U P^2 I_f||1 >=||I_f||1-gamma_U||w||1 |(P^2 I_f)_0|.

Here gamma_U||w||1<=2sqrt(k) and
||I_f||infinity<=2delta |1/(1-b lambda_f)|/sqrt(d).
This last dressing loss is at most 8delta n. Combining (14),

    ||O^2 Z_1 p_f||1 >=||I_f||1-32delta n.              (15)

All these quantities are embedded physical vectors; no inaccessible
latent query is used. The sole virtual node contribution was charged in (13).

## 9. Actual legal one-step query and degree-one visible signal

Let g_hi=sech^2(1/4), g_lo=sech^2(3/4), s_gate=(g_hi-g_lo)/2>4/25.
For an exact scalar check, cosh(1/4)<197/191<129/125 by its positive
series and the geometric ratio 1/192 after its first quadratic term;
cosh(3/4)>2651/2048>129/100 by its first three terms. Hence
s_gate>5625/33282>4/25. Also tanh1>3/4 follows from e^2>7:
the exponential series through degree4 sums to exactly 7 and has positive
remaining terms. None of these constants comes from a floating-point fit.
For any real physical vector z, legal future preactivations chosen separately
at 1/4 or 3/4 give

    sup_g |g^T z| = ((g_hi+g_lo)/2)|sum z|+s_gate||z||1.

For a complex column at least one of its real/imaginary parts has L1 at least
half its complex L1; its real parameter projection has norm <=1. Thus a
LEGAL one-step query yields

    nu_(R0)(aO_* Z_1) >= a^2||H|| s_gate/[2 n sqrt(n)]
                                   max_f ||O^2 Z_1 p_f||1
                            >=1/(50n) max_f ||O^2 Z_1 p_f||1. (16)

This uses the unchanged w_R/beta=1/n, head 1_n/sqrt(n) and H=.4*1_l.
Indeed a^2>99/100, ||H||/sqrt(n)>=2/(5sqrt2)>4/15,
and s_gate/2>2/25; their product exceeds 1/50.
No arbitrary adjoint is granted. Future inputs are allowed to realize these
preactivations; they need not lie in the PAST input cube. Source/direct future
terms cancel because the compared current endpoint is h=0.

With (12)--(15), d>=n/5 and 5sqrt5<12,

    degree-one half-signal >=10^(-17)delta sqrt(n)/F^5-delta. (17)

The exact rational constant is stronger:
c_sat^2/(50*5120*12)>10^(-17). The negative dressing term is at most
(32/50)delta<delta IN THIS CONSERVATIVE LOWER EXPRESSION: apply the
1/(50n) query coefficient only after the L1 lower is nonnegative. It is
not a separate upper bound on a query perturbation using a lower coefficient.
If the intermediate right side is negative the displayed lower holds
trivially by nonnegativity; at the final threshold it is strongly positive.

For ONE harmonic f and an orthogonal profile with L1>=rho d, the same proof
gives the more transparent bound

    signal_f >=rho delta sqrt(n)/(200000 f)-delta.

In particular if sqrt(n)>=400000f/rho,
signal_f >=rho delta sqrt(n)/(400000 f). This is a concrete
amplitude*sqrt(n)/f lower in the actual legal-query geometry, including the
physical twist errors. An unqualified scalar coefficient from a numerical
fit is not used as a theorem.

## 10. All nonlinear corrections, including cross-harmonic words

The ACTUAL sup-norm gate amplitude is delta, not the amplitude of one block.
Let

    C_delta=delta/[n(1-b)^2]<=delta n,
    q_delta=a delta/[n(1-b)]<=delta.

The accepted chronological coefficient recursion gives
||Z_j||op<=C_delta q_delta^(j-1), by direct induction with these smaller
amplitudes. Odd antipodal orders j>=3 have query half-error at most

    A_n a C_delta q_delta^2/(1-q_delta^2)
       <=(.3 delta^3 sqrt(n))/(1-delta^2)
       <=delta^3 sqrt(n).                              (18)

This controls degree3, degree5 and above jointly, under the ACTUAL supremum
of permitted queries. It includes every mixed-frequency and chronological
noncommuting word. No assumption of negligible cross terms or a relative
q_n^2 error compared with (17) is made. Amplitude shrinking pays for the
entire tail. In particular delta^2 F^5<=10^(-20)/F leaves ample room in (17).
The same safe A_n upper holds for the reference R0 adjoint using the actual
public beta/weight, because ||R0||op=a. Thus one may first apply (18) to
the reference odd carrier and then transfer its COMPLETE one-step query
to R as in section11; no extra adjoint error per polynomial order is needed.

## 11. Dense transfer and complete structural ledger

At one future step, using the same permitted preactivations, replacing R0 by
R changes the query on any reference endpoint Y by at most

    (||H||/n)e_R ||Y||op.

The reference matrices obey ||M_t||op<=n, since every gate has norm <=1 and
||aO||=a. An antipodal half-difference after reset therefore has norm <=n.
The extra query-side perturbation is <=.4sqrt(n)e_R<2*10^(-9) for n>=200.
The accepted dense-credit and polynomial approximation ledger costs at most
epsilon/4; charging the extra query bound separately is conservative even if
part of it was already inside that ledger. Preparation gives zero selected
credit; any already allowed faded old term is inside the same accepted ledger.

The complete bound for both the actual dense half-distance and, conservatively,
the accepted polynomial half-distance is

    H_n >=10^(-17)delta sqrt(n)/F^5
               -delta-delta^3 sqrt(n)-epsilon/4-2*10^(-9). (19)

Ledger by source:
* finite cycle / early window: exact kernel (9); its bounded finite-Q defect
  is in (10), not charged a second time;
* node0, rank-two/twist and final dressing: <=32delta n in physical L1,
  yielding the <=delta query loss in (17);
* reset: common +I cancels; two O factors and a^2 are explicitly in (16);
* degree3 and all higher odd/cross chronological terms: (18);
* even degrees: exactly zero in the half-difference;
* dense-reference, old-credit and original polynomial ledger: <=epsilon/4;
* extra actual-R one-step adjoint perturbation: <2e-9;
* endpoint/admissibility: exact construction, not an error term.

## 12. Uniform margin, explicit threshold and dimension

Use delta=10^(-10)/F^3. Then (19) is bounded below by

    (10^(-27)-10^(-30)) sqrt(n)/F^8
                       -10^(-10)-1/4000-2*10^(-9).

Since F<=n^(1/18), sqrt(n)/F^8>=n^(1/18). For n>=10^504,
n^(1/18)>=10^28, so

    H_n >9.99-10^(-10)-.00025-2*10^(-9)>9.             (20)

No numerical rank threshold or high-precision midpoint establishes this
inequality: all constants in it are rational and the exponent comparison is
exact. The threshold also ensures d>=2,000,000, 2F+1<=d/4096,
F<d/4 and d-1>2F. For example 2F+1<=3n^(1/18),
d>=n/5, and n^(17/18)>=61440 is more than sufficient for the projection
rank condition; all hold already far below n0.

Finally q>=d/2,000,000 and F>=n^(1/18)/2, so

    D=qF>=n^(19/18)/20,000,000=omega(n).

The weakest margin of this conservative proof grows as n^(1/18); the theorem
only needs the stated width-independent lower 9 beyond n0.

## 13. Continuous encoder lower and what is not concluded

Compose any proposed continuous encoder with the ONE joint section on the
unit sphere S^(D-1). If it has K<D counted coordinates, Borsuk-Ulam gives
one equal-code antipodal pair. A uniform physical epsilon decoder would then
bound their gradient-query distance by 2epsilon, contrary to (20). A strict
finite-jet decoder of error 3epsilon/4 would bound its pair distance by
3epsilon/2, also contrary to the buffered polynomial half-margin in (20).
The same lower holds for a causal encoder because it must in particular
work at the terminal time; causal updates are not used to weaken the lower.

This is a robust antipodal continuous-encoding dimension certificate, not a
claim of a global bi-Lipschitz chart, a bit bound, or an upper bound. There is
one sphere/ball with all combinations admissible; separately visible axes,
an ambient operator ball, a tangent rank or a monomial count play no role.

The exponent 19/18 is deliberately conservative. The sketch's n^(7/6)
exponent and its quoted numeric coefficients are NOT proved. This theorem
does not settle the full-model n^2--n^2 log n gap: independent source sections
cannot be multiplied without another joint admissibility/query proof.
It gives no architecture, training, moderate-width effect, finite-bit/VRAM
bound or production interpretation of epsilon. The new derivation requires
independent hostile review before it becomes an accepted project checkpoint.
