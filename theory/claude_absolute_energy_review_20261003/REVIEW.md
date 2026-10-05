# Independent hostile review: absolute-history-energy obstruction

Claude, 2026-10-03. Review of `theory/codex_absolute_history_energy_20261003/`
(PROOF.md, REPORT.md, STATUS.md, CHECKS.md, arithmetic.py, ARITHMETIC.json) at
commit f62aa45, merged into this branch as 085977c. The accepted local-radius
lower bounds are premises; I did not re-audit them. `Codex_Research.md` and
`Cursor_Research.md` were not opened. I modified no Codex file, AGENTS.md or
shared-map entry.

**Method.**
1. I derived the main argument myself (`own/`).
2. A workflow ran five independent refutation lenses (reset algebra, evasion,
   endpoint, center, scope), followed by a completeness critic (`lenses/`,
   with the full structured results in `lenses/workflow_result.json`).
3. Every claim below that rests on a lens result, I either re-derived or
   re-ran, or I mark it **[lens]**.

Labels: **[V]** analytic, verified by me; **[N]** numerical diagnostic only.

---

## Verdict: **VERIFIED**

Every step of the primary claim holds as written, for every n >= 200. These are:

- the terminal identity;
- the source-block bound `||X|| >= (b0-lambda)sqrt(l) - e_n sqrt(n)`;
- the constant `0.0499 sqrt(n/2)`;
- `||X||^2 > (249001/200000000) n`;
- the threshold `n >= (200000000/249001)R^2 ~ 803.209626 R^2`.

No history length, gate schedule, harmonic construction, preparation path or
multi-step reset evades it. It is correctly framed as a feasibility
obstruction, not a memory-compression theorem.

The bound is **true but not sharp**. The proof discards the memory block, which
also forces an unavoidable final-step residual once n >= 804. The sharp minimal
energy is `b0 sqrt(n) - Theta(1)`, about `0.05 sqrt n`, not
`0.0499 sqrt(n/2)`. The sharp emptiness threshold is therefore
`n*(R) = 400 R^2 (1+O(1/R))`, about half of 803.21 R^2 for large R.
Looseness is not a false statement, so the verdict stays VERIFIED rather than
REPAIRABLE.

---

## 1. Reset equation from the actual recurrence [V]

The model is `h_t = tanh(R h_(t-1) + x_t + b0 1_n)` with W=I, b0=1/20 and h_0=0.

- tanh is a bijection from R onto (-1,1) and vanishes only at 0.
- So `h_T = 0` holds if and only if `R h_(T-1) + x_T + b0 1_n = 0`, that is,
  `x_T = -R h_(T-1) - b0 1_n` exactly.
- h_(T-1) is either h_0=0 or a tanh output, so `|h_(T-1,i)| < 1` for every i,
  whatever the inputs were.
- Under the project's convention, the reset input x_T is a counted history
  input (PROOF section 1, and the accepted radius estimates that count the
  reset), so `||X||_2 >= ||x_T||_2`.

The past input cube is not used, so the bound also covers unrestricted inputs.

## 2. Why the bias cannot be cancelled cheaply [V]

