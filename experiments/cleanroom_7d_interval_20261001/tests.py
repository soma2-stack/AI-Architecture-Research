"""Synthetic tests only; no original engine or generated certificate imports."""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['OMP_NUM_THREADS']='1'
import ast,itertools,json,math,time,unittest
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import mpmath as mp
import torch
from arithmetic import *
from taylor import Ring,hidden_compose
from replay import center,bound_jets,transform,mixed,left,arr
torch.set_num_threads(1)
HERE=Path(__file__).resolve().parent

def tiny():
    return {'endpoint':{'n':2,'X':[['1/5','-1/4'],['-1/7','1/3']]},'r':2,
            'model_parameters':['3/10','2/5','1/2','-1/4','1/8','3/8','1/64','-1/64'],
            'B':[['1/10','0','0','0'],['0','1/10','0','0'],['0','0','1/10','0'],['0','0','0','1/10']],
            'a':['1/1000','1/1000'],'ah':'1/1000'}

def torch_map(c,w):
    n=c['endpoint']['n']; th=torch.tensor([float(F(x)) for x in c['model_parameters']],dtype=torch.float64,requires_grad=True)
    X=torch.tensor([[float(F(x)) for x in row] for row in c['endpoint']['X']],dtype=torch.float64)
    B=torch.tensor([[float(F(x)) for x in row] for row in c['B']],dtype=torch.float64)*math.sqrt(3/32)
    hist=X+(B@w).reshape(X.shape)
    h=torch.zeros(n,dtype=torch.float64)
    for x in hist:
        h=torch.tanh(th[:n]*h+th[n:n+n*n].reshape(n,n)@x+th[n+n*n:])
    weights=[th[a:b].square().mean().sqrt().detach() for a,b in ((0,n),(n,n+n*n),(n+n*n,len(th)))]
    coords=[]
    for i in range(n):
        sens=torch.autograd.grad(h[i],th,create_graph=True,retain_graph=True)[0]
        owned=[i]+[n+i*n+j for j in range(n)]+[n+n*n+i]
        coords.extend(sens[p]*weights[g] for p,g in zip(owned,[0]+[1]*n+[2]))
    return torch.cat((h,torch.stack(coords)))

