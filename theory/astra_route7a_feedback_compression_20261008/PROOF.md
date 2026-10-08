# Route 7A: complete donor-feedback compression without a final clear

Date: 2026-10-08. Codex, requested Astra focused investigation.
Starting commit: `127eb79af4866368192dbf27d7f6086adac02659`.
Repository status: **PENDING REVIEW**. Overall main-target status: **PARTIAL**.

## 0. Resume and strongest result

The central target D=Omega(n), mT=o(n^(3/2)) remains unsolved. This report claims a new scoped obstruction, not a universal RNN theorem.

**New author theorem.** For the consecutive three-step trace-neutral donor protocol, complete donor feedback can be approximated by ONE common receiver row, driven by the ACTUAL complete J history. The residual has a uniform all-legal-query bound that tends to zero at Route-6 scaling. No final low-donor clear is needed.

Combining this with an exact public parameter subspace and a recent-capture code gives

    D <= O_(C_T,b_0,query tolerance)(m+N) = o(n)

for the public, distinct strong-Walsh capture family at m~n/R, N~C_T sqrt(nR), R~log log n, fixed C_T. One version permits arbitrary public survivor gates between captures when the last ell captures occupy at most 3ell+1 steps; this covers the public-cohort schedule of the sparse prototype subject to the explicit inherited bath/front/query premises below. A second version permits longer waits AFTER complete triples when the survivor bank is uniformly high between captures.

This closes a previously unbounded receiver-filter term in H_N. It does not show that H_N has small diameter: the shared receiver and bath rows may carry substantial information, and their complete parameter vectors are explicitly coded.

The meaningful remaining alternative is a LONG public release interval INSIDE an imprint/compensation block. Its scalar trace correction remains legal, but the new receiver error estimate grows with the interval length. That is the single next obligation.

No new numerical experiment was run. Corrected simulation results were read as diagnostics, not used as proof. No historical files, measurements, or CURRENT_THEORY.md are changed.

## 1. Exact scope, notation, and dependencies

Use even admitted n>=10^6 (n divisible by four suffices), k=l=n/2, r=k-1, d=floor(n/4), a=1-1/n, gamma=(1-1/sqrt(k))^-1, c=gamma^2/k, eta_H=gamma/sqrt(k). Let e_T denote the terminal coordinate e_(d-1), and e_P=e_(d-2). Do not confuse eta_H with a query-error tolerance.

The complete fixed-source reference sensitivity is

    M_0=0, M_t=G_t(a O_* M_(t-1)+I),
    O_*=C+1 u^T+e_1 v_H^T,
    u^T=eta_H e_T^T-c 1^T, v_H^T=eta_H 1^T,
    J_t=u^T M_t, B_t=v_H^T M_t.                         (1)

All quantities J,B are full r-coordinate ROW VECTORS. O_* is orthogonal on the selected memory block, and 0<=G_t<=I. Therefore ||M_t||_op<=t. There is one fixed source with physical coefficient sigma sqrt(l), .0499<sigma<.051. No parameter coordinate is selected independently at different source times.

Private gates occur only on m or fewer four-site donor tuples, each with synchronized moving and stationary gates. They are the consecutive trace-neutral triples of section 3, separated only by donor-common PUBLIC operations. Incoming local scalar traces are public and common across donor tuples. Public precharge is included in N, followed by R triples and the common endpoint reset. Source, gates, and inverse-lift inputs have the inherited meaning: the realized inputs are frozen during differentiation.

For the explicit no-wait version N=L_pre+3R+1. Public capture rows form fixed co-moving cohorts, disjoint from donors/front/terminal, of total size h_S<=4m. Private donor sites plus public cohort sites number at most 8m at each time. All remaining ordinary rows have the chronological public bath gate q_t. The following admitted premises are explicit:

    q_t<=q_*:=.9992,
    f_(1,t)<=1/n,
    0<=q_t-f_(z,t)<=2 q_*^(z-1),
    at least n/8 stationary ordinary bath rows remain,
    terminal and predecessor backward C-paths stay in the bath.       (2)

The public cohorts need not have bath gates and are excluded from the front bound. The no-wrap geometry ensures they and the private tracks remain far from the front and terminal. We do not infer (2) merely from the sparse simulator's geometry check. For a variant whose public state prescription has not established these bounds, the theorem is conditional on (2).

