"""Independent equation checks and fixed-realized-input derivatives on CPU."""
import math
import pytest
import torch

from prototypes.rnn_llm_architecture.full_reference import (
    CorridorOperator, CorridorCreditEngine, FrozenTanhReference, FourSiteGeometry,
    realize_four_site_history, orthonormal_probe_bank, survivor_walsh,
    early_capture_schedule, trace_neutral_triple, OPEN_MECHANISMS,
)
from prototypes.rnn_llm_architecture.theory_reference import FrozenCorridorCreditReference


def independent_dense(n):
    k,d = n//2,n//4
    v = torch.full((k,),-1/math.sqrt(k),dtype=torch.float64); v[0]+=1
    u = torch.eye(k,dtype=torch.float64)-torch.outer(v,v)/(1-1/math.sqrt(k))
    p = torch.eye(k,dtype=torch.float64)
    p[:d,:d] = torch.roll(torch.eye(d,dtype=torch.float64),1,0)
    o = u@p@u
    r = torch.zeros(n,n,dtype=torch.float64)
    r[:k,:k]=(1-1/n)*o
    r[k:,k:]=torch.eye(n-k,dtype=torch.float64)/(100*n)
    return o,r


@pytest.mark.parametrize("n",(16,31,32,64))
def test_independent_householder_and_frozen_operator(n):
    o,r = independent_dense(n)
    op,model = CorridorOperator(n),FrozenTanhReference(n)
    eye = torch.eye(op.r,dtype=torch.float64)
    torch.testing.assert_close(op(eye),o[1:,1:],atol=3e-15,rtol=3e-15)
    torch.testing.assert_close(op(eye).T@op(eye),eye,atol=3e-15,rtol=3e-15)
    torch.testing.assert_close(model.dense_recurrent(),r,atol=3e-15,rtol=3e-15)
    torch.testing.assert_close(op(eye,transpose=True),op(eye).T)
    torch.testing.assert_close(model.reference_apply(torch.eye(n,dtype=torch.float64),transpose=True),r.T)
    assert abs(torch.linalg.matrix_norm(r,ord=2).item()-model.a)<2e-15
    assert len(list(model.parameters()))==0


def test_streaming_renewal_includes_full_private_feedback():
    torch.manual_seed(40)
    n=64
    engine = CorridorCreditEngine(n)
    probes = torch.randn(engine.op.r,3,dtype=torch.float64)
    gates = .99+.009*torch.rand(12,engine.op.r,dtype=torch.float64)
    result,history = engine.scan(gates,probes,return_history=True)
    frozen,fh = FrozenCorridorCreditReference(n).scan(gates,probes,return_history=True)
    torch.testing.assert_close(history,fh,atol=2e-14,rtol=2e-14)
    torch.testing.assert_close(result.response,frozen.response)
    left = engine.scan(gates[:5],probes)
    right = engine.scan(gates[5:],probes,left)
    torch.testing.assert_close(right.response,result.response)
    assert right.steps==12
    assert torch.linalg.vector_norm(result.feedback)>0
    assert torch.linalg.vector_norm(engine.op.u@result.response)>0
    # Exact unpaired feedback cannot be replaced with the direct-path recurrence.
    assert not torch.allclose(result.local,result.response)
    empty = engine.scan(gates[:0],probes,result)
    assert empty is result


