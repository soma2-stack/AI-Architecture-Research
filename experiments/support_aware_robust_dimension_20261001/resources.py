import os
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import time,json,threading,shutil
import psutil
ROOT=Path(__file__).parent
CFG=json.loads((ROOT/'config.json').read_text())
class Monitor:
 def __init__(self,label):
  self.label=label;self.process=psutil.Process();self.start=time.perf_counter();self.peak=0
  self.prior=sum(json.loads(s)['cpu_seconds'] for s in (ROOT/'resources.jsonl').read_text().splitlines()) if (ROOT/'resources.jsonl').exists() else 0
  self.stop=threading.Event();self.thread=threading.Thread(target=self.sample,daemon=True);self.thread.start()
 def sample(self):
  while not self.stop.is_set():self.peak=max(self.peak,self.process.memory_info().rss);self.stop.wait(.5)
 def check(self):
  assert self.prior+time.process_time()<CFG['max_cpu_seconds'],'CPU budget exhausted'
  assert self.process.memory_info().rss<CFG['rss_cap_bytes']
  assert psutil.virtual_memory().available>4*2**30 and shutil.disk_usage(ROOT).free>2*2**30
 def finish(self):
  self.stop.set();self.thread.join();m=self.process.memory_info()
  row={'label':self.label,'cpu_seconds':time.process_time(),'wall_seconds':time.perf_counter()-self.start,'peak_ram_bytes':max(self.peak,m.rss,getattr(m,'peak_wset',m.rss)),'workers':1,'gpu_seconds':0,'gpu_used':False,'peak_own_VRAM_bytes':0,'gpu_temperature_c':None}
  with (ROOT/'resources.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print('RESOURCE',json.dumps(row),flush=True)
