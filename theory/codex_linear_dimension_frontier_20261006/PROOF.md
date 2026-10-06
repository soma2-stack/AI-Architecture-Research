# Capture before trace repair: removal of the logarithmic mask restriction

Codex, 2026-10-06. THEORY ONLY. **New author-derived scoped theorems,
pending independent hostile review.** The owner reports the coded-donor
theorem at 5cfe9c4 independently verified by Grok and Gemini. Its proved
code, chronological comparison and complete front estimates are premises.
The main question, linear robust dimension with mT=o(n^(3/2)), remains OPEN.

## 1. Precise conclusions

THEOREM A (early capture). For every integer n>=10^3000 and public real M
such that

    sqrt(n) <= M <= 10^-40 n,

there is ONE continuous injective admissible same-endpoint section B^D in
the unchanged frozen dense tanh fixed-feature family with

    K=floor(10^-20 M), q=floor(K/10^9), D=2q >= M/10^30,
    m=8K floor(M/(8K)), .99 M <= m <= M,

    actual boundary antipodal pair distance > .3,
    half-margin > .15, epsilon=.001,
    mT < 4*10^8 n sqrt(M),
    ||X_raw||_2 < 50000 sqrt(n) M^(1/4).                  (1)

All final donor local traces are exactly public. Two writes, two ONE-step
public captures, one source feature and one final common reset are used.
The long correction tails occur AFTER capture. Realized inputs, not the
inverse-lift policy, are differentiated.

For M=10^-40 n, (1) gives D>=10^-70 n, but this protocol has
mT=Theta(n^(3/2)). It does NOT prove the requested strict-budget theorem.

For EVERY public function f(n) tending to infinity with

    10^40 <= f(n) <= sqrt(n),

eventually M=n/f(n) is admitted, and

    D >= n/[10^30 f(n)],
    mT < 4*10^8 n^(3/2)/sqrt(f(n)) = o(n^(3/2)),
    ||X_raw||_2 < 50000 n^(3/4)/f(n)^(1/4).              (2)

Thus no fixed logarithmic power is needed by this new construction.
For f(n)=log log n these statements hold for every integer
n>=ceil(exp(exp(10^40))); that threshold also exceeds 10^3000.
Equation (2) is still o(n) dimension. No Omega(n) result at the strict
budget, omega(n) result, or new superlinear energy exponent is asserted.

A more convenient explicit specialization, valid ALREADY for all
n>=10^3000, is M=10^-40 n/(log log n). It gives

    D >= n/[10^70 log log n],
    mT < 4*10^-12 n^(3/2)/sqrt(log log n),
    ||X_raw||_2 < 5*10^-6 n^(3/4)/(log log n)^(1/4).     (2a)

Both (2) and (2a) are existential lower constructions, not optimality
claims or reversals of an input-norm upper bound.

THEOREM B (finite-stage control obstruction). Consider the inherited
partitioned stationary-donor corridor framework, with at most K<=m/2
groups and R write stages. Suppose the ENTIRE history depends continuously
on at most RK scalar donor controls, with all other schedules public or
continuously determined corrections, and each section factors through a
CONTINUOUS map into those controls. The inherited constant early-gate
amplitudes are continuously recoverable from the realized history, so
every continuous section in that specified amplitude family meets this
extra premise. Every such robust section
at epsilon=.001 satisfies, for n>=10^3000,

    D <= RK <= Rm/2,
    T > .020 sqrt(n),
    D < 25 R mT/sqrt(n).                                (3)

For bounded R and mT=o(n^(3/2)), necessarily D=o(n). This is a
parametrization-plus-time obstruction, not a complete-corridor compression
or a universal RNN/energy theorem. It does not apply to a redesigned
family with diverging independent controls per group within one interval.

## 2. Exact source of the old logarithmic loss

Read ../codex_frontier_invention_20261006/PROOF.md, sections 6--10.
Its old equation (12) was the sufficient loss bound

    E_old <= 10^8(log n+1) kappa sqrt(m/n)
             +8N^2 n^-5+3kappa n^-10+2N n^-6.            (4)

