import json,inspect,unittest
from common import ROOT,np,torch,hardware_check,state_bytes
from data import Generator,training_batches
from models import build
from train import curve_metrics,kill_gate,run

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads((ROOT/'config.json').read_text()); cls.seed=cls.c['development_seeds'][0]; cls.g=Generator(cls.seed,cls.c)
    def test_determinism(self):
        other=Generator(self.seed,self.c); self.assertEqual(other.hash,self.g.hash)
        np.testing.assert_array_equal(other.phase('B')[0],self.g.phase('B')[0])
    def test_seed_isolation(self):
        self.assertFalse(set(self.c['development_seeds'])&set(self.c['official_seeds']))
        self.assertNotEqual(Generator(self.seed+1,self.c).hash,self.g.hash)
    def test_correlations_labels_shape(self):
        for p,target in self.c['phase_agreement'].items():
            x,y,c,s=self.g.phase(p); self.assertEqual(x.shape,(8192,64)); np.testing.assert_array_equal(y,(c+1)/2)
            self.assertLessEqual(abs(np.mean(s==c)-target),1/8192)
    def test_variance(self):
        np.testing.assert_allclose(self.g.calibration_covariance,np.eye(64),atol=2e-6)
    def test_identifiable_and_linear_shortcut(self):
        for p in ['A','B','C']:
            x,y,c,s=self.g.phase(p); z,ss=self.g.inverse(x)
            np.testing.assert_array_equal(np.sign(z[:,0]),c); np.testing.assert_allclose(ss,s,atol=2e-6)
    def test_no_ids(self):
        m=build(self.seed,'mlp2','continuous',self.c); self.assertEqual(m.blocks[0][0].in_features,64)
        self.assertEqual(list(inspect.signature(m.forward).parameters),['x'])
    def test_cpu(self):
        self.assertEqual(hardware_check()['cuda_build'],None); m=build(self.seed,'mlp2','continuous',self.c)
        self.assertTrue(all(p.device.type=='cpu' for p in m.parameters())); self.assertGreater(state_bytes(m),0)
    def test_nested_optimizer_state_accounting(self):
        m=build(self.seed,'logistic','continuous',self.c); o=torch.optim.LBFGS(m.parameters(),max_iter=1)
        base=state_bytes(m,o); p=next(m.parameters()); o.state[p]['old_dirs']=[torch.ones(17,device='cpu')]
        self.assertEqual(state_bytes(m,o)-base,17*4)
    def test_matching(self):
        a=training_batches(self.seed,'B',1000,256,8192); b=training_batches(self.seed,'B',1000,256,8192)
        np.testing.assert_array_equal(a,b); self.assertNotEqual(a[:10].tolist(),training_batches(self.seed,'C',1000,256,8192)[:10].tolist())
        a=build(self.seed,'mlp2','continuous',self.c); b=build(self.seed,'mlp2','optimizer_reset',self.c)
        self.assertTrue(all(torch.equal(v,b.state_dict()[k]) for k,v in a.state_dict().items()))
    def test_curve_metric(self):
        r=curve_metrics([{'step':0,'cf_accuracy':.5},{'step':100,'cf_accuracy':.96}],256)
        self.assertAlmostEqual(r['correction_accuracy_auc'],.73); self.assertEqual(r['samples_to_exceed_95_upper'],25600)
    def test_strict_kill_threshold(self):
        c=self.c.copy(); c['kill_seeds']=4
        scratch={'cf_accuracy':1.0}; phases={p:({'cf_accuracy':.99,'train_'+p+'_accuracy':.99},scratch) for p in ['B','C']}
        yes,checks=kill_gate({i:phases for i in range(4)},c); self.assertTrue(yes)
        phases={p:({'cf_accuracy':.97,'train_'+p+'_accuracy':.99},scratch) for p in ['B','C']}
        self.assertFalse(kill_gate({i:phases for i in range(5)},c)[0])
    def test_no_eval_in_selection_or_training(self):
        text=inspect.getsource(run); self.assertNotIn("loss=",text); self.assertNotIn("cf_accuracy']>=",text)
        a,b=self.g.probes(); self.assertFalse(np.array_equal(a[0][:len(b[0])],b[0]))
    def test_scratch_gate(self):
        p=ROOT/'development_validity.json'
        if not p.exists(): self.skipTest('Development fitting precedes mandatory final unit validation')
        r=json.loads(p.read_text()); self.assertTrue(r['passed'])

if __name__=='__main__': unittest.main()
