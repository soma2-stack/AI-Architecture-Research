# Equal local codes can hide macroscopic private renewal credit

Codex, 2026-10-03. **NEW theorems; internally checked, hostile review required.**
The accepted corridor lift, paired obstruction, complete short-packet bound,
and global energy results are premises, not reopened. Fixed source feature,
epsilon=.001, full absolute input energy, actual legal future queries only.

## 1. Result and limits

THEOREM A (failure of the proposed local-code extension). For every integer
n>=10^200, set

    m=2 floor(sqrt(n)/2), T=ceil(10 n^(3/4)),
    L=ceil(1000 log n), t0=T-L.

There are TWO accepted moving-corridor histories with the SAME public
preparation, SAME exact nonzero endpoint, SAME local quantile code and SAME
compensator traces, for which

    Gamma_(n,m,T) > .03.

The private reference metric is the accepted nu, retaining ALL legal future
queries. The lower uses a subset of two legal one-step queries and ONE fixed
unit parameter probe. The corresponding ACTUAL complete gradient pair has
distance >.03-8e-9. Both histories, and a continuous interpolation between
them, satisfy

    ||X||2 <= 2 sqrt(m(T+2)+1) < 8 n^(5/8),
    mT <= 11 n^(5/4) = o(n^(3/2)).

Thus Gamma<=epsilon-16e-9 is FALSE as a uniform claim in the requested
subcritical coordinate-time regime. This does NOT refute a different
complete corridor code. It does NOT prove superlinear robust dimension or
improve the constructive superlinear energy exponent. The interpolation is
only a ONE-dimensional robust section, with half-margin >.014999996.

THEOREM B (nonperturbative complement damping). The exact co-moving zero-sum
subspace on a set of h=2m survivor sites is preserved. If its common gate is
g_H>=.99 and all other selected-memory gates are <=.9992, every TWO-step
homogeneous propagator on the orthogonal complement has norm at most

    1 - m/(8000n).

Consequently the forced complementary state with forcing norm <=1 and zero
initial state has norm <=16000n/m at every time. This theorem keeps the
FULL Householder matrix, not a first-insertion truncation.

## 2. Frozen definitions and the dense-display correction

Use n>=10^6, k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,
sigma=tanh(sigma/(100n)+.05), .0499<sigma<.051, and the accepted R0
memory block aO, O=UPU. Node0 is invariant; O_*=E^T O E is ORTHOGONAL.
On the selected physical coordinates1,...,k-1,

    O_*=C+1_r u^T+e1 v_H^T,
    u^T=gamma e_(d-1)^T/sqrt(k)-gamma^2 1_r^T/k,
    v_H^T=gamma 1_r^T/sqrt(k), gamma=1/(1-1/sqrt(k)).

C is the open cycle shift plus off-cycle identity. Put c=gamma^2/k.
For S=m+T+4<=d/100, tracks are A+i+t,B+i+t, A=2S,B=5S, plus two
stationary off-cycle compensators per tuple. Public beta_(i,0)=.04. Gates
are shared by all FOUR sites of a tuple, with paired states +/-sqrt(1-g).
All preparation, dense corrections and reset input costs remain counted.

CORRECTION: the previous printed dense-error bracket was algebraically
displayed incorrectly. The independently reviewed reconstructed pair bound
is approximately1.4e-12 at n=10^6, and the accepted conservative pair charge
<=8e-9 remains valid. We DO NOT reuse that display. The short-packet theorem
uses actual contraction directly and is independent of it.

For completeness a correct, horizon-explicit ledger is available here.
Write e_R=||R-R0||<=4/(10^8 n^2), N=T+1, q_f=sech^2(.25)<.941.
For ONE history, identical forcing gives past discrepancy
<=e_R sigma sqrt(l) N(N-1)/2. Identical prescribed future gates give adjoint
discrepancy <=e_R L_Q q_f^(L_Q), and sup_(L_Q>=1)L_Q q_f^(L_Q)<7.
The normalized TWO-history charge is consequently bounded by

    e_R sigma sqrt(l) [q_f N(N-1)/n +14N/n].             (1)

