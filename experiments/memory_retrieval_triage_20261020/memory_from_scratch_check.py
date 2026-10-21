"""Post-training independent checks: native bank-ablation hook, routing audit,
raw-count recomputation and exact late-update target reconstruction. No training.
"""
import os,sys
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[k]='4'
sys.dont_write_bytecode=True
import hashlib,json,time
from pathlib import Path
import torch
from memory_from_scratch import HERE,PREFIX,SEEDS,factory,address,make_batch,idle,metric,peak_memory,sha
from prototypes.rnn_llm_architecture.capacity_010 import replay,query_histories
OUT=HERE/(PREFIX+'_extra_checks.json')

def main():
    if OUT.exists():raise FileExistsError(OUT)
    torch.set_num_threads(4);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
    assert not torch.cuda.is_available()
    tic=time.monotonic();cpu=time.process_time()
    d=json.loads((HERE/(PREFIX+'_results.json')).read_text());assert d['complete']
    weights=torch.load(HERE/(PREFIX+'_weights.pt'),map_location='cpu',weights_only=True)
    reference=torch.load(HERE/'learned_gate_repair_weights.pt',map_location='cpu',weights_only=True)
    checks=[]
    with torch.no_grad():
        for row in d['runs']:
            seed=row['seed'];arm=row['arm'];m=factory(seed)
            s=reference[f'{dict(zip(SEEDS,(17,29,43)))[seed]}_answer_only'] if arm=='guided_reference' else weights[f'{seed}_{arm}']
            m.load_state_dict(s);wp,qp=address(m)
            wa=wp.argmax(1).tolist();qa=qp.argmax(1).tolist()
            # Passive, exact linear survival coefficient of initial bank content
            # through idle writes; distinguishes gate activity from addressed harm.
            mass=torch.zeros(8);survival=torch.zeros(8)
            for start in (0,32,64):
                xx,_=make_batch(21000000000+seed*100003+start*677,32,4080,64,True)
                emb=m.embedding(xx)
                prev=torch.cat((emb.new_zeros(32,1,32),emb[:,:-1]),1)
                gates=torch.sigmoid(m.gate(torch.cat((prev,emb),-1)))
                probs=torch.softmax(8*(torch.nn.functional.normalize(m.write_key(prev),dim=-1)@torch.nn.functional.normalize(m.keys,dim=-1).T),-1)
                amount=(gates*probs)[:,64:]
                mass+=amount.sum((0,1))
                survival+=torch.log1p(-amount).sum(1).exp().sum(0)
            mass/=96;survival/=96
            e=next(e for e in row['eval'] if e['domain']=='ood' and e['tail']==4080)
            x,y=make_batch(21000000000+seed*100003,32,4080,64,True)
            def remove_bank(module,args):
                features=args[0].clone();features[:,-m.memdim:]=0
                return (features,)
            hook=m.head.register_forward_pre_hook(remove_bank)
            try:
                p=m(query_histories(x[:2],8)).reshape(8,2,2).transpose(0,1).argmax(-1)
            finally:hook.remove()
            assert p.tolist()==e['zero_bank']['predictions'][:2]
            for ev in row['late']:
                slots=[];targets=[];inputhash=hashlib.sha256()
                for start in (0,32):
                    data_seed=22000000000+seed*100003+start*677
                    xx,yy=make_batch(data_seed,32,1024,64,ev['domain']=='ood')
                    rng=torch.Generator().manual_seed(data_seed+777)
                    slot=torch.randint(8,(32,),generator=rng);new=1-yy[torch.arange(32),slot]
                    command=torch.stack((2+slot,10+new),1)
                    tail=idle(32,256,rng,ev['domain']=='ood')
                    xx=torch.cat((xx,command,tail),1)
                    yy[torch.arange(32),slot]=new
                    assert torch.equal(replay(xx,8,2),yy)
                    slots.append(slot);targets.append(yy)
                    inputhash.update(xx.numpy().tobytes());inputhash.update(yy.numpy().tobytes())
                    if start==0 and ev['domain']=='ood':
                        native=m(query_histories(xx[:2],8)).reshape(8,2,2).transpose(0,1).argmax(-1)
                        assert native.tolist()==ev['normal']['predictions'][:2]
                yy=torch.cat(targets);ss=torch.cat(slots);pred=torch.tensor(ev['normal']['predictions'])
                same=pred.eq(yy);mask=torch.ones_like(same);mask[torch.arange(64),ss]=False
                assert yy.tolist()==ev['normal']['labels']
                assert int(same.sum())==ev['normal']['correct_bits']
                assert int(same.all(1).sum())==ev['normal']['correct_records']
                assert int(same[torch.arange(64),ss].sum())==ev['changed_fact_correct']
                assert int(same[mask].sum())==ev['unaffected_bits_correct']
                assert inputhash.hexdigest()==ev['input_sha256']
            checks.append(dict(seed=seed,arm=arm,native_bank_ablation_replay=True,native_late_update_replay=True,
              late_targets_counts_hashes_reconstructed=True,write_probs=wp.tolist(),read_probs=qp.tolist(),
              write_argmax=wa,read_argmax=qa,unique_write_argmax=len(set(wa)),unique_read_argmax=len(set(qa)),
              paired_argmax_matches=sum(a==b for a,b in zip(wa,qa)),
              idle_write_integral_per_physical_bank=mass.tolist(),
              initial_bank_survival_per_physical_bank=survival.tolist(),
              read_weighted_initial_bank_survival=(survival@qp.T).tolist()))
            print('EXTRA_CHECK',seed,arm,'routes',len(set(wa)),len(set(qa)),flush=True)
    unchanged={n:sha(HERE/n)==h for n,h in d['originals'].items()};assert all(unchanged.values())
    result=dict(checks=checks,original_files_unchanged=unchanged,cpu_threads=4,gpu=False,
      source_sha256=sha(Path(__file__)),wall_s=time.monotonic()-tic,cpu_s=time.process_time()-cpu,
      peak_working_set_bytes=peak_memory())
    OUT.write_text(json.dumps(result,indent=2),encoding='utf8')
    print('EXTRA_COMPLETE',result['wall_s'],result['cpu_s'],flush=True)
if __name__=='__main__':main()

