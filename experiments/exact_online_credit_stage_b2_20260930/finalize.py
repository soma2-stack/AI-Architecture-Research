"""Final descriptive record and append-only shared CPU ledger update."""
import argparse
import hashlib
import json
import os
import statistics as stat
from datetime import datetime,timezone
import core as c
import analyze

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--corrected',action='store_true');args=parser.parse_args()
    base=c.ROOT
    if args.corrected:c.ROOT=base/'corrected_single_thread'
    meter=c.Meter('Stage-B2 final audit and documentation')
    rows=analyze.load('raw.jsonl');families=analyze.load('family.jsonl');s=json.loads((c.ROOT/'summary.json').read_text())
    precision=json.loads((c.ROOT/'precision.json').read_text())
    previous=json.loads((c.ROOT/'prior_artifact_comparison.json').read_text())
    s['reference_provenance_matches']=previous['matches']
    s['optional_archive_lookup_correction']=previous['correction']
    # This additional accounting table is a formal comparison, not an unregistered run:
    # already-validated RTRL reconstructs S from frozen theta and the stored input stream.
    replay=[{'id':r['id'],'input_history_values':r['n']*r['T'],'full_size':r['full_size'],
             'ratio_history_to_full':r['n']*r['T']/r['full_size'],'RTRL_reconstruction_seconds':r['RTRL_seconds'],
             'history_grows_with_T':True,'scope':'Derived storage/query bound; append time not measured; history explicitly retained, no closed horizon-independent state claim'} for r in rows]
    analyze.csvfile('replay_tradeoff.csv',replay)
    groups=[]
    for case in c.CFG['cases']:
        rr=[r for r in rows if r['case']==case]
        cells=[]
        for n in (8,16):
            picked=[r for r in rr if r['n']==n]
            best=[analyze.best(r) for r in picked]
            vals=[b['stored_numbers'] for b in best]
            full=picked[0]['full_size'];P=picked[0]['P']
            packed=[m for r in picked for m in r['online'] if m['method']=='packed_exact']
            fast=[m for r in picked for m in r['online'] if m['method']=='shared_exact']
            time=stat.median(m['inclusive_to_inference'] for m in (fast or packed))
            cells.append(f"{P};{full};{min(vals)}–{max(vals)};{stat.median(b['ratio_to_full'] for b in best):.3f};{time:.2f}x")
        groups.append(f"|{case}|{'|'.join(cells)}|")
    curves=[]
    for case in c.CFG['family_priority']:
        for n in (8,16):
            found=[f for f in families if f['case']==case and f['n']==n and f['T']==32]
            if not found:continue
            values=[]
            for i,count in enumerate(c.CFG['family_sample_counts']):
                v=[f['checkpoints'][i]['centered']['ranks']['1e-08'] for f in found]
                values.append(str(min(v)) if min(v)==max(v) else f'{min(v)}–{max(v)}')
            curves.append(f"|{case}|{n}|{len(found)}|{'|'.join(values)}|")
    onlinegroup={}
    for method in ('packed_exact','online_svd','online_local_residual','shared_exact','unfused_kronecker_history'):
        selected=[m for r in rows for m in r['online'] if m['method']==method]
        onlinegroup[method]={'cases':len(selected),'max_relative_reconstruction':max(m['reconstruction']['relative_error'] for m in selected),
                             'storage_over_full_min':min(m['ratio_to_full'] for m in selected),'storage_over_full_max':max(m['ratio_to_full'] for m in selected),
                             'runtime_over_inference_median':stat.median(m['inclusive_to_inference'] for m in selected),
                             'runtime_over_inference_range':[min(m['inclusive_to_inference'] for m in selected),max(m['inclusive_to_inference'] for m in selected)]}
    s['online_methods']=onlinegroup
    s['precision_matrix_error']=precision['matrix_discrepancy']
    s['source_correctness_revisions']=['Pre-official rank lookup notation fixed; first29/31, second31/31. Both runs charged.',
        'Post-run BLAS import ordering correction. Original runtime nonconforming and all artifacts preserved.32 tests passed including real BLAS pool counts. Same frozen config, thresholds/seeds, cumulative CPU and start-stop gates.']
    meter.finish()
    ledger=analyze.load('cpu_ledger.jsonl')
    if args.corrected:ledger=[json.loads(l) for l in (base/'cpu_ledger.jsonl').read_text().splitlines()]+ledger
    reserve={'cpu_seconds':10.,'wall_seconds':0.,'note':'Conservative repair/administrative estimate, not measured numerical CPU'}
    resources={'measured_cpu_seconds':sum(r['cpu_seconds'] for r in ledger),'cpu_minutes':sum(r['cpu_seconds'] for r in ledger)/60,
               'charged_cpu_seconds':sum(r['cpu_seconds'] for r in ledger)+(20. if args.corrected else 10.),'job_wall_seconds':sum(r['wall_seconds'] for r in ledger),
               'peak_rss_bytes':max(r['peak_rss_bytes'] for r in ledger),'worker_count':1,'threads':1,'GPU_CUDA_used':False,
               'original_attempt_BLAS_pool_threads':24,'corrected_attempt_BLAS_pool_threads':1,
               'wall_scope':'Sum of sequential numerical job lifetimes INCLUDING original nonconforming attempt and repair; human/tool/documentation gaps excluded',
               'RAM_scope':'RSS sampled every20ms after imports; process-wide including audit and family buffers'}
    assert resources['measured_cpu_seconds']<1800
    s['resources']=resources
    (c.ROOT/'summary.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
    report=f'''# Exact Online Credit Stage B2 — completed 2026-09-30

## Classification and recommendation

**{s['classification']}**

No tested cheap compact online format closes all hard cases. That is NOT proof
that such a format cannot exist. The larger family test still hits its sample
ceiling in {s['hard_families_at_sample_ceiling']}/{s['hard_families_tested']} hard families.
Cutoff-dependent small directions remain; finite spectra do not identify the
maximum family dimension or all possible nonlinear exact encodings.
**Recommendation: Stage B2 inconclusive. Do not proceed to Stage C.**
No training/optimizer, architecture invention, learning benchmark, AMS v10 or GAS-0 activity.

## Frozen scope and validity

Setup/source freeze {s['source_freeze']}.160 selected width8/16, T32/128,5-seed cases,
{s['family_count']} fixed-parameter family collections ×128 inputs =
{s['family_recurrences']:,} family sensitivity calculations. This is a focused8-case
compression audit, not a repeat of460-case Stage B. All{s['tests_passed']} tests passed before
this attempt (20 copied B controls +12 B2 checks). Earlier development key-format
failure preserved and corrected before freeze; no reference/numerical repair afterward.
Stage A/B files unchanged. Corrected primary results are in corrected_single_thread/;
original outputs in its parent are preserved as NONCONFORMING RUNTIME. Import
ordering allowed NumPy/SciPy to initialize24-thread BLAS before the limit. This
was fixed before the corrected run; actual both-pool thread counts1 in provenance.
All frozen scientific settings unchanged. The1000s family-start cutoff and1800s
CPU cap include previous work; missing corrected families are not silently replaced
by original data. Status.json records whether family repetition completed.
{s['reference_provenance_matches']} B2 final matrices also
match Stage-B archived theta/inputs/S elementwise; newly added n16 configurations
receive the same independent BPTT checks.
The original optional lookup expected bare NPZ names, but B's ZIP contains a
matrices/ prefix, so raw metadata incorrectly says unavailable. Post-run read-only
comparison fixes this metadata in prior_artifact_comparison.json; original raw
flags/results remain unchanged. No measured run or scientific setting rerun/changed.

Frozen parameters, deterministic CPU float64, identical forward trajectories,
all finite. BPTT/RTRL max group relative {s['reference_max_relative_error']:.3e},
absolute {s['reference_max_absolute_error']:.3e}. Intended-exact online methods
max group relative {s['online_max_group_relative_error']:.3e}, absolute
{s['online_max_group_absolute_error']:.3e}; max sensitivity reconstruction
{s['online_max_reconstruction_error']:.3e}. All inside1e-8 numerical gate.

## Storage/compression summary

Each cell below is **P; full NP; smallest passing snapshot numbers across10
seed/horizon cases; median compressed/full ratio; median inclusive online
packed/inference time** (shared control uses shared method). Ratio<1 is smaller.
Snapshot minimum is selected among preregistered known formats, not a global
optimality claim. Value AND int64 index numbers counted; eight bytes each.

|Case|Width8|Width16|
|---|---|---|
{chr(10).join(groups)}

Independent packed exact rule needs80/288 value scalars (168/592 including row/column
indices). Shared-linear needs17/33 scalar factors, no index arrays or history; full
matrices640/4608. Shared control demonstrates full row rank is compatible with
small exact state. Numerical reconstruction and terminal gradients both pass.

Block/triangular closure is a real known compression: depth3 dense stacks retain
6528/50688 sensitivity values versus9792/76032 full; actual packed indices bring
these to6984/52368. It remains much larger than P (408/1584).
Rank1 recurrence has full state dependency coverage, but coverage alone is not the
result. Generic scalar sparse storage can exceed dense storage after indices.

## Methods that worked and failed

- Packed exact block/triangular recurrence:160/160 reconstructions correct; reduces
  known structural zeros, but interacting retained state grows with width/depth.
- Shared-linear known sharing:20/20 correct with2n+1 values and cheap update.
- Online global SVD:160/160 numerical-exact; generally retains full row rank N,
  N*(N+P) factor values, with full temporary reconstruction/SVD work at each step.
- Online cheap local eligibility PLUS SVD correction:160/160 correct. Includes
  the SnAp1 baseline values/indices AND full residual factors. It restores omitted
  paths but does not make hard cases compact/cheap; full matrices are scratch,
  no retained backup/history. Peak retained storage and scratch bounds disclosed.
- Snapshot SVD, pivoted QR repeated bases, supported group/block factorizations,
  W-owner factorizations and Kronecker shared-input bases reconstruct numerically
  at each requested tolerance. They often fail to save storage. Passing a snapshot
  says nothing about cheap closed online update. Large/rejected forms retained.
- Unfused online Kronecker history:12 one-layer seed0/T32 cases correct; all32
  historical factors counted. It is horizon-growing, not a compact closed solution.
- Exact within-immediate-support slice + SVD correction is a stronger offline
  alternative to whole-matrix low rank, but no hidden baseline/history discounts.

Thus "failed" here means failed compact-storage/cheap-update criterion, not
incorrect mathematics. No format is called algebraically exact merely because a
tolerance truncation passes. Tiny discarded singular tails are approximations
that satisfy this specified numerical equivalence audit, not proven zeros.

## Rank uncertainty resolved in part, not forced away

Saved full spectra, condition numbers, stable ranks, pointwise ranks at1e-6/8/10/12/14
and reconstruction-tail ranks at1e-8/10/12. Full row ranks stable; owner slices are
often ill-conditioned. {s['cutoff_dependent_slices']}/{s['rank_slice_records']} audited
full/owner slices change numerical rank across cutoffs. LAPACK gesdd/gesvd and
Torch SVD max relative spectrum discrepancy {s['max_svd_algorithm_discrepancy']:.3e}.
This is mostly cutoff sensitivity of real small singular directions, not an
algorithmic SVD disagreement. Do not give a single mathematical rank from that.

Preselected60-digit n8 rank1/T32 seed9401100 ownerW0 recurrence agrees with float64
matrix to relative {precision['matrix_discrepancy']['relative_error']:.3e}; both
give ranks6/8/8/8/8 at listed cutoffs. Spectrum ranges.63166 to2.7948e-8,
condition~2.26e7, stable rank~1.014. High precision covers this one preselected
slice; it is not certification of all ill-conditioned width16/deep slices.
Tiny exact-rational tests show a1e-20 singular direction can have algebraic rank2
while a numerical tolerance calls it rank1. Known Kronecker/outer-product control
ranks computed symbolically. These are controls, not proofs for nonlinear cases.

There are {len(s['compact_gate_tolerance_crossings'])} cases whose smallest tested
snapshot crosses the4P compact gate between1e-8 and1e-12. Detailed counts retained;
the compact/noncompact decision is stable in this sweep. Small factor-rank changes
still do not establish an algebraic minimum among all possible representations.

## Family dimension: incremental fixed-theta evidence

Centered numerical family ranks at relative1e-8, T32, min–max across the listed
number of theta seeds. Missing cases are explicit in summary.json; no imputation.

|Case|Width|Seeds|8 samples|16|32|64|128|
|---|---|---|---|---|---|---|---|
{chr(10).join(curves)}

T128 and every cutoff/uncentered spectrum are in family_growth.csv/family.jsonl.
All128 streams independently generated; never pool across different parameter
seeds. QR reorthogonalization has explicit orthogonality/reconstruction checks.
Shared-linear saturates within known centered bound2n; this proves recognition of
true finite shared structure. A rank127 at128 centered samples is the SAMPLE CEILING,
not the actual maximum. More samples might keep growing or eventually saturate.
Family span is not a retained-information lower bound; a nonlinear function of
a few state scalars can generate a large linear span of matrices.

## Width/horizon stability and strongest ordinary escape

All five seeds and both horizons included at both widths. Packed hard-case values
stay stable once support saturates, but width-normalized numbers rise with width
and depth. Factor ranks/storage can change at tighter tolerance. No measured
asymptotic law inferred from two widths. Timings are single-run inclusive CPU
measurements; no unjustified precision or independent-repeat significance.

Another ordinary escape is replay/recomputation: frozen theta plus the input
stream reconstructs S exactly using the already-validated RTRL program. Derived
input storage T*n and measured reconstruction time in replay_tradeoff.csv; appending
cost not benchmarked. This is an explicit horizon-growing history, not a closed
compact causal sensitivity. For n16/depth3/T128,2048 input values versus76032 S
values is a large storage saving, paid by replay/query cost; T32->128 costs4x history.
This demonstrates why the result cannot rule out all exact memory/time tradeoffs.
No claim that a dense matrix must be independently retained entry-by-entry.

## Resources, artifacts and stop

Measured {resources['measured_cpu_seconds']:.6f} CPU-s = {resources['cpu_minutes']:.4f}
CPU-min INCLUDING original attempt and repair, below hard30min;
+20s combined original/repair administrative estimates charged separately.
Summed job wall {resources['job_wall_seconds']:.3f}s (excludes writing/tool gaps).
Peak sampled RSS {resources['peak_rss_bytes']:,} bytes
({resources['peak_rss_bytes']/1048576:.2f}MiB); one worker throughout, one numerical
thread in the corrected run (original BLAS pools24; total resources include it). CPU-only
Torch2.13.0+cpu, CUDA build=None, CUDA_VISIBLE_DEVICES=-1, deterministic float64.
**No GPU/CUDA, GAS-0/model-server, Ollama/llama.cpp or local LLM workload.**

config.json/PREREGISTRATION.md; core.py/structures.py copies; compression.py/run.py;
{s['tests_passed']} tests; provenance.json; raw.jsonl; precision.json; family.jsonl (all spectra and
128 per-family stream/input/S digests); summary.json; CPU ledger; six CSV tables;
manifest.csv and160-snapshot matrices.zip. Analysis family buffers count as process
RAM, not an alleged online-method state. Main reference S/audit masks/trajectories
are also auditor memory; online retained values, indices, scratch and terminal
reconstruction counted separately. RSS is sampled, not a complete allocator census.
**Stop after B2. No Stage C, learning, scale-up or AMS v10.**
'''
    (c.ROOT/'REPORT.md').write_text(report,encoding='utf-8')
    readme=(c.ROOT/'README.md').read_text() if (c.ROOT/'README.md').exists() else '# Corrected single-thread Stage-B2 results\n\nScientific config identical to first freeze; runtime fix at8271f74. See parent RUNTIME_CORRECTION.md.\n'
    if '\nCompleted:' not in readme:
        (c.ROOT/'README.md').write_text(readme+f"\nCompleted: **{s['classification']}**. See REPORT.md/summary.json. Stop; Stage C not authorized.\n",encoding='utf-8')
    path=base.parents[1]/'experiments/automated_mechanism_search/runs/cpu_ledger.json'
    lock=path.with_name('.exact_online_credit_stage_b2.lock')
    with lock.open('x') as f:f.write(str(os.getpid()))
    try:
        original=path.read_bytes();shared=json.loads(original);seen={r.get('exact_stage_b2_entry_id') for r in shared['entries']}
        for i,row in enumerate(ledger+[reserve]):
            ident=hashlib.sha256(json.dumps([i,row],sort_keys=True).encode()).hexdigest()
            if ident in seen:continue
            shared['entries'].append({'stage':'exact_online_credit_stage_b2','cpu_seconds':row['cpu_seconds'],'wall_seconds':row['wall_seconds'],
                                      'note':row.get('note','Measured whole process: '+row.get('job','administration')),
                                      'utc':datetime.now(timezone.utc).isoformat(),'exact_stage_b2_entry_id':ident})
        shared['total_cpu_seconds']=sum(r['cpu_seconds'] for r in shared['entries']);shared['total_cpu_hours']=shared['total_cpu_seconds']/3600
        assert shared['total_cpu_hours']<shared['cap_cpu_hours'] and path.read_bytes()==original
        temp=path.with_name('exact_stage_b2_ledger.tmp')
        with temp.open('x') as f:json.dump(shared,f,indent=1)
        os.replace(temp,path)
    finally:lock.unlink()
    print(json.dumps({'classification':s['classification'],'resources':resources,'shared_cpu_seconds':shared['total_cpu_seconds']},indent=2))

if __name__=='__main__':main()
