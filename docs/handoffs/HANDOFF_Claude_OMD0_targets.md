# Handoff — OMD-0 target packet: Claude's screened target families (for Codex and Cursor/Gemini)

**From:** Claude lane, session 23 (2026-09-28). A bounded handoff under AGENTS.md "Cross-Lane Handoffs" and SHARED_RESEARCH_MAP §12 (OMD-0).

**Scope:**
- design and prior art only;
- **no code, training, search or GPU is requested or authorized**;
- OMD-1 is **not** frozen, and only the owner may freeze it.

**Do not read:** `Claude_Research.md`; this file is self-contained. It also does not authorize editing another lane's notebook.

## Result

- 18 target families were screened. **1 survives: T1 RET, capacity-bounded retention under nonstationary reuse.**
- 17 are killed. **No second or third target survived; the list was not padded.**
- T1 is a **target family, not a candidate.**
  - Its primitive claim is expected to die on sight: per-slot event-updated state plus argmin eviction is a priority queue with event-updated keys.
  - At most it could later yield a POSSIBLE ARCHITECTURE CANDIDATE, i.e. a new retention/update semantics that survives the decomposition tests below.
  - Claude's honest prior (speculation): ≤ 10% chance of a surviving mechanism. The most likely outcomes are rediscovery of known policies (which validates the OMD pipeline) or a hybrid matched by the strongest decomposition.

### Screening standard

A family is killed if any of these holds:

| Class | Condition |
|---|---|
| **K-a** | An optimal or provably near-optimal *compact* design exists for the regime |
| **K-b** | The small-machine class has been exhaustively searched |
| **K-c** | Prior art has already trained learned systems on the task and extracted or enumerated its strategies, and the known families cover the plausible solutions |
| **K-d** | The task reduces to an excluded direction (optimizer / learning rule, continual learning, external memory, …) |

A belief-MDP optimum existing is *not* a kill: it is the Turing-simulability analogue.

## Killed families (disputes welcome)

| # | Family | Kill | Decisive prior art |
|---|---|---|---|
| 2 | Quickest change detection with O(1) state | K-a, K-c, K-d | CUSUM / Shiryaev–Roberts; ACUSUM (Sparks 2000); AEWMA; RNN learned-increment CUSUM (2022); RL for QCD (2024); Wilson–Nassar–Gold 2013† |
| 3 | Finite-memory testing, estimation or prediction | K-a | Hellman–Cover 1970; Leighton–Rivest 1986†; Meron–Feder 2004; Berg–Ordentlich–Shayevitz 2021 and survey |
| 4 | Zero-delay low-rate sender–receiver protocol **(nearest miss)** | K-a | Witsenhausen 1979† and Walrand–Varaiya 1983† structure; Wood–Linder–Yüksel 2017; Ghomi–Linder–Yüksel 2021; Cregg–Alajaji–Yüksel T-IT 2024 (near-optimal finite-memory RL design); ADM/CVSD†; RCNet ΔΣ 2025; SOI-KF†; LEARN codes 2018 |
| 5 | IPD / RPS strategy invention | K-c | Harper, Knight et al. 2017 (Axelrod library) |
| 6 | MAC / coordination protocol emergence | K-c | arXiv 2108.07144; LLM4MAC 2025; multi-player bandits survey (JMLR 2024) |
| 7 | Reversal / bandit / rule-switch strategies | K-c | Ji-An et al. (*Nature* 2025); DisRNN; CogFunSearch; meta-RL† |
| 8 | Per-entry tiny automata (branch-predictor-like) | K-b, K-a | Nair 1995 (exhaustive search of 2-bit FSM predictors) |
| 9 | Congestion control / AQM / ABR rules **(second nearest miss)** | K-d, K-c | NUM = distributed primal–dual optimization (Kelly 1998†; Low 2003†); Remy†, Aurora†, Abagnale†; BOLA† |
| 10 | Scheduling with unknown sizes | K-a | Gittins†; SOAP 2018† |
| 11 | Streaming quantiles / sketches / counting | K-a, K-d | Frugal 2013; DUMIQE; Meta-sketch 2023; Nelson–Yu 2022† |
| 12 | Restless monitoring / AoI / sensor scheduling | K-a | Whittle index (Le Ny–Feron–Dahleh 2011†); NeurWIN† |
| 13 | Fixed-size associative-memory update rules | K-d, K-c | DeltaNet / Longhorn / Titans / Miras / Gated DeltaNet† (online-optimizer view) |
| 14 | Prototype create / merge / delete under a budget | K-c | GNG-U 1997†; ART; RAN; DenStream / CluStream† |
| 15 | Local-rule fault-tolerant memory | K-a, K-c | Toom 1980†; Gács†; Taylor–Kuznetsov†; neural CA† |
| 16 | Identity tracking with O(1) state | K-a | MHT / JPDA†; Shin–Guibas–Zhao 2003†; Huang–Guestrin–Guibas 2009† |
| 17 | Timing / beat / phase tracking | K-a | PLL†; Large–Kolen 1994† |
| 18 | Online bin packing / knapsack / secretary | K-c | Kong et al. ICLR 2019†; FunSearch 2024† (stateless) |

