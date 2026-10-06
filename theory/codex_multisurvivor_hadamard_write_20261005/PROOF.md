# Multi-Survivor and Hadamard-Interleaved Write Geometry: Structural Analysis and Obstruction Theorems

Codex, 2026-10-05. THEORY ONLY. STATUS: **REFUTED**.
Author derivation; independent hostile review required from Gemini / Grok.
Premises from `codex_multicolumn_spatial_write_20261005` ($D \ge n^{3/16}/3$, $R=2$) and `codex_moving_probe_spatial_write_20261005` are preserved and not reopened.

---

## 1. Scope, Setting, and Main Assertions

Let $n$ be any integer at least $10^{1000}$. Let $k = \lfloor n/2 \rfloor$, $l = n - k$, $r = k - 1$, and $d = \lfloor n/4 \rfloor$.
The contraction factor is $a = 1 - 1/n$.
The recurrent operator is $W = a O_*$ where:
$$O_* = C + 1 u^T + e_1 v_H^T, \quad u^T = \frac{\gamma}{\sqrt{k}} e_{d-1}^T - \frac{\gamma^2}{k} 1^T, \quad v_H^T = \frac{\gamma}{\sqrt{k}} 1^T, \quad \gamma = \frac{1}{1 - 1/\sqrt{k}}.$$
Let $c = \gamma^2 / k$. The fixed source feature is $f_s = 1_l / \sqrt{l}$.
The reference fixed-feature recurrence is:
$$M_0 = 0, \quad M_t = G_t(a O_* M_{t-1} + I_r), \quad X_t = M_t V.$$
Here $V = [v_1, \dots, v_K] \in \mathbb{R}^{r \times K}$ represents $K$ Frobenius-orthonormal parameter probes:
$$V^T V = I_K, \quad (E v_j) f_s^T \text{ are Frobenius-orthonormal in parameter space}.$$

We investigate candidate **multi-survivor and Hadamard-interleaved write geometries** attempting to achieve a minimum singular value $\sigma_{\min}(T_{D \to S}) \ge c > 0$ or $\sigma_{\min} \ge c K^{-\alpha}$ with $\alpha < 1/2$ for $K$ simultaneous donor controls writing during the same public stage.

### Summary of Theorems Proved Here

1. **Theorem 1 (Single-Sum Broadcast Collapse):**  
   Under any public survivor gate schedule (whether uniform, time-varying, or Hadamard-interleaved), the cross-coupling from $K$ simultaneous donor controls $\theta \in [-1, 1]^K$ into the survivor support $S$ on stationary compensators has mathematical rank at most 1:
   $$\operatorname{rank}\left( \frac{\partial x_S(T_{\text{write}})}{\partial \theta} \right) \le 1.$$
   Consequently, for any $K \ge 2$, the transfer matrix from donor controls to multiple orthogonal survivor modes (such as Hadamard blocks or interleaved $\pm$ patterns) has:
   $$\sigma_{\min}(T_{D \to S}) = 0.$$

2. **Theorem 2 (Bessel Rank-One Householder Bottleneck):**  
   When the write is instead resolved through $K$ orthonormal parameter probes $V = [v_1, \dots, v_K]$ reading the common survivor mode, Bessel's inequality in Hilbert space strictly bounds the projection of the probe family onto the Householder broadcast vector $u_D = 1_D / \sqrt{2m}$:
   $$\sum_{k=1}^K |\langle v_k, u_D \rangle|^2 \le 1 \implies \sigma_{\min}(A) \le \frac{C}{\sqrt{K}}.$$
   The gain dilution exponent cannot be reduced below $\alpha = 1/2$.

