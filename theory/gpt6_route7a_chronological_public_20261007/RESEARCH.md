# Route 7A: replacing toy bath/front gates with exact chronological public-state gates

Date: 2026-10-07 (US Eastern). Author: GPT-6.
**Status: FINITE REFERENCE-MODEL EXPERIMENT / AUTHOR FINDINGS / PENDING INDEPENDENT REVIEW.**
The target \(D=\Omega(n)\) with \(mT=o(n^{3/2})\) remains **OPEN**.

## 0. Finding

The previous [full-feedback probe](../gpt6_route7a_fullH_spectrum_20261007/) set every non-donor public gate to 1 and employed toy survivor masks. This experiment replaces those gates with **the actual chronological frozen-reference tanh evolution on every undriven memory coordinate**, implements balanced public Walsh capture masks, and checks the common final endpoint of two antipodal donor-control histories.

For \(n\in\{16384,32768,65536\}\), the histories reach the same endpoint within \(\approx 2\cdot10^{-16}\). At \(n=65536,m=32,R=16\), the gate histories differ **only** at controlled donor coordinates to \(\approx2.22\cdot10^{-16}\), directly checking that the bath/front and public survivor gates are common. The maximum required driven raw input in the finite tests is below 0.12, versus the inherited 0.5 budget. This checks the sparse reference model, not the actual dense-matrix perturbation.

In contrast with the earlier all-public-gates=1 surrogate, for these schedules the observed full-\(H\) feedback readout is **weaker than** the local \(L\) readout on optimized one-step queries. It grows with R, but remains extremely small. This is a model-dependent finite-size observation. No proof of a universal feedback upper bound or robust dimension limitation follows.

## 1. Actual frozen-reference state simulator

Use the inherited fixed-source memory model, with \(k=n/2,\ r=k-1,\ d=n/4,\ a=1-1/n\), \(O_*=C+\mathbf1u^T+e_1v_H^T\), memory bias \(b_0=.05\), and \(G_t=\mathrm{diag}(1-h_t^2)\).

The reference state \(h_t\in\mathbb R^r\) evolves on **every undriven coordinate** by
\[
h_t(i)=\tanh\bigl(b_0+a(O_*h_{t-1})_i\bigr).
\]
The driven rows are set to a prescribed value \(\pm\sqrt{1-g}\) using the inverse-lift input
\[
x_t(i)=\operatorname{atanh}(h_t(i))
       -b_0-a(O_*h_{t-1})_i.
\]
Thus the resulting gates are read from the actual state \(1-h_t^2\), not assigned arbitrary nondriven baselines. We begin after preparation at \(h_0(i)=\tanh(b_0)\) on nondriven rows; memory coordinate 0 and the public source block are omitted from the *reduced* sensitivity recurrence because the inherited frozen \(O\) fixes coordinate 0. The probe takes \(\sigma=.05\) for its fixed-feature query normalization, rather than numerically solving for the exact public source root \(\sigma\in(.0499,.051)\).

### Geometry and balances

For \(N=L+3R+1,\ L=\lceil\sqrt{nR}\rceil,\ S=m+N+4,\ A=2S,\ B=5S\), the \(m\) moving donor groups at \(A+1+i+t\), \(B+1+i+t\) carry \(+\beta_i(t)\); the two off-cycle stationary compensators carry \(-\beta_i(t)\). Hence the four-site donor state sum is exactly zero for each group and every time step. Precharge uses \(g_H=.99999\); the write uses \(d_1=.9975+10^{-4}x_i\), middle high, and Astra's exact trace-matching \(d_3\); reset sets all four donor sites to the same public \(\tanh(b_0)\). The private controls are \(x_i=\pm1\) in every stage.

For additional **PUBLIC** survivor capture rows, two moving blocks at \(3S+1+i+t\) and \(6S+1+i+t\) are paired with opposite signs; their magnitude uses \(g_H\) or \(g_L=.995\). At capture stage \(j\) (0-based), the low-group mask is the balanced Walsh parity
\[
\chi_{j+1}(i)=(-1)^{\operatorname{popcount}(i\mathbin{\&}(j+1))},
\]
where \(m\) is a power of 2 and \(1\le j+1\le R<m\). These masks are distinct and half-low. Public survivor inputs are fully charged to the finite input history; no private survivor controls are introduced. Public masks are not a proof of an independent protected readout.

The script checks the no-wrap condition \(7S+m+N<d\). **It does not meet the stronger accepted asymptotic corridor condition \(S\le d/100\) at these finite widths.** Therefore these numbers are diagnostic finite reference histories, not instances already certified by the published all-width corridor theorem. They cannot by themselves certify a frozen **dense** family section.

## 2. Exact full-feedback sensitivity and future query

For each private history, the script reads its actual gates \(G_t\), then evaluates \(M_t=G_t(aO_*M_{t-1}+I)\) matrix-free. The transpose is propagated backwards, and the local version \(L_t=G_t(aCL_{t-1}+I)\) is evaluated with the same gates. The private feedback is \(H_t=M_t-L_t\); it is **never replaced by a Born truncation or an external prescribed \(J_t\)**. All chronological front and bath gates, including exceptional highly saturated front gates, enter every factor of \(G_t\).

