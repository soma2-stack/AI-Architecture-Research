# Time-Varying Near-Critical Filter Writing: Robust $K=3, 4$ Theorems and the Growing-$K$ Dilution Barrier

Gemini, 2026-10-06. THEORY ONLY. Scoped author proofs for $K=3, 4$ and the structural dilution obstruction for growing $K$. Verified historical results are premises, not reopened.

---

## 1. Theorems and Limitations

### Theorem 1 (Scoped Robust $K=3$ Time-Varying Filter Theorem)
For every integer $n \ge 10^{1000}$, there exists one jointly admissible continuous $\mathcal{B}^3$ section in the frozen dense tanh fixed-feature family, with one source feature, three fixed Frobenius-orthonormal recurrent parameter probes, four public time-varying near-critical survivor filter words, exact public final donor traces, and one exact common nonzero endpoint. All three donor controls act at EVERY primary write step simultaneously using repeated Walsh codes.

Let $W = \lceil 10^{60} n^{3/4} \rceil$, $L = \lceil 1000 \log n \rceil$, $T = W + L$, $N = T + 1$. Then:
$$\text{actual boundary antipodal pair distance} > 1000,$$
$$\text{half-margin} > 500 \quad \text{at } \epsilon = 0.001,$$
$$mT < 10^{60} n^{5/4} = o(n^{3/2}),$$
$$\|X_{\text{raw}}\|_2 < 3 \cdot 10^{30} n^{5/8}.$$
The complete finite control-to-survivor-read antipodal matrix has minimum singular value $\ge 7.0 \times 10^{-41} W$ after trace matching and reset.

### Theorem 2 (Scoped Robust $K=4$ Time-Varying Filter Theorem)
Under the same conditions, using four donors, five public time-varying survivor filter words, and repeated Walsh donor codes, there exists one jointly admissible continuous $\mathcal{B}^4$ section with:
$$\text{actual boundary antipodal pair distance} > 1000,$$
$$\text{half-margin} > 500 \quad \text{at } \epsilon = 0.001,$$
$$\sigma_{\min}(A_{\text{actual}}(\theta)) \ge 2.5 \times 10^{-41} W.$$

### Theorem 3 (The Spatial and Coupling Dilution Barrier for Growing $K$)
For any shared-corridor architecture with $K$ donors and $S \ge K+1$ survivors ($C \ge 2K+1$ total cohorts) using any time-varying near-critical filter bank and any fixed unit witness in an orthonormal Frobenius probe space:
1. Probe amplitude normalization forces $f_{D, j} \le \frac{1}{2\sqrt{K}}$.
2. Mean-centering spatial coupling forces $|P_{cj}| = \frac{1}{C} \le \frac{1}{2K+1}$.
3. Bessel's inequality on the orthonormal survivor reads forces $\|J\|_F \le \frac{\eta}{\sqrt{K}}$.
Consequently:
$$\sigma_{\min}(J_K) \le \frac{\|J\|_F}{\sqrt{K}} \le \frac{\eta}{K} = O(K^{-1}).$$
Thus, the scaling exponent $\alpha$ in $\sigma_{\min}(J_K) \ge c \cdot \kappa / K^\alpha$ must satisfy:
$$\alpha \ge 1.0 > 0.5.$$
With Walsh temporal codes, integrating oscillations of frequency $K$ scales the integrated signal by $1/K$, yielding:
$$\sigma_{\min}(J_K) = \Theta\left( \frac{\eta}{K^{5/2}} \right) \implies \alpha = 5/2.$$
Hence, $\alpha < 1/2$ is **impossible** in the shared-corridor architecture, and the maximum robust dimension is bounded by $D \le O(n^{1/12})$, which **does not** improve the verified dimension frontier $\beta = 3/16$.

---

## 2. Model, Architecture, and Accepted Premises

Let $k = \lfloor n/2 \rfloor$, $l = n - k$, $r = k - 1$, $d = \lfloor n/4 \rfloor$, $a = 1 - 1/n$, $\gamma = 1/(1 - 1/\sqrt{k})$, $c = \gamma^2 / k$.
The selected-memory orthogonal map is:
$$O_* = C + \mathbf{1} u^T + e_1 v_H^T,$$
$$u^T = \gamma \frac{e_{d-1}^T}{\sqrt{k}} - c \mathbf{1}^T, \quad v_H^T = \gamma \frac{\mathbf{1}^T}{\sqrt{k}}.$$
The fixed source is $\sigma \mathbf{1}_l$, with $0.0499 < \sigma < 0.051$, and feature $f_s = \mathbf{1}_l / \sqrt{l}$.
For any fixed unit recurrent action $(E v) f_s^T$, with realized inputs frozen:
$$x_0 = 0, \quad x_t = G_t(a O_* x_{t-1} + v), \quad \|x_t\| \le t.$$