This formula includes the division by n and is valid without replacing a
finite N by an infinite steady-state bound. For N<=n/400 it is even smaller
than the accepted conservative charge. Only8e-9 is used in Theorem A.

## 3. Exact full renewal, including every insertion

For the complete fixed source feature, with realized inputs frozen,

    M0=0, M_t=G_t(aO_* M_(t-1)+I),
    L0=0, L_t=G_t(aC L_(t-1)+I), H_t=M_t-L_t.           (2)

All M,L,H have r-by-r parameter columns; no paired projection is taken.
Let U2=[1_r,e1], W2=[u^T;v_H^T], A_t=aG_t C, Phi_C(t,s)=A_t...A_(s+1).
Let ell_t=W2 L_t and b_t=W2 H_t; each is a2-by-r vector array. Exactly,

    H_t=A_t H_(t-1)+aG_t U2(ell_(t-1)+b_(t-1)),
    b_t=sum_(s=1)^t Kcal_(t,s)(ell_(s-1)+b_(s-1)),
    Kcal_(t,s)=W2 Phi_C(t,s) aG_s U2.                   (3)

The associated temporal operator is strictly causal and nilpotent on any
finite prefix. Thus b=(I-Vcal)^(-1)Vcal ell=sum_(j=1)^N Vcal^j ell is an
EXACT FINITE sum, not a small-feedback Neumann approximation. Individual
terms can be large or cancel; their absolute sums are not used for stability.

Equivalently, putting Acal_t=aG_t O_* and Phi_O(t,s)=Acal_t...Acal_(s+1),

    H_t=Acal_t H_(t-1)+aG_t(O_*-C)L_(t-1),
    H_t=sum_(s=1)^t Phi_O(t,s)aG_s(O_*-C)L_(s-1).        (4)

Since O_* is orthogonal, ||Phi_O(t,s)||<=a^(t-s). This exact resummation
has no exp(CmT/n) instability. It does NOT bound the accumulated forcing or
Gamma by epsilon; an undamped observable component can still accumulate.

The smallest aggregate DRIVER has two private r-vectors J_t=u^TM_t,
B_t=v_H^TM_t. They do not constitute a sufficient2r-coordinate causal
state on their own. An explicit feedback bank is m vectors V_i, one Z,
and t front vectors F_z, each in R^r, conditional on direct L. With its
direct product array the known exact credit count is

    mt+r(m+t+1), or alternatively r^2 via M_t.          (5)

This is the smallest explicit bank established here, not a minimal-realization
theorem. All stored history-dependent vectors are counted. No evolving
O(1)-dimensional probe space for the complete private vector is proved.

## 4. Exact query-weighted error recurrence

For two words, write Delta G_t=G_t-G'_t, Delta L_t=L_t-L'_t. Equation(4)
gives EXACTLY

    Delta H_t=Acal_t Delta H_(t-1)+Y_t,
    Y_t=aG_t(O_*-C)Delta L_(t-1)
          +a Delta G_t[O_*H'_(t-1)+(O_*-C)L'_(t-1)].    (6)

For ANY actual permitted reference adjoint c_Q, put
p_(Q,s)=Phi_O(N,s)^T c_Q. Then

    (Delta H_N)^T c_Q=sum_s Y_s^T p_(Q,s),
    ||(Delta H_N)^T c_Q||2<=sum_s ||Y_s^T p_(Q,s)||2.    (7)

Multiplying by sigma sqrt(l)/n and taking the SUP over legal Q is a valid
query-weighted renewal inequality. The weighting retains the same query
for every summand. There is no RMS norm or old paired8/n substitution.
One may further use ||p_(Q,s)||<=a^(N-s)q_f^(L_Q), but that loses structure.
Equal FINAL local codes do not bound all Delta L_(s-1) in(6), or the second
forcing term. The counterexample below shows this failure is substantive.

## 5. A public gate cap away from the survivor group

