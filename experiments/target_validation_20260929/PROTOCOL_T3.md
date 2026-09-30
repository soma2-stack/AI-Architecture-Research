# T3 freeze — generic finite-state rule induction

Unlock only after T2 is finalized KILLED. Development seeds 9200900–02;
official seeds 9203100–09. This is a bounded transduction benchmark, not a
claim about all algorithmic reasoning. Same learner/interface across four tasks.

Tasks: prefix parity (alphabet2); least-significant-digit-first addition
(alphabet100 encoding 10*a+b, output sum digit, carry hidden; terminal00 flush);
composition of S3 permutations (alphabet6, output current permutation index);
running sum modulo5 (alphabet5). Output at every prefix. Addition word lengths
include the flush symbol. No teacher state, transition table or task-specific
architecture is supplied to learners. Teachers are used for generation/audit only.

Training: 1024 independent random words, lengths4–16 inclusive, with all prefix
outputs. Test: 128 independent words at **every** length4–64. Independent RNG
streams; no test selection of parameters or steps. Prefix supervision makes
shorter prefixes available equally to all learners. The finite input domain can
produce incidental overlap; hashes and distribution separation are recorded.
Every reachable teacher state/input transition must occur >=10 times in training.
This is local coverage, not uniqueness over every imaginable program class.

Strong known control: passive Mealy-machine inference, AALpy1.6.2 GSM-RPNI,
unchanged algorithm for all tasks, no active membership/equivalence queries,
no completion of missing transitions, no supplied state bound. Input is only
observed training prefixes/outputs. Record inferred graph, states/transitions,
numeric table bytes, actual CPU/RSS; it has zero neural parameters and a strong
finite-state inductive bias. Its learned transition table is a known recurrent
state-tracking mechanism, explicitly permitted by the owner's kill criterion.
Exact product-automaton equivalence is an **after-fit audit**, never training
feedback or model selection. Exact equivalence must hold on development examples
before official unlocking. Official divergence is a failed result, not repair.

Neural diagnostics (first official seed, not a selected best seed): GRU, LSTM,
one-layer Transformer, ALiBi relative-bias Transformer (not called faithful FIRE),
and four-pass tied Universal Transformer. Same input vocab100, embedding16,
hidden16, output10, no task-specific network changes. AdamW LR{.003,.01}, decay0,
clip5, 512 updates, batch32. Training samples the same fixed words; each batch
uses one length to avoid padding leakage. Select final training cross-entropy,
never test accuracy. No learned position parameters; sinusoidal positions for
standard/tied Transformers; ALiBi only for relative control. Context supports64.
Record parameters, persistent tensor bytes, steps, examples, operations estimate,
training/ID/test exact sequence accuracy by length, failure length and slope.
These diagnostics do not establish ten-seed neural success rates.

Development gate: all four GSM-RPNI models fit all prefixes and are exactly
equivalent to teachers; coverage passes. Unit tests cover labels, seeds, data
separation, CPU, accounting, metrics and learner information interface.
Do not infer architectural failure from an invalid positive control.

Kill: one unchanged known state-tracking learner obtains >=99% exact sequence
accuracy at64 on **all four tasks** in >=9/10 official seeds. Report every length
and seed, with exact graph audit as stronger diagnostic. Then do not spend compute
on curriculum/decay/prolonged-training/Abacus panels: a strong permitted known
control already closes this bounded residual. If it does not kill, classification
is INCOMPLETE until those additional controls and ten-seed neural fitting checks
are frozen and run. No survival or AMS v10 can follow this partial panel alone.

Global 4-CPU-hour phase cap, shared30h cap, one CPU thread,2GiB process RSS remain.
No GPU, no GAS-0. No protocol changes after official results. Package-source hashes
are stored with run provenance. Preserve every failure/negative result.

Primary known-method reference:
https://github.com/DES-Lab/AALpy/wiki/RPNI---Passive-Deterministic-Automata-Learning
