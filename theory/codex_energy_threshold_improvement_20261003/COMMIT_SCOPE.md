# Commit scope and preservation

Base HEAD: a8c5d3407580c96c32bb370f883952d2accf1c94, branch main.

Before this task, the index was empty and tracked changes existed in
Claude_Research.md, Codex_Research.md and experiments/gas0/README.md.
Other prior research folders were also untracked. They are not staged by
this task. No historical proof/review file was edited.

This commit stages only:

- this NEW theory/codex_energy_threshold_improvement_20261003/ folder;
- the new resume block stored verbatim in RESUME_ENTRY.md.

The notebook index version is constructed from its original HEAD plus only
our resume block, leaving the pre-existing uncommitted resume additions in
the worktree. The worktree insertion itself preserves every prior byte.
No AGENTS, Claude/Grok/Perplexity record, GAS-0, CreditLab, existing experiment,
model weight, old result or historical proof is rewritten.

PROVENANCE.json records 25 input hashes. FINAL_AUDIT.json verifies equality
and the auxiliary legal-spike formula; checks_result.json preserves the
independent math checks. Failed administration/auxiliary calculations and
their repairs are retained rather than erased.

The new analytic results remain pending independent hostile review.
