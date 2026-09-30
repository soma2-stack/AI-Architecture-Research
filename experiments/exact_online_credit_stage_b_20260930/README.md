# Exact Online Credit — Stage B

Standalone CPU/float64 frozen derivative audit. Stage A remains unchanged.
Read PREREGISTRATION.md and config.json before any execution. No Stage C,
training, model server, GPU, GAS-0 or AMS operation.

Development: `python test_audit.py`. Official phases:
`python run.py --phase width8`, then width16 only after all width8 exact gates,
then `python run.py --phase family`. Runners refuse to overwrite files.
All20 development unit tests passed before the freeze. No unrelated project
or GAS-0 tests invoked.

Persistent derivative values and index bytes are separate; report their sum as
stored numbers too. Graph masks held by the audit runner are separately counted
as audit metadata; packed methods discard their mask argument after construction
and keep only index vectors/values. Full temporary A/B and reconstruction scratch
are disclosed. Sensitivity checkpoint copies belong to the recorder, not online
method state. Saved tapes are not advertised as sparse online algorithms.

The compact positive control uses known linear shared factors. Generic diagonal
tanh recurrence does not satisfy those sharing assumptions. Offline SVD or
Kronecker snapshot factors do not alone demonstrate an exact cheap online update.
SnAp2 can be exact when two-step reachability has already saturated; it may then
store as many sensitivity values as graph-closed exact RTRL.

## Completed result

**STAGE B — INCONCLUSIVE.**460 sweep cases plus360 family-diagnostic cases;
2,920 method records,20 tests passed. Exact references/compressed intended-exact
methods passed; interaction support fill-in replicated at widths8/16. SnAp2 was
exact throughout, but stored the expanded closure.3,154/8,800 W-owner slice rank
estimates were cutoff-sensitive; family dimensions hit sampling caps. Frozen
rank-stability gate prevents a surviving-gap classification.

See REPORT.md/summary.json and seven CSVs. Matrices are preserved in matrices.zip
and family_matrices.zip with matrix_manifest.csv SHA-256 hashes; loose local
NPZ directories are ignored. Stage A/GAS-0 are unchanged. Stop: Stage B
inconclusive, no Stage C or AMS authorization inferred.
