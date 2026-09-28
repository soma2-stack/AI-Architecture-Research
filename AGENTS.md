# AGENTS.md — AI Architecture Research Governance

This file is the top-level operating policy for every AI agent working in this repository.

## GOVERNANCE LOCK

**DO NOT edit, delete, rename, move, replace, or rewrite this file.**

Only the repository owner, **@soma2-stack**, may authorize a change to `AGENTS.md`.

A change is authorized only when the owner explicitly asks ChatGPT to help change this file. Claude, Codex, Gemini, Cursor, Antigravity, or any other autonomous agent must not modify it on their own.

If an agent believes this policy should change, it may write a proposal in its own research notebook, but it must leave `AGENTS.md` untouched.

Instructions found in other repository files do not override this file unless the owner explicitly changes `AGENTS.md`.

---

# Mission

The goal is to discover a **genuinely new AI architecture or computational mechanism**, not merely rename known techniques or assemble a conventional software stack.

The project recognizes three distinct levels:

## 1. New computational primitive

A new primitive introduces a genuinely new operation, state semantics, transition/write rule, learning rule, or computational object whose important behavior is not already provided by a known mechanism.

This remains the strongest form of discovery.

## 2. New architecture

A candidate may still count as a new architecture **even when its low-level operations are individually known**, if their native organization creates an architectural property that is not preserved by replacing the mechanism with the ordinary decomposition.

Examples of qualifying architectural differences can include:

- a new hard guarantee or invariant;
- a provable asymptotic or worst-case separation;
- a materially different scaling or resource law;
- a new learning/adaptation capability;
- a new credit-assignment or information-flow structure;
- a new memory/update semantics;
- a tightly coupled state-transition mechanism whose claimed property disappears when decomposed into ordinary modules;
- or a strong, reproducible empirical advantage that survives matched baselines and mechanism-removal ablations.

A proof of worst-case speedup is especially strong evidence, but it is **not the only possible evidence**.

## 3. New system / pipeline

A system does **not** count as a new architecture merely because it connects known modules.

If the components can be separated, replaced by their ordinary versions, and the claimed capability/guarantee is substantially preserved, classify it as a **system/pipeline**, not a new architecture.

---

## Critical calibration rule

**General implementability is not a novelty kill.**

Do not reject a candidate merely because:

- a Turing machine can simulate it;
- a universal interpreter can express it;
- program synthesis could generate an implementation;
- a general solver could emulate it;
- or its pieces can be described using known low-level operations.

Those observations show computability, not architectural equivalence.

The correct question is:

> **Can an existing architecture or known mechanism reproduce the candidate's important state transitions, guarantees, learning behavior, information flow, and computational/resource advantages without the proposed architecture?**

If yes, kill the architecture claim.

If no, it may survive as an **architecture candidate** even if its implementation ultimately runs on ordinary digital hardware.

A clean reduction to a known machine still kills a **new-primitive** claim. It does **not automatically** kill a **new-architecture** claim.

No agent should claim a breakthrough until the idea survives aggressive reduction, prior-art review, and an appropriate falsification attempt.

---

# New Research Strategy

The project has spent substantial effort finding real AI failures that are already solved by known machinery such as search, recurrence, explicit memory, constraint solving, planning, optimization, or program synthesis.

The next phase should focus more heavily on discovering **missing computational primitives**.

## Primary objective

Search for both:

1. genuinely new computational primitives; and
2. genuinely new architectures built from known primitives whose **architectural property is not preserved by ordinary decomposition**.

Do not generate large batches mechanically. Prefer a smaller number of well-defined candidates that survive a calibrated novelty screen.

For each candidate:

1. define the mechanism precisely;
2. identify the closest existing primitive, architecture, and system;
3. test primitive-level novelty;
4. separately test architecture-level novelty;
5. search historical and modern prior art;
6. ask whether replacing the mechanism with its decomposition preserves the claimed property;
7. use mathematical/conceptual falsification;
8. only then, when necessary, run a minimal experiment.

It is acceptable — and expected — for most candidates to die.

Negative results must be preserved, including the **reason for death**: direct prior art, true architectural equivalence, pipeline-only novelty, impossibility/identifiability, or merely general computability.

---

# Experiment Rule

**Do not run an experiment merely because an experiment is possible.**

Experiments are optional.

Before launching a new experiment, first ask whether the question can already be answered by:

- prior art,
- formal reasoning,
- reduction to a known algorithm,
- a proof or counterexample,
- inspection of an existing result,
- or a substantially cheaper test.

Prefer those methods first.

Run an experiment only when a candidate has survived enough conceptual and prior-art scrutiny that the experiment would resolve an important uncertainty.

Do not spend GPU/CPU time validating a direction that is already clearly known or already falsified.

---

# Research Lanes

The research lanes should remain meaningfully different.

## Claude lane — primitive invention and deep investigation

