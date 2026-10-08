# Independent focused review: Route 7B MTAB

Date: 2026-10-07. Reviewer: GPT-6 (independent mathematical desk review).
Target: `theory/claude_route7b_mtab_20261007/RESEARCH.md` and `REVIEW_HANDOFF.md` at commit `b003a85f1b8f5ca93a25b6b404406249383e9c46`.
**Status: SCOPED REVIEW COMPLETE.** This does not promote the original author submission or any upstream proof.

## Overall verdict

**The abstract non-crossing no-reuse theorem (NC) is VERIFIED within its explicit hypotheses.** It does **not** establish an unconditional cost impossibility in the full frozen-RNN model, because the needed long-mask signal-mass/passivity bound and the particular legal-query reader/normalization are not independently established here. Arbitrary crossing schedules remain OPEN.

| Claim | Independent verdict |
|---|---|
| Public survivor filter operator, equal class geometry | VERIFIED under the inherited fixed-source/no-wrap public-survivor model |
| Tail-sum measure representation | VERIFIED |
| Factorization width theorem Gamma | VERIFIED conditional on already reviewed topological Lemma F |
| Non-crossing Haar-prefix/Takagi theorem NC | VERIFIED under the public, common-order, equal-class conditions |
| Original constant-rate and staggered-start designs are non-crossing | VERIFIED |
| M-order crossing bound | VERIFIED for a valid measurable decomposition into M orders; exact M is not certified by sampled level counts |
| Universal crossing-schedule MON claim | OPEN |
| Literal TV-W (per-row TV <= 1 only) | REFUTED as an abstract statement by repeated filters |
| Strong physically applicable TV-W* | OPEN |
| Main robust linear memory construction / full MTAB cost obstruction | OPEN |

## 1. Exact readout and measure

For each of C equal co-moving survivor classes, the public local propagator multiplies a common source feedback coefficient `y_t` by
`phi_c(t)=prod_{r=t+1}^N a*g_c(r)`.
The class-orthonormal coordinates of its difference are `C^(-1/2) Phi y`; removing the common class mode yields exactly
`x = C^(-1/2) P0 Phi y`.
For every c, `phi_c(t)` is nondecreasing in t and `phi_c(N)=1`. Define `mu_c(1)=phi_c(1)`, `mu_c(u)=phi_c(u)-phi_c(u-1)` for u>1. These are nonnegative and sum to 1. Therefore
`sum_t phi_c(t)y_t = sum_u mu_c(u) sum_{t>=u} y_t`.
This is an algebraic representation, not a proof of a bound on the signal mass `Lambda`. Direct forcing cancels only for the stipulated pair of histories with the identical public survivor schedule.

## 2. Theorem Gamma

For `T=A W`, `Z(theta)=W y(theta)` is odd and continuous, and
`||Z||_1 <= [max_i ||W e_i||_1] Lambda`.
On an equal-nuisance-code antipodal zero set the separation hypothesis gives `||Z||_2 >= s/||A||`. Applying Lemma F and its zero-set index estimate gives
`D-q <= (||A|| max_i ||W e_i||_1 Lambda/s)^2`.
Block-diagonal identical factorizations on parameter columns do not incur a factor `sqrt(P)` if `Lambda` is the sum of absolute values over every time and column. This is a valid sufficient bound, not an optimization over all possible nonlinear representations.

The stated `gamma^(2/3)` subadditivity is also algebraically justified: stacking `alpha_i W_i` and the corresponding `A_i/alpha_i`, then minimizing `(sum alpha_i kappa_i)*sqrt(sum a_i^2/alpha_i^2)`, gives `gamma(T)^(2/3) <= sum gamma(T_i)^(2/3)`.

## 3. Theorem NC: the main calculation

If every time-slice `phi(t)` is decreasing in one common class order and lies in `[0,1]^C`, layer-cake decomposition makes each slice an integral of prefix indicator vectors in that order. Its image under the zero-sum Haar basis therefore has `ell_1` norm no greater than the largest prefix value.