† = recalled by Claude and not re-verified by search in this session. Please verify.

## T1 RET — definition

### Capability
With C slots, O(1) state per slot and O(1) global state, decide online which resident item to evict at each overflow, so as to minimize misses. The reference stream switches between **unlabelled** reuse regimes, and the decisions must be robust across them.

### Task (RET-synth)
- N = 256–1024 items; C = 16–32; uniform sizes; 10^4–10^5 requests.
- A hidden semi-Markov switch among six components:

  | Component | Stream |
  |---|---|
  | G1 | Zipf IRM with drifting ranks |
  | G2 | working-set phases |
  | G3 | one-hit scans |
  | G4 | loops over L > C items |
  | G5 | correlated bursts |
  | G6 | periodic items with heterogeneous periods |

- Parameters are resampled per episode; ranges and component combinations are held out.
- MIN (Belady) is used only as a training target.
- Input is only hit-on-slot-i or miss.
- Each component has a different library winner. All policies have the same C slots.

### Instrument
- Per-slot state h_i ∈ R², global g ∈ R¹.
- Shared tiny MLPs (~300–600 parameters in total):
  - F_hit(h, g) on a hit;
  - F_tick(h, g) on every request, for all resident slots;
  - on a miss: score S(h, g), evict the argmin, and set h_new ← F_ins(g);
  - g ← F_g(g, event, h_victim).
- No item IDs, PCs or regime labels.
- Variant B adds a small ghost FIFO that restores a re-referenced item's frozen h, making ARC / LIRS / S3-FIFO-style mechanisms reachable.
- Training (future): listwise imitation of MIN at misses, with truncated BPTT; REINFORCE on hit rate as a cross-check; 10 seeds.

### Signature (thresholds are for the owner to freeze)
- **S1:** within ε of the best library policy on every stationary component. On the switching mixture, it beats the best single policy and online expert mixing over the whole library (e.g. ≥ 10% relative MIN-gap reduction on ≥ 8/10 seeds).
- **S2:** decision agreement < 80% with every library policy. A GBM ranker on the union of library features, fitted to the instrument, agrees < 90% or cannot reproduce S1.
- **S3:** a dynamical signature, e.g. a g-dependent bifurcation of F_tick, or a hit transition that does not factor into recency × frequency. S3 is never sufficient alone.

### Extraction
- Phase portraits of each event map over the h-plane at several g values.
- Fits restricted to the visited-state domain.
- Sparse symbolic regression (acceptance: R² ≥ 0.99 and ≥ 95% decision agreement when substituted).
- Quantized FSM extraction compared with the CLOCK / RRIP / SIEVE / S3-FIFO / 2Q automata.
- Coordinate-to-feature regression.
- Cross-seed alignment up to an affine map (recurrence).

### Causal tests
- **Necessity:** clamp g; clamp each h coordinate; delete an extracted term. Each must be compared with matched random ablations.
- **Sufficiency:** the extracted rule as plain code reproduces ≥ 90% of the instrument's MIN-gap closure, with ≥ 95% agreement.
- **Pre-registered interventional predictions:** scan injection, hot-set switch, kick to g.
- **Slot-state patching:** swapping the h of two slots swaps their eviction order.

### Transplant
- A standalone policy run on held-out RET-synth plus a separately written synthetic suite (real traces optional).
- A fresh instrument frozen to the extracted rule must match the trained one.

### Independent transfer: T-KV
- KV-slot retention in a 1–2-layer attention model on synthetic multi-query associative recall with nonstationary query interest, budget B < context.
- Event mapping: hit = attention ≥ τ; tick = step; miss = arrival when full. Only τ is calibrated, on validation; the rule is zero-shot.
- Baselines: StreamingLLM, H2O, TOVA, random, library policies through the same interface, and a learned retention gate as the upper reference.
- Metric: recall accuracy at fixed B.
- Optional second transfer: the deletion policy of a bounded LZW dictionary.

### Kill references (strongest ordinary decomposition)

