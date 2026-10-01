"""Read-only hostile review replay; original files are never written.

Reuses the accepted interval/curvature engine. This is fresh execution,
not an independently implemented interval arithmetic library.
"""
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import sys
sys.dont_write_bytecode = True
import json, hashlib, time
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import psutil

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / 'antipodal_robust_dimension_20261001'
sys.path.insert(0, str(SRC))
import antipodal_kernel as k

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(): return {str(p.relative_to(SRC)): digest(p) for p in SRC.rglob('*') if p.is_file()}
start = time.perf_counter(); cpu = time.process_time()
before = snapshot()
checks = {}
frozen = json.loads((SRC/'FROZEN.json').read_text())
checks['frozen_hashes'] = all(digest(SRC/p) == h for p,h in frozen['sha256'].items())
repair = json.loads((SRC/'REPAIR_FROZEN.json').read_text())
checks['repair_hashes'] = all(digest(SRC/p) == h for p,h in repair['sha256'].items())
checks['original_freeze_hash'] = digest(SRC/'FROZEN.json') == repair['original_FROZEN_sha256']
assert all(checks.values())
rows = [json.loads(p.read_text()) for p in (SRC/'results').glob('*.json')]
checks['67_results'] = len(rows) == 67
checks['19_passes'] = sum(bool(x.get('certified_dimension')) for x in rows) == 19
checks['48_early_failures'] = sum(x.get('result_192',{}).get('reason') == 'hidden_section_box_inclusion' for x in rows) == 48
assert all(checks.values())
report = {'checks':checks,'original_input_hashes':frozen['sha256'], 'regenerations':[]}
ids = ['independent_n4_confirmation_query_r5_s1',
       'independent_n4_confirmation_frob_r5_s1',
       'dense_n4_confirmation_frob_r4_s2', 'dense_n3_archived_query_r3_s2']
for cid in ids:
    old = json.loads((SRC/f'results/{cid}.json').read_text())
    cand = old['candidate']; n=cand['name']; r=cand['r']
    case = next(x for x in k.INPUT['cases'] if x['name']==n)
    chart=json.loads((SRC/f"charts/{cand['chart']}.json").read_text())
    B=[[Q(x) for x in row[:case['n']+r]] for row in chart['B']]
    L=[[Q(x) for x in row] for row in chart['L'][:r]]
    aa=list(map(Q,cand['a'])); ah=Q(cand['ah'])
    Kh=[[Q(x) for x in row] for row in old['result_192']['K_hidden']]
    K=[[Q(x) for x in row] for row in old['result_192']['K_selected']]
    for bits in (192,256):
        t=time.perf_counter()
        # JI=None is essential: regenerate interval jets from frozen model/history.
        base=k.base_for(case,B,bits,JI=None)
        cache=json.loads((SRC/f'cache/JI_{n}_{bits}.json').read_text())
        ji=base['JI']; cache_equal=all(v.lo==lo and v.hi==hi for row,rl,rh in zip(ji,cache['lo'],cache['hi']) for v,lo,hi in zip(row,rl,rh))
        out, cap=k.certify_antipodal(base,aa,ah,L,frozen=(Kh,K))
        original=old[f'result_{bits}']
        same=out==original
        saved=np.load(SRC/f'results/curvature_{cid}_{bits}.npz')
        curvature_equal=all(np.array_equal(cap[name],saved[name]) for name in ('HH','HS'))
        # Independently recompute per-face row sums and exact collision margin.
        E=out['scaled_jacobian_residual_upper']
        exact_rows=[sum(map(lambda v: Q(float(v)),row),Q(0)) for row in E]
        margin=[Q(mu)*(1-row) for mu,row in zip(out['mu_tilde_i'],exact_rows)]
        assert all(m>Q(1,1000) for m in margin)
        assert all(row<=Q(float(bound)) for row,bound in zip(exact_rows,out['row_sums_upper']))
        assert all(Q(float(v)) <= (1-Q(out['eta_hidden']))*ah for v in out['hidden_forcing_upper'])
        assert cache_equal and same and curvature_equal and out['certified_dimension']==r
        item={'id':cid,'precision_bits':bits,'endpoint_cache_identical':cache_equal,
              'all_output_fields_identical':same,'all_mixed_curvature_identical':curvature_equal,
              'exact_row_sum_lower_beta':[str(x) for x in margin],
              'minimum_beta':float(Q(out['weakest_beta'])),
              'hidden_contraction':out['eta_hidden'],'face_rows':out['row_sums_upper'],
              'seconds':time.perf_counter()-t,'certificate':out}
        report['regenerations'].append(item)
        np.savez_compressed(ROOT/f'curvature_{cid}_{bits}.npz',**cap)
        (ROOT/'replay.json').write_text(json.dumps(report,indent=2))
        print(cid,bits,'PASS',item['seconds'],flush=True)
checks['original_evidence_unchanged']=snapshot()==before
assert checks['original_evidence_unchanged']
report.update(cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-start,
              peak_working_set_bytes=psutil.Process().memory_info().peak_wset,
              gpu_used=False,implementation_independence='Shared accepted arithmetic engine; independently checked rational downstream inequalities; endpoint cache bypassed.')
(ROOT/'replay.json').write_text(json.dumps(report,indent=2))
print('COMPLETE',report['cpu_seconds'],flush=True)
