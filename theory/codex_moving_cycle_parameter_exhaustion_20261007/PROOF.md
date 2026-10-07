# Moving-cycle parameter exhaustion: author report

Date: 2026-10-07. Author: Codex. Repository disposition: **PENDING REVIEW**.
This preserves the author's complete A–O argument for independent hostile review. The author-local conclusions below are not repository-level VERIFIED results. No independent review is asserted.

## Scope, notation, and inherited premises

The scope is one fixed source feature, the inherited four-site moving corridor, no wrap, public capture times and donor-segment boundaries, segment-constant group-shared donor gates, and one-step public captures. Arbitrary long survivor masks and independently prescribed bath forcing are excluded. Route 6 has not been constructed. This report neither constructs Route 6 nor proves linear dimension or its impossibility.

Write
\[
k=\lfloor n/2\rfloor,\quad l=n-k,\quad r=k-1,\quad
a=1-1/n,\quad \gamma=(1-1/\sqrt{k})^{-1},\quad c=\gamma^2/k,
\]
\[
s_k=\sqrt{k}/\gamma,\qquad cs_k^2=1,
\qquad g_H=1-n^{-2},\quad g_L=.995,
\quad b=(g_H-g_L)/2,\quad \bar g=(g_H+g_L)/2.
\]
There are \(m\) four-site tuples, \(K\) donor groups, \(h_S=2m\) survivor physical sites, and \(h_D=2m/K\) sites per donor group. Put \(w_j=ch_D\), \(w_S=ch_S\), \(w_B=\gamma-4mc>.9\). The group weights sum to \(\gamma\), not one.

The no-wrap/separation premise is \(m+N+4\le \lfloor n/4\rfloor/100\), with two moving tracks separated as in the inherited construction. We use \(m/n,N/n\le1/400\), and sufficiently large inherited \(n\). Here \(N\) counts the complete chronological history including trace repair, clear, and reset. The physical memory coordinate zero is invariant and excluded by the embedding \(E\).

The public bath/front bounds are
\[
.99<q_t\le q_{\max}=.9992,\quad f_{1,t}\le1/n,
\quad 0\le q_t-f_{z,t}\le2q_{\max}^{z-1}.
\]
All driven gates are at most \(g_H\) outside the common reset; the legal terminal trace corrections remain above .994. At each actual early-capture step all donor gates are \(g_L\). A broader version permitting high donors at capture is stated separately below.

Let \(\Psi\) be a PUBLIC ORTHONORMAL basis of the protected survivor suffix space, with \(d\le R\). Raw suffix vectors need not be orthonormal; no conditioning bound for an unnormalized suffix-mixing matrix is assumed. Every row observable \(\psi\) below has unit Euclidean norm and is supported on the survivors.

The complete legal-query normalization and stationary-complement code are supplied checkpoints for this task, not newly proved by this report:
\[
\nu\le7.213\frac{\sqrt m}{n}\|B\Delta Y_{\rm full}\|_F+\eta,
\quad \eta<.001,\qquad q_{\rm stat}\le R(2^R+1).
\]
Their independent provenance must be checked separately; the older repository query sections establish the underlying metric but do not themselves assert these newer constants or this stationary-code theorem.

# A. RECURRENCE AUDIT

