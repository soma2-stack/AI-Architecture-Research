"""Architecture correctness, no optimizer or learning experiments."""
import dataclasses
import pytest
import torch

from prototypes.rnn_llm_architecture.candidates import (CandidateConfig, CandidateLanguageModel,
                         NearCriticalCell, ProtectedMemoryCell)
from prototypes.rnn_llm_architecture.model import RNNConfig, RNNLanguageModel


KINDS = ("tanh", "near_critical", "protected")


def make(kind, **kwargs):
    return CandidateLanguageModel(CandidateConfig(vocab_size=23,width=16,layers=2,
                                   protected_channels=4,cell_type=kind,precision="float64",**kwargs))


@pytest.mark.parametrize("kind", KINDS)
def test_scan_matches_frozen_original_with_same_weights(kind):
    new = make(kind)
    old = RNNLanguageModel(RNNConfig(vocab_size=23,width=16,layers=2,
                                    protected_channels=4,cell_type=kind)).double()
    weights = new.state_dict()
    if kind == "protected":
        weights = {k:(-v if '.slow_gate.' in k else v) for k,v in weights.items()}
    old.load_state_dict(weights)
    ids = torch.tensor([[1,2,3,4,5],[5,4,3,2,1]])
    a,sa,ha = old(ids,return_history=True)
    b,sb,hb = new(ids,return_history=True)
    torch.testing.assert_close(a,b,atol=2e-12,rtol=2e-12)
    torch.testing.assert_close(ha,hb,atol=2e-14,rtol=2e-13)
    for x,y in zip(sa,sb):
        torch.testing.assert_close(x,y)
    assert old.trainable_parameters == new.trainable_parameters


@pytest.mark.parametrize("kind", KINDS)
def test_stream_empty_reset_and_state_ownership(kind):
    model = make(kind)
    ids = torch.tensor([[1,3,5,7,9],[2,4,6,8,10]])
    original = model.initial_state(2)
    full,fs,history = model(ids,original,return_history=True)
    a,s = model(ids[:,:2]); b,cs = model(ids[:,2:],s)
    torch.testing.assert_close(full,torch.cat((a,b),1))
    for x,y in zip(fs,cs):
        torch.testing.assert_close(x,y)
    assert all(torch.count_nonzero(x)==0 for x in original)
    empty,es,eh = model(ids[:,:0],s,return_history=True)
    assert empty.shape == (2,0,23) and eh.shape == (2,0,2,16)
    assert all(x is y for x,y in zip(es,s))
    mask = torch.zeros_like(ids,dtype=torch.bool); mask[0,2] = True
    reset,rs = model(ids,reset_mask=mask)
    suffix,ss = model(ids[:1,2:])
    torch.testing.assert_close(reset[0,2:],suffix[0])
    torch.testing.assert_close(reset[1],full[1])
    for x,y in zip(rs,ss):
        torch.testing.assert_close(x[0],y[0])
    assert history.shape == (2,5,2,16)


@pytest.mark.parametrize("kind", KINDS)
def test_initialization_reproducible_and_does_not_change_caller_rng(kind):
    torch.manual_seed(81); rng = torch.get_rng_state().clone()
    a,b = make(kind),make(kind)
    assert torch.equal(rng,torch.get_rng_state())
    assert all(torch.equal(a.state_dict()[k],v) for k,v in b.state_dict().items())
    changed = make(kind,seed=82)
    assert not torch.equal(a.embedding.weight,changed.embedding.weight)


@pytest.mark.parametrize("kind", KINDS)
def test_state_gradient_finite_difference_and_chunk_boundary(kind):
    model = make(kind)
    h = tuple(s.requires_grad_() for s in model.initial_state(1))
    ids = torch.tensor([[1,2,3,4]])
    f = lambda state: model(ids,state)[0][0,-1,3]
    grad = torch.autograd.grad(f(h),h)[0]
    direction = torch.linspace(-1,1,16,dtype=torch.float64)[None]
    eps = 1e-6
    plus,minus = list(h),list(h)
    plus[0] = h[0]+eps*direction; minus[0] = h[0]-eps*direction
    fd = (f(plus)-f(minus))/(2*eps)
    torch.testing.assert_close((grad*direction).sum(),fd,atol=2e-7,rtol=1e-5)
    _,s = model(ids[:,:2],h)
    suffix = model(ids[:,2:],s)[0][0,-1,3]
    streamed = torch.autograd.grad(suffix,h)[0]
    torch.testing.assert_close(grad,streamed)
    assert all(not x.requires_grad for x in model.detach_state(s))
    _,s = model(ids[:,:2],h)
    reset = torch.ones_like(ids[:,2:],dtype=torch.bool)
    cutoff = torch.autograd.grad(model(ids[:,2:],s,reset_mask=reset)[0].sum(),s)[0]
    assert torch.count_nonzero(cutoff)==0


@pytest.mark.parametrize("operator", ("orthogonal","identity","householder_cycle"))
@pytest.mark.parametrize("leak", (1.,.2))
def test_near_critical_spectral_and_zero_trajectory_horizon(operator,leak):
    cfg = CandidateConfig(width=16,cell_type="near_critical",precision="float64",
                          operator=operator,leak=leak,gap=.01)
    cell = NearCriticalCell(cfg)
    torch.testing.assert_close(torch.linalg.svdvals(cell.recurrent),torch.full((16,),.99,dtype=torch.float64))
    h = torch.zeros(1,16,dtype=torch.float64,requires_grad=True)
    origin = h
    x = torch.zeros_like(h)
    for _ in range(64):
        h = cell(x,h)
    jac = torch.autograd.functional.jacobian(lambda initial: cell(x,initial),origin)[0,:,0,:]
    assert torch.linalg.matrix_norm(jac,ord=2) <= (1-leak+leak*.99)+1e-12
    grad = torch.autograd.grad(h.sum(),origin)[0]
    assert torch.isfinite(grad).all()
    if operator == "identity":
        torch.testing.assert_close(grad,torch.full_like(grad,(1-leak+leak*.99)**64))


