# GAS-0

Candidate A (Verified Project State) implementation. The governing experimental
design is `HANDOFF_Claude_GAS0_design.md` at the repository root. No novelty is
claimed. The official 105-episode matrix requires separate owner authorization.

Status: Stage 1 (harness and dev project) has passed its scoped validation:
six harness unit cases and the eight-stage dev reference check. The dev starter
has 608 nonblank Python lines in 14 files, 31 visible tests, 13 hidden tests,
four text-only/retention probes and eight stage requests. A null replay scored
0.08229 RPS; reference patch and tool-replay oracles scored 1.0 RPS. The
calibration and seven evaluation projects, model freeze and pilot are pending.
Do not run an official episode until every Section 12 validation check passes
for all projects and `frozen_config.json` is committed.