This charged movement of a common survivor row during the donor tail
and a length ceil(2000 log n) erasure mask. The erased-half geometric
bound also charged 2000 kappa sqrt(m/n). Requiring E_old<10^-6 kappa
was sufficient. In exact algebra its first term requires

    m/n < 10^-28/(log n+1)^2.                           (5)

The previous envelope m/n<=(log n)^(-12), n>=10^3000, made
10^8(log n+1)sqrt(m/n)<=2*10^8/(log n)^5<10^-6.
Power 12 was a convenient envelope, not proved necessary.
Even the old sufficient inequality permits a log^2 denominator with a
sufficiently small fixed prefactor (or a power 2+eta eventually). That
observation alone is not our new construction: (2a) eventually violates
(5) for every fixed prefactor, and instead uses exact protected transport.

Other dependencies:

* Geometry uses 401[(m+T+4)/n]<1; it permits a small constant m/n.
* Bath capacity requires a fixed positive fraction of nondriven ordinary
  rows and small |C_n|. It does not require log n times sqrt(m/n) small.
* Auxiliary damping requires w_H>=6m/n>gamma-1 and w_H<.01. A sufficiently
  small constant m/n meets both conditions.
* Front error divided by kappa is O(t/n)=O(1/sqrt(m)); global-time
  chronology does not force a logarithmic upper cutoff on m.
* Exact trace legality uses (.995)^(L_d-1)N<=2N n^-5. The tail needs
  logarithmic LENGTH, but a protected read need not drift during it.
* The query coefficient grows as sqrt(m)/n; it does not impose the cutoff.
* The old prescribed duration t=Theta(n/sqrt(m)) is a SEPARATE cost issue.
  Taking m=Theta(n) yields Theta(n^(3/2)) even if (4) is eliminated.

No historical equation or accepted conclusion is modified.

## 3. Exact inherited model and probe bank

Use k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,
R0=diag(aO,I_l/(100n)), input matrix I, bias .05*1_n,
||R_actual||op=a, e_R=||R_actual-R0||op<=4/(10^8 n^2).
The source is sigma*1_l, sigma=tanh(sigma/(100n)+.05),
.0499<sigma<.051; f_s=1_l/sqrt(l) is the ONE fixed source feature.
All recurrent entries are independently differentiated.

There are m balanced four-site tuples: two moving +sqrt(1-g) cycle
coordinates and two stationary -sqrt(1-g) off-cycle compensators. Each
tuple gate is shared across its four sites. The selected public state sum
is identically zero. The zero-start preparation, autonomous bath, actual
dense inverse lift and common nonzero reset are the accepted construction
in ../codex_holding_cost_attack_20261003/PROOF.md, section 4, and
../codex_unpaired_corridor_sensitivity_20261003/PROOF.md, sections 1--5.

Half the tuples are donors divided into K equal groups; half are survivors
with four equally represented Walsh labels. There are h_S=2m physical
survivor sites, m stationary survivor sites, and m/K stationary sites in
each donor group. Let d_j,s be their unit indicator vectors and set

    w_j=d_j-s/sqrt(K), W=[w_j], P=1_K1_K^T/K,
    H=I-(1-1/sqrt(2))P, V=WH.

Exactly V^TV=I. The fixed recurrent actions (Ev_j)f_s^T are
Frobenius-orthonormal. The unit donor witnesses b_j=w_j/sqrt(1+1/K)=V a_j
have frame bound sum_j|a_j^T r0|^2<2||r0||^2.

The COMPLETE reference response is

    X_0=0, X_t=G_t(a O_* X_(t-1)+V),
    O_*=C+1_r u^T+e_1 v_H^T,
    u^T=gamma e_(d-1)^T/sqrt(k)-(gamma^2/k)1_r^T,
    v_H^T=gamma1_r^T/sqrt(k), gamma=1/(1-1/sqrt(k)).       (6)

J_t=u^T X_t and B_t=v_H^T X_t are private K-vectors. All front slots,
terminal paths, bath and repeated Householder renewals remain in (6).
Physical projected sensitivity is sigma sqrt(l) E X_t.

