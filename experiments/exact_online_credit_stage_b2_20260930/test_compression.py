import os
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for _key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[_key]='1'
import hashlib
import unittest
import numpy as np
import sympy as sp
import torch
import core as c
import structures as st
import compression as comp
import run

class CompressionTests(unittest.TestCase):
    def make(self,case='rank1_feedback'):
        return run.make(case,4,c.CFG['development_seed'])
    def audit(self,m):
        x,q,y=c.data(c.CFG['development_seed'],7,m.n);ref=c.rtrl(m,x,q,y)
        local=comp.residual_run(m,x,q,y)
        self.assertLess(c.metric(local['S'],ref['S'])['relative_error'],1e-8)
        return x,q,y,ref,local
    def test_copied_frozen_source(self):
        old=c.ROOT.parent/'exact_online_credit_stage_b_20260930'
        for p in ('core.py','structures.py'):
            self.assertEqual(hashlib.sha256((old/p).read_bytes()).hexdigest(),hashlib.sha256((c.ROOT/p).read_bytes()).hexdigest())
    def test_scope_count(self):
        cases=list(run.configurations());self.assertEqual(len(cases),160)
        self.assertEqual(len({run.name(z) for z in cases}),160)
        self.assertEqual(set(c.CFG['seeds']),set(range(9401100,9401105)))
    def test_all_snapshot_reconstructions(self):
        for case in c.CFG['cases']:
            m=self.make(case);x,q,y,ref,local=self.audit(m)
            shared=c.shared_run(m,x,q,y)['S'] if m.linear_shared else None
            for row in comp.snapshot(m,ref['S'],local['E'],shared):
                self.assertTrue(row['passes'],(case,row['method'],row['tolerance']))
                self.assertEqual(row['stored_bytes'],8*row['stored_numbers'])
    def test_residual_exact_gradient_all_layers(self):
        for case in ('rank1_feedback','explicit_feedback','deep2','deep3'):
            m=self.make(case);x,q,y,ref,local=self.audit(m);b=c.bptt(m,x,q,y)
            self.assertTrue(all(c.passes(g) for g in c.grouped(m,local['gradient'],b['gradient'])))
            self.assertTrue(torch.equal(ref['trajectory'],local['trajectory']))
    def test_zero_and_rank_one(self):
        for matrix,rank in [(torch.zeros(4,9),0),(torch.ones(4,9),1)]:
            rebuilt,count,r=comp.svd(matrix,1e-12);self.assertEqual(r,rank)
            self.assertLess(float((rebuilt-matrix).norm()),1e-12)
            self.assertEqual(count,rank*13)
    def test_family_QR_matches_direct(self):
        rng=np.random.default_rng(901);mat=rng.normal(size=(32,3,7))
        rows=comp.family_span(mat,[8,16,32])
        for row in rows:
            actual=comp.rank_details(torch.tensor(mat[:row['samples']].reshape(row['samples'],-1)))
            self.assertEqual(actual['ranks'],row['uncentered']['ranks'])
            expected=np.linalg.svd((mat[:row['samples']]-mat[:row['samples']].mean(axis=0)).reshape(row['samples'],-1),compute_uv=False)
            got=np.array(row['centered']['singular_values'])
            self.assertLess(np.linalg.norm(got-expected[:len(got)])/np.linalg.norm(expected),1e-12)
            self.assertLess(row['QR_reconstruction_error'],1e-12)
    def test_shared_family_saturation(self):
        m=self.make('shared_linear');samples=[]
        for stream in range(1000,1032):
            x,q,y=c.data(c.CFG['development_seed'],12,4,stream);samples.append(c.rtrl(m,x,q,y)['S'].numpy())
        rows=comp.family_span(np.stack(samples),[8,16,32])
        self.assertEqual(rows[-1]['centered']['ranks']['1e-08'],8)
        self.assertEqual(rows[-1]['uncentered']['ranks']['1e-08'],9)
    def test_rank_interval_and_tail(self):
        D=torch.diag(torch.tensor([1.,1e-9,1e-13]))
        r=comp.rank_details(D)
        self.assertEqual(r['ranks']['1e-08'],1);self.assertEqual(r['ranks']['1e-14'],3)
        self.assertEqual(r['tail_ranks']['1e-08'],1)
    def test_symbolic_control_ranks(self):
        # Exact rationals distinguish real algebraic rank from tolerance-based rank.
        D=sp.diag(1,sp.Rational(1,10**20));self.assertEqual(D.rank(),2)
        K=sp.kronecker_product(sp.eye(3),sp.Matrix([[1,2,3]]));self.assertEqual(K.rank(),3)
        self.assertEqual((sp.Matrix([[1],[2],[3]])*sp.Matrix([[1,2,3]])).rank(),1)
    def test_mutation_CPU_budget(self):
        m=self.make('deep3');before=c.digest(m.theta);self.audit(m)
        self.assertEqual(before,c.digest(m.theta));self.assertEqual(m.theta.device.type,'cpu')
        self.assertEqual(m.theta.dtype,torch.float64);self.assertIsNone(torch.version.cuda)
        self.assertEqual(c.CFG['measured_cpu_cap_seconds'],1800)
        self.assertFalse(c.CFG['stage_c_authorized']);self.assertFalse(c.CFG['parameter_updates'])
    def test_no_ceiling_promotion(self):
        self.assertEqual(comp.classify([],[],False),'STAGE B2 — INCONCLUSIVE')
    def test_actual_BLAS_pools(self):
        import psutil
        from pools import thread_pools
        pools=thread_pools(psutil.Process());self.assertEqual(len(pools),2)
        self.assertTrue(all(p['threads']==1 for p in pools),pools)

if __name__=='__main__':
    meter=c.Meter('Stage-B2 development validation including copied Stage-B controls')
    try:
        c.hardware()
        suite=unittest.defaultTestLoader.discover(str(c.ROOT),pattern='test_*.py')
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():raise SystemExit(1)
    finally:meter.finish()
