"""Write the concise TEST 1/2 checkpoint from saved JSON only."""
import json, math, itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'results.json').read_text(encoding='utf-8'))
meta=json.loads((ROOT/'run_metadata.json').read_text(encoding='utf-8'))
progress=json.loads((ROOT/'progress.json').read_text(encoding='utf-8'))
prior=json.loads((ROOT.parent/'finite_n_clean_mask_scaling_20261006'/'results.json').read_text(encoding='utf-8'))
cases=list(data['cases'].values()); inherited=list(data.get('inherited_baselines',{}).values())
source=prior.get('cases',{})
for c in inherited:
    if c.get('source_case') in source:
        src=source[c['source_case']]
        for f in ('combined_B_norm','individual_B_mean_abs','retention','max_trace_step_error_over_initial','alias_audit','checkpoints'):
            if f in src: c[f]=src[f]

def flatten(x):
    if isinstance(x,list):
        for z in x: yield from flatten(z)
    elif isinstance(x,(int,float)): yield float(x)
def aliases(c):
    # Recompute the complete requested order-2..5 audit from the selected
    # Walsh labels. This also fills order 5 for inherited baselines whose
    # original experiment only recorded orders 2..4.
    masks=c.get('walsh_masks') or c.get('alias_audit',{}).get('masks',[])
    chosen=set(masks)
    counts={}
    for p in range(2,6):
        counts[str(p)]=sum(1 for src in itertools.combinations(masks,p)
                           if (lambda x: x in chosen and x not in src)(
                               __import__('functools').reduce(lambda a,b:a^b,src,0)))
    return counts
def family_rows():
    chosen={}
    for c in cases+inherited:
        if c.get('n')!=2048 or c.get('R') not in (4,8,12,16): continue
        key=(c.get('family'),c['R'])
        old=chosen.get(key)
        # Prefer the K=32 source case for cross-family comparison.
        if old is None or (c.get('K')==32 and old.get('K')!=32): chosen[key]=c
    return sorted(chosen.values(),key=lambda c:(c['family'],c['R']))

fam=family_rows()
lines=['# TEST 1–2 Checkpoint','',
       'This checkpoint stops after TEST 2 as requested. TEST 3 and all later tests were not run. Numerical thresholds remain unchanged: complete-response cross-talk < 0.001 (0.1%).','',
       '## TEST 1 — Donor count K','',
       '| R | K | Combined donor norm | Complete cross-talk | Protected-only cross-talk | Oldest/newest retention | Max trace-step error | Source |',
       '|---:|---:|---:|---:|---:|---:|---:|---|']
krows=sorted([c for c in cases+inherited if c.get('n')==2048 and c.get('R') in (8,16) and c.get('family')=='sum_free'],key=lambda c:(c['R'],c['K']))
for c in krows:
    mm=c['metrics']; ret=c.get('retention') or mm.get('raw_retention_by_channel') or []
    oldnew=(ret[0]/max(ret[-1],1e-300)) if ret else float('nan')
    tr=max(c.get('max_trace_step_error_over_initial') or [0.])
    src='prior clean-mask experiment' if c.get('not_a_new_measurement') else 'new CUDA run'
    lines.append(f"| {c['R']} | {c['K']} | {c.get('combined_B_norm',float('nan')):.8g} | {mm['max_complete_normalized_crosstalk']:.6g} | {mm['max_protected_normalized_crosstalk']:.6g} | {oldnew:.5g} | {tr:.3g} | {src} |")
lines += ['',
  'For R=8, the new K=8,16,64 cases and inherited K=32 reference all report complete cross-talk 1.88452e-5 and protected-only cross-talk 1.88425e-5. For R=16, the new K=16,64 cases and inherited K=32 reference all report 4.39714e-5 and 4.39687e-5, respectively. The measured protected-memory quality is therefore K-insensitive over these tested values. K=128 is invalid at n=2048 because K must divide nd=64.','',
  '## TEST 2 — Mask families at n=2048','',
  '| Family | R | Labels | XOR relations (orders 2,3,4,5) | Complete cross-talk | Protected-only cross-talk | Target | Source |',
  '|---|---:|---|---|---:|---:|---|---|']
for c in fam:
    m=c['metrics']; aa=aliases(c); counts=[aa.get(str(p),'not recorded') for p in (2,3,4,5)]
    labels=c.get('walsh_masks') or c.get('alias_audit',{}).get('masks',[])
    src='prior clean-mask experiment' if c.get('not_a_new_measurement') else 'new CUDA run'
    lines.append(f"| {c['family']} | {c['R']} | `{labels}` | `{counts}` | {m['max_complete_normalized_crosstalk']:.6g} | {m['max_protected_normalized_crosstalk']:.6g} | {'PASS' if m['max_complete_normalized_crosstalk']<1e-3 else 'FAIL'} | {src} |")
