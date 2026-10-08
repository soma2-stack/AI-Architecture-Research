"""CPU-only protocol and regression checks; no lengthy training invoked."""
import json
import pytest
import torch
from prototypes.rnn_llm_architecture import experiment_003 as e


def test_marked_label_balancing_and_no_leak():
    for regime in e.EVAL_REGIMES:
        for delay in (16,64,256):
            ids,y,meta=e.make_batch(regime,delay,512,seed=13)
            assert ids.shape==(512,delay+3)
            assert int(y.sum())==256
            assert torch.equal(ids[:,0],torch.full((512,),e.STORE))
            assert torch.equal(ids[:,1],y+e.BIT0)
            assert torch.all(ids[:,-1]==e.QUERY)
            assert torch.equal(ids[:,:2],e.make_batch(regime,delay,512,seed=13)[0][:,:2])
            if regime=='benign':assert meta['bit_noise_fraction']==0
            if regime=='all_bits':
                assert meta['bit_noise_fraction']==1
                assert meta['conflicting_noise_fraction']>0.99
            if regime=='interfering':
                assert .45<meta['bit_noise_fraction']<.55
                assert meta['conflicting_noise_fraction']>.95


def test_interference_is_not_position_or_last_bit_shortcut():
    ids,y,_=e.make_batch('interfering',64,4096,seed=44)
    noise=ids[:,2:-1]
    # Last encountered bit token is independent of the initial marked bit.
    is_bit=(noise==e.BIT0)|(noise==e.BIT1)
    positions=torch.arange(noise.shape[1]).expand_as(noise)
    last=torch.where(is_bit,positions,-1).max(1).values
    pred=noise[torch.arange(len(y)),last]-e.BIT0
    assert .47<float((pred==y).float().mean())<.53


def test_comparison_model_shapes_and_determinism():
    for name in e.VARIANTS:
        m=e.build(name,17)
        ids,y,_=e.make_batch('interfering',2,2,seed=22)
        logits,state=m(ids)
        assert logits.shape==(2,5,16)
        assert torch.isfinite(logits).all()
        assert m.trainable_parameters>0
    x1,y1,z1=e.make_batch('interfering',23,50,seed=42)
    x2,y2,z2=e.make_batch('interfering',23,50,seed=42)
    assert torch.equal(x1,x2) and torch.equal(y1,y2) and z1==z2


def test_small_pilot_reproducible_no_overwrite(tmp_path):
    cfg=e.Config(variants=('tanh_w32','protected_w32'),regimes=('interfering',),
       seeds=(17,),train_delay=2,eval_delays=(2,4),steps=3,batch_size=8,eval_batch=16,max_wall_seconds=30)
    a=e.execute(cfg,output=tmp_path/'a.json');b=e.execute(cfg,output=tmp_path/'b.json')
    assert a['status']==b['status']=='complete'
    assert len(a['runs'])==2
    for x,y in zip(a['runs'],b['runs']):assert x['metrics']==y['metrics']
    with pytest.raises(FileExistsError):e.execute(cfg,output=tmp_path/'a.json')


def test_config_rejects_invalid():
    with pytest.raises(ValueError):e.Config(variants=('not_a_model',))
    with pytest.raises(ValueError):e.Config(regimes=('all_bits',))
    with pytest.raises(ValueError):e.Config(eval_delays=())
