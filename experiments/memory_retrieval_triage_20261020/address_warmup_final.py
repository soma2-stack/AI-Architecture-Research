"""One bounded six-run inverse-temperature test. No further optimization.
Architecture/generator reused from memory_from_scratch.py; only training beta differs.
"""
import os,sys,time
START=time.monotonic()
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='4'
sys.dont_write_bytecode=True
import threading,json,random,hashlib,traceback
from pathlib import Path

def hard_stop():
    print('HARD_WALL_LIMIT: own experiment stopped before600 seconds',flush=True)
    os._exit(124)
WATCHDOG=threading.Timer(max(1,599-(time.monotonic()-START)),hard_stop);WATCHDOG.daemon=True;WATCHDOG.start()
import torch
from torch.nn import functional as F
import memory_from_scratch as base
from prototypes.rnn_llm_architecture.capacity_010 import query_histories,replay
HERE=Path(__file__).resolve().parent;PREFIX='address_warmup_final'
OUT=HERE/(PREFIX+'_results.json');WEIGHTS=HERE/(PREFIX+'_weights.pt');REPORT=HERE/(PREFIX+'_report.md')
SEEDS=(101,211,307);ARMS=('fixed8','warmup1to8')

def budget():
    if time.monotonic()-START>=570:raise TimeoutError('Cooperative570-second experiment limit; no retry authorized')
def beta_for(arm,step):return 8. if arm=='fixed8' else 1.+7.*min(step/127.,1.)
def fast(m,ids,beta):
    x=m.embedding(ids);prev=torch.cat((x.new_zeros(len(x),1,x.shape[-1]),x[:,:-1]),1)
    gates=torch.sigmoid(m.gate(torch.cat((prev,x),-1))).squeeze(-1)
    ad=F.normalize(m.keys,dim=-1)
    probs=F.softmax(beta*(F.normalize(m.write_key(prev),dim=-1)@ad.T),-1)
    vals=torch.tanh(m.value(x));h=x.new_zeros(len(x),32)
    for cur in x.unbind(1):h=m.gru(cur,h)
    bank,_=base.sweep(gates,probs,vals)
    b=len(x);cur=m.embedding(torch.arange(14,22)).repeat_interleave(b,0)
    hh=m.gru(cur,h.repeat(8,1));old=x[:,-1].repeat(8,1)
    gate=torch.sigmoid(m.gate(torch.cat((old,cur),-1)))
    p=F.softmax(beta*(F.normalize(m.write_key(old),dim=-1)@ad.T),-1)
    amount=gate[:,None,:]*p[:,:,None]
    bb=bank.repeat(8,1,1)*(1-amount)+amount*torch.tanh(m.value(cur))[:,None,:]
    attn=F.softmax(beta*(F.normalize(m.read_key(cur),dim=-1)@ad.T),-1)
    found=(attn[:,:,None]*bb).sum(1)
    return m.head(torch.cat((hh,found),-1)).reshape(8,b,2).transpose(0,1)

def slow(m,ids,beta):
    x=m.embedding(ids);h=x.new_zeros(len(x),32);bank=x.new_zeros(len(x),8,12);old=x.new_zeros(len(x),32)
    ad=F.normalize(m.keys,dim=-1)
    for cur in x.unbind(1):
        h=m.gru(cur,h);gate=torch.sigmoid(m.gate(torch.cat((old,cur),-1)))
        p=F.softmax(beta*(F.normalize(m.write_key(old),dim=-1)@ad.T),-1)
        amount=gate[:,None,:]*p[:,:,None]
        bank=bank*(1-amount)+amount*torch.tanh(m.value(cur))[:,None,:];old=cur
    attn=F.softmax(beta*(F.normalize(m.read_key(old),dim=-1)@ad.T),-1)
    return m.head(torch.cat((h,(attn[:,:,None]*bank).sum(1)),-1))

def validate_forward():
    m=base.factory(101);x,y=base.make_batch(51000000001,2,16,48,False);checks=[]
    for beta in (1.,8.):
        budget();p=fast(m,x,beta)
        q=slow(m,query_histories(x,8),beta).reshape(8,2,2).transpose(0,1)
        err=float((p-q).abs().max().detach());assert err<3e-5
        pa=list(m.parameters())
        ga=torch.autograd.grad(F.cross_entropy(p.reshape(-1,2),y.reshape(-1)),pa)
        gb=torch.autograd.grad(F.cross_entropy(q.reshape(-1,2),y.reshape(-1)),pa)
        ge=max(float((a-b).abs().max()) for a,b in zip(ga,gb));assert ge<3e-5
        checks.append(dict(beta=beta,max_logit_error=err,max_parameter_gradient_error=ge))
    return checks