The accepted corridor bath induction gives |u_t|<.1, |C_n|<.05 and
a gamma^2 |W_state,t|/k<.012. Its explicit recurrence therefore gives

    u_t>=tanh(.05-.005-.012)=tanh(.033)>.032.            (8)

All ordinary public states are u_t. The exceptional public front is no
smaller: inductively a front predecessor is >=u_(t-1), and the row1
preactivation exceeds the ordinary one because
gamma sum_selected(h)/sqrt(k)>=u_(t-1), using
sum_selected(h)>=(r-4m)u_(t-1)>0. The last-cycle state remains ordinary.
The prepared public front equals u0; this starts the induction. Selected
front states may saturate near1, which only strengthens the gate cap.
Hence every nondriven selected-memory gate satisfies

    G_public<=1-tanh(.032)^2<.9992.                     (9)

This is a public-state bound, not a private-credit norm bound. Dead/donor
tuples with gate g_L=.995 also obey(9). High survivor tuples will have
g_H=1-n^(-2). Their gate is above the public cap.

## 6. Exact co-moving decomposition and two-step damping proof

Let A_t be the high survivor support. It contains h=2m physical sites:
half of the m tuples, each with four sites. Its two tracks shift with P;
its compensators are fixed. Define

    mathcal H_t={x: support(x) subset A_t, sum(x)=0},
    w_t=1_(A_t)/sqrt(h).

O_* maps mathcal H_(t-1) ISOMETRICALLY onto mathcal H_t: the Householder
terms vanish for zero sum and no terminal support. G_t multiplies this
space by g_H. Orthogonality of O_* and symmetry of G_t show that its
orthogonal complement also evolves independently. A vector in that
complement is beta w_t+z with z supported outside A_t.

On the common high direction the exact compression coefficient is

    alpha=w_t^T O_* w_(t-1)=1-ch,
    ell^2=1-alpha^2=2ch-c^2h^2.                         (10)

For the candidate n,m, ch<=5m/n<1, so
ell^2>=ch>=h/k>=4m/n and ell<=sqrt(10m/n).

Here is a two-step estimate that retains ALL signed Householder paths.
Ignore a<=1 when upper bounding norms. After the first O_* let y=beta w_t+z,
||y||=||x||. If ||z||>=ell||y||/4, the first G loses at least
(1-.9992^2)ell^2||x||^2/16 in squared norm. Otherwise
|beta|>=sqrt(15/16)||y||. The outside component after the next O_* is at
least

    g_H ell|beta|-||G_t z||
      >=(.99 sqrt(15/16)-1/4)ell||y|| > .70ell||y||.

The second G loses at least .49(1-.9992^2)ell^2||x||^2. Thus in BOTH cases
the two-step squared norm is <=1-delta ell^2/16, delta=1-.9992^2>.001.
Taking square roots gives two-step norm <=1-delta ell^2/32
<=1-m/(8000n). This proves Theorem B. A bounded unit forcing has total
impulse sum <=2/[m/(8000n)]=16000n/m. No path-order truncation occurs.

## 7. Histories, fixed probe and exact trace matching

Split tuples into equally sized donor and survivor groups. Choose the
UNIT, TIME-INDEPENDENT parameter probe v as follows:

    v_z=+1/sqrt(2m) on the m donor compensator sites,
    v_z=-1/sqrt(2m) on the m survivor compensator sites,
    v_z=0 elsewhere.                                   (11)

It is supported off-cycle and has total sum0. The actual parameter action
is (Ev) f_s^T with the SAME frozen unit source feature f_s.

History A: every tuple uses g_H for1<=t<=t0. History B: survivor tuples use
g_H, donor tuples use g_L=199/200 throughout. Both histories then use g_L
on donors for t0+1,...,T-1. Survivors keep g_H through T.

Let kappa(g;t)=g sum_(j=0)^(t-1)(ag)^j. Write kappa_A,prev and
kappa_B,prev for donor traces at T-1. Prescribe A's LAST donor gate as

    g_A,T = g_L(1+a kappa_B,prev)/(1+a kappa_A,prev).     (12)

