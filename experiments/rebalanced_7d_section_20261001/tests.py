import sys,time,unittest,importlib.util
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import common as c
spec=importlib.util.spec_from_file_location('accepted_tests',c.ACCEPTED/'tests.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
class Extra(unittest.TestCase):
    def test_source_transform(self):
        d=c.json.loads((c.ROOT/'SOURCE_TRANSFORM.json').read_text())
        s=(c.ACCEPTED/'kernel.py').read_text()
        for a,b in d['kernel_replacements']:
            self.assertEqual(s.count(a),1);s=s.replace(a,b)
        self.assertEqual(s,(c.ROOT/'kernel.py').read_text())
    def test_exact_cancellation(self):
        I=c.k.I;I.precision(192)
        W=[[c.Q(1),c.Q(-1)],[c.Q(2),c.Q(3)]]; V=[c.Q(1,7),c.Q(1,7)]
        value=sum((I(w)*I(v) for w,v in zip(W[0],V)),I(0))
        self.assertLess(float(value.absq()),1e-50)
        bound=c.k.uq(sum((I(w)*I(v) for w,v in zip(W[1],V)),I(0)).absq())
        self.assertGreaterEqual(c.Q(bound),c.Q(5,7))
        rad=c.Q(5,7);box=I(-I(rad).hi,I(rad).hi,True)
        self.assertLessEqual(c.Q(box.lo,I.scale),-rad);self.assertGreaterEqual(c.Q(box.hi,I.scale),rad)
    def test_rotations_deterministic(self):
        self.assertEqual(c.fixtures(),c.fixtures())
        for d in c.fixtures().values():
            self.assertEqual(c.np.array(d['B']).shape,(148,11));self.assertEqual(c.np.array(d['L']).shape,(7,24))
    def test_rounding(self):
        aa,h=c.round_widths([.013,.001234,.3],.005)
        for v,x in zip(aa,[.013,.001234,.3]):self.assertLessEqual(v,c.Q(x))
        self.assertGreaterEqual(h,c.Q(.005)*c.Q(51,50))
    def test_tightened_mixed_derivatives(self):
        k=c.k; Q=c.Q; np=c.np; torch=k.a.c.torch
        case={'case':'independent','n':2,'X':[['1/8','-1/7'],['2/9','1/11'],['-1/10','1/12']]}
        B=[[Q((-1)**(i+j)*(i+2*j+1),17) for j in range(4)] for i in range(6)]
        base=k.a.base_for(case,B,192,JI=None); m=base['model']; before=m.serialize()
        hh,h3,ss,s3=k.third_majorants(base,2,[Q(1,100)]*4)
        params=torch.tensor(list(map(float,m.params))); X=torch.tensor([[float(Q(v)) for v in row] for row in case['X']])
        Bt=torch.tensor([[float(v) for v in row] for row in B])*(3/32)**.5
        weights=torch.tensor([float(base['scaleI'][m.meta[p][2]].midq()) for i,p in m.support])
        def f(z):
            xx=X+(Bt@z).reshape(3,2);h=k.a.c.forward(m,params,xx)
            S=torch.func.jacrev(lambda theta:k.a.c.forward(m,theta,xx))(params)
            return torch.cat([h,torch.stack([S[i,p] for i,p in m.support])*weights])
        d2=torch.func.jacfwd(torch.func.jacrev(f));d3=torch.func.jacfwd(d2)
        for signs in ([0,0,0,0],[1,-1,1,-1],[-1,1,1,-1]):
            z=torch.tensor(np.array(signs)*.01)
            self.assertTrue((abs(d2(z).detach().numpy())<=np.concatenate([hh,ss])+1e-13).all())
            self.assertTrue((abs(d3(z).detach().numpy())<=np.concatenate([h3,s3])+1e-13).all())
        self.assertEqual(before,m.serialize())
if __name__=='__main__':
    hist={str(p):c.sha(p) for p in c.CONTROL.rglob('*') if p.is_file()}
    suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(old.Checks),unittest.defaultTestLoader.loadTestsFromTestCase(Extra)])
    res=unittest.TextTestRunner(verbosity=2).run(suite)
    unchanged=all(c.sha(c.Path(p))==h for p,h in hist.items())
    c.write('tests.json',{'passed':res.wasSuccessful() and unchanged,'tests':res.testsRun,
        'failures':[(str(t),s) for t,s in res.failures+res.errors],'control_unchanged':unchanged,
        'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
        'peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset})
    sys.exit(0 if res.wasSuccessful() and unchanged else 1)
