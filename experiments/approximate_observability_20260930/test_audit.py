import unittest
from fractions import Fraction as Q
import json
import numpy as np
import mpmath as mp
import audit as a

class Checks(unittest.TestCase):
    def setUp(self):
        mp.mp.dps = 100
    def test_cpu_enforcement(self):
        self.assertEqual(a.archived.hardware()['device'], 'cpu')
        self.assertIsNone(a.archived.torch.version.cuda)
    def test_operator_query_metric(self):
        S = np.array([[1.,2.,-1.], [3.,0.,4.]])
        u,s,_ = np.linalg.svd(S)
        self.assertAlmostEqual(np.linalg.norm(S.T @ u[:,0]), s[0])
        self.assertLessEqual(np.linalg.norm(S)/np.sqrt(2), s[0]+1e-14)
        self.assertLessEqual(s[0], np.linalg.norm(S)+1e-14)
    def test_collision_error_factor_two(self):
        # One shared answer can serve two exact scalar answers at distance 2eps.
        eps = Q(1,10)
        answer = Q(0)
        self.assertEqual(abs(answer-eps)+abs(answer+eps),2*eps)
    def test_patch_rational_positive(self):
        data = json.loads((a.REPO/a.CFG['dense_certificates']['2']).read_text())
        patch = a.certified_patch(data,2)
        self.assertGreater(Q(patch['fixed_h_frobenius_radius_exact']),0)
        self.assertLess(Q(patch['contraction_bound_exact']),1)
        self.assertEqual(Q(patch['fixed_h_frobenius_radius_exact'])*2,Q(patch['output_cube_radius_exact']))
    def test_nullspace_projection(self):
        J = mp.matrix([[1,2,3,4],[2,-1,0,2],[3,2,1,4],[1,4,2,0]])
        A,N,defect = a.fixed_h_matrix(J,2)
        self.assertEqual((A.rows,A.cols),(2,2))
        self.assertLess(defect,mp.mpf('1e-65'))
        self.assertLess(mp.norm(N.T*N-mp.eye(2)),mp.mpf('1e-65'))
    def test_head_jacobian(self):
        R = mp.matrix([[mp.mpf('.4'),mp.mpf('.1')],[-mp.mpf('.2'),mp.mpf('.3')]])
        W = mp.matrix([[mp.mpf('.6'),mp.mpf('.1')],[mp.mpf('.1'),mp.mpf('.7')]])
        v = mp.matrix([mp.mpf('.8'),mp.mpf('.9')])
        q = mp.matrix([1/mp.sqrt(2)]*2)
        def c(vv):
            aa = W*vv
            return R.T*mp.matrix([mp.sech(aa[i])**2*q[i] for i in range(2)])
        aa = W*v
        formula = R.T*mp.diag([-2*q[i]*mp.sech(aa[i])**2*mp.tanh(aa[i]) for i in range(2)])*W
        actual = mp.matrix([[mp.diff(lambda t:c(mp.matrix([t,v[1]]))[i],v[0]),
                             mp.diff(lambda t:c(mp.matrix([v[0],t]))[i],v[1])] for i in range(2)])
        self.assertLess(mp.norm(actual-formula),mp.mpf('1e-90'))
    def test_independent_support_and_frozen_parameters(self):
        data = json.loads((a.REPO/a.CFG['dense_certificates']['2']).read_text())
        model = a.model_at(data,2,True)
        initial = model.serialize()
        F,J,S = a.archived.jets(model,[[Q(1,4),Q(-1,4)]], 'float')
        self.assertEqual(len(model.support),model.P)
        self.assertEqual(initial,model.serialize())
        self.assertTrue(np.isfinite(J).all())
    def test_archived_jet_vs_autograd(self):
        model=a.archived.Model('dense',2)
        X=[[Q(1,4),Q(-1,4)],[Q(1,8),Q(3,8)]]
        F,J,S=a.archived.jets(model,X,'float')
        FF,JJ=a.archived.autograd(model,X)
        self.assertLess(np.max(np.abs(J-JJ)),1e-12)
        self.assertLess(np.max(np.abs(np.asarray(F)-FF)),1e-12)
    def test_global_activation_derivative_bounds(self):
        # Algebra: t=tan h, |t|<=1; tanh'''=-2(1-t^2)(1-3t^2).
        t=np.linspace(-1,1,1001)
        self.assertLessEqual(np.max(np.abs(-2*t*(1-t*t))),2)
        self.assertLessEqual(np.max(np.abs(-2*(1-t*t)*(1-3*t*t))),4)
    def test_unit_and_head_gradient_normalizations(self):
        data=json.loads((a.REPO/a.CFG['dense_certificates']['2']).read_text())
        bounds=a.head_bounds(a.model_at(data,2))
        self.assertGreater(mp.mpf(bounds['alpha_lower_formula_value']),0)
        self.assertGreater(mp.mpf(bounds['adjoint_ball_radius_formula_value']),0)
        self.assertGreaterEqual(mp.mpf(bounds['beta']),1)

if __name__=='__main__':
    meter=a.Meter('focused quantitative-observability checks')
    try:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Checks)
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        (a.ROOT/'test_results.json').write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),
            'errors':len(result.errors),'passed':result.wasSuccessful()},indent=2))
        if not result.wasSuccessful():
            raise SystemExit(1)
    finally:
        meter.finish()
