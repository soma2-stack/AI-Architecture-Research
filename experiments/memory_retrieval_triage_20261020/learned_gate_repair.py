"""Fixed, answer-only sparse gate repair. See learned_gate_repair_protocol.md.
No grammar or boundaries in learned inference / training loss; boundary used
only by diagnostic evaluator. Original files are hashed and never written.
"""
import os, sys
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[k]='4'
sys.dont_write_bytecode=True
import copy, hashlib, json, time, platform
from pathlib import Path
import torch
from torch.nn import functional as F
from learned_address import LearnedMemoryRNN
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories, WRITE_START, VALUE_START
HERE=Path(__file__).resolve().parent
OUT=HERE/'learned_gate_repair_results.json'
WEIGHTS=HERE/'learned_gate_repair_weights.pt'
SEEDS=(17,29,43)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(x): OUT.write_text(json.dumps(x,indent=2),encoding='utf8')
def state(m): return {k:v.detach().cpu().clone() for k,v in m.state_dict().items()}
def model(seed,s):
    m=LearnedMemoryRNN(8,seed=seed)
    m.read_key=m.write_key
    m.load_state_dict(s,strict=True)
    for n,p in m.named_parameters(): p.requires_grad_(n.startswith('gate.'))
    return m

def prepare(m,ids):
    # Only the gate is trainable. These fixed features and GRU states have
    # exactly the original semantics. No WRITE IDs or event masks used here.
    with torch.no_grad():
        x=m.embedding(ids)
        prev=torch.cat((x.new_zeros(len(x),1,x.shape[-1]),x[:,:-1]),1)
        pairs=torch.cat((prev,x),-1)
        addr=F.normalize(m.keys,dim=-1)
        probs=F.softmax(8*(F.normalize(m.write_key(prev),dim=-1)@addr.T),-1)
        vals=torch.tanh(m.value(x))
        h=x.new_zeros(len(x),m.gru.hidden_size)
        for cur in x.unbind(1): h=m.gru(cur,h)
    return pairs,probs,vals,h,x[:,-1],addr

def query(m,h,bank,old,addr,freeze=False):
    b=len(h); s=m.slots
    cur=m.embedding(torch.arange(s)+14).repeat_interleave(b,0)
    hh=m.gru(cur,h.repeat(s,1))
    prev=old.repeat(s,1)
    gate=torch.sigmoid(m.gate(torch.cat((prev,cur),-1)))
    bb=bank.repeat(s,1,1)
    if not freeze:
        probs=F.softmax(8*(F.normalize(m.write_key(prev),dim=-1)@addr.T),-1)
        amount=gate[:,None,:]*probs[:,:,None]
        bb=bb*(1-amount)+amount*torch.tanh(m.value(cur))[:,None,:]
    attn=F.softmax(8*(F.normalize(m.read_key(cur),dim=-1)@addr.T),-1)
    found=(attn[:,:,None]*bb).sum(1)
    pred=m.head(torch.cat((hh,found),-1)).reshape(s,b,2).transpose(0,1)
    return pred,gate

def forward(m,ids,snapshot=None):
    pairs,probs,vals,h,old,addr=prepare(m,ids)
    gates=torch.sigmoid(m.gate(pairs)).squeeze(-1)
    bank=vals.new_zeros(len(ids),m.slots,m.memdim)
    body=None
    for j in range(ids.shape[1]):
        amount=gates[:,j,None,None]*probs[:,j,:,None]
        bank=bank*(1-amount)+amount*vals[:,j,None,:]
        if snapshot is not None and j==snapshot-1: body=bank.clone()
    pred,qgate=query(m,h,bank,old,addr)
    activity=(gates.sum()+qgate.sum())/(gates.numel()+qgate.numel())
    return pred,activity,(h,bank,old,addr,gates,body)

