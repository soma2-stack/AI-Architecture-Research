# Failed Routes and Structural Failure Modes

Codex, 2026-10-05. THEORY ONLY.
Artifact directory: `theory/codex_multisurvivor_hadamard_write_20261005/`

This document records the exact failure points of five candidate constructions for beating the $1/\sqrt{K}$ gain dilution via multi-survivor and Hadamard-interleaved geometries.

---

## Route 1: Simultaneous Multi-Survivor Spatial Coding (Hadamard-Coded Survivor Blocks)

### Proposed Construction
Partition the survivor support $S$ into $K$ blocks and define $K$ orthogonal Hadamard spatial modes:
$$\mu_k = \frac{1}{\sqrt{h_S}} \sum_{j=1}^K H_{kj} 1_{S_j}, \quad k = 1, \dots, K,$$
where $H$ is a $K \times K$ Hadamard matrix. Attempt to write $K$ simultaneous donor controls $\theta_1, \dots, \theta_K$ into the $K$ orthogonal modes $\mu_1, \dots, \mu_K$ during a single public write stage.

### First Failed Inequality / Structural Obstruction
On stationary compensators, $C$ acts as the identity, and the exceptional Householder row $e_1 v_H^T$ is localized to cycle node 1. The off-diagonal coupling from donors to survivors is mediated EXCLUSIVELY by the rank-one broadcast operator:
$$T_{SD} = -a c (G_S 1_S) 1_D^T.$$
Because $T_{SD}$ factors through the all-ones vector $1_S$, the state difference on the survivor support at the end of the write stage is strictly proportional to $1_S$:
$$\Delta_{\theta} x_S(T_{\text{write}}) = \Phi(T_{\text{write}}) \left( \sum_{k=1}^K \theta_k \right) 1_S.$$
For every zero-sum Hadamard mode $k \ge 2$:
$$\langle \mu_k, 1_S \rangle = \frac{1}{\sqrt{h_S}} \sum_{j=1}^K H_{kj} h_{S_j} = \frac{\sqrt{h_S}}{K} \sum_{j=1}^K H_{kj} = 0.$$
Therefore:
$$(T_{D \to S})_{kj} = \langle \mu_k, \Delta_{\theta=e_j} x_S \rangle = 0 \quad \text{for all } k \ge 2, \; j \in \{1, \dots, K\}.$$
Rows $2, \dots, K$ of the transfer matrix are identically zero. The transfer matrix has rank 1, and its minimum singular value is:
$$\sigma_{\min}(T_{D \to S}) = 0.$$
**Verdict: FAILED (Rank-1 Collapse).**

---

## Route 2: Time-Varying Public Survivor Gate Schedules During Write

### Proposed Construction
Keep donors on constant or linear controls, but modulate survivor gates over time using a public schedule $G_S(t) = \operatorname{diag}(g_{S, 1}(t), \dots, g_{S, K}(t))$ across the $K$ survivor blocks to break spatial symmetry and induce multi-mode coupling.

### First Failed Inequality / Structural Obstruction
The input arriving at the survivors at time $t$ from the donors is:
$$T_{SD}(t) x_D(t-1) = -a c [G_S(t) 1_S] [1_D^T x_D(t-1)].$$
Because all $K$ donor groups have identical size $h_D = 2m/K$ and identical gate response functions, the donor state sum is:
$$1_D^T x_D(t-1) = \sum_{j=1}^K 1_{D_j}^T x_{D_j}(t-1) = [\phi(t-1) + K \psi(t-1)] \left( \sum_{k=1}^K \theta_k \right).$$
The donor sum entering the survivor support at every single time step $t$ is proportional to the scalar $\sum_{k=1}^K \theta_k$.
Consequently, the accumulated survivor state at $T_{\text{write}}$ is:
$$\Delta_{\theta} x_S(T_{\text{write}}) = \mathbf{w}_{\text{surv}} \cdot \left( \sum_{k=1}^K \theta_k \right),$$
where $\mathbf{w}_{\text{surv}} = \sum_{s=0}^{T-1} [\phi(s) + K \psi(s)] \left( \prod_{\tau=s+1}^T a G_S(\tau) \right) G_S(s+1) 1_S \in \mathbb{R}^{h_S}$.
Although $\mathbf{w}_{\text{surv}}$ is no longer uniform across sites, it remains a SINGLE fixed spatial vector independent of $\theta$. The map $\theta \mapsto x_S$ remains strictly rank 1:
$$\operatorname{rank}\left( \frac{\partial x_S}{\partial \theta} \right) \le 1 \implies \sigma_{\min} = 0.$$
**Verdict: FAILED (Scalar Input Bottleneck).**

---

## Route 3: Temporal Walsh-Hadamard Gate Modulation Across Donors

