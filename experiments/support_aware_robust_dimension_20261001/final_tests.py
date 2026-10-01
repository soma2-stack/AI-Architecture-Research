"""Result/legacy machinery tests without invoking old entry points or outputs."""
from resources import ROOT,Monitor
import core as k
import unittest,json,hashlib,ast,math
import numpy as np
import mpmath as mp
from fractions import Fraction as Q
from types import SimpleNamespace
e=k.e;e.prior=SimpleNamespace(archived=k.c)
src=(k.REPO/'experiments/anisotropic_robust_packing_20260930/test_engine.py').read_text()
node=next(x for x in ast.parse(src).body if isinstance(x,ast.ClassDef))
exec(ast.get_source_segment(src,node))

class Results(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.rows=json.loads((ROOT/'results.json').read_text())
 def test_sources_and_freeze(self):
  for f,h in json.loads((ROOT/'preservation_manifest.json').read_text()).items():self.assertEqual(hashlib.sha256((k.REPO/f).read_bytes()).hexdigest(),h,f)
  for f,h in json.loads((ROOT/'FROZEN_SETUP.json').read_text())['sha256'].items():self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),h,f)
 def test_all_trials_and_endpoints(self):
  self.assertEqual(len(self.rows),8);self.assertEqual(sum(x['trials_count'] for x in self.rows),1152)
  self.assertEqual({(x['case'].split('_n')[0],x['certificate']['n']) for x in self.rows},{('dense',3),('dense',4),('independent',3),('independent',4)})
 def test_finite_radius_dimension(self):
  for row in self.rows:
   d=row['dimension'];q=d['epsilon_essential_dimension'];b=list(map(Q,d['b_i']));good=d['retained_indices']
   self.assertEqual(good,[i for i,x in enumerate(b) if x>k.EPS]);self.assertEqual(q,len(good))
   m=Q(d['m_Euclidean_lower']);M=Q(d['M_Euclidean_upper']);lo=min(b[i] for i in good)
   self.assertGreater(lo,k.EPS);self.assertLessEqual(m*m*q,lo*lo);self.assertGreater(M,m)
 def test_256_verification(self):
  for row in self.rows:self.assertTrue(row['verification_256']['passed'])
 def test_strict_corner_and_entropy_counts(self):
  for row in self.rows:
   d=row['dimension'];b=[Q(d['b_i'][i]) for i in d['retained_indices']]
   for value in b:
    N=math.ceil(value/k.EPS);self.assertGreaterEqual(N,2);self.assertGreater(2*value/(N-1),2*k.EPS)
   self.assertGreaterEqual(math.prod(math.ceil(x/k.EPS) for x in b),2**len(b))
 def test_scale_diagnostic_separation(self):
  for row in json.loads((ROOT/'scale_diagnostics.json').read_text()):
   self.assertLess(row['fixed_h_projection_residual'],2e-12)
   self.assertLess(row['maximum_box_use_fraction'],1+1e-10)
   self.assertGreaterEqual(row['actual_pair_ratio_min'],row['certified_m']*(1-1e-9))
   self.assertLessEqual(row['actual_pair_ratio_max'],row['certified_M']*(1+1e-9))
 def test_frozen_model_and_cpu(self):
  self.assertEqual(k.c.hardware()['device'],'cpu')
  for case in k.INPUT['cases']:
   m=k.model(case);self.assertEqual(m.P,2*m.n*m.n+m.n if not m.diagonal else m.n*m.n+2*m.n)

if __name__=='__main__':
 meter=Monitor('CPU final results and accepted machinery tests')
 try:
  suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(Checks),unittest.defaultTestLoader.loadTestsFromTestCase(Results)])
  out=unittest.TextTestRunner(verbosity=2).run(suite)
  (ROOT/'final_tests.json').write_text(json.dumps({'passed':out.wasSuccessful(),'tests':out.testsRun,'failures':[str(x) for x in out.failures+out.errors]},indent=2)+'\n')
  if not out.wasSuccessful():raise SystemExit(1)
 finally:meter.finish()