This makes kappa_A,T=kappa_B,T EXACTLY. Every survivor trace is already
equal, since its gate word is identical. Preparation beta0 and endpoint
reset are public and unchanged. Since

    0<=kappa_A,prev-kappa_B,prev
       <=T(.995)^(L-1)<=12 n^(-17/4),

we have .994<g_A,T<=.995. All gates are legal. This analytic final correction
is part of the frozen construction; it is not post-certificate tuning.

For n>=10^200 the accepted quantile value is

    16000 sqrt(mT min(m,T))/n
      =16000 m sqrt(T)/n <=16000 sqrt(11)n^(-1/8)<1.

Thus p=1: there are NO quantile-position coordinates, and E_local consists
of precisely the m exact traces. The two histories have equal FULL local
codes. Their direct complete local operators satisfy Delta L_N v=0:
the probe has only stationary compensator columns, whose final traces
match; reset has a public gate and common direct injection.

## 8. Full credit before the terminal tail

Let x_t=M_t v. In A, before the tail, v is a zero-sum, stationary off-cycle
vector supported on equally gated active sites. Exactly,

    x_A,t=kappa_H(t)v,
    kappa_H(t)=g_H sum_(j=0)^(t-1)(ag_H)^j.              (13)

In B, put p_t=Proj_(mathcal H_t)v. Its high survivor cycle entries are
+1/(2sqrt(2m)), and its high survivor compensator entries
-1/(2sqrt(2m)). It has norm1/2 and O_*p_(t-1)=p_t. Therefore the COMPLETE
response decomposes EXACTLY as

    x_B,t=kappa_H(t)p_t+e_t,
    e_t in mathcal H_t^perp, ||e_t||<=16000n/m.          (14)

Equation(14) is an exact invariant-space split plus a controlled forced
complement. It includes infinitely many potential renewals over growing
windows; no insertion order has been dropped.

At t0 define x=x_A,t0-x_B,t0. Since ||v-p_t0||=sqrt(3)/2,

    |w_t0^T x|>=kappa_H(t0)/2-16000n/m,
    ||x||<=sqrt(3)kappa_H(t0)/2+16000n/m.                (15)

For n>=10^200, kappa_H(t0)>=.998T, and 16000n/m<.001 kappa_H(t0).
These integer/threshold bounds do not rely on numerical rounding. Bernoulli's
inequality and ag_H>=1-2/n give

    kappa_H(t0)/T >=1-L/T-n^(-2)-T/n.

Here T/n<=11n^(-1/4), L/T<=1001log(n)/(10n^(3/4)), and
16000n/(m kappa_H(t0))<=16000 n^(-1/4)/(.99*.998*10).
At n>=10^200 these are strictly within the claimed slack and improve with n.
Consequently |w_t0^T x|>.499 kappa_H(t0), and ||x||<kappa_H(t0).
The leading common component is NEGATIVE; absolute signs in what follows
allow either orientation of the antipodal pair.

## 9. Carrying the common component through the tail and reset

The two histories have identical G for the next L-1 steps. Their difference
is propagated by the FULL aG O_*, so its norm cannot increase. If beta_t
is its common high component, orthogonality and(10) imply

    |beta_t-beta_(t-1)|
      <=[(1-ag_H)+ch+ell]||x_(t-1)||
      <=3ell kappa_H(t0).                              (16)

The last donor-gate correction adds at most

    |g_A,T-g_L|(a||x_A,T-1||+||v||)
      <=144 n^(-7/2)                                   (17)

to the full difference norm. Its support is OUTSIDE the survivor set. For
the explicit threshold, 3L ell<.001 and(17)<.001 kappa_H(t0). Therefore
after all T steps the common high magnitude is >.497 kappa_H(t0), with
full norm <1.001 kappa_H(t0).

Reset has a PUBLIC gate q_N=1-u_N^2>.99 on ALL former driven sites. Direct
forcing cancels in the pair. Advancing the co-moving high support through
reset and then through ONE future O_* costs at most the outside coupling
ell||x|| per step. Using q_N>.99, a>.99, ch<.001 and ell<.001 gives

    |w_(T+2)^T O_* Delta M_N v| > .48 kappa_H(t0).      (18)