The inherited ACTUAL reference query is

    nu_ref(A)=(sigma sqrt(l)/n) sup_(legal Q)||A^T c_Q||,
    ||c_Q||<=1, |c_Q(i)|<=100/sqrt(n) on ordinary active rows.         (3)

The coordinate bound is NOT applied to the terminal. Futures have at least one step. The dense pair error used below is

    e_dense <= e_R sigma sqrt(l)
               [q_f N(N-1)/n+14N/n],
    e_R<=4/(10^8 n^2), q_f<.941.                                  (4)

Primary repository dependencies:

- [unpaired corridor](../codex_unpaired_corridor_sensitivity_20261003/PROOF.md), sections 1–5 and 9–10: exact model, full J/B recurrence, actual query, ordinary-row bound;
- [holding cost](../codex_holding_cost_attack_20261003/PROOF.md), section 4: balanced inverse lift and chronological geometry;
- [linear frontier](../codex_linear_dimension_frontier_20261006/PROOF.md), sections 5 and 10: inherited bath/front and dense comparison;
- [growing-R local theorem](../gpt6_route7a_growing_R_local_20261007/PROOF.md), sections 1–3, and [Gemini review](../gemini_growing_R_route7a_audit_20261007/PROOF.md): local row bound and exact trace neutrality;
- [earlier Astra report](../astra_route7a_reservoir_20261007/PROOF.md), sections 4–5: public right space and Walsh suffix count, rederived below;
- [erratum](../gpt6_route7a_chronological_public_20261007/ERRATUM.md), [corrected results](../gpt6_route7a_chronological_public_20261007/CORRECTED_RESULTS_20261008.md), and [sparse report](../gpt6_route7a_sparse_geometry_20261008/RESEARCH.md): implementation scope, not theorem evidence.

## 2. NEW: a uniform bound on the complete common-field row

### Exact identity

The open-shift identities are 1^T C=1^T-e_T^T, e_T^T C=e_P^T, u^T1=-gamma, and u^T e_1=-c. Hence exactly

    u^T O_*=(1-gamma)u^T
             +eta_H(e_P-e_T)^T+c e_T^T-c v_H^T.                  (5)

Write G_t=q_t I+E_t. Multiplication of (1) gives

    J_t=a q_t[(1-gamma)J_(t-1)
         +eta_H(e_P-e_T)^T M_(t-1)
         +c e_T^T M_(t-1)-c B_(t-1)]
         +a u^T E_t O_* M_(t-1)+u^T G_t.                        (6)

This is a complete chronological identity. No rho is discarded: the full front and terminal are represented through E_t, B_t and the terminal rows. In particular this is not a positive-cone approximation or a bound on separately absolute-valued cancelling replenishment terms.

### Bounds on the terms

The terminal and predecessor have the same feedback row Z, so their difference in (6) is purely local. Each of their local C-path rows has norm <=sum q_*^s=1250. Therefore

    ||(e_P-e_T)^T M_t||<=2500.                                 (7)

The non-bath diagonal deviations occupy at most 8m active rows plus the front. On both sets u_i=-c. Premise (2) gives

    ||u^T E_t||<=c[sqrt(8m)+2/sqrt(1-q_*^2)]
                <(3/n)[sqrt(8m)+51].                          (8)

Also ||B_t||<=2t, ||u^T G_t||<=3/sqrt(n), eta_H<=2/sqrt(n), c<=3/n, and gamma-1<=2/sqrt(n). These numerical inequalities hold for n>=10^6.

Taking the maximum of (6), absorbing the coefficient <=.002 of the previous J, and using ||M_t||<=N gives the safe envelope

    J_max:=max_(t<=N)||J_t||_2
      <= J_*:=10 N sqrt(m)/n+200 N/n+6000/sqrt(n).               (9)

No K or R is hidden in these constants. The terminal-path premise in (7) is essential: applying a small coordinate bound to an arbitrary terminal response would be wrong.

At the intended scaling, J_*=O(C_T), whereas the generic bound ||u|| N only gives O(C_T sqrt(R)). This improvement is load-bearing.

## 3. NEW: trace-neutral donor feedback filters collapse to one receiver

Let epsilon=10^-4, g_*=.9975, .99<=g_H<=1, and let tau be the public incoming LOCAL scalar trace. For d=g_*+epsilon x, x in [-1,1], write

    d_3(d)=g_* (A+B g_*)/(A+B d),
    A=1+a g_H, B=a^2 g_H(1+a tau),
    z=A/B, p(d)=d d_3(d).                                     (10)