Accepted premises from verified prior theory:
- `codex_unpaired_corridor_sensitivity_20261003/PROOF.md`: full recurrence, four-site moving tuples, inverse lift, endpoint, queries and dense ledger.
- `codex_private_renewal_gamma_20261003/PROOF.md`: corrected dense ledger, public bath/front cap $\le 0.9992$, complete complement contraction.
- `codex_multicolumn_spatial_write_20261005/PROOF.md`: complement bound $16000 n / m$ on high sets with $\ge 2m$ physical sites.
- `codex_repeated_nearcritical_filter_write_20261005/PROOF.md`: verified $K=2$ repeated near-critical filter write mechanism, four-site tuple balance, exact low-tail trace correction.

---

## 3. Time-Varying Near-Critical Filter Bank Formulation

Let $p = 2 \lfloor \sqrt{n}/10 \rfloor$, $m = C p / 2$, $h = 2p$.
For a system with $K$ donors and $S = K + 1$ survivors, total cohorts $C = K + S = 2K + 1$:
- For $K=3$: $C = 7$ cohorts ($D_1, D_2, D_3, S_1, S_2, S_3, S_4$).
- For $K=4$: $C = 9$ cohorts ($D_1, D_2, D_3, D_4, S_1, S_2, S_3, S_4, S_5$).

All tuples use corridor spacing $A = 2(m + T + 4)$, $B = 5(m + T + 4)$.
Each tuple has four physical sites (2 moving cycle sites, 2 compensators) initialized to $(+\beta, +\beta, -\beta, -\beta)$ with $\beta = \sqrt{1-g}$, ensuring zero state sum.

### Repeated Walsh Donor Codes
For each donor $j \in \{1, \dots, K\}$, the primary write rate is modulated continuously at every step $t \in \{1, \dots, W\}$:
$$\lambda_{D, j}(t, \theta) = \lambda_{D, j}^0 + \delta \, \theta_j \, r_j(t/W),$$
$$g_{D, j, t} = 1 - \frac{\lambda_{D, j}(t, \theta)}{W},$$
where $\eta = 10^{-6}$, $\delta = 10^{-30}$, $\theta \in \mathcal{B}^K$, baseline $\lambda_{D, j}^0 = (j + 1)\eta$, and $r_j(s) = w_j(s) \in \{+1, -1\}$ is the $j$-th zero-mean Walsh function on $[0, 1]$.
Notice that $|r_j(t)| = 1$ at every step, so each donor control writes repeatedly throughout all $W$ steps.

### Time-Varying Public Survivor Filter Words
The survivor cohorts use public, time-varying near-critical rates:
$$\lambda_S(s) = \eta \mathbf{1}_S + \rho \eta \sum_{k=1}^K \psi_k(s) q_k,$$
$$g_{S, c, t} = 1 - \frac{\lambda_{S, c}(t/W)}{W},$$
where $\rho = 1/2$, $q_1, \dots, q_K$ are $K$ orthonormal zero-sum vectors in $\mathbb{R}^S$, and $\psi_k(s)$ are public temporal filter waveforms on $[0, 1]$ satisfying $\max_s |\psi_k(s)| \le 1$.
Because $\rho = 1/2$ and $\|q_k\|_\infty \le 1$, all survivor rates satisfy $\lambda_{S, c}(s) \in [\eta/2, 3\eta/2] \subset (0, 4\eta)$, and all gates remain legal in $(0.994, 1.0)$.

