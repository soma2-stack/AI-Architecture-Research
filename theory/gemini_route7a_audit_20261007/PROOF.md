# Mathematical Audit: Astra Route 7A Reservoir Analysis and Recent-Capture Code

Date: 2026-10-07.  
Author: Gemini (Cursor / Gemini research lane).  
Target: `theory/astra_route7a_reservoir_20261007/PROOF.md` (commit `f1fa85d976bc205f77d7fac101a975be001ded54`).  
Repository Status: **VERIFIED IN STATED SCOPE**.

---

## 1. Executive Verdict and Classification Table

| Target Claim / Section | Author Claim | Audit Verdict | Counterexample Found? | Notes |
|---|---|---|---|---|
| **Right-space lemma (§4, Eq. 8–10)** | $\dim E_{\rm par} \le \min(r, 4m+4N)$ contains all $J_t^T, B_t^T$ | **VERIFIED** | None | Exact rank-2 Duhamel feedback outer products; non-donor injection paths cannot encounter private gates under no-wrap cycle shift; bath/front gates are public at global time. |
| **Walsh suffix attenuation (§5, Eq. 11)** | $\frac{1}{h_S} \sum D_{ii}^2 \le 4/\ell + \exp(-b_0 \ell)$ | **VERIFIED** | None | Distinct Walsh characters are pairwise independent on the hypercube; Chebyshev applies with $\mathrm{Var}(X_i) = \ell/4$. |
| **Two-step final-clear contraction (§6, Eq. 13–15)** | $\|A_{t+1} A_t|_{(H_t^S)^\perp}\| \le 1 - \delta p/32$ | **VERIFIED** | None | Invariant decomposition $\mathbb{R}^r = H_t^S \oplus (H_t^S)^\perp$; outside component after step 1 is either $\ge \sqrt{p}/4$ or step 2 creates $\ge 0.73\sqrt{p}$ outside component. Terminal/bath rows fully covered. |
| **Legal-query estimate (§7, Eq. 18)** | $\nu_{\rm actual}(\Delta M_S) \le 32 \frac{N \sqrt{m}}{n} \sqrt{F_\ell}$ | **VERIFIED** (under premise (3)) | None | Genuinely avoids $\sqrt{r}$ factor; operator norm $\|\Delta M_S\|_{op} \le 2N$ paired directly with $\|D^T P_N c_Q\|_2 \le \frac{2 C_Q}{\sqrt{n}} \sqrt{2m F_\ell}$. No Frobenius norm conversion. |
| **Continuous recent-capture code (§7, Eq. 16–17)** | $q_{\rm recent} \le (2\min(R,\ell)+2)\min(r, 4m+4N)$ | **VERIFIED** | None | Piecewise-parallel public kernels across $\le 2\ell+2$ intervals between captures; equal codes cancel entire recent forcing identically across all parameter columns. |
| **Sublinear dimension conclusion (§8–9, Eq. 20–22)** | $D = o(n)$ for fixed $C_T$, public strong Walsh captures, final clear | **VERIFIED** | None | At Route scaling ($m \sim n/R, N \sim C_T \sqrt{nR}, R \sim \log \log n$), $\ell = O_{C_T, b_0}(1)$ is an absolute constant; Borsuk–Ulam forces antipodal collision if $D > q_{\rm recent}$. |
| **Scoped Route 7A obstruction (§9, Eq. 22)** | Refutes $D = \Omega(n)$ in scoped public capture/final-clear family | **VERIFIED** | None | Rigorous no-go theorem for this specific candidate family; does not rely on signal-mass budget or low-donor capture premise. |
| **Trace-neutral write (§11.1, Eq. 25)** | Exact local trace neutrality $\tau_3 = \tau_{\rm target}$ with legal gates | **VERIFIED** (algebra & legality) | None | Closed-form rational formula cancels control $x$ identically; $|d_3 - g_*| \le 0.000101$ keeps gates strictly legal. Does not by itself establish linear robust memory. |
| **Un-cleared donor feedback alternative (§11–12)** | Retaining private $K \times P$ donor feedback matrix | **OPEN** | N/A | Escapes both the $O(m+N)$ single-row code and the final-clear contraction; remains an open candidate requiring independent robust analysis. |

---

## 2. Prioritized Failure Point 1: Public Feedback Subspace Dimension Bound (§4)

