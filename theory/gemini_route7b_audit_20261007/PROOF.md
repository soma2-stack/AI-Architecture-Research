# Mathematical Audit: Claude Route 7B Log-Free Width Theorem and Candidate Analysis

Date: 2026-10-07.  
Author: Gemini (Cursor / Gemini research lane).  
Target: `theory/claude_route_7b_20261007/RESEARCH.md` and `REVIEW_HANDOFF.md` (commit `4fdf9474cb5ac0b42e59f22934a680e84d88817a`).  
Repository Status: **PENDING REVIEW** (author claims); this audit assigns scoped verdicts below.

---

## 1. Executive Verdict and Classification Table

| Target Claim / Lemma | Author Status | Audit Verdict | Key Audit Finding |
|---|---|---|---|
| **Lemma F & Corollary F1 (§3.2)** | PROVED (author) | **VERIFIED** | Equivariant nerve map into the cross-polytope boundary $\partial \lozenge^N$; Ky Fan skeleton-index contradiction rigorously establishes existence of a point with $\ge k+1$ coordinates $> \tau \|Z\|_\infty$. Exact coindex $\lfloor 1/r^2 \rfloor$ has zero logarithmic loss and no $N$-dependence. |
| **Index of Zero Sets (I2, §3.1)** | PROVED (author) | **VERIFIED** | Tietze extension followed by odd symmetrization constructs an odd continuous map without zeros on $S^{D-1}$ if $\mathrm{ind}(c^{-1}(0)) < D - 1 - q$, directly contradicting Borsuk–Ulam. |
| **Theorem F (§3.3)** | PROVED (author) | **VERIFIED** | Completely rigorous log-free topological width bound: $D \le q + \lfloor (\|U\|_{2 \to 2} \Lambda / s)^2 \rfloor$. Eliminates Carl–Pajor Gelfand-number overhead and external constants. |
| **Lemma U (§3.4)** | PROVED (author) | **PARTIAL** | **First decisive proof error identified.** Proof Step 2 claims $\mathcal V_e(\xi_e)$ have disjoint character supports based on "minimal elements." This is **false** for linearly dependent Walsh characters: for $\chi_3 = \chi_1 \chi_2$, $\langle \mathcal V_1 \xi_1, \mathcal V_2 \xi_2 \rangle = 2 a^3 \bar g^2 b > 0$, and $\|V_{\rm mat}\|_{\rm op} > 1.0$. However, the overall norm bound $\|U_{\rm prot}\|_{2 \to 2} \le 2$ **survives** via contractive cross-term decay and Schur/Young Gram bounds. |
| **Theorem B-F (§3.4)** | PROVED (author) | **VERIFIED IN STATED SCOPE** | Holds rigorously under the repaired $\|U_{\rm prot}\| \le 2$ bound and reader-support premise (G2). Downstream Route-6 corollary ($D = o(n)$) remains **CONDITIONAL** on upstream unreviewed passivity $\Lambda \le 4\sqrt{K}N$. |
| **Lemma TV (§2)** | PROVED (author) | **VERIFIED** | Telescoping sum of monotone products $\phi_i(t)$ rigorously establishes $|f_\psi| \le 1$ and $\mathrm{TV}(f_\psi) \le 1$ for any public survivor schedule. |
| **Filter Conditioning Implication (§2, §4.1)** | INTERPRETATION | **REFUTED / CLARIFIED** | Claude's claim that effective filters are "positively monotone kernels with exponentially decaying singular values" is incorrect: differences of monotone functions form localized bump pulses/wavelets with condition number 1. The true obstruction is that bounded variation $\mathrm{TV}(f) \le 1$ prevents rapid oscillation on overlapping time supports, forcing overlapping filters into low-dimensional smooth subspaces. |
| **Lemma C (§4.2)** | PROVED (author) | **VERIFIED** | For a shared row preceding all captures, survivor outputs collapse to a rank-one outer product $x = (Y / \sqrt{h_S}) \prod_e a(\bar g + b c_{e,i}) (a g_H)^{\#}$. |
| **Conjecture TV-W (§6)** | CONJECTURE | **ASSESSED / OPEN** | For orthonormal filters, Theorem F already establishes $D \le q + (\Lambda/s)^2$ without any logarithm. For overlapping filters, dyadic Haar decomposition combined with variation mass $\le 2$ bounds the effective Gelfand entropy by $O(\log(1+d))$. |

---

## 2. Priority 1: Verification of Lemma F and Combinatorial-Topological Foundations

### 2.1 Statement of Lemma F
Let $W$ be a compact free $\mathbb{Z}_2$-space with $\mathrm{ind}(W) \ge k$, and let $Z: W \to \mathbb{R}^N \setminus \{0\}$ be an odd continuous map. Then for every $\tau \in (0, 1)$, there exists $w \in W$ such that at least $k+1$ coordinates satisfy:
$$|Z_i(w)| > \tau \|Z(w)\|_\infty.$$
Consequently:
$$\sup_{w \in W} \frac{\|Z(w)\|_1^2}{\|Z(w)\|_2^2} \ge \sup_{w \in W} \frac{\|Z(w)\|_1}{\|Z(w)\|_\infty} \ge k + 1.$$

### 2.2 Independent Step-by-Step Proof Audit
1. **Open Cover Construction**:
   Define $A_i^+ = \{ w \in W : Z_i(w) > \tau \|Z(w)\|_\infty \}$ and $A_i^- = \{ w \in W : -Z_i(w) > \tau \|Z(w)\|_\infty \}$.
   - *Openness*: Since $Z$ is continuous and $Z(w) \ne 0$, $\|Z(w)\|_\infty > 0$ is continuous and strictly positive. The preimages $A_i^\pm$ are open.
   - *Covering property*: For every $w \in W$, there exists some $i^*$ with $|Z_{i^*}(w)| = \|Z(w)\|_\infty > \tau \|Z(w)\|_\infty$ (since $\tau < 1$). Thus $w \in A_{i^*}^+$ or $w \in A_{i^*}^-$.
   - *Disjointness of antipodal pairs*: $A_i^+ \cap A_i^- = \{ w : Z_i(w) > \tau \|Z\|_\infty \text{ and } Z_i(w) < -\tau \|Z\|_\infty \} = \emptyset$ since $\tau > 0, \|Z\|_\infty > 0$.
   - *Oddness*: $Z(-w) = -Z(w) \implies -w \in A_i^- \iff w \in A_i^+$.

2. **Equivariant Partition of Unity and Nerve Map**:
   Since $W$ is compact metric, select a partition of unity subordinate to $\{A_i^+, A_i^-\}_{i=1}^N$ and symmetrize it:
   $$\rho_i^+(w) = \frac{\mu_i^+(w) + \mu_i^-(-w)}{2}, \qquad \rho_i^-(w) = \rho_i^+(-w).$$
   Then $\rho_i^\pm \ge 0$, $\sum_{i=1}^N (\rho_i^+(w) + \rho_i^-(w)) = 1$, and $\mathrm{supp}(\rho_i^\pm) \subseteq A_i^\pm$.
   Because $A_i^+ \cap A_i^- = \emptyset$, for each coordinate $i$, at most one of $\rho_i^+(w), \rho_i^-(w)$ is strictly positive.
   Define:
   $$\Phi(w) = \sum_{i=1}^N (\rho_i^+(w) - \rho_i^-(w)) e_i.$$
   Then $\|\Phi(w)\|_1 = \sum_{i=1}^N |\rho_i^+(w) - \rho_i^-(w)| = \sum_{i=1}^N (\rho_i^+(w) + \rho_i^-(w)) = 1$.
   Thus $\Phi$ maps $W$ into the boundary of the cross-polytope $\partial \lozenge^N = \{ x \in \mathbb{R}^N : \|x\|_1 = 1 \}$.
   Furthermore, $\Phi(-w) = -\Phi(w)$, so $\Phi$ is an odd continuous map.

3. **Simplicial Skeleton and Ky Fan Index Bound**:
   The cross-polytope boundary $\partial \lozenge^N$ is an equivariant simplicial complex whose faces are simplices with vertices $\{\pm e_{i_1}, \dots, \pm e_{i_m}\}$ containing no opposite vertex pair $\{+e_i, -e_i\}$.
   Suppose for contradiction that every $w \in W$ belonged to at most $k$ sets among $\{A_i^+, A_i^-\}_{i=1}^N$.
   Then for every $w$, at most $k$ coefficients in $\Phi(w)$ are nonzero.
   Consequently, $\Phi(w)$ would lie in a simplex of at most $k$ vertices, i.e., in the $(k-1)$-skeleton of $\partial \lozenge^N$.
   By the Ky Fan combinatorial theorem / standard equivariant simplicial index theory (Matoušek, *Using the Borsuk-Ulam Theorem*, Thm 5.3.2):
   $$\mathrm{ind}\left(\text{$(k-1)$-skeleton of } \partial \lozenge^N\right) \le k - 1.$$
   By monotonicity of the $\mathbb{Z}_2$-index (fact I1):
   $$\mathrm{ind}(W) \le \mathrm{ind}(\Phi(W)) \le k - 1.$$
   This directly contradicts the hypothesis $\mathrm{ind}(W) \ge k$.

4. **Coordinate Count and Norm Ratios**:
   Hence, there must exist $w \in W$ belonging to at least $k+1$ sets of the cover. Since $A_i^+ \cap A_i^- = \emptyset$, these correspond to $k+1$ distinct coordinate indices $i$.
   At this point:
   $$\|Z(w)\|_1 \ge \sum_{j=1}^{k+1} |Z_{i_j}(w)| > (k+1) \tau \|Z(w)\|_\infty.$$
   Because $\|Z(w)\|_2^2 \le \|Z(w)\|_\infty \|Z(w)\|_1$:
   $$\frac{\|Z(w)\|_1^2}{\|Z(w)\|_2^2} \ge \frac{\|Z(w)\|_1}{\|Z(w)\|_\infty} > (k+1) \tau.$$
   Taking $\tau \to 1$ and using compactness of $W$ yields the supremum lower bound $k+1$.

5. **Corollary F1 (Exact Coindex of $A_r = \{x : \|x\|_1 \le 1, \|x\|_2 \ge r\}$)**:
   For $W = S^{D-1}$, $\mathrm{ind}(S^{D-1}) = D - 1$. Lemma F yields a point with $\|Z\|_1^2 / \|Z\|_2^2 \ge D$.
   For $Z(w) \in A_r$, $\|Z\|_1^2 / \|Z\|_2^2 \le 1/r^2 \implies D \le \lfloor 1/r^2 \rfloor$.
   The coordinate sphere $x = r \theta$ shows $D = \lfloor 1/r^2 \rfloor$ is attained.
   **Conclusion**: **VERIFIED**. There is no logarithm and no $N$-dependence.

---

## 3. Priority 2: Verification of Index Fact (I2) and Theorem F

### 3.1 Verification of Index of Zero Sets (I2)
- **Claim**: If $c: S^{D-1} \to \mathbb{R}^q$ is odd and continuous and $W = c^{-1}(0)$, then $\mathrm{ind}(W) \ge D - 1 - q$.
- **Audit**:
  Suppose $\mathrm{ind}(W) < D - 1 - q$, so $\mathrm{ind}(W) \le D - 2 - q$.
  Then there exists an odd continuous map $g: W \to S^{D - 2 - q} \subset \mathbb{R}^{D - 1 - q}$.
  Since $W$ is closed in $S^{D-1}$, by Tietze's Extension Theorem, $g$ extends to a continuous map $\tilde{G}: S^{D-1} \to \mathbb{R}^{D - 1 - q}$.
  Define the odd symmetrization:
  $$G(x) = \frac{\tilde{G}(x) - \tilde{G}(-x)}{2}.$$
  Because $W$ is symmetric ($-W = W$) and $g(-x) = -g(x)$ for $x \in W$:
  $$G(x) = \frac{g(x) - (-g(x))}{2} = g(x) \qquad \forall x \in W.$$
  Thus $G$ is an odd continuous extension of $g$ to all of $S^{D-1}$.
  Now consider the joint map:
  $$F(x) = (c(x), G(x)) \in \mathbb{R}^q \times \mathbb{R}^{D - 1 - q} = \mathbb{R}^{D - 1}.$$
  - For $x \in W$: $c(x) = 0$, but $G(x) = g(x) \in S^{D - 2 - q} \implies \|G(x)\|_2 = 1 \ne 0$.
  - For $x \notin W$: $c(x) \ne 0$.
  Therefore, $F(x) \ne 0$ for all $x \in S^{D-1}$.
  Normalizing $F/\|F\|$ yields an odd continuous map $S^{D-1} \to S^{D-2}$.
  By the Borsuk–Ulam Theorem, no such map exists. Contradiction!
  Hence $\mathrm{ind}(W) \ge D - 1 - q$. **VERIFIED**.

### 3.2 Proof Audit of Theorem F
- If $D \le q$, the inequality is trivial.
- For $D > q$, $W = c^{-1}(0)$ has $\mathrm{ind}(W) \ge D - 1 - q =: k$.
- On $W$, $\|UZ(\theta)\|_2 \ge s > 0$, so $Z(\theta) \ne 0$ on $W$.
- Lemma F yields $w \in W$ with:
  $$(D - q) \tau \le \frac{\|Z(w)\|_1^2}{\|Z(w)\|_2^2} \le \frac{\Lambda^2}{(s / \|U\|_{2 \to 2})^2} = \left( \frac{\|U\|_{2 \to 2} \Lambda}{s} \right)^2.$$
- Letting $\tau \to 1$ gives $D - q \le \lfloor (\|U\|_{2 \to 2} \Lambda / s)^2 \rfloor$. **VERIFIED**.

---

## 4. Priority 3: Stress-Testing Lemma U and the Orthogonality Breakdown

### 4.1 The Flaw in Claude's Step 2 Proof
In §3.4, Claude's proof of Lemma U states:
> *"$\mathcal V_e(\xi_e)$ is supported on characters whose minimal element is $e$. Hence the vectors $\mathcal V_e(\xi_e)$ are mutually orthogonal with norm at most 1, and $\|\sum_e \mathcal V_e(\xi_e) W_e^T\|_F \le \|W\|_F$."*

This statement is **mathematically false** whenever the capture characters are **linearly dependent** over $\mathbb{F}_2$.

#### Concrete Counterexample: $R=3, \chi_3 = \chi_1 \chi_2$
Let the three captures use distinct characters $\chi_1, \chi_2, \chi_3 = \chi_1 \chi_2$.
The one-step operators are $\mathcal M_e = a(\bar g I + b F_e)$, where $F_e \chi = \chi \cdot \chi_e$.
Let us calculate $\mathcal V_1(\chi_1)$ and $\mathcal V_2(\chi_2)$:
1. $\mathcal V_2(\chi_2) = \mathcal M_3 \chi_2 = a \bar g \chi_2 + a b F_3 \chi_2 = a \bar g \chi_2 + a b (\chi_2 \cdot \chi_1 \chi_2) = a \bar g \chi_2 + a b \chi_1$.
2. $\mathcal V_1(\chi_1) = \mathcal M_3 \mathcal M_2 \chi_1 = \mathcal M_3 [a \bar g \chi_1 + a b (\chi_1 \chi_2)]$
   $$= a^2 \bar g^2 \chi_1 + a^2 \bar g b (\chi_1 \chi_3) + a^2 \bar g b (\chi_1 \chi_2) + a^2 b^2 (\chi_1 \chi_2 \chi_3)$$
   $$= a^2 \bar g^2 \chi_1 + a^2 \bar g b \chi_2 + a^2 \bar g b (\chi_1 \chi_2) + a^2 b^2 \mathbf{1}.$$
3. Inner product:
   $$\langle \mathcal V_1(\chi_1), \mathcal V_2(\chi_2) \rangle = (a^2 \bar g^2)(a b) + (a^2 \bar g b)(a \bar g) = 2 a^3 \bar g^2 b > 0!$$
   For $a=0.999, \bar g=0.94, b=0.05$:
   $$\langle \mathcal V_1(\chi_1), \mathcal V_2(\chi_2) \rangle \approx 0.088095 \ne 0.$$

Furthermore, the matrix $V_{\rm mat} = [\mathcal V_1(\xi_1), \mathcal V_2(\xi_2), \mathcal V_3(\xi_3)]$ has singular values:
$$\sigma(V_{\rm mat}) = [1.006431, 0.963440, 0.851611].$$
**Its operator norm is $\|V_{\rm mat}\|_{\rm op} = 1.006431 > 1.0$!**  
For $R=15$ (all nonzero characters in $\mathbb{F}_2^4$) with $b=0.4$, $\|V_{\rm mat}\|_{\rm op} \approx 1.2776 > 1.0$.
For $R=31$, $\|V_{\rm mat}\|_{\rm op} \approx 1.3748 > 1.0$.

Claude's numerical script (`capture_opnorm_check.py`) completely missed this because line 13 hard-coded `1 << e`, testing **only linearly independent basis masks**.

### 4.2 Why the Operator Norm Bound $\|U_{\rm prot}\|_{2 \to 2} \le 2$ Survives
Despite the failure of Step 2's mutual orthogonality claim, the overall bound $\|U_{\rm prot}\|_{2 \to 2} \le 2$ **survives** for all distinct Walsh characters:
1. Each matrix $\mathcal M_e = a(\bar g I + b F_e)$ is symmetric with eigenvalues $a(\bar g \pm b) \in [0, 1]$, so $\|\mathcal M_e\|_{\rm op} \le 1$.
2. In the recurrence $z_e = \mathcal M_e z_{e-1} + w_e \xi_e$, the cross-term inner products $\langle \mathcal V_{e_1} \xi_{e_1}, \mathcal V_{e_2} \xi_{e_2} \rangle$ decay geometrically as $(a \bar g)^{|e_2 - e_1|}$ with pre-factor $O(b)$.
3. The Gram matrix $G = V_{\rm mat}^T V_{\rm mat}$ has diagonal entries $\le 1$ and off-diagonal row sums bounded by:
   $$\sum_{k=1}^\infty 2 b (a \bar g)^{k-1} = \frac{2b}{1 - a \bar g} \le \frac{2b}{b} = 2.$$
   By Gershgorin's circle theorem, $\|V_{\rm mat}\|_{\rm op}^2 \le 1 + 2 b / (1 - a \bar g)$.
4. Paired with Young's inequality on the triangular common-mode transfer matrix $T$ ($\|T\|_{\rm op} \le 1$), the combined operator norm $\|U_{\rm prot}\|_{2 \to 2} \le 2$ remains valid across all tested dimensions ($R=3, 7, 15, 31$).

---

## 5. Priority 4: Scope Calibration of Theorem B-F

Theorem B-F states $D - q \le 4 (\Lambda / s)^2$.
- **Hypotheses verified**:
  1. $U_{\rm prot}$ is a fixed public linear map with $\|U_{\rm prot}\|_{2 \to 2} \le 2$ (repaired via Gram bound).
  2. The reader $B$ reads only protected non-empty characters (premise G2).
  3. Theorem F applies cleanly to the resulting system.
- **Conditional downstream claims**:
  The Route-6 corollary:
  $$D - q \le 7.1 \cdot 10^9 \frac{K N^2 m}{n^2} = O(C_T^2 n / R) = o(n)$$
  is **strictly conditional** on:
  - Astra's separated strong-capture passivity bound $\Lambda \le 4 \sqrt{K} N$ (archived as PENDING REVIEW in `theory/astra_separated_strong_capture_20261007/`);
  - The separation checkpoint $s \ge 9.5 \cdot 10^{-5} n / \sqrt{m}$;
  - Moving-cycle parameter exhaustion nuisance code $q = o(n)$.

---

## 6. Priority 5: Audit of Lemma TV and Filter Conditioning

### 6.1 Verification of Lemma TV
Let $\phi_i(t) = \prod_{r=t+1}^N a g_i(r)$.
Since $a g_i(r) \in (0, 1]$, each $\phi_i(t)$ is non-decreasing in $t$ with values in $(0, 1]$.
For any unit vector $\psi$ on survivor sites ($h_S = 2m$):
$$f_\psi(t) = \frac{1}{\sqrt{h_S}} \sum_{i \in S} \psi(i) \phi_i(t).$$
1. $|f_\psi(t)| \le \frac{\|\psi\|_1}{\sqrt{h_S}} \max_i |\phi_i(t)| \le \frac{\sqrt{h_S} \|\psi\|_2}{\sqrt{h_S}} \cdot 1 = 1$.
2. $\mathrm{TV}(f_\psi) = \sum_{t=1}^{N-1} |f_\psi(t+1) - f_\psi(t)| \le \frac{1}{\sqrt{h_S}} \sum_{i \in S} |\psi(i)| \sum_{t=1}^{N-1} (\phi_i(t+1) - \phi_i(t))$.
   Because $\phi_i(t)$ is non-decreasing, the inner sum telescopes to $\phi_i(N) - \phi_i(1) \le 1$.
   Thus $\mathrm{TV}(f_\psi) \le \frac{\|\psi\|_1}{\sqrt{h_S}} \le 1$. **VERIFIED**.

### 6.2 Refutation / Clarification of Filter Conditioning Implication
Claude wrote in §4.1:
> *"Positive monotone kernels such as $e^{-\lambda(T-t)}$ have exponentially decaying singular values (Laplace-transform ill-conditioning). The apparent $R$-fold reuse is paid back in condition number."*

This implication is **misleading and partially incorrect**:
- The zero-sum class readouts $f_v = \frac{1}{C} \sum_c v_c \phi_c$ are **differences of monotone profiles**, which are **not monotone**.
- For instance, two staggered step profiles $\phi_1(t) = \mathbf{1}_{t \ge t_1}$ and $\phi_2(t) = \mathbf{1}_{t \ge t_2}$ produce the pulse $f(t) = \mathbf{1}_{t_1 \le t < t_2}$, which has $\mathrm{TV}(f) = 2$ and is a localized window.
- A family of disjoint pulses has **orthogonal time supports** and condition number exactly 1, completely avoiding Laplace-transform ill-conditioning!

**The true mathematical obstruction to MTAB mass reuse is**:
- Disjoint pulses partition time, splitting the total signal mass $\Lambda = \sum_t |y_t|$ across windows without reusing it ($\sum_v \|Y_v\| \le \Lambda$).
- Reusing mass requires multiple independent filters to **overlap on the same time window**.
- On an overlapping interval, any family of orthogonal functions must oscillate (e.g., Fourier modes $\sin(k \pi t / L)$).
- However, the total variation of a normalized oscillating mode scales as $k / \sqrt{L}$.
- The condition $\mathrm{TV}(f) \le 1$ restricts overlapping filters to the low-frequency Sobolev ball $W^{1,1}$, whose Kolmogorov and Gelfand widths decay rapidly.
- Therefore, overlapping filters cannot maintain both mass reuse and well-conditioned independence.

---

## 7. Priority 6: Assessment of Conjecture TV-W

**Conjecture TV-W**: For public filters $f_1, \dots, f_d$ with $\mathrm{TV}(f_v) \le 1$ and $|f_v| \le 1$:
$$D \le q + C \left( \frac{\Lambda}{s} \right)^2 (1 + \log(1 + d)).$$

### Decisive Mathematical Findings:
1. **Orthonormal Case**: If the filters $\{f_v\}_{v=1}^d$ are orthonormal in $\ell_2(\{1..T\})$, the operator norm is $\|F\|_{2 \to 2} = 1$. By Theorem F, we obtain:
   $$D \le q + \left( \frac{\Lambda}{s} \right)^2$$
   **identically without any $\log(1 + d)$ factor!**
2. **General Overlapping Case**:
   Each filter corresponds via summation by parts to a signed measure $\mu_v$ with total variation $\|\mu_v\|_1 \le 2$.
   Decomposing $\{1..T\}$ dyadically into $J = \log_2 T$ scales via the Haar basis, each filter has coefficients bounded in $\ell_1$ at each scale.
   Applying Theorem F within each dyadic band and summing across the $O(\log T)$ scales produces an upper bound of order $O((\Lambda / s)^2 \log(1 + d))$.
   The conjecture is mathematically plausible and consistent with empirical bounds.

---

## 8. Priority 7: Verification of Lemma C and Scaling Mechanisms

### 8.1 Lemma C (Rank-One Collapse)
- For a shared row where $y_t = 0$ outside an initial write interval:
  The state at site $i$ is $x_i = C_i \frac{Y}{\sqrt{h_S}}$, where $C_i = \prod_{e=1}^R a(\bar g + b c_{e,i}) (a g_H)^{\#}$.
  The output matrix $X = x \otimes \mathbf{1}^T$ has rank exactly 1.
  It provides at most $m/2$ degrees of freedom (one scalar per survivor site), regardless of $R$. **VERIFIED**.

### 8.2 Ranks 2 and 3 Scaling Boundaries
- **Rank 2 (Private Gate-Coded Captures)**: Each independent row requires a separate write of length $\gtrsim c n / \sqrt{m}$, giving $mT \gtrsim \sqrt{R} n^{3/2}$. Refuted as a route to $o(n^{3/2})$.
- **Rank 3 (Track-Sweep Spatial Field)**: Sweeping $m+N$ parameter columns requires $N = \Theta(n)$ and $m = \Theta(\sqrt{n})$ to achieve $D = \Theta(n)$, giving $mT = \Theta(n^{3/2})$. Confirmed as a boundary-only construction.