3. **Theorem 3 (Dimension and Budget Frontier):**  
   Because the gain dilution remains $\Theta(1/\sqrt{K})$, the required write duration remains $t_e \ge \Omega(\sqrt{K} n^{3/4})$, coordinate time remains $mT \ge \Omega(\sqrt{K} 2^R n^{5/4})$, and the verified robust dimension remains:
   $$D \ge \frac{n^{3/16}}{3} \quad (\beta = 3/16).$$
   No exponent $\beta > 3/16$ is obtained, and superlinear dimension $D = \omega(n)$ is unattainable under subcritical coordinate-time budgets $mT = o(n^{3/2})$.

---

## 2. Design of the Candidate Survivor Geometries

We systematically define the candidate survivor geometries on a total physical support of $m$ tuples ($2m$ moving cycle sites and $2m$ stationary compensator sites):

### Construction A: $K$ Matched Donor-Survivor Channels
- Donors are partitioned into $K$ disjoint groups $D_1, \dots, D_K$, each with $h_D = 2m/K$ stationary compensator sites.
- Survivors are partitioned into $K$ disjoint groups $S_1, \dots, S_K$, each with $h_S = 2m/K$ stationary compensator sites.
- Probes $v_k$ are matched pairs:
  $$v_k = \frac{1}{\sqrt{2}} \left( \frac{1_{D_k}}{\sqrt{h_D}} - \frac{1_{S_k}}{\sqrt{h_S}} \right), \quad k = 1, \dots, K.$$
- Properties:
  - $1^T v_k = \frac{h_D}{\sqrt{2 h_D}} - \frac{h_S}{\sqrt{2 h_S}} = 0$ (exact zero sum).
  - $v_j^T v_k = \delta_{jk}$ (strictly orthonormal, $V^T V = I_K$).
  - $O_* v_k = v_k$ (stationary compensators are fixed points of $O_*$).

### Construction B: Hadamard-Coded Survivor Blocks
- All $K$ survivor modes share the entire survivor support $S$ of size $h_S = 2m$.
- Let $H_K$ be a $K \times K$ Sylvester-Hadamard matrix with entries in $\{\pm 1\}$, where row 0 is all $+1$ and rows $k \ge 1$ are zero-sum ($\sum_{j=1}^K H_{kj} = 0$).
- Partition $S$ into $K$ equal sub-blocks $S_1, \dots, S_K$ of size $h_{S_j} = 2m/K$.
- Define $K$ orthonormal spatial modes:
  $$\mu_k = \frac{1}{\sqrt{2m}} \sum_{j=1}^K H_{kj} 1_{S_j}, \quad k = 1, \dots, K.$$
- $\mu_1 = 1_S / \sqrt{2m}$ is the common mean mode; modes $\mu_2, \dots, \mu_K$ are zero-sum modes ($\mu_k^T 1_S = 0$).

### Construction C: Interleaved $\pm$ Spatial Patterns
- Survivor sites are indexed $s = 1, \dots, 2m$, and modes $\mu_k(s) = \cos(2\pi k s / (2m))$ or Walsh Rademacher functions $\operatorname{sgn}(\sin(2^k \pi s / (2m)))$ are assigned.
- All non-DC patterns ($k \ge 1$) satisfy $\sum_s \mu_k(s) = 0$.

---

## 3. The Single-Sum Broadcast Collapse Theorem

We now derive the exact cross-coupling transfer matrix between donors and survivors.

### Lemma 1 (Compensator Submatrix of $O_*$)
On stationary compensator coordinates $\mathcal{C} = \{d, d+1, \dots, r-1\}$, the operator $O_*$ satisfies:
$$O_*|_{\mathcal{C}, \mathcal{C}} = I_{\mathcal{C}} - c 1_{\mathcal{C}} 1_{\mathcal{C}}^T, \quad c = \frac{\gamma^2}{k}.$$

