# Holding costs, paired moving corridors, and a sharper temporal kernel

Codex, 2026-10-03. NEW results internally checked; independent hostile
review required. The accepted 3/4 theorem is used without reopening it.
Fixed-feature continuous causal credit only, epsilon=.001, actual legal
future queries, full absolute raw-input norm. No architecture or bits claim.

## 1. Frozen system and two outcomes

Use the accepted n-dimensional dense tanh family:

    k=floor(n/2), l=n-k, d=floor(n/4), r=k-1,
    a=1-1/n, lambda=1/(100n), b0=.05, W=I,
    U=I-gamma w w^T, w=e0-1_k/sqrt(k), gamma=1/(1-1/sqrt(k)),
    P=P_d direct_sum I_(k-d), O=UPU,
    R0=diag(aO,lambda I_l), ||R||=a,
    e=||R-R0||<=4/(10^8 n^2).

Past raw inputs remain in (-.5,.5)^n. Start at zero. Future preactivations
are in [1/4,3/4]^n, head 1_n/sqrt(n); the accepted recurrent-group scale
divided by loss scale is exactly 1/n. All R,W,b entries are differentiated
independently, with realized raw inputs held fixed.

The fixed feature is the UNIT source direction 1_l/sqrt(l). Changing the
public source trajectory below does not change this parameter subspace or
normalization. Source amplitude is always explicitly included in the query.

NEW THEOREM A (polylog improvement). For every integer n>=10^200 and
2<=F<=n^(1/16), one admitted continuous same-zero-endpoint section has

    D>=nF/10^7,
    ||X||2<=4*10^7 n^(3/4)F^(3/2),
    boundary antipodal half-margin >.9997.

Consequently d_F=Omega(n log n) at
R_abs=O(n^(3/4)(log n)^(3/2)). The exponent 3/4 is NOT improved.
For fixed 0<beta<=1/16, eventually D>=n^(1+beta)/(2*10^7) at
R_abs<=4*10^7 n^(3/4+3beta/2). In particular 4/5 gives beta=1/30;
5/6 gives beta=1/18.

NEW THEOREM B (sparse holding and exact nonuniform kernel). For n>=10^6,
positive integers m,T with S=m+T+4<=d/100, and arbitrary continuous
0<beta_(i,t)<.1 on ONE parameter ball (beta_(i,0) public), there is an admitted common-endpoint
reference moving-corridor history, transferred to the ACTUAL R, with

    ||X||2<=2 sqrt(m(T+2)+1).

Only 4m reference coordinates are driven per interior step; all remaining
reference coordinates evolve autonomously. Every dense correcting input
is counted. An explicit coupled projected-credit kernel is proved in
section 5. This is a reachable chart and kernel theorem, NOT a robust
dimension theorem: no margin is inferred from its raw parameter count.

No exponent below 3/4, and no improved general impossibility exponent,
is proved in this stage.

## 2. Exact accepted energy decomposition

For the accepted balanced full-width packet let v_t be its k memory states,
source h_s=.4*1_l, v_0=0, and put

    r_t=atanh(v_t)-aOv_(t-1),
    c_H=atanh(.4)-b0-lambda*.4.

The REFERENCE interior squared input energy is EXACTLY

    E_int^2=l T c_H^2 +k T b0^2
                -2b0 sum_t 1_k^T r_t+sum_t ||r_t||2^2.       (1)

Source holding is the first term. Memory-side bias cancellation is the
second. Memory transport, modulation, and their interference with bias
are the final two terms; they cannot be double-counted as separate positive
costs. Public near-zero holding already costs kTb0^2 at leading order.

Preparation and reset are EXACTLY

    E_prep^2=k b0^2+l(atanh(.4)-b0)^2,
    E_reset^2=||aOv_T+b0*1_k||2^2+l(lambda*.4+b0)^2.           (2)