### Proposed Construction
Modulate donor group gates in time using orthogonal temporal Walsh functions $w_k(t) \in \{\pm 1\}$:
$$g_{D, k}(t) = g_0 + \theta_k \delta w_k(t), \quad k = 1, \dots, K.$$
Since $\int w_j(t) w_k(t) dt = \delta_{jk}$, hope that orthogonal temporal channels generate orthogonal survivor states.

### First Failed Inequality / Structural Obstruction
For any non-constant Walsh function $k \ge 2$, the temporal sum is zero: $\sum_{t=1}^T w_k(t) = 0$.
Under linear recurrence with contractive factor $a g_0 \approx 1 - 1/n$:
$$\sum_{t=1}^T (a g_0)^{T-t} w_k(t) = O\left( \frac{1}{1 - a g_0 \cos(\omega_k)} \right) = O(1),$$
whereas for the DC mode $w_1(t) = 1$:
$$\sum_{t=1}^T (a g_0)^{T-t} w_1(t) = \frac{1 - (a g_0)^T}{1 - a g_0} \approx \min(T, n) = \Theta(n^{3/4}).$$
All non-constant temporal Walsh modes undergo exact discrete telescoping (zero-moment cancellation), producing an unamplified $O(1)$ response, while the DC mode produces $\Theta(n^{3/4})$. The ratio of oscillatory signals to DC signal is $O(n^{-3/4})$. The singular value spectrum has one large entry $\sigma_1 \approx \Theta(n^{3/4})$ and $K-1$ entries $\sigma_k \le O(1) \ll \epsilon$.
**Verdict: FAILED (Zero-Moment Telescoping).**

---

## Route 4: Disjoint Physical Survivor Allocation ($m_{\text{tot}} = K m$)

### Proposed Construction
Instead of partitioning a fixed physical support of size $m$, allocate $K$ completely separate survivor blocks, each of size $m$, so that total physical support is $m_{\text{tot}} = K m$.

### First Failed Inequality / Structural Obstruction
While each separate block of size $m$ avoids the $1/\sqrt{K}$ amplitude dilution, the total physical support size grows to $m_{\text{tot}} = K m \approx K \sqrt{n}$.
The coordinate-time resource cost is:
$$m_{\text{tot}} T = (K m) T \approx K \sqrt{n} (n^{3/4}) = K n^{5/4}.$$
In `codex_multicolumn_spatial_write_20261005`, the shared support had $m \approx \sqrt{n}$ and $T \approx \sqrt{K} n^{3/4}$, giving $m T \approx \sqrt{K} n^{5/4}$.
Allocating separate physical copies increases the coordinate-time exponent from $\sqrt{K}$ to $K$, strictly worsening the subcritical budget $m T = o(n^{3/2})$:
$$K n^{5/4} \ll n^{3/2} \implies K \ll n^{1/4}.$$
Furthermore, the physical history norm $\|X\|_2 \le 2\sqrt{m_{\text{tot}} T}$ scales as $\sqrt{K} n^{5/8}$ instead of $K^{1/4} n^{5/8}$.
Hiding $K$ in spatial duplication violates the efficient space-reuse requirement and strictly degrades the achievable dimension exponent.
**Verdict: FAILED (Coordinate-Time Multiplication).**

---

## Route 5: Probe Basis Rotations in Hilbert Space

### Proposed Construction
Perform an orthogonal change of basis in probe space: $V' = V U_K$ for an orthogonal matrix $U_K \in O(K)$, attempting to rotate the probe directions so that every probe has a large projection onto the Householder broadcast vector $u_D$.

### First Failed Inequality / Structural Obstruction
Let $u_D = 1_D / \sqrt{2m}$ be the unit vector spanning the Householder broadcast mode.
In the Hilbert space $\mathbb{R}^{2m}$, Bessel's inequality states that for ANY orthonormal family of vectors $\{v'_1, \dots, v'_K\}$:
$$\sum_{k=1}^K |\langle v'_k, u_D \rangle|^2 \le \|u_D\|_2^2 = 1.$$
Because the sum of squares is invariant under orthogonal rotations $U_K$:
$$\sum_{k=1}^K |\langle (V U_K)_k, u_D \rangle|^2 = \sum_{k=1}^K |\langle v_k, u_D \rangle|^2 \le 1.$$
By the pigeonhole principle:
$$\min_{k \in \{1, \dots, K\}} |\langle v'_k, u_D \rangle|^2 \le \frac{1}{K} \sum_{k=1}^K |\langle v'_k, u_D \rangle|^2 \le \frac{1}{K}.$$
Taking the square root:
$$\min_{k \in \{1, \dots, K\}} |\langle v'_k, u_D \rangle| \le \frac{1}{\sqrt{K}}.$$
No change of probe basis, unitary rotation, or linear recombination can overcome this fundamental Hilbert-space geometric bound.
**Verdict: FAILED (Bessel Invariance).**
