# What the co-rotating screen can and cannot establish

New Codex-derived scoped lemmas, 2026-10-02. Independent review required.
All approximate statements below use the ACTUAL permitted-query metric, the
accepted c1/gamma1/n/epsilon.001 units, and the uniform dense-transfer ledger
in VERIFICATION.md. No tangent rank substitutes for finite-error dimension.

## 1. A genuine Theta(n) subclass: one fixed co-rotating profile

Fix a public locked-step count T, the public zero-memory warmup/source feature,
and one profile z in the protected-coordinate complement (z1=0). Prescribe
memory h_t=O^(t-1) z at the T active steps, then exact zero reset. Restrict z
to whatever profile set makes the WHOLE histories admissible. Model/input
rules and fixed endpoint are unchanged. These histories have r=k-1 continuous
profile degrees. Every continuous robust section therefore has dimension<=r
by Borsuk-Ulam into the profile vector. This is an all-query cap, not a
single-query or operator-rank argument.

A counted exact online description stores z plus an age/phase counter (r+1
coordinates), and n forward-state coordinates while ingesting inputs if not
provided. Extract z from the first active state, continuously; all other
history is prescribed. Public times need no counter if supplied. At a future
query do NOT replay a saved history. Because O^d=I, the physical gate pattern
G_t(z) is d-periodic even though it is NOT constant after conjugation.
Form the one-period affine map on the ACTUAL dense B:

 B -> A_cycle(z) B+C_cycle(z), A_j=G_j R, C_j=G_j E.

For T=pd+s, compose p cycles by

 A_cycle^p Bpre+sum_(j=0)^(p-1) A_cycle^j C_cycle,

then the s-phase affine remainder and final reset. Powers/geometric sums can
be computed by binary affine composition without invertibility assumptions.
All model/phase matrices are transient decoder work computed from counted z;
no history-dependent matrix persists secretly. Decode inherited gradients and
add common future injections. Runtime/transient space are not bounded.
This exact continuous representation handles arbitrary T in this subclass.

The class (with publicly declared T) includes T=1 and the independently verified
L'-1-dimensional one-pulse ball. Thus its worst-case credit memory is Theta(n).
The lower is not asserted separately for every fixed large T. This class is
NOT arbitrary changing age profiles or the full arbitrary aperiodic family.

## 2. Changing latent-cycle profiles: exact invariant support, finite-error cap

The primary screen permits arbitrary zero-sum latent z_t supported in the first
d latent coordinates, transformed to physical memory h_t=U P^(t-1) z_t. It
does NOT restrict the number of profile changes. For such profiles, h1=0 and
all physical NC coordinates equal c_k (P^(t-1)z_t)_1. Consequently all NC
tanh gates are equal at each time, though they need not be periodic.

Let Z_NC be physical NC vectors with coordinate sum zero; dim Z_NC=L-1.
Every O acts as I on Z_NC, and every actual prescribed diagonal reference
gate acts as one scalar g_s(t) there. Their orthogonal complement inside
memory coordinates2..k has dimension d, with an explicit orthonormal basis

 V=[e2,...,e_d, 1_NC/sqrt(L)].

Both O and every gate preserve this decomposition in BOTH directions. Let
O_A=V^T O V and G_A=diag(g2,...,g_d,g_s). Because the injection is the
identity and warmup is block diagonal, the exact reference operator is

 M_t=s_t P_Z+V C_t V^T,
 s_t=g_s(t)[a s_(t-1)+alpha_t],
 C_t=G_A(t)[a O_A C_(t-1)+alpha_t I_d].

There is no assumption that G_A and O_A commute. One scalar plus d^2 numbers
is an EXACT reference representation at every horizon. The actual dense
selected query error is uniformly<=eta_n<2e-9. Thus an explicit continuous
encoder with d^2+1 endpoint credit coordinates (plus n forward coordinates
while streaming) meets epsilon. It stores neither past transports nor gates.