def test_full_independent_r_w_b_directional_derivative_with_preparation():
    torch.manual_seed(41)
    n,p=16,3
    model=FrozenTanhReference(n)
    inputs = .1*torch.randn(5,n,dtype=torch.float64)
    dR,dW = (.1*torch.randn(p,n,n,dtype=torch.float64) for _ in range(2))
    db = .1*torch.randn(p,n,dtype=torch.float64)
    _,s = model.directional_scan(inputs,dR,dW,db)
    _,r = independent_dense(n)
    def independently_replay(theta):
        h=torch.zeros(n,dtype=torch.float64)
        rr = r+torch.einsum('p,pij->ij',theta,dR)
        ww = torch.eye(n,dtype=torch.float64)+torch.einsum('p,pij->ij',theta,dW)
        bb = model.bias+theta@db
        for x in inputs: h=torch.tanh(rr@h+ww@x+bb)
        return h
    theta=torch.zeros(p,dtype=torch.float64,requires_grad=True)
    jac = torch.autograd.functional.jacobian(independently_replay,theta)
    torch.testing.assert_close(s,jac,atol=2e-15,rtol=2e-13)
    eps=1e-6
    for j in range(p):
        v=torch.zeros_like(theta);v[j]=eps
        fd=(independently_replay(v)-independently_replay(-v))/(2*eps)
        torch.testing.assert_close(s[:,j],fd,atol=2e-10,rtol=2e-7)
    assert torch.linalg.vector_norm(s)>0


def test_complete_fixed_source_includes_all_parameter_rows_and_source_directions():
    torch.manual_seed(441)
    model=FrozenTanhReference(32)
    inputs=.05*torch.randn(6,32,dtype=torch.float64)
    probes=torch.randn(32,3,dtype=torch.float64)
    h,s=model.fixed_source_scan(inputs,probes)
    dr=torch.zeros(3,32,32,dtype=torch.float64)
    dr[:,:,model.k:]=probes.T[:,:,None]/math.sqrt(model.l)
    dh,ds=model.directional_scan(inputs,dr,torch.zeros_like(dr),torch.zeros(3,32,dtype=torch.float64))
    torch.testing.assert_close(h,dh)
    torch.testing.assert_close(s,ds,atol=2e-15,rtol=2e-13)
    assert s[model.k:].norm()>0 and s[:1].norm()>0


def test_balanced_history_replay_public_bath_common_endpoint_and_complete_credit():
    torch.manual_seed(42)
    model=FrozenTanhReference(512)
    geometry=FourSiteGeometry(512,2,4)
    word=.992+.006*torch.rand(4,2,dtype=torch.float64)
    x=realize_four_site_history(model,geometry,word)
    y=realize_four_site_history(model,geometry,.999-word+.992)
    end,replay=model.scan(x.inputs,return_history=True)
    torch.testing.assert_close(replay,x.states,atol=2e-14,rtol=2e-14)
    torch.testing.assert_close(x.states[-1],y.states[-1],atol=2e-14,rtol=2e-14)
    assert x.cost()['past_cube_valid_measured']
    assert not x.cost()['source_lift_premises_met']
    assert x.states[0].count_nonzero()==0
    for t in range(5):
        sites=geometry.sites(t)
        torch.testing.assert_close(x.states[t+1,sites].sum(1),torch.zeros(2,dtype=torch.float64))
        nondriven=torch.ones(512,dtype=torch.bool); nondriven[sites.flatten()]=False
        torch.testing.assert_close(x.states[t+1,nondriven],y.states[t+1,nondriven],atol=2e-14,rtol=2e-14)
    probes=torch.randn(model.r,2,dtype=torch.float64)
    h,physical=model.fixed_source_scan(x.inputs,probes)
    selected=CorridorCreditEngine(512).scan(x.gates[1:,1:model.k],probes).response
    torch.testing.assert_close(physical[1:model.k],model.sigma*math.sqrt(model.l)*selected,atol=2e-13,rtol=2e-13)
    assert physical[:1].count_nonzero()==0 and physical[model.k:].count_nonzero()==0
    hp,sp=model.fixed_source_scan(x.inputs[:3],probes)
    hs,ss=model.fixed_source_scan(x.inputs[3:],probes,state=hp,sensitivity=sp)
    torch.testing.assert_close(hs,h);torch.testing.assert_close(ss,physical)
    # State reset leaves positive gates and persistent credit.
    assert x.gates[-1].min()>=0 and physical.norm()>0