### Parameter Probes
Let $d_j, s_j$ be unit indicators of the $p$ compensators of $D_j, S_j$.
$$v_j = \frac{d_j - s_j}{\sqrt{2}}, \quad j = 1, \dots, K.$$
Then $V = [v_1, \dots, v_K]$ satisfies $V^T V = I_K$, $O_* v_j = v_j$, and $\mathbf{1}^T v_j = 0$.
The fixed unit witness probe is:
$$v = \frac{1}{\sqrt{K}} \sum_{j=1}^K v_j.$$
Its projection onto the unit cohort-mean basis is:
$$f = \frac{w}{2\sqrt{K}},$$
where $w = (\underbrace{1, \dots, 1}_{K}, \underbrace{-1, \dots, -1}_{K}, 0, \dots, 0)^T \in \mathbb{R}^C$.
Since $\mathbf{1}^T w = 0$, $P w = w$, and $\|f\|_2 = 1/\sqrt{2}$.

---

## 4. Nonperturbative Multi-Cohort Reduction

Let $A_t$ contain all $4m$ driven sites and $H_t$ be the supported sum-zero subspace.
Under uniform $g_H$ on $A_t$, $H_t$ is an exactly reducing subspace of the comparison propagator.
By the accepted complement resolvent bound, the actual complement $q_t = (I - P_{H, t}) x_t$ satisfies:
$$\|q_t\| \le B := 16000(1 + \ell) \frac{n}{m} < 35000\sqrt{n}, \quad \ell = 4\eta.$$

In the co-moving unit cohort-mean basis, let $z_t$ be the five/seven/nine cohort-mean part of $P_{H, t} x_t$.
Because within-cohort sum-zero components are exactly reducing under cohort-scalar gates, they cannot feed cohort means.
Furthermore, Householder feedback $(O_* - C) q_t \in \operatorname{span}\{\mathbf{1}, e_1\}$.
Because $e_1$ is off-corridor and $\mathbf{1}$ projects identically onto all $C$ cohorts, $P \mathbf{1} = 0$ annihilates Householder feedback before the gate.
The exact projected recurrence is:
$$z_t = a\left(I - \frac{P \Lambda(t)}{W}\right) z_{t-1} + f - \frac{P \Lambda(t) f}{W} + e_t,$$
$$\|e_t\| \le \frac{\ell B}{W}.$$

Summing the $a-1 = -1/n$ drift, Euler approximation error, and complement forcing gives the continuum error:
$$\|z_W - W Z(\theta)\| \le E := \frac{W^2}{n} + \sqrt{n},$$
where $Z(\theta)$ is the solution of the non-autonomous linear ODE on $[0, 1]$:
$$\frac{dZ}{ds} = - P \operatorname{diag}(\lambda(s, \theta)) P Z(s) + f, \quad Z(0) = 0.$$
At $n \ge 10^{1000}$, $E/W \le 3 \cdot 10^{-190}$, which is astronomically negligible.

---

## 5. The Exact First-Order Temporal Transfer Operator

Let $\Phi(s, u)$ be the propagator of $\frac{dZ}{ds} = - P \operatorname{diag}(\lambda^0(s)) P Z(s)$.
The unperturbed trajectory is $Z_0(s) = \int_0^s \Phi(s, u) f \, du$.
The directional derivative of $Z(1)$ with respect to $\delta \theta_j$ is:
$$\frac{\partial Z(1)}{\partial (\delta \theta_j)} = - \int_0^1 \Phi(1, s) P e_{D, j} [e_{D, j}^T P Z_0(s)] r_j(s) \, ds.$$
Multiplying by the survivor readout matrix $Q$:
$$J_{cj} = - \int_0^1 [q_c^T \Phi(1, s) P e_{D, j}] [e_{D, j}^T P Z_0(s)] r_j(s) \, ds.$$

### The Fubini Kernel Identity
At leading order in $\eta$:
1. $e_{D, j}^T P Z_0(s) = s f_{D, j} + O(\eta) = \frac{s}{2\sqrt{K}} + O(\eta)$.
2. $q_c^T \Phi(1, s) P e_{D, j} = \frac{1}{C} \int_s^1 \langle q_c, \lambda_S(u) \rangle \, du + O(\eta^2) = \frac{\rho \eta}{C} \int_s^1 \psi_c(u) \, du + O(\eta^2)$.