If beta_max^2=(zeta+delta)/n<=.01, then ||v_t||2<=sqrt(k(zeta+delta)/n),
||atanh(v_t)||2<=||v_t||2/(1-beta_max^2), and orthogonality gives

    sum_t||r_t||2^2<=9(zeta+delta)T,
    |2b0 sum_t 1^T r_t|<=6b0 T sqrt(k(zeta+delta)).            (3)

Actual-R correction adds at most e sqrt(n(T+1)) to the TOTAL norm; it is
charged by triangle inequality, not treated as free. Under the accepted
duration-scaled rule zeta/n->0, the uniform leading coefficient is

    E^2/(nT) -> [c_H(infinity)^2+b0^2]/2,
    c_H(infinity)=atanh(.4)-.05.

Source holding supplies approximately 98.24% of this leading squared cost.
The asymptotic coefficient is approximately .0710568; numerical values
are cross-checked separately, not used in the theorem.

## 3. Autonomous source, and the bias obstruction

There is a unique sigma in (0,1) with sigma=tanh(lambda sigma+b0), since
the scalar map is a lambda contraction. Moreover

    .0499<sigma<.05+1/(100n).

Prepare source sigma*1_l with raw input lambda*sigma per coordinate from
zero; hold it with ZERO reference input. Actual dense corrections are
-(R-R0)h_previous, including source rows, and are all counted. The unit
fixed feature is unchanged. Reset source to zero with input -lambda*sigma-b0.

Reference memory dynamics and prescribed gates are unchanged. Their selected
credit recurrence is identical after dividing out ||sigma*1_l||. All
reference query margins scale by sigma/.4>.12475, including nonlinear
errors. With the new Theorem A parameters, this autonomous-source variant
therefore has half-margin >.124 and the same energy exponent/polylog bound.

Its leading squared holding coefficient is b0^2/2=.00125, versus (1).
This genuinely eliminates extensive source holding, not the memory factor n.
The asymptotic norm coefficient is reduced to about 13.26% of the old one.
The ACTUAL source is nearly autonomous, not claimed exactly autonomous:
the tiny dense correcting inputs are included.

For any full-memory near-zero schedule, ||v_t||infinity,||v_(t-1)||infinity
<=beta, the required memory input satisfies

    ||x_mem,t||2 >=[b0-beta/(1-beta^2)-a beta]sqrt(k)-e sqrt(n). (4)

Thus if beta<=.005, full memory holding costs >=c n per step. Balanced
signs do not remove this norm lower bound. A bath can pay this forcing only
if it has substantial noncritical state, which changes the transport kernel.

An exact zero-preactivation memory configuration would require
v=-(b0/a)O^T1_k. Its coordinate d-1 equals
-(b0/a)[sqrt(k)-gamma/sqrt(k)], eventually outside (-1,1).
This excludes that particular bias-canceling configuration, not every
inhomogeneous bath. A fully autonomous model is an a contraction and has
no nontrivial periodic orbit or exactly neutral mode. The source fixed point
works because its nonzero state supplies feature forcing; its gates are not
used as the long-memory transport.

## 4. A jointly admissible moving-corridor construction

Let S=m+T+4<=d/100, A=2S, B=5S. Use two cycle corridors whose active
coordinates at time t are A+i+t and B+i+t, 1<=i<=m. They are far from
the exceptional row and from wrapping. Use 2m distinct off-cycle compensators.

At each t set BOTH cycle copies to beta_(i,t)>0 and their two compensators
to -beta_(i,t). Hence the total selected sum of the 4m driven states is
EXACTLY zero for every parameter value and time. Initially beta_(i,0) is
public. Every other memory state is tanh(b0), obtained by a ZERO-input step
from the public zero start; source is sigma*1_l. On the 4m prepared states
the raw input is atanh(+/-beta_(i,0))-b0, of magnitude <.151. Source
preparation has input lambda*sigma. Nothing is subtracted as a public center.

At every interior step all nondriven reference states take their exact
zero-input autonomous update. Then override only the 4m driven states as
specified. This is an inverse-lift prescription, not a parameter derivative.

