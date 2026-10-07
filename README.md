# AI Architecture Research

This repository preserves research on computational mechanisms, architecture novelty, and robust recurrent learning-credit memory. The current theory asks how much continuous learning state is required to answer later normalized gradient queries. It has mathematical constructions and scoped negative results, with substantial open questions.

## Main theorem target

The central open problem in this repository is whether a legal RNN construction can achieve:

**D = Ω(n)**

while simultaneously keeping

**mT = o(n³⁄²)**

Here, **D** is the robust learning-credit dimension, **n** is the recurrent width, **m** is the active history/input width, and **T** is the time horizon.

In plain language: can robust learning-credit dimension scale linearly with model width while the total coordinate-time cost remains strictly below the n³⁄² scaling boundary?

**Current status: OPEN.**

Read in this order:

1. [README.md](README.md)
2. [AGENTS.md](AGENTS.md) — repository governance
3. [04_RESEARCH_STATE.md](04_RESEARCH_STATE.md) — brief resume point
4. [theory/CURRENT_THEORY.md](theory/CURRENT_THEORY.md) — authoritative current theory
5. [theory/INDEX.md](theory/INDEX.md) — all theory folders and evidence relationships
6. [experiments/INDEX.md](experiments/INDEX.md) — finite-size evidence and limits
7. [theory/codex_linear_dimension_frontier_20261006/PROOF.md](theory/codex_linear_dimension_frontier_20261006/PROOF.md) — current proof record
8. [docs/history/SHARED_RESEARCH_MAP.md](docs/history/SHARED_RESEARCH_MAP.md) — current checkpoint followed by historical context

`theory/` contains proofs, scoped derivations, reviews, and drafts. `experiments/` contains diagnostic and certification code, frozen inputs, replay outputs, and other experimental evidence. Experiments do not automatically validate a theorem or establish an architecture.

Owner disposition and independent review are separate axes. ACCEPTED records owner acceptance; VERIFIED requires independent review evidence in its stated scope. A result can be owner-accepted and also have independent review, which is recorded separately in the theory index. Author-local labels such as `PROVED` inside preserved reports do not by themselves create repository-level VERIFIED status. PENDING REVIEW and CONDITIONAL remain unresolved. REFUTED, SUPERSEDED, HISTORICAL, and DRAFT records are kept so later researchers can reconstruct decisions and avoid repeating failed routes. A folder being committed does not certify its claims.

`docs/notebooks/Claude_Research.md`, `docs/notebooks/Codex_Research.md`, and `docs/notebooks/Cursor_Research.md` are archival notebooks with detailed provenance. They are optional detail sources rather than onboarding requirements; their lane-reading rules remain governed by AGENTS.md. Historical failed work, outputs, and review records are intentionally preserved.

[docs/audits/REPOSITORY_CLEANUP_AUDIT.md](docs/audits/REPOSITORY_CLEANUP_AUDIT.md) records the consolidation, branch inventory, artifact sizes, and proposed future storage policy. No artifact migration or history shrinking is performed in this pass.


Older handoffs, protocols, audits, preservation manifests, and historical maps are grouped under [`docs/`](docs/README.md) so the repository root stays focused on the files needed for current work.
