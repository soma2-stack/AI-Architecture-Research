# Handoff — post-v8 grammar-gap audit: Claude's candidate set and final GG2 closure (for Codex and Cursor/Gemini)

**From:** Claude lane (session 21, 2026-09-28; GG2 closure in session 22). This is a bounded handoff under AGENTS.md "Cross-Lane Handoffs".

> **FINAL STATUS (session 22): all 8 candidates are KILLED. GG2: KILLED — PIPELINE / COMPOSITION ONLY** (see "GG2 closure" at the end). No hostile reduction or matched experiment is requested. Claude recommends closing the current AMS grammar-expansion path.
**Scope:** reasoning and prior art only. No code, search, training or GPU is requested. The preregistration is unchanged (v8), and no v9 exists.
**Do not read:** `Claude_Research.md`. This file is self-contained. It also does not authorize editing another lane's notebook.

## Exact question

Can any of the operations below be expressed only by a broader AMS grammar, and still survive hostile reduction to known machinery? The target failures are:
- **B:** retain T1 while learning T2 on a sign-flipped shared map;
- **C\*:** fast R1 re-adaptation with R0 return stability;
- **F:** escape the x3 shortcut on the 3-parity task with 100 examples.

## What the frozen AMS grammar cannot express

| # | Gap |
|---|---|
| g1 | Event-triggered writes, latches, data-dependent state lifetime (register decays are constants) |
| g2 | Indexed multi-slot state and content-addressed retrieval (≤ 4 registers; one `W_ep0` anchor) |
| g3 | Structural ops other than threshold reinit/freeze of output rows every 100 steps (no copy, restore, fork, merge, edge deletion or latched freeze) |
| g4 | Topology change (fixed 32 × 32 MLP) |
| g5 | On-demand creation of context × input (higher-order) weight terms |
| g6 | Per-layer heterogeneity |
| g7 | Discrete hypothesis objects |
| g8 | Example memory (replay; excluded by design) |

## Candidates and Claude's verdicts

| ID | Task | State + operation + transition (short) | Claude's reduction | Verdict |
|---|---|---|---|---|
| GG1 | B | Latched unit **fork** on persistent gradient anti-alignment; the copies are gated by input signature | DEN (2018) split/duplicate + task-free routing (CN-DPM 2020, Active Dendrites 2022, FTN arXiv 2604.24637) | KILLED |
| **GG2** | **B** | The **conflicting gradient component is re-homed** into a new cue-gated low-rank term, `u vᵀ ⊙ gate(a)`, keyed on the inputs whose statistics changed since consolidation. The non-conflicting part updates W. No stored data, task ID or router training. | Probably task-free LoRA adapters + cue router (InfLoRA / O-LoRA, MoE-adapters), TRGP (needs task ID), XdG / Active Dendrites (external cue), PCGrad / OWM / GPM (drop or project, not re-home), gradient routing (user masks), COIN | **KILLED — PIPELINE / COMPOSITION ONLY** (session-22 closure; see below) |
| GG3 | C\* | Error-signature-keyed snapshot bank with discrete restore | Narendra–Balakrishnan multiple models, switching and tuning (1992–97); recurring-concept pools; MOLe (2019); CN-DPM; COIN (2021); FTN (2026) | KILLED |
| GG4 | C\* | Provisional Δ with hysteretic capture into W_c after the regime persists | Fast/slow weights; synaptic tagging and capture; Benna–Fusi cascade; metaplasticity (Laborieux 2021). Cannot beat the trade-off at C\*'s 64-step segments. | KILLED |
| GG5 | C\*/B | Surprise-gated register decay, and clear-on-surprise | LSTM forget gate; BOCPD run-length reset; ART reset; surprise-modulated learning rates | KILLED |
| GG6 | B/C\* | Parameter superposition with a self-inferred context key | PSP (Cheung 2019) + SupSup task inference (2020); HRR / VSA binding | KILLED |
| GG7 | F | Counterexample-refuted **input-edge deletion** | Candidate elimination (Mitchell 1977); JTT / LfF / DFR; DEEP R / SET / RigL. Fails on F: 3-parity from 100 examples stays unlearnable by an MLP. | KILLED |
| GG8 | F | In-loop **crystallization** of units that become exact k-input boolean rules | Rule extraction; logic-gate networks (Petersen 2022); ∂ILP. On F, x3 units crystallize first, locking in the shortcut. | KILLED |

Structural notes:
- **C\* no-go:** improving both second-entry AULC and R0 return needs regime-specific state that grows with the number of recurring regimes. Both corners are occupied: the bank (GG3) and the trade-off (GG4).
- **B trichotomy:** isolation/expansion, replay, or re-homing (GG2).
- **F** reduces to discrete hypothesis search: V3-F synthesis already reaches OOD 1.00.

## Expected output

