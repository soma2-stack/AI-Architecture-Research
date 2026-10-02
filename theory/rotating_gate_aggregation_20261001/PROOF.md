# Rotating gated credit: compact aggregates and method-specific obstructions

2026-10-01. New author-derived lemmas for independent review. Theory only.
The general arbitrary-horizon logarithmic gap remains OPEN. No other
contraction regime, new architecture, training or numerical witness search.

## 1. Unchanged model and precise scope

Fix c>0, epsilon=1/1000 and sufficiently large n. Let gamma=c/n, a=1-gamma.
The actual frozen predictor remains

    h_t=tanh(R h_(t-1)+W x_t+b), h0=0,
    theta=(R,W,b), P=2n^2+n, S_t=D_theta h_t.

All parameter entries are independently differentiated. Realized inputs are
held fixed for those derivatives. Past inputs remain in (-1/2,1/2)^n.
Use the accepted frozen group-RMS multipliers

    w_R=||R||F/n, w_W=||W||F/n, w_b=RMS(b), Z=S D_theta.

The accepted future scalar head is q=1/sqrt(n)*1, divided by
beta=max(1,||R||F). A future continuation has effective current-state
adjoint c_q with ||c_q||<=kappa_Q=a/beta. The future direct parameter
injections are part of the answer and are computed exactly from the actual
current h and continuation. Only the past term Z^T c_q is approximated.

Continuous persistent state, no unaccounted tape/replay, fixed public model
constants, and unrestricted decoder work are the accepted computational
model. Count n more coordinates when the actual current h is not supplied.
No bit, runtime, finite-precision, learning or architecture conclusion follows.

The owner-accepted worst-case dense-class bounds are still

    Omega_c(n^2) <= d_rob(n,epsilon) <= O_c(n^2 log n).

The accepted finite O_c(n)-horizon result is Theta_c(n^2). A theorem for a
restricted history class below is not a general upper for all histories.

## 2. The SAME hard rotating family and a reviewed transfer bound

Use the family in gamma_c_over_n_quadratic_20261001/PROOF.md unchanged:

    k=floor(n/2), l=n-k, L=max(1,ceil c),
    d=min(k,floor(n/(4cL))), J=Ld,
    delta=1/(100n), W=I, b=(1/20)*1,
    R0=diag(a O,delta I_l), O=U(P_d direct_sum I_(k-d))U^T.

Here U is the accepted Householder matrix, O is orthogonal and O^d=I_k.
The final accepted fully dense R satisfies

    ||R||op=a, ||R-R0||op=e<=4/(10^8 n^2),

and R, R^-1 have no zero entries. Its parameter values are not reselected.
The earlier n0(c) implies a>=1/2, a^J>=3/4, k/n>=2/5, l/n>=1/2 and

    L sqrt(d/n)>=7/20.                                  (1)

We may require n>=10c additionally in the new low-rank lemma, so a>=9/10.
This is a sufficiently-large-width condition, not a model modification.

Let G_t=diag(1-h_t^2) on the ACTUAL dense trajectory, and F_t denote the
normalized ungated injection

    F_t phi=w_R phi_R h_(t-1)+w_W phi_W x_t+w_b phi_b.

Then ||F_t||op<=C<6/5, and B_t=G_t F_t. The reviewed surrogate lemma is

    Zbar_t=G_t R0 Zbar_(t-1)+B_t,
    ||Z_t-Zbar_t||op<=e C/gamma^2.                       (2)

It holds uniformly over every history and horizon. For this rotating family
beta>=a sqrt(k)/2 at large n, hence kappa_Q<=2/sqrt(k), and its late-query
error is at most

    kappa_Q e C/gamma^2<=48/(5*10^8 c^2 sqrt(k)).         (3)

The issue is realizing Zbar compactly. General memory gates make its exact
row support broad. The next two theorems give compact realizations under
explicit history restrictions; they do not silently impose those restrictions
on the general problem. The actual dense forward predictor is never replaced.

## 3. Theorem: arbitrary-horizon quadratic aggregation with scalar memory gates

Suppose only that every ACTUAL memory gate has the form

    G_mem,t=g_t I_k, 0<=g_t<=1.

The common scalar may vary arbitrarily with the history and time. Source
gates may vary independently and nonlinearly. No periodicity is needed.
Use the first memory coordinate's actual gate as g_t; this defines a continuous
update even off the restricted class, without a discontinuous equality test.
This history class contains the entire accepted quadratic lower section,
whose memory states are zero, while its source histories have independent
continuous variation. The restriction is on past memory gates only; allowed
future queries are unchanged and need not satisfy it.

