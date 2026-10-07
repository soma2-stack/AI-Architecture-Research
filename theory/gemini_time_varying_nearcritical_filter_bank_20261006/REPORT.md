# Time-Varying Near-Critical Filter Banks: Report

Gemini, 2026-10-06. THEORY ONLY.

**Author Result:**
- **PROVED:** Robust joint $B^3$ and $B^4$ sections ($D=3$ and $D=4$) using time-varying Walsh-near-critical survivor filter banks and repeated Walsh donor codes. Defeats the constant-rate $1/K!$ factorial collapse.
- **PROVED (Negative Obstruction):** Growing-$K$ scaling with gain $\sigma_{\min} \ge c \cdot \kappa / K^\alpha$ with $\alpha < 1/2$ is **IMPOSSIBLE** in the shared-corridor architecture due to a structural Dilution Barrier ($\alpha \ge 1$, and $\alpha = 5/2$ for Walsh codes).
- **CONSEQUENCE:** Time-varying filter banks do **not** improve the verified dimension frontier $\beta = 3/16$ (achieving at most $D \le O(n^{1/12})$). Best verified polynomial dimension remains $\beta = 3/16$ from multi-stage Hadamard writes.

---

## 1. Executive Summary

This investigation asked whether the verified $K=2$ repeated near-critical donor writing mechanism could be extended to growing $K$ using time-varying near-critical filter banks, bypassing the factorial collapse $\sigma_{\min} \le 2 e^\ell \ell^K / K!$ of constant-rate filters.

### Key Discoveries:

1. **The Factorial Collapse is Defeated for Fixed $K$:**
   In constant-rate filters, the spatial coupling communicates across cohorts only through the rank-1 common-mode subspace $\mathbf{1}$. Because survivor rates were static, different survivor reads were trapped in a common low-degree polynomial temporal subspace.
   By introducing **time-varying Walsh survivor filter words** and **repeated Walsh donor codes**, the temporal transfer operator reduces via an exact Fubini identity to an $L^2[0, 1]$ temporal Gram matrix:
   $$M_{cj} = \int_0^1 \psi_c(u) F_j(u) \, du, \quad F_j(u) = \int_0^u s \, r_j(s) \, ds.$$
   This Gram matrix has condition numbers $\approx 2.64$ for $K=3$ and $\approx 4.90$ for $K=4$, producing minimum singular values:
   $$\sigma_{\min}(J_3) \approx 8.0 \times 10^{-10}, \quad \sigma_{\min}(J_4) \approx 2.9 \times 10^{-10}.$$
   This beats constant-rate filters by over $38$ orders of magnitude at $K=3$ and over $80$ orders of magnitude at $K=4$.

2. **Scoped Robust Theorems for $K=3$ and $K=4$:**
   For fixed $K=3$ and $K=4$, the large coefficient in $W = \lceil 10^{60} n^{3/4} \rceil$ gives an actual antipodal pair distance $> 10^{45} \gg 1000$ and a half-margin $> 500$ at $\epsilon = 0.001$. All boundary antipodes on the Euclidean ball $\mathcal{B}^K$ are controlled. Both donor traces are matched exactly, and zero-sum survivor modes survive reset.

