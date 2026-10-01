import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import time, json, threading, subprocess
from pathlib import Path
import psutil
ROOT=Path(__file__).parent;CFG=json.loads((ROOT/'config.json').read_text())
class Monitor:
    def __init__(self,label,gpu=False):
        self.label=label;self.gpu=gpu;self.start=time.perf_counter();self.process=psutil.Process();self.stop=threading.Event()
        self.peak_ram=0;self.peak_vram=0;self.peak_temperature=0;self.peak_global_vram=0;self.samples=[];self.error=None
        self.prior=[json.loads(x) for x in (ROOT/'resources.jsonl').read_text().splitlines()] if (ROOT/'resources.jsonl').exists() else []
        self.thread=threading.Thread(target=self.sample,daemon=True);self.thread.start()
    def sample(self):
        while not self.stop.is_set():
            self.peak_ram=max(self.peak_ram,self.process.memory_info().rss)
            if self.gpu:
                try:
                    output=subprocess.check_output(['nvidia-smi','--query-gpu=memory.used,temperature.gpu,utilization.gpu','--format=csv,noheader,nounits'],text=True)
                    vram,temp,util=map(int,output.strip().split(','));self.peak_global_vram=max(self.peak_global_vram,vram*2**20);self.peak_temperature=max(self.peak_temperature,temp)
                    self.samples.append({'wall':time.perf_counter()-self.start,'global_vram_MiB':vram,'temperature_c':temp,'utilization':util})
                    if temp>86:self.error='GPU temperature exceeds86C'
                except Exception as error:self.error='Hardware telemetry failed: '+str(error)
            self.stop.wait(2)
    def check(self):
        assert self.error is None,self.error
        assert self.peak_ram<CFG['rss_cap_bytes'],'RAM safety stop'
        assert psutil.virtual_memory().available>4*2**30,'System RAM headroom stop'
        assert sum(x['cpu_seconds'] for x in self.prior)+time.process_time()<CFG['max_cpu_seconds'],'CPU budget stop'
        if self.gpu:
            import cupy as cp
            self.peak_vram=max(self.peak_vram,cp.get_default_memory_pool().total_bytes())
            assert self.peak_vram<CFG['device_allocation_cap_bytes'],'Device allocation safety stop'
            assert sum(x.get('gpu_wall_upper_seconds',0) for x in self.prior)+time.perf_counter()-self.start<CFG['max_gpu_wall_seconds'],'GPU wall budget stop'
    def finish(self):
        self.stop.set();self.thread.join();m=self.process.memory_info()
        row={'label':self.label,'cpu_seconds':time.process_time(),'wall_seconds':time.perf_counter()-self.start,
             'peak_ram_bytes':max(self.peak_ram,m.rss,getattr(m,'peak_wset',m.rss)),
             'gpu_wall_upper_seconds':time.perf_counter()-self.start if self.gpu else 0,
             'peak_our_gpu_pool_bytes':self.peak_vram,'peak_global_vram_bytes':self.peak_global_vram,'peak_gpu_temperature_c':self.peak_temperature,
             'workers':1,'gpu_used':self.gpu}
        with (ROOT/'resources.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
        if self.samples:(ROOT/('telemetry_'+self.label.replace(' ','_')+'.json')).write_text(json.dumps(self.samples,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(row),flush=True);return row