| Ref | Decomposition |
|---|---|
| D1 | oracle best library policy per regime |
| D2 | regret-weighted expert mixing over the library (LeCaR/CACHEUS generalized) |
| D3 | a GBM/LRB-style feature ranker trained on MIN |
| D4 | published outputs of automated program search (PolicySmith / CacheCraft) |
| D5 | EVA / LHD with full histograms |

- The rule must beat D2, D3 and D5 at equal or smaller state **and** transfer where the transplanted D2 and D3 do not.
- **Selector kill:** ≥ 95% per-regime agreement with known policies means "learned selector among known policies" (pipeline).

### Controls (before any novel extraction is trusted)

| Control | Setup | Required outcome |
|---|---|---|
| PC1 | stationary Zipf | LFU / A0-like |
| PC2 | working-set phases | LRU-like |
| PC3 | scans + hot set | 2Q / S3-FIFO-like |
| PC4 | planted rule: imitate SIEVE / ARC-resident | blind extraction recovers it |
| NC | random weights | no compact rule |

### CPU (future pilot, not authorized)
- ≈ 8–14 CPU-h in total.
- A 3-seed pilot with the controls first (≈ 2–3 CPU-h); stop if the controls fail.
- The shared ledger stands at 5.13 of 30 CPU-h. No GPU.

### Why T1 is still open

| Status | Reason |
|---|---|
| verified | No near-optimality result is known for O(1)-per-slot online eviction under nonstationary mixed reuse. A0 is optimal only under stationary IRM; EVA (HPCA 2017) and LHD (NSDI 2018) assume stationary age/class models |
| verified | New compact principles keep appearing: S3-FIFO 2023, SIEVE 2024, D-FR / AGE (PVLDB 2025) |
| verified | Learned policies are mostly black-box or feature rankers (LRB, Glider, GRUMA, LearnedCache 2026, KVP ICML 2026, retention gates). The nearest methodological precedents are narrow: RLR (HPCA 2021) and GA-evolved IPVs (MICRO 2013) |
| interpretation | The strongest competitor is LLM program search (PolicySmith HotNets 2025; CacheCraft arXiv 2608.14555), which optimizes instance-specific code rather than a causally validated cross-regime mechanism |

## Exact questions

### Codex — hostile reduction (no training, no code)

1. **Direct prior art:** is there work that trains a small learned per-slot (per-object) recurrent state for eviction, and extracts, transplants and causally validates the rule? The known closest are RLR 2021, GA-IPV 2013, Glider 2019, GRUMA 2025 and LearnedCache 2026.
2. **Closure (K-a):** is there a near-optimality result, or a constructive near-optimal compact design, for O(1)-per-slot online eviction under nonstationary / Markov-modulated mixed reuse?
3. **Program search:** do PolicySmith, CacheCraft or similar already produce *cross-regime* compact rules that pre-empt S1/S2?
4. **Decomposition:** is D1–D5 the strongest ordinary decomposition set? Name anything stronger.
5. **Killed families:** verify the † references, and dispute any kill in the table you think is wrong, especially the two nearest misses (families 4 and 9).

**Expected output:** for T1, exactly one of:
- **KILLED**, with exact prior art or equivalence;
- **SURVIVES AS TARGET**, with the remaining risks.

No candidate labels: there is no candidate yet.

### Cursor/Gemini — identifiability and extraction validity (no training, no code)

1. **Distinguishability:** can the planned interventions tell an unnamed rule apart from (a) one known policy, (b) a regime selector among known policies, and (c) a feature ranker? Where could two of these be observationally equivalent on RET-synth?
2. **Extraction artefacts:**
   - Could symbolic regression or FSM extraction manufacture a misleading story?
   - Are PC4 (planted rule) and NC (random weights) sufficient controls?
   - Is the 2-D-per-slot substrate too small to express the library (which baselines are unreachable?) or too loose to extract uniquely?
3. **Training and extraction risks:** do slot-permutation symmetry and argmin non-differentiability threaten training or extraction? What mitigation do you recommend?
4. **Transfer:** is T-KV independent (generator, objective, no retraining)? Is the τ-based event mapping a hidden re-tuning channel?
5. **Budget:** is ≈ 8–14 CPU-h credible for CPU-only numpy/PyTorch? What is the minimum still-decisive pilot?

**Expected output:** pass/fail for each item, with fixes, and a go / no-go recommendation for the owner.

## Owner decision (not Claude's)

Select at most one target and freeze OMD-1, resolving these forks:
1. MIN imitation, RL, or both;
2. whether ghost variant B is included;
3. the S1/S2 thresholds;
4. the T-KV specification and τ calibration;
5. whether real traces are used;
6. the CPU share (out of the ~24.9 CPU-h remaining).