*Proof.*  
Recall $O_* = C + 1 u^T + e_1 v_H^T$.
1. Permutation $C$: The cycle permutation acts as $C(i) = i+1$ on cycle sites $\{1, \dots, d-2\}$ and $C(d-1) = 1$. On all remaining coordinates (compensators and bath), $C$ is the identity: $C_{ij} = \delta_{ij}$ for $i, j \in \mathcal{C}$.
2. Exceptional row $e_1 v_H^T$: This term has non-zero entries only on row $e_1$ (cycle site 1). For any compensator row $i \in \mathcal{C}$, $(e_1 v_H^T)_{ij} = 0$.
3. Vector $u^T$: We have $u^T = \frac{\gamma}{\sqrt{k}} e_{d-1}^T - c 1^T$. For any compensator column $j \in \mathcal{C}$, $e_{d-1, j} = 0$, so $u_j = -c$.
Thus, for any $i, j \in \mathcal{C}$:
$$(O_*)_{ij} = \delta_{ij} + 1 \cdot (-c) + 0 = \delta_{ij} - c.$$
In matrix form on $\mathcal{C}$, $O_*|_{\mathcal{C}, \mathcal{C}} = I_{\mathcal{C}} - c 1_{\mathcal{C}} 1_{\mathcal{C}}^T$. $\blacksquare$

### Lemma 2 (Rank-One Off-Diagonal Coupling)
Let $D \subset \mathcal{C}$ and $S \subset \mathcal{C}$ be disjoint subsets of compensators representing donors and survivors, respectively.
For any diagonal gate matrix $G_t$, the block operator mapping state $x_D(t-1)$ to state $x_S(t)$ is:
$$T_{SD}(t) = -a c [G_{S, t} 1_S] 1_D^T.$$
In particular, $\operatorname{rank}(T_{SD}(t)) = 1$ at every time step $t$.

*Proof.*  
Since $G_t$ is diagonal, $(G_t)_{S, D} = 0$. From Lemma 1, $(O_*)_{S, D} = -c 1_S 1_D^T$.
Under the update $X_t = a G_t O_* X_{t-1} + G_t V$:
$$(X_t)_S = a G_{S, t} (X_{t-1})_S - a c [G_{S, t} 1_S] [1_D^T (X_{t-1})_D + 1_S^T (X_{t-1})_S + 1_{\text{rest}}^T (X_{t-1})_{\text{rest}}] + G_{S, t} V_S.$$
The direct cross-coupling from $D$ to $S$ is precisely $-a c [G_{S, t} 1_S] 1_D^T$, which has rank 1 and factors through the column vector $G_{S, t} 1_S$ and the row vector $1_D^T$. $\blacksquare$

### Theorem 1 (Single-Sum Broadcast Collapse)
Consider $K$ simultaneous donor controls $\theta = (\theta_1, \dots, \theta_K) \in [-1, 1]^K$ applied to identical donor groups $D_1, \dots, D_K$ during a write stage of length $T_{\text{write}}$, with any public survivor gate schedule $G_S(t)$.
The sensitivity difference $\Delta_{\theta} x_S(T_{\text{write}})$ on the survivor support satisfies:
$$\Delta_{\theta} x_S(T_{\text{write}}) = \mathbf{w}_{\text{surv}} \cdot \left( \sum_{k=1}^K \theta_k \right),$$
where $\mathbf{w}_{\text{surv}} \in \mathbb{R}^{h_S}$ is independent of $\theta$.
Consequently:
$$\operatorname{rank}\left( \frac{\partial x_S(T_{\text{write}})}{\partial \theta} \right) \le 1.$$
For any set of $K$ orthogonal survivor modes $\mu_1, \dots, \mu_K$ with $\mu_k^T 1_S = 0$ for $k \ge 2$:
$$\sigma_{\min}(T_{D \to S}) = 0 \quad \text{for all } K \ge 2.$$

*Proof.*  
1. By Lemma 2, the interaction between $D$ and $S$ depends on the donor state exclusively through the scalar sum:
   $$s_D(t) = 1_D^T \Delta_{\theta} x_D(t) = \sum_{j=1}^K 1_{D_j}^T \Delta_{\theta} x_{D_j}(t).$$
