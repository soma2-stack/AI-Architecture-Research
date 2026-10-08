# Experiment 003 — ignore contradictory bit distractors

**Status:** bounded, preregistered experiment implementation; empirical outcomes pending.
This is a direct response to the falsification in Experiments 001/002:
protected memory can learn a single tagged bit across *benign* filler,
but the structural role of projection/Walsh is unclear, and actual
selective two-slot memory **has not been learned**.

## Falsifiable question

Can a recurrent model learn to preserve an explicitly tagged bit when the
**same bit-token IDs** subsequently appear as irrelevant distractors?
The original benign task never reuses the value tokens as filler, so it
may not measure selective resistance to contradictory memory writes.

## Task and controls

Each sequence is:

`STORE, BIT(original), distractor_1,...,distractor_d, QUERY`

Original BIT is randomly balanced; final query contains no answer.
All distractors are independent of the original bit and are unmarked.
The valid solution is to retain the **tagged** original despite later
unmarked contradictory bits, not simply read the most recent bit.

- **Benign training:** distractors are token IDs 8 through 13, never bits.
- **Interfering training:** half of distractors are randomly chosen
  `BIT0`/`BIT1`, half are benign. Random positions avoid a fixed shortcut.
- **All-bit evaluation:** every distractor is an independent binary value.
- Every trained checkpoint (two separate regimes) is evaluated frozen at
  delays 64, 128, 256 under **all three** noise distributions.
- Models: standard, near-critical, protected, GRU, LSTM at width 32;
  protected with random orthonormal basis; protected without fast projection.
  This is seven variants × two regimes × three seeds = **42 training runs**.
- Common training: 150 AdamW updates, batch 16, LR .002, gradient clip1;
  disjoint held-out sets with 512 examples per condition/seed; no oracle
  memory masks. Same seeded examples across variants.
- Evaluate and report **all** conditions, seeds, noise fractions,
  corruption/conflict rates, parameter counts and runtimes.
- The last observed noise bit is independent of the tagged original;
  its accuracy should be approximately 50%. Validate this control.

## Evidence and resource ceiling

Run CPU-only, PyTorch 2.14.1+cpu, Python 3.12 on the PR branch.
Use `.github/workflows/rnn-exp003-cpu.yml`, which runs all architecture
unit tests before launching a **540-second** maximum experiment, plus
an **18-minute job timeout**. Source and result JSON are uploaded as
GitHub Actions artifacts. No GPU usage, model server or external dataset.
The program is deterministic for matching input seeds and aborts on NaN/
nonfinite gradient; it refuses to overwrite existing evidence. Any
budget-limited output must preserve the completed/skipped run inventory.

## Honest interpretation

- Success on interfering-bit recall would show task-specific learned
  selectivity, **not** proven two-slot memory, robust dimension, or a
  new computational primitive. Longer lengths are distribution shifts.
- Failure on interfering-bit recall after benign success would show that
  the earlier positive result does not transfer to genuine contradictory
  distractors, under this training protocol.
- If the no-projection variant matches or wins, the fast projection is
  not empirically necessary for this task at this budget. A random
  orthogonal bank matching Walsh challenges any Walsh-specific claim.
- Short, equal-LR training may disadvantage gated models. Do not claim
  absolute superiority based on 150 updates or three random seeds.

**Main theoretical target** `D=Ω(n), mT=o(n^(3/2))` remains **OPEN**
and separate from this artificial supervised benchmark.
