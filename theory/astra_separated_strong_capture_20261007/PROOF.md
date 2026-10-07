# Separated Strong-Capture Passivity and Signal Budget

**Author derivation preserved from the Astra / Sol 6.1 session. Repository status: PENDING REVIEW.**

## Claim and scope

For the separated, zero-initial strong-capture family below, this derivation claims
\[
\Lambda\le2\sqrt K\,N,\qquad f(R)=O(1)=o(\sqrt R).
\]
It does not cover arbitrarily adjacent captures.

Assumptions:

1. Use the exact complete group recurrence and retain the single chronological front correction \(\rho_t\).
2. Survivor weight \(p=w_S\), \(s=\sqrt{h_S}\), total weight \(\sum_gw_g=\gamma\), bath weight \(w_B=\gamma-2p\).
3. \(p\le.01\), \(\epsilon=\gamma-1\le10^{-4}p\), \(\alpha=ag_H\), \(1-\alpha\le10^{-4}p\), \(a,g_H\ge.99999\).
4. \(g_L=.995\), strong balanced capture \(b=(g_H-g_L)/2\approx.0025\); capture labels are distinct Walsh characters and donors are low at capture.
5. Between captures, survivors use \(g_H\), donor gates satisfy \(d_i\le g_H\), and bath gates satisfy \(.99\le q_t\le.9992\).
6. The inherited cone condition holds: \(B_{\rm def}=\sum_{g\ne S}w_g(1-d_g/g_H)\ge\gamma-1\).
7. Consecutive captures have at least \(\lceil100/p\rceil\) ordinary steps between them. A final truncated window is charged to terminal packet storage.
8. \(np\ge160C_\rho\), where \(C_\rho=2\cdot10^{10}\). This is an explicit asymptotic large-\(n\) condition.
9. The complete front is initialized once and evolved chronologically; it is not reset at capture boundaries.

The 100/p spacing is substantive. Independently prescribed bath forcing and unaccounted dense-model perturbations are outside this derivation. The inherited recurrence and source normalization are in [codex_frontier_invention_20261006/PROOF.md, section 6](../codex_frontier_invention_20261006/PROOF.md).

## 1. Exact recurrence and source

For group averages \(z=(z_1,\ldots,z_K,z_S,Z)\), weights \(w\), and diagonal gate matrix \(D_t\), the exact complete recurrence is
\[
z_t=aD_t(I-\mathbf1w^T)z_{t-1}+D_tf+aD_t\mathbf1\rho_{t-1},
\quad S_w=w^Tz,\quad J=-S_w+\rho.
\tag{1}
\]
The front term \(\rho\) is retained and charged below.

For one normalized unit witness \(b_j\),
\[
f_j=KF,\quad f_S=-F,\quad f_i=0\ (i\ne j),\quad
F=\frac1{2\sqrt{m(K+1)}},\quad sF=\frac1{\sqrt{2(K+1)}}.
\tag{2}
\]
Its weighted source sum is zero since \(w_j=p/K\).

Define the nonnegative physical-state storage
\[
\mathcal E_{\rm core}(z)=\frac{s}{p}
\left(\sum_{g\ne S}w_g|z_g|+|S_w|\right).
\tag{3}
\]
The survivor Walsh storage is \(E_W=s\sum_{I\ne0}|z_I|\). At a capture put
\[
A_c=sb|y_0|,\qquad Q_c=sb|y_e|.
\]
The established Walsh ledger is
\[
E_W'+Q_c\le\alpha E_W+A_c.
\tag{4}
\]

## 2. Exact cone decomposition and ordinary dissipation

Use the cone
\[
\mathcal C=\{z_g\ge0\ (g\ne S),\ S_w\le0\}.
\tag{5}
\]
For \(z\in\mathcal C\), let \(V=-z_0\); then
\[
pV=\sum_{g\ne S}w_gz_g+|S_w|.
\]

For arbitrary signed \(z\), define
\[
H_+=\sum_{g\ne S}w_g(z_g)_+,\quad H_-=\sum_{g\ne S}w_g(-z_g)_+,
\]
\[
V_+=\frac{H_++(-S_w)_+}{p},\qquad
V_-=\frac{H_-+(S_w)_+}{p}.
\tag{6}
\]
Put positive non-survivor coordinates in \(x^+\), reversed negative coordinates in \(x^-\), and set \(x_S^\pm=-V_\pm\). Then
\[
z=x^+-x^-,\quad x^\pm\in\mathcal C,\quad
\mathcal E_{\rm core}(z)=s(V_++V_-),
\]
\[
|S_w(x^+)|+|S_w(x^-)|=|S_w(z)|.
\tag{7}
\]

