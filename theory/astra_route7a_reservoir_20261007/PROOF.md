# Route 7A: precharged imprints, high-donor captures, and a finite recent-capture code

Date: 2026-10-07. Requested Astra research, performed in Codex.
Repository status: **PENDING REVIEW**. Overall Route 7A status: **PARTIAL**.

## Resume / result calibration

- Search: public sensitivity precharge, rapid private donor imprints, capture without lowering donors.
- No positive D=Omega(n), mT=o(n^(3/2)) construction is established.
- New author result: in the fixed-source moving corridor, the complete feedback rows belong to a PUBLIC parameter subspace of dimension at most 4m+4N. This is an exact algebraic statement, not the dimension of the whole history.
- New author result: for distinct strong Walsh captures and a final low-donor public clear, a fixed number of recent captures suffice at a fixed legal-query tolerance when N sqrt(m)/n is bounded. Their full parameter responses have a continuous code of dimension O(m+N), including donors HIGH at captures.
- Consequently the specified public strong-capture/final-clear Route 7A family has D=o(n) at the intended scaling. This does not use the separated-capture signal theorem, the 7.213 checkpoint, the stationary-complement checkpoint, or Carl–Pajor.
- The conclusion uses the inherited all-future ordinary-row legal-query bound, explicitly identified below. It is not a theorem about arbitrary adjoints, all parameter features, private arbitrary survivor words, or omitting the final clear.
- Next: determine the robust dimension of the un-cleared donor feedback matrix with matched local traces. Exact rank alone is insufficient.
- No numerical experiments were run. Formal estimates decided the first candidates; no computed data are presented as proof.

## 1. Exact model and inherited query premise

Use the frozen reference O_*, its actual dense perturbation, balanced four-site tuples, one fixed source feature, and the inverse lift of:

1. [unpaired corridor](../codex_unpaired_corridor_sensitivity_20261003/PROOF.md), sections 1–5, 8–10;
2. [holding cost](../codex_holding_cost_attack_20261003/PROOF.md), section 4;
3. [linear frontier](../codex_linear_dimension_frontier_20261006/PROOF.md), sections 3, 5, 8–10.

There are m tuples, two moving tracks A+i+t and B+i+t, and two stationary compensators per tuple. Four gates in each tuple agree. The private states have zero total sum. Consequently the entire bath/front state and its gates are public at GLOBAL time, even for arbitrary legal private donor words. No bath or front is restarted.

Let k=floor(n/2), l=n-k, r=k-1, a=1-1/n. Write v_H for the second Householder row to avoid confusing it with a probe bank. Exactly,

    M_0=0,
    M_t=G_t(a O_* M_(t-1)+I_r),
    O_*=C+1 u^T+e_1 v_H^T,
    J_t=u^T M_t, B_t=v_H^T M_t.

C is the OPEN cycle shift and identity off-cycle. O_* is orthogonal: the full O fixes e_0, so its restriction to e_0-perp is orthogonal. All legal G have norm at most one. Thus

    ||M_t||_op <= t,    ||Delta M_t||_op <= 2t.                (1)

The full fixed-feature reference query is

    nu_ref(A)=(sigma sqrt(l)/n) sup_Q ||A^T c_Q||_2,
    .0499 < sigma < .051,
    ||c_Q||_2 <= 1.                                           (2)

Only actual legal futures of length at least one are used. For ordinary survivor rows, the inherited all-horizon bound is

    |c_Q(i)| <= C_Q/sqrt(n), C_Q=100.                          (3)

This is equation (21) and the following ordinary-row discussion in the unpaired proof, section 9. It is NOT valid on the terminal row. We use it only on survivor rows. Terminal/front/bath output is retained and handled by final clearing, not by falsely applying (3) everywhere. Without (3), the query-metric compression theorem below is conditional rather than proved.

The frozen dense-model pair correction is bounded, under the inherited lift premises, by the linear-frontier section 10 equation (18):

    epsilon_dense <= e_R sigma sqrt(l)
       [q_f N(N-1)/n + 14N/n],
    e_R <= 4/(10^8 n^2), q_f<.941.                            (4)

Actual future direct terms cancel at the common actual endpoint. We do not differentiate the inverse-lift controller. The conclusion concerns the complete parameter directions of this ONE fixed-source-feature slice, not the union of all R,W,b features.

## 2. The proposed precharge is real, but is not free

