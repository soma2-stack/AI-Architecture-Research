import unittest
import numpy as np
import torch
from common import Classifier, rng, state_bytes, tensor, hardware_check
from t1 import dataset, rule_control, metrics

class ValidationTests(unittest.TestCase):
    def test_identifiability(self):
        r=rule_control(9200900); self.assertEqual(r['zero_error_distinct_rules'],1); self.assertEqual(r['accuracy'],1)
    def test_strict_shortcuts(self):
        x,y,env,test=dataset(9200900)
        for j,ix in enumerate(env): self.assertTrue(np.all(x[ix,0,j+2]==y[ix]))
        for j in range(3): self.assertEqual(np.mean(x[:,0,j+2]==y),.5)
    def test_seed_streams(self):
        self.assertTrue(np.array_equal(rng(9200900,1,1).integers(100,size=20),rng(9200900,1,1).integers(100,size=20)))
        self.assertFalse(np.array_equal(rng(9200900,1,1).integers(100,size=20),rng(9200900,1,2).integers(100,size=20)))
    def test_seed_separation(self):
        import json
        from common import ROOT
        c=json.loads((ROOT/'config_t1.json').read_text()); self.assertFalse(set(c['development_seeds'])&set(c['official_seeds']))
    def test_cpu(self):
        self.assertEqual(hardware_check()['device'],'cpu'); self.assertEqual(tensor([1]).device.type,'cpu')
    def test_state_accounting(self):
        m=Classifier('mlp'); before=state_bytes(m); self.assertEqual(before,sum(p.numel()*p.element_size() for p in m.parameters()))
        o=torch.optim.AdamW(m.parameters()); m(tensor(np.zeros((2,3,5)))).sum().backward(); o.step(); self.assertGreater(state_bytes(m,o),before*2)
    def test_permutation_models(self):
        torch.manual_seed(9200900); x=tensor(dataset(9200900)[0][:10])
        for kind in ('set','transformer'):
            m=Classifier(kind).eval(); self.assertTrue(torch.allclose(m(x),m(x[:,[2,0,1]]),atol=1e-5))
    def test_metrics_counterfactual(self):
        class Oracle(torch.nn.Module):
            def forward(self,x): return 20*(x[:,:,:2].prod(2).max(1).values*2-1)
        x,y,env,test=dataset(9200900); r=metrics(Oracle(),x,y,env,test)
        self.assertEqual(r['accuracy'],1); self.assertEqual(r['counterfactual_flip_rate'],0)
    def test_no_test_labels_in_training_call(self):
        import inspect,t1
        text=inspect.getsource(t1.train); self.assertNotIn('y[test',text); self.assertNotIn('accuracy\']',text)

if __name__=='__main__': unittest.main()
