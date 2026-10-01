"""Reviewed machinery tests, plus isolation and independently differentiated jets."""
import ast, json, unittest, hashlib
from types import SimpleNamespace
import reviewed_kernel as e
import replay_jets as c
import replay as r

e.prior=SimpleNamespace(archived=c)
source=(r.ROOT/'frozen_sources/test_engine.py').read_text()
node=next(x for x in ast.parse(source).body if isinstance(x,ast.ClassDef) and x.name=='Checks')
exec('import numpy as np\nimport mpmath as mp\nfrom fractions import Fraction as Q\n'+ast.get_source_segment(source,node))

class CleanReplayChecks(unittest.TestCase):
    def setUp(self):e.I.precision(192)
    def test_clean_input_separation(self):
        self.assertNotIn('J_intervals',r.INPUT)
        self.assertNotIn('projected_curvature',r.INPUT)
        self.assertEqual(r.INPUT['epsilon'],'1/1000')
        self.assertEqual(hashlib.sha256((r.ROOT/'inputs.json').read_bytes()).hexdigest(),json.loads((r.ROOT/'input_manifest.json').read_text())['inputs_sha256'])
    def test_frozen_preconditioners(self):
        for key,size in (('K_hidden',3),('K_selected',2)):
            self.assertEqual(e.mpinverse([[e.I(0)]*size for _ in range(size)]),[[Q(x) for x in row] for row in r.INPUT[key]])
    def test_fresh_endpoint_jets_against_autograd(self):
        m=r.model();X=[[Q(x) for x in row] for row in r.INPUT['X'][:2]]
        before=m.serialize();F,J,_=c.jets(m,X,'float');Fa,Ja=c.autograd(m,X)
        self.assertLess(c.relative(F,Fa),1e-12);self.assertLess(c.relative(J,Ja),1e-12)
        self.assertEqual(m.serialize(),before)
    def test_all_simultaneous_mixed_entries_present(self):
        m=r.model();X=[[Q(x) for x in row] for row in r.INPUT['X'][:2]]
        base={'n':3,'model':m,'X':X,'BI':[[e.I(Q(x)) for x in row] for row in r.INPUT['B'][:6]],
              'scaleI':{g:e.I(Q(1)) for g in ('R','W','b')}}
        HH,HS=e.curvature(base,2,[Q('1/8')]*5)
        self.assertEqual(HH.shape,(3,5,5));self.assertEqual(HS.shape,(63,5,5))
        self.assertTrue(np.all(HH>0));self.assertTrue(np.all(HS>0))
    def test_normal_widths_equal(self):
        self.assertEqual(r.INPUT['normal_half_widths'],['1/8']*3)

if __name__=='__main__':
    meter=r.Meter('clean replay unit tests')
    try:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__)))
        attempt=1+len(list(r.ROOT.glob('tests_attempt*.json')))
        r.dump(f'tests_attempt{attempt}.json',{'tests':result.testsRun,'passed':result.wasSuccessful(),'failures':len(result.failures),'errors':len(result.errors)})
        if not result.wasSuccessful():raise SystemExit(1)
    finally:meter.finish()
