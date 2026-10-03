# Absolute energy after the accepted bounded-local-radius theorem

2026-10-03. Theory stage complete. New energy arguments are internally checked;
they have not yet received independent review. Earlier proofs/reviews unchanged.

## 1. Consolidated accepted status

| Contract | Accepted fixed-feature lower bound |
| --- | --- |
| Growing local radius | Omega(n^(16/15)) |
| LOCAL raw-input radius <=0.02 around public X_n(0) | Omega(n^(19/18)); n>=10^900, D>=n^(19/18)/20,000,000 |
| Fixed ABSOLUTE radius around zero input, frozen final h=0 | This stage finds the history class infeasible at sufficiently large n |

The accepted local theorem retains boundary antipodal half-margin
>999.999649997999 at epsilon=0.001. Its two hostile-review verdicts are accepted
from the owner, not re-evaluated. Historical pending-review wording is retained
for provenance; STATUS.md and the current resume entry record acceptance.

Full-model bounds remain Omega_c(n^2)--O_c(n^2 log n). No finite-bit/VRAM,
practical-onset, learning, architecture or every-RNN consequence is asserted.

## 2. Exact absolute norm of the current center

Define k=floor(n/2), l=n-k, a=1-1/n, lambda=1/(100n), b0=.05, s=.4,
beta=sqrt(.15/n), A=atanh(.4), B=atanh(beta), N=ceil(4n log n)+1.
The exact reference norm is

    E0^2 = k{2b0^2+N[(B-b0)^2+a^2 beta^2]}
            + l{(A-b0)^2+N(A-b0-lambda s)^2+(b0+lambda s)^2}.

For the ACTUAL frozen dense matrix,

    | ||X_n(0)||_2-E0 |
      <= Delta_n = 4/(10^8 n^2) sqrt(s^2 l+N[beta^2 k+s^2 l]).

PROOF.md equation (1) is additionally an exact four-transition-type formula
in the actual R. No long array is needed; no old witness is changed.

The sharp leading coefficient is

    ||X_n(0)||_2 ~ C_abs n sqrt(log n),
    C_abs=sqrt(2[.05^2+(atanh(.4)-.05)^2])
         =0.53312948339933914405679339183337895665...

This establishes actual norm divergence rather than a diverging majorant.
Memory bias cancellation and persistent source maintenance produce the leading
cost. Preparation and reset are explicitly counted; they also have growing
norm, although they are lower order than the long window's energy.

CPU numerical arithmetic of the formula, not new sensitivity evidence:

| n | Reference center norm E0 | Universal terminal norm lower bound |
| ---: | ---: | ---: |
| 200 | 244.409560367 | 0.499500000 |
| 256 | 320.033083864 | 0.565243483 |
| 400 | 519.858531517 | 0.706753228 |
| 1000 | 1396.696899383 | 1.117810382 |
| 2000 | 2932.284265626 | 1.580980716 |
| 1,000,000 | 1,981,332.888941135 | 35.355331988 |

Dense sandwich radii and both block energies are saved in ARITHMETIC.json.
These small widths are formula checks, not claimed multiharmonic onset widths.

## 3. Strongest new obstruction; best bounded-energy construction

For EVERY nonempty history ending at the required h=0,

    ||X||_2 >= (.05-1/(100n))sqrt(l)-4/(10^8 n^(3/2))
              > .0499 sqrt(n/2), n>=200.

Reason: the reset input is exactly -R h_previous-b. The source recurrent
block has norm 1/(100n), its dense leakage is tiny, and it cannot cancel
.05 bias in l source coordinates. This includes any sparse pulses, gate signs,
source changes, frequency choices, window lengths and continuous section.

Therefore fixed absolute R forces

    n < (200000000/249001)R^2 = approximately 803.209626 R^2.

**No bounded-absolute-energy construction exists at this frozen zero endpoint
for arbitrarily large n.** No positive asymptotic robust dimension/margin can
be assigned there. A zero-length zero-state history is a singleton and gives
zero credit information. An empty/singleton class has a vacuous zero-coordinate
upper bound; this is not a substantive O(n) compressor or a general theorem
for all common endpoints.

## 4. Redesign attempts and full ledger

