import unittest,itertools,json
import numpy as np
import cupy as cp
import geometry as g
from resources import Monitor
class Tests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.m=g.make({'n':3,'case':'dense'});rng=np.random.default_rng(9810000)
    cls.X=rng.uniform(-.1,.1,(6,3));cls.B=np.linalg.qr(rng.normal(size=(18,5)))[0]
  def test_cpu_gpu(self):
    a=g.jets(self.m,self.X[None],self.B,True);b=g.jets(self.m,self.X[None],self.B,True,np)
    for k in a:np.testing.assert_allclose(cp.asnumpy(a[k]),b[k],rtol=2e-12,atol=1e-12)
  def test_signed_hessian(self):
    a=g.jets(self.m,self.X[None],self.B,True,np);eps=1e-5
    plus=g.jets(self.m,(self.X+(eps*self.B[:,2]).reshape(6,3))[None],self.B,False,np)
    minus=g.jets(self.m,(self.X-(eps*self.B[:,2]).reshape(6,3))[None],self.B,False,np)
    np.testing.assert_allclose((plus['J']-minus['J'])/(2*eps),a['HS'][:,:,:,2],atol=1e-8,rtol=1e-6)
  def test_legacy_derivatives(self):
    old=g.legacy.jets(self.m,self.X[None],np);a=g.jets(self.m,self.X[None],np.eye(18),False,np)
    np.testing.assert_allclose(a['h'],old[0]);np.testing.assert_allclose(a['S'],old[1]*self.m['weights'])
    np.testing.assert_allclose(a['J'],old[2][:,3:]*self.m['supported_weights'][None,:,None])
  def test_query_vertices_dominate_interior(self):
    rng=np.random.default_rng(9810001);S=rng.normal(size=(2,3,self.m['P']))
    bound=g.min_distance(self.m,cp.asarray(S))[0]
    gates=rng.uniform(1/np.cosh(.75)**2,1/np.cosh(.25)**2,(100,3))
    C=gates@self.m['R']/(np.sqrt(3)*self.m['beta'])
    direct=np.linalg.norm(C@(S[0]-S[1]),axis=1).max()
    self.assertLessEqual(direct,bound+1e-12)
  def test_section(self):
    B=g.bases(self.m,self.X,2)['svd'];r=g.section(self.m,self.X,B,np.array([[.02,.01],[-.01,.03]]))
    self.assertTrue(r['valid'].all());self.assertLess(max(r['residual']),2e-12)
  def test_no_parameter_mutation(self):
    values=list(self.m['params']);g.jets(self.m,self.X[None],self.B,True,np)
    self.assertEqual(values,self.m['params'])
  def test_distance(self):
    S=cp.asarray(np.random.default_rng(9).normal(size=(5,3,self.m['P'])))
    D=g.pair_distances(self.m,S)
    self.assertTrue(np.allclose(D,D.T));self.assertTrue(np.allclose(np.diag(D),0))
  def test_sources_unchanged(self):
    import hashlib
    for f,v in json.loads((g.ROOT/'preservation_manifest.json').read_text()).items():
      self.assertEqual(hashlib.sha256((g.REPO/f).read_bytes()).hexdigest(),v)
if __name__=='__main__':
  meter=Monitor('development geometry tests',True)
  try:
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    (g.ROOT/'tests.json').write_text(json.dumps({'passed':result.wasSuccessful(),'tests':result.testsRun})+'\n')
    if not result.wasSuccessful():raise SystemExit(1)
  finally:meter.finish()