For j=0,...,d-1 store feature moments

    f_j^R in R^n, f_j^W in R^n, f_j^b in R.

Starting from zero, cyclically shift all three arrays by j<-j+1 mod d,
multiply them by a g_t, and add at j=0 respectively

    g_t h_(t-1), g_t x_t, g_t.

The represented memory sensitivity action is EXACTLY

    Zbar_mem,t phi=sum_(j=0)^(d-1) O^j
       [w_R phi_R,mem f_j^R+w_W phi_W,mem f_j^W
                          +w_b phi_b,mem f_j^b].        (4)

Here phi_R,mem and phi_W,mem are their k by n memory-row blocks; the
features are shared injection vectors, not independently controlled columns.
Equation (4) holds initially. Multiplying it by a g_t O gives the cyclic
shift, since O^d=I; adding B_mem,t gives the three additions above. This
proves it inductively without retaining any past input outside the moments.

For each of the l source states store its own 2n+1 normalized eligibility
entries, updated with delta times its ACTUAL gate and its ACTUAL feature
vector. R0 has no base propagation between source and memory blocks, so those
source entries realize the source rows of Zbar exactly, including derivatives
with respect to source-row parameters whose columns refer to memory states.

Total persistent credit coordinates are

    (d+l)(2n+1)<=n(2n+1)=P.                             (5)

The matrices O^j are fixed model constants; they may be reconstructed at
decode time and are not history-dependent buffers. All moments and source
eligibilities are counted. The update is continuous, online and contains no
replay/tape. Query answers use the ACTUAL dense future adjoint and exact
future injections. Equations (2)-(3) give uniform error below epsilon for
fixed c and sufficiently large n, at EVERY horizon.

Thus the SAME hard rotating/dense family has O_c(n^2) sufficient credit
memory on this history class. The accepted Omega_c(n^2) section is contained
in the class, so its worst-case arbitrary-horizon requirement is
Theta_c(n^2) ON THIS CLASS. This is not Theta_c(n^2) on arbitrary histories
of the model: non-scalar memory gates are excluded from this theorem.

## 4. Theorem: fixed-period noncommuting memory gates also aggregate quadratically

Now suppose G_mem,t has period p, with p independent of n and history length:

    G_mem,bp+i=D_i, i=1,...,p.

The D_i are diagonal but need NOT commute with O, or with the other gated
transition matrices. Source gates remain arbitrary. This genuinely admits
noncommuting G_t O products. A pattern may be specified publicly; alternatively
it may differ between histories and be saved from their first p transitions.
All stored pattern entries in that case are counted below. Again this is a
conditional history class, not a fact about every actual trajectory.

Define fixed-within-history memory matrices

    A_i=a D_i O,
    M=A_p ... A_1,
    K_i=A_p ... A_(i+1) D_i.

At block boundaries the exact surrogate satisfies

    Zbar_mem,(b+1)p phi=M Zbar_mem,bp phi
       +sum_i K_i [w_R phi_R,mem h_(bp+i-1)
                    +w_W phi_W,mem x_(bp+i)+w_b phi_b,mem].

Let det(lambda I-M)=lambda^k+sum_(j=0)^(k-1)chi_j lambda^j.
Cayley-Hamilton gives M^k=-sum_j chi_j M^j. Use degree k, not a discontinuously
selected minimal polynomial. Store p k feature moments of each type R/W/b
and represent the boundary sensitivity by

    sum_(i=1)^p sum_(j=0)^(k-1) M^j K_i
       [w_R phi_R,mem f_i,j^R+w_W phi_W,mem f_i,j^W
                          +w_b phi_b,mem f_i,j^b].      (6)

Multiplication by M updates, for each feature type and phase i,

    f'_i,0=-chi_0 f_i,k-1+new_feature_i,
    f'_i,j=f_i,j-1-chi_j f_i,k-1, j=1,...,k-1,

where the new features are the actual h before phase i, its input x, and 1.
This follows directly from the displayed characteristic-polynomial identity.
Noncommutation of the A_i is retained in M and K_i, not approximated away.

Within an incomplete period, retain its at most p pairs (h_previous,x):
2pn coordinates. The decoder applies the appropriate partial products to
(6) and adds the partial-period injections using only those COUNTED features.
It does not replay a discarded forward trajectory. At the first period,
the same buffer allows initialization after M,K_i are formed; earlier
queries use the buffered partial sum directly.

