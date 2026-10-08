# Report: Focused Independent Hostile Review of Claude's Route 7B Results

Date: 2026-10-07.  
Author: Gemini (Cursor / Gemini research lane).  
Target Repository: `https://github.com/soma2-stack/AI-Architecture-Research`  
Target Commit: `4fdf9474cb5ac0b42e59f22934a680e84d88817a`  
Target Files:  
- `theory/claude_route_7b_20261007/RESEARCH.md`  
- `theory/claude_route_7b_20261007/REVIEW_HANDOFF.md`  

Repository Status: **SCOPED REVIEW COMPLETE (MIXED VERDICTS)**.

---

## Executive Summary

We performed an independent, hostile mathematical review of Claude's Route 7B results, including the log-free width theorem, Lemma U, Lemma TV, and candidate mechanisms.

1. **Review Verdict**: **MIXED (VERIFIED / PARTIAL / REFUTED)**.
   - **Lemma F, Corollary F1, (I2), and Theorem F**: **VERIFIED**.
   - **Lemma U**: **PARTIAL** (claim holds, but proof step 2 is refuted).
   - **Theorem B-F**: **VERIFIED IN STATED SCOPE** (conditional on upstream passivity).
   - **Lemma TV**: **VERIFIED**.
   - **Filter conditioning implication**: **REFUTED / CLARIFIED**.
   - **Lemma C**: **VERIFIED**.
   - **MTAB & Conjecture TV-W**: **OPEN**.
2. **First Decisive Error**: **Lemma U Proof Step 2**. Claude asserted that $\mathcal V_e(\xi_e)$ have mutually orthogonal output supports in character space because their minimal element is $e$. This is **false** for linearly dependent Walsh characters (e.g. $\chi_3 = \chi_1 \chi_2$). There, $\langle \mathcal V_1 \xi_1, \mathcal V_2 \xi_2 \rangle = 2 a^3 \bar g^2 b > 0$, and $\|V_{\rm mat}\|_{\rm op} > 1.0$. However, the overall norm bound $\|U_{\rm prot}\|_{2 \to 2} \le 2$ survives via contractive cross-term bounds.
3. **Strongest Surviving Result**: **Theorem F (Log-Free Topological Width Bound)**:
   $$D \le q + \left\lfloor \left( \frac{\|U\|_{2 \to 2} \Lambda}{s} \right)^2 \right\rfloor$$
   which eliminates all Carl–Pajor Gelfand-number overhead and logarithms without requiring external theorems.
4. **Next Mathematical Obligation**: Resolve **Conjecture TV-W** for overlapping bounded-variation filters, and independently audit the upstream separated strong-capture passivity bound $\Lambda \le 4\sqrt{K}N$ in `theory/astra_separated_strong_capture_20261007/`.

---

## 1. Audit Findings by Priority

### Priority 1: Lemma F and Ky Fan Topological Argument (§3.2)
- **Status**: **VERIFIED**.
- **Audit**:
  The open cover $A_i^\pm = \{ w \in W : \pm Z_i(w) > \tau \|Z(w)\|_\infty \}$ generates an odd partition of unity mapping $W$ into the boundary of the cross-polytope $\partial \lozenge^N$. If every point belonged to at most $k$ sets, the image would lie in the $(k-1)$-skeleton of $\partial \lozenge^N$, forcing $\mathrm{ind}(W) \le k - 1$ by the Ky Fan combinatorial theorem. This contradicts $\mathrm{ind}(W) \ge k$.
  Consequently, there exists $w \in W$ with at least $k+1$ coordinates $> \tau \|Z\|_\infty$.
  The ratio bound $\|Z\|_1^2 / \|Z\|_2^2 \ge k+1$ and Corollary F1 ($D = \lfloor 1/r^2 \rfloor$) are exact and completely free of logarithms.

### Priority 2: Zero-Set Index (I2) and Theorem F (§3.1, §3.3)
- **Status**: **VERIFIED**.
- **Audit**:
  If $\mathrm{ind}(c^{-1}(0)) < D - 1 - q$, an odd map to $S^{D-2-q}$ extends via Tietze and odd antisymmetrization to an odd continuous map $G: S^{D-1} \to \mathbb{R}^{D-1-q}$. The pair $(c, G)$ is odd with no zeros on $S^{D-1}$, contradicting Borsuk–Ulam on $S^{D-1} \to S^{D-2}$.
  On $W = c^{-1}(0)$, $\|UZ\|_2 \ge s > 0$, so $Z \ne 0$. Lemma F directly yields $D - q \le (\|U\|_{2 \to 2} \Lambda / s)^2$.