For homogeneous ordinary transport with survivor gate \(g_H\), put \(d_i=g_i/g_H\). On a cone vector the exact survivor recurrence gives
\[
V'=\alpha(V-|S_w|).
\tag{8}
\]
Non-survivor coordinates remain nonnegative. The inherited bath-deficit premise ensures
\[
\frac{S_w'}{\alpha}\le |S_w|(\gamma-B_{\rm def}-1)\le0,
\tag{9}
\]
so the cone is invariant. Apply (8) to the two vectors in (7), and re-decompose their output:
\[
\boxed{\mathcal E_{\rm core}(Tz)+\alpha s|S_w|
\le\alpha\mathcal E_{\rm core}(z).}
\tag{10}
\]

The ordinary gated source \(Df\) lies in the cone because its weighted sum is \(pF(d_j-g_H)\le0\). Its storage is exactly
\[
\mathcal E_{\rm core}(Df)=sg_HF.
\tag{11}
\]
Thus the per-step outside source is \(sg_HF=O(1/\sqrt K)\).

## 3. Strong-capture identity

At capture, survivor mean gate \(\bar g=g_H-b\), donor gate \(g_L=\bar g-b\), bath gate \(q_c\). For a cone packet write \(u=-S_w\ge0\). Its pre-gate states are
\[
y_g=a(z_g+u)+f_g,\qquad y_0=a(-V+u)-F\le0
\tag{12}
\]
for the source packet; omit \(-F\) for a homogeneous packet. Since \(u\le pV\), the displayed sign holds.

The captured survivor mean is \(z_0'=\bar g y_0+b y_e\). First omit hidden return \(b y_e\), and let \(\widehat S\) be the weighted sum after capture gates. Since \(\sum_gw_gy_g=a(1-\gamma)S_w\), exact gate splitting gives
\[
\boxed{\widehat S
=a\bar g(\gamma-1)|S_w|
-b\sum_{i\in D}w_i y_i
+(q_c-\bar g)w_By_B.}
\tag{13}
\]
The donor term is nonpositive; the bath deviation is explicit.

If \(\widehat S\le0\), the post-capture core is in the cone and \(\mathcal E'_{\rm core}=s\bar g|y_0|\). If \(\widehat S>0\), then \(D'=\widehat S+p\bar g|y_0|\) and \(\mathcal E'_{\rm core}=s\bar g|y_0|+2s\widehat S/p\). Thus
\[
\boxed{\mathcal E'_{\rm core}+A_c
=sg_H|y_0|+\frac{2s}{p}(\widehat S)_+.}
\tag{14}
\]
Adding hidden return changes core storage by at most \(Q_c\), since it is \(s\)-Lipschitz in the survivor mean. The \(A_c-Q_c\) terms cancel against the Walsh ledger (4).

For a homogeneous cone packet, \(g_H|y_0|\le\alpha V\); for the source packet, \(g_H|y_0|\le\alpha V+g_HF\). Thus only the positive cone crossing in (14) remains to be paid.

## 4. Bath-versus-donor crossing charge

For a cone packet let \(Z=z_B\ge0\), so \(y_B=a(Z+u)\), \(Z_{\rm post}=q_ca(Z+u)\). Drop the nonpositive donor term in (13):
\[
(\widehat S)_+\le
a[\bar g\epsilon+(q_c-\bar g)_+w_B](Z+u).
\tag{15}
\]
The assumptions imply \(w_B\le1.000001\), \(q_c-\bar g\le.001705\), and
\[
\boxed{\frac{2s}{p}(\widehat S)_+
\le .0035\,\frac{s}{p}Z_{\rm post}.}
\tag{16}
\]

For the subsequent ordinary cone evolution define
\[
\beta_t=aq_t,\quad \eta_t=aw_B(g_H-q_t),\quad
L_{D,t}=\sum_iw_i(g_H-d_{i,t})a(z_{i,t}+u_t)\ge0.
\]
The exact bath/mean recurrence is
\[
u_{t+1}=(\eta_t-\alpha\epsilon)u_t+\eta_tZ_t+L_{D,t},
\quad Z_{t+1}=\beta_t(u_t+Z_t).
\tag{17}
\]
Let \(H_t=u_t+Z_t\). With \(w_B\ge.98\), \(g_H-q_t\ge.00079\), \(\alpha\epsilon\le10^{-6}\), and \(1-w_B=2p-\epsilon\),
\[
u_{t+1}\ge.0007H_t,\qquad H_{t+1}\ge(1-.021p)H_t.
\tag{18}
\]
For at least \(\lceil100/p\rceil\) ordinary steps this yields
\[
\boxed{\sum_{1\le t<L}u_t\ge Z_0/(40p).}
\tag{19}
\]
The crossing charge (16) is at most .14 times raw future output \(s\sum u_t\). Relative to actual ledger dissipation \(\alpha s\sum u_t\), use the conservative factor .15.

For a final capture with a shorter remaining interval, (18) gives \(H_N\ge.12H_0\), and cone storage satisfies
\[
\mathcal E_{\rm core}(z_N)=sV_N
\ge \frac{s w_B}{p}Z_N
\ge .11\frac{sZ_0}{p}.
\tag{20}
\]
This pays the final crossing from terminal storage.

Keep a signed collection of cone packets representing the core state; split after captures and carry each packetâ€™s bath value forward. Charge source packets by (11) and hidden returns by (4). The payment windows are disjoint by the capture spacing. Triangle bounds \(|Z|\le\sum Z_{\rm packet}\) and \(|S_w|\le\sum u_{\rm packet}\) dominate the canonical crossing. Therefore
\[
\boxed{\sum_c\Xi_c
\le .15\left(\alpha s\sum_t|S_{w,t}|+\mathcal E_N\right).}
\tag{21}
\]

## 5. Complete chronological front correction

For the stationary probe, inherited global front equations and moment relation are
\[
Z_t=aq_t(Z_{t-1}+J_{t-1}),\quad
F_{1,t}=af_{1,t}(J_{t-1}+B_{t-1}),\quad
F_{z,t}=af_{z,t}(F_{z-1,t-1}+J_{t-1}),
\]
\[
B_t=Z_t-\frac{\sqrt k}{\gamma}J_t.
\tag{22}
\]
Set \(e_{z,t}=F_{z,t}-Z_t\). Using \(f_1\le1/n\) and \(0\le q_t-f_{z,t}\le2(.9992)^{z-1}\),
\[
|e_{1,t}|\le |Z_t|+2|J_t|,
\]
\[
|e_{z,t+1}|\le .9992|e_{z-1,t}|
+2(.9992)^{z-1}|Z_t+J_t|,\quad z\ge2.
\]
Summing the non-restarted chronology,
\[
\sum_{t,z}|e_{z,t}|\le4\cdot10^6\sum_t(|Z_t|+|J_t|),
\qquad \sum_t|Z_t|\le1250\sum_t|J_t|.
\]
Since \(c=\gamma^2/k<3/n\) and \(\rho=-c\sum_z(F_z-Z)\),
\[
\boxed{\sum_t|\rho_t|\le\frac{C_\rho}{n}\sum_t|J_t|,
\quad C_\rho=2\cdot10^{10}.}
\tag{23}
\]
Core and capture-input front cost is at most \(4s|\rho_t|/p\). Also \(s\sum|J|\le s\sum|S_w|+s\sum|\rho|\). If \(np\ge160C_\rho\), the front cost is at most .05 of accumulated output. This charges the complete front once.

## 6. Full signal-mass bound

Let \(U=s\sum_t|S_{w,t}|\). Core, Walsh, capture and front ledgers give
\[
\mathcal E_N+\alpha U
\le sg_HFN+.15(\mathcal E_N+\alpha U)+.05U.
\tag{24}
\]
For the admitted large \(n\), this implies
\[
\mathcal E_N+U\le1.25sg_HFN,\qquad
s\sum_t|J_t|\le1.27sg_HFN.
\tag{25}
\]
With (2), each normalized \(b_j\) has output at most \(.90N/\sqrt K\), with slack.

The inherited probe relation is \(B=VA\), \(A=H^{-1}/\sqrt{1+1/K}\), so \(A^{-1}=\sqrt{1+1/K}H\), where \(H=I-(1-1/\sqrt2)\mathbf1\mathbf1^T/K\). Its induced column \(\ell_1\) norm is below 1.84. Linearity and the triangle inequality yield
\[
\boxed{\Lambda=\sum_{t,j}|s\,u^TX_tv_j|\le2\sqrt K\,N.}
\tag{26}
\]

No \(R\)-dependent factor appears in this scope. Thus \(f(R)=O(1)=o(\sqrt R)\).

## 7. Route-6 consequence and limitations

At \(R\asymp\log\log n\), \(p\asymp m/n\asymp1/R\), so \(100/p=O(R)\). The intended gap \(\Delta_{\min}\ge C(n/m)\log n=\Omega(R\log n)\) eventually exceeds \(100/p\), for fixed positive \(C\).

Together with the segment-atom width estimate, this gives conditionally
\[
D-q=O(n\log R/R)=o(n).
\]
This remains conditional on the separate query-normalization, parameter-exhaustion and width premises. Close captures and unaccounted dense perturbations remain outside scope. The threshold \(np\ge3.2\cdot10^{12}\) is explicit and intended asymptotically.\n