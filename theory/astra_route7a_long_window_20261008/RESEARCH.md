# Route 7A long-window feedback: experiments and a recent-block code

2026-10-08. Author: Codex, requested Astra research. **PENDING REVIEW. Overall PARTIAL.**
Starting source: `1fa6b00018f7dceb72b689c4ebdbe3928ba717f9`.

## 1. What changed

The long-window schedule is implemented and actually evaluated with complete chronological reference feedback. Longer windows improve some found query scores, but no constant-margin memory construction results. Full numerical tables and limitations are in [EXPERIMENTS.md](EXPERIMENTS.md).

At n=1,048,576, m=8, R=4, precharge=2048, the best found complete reference query scores for W=1,16,64 are respectively 3.14891e-11, 9.56839e-11, and 1.95574e-10. At the W=64 selected query, L has norm 1.95510e-10 and H has norm 7.42513e-12: the complete improvement is not evidence that feedback dominates. Across the main battery the maximum live trace error is 1.23e-11, endpoint disagreement is zero to printed precision, and maximum measured input is .120699. Eight-control local spectra are nonzero; the strongest H singular value grows about 6.3-fold from W=1 to 64, while the weakest does not improve. None of these found values bounds the supremum over queries or proves robust continuous dimension.

The main mathematical advance is a different compression argument: **old donor state contracts once per completed block, and each long block receives only two common vector-valued feedback aggregates.** Coding recent controls and these aggregates gives an approximate donor-response code of size O((m+N) log R), uniformly in window length. This does not require a W-independent bound on individual receiver error.

For a public survivor bank held uniformly high between distinct one-step captures, the code extends to the full fixed-feature query and conditionally implies D=O(n log R/R)=o(n). The autonomous public capture cohorts of the corrected sparse prototype are a DIFFERENT schedule. Their donor channel is covered; the full autonomous-cohort channel is not compressed by this new argument. The broader target remains OPEN. No constructive dimension frontier is improved.

## 2. Sources and exact scope

- [Previous author proof](../astra_route7a_feedback_compression_20261008/PROOF.md), equations (1)–(9), (18)–(26), (32)–(35): model, all-query normalization, complete field, bath/front, public parameter space, long-window formula.
- [Gemini audit](../gemini_astra_route7a_feedback_audit_20261008/PROOF.md), sections 4–5: conditional premises and long-window identity.
- [Corrected chronological implementation](../gpt6_route7a_chronological_public_20261007/chronological_probe.py), [erratum](../gpt6_route7a_chronological_public_20261007/ERRATUM.md), [corrected results](../gpt6_route7a_chronological_public_20261007/CORRECTED_RESULTS_20261008.md).
- [Sparse evaluator](../gpt6_route7a_sparse_geometry_20261008/sparse_geometry.py) and its [scope report](../gpt6_route7a_sparse_geometry_20261008/RESEARCH.md).
- [Unpaired corridor](../codex_unpaired_corridor_sensitivity_20261003/PROOF.md), sections 1–5, 9–10: complete M/J/B recurrence, ordinary-row legal future queries, terminal exception.

Use one fixed source and the reference recurrence

    M_t=G_t(a O_* M_(t-1)+I), M_0=0,
    O_*=C+1 u^T+e_1 v_H^T,
    J_t=u^T M_t, B_t=v_H^T M_t,
    a=1-1/n, g_*=.9975, epsilon=10^-4, g_H=1-n^-2.

J and B are full ROW VECTORS, not scalar summaries. The unit operator bound ||M_t||<=t follows from contraction. Sensitivities freeze realized inputs, not the inverse-lift policy.

There are m four-site donor tuples, R public stages, no-wrap moving tracks, two public survivor cohorts of total size 2m, and one final common donor reset. The private x_(r,i) lie in [-1,1]. All four sites of a donor share gates, with two positive and two negative target states. N=L_pre+R(W+2)+1. Captures occur at the FINAL high step of each window, before compensation. This is fixed publicly and equals the old middle step when W=1.

Two public-cohort options are kept separate:

1. **Autonomous:** the inherited sparse schedule; cohorts evolve autonomously except at captures.
2. **Held-high:** public inverse-lift control maintains the cohorts at g_H between captures. This adds O(m) driven coordinates per step, not a changed recurrent operator. It is an explicit alternative, not silently substituted into the main experiment.

## 3. Exact long-window gate and legality