def train(seed,arm,d):
    assert d['training_runs_started']<6
    d['training_runs_started']+=1
    m=base.factory(seed);initial=base.digest(m.state_dict());opt=torch.optim.AdamW(m.parameters(),lr=.003)
    trace=[];btrace=[];datahash=hashlib.sha256();pairs=set();tic=time.monotonic();cpu=time.process_time()
    for step in range(512):
        budget()
        if step==384:opt=torch.optim.AdamW(m.parameters(),lr=.003)
        sd=11000000000+seed*1000003+step*8191;rng=random.Random(sd)
        body=rng.choice((48,64,80));tail=rng.choice((0,16,64,128))
        x,y=base.make_batch(sd,12,tail,body,False)
        datahash.update(x.numpy().tobytes());datahash.update(y.numpy().tobytes());pairs|=base.pair_set(x)
        beta=beta_for(arm,step);p=fast(m,x,beta)
        loss=F.cross_entropy(p.reshape(-1,2),y.reshape(-1));assert bool(torch.isfinite(loss))
        opt.zero_grad(set_to_none=True);loss.backward();torch.nn.utils.clip_grad_norm_(m.parameters(),1.);opt.step()
        trace.append(float(loss.detach()));btrace.append(beta);d['total_optimizer_updates']+=1
        d['active_run']=dict(seed=seed,arm=arm,updates=step+1)
        if (step+1)%128==0:
            base.save(OUT,d)
            print('TRAIN',seed,arm,step+1,'CE',sum(trace[-32:])/32,'elapsed',round(time.monotonic()-START,2),flush=True)
    return m,dict(seed=seed,arm=arm,updates=512,histories=6144,query_examples=49152,
        initial_sha256=initial,data_sha256=datahash.hexdigest(),final_sha256=base.digest(m.state_dict()),
        train_filler_pairs=sorted(pairs),ce_trace=trace,beta_trace=btrace,
        wall_s=time.monotonic()-tic,cpu_s=time.process_time()-cpu,
        parameters=sum(p.numel() for p in m.parameters()))

@torch.no_grad()
def routing(m):
    w,q=base.address(m);wa=w.argmax(1);qa=q.argmax(1)
    wc=int(torch.triu(wa[:,None].eq(wa[None,:]),1).sum());qc=int(torch.triu(qa[:,None].eq(qa[None,:]),1).sum())
    return dict(write_probs=w.tolist(),read_probs=q.tolist(),write_argmax=wa.tolist(),read_argmax=qa.tolist(),
       unique_writes=len(set(wa.tolist())),unique_reads=len(set(qa.tolist())),write_collision_pairs=wc,read_collision_pairs=qc,
       paired_matches=int(wa.eq(qa).sum()),write_soft_pair_overlap=float(torch.triu(w@w.T,1).sum()/28),
       read_soft_pair_overlap=float(torch.triu(q@q.T,1).sum()/28),paired_soft_overlap=(w*q).sum(1).tolist())

@torch.no_grad()
def evaluate(m,seed,tail):
    pp=[];zz=[];yy=[];inputhash=hashlib.sha256();bodyhash=hashlib.sha256();pairs=set()
    vs=ns=gs=0.;vn=nn=gn=0;cos=[];drift=[]
    tic=time.monotonic();cpu=time.process_time()
    for start in (0,32,64):
        budget();x,y=base.make_batch(21000000000+seed*100003+start*677,32,tail,64,True)
        assert torch.equal(replay(x[:,:64],8,2),y)
        inputhash.update(x.numpy().tobytes());inputhash.update(y.numpy().tobytes())
        bodyhash.update(x[:,:64].numpy().tobytes());bodyhash.update(y.numpy().tobytes());pairs|=base.pair_set(x)
        a=base.encode(m,x,snapshot=64);p,qg=base.read(m,a['h'],a['bank'],a['old'],a['addr'])
        zero,_=base.read(m,a['h'],a['bank'],a['old'],a['addr'],zero=True)
        pp.append(p.argmax(-1));zz.append(zero.argmax(-1));yy.append(y)
        valid=base.valid_events(x);g=a['gates']
        vs+=float(g[valid].sum());vn+=int(valid.sum())
        ns+=float(g[~valid].sum())+float(qg.sum());nn+=int((~valid).sum())+qg.numel()
        gs+=float(g[:,64:].sum());gn+=g[:,64:].numel()
        cos.extend(F.cosine_similarity(a['bank'].flatten(1),a['body'].flatten(1),dim=1).tolist())
        drift.extend(((a['bank']-a['body']).flatten(1).norm(dim=1)/a['body'].flatten(1).norm(dim=1).clamp_min(1e-12)).tolist())
    y=torch.cat(yy)
    return dict(tail=tail,input_sha256=inputhash.hexdigest(),body_sha256=bodyhash.hexdigest(),
       normal=base.metric(torch.cat(pp),y),zero_bank=base.metric(torch.cat(zz),y),
       valid_gate=vs/vn,invalid_gate=ns/nn,tail_gate=gs/gn,bank_cosine=sum(cos)/len(cos),
       relative_bank_drift=sum(drift)/len(drift),filler_pairs=sorted(pairs),
       wall_s=time.monotonic()-tic,cpu_s=time.process_time()-cpu)