Let V be the stationary zero-sum probe bank from the linear-frontier proof. During a public period with every active donor and survivor high,

    O_* V=V, G_t V=g_H V,
    X_L=M_L V=kappa_L V,
    kappa_L=g_H sum_(u=0)^(L-1)(a g_H)^u.                     (5)

This is exact in the reference model despite the chronological bath/front: the source subspace is stationary and zero-sum, so these rows are not forced. For L=o(n), kappa_L=(1-o(1))L. Precharging for L steps costs mL, including the corridor hold. It cannot be excluded from N.

At the next private donor imprint, from that exact public state,

    X_(L+1)=(a kappa_L+1) G_(L+1)V.

Two imprint choices differ by

    Delta X_(L+1)=(a kappa_L+1) Delta G_D V.                  (6)

This is a genuine large sensitivity change made by a short gate intervention. It initially occupies donor rows. It is not yet a large protected survivor response, and is not a proof of KR robust dimensions.

Capturing with donors high is legal: tuple gates remain in the admitted interval, the four-site state balance is preserved, the bath/front remains public, and the accepted inverse lift and final reset apply. It escapes the LOW-donor-at-capture premise of the supplied mass theorem. It does NOT escape the public-survivor atom identity.

## 3. Failed inference: repeated access to the local precharge is not R fresh reservoirs

For an individual stationary local homogeneous packet, with no new source in that packet,

    v_(t+1)=a g_t v_t.

Its extra high-reference erasure is

    e_t=a(g_H-g_t)|v_t|.

Since e_t <= |v_t|-|v_(t+1)|, exactly

    sum_t e_t <= |v_0|.                                     (7)

With local nonnegative source, the corresponding bound is initial load plus total injected load. Repeating fixed-contrast imprints attenuates the local reservoir geometrically; contrasts of order 1/R preserve load but make each local imprint of order 1/R of that load.

This alone is NOT a theorem about complete feedback. J can replenish a physical donor. We do not absolute-value separately the cancelled contrast and replenishment terms, and do not infer a global signal-mass bound from (7). Adaptive control encodings also require a whole-boundary argument; a late weak axis does not by itself refute every nonlinear encoding.

## 4. New exact right-space lemma: complete feedback has only O(m+N) parameter types

### Statement

For a fixed public geometry and survivor schedule, there is a PUBLIC linear subspace E_par of R^r such that every J_t and B_t, for every legal donor history up to N, belongs to E_par, and

    P:=dim E_par <= min(r,4m+4N).                             (8)

This includes every moving-cycle parameter column, stationary parameter column, terminal path, and front renewal. It does not approximate donor temporal waveforms.

### Proof

Define L_t=G_t(a C L_(t-1)+I), H_t=M_t-L_t, as in the exact unpaired decomposition. Fix a public baseline G_t^0 that agrees on all public rows and has high donor gates. Its local matrix L_t^0 is public, even when the public bath/front changes with time.

A local source path can be private only if it hits a donor-gate site. If it hits moving site A+i+t at time t, its source column injected at time u is A+i+u. Thus the union of possibly affected physical parameter columns lies in the two track intervals of length at most m+N and the at most 2m stationary compensator columns. There is no wrap. For a fixed set I_exc,

    |I_exc| <= 4m+2N,
    (L_t-L_t^0)e_c=0 for c outside I_exc.                    (9)

This deliberately includes more than just donor columns; the conservative bound avoids divisibility or donor-layout issues.

Set

    E_par = span{ e_c : c in I_exc }
          + span{ (u^T L_t^0)^T, (v_H^T L_t^0)^T : 1<=t<=N }.

It is public and has dimension at most |I_exc|+2N. The exact Duhamel formula is

    H_t=sum_(s=1)^t Phi_C(t,s) aG_s
                     [1 J_(s-1)+e_1 B_(s-1)].               (10)

Multiplying by u^T or v_H^T produces scalar coefficients multiplying earlier J and B rows. Meanwhile u^T L_t and v_H^T L_t belong to E_par by (9). Induction from J_0=B_0=0 proves (8).

The coefficients in this induction can depend privately and arbitrarily on the entire donor history. This does not change the right subspace. In particular no false assertion that J or B is a scalar statistic is made: each requires P coordinates. Also, R readout rows would still naively require RP coordinates. The next result is what removes that factor at fixed query tolerance.

## 5. Distinct strong Walsh captures attenuate an old survivor packet in query norm

