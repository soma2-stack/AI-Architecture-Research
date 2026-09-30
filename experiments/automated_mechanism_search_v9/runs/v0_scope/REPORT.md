# AMS v9 V0-SCOPE result

**Verdict: INSUFFICIENT SCIENTIFIC JUSTIFICATION — STOP BEFORE TRAINING.**

Owner authorization: CPU-only Stages 0–3 under the unchanged proposed
preregistration. Authorization does not waive Section 2's V0-SCOPE gate.
Repository inspected: `c642ffbfec063623e200d044d575ee874a39a671`.
Preregistration file SHA-256:
`4396a5849d775a5c026b134d9d006a9d43980772c95782ee2c7c4f6701ed3ab4`.

This is a literature/formal scope result, not an empirical search result.
No candidate was generated, trained, probed, promoted or rejected by a numerical
gate. Stages 0 implementation/calibration and Stages 1–3 were not launched.
No protocol, seed, threshold, baseline, task or resource setting was changed.
GAS-0, AGENTS.md, historical AMS/OMD results and other-lane notebooks were untouched.

## 1. Exact claim reviewed

At fixed parameters within each sequence, the proposed state is
`h[8], U[8,2], V[2,154], s[1]`, initialized to zero. Old factors enter a
bounded forward residual; current local derivatives J/R and activity enter
factor writes. A terminal error contracts the new factor product to update
parameters once. The proposed property is better sparse-terminal-feedback
learning at matched parameters, state and compute, caused by the forward/credit
organization rather than a new estimator, recurrent cell or optimizer alone.

The preregistration's sole proposed new justification was S1's feedback-density
scope condition. Section 2 explicitly requires stopping if full-source evidence
does not justify that hypothesis. The complete S1 paper was accessible in this
review; its abstract had been the basis of the earlier proposal.

## 2. What full-source inspection changed