For C=2^r, a prefix of k classes has exactly one nonzero Haar coefficient at each scale. Its total normalized `ell_1` mass equals
`f_r(k/C) = sum_{m=0}^{r-1} 2^(-m/2) dist(2^m k/C, Z)`.
Writing `w=1/sqrt(2)`, `f_r(x)=dist(x,Z)+w f_{r-1}(2x)`.
For x in [0,1/3], `f_r(x)<=1/3+wM=M` if `M=1/[3(1-w)]`.
For x in [1/3,1/2], `f_r(x)<=x+w(1-2x)+w^2 M`, whose maximum is at x=1/3, again M. Symmetry completes induction. Hence
`c_star = (2+sqrt(2))/3 = 1.138071...,`
and
`D-q <= floor(c_star^2 (||B|| Lambda/s)^2)`.
The alternating-binary prefixes approaching x=1/3 show sharpness of the **Haar certificate constant**, not necessarily sharpness of the true robust-dimension bound.

Independent finite exhaustive evaluation of the explicit prefix formula gave maxima:
- C=2: 0.500000
- C=4: 0.603553
- C=16: 0.879442
- C=64: 1.010914
- C=256: 1.075032
- C=1024: 1.106686
- C=2048: 1.116042
All are below the analytic limit 1.138071. This finite check supplements, rather than replaces, the proof.

Both original MTAB constructions satisfy the common-order hypothesis: constant class rates preserve gate order in each suffix product; staggered switch times preserve the same ordering of the number of low-gate future steps. Thus **their proposed d-fold *readout mass reuse* is disproved assuming a uniform signal-mass budget**, even when many linearly independent filters exist.

## 4. Crossing schedules and numerical scope

Splitting a layer-cake integral by regions of levels on which a fixed class order is valid gives the M-order bound. For weights `mu_i` summing to at most 1, `(sum mu_i^(2/3))^3 <= M` by Hölder. However `crossing_orders()` samples 400 level values and reports a heuristic order count, not a mathematically exhaustive M for arbitrary continuously varying profiles. The numerical `gamma` values from optimized nearly orthonormal bases are useful upper-bound witnesses **for the finite sampled instance subject to floating-point error**, not a universal proof or exact machine-checked interval certificate. No legal crossing family with robust D=Omega(n) is constructed, and Conjecture MON stays OPEN.

## 5. Literal TV-W counterexample

Take D disjoint time windows and b copies of each filter `f_i(t)=0.5*1_{W_j}(t)`, one for each orthonormal output row, so d=Db. Every row has sup norm <=0.5 and total variation <=1. With coefficients `y(theta)=theta/sqrt(D)` on the D windows, `Lambda<=1` for `theta in S^(D-1)`. The output norm is `sqrt(b)/(2sqrt(D))` for all theta, so `D*(s/Lambda)^2=b/4`; letting b grow at fixed D disproves any proposed universal `O(1+log(1+d))` factor under **only the literal per-row hypotheses**. But this abstract example violates the corridor's stronger bound for **every unit combination** of reader rows: combining b duplicate rows gives sup norm `sqrt(b)/2>1` for b>4. It is not an admissible physical MTAB gate construction.

## 6. Scope and exact next obligation

NC bounds the dimension obtainable *per unit of feedback mass*, not `Lambda` itself. Its RNN implication `mT=Omega(n^(3/2))` is conditional on:
1. a valid `Lambda <= C sqrt(K) N` for long masks / split survivor hubs;
2. valid fixed-source, normalized legal-query separation `s` with the same protected reader `B`, including the dense-model correction and nuisance-code handling;
3. the non-crossing, public, equal-class model.

Therefore the headline “MTAB as designed does not work” should be read narrowly: the two named designs cannot obtain a growing **multiplicative mass-reuse factor**, but their full legal-query target is not ruled out independently without the upstream mass budget. Crossing MON, TV-W*, and the non-cleared donor-feedback alternative remain open.

Recommended next work: keep obstruction optimization limited; if needed, independently verify long-mask signal-mass under the actual recurrence, while continuing constructive exploration of history-dependent readouts and the Route 7A donor-feedback channel. Do not modify CURRENT_THEORY.md on the basis of this review.
