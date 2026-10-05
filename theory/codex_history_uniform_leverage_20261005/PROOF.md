# History-uniform adjoint leverage: exact split, partial bounds, and obstruction

Codex, 2026-10-05. Theory only. **Status: STILL OPEN.**

## 1. Scope and exact object

Use the accepted fixed-feature moving-corridor contract, its legal future
query family, and the independently reviewed midpoint/dissipation identities
from theory/codex_filtered_timing_packing_repair_20261005/PROOF.md as premises.
No claim about D=2, spatial writes, arbitrary RNNs, or full-model memory is
made here.

Let N=T+1, let R be the frozen recurrent map on the selected memory
coordinates, and let bar G_s be the actual midpoint gate matrix at history
step s. Put
\[
 B_s=\bar G_s R,\qquad
 \Phi_R(N,t)=B_NB_{N-1}\cdots B_{t+1},\qquad v=N-t.
\]
Thus the adjoint is ordered
\[
 p_N=c_Q,\qquad
 p_{s-1}=B_s^Tp_s=R^T\bar G_s p_s,\qquad
 p_t=\Phi_R(N,t)^Tc_Q
     =B_{t+1}^T\cdots B_N^Tc_Q.
\]
The rightmost factor acts first in the displayed product for p_t.
The query vector c_Q is the unnormalized effective adjoint of the
accepted normalized head, restricted to the selected memory coordinates.
The query Q includes every permitted future horizon L_Q>=1, every
future preactivation choice in [.25,.75]^n, and the corresponding frozen
future-input realization. In the accepted convention,
\|c_Q\|_2<=q_f^{L_Q}<=q_f<.941. The actual query metric multiplies
the resulting read by sigma sqrt(ell)/n; that factor is not part of
Lambda.

For an ordinary physical support S in the selected memory coordinates,
\[
 \Lambda_R(t,S)=\sup_{Q\ {\rm legal}}\|P_Sp_t\|_2,\quad |S|=s.
\]
The terminal exceptional coordinate is excluded from ordinary S:
its legal adjoint can exceed .66 and the ordinary-coordinate envelope does
not apply there. Support size s, age v, number of survivor tuples,
number of changed gates, and dimension of a parameter section are distinct
quantities.

The midpoint recurrence is complete. In particular, its transpose includes
the two Householder feedback terms at every step; it is not a paired-channel
projection.

## 2. Complete adjoint and renewal terms

For the reference block R0=aO_*, the exact structural identity is
\[
 O_*=C+\mathbf 1u^T+e_1v_H^T,
 \quad
 u^T=\frac{\gamma}{\sqrt{k}}e_{d-1}^T-\frac{\gamma^2}{k}\mathbf 1^T,
 \quad
 v_H^T=\frac{\gamma}{\sqrt{k}}\mathbf 1^T .
\]
The full reference adjoint step is therefore
\[
 p_{s-1}
 =a\{C^T\bar G_sp_s
       +u(\mathbf 1^T\bar G_sp_s)
       +v_H(e_1^T\bar G_sp_s)\}.                 \tag{1}
\]
The last two terms are the uniform and exceptional-front Householder
renewals. Equation (1) retains every renewal, with its sign and chronological
gate weighting. For the actual dense map write R=R0+E, where the
accepted frozen-family estimate is
\|E\|_{\rm op}\le e_R=4\cdot10^{-8}n^{-2}; then the complete step has
the additional term E^T\bar G_sp_s.

The exact legal-query supremum is taken after the entire chronological
propagator. Direct future-gradient terms are absent from this past-credit
read; for two histories they cancel because the endpoint and the same future
query are common. The group/head factors remain exactly those in the
definition of nu.

## 3. Accepted complete upper bound; dense-model transfer

The reviewed ordinary-characteristic estimate in the packing repair gives,
for the reference model and every legal Q,
\[
 \Lambda_{R0}(t,S)
 \le a^v\min\left\{q_f,\,
       \frac{\sqrt{s}}{\sqrt n}(100+6q_fv)\right\}.       \tag{2}
\]
It is an upper bound over all legal future horizons and choices. The
6q_fv/sqrt(n) term comes from first departure from the ordinary C
characteristic; after that departure the proof propagates the remainder with
the full norm-contractive operator. Thus (2) retains all later Householder
paths and front feedback. It is not an assertion that each path is small
separately.