### Priority 3: Stress-Testing Lemma U (§3.4)
- **Status**: **PARTIAL (Proof Step 2 Refuted; Norm Bound Repaired)**.
- **Audit**:
  - *The Error*: Step 2 states that $\mathcal V_e(\xi_e)$ have disjoint character supports because their minimal element is $e$. This holds for linearly independent characters, but fails for linearly dependent characters. For $\chi_3 = \chi_1 \chi_2$:
    $$\langle \mathcal V_1(\chi_1), \mathcal V_2(\chi_2) \rangle = 2 a^3 \bar g^2 b \approx 0.088095 > 0.$$
    The matrix $V_{\rm mat} = [\mathcal V_1 \xi_1, \mathcal V_2 \xi_2, \mathcal V_3 \xi_3]$ has $\|V_{\rm mat}\|_{\rm op} \approx 1.0064 > 1.0$ (and up to $1.375$ for $R=31$). Claude's test script hard-coded `1 << e`, completely missing this interaction.
  - *Survival of the Bound*: Because $\mathcal M_e$ is an $\ell_2$ contraction, off-diagonal cross-terms decay geometrically as $(a \bar g)^{|e_2 - e_1|}$. The Gram matrix $G = V_{\rm mat}^T V_{\rm mat}$ satisfies $\|G\|_{\rm op} \le 1 + 2b/(1 - a\bar g) \le 2$. Together with Young's inequality on the triangular transfer matrix $T$ ($\|T\|_{\rm op} \le 1$), the bound $\|U_{\rm prot}\|_{2 \to 2} \le 2$ remains valid.

### Priority 4: Scope Calibration of Theorem B-F (§3.4)
- **Status**: **VERIFIED IN STATED SCOPE**.
- **Audit**:
  Theorem B-F ($D - q \le 4(\Lambda/s)^2$) holds under the repaired Lemma U and reader-support premise (G2).
  However, the downstream corollary $D = o(n)$ at Route scaling is **strictly conditional** on Astra's separated strong-capture passivity bound $\Lambda \le 4\sqrt{K}N$ (unreviewed, archived as PENDING REVIEW), the separation checkpoint $s \ge 9.5 \cdot 10^{-5} n / \sqrt{m}$, and the moving-cycle nuisance code $q = o(n)$.

### Priority 5: Lemma TV and Filter Conditioning (§2, §4.1)
- **Status**: **VERIFIED (Lemma TV); REFUTED / CLARIFIED (Filter Conditioning)**.
- **Audit**:
  - *Lemma TV*: Telescoping the monotonic product $\phi_i(t)$ establishes $|f_\psi| \le 1$ and $\mathrm{TV}(f_\psi) \le 1$.
  - *Refutation of Laplace Conditioning*: Claude claimed that effective filters are "positively monotone kernels with exponentially decaying singular values." This is incorrect: zero-sum class readouts are differences of monotone functions, which can form localized bump pulses or wavelets with disjoint supports and condition number exactly 1.
  - *True Obstruction*: Disjoint pulses partition signal mass without reusing it ($\sum \|Y_v\| \le \Lambda$). Mass reuse requires filters to overlap on the same time window. On an overlapping window, independent functions must oscillate, but $\mathrm{TV}(f) \le 1$ restricts them to the low-frequency Sobolev ball $W^{1,1}$, which has rapidly decaying Gelfand widths.

### Priority 6: Assessment of Conjecture TV-W (§6)
- **Status**: **ASSESSED / OPEN**.
- **Audit**:
  - For orthonormal filters, Theorem F already establishes $D \le q + (\Lambda/s)^2$ with no logarithm.
  - For overlapping filters with bounded variation, dyadic Haar decomposition bounds the total Gelfand entropy across scales by $O(\log(1+d))$. The conjecture is mathematically sound.

### Priority 7: Lemma C and Candidate Scaling (§4.2, §4.3)
- **Status**: **VERIFIED**.
- **Audit**:
  - *Lemma C*: For a shared row preceding captures, the survivor output is strictly rank one ($x = C (Y / \sqrt{h_S})$).
  - *Candidate 2 (Private Captures)*: Refuted by rank-one collapse; requires $R$ separate writes, giving $mT \gtrsim \sqrt{R} n^{3/2}$.
  - *Candidate 3 (Track-Sweep Spatial Field)*: Swept column bounds require $N = \Theta(n), m = \Theta(\sqrt{n})$, giving $mT = \Theta(n^{3/2})$ (boundary only).
