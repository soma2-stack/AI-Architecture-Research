"""Freeze hashes without reading any original generated numerical arrays."""
from pathlib import Path
import hashlib,json,subprocess,time
import mpmath,numpy,psutil
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    source=ROOT/'experiments/rebalanced_7d_section_20261001'
    proofs=[ROOT/'experiments/third_order_antipodal_20261001/PROOF.md',source/'PROOF_AFFINE.md']
    methods=['PREREGISTRATION.md','IMPLEMENTATION.md','arithmetic.py','taylor.py','replay.py','tests.py','freeze.py','frozen_candidate.json']
    libs=[Path(mpmath.__file__).parent/'ctx_iv.py']+sorted((Path(mpmath.__file__).parent/'libmp').glob('*.py'))
    result={'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'source_candidate_sha256':sha(source/'candidate.json'),
        'method_hashes':{p:sha(HERE/p) for p in methods},
        'proof_hashes':{str(p.relative_to(ROOT)):sha(p) for p in proofs},
        'original_preservation':{str(p.relative_to(ROOT)):sha(p) for p in source.glob('*') if p.is_file()},
        'library_version':{'mpmath':mpmath.__version__,'numpy':numpy.__version__},
        'arithmetic_library_hashes':{str(p):sha(p) for p in libs},
        'config':{'n':4,'P':24,'T':37,'r':7,'epsilon':'1/1000','precision_bits':[192,256],
                  'candidate_selection':'none; frozen input only','device':'cpu','workers':1,
                  'cpu_limit_seconds':2700,'relative_comparison_tolerance':1e-10,'absolute_near_zero_tolerance':1e-14},
        'prospective_status':'Development tests passed. No official replay or generated-array comparison yet.'}
    assert result['source_candidate_sha256']==result['method_hashes']['frozen_candidate.json']
    (HERE/'METHOD_FROZEN.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'candidate_sha':result['source_candidate_sha256'],'methods':len(methods),
                      'historical_files_hashed':len(result['original_preservation'])}))
if __name__=='__main__': main()