If the pattern is history-dependent, retain its pk gate entries. M,K_i and
their characteristic coefficients can be recomputed from them and public
R0 in transient workspace; no persistent k by P matrix is hidden. The
coefficients are polynomials in M entries, so the encoder remains continuous
in the pattern and feature data. Source eligibility uses l(2n+1) entries,
as before. A public phase clock (or one extra counted clock coordinate)
specifies the deterministic block position.
No period-membership check or pivot selection is needed: the same formulas
extend continuously off this class, where their accuracy is not promised.

Total persistent credit and buffers, excluding supplied current h, are at most

    (pk+l)(2n+1)+2pn+pk+1=O_p(n^2).                    (7)

The actual dense family's transfer error remains (3), for every horizon
and every permitted future query. Fixed p may affect storage constants;
p that grows with n is NOT covered by the O(n^2) conclusion.

These conditional scalar/periodic encoders show that neither rotation nor
noncommutation alone forces a logarithmic penalty. The still-open issue is
arbitrary APERIODIC, history-dependent memory gating.

## 5. Query-visible combinations: an exact normalized matrix bound

At the fixed endpoint h=0, use only one-step future inputs

    v_i in [1/5,9/20],

which remain inside the original input cube. Since W=I,b_i=1/20, their
preactivations cover [1/4,1/2]^n, a SUBSET of the accepted future box.
Set

    g_hi=sech^2(1/4), g_lo=sech^2(1/2),
    g_mid=(g_hi+g_lo)/2, s_g=(g_hi-g_lo)/2>7/100.

For the last strict bound, tanh(1/4)<1/4 gives g_hi>15/16;
tanh(1/2)>9/20 gives g_lo<319/400. The latter follows from
e>65/24>29/11 and tanh(1/2)=(e-1)/(e+1). Thus half their difference >7/100.

For an arbitrary sensitivity error Delta Z define

    Y=R Delta Z/beta.

This one-step box query distance is exactly

    D_box(Delta Z)=max_(g in [g_lo,g_hi]^n) ||Y^T g/sqrt(n)||.

Average squared norm over g=g_mid*1+s_g*s, where s has independent uniform
signs. The cross terms vanish, yielding

    D_box^2 >= (g_mid^2/n)||Y^T 1||^2
                         +(s_g^2/n)||Y||F^2,
    D_box >= s_g ||Y||F/sqrt(n),
    D_box <= g_hi ||Y||op.                              (8)

Full permitted query distance is at least D_box. The upper in (8) is for
the box only, not every longer continuation. No residual coordinate is
assumed absent: (8) applies to the entire matrix. It also applies after
projecting onto any selected parameter block, since gradient norm dominates
that block. This separates a fixed single query from its permitted family.

## 6. Theorem: ordinary low-row-rank truncation fails on the rotating family

This theorem concerns an approximation represented by ONE rank-r matrix
Zhat whose queries are Zhat^T c_q plus the exact future direct terms. It is
not a theorem about every nonlinear encoder/decoder or structured moment
representation. In particular, (4) may decode a high-rank matrix from few
moments without storing its dense factors.

Use the SAME rotating R family. Choose d orthogonal real source column vectors H_s
with |H_s,j|<=sigma=2/5 and ||H_s||^2=sigma^2 l/2. Such rows exist explicitly:
take d vectors from the real Fourier basis on l entries. Use the constant
row 1/sqrt(2), the sine/cosine rows at frequencies 1,...,floor((l-1)/2),
and the alternating row divided by sqrt(2) if l is even. Their norms are
sqrt(l/2), entries bounded by one; orthogonality follows by summing the
geometric series of l-th roots of unity. There are l rows, and d<=k<=l.
Scale the selected rows by sigma. This is an analytic history specification,
not a numerical witness search or a change of model parameters.

Repeat these source rows L times with zero memory state and final h_T=0,
exactly as in the accepted quadratic construction, T=J+1. Its realized
inputs atanh(h_t)-R h_(t-1)-b remain in the same cube by the existing
input-slack/perturbation bounds. Parameters see those realized inputs fixed.

Let T0 be the raw reference sensitivity from K=deltaR_mem,source to final
state, using any Frobenius-compatible ordering of K's entries. On the memory
rows its action is

    T0 K=B_L sum_(s=1)^d a^(d-s) O^(d-s) K H_s,
    B_L=sum_(v=0)^(L-1)a^(v d).

Source output rows are zero at R0. Orthogonality of the H_s and of O gives

    T0 T0^T=lambda I_k on memory rows,
    lambda=(sigma^2 l/2) B_L^2 sum_s a^(2(d-s))
          >=(sigma^2 l d/2)(3L/4)^2.                   (9)

