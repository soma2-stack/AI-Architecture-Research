# Automated mechanism search (AMS) — preregistration v2 implementation

Protocol: `../../AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` (v2).

Open choices are fixed in `IMPLEMENTATION_DECISIONS.md`, committed before any gate or run.

**Status:** Stage 0 **failed** on the v2 Task-B gradient-conflict gate (see `STAGE0_REPORT.md`). Stages 1–3 have not run.

## Layout

| Path | Contents |
|---|---|
| `ams/grammar.py` | typed grammar, s-expression parser, typechecker |
| `ams/interp.py` | vectorized safe interpreter, FLOP cost model |
| `ams/substrate.py` | MLP substrate, program learner, SGD / SGDM / AdamW / GPM, guards |
| `ams/canon.py` | canonicalizer and structural / abstract hashes |
| `ams/probes.py` | v2 probe-corpus verifier, behaviour vectors, duplicate index |
| `ams/fingerprint.py` | F1–F26, AR-141 schema fields, C1–C3 couplings, descriptors |
| `ams/families.py` | reference library R1–R24 + extras, disguises, matcher, K(P) |
| `ams/tasks.py`, `ams/runners.py`, `ams/metrics.py` | v2 tasks, runners, learning-rate selection, metrics |
| `ams/generate.py`, `ams/search.py` | random programs, mutation / crossover, collision pipeline, MAP-Elites |
| `ams/accounting.py`, `ams/manifest.py`, `ams/stats.py` | CPU ledger and cap, immutable config and manifest, statistics |
| `scripts/stage0.py` | official Stage-0 gate |
| `tests/` | Stage-0 test suite (114 tests) |
| `runs/` | machine-readable results and `cpu_ledger.json` |
| `config/behavioral_probes_v2.json` | frozen v2 probe corpus (owner-supplied) |
| `config/run_config.json` | immutable run configuration |

## Reproduce Stage 0

```
cd experiments/automated_mechanism_search
python3 -m pytest -q              # 114 tests
python3 scripts/stage0.py         # writes runs/stage0/*, exits 2 on a validity failure
```

CPU only. Requirements: numpy 2.4, scipy 1.17, pytest 9 (versions are recorded in the manifest).