S1 Section 4.4/Table 7 reports unsuccessful sparse-feedback controls: adding-task
MSE is .189 for BPTT and .289 for full RTRL, versus .167 for the trivial predictor.
The paper acknowledges that its architecture/task comparison does not isolate
gradient approximation. It nevertheless attributes poorer RTRL performance to
missing continuous corrective feedback in Sections 4.4/5.4. This evidence does
not isolate feedback density from learnability, conditioning, implementation or
optimization. No public implementation link was identified in the inspected
paper or the targeted title/code search; its code was not verified or executed.
This is an access limitation, not a claim that code cannot exist.
[S1, version 2, Sections 4.4/5.4 and Table 7](https://arxiv.org/pdf/2603.15195v2).

**Audit inference:** the broad failure explanation cannot justify the particular
architectural exception proposed by v9. A narrower empirical hypothesis about
finite-precision sensitivity transport remains possible, but it is not established
by a comparison without a successful task control. This does not invalidate the
paper's separate dense-feedback findings.

## 3. Formal discriminator, without running an experiment

For a differentiable recurrent system with parameters fixed during the sequence,

`h_t = f(h_(t-1), x_t, theta)`

`M_t = A_t M_(t-1) + B_t`,

where `M_t = d h_t / d theta`, `A_t = partial f / partial h_(t-1)` and
`B_t = partial f / partial theta`. Starting at `M_0=0`, induction gives the
same chain-rule derivative as unrolled reverse-mode differentiation. For a
terminal loss the gradient is its hidden-state cotangent times `M_T`, plus
the direct readout term. Neither the recurrence nor the induction contains an
intermediate loss or error. This is the actual RTRL recurrence, not a universal
simulation argument. [S5, Section 3.1, Equations 4–5](https://arxiv.org/html/1702.05043).

Consequently, absent continuous error cannot by itself make exact forward-mode
differentiation wrong in the setting v9 freezes. Finite-precision error, exploding
or vanishing sensitivity, approximate-estimator noise, and stale sensitivities
when parameters change can matter. Those are distinct hypotheses; the formal
identity does not prove good task performance or numerically identical floating
point outputs. It rules out interpreting missing intermediate errors as a general
architectural need for sensitivity 'grounding'. KF-RTRL explicitly discusses
parameter-change staleness separately from the fixed-parameter recurrence.
[S6, Section 3, Equations 1–3](https://proceedings.neurips.cc/paper_files/paper/2018/file/dba132f6ab6a3e3d17a8d59e82105f4c-Paper.pdf).

The candidate's omission of old U/V/s sensitivities is already declared a
surrogate derivative in the preregistration. It cannot inherit an exact-RTRL
guarantee from the base factor update. No candidate exists whose surrogate
improves the proposed property; that remains untested.

## 4. S1–S9 collision review

| Source | Material inspected | Relevance and limits |
|---|---|---|
| S1 | Full v2 PDF, especially Sections 4.4/5.4; code search found no attributable implementation | Sparse-feedback justification fails the causal/control check above. |
| S2 | Full RTU HTML, Sections 3–5 and Appendices E.5/E.6 | Known forward state plus carried gradient traces, linear resource scaling, and reverse-mode integration. No claim that RTU matches every proposed factor-feedback program. |
| S3 | Full v2 PDF, introduction and streaming method | RTU sensitivities compose with streaming eligibility traces; delayed credit is already an explicit target. Not a matched numerical comparison to v9. |
| S4 | Primary indexed conference PDF abstract/introduction; direct PDF fetch blocked | SnAp selects influence entries by recurrent connectivity. Not treated as a complete reproduction or proof of equivalence. |
| S5 | Full HTML, Sections 2–3.4 and Algorithm 1; author repository identified | Known sensitivity recursion, stochastic factor compression and rank-r variants. No source code executed. |
| S6 | Primary indexed NeurIPS PDF equations/theorem and arXiv abstract | Known factorized credit transport; stability assumptions and parameter staleness are explicit. |
| S7 | Primary indexed PMLR PDF Algorithms 2–3; author repository identified | Known rank-budgeted stochastic compression with a variance objective. Direct full-page fetch was unavailable. |
| S8 | Primary article indexed methods and author-deposited PMC text; official code repository identified | Known local eligibility combined with later learning signals and slow neuronal state. Spiking results are not relabeled as tanh results. |
| S9 | Full author arXiv HTML and indexed ICML PDF Section 2.5 | Recurrent forward plasticity, eligibility and trial-terminal reward already coexist. Its state, learning protocol and resources differ from v9. |

Source locations, retaining the preregistration's S labels:

- [S2: RTUs](https://arxiv.org/html/2409.01449), especially Appendix E.5/E.6.
- [S3: streaming RTRL](https://arxiv.org/pdf/2605.24709), v2, Sections 1–3.
- [S4: SnAp](https://openreview.net/pdf?id=q3KSThy2GwB).
- [S5: UORO](https://arxiv.org/html/1702.05043);
  [author repository](https://github.com/ctallec/uoro).
- [S6: KF-RTRL](https://proceedings.neurips.cc/paper_files/paper/2018/file/dba132f6ab6a3e3d17a8d59e82105f4c-Paper.pdf).
- [S7: OK](https://proceedings.mlr.press/v97/benzing19a/benzing19a.pdf);
  [author repository](https://github.com/marcelomatheusgauy/optimal_kronecker_approximation).
- [S8: e-prop](https://pmc.ncbi.nlm.nih.gov/articles/PMC7367848/);
  [author repository](https://github.com/IGITUGraz/eligibility_propagation).
- [S9: recurrent plasticity](https://arxiv.org/html/2112.08588), Section 2.5;
  [published record](https://proceedings.mlr.press/v202/miconi23a.html).

No secondary reproduction was used to establish a primary-source claim. This
review did not complete executable reference pinning: the earlier scope gate
failed first, and no reference implementation is represented as validated.

## 5. Ordinary decomposition and boundary of the verdict

The frozen state is already partitioned into forward h and credit U/V/s. An
ordinary recurrent cell can read the old credit buffers; an online sensitivity
module can read the same old state and current J/R. Ordered reads followed by
simultaneous writes preserve the specified schedule. In one process, a shared
buffer interface needs no additional persistent numerical state, extra parameter,
additional model evaluation or mandatory bidirectional copy. This is a concrete
interface decomposition of the header and timing, not a Turing-machine reduction.

However, preserving an as-yet-unknown candidate expression at each module boundary
does not prove that a published fixed rule reproduces every possible searched
transition or empirical advantage. The scope verdict therefore is **not**
`CLOSED AT DESIGN GATE — KNOWN ORGANIZATION` for all possible programs. Known
references occupy the generic organization; the additional scientific rationale
for reopening it fails. No claim is made that all temporal-credit research is
exhausted, or that all future programs are prior art.

## 6. Results, resources and stop

| Item | Result |
|---|---|
| V0-SCOPE | FAIL — INSUFFICIENT SCIENTIFIC JUSTIFICATION |
| Stage-0 implementation/probes/profile | NOT RUN |
| Stage-1 numerical validity | NOT RUN |
| Stage-2 generation/training/confirmation | NOT RUN |
| Stage-3 controls/ablation/prior-art promotion | NOT RUN |
| Programs generated / trained / numerically rejected | 0 / 0 / 0 |
| Empirically classified rediscoveries / survivors | 0 / 0 |
| Training steps / official seeds consumed | 0 / none |
| Experimental CPU / wall time | 0 / 0 seconds; no numerical workload launched |
| Numerical worker RAM peak | Not applicable; no numerical worker existed |
| Literature/administrative CPU, wall and RAM | Not instrumented; not represented as measured zero |
| GPU / CUDA / llama.cpp use by this task | None |
| Existing shared experiment ledger | 18,706.656 CPU-s; unchanged |

The single rejection is of the **design justification**, not an empirical
negative candidate. Browsing and light file/Git operations occurred; no CPU
profiling, training, benchmark, dependency import or device initialization occurred.
No candidate deserves independent prior-art review or Stage 4 on this record.
Stop now. Replacing the motivating hypothesis, changing the search family, or
launching calibration despite this result would require a new owner-reviewed
scientific decision; this authorization supplies none of those changes.