## 4. Whole-ball code and the new schedule

Use exactly the verified code lemma, not new random samples. A fixed
full-spark B in R^(K x q) has norm<=1.5sqrt(K); clipping Bz/2 is
continuous, odd and injective on B^q, and every boundary z saturates at
least K/20000 donor controls. Map B^(2q) odd-homeomorphically onto
B^q x B^q by z_e=||y||y_e/max(||y_1||,||y_2||), with zero at y=0.
Write theta_e=clip(Bz_e/2). Some stage has >=K/20000 full endpoint tests
for EVERY boundary y. This is the same verified whole-boundary code.

Let C0=10^8, t=ceil(C0 n/sqrt(m)), and

    g_H=1-n^-2, g_L=.995,
    L_d=ceil(1000 log n),
    L_clear=100000 ceil(n/m) ceil(log n).

Each of the two stages consists of:

1. t repeated donor writes, group j using
   g_j=g_L+(theta_j,e+1)(g_H-g_L)/2, all survivors high.
2. ONE public capture step. Donors are low; survivors have g_H on
   chi_e=+1 and g_L on chi_e=-1.
3. Restore ALL survivors high. Donors use L_d-1 common low steps and
   then one exact final trace-correction step.
4. Public L_clear steps, all donors low and all survivors high.

Prepare once, reset once. In this indexing

    T=2(t+1+L_d+L_clear), N=T+1.                         (7)

The prior protocol repaired traces BEFORE a long erasure mask. The new
protocol captures BEFORE repair, using a partial contrast instead of
erasing one half. It is a change of chronology and protected state, not a
larger constant in the old error estimate.

## 5. Large-m premises, global chronology and exact feasibility

Put S_geom=m+T+4, A=2S_geom, B_track=5S_geom. Below S_geom<=d/100,
so neither cycle track wraps or touches a public front/terminal site.
All tuple gates are in (.994,1); beta=sqrt(1-g)<.1 throughout the whole
control ball. All four sites remain balanced.

The accepted public bath recurrence is

    u_t=tanh(.05+C_n u_(t-1)-a gamma^2 W_state,t-1/k),
    C_n=a gamma^2[(1+4m)/k-1/sqrt(k)], |W_state,t|<=1.1t.

For n>=10^3000, m/n<=10^-40 and N/n<=5*10^8 n^(-1/4),
|C_n|<.05 and a gamma^2*1.1N/k<.012. The inherited induction starts
at u_0=tanh(.05), gives |u_t|<.1 and u_t>tanh(.033)>.032, and makes
every front state no smaller than the bath. Thus

    .99<q_t=1-u_t^2<=.9992,
    f_1,t<=1/n, 0<=q_t-f_z,t<=2(.9992)^(z-1).             (8)

The first front suppression uses the selected-state sum
>=(r-4m)u_t; its positive preactivation is order sqrt(n). These are
GLOBAL-time inequalities. The growing stage count is not reset (there
are only two stages here). At least n/4 ordinary bath rows remain.

The auxiliary weights of the verified comparison satisfy w_b>.9,
6m/n<=w_H<.01 and w_H>gamma-1. These hold at both the lower endpoint
m>=.99sqrt(n) and the new constant upper endpoint. The bath-deficit
positive-cone premise is unchanged. No prior final range such as
K<=n^(3/16) or M<=n/(log n)^12 is imported.

Actual controls are x_t=atanh(h_t)-R_actual h_(t-1)-b. The accepted
lift's uniform past-cube bound |x_ref|<.401 plus the dense correction
<e_R sqrt(n) leaves every actual input in (-.5,.5). Nondriven reference
coordinates are autonomous; their actual dense corrections are counted.
The source preparation, moving entrance/exit coordinates, all masks,
tail gates and reset are part of the same lift.

## 6. Exact trace matching AFTER capture

At a stage entrance every stationary donor trace tau_in is public.
For each group run its actual scalar local recurrence

    tau_next=g(1+a tau_prev).

The capture donor gate is the public g_L. Define tau_target publicly by
using g_L for all t+1+L_d steps from tau_in. At the last tail step set

    g_last,j=tau_target/(1+a tau_prev,j).                 (9)