Substituting into $J_{cj}$ and defining $\Psi_c(s) = \int_s^1 \psi_c(u) \, du$:
$$J_{cj} = - \frac{\rho \eta}{2 C \sqrt{K}} \int_0^1 \Psi_c(s) s \, r_j(s) \, ds + O(\eta^2).$$
Applying Fubini's theorem (or integration by parts):
$$\int_0^1 \Psi_c(s) s \, r_j(s) \, ds = \int_0^1 \left( \int_s^1 \psi_c(u) \, du \right) s \, r_j(s) \, ds = \int_0^1 \psi_c(u) \left( \int_0^u s \, r_j(s) \, ds \right) du.$$
Defining the integrated donor code:
$$F_j(u) = \int_0^u s \, r_j(s) \, ds,$$
we obtain the exact leading-order transfer matrix:
$$J_{cj} = - \frac{\rho \eta}{2 C \sqrt{K}} M_{cj} + O(\eta^2), \quad M_{cj} = \int_0^1 \psi_c(u) F_j(u) \, du.$$

$M_{cj}$ is the $L^2[0, 1]$ inner product between the public survivor filter $\psi_c$ and the integrated donor code $F_j$.
By choosing $\psi_c$ matched to $F_j$ (specifically $\psi_c = \sum_k (G^{-1/2})_{ck} F_k$), $M$ becomes the positive definite matrix $G^{1/2}$, with:
$$\sigma_{\min}(M) = \sqrt{\sigma_{\min}(G)}, \quad G_{jk} = \int_0^1 F_j(u) F_k(u) \, du.$$
This completely defeats the factorial collapse: $M$ is well conditioned, and $\sigma_{\min}(J) = \Theta(\eta)$, not $O(\eta^K / K!)$.

---

## 6. Quantitative Derivative Bounds and Conditioning for $K=3$ and $K=4$

### Analysis for $K=3$
Using Walsh codes $w_1, w_2, w_3$, the integrated functions $F_1, F_2, F_3$ have Gram matrix:
$$G_3 = \begin{bmatrix}
8.354 \cdot 10^{-3} & 6.668 \cdot 10^{-4} & 1.309 \cdot 10^{-3} \\
6.668 \cdot 10^{-4} & 1.828 \cdot 10^{-3} & -1.297 \cdot 10^{-3} \\
1.309 \cdot 10^{-3} & -1.297 \cdot 10^{-3} & 9.625 \cdot 10^{-3}
\end{bmatrix}.$$
Its singular values are $[0.01051, 0.00779, 0.00151]$, yielding:
$$\sigma_{\min}(M_3) = \sqrt{0.00151} \approx 0.0388, \quad \text{cond}(M_3) = \sqrt{6.98} \approx 2.64.$$
With $C = 7$, $\rho = 1/2$, $\eta = 10^{-6}$:
$$\sigma_{\min}(J_3) \ge \frac{0.5 \cdot 10^{-6}}{2 \cdot 7 \cdot \sqrt{3}} \cdot 0.0388 \approx 7.997 \times 10^{-10}.$$

### Analysis for $K=4$
Using Walsh codes $w_1, w_2, w_3, w_4$, the Gram matrix $G_4$ has minimum eigenvalue $\lambda_{\min} \approx 4.38 \cdot 10^{-4}$, yielding:
$$\sigma_{\min}(M_4) = \sqrt{4.38 \cdot 10^{-4}} \approx 0.0209, \quad \text{cond}(M_4) \approx 4.90.$$
With $C = 9$, $\rho = 1/2$, $\eta = 10^{-6}$:
$$\sigma_{\min}(J_4) \ge \frac{0.5 \cdot 10^{-6}}{2 \cdot 9 \cdot 2} \cdot 0.0209 \approx 2.907 \times 10^{-10}.$$

---

## 7. Finite $\mathcal{B}^K$ Boundary Control and Hessian Remainder

Along the control ball $\mathcal{B}^K$, Duhamel's formula integrated twice yields:
$$\|D^2 F[\alpha, \beta]\| \le \|Q\| \cdot \|f\| \cdot \|\alpha\|_2 \|\beta\|_2 \int_0^1 s^2 \, ds \le \frac{1}{3} \|\alpha\|_2 \|\beta\|_2.$$
For any unit boundary vector $\theta \in S^{K-1} = \partial \mathcal{B}^K$:
$$F(\theta) - F(-\theta) = 2\delta \bar{J}(\theta) \theta, \quad \bar{J}(\theta) = \frac{1}{2} \int_{-1}^1 D F(t \delta \theta) \, dt.$$
By Taylor's theorem:
$$\|\bar{J}(\theta) - J_0\| \le \frac{\delta}{6} \le \frac{\delta}{3}.$$
Because $\delta/3 = 10^{-30}/3 \ll 10^{-10}$, Weyl's inequality guarantees:
$$\sigma_{\min}(\bar{J}(\theta)) \ge \sigma_{\min}(J_0) - 10^{-30} > 0.99 \sigma_{\min}(J_0)$$
for **every** unit vector $\theta \in S^{K-1}$.
The reference finite antipodal difference satisfies:
$$\|F(\theta) - F(-\theta)\| \ge 2\delta W (0.99 \sigma_{\min}(J_0)) - 2E.$$

