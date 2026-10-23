"""Preregistered Experiment 014 classification rules on synthetic switch-rate profiles."""
from prototypes.rnn_llm_architecture.experiment_014_report import classify, phase5_category


def prof(**kw):
    base = dict(n=500, S_sub=0.0, I_sub=1.0, S_comp=0.0, I_comp=1.0, R8=[0.0, 0.1, 0.2], R24=[0.5, 0.6, 0.7])
    base.update(kw)
    return base


def test_localized_outside_distributed_insufficient_and_few():
    assert classify(prof(S_sub=.99, S_comp=.01))[0] == "protected"
    assert classify(prof(S_sub=.0, S_comp=.99, R24=[0.0, 0.1, 0.2]))[0] == "outside"
    # complement transplant works but a random 24-d control works almost as well -> selectivity not met -> ambiguous, not "outside"
    assert classify(prof(S_sub=.0, S_comp=1.0, R24=[.5, .6, .75]))[0] == "distributed"      # margin 0.25 < 0.30
    assert classify(prof(S_sub=.0, S_comp=1.0, R24=[.5, .6, .70]))[0] == "outside"           # margin exactly 0.30 passes (>=)
    assert classify(prof(S_sub=.6, S_comp=.4))[0] == "distributed"
    assert classify(prof(S_sub=.99, S_comp=.99, R24=[0, .1, .2]))[0] == "distributed"        # redundant carriers
    assert classify(prof(S_sub=.1, S_comp=.1))[0] == "insufficient"
    assert classify(prof(n=10, S_sub=.99))[0] == "few"


def test_selectivity_and_integrity_gates():
    # random 8-d control nearly as good as the designated subspace: not P-sufficient; by the literal rule (switch >= 0.30) -> distributed/ambiguous
    assert classify(prof(S_sub=.9, S_comp=.0, R8=[.6, .7, .85]))[0] == "distributed"
    cat, flags = classify(prof(S_sub=.95, S_comp=.0, I_sub=.5))     # switches, but destroys the other slots: off-distribution artefact
    assert cat == "insufficient" and flags["P_integrity_violation"] and flags["tie_break_applied"]


def test_phase5_label_reports_subcriteria():
    ip = {str(a): {"tau_median": a, "fraction_near_an_endpoint(|tau| or |tau-1| < 0.15)": 0.0, "fraction_predicting_B_value": a} for a in (0.25, 0.5, 0.75)}
    p = {"memory_displacement_ratio": [[1.0], [0.9]], "random_full_space_displacement_ratio": [[0.05], [0.3]],
         "random_in_designated_subspace_displacement_ratio": [[0.05], [0.3]], "memory_separation_at_end_over_natural_spread": [0.5, 0.5], "interpolation": ip}
    one = phase5_category(p, 1)
    assert one["sub_criteria"] == {"memory_ratio>=0.25": True, "memory>=10x_random_full": False, "separation/spread>=0.10": True}
    assert one["label"].startswith("collapsing")                  # preregistered mapping: failing any sub-criterion
    p["random_full_space_displacement_ratio"][1] = [0.01]
    assert phase5_category(p, 1)["label"] == "continuum / line-attractor-like"