These displayed .001 bounds are very loose: L=O(log n), ell=O(n^(-1/4)),
and all are far smaller at n>=10^200. The reset does not assume private
feedback is erased. Because Delta L_N v=0, the left side equals the same
expression with Delta H_N. No other parameter residual is set to zero.

## 10. Actual permitted-query lower bound

Let g_hi=sech^2(.25), g_lo=sech^2(.75), s_gate=(g_hi-g_lo)/2>.17.
Choose TWO legal one-step preactivation patterns whose gates are identical
off the co-moving survivor support A_(T+2), and are g_hi versus g_lo on it.
Every coordinate has a preactivation in[.25,.75], with the accepted future
input/head/group contract. The same query is applied to BOTH histories.
The triangle inequality over those two query outputs yields

    nu(Delta H_N)
       >=sigma sqrt(l) a s_gate sqrt(2m)/(n sqrt(n))
                      |w_(T+2)^T O_* Delta H_N v|
       > .0499*.99*.17*.48 kappa_H(t0) sqrt(m)/n.         (19)

Here l>=n/2. Since m>=.99sqrt(n), T>=10n^(3/4), and
kappa_H(t0)>=.998T, the final quantity is >.039, in particular >.03.
The supremum in nu includes these one-step queries, so this proves a lower
in the FULL all-legal-query metric, not an RMS or sampled proxy. It does
not require an arbitrary unit adjoint or the old8/n paired coefficient.

The selected gradient projection onto the FIXED unit parameter probe v is
a valid lower bound on the complete gradient Euclidean norm. Dense pair
charge<=8e-9 implies the stated actual lower >.03-8e-9. The two histories
share the actual endpoint, so future direct sensitivity injections cancel.

## 11. One continuous finite-radius section, and what it does not prove

For theta in[-1,1], give early donor gates

    g_theta=g_L+(theta+1)(g_H-g_L)/2,

the same final L-1 donor gates g_L, and last donor gate

    g_last(theta)=kappa_B,T/(1+a kappa_theta,T-1).

Survivors stay at g_H. This continuous, injective gate family stays inside
(.994,1), has equal exact donor traces for ALL theta, and the same reset
endpoint. The accepted inverse lift gives one continuous input section,
all histories admissible. Every history has FULL absolute norm

    <=2sqrt(m(T+2)+1) <8n^(5/8).                         (20)

Its two boundary points are A,B; hence it is a robust1D section with actual
antipodal half-margin >(.03-8e-9)/2. There are no added independent axes.
This construction uses two cohorts and ONE early gate parameter. Enlarging
it to one early amplitude per tuple gives at most m parameters, not
omega(n); it requires a new JOINT finite-radius proof even for that count.
This upper is topological, not a raw rank assertion: any continuous robust
D-ball section inside that restricted family induces a continuous map from
its boundary sphere to the m early amplitudes. If D>m, Borsuk-Ulam gives
equal amplitudes at antipodes, hence identical full histories and zero
query separation. Thus D<=m in that restricted family. Multiple temporal
changes require an actually new joint section, not independent-axis sums.

The familiar necessary exponent conditions remain rho<=tau, tau>=1/2,
mu+rho>1, mu+tau<3/2. Here mu=1/2,tau=3/4 give subcritical mT, but D=1,
not D=n^(5/4). This pair/section does not improve the accepted superlinear
energy threshold or imply bits/VRAM/practical training claims.

## 12. Same construction at near-linear coordinate-time cost

The power-law example is not the smallest budget at which the CODE can fail.
This is an analytical corollary of the same exact split, not a new witness
search or a changed official candidate. Replace ONLY public m,T by

    m=2 floor((log n)^4/2), T=ceil(10n/(log n)^2),
    L=ceil(1000 log n), n>=10^1000.                     (21)

