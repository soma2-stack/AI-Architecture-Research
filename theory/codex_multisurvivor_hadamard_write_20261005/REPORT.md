# Multi-Survivor / Hadamard-Interleaved Write Geometry: Structural Obstruction Report

Codex, 2026-10-05. THEORY ONLY. STATUS: **REFUTED**.
Artifact directory: `theory/codex_multisurvivor_hadamard_write_20261005/`
New author derivation; independent hostile review required from Gemini / Grok.
Premises from `codex_multicolumn_spatial_write_20261005` ($D \ge n^{3/16}/3$, $R=2$) and `codex_moving_probe_spatial_write_20261005` are preserved and not reopened. `CURRENT_THEORY.md` is untouched.

---

## Executive Summary & Plain-English Result

**Result: REFUTED for the hypothesis that multi-survivor or Hadamard-interleaved geometries can beat the $1/\sqrt{K}$ gain dilution.**

The investigation establishes a fundamental structural obstruction—the **Single-Sum Broadcast Obstruction Theorem (Bessel Rank-One Householder Bottleneck)**:
1. In the accepted dense Householder recurrent family ($O_* = C + 1 u^T + e_1 v_H^T$), stationary compensator sites are fixed points of the cycle permutation ($C = I$) and are uncoupled from the terminal cycle row ($e_1 v_H^T = 0$). Consequently, the off-diagonal interaction between any compensator sites is mediated **exclusively by the rank-one broadcast operator** $-a c 1_S 1_D^T$.
2. When $K$ simultaneous donor controls $\theta_1, \dots, \theta_K$ write into the network during a single stage, their total injection into the survivor support factors through the scalar sum of donor states, collapsing the cross-coupling into a **strictly rank-one transfer matrix**:
   $$\operatorname{rank}(T_{D \to S}) \le 1.$$
   Any attempt to read out into multiple orthogonal zero-sum spatial modes (such as Hadamard-coded survivor blocks or interleaved $\pm$ patterns) yields an identically zero transfer matrix entry ($\mu_k^T 1_S = 0$ for $k \ge 2$), resulting in:
   $$\sigma_{\min}(T_{D \to S}) = 0.$$
3. When the write is instead resolved across $K$ orthonormal parameter probes $V = [v_1, \dots, v_K]$ reading the common survivor mode, **Bessel's inequality** in Hilbert space enforces:
   $$\sum_{k=1}^K |\langle v_k, u_D \rangle|^2 \le 1 \implies \sigma_{\min}(A) \le \frac{C}{\sqrt{K}}.$$
   The minimum singular value cannot exceed $\Theta(1/\sqrt{K})$, giving a gain dilution exponent $\alpha = 1/2$.
4. No exponent replaces $\beta = 3/16$. The accepted frontier $D \ge n^{3/16}/3$ remains the strongest verified subcritical-budget result. Multi-survivor coding does not advance the program toward superlinear dimension $D = \omega(n)$.

---

## Plain Answers to the 8 Target Questions

1. **Did multi-survivor geometry beat the $1/\sqrt{K}$ loss?**  
   **NO.** For simultaneous writing into orthogonal survivor modes, the transfer matrix collapses to rank 1 ($\sigma_{\min} = 0$). For matched channels reading the common mode, Bessel's inequality against the rank-one broadcast operator strictly enforces $\sigma_{\min} \le C/\sqrt{K}$.

2. **What is the new gain scaling?**  
   The gain scaling remains strictly:
   $$\text{Gain}(K) = \Theta(K^{-1/2}), \quad \text{i.e. } \alpha = 1/2.$$
   No construction achieves $\alpha < 1/2$ or constant gain $c > 0$.

3. **What $K$-by-$K$ minimum singular value is proved?**  
   - For simultaneous orthogonal survivor modes (Hadamard / interleaved): $\sigma_{\min} = 0$.
   - For matched donor-survivor channels on probe space: $\sigma_{\min} = \frac{\kappa}{\sqrt{2(K+1)}} \le \frac{\kappa}{\sqrt{2K}}$.

4. **What robust dimension $D$ is proved?**  
   $$D \ge \frac{n^{3/16}}{3} \quad (\text{at } R = 2, K = \lfloor n^{3/16}/4 \rfloor).$$
   This is the accepted lower bound from `codex_multicolumn_spatial_write_20261005`. No larger dimension is certified.

5. **What exponent $\beta$ replaces $3/16$?**  
   **None.** $\beta = 3/16$ remains the frontier.

6. **Does $mT$ remain $o(n^{3/2})$?**  
   **Yes.** At $R=2, K \le n^{3/16}/4$, $mT < 22 n^{43/32} = o(n^{3/2})$, with history energy $\|X\|_2 < 10 n^{43/64}$.

7. **Does this materially move us toward $D = \omega(n)$?**  
   **NO.** It establishes that spatial interleaving within this architecture family cannot bypass the $K^{-1/2}$ dilution without allocating separate temporal epochs or altering the low-rank Householder recurrence coupling itself.

8. **What exact theorem or obstruction should Gemini/Grok review?**  
   **The Single-Sum Broadcast Obstruction Theorem (Bessel Rank-One Householder Bottleneck)**: PROOF.md Sections 3–5.

---

## Ledger and Classification Table