@torch.no_grad()
def verify_model(m,seed,row):
    budget();x,y=base.make_batch(21000000000+seed*100003,32,4080,64,True)
    native=m(query_histories(x[:2],8)).reshape(8,2,2).transpose(0,1)
    assert native.argmax(-1).tolist()==row['eval'][1]['normal']['predictions'][:2]
    optimized=base.forward(m,x[:2]);err=float((native-optimized).abs().max());assert err<3e-5
    def erase(module,args):
        a=args[0].clone();a[:,-12:]=0;return (a,)
    hook=m.head.register_forward_pre_hook(erase)
    try:z=m(query_histories(x[:2],8)).reshape(8,2,2).transpose(0,1).argmax(-1)
    finally:hook.remove()
    assert z.tolist()==row['eval'][1]['zero_bank']['predictions'][:2]
    for e in row['eval']:
        for mode in ('normal','zero_bank'):
            r=e[mode];same=torch.tensor(r['predictions']).eq(torch.tensor(r['labels']))
            assert int(same.sum())==r['correct_bits'];assert int(same.all(1).sum())==r['correct_records']
    return dict(native_predictions_match=True,native_bank_ablation_match=True,max_logit_error=err)

def decide(d):
    rr={(r['seed'],r['arm']):r for r in d['runs']}
    delta=[rr[s,'warmup1to8']['eval'][1]['normal']['correct_records']-rr[s,'fixed8']['eval'][1]['normal']['correct_records'] for s in SEEDS]
    short=[rr[s,'warmup1to8']['eval'][0]['normal']['correct_records']-rr[s,'fixed8']['eval'][0]['normal']['correct_records'] for s in SEEDS]
    coll={arm:sum(rr[s,arm]['routing']['write_collision_pairs'] for s in SEEDS) for arm in ARMS}
    longgain=sum(delta)>0;colgain=coll['warmup1to8']<coll['fixed8']
    shortharm=sum(short)/288<-.05 or min(short)/96<-.10
    seeddep=sum(v>0 for v in delta)<2 or min(delta)/96<-.05
    if longgain and colgain and not shortharm and not seeddep:verdict='PASS'
    elif not longgain and not colgain:verdict='FAIL'
    else:verdict='INCONCLUSIVE'
    return dict(verdict=verdict,long_record_differences=delta,short_record_differences=short,
       pooled_long_gain_pp=100*sum(delta)/288,pooled_short_gain_pp=100*sum(short)/288,
       write_collision_pairs_totals=coll,material_short_harm=shortharm,strong_seed_dependence=seeddep,
       stop_allocation_optimization=True)

