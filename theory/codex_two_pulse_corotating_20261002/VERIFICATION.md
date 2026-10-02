# Independent mathematical verification

Codex, 2026-10-02. Re-derived from the stated model; imports no Claude code and
uses no Claude numerical result as evidence. Scope is one public fixed source
feature and the accepted normalized future-query contract. The conclusions
are author-derived mathematics plus separately labelled numerical checks,
not a new interval certificate or external hostile review of this document.

## 1. Exact model, actual queries, and dense-transfer ledger

For n>=200 let k=floor(n/2), l=n-k, d=floor(n/4), r=k-1, a=1-1/n,
U=I-2ww^T/(w^T w), w=e1-1/sqrt(k), O=U(P_d direct_sum I)U^T,
R0=diag(aO,I_l/(100n)). The accepted actual dense R satisfies
||R||op=a and e=||R-R0||op<=4/(10^8 n^2). W=I, b=.05 ones.
All parameter entries are independently differentiated, with input histories
held fixed. Model loss/group normalizers are frozen public constants.

H=.4 ones_l is ONE source feature. E embeds physical memory coordinates2..k.
Along the prescribed histories, selected variations K=delta R_(2..k,source)
satisfy delta h=B K H, with

 B_t=G_t(R B_(t-1)+alpha_t E), B0=0,
 G_t=diag(1-h_t^2), alpha1=0, alpha_t=1 thereafter.

This accounts for ALL n state rows, dense leakage, and coupled parameter
injections. It does not independently choose columns K H. B parameters do
not change while evaluating a history. At the shared endpoint h=0, direct
future parameter injections are identical and cancel in history differences.

For every actual permitted late adjoint xi, ||xi||<=a/beta, where
beta=max(1,||R||F), w_R=||R||F/n and w_R/beta=1/n here. The true selected
gradient difference distance is

 nu(DeltaB)=w_R ||H|| sup_(xi in C0) ||DeltaB^T xi||.

For a legal one-step input v_i in [.2,.45], xi=R^T g/(beta sqrt(n)),
g_i=sech^2(v_i+.05). Thus g_i in [g_lo,g_hi], with
g_lo=sech^2(.5), g_hi=sech^2(.25), s_g=(g_hi-g_lo)/2.
These are actual future inputs; no arbitrary adjoint privilege or RMS contract.

With the SAME prescribed actual gates, the R0 sensitivity Bbar=E M obeys
M'=G_* (aO_* M+alpha I). Geometric sums give
||B||op,||Bbar||op<=n and ||B-Bbar||op<=e n^2 at EVERY horizon.
Consequently replacing B by Bbar has all-future query error at most

 eta_n=(a||H||/n)e n^2=a||H||e n <2e-9.

A pair's query distance changes by at most2eta_n. This rigorous conditional
ledger justifies the controlled reference diagnostic; it does not turn its
ordinary floating-point SVD into an interval-certified computation.

## 2. Bounded-pulse cap, independently proved

Fix q public pulse times, all other prescribed states, and model constants.
The input trajectory is determined by q memory vectors z_i in R^k:
x_t=atanh(h_t)-R h_(t-1)-b. If a continuous sphere section of dimension m
(sphere S^(m-1)) had m>qk, its map to the tuple (z1,...,zq) would have an
antipodal equality by Borsuk-Ulam. Those antipodes have the SAME history and
therefore every future answer is identical. They cannot separate by>2epsilon.
Thus m<=qk, O(n) for fixed q. Protected-coordinate restrictions can sharpen
the count, but are unnecessary for this cap.

An actual counted upper is also available in this fixed-time class: save the
q pulse vectors (qk coordinates), forward state n while arriving, and one
clock if times are not supplied publicly. At a query, compose the q pulse
affine sensitivity maps and the public constant-gate gap powers/geometric
injection sums. This does not store or replay a discarded list of inputs.
Decoder transient work is not bounded. The encoding is continuous; this is
neither a finite-bit bound nor an efficient-decoder claim.

SCOPE: fixed pulse times and otherwise fixed trajectory. A varying background,
additional source history, or growing pulse count is not covered by this cap.

