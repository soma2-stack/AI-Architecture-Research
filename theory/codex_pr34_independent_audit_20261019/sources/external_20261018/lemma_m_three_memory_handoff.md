# Lemma M off-cycle: three-memory timing diagnostic (provisional)

Reference: Claude PR #31, `theory/claude_lemma_m_bus_capacity_20261015/exp_offcycle_leak.py` (`soma2-stack/AI-Architecture-Research`, commit `35cdb7a...`).

## Method
- Reproduces the original state/bus recurrences but evolves only columns observed at the gather row `d-1`, an exact column reduction of the original matrices.
- Three distinct off-cycle row-pairs at `(d+10,d+11)`, `(d+20,d+21)`, `(d+30,d+31)`; each bit toggles a balanced seven-step pulse within a 25-step held interval.
- Eight combinations of three binary bits. At `n=256` and `n=512`, hold `H=25` fixed; test offsets of `(0,0,0)`, `(0,4,8)`, `(0,8,16)` steps. The nominal window begins at the same time relative to the gathered spike in each size.
- Measurement: compute the change in readout of memory `i` caused by toggling `i` in each of the four possible contexts for the other two bits, relative to the isolated-bit change. Report maximum relative context dependence; it measures context-sensitive modulation of the *bit's own* signal, not a memory-loss rate.
- Independent additive interaction error also computed as maximum relative difference between observed three-bit readouts and sum of isolated-bit effects.

## Results
| n | pulse offsets (steps) | max context dependence | max additive-interaction error | distinct bit-pattern readouts |
|---|---|---|---|---|
|256|0,0,0|1.7660%|1.7153%|8 / 8|
|256|0,4,8|2.8271%|2.7833%|8 / 8|
|256|0,8,16|2.8747%|2.8354%|8 / 8|
|512|0,0,0|0.8469%|0.8356%|8 / 8|
|512|0,4,8|1.3535%|1.3434%|8 / 8|
|512|0,8,16|1.4387%|1.4291%|8 / 8|

## Validation and limits
- One-memory baseline n=1024, H=25: 0.616257968335228 vs Claude's original 0.616257968335227; absolute discrepancy ~1e-15.
- These are small, specially constructed deterministic histories with imposed state overwrites, not a demonstration that all histories arise from legal bounded input schedules. Claimed distinctness is numerical and should not be read as proof of robust independent capacity, scaling, all channels or full Lemma M.
- Caveat: the onset offsets shift both holding periods and pulse positions, at fixed duration. Compare differently framed experiments before attributing the effect to pulse onset *alone* independent of position in a hold.
- Follow up: cross-check bounded-input legality; vary bit amplitude; test separate centered-channel or longer-query readouts; compare across sizes with matched geometric resource accounting.

**Status:** experimental clue only, for independent critique by Claude. Theorem and Lemma M remain open beyond their restricted proved components.

Reproduce: `OPENBLAS_NUM_THREADS=1 python lemma_m_three_memory_probe.py`.
