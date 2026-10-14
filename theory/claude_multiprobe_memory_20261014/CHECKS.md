# Checks — claude_multiprobe_memory_20261014

Two scripts, both CPU, each under a minute, float64. They verify **exact identities and
finite samples only**. The asymptotic theorems rest on the proofs.

## `python -I exp_identities.py` (torch autograd) → `exp_identities_result.json`

| Check | n, T | Result |
|---|---|---|
| Credit-matrix recursion (0.1) vs autograd, actual `R = R0 + H`, `||H|| = 4e-8/n^2` | 96, 25 / 160, 40 | rel. err. `5.6e-16` / `1.1e-15` |
| One-step legal query gradient `sigma sqrt(l) nu^T B_T` + direct term vs autograd | same | rel. err. `8.1e-16` / `1.6e-15` |
| Gather identity `O^T 1_k = sqrt(k) e_(d-1) + gamma e_0 - (gamma/sqrt k) 1_k` | k = 48 / 80 | `1.8e-15` / `1.2e-14` |
| Readout weights (Lemma 1.2), inline check in the session | k = 50, 400, 2000 | formula err. `<= 1.2e-13`; `max |nu_i| <= .339` off `{0, d-1}`; `nu_(d-1)/sqrt k >= .739` |

## `python -I exp_bus_checks.py` (numpy) → `exp_bus_checks_result.json` (added 2026-10-14)

| Check | Sizes | Result |
|---|---|---|
| A. Local skeleton (3.0): `O x = S x + 1 J(x) + (gamma/sqrt k) Sum(x) e_1`, `x_0 = 0`; column `d-1` of `S` | k = 50, 400 | err `<= 6.3e-15`; column exactly 0 |
| B. Row 0: `nu_0 = a g_0`; reference row-0 credit | n = 200, 800 | `<= 5.3e-15`; `<= 1.4e-15` (rounding) |
| C. U-coordinate gating formula (1.2), rows `>= 1` | k = 50, 400 | `<= 2.3e-15` |
| D. U-coordinate credit dynamics `Y_t = U G_t U (a P Y_(t-1) + c_t U E)`; `u^T Y = 0` | k = 50, 300 | `<= 4.2e-15`; `<= 8e-17` |
| E. Multi-step legal readout weights, `F <= 40`, random and adversarially correlated future gates | n = 800, 4000 | max non-exceptional weight `.21` / `.19` (bound proved: `1.2`) |
| F. Lemma 7.1(c): three-term split of `X_t V_t` (corrected leak coefficient `gamma/sqrt k`); capture coefficient; `Y(0)` update | k = 50, 400, 2000 | `<= 2.7e-15`; `<= 1e-17`; `<= 3.1e-15` |

Check F was added after my own first draft of §7 used the wrong leak coefficient
(`gamma/k`); the draft was corrected before commit.

The arithmetic of Theorem 4's constants (block lengths `b_j`, the release terms
R1–R3 `<= 6.8e-4 n < tau/32`, the source-channel margins, the resource cases) was
spot-checked in the session with a short script. Those checks are arithmetic, not proofs.
