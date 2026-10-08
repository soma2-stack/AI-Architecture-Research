# Route 7A with growing R: uniform local-direct diameter, feedback obligation isolated

Author: GPT-6. Date: 2026-10-07 (America/Detroit).
**Status: NEW AUTHOR PROOF / PENDING INDEPENDENT REVIEW.**
This is a rigorous result *under its stated inherited local-C corridor assumptions*, not a verified full-model theorem. Main Route 7A \(D=\Omega(n),\ mN=o(n^{3/2})\) is OPEN.
Do not modify \`CURRENT_THEORY.md\`.

## 0. Main result

In the exact local part \(L_t\) of Astra's open-cycle/rank-two decomposition, consider \(R\) legal trace-neutral donor stages (Astra's Eq. (25)), on two moving donor rows and two stationary compensator rows per tuple, and **no private gates on any other characteristic**. All public waits, public survivor captures, and final common reset are allowed as contractions. Let \(m\) denote the number of four-site tuples; distinct moving tracks have \(2m\) final moving donor rows.

Write \(\epsilon=10^{-4},\ g_*=0.9975\), and \(0.99\le a,g_H\le1\). Set
\[
d_{\min}=g_*-\epsilon,\qquad
L_*=(g_*/d_{\min})^2=1.0002005314\ldots,\qquad
\rho=(g_*+\epsilon)\frac{g_*^2}{g_*-\epsilon}=0.9952057701\ldots<1.
\]
For any two full control schedules \(x,y\in[-1,1]^{Rm}\), with the same public schedule and incoming local scalar traces matched at all three-step boundaries, and with one fresh source coordinate per time on each no-wrap moving characteristic,
\[
\boxed{\|\Delta L_N\|_{\rm op}\le\|\Delta L_N\|_F
\le \frac{8\epsilon}{1-\rho}\sqrt{2m}
<0.16687\sqrt{2m}.}\tag{A}
\]
The stationary compensator rows of \(\Delta L_N\) are exactly zero.

Consequently, for even n, \(\ell=n/2\), \(\sigma<0.051\) and the inherited fixed-feature query normalization,
\[
\boxed{\nu_{\rm ref}(\Delta L_N)
\le\frac{\sigma\sqrt{\ell}}n\|\Delta L_N\|_{\rm op}
<0.00852\sqrt{m/n}.}\tag{B}
\]
For \(m\le n/R\),
\[
\nu_{\rm ref}(\Delta L_N)<0.00852/\sqrt R<0.002 \quad(R\ge19).\tag{C}
\]
More generally with \(m\le C_m n/R\), the RHS is \(0.00852\sqrt{C_m/R}\).
The bound is **uniform in \(R\), precharge duration, public waits and horizon** while no-wrap and trace-neutrality hold. It does NOT bound \(H_N=M_N-L_N\) and does NOT imply that the full un-cleared candidate fails. The new result identifies complete private \(J/B\) feedback as the only possible source of the missing \(0.002\) margin once \(m/n\to0\).

## 1. Local characteristic setup and exact three-step row formula

The exact inherited matrices are
\[
M_t=G_t(aO_*M_{t-1}+I),\quad L_t=G_t(aCL_{t-1}+I),\quad H_t=M_t-L_t,\quad
O_*=C+\mathbf1u^T+e_1v_H^T.
\]
The open shift \(C\) maps each moving donor characteristic \(c_i(t)=A+i+t\) or \(B+i+t\) from \(c_i(t-1)\) to \(c_i(t)\), and fixes each off-cycle compensator. Public bath/front/other characteristic gates are identical for both histories. In no-wrap geometry, each moving characteristic receives an input into a *different* parameter column \(e_{c_i(t)}\) at each time. Its local row vector \(\ell_t\) has **nonnegative entries bounded by 1**, therefore
\[
\tau_t=\ell_t\mathbf1\ge0,\qquad
\|\ell_t\|_2^2\le\tau_t. \tag{1}
\]
Under public local gates the scalar trace obeys \(\tau\mapsto g(1+a\tau)\).

At the start of private stage \(j\), \(\ell_0(x),\ell_0(y)\) may differ but their traces are exactly the same public scalar \(\tau\). Take phase gates \(d_1=g_*+\epsilon x,\ d_2=g_H,\ d_3=d_3(x)\); denote by \(e_1,e_2,e_3\) the fresh, pairwise distinct unit parameter coordinate rows injected at the three moving sites (NOT the fixed front coordinate \(e_1\) of \(O_*\)). The local row after the stage is exactly
\[
\ell_3(x)= a^3 g_H d_1d_3\,\ell_0(x)
+a^2g_Hd_1d_3\,e_1^T
+a g_H d_3\,e_2^T+d_3\,e_3^T. \tag{2}
\]
For stationary compensators \(e_1=e_2=e_3=e_c\) and the incoming row is \(\tau e_c^T\), so the scalar trace-neutral formula matches the **entire stationary row**.

The compensation gate is
\[
d_3(x)=g_*\frac{A+B g_*}{A+B d_1(x)},\quad
A=1+a g_H,\quad B=a^2g_H(1+a\tau)>0, \tag{3}
\]
giving \(d_3(1+a g_H(1+a d_1(1+a\tau)))=\tau_{\rm target}\) independent of \(x\). This is an identity for the *LOCAL trace*, not \(J_t,B_t,H_t\).

## 2. A uniform single-stage local perturbation bound

Set \(z=A/B\), \(p(d)=d\,d_3(d)\). From Eq. (3),
\[
|d_3(x)-d_3(y)|\le L_*\epsilon|x-y|,\qquad
|p(d_1(x))-p(d_1(y))|\le L_*\epsilon z|x-y|. \tag{4}
\]
For the second inequality, \(p'(d)=g_*(z+g_*)z/(z+d)^2\), and
\((z+g_*)/(z+d_{\min})^2\) is decreasing in \(z\ge0\); its maximum is \(g_*/d_{\min}^2\). This yields \(p'\le L_*z\).

For \(a,g_H\ge0.99\),
\[
z=\frac{1+a g_H}{a^2g_H(1+a\tau)}
\le\frac{2}{0.99^3(1+0.99\tau)}.\tag{5}
\]
The elementary inequality
\[
\frac{1+\sqrt\tau}{1+0.99\tau}\le\frac54\quad(\tau\ge0)
\tag{6}
\]
holds because, with \(v=\sqrt\tau\), the difference
\((5/4)(1+0.99v^2)-(1+v)=1.2375v^2-v+0.25>0\)
(negative discriminant).

Fix one incoming row \(\ell_0(y)\) and subtract the two stage updates (2). The difference is the surviving homogeneous part \(a^3g_Hp_x\,\Delta\ell_0\), plus the gate-change forcing
\[
\delta_{\rm fresh}
=(p_x-p_y)\,[a^3g_H\ell_0(y)+a^2g_He_1^T]
+(d_3(x)-d_3(y))\,[a g_H e_2^T+e_3^T].\tag{7}
\]
Since \(e_2,e_3\) are distinct,
\(\|a g_H e_2+e_3\|_2\le\sqrt2\).
By (1),(4),(5),(6),
\[
\|\delta_{\rm fresh}\|_2
\le\epsilon|x-y|L_*
\left[\frac{2}{0.99^3}\frac{\sqrt\tau+1}{1+0.99\tau}+\sqrt2\right]
\le\epsilon|x-y|L_*
\left[\frac{2}{0.99^3}\frac54+\sqrt2\right]
<4\epsilon|x-y|.\tag{8}
\]
The homogeneous multiplier obeys
\[
a^3 g_H p_x \le (g_*+\epsilon)\,\max_x d_3(x)
\le (g_*+\epsilon)\frac{g_*^2}{g_*-\epsilon}
=\rho<1. \tag{9}
\]
Therefore, for the difference on any one moving track at consecutive private stage boundaries,
\[
\|\Delta\ell_{j}\|_2\le
\rho\|\Delta\ell_{j-1}\|_2+4\epsilon|x_j-y_j|.\tag{10}
\]
Any intervening public waiting/capture gates are contractions on the moving characteristic and add the SAME public injections. They do not increase the difference; both scalar traces remain matched. At the initial public preparation, \(\Delta\ell_0=0\).

Iterating, for all \(R\), including arbitrarily large \(R\),
\[
\|\Delta\ell_R\|_2\le4\epsilon\sum_{j=1}^R\rho^{R-j}|x_j-y_j|
\le\frac{8\epsilon}{1-\rho}<0.16687.\tag{11}
\]

## 3. Matrix bound, query and limitations

The only local \(C\)-paths that can encounter private gate sites are the \(2m\) moving donor tracks and \(2m\) stationary compensators. The latter have zero **final** local difference by (3) and the fixed injection column, including under public waits and common reset. The remaining local rows are publicly forced and identical across histories. Thus \(\Delta L_N\) has at most \(2m\) nonzero physical rows, each satisfying (11), yielding (A).

For any legal future \(Q\), \(\|c_Q\|_2\le1\), so \(\nu_{\rm ref}(A)\le(\sigma\sqrt\ell/n)\|A\|_{\rm op}\). Insert (A) and \(\ell=n/2\) to get (B), then \(m\le n/R\) gives (C). (B) bounds the entire local direct term at the actual endpoint, regardless of how local traces were maintained throughout.

**Critical:** The complete sensitivity is \(M_N=L_N+H_N\). Even when \(\Delta L_N\) is negligible, \(\Delta H_N\) may contain replenished, persistent feedback and broad bath/front contributions. Triangle inequality gives only
\(\nu_{\rm ref}(\Delta M_N)\le\nu_{\rm ref}(\Delta L_N)+\nu_{\rm ref}(\Delta H_N)\);
it does not upper bound \(\Delta H_N\). A hypothetical robust pair with \(\nu_{\rm ref}(\Delta M_N)>0.002\) must have
\[
\nu_{\rm ref}(\Delta H_N)\ge
\nu_{\rm ref}(\Delta M_N)-0.00852\sqrt{m/n}.\tag{12}
\]
This is the new **feedback-only obligation** for growing \(R\).

The proof applies only where the trace-neutral scalar \(\tau\) is in fact public at each private boundary, all four tuple gates are synchronized, moving donor characteristics are no-wrap and receive at most one injection per parameter column, all non-donor gates are public, and \(a,g_H\in[0.99,1]\). It does not cover private survivor gates, source schedules with repeated injections into the moving characteristic, changes in frozen matrices, or readout features outside the fixed-source slice. The full historical model's exact endpoint/lift and dense-model error remain inherited premises, not re-proved here.

The bounds are intentionally loose: a triangle inequality loses the orthogonality between fresh input columns from different stages; no claim of optimal constant 4 or \(\rho\) is made. This is **not** a universal impossibility result.

## 4. Finite checks, status, next obligation

Independent algebra check of (3) on randomly selected \(x,y,\tau\) gives identical scalar endpoint traces. A scalar moving-row reference simulation (no rank-two feedback) with \(n=10^6\), \(g_H=.99999\), \(L=500\), and \(R=1,8,32,128,512\), with or without four public waits per stage, found exact trace matching at printed precision. Sampled row differences grew from about \(2\cdot10^{-4}\) (R=1) to \(1.65\cdot10^{-3}\) (R=512), well below the uniform \(0.16687\) bound. These finite checks are diagnostic only; they are not a certificate of full-model query performance.

**Verdict:** Scoped local-direct theorem (A)–(C) **PROVED BY AUTHOR / PENDING REVIEW**; original strict-cost \(D=\Omega(n)\) construction **OPEN**; retained feedback \(H_N\) **OPEN**.

**Next exact mathematical obligation:** For the identical trace-neutral protocol and public survivor schedule, derive a comparable uniform bound for the **actual legal-query projection of the full private feedback \(\Delta H_N\)**, or construct a continuous \(D=c n\) sphere with a uniform \(>0.002\) antipodal separation. In particular, bound or exhibit the re-injection via \(J_t=u^TM_t\) and \(B_t=v_H^TM_t\) without replacing it by the local \(L_t\), artificially freezing the bath/front, or claiming rank alone gives robust memory.

Archive/commit evidence only; do not modify CURRENT_THEORY.md.