Assume survivor gates are high except public balanced one-step Walsh captures. Their nonzero characters are distinct and orthogonal under uniform survivor weight. At each capture the low gate is at most 1-2b_0, with an absolute b_0>0; b approximately .0025 admits, for example, b_0=.0024. Captures can be arbitrarily spaced; donors can be high.

Consider any ell of these captures. In co-moving survivor coordinates their local suffix product D has entries bounded by

    D_ii <= (1-2b_0)^(X_i),

where X_i counts low choices at site i. Scalar a factors and ordinary high gates only decrease the entries. Distinct Walsh characters are pairwise independent under uniform site sampling, whether or not they are linearly independent. Consequently

    E X_i=ell/2, Var X_i=ell/4,
    P(X_i<ell/4) <= 4/ell.

Hence

    (1/h_S) sum_i D_ii^2
       <= F_ell := 4/ell + (1-2b_0)^(ell/2)
       <= 4/ell + exp(-b_0 ell).                            (11)

Use min(1,F_ell) if desired. The count is over the actual equally represented Walsh sites; repeated physical tuple copies do not alter the probability calculation. A nonzero XOR relation among three or more labels does not invalidate pairwise independence.

If these ell labels are linearly independent, the exact stronger bound is

    E D_ii^2 <= product_c[(g_H,c^2+g_L,c^2)/2]
              <= exp(-b_0 ell).                            (12)

This is attenuation of the LOCAL old survivor packet, not rapid decay of the entire complete state. Old donor information can regenerate J at later times; that later J is retained in the code below.

## 6. Complete final clear, including bath/front/terminal

A final public low-donor clear is part of the family treated here. During it all survivor gates equal g_H; all other selected memory gates are at most q_*<=.9992. No changing bath or front is frozen. The first front gate is even smaller. Trace correction, if used, precedes this common clear.

Let H_t^S be the co-moving survivor zero-sum space, P_t its orthogonal projection, and u_t^S the normalized survivor constant vector. O_* maps H_(t-1)^S isometrically to H_t^S. Gates act there by g_H, so its orthogonal complement is invariant as well. Put p=c h_S, c=gamma^2/k. Exactly

    <u_t^S,O_*u_(t-1)^S>=1-p,
    ||1_(outside S_t) O_*u_(t-1)^S||^2=2p-p^2.              (13)

Here p<.01 and g_H>.99. Write delta=1-q_*^2.

For a unit vector in the complement, after the first orthogonal step write y=eta u_t^S+v with v outside S_t. If ||v||>=sqrt(p)/4, the first gate loses at least delta p/16 of squared norm. Otherwise |eta|>=sqrt(1-p/16)>.99. After that gate and the next orthogonal step, the outside component has norm at least

    g_H |eta| sqrt(2p-p^2)-||v|| > .73 sqrt(p).

The second gate then loses more than delta p/16. All a factors are contractions and may be factored out. Therefore every two-step chronological clear block on the complement obeys

    ||A_(t+1) A_t restricted to complement||
       <= sqrt(1-delta p/16) <= 1-delta p/32.               (14)

This proves a complete homogeneous contraction, not a group-average estimate. It includes terminal and all global front coordinates.

Taking at least

    L_clear = 2 ceil[320 log(n)/(delta p)]                  (15)

steps makes the complementary pair operator norm at most 2N n^-10. This has the inherited O((n/m)log n) cost. The final public survivor-uniform reset is another contraction and preserves the zero-sum split; public front gates need not equal the survivor reset gate. The protected survivor component need not decay rapidly during this clear.

## 7. New recent-capture continuous code

Fix ell. If R>=ell, cut immediately before the earliest of the last ell captures; call that time t_0. If R<ell, cut at zero and retain all captures.

The survivor pair recurrence, now for ALL r fixed-feature parameter columns, has public direct forcing, so exactly

    Delta M_S(N)=D_(N,t_0) Delta M_S(t_0)
                 +sum_(t=t_0)^(N-1) beta_t Delta J_t,       (16)

where the harmless normalization of beta may be chosen without sqrt(h_S). Co-moving shifts are understood. This local formula includes the complete private J. The row-1 input never lands on survivor characteristics under no-wrap.

The recent public kernels are piecewise parallel, with at most 2ell+2 segments. Choose beta_t=lambda_t b_sigma with public lambda_t and public b_sigma. Let Q_par be any fixed orthonormal basis of E_par and store, per single history,

    C_sigma(H)=sum_(t in sigma) lambda_t J_t(H) Q_par.

