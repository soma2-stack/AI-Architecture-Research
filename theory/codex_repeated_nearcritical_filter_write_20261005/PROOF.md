# Repeated near-critical writing: a joint robust two-control filter theorem

Codex, 2026-10-06. THEORY ONLY. New author proof; independent hostile review
required. STATUS=PROVED refers to the scoped K=2 theorem below, NOT improved
growing-K dilution. Verified historical results are premises, not reopened.

## 1. Theorem and limitations

For every integer n>=10^1000 there is one jointly admissible continuous
B^2 section in the frozen dense tanh fixed-feature family, with one source
feature, two fixed Frobenius-orthonormal recurrent parameter probes, three
public near-critical survivor filter words, exact public final donor traces,
and one exact common nonzero endpoint. Both donor controls act at EVERY
primary write step, simultaneously. No separate donor epoch is used.

Let W=ceil(10^60 n^(3/4)), L=ceil(1000 log n), T=W+L, N=T+1. Then

    actual boundary antipodal pair distance >1000,
    half-margin >500, epsilon=.001,
    mT <10^60 n^(5/4),
    ||X_raw||_2 <3*10^30 n^(5/8).                    (1)

The COMPLETE finite control-to-two-spatial-read antipodal matrix can be
chosen with minimum singular value >=10^(-54) W after trace matching and
reset. Responses here are normalized by sigma sqrt(l), as in M_t v. Thus
for this fixed K=2 the useful protected gain is Theta(W), with a very small
width-independent constant. These are TWO spatial reads of one fixed unit
probe in the stated two-probe space, not a claim that every K-column gradient
matrix has that minimum singular value.

This does NOT improve D>=n^(3/16)/3, prove alpha<1/2 for growing K, or lower
the superlinear energy threshold. The large constants/width threshold have
no practical-onset, finite-bit, VRAM, architecture, or generic-RNN meaning.

## 2. Model, complete sensitivity, and premises

Use k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,
gamma=1/(1-1/sqrt(k)), c=gamma^2/k. The selected-memory orthogonal map is

    O_*=C+1u^T+e_1 v_H^T,
    u^T=gamma e_(d-1)^T/sqrt(k)-c1^T,
    v_H^T=gamma1^T/sqrt(k).                           (2)

The fixed source is sigma 1_l, .0499<sigma<.051, feature f_s=1_l/sqrt(l).
For any fixed unit recurrent action (Ev)f_s^T, with REALIZED inputs frozen,

    x_0=0, x_t=G_t(a O_* x_t-1+v), ||x_t||<=t.       (3)

Preparation precedes t=0 and has zero recurrent forcing. The required
physical start is zero. Source/node-0 reference responses outside this
selected action are public; actual dense leakage is charged in section 9.

Dependencies used as accepted premises:

- ../codex_unpaired_corridor_sensitivity_20261003/PROOF.md: full recurrence,
  four-site moving tuples, inverse lift, endpoint, queries and dense ledger.
- ../codex_private_renewal_gamma_20261003/PROOF.md sections 2--6: corrected
  dense ledger, exact renewal, public bath/front cap <=.9992, and complete
  two-step complement contraction.
- ../codex_multicolumn_spatial_write_20261005/PROOF.md section 4: the same
  complement bound applies to a high set with at least 2m physical sites.
- ../codex_single_block_spatial_write_20261004/PROOF.md: exact donor low-tail
  trace correction and zero-sum survivor protection through reset.
- ../codex_multisurvivor_hadamard_write_20261005/PROOF.md: accepted prior
  structural checkpoint; the new repeated write is not its single-pulse case.

No front is discarded. No perturbative truncation in the number of
Householder insertions, support-localization principle, or frozen-matrix
monotonicity assertion is used.

For explicit completeness, M_t=G_t(aO_*M_(t-1)+I), M_0=0. Put
L_t=G_t(aCL_(t-1)+I), H_t=M_t-L_t, J_t=u^T M_t and B_t=v_H^T M_t.
With Phi_C(t,s)=(aG_t C)...(aG_(s+1) C), identity at t=s,

    H_t=sum_(s=1)^t Phi_C(t,s) aG_s
                       [1 J_(s-1)+e_1 B_(s-1)].

