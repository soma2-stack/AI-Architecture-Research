# Automated mechanism search (AMS) — preregistration v7 implementation

Protocol: `../../AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` (v7; v2 package, v3 Task-B gate, v4/v5 Stage-1 calibration, v6/v7 SGD-anchored Stage-2 constructor).

Open choices are fixed in `IMPLEMENTATION_DECISIONS.md`, committed before any gate or run.

**Status:** v3 Stage 0 PASS (`runs/stage0_v3/`); v5 Stage 1 PASS (`runs/stage1_v5/`). Stage 2 first run stopped on the implementation-defect rule (`runs/stage2/`); after repair 1, the official rerun (`runs/stage2_repair1/`) completed at `N_GEN_MAX` with 0 Tier-1 evaluations and 0 promoted (`STAGE2_REPORT.md` §6). **v6:** the static validation failed on C2 coupling presence, and no v6 search ran (`STAGE2_V6_REPORT.md`). **v7:** the static validation passed. The official Stage 2 (`runs/stage2_v7/`) reached `G_MAX` with 1,200 Tier-1 evaluations, 35/56 cells and 8 promotions (all C\*). Stage 3 (`runs/stage3_v7/`) labelled **all 8 NEGATIVE**: none met the preregistered fresh-seed threshold. See `STAGE2_V7_REPORT.md`. Earlier stops: `STAGE0_REPORT.md` (v2), `STAGE1_REPORT.md` (v3), `STAGE1_V4_REPORT.md` (v4).

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
| `ams/v6gen.py`, `ams/v7gen.py` | prereg v6 SGD-anchored initial constructor; v7 detector-aligned C2 |
| `ams/stage3.py`, `scripts/stage3.py` | Stage-3 matched validation (D-S3 / D-S3-v4) |
| `ams/accounting.py`, `ams/manifest.py`, `ams/stats.py` | CPU ledger and cap, immutable config and manifest, statistics |
| `scripts/stage0.py` | official Stage-0 gate |
| `scripts/stage2.py`, `scripts/v6_static_validation.py`, `scripts/v7_static_validation.py` | Stage-2 search (v5 runs; `stage2_v6` gated on the v6 static validation) and the v6 static validation |
| `tests/` | Stage-0 test suite (114 tests) |
| `runs/` | machine-readable results and `cpu_ledger.json` |
| `config/behavioral_probes_v2.json` | frozen v2 probe corpus (owner-supplied) |
| `config/run_config*.json` | immutable run configurations (v2 … v7; `run_config_v7.json` is active) |

## Reproduce Stage 0

```
cd experiments/automated_mechanism_search
python3 -m pytest -q              # 114 tests
python3 scripts/stage0.py         # writes runs/stage0/*, exits 2 on a validity failure
```

CPU only. Requirements: numpy 2.4, scipy 1.17, pytest 9 (versions are recorded in the manifest).
