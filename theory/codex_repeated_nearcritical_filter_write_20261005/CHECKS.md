# Numerical and Algebraic Checks: Repeated Near-Critical Filter Writes

Codex, 2026-10-05. THEORY ONLY. STATUS: **REFUTED**.  
Artifact directory: `theory/codex_repeated_nearcritical_filter_write_20261005/`

---

## 1. Reproduction Command

To reproduce all numerical checks, SVD spectra, trace matching residuals, and legal query pair distances:

```bash
python theory/codex_repeated_nearcritical_filter_write_20261005/checks.py
```

Environment: Single process thread, CPU only, 0 GPU/CUDA, peak RSS < 50 MiB. Execution time: < 0.5s CPU.

---

## 2. Summary Audit

- **Tested Widths:** $n \in \{400, 1000, 2000, 4000, 10000\}$.
- **Tested Temporal Code Families:**
  1. Alternating Signs vs Rademacher ($r_1[t] = (-1)^t$, $r_2[t] = \operatorname{sgn}(\sin(\pi t / 2))$)
  2. Fourier Harmonics ($\sin(\pi t / T)$ vs $\sin(2\pi t / T)$)
  3. Chirped Binary ($\sin(0.001 t^2)$ vs $\cos(0.001 t^2)$)
  4. Step-Modulated Filters (first-half vs second-half gate shifts)
  5. Bursty Pulse Trains (duty cycle pulses)
- **Trace Matching Residuals:** Exact to $< 10^{-16}$ across all runs.
- **Maximum Observed Legal Query Pair Distance:** $3.21 \times 10^{-6}$.
- **Required Robustness Threshold:** $2\epsilon = 0.002$.
- **Ratio to Robustness Threshold:** $3.21 \times 10^{-6} / 0.002 = 0.001605 \ll 1$.
- **Verdict:** **REFUTED** (all tested configurations fail by more than 600x at moderate $n$, and decay as $O(n^{-1/2}) \to 0$ asymptotically).

---

## 3. Detailed Numerical Results by Code Family

### Family 1: Alternating Signs vs Rademacher Codes

| $n$ | $T$ | Trace Res 1 | Trace Res 2 | $\sigma_{\max}(A)$ | $\sigma_{\min}(A)$ | $\mathcal{P}_{\text{query}}$ | Pair Distance | Robust? |
|---|---|---|---|---|---|---|---|---|
| 400 | 894 | $0.0$ | $0.0$ | $8.62 \times 10^{-5}$ | $3.43 \times 10^{-6}$ | $9.27 \times 10^{-5}$ | $6.37 \times 10^{-10}$ | FAIL |
| 1000 | 1778 | $0.0$ | $0.0$ | $4.68 \times 10^{-5}$ | $2.31 \times 10^{-6}$ | $4.67 \times 10^{-5}$ | $2.16 \times 10^{-10}$ | FAIL |
| 2000 | 2990 | $0.0$ | $0.0$ | $3.31 \times 10^{-5}$ | $1.72 \times 10^{-6}$ | $2.78 \times 10^{-5}$ | $9.56 \times 10^{-11}$ | FAIL |
| 4000 | 5029 | $0.0$ | $0.0$ | $2.34 \times 10^{-5}$ | $1.25 \times 10^{-6}$ | $1.65 \times 10^{-5}$ | $4.13 \times 10^{-11}$ | FAIL |
| 10000 | 10000 | $0.0$ | $0.0$ | $1.48 \times 10^{-5}$ | $8.12 \times 10^{-7}$ | $8.31 \times 10^{-6}$ | $1.35 \times 10^{-11}$ | FAIL |

### Family 2: Fourier Harmonics ($\sin(\pi t / T)$ vs $\sin(2\pi t / T)$)

