import json,unittest
from common import ROOT,Meter,append

if __name__=='__main__':
    c=json.loads((ROOT/'config.json').read_text()); meter=Meter(c,'unit_validation'); status='ERROR'
    try:
        r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT),pattern='test_*.py'))
        result={'passed':r.wasSuccessful(),'tests':r.testsRun,'skips':len(r.skipped),'errors':len(r.errors),'failures':len(r.failures)}
        append(ROOT/'validation.jsonl',result); print(json.dumps(result)); status='PASS' if r.wasSuccessful() else 'FAIL'
        if not r.wasSuccessful(): raise SystemExit(1)
    finally: print(json.dumps(meter.finish(status)))
