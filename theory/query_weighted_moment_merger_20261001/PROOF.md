# Query-weighted moment merger: centered covariance and an error ledger

2026-10-01. Theory only; new lemmas require independent review.

**The arbitrary-aperiodic quadratic upper bound is NOT proved.** This note gives
an explicit counted continuous packet encoder, an exact centered merger-error
formula, and a horizon-uniform, loss-weighted accuracy certificate for that
encoder. A width-independent packet budget satisfying the certificate on ALL
histories remains unproved. No logarithmic robust lower is obtained either.

## 1. Premises, scope and unchanged units

Use the accepted actual rotating/dense family, without reselecting R:

    h_t=tanh(R h_(t-1)+W x_t+b), h0=S0=0,
    theta=(R,W,b), P=2n^2+n, Z_t=S_t D_theta,
    gamma=c/n, a=1-gamma,
    k=floor(n/2), l=n-k, L=max(1,ceil c),
    d=min(k,floor(n/(4cL))), delta=1/(100n),
    R0=diag(a O,delta I_l), O^d=I_k, O orthogonal,
    W=I, b=(1/20)*1, ||R||op=a,
    ||R-R0||op=e<=4/(10^8 n^2).

O is the previously accepted Householder-conjugated rotation; all entries of
actual R,W,b are independently differentiated. Actual past inputs remain in
(-1/2,1/2)^n. Sensitivity differentiation holds the realized inputs fixed.

The frozen parameter multipliers and head normalization are

    w_R=||R||F/n, w_W=||W||F/n, w_b=RMS(b),
    q=1/sqrt(n)*1, beta=max(1,||R||F), epsilon=1/1000.

An actual allowed future continuation has effective current adjoint c_q with
||c_q||<=kappa_Q=a/beta. This note does not replace allowed queries with
arbitrary scalar losses. A Euclidean adjoint ball is used only as a conservative
upper envelope in proving accuracy for the actual permitted family.

The accepted surrogate and transfer premise, with ACTUAL h,x,G throughout, is

    G_t=diag(1-h_t^2),
    F_t phi=w_R phi_R h_(t-1)+w_W phi_W x_t+w_b phi_b,
    Zbar_t=G_t R0 Zbar_(t-1)+G_t F_t,
    ||Z_t-Zbar_t||op<=e C/gamma^2, C<6/5,
    delta_dense=kappa_Q e C/gamma^2
               <=48/(5*10^8 c^2 sqrt(k)).              (1)

All actual future injections are included exactly. The encoder approximates
only the past term Z^T c_q. Storing true current h costs n coordinates; if h
is supplied, omit those n. Every history-dependent packet, mass, source trace,
clock and error ledger below is counted. No discarded-history replay or tape.

The target in this note is already open on THIS hard family. A construction
using its public O would not, by itself, prove an upper bound for every dense
R with the same norm gap. The general class must not be silently replaced by
this parameter family.

The accepted diagnostic motivates these calculations but is not a premise of
any lemma. Its source-restricted RMS spectra and small complete-history spectra
establish no uniform error, packet bound or robust dimension.

## 2. Exact shared-feature packets

Let p=2n+1. A feature array f consists of

    f_j=(f_j^R,f_j^W,f_j^b) in R^n x R^n x R,
    j=0,...,d-1.

For memory-row parameter perturbations phi define the linear sensitivity map

    M_f phi=sum_j O^j [w_R phi_R,mem f_j^R
                       +w_W phi_W,mem f_j^W
                       +w_b phi_b,mem f_j^b].          (2)

A packet (Q,f) represents Q M_f, Q in R^(k x k). Its feature and transport
coordinates number d p+k^2. Features are shared between parameter rows; no
parameter columns are being made independently selectable by the history.

Use weighted feature rows

    v_j(f)=(w_R f_j^R,w_W f_j^W,w_b f_j^b) in R^p.

Linearity gives M_(f1+f2)=M_f1+M_f2. If f+=a g times the cyclic shift
j<-j+1 mod d, then

    M_f+=a g O M_f.                                    (3)

This is an algebraic consequence of O^d=I, not a periodic-gate assumption.

## 3. Exact centered covariance of a two-packet merger

Take any two packets (Q1,f1),(Q2,f2) and alpha in [0,1]. Replace them by

    Q*=alpha Q1+(1-alpha)Q2,
    f*=f1+f2.

