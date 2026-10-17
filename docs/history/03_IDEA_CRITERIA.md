# Architecture Evaluation Criteria

Use this file to evaluate ideas consistently.

Do **not** turn the criteria into fake precision. Numerical scores may be used internally if helpful, but written reasoning matters more.

## 1. Novelty

Ask:

- Is the fundamental mechanism actually different?
- Is it more than a new arrangement of existing modules?
- Does similar research already exist?
- Would an AI researcher immediately recognize it as an established concept?

High novelty alone does not make an idea good.

## 2. Usefulness

Ask:

- What important problem does this solve?
- Why would anyone use it instead of current models?
- Does it unlock something existing systems struggle with?
- Is the benefit meaningful enough to justify a new architecture?

## 3. Technical Plausibility

Ask:

- Could this actually be implemented?
- Is the information flow well defined?
- Is there a plausible training signal?
- Can gradients, local learning, search, or another learning mechanism make it improve?
- Are there obvious mathematical contradictions?

## 4. Scalability

Ask:

- What happens at 1 million parameters?
- What happens at 1 billion?
- Does compute grow reasonably?
- Does memory usage explode?
- Can training be parallelized?
- Does it require excessive communication between components?

## 5. Compute Efficiency

Consider:

- training FLOPs
- inference FLOPs
- memory bandwidth
- VRAM/RAM requirements
- sparse vs dense computation
- ability to reuse previous computation
- hardware friendliness

## 6. Data Efficiency

Ask:

- How much data is likely required?
- Can it learn from interaction?
- Can it learn from few examples?
- Does it need expensive labels?
- Can experience be reused?

## 7. Continual Learning

Ask:

- Can it learn new things after deployment?
- Does new learning destroy old knowledge?
- Can knowledge be added locally?
- Does it require complete retraining?

## 8. Memory

Ask:

- Where does knowledge live?
- How is short-term state stored?
- How is long-term knowledge stored?
- Can knowledge be updated?
- Can memory grow without making inference unbearably expensive?

## 9. Reasoning and Planning

Ask:

- Can the architecture perform multi-step computation?
- Can it revise intermediate beliefs?
- Can it represent uncertainty?
- Can it explore alternatives?
- Can it allocate more compute to hard problems?

## 10. Testability

A strong research idea must make predictions that can fail.

Ask:

- What experiment would show the idea is wrong?
- What baseline should it beat?
- What metric matters?
- Can a small prototype reveal useful evidence?

## 11. Hardware Fit

Consider whether it maps well to:

- GPUs
- CPUs
- NPUs
- distributed clusters
- neuromorphic hardware
- custom accelerators

Do not require exotic hardware unless the advantage would justify it.

## 12. Adoption Potential

Ask:

- Could developers realistically use it?
- Does it integrate with existing software?
- Is there a strong use case?
- Is it understandable enough to build upon?
- Could it become a general platform rather than a one-off experiment?

## Red Flags

Be cautious when an idea:

- depends on vague terms like "understanding" without defining computation
- claims human-like cognition without measurable mechanisms
- requires enormous scale before producing any testable result
- solves every AI problem simultaneously
- cannot explain where learning signals come from
- cannot explain what information is represented internally
- depends entirely on another LLM doing the real intelligence
- has no clear baseline comparison
- sounds new mainly because of a new name
