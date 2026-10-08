# Hostile Audit Report: Claude's Lemma U Repair

**Auditor:** Gemini (Cursor / Gemini Research Lane)  
**Date:** 2026-10-07  
**Target Commit:** `11c8867a8f0fc1bff0bf91876e1a9d1b27345c4a`  
**Target Directory:** [`theory/claude_lemma_u_repair_20261007/`](file:///c:/Users/coler/OneDrive/Desktop/ai%20new/theory/claude_lemma_u_repair_20261007/)  
**Audit Directory:** [`theory/gemini_lemma_u_repair_audit_20261007/`](file:///c:/Users/coler/OneDrive/Desktop/ai%20new/theory/gemini_lemma_u_repair_audit_20261007/)  
**Executable Test Suite:** [`checks.py`](file:///c:/Users/coler/OneDrive/Desktop/ai%20new/theory/gemini_lemma_u_repair_audit_20261007/checks.py)

---

## 1. Audit Verdicts & Executive Summary

| Target Claim | Verdict | Core Finding |
| :--- | :--- | :--- |
| **Lemma A Anti-Concentration** | **VERIFIED** | Every step of the 6-step proof is mathematically sound. The differential inequality $(1-2p)F'(p) + (k+1)F(p) \le 1$ rigorously integrates to $\Pr(X_k = \gamma) \le \frac{1 - (1-2p)^{(k+1)/2}}{k+1} \le \min(p, \frac{1}{k+1})$. |
| **Atom Mapping & Discrete Hardy Bound** | **VERIFIED** | Protected projection removes common-mode component; pre-capture interval atoms are collinear with capture atoms ($a g_H \mathrm{cap}_e$); Gram entries satisfy $\Gamma(j,k) \le 1/(\max(j,k)+1) \le (H^T H)(j,k)$; classical Hardy inequality gives $\|H\|_{2 \to 2} = 2$, proving $\|P A_{\rm cap}\| \le 2$ and $\|U_{\rm prot}\| \le 2\sqrt{1+(a g_H)^2} \le 2\sqrt{2} \approx 2.8284$. |
| **Original Lemma U Bound $\|U_{\rm prot}\| \le 2$** | **REFUTED** | Explicit legal finite counterexamples reproduce $\|U_{\rm prot}\| > 2$ at $r=11, 12$ ($R=2047, 4095$). |
| **Previous Gemini Gram-Decay Repair** | **REFUTED** | The conjectured geometric decay $|G_V(e,f)| \le 2b (a\bar{g})^{|e-f|-1}$ fails within levels; ratio of true entry to bound reaches $3.60 \times 10^{16}$ at $r=6$; off-diagonal row sums grow like $\log R$ ($2.2656 > 2.0$ at $r=6$). |
| **Certified Counterexample at $b=0.0025$** | **VERIFIED** | Proposition L2 holds at $r=26$ ($R = 2^{26}-1 \approx 6.71 \cdot 10^7, i_0=16$), yielding $\|U_{\rm prot}\| \ge 2.00387 > 2.0$. Scale analysis confirms it is an asymptotic boundary phenomenon ($R \gg 1$) that does not threaten Route 6's physical regime ($R \asymp \log \log n$). |
| **Theorem B-F with Constant 8** | **VERIFIED IN STATED SCOPE** | $\|U_{\rm prot}\|^2 \le 8$ yields $D - q \le \lfloor 8 (\Lambda/s)^2 \rfloor \approx 1.42 \cdot 10^{10} K N^2 m / n^2 = o(n)$ conditional on upstream passivity $\Lambda$. |

---

## 2. Identification of the First Concrete Errors

### 2.1 First Error in Original Lemma U
In the original Route 7B Lemma U, it was asserted that because distinct Walsh characters $\chi_{\alpha_e}$ are orthogonal, their contributions to the protected subspace can be decoupled to bound $\|U_{\rm prot}\| \le 2$.  
**Concrete Error:** In the time-reversed random walk, products of multipliers $\prod_{f > e} (a\bar{g} + ab \chi_f)$ generate non-orthogonal shared character components across different steps. In binary counting order, these constructive interferences accumulate positive mass that pushes $\|U_{\rm prot}\|$ strictly above 2 ($2.0346$ at $R=2047$, $2.0746$ at $R=4095$).

### 2.2 First Error in Gemini's Previous Gram-Decay Repair
In our prior attempted repair, we claimed that the Gram matrix of normalized vectors $V$ satisfied geometric decay across indices:
$$|G_V(e, f)| \le 2b (a\bar{g})^{|e-f|-1},$$
and used Gershgorin's circle theorem to argue $\|V\|^2 \le 1 + \frac{2b}{1-a\bar{g}} \le 2$.  
**Concrete Error:** This geometric decay assumed each subsequent step independently attenuates previous correlations. However, steps belonging to the same hierarchical bit-level in binary counting order share common basis vectors, so cross-terms within a level do not decay with $|e-f|$. At $r=6, b=0.5$, the actual Gram entry exceeds the conjectured bound by a factor of $3.60 \times 10^{16}$, and the off-diagonal row sum reaches $2.2656 > 2.0$ (diverging as $\log R$). The Gershgorin argument is completely invalid.

---

## 3. Detailed Audit of Claude's Lemma U Repair

### 3.1 Verification of Lemma A (Anti-Concentration Inequality)
Claude models the reverse-time accumulation of multipliers as a lazy random walk $X_k = \sum_{l=1}^k \eta_l \beta_l$ on $\mathbb{F}_2^r$ with $\eta_l \sim \mathrm{Bernoulli}(p)$ and distinct non-zero steps $\beta_l$.
1. **Walsh-Fourier identity:** $\mathbb{E}[\chi_u(X_k)] = \prod_{l=1}^k (1 - 2p \mathbf{1}_{\langle u, \beta_l \rangle = 1})$.
2. **Derivative identity:** Differentiating $F(p) = \Pr(X_k = \gamma)$ yields:
   $$(1-2p) F'(p) = \sum_{l=1}^k \Pr(X_k = \gamma + \beta_l) - k F(p).$$
3. **Disjoint support:** Since $\beta_l$ are distinct and non-zero, the points $\gamma + \beta_l$ are distinct from each other and from $\gamma$. Thus:
   $$\sum_{l=1}^k \Pr(X_k = \gamma + \beta_l) \le 1 - F(p).$$
4. **Differential inequality:** $(1-2p)F'(p) + (k+1)F(p) \le 1$.
5. **Exact solution:** Multiplying by integrating factor $(1-2p)^{-(k+1)/2 - 1}$ and integrating with boundary condition $F(0) = 0$ for $\gamma \ne 0$:
   $$F(p) \le \frac{1 - (1-2p)^{(k+1)/2}}{k+1}.$$
6. **Upper envelope:** Bernoulli's inequality gives $\le p$, and $(1-2p)^{(k+1)/2} \ge 0$ gives $\le \frac{1}{k+1}$.
**Verdict:** Complete, independent verification confirms this proof is exact and mathematically sound.

### 3.2 Verification of Theorem U* (Discrete Hardy Operator Domination)
1. **Atom Structure:**
   - Pre-capture interval atoms are collinear with capture atoms: $\mathrm{ord}_e = a g_H \mathrm{cap}_e$.
   - Post-capture interval atoms are site-independent common modes with protected projection $P[\mathrm{const}] = 0$.
   - Hence, $U_{\rm prot} = [P A_{\rm cap} \mid a g_H P A_{\rm cap}]$, which implies:
     $$\|U_{\rm prot}\|^2 = (1 + (a g_H)^2) \|P A_{\rm cap}\|^2 \le 2 \|P A_{\rm cap}\|^2.$$
2. **Gram Matrix Domination:**
   - In walk order, the Gram matrix entries are inner products of zero-mean probability distributions $\pi_j, \pi_k$.
   - Using Lemma A, $\Gamma(j,k) \le \max_{x \ne 0} \pi_{\max(j,k)}(x) \le \frac{1}{\max(j,k)+1} =: K(j,k)$.
3. **Discrete Hardy Operator:**
   - Define $(Hx)_n = \frac{1}{n} \sum_{m=1}^n x_m$. Its adjoint satisfies $(H^T H)(j, k) = \sum_{n = \max(j,k)}^\infty \frac{1}{n^2}$.
   - By integral comparison: $\sum_{n = \max(j,k)}^\infty \frac{1}{n^2} \ge \frac{1}{\max(j,k)} > \frac{1}{\max(j,k)+1} = K(j,k)$.
   - By Hardy's inequality on $\ell^2$, $\|H\|_{2 \to 2} = 2$, so $\|H^T H\|_{2 \to 2} = 4$.
   - Since $0 \le K(j,k) \le (H^T H)(j,k)$ entrywise, Perron-Frobenius / Schur test gives $\|K\|_{2 \to 2} \le 4$.
   - Thus $\|P A_{\rm cap}\| \le \sqrt{4} = 2$, and $\|U_{\rm prot}\| \le \sqrt{2} \cdot 2 = 2\sqrt{2}$.
**Verdict:** Rigorous, mathematically sound, and fully verified.

### 3.3 Verification of Finite and Certified Counterexamples
1. **Finite witnesses reproduced in `checks.py`:**
   - $r=11, R=2047, b=0.5 \implies \|U_{\rm prot}\| = 2.0346 > 2.0$.
   - $r=12, R=4095, b=0.5 \implies \|U_{\rm prot}\| = 2.0746 > 2.0$.
   - $r=12, R=4095, b=0.2 \implies \|U_{\rm prot}\| = 2.0485 > 2.0$.
2. **Certified Counterexample at $b=0.0025$:**
   - At $r=26$ ($R = 2^{26}-1 \approx 6.71 \cdot 10^7, i_0=16$), Proposition L2 yields $\|P A_{\rm cap}\| \ge 1.41695$, so $\|U_{\rm prot}\| \ge \sqrt{2} \times 1.41695 = 2.00387 > 2.0$.
   - **Gate and Spacing Legality:** In the formal model with $a=1, g_H=1, \Delta_e = 1$, all multipliers $m_e \in [a(g_H-2b), a g_H] = [0.995, 1.0]$ are strictly legal.
   - **Asymptotic Regime:** The counterexample requires $R \approx 6.71 \cdot 10^7$ captures. In Route 6's parameter regime ($R \asymp \log \log n$), $R$ is at most $\sim 10$, where $\|U_{\rm prot}\|^2 \le 2 p R \le 0.05 \ll 1$.

### 3.4 Verification of Theorem B-F Dimension Bound
1. **Interlacing Bound:** Ky Fan eigenvalue interlacing establishes that the number of singular values exceeding $s$ satisfies:
   $$D - q \le \left\lfloor \|U_{\rm prot}\|^2 \left(\frac{\Lambda}{s}\right)^2 \right\rfloor \le \left\lfloor 8 \left(\frac{\Lambda}{s}\right)^2 \right\rfloor.$$
2. **Asymptotic Order:**
   - With Route 6 passivity bound $\Lambda \le 4.21 \cdot 10^4 \frac{\sqrt{K} N \sqrt{m}}{n}$ and $s=1.0$:
     $$D - q \le 8 \cdot (4.21 \cdot 10^4)^2 \frac{K N^2 m}{n^2} \approx 1.42 \cdot 10^{10} \frac{K N^2 m}{n^2} = o(n).$$
   - Replacing constant 4 with constant 8 doubles the numerical prefactor but preserves $o(n)$ scaling identically.

---

## 4. Test Suite Execution Summary

The verification script [`checks.py`](file:///c:/Users/coler/OneDrive/Desktop/ai%20new/theory/gemini_lemma_u_repair_audit_20261007/checks.py) was executed cleanly (exit code 0):
```text
RUNNING GEMINI AUDIT VERIFICATION SUITE FOR CLAUDE LEMMA U REPAIR

--- 1. Testing Lemma A Anti-Concentration Inequality ---
Lemma A verified across all tested k, p, and target points gamma.

--- 2. Testing Discrete Hardy Operator Bound ---
R=  10: ||K||_op = 1.5052 <= 4.0: True
R=  50: ||K||_op = 2.1496 <= 4.0: True
R= 100: ||K||_op = 2.3665 <= 4.0: True
R= 500: ||K||_op = 2.7543 <= 4.0: True
R=1000: ||K||_op = 2.8824 <= 4.0: True
Hardy domination verified: ||K||_op <= 4 implies ||PA_cap|| <= 2 and ||U_prot|| <= 2*sqrt(2).

--- 3. Reproducing Finite Counterexamples to ||U_prot|| <= 2 ---
Witness 1: r=11 (R=2047), b=0.5: ||U_prot|| = 2.0346 > 2.0: True
Witness 2: r=12 (R=4095), b=0.5: ||U_prot|| = 2.0746 > 2.0: True
Witness 3: r=12 (R=4095), b=0.2: ||U_prot|| = 2.0485 > 2.0: True
Original claim ||U_prot|| <= 2 is definitively refuted by explicit finite witnesses.

--- 4. Verifying Certified Counterexample at b=0.0025 ---
At b=0.0025, r=26 (R=2^26-1), i0=16:
  ||M_[i0,r]||^0.5 = 1.49477
  eta = 0.07781
  ||PA_cap|| >= 1.41695
  ||U_prot|| >= 2.00387 > 2.0: True
Certified counterexample at b=0.0025 verified mathematically.

--- 5. Verifying Refutation of Previous Gram-Decay Claim ---
r=6, b=0.5: max ratio to conjectured Gram-decay bound = 3.60e+16 (expected > 1e10)
r=6, b=0.5: max off-diagonal row sum = 2.2656 > 2.0: True
Refutation of previous Gram decay / Gershgorin bound confirmed.

==========================================
ALL TESTS COMPLETED AND VERIFIED.
==========================================
```

---

## 5. Next Mathematical Obligations

Per instructions, Route 6's upstream proofs and the sharp-constant conjecture remain paused. When work resumes, the remaining open obligations are:
1. **Upstream Passivity Review (Route 6):** Independent verification of the passivity bound $\Lambda \le 4.21 \cdot 10^4 \sqrt{K} N m^{1/2} / n$ on which Theorem B-F relies.
2. **Exact Asymptotic Constant (Paused):** Determining whether $\sup \|U_{\rm prot}\| = 1 + \sqrt{2} \approx 2.4142$ or whether the discrete Hardy upper bound of $2\sqrt{2} \approx 2.8284$ can be tightened.
