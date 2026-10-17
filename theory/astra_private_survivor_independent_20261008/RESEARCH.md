# Independent private-survivor research: echoes and monotone local-memory codes

2026-10-08. Codex, requested Astra independent lane. **PENDING REVIEW. Overall PARTIAL.**

Baseline `1bd496ff4e64bed59248df8ff25859c469858f79`. The independent theorem, implementation and first experiments were committed as `185320f` BEFORE reading GPT-6 commit `f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c`. [INDEPENDENT_CHECKPOINT.md](INDEPENDENT_CHECKPOINT.md) is preserved unchanged. This document adds post-comparison analysis explicitly labeled below.

## 1. Resume

Original strategy: privately control survivors with reciprocal boundary gates, producing a multiplicative echo. Keep both moving survivor tracks explicitly pair-balanced at EVERY time; do not let a privately changed state become autonomous and silently assume its future bath remains public.

Strongest independent theorem: complete credit for fixed-gap private echoes, including independent trace-neutral private donors, admits an O((m+N)log R) continuous approximate code. Under the explicit legal-query/dense premises, this obstructs D=Omega(n) at the intended scaling.

Strongest additional result after comparison: for arbitrary private survivor gate words confined to the post-precharge horizon S=O(R^2), the COMPLETE LOCAL contribution L can be approximately coded with O(m) coordinates at fixed legal-query tolerance. Large changes in cumulative gate product account for only m coordinates. Full H is not controlled by that result.

The weak echo and GPT-6's private interior family still lack a full feedback theorem or robust lower construction. No certified advantage in robust memory dimension is established. This is a within-model control protocol / mathematical obstruction, not a new-primitive claim.

## 2. Exact model and original echo protocol

Use the inherited fixed-source reference recurrence

    M_t=G_t(a O_* M_(t-1)+I),
    O_*=C+1u^T+e_1v_H^T, J_t=u^T M_t, B_t=v_H^T M_t,
    L_t=G_t(a C L_(t-1)+I), H_t=M_t-L_t.

J,B are full row vectors. Full chronological feedback is propagated in all numerical products, with realized inputs frozen during differentiation. Source scale is .05 numerically; the inherited exact root is in (.0499,.051). The dense perturbation is not silently identified with the reference operator.

There are 4m donor sites (two moving copies and two stationary compensators) and 2m moving survivor sites. Survivor copies have opposite states and the SAME gate at each site index. For each stage/site control y_ri in [-1,1], use d_first=g_0 exp(eta y_ri), W high steps g_H, d_last=g_0 exp(-eta y_ri), with g_H=1-n^-2. The local homogeneous product is exactly

    A_echo=a^2(ag_H)^W g_0^2.

Fixed echo: g_0=.9975, eta=.0001. Weak echo: g_0=g_H exp(-.0025/R), eta=.002/R. Gates lie in [.995,g_H]. The final survivor reset is PUBLIC with gate 1-tanh(.05)^2. Every reference history has the same endpoint. Donors use the previous exact long-window trace-neutral compensation formula, with either zero/public controls or an independent control bank.

This echo is PRODUCT-neutral, not TRACE-neutral on survivors. The distinction is intentional: it cancels old local precharge but permits new-source timing information. Only donor trace neutrality is asserted/measured.

Full proof of the independent local-source bound and fixed-gap compression is in the preserved checkpoint. Key formulas are restated for navigation:

    ||Delta ell_survivor||_2
      <=2g_0 sinh(eta) sqrt[(W+1) sum_(r<R) A_echo^(2r)],

    q_echo <=2hm+(2h+2)P, P<=min(r,6m+6N),

    equal-code nu_actual <=.073(N/sqrt n)(.995206)^h
                             +30000(N+1250)/n+e_dense.