The post-merge minus pre-merge sensitivity residual is

    r=Q* M_f* - Q1 M_f1 - Q2 M_f2
     =-(Q1-Q2) M_v,
    v=(1-alpha) f1-alpha f2.                           (4)

This identity retains the transport--feature association. It is NOT the
incorrect replacement of sum Q_s M_s by one sum of transports times an
unrelated sum of features.

Put Delta Q=Q1-Q2. Form V in R^(d x p) whose j-th row is

    V_j=(w_R v_j^R,w_W v_j^W,w_b v_j^b).

For any actual permitted adjoint c_q, put z=Delta Q^T c_q and

    B(z)=[z,O^T z,...,(O^(d-1))^T z] in R^(k x d).

The R, W and b parameter groups in r^T c_q are the respective columns of
-B(z)V, reshaped into the actual parameter order. Their squared Euclidean
norms add; hence the EXACT merger query error is

    ||r^T c_q||_2=||B(Delta Q^T c_q)V||F.              (5)

Define

    K(V)=sum_(j,l=0)^(d-1) (V_j dot V_l) O^j (O^l)^T. (6)

Expanding the squared Frobenius norm proves

    M_v M_v^T=K(V),
    K(V) is symmetric positive semidefinite,
    ||r^T c_q||_2^2=c_q^T Delta Q K(V) Delta Q^T c_q.  (7)

For example, alpha=1/2 makes v=(f1-f2)/2 and reproduces the quarter factor
in the familiar centered product covariance. The factor must not be lost.

### 3.1 Only d orbit autocorrelations determine K

Since O^j(O^l)^T=O^(j-l) and O^d=I, let

    b_s=sum_j V_j dot V_(j-s mod d), s=0,...,d-1.

Then

    K(V)=sum_s b_s O^s, b_s=b_(d-s mod d).             (8)

Thus the feature part of the exact merger covariance reduces to d scalar
autocorrelations and public matrix powers. No history-dependent n by P tensor
is needed to evaluate this formula. K or its eigenvalues can be computed in
transient workspace from the COUNTED packet features; if b_s or K are retained
between steps, their d or k^2 coordinates must be counted additionally.

The actual family of queries has exact one-step merger distance

    sup_(c_q in C(h)) sqrt(c_q^T Delta Q K(V) Delta Q^T c_q).

A conservative bound valid for EVERY actual permitted continuation is

    kappa_Q sqrt(lambda_max(Delta Q K(V) Delta Q^T)).  (9)

No claim is made that (9) equals the allowed-query supremum. High correlation
of selected RMS columns cannot be substituted for a bound on (7).

## 4. Remove the full old-credit mass from a merge

Attach a nonnegative mass mu_s to each packet, with invariant

    mu_s>=sum_j ||v_j(f_s)||_2.                       (10)

Whenever mu1+mu2>0 choose

    alpha=mu1/(mu1+mu2), mu*=mu1+mu2.

The invariant survives f*=f1+f2 by the triangle inequality. The centered
feature array satisfies

    sum_j ||V_j||
       <=(1-alpha)mu1+alpha mu2
        =2mu1 mu2/(mu1+mu2)
       <=2 min(mu1,mu2).                              (11)

Since ||O^j||op=1, (2) and (6) give

    ||M_v||op=sqrt(||K(V)||op)
              <=sum_j ||V_j||<=2 min(mu1,mu2).

Therefore

    ||r||op<=2 min(mu1,mu2) ||Q1-Q2||op.              (12)

If one packet is a fresh injection of mass <=C, then (12) never multiplies
the transport mismatch by the entire old C/gamma accumulator. This is a
genuine improvement in the merger residual estimate. It is not yet a small
total gradient-error theorem: many residuals may still accumulate.

### 4.1 Coherent stationary feature credit cancels exactly

Let Pi=(1/d)sum_j O^j, the projector onto ker(I-O). Consider ONE feature
channel for which both packets have

    v_j(f_s)=b_s,j f0, b_s,j>=0,
    mu_s=||f0|| sum_j b_s,j, f0 !=0.

For the mass-weighted alpha above, sum_j V_j=0. Since O^j Pi=Pi,

    M_v^T Pi=0, K(V) Pi=Pi K(V)=0.                   (13)