| Change considered | Absolute energy | Dimension/signal | Admissibility/endpoint |
| --- | --- | --- | --- |
| Accepted local section unchanged | E0 +/- Delta_n +/- .00970048 | Accepted D and margin retained | Accepted admitted lift and exact h=0 retained |
| Smaller F/delta or better co-moving cancellation | Center unchanged | May reduce dimension/signal; no new margin claimed | h=0 obstruction unchanged |
| Shorter window / sparse active times | Maintenance can fall | Long-window signal proof no longer inherited | Reset alone still costs sqrt(n) |
| Smaller source level / duty cycle | Changes maintenance/preparation | Feature and signal ledger change | Reset obstruction still independent of source history |
| Source level at autonomous reference equilibrium | Reference source maintenance zero | No robust section proved | Source reset still costly; weak memory window also costly |
| Different common endpoint | Can avoid terminal zero obstruction | No bounded-energy superlinear section or O(n) theorem obtained | Different endpoint scope; not silently adopted |
| Different public bias | Could change all energy costs | No accepted lower transferred | Different frozen model; not used |

The lower bound is upstream of nonlinear/query-error calculations: no candidate
can meet the required energy and endpoint conditions. Keeping the old signal
ledger while subtracting public preparation or reset would be invalid.

Independently, for N consecutive weak selected states in the accepted gate
cube, define

    B_n=.05sqrt(r)-[a+(1-1/(4n))^(-1)]sqrt(r/(4n))
                     -4/(10^8 n^(3/2)).

Then ||X||_2 >=sqrt(N-1)max(0,B_n), even without a final reset or fixed H.
For N=ceil(4n log n)+1 this is asymptotic to .05sqrt(2)n sqrt(log n).
Thus removing the reset alone does not make this intermediate multiharmonic
window an absolute-energy-bounded mechanism. See PROOF.md section 6.

## 5. Exact energy--dimension--margin tradeoff

For the existing accepted family:

    D_n=floor(floor(n/4)/10^6)*floor(n^(1/18)),
    E0-Delta_n-.00970048 < ||X_n(y)||_2 < E0+Delta_n+.00970048,
    boundary antipodal half-margin >999.999649997999.

These are joint-section bounds, not separate-axis estimates. Asymptotically

    D_n ~ n^(19/18)/(4*10^6),
    R_family ~ C_abs(4*10^6 D_n)^(18/19)
                          sqrt((18/19)log(4*10^6 D_n)).

The last expression is a cost of this construction, not a universal
energy-versus-dimension lower bound. For all histories at the required zero
endpoint, the universal necessary condition is instead n<803.209626 R^2.

## 6. What remains open if the endpoint scope changes

If arbitrary common endpoints z_n are allowed, the terminal bound becomes

    ||X||_2 >= ||atanh(z_source)-.05 1_l||_2
                         -sqrt(l)/(100n)-4/(10^8 n^(3/2)).

It need not grow near autonomous source equilibria. We have neither a
superlinear bounded-energy section nor a useful O(n) theorem for that enlarged
class. Its precise remaining object is the robust antipodal width, in the
unchanged actual legal-query metric, of

    {X: ||X||_2<=R, h_T(X)=z_n},

uniformly over public endpoints and horizon. This is not inferred from raw
rank, RMS, tangent counts, local-radius lower bounds or failed constructions.

**Recommendation:** review the new terminal-energy and weak-window feasibility
lemmas first. Before another bounded-absolute-energy construction, explicitly
decide whether to retain h=0 or permit autonomous common endpoints. Under h=0
the frozen-family target is already infeasible, so further witness work is
unnecessary. No new research stage is begun here.

## 7. Checks, compute and files

18 CPU arithmetic checks passed: exact rational feasibility constants;
80/120-decimal scalar agreement; Householder orthogonality; exact transition
energy versus the closed formula; and a bounded-perturbation sandwich check.
None re-evaluates the accepted robust theorem. High-precision values are
numerical diagnostics; all-width conclusions follow the written identities
and explicit inequalities, not floating-point certification.

Measured arithmetic CPU: 0.015625 seconds; peak RAM: 38,293,504 bytes
(36.52 MiB). Runtime initialization/administrative commands were not included
in that arithmetic timer. GPU/CUDA/model-server use: zero. No training.

New files: STATUS.md, PROOF.md, REPORT.md, arithmetic.py, ARITHMETIC.json,
CHECKS.md and PROVENANCE.json in this directory. Codex_Research.md receives
an additive current resume. The shared map receives only the owner-accepted
theorem checkpoint. Historical proof/output/review files remain untouched.