For the actual dense model, product telescoping gives
\[
 \|\Phi_R(N,t)-\Phi_{R0}(N,t)\|_{\rm op}
       \le v e_R a^{v-1}\quad(v\ge1).                     \tag{3}
\]
Under the accepted same-query dense comparison, the future effective
adjoints differ by at most e_R L_Q q_f^{L_Q}, whose supremum over
L_Q>=1 is below 7e_R. Consequently
\[
 \boxed{\;
 \Lambda_R(t,S)\le
 a^v\min\left\{q_f,\,
       \frac{\sqrt{s}}{\sqrt n}(100+6q_fv)\right\}
 +(v+7)e_R .\;}                                           \tag{4}
\]
This is the strongest complete all-query upper bound established here. It
is the accepted bound plus an explicit dense-transfer charge; it does not
remove the age factor. For v=0, use the corresponding endpoint query
bound without the product term.

## 4. An exact reducing subspace for the reference chronology

This subsection gives a sharper bound on one invariant component, not on
the whole Lambda.

For tuple i at time s, let U_{i,s} be the three-dimensional zero-sum
subspace supported on its four sites (two co-moving cycle sites and two
stationary compensators). Let U_s be the direct sum over tuples.

All tuple sites are ordinary, away from d-1, and the tuple gate is shared by
its four sites. Hence u^Tx=0 and v_H^Tx=0 for every x in U_{i,s}; the
exceptional coefficient in u is outside these supports. The open shift C
moves the two cycle sites to the next tuple positions and fixes the
compensators. It preserves zero sum and gives an isometry U_{i,s} to
U_{i,s+1}. Therefore O_* does the same, and the scalar tuple gate makes
bar G_s preserve the subspace. Orthogonality of O_*, symmetry of bar G_s,
and the reducing property imply that U_s-perp is invariant too.

The private Householder renewal is not being discarded: its two rank-one
functionals vanish identically on U_s, while every common-mode, bath, and
front renewal remains in the complementary system U_s-perp. In reference
coordinates the adjoint splits exactly:
\[
 p_s=p_s^U+p_s^\perp,\qquad
 p_s^U\in U_s,\quad p_s^\perp\in U_s^\perp. \tag{5}
\]
If r_S is the number of four-site tuples touched by S, the accepted
all-query ordinary-coordinate bound |(c_Q)_z|<=100/sqrt(n) yields
\|P_{U_{i,N}}c_Q\|<=200/sqrt(n) per tuple. Gates have magnitude at most
one, so
\[
 \boxed{\;
 \|P_Sp_t^U\|_2
       \le 200\,a^v\sqrt{r_S/n}
       \le 200\,a^v\sqrt{s/n}.\;}                          \tag{6}
\]
For the actual dense map the same component comparison incurs at most
(v+7)e_R, by (3) and the accepted query-adjoint transfer.

Equation (6) is not an upper bound for \|P_Sp_t\|: after restricting to
S, the complementary component can overlap the zero-sum coordinates.
In particular, it does not control the tuple-common private renewal.

## 5. Legal persistent-leverage example

A cycle-track antisymmetric mode already prevents any uniform
age-decaying bound for the full leverage.

Take m_s legal survivor tuples and define the unit vector
\[
 y_t=\frac1{\sqrt{m_s}}\sum_{i=1}^{m_s}
       \frac{e_{c_i^A(t)}-e_{c_i^B(t)}}{\sqrt2},
 \qquad S_t=\operatorname{supp}(y_t),\quad |S_t|=2m_s.
\]
It is zero sum on each tuple. Thus O_*y_t=Cy_t, and every history
gate on the selected tuple multiplies this mode by the same scalar. Choose
the admissible high gate g_H=1-n^{-2} on these tuples for the interior
steps. The common public reset has gate q_N=1-u_N^2>.99, since the
accepted corridor has |u_N|<.1. With age v=N-t, the reference
forward transport is exactly
\[
 \Phi_{R0}(N,t)y_t
   =a^v g_H^{v-1}q_N C^v y_t,                              \tag{7}
\]
when the v-1 intervening steps are interior and the last is reset.