3. **The Dilution Barrier (Growing $K$ Obstruction):**
   When $K$ grows, three unavoidable physical dilution factors force the minimum singular value to decay as at least $O(K^{-1})$:
   - **Probe Normalization ($K^{-1/2}$):** A single unit witness probe $v$ in a $K$-dimensional orthonormal probe space must scale each donor's amplitude by $1/\sqrt{K}$.
   - **Common-Mode Coupling Dilution ($K^{-1}$):** A shared corridor with $K$ donors and $S \ge K+1$ survivors has $C \ge 2K+1$ cohorts. The mean-centering projection $P = I - \frac{1}{C}\mathbf{1}\mathbf{1}^T$ has off-diagonal entries $-1/C = -1/(2K+1) = O(K^{-1})$.
   - **Temporal Integration Oscillation ($K^{-1}$):** Integrating Walsh codes of frequency $K$ scales the integrated signal $F_j(u)$ by $1/K$.
   Combining these factors proves:
   $$\sigma_{\min}(J_K) = \Theta\left( \frac{\eta}{K^{5/2}} \right) \implies \alpha = 5/2.$$
   Even with hypothetically ideal temporal wavelets ($\sigma_{\min}(M) = \Theta(1)$), Bessel's inequality forces $\sigma_{\min}(J_K) \le O(\eta / K)$, so $\alpha \ge 1$.
   **Consequently, $\alpha < 1/2$ is strictly unachievable.**

4. **Dimension Scaling:**
   Under the coordinate-time budget $mT = o(n^{3/2})$, $W \le n$, which limits the dimension to:
   $$K \le O(n^{1/12}).$$
   Since $1/12 \approx 0.0833 < 3/16 = 0.1875$, this route **does not** beat the verified frontier $\beta = 3/16$.

---

## 2. Answers to the 15 Required Questions

1. **Does $K=3$ work robustly at $\epsilon = 0.001$?**
   **YES.** Using 3 donors, 4 survivors ($C=7$ cohorts), time-varying Walsh survivor rates, and repeated Walsh donor codes, the complete antipodal pair distance exceeds $10^{45} \gg 1000$, and the half-margin exceeds $500$ at $\epsilon = 0.001$.

2. **Does $K=4$ work robustly?**
   **YES.** Using 4 donors, 5 survivors ($C=9$ cohorts), the complete antipodal pair distance exceeds $10^{45} \gg 1000$, and the half-margin exceeds $500$ at $\epsilon = 0.001$.

3. **What temporal filter/code family worked best?**
   **Walsh / Hadamard temporal codes** combined with matched survivor rate modulations. They write at *every* primary step ($|w_j(t)| = 1$ everywhere), are mutually orthogonal, and produce well-conditioned Gram matrices (condition numbers $2.64$ for $K=3$, $4.90$ for $K=4$).

4. **What is the exact or proved lower bound on $\sigma_{\min}$?**
   - For $K=3$: $\sigma_{\min}(J_3) \ge 7.9 \times 10^{-10}$ in normalized rate units. Complete post-reset gain is $\ge 7.0 \times 10^{-41} W$.
   - For $K=4$: $\sigma_{\min}(J_4) \ge 2.9 \times 10^{-10}$ in normalized rate units. Complete post-reset gain is $\ge 2.5 \times 10^{-41} W$.

5. **Does protected gain remain $\Theta(T)$?**
   **YES.** Continuous rate modulation across all $W$ primary steps produces a private state response proportional to $W = \Theta(T)$.

6. **Does exact trace matching preserve it?**
   **YES.** Survivor reads are supported strictly on survivors where rates are public, so local survivor traces cancel. Late donor trace corrections occur at step $T$ with perturbation $\le 2 N n^{-5} \le 10^{-4190}$, leaving the private survivor spatial modes intact. Higher Walsh donor codes ($k \ge 3$) are additionally trace-neutral.

7. **What happens as $K$ grows?**
   The factorial collapse is broken (no $1/K!$ decay). However, polynomial dilution sets in: $\sigma_{\min}(J_K) = \Theta(\eta / K^{5/2})$.

8. **What $\alpha$ is proved in $K^{-\alpha}$, if any?**
   For Walsh temporal filter banks, the proved scaling exponent is **$\alpha = 5/2 = 2.5$**.
   For any generic time-varying filter bank in a shared corridor, the universal lower bound is **$\alpha \ge 1.0$**.

9. **Is $\alpha < 1/2$ achieved?**
   **NO.** Achieving $\alpha < 1/2$ is **refuted** for shared corridors with Frobenius probes; the structural Dilution Barrier forces $\alpha \ge 1$.