For this R block, w_R/beta=1/n exactly. The query-composed reference matrix
is Y0=R0 T0/n. It has k equal nonzero singular values at least

    y0=(a/n)(3L/4)sigma sqrt(l d/2).                  (10)

For the actual dense model let T be that same raw parameter-block sensitivity
on the same prescribed hidden trajectory and Y=R T/n. The injection norm is
at most sigma sqrt(l). Actual and reference gates/injections agree in this
block. The reviewed perturbation recursion gives

    ||T-T0||op<=e sigma sqrt(l)/gamma^2,
    ||T0||op<=sigma sqrt(l)/gamma,
    ||Y-Y0||op<=(sigma sqrt(l)/n)e(a/gamma^2+1/gamma)
               <=E_n:=4sigma/(10^8 c^2 sqrt(n)).       (11)

We used a+gamma=1. All final source leakage is included in T and Y.
There is no projection before applying R that might hide cancellation.

For ANY rank-r approximation Yhat, take k-r orthonormal vectors in the
reference memory subspace intersected with ker(Yhat^T). This intersection
has dimension at least k-r. Each has ||Y0^T u||>=y0, so by (11)

    ||Y-Yhat||F>=sqrt(k-r)(y0-E_n).                     (12)

Projecting a rank-r Zhat onto this parameter block and multiplying by the
actual R/beta still gives rank at most r. Equation (8) then makes some
ACTUAL permitted future query have error at least

    s_g sqrt((k-r)/n)(y0-E_n).                         (13)

For r<=k/2, n>=10c and the accepted n0(c), use
a>=9/10, (1), sqrt(l/n)>=7/10, sqrt((k-r)/n)>=2/5, and
3sigma/(4sqrt(2))>=1/5. The reference part of (13) is strictly larger than

    (7/100)(9/10)(1/5)(7/20)(7/10)(2/5)
      =3087/2500000=0.0012348.                         (14)

Since s_g<=1/2, the perturbation loss is at most E_n/2. For fixed c and
n large enough that E_n<=1/10000, the error is >0.0011848>epsilon.
The direct future R injection is zero at h_T=0, so cannot rescue this failure.

Therefore ordinary rank-r sensitivity truncation needs r>k/2=Omega(n) on
this unchanged hard dense family, EVEN under the normalized late queries.
Storing unstructured dense rank factors then costs r(n+P)=Omega(n^3), or
already Omega(n^3) for dense factors of this selected Theta(n^2)-parameter
block. Factor-sharing/structured compression is expressly not ruled out.
This method-specific obstruction is consistent with (4)-(7) and with the
general O(n^2 log n) window encoder, whose dense decoded matrices are
transient, not persistent buffers. A single fixed history does not itself
prove a continuous-memory lower for arbitrary decoders.

## 7. Exact fixed-Krylov closure fails for arbitrary gates

Every polynomial in R commutes with R. Choose a realizable non-scalar gate
G=I-t E_ii, with 0<t<1/25, by prescribing one hidden coordinate sqrt(t)
and the others zero following h0=0. With W=I,b=1/20 its first input lies
inside the same cube. For fully dense invertible R,

    [G R,R]=[G,R]R !=0,

because R_ij!=0 for j!=i. Thus G R is not a polynomial in R; a fixed basis
of powers of R is not invariant under all admissible gates.

More generally let A be a linear matrix algebra containing every G R for
G in an open diagonal box. Taking differences shows E_ii R belongs to A.
Closure under multiplication gives

    (E_ii R)(E_jj R)=R_ij e_i e_j^T R.

All R_ij are nonzero and R is invertible, so these n^2 matrices are linearly
independent. Hence A is the full n by n matrix algebra. A naive fixed-template
moment scheme with independent 2n+1 feature moments for every template then
uses n^2(2n+1) coefficients, not O(n^2).

This is an EXACT closure obstruction for that scheme. It is NOT a finite-
error information lower: matrix words may be weak, their coefficients may
be correlated, and propagation/injections must belong to one real history.
The periodic theorem avoids it by restricting word order, not by claiming
the entire generated algebra is small. No logarithmic robust lower follows.

## 8. New arbitrary-history query-weighted gate budget

The following holds for EVERY admissible R and history, without periodic or
scalar gates. For a future query set p_T=c_q and propagate the actual past
adjoint p_(t-1)=R^T G_t p_t. Put u_t=||p_t|| and e_t=||(I-G_t)p_t||.

Since ||R||op<=a and 0<=G_t<=I,

    ||p_(t-1)||^2<=a^2 ||G_t p_t||^2.