---

## 8. Trace Neutrality, Exact Late Trace Matching, and Reset

### Trace Neutrality of Higher Walsh Codes
For Walsh code $w_3 = w_1 w_2$, the trace weight is:
$$\int_0^1 (1 - s) w_3(s) \, ds = 0.$$
Higher Walsh codes are trace-neutral, producing zero primary donor trace drift.

### Exact Late Trace Matching
For any residual trace difference, donor $j$ runs at $g_L = 0.995$ for $L-1$ tail steps, and at step $T = W + L$ uses:
$$g_{\text{last}, j}(\theta) = \frac{\tau_{\text{target}, j}}{1 + a \tau_{\text{prev}, j}(\theta)}.$$
Because $(a g_L)^{L-1} < 2n^{-5}$, $|g_{\text{last}, j} - g_L| \le 2 N n^{-5} \le 10^{-4190}$.
Survivor gates are uniformly $g_H = 1 - n^{-2}$, and their zero-sum subspace is exactly reducing.
The protected survivor read difference survives through reset with multiplier:
$$\beta = (a g_H)^L a q_N > 0.97.$$

---

## 9. Dense Model Comparison and Actual Protected Matrix

With $\|R - R_0\| \le e_R \le \frac{4}{10^8 n^2}$:
$$\text{state charge} \le e_R \frac{N(N-1)}{2} \le 8 \cdot 10^{-388}.$$
$$\text{query charge} \le 8 \cdot 10^{-9}.$$
Dividing by $W \ge 10^{810}$, the dense state error is $\le 8 \cdot 10^{-1198} \ll \delta \sigma_{\min}(J)$.
Thus, for every unit $\theta$:
- For $K=3$: $\sigma_{\min}(A_{\text{actual}}(\theta)) \ge 7.0 \times 10^{-41} W$.
- For $K=4$: $\sigma_{\min}(A_{\text{actual}}(\theta)) \ge 2.5 \times 10^{-41} W$.

---

## 10. Legal Queries, Pair Margin, and Robust $\mathcal{B}^K$

Using the legal query metric $\nu = \frac{\sigma \sqrt{l}}{n} \sup_{\text{legal } Q} \|\Delta M^T c_Q\|$:
$$\nu_{\text{ref}} \ge \frac{\sigma \sqrt{l} a s_{\text{gate}}}{n\sqrt{n}} \frac{|\xi_j^T O_* \Delta M_N v|}{\|\xi_j\|_\infty}.$$
Since $h \ge 0.39\sqrt{n}/K$ and $\|\xi_j\|_\infty \le 1/\sqrt{h}$, the prefactor is $> 0.003 n^{-3/4} / \sqrt{K}$.
For an antipodal unit pair $\theta - (-\theta) = 2\theta$, at least one coordinate satisfies:
$$|\Delta \text{read}_j| \ge \frac{2}{\sqrt{K}} \sigma_{\min}(A_{\text{actual}}) \ge \frac{2}{\sqrt{K}} \beta \delta W \sigma_{\min}(J_K).$$
Thus:
$$\nu_{\text{ref}} > \frac{0.003}{\sqrt{K}} n^{-3/4} \cdot \frac{2}{\sqrt{K}} (0.97) (10^{-30}) (10^{60} n^{3/4}) \sigma_{\min}(J_K) = \frac{5.82 \cdot 10^{27}}{K} \sigma_{\min}(J_K) > 10^{17} \gg 1000.$$
Subtracting the dense query charge $\le 8 \cdot 10^{-9}$:
$$\text{actual pair distance} > 1000, \quad \text{half-margin} > 500 \quad \text{at } \epsilon = 0.001.$$
Borsuk–Ulam on the continuous $\mathcal{B}^K$ section guarantees robust continuous memory dimension $D \ge K$.