This is continuous. The code dimension is

    q_recent <= (2 min(R,ell)+2) min(r,4m+4N).              (17)

Equal codes make the ENTIRE recent term in (16) equal, across all parameter directions. No chosen-probe restriction or parameter-complement assumption is used. The initial term remains; it is quantitatively small in the actual query metric as follows.

Let P_N project to survivor zero-sum rows. By (3), each coordinate of P_N c_Q on the survivor set has magnitude at most 2C_Q/sqrt(n). By (1) and (11), the old protected term has legal-query norm at most

    (sigma sqrt(l)/n) 2N ||D_(N,t_0)^T P_N c_Q||
       <= 4 C_Q sigma (N/n) sqrt(l h_S/n) sqrt(F_ell)
       <= 32 (N sqrt(m)/n) sqrt(F_ell).                    (18)

We used h_S=2m and sigma<.051; 32 is a safe round-up. When t_0=0 the initial term is exactly zero, so this error is zero.

Combining (14)–(18) and the dense correction,

    equal C_recent => nu_actual(pair)
       <= 32 (N sqrt(m)/n) sqrt(F_ell)
          + .102 N n^(-10.5) + epsilon_dense.              (19)

Equation (19) does not bound the whole survivor Frobenius norm. It bounds every legal future query, which is exactly what the robust-section collision needs. It would not follow for arbitrary concentrated unit adjoints. There is no sqrt(K), sqrt(r), or Frobenius conversion hidden in (18).

## 8. Quantitative choice and Borsuk–Ulam

Let A_0>=max(1,N sqrt(m)/n) be a public bound, let tau=5*10^-4, and set epsilon=tau/(32 A_0). It is enough to choose the INTEGER

    ell >= max(1,8/epsilon^2,(1/b_0) log(2/epsilon^2)).       (20)

Then F_ell<=epsilon^2, and the first term of (19) is at most tau. If the labels are linearly independent, ell >= (1/b_0)log(epsilon^-2) suffices instead. These constants can be enormous; this is an asymptotic statement.

For sufficiently large n in the admitted corridor, the complementary and dense errors together are less than .0005. Equal codes therefore imply actual fixed-feature pair distance less than .001, strictly below .002.

On a continuous robust section S^(D-1), a continuous q_recent-coordinate code has equal antipodes if q_recent<D. This contradicts robust separation >.002. Consequently

    D <= q_recent.                                         (21)

No Gaussian width, logarithmic width theorem, signal-mass bound, exact history reconstruction, or linearity of the section is used. No section injectivity is inferred from Jacobian rank.

## 9. Route-6 / Route-7A substitution and total cost

Suppose

    R~log log n, m~K~n/R, N~C_T sqrt(nR), C_T fixed.

Then N sqrt(m)/n=O(C_T), so ell in (20) is a constant independent of n and R. Eventually R>=ell, however large that asymptotic threshold is. Since N/m=O(R^(3/2)/sqrt(n)) tends to zero,

    q_recent=O_(C_T,b_0,tau)(m+N)
            =O_(C_T,b_0,tau)(n/R)=o(n).                    (22)

Thus the public, distinct strong one-step capture family WITH the complete final clear cannot realize D=Omega(n) in the fixed-source query metric, even with donors high at every capture and arbitrary donor words. It is unnecessary to prove the previous Lambda bound in this family.

Precharge L~sqrt(nR), R imprint/release blocks of length O(n/m), a trace tail O(log n), clear O((n/m)log n), and one reset have

    N = L + O(R n/m + (n/m)log n + log n),
    mN = Theta(n^(3/2)/sqrt(R)) + O(nR+n log n).

This is a genuinely subcritical COST schedule; the obstruction is its robust dimension, not an omitted precharge/clear cost. The same bath/front/no-wrap legality holds asymptotically because (m+N)/n tends to zero. Constants and divisibility can be handled by restricting to admitted widths; the obstruction itself is uniform over those widths.

This does not rule out Route 7A without a clear, a scheme with vanishing capture contrast, or a different query/feature family. It also does not assert q_recent=o(K); O(K) is enough because K=o(n).

## 10. Failed attempts and adversarial checks

### 10.1 One rapid imprint

Equation (6) creates large donor credit but only K independent scalar donor controls. It cannot alone establish KR dimensions. An immediate high-donor capture does not magically move this donor-local state to a new survivor row; the previous J enters the survivor recurrence with its actual time index.

