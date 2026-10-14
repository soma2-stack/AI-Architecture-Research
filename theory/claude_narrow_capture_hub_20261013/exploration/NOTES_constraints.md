# Working notes 1 — necessary resource constraints (peak width × horizon)

Provenance only. Superseded by ../PROOF.md: C8/C9 below were heuristic here and are
proved there as Lemmas 2.1–2.5 and Theorem 1.

Model and contract: unchanged from PR #26 §0 (frozen dense tanh, R0 = diag(aO, delta I_l),
O = UPU, b = .05, legal one-step queries, d_F selected source, eps = .001).
Budget: m = max_t |supp x_t| (peak driven width), T = horizon; target D = Omega(n),
mT = o(n^(3/2)). Repository usage: Theorem B of codex_holding_cost_attack ("only 4m
reference coordinates are driven per interior step"), bound (20) there ("every antipodal
past half-distance <= H/sqrt(n)"), so T >= eps sqrt(n) for any robust section.

## C1. Exact separation functional (single probe v)

For z = R0 Delta B_T v and legal gates g in [LO,HI]^n:

    max_g |g^T z| = gbar |sum z| + Dg ||z||_1,   gbar = (HI+LO)/2 = .7684, Dg = (HI-LO)/2 = .1718.

Proof: if sum z >= 0 the maximiser is HI on z>0, LO on z<0, giving HI P - LO N =
gbar(P-N) + Dg(P+N); symmetric otherwise.  So the single-probe separation is
s = (sigma sqrt(l)/(n sqrt n)) (gbar|sum z| + Dg ||z||_1), and s > .002 iff
gbar|sum z| + Dg||z||_1 > tau := .002 n sqrt(n)/(sigma sqrt l) (~ .0566 n).

## C2. The mean channel is one-dimensional

theta -> sum z(theta) is odd and continuous; for D >= 2 it vanishes on a subsphere
S^(D-2). There robustness needs ||z||_1 > tau/Dg ~ .33 n, hence
||Delta B_T v||_2 >= ||z||_2 >= .33 sqrt(n).

## C3. Single-probe rank lemma (Borsuk–Ulam)

If z(theta) = z_V(theta) + z_err(theta) with z_V odd, continuous, valued in a fixed
subspace V of dimension r, and (gbar+Dg)||z_err||_1 < tau - (something) uniformly, then a
robust section has D <= r.  (Odd map S^(D-1) -> V\{0}.)  For a single probe the whole
memory therefore lives in ONE n-vector; D is at most the number of independent row
directions that still carry difference at the query time.

## C4. Odd/even source expansion (exact)

Write G(+-theta) = Gbar +- dG, X_t = R0 B_(t-1) + c_t E v. Then

    Delta B_T = sum_t (prod_(s>t) Gbar_s R0) 2 dG_t Xbar_t.

Sources are (row,time) pairs with an odd gate part; each contributes
phi_e(theta) V_e(theta) with phi_e odd scalar and V_e even.  D <= number of sources whose
contribution is not negligible (Borsuk–Ulam on (phi_e)).

## C5. No amplification (exact)

||G R0 y|| <= ||y|| since ||R0|| <= 1 and 0 <= g <= 1.  Hence ||B_t|| <= ||B_(t-1)|| + c_t:
credit l2 grows only by injection. Broadcast is an orthogonal rotation, never a gain.
A hole of path length L carries c <= sum_(t) |v_(p(t))| <= sqrt(L) ||v|_path||.

## C6. Broadcast lifetime (exact structure)

In U-coordinates the k-block credit map is a P (U G U): the uniform mode u is U-coordinate
0, it is shifted to U-coordinate 1 = e1 + O(1/sqrt k), the front row, whose
preactivation contains gamma*Sum(h)/sqrt(k) ~ .035 sqrt(n): gate ~ 0.  So uniform credit
lives ONE step; only its gate-variation part G u - gbar u (l2 = alpha*std(g)) survives.
Per broadcast of l2 size alpha, captured l2 <= alpha*std(g_t).

## C7. Mass cap (exact steady-state identity, PR #26 §5)

J removes gamma^2 Sum(B)/k from every row each step; stored credit on gate-1 rows
saturates at Sum = sqrt(k) c_h / gamma (one step of broadcast inflow).

## C8. Storage lifetime (to be made rigorous)

Undriven ordinary rows sit at the bath value s ~ .05 - M/k (M = extra mass on special
rows; one-step adjustment because J subtracts the current mean): gate deficit ~ s^2.
Undriven near-zero chains drift at beta = .05 + aJ ~ s^3/3 + (M_(t-1)-M_t)/k.
Neutralising the bath needs M ~ .05k, i.e. Theta(n) mass; off-cycle particles decay
like sqrt(3/(2 age)), so holding it costs width >= c n (c ~ 1e-3).
Consequence (heuristic): with m = o(n), any undriven storage has an n-independent
lifetime Lambda.

## C9. Counting consequence (heuristic, single probe)

Final difference support at T lives on rows refreshed within ~Lambda + tau_b log(T/sqrt n)
steps, plus O(1) J-induced directions per step:  D <= C (m+1)(1 + log+(T/sqrt n)).
With T >= eps sqrt(n):  mT >= c D sqrt(n).  For D = Theta(n): mT = Omega(n^(3/2)).

Naive hub accounting agrees: N_b broadcasts x m_c captures >= C n, holes in flight
N_b L/T with L ~ n, so mT >= N_b L + m_c T >= 2 sqrt(C) n^(3/2)/2.
