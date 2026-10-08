"""Shared architecture diagnostics on CPU, without fitting any parameters.

python -m prototypes.rnn_llm_architecture.validation --output /tmp/rnn-report.json
All sensitivities here are diagnostics, never robust learning-credit dimension.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import platform
import statistics
import time

import torch
from torch import Tensor

from .candidates import CandidateConfig, CandidateLanguageModel, ProtectedMemoryCell
from .model import RNNConfig, RNNLanguageModel
from .full_reference import (FrozenTanhReference, CorridorCreditEngine, FourSiteGeometry,
    early_capture_schedule, realize_four_site_history, orthonormal_probe_bank, survivor_walsh)


@dataclass(frozen=True)
class ValidationConfig:
    width: int = 32
    vocabulary: int = 97
    layers: int = 2
    channels: int = 8
    seed: int = 20261007
    horizons: tuple[int,...] = (1,16,64,256,1024)
    benchmark_steps: int = 64
    benchmark_batch: int = 2
    benchmark_repeats: int = 7


class RecurrentPath:
    """Common real-valued scan [batch,time,width], one state [batch,width].

For paths 1-3 this tests a single cell before token heads / LayerNorm.
Path 4 consumes raw controls with W=I. Same width/input does not assert
equivalent state semantics, parameter access, or matched token models.
"""
    def __init__(self, kind: str, config: ValidationConfig):
        self.kind,self.width = kind,config.width
        if kind == "theory":
            self.module = FrozenTanhReference(config.width)
        else:
            self.module = CandidateLanguageModel(CandidateConfig(vocab_size=config.vocabulary,
                width=config.width,layers=1,protected_channels=config.channels,
                cell_type=kind,seed=config.seed,precision="float64")).cells[0]

    def initial_state(self, batch):
        return torch.zeros(batch,self.width,dtype=torch.float64)

    def scan(self, inputs: Tensor, state: Tensor | None = None):
        h=self.initial_state(inputs.shape[0]) if state is None else state
        if self.kind == "theory":
            return torch.stack([self.module.scan(x,s) for x,s in zip(inputs,h)])
        prepared=self.module.prepare(inputs)
        for t in range(inputs.shape[1]):
            h=self.module.step(tuple(x[:,t] for x in prepared),h)
        return h


def parameter_inventory(module):
    """Unique registered parameters/buffers, measured tensor payload bytes."""
    return {"trainable_parameters_measured":sum(p.numel() for p in module.parameters() if p.requires_grad),
            "frozen_parameters_measured":sum(p.numel() for p in module.parameters() if not p.requires_grad),
            "buffer_values_measured":sum(p.numel() for p in module.buffers()),
            "parameter_bytes_measured":sum(p.numel()*p.element_size() for p in module.parameters()),
            "buffer_bytes_measured":sum(p.numel()*p.element_size() for p in module.buffers())}


def token_cost_estimate(config: CandidateConfig, *, batch=1, steps=1):
    """Dense MAC estimate; 2 MAC FLOPs, excluding gates/LN and memory traffic."""
    w,r,l,v=config.width,config.protected_channels,config.layers,config.vocab_size
    core=2*w*w
    if config.cell_type=='protected':
        core=3*w*w+(8 if config.project_fast else 6)*w*r
        if not config.slow_feedback: core+=2*w*r
    element=8 if config.precision=='float64' else 4
    return {"core_MAC_per_token_per_layer_estimate":core,
            "whole_model_MAC_per_token_estimate":l*core+v*w,
            "state_values_per_example":l*w,"state_bytes_per_example":l*w*element,
            "logits_payload_bytes_estimate":batch*steps*v*element,
            "hidden_history_payload_bytes_estimate":batch*steps*l*w*element,
            "complexity":"O(B T [L n^2 + V n + L n R]) arithmetic; O(B L n) persistent forward state",
            "excluded":"nonlinearities, normalizations, allocator/Python overhead, autograd tape and temporary projected sequences"}


def theoretical_cost_estimate(n: int, directions: int, *, split_renewal=True, actual_dense=False):
    r=n//2-1
    return {"forward_state_values":n,"fixed_source_physical_credit_values":n*directions,
            "selected_renewal_credit_values":(2 if split_renewal else 1)*r*directions,
            "feedback_row_values_each":directions,
            "public_operator_values_estimate":2*r+n,
            "dense_actual_buffer_values":n*n if actual_dense else 0,
            "reference_step_complexity":"O(n*p) arithmetic, O(n*p+n) streaming storage",
            "dense_actual_step_complexity":"O(n^2*p) arithmetic; O(n^2+n*p) storage" if actual_dense else "not selected",
            "full_selected_matrix_case":"p=r gives quadratic credit storage; no compression",
            "independent_parameter_direction_buffers":"full R/W directions additionally cost 2*p*n^2+p*n values",
            "offline_history":"realized inputs, states and gates add O(T*n); optional credit history adds O(T*r*p)",
            "formal_D":"not inferred"}


def cell_diagnostics(config: ValidationConfig):
    generator=torch.Generator().manual_seed(config.seed)
    inputs=.02*torch.randn(1,max(config.horizons),config.width,generator=generator,dtype=torch.float64)
    reader=torch.randn(config.width,generator=generator,dtype=torch.float64)
    reader=reader/reader.norm()
    results={}
    for kind in ('tanh','near_critical','protected','theory'):
        path=RecurrentPath(kind,config)
        full=path.scan(inputs); split=max(config.horizons)//3
        prefix=path.scan(inputs[:,:split]); chunk=path.scan(inputs[:,split:],prefix)
        row={**parameter_inventory(path.module),"state_bytes_measured":path.initial_state(1).numel()*8,
             "streaming_max_abs_error_measured":(full-chunk).abs().max().item(),
             "reset_reproducibility_max_abs_error_measured":(full-path.scan(inputs)).abs().max().item(),
             "max_abs_final_state_measured":full.abs().max().item(),"horizons":[]}
        for horizon in config.horizons:
            state=path.initial_state(1).requires_grad_()
            final=path.scan(inputs[:,:horizon],state)
            grad=torch.autograd.grad((final*reader).sum(),state)[0]
            row['horizons'].append({"steps":horizon,"initial_state_gradient_l2_measured":grad.norm().item(),
                  "all_finite":bool(torch.isfinite(final).all() and torch.isfinite(grad).all())})
        if kind=='near_critical':
            sv=torch.linalg.svdvals(path.module.recurrent)
            row['recurrent_singular_values_measured']={"min":sv.min().item(),"max":sv.max().item()}
        if kind=='theory':
            row['resource_estimate']=theoretical_cost_estimate(config.width,config.width//2-1)
        results[kind]=row
    return results


def protected_diagnostics(config: ValidationConfig):
    cell=RecurrentPath('protected',config).module
    generator=torch.Generator().manual_seed(config.seed+1)
    original=torch.randn(1,config.channels,generator=generator,dtype=torch.float64)
    h=cell.synthesize(original)
    mask=torch.zeros_like(original);mask[:,0]=1
    for _ in range(256):
        h=cell(torch.randn(1,config.width,generator=generator,dtype=torch.float64),h,write_mask=mask)
    final=cell.read_protected(h)
    return {"Walsh_Gram_max_abs_error_measured":(cell.masks@cell.masks.T-torch.eye(config.channels)).abs().max().item(),
            "closed_channel_drift_after_256_steps_measured":(final[:,1:]-original[:,1:]).abs().max().item(),
            "updated_channel_change_measured":(final[:,0]-original[:,0]).abs().max().item(),
            "claim":"only externally closed coefficient invariance; learned open-channel interference NOT YET TESTED"}


def token_benchmarks(config: ValidationConfig):
    generator=torch.Generator().manual_seed(config.seed+2)
    ids=torch.randint(config.vocabulary,(config.benchmark_batch,config.benchmark_steps),generator=generator)
    results={}
    for kind in ('tanh','near_critical','protected'):
        cfg=CandidateConfig(vocab_size=config.vocabulary,width=config.width,layers=config.layers,
                            protected_channels=config.channels,cell_type=kind,seed=config.seed)
        candidate=CandidateLanguageModel(cfg)
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(config.seed)
            original=RNNLanguageModel(RNNConfig(vocab_size=config.vocabulary,width=config.width,
                      layers=config.layers,protected_channels=config.channels,cell_type=kind))
        weights=candidate.state_dict()
        if kind=='protected': weights={k:(-v if '.slow_gate.' in k else v) for k,v in weights.items()}
        original.load_state_dict(weights)
        row={"config":asdict(cfg),"inventory":parameter_inventory(candidate),
             "resource_estimate":token_cost_estimate(cfg,batch=config.benchmark_batch,steps=config.benchmark_steps)}
        with torch.no_grad():
            difference=(candidate(ids)[0]-original(ids)[0]).abs().max().item()
            row['matched_weights_logits_max_abs_error_measured']=difference
            for name,model in (('original',original),('candidate',candidate)):
                for _ in range(2): model(ids)
                samples=[]
                for _ in range(config.benchmark_repeats):
                    start=time.perf_counter();model(ids);samples.append(time.perf_counter()-start)
                row[name+'_median_forward_seconds_measured']=statistics.median(samples)
        results[kind]=row
    return results


def theory_diagnostics():
    n,m=2048,8
    controls=torch.tensor([[1.,-.5],[-.2,.8]],dtype=torch.float64)
    schedule,phases,metadata=early_capture_schedule(n,m,controls,(1,2),write_steps=1,tail_steps=16,clear_steps=4)
    geometry=FourSiteGeometry(n,m,len(schedule))
    model=FrozenTanhReference(n)
    history=realize_four_site_history(model,geometry,schedule,phases=phases)
    other_schedule,_,_=early_capture_schedule(n,m,-controls,(1,2),write_steps=1,tail_steps=16,clear_steps=4)
    other=realize_four_site_history(model,geometry,other_schedule)
    probes=orthonormal_probe_bank(geometry,2)
    engine=CorridorCreditEngine(n)
    a=engine.scan(history.gates[1:,1:model.k],probes).response
    b=engine.scan(other.gates[1:,1:model.k],probes).response
    h,replay=model.scan(history.inputs,return_history=True)
    walsh=survivor_walsh(geometry,(1,2),geometry.interior_steps+1)
    # Two explicit legal queries (complementary patterns); no supremum search.
    physical=torch.zeros(n,2,dtype=torch.float64)
    physical[1:model.k]=model.sigma*math.sqrt(model.l)*(a-b)
    z=torch.full((1,n),.5,dtype=torch.float64)
    z[0,1:model.k][walsh[0]>0]=.25;z[0,1:model.k][walsh[0]<0]=.75
    answer=model.normalized_past_answer(physical,z)
    return {"history":history.cost(),"schedule":metadata,"realization":model.realization,
            "replay_max_abs_error_measured":(history.states-replay).abs().max().item(),
            "endpoint_pair_max_abs_error_measured":(history.states[-1]-other.states[-1]).abs().max().item(),
            "probe_Gram_max_abs_error_measured":(probes.T@probes-torch.eye(2)).abs().max().item(),
            "selected_sensitivity_pair_norm_measured":(a-b).norm().item(),
            "protected_read_pair_norm_measured":(walsh@(a-b)).norm().item(),
            "one_legal_query_pair_norm_measured":answer.norm().item(),
            "epsilon":.001,"margin_status":"finite witness; no robust section certified",
            "resource_estimate":theoretical_cost_estimate(n,2),
            "clear_status":"4 diagnostic steps; theorem-scale complementary clearing NOT CERTIFIED"}


def run_validation(config=ValidationConfig()):
    if config.width < 16 or config.width&(config.width-1) or not 1<=config.channels<=config.width//2:
        raise ValueError("shared validation needs power-of-two width>=16 and valid channel count")
    before_threads=torch.get_num_threads()
    torch.set_num_threads(1)
    try:
        start=time.perf_counter()
        report={"config":asdict(config),"environment":{"torch":torch.__version__,"python":platform.python_version(),
                    "device":"cpu","dtype_cell_diagnostics":"float64","dtype_token_benchmarks":"float32","threads":1},
                "scope":"Untrained CPU architecture diagnostics. No weight updates. Gradients/rank/state width are NOT formal D.",
                "cells":cell_diagnostics(config),"protected":protected_diagnostics(config),
                "tokens":token_benchmarks(config),"theory":theory_diagnostics()}
        report['wall_seconds_measured']=time.perf_counter()-start
        return report
    finally:
        torch.set_num_threads(before_threads)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    report=run_validation()
    report['source_sha256']={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
              for name in ('candidates.py','full_reference.py','validation.py','model.py','theory_reference.py')}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({"output":str(args.output),"wall_seconds":report['wall_seconds_measured'],
                      "training_executed":False,"formal_D":"NOT CERTIFIED"}))


if __name__=='__main__':
    main()