Here J,B are PRIVATE ROW VECTORS, determined by L+H, not public forcings.
Equivalently, with Phi(t,s)=(aG_t O_*)...(aG_(s+1) O_*),

    M_t=sum_(s=1)^t Phi(t,s)G_s.

These are exact finite chronological identities. They retain terminal,
public-front/bath and every repeated feedback insertion. Equation (7)
below is their exact projected recurrence with a bounded COMPLETE residual,
not a truncation of either path sum.

## 3. One simultaneous history family

Put

    p=2floor(sqrt(n)/10), m=5p/2, h=2p,
    eta=10^(-6), delta=10^(-30), g_H=1-n^(-2), g_L=.995.

Use five equal cohorts of p/2 tuples: D1,D2,S1,S2,S3. Each tuple has two
moving cycle sites and two fixed compensators; a cohort has h=2p physical
sites. All tuples use the accepted geometry A=2(m+T+4), B=5(m+T+4).

For theta in the WHOLE cube [-1,1]^2 the primary W steps have constant rates

    lambda(theta)=(eta+delta theta_1, 3eta+delta theta_2, eta, 2eta, 3eta),
    g_i,t=1-lambda_i(theta)/W, t=1,...,W.             (4)

Every donor control acts repeatedly at all W steps. The survivor words are
different PUBLIC words, not renamed identical schedules. 0<lambda_i<4eta,
so all gates are legal and in (.994,1). Each tuple's prescribed states are
(+sqrt(1-g),+sqrt(1-g),-sqrt(1-g),-sqrt(1-g)), with exact zero state sum.
The source/bath/front trajectory is therefore public and independent of
BOTH controls. Its complete chronological gate bank remains in (3).

During the following L steps, restore all survivors to public g_H. Donors
use g_L for L-1 steps and the analytic last-step trace correction of section 8.
Then apply one public reset to the accepted common nonzero state.

Let d_j,s_j be unit indicators of the p compensators of D_j,S_j. Define

    v_j=(d_j-s_j)/sqrt(2), j=1,2,
    V=[v_1,v_2], V^T V=I_2,
    v=(v_1+v_2)/sqrt(2).                              (5)

All three are FIXED stationary zero-sum probes, O_*v_j=v_j, and v is unit.
No time-dependent parameter direction or extra source feature is selected.
The actions (Ev_j)f_s^T are exactly Frobenius-orthonormal. A gradient's
projection onto v is a valid lower witness within their two-column space.

The accepted inverse lift realizes every word in (4) and every correction
as actual raw inputs in (-.5,.5)^n, starting from zero. It is used only to
generate histories; it is NOT differentiated. Different theta change the
first prescribed donor state, so the history section is continuous and
injective. Its restriction to Euclidean B^2 is the section used below.

## 4. Nonperturbative reduction to a controlled five-cohort flow

Let A_t contain ALL 4m driven sites and let H_t be the supported sum-zero
space. Uniform g_H on A_t and the actual public gates off A_t give a
comparison propagator for which H_t is exactly reducing. Its complete
complement has the accepted forced bound 16000n/m per unit forcing. This
uses full O_*, including bath, terminal and exceptional-front feedback.

Replace actual driven gates by g_H only for this comparison. The actual
perturbation on A_t is at most ell/W, ell=4eta. Since ||x_t||<=t<=W,
the complementary forcing has norm <=1+ell. Consequently the actual
complement q_t=(I-P_H,t)x_t satisfies, throughout the primary write,

    ||q_t||<=B:=16000(1+ell)n/m<35000 sqrt(n).        (6)

This is variation of constants for the entire complement, not a first
renewal approximation. Public front slots at GLOBAL time, including any
bank present in the schedule, obey the same bound; no front restart occurs.

Within-cohort sum-zero components are also exactly reducing for arbitrary
cohort-scalar gates. In the co-moving unit cohort-mean basis, write z_t for
the five-cohort mean part of P_H,t x_t. Its sum is zero. Put

    P=I_5-11^T/5, Lambda=diag(lambda),
    w=(1,1,-1,-1,0)^T, f=w/(2sqrt(2)).

The cohort-mean forcing of v is exactly f. The exact projected equation is

    z_t=a(I-P Lambda/W)z_t-1+f-P Lambda f/W+e_t,
    ||e_t||<=ell B/W.                                (7)

