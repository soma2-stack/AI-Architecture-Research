"""Rerun previous independent checks without rewriting their historical results.
Usage: python -I .../regressions.py --pr27-root PATH_TO_PR27_CHECKOUT
Only imports independently written Codex verifier modules, never author code.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
import pathlib
import time

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent.parent

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--pr27-root',type=pathlib.Path,required=True)
    args=p.parse_args(); start=time.perf_counter()
    folder=args.pr27_root/'theory/codex_pr27_repair_verification_20261015'
    f=load(folder/'check_foundations.py','prior_foundations')
    r=load(folder/'check_repairs.py','prior_repairs')
    s=load(ROOT/'theory/codex_pr28_repair_verification_20261014/checks.py','prior_pr28')
    results={'PR27_foundations':{},'PR27_repairs':{},'PR28_repairs':{},'source_hashes':{}}
    for path in (folder/'check_foundations.py',folder/'check_repairs.py',
                 ROOT/'theory/codex_pr28_repair_verification_20261014/checks.py'):
        results['source_hashes'][str(path.name)+'_'+str(path.parent.name)]=hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    for name in ('certified_excess','certified_floor','algebra','moving_bath','chains_and_union',
                 'coupled_state_credit','compressed_legal_histories','release_paths',
                 'constants_and_unused_counterexamples','sparse_bu_linearization'):
        results['PR27_foundations'][name]=getattr(f,name)()
    results['PR27_foundations']['larger_start_excess']=f.certified_excess(Fraction(53,50))
    for name in ('own_and_bus','transport_and_contrast','conditional_front','scalar_box',
                 'horizon_and_integer_edges','fresh_source_reset'):
        results['PR27_repairs'][name]=getattr(r,name)()
    for name in ('identities','adversarial_queries','source_and_rounding','cutoff_counterexample',
                 'repaired_bounds','block_checks','release_checks'):
        results['PR28_repairs'][name]=getattr(s,name)()
    results.update({'seconds':time.perf_counter()-start,'training':False,'gpu':False,
        'source_hash_convention':'SHA-256 of UTF-8 with universal-newline LF normalization',
        'scope':'Regression of pinned independent code; historical counterexample labels are not current theorem claims. Small comparison fixture loses its premises at step 13; only steps 1-12 are admitted.'})
    (HERE/'regression_results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','seconds':results['seconds'],
                      'groups':list(results)[:3]},indent=2))
