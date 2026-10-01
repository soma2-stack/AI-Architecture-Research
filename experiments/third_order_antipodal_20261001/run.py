"""Official one-candidate run; no tuning, no fallback, all failures preserved."""
import sys,time,os
CPU=time.process_time(); WALL=time.perf_counter()
sys.dont_write_bytecode=True
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
os.environ['CUDA_VISIBLE_DEVICES']='-1'
import json,hashlib,subprocess,traceback
from fractions import Fraction as Q
import numpy as np
import kernel as k
ROOT=k.ROOT; REPO=ROOT.parents[1]; k.CPU_START=CPU
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((ROOT/'FROZEN.json').read_text())
for name,h in freeze['local_sha256'].items():assert sha(ROOT/name)==h,name
for name,h in freeze['source_sha256'].items():assert sha(REPO/name)==h,name
assert not (ROOT/'result.json').exists(),'Official run already exists; do not overwrite it'
archive=k.OLD/'BYTE_EXACT_ARCHIVE.json'; original=json.loads(archive.read_text())
assert all(sha(k.OLD/name)==h for name,h in original['sha256'].items())
data=json.loads((ROOT/'candidate.json').read_text()); config=json.loads((ROOT/'config.json').read_text())
accounted=sum(json.loads((ROOT/name).read_text())['cpu_seconds'] for name in ('setup_resources.json','development_tests.json'))
k.CPU_START=CPU-accounted
record={'status':'INCOMPLETE','setup_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        'freeze_sha256':sha(ROOT/'FROZEN.json'),'candidate_sha256':sha(ROOT/'candidate.json'),
        'epsilon':config['epsilon'],'attempts':[], 'budget_cpu_seconds':1200}
try:
    record['hardware']=k.a.c.hardware()
    B=[[Q(v) for v in row] for row in data['B']]; L=[[Q(v) for v in row] for row in data['L']]
    Kh=[[Q(v) for v in row] for row in data['K_hidden']]; K=[[Q(v) for v in row] for row in data['K_selected']]
    aa=list(map(Q,data['a'])); ah=Q(data['ah'])
    for bits in (192,256):
        k.check_budget(); t=time.process_time()
        base=k.a.base_for(data['endpoint'],B,bits,JI=None)
        assert base['model'].serialize()==data['model_parameters']
        before=base['model'].serialize()
        outcome,bounds=k.certify(base,aa,ah,L,Kh,K)
        assert base['model'].serialize()==before
        assert k.a.c.psutil.Process().memory_info().rss<config['ram_limit_bytes']
        record['attempts'].append({'precision':bits,'cpu_seconds':time.process_time()-t,'certificate':outcome})
        np.savez_compressed(ROOT/f'bounds_{bits}.npz',**bounds)
        if not outcome.get('all_antipodal_faces_pass'):
            record['status']='THIRD-ORDER METHOD FAILS ON FROZEN CANDIDATE';break
        (ROOT/'result.json').write_text(json.dumps(record,indent=2))
        print(bits,'PASS','beta_min',float(Q(outcome['weakest_beta'])),flush=True)
    else:record['status']='6D RIGOROUSLY CERTIFIED — INDEPENDENT REVIEW REQUIRED'
except Exception:
    record['status']='MATHEMATICAL GAP / IMPLEMENTATION INVALID — REVIEW REQUIRED'
    record['error']=traceback.format_exc()
finally:
    record.update(cpu_seconds=time.process_time()-CPU,wall_seconds=time.perf_counter()-WALL,
                  prior_development_cpu_seconds=accounted,
                  total_measured_cpu_seconds=time.process_time()-CPU+accounted,
                  peak_working_set_bytes=k.a.c.psutil.Process().memory_info().peak_wset,
                  gpu_seconds=0,gpu_used=False,
                  original_archive_unchanged=all(sha(k.OLD/name)==h for name,h in original['sha256'].items()))
    (ROOT/'result.json').write_text(json.dumps(record,indent=2))
    print(record['status'],record['total_measured_cpu_seconds'],flush=True)