The exact reference sensitivity and local sensitivity are
\[
M_0=L_0=0,\quad M_t=G_t(aO_*M_{t-1}+I),
\quad L_t=G_t(aCL_{t-1}+I),\quad H_t=M_t-L_t,
\]
\[
O_*=C+\mathbf1u^T+e_1v_H^T,
\quad u^T=\frac\gamma{\sqrt k}e_{d_{\rm cycle}-1}^T-c\mathbf1^T,
\quad v_H^T=\frac\gamma{\sqrt k}\mathbf1^T.
\]
For \(p_N=p_N^0=\psi\), the full and local costates are
\[
p_s=aO_*^TG_{s+1}p_{s+1},\qquad
p_s^0=aC^TG_{s+1}p_{s+1}^0.
\]
Expansion of the inhomogeneous sensitivity gives EXACTLY
\[
\psi^TH_Ne_c=\sum_{s=1}^N d_{c,s}[p_s(c)-p_s^0(c)].
\]
For a co-moving group,
\[
\Phi(s,g)=\frac{d_{g,s}}{h_g}
\sum_{i\in G_g(s)}[p_s(i)-p_s^0(i)].
\]
No-wrap and track separation prevent the local donor costate from reaching the protected survivor observable. Complete donor costates have constant density within a group: \(p_s(i)=c\Lambda_j(s)\). Consequently
\[
\Phi(s,j)=cd_j(s)\Lambda_j(s),
\quad \Lambda_j(s)=ad_j(s+1)\Lambda_j(s+1)+\kappa_s,
\]
\[
\kappa_s=-a\sum_i d_{i,s+1}p_{s+1}(i)
+as_k f_{1,s+1}p_{s+1}(1).
\]
The propagation gate is at \(s+1\); the injection gate in \(\Phi\) is at \(s\). The complete \(p\), not a frozen-feedback or first-renewal substitute, appears here.

Bath normalization needs care. If \(\lambda_B\) is the aggregate costate in the bath-plus-front-difference coordinates, define \(\Lambda_B=\lambda_B/w_B\). It is NOT the density of a single physical bath column divided by \(c\). The physical bulk bath response is a separate scalar filter below.

# B. POSITIVE-SYSTEM STRUCTURE

Physical contraction gives \(\|p_s\|_2\le1\). Set
\[
A_0=\frac1{c\sqrt{h_S}},\quad U=\Lambda_S,
\quad r_j=U-\Lambda_j.
\]
Thus \(|U|\le A_0\). During uniform-high survivor transport,
\[
r_j^+=ad_jr_j+a(g_H-d_j)U.
\]
At a balanced capture,
\[
r_j^+=ad_jr_j+a(\bar g-d_j)U
+\frac{ab}{c\sqrt{h_S}}\nu,
\quad \nu=\langle\chi/\sqrt{h_S},p_S\rangle,\quad |\nu|\le1.
\]
With donors low, \(g_L+2b=g_H\), so \(|r_j|\le A_0\) is preserved. The common reset gives \(r_j^+=aqr_j\). Uniform-high-survivor trace repair also preserves the bound for every legal donor gate \(d_j\le g_H\).

If donors need not be low at capture, each capture adds at most \(2bA_0\), yielding \(|r_j|\le(1+2bR)A_0\). We expose this extra factor rather than treating it as an absolute constant.

The aggregate bath satisfies \(|\lambda_B|\le\sqrt n\), hence \(|\Lambda_B|\le\sqrt n/w_B<A_0\), using \(c\sqrt{h_S n}\le3\sqrt{2m/n}<.212\). Therefore \(|r_B|\le2A_0\). For \(x=(U,r_D,r_B)\),
\[
\|x\|_\infty\le2A_0
\]
in the low-donor capture schedule, and at most \((2+2bR)A_0\) in the broader schedule.

During a constant-donor, uniform-high-survivor interval, compare with a CONSTANT PUBLIC bath gate \(q_*\). Put \(\alpha_H=ag_H\), \(\delta_i=g_i/g_H\), and
\[
B_{\rm def}=\sum_{i\ne S}w_i(1-\delta_i),\qquad
\beta=B_{\rm def}-(\gamma-1).
\]
The reference system is \(x^+=\alpha_HP x\), with
\[
r_i^+=\alpha_H[\delta_i r_i+(1-\delta_i)U],
\]
\[
U^+=\alpha_H\left[\sum_{i\ne S}w_i\delta_i r_i+\beta U\right].
\]
The inherited bath deficit gives \(\beta\ge0\). Its hub row sum is \(1-w_S\); every leaf row sum is one. It is positive and substochastic. The changing actual bath is retained as exact Duhamel forcing, not silently frozen.

# C. EXACT KAPPA REPRESENTATION