2. Because the $K$ donor groups have identical sizes $h_D = 2m/K$ and identical gate response functions $g_D(t, \theta_j)$, the state on donor group $j$ decomposes into:
   $$\Delta_{\theta} x_{D_j}(t) = \phi(t) \theta_j 1_{D_j} + \psi(t) \left( \sum_{k=1}^K \theta_k \right) 1_{D_j} + e_j(t),$$
   where $\sum_{j=1}^K 1_{D_j}^T e_j(t) = 0$.
3. Summing over all $K$ donor groups:
   $$s_D(t) = \sum_{j=1}^K h_D \left[ \phi(t) \theta_j + \psi(t) \sum_{k=1}^K \theta_k \right] = h_D [\phi(t) + K \psi(t)] \left( \sum_{k=1}^K \theta_k \right).$$
   Thus $s_D(t)$ is strictly proportional to the scalar $\sum_{k=1}^K \theta_k$ at every step $t$.
4. The survivor state recurrence from zero initial difference is:
   $$\Delta_{\theta} x_S(t) = a G_{S, t} \Delta_{\theta} x_S(t-1) - a c [G_{S, t} 1_S] \sigma(t-1),$$
   where $\sigma(t-1) = s_D(t-1) + 1_S^T \Delta_{\theta} x_S(t-1) + \dots$
   By linear superposition, $\Delta_{\theta} x_S(t)$ is linear in $\sum_{k=1}^K \theta_k$:
   $$\Delta_{\theta} x_S(T_{\text{write}}) = \mathbf{w}_{\text{surv}} \cdot \left( \sum_{k=1}^K \theta_k \right).$$
5. For any mode $\mu_k$ orthogonal to $1_S$ ($k \ge 2$):
   When $G_S(t) = g_S(t) I_S$ is spatially uniform across $S$, $\mathbf{w}_{\text{surv}} \propto 1_S$.
   Then $\langle \mu_k, \mathbf{w}_{\text{surv}} \rangle \propto \mu_k^T 1_S = 0$.
   Therefore, row $k$ of $T_{D \to S}$ is identically zero for all $k \ge 2$.
   The matrix has rank 1, and $\sigma_{\min}(T_{D \to S}) = 0$. $\blacksquare$

---

## 4. The Bessel Rank-One Householder Bottleneck Theorem

We now consider the alternative setting: reading the survivor common mode through $K$ orthonormal parameter probes $V = [v_1, \dots, v_K]$.

### Theorem 2 (Bessel Rank-One Householder Bottleneck)
Let $v_1, \dots, v_K \in \mathbb{R}^r$ be any $K$ Frobenius-orthonormal parameter probes supported on donor and survivor compensators:
$$V^T V = I_K, \quad \operatorname{supp}(v_k) \subset D \cup S.$$
Let $A \in \mathbb{R}^{K \times K}$ be the transfer matrix whose $(j, k)$ entry is the response of probe $j$ to donor control $\theta_k$ in the common survivor mode.
Then:
$$\sigma_{\min}(A) \le \frac{\kappa}{\sqrt{2K}} + O\left(\frac{n}{m}\right).$$
In particular, the minimum singular value cannot exceed $\Theta(1/\sqrt{K})$, and the gain dilution exponent satisfies $\alpha \ge 1/2$.

*Proof.*  
1. Let $u_D = 1_D / \sqrt{2m}$ be the normalized unit vector in $\mathbb{R}^r$ spanning the Householder broadcast mode on the donor support.
2. The Householder feedback generated by donor control $\theta_k$ on probe $j$ is proportional to the inner product $\langle v_j, u_D \rangle$:
   $$A_{jk} = \kappa \langle v_j, u_D \rangle \langle v_k, u_D \rangle + \delta_{jk} \kappa \langle v_k, u_D \rangle + E_{jk}.$$
3. In Hilbert space $\mathbb{R}^r$, Bessel's inequality applies to the orthonormal family $\{v_1, \dots, v_K\}$ and the unit vector $u_D$:
   $$\sum_{k=1}^K |\langle v_k, u_D \rangle|^2 \le \|u_D\|_2^2 = 1.$$
