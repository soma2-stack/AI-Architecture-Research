# Route 7A: compressed chronological public bath and a geometry-admissible finite test

Author GPT-6; 2026-10-08.
**Status: AUTHOR-DERIVED EXACT REFERENCE COMPRESSION + FINITE NUMERICAL EXPERIMENT / PENDING INDEPENDENT REVIEW.**
The \(D=\Omega(n)\), \(mT=o(n^{3/2})\) robust-width target remains **OPEN**.

## 1. Reason for this checkpoint

The fixed-reference Route 7A chronological prototype previously stored \(O(nN)\) gate values. An independent continuation found TWO load-bearing simulation bugs (stale sensitivity trace during public precharge; compensator double-offset indexing) and repaired them. See [corrected results](../gpt6_route7a_chronological_public_20261007/CORRECTED_RESULTS_20261008.md) and [erratum](../gpt6_route7a_chronological_public_20261007/ERRATUM.md). After repairs, one-step full M signals of the all-positive/all-negative pair were only \(1.28\cdot10^{-9}\) at \(R=2\) through \(2.23\cdot10^{-8}\) at \(R=48\), much smaller than in the bugged simulations. None of those smaller tested widths satisfied the source's stronger \(S\le d/100\) condition.

This folder implements an **exact sparse representation of the frozen reference state and its full rank-two sensitivity** and evaluates the first instance satisfying both \(n\ge10^6\) and \(S\le d/100\). This is an infrastructure result plus experimental observation, not a feedback width theorem.

## 2. Exact sparse state recurrence

The reduced reference matrix is
\[
O_*=C+\mathbf1 u^T+e_1v_H^T,\quad
u^T=(\gamma/\sqrt{k})e_{d-1}^T-(\gamma^2/k)\mathbf1^T,\quad
v_H^T=(\gamma/\sqrt{k})\mathbf1^T,
\quad \gamma=(1-1/\sqrt{k})^{-1}.
\]
The accepted chronological reference tanh state is \(h_t=\tanh(b_0\mathbf1+aO_*h_{t-1}+x_t)\), with \(b_0=.05\); driven coordinates are inverse-lift overrides and all other inputs are zero.

Decompose \(h_t=q_t\mathbf1+\delta_t\), where \(q_t\) is a public uniform ordinary bath scalar and \(\delta_t\) is stored only on exceptional coordinates. Write
\[
s_{t-1}=r q_{t-1}+\mathbf1^T\delta_{t-1},
\qquad j_{t-1}=\frac{\gamma}{\sqrt{k}}h_{t-1}(d-1)-\frac{\gamma^2}{k}s_{t-1}.
\]
Then the bulk update is
\[
q_t=\tanh\left(b_0+a(q_{t-1}+j_{t-1})\right).
\]
For an exceptional old cycle row \(i<d-1\), its predecessor value is shifted to \(i+1\), and for exceptional off-cycle rows the predecessor remains at \(i\); at each destination, the new deviation is \(\tanh(b_0+a(h_{t-1}(i)+j_{t-1}))-q_t\). The exceptional front row 1 is updated separately from \(j_{t-1}+(\gamma/\sqrt k)s_{t-1}\). All private balanced donor overrides and PUBLIC paired survivor captures replace designated sparse entries by their exact \(\pm\sqrt{1-g}\) states.

The next gate is represented by one scalar baseline
\(g_t^{\rm bulk}=1-q_t^2\), plus sparse corrections
\[
g_t(i)-g_t^{\rm bulk}=-2q_t\delta_t(i)-\delta_t(i)^2.
\]
No private feedback is discarded. For a given legal future-query vector \(c\), the **complete** exact rank-two sensitivity transpose is still
\[
M_N^Tc=\sum_{t=1}^N G_tw_t,\quad
w_N=c,\quad w_{t-1}=aO_*^TG_tw_t.
\]
The sparse gate encoding reconstructs \(G_tw_t\) exactly up to floating rounding. This is *not* an approximation that fixes public gates or truncates \(J/B\). The forward operator \(Mv\) is likewise implemented sparsely for gradient-based future query optimization. Code: [sparse_geometry.py](sparse_geometry.py), [sparse_optimize.py](sparse_optimize.py).

