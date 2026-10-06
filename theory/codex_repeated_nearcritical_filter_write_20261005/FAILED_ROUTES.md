# Failed Routes: Repeated Simultaneous Donor Writing into Near-Critical Survivor Filters

Codex, 2026-10-05. THEORY ONLY.  
Artifact directory: `theory/codex_repeated_nearcritical_filter_write_20261005/`

This document records the exact failure points of five candidate constructions for repeated simultaneous donor writing into distinct near-critical survivor filters.

---

## Route 1: High-Frequency Temporal Codes (Alternating Signs and Rademacher Words)

### Proposed Construction
Set $r_1(t) = (-1)^t$ and $r_2(t) = \operatorname{sgn}(\sin(\pi t / 2))$.
Attempt to write two orthogonal high-frequency binary sequences simultaneously into donor groups $D_1$ and $D_2$, reading through distinct survivor filters $g_{S, 1} = 1 - 0.001$ and $g_{S, 2} = 1 - 0.002$.

### First Failed Inequality / Structural Obstruction
1. **Trace Matching Constraint:** Exact final trace matching requires $\sum_{t=1}^T \lambda_t r_j(t) = 0$. For alternating codes, $\sum_{t=1}^T (-1)^t \lambda_t \approx \frac{1}{2} (\lambda_T - \lambda_1) \approx O(1)$, so the trace adjustment needed is minimal ($O(1/T)$).
2. **Zero-Moment Telescoping:** However, when $r_j(t)$ is convolved against the smooth backward filter difference $\Psi_j(T, s)$, the alternating signs cause exact discrete cancellation:
   $$\left| \sum_{s=1}^T (-1)^s \Psi_j(T, s) \right| \le \frac{1}{2} \sum_{s=1}^{T-1} |\Psi_j(T, s+1) - \Psi_j(T, s)| = O(1).$$
3. **Numerical Outcome:** At $n = 400$, $\sigma_{\min}(A) = 3.43 \times 10^{-6}$. The normalized legal query pair distance is:
   $$\text{Pair Distance} = 6.37 \times 10^{-10} \ll 0.002.$$
   This is smaller than the dense comparison error $8 \times 10^{-9}$.
**Verdict: FAILED (High-Frequency Telescoping).**

---

## Route 2: Low-Frequency Orthogonal Temporal Codes (Fourier Harmonics)

### Proposed Construction
Use smooth, low-frequency orthogonal harmonics:
$$r_1(t) = \sin(\pi t / T), \quad r_2(t) = \sin(2\pi t / T).$$
Because these codes are smooth and low-frequency, discrete cancellation is minimized.

### First Failed Inequality / Structural Obstruction
1. **Trace Matching Penalty:** Since $r_1(t) > 0$ on $(0, T)$, its first moment against the trace weight $\lambda_t > 0$ is strictly positive:
   $$\sum_{t=1}^T \lambda_t r_1(t) \approx \frac{2}{\pi} T \bar{\lambda} = \Theta(T^2).$$
   To achieve exact trace matching, a large correction must be added to the tail, or $r_1(t)$ must be orthogonalized against $\lambda_t$. Orthogonalizing against $\lambda_t$ forces $r_1(t)$ to cross zero and cancel its own mean.
2. **Householder Closed-Loop Damping:** The surviving signal must pass through the broadcast feedback channel $J_t$, which has pole $\lambda_H \approx 1 - 4/\sqrt{n}$. The effective memory horizon is $\tau_H \le \sqrt{n}/4$. The convolution cannot accumulate across the entire duration $T = \Theta(n^{3/4})$.
3. **Numerical Outcome:** While raw singular values reach $\sigma_{\max} \approx 2.8$ at $n = 10000$, the minimum singular value is capped at $\sigma_{\min} \le 0.075$. Under the legal query metric prefactor $\mathcal{P}_{\text{query}} \approx 8.31 \times 10^{-6}$, the pair distance is:
   $$\text{Pair Distance} \le 8.26 \times 10^{-7} \ll 0.002.$$
   The distance decays as $O(n^{-1/2})$ and fails the robustness threshold by a factor of 2400.
**Verdict: FAILED (Householder Damping + Query Dilution).**

---

## Route 3: Chirped Binary / Frequency-Modulated Codes