Let alpha=a g_H and G_h=sum_(j=0)^(h-1) alpha^j. At public incoming local trace tau, set

    d=g_*+epsilon x,
    T_W=g_H G_W,
    A_W=1+a T_W=G_(W+1),
    B_W=a alpha^W(1+a tau),
    d_last=g_* (A_W+B_W g_*)/(A_W+B_W d).

Use d, then W copies of g_H, then d_last. Direct scalar recurrence tau'=g(1+a tau) gives

    tau_out=d_last(A_W+B_W d)=g_*(A_W+B_W g_*).

Thus incoming and outgoing boundary traces are PUBLIC at every stage, including the precharge. Moreover |d_last-g_*|<=g_* epsilon/(g_*-epsilon)<.000101, so donor gates stay within the same inherited admissible interval. The actual live trace is independently evolved in code; it is not merely recomputed from the target formula.

Private donor state sums vanish at every step. The open shift takes each moving donor to its next controlled location. Consequently the sum and terminal coordinate determining the public forward field are independent of private controls; all off-donor states are public. The final donor reset makes the whole reference endpoint equal. This forward-state field must not be confused with the private SENSITIVITY field J_t.

## 4. Public bath/front assumptions: an explicit sufficient certificate

Write the forward state h_t=u_t 1+delta_t and D_t=sum delta_t. Under the separated geometry the exceptional support has at most N+6m coordinates: front at most N, moving donors 2m, stationary donors 2m, public cohorts 2m. Since states lie in [-1,1], |D_t|<=D_max:=2(N+6m). The terminal is ordinary bath. With k=n/2, r=k-1, gamma=(1-1/sqrt(k))^-1, c=gamma^2/k, eta=gamma/sqrt(k), the exact public bath update is

    u_t=tanh(.05+a[(1-gamma)u_(t-1)-c D_(t-1)]).

Define e=(gamma-1)+c D_max. If e<=.02 then

    tanh(.05-e)<=u_t<=tanh(.05+e),
    q_t=1-u_t^2<=sech^2(.03)<.9992.

The initial bath tanh(.05) is included. This argument uses only |u|<=1 and support, not a conjectured stationary bath.

At the first front, the raw argument is

    .05+a[(eta r-gamma)u+(eta-c)D].

Hence, writing u_min=tanh(.05-e), a sufficient bound is

    f_1<=4 exp(-2[.05+a((eta r-gamma)u_min-(eta-c)D_max)])<=1/n.

For admitted n>=10^6 this also makes the first front state larger than the bath. At later front positions order preservation and the bath lower bound imply

    0<=q_t-f_(z,t)<=2(.9992)^(z-1).

Proof: the front-state excess propagates through the same increasing tanh map as the bath, whose derivative on the intervening positive-state interval is at most .9992; its initial excess is at most one. Gate difference is at most twice state difference. This follows the global chronological front, never a restarted stage front.

These are sufficient finite certificates, evaluated independently in `extra_checks.py`. All three million-width schedules satisfy them. Under m~n/R, N~C_T sqrt(nR)+O(R^2), R->infinity, e=O(1/sqrt(n)+N/n+m/n)->0, and the first-front exponent grows as a positive constant times sqrt(n). The certificate therefore holds asymptotically as well.

Other inherited assumptions remain: ordinary-row future-query dilution, the fixed-source root and dense inverse lift, and the dense comparison estimate. The numeric evaluator implements the reference model with sigma=.05; it does not independently certify every dense-model input. Past inverse-lift input amplitudes are measured, including public captures. No-wrap and enough untouched stationary bath rows are checked separately.

## 5. Exact variable-field receiver identity and its limitation

Let a block have length L_b=W+2. Define

    A(d)=a^2 alpha^W d d_last,
    K_0(d)=A(d),
    K_k(d)=a d_last alpha^(W+1-k), 1<=k<=W+1.

For one fixed forcing sequence, V_out=A V_in+sum K_k J_k. For two gate choices at the same tau, write delta for coefficient differences. Trace neutrality implies

    a tau delta A+sum delta K_k=0.

Therefore, EXACTLY,

    delta V_out=delta A(V_in-a tau J_0)
      +a delta d_last sum_(u=0)^W G_(W-u+1)(J_(u+1)-J_u).     (1)

This is the centered-input identity with Abel summation performed explicitly. It identifies one signed geometric average of field increments; a large amplitude J_* alone need not be repeatedly charged as new signal.