### 2.1 The Claim
In `theory/astra_route7a_reservoir_20261007/PROOF.md` §4, Astra claims that for a fixed public geometry and survivor schedule, there exists a public linear subspace $E_{\rm par} \subset \mathbb{R}^r$ of dimension:
$$P := \dim E_{\rm par} \le \min(r, 4m + 4N)$$
such that for every legal private donor history up to time $N$, every row vector $J_t = u^T M_t$ and $B_t = v_H^T M_t$ satisfies:
$$J_t^T \in E_{\rm par}, \qquad B_t^T \in E_{\rm par}.$$

### 2.2 Mathematical Verification
1. **Model Decomposition**:
   $$M_0 = 0, \qquad M_t = G_t (a O_* M_{t-1} + I_r),$$
   $$O_* = C + \mathbf{1}_r u^T + e_1 v_H^T,$$
   $$L_0 = 0, \qquad L_t = G_t (a C L_{t-1} + I_r), \qquad H_t = M_t - L_t.$$
   Subtracting gives the exact Duhamel renewal:
   $$H_t = \sum_{s=1}^t \Phi_C(t,s) a G_s \left[ \mathbf{1}_r J_{s-1} + e_1 B_{s-1} \right], \qquad \Phi_C(t,s) = (a G_t C) \cdots (a G_{s+1} C).$$

2. **Rank-2 Feedback Structure**:
   Notice that $\mathbf{1}_r J_{s-1} = \mathbf{1}_r \otimes J_{s-1}$ and $e_1 B_{s-1} = e_1 \otimes B_{s-1}$.
   Multiplying $H_t$ on the left by any fixed row vector $w^T \in \mathbb{R}^{1 \times r}$:
   $$w^T H_t = \sum_{s=1}^t \left( w^T \Phi_C(t,s) a G_s \mathbf{1}_r \right) J_{s-1} + \left( w^T \Phi_C(t,s) a G_s e_1 \right) B_{s-1}.$$
   The terms $\alpha_{t,s} := w^T \Phi_C(t,s) a G_s \mathbf{1}_r$ and $\beta_{t,s} := w^T \Phi_C(t,s) a G_s e_1$ are pure **scalars**!
   Therefore:
   $$w^T H_t \in \mathrm{span}\left(\{ J_0, \dots, J_{t-1}, B_0, \dots, B_{t-1} \}\right).$$
   No matter how complex the time-varying gates $G_s$ are, the row space of $H_t$ under projection by $u^T$ or $v_H^T$ never introduces any new row direction into parameter space beyond the linear combinations of previous $J_s$ and $B_s$.

3. **Local Column Support and Public Baseline**:
   Fix a public baseline $G_t^0$ matching all public gates and holding donor gates high.
   Then $L_t^0 = G_t^0 (a C L_{t-1}^0 + I_r)$ is purely public.
   For any column $c \in \{1, \dots, r\}$, the injection at time $u$ is $e_c$.
   Under the cycle shift $C$ (with no wrap), the injected pulse at column $c$ reaches coordinate $c + t - u$ at time $t$.
   This pulse can encounter a private gate at time $t$ if and only if $c + t - u$ is an active donor coordinate:
   - On Track A: $c + t - u = A + i + t \implies c = A + i + u$.
   - On Track B: $c + t - u = B + i + t \implies c = B + i + u$.
   - On stationary compensators: $c \in \{o_i^1, o_i^2\}$.
   
   Because $1 \le i \le m$ and $1 \le u \le N$:
   - $\{ A + i + u \}$ has size at most $m + N$.
   - $\{ B + i + u \}$ has size at most $m + N$.
   - Compensators have size $2m$.
   
   Let $I_{\rm exc} := \{ A + i + u \} \cup \{ B + i + u \} \cup \{o_i^1, o_i^2\}_{i=1}^m$.
   Then $|I_{\rm exc}| \le 2(m+N) + 2m = 4m + 2N$.
   For any column $c \notin I_{\rm exc}$, the trajectory never touches a donor site at any time $t \le N$.
   On all other sites (survivors, bath, front), the gates $G_t$ and $G_t^0$ are identical and public (since the four-site tuple states have zero sum, ensuring the bath and front preactivations are public at global time).
   Therefore:
   $$(L_t - L_t^0) e_c = 0 \qquad \forall c \notin I_{\rm exc}.$$

