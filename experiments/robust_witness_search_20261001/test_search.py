import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import unittest,json,hashlib
from fractions import Fraction as Q
import numpy as np
import numerics as a
import cpu_jets as c
os.environ['CUDA_VISIBLE_DEVICES']='0'
from resources import Monitor,ROOT,CFG

class Checks(unittest.TestCase):
    def test_pool_split_and_domain(self):
        for n in (2,3,4):
            p=np.load(ROOT/f'pool_n{n}.npz');self.assertEqual(len(p['X']),10000)
            self.assertEqual(np.sum(p['confirmation']),2000)
            self.assertTrue(np.all(np.abs(p['X'])<=.5))
            h=json.loads((ROOT/'pool_manifest.json').read_text())[str(n)]
            self.assertEqual(hashlib.sha256(p['X'].tobytes()).hexdigest(),h['history_array_sha256'])
    def test_cpu_gpu_jets_all_models(self):
        rng=np.random.default_rng(CFG['development_seed'])
        for n in (2,3,4):
            for case in CFG['models']:
                m=a.model(n,case);X=rng.uniform(-.5,.5,(2,3,n))
                _,_,GPU=a.jets(m,X);_,_,CPU=a.jets(m,X,np)
                self.assertLess(np.max(np.abs(a.cp.asnumpy(GPU)-CPU)),1e-12)
                archived=c.Model(case,n);archived.params=[Q(float(x)) for x in m['params']]
                F,J,S=c.jets(archived,[[Q(float(v)) for v in row] for row in X[0]],'float')
                self.assertLess(np.max(np.abs(J-CPU[0])),1e-12)
    def test_cpu_gpu_curvature(self):
        m=a.model(3,'dense');rng=np.random.default_rng(CFG['development_seed'])
        X=rng.uniform(-.5,.5,(2,3,3));B=rng.normal(0,.05,(2,9,5));amp=np.full((2,5),.125)
        HH,HS=a.curvature_batch(m,X,B,amp);HC,SC=a.curvature_batch(m,X,B,amp,np)
        self.assertLess(np.max(np.abs(HH-HC)),1e-12);self.assertLess(np.max(np.abs(HS-SC)),1e-12)
        self.assertEqual(HH.shape,(2,3,5,5));self.assertEqual(HS.shape,(2,63,5,5))
        self.assertTrue(np.all(HH>0) and np.all(HS>0))
    def test_query_duality(self):
        m=a.model(3,'dense');rng=np.random.default_rng(CFG['development_seed']);L=rng.normal(size=(4,63));mu=a.margins(m,L)
        delta=rng.normal(size=(3,21));proj=np.einsum('rip,ip->r',a.tensor_rows(m,L),delta)
        queries=m['C']/(np.sqrt(3)*m['beta']);dist=np.linalg.norm(delta.T@queries,axis=0).max()
        self.assertTrue(np.all(mu*np.abs(proj)<=dist))
    def test_fixed_hidden_frames(self):
        m=a.model(3,'dense');X=np.load(ROOT/'pool_n3.npz')['X'][0];f=a.frame(m,X)
        self.assertLess(np.linalg.norm(f['J'][:3]@f['B'][:,3:]),1e-10)
        L=a.query_projection(m,f['U'][:4]);self.assertTrue(np.all(a.margins(m,L)>0))
    def test_baseline_proxy_valid(self):
        m=a.model(3,'dense');X=np.array([[float(Q(v)) for v in row] for row in a.SAVED['baseline_histories']['3']]);f=a.frame(m,X)
        amp=np.full((1,5),.125);HH,HS=a.curvature_batch(m,X[None],f['B'][None,:,:5],amp)
        row=a.proxy(m,f,2,.125,'equal',1,HH[0],HS[0]);self.assertTrue(row['valid']);self.assertGreaterEqual(row['robust'],1)
    def test_error_contract(self):
        self.assertEqual(Q(CFG['epsilon']),Q(1,1000));self.assertEqual(CFG['widths'],[2,3,4])
        self.assertEqual(CFG['horizons'],{'2':11,'3':22,'4':37})

if __name__=='__main__':
    meter=Monitor('development tests',gpu=True)
    try:
        r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
        path=ROOT/f'tests_attempt{len(list(ROOT.glob("tests_attempt*.json")))+1}.json'
        path.write_text(json.dumps({'tests':r.testsRun,'passed':r.wasSuccessful(),'failures':len(r.failures),'errors':len(r.errors)},indent=2)+'\n',encoding='utf-8')
        if not r.wasSuccessful():raise SystemExit(1)
    finally:meter.finish()