On a uniform-high survivor interval,
\[
\kappa_s=U_s-\alpha_HU_{s+1}.
\]
Thus \(TV(\kappa)\le(1+\alpha_H)TV(U)\), with explicit interval endpoint charges. At a capture,
\[
U_s=a\bar g U_{s+1}+\frac{ab}{c\sqrt{h_S}}\nu+\kappa_s.
\]
These identities imply the global bound \(|\kappa_s|\le3A_0\).

For the exact front, write forward front differences \(\delta_z=F_z-Z\), and \(\mu_z\) for their adjoints. Define
\[
C_F=[q+(s_k-1)f_1]\mu_1+\sum_{z\ge2}(q-f_z)\mu_z,
\]
\[
D_F=(f_1-q)\mu_1+\sum_{z\ge2}(f_z-q)\mu_z.
\]
The augmented adjoint equations are
\[
\kappa=-a\sum_gw_gd_g\Lambda_g^{\rm next}+aC_F,
\]
\[
\Lambda_B^+=aq\Lambda_B+\kappa+aD_F/w_B.
\]
In \(x\) coordinates the exact front forcing is
\[
e_F=(aC_F,0_D,-aD_F/w_B).
\]
The cancellation in this change of coordinates uses \(cs_k^2=1\), including the terminal-row contribution. It is not permissible to drop the terminal term before this cancellation.

# D. DONOR MAXIMAL-CONVOLUTION BOUND

## Dimension-independent arrowhead lemma

The author claims that for the preceding arrowhead system, with \(.99\le\delta_i\le1\),
\[
\boxed{\| (\alpha_HP)^{t+1}-(\alpha_HP)^t\|_{\infty\to\infty}
\le\frac{4096}{t+1}.}
\]
This is the highest-risk new lemma and requires independent review.

Here is the argument, including the treatment of absolute values. Let hub-to-leaf coefficients be \(p_i=w_i\delta_i\), leaf-to-hub coefficients \(q_i=1-\delta_i\), and leaf diagonal \(\delta_i\). For \(q_i>0\), the similarity weights \(\pi_0=1\), \(\pi_i=p_i/q_i\) symmetrize \(P\). The \(\delta_i=1\) case follows by continuity; no division by a private rate gap enters the final estimate.

An equivalent symmetric representation is diagonal \(\delta\) minus the rank-one form \(\sqrt{w\delta}\sqrt{w\delta}^{\,T}\), including survivor \(\delta_S=1\). Its spectrum lies in \([-(\gamma-1),1]\), with at most one negative eigenvalue. Indeed
\[
\sum_i\frac{w_i\delta_i}{\delta_i+\gamma-1}\le
\sum_i\frac{w_i}{\gamma}=1,
\]
which proves the shifted matrix is positive semidefinite. A rank-one subtraction has at most one negative eigenvalue.

Let \(K_t=(P^t)_{00}\). Its spectral measure has nonnegative weights; there is at most one negative pole \(-\rho\), \(\rho\le\gamma-1<.01\). Power entries are
\[
(P^t)_{00}=K_t,
\quad(P^t)_{0j}=p_j(K*\delta_j)_{t-1},
\]
\[
(P^t)_{i0}=q_i(\delta_i*K)_{t-1},
\]
\[
(P^t)_{ij}=\mathbf1_{i=j}\delta_i^t
+q_ip_j(\delta_i*K*\delta_j)_{t-2}.
\]
Here convolution is of geometric sequences. Positive spectral poles give nonnegative mixtures of at most three geometric kernels. Their complete homogeneous polynomial satisfies
\[
h_n(z_1,\ldots,z_k)=\binom{n+k-1}{k-1}
\mathbb E(\textstyle\sum_iX_i z_i)^n,\qquad k\le3,
\]
where \(X\) is uniform on the simplex. For the correspondingly shifted kernel
\(q_k(t)=\binom t{k-1}\int x^{t-k+1}d\mu(x)\), and \(t\ge8\), \(m_t=\lfloor t/2\rfloor\),
\[
|\Delta q_k(t)|\le\frac{64}{t+1}q_k(m_t).
\]
The binomial coefficient ratio is bounded by ten for \(k\le3\); its increment is bounded by a constant over \(t+1\). The exponential increment uses
\((1-x)x^{t-m_t}\le1/(t-m_t+1)\). This estimate is uniform even when poles coincide.