Subtract and sum to obtain

    (1-a^2)sum_t ||p_t||^2
       +a^2 sum_t ||(I-G_t^2)^(1/2)p_t||^2
       <=||c_q||^2.                                   (15)

There is also a useful first-moment bound. Let v_t=||G_t p_t||. Then

    u_t-u_(t-1)/a >= u_t-v_t >= e_t^2/(2u_t).

The final inequality follows from 1-g^2>=(1-g)^2 and u_t+v_t<=2u_t.
Terms with u_t=0 have e_t=0 and quotient defined as zero. Summing gives

    sum_t e_t^2/u_t<=2||c_q||,
    sum_t u_t<=||c_q||/gamma,
    sum_t e_t<=||c_q|| sqrt(2/gamma).                  (16)

The first sum telescopes with a nonpositive residual:
sum_t(u_t-u_(t-1)/a)=u_T-u_0/a-(gamma/a)sum_(t=1)^(T-1)u_t<=u_T.
The last inequality is Cauchy-Schwarz with weights u_t.

For the rotating family, kappa_Q=O(n^-1/2), gamma=c/n. Thus both
sum_t ||p_t||^2=O_c(1) and sum_t e_t=O_c(1), uniformly in horizon.
This is a genuine horizon-free constraint on query-visible gating damage.
It does not say that all credit injections are weak or low dimensional.

### Why this does not yet prove the desired aggregate theorem

Try the compact ungated-memory reference of section 3, keeping actual source
gates and actual features. Its sensitivity norm is at most C/gamma.
The exact variation-of-constants formula for a query error gives terms

    sum_t Zbar_(t-1)^T (A_t-Abar_t)^T p_t
                    +(B_t-Bbar_t)^T p_t.

The dense perturbation contributes at most kappa_Q C e/gamma^2. Removing
memory gate defects contributes at most

    C(a/gamma+1)sum_t e_t
       <=sqrt(2) C kappa_Q/gamma^(3/2).                (17)

At gamma=c/n, kappa_Q=Theta(n^-1/2), this is O_c(n), not epsilon.
The horizon-free gate budget alone therefore does not control its coupling
to a large OLD eligibility accumulator. This is a failure of this upper-
proof estimate, not an impossibility theorem; scalar gates in section 3 can
be large yet aggregate exactly, so dropping them was already avoidable loss.

## 9. Remaining gap, compression attempts and next theorem

| Attempt | New conclusion | Limitation |
|---|---|---|
| Shared cyclic moments | O(n^2) arbitrary horizon on scalar-memory-gate histories | Not arbitrary gates |
| Periodic/Floquet plus characteristic moments | O_p(n^2), even with noncommuting memory gates | Fixed p only |
| Ordinary low-row-rank sensitivity factors | Rank Omega(n) required at the SAME epsilon/query metric | Not every structured/nonlinear encoder |
| Fixed powers/Krylov basis of R | Not closed under admissible non-scalar gates | Exact barrier, not robust lower |
| Full generated matrix algebra | n^2 templates for naive independent moments | Does not establish n^2 log n independent robust information |
| Query-weighted gate energy/variation | Horizon-free bounds (15)-(16) | Coupled old sensitivity factor remains too large in (17) |

Learned nonlinear coordinates, query-specific nonlinear decoding and adaptive
structured summaries are not refuted by the low-rank theorem. Random sketches
or UORO expectation/unbiasedness do not establish deterministic uniform
absolute error for every future query. A decoder may do transient dense
work, but persistent factors, moments and update buffers must all be counted.
One cannot quietly recompute an aperiodic discarded gate history.

No universal O_c(n^2) encoder for ALL dense models/histories and no
Omega_c(n^2 log n) robust section is obtained. Log necessity for general
continuous credit state remains OPEN. The new conditional Theta(n^2)
result concerns arbitrary length on restricted histories; it is different
from both the accepted finite-horizon theorem and the desired general upper.

The single next theorem should target APERIODIC memory gates on the same
rotating family: a continuous online moment compression whose query-error
bound couples (15)-(16) to the actual old injections without the loose
C/gamma multiplier in (17). If that is false, it must be refuted by a
jointly robust high-dimensional fixed-h section, not by a noncommutative
algebra, a matrix rank, or a long suffix alone.

New lemmas need independent review. No automated tests, experiments, witness
optimization, GPU/CUDA, architecture or training were executed. Mathematical
checks cover moments, phase/startup buffers, query normalization, Fourier
Gram identity, dense perturbation, rank-method scope and weighted telescoping.
Local experiment compute is zero; shell/writing overhead and RAM unprofiled.
All historical evidence, AGENTS.md, GAS-0 and independent notebooks unchanged.