def test_fixed_source_legal_future_gradients_match_autograd_and_common_endpoint_cancellation():
    torch.manual_seed(43)
    n=256; model=FrozenTanhReference(n)
    geometry=FourSiteGeometry(n,1,2)
    past=realize_four_site_history(model,geometry,torch.tensor([[.993],[.998]],dtype=torch.float64))
    other=realize_four_site_history(model,geometry,torch.tensor([[.998],[.993]],dtype=torch.float64))
    probes=torch.randn(model.r,2,dtype=torch.float64)
    _,s1=model.fixed_source_scan(past.inputs,probes)
    _,s2=model.fixed_source_scan(other.inputs,probes)
    z=.25+.5*torch.rand(3,n,dtype=torch.float64)
    query=model.realize_query(past.states[-1],z)
    assert not query.requires_grad
    c=model.query_adjoint(z)
    assert c.norm() <= (1/math.cosh(.25)**2)**3
    # Independent R0 differentiating fixed raw inputs, not the inverse controller.
    _,base=independent_dense(n)
    dr=torch.zeros(2,n,n,dtype=torch.float64)
    dr[:,1:model.k,model.k:]=probes.T[:,:,None]/math.sqrt(model.l)
    def answer(raw):
        theta=torch.zeros(2,dtype=torch.float64,requires_grad=True)
        r=base+torch.einsum('p,pij->ij',theta,dr)
        h=torch.zeros(n,dtype=torch.float64)
        for x in torch.cat((raw,query)): h=torch.tanh(r@h+x+model.bias)
        return torch.autograd.grad(h.sum()/(n*math.sqrt(n)),theta)[0]
    difference=answer(past.inputs)-answer(other.inputs)
    expected=model.normalized_past_answer(s1-s2,z)
    torch.testing.assert_close(difference,expected,atol=5e-17,rtol=1e-9)
    # Finite query evaluation is not the legal-query supremum or dimension D.
    with pytest.raises(ValueError): model.query_adjoint(z*.1)
    with pytest.raises(ValueError): model.query_adjoint(z[:0])


def test_early_capture_transport_trace_repair_and_later_character_mixing():
    n,m=2048,8
    controls=torch.tensor([[1.,-.5],[-.2,.8]],dtype=torch.float64)
    gates,phases,meta=early_capture_schedule(n,m,controls,(1,2),write_steps=1,tail_steps=16,clear_steps=4)
    geometry=FourSiteGeometry(n,m,len(gates))
    probes=orthonormal_probe_bank(geometry,2)
    torch.testing.assert_close(probes.T@probes,torch.eye(2,dtype=torch.float64),atol=2e-15,rtol=2e-15)
    assert probes.sum(0).abs().max()<1e-15
    assert max(meta['donor_trace_match_errors'])<1e-14
    model=FrozenTanhReference(n)
    a=realize_four_site_history(model,geometry,gates,phases=phases)
    gates2,_,_=early_capture_schedule(n,m,-controls,(1,2),write_steps=1,tail_steps=16,clear_steps=4)
    b=realize_four_site_history(model,geometry,gates2)
    torch.testing.assert_close(a.states[-1],b.states[-1],atol=3e-14,rtol=3e-14)
    op=model.op
    engine=CorridorCreditEngine(n)
    _,ah=engine.scan(a.gates[1:,1:model.k],probes,return_history=True)
    _,bh=engine.scan(b.gates[1:,1:model.k],probes,return_history=True)
    delta=ah-bh
    gh,gl=1-1/n**2,.995
    for t,phase in enumerate(phases,1):
        old=survivor_walsh(geometry,(1,2),t-1)
        new=survivor_walsh(geometry,(1,2),t)
        torch.testing.assert_close(old@old.T,torch.eye(2,dtype=torch.float64))
        torch.testing.assert_close(op(old.T),new.T,atol=2e-15,rtol=2e-15)
        if phase in ('trace_tail','trace_correction','clear','write'):
            torch.testing.assert_close(new@delta[t],op.a*gh*(old@delta[t-1]),atol=3e-15,rtol=1e-10)
        if phase=='capture':
            e=0 if t==2 else 1
            chi=new[e]
            before=op.a*op(delta[t-1])
            after=a.gates[t,1:model.k,None]*before
            torch.testing.assert_close(chi@delta[t],chi@after,atol=4e-15,rtol=1e-10)
            support=chi!=0
            mean=before[support].mean(0)
            if e==0:  # first capture of a common survivor response
                torch.testing.assert_close(chi@delta[t],(gh-gl)/2*math.sqrt(int(support.sum()))*mean,atol=4e-15,rtol=1e-10)
    final=survivor_walsh(geometry,(1,2),geometry.interior_steps+1)@delta[-1]
    assert final.norm()>0
    # Public reset preserves the row by its public survivor gate, not by zeroing credit.
    old=survivor_walsh(geometry,(1,2),geometry.interior_steps)
    reset_gate=a.gates[-1,geometry.sites(geometry.interior_steps+1)[-1,0]]
    torch.testing.assert_close(final,op.a*reset_gate*(old@delta[-2]),atol=5e-15,rtol=1e-10)


