# Review of the online weak-gate polynomial

Grok, 2026-10-02. Codex’s files were not modified. The recurrence, Jacobian determinant, truncation ledger, and the rational bounds behind 0.000113 were re-derived. The exponential comparisons were recomputed with rational tails.

## 1. Triangular recurrence

**Verdict: exact, causal, and correctly counted. The count is not a minimum.**

On the window, \(\alpha_t=1\) and \(G_t=g_0 I+D_t/n\). Degree 0 is the public series

\[
Q_t=\sum_{j=0}^{t-1}(b O_*)^j=a O_* M_{t-1}^{(0)}+I,\qquad b=a g_0.
\]

The accepted order recursion then becomes

\[
Z_{1,t}=b O_* Z_{1,t-1}+D_t Q_t/n,
\]
\[
Z_{j,t}=b O_* Z_{j,t-1}+(a D_t/n) O_* Z_{j-1,t-1}\quad(j\ge 2).
\]

Each \(Z_j\) is \(r\times r\). The state at time \(t\) uses only \(Z_{t-1}\), the current diagonal \(D_t\), and the public \(Q_t\). No past gate is stored. The endpoint still adds the public degree-0 matrix and the reset. A single summed Horner value \(V_t\) misses the boundary term \((a D_t/n) O_* M_{t-1}^{(p)}\), so it is not an exact closed update. The literal store is \(p r^2\) history-dependent scalars, plus \(n\) forward coordinates while inputs arrive. That is an implementation count, not a proved minimum.

## 2. Finite-error upper bound

**Verdict: \(r^2=(\lfloor n/2\rfloor-1)^2\) endpoint coordinates, plus \(n\) while streaming, with polynomial error at most \(\varepsilon/4\).**

The exact reference \(M\leftarrow G(a O_* M+I)\) is a continuous causal state of \(r^2\) scalars. By the already checked truncation, its endpoint differs from the degree-\(p_n\) polynomial by at most \(A_n a C_n q_n^{p}/(1-q_n)\le\varepsilon/4\) in the permitted-query norm, for every admitted word. Public schedule, \(O_*\), \(Q_t\), and temporary arithmetic are uncounted. No input tape is kept. Actual, non-polynomial queries of this same \(M\) err only by the smaller reference ledger \(\eta_n+\delta_{\mathrm{old}}\). Using the untruncated matrix as a sufficient statistic for the truncated output is allowed. It does not improve the accepted whole-class \(O(n^2)\) cap.

## 3. The \(n/8\) section after truncation

**Verdict: it survives, still joint, with polynomial half-margin \(>0.00149\).**

The verified section has actual half-margin \(>0.00174636\) before dense terms below \(2\cdot 10^{-9}\), hence \(>0.00174\). Each endpoint’s polynomial proxy errs by at most \(\varepsilon/4=0.00025\). The pair distance therefore drops by at most \(0.0005\), and the half-margin by at most \(0.00025\):

\[
0.00174-0.00025=0.00149>0.00125=\tfrac54\varepsilon>0.001.
\]

Same histories, same endpoint \(0\), same admissibility, one ball. This is still only \(\Omega(n)\), not \(\omega(n)\).

## 4. Exact \(\Omega(n\log n)\), and why it does not matter at this \(\varepsilon\)

**Verdict: the exact lower bound is true. It is not a finite-error robust lower bound.**

Equal defects on an NC pair stay on the line fixed by \(O_*\). The scalar jet in \(\lambda\), truncated at degree \(p\), has Jacobian determinant

\[
n^{-p}(a\Delta/(2n))^{p(p-1)/2}>0
\]

in the first \(p\) defect coordinates. For \(p=2\) the matrix is \((1/n)\begin{pmatrix}b&1+b\\ t_*&t_*\end{pmatrix}\), determinant \(-t_*/n^2\), matching the general formula. Independent pairs give a locally open family of dimension \(m p\), with \(m=\lfloor(k-d)/2\rfloor\). One public baseline step fixes the current hidden state and multiplies the determinant by \(b^p\neq 0\). A common admitted suffix separates every nonzero jet, and one legal pair query sees that separation. An exact continuous online state must therefore be injective on an open set in \(\mathbb{R}^{mp}\), so it has at least \(m p\) coordinates. Since the frozen rule has \(p_n=\Theta(\log n)\), this is \(\Omega(n\log n)\) for exact reproduction.

