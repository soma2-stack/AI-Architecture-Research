"""Experiment 007 deterministic query-aware readout controls."""
import pytest
import torch

from prototypes.rnn_llm_architecture.experiment_007 import (
    AddressedReadout, Config, eval_frozen, fit_frozen, paired_prefix,
    paired_loss, score, state_features, train_joint, weight_digest)
from prototypes.rnn_llm_architecture.experiment_005 import make_variant
from prototypes.rnn_llm_architecture.experiment_002 import _slot_targets
from prototypes.rnn_llm_architecture.learning_pilot import make_batch


def test_two_query_output_and_counterfactual_scoring():
    head=AddressedReadout(5)
    features=torch.zeros(4,5)
    assert head(features).shape==(4,2,2)
    labels=torch.tensor([[0,0],[0,1],[1,0],[1,1]])
    logits=torch.tensor([[[9.,0.],[9.,0.]],[[9.,0.],[9.,0.]],[[0.,9.],[9.,0.]],[[0.,9.],[0.,9.]]])
    m=score(logits,labels)
    assert m['paired_both_accuracy']==.75
    assert m['paired_on_unequal']==.5
    assert torch.isfinite(paired_loss(logits,labels))


@pytest.mark.parametrize('variant,width', [('protected_w32',64),('gru_w32',64),('lstm_w32',128)])
def test_prefix_is_query_free_and_features_include_cell(variant,width):
    ids,_,_=make_batch('selective',4,6,seed=19)
    prefix,labels=paired_prefix(4,6,seed=19)
    assert torch.equal(prefix,ids[:,:-1])
    assert torch.equal(labels,_slot_targets(prefix,4))
    model=make_variant(variant,17)
    _,state=model(prefix)
    assert state_features(state,'all').shape==(6,width)
    assert state_features(state,'top').shape==(6,32)
    with pytest.raises(ValueError):state_features(state,'bad')


def test_frozen_reader_cannot_mutate_model():
    torch.set_num_threads(1)
    model=make_variant('protected_w32',17)
    before=weight_digest(model)
    cfg=Config(variants=('protected_w32',),seeds=(17,),delays=(4,),pretrain_steps=1,
               additional_steps=4,batch_size=2,head_examples=16,head_batch=8,eval_examples=8,max_wall_seconds=100)
    import time
    for kind in ('top','all'):
        head,norm,steps=fit_frozen(model,delay=4,seed=17,kind=kind,config=cfg,began=time.monotonic())
        assert steps==4
        assert weight_digest(model)==before
        measure=eval_frozen(model,head,norm,4,8,seed=999,kind=kind)
        assert 0<=measure['paired_on_unequal']<=1


def test_joint_training_updates_memory_and_decoder():
    import time
    torch.set_num_threads(1)
    model=make_variant('protected_w32',17)
    head=AddressedReadout(64)
    before=weight_digest(model)
    cfg=Config(variants=('protected_w32',),seeds=(17,),delays=(4,),pretrain_steps=1,
               additional_steps=2,batch_size=4,head_examples=16,head_batch=8,eval_examples=8,max_wall_seconds=100)
    done=train_joint(model,head,delay=4,seed=17,config=cfg,began=time.monotonic())
    assert done==2
    assert weight_digest(model)!=before


def test_bad_configs_and_shapes():
    with pytest.raises(ValueError):AddressedReadout(0)
    with pytest.raises(ValueError):AddressedReadout(3)(torch.zeros(2,1,3))
    with pytest.raises(ValueError):score(torch.zeros(4,2,2),torch.zeros(4,2,1,dtype=torch.long))
    for bad in ({'variants':('other',)},{'seeds':(-1,)},{'delays':(1,)},
                {'additional_steps':0},{'head_lr':float('nan')}):
        with pytest.raises(ValueError):Config(**bad)
