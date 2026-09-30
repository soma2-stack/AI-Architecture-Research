"""CPU-only frozen recurrence and exact analytic Jacobians. No training code."""
import os
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[key]='1'
import atexit
import hashlib
import json
import shutil
import threading
import time
from pathlib import Path
import numpy as np
import psutil
import torch

ROOT=Path(__file__).resolve().parent
CFG=json.loads((ROOT/'config.json').read_text())
torch.set_num_threads(1);torch.set_num_interop_threads(1)
torch.set_default_dtype(torch.float64);torch.use_deterministic_algorithms(True)

def digest(t):return hashlib.sha256(t.detach().numpy().tobytes()).hexdigest()
def hardware():
    assert torch.version.cuda is None and torch.tensor(0.).device.type=='cpu'
    assert psutil.virtual_memory().available>CFG['minimum_free_ram_bytes']
    assert shutil.disk_usage(ROOT).free>CFG['minimum_free_disk_bytes']
    return {'torch':torch.__version__,'cuda_build':torch.version.cuda,'threads':torch.get_num_threads(),
            'free_ram':psutil.virtual_memory().available,'device':'cpu','dtype':'float64'}

class Meter:
    def __init__(self,job):
        self.job=job;self.done=False;self.process=psutil.Process();self.start=time.perf_counter()
        self.prior=sum(json.loads(l)['cpu_seconds'] for l in (ROOT/'cpu_ledger.jsonl').read_text().splitlines()) if (ROOT/'cpu_ledger.jsonl').exists() else 0.
        self.peak=self.process.memory_info().rss;self.stop=threading.Event()
        self.thread=threading.Thread(target=self.sample,daemon=True);self.thread.start();atexit.register(self.finish)
    def sample(self):
        while not self.stop.wait(.02):self.peak=max(self.peak,self.process.memory_info().rss)
    def check(self):
        assert self.prior+time.process_time()<CFG['measured_cpu_cap_seconds']-CFG['cpu_stop_margin_seconds'],'CPU budget stop'
        assert self.peak<CFG['rss_cap_bytes'],'RSS budget stop'
    def finish(self):
        if self.done:return
        self.done=True;self.stop.set();self.thread.join()
        self.peak=max(self.peak,self.process.memory_info().rss)
        row={'job':self.job,'cpu_seconds':time.process_time(),'wall_seconds':time.time()-self.process.create_time(),
             'post_import_wall_seconds':time.perf_counter()-self.start,'peak_rss_bytes':self.peak,'gpu_used':False}
        with (ROOT/'cpu_ledger.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        return row

class Model:
    def __init__(self,n,depth,family,interaction,seed,mode='stack_nonlinear',linear_shared=False):
        self.n,self.depth,self.N=n,depth,n*depth
        self.family,self.interaction,self.mode=family,interaction,mode
        self.linear_shared=linear_shared;self.groups=[];self.layer_groups=[];parts=[];offset=0
        rng=np.random.default_rng(np.random.SeedSequence([seed,1]))
        def add(name,array,layer):
            nonlocal offset
            array=np.asarray(array);size=array.size
            g={'name':name,'layer':layer,'start':offset,'end':offset+size,'shape':array.shape}
            parts.append(array.ravel());self.groups.append(g);offset+=size
            return g
        for l in range(depth):
            groups={}
            if family=='block':
                k=interaction;assert n%k==0
                if k==1:r=np.full((n,1,1),.35) if linear_shared else rng.uniform(.2,.5,(n,1,1))
                else:r=np.stack([np.linalg.qr(rng.normal(size=(k,k)))[0]*.4 for _ in range(n//k)])
                groups['R']=add('R',r,l)
            else:
                rank=interaction
                groups['D']=add('D',rng.uniform(.2,.5,n),l)
                if rank:
                    u=rng.normal(size=(n,rank));v=rng.normal(size=(n,rank))
                    scale=np.sqrt(.2/np.linalg.norm(u@v.T,2));u*=scale;v*=scale
                    groups['U']=add('U',u,l);groups['V']=add('V',v,l)
            groups['W']=add('W',rng.normal(size=(n,n))*.4/np.sqrt(n),l)
            groups['b']=add('b',rng.uniform(-.05,.05,n),l)
            self.layer_groups.append(groups)
        self.head=None;self.fixed=None
        if mode=='fixed_linear':self.fixed=torch.tensor(np.linalg.qr(rng.normal(size=(n,n)))[0]*.4)
        if mode in ('trainable_linear','nonlinear_trainable','feedback'):
            assert depth==1
            self.head=add('M',np.linalg.qr(rng.normal(size=(n,n)))[0]*.4,0)
        self.theta=torch.tensor(np.concatenate(parts),device='cpu');self.P=offset
    def value(self,g,theta):return theta[g['start']:g['end']].reshape(g['shape'])
    def recurrence(self,l,theta):
        groups=self.layer_groups[l]
        if self.family=='block':return torch.block_diag(*self.value(groups['R'],theta).unbind(0))
        result=torch.diag(self.value(groups['D'],theta))
        if self.interaction:result=result+self.value(groups['U'],theta)@self.value(groups['V'],theta).T
        return result
    def step(self,prev,x,theta):
        states=[]
        for l,groups in enumerate(self.layer_groups):
            hp=prev[l*self.n:(l+1)*self.n]
            if self.mode=='feedback':hp=torch.tanh(self.value(self.head,theta)@hp)
            z=x if l==0 else torch.tanh(states[-1])
            a=self.recurrence(l,theta)@hp+self.value(groups['W'],theta)@z+self.value(groups['b'],theta)
            states.append(a if self.linear_shared else torch.tanh(a))
        return torch.cat(states)
    def output(self,h,theta):
        top=h[-self.n:]
        if self.fixed is not None:return self.fixed@top
        if self.head is None:return top
        out=self.value(self.head,theta)@top
        return torch.tanh(out) if self.mode in ('nonlinear_trainable','feedback') else out
    def terminal(self,h,q,y):
        out=self.output(h,self.theta);error=q@out-y;v=error*q
        direct=torch.zeros(self.P);cot=torch.zeros(self.N)
        if self.head is not None:
            if self.mode in ('nonlinear_trainable','feedback'):v=v*(1-out**2)
            cot[-self.n:]=self.value(self.head,self.theta).T@v
            direct[self.head['start']:self.head['end']]=(v[:,None]*h[-self.n:][None,:]).reshape(-1)
        elif self.fixed is not None:cot[-self.n:]=self.fixed.T@v
        else:cot[-self.n:]=v
        return cot,direct

def data(seed,T,n,stream=2):
    rng=np.random.default_rng(np.random.SeedSequence([seed,stream]))
    x=torch.tensor(rng.uniform(-.3,.3,(T,n)),device='cpu')
    rng=np.random.default_rng(np.random.SeedSequence([seed,3]))
    q=torch.tensor(rng.normal(size=n),device='cpu');q=q/q.norm()
    y=torch.tensor(rng.uniform(.2,.4),device='cpu')
    return x,q,y

def partials(model,prev,x):
    n,N,P=model.n,model.N,model.P
    h=model.step(prev,x,model.theta);A=torch.zeros(N,N);B=torch.zeros(N,P);identity=torch.eye(n)
    for l,groups in enumerate(model.layer_groups):
        rows=slice(l*n,(l+1)*n);hp=prev[rows]
        gain=torch.ones(n) if model.linear_shared else 1-h[rows]**2
        R=model.recurrence(l,model.theta);rec=hp
        if model.mode=='feedback':
            rec=torch.tanh(model.value(model.head,model.theta)@hp)
            J=(1-rec**2)[:,None]*model.value(model.head,model.theta)
            A[rows,rows]=gain[:,None]*(R@J)
            K=gain[:,None]*R*(1-rec**2)[None,:]
            B[rows,model.head['start']:model.head['end']]=torch.einsum('ij,k->ijk',K,hp).reshape(n,n*n)
        else:A[rows,rows]=gain[:,None]*R
        if model.family=='block':
            k=model.interaction;g=groups['R']
            for block in range(n//k):
                for i in range(k):
                    row=block*k+i;start=g['start']+block*k*k+i*k
                    B[l*n+row,start:start+k]=gain[row]*rec[block*k:(block+1)*k]
        else:
            g=groups['D'];B[rows,g['start']:g['end']]=torch.diag(gain*rec)
            if model.interaction:
                u=model.value(groups['U'],model.theta);v=model.value(groups['V'],model.theta)
                g=groups['U'];B[rows,g['start']:g['end']]=torch.einsum('ij,a->ija',gain[:,None]*identity,v.T@rec).reshape(n,n*model.interaction)
                g=groups['V'];B[rows,g['start']:g['end']]=torch.einsum('ia,j->ija',gain[:,None]*u,rec).reshape(n,n*model.interaction)
        z=x if l==0 else torch.tanh(h[(l-1)*n:l*n])
        g=groups['W'];B[rows,g['start']:g['end']]=torch.einsum('ij,k->ijk',gain[:,None]*identity,z).reshape(n,n*n)
        g=groups['b'];B[rows,g['start']:g['end']]=gain[:,None]*identity
        if l:
            lower=slice((l-1)*n,l*n)
            J=gain[:,None]*model.value(groups['W'],model.theta)*(1-z**2)[None,:]
            A[rows]+=J@A[lower];B[rows]+=J@B[lower]
    # Conservative bound for rebinding overlap, contraction temporaries and row scratch.
    workspace=2*(N*N+N*P+5*n*n+3*n*P+8*N)
    return h,A,B,workspace

def graphs(model):
    n,N,P=model.n,model.N,model.P
    A=np.zeros((N,N),bool);B=np.zeros((N,P),bool)
    for l,groups in enumerate(model.layer_groups):
        rows=slice(l*n,(l+1)*n)
        if model.family=='block':
            k=model.interaction
            R=np.zeros((n,n),bool)
            for block in range(n//k):R[block*k:(block+1)*k,block*k:(block+1)*k]=True
            g=groups['R']
            for block in range(n//k):
                for i in range(k):
                    owner=l*n+block*k+i;start=g['start']+block*k*k+i*k
                    B[owner,start:start+k]=True
        else:
            R=np.ones((n,n),bool) if model.interaction else np.eye(n,dtype=bool)
            g=groups['D'];B[rows,g['start']:g['end']]=np.eye(n,dtype=bool)
            if model.interaction:
                g=groups['U']
                for i in range(n):B[l*n+i,g['start']+i*model.interaction:g['start']+(i+1)*model.interaction]=True
                g=groups['V'];B[rows,g['start']:g['end']]=True
        if model.mode=='feedback':R[:]=True;B[rows,model.head['start']:model.head['end']]=True
        A[rows,rows]=R
        g=groups['W']
        for i in range(n):B[l*n+i,g['start']+i*n:g['start']+(i+1)*n]=True
        g=groups['b'];B[rows,g['start']:g['end']]=np.eye(n,dtype=bool)
        if l:
            lower=slice((l-1)*n,l*n)
            A[rows]|=np.broadcast_to(A[lower].any(axis=0),(n,N))
            B[rows]|=np.broadcast_to(B[lower].any(axis=0),(n,P))
    K=B.copy()
    while True:
        new=K|((A.astype(np.int64)@K.astype(np.int64))>0)
        if np.array_equal(new,K):break
        K=new
    snap2=B|((A.astype(np.int64)@B.astype(np.int64))>0)
    local=np.zeros_like(B)
    for l,groups in enumerate(model.layer_groups):
        for g in groups.values():
            local[l*n:(l+1)*n,g['start']:g['end']]=K[l*n:(l+1)*n,g['start']:g['end']]
        if model.family=='block':
            k=model.interaction
            for col in range(P):
                owners=np.flatnonzero(B[l*n:(l+1)*n,col])
                if len(owners)==1:
                    block=owners[0]//k
                    for row in range(n):
                        if row//k!=block:local[l*n+row,col]=False
    if model.head is not None and model.mode=='feedback':local[:,:]|=B & (np.arange(P)[None,:]>=model.head['start'])
    return A,B,K,{'packed_exact':K,'SnAp1':B,'SnAp2':snap2,'local_block':local}

def metric(value,reference):
    delta=value-reference;norm=float(reference.norm());degenerate=norm<=CFG['degenerate_norm']
    return {'relative_error':float(delta.norm()/max(norm,1e-12)),'maximum_absolute_error':float(delta.abs().max()),
            'reference_norm':norm,'degenerate':degenerate,
            'cosine':None if degenerate or float(value.norm())<=1e-12 else float(torch.sum(value*reference)/(value.norm()*reference.norm()))}
def passes(m):return m['maximum_absolute_error']<CFG['degenerate_absolute_tolerance'] if m['degenerate'] else m['relative_error']<CFG['relative_gradient_tolerance']
def grouped(model,g,reference):
    result=[{'layer':z['layer']+1,'group':z['name'],**metric(g[z['start']:z['end']],reference[z['start']:z['end']])} for z in model.groups]
    for l in range(model.depth):
        idx=[i for z in model.groups if z['layer']==l for i in range(z['start'],z['end'])]
        result.append({'layer':l+1,'group':'ALL',**metric(g[idx],reference[idx])})
    return result

def inference(model,x):
    start=time.perf_counter();h=torch.zeros(model.N);trajectory=[]
    with torch.no_grad():
        for xt in x:h=model.step(h,xt,model.theta);trajectory.append(h)
    return torch.stack(trajectory),time.perf_counter()-start

def bptt(model,x,q,y):
    start=time.perf_counter();cpu=time.process_time();theta=model.theta.clone().requires_grad_(True);h=torch.zeros(model.N)
    aliases=(theta.untyped_storage().data_ptr(),x.untyped_storage().data_ptr());saved={};trajectory=[]
    def pack(t):
        ptr=t.untyped_storage().data_ptr();saved[ptr]=(t,t.untyped_storage().nbytes(),ptr in aliases);return t
    with torch.autograd.graph.saved_tensors_hooks(pack,lambda t:t):
        for xt in x:h=model.step(h,xt,theta);trajectory.append(h.detach())
        objective=.5*(q@model.output(h,theta)-y)**2
        before=time.perf_counter();g,=torch.autograd.grad(objective,theta);derivative=time.perf_counter()-before
    return {'gradient':g.detach(),'trajectory':torch.stack(trajectory),'seconds':time.perf_counter()-start,
            'cpu_seconds':time.process_time()-cpu,'derivative_seconds':derivative,
            'stored_derivative_scalars':sum(b for _,b,alias in saved.values() if not alias)//8,
            'derivative_bytes':sum(b for _,b,alias in saved.values() if not alias),
            'alias_bytes':sum(b for _,b,alias in saved.values() if alias),'index_bytes':0,
            'terminal_query_scalars':model.P+model.N,'scratch_scope':'autograd tape; transient allocator not enumerated; process RSS sampled'}

def rtrl(model,x,q,y,snapshot=False):
    start=time.perf_counter();cpu=time.process_time();h=torch.zeros(model.N);S=torch.zeros(model.N,model.P)
    trajectory=[];checkpoints={};derivative=0.;peak=0
    for t,xt in enumerate(x,1):
        before=time.perf_counter();h,A,B,workspace=partials(model,h,xt)
        peak=max(peak,3*S.numel()+workspace);S=A@S+B;del A,B
        derivative+=time.perf_counter()-before;trajectory.append(h)
        if snapshot and t in CFG['snapshot_steps']:checkpoints[t]=S.clone()
    before=time.perf_counter();cot,direct=model.terminal(h,q,y);g=cot@S+direct;derivative+=time.perf_counter()-before
    return {'gradient':g,'trajectory':torch.stack(trajectory),'S':S,'checkpoints':checkpoints,
            'seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'derivative_seconds':derivative,
            'stored_derivative_scalars':S.numel(),'derivative_bytes':8*S.numel(),'index_bytes':0,
            'peak_derivative_scratch_bound_scalars':peak,'terminal_query_scalars':model.N+2*model.P,
            'audit_snapshot_scalars':sum(v.numel() for v in checkpoints.values()),'scratch_scope':'analytic Jacobians and sensitivity-update temporaries, conservative bound'}

class Packed:
    def __init__(self,mask):
        patterns={}
        for col in range(mask.shape[1]):
            rows=tuple(np.flatnonzero(mask[:,col]))
            if rows:patterns.setdefault(rows,[]).append(col)
        self.parts=[(torch.tensor(rows,dtype=torch.int64),torch.tensor(cols,dtype=torch.int64),torch.zeros(len(rows),len(cols))) for rows,cols in patterns.items()]
    def update(self,A,B):
        new=[]
        for rows,cols,values in self.parts:
            block=A[rows[:,None],rows[None,:]]@values+B[rows[:,None],cols[None,:]]
            new.append((rows,cols,block))
        self.parts=new
    def reconstruct(self,N,P):
        result=torch.zeros(N,P)
        for rows,cols,values in self.parts:result[rows[:,None],cols[None,:]]=values
        return result
    def storage(self):return sum(v.numel() for _,_,v in self.parts),sum((r.numel()+c.numel())*8 for r,c,_ in self.parts)

def packed_run(model,x,q,y,mask):
    start=time.perf_counter();cpu=time.process_time();packed=Packed(mask);del mask
    h=torch.zeros(model.N);trajectory=[];derivative=0.
    values,index_bytes=packed.storage()
    for xt in x:
        before=time.perf_counter();h,A,B,workspace=partials(model,h,xt);packed.update(A,B);del A,B
        derivative+=time.perf_counter()-before;trajectory.append(h)
    before=time.perf_counter();S=packed.reconstruct(model.N,model.P);cot,direct=model.terminal(h,q,y);g=cot@S+direct
    derivative+=time.perf_counter()-before
    return {'gradient':g,'trajectory':torch.stack(trajectory),'S':S,'seconds':time.perf_counter()-start,
            'cpu_seconds':time.process_time()-cpu,'derivative_seconds':derivative,
            'stored_derivative_scalars':values,'index_bytes':index_bytes,'derivative_bytes':8*values+index_bytes,
            'terminal_query_scalars':model.N*model.P+model.N+2*model.P,
            'peak_derivative_scratch_bound_scalars':3*values+workspace+model.N*model.P,
            'scratch_scope':'full temporary A/B and terminal reconstruction counted; grouped sparse state only between steps'}

def shared_run(model,x,q,y):
    assert model.linear_shared and model.depth==1
    start=time.perf_counter();cpu=time.process_time();h=torch.zeros(model.n);ex=torch.zeros(model.n);eh=torch.zeros(model.n);eb=torch.zeros(())
    trajectory=[];derivative=0.
    for xt in x:
        prev=h;h=model.step(prev,xt,model.theta);before=time.perf_counter()
        ex=.35*ex+xt;eh=.35*eh+prev;eb=.35*eb+1;derivative+=time.perf_counter()-before;trajectory.append(h)
    before=time.perf_counter();S=torch.zeros(model.N,model.P);groups=model.layer_groups[0]
    for i in range(model.n):
        S[i,groups['R']['start']+i]=eh[i]
        S[i,groups['W']['start']+i*model.n:groups['W']['start']+(i+1)*model.n]=ex
        S[i,groups['b']['start']+i]=eb
    cot,direct=model.terminal(h,q,y);g=cot@S+direct;derivative+=time.perf_counter()-before
    return {'gradient':g,'trajectory':torch.stack(trajectory),'S':S,'seconds':time.perf_counter()-start,
            'cpu_seconds':time.process_time()-cpu,'derivative_seconds':derivative,
            'stored_derivative_scalars':2*model.n+1,'derivative_bytes':8*(2*model.n+1),'index_bytes':0,
            'terminal_query_scalars':model.N*model.P+model.N+2*model.P,
            'peak_derivative_scratch_bound_scalars':model.N*model.P+3*model.P+8*model.N,
            'scratch_scope':'shared factors; full reconstruction only at terminal audit, no retained history'}