### 10.2 Reusing the local reservoir

Equation (7) rules out R independent full-amplitude LOCAL cash-outs without replenishment. We explicitly leave full feedback replenishment intact. The recent-capture theorem resolves the scoped robust-dimension question without pretending to resolve that signal-budget question.

### 10.3 Persistent hidden modes

A survivor Walsh mode can survive a long ordinary interval essentially unchanged. This is fully compatible with (11): the loss there comes from MANY strong capture gates, not from an n/m relaxation of all modes. Old donor modes that affect late J are exactly encoded, not assumed dead.

### 10.4 Walsh aliases / never-low sites

Distinct labels need not be independent. Chebyshev gives the safe 4/ell tail. Sites never lowered can exist, but their total fraction is at most 4/ell. Their legal-query contribution is small by (18), even if old credit concentrates there. Arbitrary concentrated adjoints would invalidate this argument.

### 10.5 Front and terminal bypass

E_par includes all public local front/terminal source rows for every global time. Formula (10) retains all repeated feedback. Final clear contraction is a full-state estimate on the complement, including the terminal row. No terminal coordinate dilution assumption is made.

### 10.6 Growing precharge constants

If A_0 grows with n, ell grows as O(A_0^2) in the distinct-label estimate. Then (22) need not be o(n). Fixed C_T is substantive. The theorem is not an arbitrary-duration obstruction.

### 10.7 Repeated labels, weak masks, private survivor words

Repeated labels fail the variance proof; a permanently high half can remain. Contrasts tending to zero fail the fixed b_0 hypothesis. Private survivor schedules fail the public direct-forcing cancellation and public atom code as stated. None is silently covered. Repeating a SINGLE public fixed mask nevertheless has a small exact spatial suffix span; merely repeating that one mask is not automatically a successful alternative.

## 11. Alternative investigated: keep the donor feedback matrix instead of clearing it

The remaining promising change within this lane is to omit the final low-donor clear, match local donor traces where possible, and read the private donor-to-donor feedback matrix itself. Its row kernels are PRIVATE:

    V_i(N)=a sum_(s=1)^N [a^(N-s) product_(v=s)^N g_(i,v)] J_(s-1).

The right space still has P=O(m+N), but the number of private receiver rows can be K (or m). Thus exact formal capacity may be KP, rather than the O(P) public recent-capture code. This is a possible bypass, not a robust lower bound.

An attempted implementation uses gate-order information. For two private gate patterns P,Q in consecutive slots, the exact affine endpoint difference from a common precharged M is

    Delta M_2 = a^2 [G_Q(2)O_*G_P(1)-G_P(2)O_*G_Q(1)]O_* M
              +a [G_Q(2)O_*G_P(1)-G_P(2)O_*G_Q(1)]
              +G_Q(2)-G_P(2).                              (23)

Public bath/front factors remain at their actual times (1),(2). This is not a frozen-bath commutator model. The last two terms cannot be discarded when matching local traces.

The noncommuting uniform-feedback part, on a stationary donor/survivor block with c=gamma^2/k, has second-order cross-block form proportional to

    c kappa epsilon^2 (P_S Q 1)(1^T P V),                  (24)

up to sign, for disjoint donor selector P and survivor selector Q. Its norm is at most C kappa epsilon^2 m/n. The term is obtained by expanding (I-epsilon Q)(I-c11^T)(I-epsilon P) in the stationary block; it is only that path contribution, not the complete chronological response (23).

At kappa~sqrt(nR), m/n~1/R, its query scale is at most O(epsilon^2/R). A single two-step order imprint therefore does not reach .002 uniformly as R grows. Repeating such loops consumes local reservoir through (7); an assertion of feedback-restored gain would require a new proof. Known bilinear-control Lie-bracket accessibility does not provide a robust singular-value bound or legal-query margin here.

Novelty calibration: gate-order commutators are an existing control mechanism, not a new primitive. See Zhang and Li, *Analyzing Controllability of Bilinear Systems on Symmetric Groups* (2017), https://arxiv.org/abs/1708.02332, and Cheng, Zhang and Li (2020), https://arxiv.org/abs/2009.03430. What remains potentially new is a fixed-model robust dimension/cost separation; none is established here. A mere replay/decoder pipeline or exact controllability rank would not qualify.

### 11.1 A precise legal trace-neutral alternative to test next

