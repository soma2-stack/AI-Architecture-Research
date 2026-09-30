import inspect,json,unittest
from common import ROOT,torch,state_bytes
from t3 import labels,transition,data,infer,SequenceModel

class T3Tests(unittest.TestCase):
    def test_labels(self):
        self.assertEqual(labels('parity',[1,1,0,1]),[1,0,0,1])
        self.assertEqual(labels('addition',[99,0]),[8,1])
        self.assertEqual(labels('modsum',[4,4,4]),[4,3,2])
        self.assertNotEqual(labels('permutation',[1,2])[-1],labels('permutation',[2,1])[-1])
    def test_seeds_lengths(self):
        c=json.loads((ROOT/'config_t3.json').read_text()); a,b,h=data(c['development_seeds'][0],'parity',c); a2,b2,h2=data(c['development_seeds'][0],'parity',c)
        self.assertEqual(h,h2); self.assertTrue(all(4<=len(w)<=16 for w in a)); self.assertEqual(max(b),64)
        self.assertNotEqual(h['training_sha256'],h['test_sha256']); self.assertFalse(set(c['official_seeds'])&set(c['development_seeds']))
        self.assertGreaterEqual(h['minimum_transition_count'],10)
    def test_learner_interface(self):
        self.assertEqual(list(inspect.signature(infer).parameters),['train','outputs'])
        model=infer([[0,0],[1,0],[0,1],[1,1]],[[0,0],[1,1],[0,1],[1,0]])
        self.assertIsNotNone(model)
    def test_cpu_state(self):
        for kind in ['gru','lstm','transformer','relative','universal']:
            model=SequenceModel(kind); out=model(torch.zeros(2,4,dtype=torch.long,device='cpu'))
            self.assertEqual(tuple(out.shape),(2,4,10)); self.assertEqual(out.device.type,'cpu'); self.assertGreater(state_bytes(model),0)

if __name__=='__main__': unittest.main()
