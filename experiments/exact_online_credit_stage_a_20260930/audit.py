"""Frozen-parameter CPU derivative audit; no optimizer or training code."""
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
for name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[name] = '1'
import atexit
import hashlib
import json
import shutil
import subprocess
import threading
import time
from pathlib import Path
import numpy as np
import psutil
import torch

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / 'config.json').read_text())
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.use_deterministic_algorithms(True)
torch.set_default_dtype(torch.float64)

def digest(t):
    return hashlib.sha256(t.detach().numpy().tobytes()).hexdigest()

def hardware():
    assert torch.version.cuda is None, 'Require installed CPU-only PyTorch'
    assert torch.tensor(0.).device.type == 'cpu'
    assert psutil.virtual_memory().available >= CFG['minimum_available_ram_bytes']
    assert shutil.disk_usage(ROOT).free >= CFG['minimum_free_disk_bytes']
    return {'torch': torch.__version__, 'cuda_build': torch.version.cuda,
            'device': 'cpu', 'threads': torch.get_num_threads(),
            'available_ram': psutil.virtual_memory().available}

class Meter:
    def __init__(self, job):
        self.job = job
        self.prior = sum(json.loads(l)['cpu_seconds'] for l in
                         (ROOT/'cpu_ledger.jsonl').read_text().splitlines()) if (ROOT/'cpu_ledger.jsonl').exists() else 0.
        self.start = time.perf_counter()
        self.peak = psutil.Process().memory_info().rss
        self.done = False
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self.sample, daemon=True)
        self.thread.start()
        atexit.register(self.finish)
    def sample(self):
        while not self.stop.wait(.02):
            self.peak = max(self.peak, psutil.Process().memory_info().rss)
    def check(self):
        assert self.prior + time.process_time() < CFG['measured_cpu_cap_seconds']-CFG['stop_margin_seconds'], 'CPU budget stop'
        assert self.peak < CFG['rss_cap_bytes'], 'RSS budget stop'
    def finish(self):
        if self.done:
            return
        self.done = True
        self.stop.set()
        self.thread.join()
        self.peak = max(self.peak, psutil.Process().memory_info().rss)
        record = {'job': self.job, 'cpu_seconds': time.process_time(),
                  'wall_seconds': time.perf_counter()-self.start, 'peak_rss_bytes': self.peak,
                  'gpu_used': False, 'cuda_build': torch.version.cuda}
        with (ROOT/'cpu_ledger.jsonl').open('a') as f:
            f.write(json.dumps(record)+'\n')
        return record

class Model:
    def __init__(self, kind, depth, seed, n=8):
        self.kind, self.depth, self.n = kind, depth, n
        self.N = depth*n
        rng = np.random.default_rng(np.random.SeedSequence([seed, 1]))
        self.groups = []
        parts = []
        offset = 0
        for layer in range(depth):
            if kind == 'dense':
                r, _ = np.linalg.qr(rng.normal(size=(n,n)))
                r *= .4
            else:
                r = rng.uniform(.2,.5,n)
            w = rng.normal(size=(n,n))*.4/np.sqrt(n)
            b = rng.uniform(-.05,.05,n)
            for name, a in [('R' if kind=='dense' else 'r',r),('W',w),('b',b)]:
                size = a.size
                self.groups.append({'layer':layer,'name':name,'start':offset,'end':offset+size,'shape':a.shape})
                parts.append(a.ravel())
                offset += size
        self.theta = torch.tensor(np.concatenate(parts), device='cpu')
        self.P = offset
    def unpack(self, theta):
        groups = [theta[g['start']:g['end']].reshape(g['shape']) for g in self.groups]
        return [groups[i:i+3] for i in range(0,len(groups),3)]
    def step(self, prev, x, theta):
        states=[]
        for l,(r,w,b) in enumerate(self.unpack(theta)):
            z=x if l==0 else torch.tanh(states[-1])
            hp=prev[l*self.n:(l+1)*self.n]
            recurrent=r@hp if self.kind=='dense' else r*hp
            states.append(torch.tanh(recurrent+w@z+b))
        return torch.cat(states)

def data(seed,T,n):
    rng=np.random.default_rng(np.random.SeedSequence([seed,2]))
    x=torch.tensor(rng.uniform(-.3,.3,(T,n)),device='cpu')
    q=torch.tensor(rng.normal(size=n),device='cpu'); q=q/q.norm()
    y=torch.tensor(rng.uniform(.2,.4),device='cpu')
    return x,q,y

