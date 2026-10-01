# Third-order antipodal result: one frozen 6D attempt

## Classification

**6D RIGOROUSLY CERTIFIED — INDEPENDENT REVIEW REQUIRED.**

Independent width-4 confirmation, the existing horizon37 endpoint, at unchanged
epsilon=1/1000 and the accepted normalized gradient/query metric. Parameters and
history are unchanged. No new witness, architecture, training or wider model.

The result is a lower bound of six real coordinates for a continuous no-external-
history encoder required to answer every permitted late gradient query with
uniform absolute error epsilon on this fixed-h section. It is not a finite-byte
bound or proof of the maximum robust dimension.

## Archive and preregistration chronology

1. Review b7e1e45 accepted the stage-1 5D joint certificate with qualifications.
2. Commit357765a added the original evidence and a separate documentation
   clarification file. Original proof, outcomes, repair records and old manifests
   stayed byte-identical in the working tree.
3. Commit1e1b141 disabled Git newline conversion and preserved raw dependencies,
   ensuring original frozen bytes can be retrieved. This is a current archive,
   not a retroactive claim of pre-screen preregistration.
4. This new method, selection rule, actual candidate and code were frozen and
   committed at914b075 BEFORE any official third-order box evaluation. No
   scientific code or constant has changed since. FROZEN.json verifies this.
5. A post-result Git-byte check exposed26 ignored historical logs omitted by the
   earlier git add. They were already hashed and unchanged in the working-tree
   archive before certification. Commitc482a73 adds those logs; all568 entries in
   BYTE_EXACT_ARCHIVE.json now verify against actual Git blobs. Packaging was
   completed after the new run; do not describe that log commit as pre-run.

The new candidate was chosen using already inspected numerical development
evidence, not an untouched holdout. The preregistration freezes a deterministic
existence-certificate attempt; it is not a statistical discovery-rate experiment.

## Frozen candidate

Selection: highest prior numerical beta3 score among archived r6 candidates for
independent_n4_confirmation. This selects query_r6_s2, prior proxy score1.65742026.
No new optimizer/search was run. Query-SVD B,L were regenerated with the original
code and frozen as exact dyadic2^-128 constants; their orthogonality is not assumed.

Tangent half-widths (exact):

    33277/1048576
    26501/524288
    101613/1048576
    103605/1048576
    353511/1048576
    419801/1048576

Equal normal half-width8087/1048576=0.007712364196777344. It follows the
predeclared2% safety padding and upward2^-20 rounding; no certification-driven
adjustment occurred. Tangent widths were rounded downward. Frozen K_h,K are
exact rationals derived only from the192-bit center Jacobian before official
curvature evaluation. The candidate/model/input hashes are in FROZEN.json;
candidate SHA256 is629751f273e8cb59122a0a3c39cd04a483f3ad31da4cd6b4e405bd3a6d547fb9.

## Rigorous results

| Face | beta3 lower margin | Cubic upper M3 |
| --- | ---: | ---: |
| 1 | 0.001657003876592377 | 2.7282826425098716 |
| 2 | 0.001720684006565376 | 0.7770523105264474 |
| 3 | 0.001720706467474263 | 1.7510339254985723 |
| 4 | 0.001657276990838233 | 1.7541658384188168 |
| 5 | 0.001657299155294360 | 1.3970520728175126 |
| 6 | 0.001657226382997007 | 1.7000897811392064 |

All six beta3 values exceed0.001. Every boundary antipodal pair has query
distance at least0.003314007753184754, strictly greater than2epsilon=0.002.

Hidden contraction eta_h=0.049664944775466374<3/4. The full simultaneous normal
self-map passed; maximum raw history perturbation is0.11136472065634755<1.
The fixed-point implication is exact H=0, not a numerical root approximation.

Both192-bit and256-bit runs regenerated endpoint jets and all third-order
majorants from scratch using the same frozen rational inputs and preconditioners.
Displayed binary64 majorants and margin decimals match; exact rational margin
bounds differ by at most1.0361924747907508e-56, as expected from interval precision.
Both separately pass. The prior proxy was not treated as a certificate.

## Why this method can improve on the 5D certificate