Proof: B(Pi z) has all columns Pi z, so B(Pi z)V=(Pi z)(sum V_j)=0;
then (7) implies the stated PSD-kernel restriction.

This removes the stationary coherent feature component BEFORE it is acted
on by the gate/transport mismatch. It does not require Q1,Q2 to commute with
O or with any gate. A constant source-feature channel is an actual example:
its R_mem,source injections remain shared even while memory gates vary.

Qualification: alpha must use THAT channel's feature mass. A mass from a
larger heterogeneous R/W/b tuple need not cancel its particular subchannel.
Separate channels/packets require separate counted storage. For general
varying features sum V_j need not be zero, and (13) must not be asserted.

The large coherent old-credit gain in the previous pulse obstruction therefore
does not, by itself, refute centered mergers. Its removal does not prove that
every remaining nonstationary covariance is weak.

## 5. A horizon-uniform loss-weighted error theorem

This lemma is more general than the rotating family. Suppose state Jacobians
A_t obey ||A_t||op<=a<1. Choose public lambda with a<lambda<1 and set

    D_t=(I-A_t A_t^T/lambda^2)^(1/2),
    E_t=A_t E_(t-1)+r_t, E0=0,
    H_t=D_t^-1 r_t.                                  (14)

D_t is the positive definite square root; the strict lambda>a makes it
invertible even if all gates equal one. H_t is a proof quantity computed
from the decoder residual, NOT an uncounted persistent tensor.

For any terminal actual adjoint c, propagate p_T=c,
p_(t-1)=A_t^T p_t. Define ptilde_t=lambda^(-(T-t))p_t. Then

    ptilde_(t-1)=(A_t/lambda)^T ptilde_t,
    ||ptilde_t||^2-||ptilde_(t-1)||^2
                      =||D_t ptilde_t||^2.

Telescoping over the ACTUAL history yields

    sum_t ||D_t ptilde_t||^2<=||c||^2.                (15)

Variation of constants, with a unit parameter vector phi, gives

    phi^T E_T^T c
      =sum_t lambda^(T-t) (H_t phi)^T D_t ptilde_t.

Vector Cauchy--Schwarz and (15) prove

    ||E_T^T c||^2
       <=||c||^2 ||sum_t lambda^(2(T-t)) H_t^T H_t||op
       <=||c||^2 sum_t lambda^(2(T-t)) ||H_t||op^2.  (16)

This controls all gate-history variation and is not a tangent argument. It
uses no full old-credit norm. The matrix Gram in the first bound is NOT
stored for free; the second bound has a counted scalar implementation:

    nu_t=||H_t||op,
    z0=0, z_t=lambda^2 z_(t-1)+nu_t^2.

For all actual allowed future adjoints,

    error_history(T)<=kappa_Q sqrt(z_T).              (17)

If nu_t<=eta for all t, then

    error_history(T)<=kappa_Q eta/sqrt(1-lambda^2)    (18)

uniformly in horizon. More generally the discounted ledger condition in
(17) suffices without a per-step eta cap.

### 5.1 Diagonal loss metric for the hard rotating memory block

Here A_t=a G_mem,t O, so

    D_t=diag(sqrt(1-(a/lambda)^2 g_t,i^2)).

Use lambda=(1+a)/2=1-gamma/2. For a merged pair, (7) gives the exact
loss-scaled residual norm without storing a k by P_mem matrix:

    nu_t^2=lambda_max[
       D_t^-1 Delta Q K(V) Delta Q^T D_t^-1].        (19)

All matrices in (19) are current transient evaluations of counted state.
This is a loss-weighted covariance, not a new parameter/query normalization.

With k/n>=2/5 and kappa_Q<=2/sqrt(k),

    1-lambda^2=gamma(1-gamma/4)>=3gamma/4,
    kappa_Q/sqrt(1-lambda^2)<=sqrt(40/(3c)).          (20)

Once delta_dense<=epsilon/2, the WIDTH-INDEPENDENT sufficient per-step bound

    eta_*=(epsilon/2) sqrt(3c/40)                    (21)

ensures total actual gradient error<=epsilon at every horizon by (1),(18).
At c=1 this is eta_*=0.0001369306394..., a bound on the LOSS-SCALED residual,
not a changed gradient epsilon. No numerical measurement establishes (21).