After L_d-1 common low steps,

    |tau_prev,j-tau_prev,low|<=N(.995)^(L_d-1)<=2N n^-5.

Consequently |g_last,j-g_L|<=2N n^-5 and .994<g_last,j<.996.
This is continuous, legal for the whole ball and sets every group trace
EXACTLY. Public clear steps keep it public for the next stage. Each
survivor gate schedule is public. Therefore L_N V is public at the final
reset, and the final comparison on V is private H_N=M_N-L_N.

The gate correction is not an infinitesimal claim. It is specified at
every control point. Its support is entirely off the survivor; after
capture its effect on the protected survivor row is exactly zero, as
proved next. No approximate trace equality is used.

## 7. Full finite-amplitude early write calibration

Use the verified auxiliary cone/calibration and full row-norm front
estimate of ../codex_frontier_invention_20261006/PROOF.md, section 6,
under the rechecked premises (8). For the zero-initial forced component
let kappa=g_H sum_(s=0)^(t-1)(a g_H)^s. Bernoulli gives kappa>=.998t.

For every full endpoint comparison in donor j, independently of all
other donor gates, the SAME auxiliary survivor row r^0 satisfies

    |r^0 a_j|>=.35 kappa/sqrt(K)-16000n/m.

The verified clipped code and frame bound give

    ||r^0|| >=[.35kappa-16000sqrt(K)n/m]/200
             >.00174 kappa.                            (10)

K/m<=2*10^-20. The complete global-front comparison is a ROW-NORM bound
2*10^12 t^2/n, charged once. Incoming complementary credit is bounded by
B0=16000n/m+N n^-6, again charged once; identical incoming survivor
zero-sum credit cancels. Hence

    ||r_write||>.00173 kappa,
    ||Delta X_write||op<=3 kappa.                        (11)

This is a comparison of finite antipodes, with many simultaneous donor
tests. There is no Jacobian-rank substitution or new full-system
monotonicity assertion. The new schedule has NOT yet taken a trace tail
or a mask at this point. The full J,B renewal has not been truncated.

For arbitrary (unsaturated) stage differences, the survivor difference
at write end is still a common row plus a bounded incoming complement.
Incoming protected rows evolve identically, because survivor gates are
uniform high during writing. This structural statement, not an amplitude
lower, will remove cross-stage cancellation.

## 8. The exact one-step capture identity

Let w_t=1_(S_survivor(t))/sqrt(h_S), and
xi_e,t=chi_e/sqrt(h_S) on the same support. At the end of a stage write,
the common survivor row is r=w_t^T Delta X_t. For the difference of the
two histories in that stage, the private survivor rows are identical
on the four sites of every survivor tuple. Their direct local rows are
public. The next complete pre-gate survivor row is therefore exactly

    r_pre=a[r+sqrt(h_S) J_t], J_t=u^T Delta X_t.          (12)

The fixed V forcing cancels, and e_1 feedback is outside the tracks.
Equation (12) is the COMPLETE row identity, not only a direct kernel.
Since ||u||<3/sqrt(n), (11) implies

    ||sqrt(h_S)J_t||<=13 kappa sqrt(m/n).

At the constant upper range its ratio to kappa is <=13*10^-20.
For every boundary-coded stage, ||r_pre||>.00172 kappa.

Let b_mask=(g_H-g_L)/2>.00249. Applying the ONE public contrast gate
and taking xi_e gives the exact identity

    xi_e,t+1^T Delta X_(t+1)=b_mask r_pre.                (13)

The norm of this protected row is >4.2*10^-6 kappa. There is no log n
factor, no erased-half approximation and no geometric waiting estimate.

For later tail and clear steps let H_t be the co-moving survivor
zero-sum space. O_* maps it isometrically to H_(t+1); uniform survivor
g_H maps it by g_H. Its orthogonal complement is invariant, even with
arbitrary legal donor/front/bath gates. Moreover xi_e^T V=0. Hence its
row evolves EXACTLY as

    r_protected,next = a g_H r_protected,                (14)