def test_trace_neutral_no_clear_is_local_only():
    tau=torch.tensor([0.,10.,1000.],dtype=torch.float64)
    for x in (-1.,-.5,0.,.5,1.):
        gates,target=trace_neutral_triple(tau,torch.full_like(tau,x),1-1/2048,1-1/2048**2)
        realized=tau
        for g in gates: realized=g*(1+(1-1/2048)*realized)
        torch.testing.assert_close(realized,target,atol=2e-13,rtol=2e-15)
        assert (gates[2]-.9975).abs().max()<.000101


def test_invalid_geometry_realization_and_hypothetical_modules():
    with pytest.raises(ValueError): FourSiteGeometry(64,8,8)
    with pytest.raises(ValueError): FourSiteGeometry(512,2,4,require_proof_margin=True)
    with pytest.raises(ValueError): FrozenTanhReference(16,actual_recurrent=torch.eye(16,dtype=torch.float64))
    for gap in OPEN_MECHANISMS:
        with pytest.raises(NotImplementedError,match=gap.name): gap.require_implementation()


def test_no_false_dense_realization_claim_and_valid_dense_parameter_scan():
    base=FrozenTanhReference(16)
    actual=FrozenTanhReference(16,actual_recurrent=base.dense_recurrent())
    assert base.realization=='R0_reference' and actual.realization=='caller_supplied_R_actual'
    inputs=torch.full((3,16),.02,dtype=torch.float64)
    torch.testing.assert_close(base.scan(inputs),actual.scan(inputs))


def test_chronological_two_step_clear_on_full_complement_including_front_and_terminal():
    n,m=1024,2
    geometry=FourSiteGeometry(n,m,4)
    op=CorridorOperator(n)
    r=op.r
    o=op(torch.eye(r,dtype=torch.float64))
    projectors=[]
    gates=[]
    qstar=.9992; gh=1-1/n**2
    for t in range(3):
        sites=(geometry.sites(t)[m//2:]-1).flatten()
        indicator=torch.zeros(r,dtype=torch.float64);indicator[sites]=1
        protected=torch.diag(indicator)-torch.outer(indicator,indicator)/len(sites)
        projectors.append(torch.eye(r,dtype=torch.float64)-protected)
        # Public chronological outside gates vary; front/terminal are included.
        g=torch.full((r,),qstar-.0001*t,dtype=torch.float64)
        g[:t+1]=.2;g[op.d-2]=.8;g[sites]=gh
        gates.append(g)
    first=gates[1][:,None]*o;second=gates[2][:,None]*o
    torch.testing.assert_close(first@projectors[0],projectors[1]@first,atol=2e-15,rtol=2e-15)
    torch.testing.assert_close(second@projectors[1],projectors[2]@second,atol=2e-15,rtol=2e-15)
    p=op.gamma**2*4/op.k
    assert p<.01
    # SVD checks the entire complementary space, not selected random directions.
    norm=torch.linalg.matrix_norm(second@first@projectors[0],ord=2).item()
    bound=math.sqrt(1-(1-qstar**2)*p/16)
    assert norm <= bound+2e-14
