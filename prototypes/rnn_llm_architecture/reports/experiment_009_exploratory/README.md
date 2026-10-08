# Experiment 009 — Phase A exploratory evidence (pre-registration)

These files are the **exploratory** diagnostics that motivated the
preregistered Experiment 009 design. They were run locally on CPU
(PyTorch 2.14.1, one thread per process, 4-core container) *before*
`EXPERIMENT_009_PLAN.md` was committed. Most are single-seed and are
**hypothesis-generating, not confirmatory**. Nothing here was edited after
the fact; `*_console.txt` is a verbatim transcription of console output that
was not written to a file at run time.

| File(s) | Script | What it measured |
|---|---|---|
| `a_p64_17.txt`, `a_p64_29.txt`, `a_p16_17.txt`, `a_p16_43.txt` | `explore_a.py` | Original protected model, legacy task, Exp-005 schedule (200 updates at delay 64; 350 at delay 16): behaviour stratification (D1), linear probes on slow vs fast state (D2), slow-gate values by token class and update slot (D3), gradient conflict between updated- and untouched-slot query losses (D4). |
| `b_none.txt`, `b_tag.txt`, `b_route.txt`, `b_full.txt` | `explore_b.py` | Oracle write-mask factorial on the legacy task (seed 17, 300 updates). `tag` = exact closure on non-write tokens, no slot routing; `route` = slot routing at write tokens, learned gates elsewhere; `full` = both. **Oracle masks are upper-bound diagnostics only.** |
| `c_300step_console.txt`, `c_long.txt` | `explore_c.py` | Learned gate variants (hard straight-through, token shift, bias −6 init, hard-keep GRU) at 300 updates; then learning-rate (0.01) and budget (1500 updates) probes. |
| `d_*.txt` | `explore_d.py` | Length transfer, gate statistics, fast-retention and frozen-state probes after long training (legacy vs new randomized task). |
| `pilot_seed29_two_slot.json`, `pilot_seed29_two_slot_stdout.txt` | `experiment_009.py` (pre-plan revision) | One-seed (29) pilot of the runner on the randomized two-slot task, 2000 updates, 10 two-slot arms + 2 legacy-trained arms; used to set the budget. This revision lacked the state-perturbation diagnostic. |

The scripts insert an absolute repository path into `sys.path`; adjust it to
re-run. `explore_c.py` was edited between its two batches (learning-rate
argument added, 8x evaluation removed); the archived file is the second version.
