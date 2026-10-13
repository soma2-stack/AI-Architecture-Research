# Numerical checks (diagnostic only)

Script: [checks.py](checks.py). Output: [checks_result.json](checks_result.json).
Environment: Python 3.11.9, numpy 2.4.6, torch 2.13.0 (CPU), float64, seed `20261013`.
The script runs at BelowNormal priority with at most 4 threads; runtime is about 25 s.
Exact identities were also checked in exact rational arithmetic (`fractions.Fraction`).
The script contains hard `assert`s (endpoints exactly zero, inequalities hold), and all of
them pass.

None of these numbers proves an asymptotic statement. The proofs are in
[PROOF.md](PROOF.md).

| Sec. | Claim checked | PROOF.md | Result |
|---|---|---|---|
| A | `h_(2R) = 0` and zero-input continuation, `R = 1,2,3,4,8`, `m = 1,2,5` | Thm 1.3 | float64 max abs `0.0`; exact rationals `True`, including the `h_R` structure |
| B | `Phi_T = S^(T-2R) Gamma(z)` for `T = 2R, 2R+1, 3R, 3R+2` | Thm 1.4 | product `0.0`; autograd `2.2e-16`; finite differences `6.3e-11`; exact rationals `True` |
| B | singular values | Thm 1.4 | random `z`: `[.5025, 1.4936]`; cube vertex: `[.5, 1.5]` |
| B | general multi-round history has a monomial Jacobian | Lemma 1.2 | `True` |
| C | cancellation input bound | Sec. 2.1 | `.625` on `[-1/2,1/2]`; `.5` at `rho = sqrt2-1`; `.375` on `[-1/2,0]` |
| D | parameter gradients (`W`, `c`, `U`, `b`, `theta_0`) vs torch autograd | Prop. 3.1 | max abs error `8.9e-16` |
| D | `grad_theta0 = Gamma(z) lambda_T` | Sec. 3 | error `0.0` |
| E | fixed-head adjoint `mu^(R+1-r) = (1+v^(r))/sqrt n` | Lemma 5.2 | error `5.6e-17` |
| E | Gemini's terminal adjoints span `R^n` | Sec. 4 | sample rank `6 = n` |
| E | Gemini's literal metric on the cube boundary | Prop. 4.1 | minimum sup-separation `.5` for `R = 1,2,4,8`; brute-force random `v` never exceeds the computed supremum |
| E | `theta_0` with fixed head, single saturated coordinate | Prop. 4.3 | `1/sqrt(n)`: `.25, .125, .0625, .03125, .0156` for `n = 16 ... 4096` |
| E | Gemini's schedule, bias, `w = .035/sqrt n`, `R = 2` | Cor. 4.5b | `.00216, .00116, .00059, .00029` (`n = 64 ... 4096`), i.e. `~ n^(-1/2)` |
| E | same with `R = 3` | Cor. 4.5b | `.00260, .00143, .00072, .00036` |
| E | same with `R = sqrt n` (not Gemini's choice) | — | `.0048, .0032, .0031, .0028`: small but not vanishing; no proof |
| F | Lemma 5.1 closed form vs actual recurrence | Lemma 5.1 | at most `1.4e-15`; endpoints exactly `0` |
| F | future part of the gradient identical for the pair | Lemma 3.2 | `0.0` |
| F | repair scaling, `n = R^2 = 64 ... 4096`, `q = 193`, `w = .035/sqrt n` | Thm 5.4 | normalized separation `1.146, 1.120, .930, .936`; actual / proved inequality `>= 1.32`; `||Dz||_1/(rho n) >= .72` (empirical code) |
| F4 | sign query vs best vertex query | Thm 5.4 proof | ratio `.963, 1.000, .951` (exhaustive, `n <= 16`); `.996` (`n = 32`, coordinate ascent) |
| G | `||Delta grad_b|| <= 2T` on 200 random nonexpansive pairs | Thm 4.4 | largest ratio `.10` |
| H | clipped random-sign code, `N = 2000`, adversarial search | Lemma 5.3 | min saturated fraction `.49, .76, .69, .62` at `D = 2, 20, 100, 250`; `||G||/sqrt N = 1.01`-`1.34` (lemma uses `5.06`) |
| I1 | zero-bias tanh RNN with `W` = cyclic shift (ablation) | Sec. 7.2 | endpoint `0.0`; inputs `<= .37`; separation `1.78, 1.17, 1.24` (sign-aligned idealized adjoints) and `1.34, .59, .71` (uniform head), `n = 64, 256, 1024` |
| I2 | bias tax: tanh shift RNN with `b = .05`, zero input | Sec. 8.2 | autonomous state `.502`, gate `.748`, credit saturates below `3.97` |
| I3 | `R = 1` necessary cost under `w = .035/sqrt n` | Cor. 4.5c | `mT_nec / n^1.5 = .0286` |
| I4 | expansive amplification, `R = 1` | Sec. 6 | horizon `4, 6, 8, 13` for `n = 2^6 ... 2^20`; closed form `1.1e-14` |
| K | fixed-feature projection of the full `W_full` gradient vs formula | Cor. 5.6 | autograd error `2.1e-17` |
| K | transplanted normalization, `n_tot = 128, 512, 2048` | Cor. 5.6 | `d_F = .654, .643, .535`; actual / proved inequality `>= 1.55`; bound with lemma constants `.00895` |
| J | blow-up after about `2/epsilon` passes | Rem. 1.5 | `209` (`2/epsilon = 200`), `2012` (`2000`) |
| J | perturbed `h_0`: second-order endpoint error | Rem. 1.5 | `||h_T - Phi delta||/||delta||^2 = .87, .78, .53` |

Two caveats.

* Section I1 uses an idealized adjoint family `[1/2,1] n^(-1/2)` for the tanh ablation. It
  is evidence for the novelty verdict, not a theorem.
* Section H's adversarial search finds an upper estimate of the minimum saturated fraction,
  not a certificate. The certificate is Lemma 5.3.

## Independent-review scope and adversarial diagnostic

The table above is the author's original finite diagnostic output; its empirical rows are
not universal claims. The independent review found that the finite exhaustive/coordinate-
ascent sign-query comparison in F4 does not justify a worst-case constant-factor statement.
For example, at `R=5, m=1, q=1, rho=rho_f=1/2` and
`dz=(1/2,0,0,0,-1/2)`, the prescribed sign query has value `1/sqrt(10)` times the
best vertex-query value (`0.3162...`). This is a diagnostic counterexample to that broader
interpretation, not to Theorem 5.4's stated worst-case window-subtraction bound. The
independent review's exact-rational and forward-tangent reproduction instructions and
scope are recorded in [REVIEW_HANDOFF.md](REVIEW_HANDOFF.md) and [PR #25](https://github.com/soma2-stack/AI-Architecture-Research/pull/25).

The tanh rows remain numerical evidence only: the sign-aligned adjoints in I1 are
idealized, and these finite samples do not establish legal future-query realization or
uniform separation over every boundary point. No training was performed.