through ALL the trace-tail steps, including the donor-dependent last
correction, and every clear step. This is why moving capture before
trace repair removes the old loss (4).

During the public clear, the complete complementary response contracts
by the reviewed two-step bound 1-m/(8000n). Its forced norm is <=16000n/m;
the homogeneous residue is <=N n^-6. A pair differing only in this
stage has no different forcing during clear, so its leftover complement
is <=2N n^-6. All protected rows remain exactly (14).

## 9. Simultaneous two-stage boundary, reset and private read

The two fresh Walsh bits use the same survivor support and source. On a
stored character with an earlier bit, the later ONE-step public capture
acts exactly as

    xi_I -> A_mask xi_I+B_mask xi_(I xor {e}),
    A_mask=a(g_H+g_L)/2>.997, B_mask=a(g_H-g_L)/2.

Both terms retain the earlier bit, have zero sum and stay protected.
There is no half-erasure and no factor 1/2 in older singleton survival.
No stage-1 component has a xi_2 singleton read; a new stage-2 component
has only its own xi_2 singleton, plus the negligible complement residue.

Telescope the two WHOLE stages, not individual donors. Later gate words
and trace corrections are independent of earlier controls by (9).
Some stage e has the uniform coded endpoint lower (10); every other
stage's ideal component is annihilated by its singleton read. The sum
of the cross-stage residual norms is <=4N n^-6. This argument covers
every y on S^(D-1), not just axes. All scalar high transport over the
entire history is (a g_H)^N>.999, and the common reset gate is q_N>.98.
Consequently, for the selected stage,

    ||xi_e,future^T O_* Delta X_N|| > 2*10^-6 kappa.      (15)

The inverse lift makes all nondriven actual coordinates public; at
reset every driven coordinate is set to the public ordinary value u_N.
The ENTIRE actual endpoint is common. The protected row is not erased
by reset. The section is injective: the verified control code is
injective, and distinct early gates imply distinct actual states/inputs
from the required common start.

## 10. Actual legal query and finite-error topology

Use the two legal one-step preactivation patterns .25/.75 according to
chi_e on the next survivor support, swapped in the other query, and
identical off that support. The same query is applied to both histories
at their exact common endpoint. Realized future inputs are frozen.
The head is 1_n/sqrt(n). The accepted frozen loss and group factors have
w_R/beta_loss=1/n. With s_gate=(sech^2(.25)-sech^2(.75))/2>.17, the
complete reference gradient metric is bounded BELOW by the projected
gradient vector on the Frobenius-orthonormal probe bank:

    nu >= sigma sqrt(l) a s_gate sqrt(2m)/(n sqrt(n))
                       * ||xi_e,future^T O_* Delta X_N||. (16)

No per-probe source normalization or arbitrary adjoint is introduced.
Using l>=n/2, (15), kappa>=.998 C0 n/sqrt(m), the reference pair distance
exceeds

    .0499*.999*.17*(2*10^-6)*.998*10^8 > 1.69.           (17)

Direct future terms cancel at the common ACTUAL endpoint. The corrected
finite-N COMPLETE dense pair charge is

    e_R sigma sqrt(l)[q_f N(N-1)/n+14N/n], q_f<.941,       (18)

and is <=8e-9 here. It is uniform over the full ball and probe bank;
projection cannot magnify it. The erroneous historical dense display
is not reused. Thus the conservative actual pair claim >.3 in (1)
holds with substantial slack.

Borsuk-Ulam applied to any continuous memory encoder with fewer than D
coordinates yields equal encoded antipodes. Their common endpoint allows
the SAME chosen future query; error<=.001 for both would imply pair
distance<=.002, contradicting (17)-(18). This is the exact-real
continuous-coordinate lower bound, not bits, rank, or packing.

## 11. Every-width bounds and full absolute input norm

For all n>=10^3000, put L=log n. Rounding and the schedule give

    .99M<=m<=M, K/m<=2*10^-20, D>=M/10^30,
    T+2<4*10^8 n/sqrt(m), N/n<5*10^8 n^(-1/4).

