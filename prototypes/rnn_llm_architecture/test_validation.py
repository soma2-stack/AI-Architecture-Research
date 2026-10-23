import hashlib
import json
from pathlib import Path

import pytest
import torch

from prototypes.rnn_llm_architecture.candidates import CandidateConfig, CandidateLanguageModel
from prototypes.rnn_llm_architecture.gated import GatedConfig, GatedLanguageModel, LSTMState
from prototypes.rnn_llm_architecture.full_reference import (FrozenTanhReference,FourSiteGeometry,
    trace_neutral_schedule,realize_four_site_history,orthonormal_probe_bank,CorridorCreditEngine)
from prototypes.rnn_llm_architecture.validation import (ValidationConfig,RecurrentPath,
    parameter_inventory,token_cost_estimate,gated_token_cost_estimate,
    fair_comparison_profiles,theoretical_cost_estimate)


def test_original_sources_and_research_evidence_are_frozen():
    directory=Path(__file__).parent
    root=directory.parents[1]
    manifest=json.loads((directory/'frozen_sources.json').read_text())
    for name,digest in manifest['sha256'].items():
        assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name


def test_configuration_definitions_are_executable_and_match_report_defaults():
    from dataclasses import asdict
    data=json.loads((Path(__file__).parent/'comparison_configs.json').read_text())
    expected=json.loads(json.dumps(asdict(ValidationConfig())))
    assert data['validation']==expected
    assert len(data['token_configurations'])==9
    for config in data['token_configurations'].values():
        model=CandidateLanguageModel(CandidateConfig(**config))
        assert model.initial_state(1)[0].shape==(1,config['width'])
    assert len(data['gated_equal_width_configurations'])==6
    for config in data['gated_equal_width_configurations'].values():
        model=GatedLanguageModel(GatedConfig(**config))
        state=model.initial_state(1)[0]
        value=state.hidden if isinstance(state,LSTMState) else state
        assert value.shape==(1,config['width'])


@pytest.mark.parametrize('kind',('tanh','near_critical','protected','gru','lstm','theory'))
def test_shared_interface_width_streaming_and_reset(kind):
    cfg=ValidationConfig(width=16,channels=4)
    path=RecurrentPath(kind,cfg)
    x=torch.linspace(-.1,.1,2*8*16,dtype=torch.float64).reshape(2,8,16)
    h=path.scan(x)
    def leaves(state):
        return (state.hidden,state.cell) if isinstance(state,LSTMState) else (state,)
    assert all(value.shape==(2,16) and torch.isfinite(value).all() for value in leaves(h))
    streamed=path.scan(x[:,3:],path.scan(x[:,:3]))
    for a,b in zip(leaves(streamed),leaves(h)):
        torch.testing.assert_close(a,b)
    repeated=path.scan(x,path.initial_state(2))
    for a,b in zip(leaves(repeated),leaves(h)):
        torch.testing.assert_close(a,b)
    empty=path.scan(x[:,:0])
    for a,b in zip(leaves(empty),leaves(path.initial_state(2))):
        torch.testing.assert_close(a,b)


@pytest.mark.parametrize('kind',('tanh','near_critical','protected'))
def test_exact_parameter_state_and_payload_accounting(kind):
    w,r,v,l=16,4,23,2
    cfg=CandidateConfig(width=w,protected_channels=r,vocab_size=v,layers=l,cell_type=kind)
    model=CandidateLanguageModel(cfg)
    core={'tanh':2*w*w+3*w,'near_critical':w*w+3*w,
          'protected':3*w*w+w*r+4*w+r}[kind]
    expected=v*w+l*core+2*w
    inventory=parameter_inventory(model)
    assert inventory['trainable_parameters_measured']==expected
    assert inventory['parameter_bytes_measured']==4*expected
    assert sum(s.numel() for s in model.initial_state(3))==3*l*w
    cost=token_cost_estimate(cfg,batch=3,steps=5)
    assert cost['state_bytes_per_example']==4*l*w
    assert cost['logits_payload_bytes_estimate']==3*5*v*4
    assert cost['hidden_history_payload_bytes_estimate']==3*5*l*w*4