When g_t,i=1, D_t,i is of order sqrt(gamma); a merger must then be correspondingly
accurate in that row. Strong gate dissipation permits larger raw residuals.
This is the cost that an unqualified 'old credit is query-invisible' argument
would have hidden.

## 6. Explicit bounded-packet continuous online encoder

Fix m>=1 publicly, independent of n and horizon if a quadratic count is desired.
Preallocate m triples (Q_s,f_s,mu_s), initially all zero. Retain source-row
eligibilities of size l p, initially zero. The actual forward state/gates/features
are used at every step. Gates may be arbitrary, non-scalar and aperiodic.

Let g=max_i G_mem,t,ii. Actual tanh gates are strictly positive; max is continuous.
Normalize the common scalar into feature moments. Advance every packet by

    Q_s^-= (G_mem,t/g) O Q_s O^T,
    f_s^-=a g cyclic_shift(f_s),
    mu_s^-=a g mu_s.                                 (22)

(3) verifies Q_s^- M_f_s^-=A_t Q_s M_f_s EXACTLY. Form a fresh packet

    Q_new=G_mem,t/g,
    f_new,0=(h_(t-1),x_t,1) g, f_new,j=0 for j!=0,
    mu_new=g sqrt(w_R^2||h_(t-1)||^2
                  +w_W^2||x_t||^2+w_b^2).           (23)

Its decoder is the exact new G_mem,t F_mem,t injection. Its mass is <=C,
and is positive because w_b=.05>0. Merge it with one publicly scheduled slot
using sections3--4. All other slots retain their advanced packets. The schedule
can be round-robin and depends only on the counted clock, never on a discontinuous
argmin over history-dependent scores. Computing a fresh packet/merged covariance
is transient workspace, not an extra persistent history slot.

The masses satisfy (10). Their sum obeys

    mu_total,t<=a mu_total,t-1+C<=C/gamma.

The Q norms remain <=1: (22) is a contraction/conjugation, and a merge is a
convex average. Since mu_new>0, the merger denominator never vanishes, even
when the scheduled old slot is empty. An empty slot merges exactly.

Source row i keeps its 2n+1 normalized surrogate eligibilities, updated by

    E_source,i,t=G_source,t,ii [delta E_source,i,t-1
                      +(w_R h_(t-1),w_W x_t,w_b)].

Features and gates are ACTUAL; the propagation uses the reference delta,
and (1) handles the difference from actual dense sensitivity. Source gates
are unrestricted. No gate-history coordinate is omitted.

The feature updates, positive scalar normalization, mass-weighted merger and
source updates are continuous on the admissible history domain. Max, spectral
norm and the positive-definite inverse used for the ledger are continuous;
differentiability is not required. At each fixed n, actual preactivations are
bounded by a sqrt(n)+.55, so actual gates have a positive model-dependent lower
bound. Continuous extensions may clamp the scalar denominator below that public
bound outside the admissible domain. No equality test for scalar gates is used.
Public clock schedules have continuous extensions between their integer times;
they contain no history-dependent branching.

At the decoder, reconstruct sum_s Q_s M_f_s and the counted source eligibilities
in transient dense workspace. Answer the actual future query with this past term
and exact future direct injections. Do not reconstruct discarded histories.

The pre-merge sensitivity obeys A_t Zhat_(t-1)+B_t; its post-merge residual is
exactly (4). E_t=Zhat_mem,t-Zbar_mem,t therefore obeys (14). Compute (19) and
update the ONE scalar z_t in (17). This is an unconditional, online error ledger,
not an uncounted future-query oracle.

### 6.1 Exact persistent coordinate count

    K_m=m[k^2+d(2n+1)+1]+l(2n+1)+2.                 (24)

The +1 per packet is its mass. The final +2 are the clock and z ledger.
Add n when true current h is not supplied. Public O,R,W,b, parameter weights,
lambda and other model constants are uncounted as agreed. No history-dependent
Gram, inverse, singular vectors, discarded features or transport matrices are
hidden in a cache. Runtime/temporary workspace are not bounded by this theorem.

For even n at c=1 when d=n/4 is integral,

    K_m=(3m/4+1)n^2+(m/4+1/2)n+m+2.

For fixed m,c,epsilon this is O_c(n^2). This STORAGE count is unconditional.
Uniform epsilon accuracy is NOT unconditional: the exact sufficient requirement is

    sup_T z_T <=[(epsilon-delta_dense)/kappa_Q]^2.    (25)

