import unittest
import weakref
import numpy as np
import torch
import core as c
import structures as s

class Tests(unittest.TestCase):
    def setUp(self):self.seed=c.CFG['development_seed']
    def model(self,family='block',interaction=1,depth=1,mode='stack_nonlinear',linear=False):
        return c.Model(4,depth,family,interaction,self.seed,mode,linear)
    def check(self,m):
        x,q,y=c.data(self.seed,9,m.n);before=c.digest(m.theta);ref=c.bptt(m,x,q,y);exact=c.rtrl(m,x,q,y)
        self.assertTrue(all(c.passes(g) for g in c.grouped(m,exact['gradient'],ref['gradient'])))
        self.assertLess(float((ref['trajectory']-exact['trajectory']).abs().max()),1e-14)
        self.assertEqual(before,c.digest(m.theta));self.assertTrue(torch.isfinite(exact['S']).all())
        return x,q,y,ref,exact
    def test_data_and_loss_prefix(self):
        a=c.data(self.seed,5,4);b=c.data(self.seed,10,4)
        self.assertTrue(torch.equal(a[0],b[0][:5]));self.assertTrue(torch.equal(a[1],b[1]));self.assertEqual(float(a[2]),float(b[2]))
    def test_seed_isolation(self):
        self.assertNotIn(self.seed,c.CFG['seeds'])
        self.assertFalse(torch.equal(c.data(self.seed,5,4)[0],c.data(self.seed+1,5,4)[0]))
    def test_initialization(self):self.assertTrue(torch.equal(self.model().theta,self.model().theta))
    def test_block_axis_correctness(self):
        for k in (1,2,4):self.check(self.model(interaction=k,depth=3))
    def test_rank_axis_correctness(self):
        for r in (0,1,2,4):self.check(self.model('lowrank',r,3))
    def test_mix_modes_correctness(self):
        for mode in c.CFG['mix_modes']:self.check(self.model(mode=mode))
    def test_analytic_partials(self):
        for m in (self.model('lowrank',2,2),self.model(mode='feedback'),self.model(interaction=2,depth=2)):
            prev=torch.arange(m.N)*.01;x=c.data(self.seed,1,m.n)[0][0]
            h,A,B,_=c.partials(m,prev,x)
            aa,bb=torch.autograd.functional.jacobian(lambda hp,theta:m.step(hp,x,theta),(prev,m.theta))
            self.assertLess(float((A-aa).abs().max()),1e-14);self.assertLess(float((B-bb).abs().max()),1e-14)
    def test_exact_packed(self):
        for m in (self.model(depth=3),self.model('lowrank',1,3),self.model(interaction=2),self.model(mode='feedback')):
            x,q,y,ref,full=self.check(m);_,_,closure,masks=c.graphs(m)
            value=c.packed_run(m,x,q,y,closure)
            self.assertTrue(c.passes(c.metric(value['S'],full['S'])))
            self.assertTrue(all(c.passes(g) for g in c.grouped(m,value['gradient'],ref['gradient'])))
            self.assertEqual(value['stored_derivative_scalars'],int(closure.sum()))
            self.assertGreater(value['index_bytes'],0)
    def test_snap_reachability(self):
        for m in (self.model(),self.model(interaction=4),self.model('lowrank',1,3)):
            x,q,y,ref,full=self.check(m);_,_,closure,masks=c.graphs(m)
            self.assertTrue(np.array_equal(masks['SnAp2'],closure))
            value=c.packed_run(m,x,q,y,masks['SnAp2'])
            self.assertTrue(c.passes(c.metric(value['S'],full['S'])))
        self.assertFalse(np.array_equal(c.graphs(self.model(interaction=4))[3]['SnAp1'],c.graphs(self.model(interaction=4))[2]))
    def test_readout_does_not_change_state(self):
        for mode in ('trainable_linear','nonlinear_trainable'):
            m=self.model(mode=mode);*_,full=self.check(m)
            self.assertEqual(int(torch.count_nonzero(full['S'][:,m.head['start']:m.head['end']])),0)
    def test_feedback_does_change_state(self):
        m=self.model(mode='feedback');*_,full=self.check(m)
        self.assertGreater(int(torch.count_nonzero(full['S'][:,m.head['start']:m.head['end']])),0)
    def test_shared_exact_positive(self):
        m=self.model(linear=True);x,q,y,ref,full=self.check(m);shared=c.shared_run(m,x,q,y)
        self.assertTrue(c.passes(c.metric(shared['S'],full['S'])))
        self.assertTrue(all(c.passes(g) for g in c.grouped(m,shared['gradient'],ref['gradient'])))
        self.assertEqual(shared['stored_derivative_scalars'],2*m.n+1)
    def test_online_lowrank_factor(self):
        m=self.model('lowrank',1,2);x,q,y,ref,full=self.check(m);value=s.factor_run(m,x,q,y)
        self.assertTrue(c.passes(c.metric(value['S'],full['S'])))
        self.assertTrue(all(c.passes(g) for g in c.grouped(m,value['gradient'],ref['gradient'])))
    def test_exact_kronecker_sum(self):
        m=self.model('lowrank',1);x,q,y,ref,full=self.check(m);value=s.kronecker_sum_run(m,x,q,y)
        self.assertTrue(c.passes(c.metric(value['S'],full['S'])))
        self.assertEqual(value['kronecker_terms'],len(x))
        self.assertTrue(all(c.passes(g) for g in c.grouped(m,value['gradient'],ref['gradient'])))
    def test_compression_metadata(self):
        m=self.model('lowrank',1);x,q,y,ref,full=self.check(m)
        probes=s.compression(m,full['S'],full['trajectory'][-1],q,y,ref['gradient'])
        for name in ('matrix_minimum_rank','kronecker_minimum_sum'):
            self.assertTrue(next(p for p in probes if p['name']==name)['passes'])
    def test_degenerate_metric(self):
        self.assertTrue(c.passes(c.metric(torch.zeros(4),torch.zeros(4))))
        self.assertFalse(c.passes(c.metric(torch.ones(4)*1e-9,torch.zeros(4))))
    def test_no_parameter_update(self):
        m=self.model();before=c.digest(m.theta);self.check(m)
        self.assertEqual(before,c.digest(m.theta));self.assertFalse(m.theta.requires_grad)
        self.assertNotIn('torch.optim',(c.ROOT/'core.py').read_text())
    def test_cpu_enforcement(self):
        self.assertEqual(c.hardware()['device'],'cpu');self.assertIsNone(torch.version.cuda);self.assertEqual(torch.get_default_dtype(),torch.float64)
    def test_resource_and_index_inventory(self):
        m=self.model(depth=2);x,q,y,ref,full=self.check(m)
        self.assertEqual(full['stored_derivative_scalars'],m.N*m.P)
        p=c.Packed(c.graphs(m)[2]);values,idx=p.storage()
        self.assertEqual(values,int(c.graphs(m)[2].sum()))
        self.assertEqual(idx,sum((r.numel()+col.numel())*8 for r,col,_ in p.parts))
    def test_support_direction(self):
        m=self.model(depth=3);x,q,y,ref,full=self.check(m)
        for block in s.support(m,full['S'])['blocks']:
            if block['parameter_layer']>block['state_layer']:self.assertEqual(block['nonzero'],0)
            elif block['parameter_layer']<block['state_layer']:self.assertGreater(block['threshold_counts']['1e-12'],0)

if __name__=='__main__':
    meter=c.Meter('development unit validation')
    try:unittest.main()
    finally:meter.finish()
