"""Preregistered Experiment 015 cell rules on synthetic intervention summaries."""
from prototypes.rnn_llm_architecture.experiment_015_report import cell


def summary(A_S, r8=.95, r8n=.95, C=1.0, rescue=1.0, same=1.0, diff=1.0, n=500, with_rescue=True):
    row = lambda acc, **kw: {"eligible": {"n": n, "target_acc": acc, "other_acc": .9, **kw}, "all": {"target_acc": acc},
                             "off_distribution_nn_ratio": 1.5}
    v = {"S_mean": row(A_S), "S_zero": row(A_S), "C_mean": row(C), "S_unrelated_same": row(same), "S_unrelated_diff": row(1 - diff, donor_value_rate=diff),
         "S_twin": row(0, donor_value_rate=1.0), "C_twin": row(1, donor_value_rate=0.0), "C_unrelated_diff": row(1, donor_value_rate=0.0),
         "full_mean": row(.5), "fullspace_normrand": row(.99), "sham": {**row(1.0), "sham_max_abs_logit_gap": 0.0}}
    for i in range(8):
        v[f"R8_mean_b{i}"], v[f"R8_normrand_b{i}"], v[f"R24_mean_b{i}"] = row(r8), row(r8n), row(.7)
    if with_rescue:
        v["S_mean_rescue_S"], v["S_mean_rescue_C"] = row(rescue), row(.6)
    return v


def test_cell_verdicts():
    assert cell(summary(.55), "after_write")["verdict"] == "supported"
    assert cell(summary(.95), "after_write")["verdict"] == "contradicted"
    assert cell(summary(.83, with_rescue=False), "before_query")["verdict"] == "inconclusive"         # partial destruction
    assert cell(summary(.55, r8=.80), "after_write")["verdict"] == "inconclusive"                      # random 8-d nearly as destructive
    assert cell(summary(.55, rescue=.7), "after_write")["verdict"] == "inconclusive"                   # no rescue
    assert cell(summary(.55, diff=.5), "after_write")["verdict"] == "inconclusive"                     # natural donors disagree
    assert cell(summary(.55, with_rescue=False), "before_query")["N"]["N4_rescue"] is None
    assert cell(summary(.55, n=10), "after_write")["verdict"] == "too few eligible"
