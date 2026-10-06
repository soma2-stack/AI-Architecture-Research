# Scoped Failures and Proved Obstructions

Gemini, 2026-10-06. THEORY ONLY.

These classifications concern the investigation of time-varying near-critical filter banks and their generalization to growing $K$. No historical report or accepted premise is altered.

---

## 1. FAILED: Constant-Rate Filter Bank Extension for $K \ge 3$

- **Mechanism:** Using constant rates $\lambda_c = c \cdot \eta$ on all survivor cohorts $S_1, \dots, S_{K+1}$.
- **Obstruction:** In constant-rate filters, the survivor impulse response to the common corridor drive $q(s)$ is $\exp(-\lambda_c(1-s))$. When all rates are bounded within $[0, 4\eta]$, these functions are uniformly approximated by degree-$(K-1)$ polynomials with remainder bounded by $2 e^\ell \ell^K / K!$. After spatial centering, degree zero cancels, leaving at most $K-1$ degrees of freedom.
- **Consequence:** For $K=3$, the 3x3 derivative determinant cancels through order 3 in $\eta$, dropping to order $\eta^{10} \approx 10^{-60}$, with $\sigma_{\min} \sim \eta^8 \approx 10^{-48}$. For $K=4$, it collapses to $O(\eta^{18}) \approx 10^{-108}$.
- **Status:** **PROVED FACTORIALLY ILL-CONDITIONED.** Constant-rate survivor filters cannot provide a viable multi-channel transfer for growing $K$.

---

## 2. FAILED / OBSTRUCTED: Achieving $\alpha < 1/2$ via Shared-Corridor Temporal Filter Banks

- **Target Claim:** A complete protected $K$-channel transfer with minimum singular value scaling as $\sigma_{\min}(J_K) \ge c \cdot \kappa / K^\alpha$ with $\alpha < 1/2$.
- **First Load-Bearing Obstruction: Frobenius Probe Normalization ($K^{-1/2}$)**
  To witness the gradient lower bound using a single fixed unit witness probe $v$ within an orthonormal $K$-probe space $V = [v_1, \dots, v_K]$ with $V^T V = I_K$, Cauchy-Schwarz requires:
  $$v = \frac{1}{\sqrt{K}} \sum_{j=1}^K v_j \implies f_{D, j} = \frac{1}{2\sqrt{K}}.$$
  The driving amplitude into each donor cohort is diluted by $1/\sqrt{K}$.
- **Second Load-Bearing Obstruction: Common-Mode Coupling Dilution ($K^{-1}$)**
  In a shared corridor containing $K$ donors and $S \ge K+1$ survivors ($C \ge 2K+1$ total cohorts), the only spatial communication between cohorts is the mean-centering projection $P = I_C - \frac{1}{C}\mathbf{1}\mathbf{1}^T$. Off-diagonal coupling entries are:
  $$|P_{cj}| = \frac{1}{C} \le \frac{1}{2K+1} = O(K^{-1}).$$
  Every transfer from donor $j$ to survivor $c$ must cross this rank-1 common-mode channel, scaling the transferred amplitude by $1/C \le 1/(2K+1)$.
- **Third Load-Bearing Obstruction: Bessel Energy Bound on Temporal Transfer ($K^0$)**
  For any orthonormal survivor readout matrix $Q$ ($Q Q^T = I_K$), Bessel's inequality on the temporal inner products bounds the Frobenius norm of the Jacobian by:
  $$\|J\|_F^2 = \sum_{c=1}^K \sum_{j=1}^K |J_{cj}|^2 \le \frac{\eta^2}{K}.$$
  Since $\|J\|_F^2 \ge K \cdot \sigma_{\min}(J)^2$, this proves the universal upper bound:
  $$\sigma_{\min}(J_K) \le \frac{\eta}{K} = O(K^{-1}).$$
- **Consequence:** For **any** legal time-varying filter bank in this shared corridor, the decay exponent must satisfy:
  $$\alpha \ge 1 > 1/2.$$
  With Walsh/Hadamard temporal codes, integrating the frequency-$K$ oscillations introduces an additional factor of $1/K$, yielding $\sigma_{\min}(J_K) = \Theta(\eta / K^{5/2})$, i.e., $\alpha = 5/2$.
- **Status:** **PROVED OBSTRUCTED.** The target scaling $\alpha < 1/2$ is impossible in the shared-corridor architecture with Frobenius-orthonormal parameter probes.

---

## 3. FAILED: Improving the Dimension Exponent Beyond $\beta = 3/16$

- **Target Claim:** Using growing $K$ in time-varying filter banks to prove $D \ge n^\beta$ with $\beta > 3/16$.
- **Obstruction:** With $\sigma_{\min}(J_K) \sim \Theta(\eta / K^{5/2})$, the total state displacement across $W$ steps is $\delta W \frac{\eta}{K^{5/2}}$.
  In the legal query metric, splitting $4m$ physical sites among $C \approx 2K$ cohorts reduces each cohort's support to $h \sim \sqrt{n}/K$.
  The query normalization prefactor scales as $n^{-3/4} / \sqrt{K}$.
  Thus, the complete antipodal distance scales as:
  $$\nu \sim n^{-3/4} K^{-1/2} \cdot W \cdot K^{-5/2} = W n^{-3/4} K^{-3}.$$
  Under the coordinate-time budget $m T = o(n^{3/2})$, we have $W \le n^{3/2}/m \sim n$.
  Requiring $\nu \ge 2\epsilon = 0.002$ forces:
  $$K^3 \le O(W n^{-3/4}) \le O(n^{1/4}) \implies K \le O(n^{1/12}).$$
- **Consequence:** The maximum achievable robust dimension is $D = O(n^{1/12})$.
  Since $1/12 \approx 0.0833 < 3/16 = 0.1875$, this route fails to improve the existing verified frontier $\beta = 3/16$.
- **Status:** **PROVED UNCOMPETITIVE WITH MULTI-STAGE HADAMARD WRITES.**

---

## 4. WHAT SURVIVED: Fixed $K=3$ and Fixed $K=4$ Theorems

- Time-varying Walsh survivor filter banks and repeated Walsh donor codes break the factorial collapse and yield $\sigma_{\min}(J_3) \approx 8.0 \cdot 10^{-10}$ and $\sigma_{\min}(J_4) \approx 2.9 \cdot 10^{-10}$.
- For fixed $K=3$ and $K=4$, the large coefficient in $W = \lceil 10^{60} n^{3/4} \rceil$ produces an actual legal query pair distance $> 10^{45} \gg 1000$ and half-margin $> 500$ at $\epsilon = 0.001$.
- These are verified as scoped finite theorems, not asymptotic dimension frontier improvements.