def make_report(d):
    lines=['# Final address-allocation experiment', '', '**'+d.get('decision',{}).get('verdict','INCONCLUSIVE')+'** — one fixed six-run test; no follow-up optimization.', '',
      'Only the training softmax sharpness changed: fixed beta8 versus beta1→8 over128 updates, then8. Both evaluate at8. Same11,507-parameter architecture, seeds101/211/307, examples, optimizer/reset and512 full-training updates. No pretrained initialization, extra supervision, masks or address assignments.', '',
      '| Idle tokens | Fixed8: complete /fact accuracy | Warmup: complete /fact accuracy |','|---:|---:|---:|']
    for i,tail in enumerate((256,4080)):
        cells=[]
        for arm in ARMS:
            rs=[r['eval'][i]['normal'] for r in d['runs'] if r['arm']==arm]
            cells.append(f'{sum(r["correct_records"] for r in rs)}/288 ({100*sum(r["correct_records"] for r in rs)/288:.2f}%) / {100*sum(r["correct_bits"] for r in rs)/2304:.2f}%')
        lines.append(f'| {tail:,} | '+' | '.join(cells)+' |')
    lines+=['','| Seed | Long recall fixed→warmup (/96) | Write collision pairs fixed→warmup | Distinct write slots fixed→warmup | Read/write matches fixed→warmup |','|---:|---:|---:|---:|---:|']
    rr={(r['seed'],r['arm']):r for r in d['runs']}
    for s in SEEDS:
        a=rr[s,'fixed8'];b=rr[s,'warmup1to8'];ar=a['routing'];br=b['routing']
        lines.append(f'| {s} | {a["eval"][1]["normal"]["correct_records"]}→{b["eval"][1]["normal"]["correct_records"]} | {ar["write_collision_pairs"]}→{br["write_collision_pairs"]} | {ar["unique_writes"]}→{br["unique_writes"]} | {ar["paired_matches"]}→{br["paired_matches"]} |')
    dc=d['decision']
    lines+=['',f'Long recall change **{dc["pooled_long_gain_pp"]:+.2f} points**; short recall change **{dc["pooled_short_gain_pp"]:+.2f} points**. Total dominant write collision pairs: **{dc["write_collision_pairs_totals"]["fixed8"]}→{dc["write_collision_pairs_totals"]["warmup1to8"]}**. Material short-delay harm: {dc["material_short_harm"]}; strong seed dependence under the preregistered rule: {dc["strong_seed_dependence"]}.', '',
      'Allocation is measured at the same evaluation sharpness, including full soft probabilities, overlap and per-query errors in raw JSON. Dominant collisions are not a rank/capacity proof. Temperature changes optimization of all learned weights: co-improvement supports an allocation explanation, but does not isolate routing causally from gate/value/readout changes.', '',
      '| Seed/arm | Soft write-pair overlap | Valid /invalid gate | Bank cosine at4080 | Zero-bank fact accuracy at4080 |','|---|---:|---:|---:|---:|']
    for r in d['runs']:
        e=r['eval'][1]
        lines.append(f'| {r["seed"]}/{r["arm"]} | {r["routing"]["write_soft_pair_overlap"]:.5f} | {e["valid_gate"]:.4f}/{e["invalid_gate"]:.6f} | {e["bank_cosine"]:.4f} | {100*e["zero_bank"]["correct_bits"]/768:.2f}% |')
    lines+=['',
      'Limits: three seeds,96 records/seed/horizon, one small synthetic binary task. Same previously inspected held-out benchmark as the prior run; not an untouched external test. Evaluation filler bigrams are absent from training, but token identities are familiar. All neural inference is beta8 with no parser/oracle. Zero-bank is an inference diagnostic, not a trained baseline. No claim about PR #35, PR #36 or a new architecture.', '',
      f'Checks: paired initial/data hashes agree; baseline predictions reproduce the prior full-training benchmark; native inference and native head-input bank ablation agree with saved predictions. Full-gradient checks at beta1 and8 pass. All **{len(d["original_files_unchanged"])} pre-existing files** remain byte-identical.', '',
      f'Resources: **{d["training_runs_started"]} training runs,512 updates each**,4 intra-op threads,1 inter-op thread,no GPU/workers. End-to-end experiment **{d["wall_s"]:.2f} wall seconds /{d["cpu_s"]:.2f} process CPU seconds**, including startup/training/evaluation/verification. Peak process working set **{d["peak_working_set_bytes"]/2**20:.1f} MiB**. Hard599-second watchdog and cooperative570-second limit; no retries.', '',
      '**Recommendation: close address-allocation optimization for now. Return to independent auditing of Claude Opus mathematical constructions, lemmas and proofs; do not start another benchmark optimization.**' if dc['verdict']!='PASS' else '**Recommendation: preserve this bounded result without claiming a breakthrough. No additional training is authorized in this turn; return to independent mathematical auditing.**', '',
      'Status: experiment complete; allocation lane stopped for now. Unresolved: robustness, isolation of the optimization mechanism and any broader architecture significance. Next work: mathematical auditing, not another allocation test.', '',
      'Artifacts: [protocol](address_warmup_final_protocol.md), [script](address_warmup_final.py), [raw traces/predictions/checks](address_warmup_final_results.json), [new weights](address_warmup_final_weights.pt). The script refuses existing outputs. Prior code/checkpoints/reports/proofs/notebooks remain intact; no PR or outreach.', '']
    REPORT.write_text('\n'.join(lines),encoding='utf8')

