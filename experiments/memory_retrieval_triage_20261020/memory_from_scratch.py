"""Fixed-budget, answer-only scratch experiment. See protocol. No architecture change.
Task semantics appear ONLY in generators and explicitly named diagnostics.
The neural features/encode/read functions have no event parser or write mask.
"""
import os,sys
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='4'
sys.dont_write_bytecode=True
import argparse,copy,ctypes,hashlib,json,random,time
from pathlib import Path
import torch
from torch.nn import functional as F
from learned_address import LearnedMemoryRNN
from run import batch as legacy_batch
from prototypes.rnn_llm_architecture.capacity_010 import replay,query_histories
HERE=Path(__file__).resolve().parent
PREFIX='memory_from_scratch'
SEEDS=(101,211,307)
ARMS=('original_policy','gate_repair_policy')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(s):
    h=hashlib.sha256()
    for k,v in sorted(s.items()):h.update(k.encode());h.update(v.detach().numpy().tobytes())
    return h.hexdigest()
def state(m):return {k:v.detach().clone() for k,v in m.state_dict().items()}
def save(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf8')
def factory(seed):
    m=LearnedMemoryRNN(8,seed=seed);m.read_key=m.write_key
    return m

def peak_memory():
    from ctypes import wintypes
    class PMC(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in
          ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
           'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
    api=ctypes.windll.kernel32;api.GetCurrentProcess.restype=wintypes.HANDLE
    gm=ctypes.windll.psapi.GetProcessMemoryInfo
    gm.argtypes=[wintypes.HANDLE,ctypes.POINTER(PMC),wintypes.DWORD]
    pm=PMC();pm.cb=ctypes.sizeof(pm)
    assert gm(api.GetCurrentProcess(),ctypes.byref(pm),pm.cb)
    return pm.PeakWorkingSetSize

def idle(n,t,g,ood):
    # All token identities occur in both domains. Only pure-filler bigrams differ.
    out=torch.empty(n,t,dtype=torch.long);prev=torch.full((n,),-1)
    for j in range(t):
        parity=torch.randint(2,(n,),generator=g)
        sameprev=(prev>=22)&(prev<30)
        inherited=(prev-22)%2
        if ood:inherited=1-inherited
        parity=torch.where(sameprev,inherited,parity)
        filler=22+2*torch.randint(4,(n,),generator=g)+parity
        value=10+torch.randint(2,(n,),generator=g)
        token=torch.where(torch.rand(n,generator=g)<.25,value,filler)
        out[:,j]=token;prev=token
    return out

def make_batch(seed,n,tail,body=64,ood=False):
    g=torch.Generator().manual_seed(seed)
    x=idle(n,body+tail,torch.Generator().manual_seed(seed+123456789),ood)
    final=torch.randint(2,(n,8),generator=g)
    initial=torch.randint(2,(n,8),generator=g)
    same=initial.eq(final).all(1)
    initial[same,0]=1-initial[same,0]
    order1=torch.argsort(torch.rand(n,8,generator=g),1)
    order2=torch.argsort(torch.rand(n,8,generator=g),1)
    slots=torch.cat((order1,order2),1)
    values=torch.cat((initial.gather(1,order1),final.gather(1,order2)),1)
    loc=torch.sort(torch.argsort(torch.rand(n,body-17,generator=g),1)[:,:15],1).values+torch.arange(15)
    loc=torch.cat((loc,torch.full((n,1),body-2,dtype=torch.long)),1)
    ii=torch.arange(n)[:,None]
    x[ii,loc]=2+slots;x[ii,loc+1]=10+values
    return x,final

def valid_events(ids):
    prev=ids[:,:-1];cur=ids[:,1:]
    return torch.cat((torch.zeros(len(ids),1,dtype=torch.bool),
      (prev>=2)&(prev<10)&(cur>=10)&(cur<12)),1)

def pair_set(x):
    a=x[:,:-1];b=x[:,1:];mask=(a>=22)&(a<30)&(b>=22)&(b<30)
    return set(zip(a[mask].tolist(),b[mask].tolist()))

def features(m,ids,snapshot=None):
    x=m.embedding(ids)
    prev=torch.cat((x.new_zeros(len(x),1,x.shape[-1]),x[:,:-1]),1)
    gates=torch.sigmoid(m.gate(torch.cat((prev,x),-1))).squeeze(-1)
    addr=F.normalize(m.keys,dim=-1)
    probs=F.softmax(8*(F.normalize(m.write_key(prev),dim=-1)@addr.T),-1)
    vals=torch.tanh(m.value(x))
    h=x.new_zeros(len(x),m.gru.hidden_size);hb=None
    for j,cur in enumerate(x.unbind(1)):
        h=m.gru(cur,h)
        if snapshot is not None and j==snapshot-1:hb=h
    return x,gates,probs,vals,h,hb,addr

def sweep(gates,probs,vals,snapshot=None):
    bank=vals.new_zeros(len(vals),8,vals.shape[-1]);body=None
    for j in range(vals.shape[1]):
        amount=gates[:,j,None,None]*probs[:,j,:,None]
        bank=bank*(1-amount)+amount*vals[:,j,None,:]
        if snapshot is not None and j==snapshot-1:body=bank
    return bank,body

def read(m,h,bank,old,addr,zero=False,attention=None):
    # Enumerates the queries provided by this benchmark; no desired values enter.
    b=len(h);cur=m.embedding(torch.arange(14,22)).repeat_interleave(b,0)
    hh=m.gru(cur,h.repeat(8,1));prev=old.repeat(8,1)
    gate=torch.sigmoid(m.gate(torch.cat((prev,cur),-1)))
    probs=F.softmax(8*(F.normalize(m.write_key(prev),dim=-1)@addr.T),-1)
    amount=gate[:,None,:]*probs[:,:,None]
    bb=bank.repeat(8,1,1)*(1-amount)+amount*torch.tanh(m.value(cur))[:,None,:]
    attn=F.softmax(8*(F.normalize(m.read_key(cur),dim=-1)@addr.T),-1)
    if attention is not None:attn=attention.repeat_interleave(b,0)
    found=(attn[:,:,None]*bb).sum(1)
    if zero:found=torch.zeros_like(found)
    p=m.head(torch.cat((hh,found),-1)).reshape(8,b,2).transpose(0,1)
    return p,gate

def encode(m,ids,snapshot=None):
    x,gates,probs,vals,h,hb,addr=features(m,ids,snapshot)
    bank,body=sweep(gates,probs,vals,snapshot)
    return dict(h=h,bank=bank,old=x[:,-1],addr=addr,gates=gates,body=body,hb=hb,
                bodyold=x[:,snapshot-1] if snapshot is not None else None)

def forward(m,ids):
    a=encode(m,ids)
    return read(m,a['h'],a['bank'],a['old'],a['addr'])[0]

def parity(m):
    x,y=make_batch(31000000001,2,16,48)
    p=forward(m,x);q=m(query_histories(x,8)).reshape(8,2,2).transpose(0,1)
    err=float((p-q).abs().max().detach());assert err<3e-5,err
    pars=list(m.parameters())
    a=torch.autograd.grad(F.cross_entropy(p.reshape(-1,2),y.reshape(-1)),pars)
    b=torch.autograd.grad(F.cross_entropy(q.reshape(-1,2),y.reshape(-1)),pars)
    grad=max(float((u-v).abs().max()) for u,v in zip(a,b));assert grad<3e-5,grad
    return dict(max_logit_error=err,max_all_parameter_gradient_error=grad)

def metric(p,y):
    same=p.eq(y)
    return dict(histories=len(y),correct_records=int(same.all(1).sum()),correct_bits=int(same.sum()),
       per_query_correct=same.sum(0).tolist(),predictions=p.tolist(),labels=y.tolist())

def address(m):
    ad=F.normalize(m.keys,dim=-1)
    w=F.softmax(8*(F.normalize(m.write_key(m.embedding(torch.arange(2,10))),dim=-1)@ad.T),-1)
    q=F.softmax(8*(F.normalize(m.read_key(m.embedding(torch.arange(14,22))),dim=-1)@ad.T),-1)
    return w,q

@torch.no_grad()
def audit():
    out=HERE/(PREFIX+'_audit.json')
    if out.exists():raise FileExistsError(out)
    start=time.monotonic();cpu=time.process_time()
    prior=json.loads((HERE/'learned_gate_repair_results.json').read_text())
    saved=torch.load(HERE/'learned_gate_repair_weights.pt',map_location='cpu',weights_only=True)
    source=torch.load(HERE/'faded_guidance_weights.pt',map_location='cpu',weights_only=True)
    assert sha(HERE/'learned_gate_repair.py')==prior['source_sha256']
    assert sha(HERE/'learned_gate_repair_weights.pt')==prior['weights_sha256']
    checks=[]
    for s in (17,29,43):
        m=factory(s);m.load_state_dict(saved[f'{s}_answer_only'])
        changed=[k for k,v in m.state_dict().items() if not torch.equal(v,source[f'{s}_8_linear_fade'][k])]
        assert all(k.startswith('gate.') for k in changed)
        old=next(r for r in prior['runs'] if r['seed']==s and r['arm']=='answer_only')
        for i,tail in enumerate((256,1024,4080)):
            pp=[];yy=[];hsh=hashlib.sha256()
            for pos in range(0,128,32):
                x,y=legacy_batch(8,tail+16,32,7100000000+s*100003+pos*677)
                hsh.update(x.numpy().tobytes());hsh.update(y.numpy().tobytes())
                pp.append(forward(m,x).argmax(-1));yy.append(y)
            p=torch.cat(pp);y=torch.cat(yy);oldrow=old['eval'][i]
            assert p.tolist()==oldrow['normal']['predictions']
            assert y.tolist()==oldrow['normal']['labels']
            assert hsh.hexdigest()==oldrow['input_sha256']
            checks.append(dict(seed=s,tail=tail,correct_records=int(p.eq(y).all(1).sum()),
                               correct_bits=int(p.eq(y).sum()),changed_tensors=changed))
    m=factory(29);m.load_state_dict(saved['29_answer_only'])
    wp,qp=address(m);assigned=wp.argmax(1).tolist()
    groups={a:[i for i,p in enumerate(assigned) if p==a] for a in set(assigned)}
    collision=next(v for v in groups.values() if len(v)>1)
    split=collision[-1];unused=next(i for i in range(8) if i not in assigned)
    variants=('normal','oracle_event_gate','split_write_only','split_read_only','split_both')
    pred={v:[] for v in variants};ys=[];gate_by_fact=[[] for _ in range(8)]
    for pos in range(0,128,32):
        ids,y=legacy_batch(8,16,32,7100000000+29*100003+pos*677)
        x,gg,probs,vals,h,hb,ad=features(m,ids)
        valid=valid_events(ids)
        prev=torch.cat((torch.full((len(ids),1),-1),ids[:,:-1]),1)
        for fact in range(8):gate_by_fact[fact].extend(gg[valid&(prev==2+fact)].tolist())
        for v in variants:
            g=valid.to(gg.dtype) if v=='oracle_event_gate' else gg
            pp=probs.clone()
            if v in ('split_write_only','split_both'):
                mask=prev==2+split
                pp[mask]=0;pp[:,:,unused]=torch.where(mask,torch.ones_like(pp[:,:,unused]),pp[:,:,unused])
            bank,_=sweep(g,pp,vals)
            attention=None
            if v in ('split_read_only','split_both'):
                attention=qp.clone();attention[split]=0;attention[split,unused]=1
            pred[v].append(read(m,h,bank,x[:,-1],ad,attention=attention)[0].argmax(-1))
        ys.append(y)
    y=torch.cat(ys);weak={v:metric(torch.cat(pred[v]),y) for v in variants}
    p=torch.cat(pred['normal']);i,j=collision[:2];agree=y[:,i].eq(y[:,j])
    weak_detail=dict(write_probs=wp.tolist(),read_probs=qp.tolist(),write_argmax=assigned,
       read_argmax=qp.argmax(1).tolist(),collision_queries=collision,unused_slot=unused,
       write_gate_by_fact=[sum(g)/len(g) for g in gate_by_fact],
       true_collision_facts_agree=int(agree.sum()),
       whole_correct_when_facts_agree=int((p.eq(y).all(1)&agree).sum()),
       whole_correct_when_facts_differ=int((p.eq(y).all(1)&~agree).sum()),
       variants=weak,warning='Oracle routing and event-gating interventions are diagnostics ONLY; no trained weights changed.')
    # Generator checks use no model training and a separate seed space.
    trainpairs=set();testpairs=set();trainids=set()
    for ood in (False,True):
        for s in range(8):
            x,y=make_batch(41000000000+s,16,128,64,ood)
            assert torch.equal(replay(x,8,2),y)
            assert bool(valid_events(x).sum(1).eq(16).all())
            assert bool(valid_events(x)[:,63].all())
            ps=pair_set(x)
            if ood:testpairs|=ps
            else:trainpairs|=ps;trainids|=set(x.flatten().tolist())
    assert not trainpairs&testpairs
    result=dict(prior_replays=checks,weak_seed29=weak_detail,
      corpus_check=dict(train_filler_pairs=sorted(trainpairs),ood_filler_pairs=sorted(testpairs),
                        overlap=[],train_ids=sorted(trainids),new_token_identities=False),
      source_sha256=sha(Path(__file__)),wall_s=time.monotonic()-start,cpu_s=time.process_time()-cpu,
      peak_working_set_bytes=peak_memory(),cpu_threads=torch.get_num_threads(),gpu=False)
    save(out,result)
    print('AUDIT',json.dumps({'replays':len(checks),'collision':collision,
          'counts':{v:z['correct_records'] for v,z in weak.items()},'wall':result['wall_s']}),flush=True)


def train_one(seed,arm):
    # Fresh initialization only; no checkpoint reads anywhere in this function.
    m=factory(seed);initial=digest(m.state_dict())
    opt=torch.optim.AdamW(m.parameters(),lr=.003)
    trace=[];corpus=hashlib.sha256();pairs=set();tokens=set();stage=None
    tic=time.monotonic();cpu=time.process_time();ntokens=0
    for step in range(512):
        if step==384:
            stage=state(m)
            if arm=='gate_repair_policy':
                for n,p in m.named_parameters():p.requires_grad_(n.startswith('gate.'))
            opt=torch.optim.AdamW([p for p in m.parameters() if p.requires_grad],lr=.003)
        data_seed=11000000000+seed*1000003+step*8191
        rng=random.Random(data_seed)
        body=rng.choice((48,64,80));tail=rng.choice((0,16,64,128))
        x,y=make_batch(data_seed,12,tail,body,False)
        corpus.update(x.numpy().tobytes());corpus.update(y.numpy().tobytes())
        pairs|=pair_set(x);tokens|=set(x.flatten().tolist());ntokens+=x.numel()
        p=forward(m,x)
        loss=F.cross_entropy(p.reshape(-1,2),y.reshape(-1))
        assert bool(torch.isfinite(loss))
        opt.zero_grad(set_to_none=True);loss.backward()
        torch.nn.utils.clip_grad_norm_([p for p in m.parameters() if p.requires_grad],1.)
        opt.step();trace.append(float(loss.detach()))
        if (step+1)%128==0:
            print('TRAIN_PROGRESS',seed,arm,step+1,'CE',sum(trace[-32:])/32,
                  'wall',round(time.monotonic()-tic,2),flush=True)
    if arm=='gate_repair_policy':
        changed=[k for k,v in m.state_dict().items() if not torch.equal(v,stage[k])]
        assert changed and all(k.startswith('gate.') for k in changed)
    else:changed=[k for k,v in m.state_dict().items() if not torch.equal(v,stage[k])]
    return m,stage,dict(seed=seed,arm=arm,initial_sha256=initial,stage384_sha256=digest(stage),
       examples_sha256=corpus.hexdigest(),updates=512,histories=6144,queries=49152,
       unique_history_tokens=ntokens,wall_s=time.monotonic()-tic,cpu_s=time.process_time()-cpu,
       parameters=sum(p.numel() for p in m.parameters()),final_trainable_parameters=sum(p.numel() for p in m.parameters() if p.requires_grad),
       last_stage_changed_tensors=changed,train_filler_pairs=sorted(pairs),token_ids=sorted(tokens),ce_trace=trace)

@torch.no_grad()
def evaluate_one(m,seed,domain):
    ood=domain=='ood';rows=[]
    for tail in (256,1024,4080):
        tic=time.monotonic();cpu=time.process_time()
        pp=[];zz=[];short=[];ys=[];hsh=hashlib.sha256();bodyhash=hashlib.sha256()
        vg=ig=tg=0.;vn=inn=tn=0;cos=[];drift=[];testpairs=set()
        for start in range(0,96,32):
            x,y=make_batch(21000000000+seed*100003+start*677,32,tail,64,ood)
            hsh.update(x.numpy().tobytes());hsh.update(y.numpy().tobytes())
            bodyhash.update(x[:,:64].numpy().tobytes());bodyhash.update(y.numpy().tobytes())
            testpairs|=pair_set(x)
            a=encode(m,x,snapshot=64)
            p,qg=read(m,a['h'],a['bank'],a['old'],a['addr'])
            zero,_=read(m,a['h'],a['bank'],a['old'],a['addr'],zero=True)
            initial,_=read(m,a['hb'],a['body'],a['bodyold'],a['addr'])
            pp.append(p.argmax(-1));zz.append(zero.argmax(-1));short.append(initial.argmax(-1));ys.append(y)
            valid=valid_events(x);g=a['gates']
            vg+=float(g[valid].sum());vn+=int(valid.sum())
            ig+=float(g[~valid].sum())+float(qg.sum());inn+=int((~valid).sum())+qg.numel()
            tg+=float(g[:,64:].sum());tn+=g[:,64:].numel()
            cos.extend(F.cosine_similarity(a['bank'].flatten(1),a['body'].flatten(1),dim=1).tolist())
            drift.extend(((a['bank']-a['body']).flatten(1).norm(dim=1)/a['body'].flatten(1).norm(dim=1).clamp_min(1e-12)).tolist())
        p=torch.cat(pp);z=torch.cat(zz);y=torch.cat(ys);s=torch.cat(short)
        bc=s.eq(y).all(1);ret=p.eq(y).all(1)&bc
        rows.append(dict(domain=domain,tail=tail,input_sha256=hsh.hexdigest(),body_sha256=bodyhash.hexdigest(),
           normal=metric(p,y),zero_bank=metric(z,y),body=metric(s,y),body_correct_retained=int(ret.sum()),
           valid_gate_mean=vg/vn,invalid_gate_mean=ig/inn,tail_gate_mean=tg/tn,tail_gate_integral=tg/96,
           bank_cosine=sum(cos)/len(cos),bank_relative_drift=sum(drift)/len(drift),
           filler_pairs=sorted(testpairs),wall_s=time.monotonic()-tic,cpu_s=time.process_time()-cpu))
    assert len({r['body_sha256'] for r in rows})==1
    return rows

@torch.no_grad()
def late_update(m,seed,domain):
    pp=[];ys=[];updated=[];unaffected=[];gates=[];hsh=hashlib.sha256()
    for start in (0,32):
        data_seed=22000000000+seed*100003+start*677
        x,y=make_batch(data_seed,32,1024,64,domain=='ood')
        rng=torch.Generator().manual_seed(data_seed+777)
        slot=torch.randint(8,(32,),generator=rng)
        new=1-y[torch.arange(32),slot]
        command=torch.stack((2+slot,10+new),1)
        tail=idle(32,256,rng,domain=='ood')
        xx=torch.cat((x,command,tail),1)
        yy=y.clone();yy[torch.arange(32),slot]=new
        assert torch.equal(replay(xx,8,2),yy)
        a=encode(m,xx);p=read(m,a['h'],a['bank'],a['old'],a['addr'])[0].argmax(-1)
        updated.extend(p[torch.arange(32),slot].eq(new).tolist())
        mask=torch.ones_like(yy,dtype=torch.bool);mask[torch.arange(32),slot]=False
        unaffected.extend(p.eq(yy)[mask].tolist());gates.extend(a['gates'][:,len(x[0])+1].tolist())
        pp.append(p);ys.append(yy);hsh.update(xx.numpy().tobytes());hsh.update(yy.numpy().tobytes())
    return dict(domain=domain,normal=metric(torch.cat(pp),torch.cat(ys)),input_sha256=hsh.hexdigest(),
      changed_fact_correct=sum(updated),unaffected_bits_correct=sum(unaffected),late_write_gate_mean=sum(gates)/len(gates))

def run():
    out=HERE/(PREFIX+'_results.json');weightpath=HERE/(PREFIX+'_weights.pt')
    if out.exists() or weightpath.exists():raise FileExistsError('Preserve scratch outputs')
    originals={p.name:sha(p) for p in HERE.iterdir() if p.is_file() and not p.name.startswith(PREFIX)}
    tic=time.monotonic();cpu=time.process_time()
    checks=parity(factory(101))
    d=dict(protocol_sha256=sha(HERE/(PREFIX+'_protocol.md')),source_sha256=sha(Path(__file__)),
       originals=originals,cpu_threads=torch.get_num_threads(),interop_threads=torch.get_num_interop_threads(),
       gpu=False,torch=torch.__version__,python=sys.version,parity=checks,training=[],runs=[],complete=False)
    weights={};models={}
    for seed in SEEDS:
        for arm in ARMS:
            m,stage,row=train_one(seed,arm)
            d['training'].append(row);weights[f'{seed}_{arm}']=state(m);weights[f'{seed}_{arm}_stage384']=stage
            models[seed,arm]=m;save(out,d)
        a,b=[r for r in d['training'] if r['seed']==seed]
        for key in ('initial_sha256','stage384_sha256','examples_sha256','unique_history_tokens'):
            assert a[key]==b[key],(seed,key)
        assert a['ce_trace'][:384]==b['ce_trace'][:384]
    # External checkpoints are first read AFTER all fresh runs have finished.
    guided=torch.load(HERE/'learned_gate_repair_weights.pt',map_location='cpu',weights_only=True)
    for seed,oldseed in zip(SEEDS,(17,29,43)):
        m=factory(oldseed);m.load_state_dict(guided[f'{oldseed}_answer_only'])
        models[seed,'guided_reference']=m
    for (seed,arm),m in models.items():
        m.eval()
        for p in m.parameters():p.requires_grad_(False)
        row=dict(seed=seed,arm=arm,eval=[],late=[])
        for domain in ('id','ood'):
            row['eval']+=evaluate_one(m,seed,domain)
            row['late'].append(late_update(m,seed,domain))
        d['runs'].append(row);save(out,d)
        print('EVAL',seed,arm,[(e['domain'],e['tail'],e['normal']['correct_records'],e['zero_bank']['correct_bits']) for e in row['eval']],flush=True)
    for seed in SEEDS:
        rr=[r for r in d['runs'] if r['seed']==seed]
        for i in range(6):assert len({r['eval'][i]['input_sha256'] for r in rr})==1
        for i in range(2):assert len({r['late'][i]['input_sha256'] for r in rr})==1
    trainpairs=set(tuple(p) for r in d['training'] for p in r['train_filler_pairs'])
    oodpairs=set(tuple(p) for r in d['runs'] for e in r['eval'] if e['domain']=='ood' for p in e['filler_pairs'])
    assert not trainpairs&oodpairs
    assert len(trainpairs)==32 and len(oodpairs)==32
    d['holdout_filler_pairs_disjoint']=True
    d['original_files_unchanged']={n:sha(HERE/n)==s for n,s in originals.items()}
    assert all(d['original_files_unchanged'].values())
    torch.save(weights,weightpath)
    d['weights_sha256']=sha(weightpath);d['wall_s']=time.monotonic()-tic;d['cpu_s']=time.process_time()-cpu
    d['peak_working_set_bytes']=peak_memory();d['complete']=True;save(out,d)
    print('COMPLETE',d['wall_s'],d['cpu_s'],flush=True)

@torch.no_grad()
def verify():
    out=HERE/(PREFIX+'_verification.json')
    if out.exists():raise FileExistsError(out)
    tic=time.monotonic();cpu=time.process_time()
    d=json.loads((HERE/(PREFIX+'_results.json')).read_text());assert d['complete']
    assert sha(Path(__file__))==d['source_sha256']
    assert sha(HERE/(PREFIX+'_weights.pt'))==d['weights_sha256']
    saved=torch.load(HERE/(PREFIX+'_weights.pt'),map_location='cpu',weights_only=True)
    guided=torch.load(HERE/'learned_gate_repair_weights.pt',map_location='cpu',weights_only=True)
    checks=[]
    for row in d['runs']:
        seed=row['seed'];arm=row['arm']
        m=factory(seed)
        if arm=='guided_reference':s=guided[f'{dict(zip(SEEDS,(17,29,43)))[seed]}_answer_only']
        else:s=saved[f'{seed}_{arm}']
        m.load_state_dict(s)
        e=next(e for e in row['eval'] if e['domain']=='ood' and e['tail']==4080)
        # Reconstruct original batch32, THEN select two histories.
        x,y=make_batch(21000000000+seed*100003,32,4080,64,True)
        native=m(query_histories(x[:2],8)).reshape(8,2,2).transpose(0,1)
        assert native.argmax(-1).tolist()==e['normal']['predictions'][:2]
        fast=forward(m,x[:2]);err=float((native-fast).abs().max());assert err<3e-5
        # Recompute EVERY reported normal/ablated/late count from raw predictions.
        for ev in row['eval']:
            for mode in ('normal','zero_bank','body'):
                z=ev[mode];same=torch.tensor(z['predictions']).eq(torch.tensor(z['labels']))
                assert int(same.sum())==z['correct_bits'];assert int(same.all(1).sum())==z['correct_records']
        if arm=='gate_repair_policy':
            stage=saved[f'{seed}_{arm}_stage384']
            assert all(torch.equal(v,stage[k]) for k,v in s.items() if not k.startswith('gate.'))
        checks.append(dict(seed=seed,arm=arm,native_prediction_replay=True,max_native_logit_error=err))
    unchanged={n:sha(HERE/n)==h for n,h in d['originals'].items()};assert all(unchanged.values())
    save(out,dict(checks=checks,original_files_unchanged=unchanged,cpu_threads=torch.get_num_threads(),gpu=False,
      source_sha256=sha(Path(__file__)),wall_s=time.monotonic()-tic,cpu_s=time.process_time()-cpu,
      peak_working_set_bytes=peak_memory()))
    print('VERIFY_COMPLETE',time.monotonic()-tic,flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=('audit','run','verify'),required=True)
    a=p.parse_args();torch.set_num_threads(4);torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True);assert not torch.cuda.is_available()
    {'audit':audit,'run':run,'verify':verify}[a.phase]()
if __name__=='__main__':main()
