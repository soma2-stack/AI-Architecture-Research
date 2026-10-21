# Status — claude_dense_transfer_20261020

| Item | Status | Independent check |
|---|---|---|
| Exact contract: prescribed `R = alpha(R0 + eta 11^T/n)`, actual inputs, metrics | from sources (PR #29 Lemma D1 Codex-verified) | Codex (PR #29) |
| Lemma 1.1 field identity / zero-sum invariance / perturbation norms | PROVED | D2 Codex-verified; (c), (d) pending |
| Lemma 2.1D exact locality and endpoints, every alpha and eta | PROVED; exact at 60 digits | pending |
| Lemma 2.2D legality `<= .4563`, actual support `m = 3`, dense ranges | PROVED; rational certificate | pending |
| Lemma 2.3D dense front gate | PROVED | pending |
| Lemma 3.1D all PR #34 `B'`-results transfer (gate facts G1–G8) | PROVED | pending |
| Lemma 3.2D dense credit correction `<= 1.5e-8 c_*` per column | PROVED | pending |
| **Theorem 6.1D** robust `D >= n^(1/4)/161`, `m = 3`, `mT = 1.5 n`, actual dense `d_F,E`, `n >= 1e18` | **PROVED (author)** | **pending — main audit target** |
| **Cor. 6.2D** original Lemma M false for the prescribed dense matrix | **PROVED (author)** | **pending** |
| Prop. 5.1 transfer to the full fixed-feature `d_F` and the full R/W/b metric (lower bounds only) | PROVED; backprop identity to `1e-12` | pending |
| Prop. 6.1 one-step merge obstruction (m-generic matrices; different problem) | PROVED | pending |
| Prop. 7.2 dense transfer principle | PROVED | pending |
| Lemma 9.1 saturation code | PROVED | pending |
| **Theorem 9.2** robust `D = floor(floor(n^(1/3))/2400)`, `m = 3`, `mT = 1.5n`, `n >= 1e16`, R0 and dense | **PROVED (author); exact certificate** | **pending** |
| Cor. 9.3 Lemma M fails for `n >= 1e63` (`C <= 1e12`) | PROVED (author) | pending |
| Cor. 9.4 Theorem M(d) order sharp at constant width | PROVED (author) | pending |
| Remark 9.5 general width `(mT)^(4/3)/n` | ANALYSIS | — |
| Mechanism cannot reach `D = Omega(n)` below the barrier | ANALYSIS (Theorem M); rigorous no-go OPEN (needs Lemma M_rest) | — |
| Original problem (`D = Omega(n)`, `mT = o(n^(3/2))`, full `d_F`, dense) | **OPEN** | — |

PR #34's folder and certificates are unchanged. No merge was performed. AGENTS.md and the
restricted notebooks were neither read nor edited.