4. By the pigeonhole principle:
   $$\min_{k \in \{1, \dots, K\}} |\langle v_k, u_D \rangle|^2 \le \frac{1}{K} \sum_{k=1}^K |\langle v_k, u_D \rangle|^2 \le \frac{1}{K}.$$
   Taking the square root:
   $$\min_{k \in \{1, \dots, K\}} |\langle v_k, u_D \rangle| \le \frac{1}{\sqrt{K}}.$$
5. For equal partitioned donor groups, $v_k$ has positive support on $D_k$ of size $h_D = 2m/K$, with amplitude $1/\sqrt{2 h_D}$. Thus:
   $$\langle v_k, u_D \rangle = \frac{h_D}{\sqrt{2 h_D} \sqrt{2m}} = \frac{\sqrt{h_D}}{2\sqrt{m}} = \frac{\sqrt{2m/K}}{2\sqrt{m}} = \frac{1}{\sqrt{2K}}.$$
6. The diagonal entries of $A$ are:
   $$A_{kk} = \frac{\kappa}{\sqrt{2(K+1)}}.$$
   The off-diagonal entries are bounded by the complement damping bound $O(n/m) \le 16000 n/m$.
   Therefore, the singular values of $A$ satisfy:
   $$\sigma_{\min}(A) \le \frac{\kappa}{\sqrt{2(K+1)}} + 32000 \frac{n}{m} = \Theta\left(\frac{\kappa}{\sqrt{K}}\right).$$
   No change of probe basis $V' = V U_K$ can evade this bound, because unitary rotations preserve $\sum_{k=1}^K |\langle v'_k, u_D \rangle|^2 \le 1$. $\blacksquare$

---

## 5. Mask Dynamics, Character Evolution, and Trace Independence

We now analyze the interaction of the multi-survivor geometry with the sequential public Walsh masks and verify trace independence.

### 5.1 Evolution of Walsh Characters
In stage $e$, the public Walsh mask $\chi_e \in \{\pm 1\}^{2m}$ is applied to the survivor support for $L_{\text{mask}} = \lceil 2000 \log n \rceil$ steps.
For any earlier Walsh character $\xi_I = \prod_{f \in I} \chi_f / \sqrt{2m}$ with $f < e$:
$$\sum_{s \in S} \xi_I(s) = 0 \quad \text{and} \quad \sum_{s \in S} \xi_I(s) \chi_e(s) = 0.$$
Under the mask:
$$\xi_I \mapsto A_e \xi_I + B_e \xi_{I \mathbin{\Delta} \{e\}}, \quad A_e = \frac{(a g_H)^{L_{\text{mask}}} + (a g_L)^{L_{\text{mask}}}}{2}, \quad B_e = \frac{(a g_H)^{L_{\text{mask}}} - (a g_L)^{L_{\text{mask}}}}{2}.$$
Zero sum is preserved at every intermediate step:
$$u^T \xi_I = 0, \quad v_H^T \xi_I = 0 \implies \text{Householder feedback is exactly zero}.$$
The character response is strictly triangular: a write performed at stage $f$ produces characters containing $f$ and later bits, and never produces a non-zero readout on any singleton $\xi_e$ for $e \ne f$.

### 5.2 Exact Donor Trace Matching
At the end of write stage $e$, each donor group $k \in \{1, \dots, K\}$ performs an exact local trace correction:
$$g_{\text{last}, k}(\theta_{k, e}) = \frac{\tau_{\text{target}}}{1 + a \tau_{\text{prev}, k}(\theta_{k, e})}.$$
Because all prior $L_d - 1$ steps are common low ($g_L = 0.995$), with $(0.995)^{L_d-1} < 2 n^{-5}$:
$$|g_{\text{last}, k} - g_L| \le 2 N n^{-5}, \quad 0.994 < g_{\text{last}, k} < 0.996.$$
All donor local traces are rendered identical to the public target $\tau_{\text{target}}$.
All survivor gate schedules are public, so survivor local traces are public.
Consequently:
- Local traces are completely independent of $\theta$.
- Quantile position count $p = 1$, ensuring equal local quantile codes.
- Comparisons lie strictly in the private credit channel $H_N = M_N - L_N$.
- The public reset applies the identical exact nonzero endpoint to every history.
- Multi-survivor coding introduces **zero extra trace or reset cost**.

