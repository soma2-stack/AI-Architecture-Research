# Multi-donor / multi-survivor joint sections: exact transfer and a code barrier

Claude, 2026-10-04. Source branch `theory/corridor-research-20261003` at
`54a915d`. NEW derivations; independent hostile review required. Nothing in
any earlier folder was edited. Codex_Research.md and Cursor_Research.md were
not opened.

Every statement carries one label: **PROVED** (complete proof here, or a
re-derivation of an accepted lemma), **CONDITIONAL** (proved from a named
hypothesis that is not proved), **HEURISTIC** (order-of-magnitude reasoning),
or **FAILED** (a route with its first failed inequality).

## 0. Premises actually used

Only folders present on the branch are used.
`theory/grok_unpaired_corridor_sensitivity_review_20261003/` does not exist;
nothing is taken from it. Consequently the unpaired-corridor folder
(`codex_unpaired_corridor_sensitivity_20261003`) is unreviewed. From it I use
only identities that I re-derive below or that the VERIFIED private-renewal
review re-derived.

| Premise | Source | Status used |
|---|---|---|
| Frozen model, legal-query contract, inverse lift | `codex_autonomous_absolute_energy_20261003`, `codex_energy_threshold_improvement_20261003` (+ Grok VERIFIED) | accepted |
| Corridor lift, ||X||<=2sqrt(m(T+2)+1), exact common endpoint | `codex_holding_cost_attack_20261003` Thm B (+ Grok VERIFIED) | accepted |
| Paired channel barrier D<16000mT/sqrt(n) | `codex_suffix_product_kernel_attack_20261003` (+ Codex hostile review VERIFIED) | accepted |
| Exact renewal H_t=sum_s Phi_O(t,s)aG_s(O_*-C)L_(s-1); O_*=C+1u^T+e1 vH^T; complement damping; Gamma>.03; 1D section | `codex_private_renewal_gamma_20261003` (+ Grok VERIFIED) | accepted |
| Dense pair charge <=8e-9 | same | accepted |

Notation is the private-renewal notation: n>=10^6, k=floor(n/2), l=n-k,
r=k-1, d=floor(n/4), a=1-1/n, gamma=1/(1-1/sqrt(k)), c=gamma^2/k, sigma
the autonomous source level (.0499<sigma<.051), q_f=sech^2(1/4)<.941,
s_gate=(sech^2(1/4)-sech^2(3/4))/2>.17. Selected memory coordinates are
physical 1,...,k-1. N=T+1 is the reset step. For a history,

    M_t=G_t(aO_*M_(t-1)+I),  L_t=G_t(aCL_(t-1)+I),  H_t=M_t-L_t,
    M_0=L_0=0,  Phi_O(t,s)=(aG_tO_*)...(aG_(s+1)O_*),

and the reference fixed-feature metric is

    nu(A)=(sigma sqrt(l)/n) sup_(legal Q) ||A^T c_Q||_2,
    |d_actual(X,X')-nu(M_N(X)-M_N(X'))|<=8e-9.

A robust D-section is a continuous map S:B^D -> admitted common-endpoint
corridor histories with d_actual(S(y),S(-y))>.002 for every ||y||=1.
Write P=mT.

## 1. What a positive answer must beat (PROVED, elementary)

**1.1 Horizon.** The actual sensitivity operator has norm
<=sigma sqrt(l) sum_(j<N) a^j <= sigma sqrt(l) N, every legal adjoint has
norm <=q_f, and the normalization is 1/n. So every pair satisfies
d_actual<=2 sigma sqrt(l) q_f N/n<.096N/sqrt(n). A robust section therefore
needs N>.0208 sqrt(n). (This re-derives the unreviewed short-packet bound
from two accepted norm facts. It also matches the VERIFIED general horizon
bound in the holding-cost proof, equation (20).)