For v_0 removed from the selected block, the accepted exact O row identity is

    J=gamma v_(d-1)/sqrt(k)-gamma^2 sum_selected(v)/k,
    (Ov)_1=J+gamma sum_selected(v)/sqrt(k),
    (Ov)_j=v_(j-1)+J for ordinary cycle rows,
    (Ov)_j=v_j+J for off-cycle rows.                         (5)

The exceptional front occupies at most t rows by time t. Every ordinary
nondriven row outside that front has a common public state u_t; the two
corridors are beyond the front. Their moving support covers the shift of
all previous private deviations. The compensators are stationary.

Inductively ALL nondriven states and J are public: private states sum to
zero, the last cycle state is u_t, and the exceptional front has no private
predecessor. In particular

    sum_selected(v_t)=(r-4m)u_t+W_t, |W_t|<=1.1t,
    u_t=tanh(b0+C_n u_(t-1)-a gamma^2 W_(t-1)/k),
    C_n=a gamma^2[(1+4m)/k-1/sqrt(k)].                      (6)

For n>=10^6 and m+T+4<=d/100, |C_n|<.05,
a gamma^2*1.1T/k<.012. Starting u_0=tanh(b0)<.05, (6) proves |u_t|<.1.
Thus |J|<.12 and |b0+aJ|<.2. On a driven row both current/preceding ordinary
states have magnitude <=.1, so

    |x_ref|<=atanh(.1)+.1+.2<.401<.5.                       (7)

Nondriven reference inputs are exactly zero, even where an autonomous
preactivation is large. No inverse tanh is numerically needed there.

At time T+1 let every nondriven row advance autonomously and reset only the
shifted cycle active set and all compensators to the public ordinary state
u_(T+1). The required inputs are a(u_T-beta_(i,T)) on the cycle and
a(u_T+beta_(i,T)) on compensators, each bounded by .2. All other states were
already public. This gives an EXACT same common endpoint for the whole ball;
it is nonzero and need not be an autonomous fixed point.

Preparation costs <4m(.151)^2+l(lambda*sigma)^2<m+1. Interior costs <=mT;
reset costs <=m. Dense correction costs in norm at most e sqrt(n(T+2)), since
every hidden magnitude <=1. Consequently

    ||X||2<=sqrt(m(T+2)+1)+e sqrt(n(T+2))
            <=2sqrt(m(T+2)+1).                             (8)

This proves Theorem B, including source, bath, preparation, reset, and every
actual correcting input. It makes no finite-error dimension assertion.

## 5. Exact sparse nonuniform credit kernel and legal queries

For every z in {A+2,...,A+m+T}, define the orthonormal paired parameter
vectors p_z=(e_z-e_(z+3S))/sqrt(2). Their translates up to T+2 steps stay
inside matched, ordinary parts of the two corridors and never wrap.
For any vector on this paired subspace, U acts as identity (sum zero),
O acts EXACTLY as P, and matched diagonal gates preserve the pairing.
Off-cycle compensator gates do not act on this subspace. This is why the
new kernel survives a nonuniform autonomous bath; no scalar global resolvent
is assumed.

Let g_(i,t)=1-beta_(i,t)^2. On the final active paired rows, the normalized
reference credit matrix K, from paired parameter coordinates to paired
output coordinates, is EXACTLY

    K_(i,z)=a^(T-j) product_(s=j)^T g_(i,s),
        if z=A+i+j for some 1<=j<=T,
    K_(i,z)=0 otherwise.                                   (9)

The source multiplier is sigma sqrt(l). Each entry is supplied by the REAL
source injection at time j and its chronological transport; entries are
not independently chosen. Earlier preparation has zero selected credit.
All private differences on this parameter frame are supported on the final
active paired rows; outside rows never encounter a private gate along the
relevant co-moving characteristic.

Let Delta K be a difference of two histories. Reset gate is public
g_r=1-u_(T+1)^2>.99. One legal next-step query can choose high/low gates on
each twice-shifted pair independently and equal gates on all other pairs.
Therefore its projected normalized query distance is EXACTLY

    D_(one-step,proj) =
      [sigma a^2 g_r s_gate sqrt(2l/n)/n]
         max_(xi in [-1,1]^m)||Delta K^T xi||2,             (10)