### Main limitations

- This is a **reduced frozen reference** state/sensitivity evaluator. The actual dense perturbation \(R-R_0\), frozen auxiliary source dynamics, and exact public source root \(\sigma\in(.0499,.051)\) have not been numerically reconstructed. We use \(\sigma=.05\) as a query scale.
- Private controls are the prescribed trace-neutral gate-3 formula, with exact public/balanced masks and a final common reset. A continuous robust \(D=\Omega(n)\) section is not constructed.
- One-step legal query gate words form only a SUBSET of all legal futures. Query optimization by one tangent-plane vertex ascent iteration is not a global maximum.
- The sparse state list contains the full exceptional front (at most order N), moving private rows, public survivor remnants, and stationary compensators. No unjustified global \(\|G_t\|\le g_H\) bound is used.

## 3. Dense-vs-sparse cross-validation

Cross-check the sparse gate histories, final public hidden states, and full sensitivity \(M_N^Tc\) against the independently repaired dense chronological reference simulator:

| n | m | R | max per-coordinate gate error | final state error | adjoint relative error |
|---:|---:|---:|---:|---:|---:|
| 16,384 | 4 | 2 | \(4.44\cdot10^{-16}\) | \(3.89\cdot10^{-16}\) | \(2.46\cdot10^{-16}\) |
| 32,768 | 8 | 4 | \(4.44\cdot10^{-16}\) | \(4.16\cdot10^{-16}\) | \(1.15\cdot10^{-16}\) |
| 65,536 | 32 | 16 | \(4.44\cdot10^{-16}\) | \(3.33\cdot10^{-16}\) | \(2.67\cdot10^{-16}\) |

The independent sparse forward/transpose comparison gave relative errors \(2.47\cdot10^{-16}\) and \(8.59\cdot10^{-16}\), respectively, at n=16,384. These pass the stated \(10^{-12}\) regression threshold. Full reproducibility script: [sparse_compare.py](sparse_compare.py).

## 4. Geometry-admissible finite reference test

Use \(n=1{,}048{,}576,\ k=n/2,\ d=n/4,\ m=8,\ R=4,\ L=2048\) precharge steps. There are \(N=2061\) total sensitivity steps and \(S=m+N+4=2073\). Hence
\[
S=2073\le d/100=2621.44,\qquad n\ge10^6,
\]
and the stronger no-wrap inequality is satisfied.

For the pair of **all-positive versus all-negative controls**:
- Stages end with exactly matched local sensitivity traces at printed floating precision. Precharge trace \(\kappa_L=2025.1900306858902\).
- The reference hidden-state endpoints match to printed precision. The maximum driven/capture inverse-lift input amplitude is approximately 0.12070.
- Maximum exceptional state coordinates at any step: 2109, rather than storing all \(r=524287\) gate values per step.
- Legal all-high ONE-step query: observed reference full \(M\) distance \(2.02160177\cdot10^{-13}\).
- One legal box-vertex gradient-ascent step finds a stronger legal one-step query with distance \(5.36513276\cdot10^{-11}\), and about 99.9746% of query gates at their high endpoint.
- This is still about \(3.73\cdot10^7\) below the \(0.002\) target **for this found query**. The gap does not bound the global maximum.
- The control family here has \(mR=32\) inputs, nowhere near \(D=\Omega(n)\); it is a machinery check, not evidence about independent linear memory width.

The precharge/write path has \(mN=16488\) active-tuple steps in this finite example, trivially far below \(n^{3/2}\), but an isolated finite inequality is not a proof of little-o scaling with \(D=\Omega(n)\).

## 5. Next research obligation

The corrected chronological simulation and sparse evaluator should receive hostile independent review before scaling. Then:
1. Incorporate exact public source root, dense perturbation comparisons, and full permitted legal future queries as the inherited contract requires.
2. Extend geometry-admissible tests to **many** donor groups and independently varied controls, not just the 32-control aligned pair used here.
3. Develop a uniform robust-width theorem or explicit continuous \(D=cn\) antipodal section for **full \(H_N=M_N-L_N\)**; do not treat finite Jacobian rank or one query's amplitude as a theorem.

**Verdict: strict-geometry finite reference test works; full Route 7A theorem remains OPEN.**