The overhead ratio is bounded by a constant times
(L+1)/sqrt(m)+L sqrt(m)/n, which decreases to zero under both extreme
envelopes m>=.99sqrt(n), m<=10^-40n. In particular it is much below
one at the stated threshold. Geometry follows from

    401[10^-40+5*10^8 n^(-1/4)+4/n]<1.

The auxiliary calibration relative loss is <10^-12, full-front row loss
is <4*10^20 n^(-1/4), and incoming-complement loss is
<.001/sqrt(m)+3Nn^-6/kappa. These vanish with enormous threshold slack.
The capture renewal loss is <=13*10^-20 kappa, uniformly in age/width.
There is NO (log n)*sqrt(m/n) loss after capture. Cross-stage residues
and scalar losses are bounded by N n^-6 and 2N/n respectively. All
width-dependent envelopes are decreasing for L>=3000log 10. These are
analytic monotone envelopes, not sample-width certifications.

The accepted complete inverse-lift norm is used on the ACTUAL history:

    ||X_raw||_2<=2sqrt(m(T+2)+1)
                   <50000 sqrt(n) M^(1/4).              (19)

Preparation, source, moving holds, both donor writes, survivor captures,
stationary compensators, all inverse-lift corrections, trace tails,
last trace repairs, clears, reset and dense realization are included.
There is no subtracted public center. Autonomous reference bath/source
steps use zero reference input; actual dense corrections are counted.

Equation (7) also proves mT>=2 C0 n sqrt(m). Thus if M=cn for any fixed
0<c<=10^-40, mT is BOTH O(n^(3/2)) and Omega(n^(3/2)); it is not little-o.
This is a direct duration calculation, not a reversal of (19).

## 12. Proof of the finite-stage obstruction

The complete family factors continuously through its RK donor controls,
including continuously determined trace corrections and the inverse
lift. Precisely, S=F composed with theta, where theta:B^D->R^(RK) is
continuous. In the inherited amplitude family, theta_j,e is recovered
continuously from the first realized early-write gate of group j,
2(g_j,e-g_L)/(g_H-g_L)-1. Hidden states are continuous functions of the
realized inputs from the common start, and g=1-h^2. Hence this requirement
does not assume an arbitrary set-theoretic lifting of a continuous image.
If a purported robust B^D section had D>RK, Borsuk-Ulam on its
boundary into R^(RK) would give identical control vectors at some
antipodes, hence identical realized histories and zero query distance.
Therefore D<=RK. This is true even if the encoding itself is nonlinear
or clipped; no dimension is inferred from injective raw rank.

Every donor group uses at least one of the m/2 donor tuples, so K<=m/2.
The reviewed COMPLETE ACTUAL short-packet bound is

    pair distance < .095982(T+1)/sqrt(n)

for all permitted future queries, retaining all private renewal and dense
dynamics. A robust pair>.002 requires
T+1>(.002/.095982)sqrt(n)>.020837sqrt(n). At n>=10^3000 this implies
T>.020sqrt(n). Combining these facts gives

    mT>.020m sqrt(n)>=.040D sqrt(n)/R,
    D<25R mT/sqrt(n).

This proves (3). It is not an upper on arbitrary complete moving-corridor
sensitivities, and does not apply merely because a history has m tuples.
The bounded independent donor-controls-per-group premise is essential.
For diverging R the displayed inequality remains valid but no longer
rules out linear D at the strict budget.

## 13. What remains unresolved

The logarithmic mask cutoff has been removed in a legal construction.
The FIXED-stage route now attains linear D at the critical cost, but
provably cannot attain linear D with the requested little-o budget.
The exact next issue is not a smaller coefficient in (4). It is obtaining
divergingly many jointly robust controls per active donor group in ONE
write interval, with multiple protected read rows and no proportional
duration increase. IDEAS.md specifies a precise target lemma.

The complete corridor is not closed. The global superlinear absolute-norm
exponent bracket [1/4,3/4] and the separate full-model bounds are unchanged.
No architecture, finite-bit, VRAM, practical-width or universal-RNN claim
is made. STATUS.md remains STILL OPEN for the primary strict-budget mission.