where s_gate=(sech^2(.25)-sech^2(.75))/2>.17.
The coefficient is >=1/(200n). Direct future injections cancel at the
common nonzero endpoint. Raw future inputs realize the preactivation box;
they are not restricted by the PAST input cube. This is the actual worst
one-step query supremum on the projected block, not RMS visibility.
Dense transfer has the inherited <4e-9 half-margin cost.

For completeness, ALL legal future horizons admit a constant-factor upper
on this projected metric. For an ordinary cycle column i, away from wrapping,
||Oe_i-e_(i+1)||2<=6/sqrt(n). In fact for 1<=i<=d-2 its square is
(gamma/sqrt(k)-gamma^2/k)^2+(k-2)gamma^4/k^2, directly from (5).
At n>=10^6, gamma<1.003 makes this <9/n. The stated 6 constant is conservative.
Backward legal adjoints have norm <=q_f^L, q_f=sech^2(.25)<1. Until the
characteristic reaches the exceptional column,

    |c_(L,i)|<=q_f^L(1+6L)/sqrt(n).                        (11)

For our rows that distance is >=d-7S-3>=n/8 for n>=10^6. At longer horizons
the full norm bound q_f^L is <=C/sqrt(n). Taking the maximum over L gives
an absolute C_Q (10^4 suffices, since sup_L q_f^L(1+6L)<100), and
(10)'s infinity-to-L2 operator norm divided by n is
also an upper, up to a fixed C_Q factor, for every permitted future on this
PROJECTED private block. Reset and dense replacement are included as above.
Dense replacement contributes the separately stated additive error; it is
not hidden inside a multiplicative equivalence near zero. This does not
upper-bound the full feature's other parameter blocks.

## 6. Sparse harmonic realization and its current certificate barrier

Write L=m+T-1. Use unit parameter probes on the paired z interval with
coefficients exp(i nu_j z)/sqrt(L), nu_j=2pi j/T. They need not be mutually
orthogonal: only one unit parameter projection is selected by a lower bound.
Their finite interval suffices for every relevant characteristic. Exact
temporal frequencies are available WITHOUT spatial Fourier rounding.

For m>=2*10^6 use the accepted entropy-profile lemma on m tracks with A=0,
q=floor(m/10^6),
one qF-ball, max_j||s_j||1>=m/1024, and the SAME shared gate budget. Set

    g_(i,t)=g0+c_(i,t)/n, g0=1-zeta/n,
    c_(i,t)=delta/F sum_j s_j(i)cos(nu_j(T-t)),
    beta_(i,t)=sqrt((zeta-c_(i,t))/n),
    zeta=.15+2delta, kappa=delta T/n<=1/2.                   (12)

Every old term on a characteristic remains active from injection to endpoint.
Thus (9) gives the EXACT finite Q_t and K_jg identity on these probes, with
omega_j=nu_j. Exact cosine periods cancel startup. If
F(1+zeta)T/(2n)<=1/4096, the diagonal-dominance estimate of section 8 gives
for some j a first-order paired-column L1 at least

    delta T^2 m/(65536 n sqrt(L)F^2).

Even orders cancel on antipodes of the WHOLE word. The same chronological
induction bounds every odd tail, now on m paired output rows. Using (10)
with a correct UPPER coefficient for errors gives the sufficient ledger

    M_sparse >= A_s kappa Tm/[n sqrt(L)F^2]
                      -kappa^3 T sqrt(m)/n-4e-9,
    A_s=10^-9.                                            (13)

No twist term exists on this paired frame; actual dense transfer is paid.
The sparse full history is jointly admitted by section 4. Its margin, if
(13) is positive, is a legal-query lower on the full feature as well.

Optimizing (13) over kappa gives maximum signal-minus-tail

    [2 A_s^(3/2)/(3sqrt(3))]
       T m^(5/4)/[n L^(3/4)F^3]
    <= C_s T sqrt(m)/(n F^3).                             (14)

