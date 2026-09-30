# Exact Online Credit — Stage A

Separate CPU-only frozen-parameter audit. Read PREREGISTRATION.md and config.json.
Run `python test_audit.py` for development validation and `python audit.py` once
for official results, from this directory or with the full path. The official
runner refuses to overwrite raw.jsonl. No optimizer, training or GPU use.

All14 development tests passed before freezing. This standalone implementation
does not import or exercise GAS-0 or older training experiments. Those unrelated
test suites were not run. BPTT auxiliary tape counts unique saved storage;
parameter/input aliases are separate. The terminal gradient is additional P
scalars. Autograd allocator transients are represented by process RSS rather
than a claimed exact tensor-allocation census. RTRL/local explicit scratch
inventories are conservative bounds; trajectory storage is separate audit data.

Stage B/C and mechanism searches are not authorized. Final artifacts will be
raw.jsonl, status.json, provenance.json, cpu_ledger.jsonl, summary.json and REPORT.md.

## Final status

**STAGE A VALID — STRUCTURAL DIFFERENCE OBSERVED.** All60 cases passed exact
reference gates. All15 final tests passed; the added test verifies scratch-buffer
lifetime. One resource-accounting defect was corrected and the original sweep
preserved (CORRECTIONS.md). See REPORT.md, layer_metrics.csv and resources.csv.
Measured53.843750 CPU-seconds; sampled peak284.71MiB. Owner review for Stage B;
no further experiment has run.