The prescribed histories/probe/last-gate correction are unchanged. Now
kappa_H(t0)>=.998T by the same Bernoulli estimate, now T/n<=11/(log n)^2
and L/T<=1001(log n)^3/(10n). The complement relative error is bounded by
16000/[.99*.998*10(log n)^2]<.001 at n>=10^1000. Also

    p=1, because 16000m sqrt(T)/n
       <=16000 sqrt(11)(log n)^3/sqrt(n)<1,
    3L ell<=3L sqrt(10m/n)<.001,
    m+T+4<=d/100.

The last-gate error estimates become <=12n^(-4) and <=144n^(-3), which
are still negligible. Every inequality in(15)-(19) remains valid, and
T sqrt(m)/n>=10sqrt(.99). Hence this corollary still gives

    Gamma>.03, mT<=11n(log n)^2,
    ||X||2<8sqrt(n)log n.                              (22)

All estimates hold for every n above the stated threshold: log powers
divided by sqrt(n) decrease there, the complement-relative error decreases
with log n, and the rounding errors are dominated by the displayed margins.

The same finite inequalities also allow a GROWING Gamma lower. Keep
m=2floor(sqrt(n)/2), take T=ceil(10n^(9/10)), and keep n>=10^200 and the
same L, gates, fixed probe and exact trace correction. The p-expression is
now <=16000sqrt(11)n^(-1/20)<1. The complement-relative error is
<=16000n^(-2/5)/(.99*.998*10); the Bernoulli loss is <=11n^(-1/10)
plus the negligible L/T term. Last-gate and forcing corrections are bounded
by12n^(-41/10) and144n^(-16/5). Thus(15)-(19) apply unchanged and yield

    Gamma>.03 n^(3/20),
    mT<=11n^(7/5)=o(n^(3/2)), ||X||2<8n^(7/10).       (22a)

Even a width-independent constant Gamma upper fails for this code. This
remains a counterpair/1D result, not an omega(n) dimension theorem. No new
numerical history was sought for(22a); it follows from the explicit bounds.

More generally the proof works for T=ceil(10n/sqrt(m)) whenever even public
m tends to infinity, m=o(n^(2/3)), and the displayed finite inequalities
(p=1, small3L ell, kappa>=.998T, complement relative error<.001, and geometry)
hold. Then Gamma>.03 at mT=O(n sqrt(m)), energy O(sqrt(n)m^(1/4)). This is
only a COUNTERPAIR/1D-section tradeoff. It is not a superlinear-dimension
frontier. In particular growing m arbitrarily slowly gives n^(1+o(1))
coordinate-time code failure, but does not give omega(n) memory.

## 13. Upper bounds and exact remaining question

Let B_N=sum_(j=0)^(N-1)a^j<=min(N,n). Reference M and L have operator norm
<=B_N. Thus for ALL legal histories

    Gamma <=4sigma sqrt(l)q_f B_N/n
          <.191964 min(N,n)/sqrt(n).                   (23)

On an equal local-code fiber, nu(Delta L_N)<=epsilon, giving also

    Gamma <=2sigma sqrt(l)q_f B_N/n+epsilon
          <.095982 min(N,n)/sqrt(n)+.001.              (24)

Take the minimum of(23),(24). They do not settle long-packet robust width.
Theorem A refutes uniform small Gamma, not these large upper bounds.

Repeated Householder paths partly cancel: the full propagator is
nonexpansive, and a large co-moving zero-sum subspace is exactly invariant.
The complementary response damps at rate Omega(m/n), not exp(CmT/n).
But its private common projection can retain order-T credit over a terminal
tail of O(log n) steps. The local code forgets WHEN donor credit existed.
No universal cancellation of that chronology occurs.

The smallest next lower target is a GROWING number of transfer epochs into
co-moving survivor reservoirs, with every antipodal direction surviving
simultaneously. Alternatively a code storing cohort-resolved renewal
statistics could avoid this pair. Neither is proved. Complete moving-
corridor superlinear width remains OPEN; general bracket[1/4,3/4] and the
full-model gap are unchanged. Stop this stage.