def loss(h,q,y,n):
    return .5*(q@h[-n:]-y)**2

def inference(model,x):
    start=time.perf_counter()
    with torch.no_grad():
        h=torch.zeros(model.N)
        trajectory=[]
        for xt in x:
            h=model.step(h,xt,model.theta)
            trajectory.append(h)
    return torch.stack(trajectory), time.perf_counter()-start

def bptt(model,x,q,y):
    start=time.perf_counter()
    theta=model.theta.clone().requires_grad_(True)
    parameter_ptr=theta.untyped_storage().data_ptr()
    input_ptr=x.untyped_storage().data_ptr()
    saved={}
    def pack(t):
        ptr=t.untyped_storage().data_ptr()
        # Retain references solely for the storage audit; no cloned data.
        saved[ptr]=(t,t.untyped_storage().nbytes(),ptr in (parameter_ptr,input_ptr))
        return t
    with torch.autograd.graph.saved_tensors_hooks(pack,lambda t:t):
        h=torch.zeros(model.N); traj=[]
        for xt in x:
            h=model.step(h,xt,theta); traj.append(h.detach())
        objective=loss(h,q,y,model.n)
        before=time.perf_counter()
        g,=torch.autograd.grad(objective,theta)
        derivative_seconds=time.perf_counter()-before
    storage=sum(b for _,b,alias in saved.values() if not alias)
    aliases=sum(b for _,b,alias in saved.values() if alias)
    return {'gradient':g.detach(),'trajectory':torch.stack(traj),
            'seconds':time.perf_counter()-start,'derivative_seconds':derivative_seconds,
            'persistent_derivative_scalars':storage//8,'auxiliary_derivative_bytes':storage,
            'saved_parameter_input_alias_bytes':aliases,'storage_kind':'autograd saved tape unique storage',
            'terminal_gradient_scalars':model.P,
            'peak_explicit_derivative_scalars':storage//8+model.P,
            'peak_inventory_scope':'saved tape plus returned gradient; autograd transient allocations reflected in process RSS, not a full allocator census'}

def jacobians(model,prev,x):
    """Analytic within-time recursion; independent of autograd."""
    n,N,P=model.n,model.N,model.P
    h=model.step(prev,x,model.theta)
    A=torch.zeros(N,N); B=torch.zeros(N,P)
    max_workspace=0
    for l,(r,w,b) in enumerate(model.unpack(model.theta)):
        rows=slice(l*n,(l+1)*n)
        hl=h[rows]; d=1-hl**2
        hp=prev[rows]
        z=x if l==0 else torch.tanh(h[(l-1)*n:l*n])
        recurrence=r if model.kind=='dense' else torch.diag(r)
        A[rows,rows]=d[:,None]*recurrence
        direct=torch.zeros(n,P)
        rg,wg,bg=model.groups[l*3:l*3+3]
        if model.kind=='dense':
            for i in range(n):
                direct[i,rg['start']+i*n:rg['start']+(i+1)*n]=d[i]*hp
        else:
            for i in range(n): direct[i,rg['start']+i]=d[i]*hp[i]
        for i in range(n):
            direct[i,wg['start']+i*n:wg['start']+(i+1)*n]=d[i]*z
            direct[i,bg['start']+i]=d[i]
        B[rows]=direct
        # Include full chain through lower layers computed at this same time.
        if l:
            J=d[:,None]*w*(1-z**2)[None,:]
            lower=slice((l-1)*n,l*n)
            A[rows]+=J@A[lower]
            B[rows]+=J@B[lower]
        else: J=torch.empty(0)
        # Inventory: global A/B, direct n*P, D vector, recurrence matrix,
        # current spatial J and the largest matmul result n*max(N,P).
        max_workspace=max(max_workspace,A.numel()+B.numel()+direct.numel()+d.numel()+recurrence.numel()+J.numel()+n*max(N,P))
    return h,A,B,max_workspace

