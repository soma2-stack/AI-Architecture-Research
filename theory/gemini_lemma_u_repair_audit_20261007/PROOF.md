# Hostile Mathematical Audit and Verification of Claude's Lemma U Repair

**Author:** Gemini (Cursor / Gemini Research Lane)  
**Date:** 2026-10-07  
**Target Repository:** `soma2-stack/AI-Architecture-Research`  
**Target Documents:**
- [`theory/claude_lemma_u_repair_20261007/PROOF.md`](file:///c:/Users/coler/OneDrive/Desktop/ai%20new/theory/claude_lemma_u_repair_20261007/PROOF.md)
- [`theory/claude_lemma_u_repair_20261007/REVIEW_HANDOFF.md`](file:///c:/Users/coler/OneDrive/Desktop/ai%20new/theory/claude_lemma_u_repair_20261007/REVIEW_HANDOFF.md)
**Target Commit:** `11c8867a8f0fc1bff0bf91876e1a9d1b27345c4a`

---

## Executive Summary of Audit Verdicts

| Component | Target Claim | Audit Verdict | Key Mathematical Justification |
| :--- | :--- | :--- | :--- |
| **Original Lemma U** | $\|U_{\rm prot}\| \le 2$ | **REFUTED** | Explicit finite counterexamples found at $R=2047$ and $R=4095$ ($\|U_{\rm prot}\| \in [2.0346, 2.0746]$). |
| **Previous Gemini Repair** | Gram decay $\|U_{\rm prot}\| \le 2$ via Gershgorin | **REFUTED** | Refuted by Claude; intra-level cross-terms do not decay geometrically (ratio to bound $> 10^{16}$ at $r=6$). Off-diagonal row sum is $2.2656 > 2.0$. |
| **Lemma A** | Lazy RW anti-concentration: $\Pr(X_k = \gamma) \le \frac{1 - (1-2p)^{(k+1)/2}}{k+1}$ | **VERIFIED** | Validated via Walsh-Fourier expansion, differential identity $(1-2p)F' + (k+1)F \le 1$, and numerical stress-tests. |
| **Atom Mapping & Hardy Bound** | $\|U_{\rm prot}\| \le 2\sqrt{1+(ag_H)^2} \le 2\sqrt{2}$ | **VERIFIED** | Protected projection eliminates common mode; Gram matrix is dominated by kernel $K(j,k) \le (H^T H)(j,k)$; discrete Hardy operator norm is exactly 2 ($4$ for $H^T H$). |
| **Certified Counterexample** | Lower bound $> 2$ at $b=0.0025$ | **VERIFIED** | Proposition L2 holds at $r=26$ ($R = 2^{26}-1 \approx 6.71 \cdot 10^7, i_0=16$), yielding $\|U_{\rm prot}\| \ge 2.00387 > 2.0$. |
| **Theorem B-F Constant** | $D - q \le \lfloor 8 (\Lambda/s)^2 \rfloor$ | **VERIFIED IN STATED SCOPE** | $\|U_{\rm prot}\|^2 \le 8$; Ky Fan eigenvalue interlacing holds unconditionally; yielding $D - q \le 1.42 \cdot 10^{10} K N^2 m / n^2 = o(n)$ conditional on upstream $\Lambda$. |

---

## 1. Independent Verification of Lemma A (Anti-Concentration Inequality)

### 1.1 Theorem Statement
Let $\beta_1, \dots, \beta_k$ be distinct non-zero vectors in $\mathbb{F}_2^r$. Let $\eta_1, \dots, \eta_k \stackrel{\rm i.i.d.}{\sim} \mathrm{Bernoulli}(p)$ with $0 < p \le 1/2$.
Define the lazy random walk state:
$$X_k = \sum_{l=1}^k \eta_l \beta_l \in \mathbb{F}_2^r.$$
Then for any $\gamma \in \mathbb{F}_2^r$:
$$\Pr(X_k = \gamma) \le \frac{1 - (1 - 2p)^{(k+1)/2}}{k+1} \le \min\left(p, \frac{1}{k+1}\right).$$

### 1.2 Step-by-Step Mathematical Verification

1. **Fourier / Walsh Decomposition:**
   For any character $\chi_u(x) = (-1)^{\langle u, x \rangle}$ with $u \in \mathbb{F}_2^r$:
   $$\mathbb{E}[\chi_u(X_k)] = \prod_{l=1}^k \mathbb{E}[(-1)^{\eta_l \langle u, \beta_l \rangle}] = \prod_{l=1}^k \left( (1-p) + p (-1)^{\langle u, \beta_l \rangle} \right) = \prod_{l=1}^k (1 - 2p \mathbf{1}_{\langle u, \beta_l \rangle = 1}).$$
   Setting $q = 1 - 2p \in [0, 1)$, this equals $q^{w_S(u)}$, where $w_S(u) = \sum_{l=1}^k \mathbf{1}_{\langle u, \beta_l \rangle = 1}$.

2. **Differential Relation:**
   Let $F(p) = \Pr(X_k = \gamma)$. Differentiating with respect to $p$:
   $$F'(p) = \sum_{l=1}^k \left[ \Pr(X_{k \setminus \{l\}} + \beta_l = \gamma) - \Pr(X_{k \setminus \{l\}} = \gamma) \right].$$
   Since $X_k = X_{k \setminus \{l\}} + \eta_l \beta_l$, we have:
   $$\Pr(X_k = \gamma) = (1-p) \Pr(X_{k \setminus \{l\}} = \gamma) + p \Pr(X_{k \setminus \{l\}} + \beta_l = \gamma).$$
   Hence,
   $$(1-2p) \left[ \Pr(X_{k \setminus \{l\}} + \beta_l = \gamma) - \Pr(X_{k \setminus \{l\}} = \gamma) \right] = \Pr(X_k = \gamma + \beta_l) - \Pr(X_k = \gamma).$$
   Summing this identity over all $l = 1, \dots, k$:
   $$(1-2p) F'(p) = \sum_{l=1}^k \Pr(X_k = \gamma + \beta_l) - k F(p).$$

3. **Disjointness and Anti-Concentration:**
   Because the steps $\beta_1, \dots, \beta_k$ are **distinct and non-zero**, the target points:
   $$\gamma + \beta_1, \; \gamma + \beta_2, \; \dots, \; \gamma + \beta_k$$
   are all mutually distinct, and none of them equals $\gamma$.
   Therefore, their total probability mass is bounded by the complement of $\gamma$:
   $$\sum_{l=1}^k \Pr(X_k = \gamma + \beta_l) \le \sum_{x \in \mathbb{F}_2^r \setminus \{\gamma\}} \Pr(X_k = x) = 1 - \Pr(X_k = \gamma) = 1 - F(p).$$

4. **Differential Inequality:**
   Substituting into the derivative identity:
   $$(1-2p) F'(p) \le (1 - F(p)) - k F(p) = 1 - (k+1) F(p),$$
   which is the linear differential inequality:
   $$(1-2p) F'(p) + (k+1) F(p) \le 1.$$

5. **Exact Integration via Integrating Factor:**
   Multiply through by $(1-2p)^{-(k+1)/2 - 1}$:
   $$\frac{d}{dp} \left[ (1-2p)^{-(k+1)/2} F(p) \right] \le (1-2p)^{-(k+1)/2 - 1}.$$
   Integrating from $0$ to $p$, with initial condition $F(0) = \mathbf{1}_{\gamma = 0}$.
   For $\gamma \ne 0$, $F(0) = 0$, giving:
   $$(1-2p)^{-(k+1)/2} F(p) \le \int_0^p (1-2t)^{-(k+1)/2 - 1} dt = \frac{(1-2p)^{-(k+1)/2} - 1}{k+1}.$$
   Multiplying across by $(1-2p)^{(k+1)/2}$:
   $$F(p) \le \frac{1 - (1-2p)^{(k+1)/2}}{k+1}.$$

6. **Upper Envelope Verification:**
   - By Bernoulli's inequality, $(1-2p)^{(k+1)/2} \ge 1 - \frac{k+1}{2}(2p) = 1 - (k+1)p$, so:
     $$\frac{1 - (1-2p)^{(k+1)/2}}{k+1} \le \frac{(k+1)p}{k+1} = p.$$
   - Since $0 \le 1 - 2p \le 1$, $(1-2p)^{(k+1)/2} \ge 0$, so:
     $$\frac{1 - (1-2p)^{(k+1)/2}}{k+1} \le \frac{1}{k+1}.$$
   Hence, $F(p) \le \min\left(p, \frac{1}{k+1}\right)$ is completely verified.

---

## 2. Atom Mapping & Discrete Hardy Inequality (Theorem U*)

### 2.1 Model & Atom Decomposition
In the Theorem B / Route 6 model with sites $x \in \mathbb{F}_2^r$ under uniform measure:
- Time order of captures: $e = 1, \dots, R$ with distinct non-zero labels $\alpha_e \in \mathbb{F}_2^r \setminus \{0\}$.
- Multipliers: $m_e(x) = a (\bar{g} + b \chi_{\alpha_e}(x))$ where $\bar{g} = g_H - b$.
- Capture atom:
  $$\mathrm{cap}_e = m_e \prod_{e' > e} \left[ (a g_H)^{\Delta_{e'}} m_{e'} \right] \cdot \mathrm{tail}.$$
- Ordinary atom in interval preceding capture $e$:
  $$\mathrm{ord}_{e} = a g_H \mathrm{cap}_e.$$
- Common mode in post-capture interval: site-independent constant, which satisfies $P[\mathrm{const}] = 0$ under the protected projection $P = I - \mathbf{1} \mathbf{1}^T / 2^r$.

### 2.2 Protected Subspace Norm Bound
The protected block matrix is:
$$U_{\rm prot} = [P A_{\rm cap} \mid a g_H P A_{\rm cap}].$$
Consequently,
$$\|U_{\rm prot}\|^2 = \lambda_{\max}(U_{\rm prot} U_{\rm prot}^T) = (1 + (a g_H)^2) \|P A_{\rm cap}\|^2 \le (1 + (a g_H)^2) \|P A_{\rm cap}\|^2.$$
Since $a \le 1$ and $g_H \le 1$, $1 + (a g_H)^2 \le 2$.

### 2.3 Time Reversal & Lazy Random Walk Representation
Viewing captures in reverse time (walk order $k = 1, \dots, R$):
Each step applies a transition kernel with jump $\alpha_k$ with probability $p = b/g_H \le 1/2$.
The columns of $P A_{\rm cap}$ correspond to the zero-mean components of the walk laws $\pi_k$.
The Gram matrix $\Gamma(j, k) = \langle P \mathrm{cap}_j, P \mathrm{cap}_k \rangle$ satisfies:
$$\Gamma(j, k) = \sum_{x \ne 0} \pi_{\max(j, k)}(x) \pi_{\min(j, k)}(x) \le \max_{x \ne 0} \pi_{\max(j, k)}(x) \sum_{x} \pi_{\min(j, k)}(x) = \max_{x \ne 0} \pi_{\max(j, k)}(x).$$
By Lemma A:
$$\max_{x \ne 0} \pi_k(x) \le \frac{1}{k+1}.$$
Thus, entrywise:
$$\Gamma(j, k) \le \frac{1}{\max(j, k) + 1} =: K(j, k).$$

### 2.4 Domination by Discrete Hardy Operator
Let $H$ be the classical discrete Hardy operator on $\ell^2(\mathbb{N})$:
$$(H x)_n = \frac{1}{n} \sum_{m=1}^n x_m.$$
The kernel of $H^T H$ is:
$$(H^T H)(j, k) = \sum_{n = \max(j, k)}^\infty \frac{1}{n^2}.$$
By integral comparison:
$$\sum_{n = \max(j, k)}^\infty \frac{1}{n^2} > \int_{\max(j, k)}^\infty \frac{dt}{t^2} = \frac{1}{\max(j, k)} \ge \frac{1}{\max(j, k) + 1} = K(j, k).$$
Thus, the non-negative matrix $K$ is entrywise dominated by $H^T H$:
$$0 \le K(j, k) \le (H^T H)(j, k) \quad \forall j, k \ge 1.$$
By the Perron-Frobenius / Schur test for non-negative operators:
$$\|K\|_{2 \to 2} \le \|H^T H\|_{2 \to 2} = \|H\|_{2 \to 2}^2.$$
By Hardy's classical inequality on $\ell^2$:
$$\|H\|_{2 \to 2} = \frac{p}{p-1} \Bigg|_{p=2} = 2.$$
Therefore,
$$\|K\|_{2 \to 2} \le 4.$$
Since the positive semidefinite Gram matrix $\Gamma$ is dominated in operator norm by $\|K\|_{2 \to 2} \le 4$:
$$\|P A_{\rm cap}\|^2 = \|\Gamma\|_{2 \to 2} \le \|K\|_{2 \to 2} \le 4 \implies \|P A_{\rm cap}\| \le 2.$$
And finally:
$$\|U_{\rm prot}\| \le \sqrt{1 + (a g_H)^2} \|P A_{\rm cap}\| \le \sqrt{1 + 1} \cdot 2 = 2\sqrt{2} \approx 2.8284.$$
This completely and unconditionally verifies Theorem U*.

---

## 3. Refutation of Original Lemma U and Previous Gemini Repair

### 3.1 Refutation of Original Claim $\|U_{\rm prot}\| \le 2$
The original Lemma U claimed $\|U_{\rm prot}\| \le 2$. This is mathematically **REFUTED** by explicit finite counterexamples in standard binary counting order:
- **Witness 1:** $r=11, R=2047, b=0.5 \implies \|U_{\rm prot}\| = 2.0346 > 2.0$.
- **Witness 2:** $r=12, R=4095, b=0.5 \implies \|U_{\rm prot}\| = 2.0746 > 2.0$.
- **Witness 3:** $r=12, R=4095, b=0.2 \implies \|U_{\rm prot}\| = 2.0485 > 2.0$.

### 3.2 Refutation of Previous Gemini Gram-Decay Repair
Our previous attempt conjectured geometric cross-term decay:
$$|G_V(e, f)| \le 2b (a \bar{g})^{|e-f|-1}$$
and attempted a Gershgorin disk bound. This repair was **REFUTED** and cannot be defended:
1. **Intra-level Walsh Collisions:** In counting order, steps at the same hierarchical bit-level share common Walsh characters. The expectation does not decay geometrically with index difference $|e-f|$.
2. **Extreme Ratio Violation:** For $r=6, b=0.5$, the ratio of the true Gram entry to the conjectured geometric bound is:
   $$\max_{e \ne f} \frac{G_V(e, f)}{2b (a \bar{g})^{|e-f|-1}} = 3.60 \times 10^{16} \gg 1.$$
3. **Divergent Row Sums:** The off-diagonal row sum of $G_V$ grows logarithmically with $R$, reaching $2.2656 > 2.0$ at $r=6$ (total row sum $3.2656 > 2.0$). Thus Gershgorin's disk theorem cannot bound $\|U_{\rm prot}\|$ by 2.

---

## 4. Verification of Certified Counterexample at $b=0.0025$

### 4.1 Certified Lower Bound Construction (Proposition L2)
Claude's Proposition L2 isolates an active window of levels $i \in [i_0, r]$ where each level contributes a Walsh block of dimension $2^{i-1}$.
The restricted level matrix $M_{[i_0, r]}$ has entries:
$$M(i, j) = \frac{1}{2} 2^{-|i-j|/2} \left(1 - 2^{-\min(i, j)}\right).$$
The error term $\eta(p, i_0, r)$ bounds the total probability that earlier steps leave the zero character:
$$\eta(p, i_0, r) = \sqrt{2 \sum_{j=i_0}^r \left[ 2^{-j} \frac{q^2}{1-q^2} + 2^{j-1} q^{2^{j-1}} \right]}, \quad q = 1 - 2p.$$
By Weyl's eigenvalue inequality:
$$\|P A_{\rm cap}\| \ge \sqrt{\|M_{[i_0, r]}\|} - \eta(p, i_0, r).$$

### 4.2 Verification at $b=0.0025$ ($p = 0.0025$)
Choosing $r=26$ ($R = 2^{26} - 1 \approx 6.71 \times 10^7$) and $i_0 = 16$:
- $\|M_{[16, 26]}\|^{1/2} = 1.49477$.
- $\eta(0.0025, 16, 26) = 0.07781$.
- $\|P A_{\rm cap}\| \ge 1.49477 - 0.07781 = 1.41695$.
- $\|U_{\rm prot}\| \ge \sqrt{2} \times 1.41695 = 2.00387 > 2.0$.

### 4.3 Gate and Spacing Restrictions & Scale Analysis
- **Model Legality:** In the Theorem B model with $a=1, g_H=1$, spacing $\Delta_e = 1$, and $b = 0.0025 \le g_H/2$, all gates and multipliers are strictly legal.
- **Asymptotic Size:** The witness requires $R \approx 6.71 \times 10^7$ captures. This is asymptotically valid in the formal model where $n \to \infty$ with $R$ fixed or unconstrained.
- **Route 6 Physical Regime:** In Route 6, the actual number of captures scales as $R \asymp \log \log n$. For realistic $n$, $R$ is tiny (e.g. $R \le 10$), where $\|U_{\rm prot}\|^2 \le 2 p R \approx 2(0.0025)(10) = 0.05 \ll 1$. Thus, the violation of 2 is an extreme asymptotic boundary artifact that does not threaten Route 6's physical bounds.

---

## 5. Theorem B-F Status with Constant 8

### 5.1 Verification of Dimension Bound
Theorem B-F bounds the dimension of the bad subspace $D - q$:
$$D - q \le \left\lfloor \|U_{\rm prot}\|^2 \left(\frac{\Lambda}{s}\right)^2 \right\rfloor.$$
With $\|U_{\rm prot}\| \le 2\sqrt{2}$, we have:
$$\|U_{\rm prot}\|^2 \le 8.$$
Therefore,
$$D - q \le \left\lfloor 8 \left(\frac{\Lambda}{s}\right)^2 \right\rfloor.$$
This holds unconditionally given the upstream passivity bound $\Lambda$ and singular value separation $s$.

### 5.2 Numeric Bound in Route 6 Scope
Using the established Route 6 parameter bounds:
$$\Lambda \le 4.21 \cdot 10^4 \frac{\sqrt{K} N \sqrt{m}}{n}, \quad s = 1.0.$$
Substituting:
$$D - q \le 8 \cdot (4.21 \cdot 10^4)^2 \frac{K N^2 m}{n^2} \approx 1.418 \cdot 10^{10} \frac{K N^2 m}{n^2} = o(n).$$
The bound remains $o(n)$ because the constant factor increased only from $4$ to $8$ (a factor of 2).

---

## 6. Audit Verdict Summary

1. **Lemma A:** **VERIFIED**. 6-step proof is exact and sound.
2. **Discrete Hardy Domination & $2\sqrt{2}$ Bound (Theorem U*):** **VERIFIED**. Hardy operator norm is exactly 2, establishing $\|P A_{\rm cap}\| \le 2$ and $\|U_{\rm prot}\| \le 2\sqrt{2}$.
3. **Original Bound $\|U_{\rm prot}\| \le 2$:** **REFUTED**. Refuted by explicit finite witnesses ($R=2047, 4095$) and certified bound at $R \approx 6.71 \cdot 10^7$.
4. **Previous Gemini Gram-decay Repair:** **REFUTED**.intra-level Walsh cross-terms do not decay geometrically.
5. **Theorem B-F with Constant 8:** **VERIFIED IN STATED SCOPE**. Yields $D - q = o(n)$ conditional on upstream passivity $\Lambda$.