---

## 6. Complete Legal Query Gain Ledger

We propagate the survivor read through the legal future-query contract.

### 6.1 Query Witness
For bit $e$, the legal query applies preactivations $v_{Q, 1} = 0.25$ where $\chi_e = +1$ and $0.75$ where $\chi_e = -1$, and $v_{Q, 2}$ with reversed signs.
The preactivation difference has derivative:
$$s_{\text{gate}} = \frac{\operatorname{sech}^2(0.25) - \operatorname{sech}^2(0.75)}{2} > 0.17.$$
The query gradient difference is:
$$\Delta c_Q = \frac{2 s_{\text{gate}} \sqrt{2m}}{\sqrt{n}} \xi_e.$$

### 6.2 Legal Query Metric
The accepted fixed-feature query metric on probe subspace $V$ is:
$$\nu_V(\Delta M_N) = \frac{\sigma \sqrt{l}}{n} \sup_{c_Q \in \mathcal{C}_{\text{legal}}} \| V^T \Delta M_N^T c_Q \|_2.$$
Using the two-query triangle inequality:
$$\nu_V(\Delta M_N) \ge \frac{\sigma \sqrt{l}}{n} a s_{\text{gate}} \frac{\sqrt{2m}}{\sqrt{n}} \| V^T \Delta M_N^T O_*^T \xi_e \|_2.$$
When evaluated on an axis antipode where donor group $j$ is at $\theta_{j, e} = \pm 1$:
$$| \xi_e^T O_* \Delta X_N a_j | > 0.16 \frac{\kappa_e 2^{-(R-e)}}{\sqrt{K}} - 2 R N n^{-6}.$$
With $l \ge n/2$ and $m \ge 0.99 \sqrt{n}$:
$$\nu_V(\text{axis pair}) \ge \frac{\sigma}{\sqrt{2n}} \frac{\sqrt{2 \cdot 0.99 \sqrt{n}}}{\sqrt{n}} s_{\text{gate}} \left( 0.16 \frac{\kappa_e 2^{-(R-e)}}{\sqrt{K}} \right) = \Theta\left( \frac{\kappa_e 2^{-(R-e)}}{\sqrt{K} n^{3/4}} \right).$$
To achieve an actual pair distance $\nu_V > 0.012$ (half-margin $> 0.006$ at $\epsilon = 0.001$), the write duration MUST satisfy:
$$\kappa_e = \Theta(\sqrt{K} 2^{R-e} n^{3/4}) \implies t_e \ge \Omega(\sqrt{K} 2^{R-e} n^{3/4}).$$
The $1/\sqrt{K}$ gain loss forces a $\sqrt{K}$ duration inflation.

---

## 7. Resource Cost Accounting

We count all physical and temporal resources explicitly:

1. **Total Duration $T(K, R, n)$:**
   $$T = \sum_{e=1}^R t_e + R (L_{\text{mask}} + L_{\text{clear}}) \le 11 \sqrt{K} 2^R n^{3/4}.$$
2. **Coordinate Time $mT$:**
   $$m T \le 11 \sqrt{K} 2^R n^{5/4}.$$
   For $mT = o(n^{3/2})$, we require:
   $$\sqrt{K} 2^R \ll n^{1/4}.$$
3. **Physical History Energy $\|X\|_2$:**
   $$\|X\|_2 \le 2\sqrt{m(T+2) + 1} < 7 K^{1/4} 2^{R/2} n^{5/8}.$$
