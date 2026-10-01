import json,unittest,hashlib,math
from fractions import Fraction as Q
import numpy as np
import prepare_bounds as p
from resources import Monitor
ROOT=p.ROOT
class Results(unittest.TestCase):
  def test_raw_split(self):
    rows=json.loads((ROOT/'raw_history_diagnostic.json').read_text());self.assertEqual(len(rows),128)
    for n in [3,4]:
      pool=np.load(ROOT.parents[1]/f'experiments/robust_witness_search_20261001/pool_n{n}.npz')
      dense=[v['id'] for v in rows if v['n']==n and v['case']=='dense'];ind=[v['id'] for v in rows if v['n']==n and v['case']=='independent']
      self.assertEqual(dense,ind);self.assertFalse(np.any(pool['confirmation'][dense]))
  def test_supported_query_identity(self):
    rng=np.random.default_rng(9810003)
    for case in p.DATA['cases']:
      if case['case']!='independent':continue
      m=p.model(case);n=case['n'];S=np.zeros((n,m.P))
      for i,col in m.support:S[i,col]=rng.normal()
      R=np.diag((6+3*np.arange(n))/20);beta=max(1,np.linalg.norm(R));high=1/np.cosh(.25)**2
      C=R.T@np.full(n,high)/(np.sqrt(n)*beta)
      self.assertAlmostEqual(np.linalg.norm(S.T@C),np.sqrt(sum(C[i]**2*S[i,col]**2 for i,col in m.support)),places=12)
  def test_structured_margin_duality(self):
    rng=np.random.default_rng(9810004)
    for entry in json.loads((ROOT/'structured_margins.json').read_text()):
      case=next(v for v in p.DATA['cases'] if v['name']==entry['name']);m=p.model(case);n=case['n']
      diag=(6+3*np.arange(n))/20;beta=max(1,np.linalg.norm(diag));d=.875*diag/(np.sqrt(n)*beta)
      weights=np.array([d[i] for i,col in m.support]);L=np.array([[float(Q(v)) for v in line] for line in case['certificate']['selected_projection']])
      mu=np.array([float(Q(v)) for v in entry['mu_structured']]);samples=rng.normal(size=(100,len(m.support)))
      self.assertTrue(np.all(np.max(np.abs(samples@L.T)*mu,axis=1)<=np.linalg.norm(samples*weights,axis=1)+1e-12))
  def test_structured_integer_packing(self):
    for entry in json.loads((ROOT/'structured_margins.json').read_text()):
      case=next(v for v in p.DATA['cases'] if v['name']==entry['name'])
      rho=list(map(Q,case['certificate']['rho_i']));mu=list(map(Q,entry['mu_structured']))
      counts=[int(2*a*b//Q(17,8000))+1 for a,b in zip(rho,mu)]
      self.assertEqual(counts,entry['counts']);self.assertEqual(math.prod(counts),int(entry['states']))
      self.assertGreater(Q(17,8000),Q(2,1000))
  def test_pairwise_packings(self):
    for case in p.DATA['cases']:
      for kind in ['packing','same_product']:
        D=np.load(ROOT/f"{kind}_{case['name']}.npz")['distances']
        self.assertTrue(np.all(D[np.isfinite(D)]>.00205));self.assertTrue(np.allclose(D,D.T))
  def test_preserved_and_primary(self):
    for f,v in json.loads((ROOT/'preservation_manifest.json').read_text()).items():
      self.assertEqual(hashlib.sha256((ROOT.parents[1]/f).read_bytes()).hexdigest(),v)
    frozen=json.loads((ROOT/'PRIMARY_FROZEN.json').read_text())
    self.assertEqual(hashlib.sha256((ROOT/'summary.json').read_bytes()).hexdigest(),frozen['summary_sha256'])
if __name__=='__main__':
  meter=Monitor('CPU final result tests')
  try:
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Results))
    (ROOT/'result_tests.json').write_text(json.dumps({'passed':result.wasSuccessful(),'tests':result.testsRun})+'\n')
    if not result.wasSuccessful():raise SystemExit(1)
  finally:meter.finish()