Every time (25) holds, (1),(17) prove accuracy for ALL allowed late queries,
not only a bank of probes. If (25) fails, the error certificate fails; this
does not itself prove that the actual allowed-query error exceeds epsilon.

Scalar-memory consistency check: when every G_mem,t is scalar, Q_s=I in
all nonempty slots, after absorbing g into (22)--(23). Thus Delta Q=0 at each
nonempty merge and z=0. This is a consistency check, not a reproving of the
accepted scalar theorem. Arbitrary source feature variation is retained.

### 6.2 A real aperiodic history defeats the simplest one-packet decoder

This is a method-specific counterexample at the accepted c=1, not a memory
lower and not an experiment. On the accepted O, e1 is exactly stationary:
U e1=1/sqrt(k)*1, the middle permutation fixes that uniform vector, so
O e1=e1. Orthogonality also gives e1^T O=e1^T.

Let n>=200, N=n^2, T=N+1, a=1-1/n and

    M=floor(log(1/2)/log(a)), sigma=2/5, H=sigma*1_l.

For s=1,...,N prescribe

    h_mem,s=(1/sqrt(n))*e1+v_s e2,
    v_s=s/[10n(N+1)],
    h_source,s=eta_s H,
    eta_s=+1 if N-M+1<=s<=N, and -1 otherwise,
    h0=hT=0.                                        (C1)

Every interior first memory gate equals a. The second gate varies strictly
with s, other memory gates equal one, so g=max G_mem=1. This is nonscalar,
aperiodic and genuinely noncommuting: for d>=50, e2 is not a +/-1 eigenvector
of the Householder-conjugated d-cycle, hence [E22,O]!=0. The e1 component of
the commutator is zero, so the varying e2 gate cannot alter the e1 calculation.

For clarity, the non-eigenvector claim follows by applying U to e2. Its first
d coordinates have one distinguished near-one entry at coordinate2, an entry
1/sqrt(k) at coordinate1, and the same negative value at all coordinates3..d.
They are neither constant (the +1 eigenspace of a cycle) nor alternating
(the -1 eigenspace if d is even). d>=50 excludes the exceptional tiny cycles.

Realize actual x_s=atanh(h_s)-R h_(s-1)-b. Memory input magnitudes at R0
are <.2: 1/sqrt(n)<=.071, v_s<.0005, the orthogonal memory action has norm
at most a sqrt(1/n+.0005^2), and b=.05. Source input magnitudes are at most
atanh(.4)+delta*.4+.05<.477, even at the sign switch and reset. The dense
correction e||h||<1e-6 preserves the original cube. The exact endpoint is zero;
parameter differentiation holds these realized inputs fixed.

Inspect ONLY K=delta R_(row1,source columns), an actual parameter block.
On R0 these sensitivities stay entirely in e1. The terminal reset gate is one;
all interior e1 gates equal a. Setting j=N-s for the R injection of h_s at
time s+1 gives the exact raw reference coefficient

    A_n=sum_(j=0)^(M-1)a^(2j)-sum_(j=M)^(N-1)a^(2j)
        =[1-2a^(2M)+a^(2N)]/(1-a^2).                 (C2)

The one-packet feature sum has only the a discount, because g=1. Therefore
its corresponding coefficient is

    B_n=sum_(j=0)^(M-1)a^j-sum_(j=M)^(N-1)a^j
        =[1-2a^M+a^N]/(1-a).                        (C3)

All O^j leave the parameter-row vector e1 fixed. Every Q of the encoder
preserves e1 and has norm<=1, so its raw selected decoder coefficient is
q_T B_n with |q_T|<=1, regardless of the feature masses used by the merger.

The floor in M ensures 1/2<=a^M<1/(2a). Thus

    |B_n|<=1/a+n a^N,
    A_n/n>=[1-1/(2a^2)]/(1+a).

Using a>=199/200 and a^N<=exp(-n)<=6/n^3 gives, for n>=200,

    (A_n-|B_n|)/n> .24.                             (C4)

Explicit rational bounds are
19601/79202 for the first term and 1/199+3/4000000 for the subtracted term;
their difference exceeds 6/25. In decimals the first is >.24748 and the second
is <.00503.
This elementary bound does not rely on a numerical rank or certificate engine.