The negative-pole convolutions are handled without rate-gap denominators:
\[
(\delta_j*(-\rho))_{t-1}
=\frac{\delta_j^t-(-\rho)^t}{\delta_j+\rho},
\]
\[
(\delta_i*(-\rho)*\delta_j)_{t-2}
=\frac{(\delta_i*\delta_j)_{t-1}
-((-\rho)*\delta_j)_{t-1}}{\delta_i+\rho}.
\]
All these denominators are at least .99. Row sums remain dimension-independent after absolute values: \(\sum_jp_j\le1\), while
\(q_i\sum_{u\ge0}\delta_i^u=1\) cancels the slow leaf factor. The absolute negative-part row sum is at most four. Since the complete matrix is substochastic, the positive-part row sum is at most five. Its derivative is consequently at most \(320/(t+1)\), and the explicit negative part contributes at most \(100/(t+1)\). For \(t<8\), contraction bounds the difference by two. Multiplication by \(\alpha_H^t\) adds at most \(1/(t+1)\). The stated 4096 is conservative.

For the exact forced recurrence \(x_{t+1}=\mathcal T x_t+e_t\), \(\mathcal T=\alpha_HP\), the consequence is
\[
TV_\infty(x;I)\le4096H_L\|x_0\|_\infty
+(1+4096H_L)\sum_{t\in I}\|e_t\|_\infty,
\quad H_L\le1+\log L.
\]
Because \(\Phi_j=cd_j(U-r_j)\) inside a constant-gate segment,
\[
\sum_{t\in I}\max_j|\Delta\Phi_j(t)|
\le2cg_H TV_\infty(x;I).
\]
The maximum is INSIDE the time sum throughout. No sum over donors is used. This controls the coupled common field directly, avoiding a second logarithm from separately estimating each scalar convolution.

# E. BATH VARIATION

The physical forward lift gives front-above-bath differences \(e_{z,t}=v_{z,t}-u_t\ge0\). The first difference is at most one; for every global front slot \(z\ge2\), the ordinary positive tanh update has derivative at most \(q_t\) on the interval between bath and front. Thus
\[
e_{z,t}\le aq_t e_{z-1,t-1}\le q_{\max}^{z-1},
\quad 0\le W_t=\sum_z e_{z,t}\le\frac1{1-q_{\max}}=1250.
\]
This improves the earlier \(|W_t|\le1.1t\) estimate. It follows global chronology; the front is never restarted.

The public bath recursion is
\[
u_t=\tanh(.05+C_nu_{t-1}-D_nW_{t-1}),
\]
\[
C_n=a\gamma^2[(1+4m)/k-1/\sqrt k],
\quad |C_n|<.05,\quad D_n=a\gamma^2/k\le3/n.
\]
Let \(u_*\) solve \(u_*=\tanh(.05+C_nu_*)\), and \(q_*=1-u_*^2\). This is a public comparison value, not a replacement for the actual bath. The inherited initial value gives \(|u_0-u_*|\le.005\), so
\[
|u_t-u_*|\le |C_n|^t|u_0-u_*|
+\frac{1250D_n}{1-|C_n|}.
\]
Using \(|u_t|,|u_*|<.1\),
\[
\sum_{t=0}^N|q_t-q_*|\le.002+800(N+1)/n,
\]
\[
TV(q)\le.004+1600(N+1)/n.
\]
The exact bath-comparison forcing in \(x\) is
\[
e_{B,U}=-aw_B(q-q_*)\Lambda_B,
\quad e_{B,r_B}=-a(q-q_*)\Lambda_B,
\quad e_{B,r_D}=0.
\]
Its cumulative norm is at most
\[
\sum_t\|e_{B,t}\|_\infty
\le A_0[.01+4000(N+1)/n].
\]
This charge is paid once globally, not once per donor or stage.