**Audit clarification:** constant J gives zero only when V_in=a tau J. For unmatched initial receiver it gives delta A(V_in-a tau J), generally nonzero. The earlier author formula includes this term; the independent audit's unrestricted wording that constant input always gives zero is too strong. The archived numerical algebra check supplies a nonzero unmatched-initial example. That algebra example is not claimed to be a legal RNN counterexample.

For a zero-control comparator using the SAME actual J, ||V_*,in||<=a tau J_max. Since delta A and delta d_last have opposite signs, the exact coefficient-mass identity gives the fresh bound

    ||fresh|| <= 2 a [g_*/(g_*-epsilon)] epsilon G_(W+1) J_max. (2)

To verify: delta A(1+a tau)=a g_* A_W(d-g_*) B_W/(A_W+B_W d); its absolute value is at most a(g_*/(g_*-epsilon))epsilon A_W. The sum of the absolute coefficients for k>=1 equals this same quantity by trace neutrality. Add them. Thus the prior O(epsilon(W+1)) upper bound can be sharpened and saturated at the geometric lifetime, but is NOT replaced here by a W-independent bound.

For two ACTUAL histories one must additionally retain

    A_+ Delta V_in + sum K_(+,k) Delta J_k,

as well as the same-forcing expression (1) applied to the minus-history inputs. The experiments compute these actual fields; no external waveform is substituted.

## 6. NEW: recent-block donor compression, uniform in W

This avoids needing a small receiver difference altogether.

### Exact two-row aggregate

For block r define the actual history-dependent common rows

    U_r=J_(block start),
    Q_r=sum_(k=1)^(W+1) alpha^(W+1-k) J_(block start+k).

Every donor has

    V_(i,out)=A_i V_(i,in)+A_i U_r+a d_(last,i) Q_r.          (3)

For the COMPLETE M row there is additionally the local source row generated inside this block. It is a deterministic function of public geometry and the one private x_(r,i). It need not be small. Equal recent controls make these local source rows identical.

Both moving copies follow their public characteristics; both stationary copies use the same scalar receiver. Gate coefficients satisfy

    0<=A_i<=rho:=g_*^2 (g_*+epsilon)/(g_*-epsilon)<.995206,    (4)

uniformly in tau,W,n. The long high interval cannot undo the fixed attenuation at the two boundary gates.

### Public parameter space

As in the earlier exact Duhamel argument, all feedback rows belong to the public space

    E_par=span{e_c:c in I_exc}
          +span{(u^T L_t^0)^T,(v_H^T L_t^0)^T:t<=N},
    P=dim E_par<=min(r,4m+4N).

Here |I_exc|<=4m+2N by no-wrap track support. Changing W changes N, not the proof. In particular U_r,Q_r and the reset J row are P-dimensional vectors in this space. They are NOT two scalar coordinates.

### Code and residual

Code the last h blocks' controls (hm coordinates), their U_r,Q_r (2hP), and the final reset J ((P)). If R<h, code all stages and cut at the common public precharge. Equal codes imply identical local forcing and feedback injection over those blocks. The remaining donor matrix difference is only transported older state:

    ||Delta M_(donors,N)||_op <=2N rho^h.                    (5)

The restriction to 4m donor rows and the public shift of their predecessors are partial isometries; equality of controls makes the diagonal multipliers identical. This proves (5) directly for full M, with no separate local-direct bound and no assumption of equal earlier J.

For the actual reference legal query ||c_Q||<=1,

    nu_donor <= .073 (N/sqrt(n)) rho^h.                     (6)

The code is continuous. At N~C_T sqrt(nR), a fixed query tolerance delta is achieved by

    h=O(1+log(1+C_T sqrt(R)/delta)),
    q_donor <=hm+(2h+1)P=O((m+N)log R).                    (7)

This is a NEW uniform donor-channel result even for the autonomous public-cohort schedule. Large same-forcing kernel gains do not refute it: the large common input aggregates are encoded exactly.

## 7. Full-query corollary for the explicit held-high public bank

Code the bath row Z_N (P coordinates). The complete front error is bounded by the earlier proved chronological estimate 30000(N+1250)/n under section 4's premises. Terminal is included in Z, not subject to ordinary-row dilution.

