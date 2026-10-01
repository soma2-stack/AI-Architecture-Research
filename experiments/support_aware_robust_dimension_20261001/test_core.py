from resources import ROOT,Monitor
import unittest,json,hashlib
import numpy as np
from fractions import Fraction as Q
import core as k
class Tests(unittest.TestCase):
 def test_independent_exact_query(self):
  m=k.model({'n':3,'case':'independent'});rng=np.random.default_rng(9910100)
  delta=rng.normal(size=len(m.support));gate=1/np.cosh(.25)**2
  R=np.diag([float(m.params[i]) for i in range(3)]);beta=max(1,np.linalg.norm(R))
  S=np.zeros((3,m.P))
  for value,(i,p) in zip(delta,m.support):S[i,p]=value
  norm=np.linalg.norm(S.T@(R.T@np.full(3,gate)/(np.sqrt(3)*beta)))
  direct=np.linalg.norm(delta*np.array([gate*R[i,i]/(np.sqrt(3)*beta) for i,p in m.support]))
  self.assertAlmostEqual(norm,direct,places=14)
 def test_independent_residual_safe_duality(self):
  k.e.I.precision(192);m=k.model({'n':4,'case':'independent'});base={'model':m,'n':4}
  rng=np.random.default_rng(9910100);L=[[Q(float(v)) for v in rng.normal(size=len(m.support))] for _ in range(3)]
  mu=k.structured_query(base,L)[0];diag=np.array([float(m.params[i]) for i,p in m.support])
  for _ in range(30):
   v=rng.normal(size=len(m.support));distance=np.linalg.norm(v*diag)*.875/(2*max(1,np.linalg.norm([float(m.params[i]) for i in range(4)])))
   self.assertLessEqual(max(float(b)*abs(np.dot(list(map(float,row)),v)) for row,b in zip(L,mu)),distance*(1+1e-14))
 def test_dense_residual_safe_duality(self):
  m=k.model({'n':3,'case':'dense'});base={'model':m,'n':3};rng=np.random.default_rng(9910100)
  L=[[Q(float(v)) for v in rng.normal(size=len(m.support))] for _ in range(2)]
  mu,C=k.structured_query(base,L);C=np.array(C,float)/(np.sqrt(3)*max(1,np.linalg.norm(np.array(m.params[:9],float))))
  for _ in range(20):
   S=rng.normal(size=(3,m.P));D=np.linalg.norm(S.T@C,axis=0).max()
   v=np.array([S[i,p] for i,p in m.support])
   self.assertLessEqual(max(float(b)*abs(np.dot(list(map(float,row)),v)) for row,b in zip(L,mu)),D*(1+1e-13))
 def test_cube_antipodes(self):
  rng=np.random.default_rng(9910100)
  for r in range(1,9):
   for _ in range(20):
    z=rng.normal(size=r);z/=np.max(abs(z));b=np.linspace(.0011,.01,r)
    self.assertGreater(np.max(b*abs(2*z)),.002)
    self.assertGreaterEqual(np.max(b*abs(z)),min(b)/np.sqrt(r)*np.linalg.norm(z)-1e-15)
 def test_epsilon_not_positive_rank(self):
  margins=[Q(1,10000),Q(1,1000),Q(11,10000)]
  self.assertEqual([i for i,v in enumerate(margins) if v>k.EPS],[2])
  self.assertFalse(any(v*Q(1,4)>k.EPS for v in margins))
 def test_neumann_scaled_inverse(self):
  E=[[Q(1,10),Q(1,20)],[Q(1,30),Q(1,5)]]
  Inv=k.e.inverse([[Q(int(i==j))-E[i][j] for j in range(2)] for i in range(2)])
  self.assertTrue(all(x>=0 for row in Inv for x in row))
  entry=k.e.matmul([[k.e.I(Q(int(i==j))-E[i][j]) for j in range(2)] for i in range(2)],[[k.e.I(x) for x in row] for row in Inv])[0][0]
  self.assertLessEqual(entry.lo,k.e.I.scale);self.assertGreaterEqual(entry.hi,k.e.I.scale)
 def test_deterministic_development_basis(self):
  rng=np.random.default_rng(9910100);case={'n':3,'case':'independent','X':[[str(Q(float(v))) for v in row] for row in rng.uniform(-.1,.1,(8,3))]}
  self.assertEqual(k.float_frame(case),k.float_frame(case))
 def test_CPU_and_normalization(self):
  out=k.c.hardware();self.assertEqual(out['device'],'cpu');self.assertEqual(out['cuda_build'],None)
  self.assertEqual(k.EPS,Q(1,1000));self.assertEqual(k.CFG['workers'],1)

if __name__=='__main__':
 meter=Monitor('CPU development tests')
 try:
  run=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
  (ROOT/'tests.json').write_text(json.dumps({'passed':run.wasSuccessful(),'tests':run.testsRun,'failures':[str(x) for x in run.failures+run.errors]},indent=2)+'\n')
  if not run.wasSuccessful():raise SystemExit(1)
 finally:meter.finish()
