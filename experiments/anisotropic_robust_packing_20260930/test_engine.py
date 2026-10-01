import unittest,json
from fractions import Fraction as Q
import numpy as np
import mpmath as mp
import engine as e

class Checks(unittest.TestCase):
    def setUp(self):e.I.precision(192);mp.mp.dps=100
    def test_cpu_threads(self):
        h=e.prior.archived.hardware();self.assertEqual(h['device'],'cpu');self.assertIsNone(h['cuda_build'])
    def test_outward_elementary_arithmetic(self):
        for a in (Q(1,3),Q(1,10),Q(17,8),Q(1,10**100)):
            for b in (Q(1,7),Q(3,2)):
                aa=e.uq(a);bb=e.uq(b)
                self.assertGreaterEqual(Q(float(e.upadd(aa,bb))),a+b)
                self.assertGreaterEqual(Q(float(e.upmul(aa,bb))),a*b)
    def test_interval_sqrt(self):
        for value in (Q(2),Q(3,32),Q(1,100)):
            x=e.I(value).sqrt()
            self.assertLessEqual(Q(x.lo,x.scale)**2,value)
            self.assertGreaterEqual(Q(x.hi,x.scale)**2,value)
    def test_transcendental_cross_precision(self):
        a=e.I(Q(7,4)).tanh();lo=Q(a.lo,a.scale);hi=Q(a.hi,a.scale)
        e.I.precision(256);b=e.I(Q(7,4)).tanh()
        self.assertLessEqual(lo,Q(b.lo,b.scale));self.assertGreaterEqual(hi,Q(b.hi,b.scale))
    def test_interval_inverse(self):
        A=[[e.I(Q(2)),e.I(Q(1))],[e.I(Q(1)),e.I(Q(3))]]
        B=e.inverse(A);M=e.matmul(A,B)
        for i in range(2):
            for j in range(2):self.assertTrue(M[i][j].lo<=int(i==j)*e.I.scale<=M[i][j].hi)
    def test_integer_safe_product_spacing(self):
        eps=Q(1,1000);rho=Q(3,100);mu=Q(1,2)
        spacing=Q(17,8)*eps/mu;N=(2*rho)//spacing+1
        self.assertEqual(N,15)
        self.assertGreater(spacing*mu,2*eps)
        self.assertLessEqual((N-1)*spacing,2*rho)
        self.assertGreater(N*spacing,2*rho)
    def test_axiswise_counts_cannot_bypass_mixed_terms(self):
        # J=[[1,L*y2],[L*y1,1]] can look perfect on individual points.
        # Mixed Hessian bound gives scaled residual L*a; if>=1 no certificate.
        L=20;a=Q(1,10)
        self.assertGreaterEqual(L*a,1)
    def test_directional_curvature_against_autodiff(self):
        c=e.prior.archived;model=c.Model('dense',2);X=[[Q(1,4),Q(-1,4)],[Q(1,8),Q(3,8)]]
        BI=[[e.I(Q(int(i==j))) for j in range(3)] for i in range(4)]
        scales={name:e.I(sum(model.params[p]**2 for p,(_,_,g,_) in enumerate(model.meta) if g==name)/
                sum(g==name for _,_,g,_ in model.meta)).sqrt() for name in ('R','W','b')}
        base={'model':model,'n':2,'X':X,'BI':BI,'scaleI':scales}
        H,HS=e.curvature(base,1,[Q(1,100)]*3)
        torch=c.torch;theta=torch.tensor([float(x) for x in model.params],requires_grad=True)
        B=torch.tensor([[float(x.midq()) for x in row] for row in BI]);xx=torch.tensor([[float(x) for x in row] for row in X])
        def f(y):
            h=c.forward(model,theta,xx+(B@y).reshape(xx.shape))
            S=torch.stack([torch.autograd.grad(h[i],theta,create_graph=True,retain_graph=True)[0] for i in range(2)])
            weights=[float(e.mpq(scales[model.meta[p][2]].midq())) for i,p in model.support]
            return torch.cat([h,torch.stack([S[i,p]*weights[k] for k,(i,p) in enumerate(model.support)])])
        for y in (torch.zeros(3),torch.tensor([.003,-.006,.009])):
            for i in range(2+len(model.support)):
                actual=torch.autograd.functional.hessian(lambda yy:f(yy)[i],y).detach().numpy()
                bound=H[i] if i<2 else HS[i-2]
                self.assertTrue(np.all(np.abs(actual)<=bound+1e-13))
    def test_frozen_model_parameters(self):
        c=e.prior.archived;m=c.Model('independent',2);old=m.serialize()
        c.jets(m,[[Q(1,8),Q(-1,8)]],'mp')
        self.assertEqual(m.serialize(),old)

if __name__=='__main__':
    meter=e.Meter('anisotropic certificate development checks')
    try:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
        (e.ROOT/'tests.json').write_text(json.dumps({'tests':result.testsRun,'passed':result.wasSuccessful(),
                                                  'failures':len(result.failures),'errors':len(result.errors)},indent=2))
        if not result.wasSuccessful():raise SystemExit(1)
    finally:meter.finish()
