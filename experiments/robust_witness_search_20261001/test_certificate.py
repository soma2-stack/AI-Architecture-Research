"""Accepted machinery unit checks; not a replay of the old certificate."""
import os
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import ast,unittest,json
from types import SimpleNamespace
from pathlib import Path
import certificate_kernel as e
import cpu_jets as c
from resources import Monitor,ROOT
e.prior=SimpleNamespace(archived=c)
source=(ROOT.parents[1]/'experiments/anisotropic_robust_packing_20260930/test_engine.py').read_text(encoding='utf-8')
node=next(x for x in ast.parse(source).body if isinstance(x,ast.ClassDef))
exec('import numpy as np\nimport mpmath as mp\nfrom fractions import Fraction as Q\n'+ast.get_source_segment(source,node))
if __name__=='__main__':
    meter=Monitor('certificate machinery tests',gpu=False)
    try:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
        (ROOT/'certificate_tests.json').write_text(json.dumps({'tests':result.testsRun,'passed':result.wasSuccessful(),'failures':len(result.failures),'errors':len(result.errors)},indent=2)+'\n',encoding='utf-8')
        if not result.wasSuccessful():raise SystemExit(1)
    finally:meter.finish()
