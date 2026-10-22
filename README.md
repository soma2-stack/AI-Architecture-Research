# AI Architecture Research

**Research is frozen unless the owner explicitly authorizes a specific new task.**
Read the [claim register](docs/CLAIM_REGISTER.md) before proposing work. PR36's
3,000-update rerun is withdrawn; PR37's repeat C5 is NO-GO. OPEN questions and old
next-action lists are not authorization. The organizational register from
[PR38](https://github.com/soma2-stack/AI-Architecture-Research/pull/38) is merged
and authoritative on main. [PR39](https://github.com/soma2-stack/AI-Architecture-Research/pull/39)
proposes additional repository navigation and experiment-record improvements.

This repository preserves research on computational mechanisms, architecture novelty, and robust recurrent learning-credit memory. The current theory asks how much continuous learning state is required to answer later normalized gradient queries. It has mathematical constructions and scoped negative results, with substantial open questions.

## Main theorem target

The central open problem in this repository is whether a legal RNN construction can achieve:

$$
D = \Omega(n)
$$

while simultaneously keeping

$$
mT = o\!\left(n^{3/2}\right)
$$

Here, **D** is the robust learning-credit dimension, **n** is the recurrent width, **m** is the active history/input width, and **T** is the time horizon.

In plain language: can robust learning-credit dimension scale linearly with model width while peak actual input support times the complete horizon remains strictly below the n³⁄² scaling boundary?

**Current status: OPEN.**

## Start here

| Destination | What it answers |
|---|---|
| [Current research](theory/CURRENT_THEORY.md) · [claim register](docs/CLAIM_REGISTER.md) | What is established, refuted, independently verified, or still open; exact evidence and scope. |
| [Experiments](experiments/INDEX.md) | What was run, its recorded outcome, and links to reports, code, raw results, and related claims. |
| [Active work](04_RESEARCH_STATE.md#current-authorization) | What is currently authorized. The present freeze remains unless the owner explicitly authorizes a particular task. |
| [Archived work](theory/INDEX.md#historical-folder-inventory) · [experiment archive](experiments/INDEX.md#historical-october6-finite-size-index-preserved) | Where older, failed, superseded, withdrawn, and unrun work is preserved. |

### Research and evidence

Read in this order:

1. [AGENTS.md](AGENTS.md) — locked repository governance.
2. [docs/CLAIM_REGISTER.md](docs/CLAIM_REGISTER.md) — current freeze, claims, exact evidence and retirement decisions.
3. [04_RESEARCH_STATE.md](04_RESEARCH_STATE.md) — current organizational resume point.
4. [theory/CURRENT_THEORY.md](theory/CURRENT_THEORY.md) and [theory/INDEX.md](theory/INDEX.md) — scoped theory navigation.
5. [experiments/INDEX.md](experiments/INDEX.md) — completed, stopped, unrun and unavailable records.

Historical proof folders and docs/history/SHARED_RESEARCH_MAP.md retain provenance;
their old “current” and “next” wording does not supersede the register or authorize work.

`theory/` contains proofs, scoped derivations, reviews, and drafts. `experiments/` contains diagnostic and certification code, frozen inputs, replay outputs, and other experimental evidence. Experiments do not automatically validate a theorem or establish an architecture.

Owner disposition and independent review are separate axes. ACCEPTED records owner acceptance; VERIFIED requires independent review evidence in its stated scope. A result can be owner-accepted and also have independent review, which is recorded separately in the theory index. Author-local labels such as `PROVED` inside preserved reports do not by themselves create repository-level VERIFIED status. PENDING REVIEW and CONDITIONAL remain unresolved. REFUTED, SUPERSEDED, HISTORICAL, and DRAFT records are kept so later researchers can reconstruct decisions and avoid repeating failed routes. A folder being committed does not certify its claims.

`docs/notebooks/Claude_Research.md`, `docs/notebooks/Codex_Research.md`, and `docs/notebooks/Cursor_Research.md` are archival notebooks with detailed provenance. They are optional detail sources rather than onboarding requirements; their lane-reading rules remain governed by AGENTS.md. Historical failed work, outputs, and review records are intentionally preserved.

[docs/audits/REPOSITORY_CLEANUP_AUDIT.md](docs/audits/REPOSITORY_CLEANUP_AUDIT.md) records the consolidation, branch inventory, artifact sizes, and proposed future storage policy. No artifact migration or history shrinking is performed in this pass.


Older handoffs, protocols, audits, preservation manifests, and historical maps are grouped under [`docs/`](docs/README.md) so the repository root stays focused on the files needed for current work.

Repository maintenance, branch/PR dispositions and local preservation: [cleanup execution record](docs/audits/REPOSITORY_CLEANUP_AUDIT.md). Scientific status remains governed by the claim register.