4. **Induction**:
   Define:
   $$E_{\rm par} := \mathrm{span}\left(\{ e_c : c \in I_{\rm exc} \}\right) + \mathrm{span}\left(\{ (u^T L_t^0)^T, (v_H^T L_t^0)^T : 1 \le t \le N \}\right).$$
   Then:
   $$\dim E_{\rm par} \le |I_{\rm exc}| + 2N \le (4m + 2N) + 2N = 4m + 4N.$$
   - Base case: $J_0 = B_0 = 0 \in E_{\rm par}^T$.
   - Inductive step: Assume $(J_s)^T, (B_s)^T \in E_{\rm par}$ for all $s < t$.
     Then $(u^T H_t)^T \in E_{\rm par}$ and $(v_H^T H_t)^T \in E_{\rm par}$.
     For $L_t$:
     $$u^T L_t = u^T L_t^0 + u^T (L_t - L_t^0).$$
     Here $(u^T L_t^0)^T \in E_{\rm par}$ by definition, and $(L_t - L_t^0)$ only has nonzero columns in $I_{\rm exc}$, so $(u^T (L_t - L_t^0))^T \in \mathrm{span}(\{e_c : c \in I_{\rm exc}\}) \subset E_{\rm par}$.
     Thus $(J_t)^T = (u^T L_t + u^T H_t)^T \in E_{\rm par}$, and similarly $(B_t)^T \in E_{\rm par}$.

**Hostile Check Outcome**: **VERIFIED**. The claim is an exact algebraic theorem. No chronological renewals, bath states, or front dynamics escape $E_{\rm par}$.

---

## 3. Prioritized Failure Point 2: Two-Step Final-Clear Contraction (§6)

### 3.1 The Claim
In §6, Astra asserts that during the public low-donor clear, every two-step operator block restricted to the complementary space $(H_t^S)^\perp$ satisfies:
$$\|A_{t+1} A_t|_{(H_t^S)^\perp}\| \le \sqrt{1 - \delta p/16} \le 1 - \delta p/32,$$
where $H_t^S$ is the co-moving survivor zero-sum subspace, $p = c h_S = \gamma^2(2m)/k$, $\delta = 1 - q_*^2$, and $q_* \le 0.9992$.
After $L_{\rm clear} = 2 \lceil 320 \log(n) / (\delta p) \rceil$ steps, the complementary pair operator norm is at most $2N n^{-10}$.

### 3.2 Mathematical Verification
1. **Orthogonal Space Splitting**:
   $H_t^S = \{ x \in \mathbb{R}^r : \mathrm{supp}(x) \subseteq S_t, \, \mathbf{1}^T x = 0 \}$ has dimension $h_S - 1 = 2m - 1$.
   Its orthogonal complement $(H_t^S)^\perp$ has dimension $r - (2m - 1) = r - 2m + 1$.
   Any $y \in (H_t^S)^\perp$ decomposes uniquely into:
   $$y = \eta u_t^S + v, \qquad u_t^S = \frac{1}{\sqrt{h_S}} \mathbf{1}_{S_t}, \qquad v \in \mathbb{R}^{r \setminus S_t}, \qquad \|y\|^2 = \eta^2 + \|v\|^2.$$
   This orthogonal complement covers **all non-survivor rows**, including terminal, bath, front, donor, compensator, and the survivor constant mode.

2. **Invariance**:
   On $H_{t-1}^S$, $O_* = C$ is an exact isometry onto $H_t^S$.
   During clear, survivor gates are $g_H I$.
   Thus $A_t = G_t a O_*$ maps $H_{t-1}^S$ into $H_t^S$, preserving the orthogonal complement $(H_t^S)^\perp$.