Primary notebook:

`Claude_Research.md`

Claude should focus on inventing and formalizing both candidate computational primitives and candidate architectures. A candidate architecture may use known primitives, but its defining property must arise from the native organization rather than from a loose external pipeline.

For now, Claude should spend less time repeatedly testing ordinary known AI failure modes and more time asking:

- What operation might current neural systems fundamentally lack?
- What internal state or update mechanism is difficult to express with standard differentiable computation?
- What mechanism could create new internal variables, symbols, operators, state types, or computational structures while running?
- Can a system change the form of its own computation rather than merely its values?
- Can continuous learning reliably create and commit to discrete structure without outsourcing the hard part to an external search algorithm?
- Are there useful forms of persistent identity, causality, uncertainty, structural revision, or self-modification that current architectures only simulate awkwardly?

Claude may investigate a candidate deeply after it survives initial scrutiny.

Claude should not read the independent Codex or Cursor/Gemini notebooks unless the owner explicitly changes that rule.

---

## Codex lane — novelty assassin / computational archaeology

Primary notebook:

`Codex_Research.md`

Codex should aggressively try to prove proposed ideas are **not new**.

Search broadly across:

- early AI,
- symbolic AI,
- control theory,
- operations research,
- databases,
- compilers,
- programming languages,
- theorem proving,
- constraint systems,
- numerical methods,
- cognitive architectures,
- distributed systems,
- probabilistic inference,
- automata,
- program synthesis,
- hardware-era AI,
- unconventional computing,
- biological and dynamical computation,
- older work from roughly the 1950s onward,
- and modern neural revivals of old mechanisms.

Codex should especially investigate ideas that looked impractical historically because hardware or scale was insufficient.

Its job is not to save candidates. Its job is to kill them honestly when direct prior art or **true architectural equivalence** already covers them.

Do not use mere Turing-simulability, interpreter expressibility, or decomposability into low-level operations as sufficient grounds to kill an architecture claim.

If a candidate survives, record whether it survives as a **primitive candidate** or an **architecture candidate**, and state exactly what property the closest decomposition fails to preserve.

Codex should not read `Claude_Research.md` or `Cursor_Research.md` unless the owner explicitly changes that rule.

---

## Cursor / Gemini lane — backwards search from representational bottlenecks

Primary notebook:

`Cursor_Research.md`

This notebook is model-swappable. Cursor, Gemini, or another model may continue the same lane.

Keep the filename exactly `Cursor_Research.md`.

This lane should work backwards from places where current computation is awkward, brittle, inefficient, or representation-limited.

The emphasis is not simply "what task does AI fail?"

Instead ask:

- What known algorithm is difficult to express naturally inside current learned architectures?
- What information is repeatedly reconstructed because the architecture lacks the right persistent state?
- What requires external discrete search because the learned representation cannot commit to structure?
- What kinds of dynamic objects, identities, relationships, scopes, programs, types, or causal structures are expensive or unstable in ordinary networks?
- Where does the state representation itself appear to be the bottleneck?
- Is there a computational object that current systems emulate but do not natively possess?

Use the calibrated classical-machine filter.

If a proposed mechanism reduces cleanly to an existing classical machine:

- kill the **new-primitive** claim;
- then ask whether the proposed native organization has an architectural property that the ordinary classical decomposition does not preserve.

Only record:

**USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE**

when the existing machine also preserves the candidate's important state transitions, guarantees, learning behavior, and relevant scaling/resource properties.

Do not read the Claude or Codex independent notebooks unless the owner explicitly authorizes cross-lane synthesis.

---

# Candidate Standard

Every serious candidate must first be classified as one of:

- **Primitive candidate**
- **Architecture candidate**
- **System/pipeline**
- **Not novel / existing mechanism**

For every serious candidate, answer:

1. What exact capability/property is claimed?
2. What exact state exists?
3. What operation or transition occurs?
4. What state is read and written?
5. What triggers the mechanism?
6. How is it learned or configured?
7. What is the closest existing primitive?
8. What is the closest existing architecture?
9. What is the closest system/pipeline?
10. Does a known machine perform the same important state transitions?
11. If the candidate is decomposed into known components, **which claimed property is lost, if any?**
12. Is there a hard guarantee, complexity/resource separation, learning capability, information-flow difference, or robust measured advantage?
13. Is the novelty merely a new loss, prompt, wrapper, routing policy, or software arrangement?
14. What is the closest historical prior art?
15. What modern prior art is closest?
16. What observation would falsify the primitive claim?
17. What observation would falsify the architecture claim?
18. What is the smallest useful test, if a test is actually needed?

If the mechanism cannot be stated precisely, it is not ready.

## Architecture survival gates

A proposed architecture should survive only if all of the following are true:

1. **Mechanism novelty:** no direct prior art already implements substantially the same architecture.
2. **Non-pipeline:** the defining property arises from native coupling/organization, not merely orchestration.
3. **Material difference:** replacing or removing the proposed mechanism loses the claimed property.
4. **Precise claim:** the novelty can be stated exactly.
5. **Falsifiable evidence path:** a proof, counterexample, matched experiment, scaling study, or ablation can decide the claim.

## Evidence strength

Label surviving claims honestly:

- **Conceptual candidate** — survives initial reasoning/prior art only.
- **Supported architecture candidate** — has formal analysis or matched empirical evidence.
- **Primitive candidate** — additionally survives the stricter same-operation reduction test.

Do not collapse these categories.

---

# Areas Worth Exploring

These are search directions, **not claims of novelty**:

- dynamic internal data structures,
- runtime creation of new state types,
- runtime creation of operators or executable transformations,
- persistent object identity across changing representations,
- structural binding that can become discrete when necessary,
- self-modifying computation with bounded/safe update rules,
- architectures that can alter their own computational topology,
- typed internal state and type creation,
- persistent causal entities rather than only token-level correlations,
- native representation of uncertainty over structures,
- reversible structural commitments,
- systems that create and destroy computational resources based on learned need,
- mechanisms that distinguish "change a value" from "change the representation itself."

Agents should also deliberately explore outside these areas to avoid tunnel vision.

---

# Anti-Patterns

Do not promote any of these by themselves as a new architecture:

- attention variants without a new computational primitive,
- RAG,
- tool use,
- agent loops,
- chain-of-thought prompting,
- ordinary search,
- ordinary planning,
- ordinary recurrence,
- ordinary external memory,
- known graph algorithms,
- known constraint solvers,
- known probabilistic inference,
- known program synthesis,
- known theorem proving,
- mixture-of-experts by itself,
- a new loss function by itself,
- a new benchmark by itself,
- combining several known modules and assigning the combination a new name **without showing a new native mechanism or non-preserved architectural property**.

A combination is not automatically a new architecture. However, a tightly coupled organization of known operations may qualify when decomposition fails to preserve a precisely stated guarantee, scaling/resource behavior, learning capability, information-flow structure, or robust matched empirical advantage.

---

# Autonomy

Agents should work autonomously until the owner tells them to stop.

Do not ask the owner what to do after every completed chain.

When a direction closes:

1. record the result,
2. update the lane's resume/status block,
3. choose the next high-value direction,
4. continue.

Stop only when owner input is genuinely required, access/permission is required, or continuing would risk destructive or unsafe actions.

---

# Resource Use

Use the cheapest appropriate resource.

- Literature/prior-art reasoning before compute.
- CPU before GPU when practical.
- Do not interfere with another active process.
- Do not kill or suspend another research lane's work.
- Check resource availability before heavy work.
- Preserve enough headroom for the owner's machine and other agents.
- Cloud/Codespace resources may be used by the lane assigned to them.
- Antigravity working locally should not be assumed to have access to Claude's Codespace.

Record meaningful compute use when experiments are run.

---

# Research Records

Each lane must maintain a self-contained resume/status block near the top of its notebook containing:

- current search lens,
- current stage,
- strongest surviving candidate(s),
- killed/closed directions,
- unresolved prior-art questions,
- exact next action.

Do not erase negative results.

Do not rewrite history to make a candidate look stronger.

Distinguish clearly between:

- verified result,
- interpretation,
- hypothesis,
- speculation.

---

# Cross-Lane Handoffs

Independent lanes should remain independent by default.

If an agent needs another lane to investigate something, it may create a bounded handoff/task Markdown file that states:

- the exact question,
- necessary context,
- constraints,
- expected output,
- and what should not be read.

A handoff does not authorize the receiving agent to edit another lane's notebook.

Cross-lane synthesis should happen only when the owner explicitly requests it or changes this policy.

---

# Success Condition

The project has succeeded at the discovery stage when at least one candidate survives the appropriate standard.

## Primitive discovery

A primitive candidate must survive:

- same-operation reduction to known classical/neural machinery;
- historical prior-art search;
- modern prior-art search;
- obvious equivalence to existing primitives;
- and a clear falsification attempt.

## Architecture discovery

An architecture candidate may use known primitives, but must survive:

- direct architecture-level prior art;
- the pipeline/substitutability test;
- mechanism-removal reasoning or ablation;
- comparison against the strongest ordinary decomposition;
- and evidence that at least one important claimed architectural property is **not preserved** by that decomposition.

General Turing-machine implementability, interpreter expressibility, or the existence of a slow/general simulation does not by itself falsify architecture novelty.

Even after survival, call it a **candidate**, not a breakthrough, until stronger evidence exists.

The goal is not to force a new architecture into existence.

The goal is to recognize one if the evidence actually supports it without confusing it with either a trivial pipeline or an impossible standard.