# F. FRONT / TERMINAL VARIATION

The exact forward front equations, with \(J=-w^Tz-c\sum_z\delta_z\), are
\[
\delta_1'=a(f_1-q)Z
+a[q+(s_k-1)f_1](w^Tz+c\sum_z\delta_z),
\]
\[
\delta_z'=af_z\delta_{z-1}+a(f_z-q)Z
-a(f_z-q)(w^Tz+c\sum_z\delta_z),\quad z\ge2.
\]
These give the exact adjoint forcing in section C. The complete chronological front-costate recurrence is
\[
\mu_z(s)=af_{z+1,s+1}\mu_{z+1}(s+1)+c\kappa_s,
\quad z\le s,\quad \mu_z(N)=0.
\]
It includes ALL feedback renewals. The terminal row is an ordinary bath row in this geometry. From \(|\kappa|\le3A_0\),
\[
\sup_{s,z}|\mu_z(s)|\le\frac{3cA_0}{1-aq_{\max}}
\le3750cA_0.
\]
The sums of coefficients defining \(C_F,D_F\) are at most 2502, including \(s_kf_1=O(n^{-1/2})\). Consequently
\[
\|e_F\|_\infty\le2\cdot10^7cA_0,
\quad \sum_s\|e_{F,s}\|_\infty
\le6\cdot10^7(N/n)A_0.
\]
This is a summable forcing charge. It does not require sign cancellation or a chronological total-variation estimate for every physical front column. Exceptional moving parameter columns are instead encoded exactly in section J.

# G. LEGAL COUNTEREXAMPLE SEARCH

Logarithmically spaced near-critical donor rates are covered by the dimension-independent kernel estimate. Coincident rates are covered by convolution, without inverse rate gaps. Different donors can dominate different times and produce a logarithm, but not a hidden \(K\) factor in this proof.

Coherent donor switches are charged at the public segment boundaries. One-step captures are charged explicitly; later relaxation is part of the coupled semigroup, not charged as an independent immediate capture. Trace-repair gates remain legal and add a public boundary, not arbitrary within-segment private switching.

An independently alternating bath forcing would evade section E, but is not the legal public inverse lift. Likewise, arbitrary long survivor masks are outside this theorem. Global front renewals remain in the exact recurrence and are charged by section F. No legal counterexample within the stated premises was found. This is a scope statement, not an exhaustive classification of all RNN histories.

# H. BEST VARIATION THEOREM ACTUALLY PROVED

Let \(P\) count actual constant-donor/uniform-survivor intervals, including trace correction and clear. The intended publicly segmented protocol has \(P=O(R)\); keep \(P\) explicit until that schedule is specified. Define
\[
\epsilon_*=.01+10^8(N+1)/n.
\]
For low-donor captures, the shared field obeys
\[
cTV(\kappa)\le\frac C{\sqrt{h_S}}
[(P+1+\epsilon_*)H_{N+1}+R].
\]
On one ordinary donor segment of length \(L\),
\[
V_{D,I}\le\frac C{\sqrt{h_S}}H_L(1+E_I),
\quad E_I=4\sum_{t\in I}|q_t-q_*|+2\cdot10^7cL.
\]
Each public donor boundary costs at most \(2v\) in the maximum over groups; all \(R-1\) such boundaries cost \(2(R-1)v\), not \(K\) times this amount.