Use the ACTUAL permitted one-step future input (9/20)*1 from hT=0. Its gate
is kappa I, kappa=sech^2(1/2)>3/4. The reference adjoint on e1 is
a kappa/(beta sqrt(n)). With w_R/beta=1/n, the selected-group error is

    D0=a kappa sigma sqrt(l/n) |A_n-q_T B_n|/n
      >(.99)(.75)(.4)(.7)(.24)=.049896.              (C5)

All other parameter groups are retained and cannot cancel a Euclidean error
in this selected group. The future direct R injection is zero at hT=0.

The true actual dense error differs from the reference bound by at most

    delta_dense+2C e/(beta gamma)<1e-6.              (C6)

For (C6), both Zbar and the bounded-packet decoder have operator norm<=C/gamma
(their row-parameter groups are disjoint); the actual one-step adjoint differs
from the reference by <=kappa e/beta. The accepted transfer supplies the first
term. Therefore the specified one-packet decoder has actual permitted-query
error >.048 at unchanged epsilon=.001 on this real aperiodic fixed-h history.

In the n->infinity limit (C2)--(C5) yield kappa sigma/(4 sqrt(2)), about .0556.
This limit is interpretation; the finite inequality already establishes failure.

**Scope:** this rules out the decoder (22)--(23) with m=1 and its shared cyclic
features, not every decoder of its state and not all O(n^2) encoders. It does
not involve log n independent credit packets. A p=2n+1 eligibility vector for
the reference's exact independent e1 mode fixes its credit for ALL histories;
the already counted dense transfer still bounds the actual-model discrepancy.

### 6.3 Hybrid repair that counts the easy independent mode

Treat e1 as an additional exact local row rather than as a packet row. Store
its p coordinates with update

    E1_t=G_t,11 [a E1_(t-1)+
              (w_R h_(t-1),w_W x_t,w_b)].            (C7)

O preserves the orthogonal physical coordinate subspace spanned by e2,...,ek;
diagonal gates also preserve it. Its restricted O' is orthogonal, (O')^d=I.
Run the packet and ledger method on that (k-1)-dimensional block, with all
actual h/x feature columns still included. Source and e1 rows are exact for
the surrogate; dense leakage remains handled by (1).

The counted persistent state becomes

    K_m,hybrid=m[(k-1)^2+d(2n+1)+1]
                +(l+1)(2n+1)+2.                    (C8)

Add n for current h when needed. The same loss-weighted theorem and sufficient
eta_* apply, using the original full-family kappa_Q bound. This repair removes
(C1)--(C6) without replay or a new architecture. It does NOT prove the required
ledger bound on the remaining block.

The much larger stationary eigenspace Pi is not generally preserved by diagonal
gates, unlike physical e1. Giving that entire subspace arbitrary dense parameter
eligibilities costs more than (C7), and a projection onto it is not closed under
the general gated recurrence. The remaining obstruction cannot be dismissed by
copying the one-row repair onto every eigenvector for free.

## 7. Why the universal quadratic accuracy theorem is still missing

A proof that a fixed m=m(c,epsilon), with a public or continuous merge policy,
satisfies (25) for EVERY admissible history has NOT been obtained.

The new residual formula removes large shared coherent features, but leaves
the centered nonstationary transport--feature covariance. Neither O^d=I nor
small RMS diagnostic tails controls that covariance on arbitrary histories.

At one orbit boundary, a general gate word is

    A_t ... A_(t-d+1)=a^d H_t,
    H_t=G_t O G_(t-1) O ... G_(t-d+1) O.

H_t is not generally scalar or identity. Successive H_t need not commute or
repeat. The parameter injection features change along the SAME history; they
cannot be detached and re-assigned independently. The covariance in (7) is
precisely the information lost by such a reassignment.

For (22)--(23), a mass-weighted merge has ||r_t||op<=4C by (12), since
mu_new<=C and ||Delta Q||op<=2. This bound is horizon-uniform and avoids the
old C/gamma multiplier. But the ordinary contraction sum yields only

    actual error<=delta_dense+4 kappa_Q C/gamma
                =O_c(sqrt(n))                        (26)

on this family, not epsilon. The loss-scaled ledger is sharper when the residual
is aligned with genuine dissipation, but a uniform proof of that alignment/size
is absent. A proof may also exploit cancellations that our scalar z overbounds.

