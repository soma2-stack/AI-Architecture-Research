# PR #37 — controlled staircase experiment

## Research question
Does the *actual* PR #37 staircase operator improve useful recurrent memory over a matched non-staircase operator, rather than merely amplifying one selected mathematical component?

## Source of truth
Use commit 1a8203e and the independent Step 3.7 audit at:
E:\AI-Architecture-Research-PR37-step37-audit\theory\codex_pr37_step37_audit_20261021
The original implementation is legal_class.py. The full-system consistency check is full_crosscheck.py. Read AUDIT.md before implementing anything. Do not substitute a heterogeneous-retention toy model.

## Phase 1: exact reproduction (mandatory)
Run full_crosscheck.py unmodified from its original location; record stdout, exit status, exact script hash, and Python environment. Reproduce the legal staircase cases using legal_class.py, including two- and three-stage gains where feasible. Verify the endpoint equality, legal input bounds, forcing matching, population L1 gain, legal-query component, and normalized full selected-gradient difference. Virtual n=1e12 is *not* a physically allocated 1e12-dimensional neural network.

## Phase 2: pre-registered matched control
Compare staircase and control at the same n, T, peak actual input support m, recurrent matrix R, query, physical input amplitude cap, source/forcing budget, and numerical precision. Use identical endpoints and matched normalized external forcing where the PR37 construction requires them. Control must be an admissible non-staircase schedule (e.g. one-stage or constant-bath schedule), with an explicit feasibility check. Do NOT describe controls as matched if any condition fails. Report both absolute selected-gradient signal and its amplification relative to peak forcing; also report full-gradient or retrieval metric separately.

## Phase 3: functional memory
Only after Phase 2 passes, test retrieval of held information after distractors at delays 32, 128, 512, 2048. Compare with an equally sized and equally budgeted recurrent control, with identical training/data, multiple seeds, and a held-out test set. Record accuracy, chance baseline, runtime, peak memory, sensitivity to noise, and 95% confidence intervals. If embedding the PR37 operator into the recurrent model changes the legal mathematical contract, explicitly flag that and do not call it a proof of PR37.

## Fail-fast checks
Stop on mismatched parameters, illegal inputs, unequal endpoint states, inconsistent source/forcing, missing seeds, or inconsistent accounting of m*T. Preserve negative outcomes. Never infer D=Omega(n), a robust memory section, or mT=o(n^1.5) from one-column gains.

## Resource and output rules
CPU-only by default, at most 10 CPU threads; do not occupy GPU during gaming. Save all scripts, run logs, environment details, control matching table, results.csv and a short verdict.md under this folder. Keep source repository unchanged. Every verdict must say PASS, FAIL or INCONCLUSIVE and distinguish mathematical reproduction from actual neural-memory performance.

## Current status
The previous unrelated retention simulation was deleted. The existing independent full_crosscheck.py was executed on the PC and all three cases passed, including the n=8192 staircase case. This is a consistency check, NOT a completed matched-control or neural-memory experiment. No new Phase 2/3 result is claimed.