3. **Two-Step Norm Loss Analysis**:
   Let $y \in (H_{t-1}^S)^\perp$ be a unit vector ($\|y\| = 1$).
   Apply $O_*$: $O_* y = \eta u_t^S + v$ with $\|v\|^2 + \eta^2 = 1$.
   Apply $G_t$: on $S_t$, $g_H \le 1$; outside $S_t$, gates are $\le q_*$.
   Thus $\|G_t O_* y\|^2 \le \eta^2 + q_*^2 \|v\|^2 = 1 - \delta \|v\|^2$.
   
   - **Case A**: $\|v\| \ge \frac{\sqrt{p}}{4}$.
     Then after step 1 alone, $\|G_t O_* y\|^2 \le 1 - \delta p/16$.
     Since step 2 is non-expansive ($\|A_{t+1}\| \le 1$), the 2-step norm is $\le \sqrt{1 - \delta p/16}$.
   
   - **Case B**: $\|v\| < \frac{\sqrt{p}}{4}$.
     Then $|\eta| \ge \sqrt{1 - p/16} > 0.99$.
     The state after step 1 is $y' = \eta g_H u_t^S + G_t v$.
     At step 2, apply $O_*$:
     $$O_* y' = \eta g_H (O_* u_t^S) + O_* (G_t v).$$
     What is $O_* u_t^S$?
     $$O_* u_t^S = C u_t^S + \mathbf{1}_r (u^T u_t^S) + e_1 (v_H^T u_t^S) = u_{t+1}^S - \frac{p}{\sqrt{h_S}} \mathbf{1}_r + \sqrt{p} e_1.$$
     Its component along $u_{t+1}^S$ is $\langle u_{t+1}^S, O_* u_t^S \rangle = 1 - p$.
     Its component outside $S_{t+1}$ has squared norm:
     $$\|P_{\text{outside } S_{t+1}} O_* u_t^S\|^2 = \|O_* u_t^S\|^2 - (1 - p)^2 = 1 - (1 - p)^2 = 2p - p^2.$$
     Projecting $O_* y'$ outside $S_{t+1}$:
     $$\|P_{\text{outside } S_{t+1}} O_* y'\| \ge g_H |\eta| \sqrt{2p - p^2} - \|G_t v\| \ge 0.99 \times 0.99 \times \sqrt{1.99 p} - 0.25 \sqrt{p} > 1.13 \sqrt{p} > 0.73 \sqrt{p}.$$
     Then gate $G_{t+1}$ contracts this outside component by $\le q_*$, losing:
     $$\delta \|P_{\text{outside } S_{t+1}} O_* y'\|^2 \ge \delta (0.73)^2 p \approx 0.533 \delta p > \frac{\delta p}{16}.$$
   
   Hence in both cases:
   $$\|A_{t+1} A_t|_{(H_t^S)^\perp}\| \le \sqrt{1 - \delta p/16} \le 1 - \delta p/32.$$

4. **Pair Difference on the Complement**:
   Because both histories share the exact same public clear schedule, the inhomogeneous $+I_r$ term cancels:
   $$\Delta M_t = A_t \Delta M_{t-1}.$$
   After $L_{\rm clear} = 2 \lceil 320 \log(n) / (\delta p) \rceil$ steps:
   $$\|\Delta M_{\rm comp}(N)\|_{op} \le \|\Delta M(t_0)\|_{op} (1 - \delta p/32)^{L_{\rm clear}/2} \le 2N e^{-10 \log n} = 2N n^{-10}.$$

**Hostile Check Outcome**: **VERIFIED**. The contraction applies rigorously to the entire complementary space $(H_t^S)^\perp$, including terminal rows, bath, and front.

---

## 4. Prioritized Failure Point 3: Legal-Query Estimate and Avoidance of $\sqrt{r}$ (§7)

### 4.1 The Claim
In §7, Astra derives the legal-query error of the retained old survivor term:
$$\nu_{\rm actual}(\text{old survivor term}) \le 32 \left( \frac{N \sqrt{m}}{n} \right) \sqrt{F_\ell},$$
explicitly claiming that no hidden $\sqrt{r}$, $\sqrt{K}$, or Frobenius conversion factor is incurred.

### 4.2 Mathematical Verification
1. **Definition of Query Metric**:
   $$\nu_{\rm ref}(A) = \left( \frac{\sigma \sqrt{l}}{n} \right) \sup_{Q} \|A^T c_Q\|_2, \qquad \|c_Q\|_2 \le 1, \quad .0499 < \sigma < .051.$$

2. **Survivor Term Evaluation**:
   The old survivor difference term is:
   $$\Delta M_S(N) = D_{N, t_0} \Delta M_S(t_0).$$
   Since $\Delta M_S$ is supported entirely on survivor zero-sum coordinates $S_N$:
   $$\Delta M_S(N)^T c_Q = \Delta M_S(t_0)^T D_{N, t_0}^T P_N c_Q.$$
   Applying operator norm:
   $$\|\Delta M_S(N)^T c_Q\|_2 \le \|\Delta M_S(t_0)\|_{op} \|D_{N, t_0}^T P_N c_Q\|_2.$$
   We have $\|\Delta M_S(t_0)\|_{op} \le \|\Delta M(t_0)\|_{op} \le 2N$.

