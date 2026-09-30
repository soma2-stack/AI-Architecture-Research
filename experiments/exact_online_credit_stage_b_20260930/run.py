"""Locked Stage-B sweep. Each phase refuses to overwrite existing results."""
import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path
import numpy as np
import torch
import core as c
import structures as s

def cases(width):
    configs=[]
    depths=c.CFG['depths'] if width==8 else c.CFG['width16_depths']
    for family in ('block','lowrank'):
        interactions=c.CFG['blocks' if family=='block' else 'ranks'] if width==8 else c.CFG['width16_blocks' if family=='block' else 'width16_ranks']
        for interaction in interactions:
            for depth in depths:
                configs.append({'axis':family,'family':family,'interaction':interaction,'depth':depth,'mode':'stack_nonlinear','linear_shared':False})
    if width==8:
        configs += [{'axis':'mix','family':'block','interaction':1,'depth':1,'mode':mode,'linear_shared':False} for mode in c.CFG['mix_modes']]
    configs.append({'axis':'positive','family':'block','interaction':1,'depth':1,'mode':'none','linear_shared':True})
    for config in configs:
        for T in c.CFG['horizons']:
            for seed in c.CFG['seeds']:yield {'n':width,'T':T,'seed':seed,**config}

def key(config):
    return f"n{config['n']}_{config['axis']}{config['interaction']}_d{config['depth']}_{config['mode']}_T{config['T']}_s{config['seed']}"

def create(config):return c.Model(config['n'],config['depth'],config['family'],config['interaction'],config['seed'],config['mode'],config['linear_shared'])

def gate(model,result,reference,trajectory,before,intended_exact=False,S=None):
    assert c.digest(model.theta)==before,'Parameters changed'
    assert torch.isfinite(result['gradient']).all() and torch.isfinite(result['trajectory']).all()
    assert result['gradient'].device.type=='cpu'
    trajectory_error=float((result['trajectory']-trajectory).abs().max())
    assert trajectory_error<=c.CFG['trajectory_absolute_tolerance'],'Different forward trajectory'
    groups=c.grouped(model,result['gradient'],reference['gradient'])
    reconstruction=None
    if S is not None:
        assert torch.isfinite(result['S']).all()
        reconstruction=c.metric(result['S'],S)
    exact=all(c.passes(g) for g in groups) and (reconstruction is None or c.passes(reconstruction))
    if intended_exact:assert exact,'Intended exact method failed derivative-equivalence gate'
    return groups,reconstruction,exact,trajectory_error

