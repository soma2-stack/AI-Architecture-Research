# Handoff: Independent audit of OMD-0 T1 RET validity

## Question

Audit whether the OMD-0 T1 retention target is identifiable and whether a tiny recurrent eviction policy could be extracted into a causal, reproducible rule. This is a bounded handoff for the Cursor/Gemini lane. The Codex verdict is only “SURVIVES AS OMD TARGET”; no candidate mechanism exists.

## Context

Target workload: cache capacity 16–32; hidden abrupt/semimarkov switches among drifting Zipf ranks, working-set phases, one-hit scans, loops longer than capacity, bursts, and periodic reuse. The proposed discovery instrument has two state values per resident slot, one shared global state, shared tiny event update functions, slot-hit/tick/miss inputs, no semantic item IDs, and no explicit regime labels. The intended process would train the instrument, extract its transition rule, transplant it into ordinary code, then assess novelty.

Known collision families include ARC/CAR, SIEVE/S3-FIFO, EVA/LHD/3L-Cache, LeCaR/CACHEUS/H-MC, RLR, Glider, evolved insertion/promotion vectors, PolicySmith, CacheQuery, CacheCraft, S4-FIFO/LAH, and SCION. See AR-147 in Codex_Research.md for precise boundaries and sources. Do not read Claude_Research.md or use its full contents as input.

## Audit tasks

1. **Identifiability:** Determine whether the learned state and event update semantics are identifiable from ordinary training trajectories. Analyze slot permutations, latent-state transformations, redundant state coordinates, aliasing, and unseen transition regions.
2. **Extraction validity:** Specify the minimum evidence needed to show that a symbolic/plain-code transition is behaviorally and causally equivalent to the trained controller. Include counterfactual event/state interventions, long rollouts, initialization/reset, tie-breaking, slot permutation, and rare scan/burst/phase-transition states.
3. **Ordinary decomposition:** State the strongest resource-matched baseline set needed to distinguish a learned controller from expert mixing, feature/value ranking, a cache-level controller, and compact policy search. Include local state bytes, global state, per-request update work, shadow-policy overhead, and any lazy-clock replacement for the all-slot tick.
4. **Pilot decision:** Recommend the smallest CPU-only pilot that can test identifiability and extraction before a larger search. Do not execute it. Say whether any such pilot can be preregistered without first fixing the unresolved state/input/output contract.
5. **GRUMA check:** If accessible, determine whether GRUMA already uses per-object recurrent state with online event updates and evaluates nonstationary mixed reuse. Report exact evidence and its limit. Do not infer details from title/abstract alone.

## Constraints and expected output

- Literature and formal reasoning only; no code, training, benchmark, GPU, or CPU-heavy job.
- Do not freeze or edit OMD-1 or any frozen protocol.
- Do not edit Codex_Research.md, Claude_Research.md, or Cursor_Research.md. Return a short standalone audit note to the owner or create a separate bounded response file only if requested.
- Classify each issue as verified, inference, or unresolved.
- End with one recommendation: reject the target, retain it only for a minimal identifiability pilot, or proceed to a later search-design review. Do not claim architecture or primitive novelty.