Equivalently, any proposed jointly robust sphere section of dimension>d^2+1
has two antipodes sharing (s,C), by Borsuk-Ulam. Their actual permitted-query
distance is at most2eta_n<2epsilon. It cannot be a robust section. This is a
finite-error upper, not a rank-based heuristic.

For n200/400/1000 these caps are2501/10001/62501. The largest primary
history charts have9800/39600/249000 coordinates; their WHOLE spheres
necessarily contain joint collisions regardless of sampled successes.
The apparent time-coordinate count is therefore not a robust dimension.
For q~ln n, however, q(d-1)<d^2+1: this cap does NOT decide their robustness.

The reduced block is implemented separately in adversary.py and cross-checked
against the full numerical operator; the mathematical argument above establishes
the support. The ledger includes every actual dense leakage row and future query.

SCOPE: zero-sum latent-cycle support. Individually varying NC profile coordinates
would break scalar NC gates. This is not a new upper for the arbitrary
aperiodic accepted family, whose general fixed-feature upper remains r^2.

## 3. Whole-section admissibility of the primary family

Every latent profile equals a zero-sum alternating baseline with coordinate
magnitude<=B, plus a zero-sum perturbation bounded by P. Here B<=.25,P<=.11.
For any mean-zero latent-cycle vector z, its physical transform has protected
coordinate0 and, elsewhere, h_i=z_i+c_k z1. Hence |h_i|<=(1+c_k)(B+P)<=.4.
For adjacent profiles, exploiting actual co-rotation rather than a row-sum bound,

 ||h_t-a O h_(t-1)||infinity
 <=(1+c_k)[(1+a)P+(1-a)B] <.246 for n>=200.

Thus interior input magnitude is bounded by
atanh(.4)-.4+.246+.05<.320. The initial active step is bounded by
atanh(.4)+.05<.4737; the final reset by .4+.05<.45. Actual dense corrections
are at most e times the prescribed state norm, far inside the remaining slack.
The source is H and initial/reset histories are exact. These inequalities apply
to ALL coefficient combinations in each unit ball, not just sampled points.

The spread map tanh(field)-mean(tanh(field)) is injective on the zero-sum
subspace: for unequal zero-sum x,y,
(x-y)^T[tanh(x)-tanh(y)]>0, and subtracting a constant does not change this
inner product. Its product with full-rank public time/space bases therefore
defines a genuine q(d-1)-dimensional HISTORY chart. This says nothing by itself
about credit-space dimension or antipodal margins.

Physical total-input radius is at most
(25/21+a)(P/2)sqrt(Td) for the spread chart; for the linear chart it is at
most(25/21+a)A. Sustained spread radii grow with width/horizon. Total-budget
linear controls have bounded/smaller radii. Report those costs openly.

## 4. Finite-error obstruction for long SUSTAINED profiles

This further lemma applies to the sustained B=.25,P=.11 primary sections
when d is EVEN (all three primary widths have this property). It does not
apply to the total-budget weakening-gate policy, to arbitrary profiles, or
to the stationary-coordinate one-pulse lower section.

Every latent cycled coordinate has |z_i|>=B-P=.14. For physical coordinates
2..d, |h_i|>=.14-c_k*.36>=.10 at EVERY point of the joint section. Thus
their gates are<=u=.99. In the active d-block, only the last coordinate
(uniform NC) can have a gate close to1. The model's global a=1-1/n is NOT
changed: this is history-induced dissipation inside one invariant block.

Let e be that last active unit vector, F=I-ee^T. Its rotation overlap is

 q=e^T O_A e=1-L c_k^2, with0<q<=1/2 for k>=100.

Indeed L>=k/2 and c_k^2>=1/k give the upper bound. The monotone function
(.5t^2+1)/(t-1)^2, t=sqrt(k)>=10, is at most51/81, so q>=10/27>0.

For Gbar=uF+ee^T, any admissible active gate factors as G=D Gbar with
diagonal ||D||<=1. Commutation of D with Gbar and orthogonality of O_A give

 ||G2 O_A G1 O_A|| <= ||Gbar O_A Gbar||.