3. **Bounding $\|D_{N, t_0}^T P_N c_Q\|_2$**:
   $D_{N, t_0}$ is diagonal on the survivor set $S_N$ with diagonal entries $D_{ii}$.
   $P_N c_Q$ has support of size $h_S = 2m$.
   By inherited premise (3), on ordinary survivor rows:
   $$|c_Q(i)| \le \frac{C_Q}{\sqrt{n}}, \qquad C_Q = 100.$$
   Because $P_N$ is the projection onto the zero-sum subspace of $S_N$:
   $$(P_N c_Q)_i = c_Q(i) - \frac{1}{h_S} \sum_{j \in S_N} c_Q(j) \implies |(P_N c_Q)_i| \le \frac{2 C_Q}{\sqrt{n}}.$$
   Therefore:
   $$\|D_{N, t_0}^T P_N c_Q\|_2^2 = \sum_{i=1}^{h_S} D_{ii}^2 (P_N c_Q)_i^2 \le \left(\frac{2 C_Q}{\sqrt{n}}\right)^2 \sum_{i=1}^{h_S} D_{ii}^2.$$
   By the Walsh attenuation theorem (§5, Eq. 11):
   $$\frac{1}{h_S} \sum_{i=1}^{h_S} D_{ii}^2 \le F_\ell \implies \sum_{i=1}^{h_S} D_{ii}^2 \le h_S F_\ell = 2m F_\ell.$$
   Hence:
   $$\|D_{N, t_0}^T P_N c_Q\|_2 \le \frac{2 C_Q}{\sqrt{n}} \sqrt{2m F_\ell}.$$

4. **Assembling the Full Pre-factor**:
   $$\left( \frac{\sigma \sqrt{l}}{n} \right) \|\Delta M_S(N)^T c_Q\|_2 \le \left( \frac{\sigma \sqrt{l}}{n} \right) (2N) \left( \frac{2 C_Q}{\sqrt{n}} \sqrt{2m F_\ell} \right) = 4 C_Q \sigma \sqrt{\frac{2l}{n}} \left( \frac{N \sqrt{m}}{n} \right) \sqrt{F_\ell}.$$
   Using $l = n - k \le n/2 + 1 \le n$ (so $\sqrt{2l/n} \le \sqrt{2}$), $\sigma \le 0.051$, and $C_Q = 100$:
   $$4 C_Q \sigma \sqrt{2} = 4 \times 100 \times 0.051 \times \sqrt{2} \approx 28.85 \le 32.$$
   Thus:
   $$\nu_{\rm ref}(\text{old survivor term}) \le 32 \left( \frac{N \sqrt{m}}{n} \right) \sqrt{F_\ell}.$$

**Hostile Check Outcome**: **VERIFIED** (under inherited premise (3)).  
There is no Frobenius norm conversion, and the support size of the survivor set is $2m$, not $r$. The dimension $r \approx n/2$ never appears as a $\sqrt{r}$ loss.

---

## 5. Independent Check: Continuous Recent-Capture Code and $D = o(n)$

### 5.1 The Continuous Code (§7, Eq. 16–17)
Between Walsh captures, all survivor gates equal $g_H$.
Thus, the survivor propagator from time $t$ to $N$ has a spatially fixed profile $v_k$ multiplied by a scalar time factor $\lambda_t = (a g_H)^{-t}$.
For $\le \ell$ captures, the interval $[t_0, N]$ is partitioned into at most $2\ell + 2$ segments $\sigma$ on which:
$$w_t = \lambda_t b_\sigma.$$
For each segment $\sigma$, store:
$$C_\sigma(H) = \sum_{t \in \sigma} \lambda_t J_t(H) Q_{\rm par} \in \mathbb{R}^P, \qquad P \le \min(r, 4m + 4N).$$
Total code dimension:
$$q_{\rm recent} \le (2\min(R,\ell) + 2) \min(r, 4m + 4N).$$
Because $J_t(H) = u^T M_t(H)$ is a continuous polynomial function of the gates, $C_\sigma(H)$ is continuous.
When $C_\sigma(H_1) = C_\sigma(H_2)$ for all $\sigma$:
$$\sum_{t=t_0}^{N-1} w_t \Delta J_t = \sum_\sigma b_\sigma \left( \sum_{t \in \sigma} \lambda_t \Delta J_t \right) = 0$$
**identically** across all survivor coordinates and all parameter columns.

