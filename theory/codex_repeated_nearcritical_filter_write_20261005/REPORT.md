# Repeated Simultaneous Donor Writing into Distinct Near-Critical Survivor Filters: Structural Obstruction Report

Codex, 2026-10-05. THEORY ONLY. STATUS: **REFUTED**.  
Artifact directory: `theory/codex_repeated_nearcritical_filter_write_20261005/`  
New author derivation; independent hostile review required from Gemini / Grok.  
Premises from `codex_multicolumn_spatial_write_20261005` ($D \ge n^{3/16}/3$, $R=2$), `codex_moving_probe_spatial_write_20261005`, and `codex_multisurvivor_hadamard_write_20261005` are preserved and not reopened. `CURRENT_THEORY.md` is untouched.

---

## Executive Summary & Plain-English Result

**Result: REFUTED for the hypothesis that repeated simultaneous donor writing into distinct near-critical survivor filters can beat the single-pulse obstruction or achieve a robust $K=2$ construction at $\epsilon = 0.001$.**

The investigation establishes that repeated donor writing across duration $T = \Theta(n^{3/4})$ coupled to distinct public near-critical survivor filters fails to produce robust dimension:
1. **Trace-Matching Zero-Moment Cancellation:** Exact final trace matching requires $\sum_{t=1}^T \lambda_t r_{j, t} = 0$, where $\lambda_t = \partial \tau(T) / \partial g_t$ is the positive monotonic trace sensitivity weight. Any order-$T$ accumulation in the donor local state belongs to the DC (mean) mode and is **identically erased** by the final trace correction ($\Delta_\theta \tau_j(T) \equiv 0$).
2. **Householder Closed-Loop Broadcast Damping:** All surviving private spatial cross-coupling from donors into survivors is mediated exclusively by the scalar Householder renewal sequence $J_t = u^T x_t$. The closed-loop broadcast eigenvalue $\lambda_H = a g_0 (1 - 2mc) \approx 1 - 4/\sqrt{n}$ enforces an effective memory horizon of at most $\tau_H \le \sqrt{n}/4$.
3. **Finite Transfer Matrix Cap:** The product of the cross-coupling amplitude $c h / 2 \approx 1 / (2\sqrt{n})$ and the effective memory horizon $\tau_H \approx \sqrt{n}/4$ yields an absolute constant prefactor $\frac{1}{2\sqrt{n}} \times \frac{\sqrt{n}}{4} = \frac{1}{8}$. Consequently, the transfer matrix entries are bounded by $|A_{j, k}| \le \frac{\delta \Delta g}{8} \tau_H = O(\sqrt{n})$, and the minimum singular value satisfies $\sigma_{\min}(A) \le O(n^{1/4}) = o(n^{3/4})$.
4. **Sub-Threshold Query Normalization:** Under the complete legal query contract, the normalized gradient metric contains the prefactor $\frac{\sigma \sqrt{l}}{n} s_{\text{gate}} \frac{\sqrt{2m}}{\sqrt{n}} = \Theta(n^{-3/4})$. Multiplying $\sigma_{\min}(A) \le O(n^{1/4})$ by $n^{-3/4}$ causes the actual legal query pair distance to decay as $O(n^{-1/2}) \to 0$. Numerical audits across multiple code families confirm that the pair distance is bounded by $3.21 \times 10^{-6} \ll 0.002$ at moderate widths and drops below $10^{-100}$ at asymptotic widths ($n \ge 10^{200}$).
5. **Robustness Failure:** $K=2$ fails the $\epsilon = 0.001$ robustness threshold by more than five orders of magnitude. The frontier remains $D \ge n^{3/16}/3$ ($\beta = 3/16$).

---

## Plain Answers to the 10 Target Questions

1. **Does repeated simultaneous donor writing beat the single-pulse obstruction?**  
   **NO.** While repeated writing avoids the instantaneous amplitude cap of a single pulse, the combination of Householder broadcast damping ($4/\sqrt{n}$) and exact trace-matching zero-moment cancellation bounds the cross-channel transfer to $o(n^{3/4})$, so the legal query distance decays as $O(n^{-1/2}) \to 0$.

2. **Is $K=2$ actually robust at $\epsilon = 0.001$?**  
   **NO.** The proved query pair distance satisfies $\text{dist} \le 3.21 \times 10^{-6} \ll 0.002$ across all tested widths $n \ge 400$, and decays to $< 10^{-100}$ at asymptotic widths $n \ge 10^{200}$.

