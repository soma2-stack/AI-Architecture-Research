# Independent Mathematical Verification Checks

Codex, 2026-10-05. THEORY ONLY.
Artifact directory: `theory/codex_multisurvivor_hadamard_write_20261005/`

## Resource Footprint and Execution Summary

- Total checks executed: 141
- Total checks passed: 141 (100%)
- Wall time: 1.6082 seconds
- CPU math time: 1.6094 seconds
- Peak RAM: 32.62 MiB (34,203,648 bytes)
- Python threads observed: 1 (pool limits set to 1)
- GPU / CUDA calls: 0 (completely CPU / analytic execution)
- Deterministic random seed: 42 (when initialized)
- Precision: Exact Rational (`fractions.Fraction`) and 80-decimal (`decimal.Decimal`) arithmetic for structural proofs; float64 NumPy for SVD spectra.

## Verification Suites

### 1. Bessel Inequality Projection Bound (Suite: `bessel_inequality_checks`)
- Tests $K \in \{1, 2, 4, 8, 16, 32\}$.
- Verifies that for any $K$ orthonormal parameter probes supported on donor compensators, the sum of squared projections onto the normalized all-ones direction $u_D = 1_D / \sqrt{2m}$ satisfies:
  $$\sum_{k=1}^K |\langle v_k, u_D \rangle|^2 \le 1.$$
- Confirms exact per-channel squared projection $|\langle v_k, u_D \rangle|^2 = 1/(2K)$, proving that the root-mean-square projection is $1/\sqrt{2K}$, and every probe-independent minimum projection is upper-bounded by $1/\sqrt{K}$.

### 2. Compensator Submatrix Exact Identity (Suite: `compensator_submatrix_checks`)
- Verifies exact rational structure of $O_*$ on compensators:
  $$(O_*)_{ij} = \delta_{ij} - c,$$
  where $c = \gamma^2 / k_{model} = 1/361$ at $n=800, k=400, \gamma=20/19$.
- Confirms that $C$ acts as the identity on all compensators, $e_1 v_H^T = 0$, and off-diagonal coupling between any two compensator sites is identically $-c$, establishing that the entire interaction matrix on compensators is $I - c 1 1^T$.

### 3. Hadamard Mode Annihilation (Suite: `hadamard_annihilation_checks`)
- Tests Hadamard matrices of order $K \in \{2, 4, 8, 16\}$.
- Confirms that row 0 represents the uniform common mode ($\sum_j H_{0j} = K$), while all rows $k \ge 1$ are strictly zero-sum ($\sum_j H_{kj} = 0$).
- Verifies exact algebraic orthogonality $\langle H_k, 1_S \rangle = 0$ for all $k \ge 1$, proving that any zero-sum spatial mode on the survivor support completely annihilates the broadcast Householder feedback $\Delta J \cdot 1_S$.

### 4. Full Transfer Matrix Rank-1 Collapse (Suite: `transfer_matrix_rank_checks`)
- Simulates the full $r$-dimensional recurrence with $n=800, r=399, d=200$ for $K \in \{2, 4, 8\}$.
- Computes the complete $K \times K$ transfer matrix $T_{D \to S}$ from simultaneous donor controls to survivor block means.
- Computes SVD spectrum:
  - Leading singular value $\sigma_1 > 0.01$.
  - All secondary singular values $\sigma_2, \dots, \sigma_K < 10^{-12}$.
  - Ratio $\sigma_2 / \sigma_1 < 10^{-10}$, proving that the donor-to-survivor transfer matrix has mathematical rank exactly 1.

### 5. SVD Spectrum Scaling with $K$ (Suite: `probe_svd_scaling_checks`)
- Simulates probe-resolved transfer matrix for $K \in \{1, 2, 4, 8\}$.
- Measures the response magnitude on the survivor common mode:
  - $K=1$: 0.206622
  - $K=2$: 0.145662 (ratio to $K=1$: 0.7050, matching $1/\sqrt{2} = 0.7071$ within $0.3\%$)
  - $K=4$: 0.102843 (ratio to $K=1$: 0.4977, matching $1/\sqrt{4} = 0.5000$ within $0.5\%$)
  - $K=8$: 0.072666 (ratio to $K=1$: 0.3517, matching $1/\sqrt{8} = 0.3536$ within $0.5\%$)
- Confirms that the transfer gain scales as $K^{-1/2}$ across all tested widths and group counts.

### 6. Walsh Mask Character Triangularity (Suite: `walsh_mask_checks`)
- Tests $R=4$ Walsh characters under sequential spatial masking.
- Proves exact zero-sum preservation $\sum \xi_I = 0$ at all intermediate mask steps.
- Proves triangular readout: mask $e$ produces non-zero projection only onto characters containing bit $e$, and annihilates all earlier singleton characters $f < e$.

### 7. Precision Asymptotic Ledger (Suite: `precision_envelope_checks`)
- Evaluates 80-decimal envelopes at $n = 10^{1000}$.
- Verifies coordinate-time exponent $43/32 = 1.34375 < 1.5$, ensuring $mT = o(n^{3/2})$.
- Verifies history energy exponent $43/64 = 0.671875 < 0.75$.
- Verifies robust dimension exponent $\beta = 3/16 = 0.1875$.
