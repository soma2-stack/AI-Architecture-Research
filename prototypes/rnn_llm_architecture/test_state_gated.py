"""CPU structural and gradient tests for a state-conditioned protected cell."""
import torch
import pytest
from prototypes.rnn_llm_architecture.candidates import CandidateConfig,CandidateLanguageModel
from prototypes.rnn_llm_architecture.state_gated import StateGatedProtectedCell,StateGatedProtectedLanguageModel


def make(seed=17):
    cfg=CandidateConfig(vocab_size=16,width=32,layers=2,protected_channels=8,
                        cell_type='protected',seed=seed,precision='float64')
    return cfg,StateGatedProtectedLanguageModel(cfg)


def test_zero_state_gate_exactly_matches_baseline():
    cfg,new=make()
    baseline=CandidateLanguageModel(cfg)
    ids=torch.randint(0,16,(2,8))
    a,ha=baseline(ids);b,hb=new(ids)
    torch.testing.assert_close(a,b,atol=1e-12,rtol=1e-12)
    for x,y in zip(ha,hb):torch.testing.assert_close(x,y,atol=1e-13,rtol=1e-13)
    assert all(torch.count_nonzero(cell.state_to_gate.weight)==0 for cell in new.cells)
    assert new.trainable_parameters==baseline.trainable_parameters+2*32*8


def test_state_gate_gradients_and_chunking():
    _,model=make();ids=torch.randint(0,16,(2,7))
    full,ss=model(ids);left,h=model(ids[:,:3]);right,t=model(ids[:,3:],h)
    torch.testing.assert_close(full,torch.cat((left,right),dim=1),atol=1e-12,rtol=1e-12)
    loss=full[:,-1,2].sum()
    grads=torch.autograd.grad(loss,[cell.state_to_gate.weight for cell in model.cells])
    assert all(torch.isfinite(g).all() and float(g.abs().sum())>0 for g in grads)


def test_closed_writes_stay_invariant_with_state_gate():
    cfg=CandidateConfig(width=32,protected_channels=8,cell_type='protected',precision='float64')
    cell=StateGatedProtectedCell(cfg)
    with torch.no_grad():cell.state_to_gate.weight.fill_(.03)
    coeff=torch.randn(2,8,dtype=torch.float64)
    h=cell.synthesize(coeff)
    mask=torch.zeros((2,8),dtype=torch.float64);mask[:,0]=1
    for _ in range(48):h=cell(torch.randn(2,32,dtype=torch.float64),h,write_mask=mask)
    torch.testing.assert_close(cell.read_protected(h)[:,1:],coeff[:,1:],atol=1e-12,rtol=1e-12)


def test_state_conditioning_has_actual_effect():
    cfg=CandidateConfig(width=32,protected_channels=8,cell_type='protected',precision='float64')
    cell=StateGatedProtectedCell(cfg)
    x=torch.randn(2,32,dtype=torch.float64);h=torch.randn(2,32,dtype=torch.float64)
    before=cell(x,h)
    with torch.no_grad():cell.state_to_gate.weight.fill_(.05)
    after=cell(x,h)
    assert not torch.allclose(before,after,atol=1e-8)


def test_bad_configuration_rejected():
    with pytest.raises(ValueError):StateGatedProtectedCell(CandidateConfig(width=32,cell_type='tanh'))