@pytest.mark.parametrize('kind',('gru','lstm'))
def test_gated_parameter_state_and_payload_accounting(kind):
    w,v,l=16,23,2
    cfg=GatedConfig(width=w,vocab_size=v,layers=l,cell_type=kind)
    model=GatedLanguageModel(cfg)
    core=(6*w*w+8*w) if kind=='gru' else (8*w*w+10*w)
    expected=v*w+l*core+2*w
    inventory=parameter_inventory(model)
    assert inventory['trainable_parameters_measured']==expected
    assert inventory['parameter_bytes_measured']==4*expected
    state=model.initial_state(3)
    state_values=sum(x.numel() for s in state for x in
                     ((s.hidden,s.cell) if isinstance(s,LSTMState) else (s,)))
    assert state_values==3*l*w*(2 if kind=='lstm' else 1)
    cost=gated_token_cost_estimate(cfg,batch=3,steps=5)
    assert cost['state_bytes_per_example']==4*l*w*(2 if kind=='lstm' else 1)
    assert cost['whole_model_MAC_per_token_estimate']==l*(6 if kind=='gru' else 8)*w*w+v*w


def test_no_optimization_in_diagnostic_backwards_and_full_reference_accounting():
    model=CandidateLanguageModel(CandidateConfig(width=16,vocab_size=23,protected_channels=4))
    before={k:v.clone() for k,v in model.state_dict().items()}
    output=model(torch.tensor([[1,2,3]]))[0]
    torch.autograd.grad(output.sum(),tuple(model.parameters()))
    assert all(torch.equal(before[k],v) for k,v in model.state_dict().items())
    estimate=theoretical_cost_estimate(32,3)
    assert estimate['selected_renewal_credit_values']==2*15*3
    assert estimate['fixed_source_physical_credit_values']==32*3
    norm=FrozenTanhReference(32).recurrent_normalization()
    assert abs(norm['R_group_over_loss']-1/32)<1e-16
    assert norm['independently_differentiated_R_W_b_entries']==2*32*32+32


def test_all_five_token_models_have_equal_width_and_explicit_budget_matches():
    profiles=fair_comparison_profiles(ValidationConfig())
    for width in ('16','32','64'):
        rows=profiles['equal_width_token_models'][width]
        assert set(rows)=={'tanh','near_critical','protected','gru','lstm'}
        assert all(row['config']['width']==int(width) and row['config']['layers']==2
                   for row in rows.values())
    matched=profiles['parameter_matched_token_models']
    assert matched['target_trainable_parameters']==7456
    assert set(matched['architectures'])=={'tanh','near_critical','protected','gru','lstm'}
    for row in matched['architectures'].values():
        assert row['inventory']['trainable_parameters_measured']==7456+row['trainable_parameter_delta']
        assert abs(row['trainable_parameter_delta_fraction'])<=.11
    assert 'no token-prediction' in profiles['theory_reference'].lower()


def test_no_clear_route7a_replay_and_local_trace_correction_without_feedback_erasure():
    n,m=2048,8
    control=torch.tensor([[1.,-1.],[-.5,.5]],dtype=torch.float64)
    gates,phases,meta=trace_neutral_schedule(n,m,control,(1,2),precharge_steps=4,release_steps=2)
    other_gates,_,_=trace_neutral_schedule(n,m,-control,(1,2),precharge_steps=4,release_steps=2)
    assert meta['final_clear'] is False and 'clear' not in phases
    assert max(meta['local_trace_errors'])<1e-13
    geometry=FourSiteGeometry(n,m,len(gates));model=FrozenTanhReference(n)
    a=realize_four_site_history(model,geometry,gates)
    b=realize_four_site_history(model,geometry,other_gates)
    torch.testing.assert_close(model.scan(a.inputs),a.states[-1],atol=2e-14,rtol=2e-14)
    torch.testing.assert_close(a.states[-1],b.states[-1],atol=2e-14,rtol=2e-14)
    probes=orthonormal_probe_bank(geometry,2);engine=CorridorCreditEngine(n)
    sa=engine.scan(a.gates[1:,1:model.k],probes)
    sb=engine.scan(b.gates[1:,1:model.k],probes)
    assert (sa.feedback-sb.feedback).norm()>0
    # Local donor compensation does not assert a margin or clear the feedback.