For unit v the exact two-gate energy loss is

 1-||Gbar O_A Gbar v||^2
 =(1-u^2)[||Fv||^2+||F O_A Gbar v||^2].

The sum ||Fv||^2+||F O_A v||^2 is at least1-|q|>=1/2, because the
two removed unit vectors e and O_A^T e have overlap q. Furthermore
||F O_A v||<=||F O_A Gbar v||+(1-u)||Fv||. The norm of the corresponding
two-component triangular comparison map is <=2-u. Hence

 ||Gbar O_A Gbar||^2
 <=1-(1-u^2)/(2(2-u)^2)
 =1-199/20402.

Set lambda=sqrt(1-199/20402)<1, an absolute constant. Every T-step active
transport, for arbitrary changes of these admitted gates, has norm at most
a^T lambda^floor(T/2). This is a finite, whole-family inequality, not rank.

The public warmup active credit has norm<=n. Summing all NEW identity
injections, and including the final zero reset, gives

 ||C_end||op <= n lambda^floor(T/2)+[2/(1-lambda)+1]
             <= n lambda^floor(T/2)+412.

The safe412 bound follows from1-sqrt(1-delta)>=delta/2 with delta=199/20402.
Retain the scalar NC trace EXACTLY and discard only this active block. Its
ACTUAL all-future normalized query error is bounded by

 eta_n+(a||H||/n)[n lambda^floor(T/2)+412]
 <=eta_n+.3[sqrt(n) lambda^floor(T/2)+412/sqrt(n)].

Thus the entire active-block observable diameter decays as
O(sqrt(n) exp(-const*T)+1/sqrt(n)). In particular, for T>=ceil(sqrt(n))
it tends uniformly to0. For an explicit conservative crossover, n>=10^12
and T>=ceil(sqrt(n)) make the one-scalar encoder's error<.000125<epsilon:
the412 term contributes at most.0001236, the exponentially small warmup
term is smaller than1e-6, and eta_n<2e-9. The warmup bound is decreasing
in sqrt(n) above this threshold; lambda<=exp[-199/(2*20402)].

At the shared fixed endpoint this encoder has ONE continuous credit coordinate,
s. Its online update is s'=g_s(a s+alpha); forward actual h costs n more
while ingesting inputs. Future decoder includes the known direct future
contributions; no past is replayed or stored externally. This answers the
SELECTED FIXED-FEATURE operator queries, not all R/W/b gradient coordinates.
By Borsuk-Ulam,
any section dimension>=2 has two antipodes with the same s. Their query
distance is less than2*.000125<2epsilon. Hence the long sustained class
cannot support a width-uniform superlinear lower section, or even a2D
robust section, at sufficiently large n.

This is an ASYMPTOTIC, CONSERVATIVE certificate of failure of this particular
construction. The enormous explicit crossover is not a prediction for widths
200--1000 and is not used to interpret their actual numerical minima as zero.
T=n/4,n/2,n and eventually T=sqrt(n) fall in its long-window scope.

Two loopholes survive: T only about ln(n) leaves the warmup term uncontrolled;
and B,P scaled as1/sqrt(T) makes the fast-gate gap shrink with T, invalidating
the constant-lambda bound. Their jointly robust width is not resolved here.

## 5. What has not been proved

- No O(n) or O(n polylog n) cap for unrestricted changing profiles. The
  long sustained subclass has the sharper eventual one-coordinate upper above.
- No omega(n) jointly robust section, even for q=ceil(ln n).
- No theorem that weak two-pulse channels contribute only O(1).
- No general dense quadratic merger or necessary logarithm.
- No practical finite-precision, task, architecture, or training claim.

The smallest clean obstruction now lives in the query-visible finite-radius
width of the NONCOMMUTING d-by-d recurrence C'=G_A(aO_A C+I), coupled to
the physical zero-sum latent profiles and shared scalar gate. An all-query
finite-error O(d) summary OR a joint superlinear antipodal lower section for
this exact reachable block would decide the remaining co-rotating loophole.