Indeed O_* maps the high sum-zero space isometrically with the moving
labels. Its complementary component is orthogonal before the nonuniform
gate, and can enter (7) only through G_actual-G_comparison. Within-cohort
zero-sum components cannot feed cohort means. Thus (7) has no hidden
unbounded forcing from omitted private modes.

The operator D=P Lambda P on 1^perp is self-adjoint positive, norm <=ell.
The comparison Euler scheme y_t=(I-D/W)y_t-1+f is a contraction. Summing
the a-1 drift, gate-forcing difference and (7)'s error gives

    ||z_W-y_W||<=W^2/(2n)+ell(1+B).

Euler/exponential telescoping and the Riemann-sum error, using norm D<=ell,
give ||y_W-W integral_0^1 exp(-Ds)f ds||<=ell+ell^2<=2ell. Hence UNIFORMLY
on the whole control cube,

    ||z_W-W Z(lambda)||<=E:=W^2/n+sqrt(n),
    Z(lambda)=integral_0^1 exp(-P Lambda P s) f ds.   (8)

The exponential acts on 1^perp; it is not a replacement for the actual
system without the explicit error E. All Householder paths are resummed
in (6)--(8). At our threshold E/W<3*10^60 n^(-1/4)<=3*10^(-190).

## 5. Two protected spatial reads and the continuum Jacobian

On survivor cohorts define raw rows

    q_1=(0,0,-1,0,1), q_2=(0,0,1,-2,1),
    Q rows=q_1/sqrt(2), q_2/sqrt(6), QQ^T=I_2.       (9)

Putting these normalized patterns uniformly on all h physical sites per
cohort gives unit overlapping survivor reads xi_1,xi_2. They have zero sum
and ||xi_j||_infinity<=1/sqrt(h). They are private spatial reads: the
survivor local compensator trace is public, so its comparison cancels.

Let F(lambda_D1,lambda_D2)=Q Z(lambda) with the three survivor rates fixed.
We prove a quantitative derivative bound at lambda_0=eta(1,3,1,2,3):

    sigma_min(J_0)>=eta^3/10^5=10^(-23),
    J_0=partial_(lambda_D1,lambda_D2) F(lambda_0).    (10)

This will only be used together with a finite-radius remainder bound.

### 5.1 Exact signs and determinant: fourth order is necessary

For raw rows q_1,q_2 and raw forcing w, differentiate
sum_(j>=0)(-P Lambda P)^j w/(j+1)!. Let J_raw^(4) include orders j<=4.
Exact multiplication gives

    [ -eta/15+19eta^2/300-49eta^3/1500,
      -eta/15+13eta^2/100-41eta^3/300;
       eta^2/60-29eta^3/1500,
       eta^2/60-49eta^3/1500 ].                      (11)

Its determinant has leading term -eta^4/4500; the remaining polynomial
has absolute value <2eta^5 at eta=10^-6. Stopping at third order gives
the wrong leading determinant constant: fourth-order contributions are
also of determinant order eta^4. All signs in (11) are independent exact
rational multiplications, not inherited frozen spectral conventions.

Since ||P||=1, ||Lambda_0||=3eta, ||w||=2 and ||Q_raw||=sqrt(6), the
column derivative tail after order 4 has norm at most

    5 sum_(j>=5) j(3eta)^(j-1)/(j+1)! <4eta^4.

The matrix tail is <6eta^4. The leading matrix in (11) has Frobenius norm
2eta/15; the remaining terms are bounded by eta^2 in Frobenius norm at
eta=10^-6. Adding 6eta^4 proves that both raw Jacobians have norm <=eta.
The 2-by-2 determinant perturbation therefore costs at most
12eta^5+36eta^8. Thus

    |det J_raw|>=eta^4/4500-14eta^5-36eta^8
                >eta^4/9000,
    sigma_min(J_raw)>eta^3/9000.                    (12)

Multiplication by diag(1/sqrt(2),1/sqrt(6)) and 1/(2sqrt(2)) yields
(10), since 18000sqrt(12)<10^5. No numerical determinant is proof of (12).

### 5.2 Uniform finite antipodes

Along the whole rate square, D is positive and its exponential contracts.
Two differentiated Duhamel integrals give

    ||D^2 F[alpha,beta]||<=||alpha||_2 ||beta||_2/3. (13)

