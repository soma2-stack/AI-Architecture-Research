# Private-complement leverage: all-support claim refuted

Codex, 2026-10-05. Theory only.

## Verdict and precise scope

The proposed bound
\[
\Lambda_\perp(t,S)\le C\sqrt{|S|/n}+\text{dense error}
\]
is **REFUTED as quantified here over every ordinary physical support S**.
A one-step legal query places an order-one adjoint entry on the exceptional
terminal-cycle coordinate; one backward cycle step carries that entry to its
adjacent ordinary coordinate \(d-2\), which lies in \(\mathcal U_t^\perp\).
For \(S=\{d-2\}\), \(\Lambda_\perp>0.64\) for all \(n\ge10^6\), up to a
negligible accepted dense correction. Hence
\[
\Lambda_\perp/\sqrt{|S|/n}>0.64\sqrt n\longrightarrow\infty.
\]

This does not refute the accepted leverage bound on its actual scope: the
changed-gate supports in the corridor are placed far from the terminal row,
and the accepted first-departure proof follows those far ordinary
characteristics. The counterexample support \(d-2\) is not one of those
changed-gate supports. Therefore this result gives no unconditional
long-corridor packing theorem and does not close the narrower packing
question for actual corridor gate supports.

## Exact complement recurrence

Let \(\mathcal U_s\) be the accepted direct sum of tuple-wise zero-sum
subspaces at time \(s\), \(P_s\) its orthogonal projector, and
\(Q_s=I-P_s\). Write \(p_s^U=P_sp_s\) and \(p_s^\perp=Q_sp_s\).
For the reference recurrence \(R_0=aO_*\), the midpoint tuple gates are
constant on each four-site tuple, so both \(\mathcal U_s\) and its
orthogonal complement reduce the chronological operator. The complete
complement recurrence is
\[
p_{s-1}^\perp=aO_*^T\bar G_sp_s^\perp
=aC^T\bar G_sp_s^\perp
 +a u\,\alpha_s+a v_H\,\beta_s,                         \tag{1}
\]
where
\[
\alpha_s=\mathbf1^T\bar G_sp_s^\perp,\qquad
\beta_s=e_1^T\bar G_sp_s^\perp.
\]
This includes every uniform Householder renewal and every exceptional-front
renewal. Tuple-common amplitudes, the bath, and the terminal/front rows all
remain in \(p_s^\perp\). The recurrence is not a closed two-scalar model:
\(C^T\bar G_s p_s^\perp\) is still a full vector, and legal tuple gates may
vary by tuple.

For the actual dense map \(R=R_0+E\), the projected recurrence is exactly
\[
p_{s-1}^\perp
=aO_*^T\bar G_sp_s^\perp+
 Q_{s-1}E^T\bar G_s(p_s^\perp+p_s^U).                    \tag{2}
\]
The second term is retained; it couples the two reference sectors. The
accepted bound is \(\|E\|_{\rm op}\le e_R=4\cdot10^{-8}n^{-2}\).
A length-v product comparison costs at most \(v e_R\), and the accepted
future-query adjoint comparison costs at most \(7e_R\).

The smallest exact state established for (1) remains the whole
\((r-3m)\)-dimensional complement vector, with two scalar feedback
functionals per step. No lower-dimensional closed aggregate system is
proved. Dissipation gives \(\|p_t\|\le a^v\|c_Q\|\), but cannot rule out
concentration on a coordinate: the counterexample below uses only one
backward step.

## Legal one-step counterexample

Use any admissible corridor with \(m=1,T=1\), the accepted inverse lift and
common public reset. Its moving tuples are far from \(d-2\): the prescribed
no-wrap geometry places all tuple tracks at coordinates bounded away from
the terminal end, and the compensators are off-cycle. Thus
\(e_{d-2}\perp\mathcal U_{N-1}\), and \(S=\{d-2\}\) is an ordinary
one-coordinate support in the private complement.

Choose the legal one-step future query with every future preactivation
equal to \(0.25\). Its gate vector is \(g_{\rm hi}\mathbf1\), where
\(g_{\rm hi}=\sech^2(.25)\). In the reference model the accepted exact query
formula gives
\[
c_Q^0=\frac{a}{\sqrt n}O_*^T(g_{\rm hi}\mathbf1),\qquad
(c_Q^0)_{d-1}
=\frac{a g_{\rm hi}}{\sqrt n}(\sqrt k+1-\gamma)>.66
\quad(n\ge10^6).                                          \tag{3}
\]
This query is legal under the future preactivation box and frozen-input
contract. The reset endpoint is common, so the same query applies to every
history in the corridor family.

At the reset, coordinate \(d-1\) is an ordinary public row with gate
\(q_N=1-u_N^2>.99\), using the accepted \(|u_N|<.1\) reset bound. Let
\(x=\bar G_Nc_Q^0\). The one-step past adjoint is \(p_{N-1}^0=aO_*^Tx\).
Since \(d-2\) is a regular cycle row,
\[
(p_{N-1}^0)_{d-2}
=a\left[
x_{d-1}-\frac{\gamma^2}{k}\mathbf1^Tx
+\frac{\gamma}{\sqrt k}x_1
\right].                                                   \tag{4}
\]
The leading term obeys \(x_{d-1}=q_N(c_Q^0)_{d-1}>.99\cdot.66\).
Also \(\|x\|_2\le q_f<1\), \(k=\lfloor n/2\rfloor\), and
\(\gamma<1.002\) for \(n\ge10^6\), so
\[
\frac{\gamma^2}{k}|\mathbf1^Tx|
+\frac{\gamma}{\sqrt k}|x_1|
\le\frac{3}{\sqrt n}.
\]
It follows from (4) that \(|(p_{N-1}^0)_{d-2}|>0.649\) for
\(n\ge10^6\).

For the actual dense model, the past one-step operator changes by at most
\(e_R\), and the accepted same-query future-adjoint comparison is at most
\(7e_R\). Their combined coordinate error is below \(8e_R\). Therefore,
conservatively,
\[
\|P_{\{d-2\}}\Pi_{\mathcal U_{N-1}^\perp}p_{N-1}\|_2>.64
\quad(n\ge10^6).                                          \tag{5}
\]
The query supremum includes this legal query, so (5) is a lower bound on
\(\Lambda_\perp(N-1,\{d-2\})\), not an RMS or sampled estimate. Since
\(|S|=1\), the ratio to \(\sqrt{|S|/n}\) grows at least as
\(.64\sqrt n\).

This example needs neither accumulation of repeated renewals nor an
energy argument. It is the terminal-cycle spike transported once by the
chronological adjoint. The rank-two terms in (4) are explicitly retained
and are only \(O(n^{-1/2})\) at this coordinate.

## Packing consequence and remaining narrow question

No support-only upper bound of the requested form can hold for all physical
ordinary supports. Thus any use of such a bound must state a geometric
restriction excluding terminal-adjacent supports and prove that every
support in its application satisfies that restriction.

The packing repair's conditional scalar/localized theorem remains
conditional; this counterexample neither supplies its missing premises nor
refutes them. For the actual changed-gate corridor supports, the existing
age-weighted leverage estimate remains the valid bound. It still has an age
factor and yields no unconditional continuous-dimension or packet-count
restriction for long histories.

Accordingly, the universal support-only route is refuted, but the
corridor-restricted packing route remains unresolved rather than closed.
The next precise packing question, if pursued, is whether
\(\|P_{S_t}p_t^\perp\|\le C\sqrt{|S_t|/n}\) holds when \(S_t\) is restricted
to the actual moving corridor gate support and its no-wrap geometry.

No numerical tests were run. No CPU or GPU computation was used.