lines += ['',
  '- **Clean sum-free:** R=4,8,12,16 pass the 0.1% target. R8/R12/R16 include exact inherited K=32 baselines; R4 was freshly measured.',
  '- **Legacy alias-prone:** R=8,12,16 fail the target; R=4 passes because the legacy generator still selects the power-of-two set `[1,2,4,8]`, which has no aliases at that R.',
  '- **Independent:** R=4 passes and uses the same labels as legacy R=4. R=8,12,16 are unavailable: with nd=64 there are only six Walsh-label basis directions.',
  '- Legacy failures coincide with many XOR relations. The R=8 inherited legacy set has 6 pairwise aliases; R=12 and R=16 have 30 and 60 pairwise aliases, plus higher-order relations. This supports mask-alias involvement in these finite examples, but the experiment does not isolate causation.',
  '- The clean R=16 set has 560 order-3 and 2,688 order-5 relations but still passes. Higher-order relation counts alone do not predict failure here.',
  '- Surprising matched result: at R=4, the `[1,2,4,8]` independent/legacy set has CT=2.73508e-9, roughly 2,297 times below the `[1,3,5,7]` sum-free set CT=6.28351e-6. The independent and legacy R=4 rows are the same mask set.',
  '', '## Scope and runtime','',
  f"- CUDA: {meta['gpu_name']}, {meta['cuda_runtime_version']}, PyTorch {meta['pytorch_version']}, float64; peak VRAM {meta.get('peak_allocated_vram_mib',0):.1f} MiB allocated / {meta.get('peak_reserved_vram_mib',0):.1f} MiB reserved.",
  f"- Total elapsed experiment time: {meta.get('total_runtime_seconds',0)/60:.2f} minutes.",
  '- The first n=2048 R=16 legacy attempt was stopped while incomplete to guarantee the user-requested boundary before TEST 3. It was rerun as the only unfinished TEST 2 case; no completed measurement was restarted.',
  '- No n=4096 R=16/20/24/32 case, width sweep, high-R equal-age test, or R=40/48/64 case was run.',
  '- These are finite-size diagnostics only. They do not prove a theorem, establish asymptotic capacity, or change theorem status.']
(ROOT/'CHECKPOINT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# Make the main summary a concise pointer to the precise TEST 1/2 checkpoint,
# retaining the requested run metadata and explicit non-run scope.
summary=['# R20–R32 Clean-Mask CUDA Scaling','',
 '| Test | Verdict | Main Measurement |','|---|---|---|',
 '| TEST 1: clean K sweep, R=8/16 | PASS | Complete and protected cross-talk unchanged across tested K; see CHECKPOINT.md for each K. |',
 '| TEST 2: n=2048 mask-family comparison | PASS (comparison complete) | Clean sum-free passes R=4–16; alias-prone legacy fails R=8/12/16; independent family available through R=6. |',
 '| TEST 3: n=4096 R=16/20/24/32 | NOT RUN | User directed stop immediately after TEST 2. |','',
 '## Run details','',
 f"- GPU: {meta['gpu_name']} (cuda:0); Python {meta['python_version']}; PyTorch {meta['pytorch_version']}; CUDA {meta['cuda_runtime_version']}; float64.",
 f"- Total runtime: {meta.get('total_runtime_seconds',0)/60:.2f} minutes. Peak VRAM: {meta.get('peak_allocated_vram_mib',0):.1f} MiB allocated / {meta.get('peak_reserved_vram_mib',0):.1f} MiB reserved.",
 '- CUDA was required and used. No CPU fallback, training, or optimization was used.',
 '- Full exact case matrices and provenance are in `results.json`; frozen thresholds and device details are in `run_metadata.json`; completion and pending scope are in `progress.json`.','',
 '## Simple Meaning','',
 'The number of donor controls K did not measurably change protected-memory cross-talk at R=8 or R=16 over the tested legal K values. At n=2048, clean sum-free masks passed through R=16. Legacy masks with XOR aliases failed at R=8, R=12, and R=16; the clean R=16 set had many higher-order relations and still passed, so raw higher-order counts are not sufficient to explain failure. Independent masks only support R up to 6 at this width, and at R=4 they match the legacy power-of-two masks.',
 '',
 'TEST 2 failures are mask-dependent read leakage in the alias-prone comparisons. They do not show that the stored diagonal signal was destroyed. No clean-mask failure or finite-size capacity boundary was tested, because TEST 3 and everything after it were intentionally not run.',
 '',
 'See [CHECKPOINT.md](CHECKPOINT.md) for the compact family tables and K-by-K measurements. This remains finite-size numerical evidence only; no theorem status changed.']
(ROOT/'SUMMARY.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
print('Wrote CHECKPOINT.md and concise SUMMARY.md from saved results only.')