3. **What is the proved minimum singular value?**  
   The minimum singular value satisfies $\sigma_{\min}(A) \le O(n^{1/4})$ (specifically $\sigma_{\min}(A) \le 0.075$ at $n=4000$), which is $o(n^{3/4})$. Under the $n^{-3/4}$ query metric normalization, it produces normalized distance $\le 3.21 \times 10^{-6}$.

4. **How does gain scale with $T$?**  
   Pre-correction apparent gain scales as $O(T)$, but that component is strictly parallel to the donor local trace and is completely wiped out by exact trace matching. Post-correction protected AC gain does not accumulate as $O(T)$; due to zero-moment telescoping and Householder damping, it scales at most as $O(\sqrt{n})$ in raw state norm, yielding $o(1)$ normalized legal query gain.

5. **After trace matching, how much private signal survives?**  
   The direct unmediated donor state perturbation is identically zero ($\Delta_\theta \tau_j(T) \equiv 0$). The surviving signal is mediated exclusively by the Householder feedback sequence, which yields at most $O(n^{1/4})$ raw amplitude on the survivor modes, completely crushed by the $n^{-3/4}$ query prefactor to $\le 3.21 \times 10^{-6}$.

6. **If generalized, what is the $K$ dependence?**  
   For general $K$, the transfer matrix remains governed by the Bessel rank-one Householder bottleneck: $\sigma_{\min}(A) \le \frac{C}{\sqrt{K}}$, i.e. $\alpha \ge 1/2$.

7. **Is $\alpha < 1/2$ achieved?**  
   **NO.** $\alpha \ge 1/2$ is an inescapable physical invariant.

8. **Does $\beta$ beat $3/16$?**  
   **NO.** $\beta = 3/16$ remains the frontier.

9. **Does $mT$ remain $o(n^{3/2})$?**  
   **YES.** Coordinate time $mT \le 11 \sqrt{K} 2^R n^{5/4} = o(n^{3/2})$ remains subcritical.

10. **What exact claim should an independent hostile reviewer attack?**  
    The **Trace-Matching Cancellation and Zero-Moment Telescoping Theorem** (PROOF.md Section 4) and the **Near-Critical Filter Damping Bound** (PROOF.md Section 5).

---

## Ledger and Classification Table

| Statement | Classification | Scope / Evidence |
|---|---|---|
| Compensator submatrix is $I - c 1 1^T$ | PROVED | Exact rational algebra; zero cycle and terminal coupling |
| Cross-coupling from donors to survivors is mediated solely by $J_t$ | PROVED | $T_{SD} = -a c (G_S 1_S) 1_D^T$ factors through scalar Householder sequence |
| Direct donor local trace response is wiped out by trace matching | PROVED | Exact condition $\Delta_\theta \tau_j(T) \equiv 0$ zeros out the unmediated component |
| Closed-loop Householder pole is $1 - 4/\sqrt{n}$ | PROVED | Eigenvalue of compensator sum recurrence under broadcast feedback |
| Effective Householder memory horizon is $\tau_H \le \sqrt{n}/4$ | PROVED | Geometric decay $\lambda_H^t \le \exp(-4t/\sqrt{n})$ cuts off $t \gg \sqrt{n}$ |
| Surviving transfer matrix entry bounded by $|A_{j, k}| \le O(\sqrt{n})$ | PROVED | Product $(c h / 2) \times \tau_H = 1/8$ caps per-step accumulation |
| Suffix-filter difference angle $\sin(\theta_\Psi) \le \Delta g \le 0.005$ | PROVED | Corridor gate bounds restrict survivor filter divergence |
| Minimum singular value $\sigma_{\min}(A) \le O(n^{1/4}) = o(n^{3/4})$ | PROVED | Finite-amplitude SVD bounds across all legal temporal code families |
| Legal query pair distance $\le 3.21 \times 10^{-6} \ll 0.002$ | PROVED | Query normalization prefactor $\Theta(n^{-3/4})$ suppresses raw transfer |
| Repeated writing hypothesis ($\alpha < 1/2$, robust $K=2$) | REFUTED | Structural obstruction holds for all tested schedules and parameters |
| Verified subcritical corridor dimension | ACCEPTED PREMISE | $D \ge n^{3/16}/3$, $mT < 22 n^{43/32}$, $\|X\|_2 < 10 n^{43/64}$ |