Therefore a fixed-positive certificate from THIS ledger needs
T sqrt(m)>=c_epsilon n F^3. Its dimension is only qF=Theta(mF).
For D=mF and m<=n this implies

    mT>=c_epsilon n D^3/m^(5/2)
        >=c_epsilon D^3/n^(3/2).                         (15)

For the near-zero durations in (12), actual interior cost is also Theta(mT)
asymptotically: the public bulk is within O(.05^t+T/n) of the root
mu_n=tanh(b0+C_n mu_n), and its ordinary forcing tends to
atanh(mu_n)-a mu_n>=mu_n^3/3, with mu_n>.044. Meanwhile beta_max->0.
After a fixed initial number of steps, each driven input tends to a nonzero
negative constant, so its squared cost is bounded below by a constant.
This assertion requires T=o(n) and beta_max->0, as in the useful packet
range. It is not a cost lower for arbitrary beta schedules in Theorem B.

Consequently this sufficient harmonic certificate cannot beat

    R_abs >=c n^(3/4)(D/n)^(3/2)

when D/n diverges. A vanishing active fraction worsens this certificate
frontier by (n/m)^(5/4) at fixed D. This is a METHOD barrier, not an
impossibility theorem for every sparse chart or allowed history. Its proof
does not count raw rank as robust dimension.

The smallest remaining constructive statement is whether the actual
product kernel family (9), on ONE jointly legal section, can have robust
width omega(n) in the metric (10) with mT=o(n^(3/2)). The answer is not
implied by mT raw gate variables, individually visible axes, or matrix rank.

## 7. Pulse-and-coast source accounting

For a public source alpha_t H, the exact recurrence is

    M_t=G_t(aO_*M_(t-1)+alpha_(t-1)I).

In the scalar baseline, for a harmonic eigenprobe,

    Q_t p_j=[sum_(s=1)^t (b lambda_j)^(t-s)alpha_(s-1)]p_j.

Thus if only J=rho T source times are active, |Q_t|<=J and
sum_t|Q_t|<=JT=rho T^2. The first-order injection budget is at most
delta rho T^2/n; the analogous chronological tail has the SAME rho factor,
not rho^2 by assumption. For regular resolved pulses a replacement
weighted kernel would still be needed to claim a lower bound: counting
pulses is not a minimum-gain proof.

After optimizing the accumulated modulation kappa=delta T/n, the optimistic
ledger is rho T/sqrt(n)[A kappa/F^2-kappa^3]. A fixed margin therefore
requires T to grow by 1/rho. At fixed delta instead, the leading signal alone
would require rho^(-1/2); that is not the optimized duration-scaled regime.
Even optimistically charging only active source times, source cost rho nT then does not improve its
power law; full-width memory cost nT gets worse. Physically holding the biased
source at zero during the inactive times costs extra input, so this favorable
accounting understates, rather than overstates, the obstacle. One isolated source pulse
has J=1 and only O(T), not T^2, forcing budget. The autonomous nonzero
source avoids this duty-cycle loss entirely, but not the memory holding.

No new duty-cycle robust theorem is claimed. Age-multiplexed raw variables
in (9) are products of overlapping suffixes, not independently selectable
operator entries.

## 8. A sharper joint temporal kernel: proof of Theorem A

Keep the accepted full-width balanced state lift and entropy profiles;
all additional off-cycle sensitivities and actual-query errors remain paid.
For nu_j=2pi j/T and rounded omega_j, the ideal kernel is

    K_jg=sum_(tau=0)^(T-1)b^tau exp(-i omega_j tau)cos(nu_g tau),
    b=a(1-zeta/n).

The unweighted, unrounded kernel is EXACTLY (T/2)I when 2F<T.
Since 1-b^tau<=tau(1-b) and |omega_j-nu_j|<=pi/d,

    |K_jg-(T/2)delta_jg|
       <=[(1+zeta)/n+pi/d]T(T-1)/2.                       (16)

Choose T=ceil(10^14 sqrt(n)F^3), delta=10^-6 n/(TF),
zeta=.15+2delta. Then every row's total deviation from (T/2)I is at most

    T[10^-6+9 FT/n].                                     (17)

