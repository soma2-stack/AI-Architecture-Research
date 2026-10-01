"""Prospective extraction only: no interval certificate or candidate optimization."""
import os,sys,time,json,hashlib,shutil
for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[name]='1'
os.environ['CUDA_VISIBLE_DEVICES']='-1';sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
SCREEN=HERE.parent/'independent_dimension_feasibility_20261001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def rows(a):return [[str(Q(float(v))) for v in row] for row in a]
if __name__=='__main__':
    cpu=time.process_time();wall=time.perf_counter()
    assert not (HERE/'FROZEN.json').exists()
    sys.path.insert(0,str(SCREEN));import numerics
    m=numerics.Model();source=json.loads((SCREEN/'dimension_8.json').read_text())
    selected=next(x for x in source['cases'] if x['basis']=='query_svd' and x['style']=='proxy')
    B=np.load(SCREEN/'bases.npz')['query_svd'][:,:12].copy();chart=m.chart(B)
    original=json.loads((SCREEN/'endpoint.json').read_text())
    d={'r':8,'endpoint':original['endpoint'],'model_parameters':original['model_parameters'],
       'B':rows(B),'L':rows(chart['Q']),'K_hidden':rows(np.linalg.inv(chart['Jh'][:,:4])),
       'K_selected':rows(np.eye(8)),'a':[str(Q(float(v))) for v in selected['a']],
       'ah':str(Q(float(selected['ah']))),'epsilon':'1/1000',
       'selection':{'source_commit':'c057e4e','basis':'query_svd','style':'proxy',
                    'source_case_sha256':sha(SCREEN/'dimension_8.json'),
                    'source_endpoint_sha256':sha(SCREEN/'endpoint.json'),
                    'source_bases_sha256':sha(SCREEN/'bases.npz')}}
    write('candidate.json',d)
    accepted=HERE.parent/'rebalanced_7d_section_20261001/kernel.py'
    shutil.copyfile(accepted,HERE/'reviewed_kernel.py')
    dependencies=[accepted,HERE.parent/'third_order_antipodal_20261001/PROOF.md',
       HERE.parent/'rebalanced_7d_section_20261001/PROOF_AFFINE.md',
       HERE.parent/'antipodal_robust_dimension_20261001/antipodal_kernel.py',
       HERE.parent/'robust_certificate_tightness_20261001/inputs.json']
    dependencies += [HERE.parent/'robust_witness_search_20261001'/v for v in
                     ('cpu_jets.py','interval.py','certificate_kernel.py','config.json')]
    dependencies += [SCREEN/v for v in ('numerics.py','endpoint.json','bases.npz','dimension_8.json','summary.json')]
    history={}
    for folder in ('rebalanced_7d_section_20261001','cleanroom_7d_interval_20261001','independent_dimension_feasibility_20261001'):
        for p in (HERE.parent/folder).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:history[p.relative_to(REPO).as_posix()]=sha(p)
    write('config.json',{'width':4,'horizon':37,'parameters':24,'r':8,'epsilon':'1/1000',
       'precisions':[192,256],'cpu_limit_seconds':1200,'ram_limit_bytes':2*1024**3,
       'device':'CPU','workers':1,'retry_or_fallback':False})
    write('setup_resources.json',{'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-wall,
                                 'label':'prospective candidate extraction, before certification'})
    local={p.name:sha(p) for p in HERE.iterdir() if p.is_file() and p.name!='FROZEN.json'}
    write('FROZEN.json',{'local_hashes':local,'source_hashes':{p.relative_to(REPO).as_posix():sha(p) for p in dependencies},
                       'historical_hashes':history,'candidate_sha256':sha(HERE/'candidate.json')})
    print(json.dumps({'candidate_sha256':sha(HERE/'candidate.json'),'historical_files':len(history),'selection':d['selection']},indent=2))
