# Append-only auxiliary validation repairs

1. The pre-official optional threadpoolctl import failure and environment-cap
   fallback are preserved in DEVELOPMENT_REPAIRS.md. It ran no model measurement.
2. After official measurements, an independent nested-BPTT implementation check
   used an n8/H6 development-only random-pulse history, seed11003. This too-short
   auxiliary history failed the existing noncommutation/aperiodicity gate before
   any Jacobian was evaluated. The original script is preserved as
   development/numerical_validation_initial.py. It was changed to the frozen
   diffuse generator at the same development width/horizon/seed. The subsequent
   independent Jacobian check passed. No official history/source/result changed.

Second failure traceback:

    numerical_validation.py line17: core.histories(F,'random_pulse',11003)
    run.py line172: RuntimeError('History did not pass non-scalar/aperiodic checks')

Neither failed process had a started resource timer result. Charge a conservative
unmeasured total10 CPU-s setup/repair allowance separately from measured usage.
This is an allowance, not a measurement. No scientific threshold, model, c,
epsilon, official seed, input domain or query normalization was changed.