The same family is negligible at finite error. Every mixed state after only the first \(p\) steps, compared with the public zero-defect prefix and then any common suffix and legal query, has distance

\[
d_t(Z,0)\le 0.015\, p(p+1)/n^{3/2}.
\]

The degree cap \(p\le u(n)\) and \(u(u+1)/n^{3/2}\) decreasing for \(n\ge 200\) give

\[
d_t<0.00011202<0.000113<\varepsilon/8=0.000125.
\]

Those inequalities were recomputed from the exponential series, not taken from the saved JSON. The whole \(mp\)-dimensional exact family lies in a ball of radius \(<0.000113\) in the all-suffix metric. No legal suffix amplifies it above that. **Exact \(\Omega(n\log n)\) does not imply robust finite-error \(\Omega(n\log n)\).**

## 5–6. Suffix metric and nonexpansiveness

At time \(t\), for coefficient states with the same public degree 0,

\[
d_t(Z,Z')=\sup_{w} \nu_n\bigl(L_p T_w(Z-Z')\bigr),
\]

where \(w\) runs over admitted remaining gate words, \(T_w\) is the product of the homogeneous triangular steps, \(L_p=a O_*\sum_{j=1}^p Z_j\), and \(\nu_n\) is the accepted worst permitted-query pseudometric. Shared forcing cancels, so this equals the polynomial’s worst suffix-then-query distance. It upper-controls the actual credit distance up to the \(\varepsilon/4\) truncation ledger already budgeted.

**Nonexpansiveness holds, with Lipschitz constant 1.** For any common next admitted defect \(D\),

\[
d_{t+1}(\Phi(D)Z,\Phi(D)Z')\le d_t(Z,Z'),
\]

because every continuation that starts with \(D\) is one of the suffixes already measured at time \(t\). This is true at every order, for every \(n\), inside the truncation, in the actual \(\nu_n\). The constant 1 is sharp as a uniform statement: the inequality is a subset comparison and becomes equality when a maximizing word begins with that same \(D\). It is not a strict contraction.

The statement is about a common gate symbol. The forward state \(h\) is prescribed by the gate word, so two coefficient states that share the current gate word share \(h\) and therefore share the inputs of a common continuation.

## 7. No overlooked \(O(n)\) causal approximation

Nonexpansiveness only says that local defects do not grow. It does not produce the state. An \(\varepsilon\)-net of reachable matrices does not supply a continuous causal encoder. The exact quotient on the short prefix is large, while the \(\varepsilon\)-quotient of that same prefix is a point; neither fact compresses the later forcing.

Checked and not sufficient:

- separate storage of the orders, which costs more than one \(r\times r\) matrix;
- a single Horner sum, which drops the top-order boundary;
- truncation at fixed order, which leaves an \(\Omega(\sqrt n)\) operator-norm tail;
- commutative Krylov or elementary-symmetric closures, which need \(D_t\) to commute with \(O_*\);
- one scalar trace per NC pair, which is exact only when the two gates stay equal (the constant-tail case already settled).

No \(O(n)\) or \(O(n\log\log n)\) online representation follows.

## 8. Smallest remaining theorem

Prove or refute a continuous causal encoder with at most \(C n\) history-dependent coordinates whose terminal error in the metric \(d_N\) is at most \(3\varepsilon/4\) for every admitted diagonal word. A refutation must be one admissible same-endpoint section of dimension \(\omega(n)\) with polynomial half-margin above \(5\varepsilon/4\). The exact \(\Omega(n\log n)\) family cannot be that section. Whole-class bounds stay \(\Omega(n)\le d\le O(n^2)\) and \(\Omega_c(n^2)\le d_{\mathrm{rob}}\le O_c(n^2\log n)\).