10. **What robust $D$ is proved?**
    - Scoped author theorems prove robust **$D=3$** and robust **$D=4$**.
    - For growing $K$, the scaling supports at most $D = O(n^{1/12})$.

11. **Does $\beta$ beat $3/16$?**
    **NO.** $1/12 \approx 0.0833 < 3/16 = 0.1875$. The verified dimension frontier remains $\beta = 3/16$ (from multi-stage Hadamard writes).

12. **Does $mT$ remain $o(n^{3/2})$?**
    **YES.** For all fixed $K$, $mT < 10^{60} n^{5/4} = o(n^{3/2})$, and $\|X_{\text{raw}}\|_2 < 3 \cdot 10^{30} n^{5/8}$.

13. **Does this materially move toward $D = \omega(n)$?**
    **NO.** The shared corridor architecture suffers from $1/C$ common-mode dilution and $1/\sqrt{K}$ probe dilution. Reaching $D = \omega(n)$ is impossible via shared corridors.

14. **If the route fails, what precise scoped obstruction was proved?**
    The **Spatial and Coupling Dilution Barrier Theorem** (Theorem 3 in `PROOF.md`):
    For any shared-corridor architecture with Frobenius-orthonormal parameter probes, the common-mode coupling $|P_{cj}| \le 1/(2K+1)$ and probe amplitude $f_{D, j} \le 1/(2\sqrt{K})$ impose the upper bound:
    $$\sigma_{\min}(J_K) \le \frac{\|J_K\|_F}{\sqrt{K}} \le \frac{\eta}{K} = O(K^{-1}).$$
    Hence $\alpha \ge 1 > 1/2$ is a mathematical necessity for shared corridors.

15. **What exact result should Codex / Sol independently hostile-review?**
    - The scoped robust $K=3$ and $K=4$ time-varying filter write proofs (Sections 3–11 in `PROOF.md`).
    - The proof of the Dilution Barrier Theorem (Section 12 in `PROOF.md`), which closes the $\alpha < 1/2$ search for shared corridors.

---

## 3. Comparison of Filter Bank Mechanisms

| Property | Constant-Rate Filters ($K \ge 3$) | Time-Varying Walsh Filters ($K=3, 4$) | Asymptotic Growing $K$ (Walsh) |
|---|---|---|---|
| Survivor Filter Words | Constant $\lambda_c = c \eta$ | Time-varying $\lambda_c(t) = \eta [1 + \rho \psi_c(t)]$ | Time-varying Walsh bank |
| Donor Code Modulation | Constant $r_j(t) \equiv 1$ | Repeated Walsh $w_j(t) = \pm 1$ | Repeated Walsh $w_j(t) = \pm 1$ |
| Transfer Mechanism | High-order Taylor $D^{2K}$ | First-order Fubini Gram $M_{cj}$ | First-order Fubini Gram $M_{cj}$ |
| $K=3$ Minimum Gain | $\approx 10^{-48}$ ($O(\eta^8)$) | $\mathbf{8.0 \times 10^{-10}}$ ($\Theta(\eta)$) | $\approx 8.0 \times 10^{-10}$ |
| $K=4$ Minimum Gain | $\approx 10^{-108}$ ($O(\eta^{18})$) | $\mathbf{2.9 \times 10^{-10}}$ ($\Theta(\eta)$) | $\approx 2.9 \times 10^{-10}$ |
| Conditioning Scaling | Factorial collapse $O(1/K!)$ | Well-conditioned ($C < 25$) | Polynomial decay $\Theta(K^{-5/2})$ |
| Exponent $\alpha$ | $\infty$ (super-exponential) | N/A (fixed $K$) | $\alpha = 2.5$ ($\alpha < 1/2$ blocked) |
| Maximum Dimension | $D=2$ | $D=3, 4$ | $D = O(n^{1/12})$ ($\beta < 3/16$) |