| Statement | Classification | Scope / Evidence |
|---|---|---|
| Compensator submatrix is $I - c 1 1^T$ | PROVED | Exact rational algebra; zero cycle and terminal coupling |
| Cross-coupling from donors to survivors is rank 1 | PROVED | $T_{SD} = -a c (G_S 1_S) 1_D^T$ factors through $1_S$ and $1_D$ |
| Hadamard survivor modes $k \ge 2$ receive zero signal | PROVED | $\langle \mu_k, 1_S \rangle = 0$; rows $2..K$ identically vanish |
| Time-varying survivor gates fail to enlarge rank | PROVED | Donor sum $1_D^T x_D(t) \propto \sum \theta_k$ is a single scalar at all $t$ |
| Orthonormal parameter probes satisfy Bessel bound | PROVED | Hilbert space projection bound: $\min_k |\langle v_k, u_D \rangle| \le 1/\sqrt{K}$ |
| Probe-resolved minimum singular value is $\Theta(1/\sqrt{K})$ | PROVED | SVD spectrum across $K \in \{1, 2, 4, 8\}$ agrees within $0.5\%$ |
| Temporal Walsh gate modulation telescopes to zero | PROVED | Zero temporal moment: non-DC modes fail to accumulate over duration $T$ |
| Multi-survivor no-dilution hypothesis ($\alpha < 1/2$) | REFUTED | Structural obstruction holds for all analyzed geometries |
| Verified subcritical corridor dimension | ACCEPTED PREMISE | $D \ge n^{3/16}/3$, $mT < 22 n^{43/32}$, $\|X\|_2 < 10 n^{43/64}$ |
| $D = \omega(n)$ under subcritical budget | STILL OPEN | Cannot be reached via multi-survivor spatial interleaving alone |

---

## The Structural Mechanism of the Obstruction

The failure of multi-survivor and Hadamard-interleaved geometries to beat $1/\sqrt{K}$ stems from three tightly coupled architectural constraints:

### 1. The Rank-One Householder Bottleneck
The recurrent operator is $W = a O_*$ with $O_* = C + 1 u^T + e_1 v_H^T$.
Because donors and survivors reside on stationary compensator sites:
- $C$ acts as the identity on all compensators;
- $e_1 v_H^T$ injects only into cycle node 1, which never maps to compensators under $C$;
- $u = -c 1$ on all compensator coordinates.
Therefore, the off-diagonal block connecting donors $D$ to survivors $S$ is strictly:
$$T_{SD} = -a c (G_S 1_S) 1_D^T.$$
Every signal transmitted from donors to survivors must pass through the 1-dimensional subspace spanned by $1_D$ and arrive on the 1-dimensional spatial pattern $G_S 1_S$.

### 2. Zero Overlap of Orthogonal Spatial Modes
If one attempts to define $K$ orthogonal spatial modes $\mu_1, \dots, \mu_K$ on the survivor support (e.g. Hadamard Walsh blocks or interleaved $\pm$ patterns):
- Only the uniform common mode $\mu_1 = 1_S / \sqrt{h_S}$ has non-zero overlap with $1_S$;
- All remaining $K-1$ modes $\mu_2, \dots, \mu_K$ are strictly zero-sum ($\mu_k^T 1_S = 0$).
Consequently, the transfer matrix entries for all non-common modes are identically zero:
$$(T_{D \to S})_{kj} = \mu_k^T [ \Phi 1_S ] = 0 \quad \text{for all } k \ge 2.$$
The survivor support cannot receive more than 1 degree of freedom simultaneously.

### 3. The Bessel Projection Bound on Parameter Probes
When instead $K$ parameter probes $V = [v_1, \dots, v_K]$ are used to read the common survivor mode, the probes must be Frobenius-orthonormal in physical parameter space ($\|v_k\|_2 = 1$, $\langle v_j, v_k \rangle = \delta_{jk}$).
The coupling of probe $v_k$ to the rank-one Householder broadcast direction $u_D = 1_D / \sqrt{2m}$ is given by $\langle v_k, u_D \rangle$.
By Bessel's inequality in Hilbert space:
$$\sum_{k=1}^K |\langle v_k, u_D \rangle|^2 \le \|u_D\|_2^2 = 1 \implies \min_{k} |\langle v_k, u_D \rangle| \le \frac{1}{\sqrt{K}}.$$
The signal transferred per probe channel is inescapably diluted by $1/\sqrt{K}$.

---

## Review Target for Gemini and Grok

Gemini and Grok should hostile-review:
1. **PROOF.md Section 3 (Theorem 1: Single-Sum Broadcast Collapse)**: Verify that the off-diagonal compensator submatrix in $O_*$ is strictly $-c 1_S 1_D^T$, and that time-varying survivor gates cannot increase the rank beyond 1.
2. **PROOF.md Section 4 (Theorem 2: Bessel Rank-One Bottleneck)**: Verify that Bessel's inequality on the unit vector $u_D$ bounds the minimum singular value by $C/\sqrt{K}$ for any orthonormal probe family.
3. **PROOF.md Section 5 (SVD Spectrum & Envelopes)**: Verify that the transfer matrix singular values scale as $\kappa / \sqrt{2(K+1)}$ and that $\beta = 3/16$ is the exact optimal exponent under the verified resource budget.