class Tests(unittest.TestCase):
    def setUp(self): set_precision(192)
    def test_fraction_rounding(self):
        for f in (F(1,3),F(7,10),F(123,1025)):
            self.assertLessEqual(lower_fraction(interval(f)),f)
            self.assertGreaterEqual(upper_fraction(interval(f)),f)
            self.assertGreaterEqual(Up(f).frac(),f)
    def test_directed_positive_operations(self):
        x,y=Up(F(1,3)),Up(F(1,7))
        self.assertGreaterEqual((x+y).frac(),x.frac()+y.frac())
        self.assertGreaterEqual((x*y).frac(),x.frac()*y.frac())
        self.assertGreaterEqual((x/y).frac(),x.frac()/y.frac())
        self.assertGreaterEqual(x.sqrt().frac()**2,x.frac())
    def test_tanh_enclosure_high_precision(self):
        mp.mp.prec=384
        for lo,hi in ((F(-3,4),F(1,4)),(F(1,3),F(1,3)),(F(-1,5),F(-1,5))):
            z=tanh_box(hull(lo,hi))
            for x in (lo,hi):
                v=mp.tanh(mp.mpf(x.numerator)/x.denominator)
                lower=lower_fraction(z); upperf=upper_fraction(z)
                self.assertLessEqual(mp.mpf(lower.numerator)/lower.denominator,v)
                self.assertGreaterEqual(mp.mpf(upperf.numerator)/upperf.denominator,v)
    def test_polynomial_repeated_indices(self):
        ring=Ring(2); a=ring.empty(); a[ring.lookup[(0,)]]=Up(2); a[ring.lookup[(1,)]]=Up(3)
        a2=ring.mul(a,a); a3=ring.mul(a2,a)
        self.assertEqual(a2[ring.lookup[(0,1)]].frac(),12)
        self.assertEqual(a3[ring.lookup[(0,0,1)]].frac(),36)
        t=ring.tensors([a3],3)
        self.assertEqual(t[0,0,0,1].frac(),72)
        self.assertEqual(t[0,0,0,0].frac(),48)
    def test_center_autodiff_and_frozen(self):
        c=tiny(); before=json.dumps(c,sort_keys=True)
        JH,JS,_,_=center(c)
        w=torch.zeros(4,dtype=torch.float64,requires_grad=True)
        jac=torch.autograd.functional.jacobian(lambda z:torch_map(c,z),w).detach().numpy()
        mid=np.array([[float((lower_fraction(x)+upper_fraction(x))/2) for x in row] for row in np.concatenate((JH,JS))])
        np.testing.assert_allclose(mid,jac,rtol=2e-13,atol=1e-15)
        self.assertEqual(before,json.dumps(c,sort_keys=True))
    def test_whole_box_second_third_bounds(self):
        c=tiny(); bounds,_=bound_jets(c)
        q=4
        for v in (torch.zeros(q,dtype=torch.float64),torch.tensor([.001,-.001,.001,-.001],dtype=torch.float64)):
            H2=torch.autograd.functional.jacobian(lambda z:torch.autograd.functional.jacobian(lambda w:torch_map(c,w),z,create_graph=True),v,create_graph=True)
            H3=torch.autograd.functional.jacobian(lambda z:torch.autograd.functional.jacobian(lambda w:torch.autograd.functional.jacobian(lambda a:torch_map(c,a),w,create_graph=True),z,create_graph=True),v)
            for data,names in ((H2,('HH','HS')),(H3,('HH3','HS3'))):
                b=np.concatenate([bounds[k] for k in names])
                ub=np.vectorize(float)(b)
                self.assertTrue(np.all(np.abs(data.detach().numpy())<=ub*(1+2e-13)))
    def test_affine_cancellation_keeps_W_injections(self):
        c=tiny(); c['model_parameters'][2:4]=['1','-1']; c['B'][0]=['1','0','0','0']; c['B'][1]=['1','0','0','0']
        _,JS,_,_=center(c)
        # First step W*x cancels its chart derivative, but parameter injection does not.
        self.assertGreater(float(abs_upper(JS[1,0])),.01)
        b,_=bound_jets(c)
        self.assertGreater(float(b['HS'][1,0,0]),0)
    def test_contraction_axis_order(self):
        T=arr([[1,2],[3,4]],Up).reshape(1,2,2)
        V=arr([[1,2],[3,4]],Up)
        got=transform(T,V)
        expected=np.einsum('pab,ai,bj->pij',np.array(T,dtype=float),np.array(V,dtype=float),np.array(V,dtype=float))
        np.testing.assert_array_equal(np.array(got,dtype=float),expected)
        T3=np.ones((1,2,2),dtype=object); T3.fill(Up(1)); W=np.ones((2,2,2),dtype=object); W.fill(Up(1))
        m=mixed(T3,W,V)
        # Independently explicit all three partitions.
        expect=np.zeros((1,2,2,2))
        for i,j,k in itertools.product(range(2),repeat=3):
            expect[0,i,j,k]=sum(float(V[b,k]+V[b,j]+V[b,i]) for a,b in itertools.product(range(2),repeat=2))
        np.testing.assert_array_equal(np.array(m,dtype=float),expect)
    def test_rational_and_interval_inverse(self):
        M=[[F(2),F(1)],[F(1),F(3)]]
        e=rational_inverse(M); f=matrix_inverse(M)
        for i,j in itertools.product(range(2),repeat=2):
            self.assertLessEqual(lower_fraction(f[i][j]),e[i][j]); self.assertGreaterEqual(upper_fraction(f[i][j]),e[i][j])
    def test_CPU_only(self):
        self.assertEqual(os.environ['CUDA_VISIBLE_DEVICES'],'')
        self.assertEqual(torch.tensor(0).device.type,'cpu')
        self.assertEqual(torch.get_num_threads(),1)
    def test_no_old_engine_imports(self):
        for path in HERE.glob('*.py'):
            tree=ast.parse(path.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node,ast.ImportFrom):
                    self.assertNotIn('kernel',node.module or '')
                    self.assertNotIn('cpu_jets',node.module or '')
                    self.assertFalse((node.module or '').startswith('experiments.'))
    def test_gate_derivatives(self):
        mp.mp.prec=384
        for x in (F(-1,3),F(1,4),F(1,2)):
            h=tanh_box(interval(x)); g=gates(h)
            v=mp.mpf(x.numerator)/x.denominator
            for k in range(1,5):
                actual=abs(mp.diff(mp.tanh,v,k)); uf=g[k-1].frac()
                self.assertLessEqual(actual,mp.mpf(uf.numerator)/uf.denominator)

if __name__=='__main__':
    start=time.perf_counter();cpu=time.process_time()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    (HERE/'development_tests.json').write_text(json.dumps({'tests':result.testsRun,'passed':result.wasSuccessful(),
        'failures':[str(x[0])+'\n'+x[1] for x in result.failures], 'errors':[str(x[0])+'\n'+x[1] for x in result.errors],
        'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-start},indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