**1.2 Parameter caps.** Let a family consist of histories G(theta), with
G any map from a parameter set in R^K: early amplitudes, epoch durations,
cohort onsets, departure times, and so on. Suppose a section has the form
S=G o phi with phi:B^D->R^K continuous. Then D<=K. Proof: if D>K,
Borsuk-Ulam applied to phi on S^(D-1) gives phi(y)=phi(-y), hence identical
histories and distance zero. The gate array is itself such a continuous
parameter (inverse lift is continuous), so D<=mT always.

Consequences:

- Any family with one amplitude per donor cohort, or a bounded number per
  donor tuple, has D<=O(m)<=n/400. **D=omega(n) is impossible there.** This
  covers the logarithmic-budget family and all of its per-tuple widenings
  (item 8).
- D=omega(n) with P=o(n^(3/2)) needs K=omega(n) continuously varied
  parameters. If each parameter controls a disjoint tuple-time block, the
  mean block area is P/K=o(sqrt(n)). That is shorter than the minimum robust
  horizon .0208 sqrt(n) of 1.1. So "temporal packing" must place each
  robust direction on gate blocks individually too short to be visible on
  their own. This does not forbid it: a short block can modulate long-lived
  stored credit.

**1.3 Corridor size.** Placement requires m+T+4<=d/100, so m,T<n/400.
With 1.1 and n>=10^6, T>=.0208 sqrt(n)-1>=.0198 sqrt(n), so m=P/T<=51P/sqrt(n).

## 2. The exact joint transfer operator (PROVED)

**THEOREM 1.** For every gate word (arbitrary diagonal G_t, any N), put

    b=(gamma/sqrt(k))e_1-(gamma^2/k)1_r,
    beta_s=Phi_O(N,s) aG_s b,
    eps_s=(gamma/sqrt(k)) Phi_O(N,s) aG_s 1_r,
    S_L(s)^T=1_r^T L_s     (local column sums),
    rho_s^T=e_(d-1)^T L_s  (local row at physical coordinate d-1).

Then, exactly and including every Householder insertion,

    H_N=sum_(s=1)^N [beta_s S_L(s-1)^T+eps_s rho_(s-1)^T].        (2.1)

Proof. The VERIFIED renewal gives H_N=sum_s Phi_O(N,s)aG_s(O_*-C)L_(s-1)
and O_*-C=1_r u^T+e_1 v_H^T, with u^T=(gamma/sqrt(k))e_(d-1)^T-c 1_r^T
and v_H^T=(gamma/sqrt(k))1_r^T. Therefore

    (O_*-C)L=1_r[(gamma/sqrt(k))rho^T-c S_L^T]+e_1(gamma/sqrt(k))S_L^T
            =b S_L^T+(gamma/sqrt(k))1_r rho^T.

Substitute. QED. checks.py verifies (2.1) and both renewal forms to
relative error <1e-10 at n=200,400,1000 with random gates in (.99,1).

**Corollary 1a (what a legal query reads).** For every adjoint c,

    H_N^T c=sum_s (c^T beta_s) S_L(s-1)+sum_s (c^T eps_s) rho_(s-1).  (2.2)

All feedback seen by any query is a time-weighted sum of LOCAL column-sum
rows S_L(s). The weights are scalars c^T beta_s, c^T eps_s. They depend on
the query and, through Phi_O, on every later gate. The private renewal
vectors J,B,V,Z,F of the earlier ledgers are resummed into these scalar
kernels. The private information that the terminal local code discards is
precisely the history s->S_L(s) (chronology). The kernel family s->c^T beta_s
determines how that history is read.

**Corollary 1b (two scalar input channels).** For a parameter probe v,
H_N v is the final state of

    x_s=aG_sO_*x_(s-1)+aG_s[b sigma_s(v)+(gamma/sqrt(k))1_r tau_s(v)],
    sigma_s(v)=S_L(s-1)^T v,  tau_s(v)=rho_(s-1)^T v,  x_0=0.     (2.3)