The actual donor uses d,g_H,d_3(d). The local trace at block end is public, as already verified. Define

    L_*=(g_*/(g_*-epsilon))^2<1.000201,
    rho=(g_*+epsilon)g_*^2/(g_*-epsilon)<.995206.                (11)

Then |d_3(d)-g_*|<=L_* epsilon and |p(d)-g_*^2|<=L_* epsilon z.

### The reference receiver uses the SAME actual J

For EACH actual history H, define V_*(H) by

    V_*,0=0,
    V_*,t=a g_*,t[V_*,t-1+J_(t-1)(H)],                         (12)

where g_*,t is the PUBLIC donor schedule with x=0 in every triple and the actual public precharge, waits and reset. This is a comparison of receiver kernels, not replacement of the coupled field by a baseline field. The row V_*(H) itself is private and will be coded.

At a triple entrance, the reference local trace equals tau, and positivity of the scalar kernel gives

    ||V_*,0|| <= a tau J_max <= tau J_max.                      (13)

The exact three-step feedback update is

    V_3=a^3 g_H p(d) V_0
         +a^3 g_H p(d) J_0+a^2 g_H d_3(d) J_1+a d_3(d) J_2.   (14)

The J_0,J_1,J_2 here are the complete field values of the one actual history, with their actual gate chronology.

Subtract the reference receiver using those identical inputs. The old receiver error has multiplier <=rho. Its fresh term has norm at most

    L_* epsilon [z a^3 g_H(tau+1)+a^2 g_H+a] J_max
      <=4 L_* epsilon J_max.                                 (15)

For the first summand use

    z a^3 g_H(tau+1)
       =a(1+a g_H)(tau+1)/(1+a tau)<=2.

The other two coefficients sum to at most 2. In particular the large precharge tau cancels: it does NOT multiply (15).

Public waits after complete triples and the public reset contract the receiver error because both receivers use the same input. Starting from the identical public precharge,

    max_i ||V_i(N;H)-V_*(N;H)||
      <= [4 L_* epsilon/(1-rho)] J_max < .084 J_*.             (16)

This holds for every donor word, every R, arbitrary precharge duration, and arbitrary donor-common public waits AFTER triples. The bound is at completed block boundaries and the final reset; intermediate private phases need not satisfy it.

### Query consequence

If two histories have equal V_*(N), their donor feedback difference is supported on at most 4m rows, each of norm <.168 J_*. Therefore its all-legal-query contribution is

    nu_D < .018 J_* sqrt(m/n).                                (17)

This bound uses only ||c_Q||<=1. Using ordinary-row dilution instead gives the optional stronger bound 3.5 J_* m/n. Neither estimate treats J as externally prescribed across histories: only the coded V_* rows are required to agree.

At Route scaling (17) is O(C_T/sqrt(R)), so the private multiplicity of donor receiver filters is asymptotically invisible at fixed query margin. Shared feedback can still be large; it is retained in the code.

## 4. Bath and complete front: one exact row plus a small error

The exact feedback decomposition has a common ordinary-bath row Z_t, donor rows V_i,t, public cohort rows, and global front rows F_z,t. The chronological front equations are

    Z_t=a q_t(Z_(t-1)+J_(t-1)),
    F_(1,t)=a f_(1,t)(J_(t-1)+B_(t-1)),
    F_(z,t)=a f_(z,t)(F_(z-1,t-1)+J_(t-1)).                    (18)

Code Z_N exactly. This includes the terminal feedback row; no terminal coordinate-dilution estimate is invoked.

On at least n/8 stationary bath rows, the local matrix is a diagonal trace of norm <=1250 and the feedback is the same Z. Averaging those rows of M_t yields

    ||Z_t||<=3(t+1250)/sqrt(n).                               (19)

For the front comparison use the generic ||J_t||<=3t/sqrt(n), not (9). The exact difference recurrence is

    F_(z,t)-Z_t=a f_(z,t)(F_(z-1,t-1)-Z_(t-1))
                    +a(f_(z,t)-q_t)(Z_(t-1)+J_(t-1)).        (20)

Premise (2), (19), and ||B_t||<=2t give by induction

    ||F_(z,t)-Z_t||
       <=12 z q_*^(z-1)(N+1250)/sqrt(n).                      (21)

