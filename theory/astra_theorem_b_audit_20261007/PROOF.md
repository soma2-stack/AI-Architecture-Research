# Theorem B: independent focused audit

Date: 2026-10-07. Requested Astra audit, performed in Codex. Starting source commit: `30b4429a4f8b74790cbf1702b4e55e55845238a0`.

## Verdict and scope

**Abstract Theorem B: VERIFIED after a repairable kernel-selection correction.**
**Unconditional legal-query / separated Route-6 conclusion: PARTIAL.** The implication from the stated upstream hypotheses is verified; this audit does not supply missing upstream proofs or the unarchived packet repair. No authoritative theorem status is changed.

Sources audited: [author proof](../opus_segment_atom_width_20261007/PROOF.md) and [handoff](../opus_segment_atom_width_20261007/REVIEW_HANDOFF.md), especially proof sections 3–9. Exact model checked against [unpaired corridor](../codex_unpaired_corridor_sensitivity_20261003/PROOF.md), sections 2–3 and 9; [linear frontier](../codex_linear_dimension_frontier_20261006/PROOF.md), sections 3–9; and [frontier invention](../codex_frontier_invention_20261006/PROOF.md), section 6.

## 1. Carl–Pajor: VERIFIED

Primary source: B. Carl and A. Pajor, *Gelfand numbers of operators with values in a Hilbert space*, Invent. Math. 94 (1988), 479–504, Theorem 2.2 (p. 487): [original paper](https://www.math.uci.edu/~rvershyn/teaching/hdp/carl-pajor.pdf). The original paper's indexed text was retrieved; direct PDF opening intermittently returned HTTP 502.

For a bounded operator u from ell_1^M to a Hilbert space,

    c_k(u) <= C ||u||_(1->2) sqrt(log(1+M/k)/k), 1<=k<=M,
    c_k(u) = inf_(codim E < k) ||u restricted to E||.

This is the arbitrary-atom operator theorem, not merely the width of the identity ell_1 -> ell_2. Since log(1+x)<=1+log x for x>=1, the author's displayed version follows. Applying c_(k+1) supplies codimension at most k. An arbitrarily enlarged absolute constant handles an infimum if needed; no explicit optimal numerical C_CP is claimed.

## 2. Exact public readout and atom reduction: VERIFIED in stated scope

Use co-moving survivor coordinates. The complete chosen response is

    X_t = G_t(a O_* X_(t-1)+V),
    O_* = C + 1 u^T + e_1 v_H^T.

Survivor trajectories do not meet row 1 or the terminal row in the no-wrap geometry. Their direct probe forcing is public. Therefore, between two histories,

    Delta X_S(t)=a G_S(t)[C_S Delta X_S(t-1)+1_S Delta J_(t-1)].

The complete J contains all bath, front and donor feedback: nothing is discarded. For a fixed survivor-supported reader B,

    B Delta X_S(N)=sum_(t=0)^(N-1) beta_t y_t^T,
    y_t=sqrt(h_S) Delta J_t,
    beta_t=B Phi_S(N,t+1) aG_S(t+1)1_S/sqrt(h_S).

Local transport is contractive, so ||beta_t||<=||B||. During a gap, the public local transport on the constant survivor vector is scalar. Readout vectors in that gap are parallel. Choose the largest-norm vector as the representative; then beta_t=lambda_t u_sigma with |lambda_t|<=1. Capture injections are singletons. The final uniform reset does not add a rotating direction. Hence S<=2R+1, and certainly S<=2R+2.

This argument uses the local Duhamel propagator, not the private complete propagator. Later feedback is already included in the realized J. It applies only when the entire survivor schedule, including capture times and characters, is fixed across the section.

Set Z_(sigma,j)=sum_(t in sigma)lambda_t y_(t,j). Then Z is continuous and odd, ||Z||_1<=Lambda, and X=uZ, where

    u(e_sigma e_j^T)=u_sigma e_j^T,
    ||u||_(1->F)=max_sigma ||u_sigma||<=c_B.

No factor sqrt(K), T, or orthogonality of the spatial atoms is required.

## 3. First logical error and correction

Author section 7 chooses ker A containing E_k, then concludes AZ=0 implies Z belongs to E_k. That implication has the wrong direction. Choose **ker A=E_k**, using the quotient map and padding zero coordinates to dimension k. Such A exists because codim E_k<=k. This repairs the proof without changing its bound.

With k=D-q-1 in [1,M-1], the map

    theta -> (C(H(theta))-C(H(-theta)), A Z(theta))

is continuous and odd from S^(D-1) to R^(q+k)=R^(D-1). Borsuk–Ulam gives a zero. At that point nuisance codes agree, Z belongs to E_k, and

    s_sep <= ||uZ||_F
          <= C_CP c_B Lambda sqrt((1+log(M/k))/k).

Thus the advertised inequality follows. For k>=M, an injective A gives a contradiction; D<=q+M. For k<=0 the nontrivial width inequality is unnecessary. One must not evaluate the logarithm outside its stated domain.

The nuisance map need not be linear or odd. Its antipodal difference is odd. No unsupported assertion about the dimension of a nonlinear equal-code fiber is used.

Here Lambda is already the **antipodal-difference** mass, as defined by the author. Consequently no further factor two is needed. A per-history bound 2 sqrt(K) N gives pair mass at most 4 sqrt(K) N, as the archive correctly states.

## 4. Query threshold: arithmetic VERIFIED, upstream premises OPEN in this audit

Assume the same survivor-supported B appears in the complete query bound, and all dense/reference discrepancies are consistently included:

    nu_actual <= 7.213 sqrt(m)/n ||B DeltaY_full||_F + eta,
    eta < .001.

For nu_actual>.002 the full signal exceeds (.001/7.213)n/sqrt(m). If equal codes leave complement norm at most 10^-4 n/sqrt(m), orthogonality of parameter columns gives

    ||B DeltaY_full V||_F
      > sqrt((.001/7.213)^2-10^-8) n/sqrt(m)
      > 9.5*10^-5 n/sqrt(m).

This arithmetic is correct. A triangle inequality would give a weaker constant and should not replace the orthogonal split.

The two [recovery](../codex_complete_query_normalization_recovery_20261007/PROOF.md) [records](../codex_stationary_parameter_complement_recovery_20261007/PROOF.md) explicitly did not recover the original proofs. The author cites later support and unarchived reviews. This focused audit does not independently establish those checkpoints, the precise identification of B in them, or the dense-error allocation. They remain hypotheses here. Likewise [the separated capture archive](../astra_separated_strong_capture_20261007/PROOF.md) must be used with its packet-ledger repair, not its uncorrected equation (21).

## 5. Strongest supported consequence

Conditional on the nuisance/separation hypothesis and pair mass Lambda<=4 sqrt(K) N,

    D <= q+1+C_CP^2 c_B^2 (4/(9.5*10^-5))^2
         (m K N^2/n^2)[1+log(SK/(D-q-1))].

The numerical square is less than 1.78*10^9; the author's 1.77*10^9 is rounded, not a safe strict upper. Use the exact square or round upward.

With R~log log n, K~m~n/R, N~C_T sqrt(nR), fixed C_T and c_B, M=SK=O(n), q=o(K), this gives

    D <= q+O(C_T^2 (n/R)(1+log R)) = o(n).

For D>=c n, the logarithm is bounded because M=O(n), and the inequality forces C_T^2=Omega(R). Then mN=Omega(n^(3/2)). These are conditional scope-specific conclusions, not a theorem excluding all Route 6 schedules.

## 6. Counterexample search and restrictions

No counterexample to the repaired abstract theorem was found. Allowing private readout directions invalidates the fixed-atom premise: a single atom u(theta)=theta with coefficient 1 can range over a high-dimensional sphere. That is an abstract warning, not a legal counterexample within the public-schedule scope. High donors at capture do not invalidate the atom reduction; they invalidate application of the supplied low-donor mass theorem. Long masks or additional public survivor events may increase S.

## 7. Review table and next obligation

| Item | Verdict |
|---|---|
| Carl–Pajor operator estimate / index shift | VERIFIED |
| Public survivor Duhamel formula | VERIFIED in stated geometry |
| TK to SK reduction | VERIFIED |
| Nuisance Borsuk–Ulam step | VERIFIED after ker A=E_k repair |
| Abstract Theorem B | VERIFIED after repair |
| Query checkpoint premises | OPEN in this audit |
| Separated Route-6 corollary | VERIFIED conditionally; PARTIAL unconditionally |

Next exact audit obligation: establish a single consistent survivor reader, reference/dense error allocation, and equal-code separation hypothesis (B1) from archived upstream proofs. This audit does not change CURRENT_THEORY.md or edit the author proof.
