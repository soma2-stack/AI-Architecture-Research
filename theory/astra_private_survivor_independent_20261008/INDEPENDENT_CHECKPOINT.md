# Independent private-survivor checkpoint

2026-10-08. Baseline `1bd496ff4e64bed59248df8ff25859c469858f79`.
This checkpoint was developed and saved BEFORE inspecting commit f8a96fb or its GPT-6 private-survivor folder. No competitor implementation or conclusion is used here.

## Original strategy: multiplicative echo

Use two moving survivor cohorts with opposite target states and identical private gates. Their state sums cancel, so the bath/front FORWARD history is public. Sensitivity feedback remains complete and private. At stage r and site i choose y_ri in [-1,1], use

    d_first=g_0 exp(eta y_ri),
    W interior gates g_H,
    d_last=g_0 exp(-eta y_ri).

The local homogeneous product A_echo=a^2(ag_H)^W g_0^2 is exactly public. All survivor sites receive the same final public reset, giving a common reference hidden endpoint. Donors use the baseline long-window trace-neutral protocol; they are either public (survivor-only experiment) or independently private (coupled experiment).

Two regimes: fixed-gap g_0=.9975, eta=.0001; and weak echo g_0=g_H exp(-.0025/R), eta=.002/R. Both stay between .995 and g_H. Private modulation does NOT provide new source features or change O_*.

This is a control-protocol investigation inside an existing architecture, not a claim of a new computational primitive. Multiplicative cancellation itself is elementary; the question is what complete chronological feedback retains after it.

## Exact local-source theorem

For one survivor moving characteristic, the contribution of all source injections before the block is multiplied by the public A_echo. The first injection inside the block also has the full product and is public. Only the W+1 later source coefficients depend on y, through d_last. Their coordinates are distinct under no-wrap. For two words, |Delta d_last|<=2g_0 sinh(eta). Across R stages,

    ||Delta ell_survivor||_2
       <=2g_0 sinh(eta) sqrt[(W+1) sum_(r=0)^(R-1) A_echo^(2r)].  (1)

The common final reset only contracts this. This is a row bound, not an assertion that rows for different sites have disjoint source support. Using a Frobenius bound on 2m rows gives a valid all-query upper; ordinary-row dilution gives the sharper

    nu_local <=200 sqrt(2) sigma (m/n) g_0 sinh(eta)
                         sqrt[(W+1) sum A_echo^(2r)].             (2)

At m~n/R,W~R, the fixed-gap sum is O(1), so (2)=O(R^-1/2). For the weak echo, sum<=R and eta=O(1/R), so (2)=O(1/R). Thus neither variant obtains constant-margin signal just by rereading an old LOCAL precharge. Complete H is the remaining possible mechanism.

## New scoped full compression theorem: fixed-gap echo

Let P be the common right parameter space. Four moving private tracks each meet at most m+N source coordinates, and two stationary donor compensators contribute 2m. The exact rank-two Duhamel induction gives

    P<=min(r,6m+6N).

This includes full parameter directions; it is not itself a dimension bound on matrix-valued credit.

For each completed block, all donor and survivor banks use public g_H in the interior. Define ACTUAL common feedback rows

    U_r=J_start,
    Q_r=sum_(k=1)^(W+1)(ag_H)^(W+1-k) J_(start+k).

Every complete row obeys

    M_out=A_i M_in+A_i U_r+a d_last,i Q_r+local_source_row_i.

The local source row is determined by the recent private controls and public geometry. It need not be small. Donors have A_i<=.995206; fixed-gap echoes have A_i<=.9975^2. Therefore, if two histories agree on their last h blocks' controls and U_r,Q_r, their complete active-row difference at the endpoint is <=2N rho^h in operator norm, rho=.995206. Code the final reset J as well. All controlled rows follow disjoint public characteristics; restriction and shift have operator norm one.

There is NO remaining public survivor compartment in this design: every survivor is part of the private echo bank. Code the ordinary bath row Z_N exactly and use the inherited chronological front residual. Public local rows outside the active banks cancel. A continuous code exists with

    q<=[2hm+(2h+2)P],
    equal-code nu_actual <=.073(N/sqrt(n))rho^h
                              +30000(N+1250)/n+e_dense.           (3)

The 2hm count permits independent private donor and survivor controls; survivor-only needs hm. The error includes the actual dense-model comparison when its inherited premises hold. h>=R means all stages are coded and the old difference is zero, rather than merely bounded.

For fixed C_T, N~C_T sqrt(nR)+O(R^2), m~n/R, choose h=O(log R) for fixed query tolerance. Then

    D<=q=O((m+N)log R)=O(n log R/R)=o(n).                        (4)

This is an AUTHOR conditional theorem pending independent review. It covers private boundary gates and complete feedback. It does not prove a universal private-survivor obstruction.

## Weak echo: exact unresolved point

Here A_echo can approach exp(-.005/R), so h=O(log R) does not suppress old state. The proof (3) then needs h comparable to R and does not give sublinear coding. Equation (1) still kills the old LOCAL precharge route, but full feedback can be imprinted before the echo cancels the local product. No robust construction or feedback upper theorem is claimed for weak echo.

## Legality, public chronology, cost

All private states occur in opposite pairs; all rows are driven continuously through precharge, private blocks and reset. Off-bank states are public by induction under no-wrap, with terminal outside all private paths. The chronological sparse implementation retains the full rank-two O_*, bath and front; it never supplies external J.

There are at most N+6m exceptional state sites. The previous sufficient bath/front certificate applies: if e=(gamma-1)+(gamma^2/k)2(N+6m)<=.02, the bath lies between tanh(.05-e) and tanh(.05+e), with gate <.9992; the explicit first-front lower argument and monotone propagation supply the other front bounds. This holds asymptotically, not automatically at small pilot widths. Legal future ordinary-row normalization and the dense lift remain inherited premises.

Total duration N=L_pre+R(W+2)+1; at W~R the coordinate-time scale is O(n^(3/2)/sqrt(R)+nR)=o(n^(3/2)). Actual driven reference input squares, including all holding steps and reset, are measured. Initial selected-memory preparation costs 6m[.05^2+atanh(sqrt(1-g_H))^2]. Source preparation is not free: retain its inherited fixed preparation cost; even a conservative O(n) bounded-coordinate preparation is lower order at the intended scaling. No public input center is subtracted. The finite reference tests do not independently reconstruct the exact source root or dense perturbation.

## Evidence and next obligation

The independent runner tests both echoes at seed 812, n=16384/32768/65536, stages 2/4/8, windows 8/16/64, legal horizons 1/2/4/8. Coupled and survivor-only controls are distinguished. Central-difference spectra and weakest-direction antipodal probes are diagnostics only.

Single next theorem before any competitor comparison: bound or exploit the complete feedback commutator left by a weak echo with eta=Theta(1/R), A_echo=1-Theta(1/R). A valid lower needs uniform robust antipodal separation, not exact rank or the echo's temporary precompensation signal.

Overall independent status: PARTIAL. Fixed-gap echo conditionally obstructed; weak-echo full feedback OPEN. No robust continuous memory section proved.