Sum S_2=sum_(z>=1) z^2 q_*^(2z-2)=(1+q_*^2)/(1-q_*^2)^3. For a pair, the front residual has Frobenius norm <=24 sqrt(S_2)(N+1250)/sqrt(n). Its query contribution is therefore

    nu_front <= 30000 (N+1250)/n.                             (22)

This constant is deliberately loose and n-independent. The entire front is charged once, never restarted at a donor stage. At N=O(sqrt(nR)) this error tends to zero. It is not a useful finite-width estimate for the million-width pilot.

## 5. Full parameter accounting, not just the chosen K probes

Define the local matrix L_t=G_t(a C L_(t-1)+I), H_t=M_t-L_t. Fix the public baseline obtained by setting all private donor controls to zero, and call its local matrix L_t^0.

Every private local path intersects a donor track or compensator. Under no-wrap, all affected parameter columns lie in two intervals of length at most m+N and at most 2m stationary coordinates. Call their union I_exc; |I_exc|<=4m+2N. Outside it, (L_t-L_t^0)e_c=0.

The PUBLIC subspace

    E_par=span{e_c:c in I_exc}
       +span{(u^T L_t^0)^T,(v_H^T L_t^0)^T:1<=t<=N}

has dimension P<=min(r,4m+4N). The exact formula

    H_t=sum_(s=1)^t Phi_C(t,s)aG_s[1 J_(s-1)+e_1 B_(s-1)]     (23)

proves inductively that all J_t,B_t rows lie in E_par. Thus Z_N and V_*(N) also lie there. All their P coordinates, not merely K selected probes, are counted. Coefficients in the induction may depend on the private history; the right subspace does not.

## 6. Public capture bank without a final clear

Two versions are covered.

**Rapid public-cohort version.** There are fixed co-moving public cohorts of size h_S<=4m. At the middle step of each donor triple their gates take strong balanced Walsh values with DISTINCT nonzero characters. Elsewhere their gates may be any public values in [0,1], including their exact autonomous evolution. The last ell captures plus the final reset occupy at most 3ell+1 steps.

**Uniform-gap version.** Survivors are uniformly high between the same distinct one-step captures. Donor-common public waiting periods can follow completed triples. Public survivor readout kernels are parallel within each gap, yielding at most 2ell+2 recent segment directions.

Both versions allow high donors at capture and omit the final clear. The rapid version is specifically designed not to silently treat the sparse simulator's public moving cohorts as continuously held-high survivor rows.

Let b_0>0 be fixed, and every low capture gate be <=1-2b_0; b_0=.0024 accommodates low gate .995. For the last ell distinct characters, a uniformly sampled cohort site is low X times, with E X=ell/2 and Var X=ell/4. Hence the LOCAL co-moving diagonal suffix D satisfies

    (1/h_S)sum_i D_ii^2 <= F_ell:=4/ell+exp(-b_0 ell).         (24)

The proof is Chebyshev on X<ell/4 and the bound D_ii<=(1-2b_0)^X. Intervening public gates at most one only strengthen it. Higher-order XOR aliases do not spoil pairwise independence. Independently generated Walsh labels improve this to an exponential bound, but are not required.

Cut before the last ell triples, or at the end of the public precharge if R<ell. The public-cohort difference satisfies the exact LOCAL Duhamel formula

    Delta M_S(N)=D Delta M_S(t_0)
                  +sum_(t>=t_0) beta_t Delta J_t.             (25)

Direct source forcing cancels because those gates are public. Complete renewed feedback remains in J. Since local rows on these public paths are public, Delta H_S=Delta M_S.

In the rapid version, encode each recent J_t in E_par: at most (3ell+1)P coordinates. In the uniform-gap version, encode its public segment aggregates: at most (2ell+2)P. Equal codes cancel the recent term of (25) over ALL parameter directions.

Using ||Delta M_S(t_0)||_op<=2N, h_S<=4m, and the ordinary-row query bound (3), the remaining old cohort contribution is bounded safely by

    nu_S <=32 (N sqrt(m)/n) sqrt(F_ell).                      (26)

No Frobenius conversion of an r-column matrix occurs. If the cut is at the common public precharge endpoint, this old difference is zero. Old donor information is permitted to survive and feed recent J, which is encoded exactly.

## 7. Complete no-clear code and robust dimension theorem

Take one fixed orthonormal basis of E_par. The continuous code contains:

1. Z_N in this basis;
2. V_*(N) in this basis;
3. recent J_t rows or their public segment aggregates in this basis.

For the rapid version,

    q_code <= [3 min(R,ell)+3] min(r,4m+4N).                  (27)

The uniform-gap version has q_code<=[2 min(R,ell)+4]P. This is a static approximate code for robust dimension, not a claimed online memory algorithm.

The reviewed local-direct bound contributes .00852 sqrt(m/n). Combining it with (17), (22), (26), and (4), EQUAL CODES imply

    nu_actual(Delta M_N)
      <= [.00852+.018 J_*] sqrt(m/n)
         +30000(N+1250)/n
         +32(N sqrt(m)/n) sqrt(F_ell)+e_dense.                (28)

Every component of M_N=L_N+H_N is included: moving local paths, exact matched stationary local traces, private donor feedback, public cohort feedback, ordinary bath, terminal, global front, and the dense comparison. The formula is uniform over donor controls and ALL legal future queries satisfying (3), not a found query score.

At R~log log n, m~K~n/R, N~C_T sqrt(nR), fixed C_T,

    J_*=O(C_T),
    [.00852+.018J_*]sqrt(m/n)=O((1+C_T)/sqrt(R)),
    30000(N+1250)/n=O(C_T sqrt(R/n)),
    e_dense=O(C_T^2 R/n^(3/2)).                              (29)

Let A_0>=max(1,N sqrt(m)/n) be a fixed public bound, tau=5*10^-4, and epsilon_0=tau/(32A_0). Choose a FIXED integer

    ell >= max{1,8/epsilon_0^2,b_0^-1 log(2/epsilon_0^2)}.     (30)

Then the survivor term is <=tau. All other terms in (28) tend to zero, so equal-code distance is eventually <.001, strictly below .002. Constants and onset can be enormous; no finite pilot is certified by this asymptotic inequality.

A continuous robust section S^(D-1) with D>q_code has equal-code antipodes by Borsuk–Ulam, contradicting its >.002 margin. Therefore

    D<=q_code=O_(C_T,b_0,tolerance)(m+N)=O(n/R)=o(n).          (31)

This is the new NO-FINAL-CLEAR scoped obstruction. It neither proves small total H diameter nor requires the earlier missing 7.213 checkpoint, q_stat code, Carl–Pajor theorem, or the low-donor-at-capture Lambda bound. It is conditional on the explicitly inherited legal-query and admitted public geometry bounds (2)–(4), as any transfer to that metric must be.

## 8. Adversarial checks and nonclaims

- **The common field is not frozen.** V_*(H) is driven by the actual J(H); it changes with history and is explicitly coded. Replacing it by J of the x=0 history would invalidate the proof.
- **Only boundary receiver errors are small.** Intermediate phase-1 errors can scale with precharge. This is allowed and included in the complete field bound (6).
- **No independent scalar-battery model.** The exact O_* identity (5) controls every coupled renewal. Front B is bounded in (6), not dropped.
- **Near-critical donors do not defeat (16).** The triple product has fixed rho<1 although its middle gate is near one. If g_* approaches one with R, the factor 1/(1-rho) can diverge: not covered.
- **Controls may be coherent, unequal, or adversarial.** Bounds use |x|<=1 and full row norms. They do not presume cancellation between donors or random controls.
- **Numerical evidence is not an upper bound.** The corrected small signals and query optimizations are not used in any inequality here.
- **Recent public cohorts are not assumed held high.** The rapid version encodes every recent time step. A public wait with varying cohort gates changes the code count unless the uniform-gap structure is proved.
- **Distinct masks matter in (24).** Repeated labels or contrasts tending to zero require another public-bank approximation. A single repeated public mask has a small exact spatial span, but that does not prove a theorem for arbitrary repeated schedules.
- **No arbitrary-adjoint claim.** Equation (26) uses ordinary-row legal-query dilution. Concentrated unit adjoints could invalidate it. Terminal is handled by Z, not by that dilution bound.
- **Private survivor control is excluded.** It would make (25)'s direct source forcing and kernels private.
- **One fixed feature.** This does not upper-bound all recurrent/input/bias feature blocks simultaneously.
- **No improvement to the constructive frontier.** Existing strict-budget lower bounds are unchanged. The new result excludes the specified candidate rather than constructing a better one.

## 9. One motivated alternative: delay compensation across a long release window

