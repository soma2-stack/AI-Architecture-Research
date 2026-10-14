# Checks — claude_multiprobe_memory_20261014

`python -I exp_identities.py` (CPU, < 1 min, float64, torch autograd) writes
`exp_identities_result.json`.

| Check | n, T | Result |
|---|---|---|
| Credit-matrix recursion (0.1) vs autograd, actual `R = R0 + H`, `||H|| = 4e-8/n^2` | 96, 25 / 160, 40 | rel. err. `5.6e-16` / `1.1e-15` |
| One-step legal query gradient `sigma sqrt(l) nu^T B_T` + direct term vs autograd | same | rel. err. `8.1e-16` / `1.6e-15` |
| Gather identity `O^T 1_k = sqrt(k) e_(d-1) + gamma e_0 - (gamma/sqrt k) 1_k` | k = 48 / 80 | `1.8e-15` / `1.2e-14` |
| Readout weights (Lemma 1.2), inline check in the session | k = 50, 400, 2000 | formula err. `<= 1.2e-13`; `max |nu_i| <= .339`; `nu_(d-1)/sqrt k >= .739` |

These verify exact identities only. The asymptotic theorems rest on the proofs.
