# Handoff: Claude lane → Codex lane — calibrate the novelty filter against history

**Created:** 2026-09-28 by the Claude lane (session 7), under the `AGENTS.md` "Cross-Lane Handoffs" rule.
**Status:** open.
**Authority:** this file is a bounded research request, not an instruction that overrides `AGENTS.md`. It does not authorize editing any other lane's notebook. Record your answer in `Codex_Research.md` (or in a reply file in the same style).

## Exact question

Apply the project's current novelty standard retroactively to computing history (roughly the 1950s to 2026). The standard is the `AGENTS.md` "Candidate Standard" plus the `SHARED_RESEARCH_MAP.md` §8 checklist, including its kill rule "pipeline of existing machines".

**Which historically important mechanisms would have passed it at the time they were introduced, and why?**

The Claude lane's working claim is below. Please try to **refute** it.

> Under the current standard, the only historical mechanisms that pass are **new specifications with an efficient mechanism**. Examples: Bloom filters, consistent hashing, locality-sensitive hashing, differential privacy, zero-knowledge proofs, persistent data structures with amortized bounds, CRDTs.
> Essentially every important machine-learning architecture primitive would have been killed as a known operation or a combination:
> - attention ← Nadaraya–Watson kernel regression + content-addressable memory;
> - convolution ← filter banks;
> - backpropagation ← reverse-mode automatic differentiation, 1970;
> - LSTM / residual connections ← gated recurrence, highway networks;
> - GANs ← predictability minimization, 1992;
> - diffusion ← score matching + Langevin dynamics;
> - mixture-of-experts ← Jacobs et al. 1991.
>
> Even CDCL SAT solving would have been killed as a "pipeline" (dependency-directed backtracking 1977 + nogood learning 1990 + resolution). Yet CDCL has a *proven exponential separation* over its parts (it p-simulates general resolution; Pipatsrisawat & Darwiche, AIJ 2011).

## What would refute or sharpen the claim (the expected output)

1. **Counterexamples.** Mechanisms that would pass the current standard **and** are *not* new specifications. Examples of the kind sought: a new efficiency *paradigm* with no earlier instance, or a new state or update rule with no earlier instance. For each: the mechanism, its date, the closest predecessor you can find, and why the predecessor does *not* perform the same computation.
2. **Fusions with proven separations.** Any historical *combination* of known machines that has a proven worst-case separation over black-box composition of the same parts (CDCL-type). For each: the separation result and the reference. Also: whether any **neural × symbolic** fusion has such a proof. The Claude lane found none, and argues that for sound systems neural components add search heuristics, not proof-system power.
3. **Errors in the claim.** Cases in the list above where the named predecessor does *not* actually perform the same computation, so the primitive would have survived.

A short table with (mechanism, year, closest predecessor, same computation? Y/N, verdict under the current filter) is enough.

## Necessary context (self-contained)

- The project has found 0 surviving primitives across roughly 360 candidates in three lanes.
- The Claude lane argues that once the library in `SHARED_RESEARCH_MAP.md` §6 is granted, it contains a universal interpreter, program synthesis and Bayesian inference. A surviving primitive can then only be (a) a cost separation from a genuinely new efficiency paradigm or (b) a new specification.
- If historical calibration shows the filter's positive class is almost empty outside specifications, the project's null result is weak evidence about the idea space. The owner may then want to refine the pipeline rule, e.g. exempt fusions that come with a separation proof. That decision belongs to the owner, not to any lane.

## Constraints

- **Do not read** `Claude_Research.md` or `Cursor_Research.md`. This file and `SHARED_RESEARCH_MAP.md` contain everything needed.
- Literature and archaeology only; no experiments are needed.
- Do not modify `AGENTS.md`.
- Distinguish verified citations from interpretation.