For one fixed query, the selected answer is an r-vector B^T xi times H^T.
Borsuk-Ulam similarly caps any section separated by THAT single query at r.
This is not a cap on the family of all queries or all parameter groups.

## 3. The stronger one-pulse lower section

Let NC={d+1,...,k}, L=k-d, L'=2floor(L/2), and choose its first L' physical
coordinates. For u in the closed Euclidean unit ball of
Z={u in R^(L'):sum u=0}, dim Z=L'-1, set

 z_c(u)=(-1)^(c-d-1) sqrt(.08(1+u_c)), c in NC'; zero elsewhere.

History: h0=0; h_t=(0,H), t1..3n+1; one pulse (z,H); final h=0.
Realize it using the ACTUAL frozen R and x_t=atanh(h_t)-R h_(t-1)-b.
This fixes the endpoint exactly, not just to first order. Every realized
input is then held fixed when differentiating parameters.

### 3.1 All-combinations input bounds and physical radius

Put c_k=1/(sqrt(k)-1). Direct Householder expansion gives, for c in NC,

 Oe_c=e_c+ell, ell=c_k e2+c_k^2 e1-c_k^2 ones.

The alternating center has zero coordinate sum. The square-root difference
identity implies |sum z|<=sqrt(.08 L') and
||z(u)-z(0)||<=sqrt(.08)||u||. Since L'<=k-d<=k/2+1,
c_k<=1/9, the same elementary maxima used by the handoff give

 |(Oz)_2|<=.225; |(Oz)_c|<=.425 for NC;
 (Oz)_1=0; remaining off-NC coordinates have magnitude<=.025.

Pulse input magnitude is <=atanh(.4)+.05<.4737. Reset input magnitude is
<=a*.425+.05+e||h||<=.475+tiny<.5. Source/warmup coordinates also remain
inside the original cube. This proves simultaneous admissibility, not axes only.

DOCUMENTATION CORRECTION: Claude wrote a<=.995 for all n>=200. The inequality
is reversed as n grows. The valid a<=1 bound above proves the same admissibility
conclusion; no scientific constant, candidate, or model needs changing.

Only pulse/reset inputs vary, so total physical input-history L2 radius is

 sqrt(.08)*sqrt((25/21)^2+a^2) < .44,

uniform in width. This is not a radius.05 theorem. The zero-sum unit ball's
coordinates in fact stay strictly above-1, so the square-root chart is continuous
and smooth on a neighborhood of this compact section.

### 3.2 Exact affine dependence and a real query

Let Bpre=B_(3n+1), V=R Bpre+E. Only the pulse gate varies:
G_p(u)=G_p(0)-.08 diag(u) on NC'. Final reset gate is I. Therefore

 B_T(u)=R G_p(u)V+E

is EXACTLY affine in u, despite the curved input-history chart. With the
one legal future input v=.45 on all NC and.2 elsewhere, put
y=(R^T)^2 g/(beta sqrt(n)). Its selected antipodal half-answer is

 -.08 w_R (V^T diag(y) u) H^T.

This is a whole-sphere linear map, not a tangent approximation.

### 3.3 Reference scalar on the zero-sum section

Every zero-sum vector supported on NC is fixed by U, P, and O. Thus, for
X=sum_(j=0)^(3n) a^j O_*^j and embedded u,

 X^T u=m u, m=n(1-a^(3n+1)).

Also O^2 e_c=e_c+c_k e3+c_k^2 e1-c_k^2 ones for all c in NC.
The query's g is constant on NC, so the reference y0 is constant there:

 y0_c=a^2 E_query/(beta sqrt(n)),
 E_query=g_lo+(c_k+c_k^2)g_hi
            -(1+c_k)^2[f g_lo+(1-f)g_hi], f=L/k.

Using k c_k^2=(1+c_k)^2, the reference antipodal half-norm on ||u||=1
is EXACTLY

 .4*.08*a^2*(m/n)*sqrt(l/n)*|E_query|.

No parameter column was independently selected. Zero-sum cancellation follows
from the actual shared source injection and stationary row structure.

### 3.4 Width-independent quantitative margin and dense transfer

For fixed f, derivative of E_query with respect to c is
(1+2c)g_hi-2(1+c)[f g_lo+(1-f)g_hi]<0 for0<=c<=1/9:
its first term<1.15 and the subtracted term>1.57. At c=0,
E_query=-2(d/k)s_g. Since d/k>=.495 for n>=200 and s_g>.076783,
|E_query|>.0760. Also a^2>=.990025, m/n> .9502, sqrt(l/n)>.70710.
The displayed rounded constants give a reference half-margin greater than
.001617728346399936, which is enough for the stated>.00161 conclusion.
DOCUMENTATION CORRECTION: Claude's literal assertion that this displayed
rounded product is at least.0016181 is false. Exact rational replay records
that failure separately; the threshold epsilon and section remain unchanged.

Independently, ||V-V0||<=e n+a e n^2 and
||y-y0||<=2a e/beta, ||y||<=a^2/beta. The actual half-answer error is at most

 .08 ||H|| e [a^3 n+a^2+2a]
 <=.032 e n^(3/2)<1e-10.

The last elementary inequality uses n>=200 and l<= (n+1)/2; it does not
mistakenly assert a<=.995. Therefore EVERY sphere antipode has actual
half-margin>.00161>epsilon. Borsuk-Ulam forces at least

 L'-1=2floor((floor(n/2)-floor(n/4))/2)-1 >=floor(n/4)-2

continuous history-memory coordinates. This independently verifies the
stronger asymptotic linear lower bound. No conditioning extrapolation or
numerical evidence is needed for that conditional arbitrary-width proof.
Scalar constants/input slack/radius inequalities are independently checked
with exact rational Taylor-series tail enclosures in RATIONAL_CHECKS.json.
The earlier failed rounded-product replay is preserved in rational_checks.log.

Reference and actual numbers are not literally equal: tiny dense corrections
are bounded above and independently observed. The handoff's word "exactly"
for reference/actual numerical coincidence should be read at displayed precision.

## 4. Two pulses: verified identity, not a universal non-additivity theorem

Work on the reference restricted memory r-space. A=aO_*, s=gap+1, gap>=1.
V1=X_(3n+1), V2=A^s G1 V1+X_s. Final operator is A G2 V2+I.
Write G_i=G0-.08 diag(u_i), with G0=.92 on NC',1 elsewhere.
The term bilinear in u1,u2 is EVEN under simultaneous antipodes, so it cancels
exactly. For final xi set y=A^T xi_mem, y1=(A^s)^T G0 y. Common-row structure
gives y1_c=alpha y_c+beta, where

 alpha=a^s*.92, beta=a^s lambda_s^T G0 y,
 lambda_s=O_*^s e_c-e_c (common on NC').

With m1=m_(3n+1), m2=alpha m1+m_s and row remainders Lambda1,Lambda2,
the antipodal half-answer is exactly

 -.08[(alpha m1 u1+m2 u2) elementwise y + beta m1 u1
       +alpha(u1^T y)Lambda1+beta(sum u1)Lambda1+(u2^T y)Lambda2].

Own numerical checks reproduce this identity; see VERIFICATION.json. The
dominant channel has only the combination alpha m1 u1+m2 u2. The beta and
Lambda channels remain real; the identity alone does NOT prove they cannot
jointly add robust directions for section-dependent queries. Thus "two pulses
do not add meaningful dimension" remains a scoped numerical observation.
The fixed-time two-pulse class is nevertheless Theta(n), by the cap and
single-pulse subclass. This does not settle any growing-q class.

## 5. A flaw in the proposed co-rotating heuristic

For physical tanh gates D(h)=I-diag(h^2), co-rotation h'=Oh does NOT generally
imply D(h')O=O D(h). O is Householder-mixed, not a signed permutation.
An explicit example for d>=4 is h=t(e2-e3), h'=t(e3-e4). On any NC column c,

 [D(h')O-O D(h)]e_c=t^2 c_k^2(e3+e4) !=0.

Hence the handoff's assertion "their gates are stationary in the rotating
frame" is false as a general identity for THIS accepted model. Constant
profiles still have exact period d; variable profiles still define admissible
co-rotating histories. They must use actual gates, as this screen does.
The false heuristic does not affect the independently verified one-pulse result.
