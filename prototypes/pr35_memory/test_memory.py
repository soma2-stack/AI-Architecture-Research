"""Mechanism, integration and benchmark validity tests; no costly training."""
import copy
import torch
import pytest
from .model import BalancedPairLanguageModel, BalancedPairCell
from .run import batch, logits, build, matched_width, count, jobs
from .precision import diagnostics

@pytest.mark.parametrize("width",(16,32,64))
def test_balance_and_compressed_equivalence(width):
    torch.manual_seed(5)
    c=BalancedPairCell(width).double()
    x=torch.randn(3,width,dtype=torch.float64)
    fast=torch.randn(3,c.fast,dtype=torch.float64)
    p=torch.randn(3,c.pairs,dtype=torch.float64)
    h=torch.cat((fast,p,-p),-1)
    new=c(x,h)
    nf,np=c.compressed_step(c.prepare(x),fast,p)
    torch.testing.assert_close(new,torch.cat((nf,np,-np),-1),atol=1e-14,rtol=1e-14)
    assert torch.equal(new[:,c.fast:c.fast+c.pairs],-new[:,c.fast+c.pairs:])
    # Every rank-one all-ones matrix annihilates balanced memory differences.
    v=torch.cat((torch.zeros_like(fast),p,-p),-1)
    assert torch.max((v@torch.ones(width,1,dtype=torch.float64)).abs())<1e-14

@pytest.mark.parametrize("variant",("pair_shared","pair_direct","pair_contract","pair_no_retain"))
def test_stream_reset_and_gradients(variant):
    model=BalancedPairLanguageModel(16,17,variant).double()
    ids=torch.tensor([[2,10,22,23,14],[3,11,24,25,15]])
    whole,state=model(ids)
    first,s=model(ids[:,:2]);last,end=model(ids[:,2:],s)
    torch.testing.assert_close(whole,torch.cat((first,last),1))
    torch.testing.assert_close(state[0],end[0])
    reset=torch.zeros_like(ids,dtype=torch.bool);reset[:,2]=True
    out,_=model(ids,reset_mask=reset)
    fresh,_=model(ids[:,2:])
    torch.testing.assert_close(out[:,2:],fresh)
    whole.sum().backward()
    grads=[p.grad for p in model.parameters() if p.grad is not None]
    assert grads and all(torch.isfinite(g).all() for g in grads)
    assert any(g.abs().max()>0 for g in grads)
    empty,es=model(ids[:,:0],state)
    assert empty.shape==(2,0,32)
    torch.testing.assert_close(es[0],state[0])

def test_finite_difference_input_gradient():
    torch.manual_seed(2)
    cell=BalancedPairCell(16).double()
    x=torch.randn(2,16,dtype=torch.float64,requires_grad=True)
    h=torch.randn(2,16,dtype=torch.float64)
    f=cell(x,h).square().sum()
    derivative=torch.autograd.grad(f,x)[0][0,3]
    with torch.no_grad():
        xp=x.clone();xm=x.clone();xp[0,3]+=1e-6;xm[0,3]-=1e-6
        numeric=(cell(xp,h).square().sum()-cell(xm,h).square().sum())/(2e-6)
    torch.testing.assert_close(derivative,numeric,atol=1e-7,rtol=1e-6)

def test_seed_reproducible_and_global_rng_unchanged():
    torch.manual_seed(99);before=torch.random.get_rng_state()
    a=BalancedPairLanguageModel(16,17);b=BalancedPairLanguageModel(16,17)
    assert torch.equal(before,torch.random.get_rng_state())
    assert all(torch.equal(x,y) for x,y in zip(a.parameters(),b.parameters()))
    c=BalancedPairLanguageModel(16,29)
    assert any(not torch.equal(x,y) for x,y in zip(a.parameters(),c.parameters()))

def test_no_write_hold_preserves_labels_and_prefix():
    x,y=batch(4,16,12,123)
    longer,ly=batch(4,64,12,123)
    assert torch.equal(longer[:,:x.shape[1]],x)
    assert torch.equal(y,ly)
    tail=longer[:,x.shape[1]:]
    assert not ((tail>=2)&(tail<10)).any()
    assert torch.equal(x,batch(4,16,12,123)[0])

def test_all_fact_queries_and_no_oracle_inputs():
    x,y=batch(4,16,4,123)
    model=BalancedPairLanguageModel(16)
    assert logits(model,x,4).shape==(4,4,2)
    assert y.shape==(4,4)
    loss=torch.nn.functional.cross_entropy(logits(model,x,4).reshape(-1,2),y.reshape(-1))
    opt=torch.optim.AdamW(model.parameters(),lr=.002)
    before=[p.clone() for p in model.parameters()]
    loss.backward();opt.step()
    assert any(not torch.equal(p,q) for p,q in zip(before,model.parameters()))

def test_parameter_match_and_job_budget():
    for width in (16,32,64):
        w=matched_width(width)
        target=count(build("pair_shared",width,0))
        errors=[abs(count(build("gru",i,0))-target) for i in range(2,129)]
        assert abs(count(build("gru",w,0))-target)==min(errors)
    assert len(jobs(17))==41
    assert len(set(jobs(17)))==41

def test_precision_diagnostics_are_separate():
    out=diagnostics()
    for row in out["codes"]:
        assert row["precision"]["float64"]["minimum_saturated"]>=row["D"]
    assert any(r["a_equals_one"] for r in out["rounding"] if r["dtype"]=="float32")

def test_invalid_config():
    with pytest.raises(ValueError):BalancedPairCell(17)
    with pytest.raises(ValueError):BalancedPairCell(16,"unknown")