def rtrl(model,x,q,y):
    start=time.perf_counter(); derivative_seconds=0.
    M=torch.zeros(model.N,model.P); h=torch.zeros(model.N); traj=[]
    peak=0
    for xt in x:
        before=time.perf_counter()
        h,A,B,workspace=jacobians(model,h,xt)
        # During addition, old M, matmul result and new M can coexist.
        peak=max(peak,3*M.numel()+workspace)
        M=A@M+B
        derivative_seconds+=time.perf_counter()-before
        traj.append(h)
    before=time.perf_counter()
    cotangent=torch.zeros(model.N)
    cotangent[-model.n:]=(q@h[-model.n:]-y)*q
    g=cotangent@M
    peak=max(peak,M.numel()+cotangent.numel()+g.numel())
    derivative_seconds+=time.perf_counter()-before
    return {'gradient':g,'trajectory':torch.stack(traj),'sensitivity':M,
            'seconds':time.perf_counter()-start,'derivative_seconds':derivative_seconds,
            'persistent_derivative_scalars':M.numel(),'auxiliary_derivative_bytes':8*M.numel(),
            'peak_explicit_derivative_scalars':peak,
            'terminal_gradient_scalars':model.P,
            'storage_kind':'full online sensitivity; analytic scratch inventory upper bound',
            'n_times_P':model.n*model.P,'N_times_P':model.N*model.P}

def local(model,x,q,y):
    assert model.kind=='independent'
    start=time.perf_counter(); derivative_seconds=0.
    E=[torch.zeros(model.n,model.n+2) for _ in range(model.depth)]
    h=torch.zeros(model.N); traj=[]
    for xt in x:
        prev=h; h=model.step(prev,xt,model.theta)
        before=time.perf_counter()
        for l,(r,w,b) in enumerate(model.unpack(model.theta)):
            rows=slice(l*model.n,(l+1)*model.n)
            z=xt if l==0 else torch.tanh(h[(l-1)*model.n:l*model.n])
            direct=torch.cat([prev[rows,None],z.expand(model.n,-1),torch.ones(model.n,1)],dim=1)
            E[l]=(1-h[rows]**2)[:,None]*(r[:,None]*E[l]+direct)
        derivative_seconds+=time.perf_counter()-before
        traj.append(h)
    before=time.perf_counter()
    signals=[None]*model.depth
    signals[-1]=(q@h[-model.n:]-y)*q
    parts=[None]*model.depth
    for l in reversed(range(model.depth)):
        row_grad=signals[l][:,None]*E[l]
        parts[l]=torch.cat([row_grad[:,0],row_grad[:,1:-1].reshape(-1),row_grad[:,-1]])
        if l:
            w=model.unpack(model.theta)[l][1]
            hl=h[l*model.n:(l+1)*model.n]
            lower=h[(l-1)*model.n:l*model.n]
            signals[l-1]=(1-torch.tanh(lower)**2)*(w.T@((1-hl**2)*signals[l]))
    g=torch.cat(parts)
    derivative_seconds+=time.perf_counter()-before
    entries=sum(e.numel() for e in E)
    # Conservative scratch bound: old+new row buffers, multiply/add temporaries,
    # local direct, scalar vectors, all learning signals and terminal gradient copies.
    peak=entries+5*model.n*(model.n+2)+6*model.N+3*model.P
    return {'gradient':g,'trajectory':torch.stack(traj),'seconds':time.perf_counter()-start,
            'derivative_seconds':derivative_seconds,'persistent_derivative_scalars':entries,
            'auxiliary_derivative_bytes':entries*8,'peak_explicit_derivative_scalars':peak,
            'terminal_gradient_scalars':model.P,
            'storage_kind':'row-local eligibility; scratch inventory upper bound'}

def metric(g,ref):
    norm=float(ref.norm()); delta=g-ref
    degenerate=norm<=CFG['degenerate_norm']
    return {'relative_error':float(delta.norm()/max(norm,1e-12)),
            'maximum_absolute_error':float(delta.abs().max()),'gradient_norm':norm,
            'cosine_similarity':None if degenerate or float(g.norm())<=1e-12 else float(torch.dot(g,ref)/(g.norm()*ref.norm())),
            'numerically_degenerate':degenerate}

def passes(m):
    return m['maximum_absolute_error']<CFG['absolute_tolerance_degenerate'] if m['numerically_degenerate'] else m['relative_error']<CFG['relative_tolerance']

def grouped(model,g,ref):
    out=[]
    for group in model.groups:
        out.append({'layer':group['layer']+1,'parameter':group['name'],
                    **metric(g[group['start']:group['end']],ref[group['start']:group['end']])})
    for l in range(model.depth):
        start=model.groups[3*l]['start']; end=model.groups[3*l+2]['end']
        out.append({'layer':l+1,'parameter':'ALL',**metric(g[start:end],ref[start:end])})
    return out