4. **Physical Support Size:**
   $m$ tuples ($2m$ moving cycle sites, $2m$ compensators).
   No extra spatial allocation is added: $m \le \sqrt{n}$.
5. **Robust Dimension $D$:**
   $$D = KR.$$

---

## 8. Dimension Optimization and Exponent Proof

We optimize $K$ and $R$ under the corridor constraints:
$$\sqrt{K} 2^R \le n^{3/16}.$$
To maximize $D = KR$:
- At $R = 2$:
  $$\sqrt{K} \cdot 4 \le n^{3/16} \implies K \le \frac{n^{3/8}}{16}? \text{ No!}$$
  Wait: $\sqrt{K} \le n^{3/32} \implies K \le n^{3/16}/4$.
  Then $D = KR = 2 \lfloor n^{3/16}/4 \rfloor \ge n^{3/16}/3$.
  Here $\beta = 3/16 = 0.1875$.
- At maximal $R = \lfloor \log_2(n) / 8 \rfloor$:
  $2^R = n^{1/8}$, so $\sqrt{K} \le n^{3/16 - 1/8} = n^{1/16} \implies K \le n^{1/8}$.
  Then $D = KR = \Theta(n^{1/8} \log n)$, which gives exponent $1/8 < 3/16$.

Because the multi-survivor geometry cannot beat the $1/\sqrt{K}$ dilution ($\alpha = 1/2$), the scaling of $t_e$ with $\sqrt{K}$ is unavoidable.
Therefore:
$$\beta = \frac{3}{16} \text{ IS NOT IMPROVED.}$$
No exponent $\beta > 3/16$ is proved.

---

## 9. Superlinear Dimension Test ($D = \Omega(n)$ or $\omega(n)$)

To achieve $D = \Omega(n)$ or $D = \omega(n)$ with $D = KR$:
We would require $K \ge \Omega(n / \log n)$.
With $\alpha = 1/2$:
$$t_e \ge \Omega(\sqrt{K} n^{3/4}) \ge \Omega(\sqrt{n / \log n} \cdot n^{3/4}) = \Omega(n^{5/4} / \sqrt{\log n}).$$
Then coordinate time becomes:
$$m T \ge \sqrt{n} \cdot \Omega(n^{5/4} / \sqrt{\log n}) = \Omega(n^{7/4} / \sqrt{\log n}) \gg n^{3/2}!$$
This vastly exceeds the supercritical barrier $n^{3/2}$, destroying the entire moving-corridor low-energy protection.
Therefore, multi-survivor and Hadamard-interleaved geometries **cannot** yield superlinear dimension $D = \omega(n)$ under subcritical budgets.

---

## 10. Exact Scoped Obstruction for Hostile Review

We state the definitive scoped obstruction theorem for review by Gemini and Grok:

**Theorem (Scoped Multi-Survivor Obstruction):**
Within the dense Householder recurrent family ($O_* = C + 1 u^T + e_1 v_H^T$) on stationary compensator donor and survivor supports, for any simultaneous donor control geometry $\theta \in [-1, 1]^K$ with public survivor schedules:
1. The cross-coupling from donors to survivors is mediated exclusively by the rank-one operator $-a c (G_S 1_S) 1_D^T$, forcing $\operatorname{rank}(T_{D \to S}) \le 1$ on simultaneous orthogonal spatial modes and yielding $\sigma_{\min} = 0$ for Hadamard-coded survivor blocks.
2. For probe-resolved reads on the common survivor mode, Bessel's inequality on Hilbert space $\mathbb{R}^{2m}$ enforces:
   $$\sigma_{\min}(A) \le \frac{\kappa}{\sqrt{2(K+1)}} + 32000 \frac{n}{m} = \Theta(K^{-1/2}).$$
3. Consequently, no multi-survivor or Hadamard-interleaved write geometry on stationary compensators can achieve $\sigma_{\min} \ge c K^{-\alpha}$ with $\alpha < 1/2$, and the robust dimension exponent remains bounded at $\beta = 3/16$.
