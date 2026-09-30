"""Preserve artifacts, document the frozen verdict and sync CPU accounting."""
import csv
import hashlib
import json
import os
import statistics as st
import zipfile
from datetime import datetime,timezone
import core as c

def main():
    meter=c.Meter('artifact preservation and final documentation')
    summary=json.loads((c.ROOT/'summary.json').read_text())
    rows=[json.loads(l) for w in (8,16) for l in (c.ROOT/f'raw_width{w}.jsonl').read_text().splitlines()]
    hashes=[]
    for folder in ('matrices','family_matrices'):
        archive=c.ROOT/f'{folder}.zip'
        assert not archive.exists(),'Preserve, do not overwrite existing archive'
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:
            for file in sorted((c.ROOT/folder).glob('*.npz')):
                meter.check();relative=f'{folder}/{file.name}';z.write(file,relative)
                hashes.append({'file':relative,'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
        hashes.append({'file':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
    with (c.ROOT/'matrix_manifest.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['file','bytes','sha256']);writer.writeheader();writer.writerows(hashes)
    for width in (8,16):
        provenance=json.loads((c.ROOT/f'provenance_width{width}.json').read_text())
        for name in ('core.py','structures.py','run.py','config.json','PREREGISTRATION.md','test_audit.py'):
            assert hashlib.sha256((c.ROOT/name).read_bytes()).hexdigest()==provenance['files'][name],f'Frozen file changed: {name}'
    meter.finish()
    ledger=[json.loads(l) for l in (c.ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
    reserve={'job':'administration reserve','cpu_seconds':10.,'wall_seconds':0.,'peak_rss_bytes':0,'gpu_used':False,'measured':False,
             'note':'Conservative estimate for small unmetered inspection/Git/documentation processes, not measured numerical CPU'}
    with (c.ROOT/'cpu_ledger.jsonl').open('a') as f:f.write(json.dumps(reserve)+'\n')
    summary['resources']={'cpu_seconds':sum(r['cpu_seconds'] for r in ledger),'wall_seconds':sum(r['wall_seconds'] for r in ledger),
                          'peak_rss_bytes':max(r['peak_rss_bytes'] for r in ledger),'charged_cpu_seconds':sum(r['cpu_seconds'] for r in ledger)+10,
                          'administrative_estimate_seconds':10.,'ledger':ledger+[reserve]}
    summary['reference_RTRL_max_relative_error']=max(g['relative_error'] for r in rows for m in r['methods'] if m['method']=='RTRL' for g in m['groups'])
    summary['reference_RTRL_max_absolute_error']=max(g['maximum_absolute_error'] for r in rows for m in r['methods'] if m['method']=='RTRL' for g in m['groups'])
    summary['owner_slice_diagnostic_count']=sum(len(layer['ranks']) for r in rows for p in r['compression'] if p['name']=='kronecker_minimum_sum' for layer in p['owner_slices'])
    (c.ROOT/'summary.json').write_text(json.dumps(summary,indent=2))
    block_table='\n'.join(f"| {a['n']} | {a['interaction']} | {a['P']} | {a['packed_values']} | {a['support_fraction_mean']:.4g} |" for a in summary['axes']['block'])
    rank_table='\n'.join(f"| {a['n']} | {a['interaction']} | {a['P']} | {a['packed_values']} | {a['support_fraction_mean']:.4g} | {a['median_RTRL_total_to_inference']:.2f} |" for a in summary['axes']['lowrank'])
    depth_table='\n'.join(f"| {a['n']} | {a['family']}:{a['interaction']} | {a['depth']} | {a['full_capacity']} | {a['packed_values']} | {a['packed_all_numbers']} |" for a in summary['depth'])
    mixing='\n'.join(f"| {a['mode']} | {a['P']} | {a['packed_values']} |" for a in summary['mixing'])
    resource=summary['resources']
    report=f'''# Exact Online Credit Stage B final report

**{summary['classification']}**

## 1. Frozen execution / validity

Frozen setup99a6336, work-accounting addition2cb4209 before official measurement.
Full tested commit/hashes in provenance_width8.json and provenance_width16.json.
460 configurations:330 width8 and130 width16 (20 positive-control cases included).
Five fixed official seeds9401100–04, T32/128, depths1/2/3; no T256 or width32.
360 additional family-diagnostic derivative cases;2,920 measured method records,
two timing repeats, extra reference/diagnostic passes counted in CPU ledger.

20 development tests passed twice before freezing: data/init/seed isolation,
prefix-consistent loss data, block/rank/mix Jacobians, exact BPTT/RTRL, packed
closure, SnAp reachability, readout/feedback separation, shared-factor positive
control, online factorization, exact Kronecker sum, reconstruction metadata,
nearzero handling, immutability, CPU, support direction and byte/index accounting.
No unrelated/GAS-0 suites run. No measured-run failures or scientific repairs.

Plain RTRL vs BPTT max group relative error
{summary['reference_RTRL_max_relative_error']:.9g}, maxabs
{summary['reference_RTRL_max_absolute_error']:.9g}. Across ALL intended-exact
methods (including repeated online SVD), max relative
{summary['maximum_exact_group_relative_error']:.9g}, maxabs
{summary['maximum_exact_group_absolute_error']:.9g}; max sensitivity reconstruction
error{summary['maximum_exact_reconstruction_relative_error']:.9g}. All below1e-8.
Forward trajectories matched within1e-14; parameters/input hashes unchanged;
CPU float64, finite states/sensitivities/gradients. No optimizer/update/training.

## 2. Block recurrence

Single-layer exact significant support at1e-12; counts identical across horizons
and five seeds. Trends persist at1e-14 and1e-10. Parameter counts differ and are
reported; this is no capability/performance-matching experiment.

| n | Block k | P | Significant / packed sensitivity values | Fraction of N*P |
|---|---|---|---|---|
{block_table}

For the implemented single-layer block graph, exact closure stores k*P values.
This is an algebraic property of this representation, not a general lower bound.
Index vectors add storage; raw fields report values, index bytes and their sum.

## 3. Low-rank recurrence

| n | Mixing rank | P | Significant / packed values | Fraction of N*P | RTRL total/inference ratio |
|---|---|---|---|---|---|
{rank_table}

Rank1 already connects all states and fills support; higher ranks increase P,
NOT support fraction beyond100%. Therefore a smooth monotonic relation between
mixing rank and sensitivity complexity is NOT established. Low rank of UV^T
is not low rank of S. Diagonal D, nonlinear gains, repeated injection and sums
matter. Full S has numerical row rank N throughout every tested final case,
stable across the three numerical cutoffs. Even diagonal S has full row rank
while admitting O(P) sparse storage: matrix rank alone is not a storage bound.

## 4. Depth, triangular blocks and mixing location

| n | Family:interaction | Depth | Full N*P | Exact packed values | Values + int64 indices |
|---|---|---|---|---|---|
{depth_table}

Every lower-parameter/higher-state block is nonzero across all main seeds;
upper parameters never influence lower states. Exact support stays block
triangular, not globally arbitrary. cross_layer.csv contains each block's
size, three support counts, ranks and singular spectrum. Diagonal depth1/2/3
support reproduces80/800/2160; width16 diagonal depths1/3 are288/14688.
For rich depth3, packed storage/P including indices grows about1.93x from
width8 to16; smallest tested online exact ratio is17.077 numbers/P at width8.
No universal minimum-information or asymptotic claim follows.

| Single-layer mixing location | P | Significant state sensitivity values |
|---|---|---|
{mixing}

Readout-only fixed/trainable/nonlinear mixing leaves recurrent support compact;
head parameters have zero state sensitivity but nonzero direct terminal gradient.
Feeding that nonlinear mixing into future recurrence changes support80->1152.
The information route, not a larger output head by itself, causes this fill-in.

The same-layer-only local/block mask has100% earliest-layer gradient error in
depth2/3: it deliberately discards all cross-layer credit. It is a harsher
reachability diagnostic than Stage A's current-time spatial learning-signal
approximation; do NOT substitute these100% values for Stage A's33–70% results.
Top-layer own gradients remain exact. compact_errors.csv reports every layer.

## 5. Fill-in and horizon

Single-layer n8 (five-seed means at t1,2,4): diagonal72->80->80;
full block72->640->1088; rank1 mixing72->656->768;
rank8 mixing72->1160->1664. Support has saturated by sampled t4 in these
cases; T128 does not increase it past T32. Fill-in is an early reachability
effect, NOT indefinite horizon growth. Complete checkpoint spectra/counts
are in fill_in.csv and raw records, including deep configurations.

## 6. Exact representations and approximation controls

- **Graph-closed packed RTRL:** exact in460/460 cases. Preserves block and
  triangular sparsity; rich dependencies increase its retained values. Counts
  int64 row/column indices. Uses temporary full A/B and query reconstruction;
  therefore NOT an optimized sparse runtime implementation.
- **SnAp1:** exact160/460; maximum group relative error.846148. Sparse masks
  can already be closed for diagonal stacks because within-time spatial paths
  belong to one recurrent-core transition. Exact does not imply O(P) storage.
- **SnAp2:** exact460/460, max group relative error2.174e-14. Two-step reachability
  equals full closure in this grid. It avoids approximation error by storing
  the graph-closed dependency set; it does not avoid that set's growth.
- **Online matrix SVD factors:** exact in120 selected cases. Full S rank N
  means N*(N+P) retained factors, often larger than N*P; includes all SVD and
  temporary reconstruction/update costs, no persistent backup/history.
- **Offline minimum-rank matrix and Kronecker-sum snapshots:** reconstruct
  exactly in460/460. Fixed matrix ranks1/2/4 fail all460. One Kronecker term
  passes only20 restricted shared-linear positive controls. Offline factors
  do not establish cheap closed online updates.
- **Unfused exact online Kronecker sum:**20/20 cases pass (max relative8.410e-16).
  Keeps32 terms and2,448–2,952 values/index numbers at T32; T-history and
  factor propagation costs are explicitly counted, not advertised as compact.
- **Known shared-linear positive control:**20/20 exact, max relative4.867e-16.
  Only17/33 persistent derivative numbers at n8/16. This calibrates recognition
  of real exact factor sharing, despite full matrix rank n.
- **UORO:** omitted as preregistered; no learning/capability comparison.

Compression CSV/raw files retain all rejected approximations. Nothing is called
exact on cosine similarity alone. These tests do not exhaust all exact algebraic
representations, residual factorizations, tensor networks or recomputation schemes.

## 7. Why INCONCLUSIVE

Robust facts: support expands with k; jumps at r0->r1; recurrent feedback matters;
cross-layer blocks appear; tested exact stored representations grow at width16.
All frozen support-growth checks pass in5/5 seeds at both horizons/all cutoffs.

But3,154 of8,800 W parameter-owner slice numerical-rank estimates vary between
relative cutoffs1e-12/1e-10/1e-8. Full-S/checkpoint and layer-block ranks are
stable, so this is not reference invalidity. The preregistration expressly uses
INCONCLUSIVE when numerical-rank diagnostics are cutoff-dependent; we do not
relax that condition after results. Exact compression gates still pass because
they check reconstruction, not a loosely chosen rank label. Factor stability
and minimal-size interpretations of small singular directions remain unresolved.

Family spans have rank7 for each fixed-parameter eight-input sample set, and39
when pooling40 matrices across parameter seeds. Both HIT THEIR SAMPLE CAPS.
They give no discriminating estimate of the true family dimension. Pooled ranks
also mix parameter settings. No empirical family dimension is a formal bound.

No tested cheap exact structure closes ALL rich nonlinear/deep cases, but these
data do NOT meet the frozen standard for STRUCTURAL PARETO GAP SURVIVES.
The local mask's deliberate failure is not evidence of architecture failure.

## 8. Runtime/resource measurements

Main runtime table: runtime_scaling.csv. Examples, median inclusive RTRL ratio:
full block depth3 n8~6.93x, n16~11.18x; rank1 depth3 n8~5.23x,n16~6.31x.
Corresponding packed ratios~7.66x/13.71x and~5.99x/7.98x. Shared-linear positive
control median~1.36x. Generic grouped indexing/Jacobian construction can make
packed execution SLOWER despite lower stored values; do not equate compression
with speed. G0 derivative section is backward only; RTRL includes forward
and Jacobian work. Use inclusive total/inference ratios for clearer comparisons.

Sensitivity-contraction operation estimates count dense2*N*N*P+N*P vs grouped
sum(2*m_rows^2*m_cols+m_rows*m_cols); Jacobian construction/indexing/query/SVD
are excluded from those estimates but included in timings. This is known algebra
and empirical implementation scaling, not a Big-O inferred from two widths.

Measured CPU{resource['cpu_seconds']:.6f}s ({resource['cpu_seconds']/60:.6f} CPU-min),
well below45-minute cap; whole-process job wall{resource['wall_seconds']:.6f}s.
Additional10s conservative administrative charge, total{resource['charged_cpu_seconds']:.6f}s.
Sampled peak RSS{resource['peak_rss_bytes']:,} bytes
({resource['peak_rss_bytes']/1048576:.2f}MiB). CPU includes imports; wall uses
process creation time; RSS sampling starts after imports. One worker/thread,
CPU-only PyTorch2.13.0+cpu, CUDA build=None, CUDA_VISIBLE_DEVICES=-1.
No GPU/CUDA, Ollama, llama.cpp, local LLM/model-server or GAS-0 operation.

Saved BPTT tape unique storage/aliases, derivative values, index bytes, temporary
scratch bounds, terminal-query workspace, graph audit metadata and checkpoint
copies are disclosed separately. Actual allocator transient tensors are not an
exhaustive census; sampled process RAM supplies the practical measurement.
Numerical diagnostics retain reference matrices in the audit harness; they are
not silently claimed as compact online-method state.

## 9. Artifacts and hard stop

config.json/PREREGISTRATION.md; core.py/structures.py/run.py/test_audit.py;
analyze.py/finalize.py; provenance_width*.json; raw_width*.jsonl; family.jsonl;
status*.json; summary.json; CPU ledger; seven diagnostic CSVs.
matrices.zip holds460 final S/parameter/input/q/y snapshots; family_matrices.zip
holds45 fixed-parameter input-family collections. matrix_manifest.csv hashes
every NPZ and both archives. Files remain locally available; archives preserve
them for Git without hundreds of loose binaries. Stage A is unchanged.

**Recommendation: Stage B inconclusive.** Owner review should resolve the
rank/compression diagnostic limits BEFORE considering a Stage-C learning study.
No Stage C authorization inferred. No training, learning advantage test, AMS v10,
new architecture or universal lower bound. Stop after this report.
'''
    (c.ROOT/'REPORT.md').write_text(report,encoding='utf-8')
    # Idempotent, optimistic-concurrency-protected append to shared CPU history.
    repo=c.ROOT.parents[1];path=repo/'experiments/automated_mechanism_search/runs/cpu_ledger.json'
    lock=path.with_name('.exact_online_credit_stage_b.lock')
    with lock.open('x') as f:f.write(str(os.getpid()))
    try:
        original=path.read_bytes();shared=json.loads(original);seen={r.get('exact_stage_b_entry_id') for r in shared['entries']}
        for i,row in enumerate(ledger+[reserve]):
            identifier=hashlib.sha256(json.dumps([i,row],sort_keys=True).encode()).hexdigest()
            if identifier in seen:continue
            shared['entries'].append({'stage':'exact_online_credit_stage_b','cpu_seconds':row['cpu_seconds'],'wall_seconds':row['wall_seconds'],
                                      'note':row.get('note','Measured full-process CPU/wall: '+row['job']),
                                      'utc':datetime.now(timezone.utc).isoformat(),'exact_stage_b_entry_id':identifier})
        shared['total_cpu_seconds']=sum(r['cpu_seconds'] for r in shared['entries']);shared['total_cpu_hours']=shared['total_cpu_seconds']/3600
        assert shared['total_cpu_hours']<shared['cap_cpu_hours'] and path.read_bytes()==original
        temp=path.with_name('exact_stage_b_ledger.tmp')
        with temp.open('x') as f:json.dump(shared,f,indent=1)
        os.replace(temp,path)
    finally:lock.unlink()
    print(json.dumps({'classification':summary['classification'],'resources':resource,'shared_cpu_seconds':shared['total_cpu_seconds']},indent=2))

if __name__=='__main__':main()
