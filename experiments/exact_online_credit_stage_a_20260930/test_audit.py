import unittest
import torch
import audit as a

class Tests(unittest.TestCase):
    def setUp(self):
        self.seed=a.CFG['development_seed']
    def test_data_determinism(self):
        self.assertTrue(all(torch.equal(u,v) for u,v in zip(a.data(self.seed,5,3),a.data(self.seed,5,3))))
    def test_initialization_determinism(self):
        self.assertTrue(torch.equal(a.Model('dense',2,self.seed,3).theta,a.Model('dense',2,self.seed,3).theta))
    def test_seed_isolation(self):
        self.assertFalse(torch.equal(a.data(self.seed,5,3)[0],a.data(self.seed+1,5,3)[0]))
        self.assertNotIn(self.seed,a.CFG['seeds'])
    def check_case(self,kind,depth):
        m=a.Model(kind,depth,self.seed,3); x,q,y=a.data(self.seed,7,3)
        theta=m.theta.clone()
        traj,_=a.inference(m,x)
        ref=a.bptt(m,x,q,y); exact=a.rtrl(m,x,q,y)
        self.assertTrue(all(a.passes(g) for g in a.grouped(m,exact['gradient'],ref['gradient'])))
        self.assertLess(float((exact['trajectory']-traj).abs().max()),1e-14)
        self.assertLess(float((ref['trajectory']-traj).abs().max()),1e-14)
        self.assertTrue(torch.equal(theta,m.theta))
        return m,x,q,y,ref,exact
    def test_dense_exact(self): self.check_case('dense',1)
    def test_stacked_dense_exact(self): self.check_case('dense',3)
    def test_diagonal_exact(self):
        m,x,q,y,ref,_=self.check_case('independent',1)
        cheap=a.local(m,x,q,y)
        self.assertTrue(all(a.passes(g) for g in a.grouped(m,cheap['gradient'],ref['gradient'])))
        self.assertEqual(cheap['persistent_derivative_scalars'],m.P)
    def test_deep_local_top_exact(self):
        for depth in (2,3):
            m,x,q,y,ref,_=self.check_case('independent',depth)
            groups=a.grouped(m,a.local(m,x,q,y)['gradient'],ref['gradient'])
            self.assertTrue(all(a.passes(g) for g in groups if g['layer']==depth))
    def test_layer_extraction(self):
        m=a.Model('independent',3,self.seed,3)
        g=torch.ones(m.P)
        out=a.grouped(m,g,g)
        self.assertEqual(len(out),12)
        self.assertEqual({o['layer'] for o in out},{1,2,3})
    def test_near_zero(self):
        metric=a.metric(torch.zeros(3),torch.zeros(3))
        self.assertTrue(metric['numerically_degenerate'])
        self.assertIsNone(metric['cosine_similarity'])
        self.assertTrue(a.passes(metric))
        self.assertFalse(a.passes(a.metric(torch.ones(3)*1e-9,torch.zeros(3))))
    def test_resource_inventory(self):
        m,x,q,y,ref,exact=self.check_case('independent',2)
        self.assertEqual(exact['persistent_derivative_scalars'],m.N*m.P)
        self.assertEqual(exact['auxiliary_derivative_bytes'],8*m.N*m.P)
        self.assertGreater(exact['peak_explicit_derivative_scalars'],m.N*m.P)
        self.assertGreater(ref['auxiliary_derivative_bytes'],0)
        self.assertEqual(exact['N_times_P'],2*exact['n_times_P'])
    def test_no_parameter_mutation(self):
        m=a.Model('independent',2,self.seed,3); x,q,y=a.data(self.seed,7,3)
        before=a.digest(m.theta)
        for fn in (a.bptt,a.rtrl,a.local): fn(m,x,q,y)
        self.assertEqual(before,a.digest(m.theta))
        self.assertFalse(m.theta.requires_grad)
        source=(a.ROOT/'audit.py').read_text()
        self.assertNotIn('torch.optim',source)
    def test_cpu_only(self):
        self.assertIsNone(torch.version.cuda)
        self.assertEqual(a.hardware()['device'],'cpu')
        self.assertEqual(torch.get_default_dtype(),torch.float64)
    def test_support_causal_direction(self):
        m,x,q,y,_,exact=self.check_case('independent',3)
        blocks=a.support(m,exact['sensitivity'])['blocks']
        self.assertTrue(all(b['nonzero_exact']==0 for b in blocks if b['parameter_layer']>b['state_layer']))
        self.assertTrue(all(b['nonzero_above_threshold']>0 for b in blocks if b['parameter_layer']<b['state_layer']))
    def test_local_jacobians_against_autograd(self):
        m=a.Model('dense',2,self.seed,3)
        x,q,y=a.data(self.seed,1,3)
        prev=torch.arange(m.N)*.01
        h,A,B,_=a.jacobians(m,prev,x[0])
        aa,bb=torch.autograd.functional.jacobian(lambda hp,theta:m.step(hp,x[0],theta),(prev,m.theta))
        self.assertLess(float((A-aa).abs().max()),1e-14)
        self.assertLess(float((B-bb).abs().max()),1e-14)

if __name__=='__main__':
    meter=a.Meter('development unit validation')
    try: unittest.main()
    finally: meter.finish()