def support(model,M):
    blocks=[]
    for sl in range(model.depth):
        for pl in range(model.depth):
            start=model.groups[pl*3]['start']; end=model.groups[pl*3+2]['end']
            block=M[sl*model.n:(sl+1)*model.n,start:end]
            blocks.append({'state_layer':sl+1,'parameter_layer':pl+1,
                           'nonzero_exact':int(torch.count_nonzero(block)),
                           'nonzero_above_threshold':int(torch.count_nonzero(block.abs()>CFG['support_threshold'])),
                           'size':block.numel()})
    return {'exact_nonzero':int(torch.count_nonzero(M)),
            'nonzero_above_threshold':int(torch.count_nonzero(M.abs()>CFG['support_threshold'])),
            'fraction_above_threshold':float((M.abs()>CFG['support_threshold']).double().mean()),'blocks':blocks}

def run():
    meter=Meter('official Stage-A sweep'); info=hardware()
    path=ROOT/'raw.jsonl'
    assert not path.exists(), 'Do not overwrite an existing official run'
    provenance={'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                'hardware':info,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.iterdir() if p.suffix in ('.py','.json','.md') and p.name not in ('provenance.json',)}}
    (ROOT/'provenance.json').write_text(json.dumps(provenance,indent=2))
    try:
        for kind in ('dense','independent'):
            for depth in CFG['depths']:
                for T in CFG['horizons']:
                    for seed in CFG['seeds']:
                        meter.check()
                        model=Model(kind,depth,seed); x,q,y=data(seed,T,model.n)
                        before=digest(model.theta)
                        trajectory,infer_seconds=inference(model,x)
                        inference_times=[infer_seconds]+[inference(model,x)[1] for _ in range(CFG['timing_repeats']-1)]
                        inference_seconds=float(np.median(inference_times))
                        assert float(trajectory.abs().max())<CFG['maximum_absolute_state']
                        assert abs(float(q@trajectory[-1,-model.n:]-y))>CFG['minimum_terminal_error']
                        reference=bptt(model,x,q,y)
                        methods=[('G0',bptt),('G1',rtrl)]
                        if kind=='independent': methods.append(('G2' if depth==1 else 'G3',local))
                        for name,fn in methods:
                            times=[]; derivative_times=[]
                            for repeat in range(CFG['timing_repeats']):
                                meter.check()
                                result=fn(model,x,q,y)
                                assert digest(model.theta)==before
                                assert torch.isfinite(result['gradient']).all()
                                assert result['gradient'].device.type=='cpu'
                                discrepancy=float((result['trajectory']-trajectory).abs().max())
                                assert discrepancy<=CFG['trajectory_absolute_tolerance']
                                groups=grouped(model,result['gradient'],reference['gradient'])
                                if name in ('G0','G1','G2'): assert all(passes(g) for g in groups), 'Exactness validity failure'
                                times.append(result['seconds']); derivative_times.append(result['derivative_seconds'])
                            record={'model':'M1' if kind=='dense' else 'M2' if depth==1 else 'M3',
                                    'kind':kind,'method':name,'depth':depth,'n':model.n,'T':T,'seed':seed,
                                    'P':model.P,'recurrent_state_width':model.N,'parameter_hash':before,
                                    'input_hash':digest(x),'q_hash':digest(q),'y':float(y),
                                    'trajectory_max_error':discrepancy,'maximum_absolute_state':float(trajectory.abs().max()),
                                    'groups':groups,'inference_seconds':inference_seconds,
                                    'seconds':float(np.median(times)),'all_repeat_seconds':times,
                                    'derivative_seconds':float(np.median(derivative_times)),
                                    'inference_seconds_per_step':inference_seconds/T,
                                    'gradient_seconds_per_step':float(np.median(derivative_times))/T,
                                    'total_to_inference_ratio':float(np.median(times))/inference_seconds,
                                    'gradient_to_inference_ratio':float(np.median(derivative_times))/inference_seconds,
                                    'audit_trajectory_bytes':8*T*model.N,'process_peak_rss_bytes':meter.peak,
                                    **{k:v for k,v in result.items() if k not in ('gradient','trajectory','sensitivity','seconds','derivative_seconds')}}
                            if name=='G1': record['sensitivity_support']=support(model,result['sensitivity'])
                            with path.open('a') as f: f.write(json.dumps(record)+'\n')
                        print(f'{kind} depth={depth} T={T} seed={seed}: exact gates passed',flush=True)
        (ROOT/'status.json').write_text(json.dumps({'valid':True,'complete':True,'cases':60,'method_records':150},indent=2))
    except Exception as e:
        (ROOT/'status.json').write_text(json.dumps({'valid':False,'complete':False,'reason':repr(e)},indent=2))
        raise
    finally: meter.finish()

if __name__=='__main__': run()
