"""CPU-only primitives. No dependency in this workspace discovers a GPU."""
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
for name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[name] = '1'
import hashlib
import json
import subprocess
import threading
import time
from pathlib import Path
import numpy as np
import psutil
import torch
from torch import nn

ROOT = Path(__file__).resolve().parent
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
DEVICE = torch.device('cpu')

def rng(seed, target, stream):
    return np.random.Generator(np.random.PCG64DXSM(np.random.SeedSequence([seed,target,stream])))

def digest(*arrays):
    h = hashlib.sha256()
    for a in arrays:
        a = np.ascontiguousarray(a)
        h.update(str((a.shape,str(a.dtype))).encode()); h.update(a.tobytes())
    return h.hexdigest()

def tensor(a, dtype=torch.float32):
    return torch.as_tensor(a, dtype=dtype, device=DEVICE)

def append(path, record):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a',encoding='utf-8') as f:
        f.write(json.dumps(record,allow_nan=False)+'\n'); f.flush()

def state_bytes(model, optimizer=None):
    seen = set(); total = 0
    def add(t):
        nonlocal total
        key = (t.untyped_storage().data_ptr(),t.untyped_storage().nbytes())
        if key not in seen:
            seen.add(key); total += key[1]
    for t in list(model.parameters()) + list(model.buffers()): add(t)
    if optimizer:
        for state in optimizer.state.values():
            for t in state.values():
                if torch.is_tensor(t): add(t)
    return total

def hardware_check():
    info = {'torch':torch.__version__, 'device':str(DEVICE),
            'cuda_build':torch.version.cuda, 'cuda_visible_devices':os.environ['CUDA_VISIBLE_DEVICES'],
            'free_ram_bytes':psutil.virtual_memory().available,
            'free_disk_bytes':psutil.disk_usage(str(ROOT)).free,
            'workers':1, 'torch_threads':torch.get_num_threads(),
            'gpu_processes_launched_by_this_workspace':0}
    if torch.version.cuda is not None or str(DEVICE) != 'cpu':
        raise RuntimeError('CPU-only build required; do not initialize CUDA')
    if info['free_ram_bytes'] < 4*1024**3 or info['free_disk_bytes'] < 2*1024**3:
        raise RuntimeError('Insufficient resource headroom')
    return info

class Meter:
    def __init__(self, config, name):
        self.config=config; self.name=name; self.process=psutil.Process()
        self.start_cpu=0.; self.start_wall=time.time()-self.process.create_time()
        self.created=time.perf_counter()
        self.peak=self.process.memory_info().rss; self.stop=threading.Event()
        self.worker=threading.Thread(target=self._sample,daemon=True); self.worker.start()
    def _sample(self):
        while not self.stop.wait(.1):
            self.peak=max(self.peak,self.process.memory_info().rss)
    def check(self):
        prior=0
        ledger=ROOT/'cpu_ledger.jsonl'
        if ledger.exists():
            prior=sum(json.loads(x)['cpu_seconds'] for x in ledger.read_text().splitlines())
        cpu=time.process_time()-self.start_cpu
        if prior+cpu >= self.config['phase_cpu_cap_seconds']-5:
            raise RuntimeError('Phase CPU hard stop')
        if self.config['historical_cpu_seconds']+prior+cpu >= self.config['project_cpu_cap_seconds']-5:
            raise RuntimeError('Project CPU hard stop')
        if self.peak > self.config['ram_cap_bytes']: raise RuntimeError('RAM hard stop')
    def finish(self, status):
        self.stop.set(); self.worker.join()
        r={'job':self.name,'status':status,'cpu_seconds':time.process_time()-self.start_cpu,
           'wall_seconds':self.start_wall+time.perf_counter()-self.created,'peak_rss_bytes':self.peak,
           'device':'cpu','timestamp_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
        append(ROOT/'cpu_ledger.jsonl',r); return r

class Classifier(nn.Module):
    def __init__(self, kind, norm=False):
        super().__init__(); self.kind=kind
        def block(i,o):
            return [nn.Linear(i,o), *([nn.LayerNorm(o)] if norm else []),nn.ReLU()]
        if kind=='mlp': self.net=nn.Sequential(*block(15,32),*block(32,32),nn.Linear(32,1))
        elif kind=='set':
            self.enc=nn.Sequential(*block(5,32),*block(32,32)); self.out=nn.Linear(32,1)
        else:
            self.enc=nn.Linear(5,16)
            self.attn=nn.TransformerEncoderLayer(16,2,32,dropout=0,batch_first=True)
            self.out=nn.Linear(16,1)
    def forward(self,x):
        if self.kind=='mlp': return self.net(x.flatten(1)).flatten()
        h=self.enc(x)
        if self.kind=='transformer': h=self.attn(h)
        return self.out(h.mean(1)).flatten()

def provenance(config_path):
    return {'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'config_sha256':hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.py')},
            'hardware':hardware_check()}
