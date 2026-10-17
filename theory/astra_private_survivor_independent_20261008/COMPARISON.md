# GPT-6 versus Astra: matched private-survivor comparison

**Overall winner: INCONCLUSIVE.** GPT-6 wins several tested scalar M-score comparisons; neither proves robust linear memory. No main-theorem victory is claimed.

## Independence and provenance

Astra checkpoint 185320f predates all competitor inspection. GPT-6 source is pinned to f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c and copied byte-for-byte as competitor_snapshot.py; COMPETITOR_PROVENANCE.json records its SHA-256. No historical competitor file is edited.

## Fairness controls

All paired comparisons use identical n,m,R,W, precharge L, source normalization .05, complete frozen reference O, seed 812, and query budget (two starts, one update; horizons 1,2,4,8 at small widths, horizon 1 at million width). Donor private words are zero.

GPT-6 originally starts survivor rows at the ordinary bath and resets them high; Astra prepares paired survivors high and resets to gate 1-tanh(.05)^2. compare.py explicitly harmonizes just these TWO PUBLIC operations in memory. With these edits all compared protocols share the same reference initial state and final hidden endpoint. Verbatim competitor replays are also included and show the size of that adjustment.

Architectures still differ in pulse locations, baseline attenuation and total variable-gate exposure. These are exposed rather than silently credited as storage advantages. GPT capture uses only the Walsh-low half: active controls are mR/2, not the nominal mR array size. Astra active_half ties the other half to zero for a control-count comparison.

GPT interior_independent has mR(W-1) controls. interior_tied repeats one control throughout each window and has mR controls. interior_equal_dose additionally scales the control by min(1,4/(W-1)), matching approximately the echo's two-pulse variable half-excursion sum. This is not a guarantee of identical energy or identical transfer operators.

Astra weak_equal_contrast sets its log contrast to make the boundary gate derivative approximately 1e-4; this removes the principal small-R contrast advantage of default weak echo. That finite matching setting is NOT asserted legal for arbitrarily large R.

## Results

| n | m | R | W | variant | raw GPT | controls | variable excursion/site/stage | best M | L | H |
|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---:|
| 16384 | 4 | 2 | 16 | astra_echo | False | 8 | 0.0001995 | 2.55634e-09 | 2.56713e-09 | 2.32113e-10 |
| 16384 | 4 | 2 | 16 | astra_weak_echo | False | 8 | 0.0019975 | 2.56273e-08 | 2.57355e-08 | 2.32695e-09 |
| 16384 | 4 | 2 | 16 | astra_weak_equal_contrast | False | 8 | 0.0002 | 2.56594e-09 | 2.57677e-09 | 2.32986e-10 |
| 16384 | 4 | 2 | 16 | astra_echo_active_half | False | 4 | 0.0001995 | 1.79114e-09 | 1.79511e-09 | 1.17257e-10 |
| 16384 | 4 | 2 | 16 | gpt_capture | False | 4 | 0.0001 | 5.33782e-09 | 5.4526e-09 | 1.09609e-09 |
| 16384 | 4 | 2 | 16 | gpt_interior_tied | False | 8 | 0.00075 | 7.52527e-08 | 7.67876e-08 | 1.50579e-08 |
| 16384 | 4 | 2 | 16 | gpt_interior_equal_dose | False | 8 | 0.0002 | 2.00674e-08 | 2.04767e-08 | 4.01544e-09 |
| 16384 | 4 | 2 | 16 | gpt_interior_independent | False | 120 | 0.00075 | 2.40686e-08 | 2.44831e-08 | 4.6708e-09 |
| 32768 | 8 | 4 | 16 | astra_echo | False | 32 | 0.0001995 | 3.08719e-09 | 3.09367e-09 | 1.99037e-10 |
| 32768 | 8 | 4 | 16 | astra_weak_echo | False | 32 | 0.000999375 | 1.5594e-08 | 1.5627e-08 | 1.00681e-09 |
| 32768 | 8 | 4 | 16 | astra_weak_equal_contrast | False | 32 | 0.0002 | 3.12076e-09 | 3.12735e-09 | 2.01489e-10 |
| 32768 | 8 | 4 | 16 | astra_echo_active_half | False | 16 | 0.0001995 | 2.11121e-09 | 2.11738e-09 | 1.59489e-10 |
| 32768 | 8 | 4 | 16 | gpt_capture | False | 16 | 0.0001 | 1.56872e-08 | 1.60049e-08 | 3.12539e-09 |
| 32768 | 8 | 4 | 16 | gpt_interior_tied | False | 32 | 0.00075 | 1.26935e-07 | 1.29402e-07 | 2.47841e-08 |
| 32768 | 8 | 4 | 16 | gpt_interior_equal_dose | False | 32 | 0.0002 | 3.38494e-08 | 3.45072e-08 | 6.6091e-09 |
| 32768 | 8 | 4 | 16 | gpt_interior_independent | False | 480 | 0.00075 | 3.94365e-08 | 4.01989e-08 | 7.76612e-09 |
| 32768 | 8 | 4 | 64 | astra_echo | False | 32 | 0.0001995 | 6.32265e-09 | 6.36866e-09 | 7.55295e-10 |
| 32768 | 8 | 4 | 64 | astra_weak_echo | False | 32 | 0.000999375 | 3.19345e-08 | 3.21678e-08 | 3.82063e-09 |
| 32768 | 8 | 4 | 64 | astra_weak_equal_contrast | False | 32 | 0.0002 | 6.3909e-09 | 6.43758e-09 | 7.64604e-10 |
| 32768 | 8 | 4 | 64 | astra_echo_active_half | False | 16 | 0.0001995 | 4.21503e-09 | 4.25963e-09 | 6.06751e-10 |
| 32768 | 8 | 4 | 64 | gpt_capture | False | 16 | 0.0001 | 1.77786e-08 | 1.83179e-08 | 4.34301e-09 |
| 32768 | 8 | 4 | 64 | gpt_interior_tied | False | 32 | 0.00315 | 5.70012e-07 | 5.85584e-07 | 1.32112e-07 |
| 32768 | 8 | 4 | 64 | gpt_interior_equal_dose | False | 32 | 0.0002 | 3.61908e-08 | 3.71795e-08 | 8.38793e-09 |
| 32768 | 8 | 4 | 64 | gpt_interior_independent | False | 2016 | 0.00315 | 7.69439e-08 | 7.93766e-08 | 1.91835e-08 |
| 32768 | 8 | 4 | 16 | gpt_capture | True | 16 | 0.0001 | 1.57265e-08 | 1.60456e-08 | 3.13334e-09 |
| 32768 | 8 | 4 | 16 | gpt_interior_tied | True | 32 | 0.00075 | 1.27253e-07 | 1.29732e-07 | 2.48473e-08 |
| 1048576 | 8 | 4 | 16 | astra_echo | False | 32 | 0.0001995 | 9.58174e-11 | 9.58237e-11 | 1.07069e-12 |
| 1048576 | 8 | 4 | 16 | astra_weak_echo | False | 32 | 0.000999375 | 4.83994e-10 | 4.84026e-10 | 5.41613e-12 |
| 1048576 | 8 | 4 | 16 | gpt_capture | False | 16 | 0.0001 | 1.32871e-09 | 1.33418e-09 | 1.19328e-10 |
| 1048576 | 8 | 4 | 16 | gpt_interior_tied | False | 32 | 0.00075 | 1.09411e-08 | 1.09859e-08 | 9.79827e-10 |