There is a way to eliminate the obvious stationary local-trace nuisance without a long low-donor tail. Let the incoming LOCAL scalar donor trace tau be public. Choose g_*=.9975 and epsilon=10^-4 (for sufficiently large n these are strictly inside the inherited gate interval). For a control x in [-1,1], use:

    d_1=g_*+epsilon x,
    d_2=g_H,
    tau_target=g_* [1+a g_H(1+a g_*(1+a tau))],
    d_3=tau_target/[1+a g_H(1+a d_1(1+a tau))].             (25)

At the middle step perform the public survivor capture, with donors HIGH. All three steps are part of the complete recurrence. Direct substitution into tau_next=d(1+a tau) gives tau_after3=tau_target exactly, for every x.

Writing the denominator as A+B d_1 with A,B>0,

    d_3=g_* (A+B g_*)/(A+B d_1),
    |d_3-g_*| <= g_* epsilon/(g_*-epsilon)<.000101.

Thus the gates are legal uniformly in tau>=0, and the correction is continuous. The next triple again has a public incoming local trace. Public all-high waiting can be inserted by replacing the middle update with its exact positive affine map; the same ratio argument proves legality. The complete feedback state is not reset or matched by this calculation.

Repeat R such stages on K donor groups, then use only the common state reset, with NO complementary clear. There are KR private controls but no claim of KR robust dimensions. The precharge and a three-step implementation cost m[L+3R+1]; adding O(n/m) public waits per stage adds O(nR). Both fit the subcritical cost at L~sqrt(nR). Earlier feedback is propagated by the exact matrix product, not discarded.

For immediate capture, (6) and the exact one-step survivor input show that the NEW protected Walsh component has operator norm at most

    C b epsilon p kappa, p=Theta(m/n),                    (26)

on the chosen stationary bank. Indeed the imprint's summed donor forcing has norm at most epsilon sqrt(m), u contributes c=Theta(1/n), and the normalized survivor read contributes sqrt(h_S)=Theta(sqrt(m)). At Route scaling its legal-query gain is only O(C_T b epsilon/R). This refutes an immediate constant-margin claim based solely on that new Walsh component. It does not bound the retained un-cleared donor feedback or the cumulative response of all stages.

The candidate's unresolved mechanism is therefore precise: can the complete donor feedback retained by (25), including any public release waits, provide a robust matrix-valued query signal even though local traces are exactly matched and immediate survivor capture is weak? Equation (23), not a free commutator model, governs the answer.

## 12. Next exact obligation and falsifier

For zero-initial precharge/imprint histories with a common final reset but NO low-donor clear, construct or rule out a continuous sphere of dimension c n whose donor-feedback matrix, after matching local scalar traces, obeys

    inf_theta sup_(legal Q)
      (sigma sqrt(l)/n)||Delta H_N(theta)^T c_Q|| > .002,
    mN=o(n^(3/2)).

Focus first on the exact trace-neutral family (25), allowing O(n/m) public release waits, and retain the complete J/B renewal. Prove a uniform finite-amplitude lower bound or a continuous O(m+N)-coordinate approximate code for its un-cleared donor channel. A nonzero determinant, exact rank, or selected singular values at one point do not suffice. This is ONE next robust-observability obligation, not permission to change the frozen model or source.

No bounded experiment was necessary for the public strong-capture attempt: (19)–(22) furnish an analytic falsifier. A later numerical singular-value check of the un-cleared gate-order family would be useful only after its actual legal-query operator and trace matching have been specified.

## 13. Status table

| Claim | Author status |
|---|---|
| Exact high-gate precharge (5), one-step imprint (6) | PROVED in reference model |
| Local reservoir erasure budget (7) | PROVED; not a complete feedback budget |
| Public complete-feedback parameter space (8) | PROVED, pending hostile review |
| Distinct-Walsh suffix attenuation (11) | PROVED |
| Complete chronological final-clear contraction (14) | PROVED under stated bath/front gate bounds |
| Legal-query recent-capture code (19) | PROVED using explicit inherited ordinary-row query premise (3) and dense comparison (4) |
| Public strong-capture, high-donor, final-clear Route 7A at fixed C_T | REFUTED as a linear robust-dimension construction under this scope |
| Route 7A in broader allowed schedules | PARTIAL / OPEN alternatives remain |
| Un-cleared private donor-feedback architecture | OPEN conceptual candidate; no novelty or robust dimension claim |

No CURRENT_THEORY.md change or repository-level verification is authorized by this author report.
