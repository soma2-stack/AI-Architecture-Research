"""Development-only checks on tiny charts, not the official 6D outcome."""
import sys, time, json, unittest
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import kernel as k
from fractions import Fraction as Q
import numpy as np
torch=k.a.c.torch

class Checks(unittest.TestCase):
    def test_cpu(self):
        self.assertIsNone(torch.version.cuda)
        self.assertEqual(torch.ones(1).device.type,'cpu')
        self.assertEqual(torch.ones(1).dtype,torch.float64)

    def test_fourth_tanh(self):
        for value in (-.9,-.2,0.,.3,.8):
            x=torch.tensor(value,requires_grad=True); d=torch.tanh(x)
            for _ in range(4): d=torch.autograd.grad(d,x,create_graph=True)[0]
            h=torch.tanh(x); expected=8*h*(1-h*h)*(2-3*h*h)
            self.assertLess(float(abs(d-expected).detach()),1e-13)

    def test_even_cancellation(self):
        for z in (-1.,-.25,0.,.9):
            f=lambda v: v+1000*v*v+Q(1,10)*v**3
            self.assertAlmostEqual(f(z)-f(-z),2*z+.2*z**3,places=10)

    def test_rational_collision(self):
        self.assertGreater(2*Q(1323751,10**9),2*Q(1,1000))
        self.assertFalse(Q(1,1000)>Q(1,1000))

    def test_product_rule(self):
        # Third derivative of exp(x)*exp(2x) at zero is27.
        p,p1,p2,p3=1,2,4,8; f1,f2,f3,f4=1,1,1,1
        result=f1*p3+f2*(3*p2)+f3*(3*p1)+f4*p
        self.assertEqual(result,27)

    def test_implicit_polynomial(self):
        # H=y-t^2-t^3=0, s=y*t: at zero s'''=6 from s''[y'',t].
        V=np.array([[0.],[1.]])
        HH=np.array([[[0.,0.],[0.,2.]]]); HH3=np.zeros((1,2,2,2)); HH3[0,1,1,1]=6
        y2=k.contract2(HH,V); W2=np.vstack([y2,np.zeros((1,1,1))])
        y3=k.upadd(k.contract3(HH3,V),k.mixed_chain(HH,W2,V))
        HS=np.array([[[0.,1.],[1.,0.]]])
        s3=k.mixed_chain(HS,W2,V)
        self.assertGreaterEqual(float(s3[0,0,0,0]),6.)
        self.assertLess(float(s3[0,0,0,0]),6.+1e-12)
        self.assertGreaterEqual(float(y3[0,0,0,0]),6.)
        # s=y+y*t also has the essential s_y y''' term: total12.
        composed=k.upadd(s3,k.left(np.array([[1.]]),y3))
        self.assertGreaterEqual(float(composed[0,0,0,0]),12.)
        self.assertLess(float(composed[0,0,0,0]),12.+1e-12)

    def test_upward_algebra(self):
        for x,y in [(Q(1,3),Q(2,7)),(Q(1,10**30),Q(7,9))]:
            u,v=k.uq(x),k.uq(y)
            self.assertGreaterEqual(Q(float(k.upmul(u,v))),x*y)
            self.assertGreaterEqual(Q(float(k.upadd(u,v))),x+y)

    def test_tiny_models(self):
        for family in ('dense','independent'):
            case={'case':family,'n':2,'X':[['1/8','-1/7'],['2/9','1/11'],['-1/10','1/12']]}
            B=[[Q(int(i==j)) for j in range(4)] for i in range(6)]
            base=k.a.base_for(case,B,192,JI=None); m=base['model']; saved=m.serialize()
            amps=[Q(1,100)]*4; hh,h3,ss,s3=k.third_majorants(base,2,amps)
            oldh,olds=k.a.curvature(base,2,amps)
            self.assertTrue(np.allclose(hh,oldh,rtol=1e-12,atol=1e-300))
            self.assertTrue(np.allclose(ss,olds,rtol=1e-12,atol=1e-300))
            params=torch.tensor([float(v) for v in m.params]); X0=torch.tensor([[float(Q(v)) for v in row] for row in case['X']])
            Bt=torch.tensor([[float(v) for v in row] for row in B])*(3/32)**.5
            weights=torch.tensor([float(base['scaleI'][m.meta[p][2]].midq()) for i,p in m.support])
            def endpoint(z):
                X=X0+(Bt@z).reshape(3,2)
                h=k.a.c.forward(m,params,X)
                S=torch.func.jacrev(lambda theta:k.a.c.forward(m,theta,X))(params)
                return torch.cat([h,torch.stack([S[i,p] for i,p in m.support])*weights])
            d2=torch.func.jacfwd(torch.func.jacrev(endpoint))
            d3=torch.func.jacfwd(d2)
            bound2=np.concatenate([hh,ss]); bound3=np.concatenate([h3,s3])
            for signs in ([0,0,0,0],[1,1,1,1],[-1,-1,-1,-1],[1,-1,1,-1],[-1,1,1,-1]):
                z=torch.tensor(np.array(signs)*.01)
                actual2=d2(z).detach().numpy(); actual3=d3(z).detach().numpy()
                self.assertTrue((abs(actual2)<=bound2+1e-13).all())
                self.assertTrue((abs(actual3)<=bound3+1e-13).all())
            # Independent derivative paths: exact jets versus autograd/BPTT.
            _,_,Sjet=k.a.c.jets(m,[[Q(v) for v in row] for row in case['X']],'float')
            Sauto=torch.func.jacrev(lambda theta:k.a.c.forward(m,theta,X0))(params).numpy()
            self.assertLess(float(np.linalg.norm(Sjet-Sauto)/max(np.linalg.norm(Sauto),1e-12)),1e-8)
            self.assertEqual(saved,m.serialize())

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Checks)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    data={'tests':result.testsRun,'failures':[(str(t),msg) for t,msg in result.failures],
          'errors':[(str(t),msg) for t,msg in result.errors],'passed':result.wasSuccessful(),
          'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
          'peak_working_set_bytes':k.a.c.psutil.Process().memory_info().peak_wset,'gpu_used':False}
    (k.ROOT/'development_tests.json').write_text(json.dumps(data,indent=2))
    sys.exit(0 if result.wasSuccessful() else 1)