def parity(m,seed,tail,gradient=False):
    x,y=batch(8,tail+16,2,8100000000+seed+tail)
    fast,activity,_=forward(m,x)
    native=m(query_histories(x,8)).reshape(8,2,2).transpose(0,1)
    err=float((fast-native).abs().max())
    assert err<3e-5,(seed,tail,err)
    ans={'tail':tail,'max_logit_error':err,'predictions_identical':bool(torch.equal(fast.argmax(-1),native.argmax(-1)))}
    assert ans['predictions_identical']
    if gradient:
        a=F.cross_entropy(fast.reshape(-1,2),y.reshape(-1))
        b=F.cross_entropy(native.reshape(-1,2),y.reshape(-1))
        params=list(m.gate.parameters())
        ga=torch.autograd.grad(a,params)
        gb=torch.autograd.grad(b,params)
        gerr=max(float((u-v).abs().max()) for u,v in zip(ga,gb))
        assert gerr<1e-5,gerr
        ans['max_gradient_error']=gerr
    return ans

def train(seed,source,penalty):
    m=model(seed,source); opt=torch.optim.AdamW(m.gate.parameters(),lr=.003)
    trace=[]; w=time.monotonic(); c=time.process_time()
    for step in range(128):
        x,y=batch(8,80,12,6100000000+seed*1000003+step*8191)
        pred,activity,_=forward(m,x)
        ce=F.cross_entropy(pred.reshape(-1,2),y.reshape(-1))
        loss=ce+penalty*activity
        assert bool(torch.isfinite(loss))
        opt.zero_grad(set_to_none=True);loss.backward()
        torch.nn.utils.clip_grad_norm_(m.gate.parameters(),1.)
        opt.step()
        trace.append({'ce':float(ce.detach()),'activity':float(activity.detach()),'loss':float(loss.detach())})
    changed=[k for k,v in m.state_dict().items() if not torch.equal(v,source[k])]
    assert changed and all(k.startswith('gate.') for k in changed),changed
    return m,dict(wall_s=time.monotonic()-w,cpu_s=time.process_time()-c,updates=128,
                  histories=1536,query_examples=12288,history_tokens=147456,
                  penalty=penalty,changed_tensors=changed,trace=trace)

def score(pred,y,short):
    same=pred.eq(y); whole=same.all(1); base=short.eq(y).all(1)
    return dict(correct_bits=int(same.sum()),correct_records=int(whole.sum()),
                bit=float(same.float().mean()),whole=float(whole.float().mean()),
                body_correct_records=int(base.sum()),body_correct_retained=int((whole&base).sum()),
                recall_retention=float((whole&base).sum()/base.sum()) if base.any() else None,
                predictions=pred.tolist(),labels=y.tolist())

@torch.no_grad()
def evaluate(m,seed):
    rows=[]
    for tail in (256,1024,4080):
        t0=time.monotonic();c0=time.process_time(); chunks=[]
        allpred=[];alloracle=[];allshort=[];ally=[]
        gatesum=0.;gatecount=0;gatemax=0.;writesum=0.;writecount=0
        cos=[];drift=[];inputhash=hashlib.sha256();paritycheck=None
        for start in range(0,128,32):
            x,y=batch(8,tail+16,32,7100000000+seed*100003+start*677)
            inputhash.update(x.numpy().tobytes()); inputhash.update(y.numpy().tobytes())
            p,_,(h,bank,old,addr,gates,body)=forward(m,x,snapshot=32)
            po,_=query(m,h,body,old,addr)
            ps,_,_=forward(m,x[:,:32])
            allpred.append(p.argmax(-1));alloracle.append(po.argmax(-1));allshort.append(ps.argmax(-1));ally.append(y)
            idle=gates[:,32:];gatesum+=float(idle.sum());gatecount+=idle.numel();gatemax=max(gatemax,float(idle.max()))
            # Token semantics are used exclusively for post-hoc diagnostics.
            prev=x[:,:31];cur=x[:,1:32]
            marked=(prev>=WRITE_START)&(prev<WRITE_START+8)&(cur>=VALUE_START)&(cur<VALUE_START+2)
            active=gates[:,1:32][marked]
            writesum+=float(active.sum());writecount+=active.numel()
            cos.extend(F.cosine_similarity(bank.flatten(1),body.flatten(1),dim=1).tolist())
            drift.extend(((bank-body).flatten(1).norm(dim=1)/body.flatten(1).norm(dim=1).clamp_min(1e-12)).tolist())
        yy=torch.cat(ally); short=torch.cat(allshort)
        row={'tail_tokens':tail,'histories':128,'input_sha256':inputhash.hexdigest(),
             'normal':score(torch.cat(allpred),yy,short),'oracle_tail':score(torch.cat(alloracle),yy,short),
             'tail_gate_mean':gatesum/gatecount,'tail_gate_max':gatemax,'tail_gate_integral_per_history':gatesum/128,
             'intended_write_gate_mean':writesum/writecount,
             'bank_cosine_mean':sum(cos)/len(cos),'bank_relative_drift_mean':sum(drift)/len(drift),
             'wall_s':time.monotonic()-t0,'cpu_s':time.process_time()-c0}
        rows.append(row)
    return rows