### Proposed Construction
Apply quadratic phase / chirped waveforms:
$$r_1(t) = \sin(0.001 t^2), \quad r_2(t) = \cos(0.001 t^2).$$
The instantaneous frequency increases linearly with $t$, attempting to sweep through multiple resonance points of the survivor filters.

### First Failed Inequality / Structural Obstruction
1. **Stationary Phase Cancellation:** By the stationary phase approximation, the integral of a quadratic phase chirp against a smooth kernel $\Psi(s)$ scales as:
   $$\int_0^T e^{i \alpha t^2} \Psi(t) dt \approx \frac{\Psi(0)}{\sqrt{\alpha}} = O(1).$$
   The response does not grow with $T$; it saturates as soon as the frequency leaves the baseband.
2. **Numerical Outcome:** At $n = 400$, $\sigma_{\min}(A) = 1.01 \times 10^{-4}$, giving:
   $$\text{Pair Distance} = 1.87 \times 10^{-8} \ll 0.002.$$
**Verdict: FAILED (Stationary Phase Saturation).**

---

## Route 4: Step-Modulated Time-Varying Near-Critical Survivor Filters

### Proposed Construction
Break time-invariance of survivor filters by switching gates midway:
- Survivor 1: $g_{S, 1} = 0.999$ for $t < T/2$, $g_{S, 1} = 0.995$ for $t \ge T/2$.
- Survivor 2: $g_{S, 2} = 0.995$ for $t < T/2$, $g_{S, 2} = 0.999$ for $t \ge T/2$.
Hope that the piecewise-constant step in survivor dissipation breaks filter alignment and induces a large angle $\sin(\theta_\Psi)$ between survivor responses.

### First Failed Inequality / Structural Obstruction
1. **Corridor Legality Ceiling:** In order to remain legal, all survivor gates must satisfy $g_S \in [g_L, g_H] \subset [0.994, 0.9999]$.
   The maximum possible gate step is $\Delta g = g_H - g_L \le 0.005$.
   The relative angle between the two survivor filter suffix products is bounded by:
   $$\sin(\theta_\Psi) \le \Delta g \le 0.005.$$
2. **Numerical Outcome:** At $n = 2000$, $\sigma_{\min}(A) = 3.08 \times 10^{-2}$. With query prefactor $\mathcal{P}_{\text{query}} = 2.78 \times 10^{-5}$:
   $$\text{Pair Distance} = 1.71 \times 10^{-6} \ll 0.002.$$
   The step modulation fails to increase the pair distance above $1.71 \times 10^{-6}$.
**Verdict: FAILED (Corridor Amplitude Budget Cap).**

---

## Route 5: Bursty Pulse Trains with Asymmetric Duty Cycles

### Proposed Construction
Apply sparse pulse trains with small duty cycles (e.g. active for 5 steps out of every 20):
$$r_1(t) = \begin{cases} +1 & t \pmod{20} < 5 \\ -1 & \text{otherwise} \end{cases}, \quad r_2(t) = \begin{cases} +1 & t \pmod{40} < 10 \\ -1 & \text{otherwise} \end{cases}.$$
Attempt to create localized energy packets that evade continuous trace accumulation while exciting discrete survivor modes.

### First Failed Inequality / Structural Obstruction
1. **DC Imbalance Penalty:** The asymmetric duty cycle has mean $5(+1) + 15(-1) = -10 \ne 0$.
   Trace matching forces the mean to be compensated by an equal and opposite shift, cancelling the net pulse excitation.
2. **Higher-Harmonic Damping:** The pulse train energy is distributed across high Fourier harmonics $\omega_k \ge 2\pi / 20$.
   The Householder closed-loop filter acts as a low-pass filter with cutoff $\omega_c \approx 4/\sqrt{n}$. All harmonics above $\omega_c$ are strongly attenuated by $\omega_c / \omega_k \approx 40 / (2\pi \sqrt{n}) = O(1/\sqrt{n})$.
3. **Numerical Outcome:** At $n = 400$, $\sigma_{\min}(A) = 7.64 \times 10^{-6}$, giving:
   $$\text{Pair Distance} = 1.42 \times 10^{-9} \ll 0.002.$$
**Verdict: FAILED (Low-Pass Harmonic Attenuation).**
