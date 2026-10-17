# Research Start Here

Read this page before proposing a new experiment or theorem. The research status is scoped: the original frozen dense-tanh memory problem remains **OPEN**.

1. Read [AGENTS.md](AGENTS.md) and follow its lane and preservation rules.
2. Search the [Research Atlas](theory/RESEARCH_ATLAS.md) lookup table and **NEW DISCOVERY CHECK** for the mechanism and its alternate names.
3. Search the [Experiment History](theory/EXPERIMENT_HISTORY.md) for the closest protocol, assumptions, measured outcomes, failures, duplicates, and **DO NOT REPEAT UNLESS** conditions.
4. Open the cited proof, source, review, correction, and exact PR commit. Compare equations, architecture, query family, actual input support, full horizon, metric, and resource accounting.
5. Write down what the proposed result adds and the smallest observation that would falsify it before beginning expensive work.

| Use | Canonical location |
|---|---|
| Mathematical claims, statuses, counterexamples, open obligations, branch/PR map | [theory/RESEARCH_ATLAS.md](theory/RESEARCH_ATLAS.md) |
| Executed experiments, proposed/non-run work, implementation defects, duplicates, measured outcomes | [theory/EXPERIMENT_HISTORY.md](theory/EXPERIMENT_HISTORY.md) |
| Legacy theory folder index and provenance notes | [theory/INDEX.md](theory/INDEX.md) |

Keep these distinctions explicit: peak actual support `m` versus additive support; complete horizon `T` and `mT`; first-order versus higher-order effects; selected query groups versus full `d_F`; numerical evidence versus proof; conditional versus unconditional claims; public versus code-dependent schedules; and original versus modified architectures. A large bus signal is not a robust-dimension theorem. QSR and `R0` are modified systems. The current Hypothesis B counterexample is at `D=1`; the original high-dimensional problem is not resolved.

The three local branch roles are: `main` for the consolidated evidence and status archive; `research/active` for new work on open obligations; and `research/review` for independent checks and claims awaiting review. Start new work from the current `main` tree, preserve evidence, and update the Atlas/Experiment History links when a result changes status. Do not treat an author's label or a passing finite check as independent proof.