Survivor feedback costates \(h=p-p^0\) satisfy \(h_N=0\) and
\(h_i'=ad_{S,i}h_i+c\kappa\). The mean obeys
\(|\operatorname{mean}h|\le2/\sqrt{h_S}\). Uniform survivor transport contracts the coordinate range by \(\alpha_H\). At a capture,
\[
\operatorname{range}(dh)\le g_H\operatorname{range}(h)
+(g_H-g_L)|\operatorname{mean}h|.
\]
Thus \(\operatorname{range}h\le4bR/\sqrt{h_S}\). Its ordinary-transport variation costs \(O(bRN/(n\sqrt{h_S}))\). Direct capture transitions cost \(O(R(1+bR)/\sqrt{h_S})\). The \(R^2\) term is explicit, not hidden in an absolute constant or in \(2^R\) survivor word classes.

For a physical bulk bath column, separately write
\[
\chi'=aq\chi+c\kappa,\quad \chi_N=0,
\quad \|\chi\|_\infty\le3750/\sqrt{h_S}.
\]
Its variation is bounded by
\[
TV(\chi)\le1250[\text{endpoint charge}+cTV(\kappa)
+a\|\chi\|_\infty TV(q)],
\]
and multiplication by \(q\) adds \(\|\chi\|_\infty TV(q)\). This is a single physical bath type, not \(K\) additional responses.

Combining donor maximum, survivor maximum, and this bath type gives the complete BULK theorem
\[
\boxed{V_{\rm bulk}\le\frac C{\sqrt{h_S}}
[(P+1+\epsilon_*)H_{N+1}+R(1+bR)+bRN/n].}
\]
The constant \(C\) is absolute but deliberately conservative. Direct front/terminal parameter columns are not claimed to satisfy this bulk theorem: their exact code is included below.

If donors remain high at capture, replace \(P+1\) by \((P+1)(1+2bR)\). This proves a weaker \(O(R^2\log N/\sqrt m)\) bound when \(P=O(R)\), still sufficient for the stated approximate code consequence.

We used the safe unit-observable envelope \(v_0=1/\sqrt{h_S}\), rather than assuming the candidate small-amplitude bound without checking its observable normalization. For the fixed inherited \(b>.00249\),
\[
\bar v=\frac{3b}{\alpha_H\sqrt{h_S}}
\frac{1+B_c}{1-B_c}\ge3b/\sqrt{h_S},
\quad v_0\le134\bar v
\]
when the quoted inherited \(B_c\) premises hold. This is an absolute conversion for the inherited fixed contrast; it is not uniform in an arbitrarily vanishing mask contrast.

# I. SHARPNESS / LOG FACTORS

For free exponentials \(A_\lambda e^{-\lambda t}\), \(|A_\lambda|\le v\),
\[
\sup_\lambda|\Delta(A_\lambda e^{-\lambda t})|
\le v/(t+1),\quad \sum_{t<T}\sup_\lambda|\Delta f_\lambda(t)|
\le vH_T.
\]
The logarithm is sharp for the abstract family, using logarithmically spaced rates. Near-critical gates themselves are safe: \(\sum_t(1-\alpha)\alpha^t\le1\), and
\(1-ag_H=1/n+1/n^2-1/n^3\), not merely \(n^{-2}\).

The proof above avoids a second convolution logarithm by bounding the coupled arrowhead semigroup. It does not prove that a legal corridor history attains a matching logarithmic lower bound, nor does it establish optimal constants. The separate dimension-width logarithm is not investigated here.

# J. TRACK-SHIFT / FOURIER CONSEQUENCE

Let \(L_{\rm cyc}=\lfloor n/4\rfloor-1\) be the moving cycle period. The exceptional parameter set consists of the first and last \(N+1\) cycle positions, with a harmless allowance giving size at most \(2N+4\). Those columns may interact with chronological front/terminal or local edge paths. Encode their protected responses EXACTLY. This costs at most \(d(2N+4)\) continuous coordinates.

For nonexceptional moving columns, use the co-moving coordinate \(x=c_{\rm col}-s\). On the two public initial track intervals define
\[
F_s(x)=\Phi_g(s)-\Phi_B(s),
\]
and set it to zero outside them. Each interval has length \(m\). The exact bulk reconstruction is
\[
A_{\rm bulk}(c_{\rm col})=\operatorname{base}
+\sum_{s=1}^N F_s(c_{\rm col}-s),
\]
with circular padding of period \(L_{\rm cyc}\). This is identical to the actual row off the exceptional set; the bulk extension on exceptional columns is just a public-coordinate model used for coding. Private constant background is included in the DC code.

Its spatial first difference has the exact summation-by-parts form
\[
\Delta_{c_{\rm col}}A=F_1(c_{\rm col})-F_N(c_{\rm col}-N)
+\sum_{s=1}^{N-1}(F_{s+1}-F_s)(c_{\rm col}-s).
\]
Put \(Q=2\sup|F|+\sum_s\max_x|F_{s+1}(x)-F_s(x)|\). The difference is supported on the union of the two expanded tracks, of size
\[
M\le2(m+N+2),\qquad \|\Delta A\|_2\le\sqrt M Q.
\]
Do not identify \(M\), \(L_{\rm cyc}\), \(N\), and \(n\): they are separate quantities.

For the unitary DFT with angular frequencies \(\omega\in[-\pi,\pi]\),
\(|e^{i\omega}-1|=2|\sin(\omega/2)|\ge2|\omega|/\pi\). Hence
\[
\|P_{|\omega|>\omega_0}A\|_2
\le\frac{\pi\sqrt M Q}{2\omega_0}.
\]
The previously quoted \(1/(2\omega_0)\) expression depends on frequency convention and endpoint accounting. Here the angular-frequency \(\pi\) factor and temporal endpoints are retained explicitly.

Stacking \(d\le R\) unit orthonormal rows introduces \(\sqrt d\), not one. Use the stronger tolerance
\[
\tau=10^{-4}n/\sqrt m.
\]
The suggested \(5\cdot10^{-4}\) tolerance alone would not force chosen-probe separation from \(\nu>.002\), \(\eta<.001\), and coefficient 7.213. Indeed the complete signal lower scale is only \((.001/7.213)n/\sqrt m\). The stronger tolerance leaves a strictly positive chosen-probe remainder; orthogonal decomposition gives at least
\[
\sqrt{(.001/7.213)^2-10^{-8}}\,n/\sqrt m
>9.5\cdot10^{-5}n/\sqrt m.
\]

Allocate reference pair residual \(\tau/2\). It suffices to choose
\[
\omega_0=2\pi\sqrt{dM}Q/\tau,
\quad k_0=\left\lceil L_{\rm cyc}\sqrt{dM}Q/\tau\right\rceil,
\]
capped at the full Fourier bandwidth. Encode the real low Fourier coordinates of each virtual bulk row, together with exact actual exceptional-edge coordinates. The continuous code dimension is
\[
\boxed{q_{\rm cyc}\le d(2N+4)
+d\min\{L_{\rm cyc},2k_0+1\}.}
\]
Equal codes make the actual pair difference zero on the edges. Elsewhere it is the bulk high-pass pair difference; restriction cannot increase its norm. The \(\tau/2\) allocation includes the factor two between two single-history residuals.

Finally retain the actual dense perturbation, with the same realized gates. The inherited recurrent operator difference is at most \(4/(10^8n^2)\). Both propagators are contractions. Telescoping gives operator sensitivity difference at most \(e_RN(N-1)/2\); the FULL fixed-source Frobenius pair discrepancy is bounded by
\[
4\cdot10^{-8}N^2/n^{3/2}.
\]
This already covers all parameter columns and output rows. Projection onto any orthonormal protected basis or parameter complement does not increase it. Under \(N/n,m/n\le1/400\), this is at most \(2.5\cdot10^{-13}\sqrt n\), whereas \(\tau\ge.002\sqrt n\); the ratio is at most \(1.25\cdot10^{-10}\). Thus the reference pair allocation plus dense discrepancy is strictly below \(\tau\).

The code is continuous in history controls; all projections, track positions, and edge sets are public. This is approximate protected-response compression, not exact history recovery. The local moving-to-protected contribution is public/absent off the encoded edge by no-wrap separation. The fixed source factor \(\sigma\sqrt l\) is divided out in the inherited definition of \(M\); it must not be counted a second time in the code norm.

# K. ROUTE-6 SUBSTITUTION

For \(R\asymp\log\log n\), \(K\asymp m\asymp n/R\), \(N\asymp C_T\sqrt{nR}\), and \(P=O(R)\),
\[
\epsilon_*=.01+O(C_T\sqrt{R/n}),
\quad V_{\rm bulk}=O\left(\frac{R\log N+R^2}{\sqrt m}\right)
=O\left(\frac{R^{3/2}\log n}{\sqrt n}\right).
\]
Using conservatively \(L_{\rm cyc},M=O(n)\),
\[
q_{\rm cyc}=O(RN+R^{5/2}\sqrt n\log N),
\]
\[
\frac{q_{\rm cyc}}K
=O\left(\frac{C_TR^{5/2}}{\sqrt n}
+\frac{R^{7/2}\log n}{\sqrt n}\right)\longrightarrow0.
\]
Since \(N=o(m)\), the actual support \(M=O(m+N)=O(m)\) improves the Fourier term to \(O(R^2\sqrt n\log N)\); the conservative bound already suffices.

For captures with donors not necessarily low, the weaker variation theorem gives
\[
q_{\rm cyc}=O(RN+R^{7/2}\sqrt n\log N),
\quad q_{\rm cyc}/K
=O\left(\frac{C_TR^{5/2}}{\sqrt n}
+\frac{R^{9/2}\log n}{\sqrt n}\right)\to0.
\]
Adding the supplied stationary code,
\[
q_{\rm total}\le R(2^R+1)+q_{\rm cyc},
\qquad q_{\rm stat}/K=O(R^2(2^R+1)/n)\to0.
\]
Therefore \(q_{\rm total}=o(K)\) in this intended scaling and corridor scope. Additional public tail/clear lengths of \(O(R^2\log n)\) remain negligible relative to \(\sqrt{nR}\); an unspecified different schedule must have its actual \(N,P\) substituted, not assumed away.

# L. STATUS

**SHARED-FIELD VARIATION: PROVED (author-local conclusion).**

The proof includes the complete coupled chronology through exact Duhamel bath/front forcing. The strongest displayed bound retains \(P,R^2,N/n\) explicitly. Its \(O(R\log N)\) specialization is for the low-donor, one-step-capture protocol at intended Route-6 scaling. Arbitrary masks and arbitrary forcing are not covered. Independent hostile review is pending.

# M. PARAMETER EXHAUSTION STATUS

**MOVING-CYCLE PARAMETER EXHAUSTION: PROVED (author-local conclusion).**

The public Fourier-plus-edge code has equal-code protected complement pair residual below \(10^{-4}n/\sqrt m\), including the dense perturbation. Together with the supplied stationary code, its size is \(o(K)\) at the stated scaling. This conclusion requires the inherited complete-query/protected-norm identification and stationary-code checkpoint in the scope stated above. It is not a repository-level VERIFIED promotion, a Route-6 construction, or a general RNN memory theorem.

# N. NEXT EXACT OBLIGATION

Prove or refute the log-free residual width estimate
\[
D\le q_{\rm total}+C\frac{mKT^2}{n^2}
\]
for the remaining chosen-probe family after equalizing the nuisance code. This report identifies that obligation only; it does not investigate or claim it.

# O. PLAIN ENGLISH

1. The shared field could oscillate under arbitrary external forcing, but that is not the legal corridor. The actual bath stays close to a public fixed value; the full front has a summable influence. Those facts control the legal shared field in the stated family.
2. The author claims to have proved this control through the coupled positive arrowhead system, rather than treating donors as independent exponentials. Independent review should attack that new kernel lemma first.
3. No real legal counterexample was found within this scope. Long masks and independently prescribed bath signals are excluded rather than claimed harmless.
4. The author claims robust moving-cycle parameter exhaustion in this scope: all important complement information can be summarized by substantially fewer than K continuous numbers. Tiny temporal details are not recovered exactly.
5. If independent review verifies the chain, the next problem is the separate logarithmic width factor. No claim about Route 6 succeeding or being impossible follows solely from this report.

No experiment is used as proof. No historical theorem status or numerical measurement was changed by preserving this report.