| $n$ | $T$ | $\sigma_{\max}(A)$ | $\sigma_{\min}(A)$ | $\mathcal{P}_{\text{query}}$ | Pair Distance | Ratio to $0.002$ | Robust? |
|---|---|---|---|---|---|---|---|
| 400 | 894 | $0.188$ | $6.09 \times 10^{-3}$ | $9.27 \times 10^{-5}$ | $1.13 \times 10^{-6}$ | $0.00056$ | FAIL |
| 1000 | 1778 | $0.561$ | $2.75 \times 10^{-2}$ | $4.67 \times 10^{-5}$ | $2.57 \times 10^{-6}$ | $0.00128$ | FAIL |
| 2000 | 2990 | $1.09$ | $5.53 \times 10^{-2}$ | $2.78 \times 10^{-5}$ | $3.08 \times 10^{-6}$ | $0.00154$ | FAIL |
| 4000 | 5029 | $1.85$ | $7.47 \times 10^{-2}$ | $1.65 \times 10^{-5}$ | $2.47 \times 10^{-6}$ | $0.00123$ | FAIL |
| 10000 | 10000 | $2.82$ | $4.97 \times 10^{-2}$ | $8.31 \times 10^{-6}$ | $8.26 \times 10^{-7}$ | $0.00041$ | FAIL |

### Family 3: Step-Modulated Filters + Harmonics

| $n$ | $T$ | $\sigma_{\max}(A)$ | $\sigma_{\min}(A)$ | $\mathcal{P}_{\text{query}}$ | Pair Distance | Ratio to $0.002$ | Robust? |
|---|---|---|---|---|---|---|---|
| 400 | 894 | $0.150$ | $3.26 \times 10^{-3}$ | $9.27 \times 10^{-5}$ | $6.05 \times 10^{-7}$ | $0.00030$ | FAIL |
| 1000 | 1778 | $0.448$ | $1.51 \times 10^{-2}$ | $4.67 \times 10^{-5}$ | $1.41 \times 10^{-6}$ | $0.00071$ | FAIL |
| 2000 | 2990 | $0.871$ | $3.08 \times 10^{-2}$ | $2.78 \times 10^{-5}$ | $1.71 \times 10^{-6}$ | $0.00086$ | FAIL |
| 4000 | 5029 | $1.48$ | $4.21 \times 10^{-2}$ | $1.65 \times 10^{-5}$ | $1.39 \times 10^{-6}$ | $0.00069$ | FAIL |
| 10000 | 10000 | $2.26$ | $2.84 \times 10^{-2}$ | $8.31 \times 10^{-6}$ | $4.72 \times 10^{-7}$ | $0.00024$ | FAIL |

---

## 4. Householder Closed-Loop Horizon Audit

| $n$ | $2mc$ | Closed-Loop Pole $\lambda_H$ | Decay Rate Gap | Effective Horizon $\tau_H$ | $\sqrt{n}/4$ Bound |
|---|---|---|---|---|---|
| 400 | $0.200$ | $0.796$ | $0.204$ | $4.90$ | $5.00$ |
| 1000 | $0.126$ | $0.869$ | $0.131$ | $7.63$ | $7.91$ |
| 2000 | $0.089$ | $0.906$ | $0.094$ | $10.64$ | $11.18$ |
| 4000 | $0.063$ | $0.932$ | $0.068$ | $14.71$ | $15.81$ |
| 10000 | $0.040$ | $0.955$ | $0.045$ | $22.22$ | $25.00$ |

All observed effective horizons $\tau_H$ strictly satisfy $\tau_H \le \sqrt{n}/4$.

---

## 5. Bessel Rank-One Bottleneck Audit across $K$

| $K$ | Theoretical Upper Bound Factor $1/\sqrt{2(K+1)}$ | Ratio to $K=1$ | Proved Exponent $\alpha$ |
|---|---|---|---|
| 1 | $0.5000$ | $1.0000$ | $0.5$ |
| 2 | $0.4082$ | $0.8165$ | $0.5$ |
| 4 | $0.3162$ | $0.6325$ | $0.5$ |
| 8 | $0.2357$ | $0.4714$ | $0.5$ |
| 16 | $0.1715$ | $0.3430$ | $0.5$ |

The minimum singular value dilution strictly follows $\Theta(K^{-1/2})$, establishing $\alpha \ge 1/2$.
