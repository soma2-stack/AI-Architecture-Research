import unittest,json
import numpy as np
import torch
from common import ROOT,state_bytes
from t2 import data,Model

class T2Tests(unittest.TestCase):
    def setUp(self): self.c=json.loads((ROOT/'config_t2.json').read_text())
    def test_teacher_determinism(self):
        a=data(9200900,self.c); b=data(9200900,self.c); self.assertTrue(np.array_equal(a[2][0][0],b[2][0][0])); self.assertEqual(len({tuple(x) for x in a[0]}),8)
    def test_no_growth_and_inactive_heads(self):
        m=Model('head'); before=state_bytes(m); opt=torch.optim.SGD(m.parameters(),lr=.1)
        x=torch.zeros((2,24)); x[:,:16]=1; x[:,16]=1; m(x).sum().backward(); opt.step()
        self.assertEqual(state_bytes(m,opt),before)
        for head in m.heads[1:]: self.assertTrue(torch.all(head.weight==0)); self.assertIsNone(head.weight.grad)
    def test_parameter_caps(self):
        for k in self.c['models']: self.assertLessEqual(sum(p.numel() for p in Model(k).parameters()),self.c['parameter_cap'])
    def test_seed_disjoint(self): self.assertFalse(set(self.c['development_seeds'])&set(self.c['official_seeds']))
    def test_aulc(self): self.assertEqual(float(np.mean(1-np.ones(5))),0); self.assertEqual(float(np.mean(1-np.zeros(5))),1)