For n>=10^200 and F<=n^(1/16), FT/n<=2*10^-36, so the bracket is
<1/4096. Select the ONE largest profile from the accepted whole-ball
spread guarantee, ||s_j||1>=d/1024. Without any column-pigeonhole loss,

    ||sum_g K_jg s_g||1
       >=(T/2)||s_j||1-d sum_g|K_jg-(T/2)delta_jg|
       >=Td/4096.                                       (18)

The unchanged resolvent is >=T/(16F), and the word still pays delta/F.
Thus ||I_j||1>=delta T^2 sqrt(d)/(65536 nF^2).
All inherited node/mirror/twist corrections and chronological mixed odd
orders give the new actual-query ledger

    M>=10^-8 delta T^2/(n^(3/2)F^2)
           -100delta T^2/n^2-delta^3T^4/n^(7/2)-4e-9.      (19)

The strict improvement is F^2 instead of F^3. No separate normalization
of profiles, altered metric, new model, or changed epsilon is used.

At the stated explicit parameters:

    leading>=1,
    odd tail<=.0002,
    twist<=200*10^8 F^2/sqrt(n)<=2*10^-65,
    M>.9997.

All accepted general packet conditions hold: T/n<=2*10^14 n^(-5/16),
FT/n<=2*10^14 n^(-1/4), beta_max^2=.15/n+3*10^-6/(TF)<.01,
delta T/n=10^-6/F, (1+zeta)T/n=1.15T/n+2*10^-6/F<1/3,
T<=d/2, 2F<T-1, and the rank-(2F+1) profile net condition is satisfied.
Floors give q>=n/10^7. Full energy remains <=2sqrt(n(T+2)), hence
<=4*10^7 n^(3/4)F^(3/2). Accepted whole-ball injectivity, exact endpoint,
actual legal-query realization and Borsuk-Ulam apply without modification.
This proves Theorem A; no numerical certificate substitutes for it.

The optimized full-width ledger is T/sqrt(n)[A kappa/F^2-kappa^3]. Its
maximum is 2A^(3/2)T/(3sqrt(3n)F^3). Thus T=Theta(sqrt(n)F^3) is the
best order certified by this ledger. The general range F=o(n^(1/8)) meets
rounding asymptotically; the explicit range above is conservative.

## 9. Horizon and energy obstructions; what is NOT resolved

For ANY history of length H from the public zero sensitivity, the true
fixed-feature sensitivity operator has norm <=sqrt(l)H: each injection
has norm <=sqrt(l), and all transports have norm <=a<1. Every actual
future adjoint has norm <=1, and the recurrent normalization is 1/n.
At a common endpoint, direct future terms agree. Therefore

    every antipodal past half-distance <=H/sqrt(n).         (20)

Any robust section needs H>epsilon sqrt(n). This is a general horizon
bound, not an input-energy bound. A prepaid sensitivity carrier would have
to count its preparation horizon and energy; (20) cannot be applied just
to its final packet. With the near-zero full-width condition (4), a packet
whose selected initial credit is zero needs squared energy Omega(n^(3/2)).
This proves a scoped 3/4 barrier, not a universal one.

The accepted global zero-credit bound O((log n+R_abs^2)/sqrt(n)) remains
the strongest general impossibility information: no positive robust credit
at R_abs=o(n^(1/4)). We did not prove an O(n) continuous query quotient
at a higher energy scale. Legal cycle-row spike leverage is order one,
so a uniform off-cycle-style 1/sqrt(n) leverage assumption is false.
Raw Gramian ranks, tangent spectra or finite packings cannot close this gap.

Updated GENERAL exponent bracket is still [1/4,3/4], with the sufficient
polylog factor improved from 9/4 to 3/2. Full-model Omega_c(n^2) to
O_c(n^2 log n) is unchanged. The new moving-corridor kernel (9)-(10)
provides a precise next finite-radius reachability problem, not an asserted
universal compressor or architecture.
