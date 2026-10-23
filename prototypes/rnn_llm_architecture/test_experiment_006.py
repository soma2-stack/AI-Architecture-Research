"""Focused unit tests of truly frozen two-slot memory-state probes."""
import torch
import pytest

from prototypes.rnn_llm_architecture.experiment_006 import (Config,build_probe,extract_features,fit_probe,
    flatten_recurrent_state,score_pair,train_model)
from prototypes.rnn_llm_architecture.experiment_005 import make_variant
from prototypes.rnn_llm_architecture.learning_pilot import make_batch
from prototypes.rnn_llm_architecture.experiment_002 import _slot_targets


def test_feature_shape_and_lstm_cell_included():
    a=torch.ones(3,4)
    assert flatten_recurrent_state((a,)).shape == (3,4)
    assert flatten_recurrent_state(((a,2*a),)).shape == (3,8)
    with pytest.raises(TypeError):
        flatten_recurrent_state(((a,4),))


@pytest.mark.parametrize('kind',('protected_w32','state_gated_w32','gru_w32','lstm_w32'))
def test_prefix_streaming_stage_features(kind):
    m=make_variant(kind,17)
    data,_,_=make_batch('selective',4,5,seed=213)
    features,labels=extract_features(m,4,5,seed=213,chunk=2)
    assert labels.shape==(5,2)
    assert torch.equal(labels,_slot_targets(data[:,:-1],4))
    for f in features.values():
        assert f.shape==(5,128 if kind=='lstm_w32' else 64)
        assert not f.requires_grad
        assert torch.isfinite(f).all()
    with torch.no_grad():
        full_state=flatten_recurrent_state(m(data[:,:-1])[1])
    assert torch.allclose(full_state,features['after_distractors'],rtol=2e-5,atol=2e-6)
    assert not torch.equal(features['after_update'],features['after_distractors'])


def test_probe_scores_separate_unequal_and_equal():
    labels=torch.tensor([[0,0],[0,1],[1,0],[1,1]])
    logits=torch.tensor([[9.,0.,9.,0.],[9.,0.,9.,0.],[0.,9.,9.,0.],[0.,9.,0.,9.]])
    d=score_pair(logits,labels)
    assert d['paired_both_accuracy']==.75
    assert d['paired_on_unequal']==.5
    assert d['paired_on_equal']==1.


def test_probe_does_not_mutate_frozen_state_and_scores_heldout():
    torch.manual_seed(21)
    x=torch.randn(128,4)
    y=torch.stack(( (x[:,0]>0).long(), (x[:,1]>0).long()),dim=1)
    t=torch.randn(64,4)
    truth=torch.stack(((t[:,0]>0).long(),(t[:,1]>0).long()),dim=1)
    old=x.clone()
    for kind in ('linear','mlp'):
        r=fit_probe(x,y,t,truth,kind=kind,seed=2,steps=70,batch_size=32,lr=.02)
        assert 0 <= r['held_out']['paired_on_unequal']<=1
        assert r['held_out']['paired_both_accuracy']>.50
    assert torch.equal(old,x)
    with pytest.raises(ValueError):
        fit_probe(x.requires_grad_(),y,t,truth,kind='linear',seed=2,steps=2,batch_size=32,lr=.02)


def test_config_input_validation():
    for invalid in ({'variants':('madeup',)},{'seeds':(-1,)},{'delays':(0,)},{'probe_batch':0},{'probe_lr':float('nan')}):
        with pytest.raises(ValueError):Config(**invalid)
