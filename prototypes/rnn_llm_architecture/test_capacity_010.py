"""Small deterministic task, replay, output, and bounded-training checks for Exp010."""
from pathlib import Path
import json
import pytest
import torch
from .capacity_010 import (generator_batch,replay,metrics,query_histories,DeltaRule,
                           predictions,Config,execute,VALUE_START,WRITE_START,QUERY_START,
                           FILLER_START,last_marked_value)

@pytest.mark.parametrize('slots', [2,4,8])
@pytest.mark.parametrize('values', [2,4])
def test_generator_and_independent_reference(slots,values):
    x=generator_batch(slots,values,64,24,seed=1234+slots+values)
    assert x.shape==(24,slots*2+64)
    y=replay(x,slots,values)
    assert y.shape==(24,slots)
    assert (0<=y).all() and (y<values).all()
    initial=x[:,1:slots*2:2]-VALUE_START
    orig_order=x[:,:slots*2:2]-WRITE_START
    assert initial.gather(1,orig_order.argsort(1)).shape == y.shape  # all slots initialized
    assert torch.equal(x,generator_batch(slots,values,64,24,seed=1234+slots+values))
    assert not torch.equal(x,generator_batch(slots,values,64,24,seed=777))
    ids=query_histories(x,slots)
    assert ids.shape==(24*slots,2*slots+65)
    for s in range(slots):
        assert (ids[s*24:(s+1)*24,-1]==QUERY_START+s).all()
        assert torch.equal(ids[s*24:(s+1)*24,:-1],x)


def test_manual_semantics_and_unmarked_values():
    x=torch.tensor([[WRITE_START,VALUE_START,WRITE_START+1,VALUE_START+1,
                     FILLER_START,VALUE_START+3,WRITE_START,VALUE_START+2,
                     VALUE_START+1,QUERY_START]])
    # query token in prefix is harmless and does not rewrite memory.
    assert replay(x,2,4).tolist()==[[2,1]]
    assert last_marked_value(x,2,4).tolist()==[2]
    assert metrics(torch.tensor([[2,1]]),torch.tensor([[2,1]]),4)['whole_varied']==1
    assert metrics(torch.tensor([[2,2]]),torch.tensor([[2,1]]),4)['whole_varied']==0


def test_invalid_config_and_args():
    with pytest.raises(ValueError): generator_batch(3,2,64,3,seed=17)
    with pytest.raises(ValueError): generator_batch(4,3,64,3,seed=17)
    with pytest.raises(ValueError): generator_batch(8,4,3,3,seed=17)
    with pytest.raises(ValueError): Config(variants=('bad',))
    with pytest.raises(ValueError): Config(tasks=((3,2),))
    with pytest.raises(ValueError): Config(seeds=(17,17))


def test_delta_rule_learns_and_gradients():
    model=DeltaRule(4,4,17)
    x=generator_batch(4,4,16,6,seed=83)
    y=replay(x,4,4)
    scores=predictions(model,x,4,4)
    assert scores.shape==(6,4,4)
    loss=torch.nn.functional.cross_entropy(scores.reshape(-1,4),y.reshape(-1))
    loss.backward()
    assert torch.isfinite(loss)
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())


def test_small_bounded_run(tmp_path):
    p=tmp_path/'pilot.json'
    cfg=Config(variants=('delta_rule',),tasks=((2,2),),seeds=(17,),steps=2,
               delay=8,eval_delays=(8,16),batch=4,eval_batch=12,eval_every=1,max_wall_seconds=30)
    report=execute(cfg,p)
    assert report['status']=='complete'
    assert len(report['runs'])==1 and report['runs'][0]['steps']==2
    assert json.loads(p.read_text())['status']=='complete'
    with pytest.raises(FileExistsError):execute(cfg,p)