**Source block (the proof's argument).** R0 = diag(aO, lambda I_l) is block
diagonal, so the only recurrent drive into a source row is `lambda h_src,i`
with `lambda = 1/(100n) = b0/(5n)`, plus the dense leakage `Pi_s(R-R0)h`.
That leakage is at most `e_n sqrt(n)` in total norm. Each source coordinate
must still supply at least `b0 - lambda` through the input, which gives
`||Pi_s x_T|| >= (b0-lambda)sqrt(l) - e_n sqrt(n)`.

**Memory block (dropped by the proof, but also forced).** O is orthogonal, so
`||aO h_m + b0 1_k|| = ||a h_m + b0 O^T 1_k||`. The Householder twist funnels
the uniform bias onto one latent node:

    O^T 1_k = sqrt(k) e_(d-1) + gamma w,  (O^T 1_k)_(d-1) = sqrt(k) - 1/(sqrt(k)-1),

so `u = O e_(d-1)` is a unit memory vector orthogonal to the source block.
Along it, `|<x_T,u>| >= b0(sqrt k - 1/(sqrt k - 1)) - a - |<(R-R0)h,u>|`,
because a bounded state contributes at most `a|h_(d-1)| <= a`. This residual is
positive once k >= 402, i.e. n >= 804. The near-orthogonal memory recurrence
therefore cannot absorb the bias either.

## 3. Independence from length, gates, harmonics and preparation [V]

The bound uses only the final transition and `|h_(T-1,i)| < 1`. It therefore
holds uniformly over:

- every history length T >= 1;
- every gate word;
- every harmonic or frequency choice, and every sign choice;
- every preparation path;
- whole continuous sections;
- unrestricted inputs.

Its genuine dependencies are:

- the frozen R: block structure, lambda, and `||R-R0|| <= e_n`;
- the frozen bias b0 != 0;
- W = I;
- the exact endpoint h_T = 0;
- the Euclidean norm with the reset counted.

## 4. Norm conversions and constants in 0.0499 sqrt(n/2) [V]

- `L_n = sqrt(l)[b0 - lambda - e_n sqrt(n/l)]`, with l = ceil(n/2) >= n/2.
  So `sqrt(n/l) <= sqrt 2`; the proof uses the weaker `<= 2`, which is valid.
- `b0 - lambda - 2e_n` is strictly increasing in n. At n=200 it equals
  24974999999/500000000000 exactly, which exceeds 499/10000 by
  24999999/5*10^11. The inequality is strict.
- `e_n sqrt(n) = 4/(10^8 n^(3/2))` matches the expression in REPORT/STATUS.
- `(499/10000)^2/2 = 249001/200000000` exactly.
- **[N]** The minimum of `L_n/(0.0499 sqrt(n/2))` over n >= 200 is
  1.0010020, attained at n=200.
- All six REPORT table entries for the terminal lower bound
  (0.4995, 0.565243483, ..., 35.355331988) reproduce at 60 digits.
- Dense premise: for the archived R, `||R-R0|| <= 2a eps/(a-eps) < 4 eps = e_n`
  with `eps = 1/(10^8 n^2)`. Float64 readings above e_n at n >= 1600 are
  roundoff at the 1e-14 level, not a violation.

## 5. Threshold n < 803.209626 R^2 [V]

`||X|| <= R` together with `||X||^2 > 249001 n/2e8` forces
`n < (2e8/249001) R^2 = 803.2096256641539592... R^2`. Writing it as
803.209626 rounds up, which is the safe direction. The statement also needs
**n >= 200**, the family's domain; this is implicit in PROOF (10) and explicit
in REPORT.

**Sharpening.** The bound is valid but loose, as computed in `own/a3_sharp.py`:

| R | class nonempty for 200 <= n <= | first n proven empty (sharpened) | file's threshold |
|---|---|---|---|
| 1 | 400 | 801 | 803.2 |
| 2 | 1600 | 2660 | 3212.8 |
| 10 | 40000 | 45645 | 80321 |
| 1000 | 4.0e8 | <= 4.006e8 | 8.03e8 |

Nonemptiness comes from the one-step history `x_1 = -b0 1_n`. Its inputs lie in
the past cube, it ends at h_1 = 0, and `||X|| = b0 sqrt(n)` exactly.
Emptiness for n >= 400(R+0.709)^2 comes from section 6 below. So
`n*(R) = 400R^2(1+O(1/R))`. For R <= ~1.7, the file's 803.21 R^2 is the better
of the two sufficient thresholds.

## 6. Multi-step resets cannot evade the one-step cost [V+N]

`||X|| >= ||x_T|| >= min_(h in [-1,1]^n) ||R h + b0 1||`. Earlier steps only add
nonnegative energy and can influence the last step only by choosing h_(T-1),
which ranges over a subset of this box.

**[V] Exact box minimum.** For R0 the box minimum is, up to `+/- e_n sqrt(n)`:

    S_n = sqrt( l(b0-lambda)^2 + [(b0(sqrt k - 1/(sqrt k-1)) - a)_+]^2 ),

and the bound holds as `||X|| >= S_n - e_n sqrt(n)`. This quantity equals the
proof's L_n for 200 <= n <= 803. It satisfies `S_n - e_n sqrt(n) > b0 sqrt(n) - 0.709`
for every n >= 200 (50-digit scan, minimum margin 0.0019, which tends to
0.709 - 1/sqrt2). **[N]** Bounded-variable least squares on the actual dense R
matches S_n:

| n | 200 | 400 | 800 | 1000 | 1600 | 2000 |
|---|---|---|---|---|---|---|
| box minimum | 0.4995 | 0.7068 | 0.9998 | 1.1239 | 1.4731 | 1.6840 |

**Source-only two-step refinement** [lens, re-derived by me]:
`||X|| >= b0 sqrt(l) - sqrt2 e_n sqrt(n)`. If `h_(T-1,i) < 0`, then both
`|x_(T-1,i)|` and `|x_(T,i)|` are at least `b0-lambda`, and
`2(b0-lambda)^2 >= b0^2`.

**[N] Full-history adversary** [lens]. L-BFGS over T-step histories ending
exactly at 0, on the actual R:

- n=200: T=1, 2, 10, 20, 50 give best ||X|| = 0.7071, 0.7085, 0.7069, 0.7057,
  0.6909. The best is 0.977 b0 sqrt(n), against L_n = 0.4995.
- n=400: the best is 1.0000.
- n=1600: the best is 2.0295.

No history comes within 1.38x of L_n.

**Approximate endpoints** [lens, checked]. If only `||h_T|| <= tau` is
required, then `||X|| >= (tanh(b0)-lambda)sqrt(l) - tau - e_n sqrt(n)`. The
obstruction survives any `tau = o(sqrt n)`.

## 7. Is the endpoint h=0 genuinely the source? [V]

Yes. For a general common endpoint z, the exact one-step obstruction is the
distance from `atanh(z) - b0 1_n` to the set `R[-1,1]^n` (up to the dense term).

- For z = 0 this is the bias itself.
- It vanishes if b0 = 0.
- It vanishes at the autonomous fixed point.
- Equilibrating only the source block is **not** enough. The endpoint
  (0_k, s* 1_l) is still obstructed through the memory funnel for n >= 804.

There is a second dependency: the reset input must be counted in X. If it were
exempt, the section-5 obstruction would vanish entirely, since zero inputs plus
a free reset cost 0. Section 6 of PROOF would survive, because it never uses
the reset. The counted convention is the project's, so this is a scope note,
not a defect.

## 8. Does a common nonzero autonomous endpoint avoid it? [V+N]

**Yes, it removes the obstruction entirely.**

- `F(h) = tanh(Rh + b0 1)` is an l2 contraction with factor a = 1-1/n, so it
  has a unique fixed point h*.
- Bound (15) is <= 0 at z = h*, so it is vacuous there.
- Take T-1 zero inputs, then `x_T = R(h* - h_(T-1))`. This ends exactly at h*
  with `||X|| <= a^T ||h*|| <= a^T sqrt(n)`. So
  `{||X|| <= R, h_T = h*}` is nonempty for every n and every R > 0.

**[N] Structure of h*:**

- Source coordinates are about 0.04996, with gate about 0.9975.
- The protected memory coordinate is about 0.50.
- Memory coordinate 1 receives the funnelled bias. It saturates as n grows:
  0.52, 0.64, 0.77, 0.89, 0.96 at n = 200, 400, 800, 1600, 3200 [lens].
- No memory coordinate lies in the accepted weak-gate cube.

**It is mathematically meaningful for the accepted contract**, but it is a
contract change, not a repair.

What survives:

- Same-endpoint cancellation of the direct and source future terms. It needs
  only a *common* endpoint.
- The legal query family. In the accepted contract, future inputs are
  unrestricted and only the preactivations are boxed in [1/4,3/4]^n
  (`codex_intermediate_gate_credit_20261002/PROOF.md:41-42`,
  `codex_multiharmonic_lower_20261002/PROOF.md:374-375`). So every endpoint
  admits the full query box.
- The dense-transfer operator bounds.

One lens argued autonomous endpoints lose all legal queries for n >= 1156. That
holds only if future inputs are confined to the past cube. The pre-2026-10-02
stages used that convention (a fixed future input `(9/20)1` from h=0); the
accepted contract does not.

What must be re-proved:

- The final gate becomes `G_z = diag(1-z^2)` instead of I, and its coordinate-1
  entry tends to 0.
- The harmonic and L1 query analysis must be redone.
- A one-step reset to h* leaves the past cube for n >= 400 [lens]. Relaxing
  through zero inputs instead adds Theta(n) steps.

What it cannot rescue: the accepted mechanism. PROOF section 6 is correct, and
the endpoint lens re-derived every term (atanh bound, protected coordinate,
zero source-to-selected block, dense term). Each transition between two states
in the accepted weak-gate cube costs at least `max(0, B_n)`, with
`B_n ~ b0 sqrt(n/2)`. B_n > 0 exactly from n = 400:
`B_399 = -2.19e-4`, `B_400 = 6.61e-4`. At fixed R, no weak-to-weak transition
can occur once n is about 800(R+0.71)^2, whatever the endpoint.

## 9. Baseline asymptotic [V+N]

- Formula (1) is exact for the actual R. It has four input types:
  1 preparation, 1 first-interior, N-1 later, 1 reset.
- Formula (3) checks term by term. It uses `1^T O 1 = 0`, from
  `U1 = sqrt(k) e0` and `P e0 = e1` with d >= 2, and `||O1||^2 = k`.
- The dense sandwich (4)-(5) is valid.
- `C_abs = sqrt(2[b0^2+(atanh(0.4)-b0)^2]) = 0.533129483399339144056793391833...`,
  so the quoted 0.533129483399339 is correct.
- `E0/(n sqrt(log n))` approaches C_abs from below, with relative correction
  `-0.13626/sqrt(n) + O(1/n)`. The slowest term is the memory cross-term
  `-2 b0 atanh(beta)`. **[N]** The relative gap is 0.42% at n=200, 1.35e-4 at
  n=10^6 and 4.3e-9 at n=10^15.
- The REPORT E0 table reproduces to every printed digit.
- The actual-R center norm lies strictly inside `E0 +/- Delta_n`, at about
  0.12 Delta_n (n = 200, 256, 400).
- The section-wide bound (7) and the construction-specific tradeoff (14),
  including `D_n ~ n^(19/18)/(4*10^6)`, are correct.

## 10. Emptiness versus any O(n) memory bound [V]

This is a degeneracy of the contract, not a statement about memory. The four
ingredients are:

- an absolute budget measured from zero input;
- the endpoint 0;
- b0 != 0;
- a counted reset.

Even the zero-information one-step history costs `b0 sqrt(n)`.

- For n >= 803.21 R^2 the only member is the zero-length history, a singleton.
  "Empty" in the files means "no history with T >= 1", and PROOF section 5
  says "empty/singleton".
- Assigning that class robust dimension 0 is vacuous. It is **not** an O(n),
  O(1) or any other compression theorem.
- It says nothing about nonempty classes. Examples are endpoint h*, or a
  per-coordinate budget `R_n = rho sqrt(n)` with `rho > b0`, which contains the
  reset-only history. The files do not discuss the latter regime.
- The files keep this distinction correctly.

---

## Strongest theorem actually justified

> For the frozen dense tanh family, every integer n >= 200, and any R with
> `||R-R0||_op <= 4/(10^8 n^2)`, take any history with T >= 1 steps and exact
> final state h_T = 0. Its inputs, gates, harmonics, preparation and length
> are arbitrary, including unrestricted inputs. Then
>
>     ||X||_2 >= ||x_T||_2 >= max{ L_n, S_n - e_n sqrt(n), b0 sqrt(l) - sqrt2 e_n sqrt(n) },
>     L_n = (b0-lambda)sqrt(l) - e_n sqrt(n) > 0.0499 sqrt(n/2),
>     S_n - e_n sqrt(n) > b0 sqrt(n) - 0.709,
>
> and the one-step history `x_1 = -b0 1_n` attains `||X|| = b0 sqrt(n)`. Hence
> the minimal energy is `b0 sqrt(n) - Theta(1)`.
>
> For a fixed absolute budget R, the class `{T >= 1, h_T = 0, ||X|| <= R}` is
> empty for `n >= max(200, min{803.2096257 R^2, 400(R+0.709)^2})`, and
> nonempty for `200 <= n <= 400R^2`.
>
> This is a feasibility obstruction of the frozen zero-endpoint instantiation
> only. It is not a memory-compression or O(n) theorem.

Separately verified:

- `||X_n(0)|| ~ 0.533129483399339 n sqrt(log n)`, for the accepted center and
  the whole section.
- The weak-window bound (11)-(12) holds as scoped.

**Is moving to a nonzero common endpoint meaningful?** Yes. A public common
endpoint, for example the autonomous fixed point h*, gives a well-posed,
nonempty bounded-energy class for every R > 0. The accepted contract's
same-endpoint cancellation and unrestricted future inputs carry over.

But it is a contract change requiring an owner decision. No accepted lower
bound transfers to it: the final-gate factor and the query analysis must be
redone, and section 6 shows the existing weak-gate multiharmonic mechanism
cannot run at fixed R. The open object is the robust antipodal width, in the
actual query metric, of `{X: ||X|| <= R, h_T = z_n}` for public common z_n.
Neither a superlinear construction nor an O(n) upper bound exists for it.

## Non-blocking defects in the files

- PROOF section 3 calls the enclosure (5) "sharp". It is rigorous, but the
  actual |E_R - E0| is about 0.12 Delta_n. Delta_n could also be halved, since
  `||R-R0|| <= ~e_n/2`.
- "EMPTY" should read "no history with T >= 1". The file qualifies this later.
  Likewise, "No omega(n) robust section" is an underclaim: no positive-dimensional
  section exists at all.
- CHECKS.md says "Minor implementation issues: none". This is inaccurate:
  arithmetic.py calls `ctypes.windll` (lines 129-132) and fails on Linux, and it
  refuses to overwrite its own output. A Linux replay with the memory probe
  stubbed passes 18/18 [lens].
- Some checks are tautological or weak. The "frozen local radius" check
  compares two constants. The sandwich check uses a test matrix, not the
  archived R. Inequality (8), the decimal 803.209626, B_n and (14) are not
  checked in code.
- PROVENANCE.json hashes for ARITHMETIC.json and AGENTS.md match only CRLF
  copies.
- STATUS.md says no Claude bounded-radius review folder was located. That was
  accurate for main at f62aa45; the review is at
  `theory/claude_bounded_history_radius_review_20261003/` on
  `claude/wonderful-fermi-yx8b1e`.
- PROOF section 7 says the result is "stronger than a tradeoff based on tangent
  singular values". The claim is unquantified.

## Compute

- CPU only; no GPU or CUDA.
- Own scripts: about 25 s CPU (`own/outputs/compute.txt`).
- Workflow: 6 agents (5 lenses plus 1 critic), about 81 minutes wall on 4
  shared cores. Their scripts and outputs are preserved in `lenses/`, and they
  wrote only to scratch.