For the held-high survivor schedule, local readout vectors are parallel between captures, irrespective of W. Across the last ell distinct balanced Walsh captures, the old survivor multiplier has mean square at most

    F_ell=4/ell+exp(-b_0 ell), b_0=.0024.

Encoding at most 2ell+2 recent public-segment feedback aggregates, each in E_par, eliminates new survivor feedback. The old query residual is <=32 N sqrt(m)/n sqrt(F_ell). This is the previous pairwise-independent Walsh/Chebyshev estimate; no false independence of higher-order Walsh products is needed.

The complete continuous code thus has the safe bound

    q <=h m+(2h+2ell+4)P,

with min(R,h), min(R,ell) understood when all stages are coded. Equal codes imply

    nu_actual <= .073 (N/sqrt(n))rho^h
       +32(N sqrt(m)/n)sqrt(F_ell)
       +30000(N+1250)/n+e_dense.                            (8)

All private donor local paths are already covered by (5); do NOT insert the three-step local theorem into this long-window proof. Public cohort/bath local rows cancel. The inherited dense pair bound is

    e_dense <= [4/(10^8 n^2)] sigma sqrt(n/2)
                    [.941 N(N-1)/n+14N/n].

For fixed C_T, choose ell a sufficiently large FIXED number, then h=O(log R), to make the first two terms less than .0005 each. The other terms vanish. Equal-code antipodes then contradict a >.002 robust section if D>q. At the intended scaling,

    D<=q=O((m+N)log R)=O(n log R/R)=o(n).                   (9)

This is an AUTHOR theorem pending review, conditional on the stated actual query/dense premises. It rules out this held-high public-bank, fixed-boundary-gate family, including W=Theta(n/m). It is not a universal Route 7A impossibility theorem.

## 8. Why the autonomous-cohort full theorem remains open

The sparse prototype's cohorts are not held high between captures. Older mask classes can have different autonomous scalar states, hence different gate profiles even within the latest window. Equation (3) compresses donors but does NOT make these public-cohort readouts piecewise parallel.

The straightforward code for their latest ell windows stores O(ell W P) field coordinates. With W~R and P~m~n/R this is O(n), insufficient for the desired obstruction. This is a failure of that code, not a robust lower bound. The measured feedback remains tiny, but numerical smallness cannot replace uniform compression.

Likewise (2) alone permits receiver error growth with W; no legal example saturating it is established. Arbitrary prescribed step-like fields can make its coefficient mass grow, but those are not legal coupled counterexamples.

## 9. Cost and failure modes

With W=Theta(n/m)=Theta(R), R blocks cost O(R^2) time. Including public precharge L_pre~C_T sqrt(nR),

    N=C_T sqrt(nR)+O(R^2),
    mN=Theta(n^(3/2)/sqrt(R))+O(nR)=o(n^(3/2)).

This counts precharge, imprint, high windows, compensation, capture and reset. The held-high bank changes only an absolute active-coordinate factor. One fixed source is used throughout. Inherited source preparation and dense lift remain part of the actual-model premises, not omitted claims.

The new donor theorem can fail if g_* tends to one so 1-rho shrinks, private controls occupy the interior of the window, private survivor gates are introduced, or the public parameter support expands beyond O(m+N). These are different constructions. No robust section or improved lower frontier is supplied here.

## 10. Single next falsifiable obligation

For the AUTONOMOUS paired public capture cohorts of the exact sparse schedule, prove an o(n)-coordinate continuous approximate code for their final full-parameter response when W=Theta(R), or construct a legal constant-margin family that defeats such compression. Use the already-controlled donor/bath/front code; do not infer this remaining cohort compression from scalar stability or numerical singular values.

## 11. Status

| Claim | Status |
|---|---|
| Long-window trace neutrality and centered Abel identity | PROVED algebraically by author; numerically cross-checked |
| Dimension-independent O(epsilon G_(W+1)) same-forcing gain bound | PROVED upper bound; not a legal lower construction |
| Public bath/front sufficient support certificate | PROVED by author; evaluated at all million-width configurations |
| Recent-block complete donor code, uniform in W | PROVED by author; PENDING REVIEW |
| Full held-high public-bank D=o(n) | CONDITIONAL author obstruction; PENDING REVIEW |
| Full autonomous-cohort robust width | OPEN |
| Overall strict-budget linear dimension target | OPEN / this session PARTIAL |

CURRENT_THEORY.md is unchanged. No theorem is promoted solely from these author derivations or experiments.