The three-step obstruction suggests changing the position of compensation, rather than adding public waits after a completed neutral triple.

Use d=g_*+epsilon x at the first step, then W PUBLIC high donor steps, then compensate. Let alpha=a g_H and T_W=g_H sum_(u=0)^(W-1)alpha^u. Define

    A_W=1+a T_W,
    B_W=a alpha^W(1+a tau),
    d_last(d)=g_* (A_W+B_W g_*)/(A_W+B_W d).                  (32)

The resulting local trace is exactly public. The ratio argument gives |d_last-g_*|<.000101, independent of W and tau, so gate legality is retained. All four tuple sites use the same gates. The original source, operator, bath/front chronology, and common state reset remain intact.

For W=o(n), the receiver comparison analogous to (15) has a fresh bound of order

    epsilon (W+1) J_max,                                    (33)

because z_W=A_W/B_W is of order (W+1)/(1+tau), and there are W high-step feedback inputs. Thus the present uniform receiver-collapse proof does NOT exclude W~n/m. This is a failure of the upper estimate, not evidence of amplification.

The same alteration also removes the reviewed three-step local proof's small fresh-column constant: the W distinct moving-source injections can contribute an O(epsilon sqrt(W)) local row difference. Neither this observation nor (33) is a robust lower bound; chronological cancellation may reduce both drastically.

At W~n/m~R, R such blocks add O(R^2) steps and O(nR) coordinate-time to a precharge L~sqrt(nR). Thus

    mN=Theta(n^(3/2)/sqrt(R))+O(nR)=o(n^(3/2)).               (34)

The cost is potentially acceptable. The unproved issue is whether the LONG trace-neutral block has a genuinely robust response, rather than a large upper bound on cancelling terms. Constant J cannot simply be counted W times. For every actual a, if the incoming V=a tau J and J stays constant, then V_out=a tau_target J, independent of the control: the identity V=a tau J is preserved by V'=ag(V+J), tau'=g(1+a tau).

There is an exact centered-input identity. Write L=W+2, alpha_t=a g_t, A(d)=product_(t=1)^L alpha_t, and K_k(d)=product_(t=k+1)^L alpha_t for k=0,...,L-1. Compare a controlled block with its zero-control block on identical input rows and identical initial receiver V_in; let delta denote their coefficient difference. Trace neutrality implies

    a tau delta A + sum_(k=0)^(L-1) delta K_k = 0.

Consequently their output difference is exactly

    delta V_out = delta A (V_in-a tau J_0)
                  +sum_(k=0)^(L-1) delta K_k (J_k-J_0).      (35)

For unequal initial receivers add the transported initial difference separately. Equation (35) does not assume the legal coupled J is constant or freely selectable. It identifies the actual input variation and unmatched initial receiver component that a sharper bound must control. A successful construction must exploit these components, not a constant-field approximation.

## 10. Single next falsifiable obligation

For the long-window trace-neutral block (32) with W=Theta(n/m), derive the SHARP control-dependent complete receiver response under the actual coupled J/B recurrence, after removing the constant-field component. Decide whether its legal-query-visible gain is O(epsilon J_max), O(epsilon log W J_max), or genuinely grows with W. The required estimate must hold uniformly over histories, or be refuted by a legal explicit family; a hypothetical arbitrary forcing waveform is not a counterexample.

This is the exact next obligation. If the gain stays bounded, the receiver code can likely extend. If it grows, the next step is a jointly robust continuous section, not a rank or single-query claim. No claim that the long-window variant succeeds is made.

## 11. Status

| Statement | Author status |
|---|---|
| Complete common-field identity and bound (5)–(9) | PROVED under explicit geometry/bath/front premises; pending review |
| Trace-neutral receiver collapse (16) | PROVED for consecutive triples, actual common input |
| Donor/bath/front approximate code | PROVED under stated query normalization |
| Full no-clear rapid-public-capture code (28) | PROVED under (2)–(4) and distinct strong public masks; pending review |
| Linear dimension in this scoped Route 7A family at fixed C_T | REFUTED by author code theorem, pending hostile review |
| General strict-budget linear dimension target | OPEN / overall investigation PARTIAL |
| Long-window trace-neutral alternative | OPEN; legal gates and cost established, robust signal not established |

Independent hostile review is required before promoting any new theorem. CURRENT_THEORY.md is intentionally unchanged.