For Phi restricted to a cube ray, its quadratic Taylor term is equal at opposite
points and cancels. The two third-order remainders total at mostM3/3. After
dividing by2, the face criterion is

    beta3_i=mu_tilde_i*(1-e0_i-M3_i/6)>epsilon.

This replaces the whole-box first-derivative variation penalty with a cubic
remainder penalty for antipodal pairs. No mathematical property is inferred from
the numerical optimizer itself. The full third-order recurrence includes tanh's
fourth derivative, every coupled parameter injection, all mixed chart coordinates,
implicit y'' and y''', and s_y y''' in the fixed-h composition.

The exact support-aware7/8 gate margin applies to arbitrary full supported
differences, so unselected coordinates need not vanish. Fixed h lets both histories
use the same future control and cancels its direct parameter injection.

By the accepted cube-boundary Borsuk-Ulam argument, a continuous encoder into
R^k with k<6 would collide at an antipodal pair. Uniform epsilon-correct answers
would require distance<=2epsilon, contradicting the certified lower margin.

This third-order criterion does NOT prove that all64 cube corners are pairwise
separated. Do not turn6 continuous coordinates into a6-bit finite-state claim.
Earlier finite-state bounds retain their separate provenance.

## Validation and repairs

- Eight development test cases passed before the executable freeze. They exercise
  CPU execution, tanh fourth derivative, even-term cancellation, product/chain
  rules, exact implicit polynomial compensation including s_y y''', upward
  arithmetic, and tiny dense/independent RTRL-versus-BPTT checks. Third derivatives
  are tested at five declared tiny-chart points per model; these numerical checks
  are bug detectors, not whole-box certificates.
- Both official precision runs passed with unchanged parameters and no nonfinite
  values. Full third tensors have shapes4x10x10x10 and24x10x10x10.
- Twenty-one post-result checks passed: frozen setup/sources, both results, complete
  mixed-tensor shapes, exact cubic contraction dominance, rational query margins,
  strict face arithmetic, fixed-h inclusion, symbolic chain/fourth-derivative
  identities and the complete raw-byte Git archive. Supplemental symbolic checks
  happened AFTER official certification; their timing is not claimed otherwise.
- One pre-freeze source-list syntax draft was corrected by inspection, documented
  in DEVELOPMENT_REPAIRS.md. Post-result checker Git-path and ignored-log issues
  are preserved in VERIFICATION_REPAIRS.md and the diagnostic JSONs. No primary
  scientific method, candidate or outcome was altered after freeze.

## Resources

CPU only, one worker/BLAS thread, torch2.13.0+cpu, deterministic float64
development checks; rigorous gates use dyadic interval arithmetic and explicit
upward positive binary64 tensor bounds, not ordinary GPU results.

- Official192/256 execution:28.515625CPU-s,28.9918712wall-s.
- Setup:13.671875CPU-s,13.9883164wall-s.
- Final development pass:5.296875CPU-s,5.5412725wall-s.
- Preliminary development pass:5.25CPU-s,6.0479701wall-s (retained separately).
- Successful post-result checks:1.28125CPU-s,1.8735772wall-s.
- Total measured:54.015625CPU-s=0.9002604CPU-min; summed measured wall56.4430s.
- Peak measured working set307.96875MiB, from the preliminary development pass.
- Failed-checker/Git/administrative CPU was not metered; conservatively allow
  an additional60CPU-s estimate, separately from the measured ledger. This leaves
  substantial headroom under the frozen20CPU-minute budget.
- GPU/CUDA/model-server use:zero. GAS-0, AGENTS.md and Claude's notebook untouched.

## Strongest uncertainty and next step

The NEW third-order kernel and its implicit-derivative/odd-remainder proof have
not yet received independent hostile review. That is the strongest immediate
uncertainty. The true maximum robust dimension, quantitative width scaling and
practical relevance also remain unresolved; neither this success nor the old
failures give a useful upper bound.

**Single next step:** independent hostile review and cache-free replay of this
frozen6D certificate, especially mixed third derivatives, implicit y''', residual-
safe query margins and the factor1/6. Stop here: no r7, new witness, wider model,
architecture, learning, Stage C or AMS.
