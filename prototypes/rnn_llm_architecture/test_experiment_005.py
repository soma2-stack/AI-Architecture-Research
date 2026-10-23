"""CPU-only mechanism experiment validation."""
import pytest
import torch
from prototypes.rnn_llm_architecture import experiment_005 as e


def test_variant_interface_and_explicit_state_gate():
    for variant in e.VARIANTS:
        m=e.make_variant(variant,17)
        logits,s=m(torch.randint(0,16,(2,4)))
        assert logits.shape==(2,4,16)
        assert torch.isfinite(logits).all()
    base=e.make_variant('protected_w32',17)
    sg=e.make_variant('state_gated_w32',17)
    assert sg.trainable_parameters==base.trainable_parameters+2*32*8
    for cell in sg.cells:assert torch.count_nonzero(cell.state_to_gate.weight)==0


def test_reproducibility_and_output_guard(tmp_path):
    cfg=e.Config(variants=('protected_w32','state_gated_w32'),seeds=(17,),train_delays=(2,),
                 steps=3,batch_size=4,eval_batch=16,max_wall_seconds=30)
    a=e.execute(cfg,output=tmp_path/'a.json')
    b=e.execute(cfg,output=tmp_path/'b.json')
    assert a['status']==b['status']=='complete'
    for x,y in zip(a['runs'],b['runs']):
        assert x['evaluation']==y['evaluation']
    assert a['runs'][1]['state_gate_weight_l2_by_layer'] is not None
    assert max(a['runs'][1]['state_gate_weight_l2_by_layer'])>0
    with pytest.raises(FileExistsError):e.execute(cfg,output=tmp_path/'a.json')


def test_config_rejects_invalid():
    with pytest.raises(ValueError):e.Config(variants=('bad',))
    with pytest.raises(ValueError):e.Config(train_delays=())
    with pytest.raises(ValueError):e.Config(max_wall_seconds=0)