So the complete common-mode reservoir is a full-propagator linear system
driven by two SCALAR input sequences through two FIXED public vectors.

**Corollary 1c (parameter-side confinement).** Let D_cols be the private
columns: the 2m compensator columns and the <=2(m+N+1) cycle columns ever
occupied by a track. Let Q=span{e_z: z in D_cols} + span{S_pub(s),rho_s:
0<=s<N}, with S_pub(s) the restriction of S_L(s) to columns outside D_cols.
Then for any two histories, (M_N-M'_N)v=0 for every v orthogonal to Q, and

    dim Q<=4m+4N+2,  rank(M_N-M'_N)<=4m+4N+2.

Proof. A column z outside D_cols is injected at a site whose co-moving
characteristic never enters a track: a cycle site visited at time j by
tuple i satisfies z-j=A+i or B+i, so an injection at an unoccupied time never
becomes occupied. Hence its local column of L uses public gates, and both
S_pub(s) and the public part of L are history-independent. Track columns lie
in [A,B+m+N+1]. Their distance to d-1 exceeds 94S>N, and off-cycle
compensators never enter the cycle, so rho_s vanishes on D_cols and is
public. For v orthogonal to Q: Delta L_N v=0, S_L(s-1)^T v=0, and
rho_(s-1)^T v=0 for both histories. Then (2.1) gives Delta H_N v=0. QED.

Interpretation. The parameter side of every private credit difference is a
PUBLIC subspace of dimension O(m+T)<=n/100. This is not a bound on robust
width: the row side still carries O(m+T) distinct private rows (tuple rows,
front rows and one bath vector, by the exact row ledger). A static code
storing all those entries has O((m+T)^2) coordinates, which is no better
than mT. Corollary 1c does show that "hidden" parameter directions outside
O(n) public coordinates cannot carry credit (item 9, partial).

## 3. Query visibility across cohorts (PROVED)

**LEMMA 2 (Frobenius and cohort-quadrature lower bounds).** For any two
common-endpoint histories, with Delta M=M_N-M'_N,

    nu(Delta M) >= (sigma sqrt(l) a s_gate/n^(3/2)) ||Delta M||_F
                >= .0059 ||Delta M||_F/n.                         (3.1)

More generally, for any disjoint site groups G_1,...,G_K of selected memory,

    nu(Delta M) >= (sigma sqrt(l) a s_gate/n^(3/2))
                   (sum_k ||1_(G_k)^T O_* Delta M||_2^2)^(1/2).       (3.2)

Conversely nu(Delta M)<=(sigma sqrt(l) q_f/n)||Delta M||_op<.034||Delta M||_op/sqrt(n).

Proof. A legal one-step future with gate vector g in [g_lo,g_hi]^r on
selected memory has reference adjoint c=(a/sqrt(n))O_*^T g on E. Since
Oe_0=e_0 and O is orthogonal, the selected block is invariant under O^T.
Take g_+/-=g_mid 1+/-s_gate xi with xi in [-1,1]^r. By the triangle
inequality one of the two outputs has norm >=(a s_gate/sqrt(n))
||xi^T O_* Delta M||. Choose xi=sum_k xi_k 1_(G_k) with independent
Rademacher xi_k. Then E||sum_k xi_k 1_(G_k)^T O_*Delta M||^2 equals the sum of
squares, so some sign choice attains (3.2). Singleton groups give (3.1),
because ||O_*Delta M||_F=||Delta M||_F. The upper bound is ||c||<=q_f. Use
sigma>.0499, l>=n/2, a>.99. QED.

Consequences. (i) Different cohorts never cancel each other in the best legal
query; their contributions add at least in quadrature. (ii) The total
legal-visible amplitude of K cohorts is at most sqrt(K) times their quadrature
sum. So splitting one survivor group into many cohorts multiplies the number
of separately readable rows but never the visible amplitude. (iii) A
sufficient robust criterion is ||Delta M||_F>.34n+O(1e-6 n) on every
boundary antipode. A necessary one is ||Delta M||_op>.058 sqrt(n).

## 4. Exact cohort factorization of the tuple common modes (PROVED)

On the four rows of tuple i the gates agree, and each row's C-predecessor
is the same tuple's row. The exact form of the renewal,
H_t=aG_tC H_(t-1)+aG_t[1_r J_(t-1)+e_1 B_(t-1)] with J=u^T M and B=v_H^T M,
therefore gives one common row vector

    V_(i,t)=a g_(i,t)(V_(i,t-1)+J_(t-1)),  V_(i,0)=0,
    V_(i,N)=sum_(s=1)^N a k~_(i,s) J_(s-1),
    k~_(i,s)=a^(N-s) prod_(v=s)^N g_(i,v),                      (4.1)

with the public reset gate included at v=N. (This re-derives formula (10) of
the unreviewed unpaired proof from the VERIFIED renewal.) In matrix form, the
survivor block of tuple common modes is

    V=F~ Jcal,  F~ in (0,1)^(m x N) with STRICTLY INCREASING rows,
    Jcal in R^(N x r) with rows J_(s-1), shared by ALL tuples.      (4.2)

Every tuple reads the SAME chronological row signal Jcal through its own
monotone survival profile. The legal query reads
sum_i zeta_i V_i=(F~^T zeta)^T Jcal, with |zeta_i|<=400/sqrt(n) on ordinary
rows (the accepted 100/sqrt(n) per-site leakage, four sites). Lemma 2 gives
the matching lower form with zeta=a s_gate xi/sqrt(n) on the shifted sites.
Thus the only freedom beyond the paired channel is the shared signal Jcal,
and cohorts differ only through their monotone profiles. This is the exact
form of items 1-3.

## 5. Multiple donor cohorts into one survivor group

**Design (twin-donor epochs).** m_s survivor tuples stay at g_H=1-n^(-2).
Donor tuples come in twins (i,i'). Donor i is high on [1,t_i] and low
(g_L=.995) after; its twin is low on [1,t_i] and high on (t_i,t_+]. A
single interpolated gate makes t_i continuous. The high-set size is then
public at every step, which removes the cross-cohort coupling through 1/|A_t|
that would otherwise make one donor's departure time change every other
donor's transfer. Parameters theta_i=t_i come from an odd entropy-spread map
of B^D, as in the accepted profile lemma, with D=floor(m_d/C).

**HEURISTIC estimate.** In the protection picture of the accepted Gamma
proof, donor i's compensator column contributes to the survivor common row
an amount proportional to the time it spent inside the high set. Different
donors occupy different parameter columns, so by orthogonality in v their
contributions add in quadrature. With a spread map, a constant fraction of
donors differ by Theta(t_+) on every boundary point. This suggests
||Delta(w^T O_* M_N)||=Theta(T), and by Lemma 2 visibility
Theta(T sqrt(m)/n). So D=Theta(m) is plausible at T sqrt(m)>=C n, that is
P~n sqrt(m) and R_abs~sqrt(P)~sqrt(n) m^(1/4).

**Frontier.** D~m with R_abs^2~n sqrt(m) gives D~R_abs^4/n^2. This is
EXACTLY the accepted localized frontier d_F=Omega(min(n,R_abs^4/n^2)) from
the energy-credit tradeoff folder. One survivor group plus many donors
reproduces the known linear tradeoff; it does not beat it.

**Status.** CONDITIONAL. The first missing lemma is a version of Theorem B
for a TIME-VARYING high set. When donors leave at distinct times, the
protected zero-sum space shrinks. One needs a lower bound on the survivor
common component created at each departure, uniform over all boundary
departure-time vectors, together with complement damping between
departures. Theorem B covers a single fixed survivor set only.

**Whatever that lemma gives, D<=m_d<n/400 by Section 1.2: PROVED.** This
route cannot give omega(n). FAILED for the stated goal. First failed
inequality: D<=#donor parameters<=m<n.

## 6. Many cohorts and many epochs: a conditional code barrier

To exceed n one needs omega(n/m) parameters per tuple (1.2). By (4.2) the
only place they can be read is the shared signal Jcal through monotone
profiles. The natural design has K survivor cohorts with staggered onsets
u_1<...<u_K and donors whose in-set occupancy varies per epoch. By Abel
summation,

    sum_j xi_j V_j=sum_s w_s Theta_s,  w=F~^T xi,  TV(w)<=m_s,  |w_s|<=m_s,  (6.1)

with Theta_s=aJ_(s-1). The query sees Lipschitz-in-profile time averages of
the shared signal, never independent cohort-by-epoch entries.

**Hypothesis H_TM (sparse resummed transfer).** On the family considered:

- (a) Bath, front, terminal-row and eps-channel contributions to nu(Delta M)
  are <=epsilon/8.
- (b) The history-dependent part of Theta is supported, at each s, on at most
  m_act public "active" parameter columns. Each column z is active only on a
  public time window W_z. Sum_z |W_z|<=m_act N, the number of columns is
  Z<=4m+2N+4, and |Delta Theta_(s,z)|<=theta_max.

**THEOREM 4 (CONDITIONAL on H_TM).** Let eps=.001,
kappa_0=400 sigma sqrt(l/n)<=14.5, and let n be large enough that
eps n>=16 kappa_0 m_s sqrt(m_act) theta_max. Then every robust D-section in
the family satisfies

    D <= k_loc+2Z+16 kappa_0 m_s sqrt(m_act) theta_max N (m_act+m_s)/(eps n),
    k_loc <= m+82400 P/sqrt(n).                                  (6.2)

Proof. The code has three parts. (i) The accepted inverse-level code of each
local product row plus the m exact traces, refined fourfold. Cycle-row
coefficient: each copy has per-site adjoint <=100/sqrt(n), so ||Delta L^Tc||
is controlled by 2 sigma sqrt(l/n) 100 H(Delta K)/n<10.3 H(Delta K)/n.
With the VERIFIED entry bound 1/p and H<=sqrt(mT min(m,T))/p, the choice
p_loc>=82400 sqrt(mT min(m,T))/n gives nu(Delta L)<=eps/4 for equal codes.
Equal traces make compensator rows equal. (ii) The VERIFIED quantile code of
each survivor profile F~_j, with p levels:
|Delta F~_j|<=2/p. (iii) Block sums of Theta_(.,z) over a global grid of
blocks of length g, for each column z and each block meeting W_z. For two
histories with equal codes, write Delta(sum_s w_s Theta_s)=A+B, where
A=sum_s w_s Delta Theta_s and B=sum_s Delta w_s Theta'_s. Equal block sums
give A=sum_b sum_(s in b)(w_s-w_(s_b))Delta Theta_s, so

    ||A||_2 <= TV(w) g sqrt(m_act) theta_max <= m_s g sqrt(m_act) theta_max,
    ||B||_2 <= m_s (2/p) N sqrt(m_act) theta_max.

Take g=floor(eps n/(8 kappa_0 m_s sqrt(m_act) theta_max))>=1 and
p=ceil(16 kappa_0 m_s sqrt(m_act) theta_max N/(eps n)). Then
(kappa_0/n)(||A||+||B||)<=eps/4. With (a), equal codes give
nu<=eps/4+eps/4+eps/8<eps, and the actual distance is <eps+8e-9<.002.
Borsuk-Ulam bounds D by the code dimension. Counting: blocks
<=m_act N/g+2Z<=16 kappa_0 m_s m_act^(3/2) theta_max N/(eps n)+2Z; profiles
m_s(p-1)<16 kappa_0 m_s^2 sqrt(m_act) theta_max N/(eps n). All three maps are
continuous: the local and profile codes by the VERIFIED strict-monotone
quantile lemma, block sums by continuity of Theta. QED.

**Corollary 4a (CONDITIONAL).** Suppose resummation gives
theta_max<=theta_0/m_s (each step's mean-removal over the high set dilutes
an injection by its size), and m_act<=4m (compensators plus currently
occupied cycle columns). Then

    D <= 9m+4N+8+(82400+4.7*10^6 theta_0) P/sqrt(n) < n/30+O(P/sqrt(n)),

valid for n>=5.4*10^8 theta_0^2 (this makes the block length g>=1 for every
m<=n/400). Arithmetic: m_act<=4m, m_s<=m, N<=2T and sqrt(m)<=sqrt(n) turn
the last term of (6.2) into <=160 kappa_0 theta_0 m^(3/2)N/(eps n)
<=4.7*10^6 theta_0 P/sqrt(n); 2Z<=8m+4N+8; and m,T<n/400.

**D=omega(n) is then impossible at P=o(n^(3/2)).** This is the same P/sqrt(n)
law as the VERIFIED paired barrier. Note what dominates: the additive O(m+T)
comes from storing one block per occupied column. It is linear, not
superlinear.

**Why this is not a theorem of the actual system (first missing
inequalities).**

- (b)-sparsity can fail for cycle columns. A track column's credit
  co-moves with its tuple after the visit and stays nonzero in later J_s
  whenever the high set changes. Only the rigorous bound
  |J_(s,z)|<=||u|| ||M_s e_z||<=2.01 s/sqrt(n) is available, since
  ||u||^2=gamma^2/k-2gamma^3/k^(3/2)+gamma^4 r/k^2<4.02/n. With m_act=Z and
  that Born-size theta_max, (6.2) reads D<=O(m T^2 (m+T)^(3/2)/n^(3/2)),
  which does not close.
- The resummed size theta_0/m_s is supported by the Gamma counterexample
  (survivor common entries ~T/m per donor column) but is not proved. Proving
  it needs a nonperturbative bound on J along changing high sets.
- (a) is unproved. The rigorous row ledger gives the bath coefficient
  <=102, front <=100/sqrt(n) per row, but their vectors are driven by J and
  B, whose sizes are the same open quantities.

## 7. Positive multi-epoch route: where it fails (HEURISTIC)

Take K survivor cohorts with staggered onsets and m_d donors whose occupancy
in each epoch is a parameter, so D=K m_d. In (6.1), w_s=sum_(j:u_j<=s) xi_j h_j
moves by at most h/K per epoch. With spread parameters (entries +/-rho,
rho~tau/|A|, tau=T/K), the best query gives
||sum_e W_e Delta delta_e|| ~ sqrt(m_d) rho h sqrt(K) ~ T sqrt(m_d/K) for
K<=m_d, and ~T for K>=m_d. Requiring Lemma 2 visibility (>~n) gives:

- K<=m_d: T sqrt(m_d/K)>~n, hence P>=m_d T>~n sqrt(K m_d)=n sqrt(D).
- K>=m_d: T>~n, which violates T<n/400 up to constants. Otherwise P>=K T>~n K,
  hence D<=K^2<~(P/n)^2.

In both cases D<~(C P/n)^2, so **D=omega(n) forces P=omega(n^(3/2))**.
First failed inequality: (C P/n)^2>=D=omega(n) is incompatible with
P=o(n^(3/2)). This agrees with Corollary 4a, but it is HEURISTIC: it uses
protection-picture amplitudes, not a proof.

Spatial packing (more tracks per tuple) multiplies m. Temporal packing
(sequential packets with resets in between) adds to T. Both enter only
through P and give nothing beyond these laws. Trace corrections are needed
only to defeat a particular code, not for positive sections. Each one is a
single-gate change with operator effect <=|Delta g|(a||M_(N-1)||+1) per
tuple, additive by the triangle inequality. They cost nothing in exponent.

(The per-site leakage 100/sqrt(n) for off-cycle compensator rows uses the
same unrolling as for cycle columns: ||O e_z-e_z||<=6/sqrt(n) for z>=d by
the Householder row identity, so |c_(L,z)|<=q_f^L(1+6L)/sqrt(n).)

## 8. The ten requested investigations

| # | Question | Result | Label |
|---|---|---|---|
| 1 | Multiple donor epochs | Read only through the shared signal Jcal (4.2). Per-donor parameters give D<=#parameters (1.2). Twin-donor design plausibly gives D~m, frontier R^4/n^2 = accepted localized frontier | cap PROVED; D~m CONDITIONAL; no omega(n): FAILED |
| 2 | Multiple survivor cohorts | Cohorts differ only by monotone profiles F~ reading the same Jcal; legal queries add cohorts in quadrature, never cancel (Lemma 2) | PROVED |
| 3 | Exact joint transfer operator | H_N=sum_s beta_s S_L(s-1)^T+eps_s rho_(s-1)^T: scalar kernels on local column sums; two-scalar-input probe form | PROVED (+checks) |
| 4 | Trace corrections | Needed only to defeat a code; one gate per tuple; additive operator cost | PROVED (bound); irrelevant to positive sections |
| 5 | Legal-query visibility across cohorts | nu>=.0059||Delta M||_F/n; cohort quadrature (3.2); nu<=.034||Delta M||_op/sqrt(n) | PROVED |
| 6 | Temporal/spatial packing | Enters only through P=mT; mean parameter-block area must be o(sqrt(n)) for D=omega(n) | PROVED (counting); no gain: HEURISTIC |
| 7 | Finite-radius conditioning | All identities exact; barrier codes finite-radius; no linearization anywhere | PROVED where stated |
| 8 | Widening the logarithmic family | Any per-tuple widening has D<=O(m)=O((log n)^4) | PROVED |
| 9 | O(n)-coordinate chronology compression | Parameter side confined to public dim<=4m+4N+2 (1c). Static code of dim O(m+T+P/sqrt(n)) under H_TM (Thm 4) | 1c PROVED; code CONDITIONAL |
| 10 | Best theorem | See Section 9 | |

## 9. Verdict

**Strongest unconditional new results.** Theorem 1 (exact scalar-kernel joint
transfer, all Householder orders), Corollaries 1a-1c, the cohort factorization
(4.1)-(4.2), Lemma 2 (Frobenius / cohort-quadrature legal-query lower bound),
and the parameter caps of Section 1.

**Strongest negative statement.** CONDITIONAL on H_TM: D<=n/30+O(mT/sqrt(n)).
So D=omega(n) requires mT=omega(n^(3/2)). Under H_TM the requested regime is
empty. Unconditionally: every family with at most c continuous parameters per
tuple has D<=c m<c n/400.

**Positive direction.** No omega(n) section was constructed. The best positive
candidate is the twin-donor design, D~m at R_abs~sqrt(n) m^(1/4) (CONDITIONAL).
It coincides with the accepted localized frontier.

**Exponent below 3/4: NOT proved.** The constructive superlinear threshold
remains O(n^(3/4)(log n)^(3/2)) with D=Omega(n log n). The general bracket
[1/4,3/4] and the full-model gap are unchanged.

**Single next step.** Prove or refute H_TM(b) with theta_max=O(1/m_s) for
staggered-onset families. Concretely: bound sup_z |Delta J_(s,z)| along a
time-varying high set by a Theorem-B-type invariant-space argument applied to
J=u^T M. A proof would turn Corollary 4a into an unconditional closure of the
corridor route at mT=o(n^(3/2)). A counterexample (J entries of size >>1/m
on omega(m) persisting columns) is exactly what a positive omega(n)
construction would have to exploit.