- **Codex:** a hostile reduction of GG2 (and any candidate above whose kill you dispute). Name exact prior art implementing "re-home the conflicting update component into context-conditional parameters, keyed by an input-statistics change, without task IDs", or state precisely which transition semantics remain unmatched.
- **Cursor/Gemini:** if GG2 is not reduced, the smallest matched Task-B experiment separating GG2 from "shared trunk + task-free LoRA adapter + input-cue router" at equal parameters and state. The measurable property must be something the decomposition cannot realize, not just a benchmark win. Also check that it fits in the remaining ~24.9 CPU-h.
- **Claude's recommendation:** if GG2 dies in either lane, close the AMS grammar-expansion path rather than spend the remaining budget on another search.


---

## GG2 closure (session 22) — final

**Verdict: KILLED — PIPELINE / COMPOSITION ONLY.** No code, training, search or GPU; 15 targeted prior-art searches.

**The conjunction checked:**

| Piece | Meaning |
|---|---|
| P1 | Conflict detection against consolidated knowledge |
| P2 | Preserve the non-conflicting shared update |
| P3 | Allocate new parameter state for the conflicting component |
| P4 | Context-condition that state |
| P5 | Infer the context from the input stream |
| P6 | No replay, task ID, manual mask, or trained router |

**Closest prior art** (✔ implements, ◐ partial, ✘ no):

| Mechanism | P1 | P2 | P3 | P4 | P5 | P6 |
|---|---|---|---|---|---|---|
| **TRGP** (Lin et al., ICLR 2022): trust region by gradient-projection norm onto old input subspaces; a layer-wise scaling matrix = new small state inside the old / conflicting subspace; the model updates orthogonally | ✔ | ✔ | ✔ | ✔ (task) | ✘ | ✘ (task ID) |
| API (CVPR 2023): expands dimensions when gradient projection starves plasticity | ✔ | ✔ | ✔ | ◐ | ✘ | ✘ |
| Recon (ICLR 2023): high-conflict layers become task-specific | ✔ | ✔ | ✔ | ✔ | ✘ | ✘ |
| GPM / OWM / OGD; PCGrad; A-GEM | ✔ | ✔ | ✘ (discard) | ✘ | ✘ | ◐ / ✘ |
| InfLoRA (2024): low-rank branch placed **orthogonal** to the conflict | ✔ | ◐ | ✔ | ✘ | ✘ | ◐ |
| Latent-LoRA (arXiv 2607.23837, 2026): gradient-free probabilistic routing, no trainable router, replay-free | ✘ | ✘ | ✔ | ✔ | ✔ | ✔ |
| SEMA (2025); LMC (2021); Expert Gate (2017); HNET + entropy (2020) | ✘ | ✘ / ◐ | ✔ | ✔ | ✔ | ◐ |
| RAN (Platt 1991): allocates an input-gated rank-1 unit on large error ∧ novelty, LMS update otherwise | ◐ | ✔ | ✔ | ✔ | ✔ | ✔ |
| RFWR / LWPR (1998–2005); eTS (2004): local models allocated on input novelty, explicitly anti-interference | ◐ | ✔ | ✔ | ✔ | ✔ | ✔ |
| **Fuzzy ARTMAP** (1992): predictive mismatch with a consolidated category → match tracking allocates a new input-matched category instead of overwriting | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ (prototype architecture, not a distributed trunk) |
| XdG / Active Dendrites; gradient routing; COIN / CN-DPM; multiple models, switching and tuning; PSP / SupSup | partial: context supplied, user masks, novelty-triggered, or keyed on performance |

**Ordinary decomposition (it preserves every GG2 property):**
- a shared trunk;
- a GPM / TRGP projector: the shared update is ΔW(I − UUᵀ);
- on persistent in-U conflict, allocate a TRGP-style low-rank / scaling term acting inside U, trained by the loss (its gradient is exactly the in-U signal that GPM discards, so re-homing emerges);
- a gate from a gradient-free density model of the post-change input statistics (Latent-LoRA / LWPR / RAN), fixed at allocation.

This gives T1 retention (U is protected and the gate is off on T1), T2 learning of the sign flip (the gated term acts in U), continued non-conflicting shared learning, no replay / task ID / mask / trained router, and capacity allocated only at conflict. Writing Δ_∥ directly into u vᵀ, versus training the term by its own gradient, is a parameterization detail. **No claimed property is lost.**

**What kills GG2:** TRGP already performs the distinctive move (new small state inside the conflicting subspace while the shared weights update orthogonally), lacking only a task-free key. Established gradient-free input-keyed routing supplies that key (1991–2026). Their composition preserves every property, and the transition principle is ARTMAP / RAN's "conflict allocates new input-keyed state instead of overwriting".

**Recommendation:** close the current AMS grammar-expansion path. No v9. The remaining ~24.9 CPU-h stay unspent.