All recent PRIVATE controls and the ACTUAL feedback aggregates are coded. For each block these aggregates are U=J_start and Q=sum_(k=1)^(W+1)(ag_H)^(W+1-k)J_(start+k). Full M source injections cancel when codes agree; the argument does not replace H by L or treat common feedback as a public external signal.

At m~n/R,N~C_T sqrt(nR)+O(R^2), h=O(log R) gives D=O(n log R/R)=o(n), conditional on the stated inherited query/front/dense premises. The weak echo does not have a fixed contraction per stage: A_echo approaches 1 at rate 1/R, so this proof does not settle it.

## 3. POST-COMPARISON theorem: arbitrary survivor local words are compressible

This theorem was developed AFTER observing the competitor's interior protocol and must not be presented as part of the earlier independent checkpoint.

### Hypotheses

Survivors are m paired moving characteristics in the no-wrap geometry. Their gates after a common public precharge may be ARBITRARY private numbers in [0,1]. There are S subsequent steps, including reset. Both physical copies of each characteristic share gates; the same argument with a constant-factor larger code covers independently gated copies. Donor gates are public for the statement about the whole Delta L; otherwise this theorem applies to the survivor portion and other local banks must be accounted separately.

The actual legal reference query obeys the inherited ordinary-row bound |c_Q(i)|<=100/sqrt(n). No such claim is made for arbitrary unit adjoints or the terminal.

### Exact row form

Following characteristic i to its endpoint,

    ell_i = Pi_i ell_i,pre + sum_(t=1)^S f_i(t) e_(c_i(t))^T,
    Pi_i=a^S product_(s=1)^S g_i(s),
    f_i(t)=a^(S-t) product_(s=t)^S g_i(s).

The precharge row and its public shift are fixed. Source indices c_i(t) are distinct along a no-wrap moving characteristic. Different characteristics MAY share source indices; no orthogonality between rows is assumed.

Crucially,

    0<=f_i(t)<=f_i(t+1)<=1,

since f_i(t)=a g_i(t) f_i(t+1). Thus an arbitrary private temporal word yields a bounded monotone suffix profile in the LOCAL channel.

### Explicit continuous code

Partition {1,...,S} into B consecutive bins of length at most ceil(S/B), with at most B+1 boundary sample indices. Code Pi_i and every boundary value f_i(t). If B>=S, encode all coefficients instead and the residual is zero. This is at most (B+2)m continuous coordinates; no discontinuous sorting or threshold selection is used.

For equal codes, old precharge cancels. Within bin b, the two monotone profiles lie between their common endpoint values; let Delta_b be that common range. Then

    ||Delta ell_i||_2^2 <=ceil(S/B) sum_b Delta_b^2
                       <=ceil(S/B),

because Delta_b>=0 and sum Delta_b<=1. Single-index bins are exact. This accounts for full moving-cycle parameter coordinates, not a probe projection.

Using the actual ordinary-row query upper and both physical survivor copies,

    nu_ref(Delta L_survivor)
       <=100 sqrt(2) sigma (m/n) sqrt(ceil(S/B)).             (5)

At m~n/R, S=O(R^2), the right side is O(B^-1/2)+O(R^-1). For ANY fixed tolerance delta>0, choose a sufficiently large FIXED B depending on the scaling constants and delta; then q_local=(B+2)m=O(m)=o(n) achieves that tolerance for sufficiently large n.

This is a conditional **robust approximate LOCAL code**, not exact history recovery and not a full M/H theorem. Its constants can be enormous: practical experiments with S<B may simply code every local coefficient. There is no numerical capacity claim from the asymptotic big-O.

### Why this matters

A large interior-modulation M score may contain a large old local-precharge component controlled by only Pi_1,...,Pi_m. More controls and a larger scalar pair score do not establish more robust dimensions. Even the newly injected local timing profiles have the uniform approximate code (5). The genuinely unresolved opportunity is complete FEEDBACK, after this local nuisance has been paid.

## 4. Product-matched interior stress test

