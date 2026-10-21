"""Independent reload / late-write falsification. No additional training.
Fixed before main run completed: 64 fresh records/seed/arm; 1024 idle tokens,
one deliberately changed fact, then 256 idle tokens. Tests write availability
rather than allowing global memory shutdown to pass a preservation benchmark.
"""
import os,sys
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[k]='4'
sys.dont_write_bytecode=True
import hashlib,json,time,ctypes
from pathlib import Path
import torch
from learned_gate_repair import HERE,SEEDS,model,forward,sha
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import replay,query_histories
OUT=HERE/'learned_gate_repair_verification.json'

def main():
    if OUT.exists():raise FileExistsError(OUT)
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    assert not torch.cuda.is_available()
    before=time.monotonic();cpu=time.process_time()
    source=torch.load(HERE/'faded_guidance_weights.pt',weights_only=True,map_location='cpu')
    saved=torch.load(HERE/'learned_gate_repair_weights.pt',weights_only=True,map_location='cpu')
    results=json.loads((HERE/'learned_gate_repair_results.json').read_text(encoding='utf8'))
    assert results['complete']
    assert sha(HERE/'learned_gate_repair.py')==results['source_sha256']
    checks=[];late=[]
    for seed in SEEDS:
        for arm in ('original','answer_only','sparse_gate'):
            m=model(seed,saved[f'{seed}_{arm}'])
            changed=[k for k,v in m.state_dict().items() if not torch.equal(v,source[f'{seed}_8_linear_fade'][k])]
            assert all(k.startswith('gate.') for k in changed)
            hsh=hashlib.sha256(); predictions=[]; targets=[]; updated=[]; gates=[]
            with torch.no_grad():
                for start in (0,32):
                    x,y=batch(8,1040,32,9100000000+seed*100003+start*677)
                    # A new fact value must differ from the previous one.
                    g=torch.Generator().manual_seed(9200000000+seed+start)
                    slot=torch.randint(8,(32,),generator=g)
                    new=1-y[torch.arange(32),slot]
                    command=torch.stack((2+slot,10+new),1)
                    tail=torch.randint(22,30,(32,256),generator=g)
                    decoy=torch.randint(10,12,tail.shape,generator=g)
                    tail=torch.where(torch.rand(tail.shape,generator=g)<.25,decoy,tail)
                    xx=torch.cat((x,command,tail),1)
                    yy=y.clone();yy[torch.arange(32),slot]=new
                    assert torch.equal(replay(xx,8,2),yy)
                    pp,_,aux=forward(m,xx)
                    pred=pp.argmax(-1)
                    hsh.update(xx.numpy().tobytes());hsh.update(yy.numpy().tobytes())
                    predictions.extend(pred.tolist());targets.extend(yy.tolist())
                    updated.extend(pred[torch.arange(32),slot].eq(new).tolist())
                    gates.extend(aux[4][:,x.shape[1]+1].tolist())
                # Reloaded native predictions on the actual held-out long set.
                row=next(r for r in results['runs'] if r['seed']==seed and r['arm']==arm)
                expected=torch.tensor(row['eval'][2]['normal']['predictions'][:2])
                # Prefix body is batch-size-dependent in generator. Generate the
                # original chunk32 before selecting examples, for exact replay.
                xx,yy=batch(8,4096,32,7100000000+seed*100003)
                native=m(query_histories(xx[:2],8)).reshape(8,2,2).transpose(0,1)
                assert torch.equal(native.argmax(-1),expected)
                wide=forward(m.double(),xx[:2])[0]
                precision_error=float((wide-native.double()).abs().max())
                precision_same=bool(torch.equal(wide.argmax(-1),native.argmax(-1)))
            pp=torch.tensor(predictions);yy=torch.tensor(targets);same=pp.eq(yy)
            late.append(dict(seed=seed,arm=arm,histories=64,input_sha256=hsh.hexdigest(),
                 correct_records=int(same.all(1).sum()),correct_bits=int(same.sum()),
                 changed_fact_correct=sum(updated),late_write_gate_mean=sum(gates)/len(gates),
                 predictions=predictions,labels=targets))
            checks.append(dict(seed=seed,arm=arm,changed_tensors=changed,native_fresh_prediction_replay=True,
                 float64_long_max_logit_error=precision_error,float64_predictions_equal=precision_same))
            print('VERIFIED',seed,arm,late[-1]['correct_records'],late[-1]['changed_fact_correct'],flush=True)
    for seed in SEEDS:
        assert len({r['input_sha256'] for r in late if r['seed']==seed})==1
    original_hashes={n:sha(HERE/n)==s for n,s in results['original_hashes'].items()}
    assert all(original_hashes.values())
    # Correctly typed Windows peak-process-memory measurement.
    from ctypes import wintypes
    class PMC(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in
          ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
           'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
    api=ctypes.windll.kernel32;api.GetCurrentProcess.restype=wintypes.HANDLE
    getmem=ctypes.windll.psapi.GetProcessMemoryInfo
    getmem.argtypes=[wintypes.HANDLE,ctypes.POINTER(PMC),wintypes.DWORD]
    pm=PMC();pm.cb=ctypes.sizeof(pm)
    assert getmem(api.GetCurrentProcess(),ctypes.byref(pm),pm.cb)
    out=dict(checks=checks,late_write=late,original_files_unchanged=original_hashes,
        source_sha256=sha(Path(__file__)),cuda=False,cpu_threads=torch.get_num_threads(),
        wall_s=time.monotonic()-before,cpu_s=time.process_time()-cpu,
        peak_working_set_bytes=pm.PeakWorkingSetSize)
    OUT.write_text(json.dumps(out,indent=2),encoding='utf8')
    print('VERIFICATION_COMPLETE',out['wall_s'],out['cpu_s'],flush=True)
if __name__=='__main__':main()