For the sufficient criterion, the smallest remaining object is

    z_T=sum_(t<=T)lambda^(2(T-t))
          lambda_max[D_t^-1 Delta Q_t K(V_t)
                       Delta Q_t^T D_t^-1],          (27)

on actual causally generated packets. It must stay <=(25) with m independent
of n and T. The discounted average condition is of order epsilon^2 c; a
pointwise bound such as (21) is sufficient, not necessary.

A small spectral rank, a positive model correlation, or a bounded one-packet
mass is NOT a proof of (27). Adaptive minimum-score merges would additionally
need a genuinely continuous implementation; storing a selected basis/transport
without counting it is not permitted. No free branch or stored future adjoint
is introduced here.

## 8. What future-query quotienting does and does not permit

For each current h define the actual future-query seminorm

    ||E||_(C(h))=sup_(c in C(h))||E^T c||.

Fix any admissible next input with true Jacobian A_v and next true state h'.
Every later allowed query c' from h' produces A_v^T c' in C(h) by prepending
that input. Therefore

    ||A_v E||_(C(h'))<=||E||_(C(h)).                  (28)

This uses actual future dynamics and head normalization; future injections
cancel in sensitivity differences at the same h. Thus a residual already
uniformly epsilon-invisible to ALL future queries cannot reappear above that
scale just because subsequent gates rotate it. A restricted RMS/probe bank
does not have this hereditary property in general.

The accepted exact observability result means the exact invisible subspace
is zero where its stated hypotheses hold. Approximate metric balls still
exist, but are not free linear quotients with a proven O(n^2) recursive chart.
Repeated NEW merger residuals must be controlled; (28) alone cannot assign
epsilon to each of infinitely many merges and add no error.

## 9. Does the obstruction yield an Omega(n^2 log n) lower?

No. Equations (7),(27) isolate an obstruction to THIS merger proof. Failing
the scalar ledger can be conservative; even actual failure of a fixed packet
policy rules out only that policy, not every continuous encoder.

A logarithmic lower would still need ONE jointly robust exact-fixed-h section
of dimension Omega_c(n^2 log n), with a width-independent antipodal margin
above epsilon under the same allowed future losses. Every cohort's gates and
features must be jointly realized with admissible inputs. Counting many
noncommuting transports, summing ranks from different histories, or treating
cohorts as independently selectable parameter columns does not establish it.

Centered cancellation (13) shows why repeating large stationary old-credit
gains cannot automatically supply new robust cohorts. The remaining candidates
would have to encode independent NONSTATIONARY covariance directions, while
surviving damping, normalization and shared injection constraints. No such
construction or impossibility theorem is proved here.

## 10. Checks, prior art and stop

The new proofs use elementary shared-feature algebra, PSD covariance and
adjoint-energy/Cauchy--Schwarz estimates. They are not a new architecture or
primitive, and require independent hostile mathematical review.

Related established tools include switched-system balanced truncation and
deterministic matrix sketching. The former supplies system-reduction/error
frameworks, not the constant packet/debt bound (27) for this coupled nonlinear
history class; the latter supplies sketch guarantees, not a deterministic
all-history, all-late-query continuous sensitivity encoder at this state count.
No theorem from these sources is invoked without its hypotheses:
[Petreczky--Wisniewski--Leth](https://arxiv.org/abs/1302.0221),
[Frequent Directions](https://epubs.siam.org/doi/10.1137/15M1009718).

Manual mathematical checks: injection row layout and frozen units; feature-shift
identity; merger sign/weight; parameter-gradient Frobenius correspondence;
PSD covariance/autocorrelation indices; mass invariant; coherent-channel
qualification; positive loss metric; adjoint rescaling and telescoping; scalar
ledger count; source trace scope; positive normalizer and update continuity;
all-query dense transfer; distinction between sufficient certificates and
actual error/lower bounds. No automated tests, numerical experiments, training
or GPU/CUDA work were run. No GAS-0 or historical evidence was modified.

**Conclusion:** an explicit O_m(n^2) continuous streaming packet state and
uniform error formula are established, but a constant m giving uniform
epsilon accuracy for arbitrary aperiodic histories remains OPEN. General
Omega_c(n^2) to O_c(n^2 log n) bounds are unchanged. STOP this theory stage.