def main():
    if OUT.exists() or WEIGHTS.exists(): raise FileExistsError('Preserve existing repair outputs')
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    assert not torch.cuda.is_available()
    originals={str(p.relative_to(HERE)):sha(p) for p in HERE.iterdir() if p.is_file() and not p.name.startswith('learned_gate_repair')}
    w=time.monotonic();c=time.process_time()
    saved=torch.load(HERE/'faded_guidance_weights.pt',map_location='cpu',weights_only=True)
    result={'protocol_file':'learned_gate_repair_protocol.md','protocol_sha256':sha(HERE/'learned_gate_repair_protocol.md'),
            'source_sha256':sha(Path(__file__)),'python':sys.version,'torch':torch.__version__,
            'cpu_threads':torch.get_num_threads(),'interop_threads':torch.get_num_interop_threads(),'gpu':False,
            'original_hashes':originals,'runs':[],'complete':False}
    weights={}
    for seed in SEEDS:
        source=saved[f'{seed}_8_linear_fade']
        base=model(seed,source)
        precheck=parity(base,seed,16,True)
        models={'original':base};training={}
        for arm,penalty in (('answer_only',0.),('sparse_gate',.1)):
            models[arm],training[arm]=train(seed,source,penalty)
            print('TRAIN',seed,arm,json.dumps({k:v for k,v in training[arm].items() if k!='trace'}),flush=True)
        for arm,m in models.items():
            assert all(p.device.type=='cpu' for p in m.parameters())
            row={'seed':seed,'arm':arm,'parameters':sum(p.numel() for p in m.parameters()),
                 'trainable_parameters':sum(p.numel() for p in m.parameters() if p.requires_grad),
                 'training':training.get(arm),'pretrain_parity':precheck,
                 'posttrain_long_parity':parity(m,seed,4080),'eval':evaluate(m,seed)}
            if arm=='sparse_gate':
                restored=copy.deepcopy(m);restored.gate.load_state_dict(base.gate.state_dict())
                assert all(torch.equal(v,source[k]) for k,v in restored.state_dict().items())
                row['restore_gate_matches_original_all_tensors']=True
                x,_=batch(8,4096,2,8500000000+seed)
                row['restored_logits_max_error']=float((restored(query_histories(x,8))-base(query_histories(x,8))).abs().max())
                assert row['restored_logits_max_error']==0.
            weights[f'{seed}_{arm}']=state(m)
            result['runs'].append(row);dump(result)
            print('EVAL',seed,arm,json.dumps([{'tail':r['tail_tokens'],'whole':r['normal']['whole'],
                 'oracle':r['oracle_tail']['whole'],'gate':r['tail_gate_mean']} for r in row['eval']]),flush=True)
        for i in range(3):
            assert len({r['eval'][i]['input_sha256'] for r in result['runs'] if r['seed']==seed})==1
    unchanged={n:sha(HERE/n)==v for n,v in originals.items()}
    assert all(unchanged.values()),unchanged
    result['original_files_unchanged']=unchanged
    torch.save(weights,WEIGHTS)
    result['weights_sha256']=sha(WEIGHTS)
    result['complete']=True
    result['elapsed_wall_s']=time.monotonic()-w;result['elapsed_cpu_s']=time.process_time()-c
    result['peak_working_set_bytes']=__import__('ctypes').c_size_t(0).value # replaced below using Windows API
    try:
        import ctypes
        from ctypes import wintypes
        class PMC(ctypes.Structure):
            _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in
              ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
               'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
        pm=PMC();pm.cb=ctypes.sizeof(pm)
        ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(pm),pm.cb)
        result['peak_working_set_bytes']=pm.PeakWorkingSetSize
    except Exception as e: result['memory_measurement_error']=repr(e)
    dump(result)
    print('COMPLETE',result['elapsed_wall_s'],result['elapsed_cpu_s'],flush=True)
if __name__=='__main__': main()
