"""Final prospective method/input manifest; no official numerical values."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    assert not (ROOT/'FROZEN.json').exists()
    deps=[]
    for folder,files in (
        ('antipodal_robust_dimension_20261001',['antipodal_kernel.py']),
        ('robust_witness_search_20261001',['cpu_jets.py','interval.py','certificate_kernel.py','config.json']),
        ('robust_certificate_tightness_20261001',['inputs.json']),
        ('independent_dimension_feasibility_20261001',['numerics.py','bases.npz','endpoint.json']),
        ('claude_8d_review_20261001',['REVIEW.md'])):
        deps.extend(REPO/'experiments'/folder/f for f in files)
    historical={}
    for folder in ('third_order_antipodal_8d_20261001','independent_dimension_feasibility_20261001'):
        historical.update({p.relative_to(REPO).as_posix():sha(p) for p in (REPO/'experiments'/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts})
    local={p.name:sha(p) for p in ROOT.iterdir() if p.is_file() and p.name!='FROZEN.json'}
    (ROOT/'FROZEN.json').write_text(json.dumps({'local':local,'sources':{p.relative_to(REPO).as_posix():sha(p) for p in deps},
      'history':historical,'candidate_sha256':sha(ROOT/'candidate.json'),'no_official_results_yet':True},indent=2)+'\n',encoding='utf-8')
    print('Frozen',len(local),'local files,',len(historical),'historical files')