After comparison, construct private interior words z=(u,0,-reverse(u)) per stage/site for even W. Opposite words reverse temporal order, so

    product_j [g_H-epsilon(1+z_j)/2]
      =product_j [g_H-epsilon(1-z_j)/2]

exactly. Public capture gates are unchanged. This cancels old LOCAL precharge in each antipodal pair without changing the frozen recurrence or ignoring feedback. There are mR(W-2)/2 independent controls. This is a legal reference protocol with common reset, not a prescribed external J experiment.

Found optimized signals shrink relative to unrestricted random interiors in the tested cases, but the two schedules also differ in their control subspaces. The experiment supports no universal upper bound. It is a targeted falsifier of interpreting cumulative-product changes as many independent memory directions.

## 5. Public chronology, geometry and full cost

All private pairs are forced at EVERY step. Their state sums vanish, so private controls cannot change the common forward sum, terminal, bath or front in the reference model. This is false for a privately altered pair subsequently left autonomous; we do not use that variant.

The support bound N+6m and explicit public bath/front certificate from the baseline long-window report apply. At sufficiently large n with m/n,N/n->0, the bath argument stays within .05+o(1), and the chronological first-front gate is exponentially small in sqrt(n). Finite small-width cases are labeled structural tests; million-width cases satisfy the stronger S_geometry<=d/100 condition.

N=L_pre+R(W+2)+1 includes imprint, every interior holding step, compensation and reset. At W~R and L_pre~C_T sqrt(nR), mN=O(n^(3/2)/sqrt R+nR)=o(n^(3/2)). There are at most 6m driven selected-memory coordinates per step, not merely m at capture. Their actual squared inverse-lift inputs are summed without subtracting a public center. Initial selected-memory preparation adds

    6m[.05^2+atanh(sqrt(1-g_H))^2].

The inherited source preparation must also be counted. Even a conservative O(n) bounded-coordinate source preparation is lower order at this scaling; this is an upper-order accounting observation, not an independent dense lift. All source parameters, exact source-root corrections and dense-model input constraints remain explicit inherited obligations. Numerical tests use the reduced reference family and sigma=.05.

## 6. Scope of numerical conclusions

Complete M, L and H are evaluated by exact matrix-free reference forward/transpose products. Multiple starts and horizons search only a subset of legal future gate words. A found value is a LOWER bound on the query supremum. H scores refer to a decomposition component, not an independently accessible gradient oracle.

Random cube pairs test many coordinates simultaneously; central differences test eight controls individually. Singular values at one fixed query do not describe the supremum over queries and do not prove robust memory. Re-optimizing the query for the weak singular direction can change its apparent weakness; that does not prove a sphere-wide margin either.

No experiment reaches or certifies uniform .002 antipodal separation. No continuous robust D=Omega(n) section has been proved. The public code theorems are mathematical arguments, not inferences from these finite values.

## 7. Single next precise obligation

For the weak-echo private-survivor family (eta=Theta(1/R), A_echo=1-Theta(1/R)), after matching the continuous local code of section 3, prove an o(n)-coordinate approximate code for the COMPLETE H response at legal-query tolerance .001, or construct a legal uniformly robust antipodal family contradicting such compression. Preserve actual J/B chronology and the dense/query premises. Do not spend the next investigation maximizing unconditioned local-product scores.

## 8. Verdict

| Claim | Status |
|---|---|
| Product-neutral echo identity and local bound | Author PROVED; pending review |
| Fixed-gap private-boundary full code | Author PROVED under explicit inherited premises; pending review |
| Arbitrary private-survivor local monotone code | Author PROVED under no-wrap/query premises; pending review |
| Weak echo full feedback compression or robust lower | OPEN |
| Competition winner on robust dimension | INCONCLUSIVE; neither has a certified linear section |
| Main project target | OPEN / session PARTIAL |

CURRENT_THEORY.md, main, and GPT-6's historical folder are not changed by this branch.
