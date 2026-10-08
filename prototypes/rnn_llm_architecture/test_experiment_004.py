"""Architecture-independent dual-query memory objective checks."""
import pytest
import torch
from prototypes.rnn_llm_architecture import experiment_004 as e
from prototypes.rnn_llm_architecture.experiment_002 import _slot_targets
from prototypes.rnn_llm_architecture.learning_pilot import make_batch,QUERY_A,QUERY_B


def test_dual_queries_are_identical_up_to_final_token():
    for delay in (1,16,64):
        x,y,meta=e._paired_inputs(delay,256,seed=18)
        a,b=x[:256],x[256:]
        assert torch.equal(a[:,:-1],b[:,:-1])
        assert torch.all(a[:,-1]==QUERY_A)
        assert torch.all(b[:,-1]==QUERY_B)
        assert torch.equal(y[:256],_slot_targets(a[:,:-1],delay)[:,0])
        assert torch.equal(y[256:],_slot_targets(b[:,:-1],delay)[:,1])
        assert .40<float((y[:256]!=y[256:]).float().mean())<.60


def test_dual_loss_backprop_to_actual_candidate():
    model=e.build('protected_w32',17)
    loss=e.paired_query_loss(model,4,8,seed=18)
    loss.backward()
    assert torch.isfinite(loss)
    assert model.embedding.weight.grad is not None
    assert model.embedding.weight.grad.abs().sum()>0


def test_short_training_determinism_and_guards(tmp_path):
    cfg=e.Config(variants=('tanh_w32','gru_w24'),seeds=(17,),train_delay=4,
                 eval_delays=(4,8),steps=3,batch_size=8,eval_batch=16,max_wall_seconds=30)
    a=e.execute(cfg,output=tmp_path/'a.json')
    b=e.execute(cfg,output=tmp_path/'b.json')
    assert a['status']==b['status']=='complete'
    assert len(a['runs'])==2
    for x,y in zip(a['runs'],b['runs']):assert x['evaluation']==y['evaluation']
    with pytest.raises(FileExistsError):e.execute(cfg,output=tmp_path/'a.json')


def test_invalid_config():
    with pytest.raises(ValueError):e.Config(variants=('bad',))
    with pytest.raises(ValueError):e.Config(eval_delays=())
    with pytest.raises(ValueError):e.Config(max_wall_seconds=0)
