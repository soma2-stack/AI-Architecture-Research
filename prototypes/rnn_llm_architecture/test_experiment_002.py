"""Experiment 002: CPU-only generators, counterfactual evaluator and guards."""
import json
import pytest
import torch
from torch import nn

from prototypes.rnn_llm_architecture import experiment_002 as exp
from prototypes.rnn_llm_architecture.learning_pilot import make_batch, BIT0


def test_counterfactual_targets_and_replay():
    for delay in (1,16,64,128):
        ids,labels,meta=make_batch('selective',delay,512,seed=41)
        slots=exp._slot_targets(ids[:,:-1],delay)
        assert slots.shape==(512,2)
        assert torch.equal(slots.gather(1,meta['query_slot'][:,None])[:,0],labels)
        assert abs(float((slots[:,0]!=slots[:,1]).float().mean())-.5)<.07


def test_repeated_same_prefix_probes_need_both_answers():
    class LastWrite(nn.Module):
        def forward(self,ids):
            delay=ids.shape[1]-7
            last=ids[:,5+delay//2]-BIT0
            logits=torch.zeros(ids.shape[0],ids.shape[1],16)
            logits[torch.arange(ids.shape[0]),-1,BIT0+last]=1
            return logits,None
    model=LastWrite()
    res=exp.paired_selective_eval(model,64,seed=42,batch=2000)
    assert .46<res['paired_both_accuracy']<.54
    assert res['paired_on_unequal']==0.0
    assert res['updated_accuracy']==1.0
    assert .46<res['untouched_accuracy']<.54
    assert res['paired_both_accuracy']==res['naive_last_write_paired_accuracy']


def test_model_configs_parameter_budget_and_forget_bias():
    p=exp.build('protected_w32',17)
    g=exp.build('gru_w24',17)
    l=exp.build('lstm_w20',17)
    counts=[sum(q.numel() for q in m.parameters() if q.requires_grad) for m in (p,g,l)]
    assert counts==[7504,7728,7160]
    f=exp.build('lstm_forget_w32',17)
    for cell in f.cells:
        n=cell.hidden_size
        assert torch.equal(cell.bias_ih[n:2*n],torch.ones(n))
        assert torch.equal(cell.bias_hh[n:2*n],torch.zeros(n))
    assert exp.build('protected_random_w32',17).config.protected_basis=='random_orthogonal'
    assert exp.build('protected_no_project_w32',17).config.project_fast is False
    assert exp.build('protected_no_retain_w32',17).config.retain_slow is False


def test_paired_counterfactual_actual_model():
    model=exp.build('protected_w32',17)
    p=exp.paired_selective_eval(model,16,seed=222,batch=16)
    assert 0<=p['paired_both_accuracy']<=1
    assert 0<=p['updated_accuracy']<=1
    assert 0<=p['untouched_accuracy']<=1
    assert p['paired_both_accuracy']<=min(p['updated_accuracy'],p['untouched_accuracy'])


def test_bounded_pilot_deterministic_and_no_overwrite(tmp_path):
    cfg=exp.Config(variants=('tanh_w32','protected_w32','gru_w24'),tasks=('delayed',),
                   seeds=(17,),train_delay=2,eval_delays=(2,4),steps=3,batch_size=8,eval_batch=16,max_wall_seconds=30)
    a=tmp_path/'a.json';b=tmp_path/'b.json'
    first=exp.execute(cfg,output=a)
    second=exp.execute(cfg,output=b)
    assert first['status']==second['status']=='complete'
    assert len(first['runs'])==3
    for x,y in zip(first['runs'],second['runs']):
        assert x['evaluation']==y['evaluation']
    assert json.loads(a.read_text())['runs'][0]['variant']=='tanh_w32'
    with pytest.raises(FileExistsError):exp.execute(cfg,output=a)


def test_config_guard():
    with pytest.raises(ValueError):exp.Config(variants=('bad',))
    with pytest.raises(ValueError):exp.Config(variants=('gru_w32','gru_w32'))
    with pytest.raises(ValueError):exp.Config(max_wall_seconds=0)