def measured_case(config,meter):
    meter.check();cpu_start=time.process_time();start=time.perf_counter()
    model=create(config);x,q,y=c.data(config['seed'],config['T'],model.n);before=c.digest(model.theta);input_before=c.digest(x)
    trajectory,inference_time=c.inference(model,x)
    inference_times=[inference_time]+[c.inference(model,x)[1] for _ in range(c.CFG['timing_repeats']-1)]
    inference_time=float(np.median(inference_times))
    assert float(trajectory.abs().max())<c.CFG['maximum_absolute_state']
    assert abs(float(q@model.output(trajectory[-1],model.theta)-y))>c.CFG['minimum_terminal_error']
    reference=c.bptt(model,x,q,y);full=c.rtrl(model,x,q,y,snapshot=True)
    gate(model,full,reference,trajectory,before,True)
    Agraph,Bgraph,closure,masks=c.graphs(model)
    result={'id':key(config),**config,'P':model.P,'N':model.N,'full_capacity':model.N*model.P,
            'parameter_hash':before,'input_hash':input_before,'q_hash':c.digest(q),'y':float(y),
            'trajectory_hash':c.digest(trajectory),'maximum_state':float(trajectory.abs().max()),
            'graph_closure_values':int(closure.sum()),'snap_masks_values':{k:int(v.sum()) for k,v in masks.items()},
            'audit_graph_metadata_bytes':sum(v.nbytes for v in (Agraph,Bgraph,closure,*masks.values())),
            'audit_snapshot_scalars':full['audit_snapshot_scalars'],'inference_seconds':inference_time,
            'inference_seconds_per_step':inference_time/len(x),'methods':[],
            'checkpoints':{str(t):s.support(model,matrix) for t,matrix in full['checkpoints'].items()},
            'compression':s.compression(model,full['S'],trajectory[-1],q,y,reference['gradient'])}
    functions=[('BPTT',lambda:c.bptt(model,x,q,y),True),('RTRL',lambda:c.rtrl(model,x,q,y),True)]
    for name,mask in masks.items():functions.append((name,lambda mask=mask:c.packed_run(model,x,q,y,mask),name=='packed_exact' or np.array_equal(mask,closure)))
    if config['linear_shared']:functions.append(('shared_exact',lambda:c.shared_run(model,x,q,y),True))
    if config['family']=='lowrank' and config['interaction'] in (0,1,8) and config['depth'] in (1,3):
        functions.append(('online_svd_factor',lambda:s.factor_run(model,x,q,y),True))
    if model.n==8 and model.depth==1 and len(x)==32 and config['axis'] in ('block','lowrank') and ((model.family=='block' and model.interaction in (1,8)) or (model.family=='lowrank' and model.interaction in (0,1))):
        functions.append(('online_kronecker_sum',lambda:s.kronecker_sum_run(model,x,q,y),True))
    for name,fn,intended in functions:
        times=[];cpu_times=[];derivative_times=[]
        for repeat in range(c.CFG['timing_repeats']):
            meter.check();value=fn()
            groups,reconstruction,exact,trajectory_error=gate(model,value,reference,trajectory,before,intended,None if name=='BPTT' else full['S'])
            times.append(value['seconds']);cpu_times.append(value['cpu_seconds']);derivative_times.append(value['derivative_seconds'])
        row={k:v for k,v in value.items() if k not in ('gradient','trajectory','S','checkpoints','seconds','derivative_seconds','cpu_seconds')}
        row.update({'method':name,'intended_exact':bool(intended),'exact_gate_passed':exact,'groups':groups,'reconstruction':reconstruction,
                    'trajectory_error':trajectory_error,'seconds':float(np.median(times)),'repeat_seconds':times,
                    'cpu_seconds':float(np.median(cpu_times)),'derivative_seconds':float(np.median(derivative_times)),
                    'derivative_seconds_per_step':float(np.median(derivative_times))/len(x),
                    'derivative_to_inference_ratio':float(np.median(derivative_times))/inference_time,
                    'total_to_inference_ratio':float(np.median(times))/inference_time,
                    'all_stored_numbers':value['stored_derivative_scalars']+value.get('index_bytes',0)//8})
        result['methods'].append(row)
    assert c.digest(x)==input_before and c.digest(model.theta)==before
    (c.ROOT/'matrices').mkdir(exist_ok=True)
    np.savez_compressed(c.ROOT/'matrices'/f"{result['id']}.npz",S=full['S'].numpy(),theta=model.theta.numpy(),x=x.numpy(),q=q.numpy(),y=y.numpy())
    result.update({'process_peak_rss_bytes':meter.peak,'case_cpu_seconds_including_diagnostics':time.process_time()-cpu_start,
                   'case_wall_seconds_including_diagnostics':time.perf_counter()-start})
    return result

def sweep(width):
    meter=c.Meter(f'official width{width} sweep');info=c.hardware()
    path=c.ROOT/f'raw_width{width}.jsonl';assert not path.exists(),'Never overwrite prior results'
    if width==16:
        assert json.loads((c.ROOT/'status_width8.json').read_text())=={'complete':True,'valid':True,'cases':330}
    provenance={'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'hardware':info,
                'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in c.ROOT.iterdir() if p.suffix in ('.py','.md') or p.name=='config.json'}}
    (c.ROOT/f'provenance_width{width}.json').write_text(json.dumps(provenance,indent=2))
    completed=0
    try:
        for config in cases(width):
            result=measured_case(config,meter)
            with path.open('a') as f:f.write(json.dumps(result,allow_nan=False)+'\n')
            completed+=1
            if completed%10==0:print(f'width{width}: {completed} cases passed; process CPU {time.process_time():.2f}s',flush=True)
        (c.ROOT/f'status_width{width}.json').write_text(json.dumps({'complete':True,'valid':True,'cases':completed},indent=2))
    except Exception as error:
        (c.ROOT/f'status_width{width}.json').write_text(json.dumps({'complete':False,'valid':False,'cases':completed,'reason':repr(error)},indent=2));raise
    finally:meter.finish()

def family():
    meter=c.Meter('sensitivity family diagnostics');c.hardware()
    path=c.ROOT/'family.jsonl';assert not path.exists()
    assert json.loads((c.ROOT/'status_width16.json').read_text())['valid']
    (c.ROOT/'family_matrices').mkdir(exist_ok=True)
    try:
        for family,interaction,depth in c.CFG['family_selected']:
            pooled=[]
            for seed in c.CFG['seeds']:
                model=c.Model(8,depth,family,interaction,seed);before=c.digest(model.theta);matrices=[];input_hashes=[];errors=[]
                for stream in c.CFG['family_streams']:
                    meter.check();x,q,y=c.data(seed,c.CFG['family_horizon'],8,stream)
                    reference=c.bptt(model,x,q,y);full=c.rtrl(model,x,q,y)
                    groups,_,_,_=gate(model,full,reference,reference['trajectory'],before,True)
                    matrices.append(full['S'].numpy());input_hashes.append(c.digest(x));errors.append(max(g['relative_error'] for g in groups))
                stacked=np.stack(matrices);pooled.extend(matrices)
                flat=torch.tensor(stacked.reshape(len(stacked),-1));centered=flat-flat.mean(dim=0)
                row={'family':family,'interaction':interaction,'depth':depth,'seed':seed,'samples':len(matrices),'dimension_cap':len(matrices)-1,
                     'parameter_hash':before,'input_hashes':input_hashes,'maximum_reference_relative_error':max(errors),**s.rank_info(centered)}
                with path.open('a') as f:f.write(json.dumps(row,allow_nan=False)+'\n')
                np.savez_compressed(c.ROOT/'family_matrices'/f'{family}{interaction}_d{depth}_s{seed}.npz',S=stacked)
            flat=torch.tensor(np.stack(pooled).reshape(len(pooled),-1));centered=flat-flat.mean(dim=0)
            with path.open('a') as f:f.write(json.dumps({'family':family,'interaction':interaction,'depth':depth,'seed':'pooled_parameter_settings','samples':len(pooled),'dimension_cap':len(pooled)-1,**s.rank_info(centered)})+'\n')
            print(f'family {family}{interaction} depth{depth}: fixed-parameter and pooled spans recorded',flush=True)
        (c.ROOT/'status_family.json').write_text(json.dumps({'complete':True,'valid':True,'official_derivative_cases':360},indent=2))
    finally:meter.finish()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=['width8','width16','family'],required=True)
    phase=parser.parse_args().phase
    if phase=='family':family()
    else:sweep(8 if phase=='width8' else 16)