---

## 11. Floors, Envelopes, All-Integer Range, and Resource Bounds

At all $n \ge 10^{1000}$:
$$m \le \frac{C p}{2} \le 0.5 \sqrt{n}, \quad W = \lceil 10^{60} n^{3/4} \rceil, \quad L = \lceil 1000 \log n \rceil.$$
$$mT < 10^{60} n^{5/4} = o(n^{3/2}),$$
$$\|X_{\text{raw}}\|_2 \le 2\sqrt{m(T+2)+1} < 3 \cdot 10^{30} n^{5/8}.$$
All monotone error envelopes decrease strictly with $n$, confirming the proof for every integer $n \ge 10^{1000}$.

---

## 12. Growing $K$ and the Dilution Barrier Theorem

### Proof of Theorem 3
Consider an arbitrary time-varying filter bank with $K$ donors and $S \ge K+1$ survivors in a shared corridor:
1. **Probe Normalization:** Any unit witness $v = \sum c_j v_j$ in the orthonormal probe space satisfies $\sum c_j^2 = 1$. The driving vector $f$ has donor components $|f_{D, j}| \le \frac{1}{\sqrt{2K}}$.
2. **Common-Mode Coupling:** In $P = I - \frac{1}{C}\mathbf{1}\mathbf{1}^T$ with $C = K + S \ge 2K + 1$, the off-diagonal coupling entry is $|P_{cj}| = 1/C \le \frac{1}{2K+1}$.
3. **Survivor Read Norm:** Orthonormal reads $Q Q^T = I_K$ satisfy $\sum_{c=1}^K |q_{c, i}|^2 \le 1$.
4. **Frobenius Bound:** By Cauchy-Schwarz on the Fubini kernel:
   $$|J_{cj}| \le \frac{|f_{D, j}|}{C} \cdot \left| \int_0^1 \psi_c(u) F_j(u) \, du \right| \le \frac{1}{\sqrt{2K}} \frac{1}{2K} \cdot \|\psi_c\|_{L^2} \|F_j\|_{L^2}.$$
   Since $\|\psi_c\|_{L^2} \le O(\eta)$ and $\|F_j\|_{L^2} \le 1/2$:
   $$\|J\|_F^2 = \sum_{c=1}^K \sum_{j=1}^K |J_{cj}|^2 \le K \cdot K \cdot \left( \frac{O(\eta)}{K^{3/2}} \right)^2 = \frac{O(\eta^2)}{K}.$$
   Since $\|J\|_F^2 \ge K \sigma_{\min}(J)^2$:
   $$\sigma_{\min}(J_K) \le \frac{\|J\|_F}{\sqrt{K}} \le \frac{O(\eta)}{K} = O(K^{-1}).$$
   Hence $\alpha \ge 1.0 > 0.5$ is a universal upper bound.

5. **Walsh Code Oscillation:** For Walsh codes, $F_j(u) = \int_0^u s w_j(s) \, ds$ oscillates at frequency $K$, giving $\|F_j\|_{L^2} = \Theta(1/K)$. This multiplies $J$ by an additional $1/K$, establishing:
   $$\sigma_{\min}(J_K) = \Theta\left( \frac{\eta}{K^{5/2}} \right) \implies \alpha = 5/2.$$

### Dimension Consequence
In the query metric, splitting physical support yields prefactor $\sim n^{-3/4} / \sqrt{K}$.
Total pair distance scales as $\nu \sim W n^{-3/4} K^{-3}$.
With $mT = o(n^{3/2})$, $W \le n$, so requiring $\nu \ge 2\epsilon = 0.002$ forces:
$$K^3 \le O(n^{1/4}) \implies K \le O(n^{1/12}).$$
Since $1/12 \approx 0.0833 < 3/16 = 0.1875$, this route **does not** beat $\beta = 3/16$.

---

## 13. Summary and Review Target for Independent Reviewers

Independent hostile reviewers should verify:
1. The Fubini reduction of the temporal transfer operator to $M_{cj} = \int_0^1 \psi_c(u) F_j(u) \, du$ (Section 5).
2. The exact positive definiteness and singular values of $G_3$ and $G_4$ in `checks.py` (Section 6).
3. The proof of the Dilution Barrier Theorem (Section 12), which rigorously rules out $\alpha < 1/2$ for shared corridors.
