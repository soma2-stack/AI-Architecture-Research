"""New test output; preserves the prospective development test record."""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['OMP_NUM_THREADS']='1'
import json,threading,time,unittest
from pathlib import Path
import psutil
import tests
HERE=Path(__file__).resolve().parent
def main():
    start=time.perf_counter();cpu=time.process_time();peaks=[0];stopped=threading.Event()
    def monitor():
        p=psutil.Process()
        while not stopped.wait(.05):
            mem=p.memory_info();peaks[0]=max(peaks[0],getattr(mem,'peak_wset',mem.rss))
    worker=threading.Thread(target=monitor,daemon=True);worker.start()
    res=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(tests.Tests))
    stopped.set();worker.join()
    data={'tests':res.testsRun,'passed':res.wasSuccessful(),'failures':[str(x[0])+'\n'+x[1] for x in res.failures],
          'errors':[str(x[0])+'\n'+x[1] for x in res.errors],
          'resources':{'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-start,
                       'peak_ram_bytes':peaks[0],'gpu_seconds':0}}
    (HERE/'final_tests.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data))
    if not res.wasSuccessful():raise SystemExit(1)
if __name__=='__main__':main()
