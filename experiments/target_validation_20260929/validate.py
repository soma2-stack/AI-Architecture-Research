import json
import unittest
from common import ROOT,Meter,hardware_check

if __name__=='__main__':
    c=json.loads((ROOT/'config_t1.json').read_text()); m=Meter(c,'automated_validation')
    try:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT),pattern='test_*.py'))
        (ROOT/'unit_validation.json').write_text(json.dumps({'passed':result.wasSuccessful(),'tests':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'hardware':hardware_check()},indent=2))
    finally: print(json.dumps(m.finish('PASS' if result.wasSuccessful() else 'FAIL')))
    if not result.wasSuccessful(): raise SystemExit(1)