This follows from ||P diag(alpha)P||<=||alpha||_2, ||f||<1, ||Q||=1,
and integral_0^1 s^2 ds=1/3. Therefore, for ||theta||_2<=1,

    F(lambda_0+delta theta)-F(lambda_0-delta theta)
       =2delta Jbar(theta) theta,
    ||Jbar(theta)-J_0||<=delta/3,
    sigma_min(Jbar(theta))>.99*10^(-23).            (14)

The two donor components are embedded in the first two rate slots.
Equation (14) is an exact finite segment integral, not tangent-rank
reasoning. It applies to EVERY boundary antipode simultaneously.

By (8), the complete reference read pair at the primary write end is

    2delta W Jbar(theta)theta+r_theta, ||r_theta||<=2E.

For a unit boundary theta, this is 2A_W(theta)theta, where
A_W=delta W Jbar+r_theta theta^T/2. Its minimum singular value is at least
delta W(.99*10^-23)-E. This explicitly supplies a COMPLETE finite
antipodal control-to-read matrix, with no omitted renewals.

## 6. What accumulates, and what does not

The gates differ by only O(delta/W) each step. But they differ at ALL W
steps while credit grows, so the exact Duhamel forcing in (3) accumulates
order delta W. After cancellation of public survivor local traces, two
spatial moments retain a gain bounded below by a constant times W.
The upper ||x_t||<=t supplies the corresponding O(W) bound. There is no
zero-temporal-moment telescoping: this is a fixed stationary probe and a
repeated RATE modulation, not a translated moving-cycle probe.

The constants are tiny because the weaker spatial direction appears at
high order in the small rate eta; W's large fixed coefficient compensates.
This does not turn a single-pulse signal into an order-W signal. It lies
outside the accepted pulse-only obstruction at every primary time step.

## 7. Exact private versus local trace

During the primary write the direct donor compensator trace is exactly

    tau_j,W=g_j sum_(s=0)^(W-1)(a g_j)^s,
    g_j=1-(lambda_0,j+delta theta_j)/W.              (15)

The public survivor traces use the analogous public rates. A large donor
local trace is not counted as the desired private signal. On survivors,
the direct forcing/history is the SAME at theta and -theta. Their read
difference in (9) is therefore entirely in H=M-L, even before the tail.
Fixed stationary probes inject no local cycle columns.

## 8. Trace correction and exact common endpoint

Run every donor low for L-1 steps. Let tau_target,j be the trace obtained
by running g_L for ALL L tail steps from the PUBLIC theta=0 primary trace.
Use at the last donor tail step

    g_last,j(theta)=tau_target,j/(1+a tau_prev,j(theta)). (16)

This exactly matches both donor traces. Each correction is independent,
continuous and legal. All traces are <=N and
g_L^(L-1)<2n^-5, so |g_last,j-g_L|<=2N n^-5; in particular
.994<g_last,j<.996. The simultaneous diagonal norm is a maximum, not a
sum of donor charges. Every final local column of L_N V is public.

Throughout the tail the survivor gates are UNIFORMLY g_H. Their full
supported zero-sum subspace is exactly reducing, independently of all
donor corrections and full private J,B renewal. The protected difference
from (9) is multiplied exactly by (a g_H)^L. Fresh forcing is identical
and cancels. It does not leak into donor/local trace corrections.

The one PUBLIC actual hidden-state reset gives exactly the same complete
nonzero endpoint to all histories. Its common survivor gate q_N>.98 and
cycle transport multiply the zero-sum read by a q_N. Put

    beta=(a g_H)^L a q_N>.97.                        (17)

Thus the reference finite post-reset antipodal matrix has minimum gain
>=beta[.99 delta W 10^-23-E]. The protected spatial signal survives while
the apparent donor local signal is matched away. No sensitivity reset or
control-policy differentiation is used.

## 9. Dense comparison and actual protected matrix

For e_R=||R-R0||<=4/(10^8n^2), the complete physical one-probe past-state
discrepancy divided by sigma sqrt(l) is <=e_R N(N-1)/2 per history. This
includes source/node-0 leakage and every dense path. It perturbs the
finite two-read pair matrix by at most e_R N(N-1)/2 on unit antipodes.
Combining (10), (14), (17), and the envelopes in section 11 gives an ACTUAL
normalized-state finite antipodal matrix A_actual(theta) with

    sigma_min(A_actual(theta))>=10^-54 W             (18)