All values are FOUND scores, not suprema. Large H is not a separate legal readout; complete M remains the criterion. Million-width cases satisfy the stronger geometry, but exact source-root/dense lifting remain separate inherited assumptions. No million-width spectrum or linear-size control bank is claimed.

## Product-matched interior falsifier (post-comparison invention)

Use z=(u,0,-reverse(u)), making opposite words have exactly equal interior gate products. This removes the old local precharge difference while retaining full coupled feedback. Controls number mR(W-2)/2; endpoints still match. Different control subspaces prevent treating this as a pure causal ablation of every other effect.

| n | m | R | W | controls | product error | best M | L | H |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 16384 | 4 | 2 | 16 | 56 | 3.33e-16 | 3.20737e-09 | 3.21873e-09 | 2.71523e-10 |
| 32768 | 8 | 4 | 16 | 224 | 2.22e-16 | 2.99466e-09 | 2.99842e-09 | 1.73265e-10 |
| 32768 | 8 | 4 | 64 | 992 | 1.33e-15 | 1.02696e-08 | 1.02375e-08 | 5.00201e-10 |
| 65536 | 16 | 8 | 16 | 896 | 4.44e-16 | 2.42403e-09 | 2.42358e-09 | 9.01555e-11 |

## Verdict by criterion

| Criterion | Defensible conclusion |
|---|---|
| Mathematical rigor | Astra supplies a full fixed-gap echo code and a new arbitrary-word local monotone code; GPT supplies a private-capture code. The full-code scopes differ; both depend on inherited premises and need hostile review. |
| Certified robust dimension | Neither proves a jointly readable linear section. Tie at the unresolved target. |
| Found complete signal | GPT interior and capture variants exceed the corresponding tested echo scores, including some control-count/dose-matched cases. Numerical advantage only. |
| Efficiency | N and mN are matched within comparison rows; extra controls, pulse exposure and preparation/reset are explicitly recorded. No efficiency advantage for certified memory is established. |
| Scalability | Both have scoped obstructions and remaining near-critical/interior cases. Finite scores do not establish asymptotic capacity. |
| Validity | Both use the exact reference operator and complete feedback; neither independently certifies the dense source/lift or all-query optimization numerically. |

The most useful scientific development is separating low-dimensional local-product effects from the unresolved H channel. Astra does not claim to win because it introduced stronger controls, and GPT is not declared to solve memory because one pair score is larger.

Next: a complete H approximate-width theorem or robust counterexample after matching the local survival code, beginning with weak echo.