For a legal one-step future query, choose future preactivations so that its
gate vector g equals g_hi=sech^2(.25) on positive coordinates
of O_*C^vy_t, and g_lo=sech^2(.75) on its negative
coordinates. These independent coordinate choices are legal and are
realized by frozen future inputs. In the reference convention
c_Q=(a/sqrt(n))O_*^Tg. Because
\|y_t\|_1=sqrt(2m_s), this SAME query gives
\[
 |\langle \Phi_{R0}(N,t)y_t,c_Q\rangle|
 =a^{v+1}g_H^{v-1}q_N
   \frac{g_{\rm hi}-g_{\rm lo}}2\sqrt{2m_s/n}.             \tag{8}
\]
Since (g_hi-g_lo)/2>.17, the actual dense adjoint differs
from (8) by at most (v+7)e_R, and
\|P_{S_t}p_t\|>=|\langle y_t,p_t\rangle|. Thus for all sufficiently
large n,
\[
 \Lambda_R(t,S_t)\ge .16\sqrt{|S_t|/n}                    \tag{9}
\]
for these histories and ages. This is a lower bound for the supremum,
not a claim that every query sees this mode. The endpoint is common across
histories; in fact the example can use a single legal history as its
midpoint, followed by the accepted reset. No direct future term is used.

For a growing age, take
m_s=floor(sqrt(n)),
v=T=ceil(2sqrt(n)log(n)), and t=1. The corridor no-wrap
condition 2m_s+T+4<=d/100 holds for all sufficiently large n.
Bernoulli's inequality gives a^(v+1)>=1-(v+1)/n->1 and
g_H^(v-1)>=1-(v-1)/n^2->1. The reset factor exceeds .99.
So leverage on this zero-sum component remains a fixed fraction of
sqrt(|S|/n) over ages tending to infinity. Taking instead
m_s=floor(n/2000), with the same sublinear v, gives
|S_t|=Theta(n) and a positive n-independent lower bound
(>.004 for sufficiently large n). This is order-one in n, at a
fixed small support fraction.

This refutes any proposed history-uniform estimate of the form
\[
 \Lambda_R(t,S)\le C\sqrt{|S|/n}\,\rho(v)+(v+7)e_R
\]
with fixed C and rho(v)->0 uniformly over admissible ages. It
does NOT refute an age-independent C sqrt(|S|/n) upper bound, nor does
it show that the full private complement exceeds that scale.

## 6. Consequence for support packing

For a gate-window pair, the accepted midpoint Duhamel formula and
\|A_t\|<=b_t imply, for changed ordinary support S_t and
delta_t=\|\Delta G_t\|_max,
\[
 d_{\rm actual}\le
 \frac{\sigma\sqrt\ell}{n}
 \sum_{t\in I} b_t\delta_t\Lambda_R(t,S_t)
 +8\cdot10^{-9}.                                          \tag{10}
\]
Substitution of (4) recovers the accepted age-weighted leverage bound
(repair PROOF.md, (23)). It is a complete all-query pair upper bound,
including old credit and all private renewal paths.

No unconditional packet count or continuous-dimension bound follows:
the sum can still grow over long windows, and disjoint physical supports do
not imply disjoint final sensitivity supports. The accepted
O(m(T+1)^2/n^2) conclusion remains conditional on the explicitly
localized scalar-packet hypotheses. The accepted injection-age packet
count remains conditional on separate attribution. No D=o(sqrt(n)
claim is restored.

## 7. Exact remaining statement

The unresolved quantity is the restriction of the complete adjoint to the
tuple-common/private complement:
\[
 \sup_{\text{legal corridor midpoint histories},\,Q}
 \|P_S\Pi_{\mathcal U_t^\perp}
       \Phi_{R0}(N,t)^Tc_Q\|_2,
\]
together with the O((v+7)e_R) dense-transfer charge. The complementary
adjoint obeys the full rank-two recurrence (1); it includes tuple-common
survivor coordinates, the private J,B renewals, ordinary bath, and
exceptional front. A uniform bound O(sqrt(s/n)) on this complement
would remove the linear age loss and materially strengthen packing. A
counterexample growing beyond this scale would show that support-only
leverage is insufficient. Neither result is proved here.

No experiments were run: the result is analytic and no numerical check was
needed. CPU numerical threads used: zero; GPU/CUDA use: zero.