for every unit theta. Its exact definition is the segment-average model
matrix plus the rank-one representation of the COMPLETE bounded residual
on that theta, not a fictitious affine equality across all controls.

For query comparison use the CORRECTED inherited uniform ledger

    e_R sigma sqrt(l)[q_f N(N-1)/n+14N/n],
    q_f=sech^2(.25)<.941,

or its accepted <=8e-9 pair charge in the admitted horizon. The old
incorrect printed dense bracket is not reused. All current histories
satisfy that horizon and the hypotheses of this complete ledger.

## 10. Actual normalized legal queries and robust B^2

The full metric is nu=(sigma sqrt(l)/n) sup_legal Q ||Delta M^T c_Q||.
There is one source feature, head 1/sqrt(n), recurrent group factor 1/n,
future preactivation box [.25,.75], and frozen realized future inputs.
The common actual endpoint cancels direct future terms. We use legitimate
one-step witnesses inside the arbitrary-horizon query family.

For either unit spatial pattern xi_j, placed at its NEXT-time support,
take two future gate patterns g_mid +/-s_gate xi_j/||xi_j||_infinity,
s_gate=(sech^2(.25)-sech^2(.75))/2>.17, equal off that support. They
correspond to actual legal preactivations. The SAME selected query is
applied to both histories. Two-query triangle inequality and projection
onto fixed unit v give

    nu_ref>=sigma sqrt(l)a s_gate/(n sqrt(n))
                     |xi_j^T O_* Delta M_N v|/||xi_j||_infinity. (19)

At least one of the two row reads of a unit antipodal pair is
>=sqrt(2)*10^-54 W. Since h>=.39sqrt(n), the coefficient in (19) is
>.003n^(-3/4). Consequently the reference pair lower exceeds
.003sqrt(2)10^6>4000; the ACTUAL pair is >4000-8e-9>1000.
Using the reference version of (18)'s lower is sufficient here; dense
state and dense query comparisons are NOT double-subtracted from the
same claimed ledger. These deliberately conservative final numbers
leave ample room in either route.

Every unit theta is covered, not just axes or separately chosen histories.
Borsuk--Ulam gives D>=2 in the accepted continuous-memory contract: a
one-coordinate continuous encoder on this common-endpoint B^2 has equal
encoded antipodes, which cannot both be approximated to error .001 under
a common legal query when their pair distance is >1000.

## 11. Floors, all-integer range, and FULL absolute input energy

At all n>=10^1000, .49sqrt(n)<=m<=.5sqrt(n), h>=.39sqrt(n),
W>=10^60 n^(3/4), N<2*10^60 n^(3/4). Hence

    E/W<3*10^60 n^(-1/4)<=3*10^-190,
    e_R N^2/W<32*10^52 n^(-5/4),
    N/n<2*10^60 n^(-1/4)<1/400.                     (20)

These errors are far below delta*10^-23=10^-53, yielding (18).
The geometry m+T+4<=d/100 holds with a strict margin. At n_0 the logarithm
bound log n_0<3000 makes L<3*10^6+1, negligible compared with W>=10^810.
The envelopes n^(-alpha) and log(n)/n^alpha decrease thereafter. Floor
errors are bounded by fixed 5 in m and 4 in h; they only improve relatively.
Thus this is an every-integer proof, not three high-precision samples.

Tail/reset loss is >.97 by q_N>.98 and total high decay <=2(L+1)/n.
Primary rates have min eta-delta>0 and max <4eta; W ensures all g>.994.
The correction bound 2N n^-5 improves monotonically. No gate, front,
geometric, dense, or reset exception is left outside these envelopes.

The accepted FULL inverse-lift norm bound, including zero-start preparation,
source/bath construction, every interior donor/survivor drive, compensators,
low tail, both trace corrections, dense lift and reset, gives

    ||X_raw(theta)||<=2sqrt(m(T+2)+1)<3*10^30 n^(5/8),
    mT<10^60 n^(5/4)=o(n^(3/2)).                    (21)