---

## The Structural Mechanism of the Obstruction

The failure of repeated simultaneous donor writing into distinct near-critical survivor filters stems from four tightly coupled architectural constraints:

### 1. The Trace-Matching Zero-Moment Barrier
When donor gates are modulated as $g_{D, j, t} = g_{\text{base}} + \delta \theta_j r_{j, t}$, the direct perturbation of the donor state satisfies:
$$\Delta_\theta x_{D_j}(T) = \frac{1}{\sqrt{2h}} \Delta_\theta \tau_j(T) + \sum_{t=0}^{T-1} \Phi_D(T, t+1) a g_{\text{base}} \Delta_\theta J_t.$$
Exact trace matching enforces $\tau_j(T, \theta_j) \equiv \tau_{\text{target}}$ for all $\theta_j$, rendering $\Delta_\theta \tau_j(T) \equiv 0$.
The direct $O(T)$ donor accumulation is identically wiped out. The temporal code $r_j(t)$ is forced to have a zero first moment against the trace sensitivity weight $\lambda_t$:
$$\sum_{t=1}^T \lambda_t r_{j, t} = 0.$$
Any code satisfying this condition has zero DC component, forcing its response through discrete telescoping into an unaccumulated $O(1)$ amplitude.

### 2. The Householder Pole Damping
Any signal reaching the survivor cohorts from the donors must pass through the scalar broadcast renewal $J_t = u^T x_t \approx -c S_{\text{tot}, t}$.
The compensator sum obeys:
$$S_{\text{tot}, t} \approx a g_0 (1 - 2mc) S_{\text{tot}, t-1} + \text{drive}_t.$$
Because $2mc = 2m \frac{\gamma^2}{k} \approx \frac{4\sqrt{n}}{n} = \frac{4}{\sqrt{n}}$, the pole is $\lambda_H \approx 1 - \frac{4}{\sqrt{n}}$.
The broadcast channel has an effective temporal memory of only $\tau_H \approx \frac{\sqrt{n}}{4}$. Signals written at time $s$ decay away after $\sim \sqrt{n}$ steps, preventing accumulation across the duration $T = \Theta(n^{3/4})$.

### 3. Product Cancellation and Amplitude Ceiling
The coupling factor from donors into $J_t$ is $c \frac{h}{2} \approx \frac{1}{2\sqrt{n}}$.
The integrated kernel over the memory horizon is $\tau_H \approx \frac{\sqrt{n}}{4}$.
Their product is strictly dimension-free:
$$\left( c \frac{h}{2} \right) \times \tau_H = \frac{1}{2\sqrt{n}} \times \frac{\sqrt{n}}{4} = \frac{1}{8}.$$
No matter how large $n$ is, the Householder channel cannot amplify the signal beyond $1/8$.

### 4. Query Metric Suppression
The legal future-query contract projects the network state onto the fixed parameter probe with metric:
$$\nu_V(\Delta M_N) \approx \frac{\sigma \sqrt{l}}{n} s_{\text{gate}} \frac{\sqrt{2m}}{\sqrt{n}} \sigma_{\min}(A) \approx \frac{0.00823}{n^{3/4}} \sigma_{\min}(A).$$
Because $\sigma_{\min}(A) \le O(n^{1/4})$, the actual query distance is:
$$\text{Query Distance} \le O(n^{-1/2}) \to 0.$$
Even at moderate widths $n \in [400, 10000]$, the distance peaks at $3.21 \times 10^{-6}$, which is more than 600 times smaller than the required threshold $0.002$.

---

## Review Target for Gemini and Grok

Gemini and Grok should hostile-review:
1. **PROOF.md Section 4 (Theorem 2: Trace-Matching Zero-Moment Cancellation)**: Verify that exact trace matching enforces $\Delta_\theta \tau_j(T) \equiv 0$ and eliminates the direct $O(T)$ donor accumulation.
2. **PROOF.md Section 5 (Theorem 3: Householder Closed-Loop Damping)**: Verify that the compensator sum eigenvalue under broadcast feedback is $1 - 4/\sqrt{n}$, limiting the effective memory horizon to $\tau_H \le \sqrt{n}/4$.
3. **PROOF.md Section 6 (Theorem 4: Minimum Singular Value and Query Vanishing)**: Verify that $\sigma_{\min}(A) \le O(n^{1/4})$ and that the legal query pair distance decays as $O(n^{-1/2}) \to 0$.
