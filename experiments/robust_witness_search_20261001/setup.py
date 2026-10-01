"""Freeze protocol, paired pools and parameter definitions before scoring."""
from pathlib import Path
import json, hashlib, ast, subprocess
from fractions import Fraction as Q
import numpy as np
from scipy.stats import qmc

ROOT=Path(__file__).parent;REPO=ROOT.parents[1]
def main():
    assert not (ROOT/'config.json').exists()
    source='a195ac8'
    paths={2:'experiments/endpoint_certificate_20260930/certificate_dense_9502100_full.json',
           3:'experiments/endpoint_width_scaling_20260930/certificate_dense_n3_9602100_full.json',
           4:'experiments/endpoint_width_scaling_20260930/certificate_dense_n4_9602100_full.json'}
    manifest=[];models={};baselines={}
    for n,path in paths.items():
        raw=subprocess.check_output(['git','show',source+':'+path],cwd=REPO);data=json.loads(raw)
        models[str(n)]=data['params'];baselines[str(n)]=data['X']
        manifest.append({'path':path,'sha256':hashlib.sha256(raw).hexdigest()})
    for name in ('replay_interval.py','replay_jets.py','reviewed_kernel.py'):
        path=REPO/'experiments/anisotropic_robust_packing_replay_20261001'/name
        raw=path.read_bytes();manifest.append({'path':str(path.relative_to(REPO)),'sha256':hashlib.sha256(raw).hexdigest()})
        if name=='replay_interval.py':(ROOT/'interval.py').write_bytes(raw)
        if name=='replay_jets.py':
            text=raw.decode();text=text.replace('from replay_interval import I','from interval import I')
            (ROOT/'cpu_jets.py').write_text(text,encoding='utf-8')
        if name=='reviewed_kernel.py':
            tree=ast.parse(raw.decode());names={'uq','upadd','upmul','upsum','left','abs_array','residual','curvature','query_margins','frame_projection','certify','model_case','dyadic','mpq'}
            chunks=[ast.get_source_segment(raw.decode(),x) for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in names]
            header='from fractions import Fraction as Q\nimport numpy as np\nimport mpmath as mp\nfrom interval import I,matmul,inverse\nfrom pathlib import Path\nimport json\nCFG=json.loads((Path(__file__).parent/"config.json").read_text())["certificate_config"]\ndef mpinverse(A):\n    M=mp.matrix([[mpq(x.midq() if isinstance(x,I) else x) for x in row] for row in A])**-1\n    return [[dyadic(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]\n'
            (ROOT/'certificate_kernel.py').write_text(header+'\n\n'.join(chunks)+'\n',encoding='utf-8')
    old=json.loads((REPO/'experiments/anisotropic_robust_packing_20260930/config.json').read_text())
    cfg={'stage':'ROBUST-WITNESS SEARCH / 1','source_commit':source,'widths':[2,3,4],
         'horizons':{'2':11,'3':22,'4':37},'epsilon':'1/1000','models':['dense','independent'],
         'parameter_policy':'archived dense R/W/b; independent replaces R by diag((6+3i)/20), differentiating only diagonal; W/b unchanged',
         'normalization':'same sqrt(3/32) input SD, frozen group RMS parameter scaling; q=ones/sqrt(n), beta=max(1,||R||F), existing gate frame',
         'candidate_domain':[-0.5,0.5],
         'domain_note':'same center support as archived input generator; continuous theorem domain not enlarged. Certificate history box must fit center +/-1 coordinatewise, as in prior quantitative patch.',
         'pool_size_per_width':10000,'search_size':8000,'confirmation_size':2000,
         'pool_seed':{'2':9710202,'3':9710203,'4':9710204},'split_seed':9710299,'development_seed':9710100,
         'pool_strategies':{'random':4000,'sobol':4000,'smooth_low_amplitude':2000},
         'adaptive_search':'search only: 512 Gaussian mutations from top16 stage1 parents; 8 parents x16 SPSA iterations, two probes and one updated candidate each (384 evaluations). No confirmation adaptation.',
         'mutation_scale':0.08,'spsa_probe_scale':0.015,'spsa_step':0.025,
         'stage1_objective':'sum log1p(sigma_i/(epsilon*17/8)) over strongest 8 normalized fixed-h singular directions; not sigma_min',
         'stage2_objective':'sum log1p(sigma_i*mu_i/(epsilon*17/8)), exact accepted finite-query-frame dual margins evaluated numerically on SVD axes',
         'stage2_search_shortlist':128,'stage2_confirmation_shortlist':128,
         'stage3_search_shortlist':24,'stage3_confirmation_shortlist':24,
         'primary_objective':'lexicographic (approx jointly nontrivial packing axes, approximate integer packing bits, sum observable half-ranges); full simultaneous floating-point interval-style mixed-curvature proxy, hidden section, query-aligned projections, actual query margins; numerical only',
         'prefixes':[1,2,3,4,6,8],'amplitudes':['1/16','1/8','1/4'],'profiles':['equal','sigma/sigma1'],'hidden_factors':['1','2'],
         'certification_proposal_policy':'For each history select one recipe by primary numerical score in Phase A. Freeze r,a,profile,hidden factor, rationalized B/U/L. CPU computes inverse/preconditioner once deterministically and outward rho/mu once; no recipe search/replacement after failures.',
         'selection':'per model/width: best search, second search (runner-up), best untouched confirmation; all18 preregistered for certification, regardless of preceding success/failure',
         'pool_confirmation_policy':'Complete objective and code frozen before confirmation scoring; seal SEARCH_RESULTS before opening confirmation. Identical staged screening, no joint designs from confirmation.',
         'precision':'GPU float64; CPU certificate192bits, selected valid nonzero regions verified256bits, mpmath100digits; all GPU scores NUMERICAL ONLY',
         'batch_size':128,'max_cpu_seconds':3600,'max_gpu_wall_seconds':1800,'rss_cap_bytes':4294967296,
         'device_allocation_cap_bytes':4294967296,'gpu_stop_temperature_c':86,'gpu_preferred_temperature_c':80,
         'workers':1,'blas_threads':1,'certificate_config':old,
         'classification':'Large: dense n3>=6 and n4>=8 certified axes, with confirmation same bounds. Moderate: any main width search and confirmation>=4 axes, or both improve certified bits>=2 and axes>=1 over archive. Small: some positive certified improvement below those criteria. None: completed search, all valid certificates<=archive. Numerics/certification failure: primary proxy improves but selected certificates fail. Inconclusive: missing search/paired validation/technical budget blocks decision.',
         'stop':'Stop after report. No width5, parameter training, architecture, Stage C, AMS, GAS-0 or model-server changes.'}
    (ROOT/'config.json').write_text(json.dumps(cfg,indent=2)+'\n',encoding='utf-8')
    (ROOT/'models.json').write_text(json.dumps({'dense_parameters':models,'baseline_histories':baselines,'sources':manifest},indent=2)+'\n',encoding='utf-8')
    hashes={}
    for n in cfg['widths']:
        T=cfg['horizons'][str(n)];rng=np.random.default_rng(cfg['pool_seed'][str(n)]);L=n*T
        random=rng.uniform(-.5,.5,(4000,T,n))
        sobol=qmc.Sobol(L,scramble=True,seed=cfg['pool_seed'][str(n)]+10).random_base2(12)[:4000].reshape(-1,T,n)-.5
        smooth=rng.uniform(-.5,.5,(2000,T,n));smooth=np.cumsum(smooth,axis=1)/np.sqrt(np.arange(1,T+1))[None,:,None]
        smooth=np.clip(.5*smooth,-.5,.5)
        X=np.concatenate([random,sobol,smooth]);ids=np.random.default_rng(cfg['split_seed']+n).permutation(10000)
        split=np.zeros(10000,dtype=np.int8);split[ids[8000:]]=1
        np.savez_compressed(ROOT/f'pool_n{n}.npz',X=X,confirmation=split)
        hashes[str(n)]={'pool_sha256':hashlib.sha256((ROOT/f'pool_n{n}.npz').read_bytes()).hexdigest(),
                        'history_array_sha256':hashlib.sha256(X.tobytes()).hexdigest(),'split_sha256':hashlib.sha256(split.tobytes()).hexdigest()}
    (ROOT/'pool_manifest.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
    prior_dirs=['anisotropic_robust_packing_20260930','anisotropic_robust_packing_replay_20261001']
    preserve={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for name in prior_dirs for p in (REPO/'experiments'/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    (ROOT/'preservation_manifest.json').write_text(json.dumps(preserve,indent=2)+'\n',encoding='utf-8')
    print('Frozen paired pools, models, objective and certification policy')
if __name__=='__main__':main()