def test_selective_overwrite_retains_closed_channels_and_their_gradient():
    torch.manual_seed(1)
    cfg = CandidateConfig(width=32,protected_channels=8,precision="float64")
    cell = ProtectedMemoryCell(cfg)
    torch.testing.assert_close(cell.masks@cell.masks.T,torch.eye(8,dtype=torch.float64))
    coeff = torch.randn(2,8,dtype=torch.float64,requires_grad=True)
    h = cell.synthesize(coeff)
    mask = torch.zeros_like(coeff); mask[:,0] = 1
    for _ in range(128):
        h = cell(torch.randn(2,32,dtype=torch.float64),h,write_mask=mask)
    result = cell.read_protected(h)
    torch.testing.assert_close(result[:,1:],coeff[:,1:],atol=2e-13,rtol=2e-13)
    grad = torch.autograd.grad(result[:,1:].sum(),coeff)[0]
    torch.testing.assert_close(grad[:,1:],torch.ones_like(grad[:,1:]),atol=3e-13,rtol=3e-13)
    torch.testing.assert_close(grad[:,0],torch.zeros_like(grad[:,0]),atol=3e-13,rtol=0)
    assert not torch.allclose(result[:,0],coeff[:,0])


def test_orthogonal_basis_substitution_preserves_the_claimed_closed_channel_invariant():
    # The invariant alone is not a novel Walsh primitive: any orthonormal bank works.
    cfg = CandidateConfig(width=32,protected_channels=8,precision="float64",protected_basis="random_orthogonal")
    cell = ProtectedMemoryCell(cfg)
    original = torch.randn(1,8,dtype=torch.float64)
    h = cell.synthesize(original)
    for _ in range(64):
        h = cell(torch.randn(1,32,dtype=torch.float64),h,write_mask=torch.zeros_like(original))
    torch.testing.assert_close(cell.read_protected(h),original,atol=4e-14,rtol=4e-14)


def test_sum_free_walsh_labels_do_not_prevent_cubic_nonlinear_aliasing():
    cell = ProtectedMemoryCell(CandidateConfig(width=16,protected_channels=4,precision="float64"))
    p = cell.masks  # labels 1,2,4,7; 1 XOR 2 XOR 4 = 7
    torch.testing.assert_close((p[0]*p[1])@p.T,torch.zeros(4,dtype=torch.float64),atol=1e-15,rtol=0)
    proposal = torch.tanh(2*(p[0]+p[1]+p[2]))
    assert abs(proposal@p[3]) > .01


@pytest.mark.parametrize("ablation",("project_fast","retain_slow","slow_feedback","orthogonal_masks"))
def test_mechanism_removal_has_observable_effect(ablation):
    torch.manual_seed(33)
    cfg = CandidateConfig(width=16,protected_channels=4,precision="float64")
    good = ProtectedMemoryCell(cfg)
    bad = ProtectedMemoryCell(dataclasses.replace(cfg,**{ablation:False}))
    bad.load_state_dict({k:v for k,v in good.state_dict().items() if k!='masks'},strict=False)
    x,h = torch.randn(2,16,dtype=torch.float64),torch.randn(2,16,dtype=torch.float64)
    assert not torch.allclose(good(x,h),bad(x,h))


@pytest.mark.parametrize("kind",KINDS)
@pytest.mark.parametrize("precision",("float32","float64"))
def test_long_sequence_stability(kind,precision):
    model = CandidateLanguageModel(CandidateConfig(vocab_size=23,width=16,layers=1,
                     protected_channels=4,cell_type=kind,precision=precision))
    ids = torch.arange(1024)[None]%23
    y,state = model(ids)
    grad = torch.autograd.grad(y[0,-1,3],model.embedding.weight)[0]
    assert torch.isfinite(y).all() and torch.isfinite(state[0]).all() and torch.isfinite(grad).all()


@pytest.mark.parametrize("kwargs",({"leak":0},{"gap":1},{"gap":float('nan')},
                                   {"operator":"mystery"},{"precision":"float16"},{"seed":True}))
def test_invalid_candidate_config(kwargs):
    with pytest.raises(ValueError):
        CandidateConfig(**kwargs)


def test_unrepresentable_near_critical_gap_is_rejected():
    with pytest.raises(ValueError,match="not representable"):
        CandidateConfig(cell_type="near_critical",gap=1e-20,precision="float32")


def test_invalid_stream_state_reset_and_write_mask():
    model = make("protected")
    ids = torch.ones(1,2,dtype=torch.long)
    with pytest.raises(ValueError): model(ids,(torch.zeros(1,16),))
    with pytest.raises(ValueError): model(ids,reset_mask=ids)
    with pytest.raises(ValueError): model(ids,write_masks=torch.ones(1,2,2,4,dtype=torch.float64)*2)
    with pytest.raises(ValueError): make("tanh")(ids,write_masks=torch.ones(1,2,2,4))