The public center is not subtracted. These are constructive energy UPPERS,
not reversed necessities. No R Walsh stages are needed for this K=2 theorem.
Physical driven support is 4m, of which 3h survivor sites are shared by
the two overlapping reads. Repeated writing is counted for all W steps.

## 12. General K: the constant-rate extension is poorly conditioned

Only AFTER proving K=2, consider a constant-rate bank with C total equal
cohorts, K donor rates controlled inside a bounded positive interval and
K+1 or more PUBLIC survivor rates lambda_i in [0,ell]. In the projected
cohort model z'= -P Lambda z+f, the private survivor response is

    y_i(1)=integral_0^1 exp[-lambda_i(1-s)] q(s) ds,
    q(s)=1^T Lambda z(s)/C.                          (22)

The direct survivor forcing is public and cancels in comparisons. The
shared scalar q is computed from the full projected flow, not prescribed.
For a unit forcing, ||z(s)||<=s. A directional donor-rate derivative has
norm <=s^2/2. Therefore the Euclidean norm of the K-coordinate derivative
of q is <=(1+ell/2)/sqrt(C)<2/sqrt(C).

Taylor approximation of the PUBLIC survivor exponential to degree p
has uniform remainder <=e^ell ell^(p+1)/(p+1)!. Across all survivor rows,
the derivative read matrix is within operator norm

    2 e^ell ell^(p+1)/(p+1)!                         (23)

of the common polynomial row space of dimension p after centering
(degree zero cancels). Orthonormal read rotations do not increase this
error. Taking p=K-1 proves the limiting minimum-gain upper

    sigma_min(J_K)<=2 e^ell ell^K/K!.               (24)

The same row space works for segment-averaged finite Jacobians. The
canonical finite matrix obtained by adding the rank-one residual as in
section 5.2 therefore has the scoped upper

    sigma_min(A_K)<=2delta W e^ell ell^K/K!
                        +2E+dense_state_charge.    (25)

This matrix bound alone does not bound the response on its own theta:
the matrix changes with theta. There is also a genuine finite-boundary
statement. Taylor-truncated, centered survivor outputs lie in ONE public
space of dimension <=K-1. Borsuk--Ulam on the continuous B^K control
family gives antipodes with equal truncated outputs. The derivative
remainder (23), integrated along their control segment, and the complete
uniform state error (8) give at those antipodes

    ||protected read pair||/2
       <=2delta W e^ell ell^K/K!+E+dense_state_charge. (26)

This uses the nonlinear continuous truncated-output map, not raw Jacobian
rank as dimension. Tail/reset do not expand the protected zero-sum reads.
For m~sqrt(n), W=C0 n^(3/4), fixed ell,delta,C0, K=n^b with 0<b<1/2
(provided integer cohort sizes remain legal), (26)/W is O(n^(-1/4))
plus a factorial tail. Thus THIS protected-read protocol cannot have a
uniform gain >=c K^(-alpha) for alpha<1/2, since b alpha<1/4.
This is not an upper bound on complete legal-query visibility: other
parameter probes and output modes are not coded by (26). Nor does it
cover arbitrary time-varying filter words.

No general growing-K robust lower is proved and no alpha<1/2 scaling
is achieved. Nonuniform TIME-VARYING survivor words can leave (22)--(24).
The new K=2 theorem shows real accumulation, but extrapolating its small
constant as K-independent would be invalid.

## 13. Repository consequences and precise review target

New K=2 private gain survives exact trace matching and is Theta(W), so the
single-pulse obstruction is genuinely escaped. Best reviewed polynomial
dimension remains D>=n^(3/16)/3; beta is unchanged. Global superlinear
Omega(n log n) at O(n^(3/4)(log n)^(3/2)), energy bracket [1/4,3/4], and
full-model Omega_c(n^2)--O_c(n^2 log n) are unchanged.

Hostile review should attack: the full complement-to-five-cohort bound
(6)--(8); the fourth-order determinant and tail in (11)--(12); finite-radius
Duhamel control (13)--(14); trace matching without erasing the zero-sum
survivor response; the normalized query/dense transfer and every-integer
envelopes. For (24)--(25), check that the upper is scoped to constant-rate
survivor words and a minimum-gain question, not generalized to all credit
or counted packets as continuous dimension.
