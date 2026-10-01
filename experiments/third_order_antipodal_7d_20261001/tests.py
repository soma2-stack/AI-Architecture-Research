import sys,time,unittest,importlib.util
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import common as c
spec=importlib.util.spec_from_file_location('accepted_development_tests',c.ACCEPTED/'tests.py')
old=importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
class NewChecks(unittest.TestCase):
    def test_fixed_basis(self):
        for kind in ('top','skip'):
            ep,B,L,s,full=c.basis(kind,7)
            self.assertEqual(B.shape,(148,11)); self.assertEqual(L.shape,(7,24))
            self.assertEqual(len(s),7); self.assertEqual(len(full),9)
            self.assertTrue(c.np.all(s>0))
    def test_seed_reproducibility(self):
        self.assertTrue(c.np.array_equal(c.np.random.default_rng(271072).normal(size=7),c.np.random.default_rng(271072).normal(size=7)))
    def test_rounding_rules(self):
        for x in (.00001,.123456,.998765):
            q=c.Q(float(x)); d=c.Q(int(c.np.floor(x*2**20)),2**20)
            t=q*c.Q(51,50)*2**20; u=c.Q(-((-t.numerator)//t.denominator),2**20)
            self.assertLessEqual(d,q); self.assertGreaterEqual(u,q*c.Q(51,50))
    def test_accepted_kernel_hash(self):
        f=c.json.loads((c.ACCEPTED/'FROZEN.json').read_text())
        self.assertEqual(c.sha(c.ACCEPTED/'kernel.py'),f['local_sha256']['kernel.py'])
if __name__=='__main__':
    before={str(p):c.sha(p) for p in c.ACCEPTED.iterdir() if p.is_file()}
    suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(old.Checks),unittest.defaultTestLoader.loadTestsFromTestCase(NewChecks)])
    r=unittest.TextTestRunner(verbosity=2).run(suite)
    unchanged=all(c.sha(c.Path(p))==h for p,h in before.items())
    data={'tests':r.testsRun,'passed':r.wasSuccessful() and unchanged,'old_outputs_unchanged':unchanged,
          'failures':[(str(t),s) for t,s in r.failures+r.errors],
          'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
          'peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset}
    c.write('tests.json',data); sys.exit(0 if data['passed'] else 1)
