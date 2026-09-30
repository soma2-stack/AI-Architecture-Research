"""Documentation only; numerical results and frozen protocol are untouched."""
import json
from pathlib import Path

base=Path(__file__).resolve().parent
repo=base.parents[1]
result=json.loads((base/'corrected_single_thread/summary.json').read_text())
r=result['resources']
resume=f'''### Exact Online Credit Stage-B2 resume — inconclusive (2026-09-30)

- **Lens/stage:** owner-authorized CPU-only frozen exact compression audit. **STAGE B2 — INCONCLUSIVE.** Initial freeze1d34874; generic runtime correction8271f74 before corrected measurement. No architecture candidate, learning or optimizer update.
- **Corrected evidence:**160 selected compression cases, widths8/16, T32/128,5 seeds;32 tests passed. BPTT/RTRL max group relative9.139e-16; intended-exact online methods max3.007e-14; sensitivity reconstruction5.024e-15.140 matrices also match B's archived arrays. Frozen parameters/trajectories/seed data correct.
- **Known structure:**independent compact values80/288 (actual packed numbers168/592); shared-linear exact17/33. Hard single-layer snapshot storage usually full NP; depth3 known triangular blocks reduce full9792/76032 to6672/~50960–50976 snapshot numbers, not a cheap constant-P solution. Tested SVD/QR/Kronecker/owner-block/local-plus-residual formats either remain large or expensive; snapshot size alone is not online closure.
- **Why inconclusive:**corrected family sampling91/160 collections×128 inputs,51/51 tested hard families hit centered rank127 ceiling.69 missing repeats explicitly listed; final-union claims not filled from nonconforming data.60-digit selected rank1 slice agrees to1.192e-16;144/280 owner/full ranks cutoff-dependent, although SVD algorithms agree to1.231e-15. No universal compression/storage lower bound; explicit replay/history remains another exact memory/time tradeoff.
- **Correction/resources:**first complete160-case/160-family attempt initialized24-thread NumPy/SciPy BLAS despite single-thread Torch. Preserved as NONCONFORMING RUNTIME; corrected actual pools1, main160 cases repeated, family repetition stopped at UNCHANGED1000s cumulative start cutoff. Total measured CPU{r['measured_cpu_seconds']:.6f}s ({r['cpu_minutes']:.4f}min), +20s administrative estimates, charged{r['charged_cpu_seconds']:.6f}s; job wall{r['job_wall_seconds']:.3f}s; peak{r['peak_rss_bytes']:,}bytes. Shared ledger21,921.531s (~6.0893h). One worker; CPU-only Torch2.13.0+cpu, CUDA=None; no GPU/CUDA/model server/GAS-0 operation. Config/equations/thresholds/seeds unchanged.
- **Artifacts/exact next action:**experiments/exact_online_credit_stage_b2_20260930/corrected_single_thread/REPORT.md and summary.json are PRIMARY. Parent holds original attempt and RUNTIME_CORRECTION.md; all raw/spectra/hashes/archives/provenance/negative results preserved. See AR-156. **STOP. Stage B2 inconclusive; do not proceed to Stage C, training, AMS v10 or a claimed architecture.** Owner review must decide how to resolve remaining exact-structure/family ambiguity.

'''
notebook=repo/'Codex_Research.md'
text=notebook.read_text(encoding='utf-8')
assert '## AR-156' not in text
anchor='### Exact Online Credit Stage-B resume'
idx=text.index(anchor)
text=text[:idx]+resume+text[idx:]
text+='''
## AR-156 — Exact Online Credit Stage B2: compression audit (2026-09-30)

**STAGE B2 — INCONCLUSIVE.** No architecture/capability claim and no Stage C.
Complete primary report is `experiments/exact_online_credit_stage_b2_20260930/corrected_single_thread/REPORT.md`.

### Verified facts

- Initial160-case compression/160-family run completed but a final actual-DLL
  audit found24-thread NumPy/SciPy pools. The environment limit had been set
  after imports; Torch alone was1. Resource time counted all threads correctly,
  but this violated the preregistered single-thread runtime condition. Do not
  use first-attempt timing as conforming primary evidence. All outputs preserved.
- Corrected entry points set environment BEFORE numerical imports and assert
  actual both-pool thread counts1. New regression test;32 tests passed before
  corrected measurements. Repair commit8271f74; config is byte-identical to
  first freeze1d34874. No seed/model/tolerance/threshold/stop rule relaxed.
- All160 selected compression cases repeated correctly, including all five
  seeds at both widths/horizons. Maximum BPTT/RTRL group relative9.139e-16,
  absolute2.220e-16. Intended-exact online methods group relative3.007e-14,
  absolute1.887e-15; matrix reconstruction5.024e-15. Frozen parameters,
  identical trajectories, finite CPU float64; no measured numerical invalidity.
- Known controls recognized: independent80/288 derivative VALUES (packed
  index-inclusive168/592); shared-linear17/33 numerical factors. Full row
  rank does not preclude exact compact sharing. Independent n8 family eventually
  saturates at80 dimensions; shared-linear centered families saturate16/32.
- For interacting n8/n16: rank1 full capacity768/5120, best numerical snapshot
 768/4912–5120; full dense1088/8448, best1088/8448; explicit nonlinear feedback
 1152/8704, best1152/7120–7392; depth2 full4352/33792, best3336/~25472–25488;
 depth3 full9792/76032, best6672/~50960–50976. These minima include indices and
 tested tolerance truncations, not exact-algebraic optimality among all formats.
- Block/triangular sparsity remains exactly closed and beneficial. Packed depth3
 values6528/50688, index-inclusive6984/52368; so fill-in is not arbitrary density.
 Global SVD generally full-row-rank, often exceeds full storage. Block/group,
 owner-slice, shared-input Kronecker, pivoted QR and local-baseline-plus-SVD
 correction all reconstruct within gates but do not close all hard compact/cheap
 online conditions. Unfused Kronecker sums retain historical factors explicitly.
- Rank audit:144/280 slices cutoff-dependent; gesdd/gesvd/Torch spectra agree
 to1.231e-15. Selected60-digit rank1 W-owner computation agrees1.192e-16 and
 confirms real tiny directions (condition2.26e7, stable rank1.014). High precision
 on one slice is not a certification of all deep/width16 algebraic ranks.
- Corrected family repetition completed91 collections/11,648 sensitivities.
 51/51 tested hard families show centered ranks7/15/31/63/127 at8/16/32/64/128
 samples. True maximum unresolved. Width16 rank1/full cases have all five seeds;
 depth3 width16 corrected family has only seed0/T32; other width16 depth3 main
 compression checks all passed, but incomplete family repeats cannot establish
 the strong survival gate.69 missing configurations listed. Prior original
 family160 collections/20,480 sensitivities preserved with runtime caveat.
- No need for generic full B sweep, UORO, Stage C, training, AMS v10 or GAS-0.

### Interpretation and strongest ordinary alternative

The known formats TESTED do not yield a stable cheap O(P)-like online state for
the hard cases. That is weaker than excluding all exact encodings. Snapshot
compression, numerical row rank, support and family linear span cannot prove a
retained-information lower bound; nonlinear images of small states can span a
large matrix family. Input-history replay exactly reconstructs these frozen
sensitivities too, trading T*n input storage for query/recomputation cost.
At n16/depth3/T128 it uses2048 input numbers vs76032 sensitivity numbers. This
is not a horizon-independent closed causal sensitivity; don't silently discard
it from a claim about ALL memory/time representations.

### Validity defects and preservation

Development lookup notation KeyErrors (1e-8/1e-08) fixed before first freeze;
both test attempts charged. Optional prior archive lookup initially omitted
matrices/ prefix; separate post-run comparison verified140 matches, original
raw flags unchanged. Final report reserve metadata lacked job field; corrected
report generator, no measurement or threshold changed. The BLAS import-order
issue is the material runtime defect; it was explicitly corrected and replayed.
All numerical/failed/repair work counts toward same1800s hard CPU budget.
At the unchanged1000s family-start cutoff, stop rather than relax the guard.

**Recommendation: Stage B2 inconclusive.** Stop. No Stage-C recommendation until
owner review resolves the bounded compression/family ambiguity; no discovered
architecture, universal lower bound or learning advantage established.
'''
notebook.write_text(text,encoding='utf-8')
shared=repo/'SHARED_RESEARCH_MAP.md'
text=shared.read_text(encoding='utf-8')
idx=text.index('## Latest derivative audit')
entry=f'''## Latest derivative audit — Exact Online Credit Stage B2 (2026-09-30)

**STAGE B2 — INCONCLUSIVE.** Corrected primary record:
`experiments/exact_online_credit_stage_b2_20260930/corrected_single_thread/REPORT.md`.
160 selected compression cases (width8/16,T32/128,5 seeds),32 tests passed;
BPTT/RTRL relative9.139e-16, all intended-exact online groups3.007e-14.
Known independent/shared-linear controls compress; tested hard SVD/QR/block/
Kronecker/local-plus-residual forms remain large or expensive. No lower bound.
60-digit slice check agrees; SVD algorithms agree, cutoff rank intervals remain.
Family growth still sample-limited (51/51 corrected hard families reach127 with
128 centered samples);91/160 corrected collections completed,69 missing listed.
First complete attempt had24-thread BLAS pools despite1-thread Torch; preserved
as nonconforming runtime. Generic import-order repair8271f74 verified actual
both pools1; frozen config/equations/seeds/tolerances/budgets unchanged. Repetition
stopped at unchanged1000s cumulative family-start cutoff. All work measured
{r['cpu_minutes']:.4f} CPU-min, +20s administrative estimates, peak~{r['peak_rss_bytes']/1048576:.2f}MiB;
shared ledger21,921.531s. GPU/CUDA/GAS-0 untouched; no training/Stage C/AMS v10.
**STOP — Stage B2 inconclusive.** Resolve exact-structure/family uncertainty under
owner review before considering any Stage-C learning experiment. See Codex AR-156.

'''
shared.write_text(text[:idx]+entry+text[idx:],encoding='utf-8')
readme=base/'README.md'
with readme.open('a',encoding='utf-8') as f:
    f.write(f'\n## Authoritative final B2 status\n\n**{result["classification"]}**. Use corrected_single_thread/REPORT.md and summary.json.160 compression cases repeated;91/160 family repetitions before frozen1000s cumulative start cutoff.32 tests passed. Total measured{r["cpu_minutes"]:.4f} CPU-min including original/repair, peak{r["peak_rss_bytes"]:,} bytes. Original records above remain nonconforming runtime. Stop; no Stage C.\n')
print('Updated Codex AR-156/resume, shared derivative status, and B2 README only.')