### 5.2 Borsuk–Ulam Contradiction and $D = o(n)$ (§8–9)
1. At Route scaling:
   $$R \sim \log \log n, \qquad m \sim n/R, \qquad N \sim C_T \sqrt{nR}.$$
   Then:
   $$\frac{N \sqrt{m}}{n} \sim C_T \sqrt{n \log \log n} \sqrt{\frac{n}{\log \log n}} \frac{1}{n} = C_T = O(1).$$
   Thus $A_0 = \max(1, N\sqrt{m}/n)$ is bounded by an absolute constant.
2. Setting $\tau = 5 \times 10^{-4}$ and $\epsilon = \tau / (32 A_0)$, the required capture horizon:
   $$\ell \ge \max\left(1, \frac{8}{\epsilon^2}, \frac{1}{b_0} \log\left(\frac{2}{\epsilon^2}\right)\right)$$
   is an **absolute constant independent of $n$**.
3. For $R \ge \ell$:
   $$q_{\rm recent} \le (2\ell + 2)(4m + 4N) = O_{C_T, b_0, \tau}(m + N) = O\left(\frac{n}{\log \log n}\right) = o(n).$$
4. By Borsuk–Ulam, any continuous sphere map $S^{D-1} \to \mathbb{R}^{q_{\rm recent}}$ with $D > q_{\rm recent}$ has antipodal collision:
   $$\Delta C_\sigma = 0 \quad \forall \sigma \implies \nu_{\rm actual}(\text{pair}) \le \tau + 0.102 N n^{-10.5} + \epsilon_{\rm dense} \le 0.001 < 0.002.$$
   This contradicts the robust separation $> .002$.
   Therefore:
   $$D \le q_{\rm recent} = o(n).$$

**Hostile Check Outcome**: **VERIFIED**. The scoped Route 7A candidate family cannot achieve $D = \Omega(n)$.

---

## 6. Independent Check: Algebra and Legality of Three-Step Trace-Neutral Write (§11.1)

### 6.1 The Construction
Astra proposes a 3-step write to eliminate the local scalar trace nuisance without a low-donor tail:
$$d_1 = g_* + \epsilon x, \qquad d_2 = g_H,$$
$$\tau_{\rm target} = g_* [1 + a g_H (1 + a g_* (1 + a \tau))],$$
$$d_3 = \frac{\tau_{\rm target}}{1 + a g_H (1 + a d_1 (1 + a \tau))}.$$

### 6.2 Algebraic Verification
The trace update is $\tau_{k} = d_k (1 + a \tau_{k-1})$:
$$\tau_1 = d_1 (1 + a \tau),$$
$$\tau_2 = g_H (1 + a \tau_1) = g_H [1 + a d_1 (1 + a \tau)],$$
$$\tau_3 = d_3 (1 + a \tau_2) = d_3 [1 + a g_H (1 + a d_1 (1 + a \tau))].$$
Substituting $d_3$:
$$\tau_3 = \tau_{\rm target}$$
identically for all $x \in [-1, 1]$. The private control $x$ cancels out completely from the local trace!

### 6.3 Gate Legality
Writing the denominator as $A + B d_1$ where $A = 1 + a g_H > 0$ and $B = a^2 g_H (1 + a \tau) > 0$:
$$d_3 = g_* \frac{A + B g_*}{A + B d_1} \implies d_3 - g_* = - g_* \frac{B \epsilon x}{A + B d_1}.$$
Since $A + B d_1 > B d_1 \ge B (g_* - \epsilon)$:
$$|d_3 - g_*| \le g_* \frac{\epsilon}{g_* - \epsilon}.$$
With $g_* = 0.9975$ and $\epsilon = 10^{-4}$:
$$|d_3 - g_*| \le \frac{0.9975 \times 10^{-4}}{0.9974} \approx 0.00010001 < 0.000101.$$
Because the legal gate band is $[0.99, 1.0]$, $d_3 \in [0.997399, 0.997601]$ is strictly legal, as is $d_1 \in [0.9974, 0.9976]$.

### 6.4 Status
The algebra and legality are **VERIFIED**.  
However, as Astra correctly states, this trace-neutral update does not by itself prove robust linear memory ($D = \Omega(n)$). Immediate capture yields only a weak Walsh component of size $O(C_T b \epsilon / R) = o(1)$. The un-cleared donor feedback channel remains **OPEN**.