def main():
    if OUT.exists() or WEIGHTS.exists() or REPORT.exists():raise FileExistsError('Preserve existing final-test files')
    torch.set_num_threads(4);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
    assert not torch.cuda.is_available()
    cpu=time.process_time();originals={p.name:base.sha(p) for p in HERE.iterdir() if p.is_file() and not p.name.startswith(PREFIX)}
    d=dict(source_sha256=base.sha(Path(__file__)),protocol_sha256=base.sha(HERE/(PREFIX+'_protocol.md')),
        original_hashes=originals,torch=torch.__version__,python=sys.version,cpu_threads=4,gpu=False,
        training_runs_started=0,total_optimizer_updates=0,training=[],runs=[],complete=False)
    weights={};models={}
    try:
        d['forward_gradient_checks']=validate_forward()
        for s in SEEDS:
            for arm in ARMS:
                m,row=train(s,arm,d);models[s,arm]=m;d['training'].append(row);weights[f'{s}_{arm}']=base.state(m)
                torch.save(weights,WEIGHTS);base.save(OUT,d)
            r=[z for z in d['training'] if z['seed']==s]
            assert r[0]['initial_sha256']==r[1]['initial_sha256'];assert r[0]['data_sha256']==r[1]['data_sha256']
        prior=json.loads((HERE/'memory_from_scratch_results.json').read_text())
        for (s,arm),m in models.items():
            budget();m.eval()
            for p in m.parameters():p.requires_grad_(False)
            row=dict(seed=s,arm=arm,routing=routing(m),eval=[evaluate(m,s,t) for t in (256,4080)])
            assert row['eval'][0]['body_sha256']==row['eval'][1]['body_sha256']
            row['native_verification']=verify_model(m,s,row)
            if arm=='fixed8':
                old=next(z for z in prior['runs'] if z['seed']==s and z['arm']=='original_policy')
                oldtrain=next(z for z in prior['training'] if z['seed']==s and z['arm']=='original_policy')
                cur=next(z for z in d['training'] if z['seed']==s and z['arm']==arm)
                assert cur['initial_sha256']==oldtrain['initial_sha256'];assert cur['data_sha256']==oldtrain['examples_sha256']
                for e in row['eval']:
                    oe=next(z for z in old['eval'] if z['domain']=='ood' and z['tail']==e['tail'])
                    assert e['normal']['predictions']==oe['normal']['predictions']
                row['prior_baseline_predictions_reproduced']=True
            d['runs'].append(row);base.save(OUT,d)
            print('EVAL',s,arm,[(e['tail'],e['normal']['correct_records']) for e in row['eval']],row['routing']['write_collision_pairs'],flush=True)
        for s in SEEDS:
            rr=[r for r in d['runs'] if r['seed']==s]
            for i in (0,1):assert rr[0]['eval'][i]['input_sha256']==rr[1]['eval'][i]['input_sha256']
        trainpairs=set(tuple(p) for r in d['training'] for p in r['train_filler_pairs'])
        testpairs=set(tuple(p) for r in d['runs'] for e in r['eval'] for p in e['filler_pairs'])
        assert not trainpairs&testpairs;d['ood_filler_bigrams_disjoint']=True
        d['original_files_unchanged']={n:base.sha(HERE/n)==s for n,s in originals.items()};assert all(d['original_files_unchanged'].values())
        d['decision']=decide(d);d['weights_sha256']=base.sha(WEIGHTS)
        d['wall_s']=time.monotonic()-START;d['cpu_s']=time.process_time()-cpu;d['peak_working_set_bytes']=base.peak_memory()
        assert d['training_runs_started']==6 and d['total_optimizer_updates']==3072
        d['complete']=True;base.save(OUT,d);make_report(d)
        d['wall_s_including_report']=time.monotonic()-START;base.save(OUT,d)
        print('COMPLETE',d['decision'],d['wall_s_including_report'],flush=True)
    except Exception as ex:
        d['error']=repr(ex);d['traceback']=traceback.format_exc();d['complete']=False
        d['wall_s']=time.monotonic()-START;d['cpu_s']=time.process_time()-cpu
        base.save(OUT,d)
        REPORT.write_text('# Final allocation test: INCONCLUSIVE\n\nStopped without retraining: '+repr(ex)+
            '\n\nSee partial raw results. Allocation optimization closed; return to mathematical auditing.\n',encoding='utf8')
        raise
    finally:WATCHDOG.cancel()
if __name__=='__main__':
    try:main()
    finally:WATCHDOG.cancel()