For one-step future queries, optimize over the legal box
\[
g_i\in[g_{\mathrm{lo}},g_{\mathrm{hi}}],
\quad g_{\mathrm{lo}}=\operatorname{sech}^2(.75),
\quad g_{\mathrm{hi}}=\operatorname{sech}^2(.25)
\]
via the inherited exact reference adjoint \(c_1(g)=aO_*^Tg/\sqrt n\). The score is the fixed-source reference distance
\[
\frac{\sigma\sqrt{n/2}}n
\left\| \Delta M_N^T c_1(g) \right\|_2
\]
and analogously for L and H. A simple extreme-vertex gradient ascent from all-high gates was run for two iterations; it is a **lower estimate on the best legal one-step query**, not a global optimum nor the all-horizon legal-query supremum. Each M/L/H mode gets a separately optimized query; the numbers cannot be summed or directly canceled as though they used the same query.

## 3. Results

### State/input legality checks

For the two all-positive/all-negative donor-control histories, with balanced public masks:

| n | m | R | N | max endpoint difference | max absolute driven/capture input |
|---:|---:|---:|---:|---:|---:|
| 16,384 | 4 | 2 | 189 | \(0\) | \(0.11765\) |
| 32,768 | 8 | 4 | 376 | \(5.56\cdot10^{-17}\) | \(0.11885\) |
| 65,536 | 16 | 8 | 750 | \(5.56\cdot10^{-17}\) | \(0.11968\) |
| 65,536 | 32 | 16 | 1073 | \(1.67\cdot10^{-16}\) | \(0.11974\) |
| 65,536 | 64 | 32 | 1546 | \(1.39\cdot10^{-16}\) | \(0.11991\) |

Separate finite checks showed full gate-vector differences outside donor coordinates below \(2.23\cdot10^{-16}\) (n=65536,m=32,R=16).

### Separate optimized legal one-step response magnitudes

These numerical scores are for a specific pair of control histories and found query gates, not a robust sphere.

| n | m | R | full-M score | local L score | feedback H score |
|---:|---:|---:|---:|---:|---:|
| 16,384 | 4 | 2 | \(7.7955\cdot10^{-8}\) | \(7.8979\cdot10^{-8}\) | \(4.9888\cdot10^{-9}\) |
| 32,768 | 8 | 4 | \(1.4989\cdot10^{-7}\) | \(1.5145\cdot10^{-7}\) | \(9.4936\cdot10^{-9}\) |
| 65,536 | 32 | 16 | \(6.4064\cdot10^{-7}\) | \(6.4970\cdot10^{-7}\) | \(5.7173\cdot10^{-8}\) |
| 65,536 | 64 | 32 | \(1.4079\cdot10^{-6}\) | \(1.4465\cdot10^{-6}\) | \(1.8003\cdot10^{-7}\) |
| 65,536 | 64 | 48 | \(1.7398\cdot10^{-6}\) | \(1.7934\cdot10^{-6}\) | \(2.2509\cdot10^{-7}\) |

The last \(R=48\) run (not part of the standalone default main script) uses the identical \`optimized_three(n=65536,m=64,R=48,iterations=2,restarts=1)\` function from the local development version, i.e. one all-high start and two iterations, as in the archived script. The full \(M\) score is still about 1,150 times smaller than .002. This does not bound the unknown supremum.

### Missing easy global contraction

An attempted improved proof by replacing each memory gate \(G_t\) with a uniform constant \(\|G_t\|\le g_H=.99999\) is **invalid**. Exceptional public front rows in this model sometimes have \(g_i=1-h_i^2>g_H\) and can get extremely close to 1. Scanning the histories yielded, for example:

| n | m | R | max observed gate |
|---:|---:|---:|---:|
| 16,384 | 4 | 2 | \(0.999999999765579\) |
| 32,768 | 8 | 4 | \(0.9999999999997222\) |
| 65,536 | 32 | 16 | \(0.9999999997913802\) |
| 65,536 | 64 | 32 | \(0.9999999999229368\) |

Hence do **not** deduce an \(R\)-uniform complete feedback bound from the numerical value of the designated high donor gate. A more structural front/bath contraction argument would be needed.

## 4. Interpretation and next obligation

Earlier idealized probes [fullH_spectrum](../gpt6_route7a_fullH_spectrum_20261007/) found \(H\) often stronger than \(L\). **With the true chronological public gates and paired public Walsh captures, the tested amplitudes reverse**, showing that bath/front modeling materially affects the answer. This is strong motivation to stop scaling the simplified surrogate as though it were a physical predictor.

The old review-verified local bound \(\nu_{\rm ref}(\Delta L_N)<0.00852\sqrt{m/n}\) remains a separate algebraic fact. Nothing here is a new global bound for \(\Delta H_N\); in particular all-positive versus all-negative controls need not be the hardest section. The complete \(R\to\infty\) Route 7A question, continuous robust antipodal width, dense perturbation, and stronger asymptotic corridor legality remain **OPEN**.

**Next actionable step:** Compare exact chronological full-H sensitivity against an explicit conservative legal-query *upper ledger* over all horizons (see inherited unpaired-corridor Section 9, Eq. (24)), or make a fully asymptotically admitted width-and-schedule evaluator by representing the public front sparsely to avoid storing \(O(nN)\) gate arrays. Then test adversarial control signs / multiple independently readable modes, rather than one aligned antipodal pair. Do not claim \(D\le m\) from any finite Jacobian spectra.

**Model provenance:** inherited reference identities from \`codex_unpaired_corridor_sensitivity_20261003\` §§1–3,9 and \`codex_holding_cost_attack_20261003\` §4. Astra's donor-neutral protocol is Eq. (25) in \`astra_route7a_reservoir_20261007/PROOF.md\` §11.1. Gemini's prior review validates the fixed-stage gate Lipschitz bound and the separate growing-R direct-channel estimate. Neither audit covers this new finite chronological experiment.
