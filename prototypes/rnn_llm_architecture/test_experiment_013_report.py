"""Preregistered paired-comparison rule of Experiment 013 on synthetic cells."""
from prototypes.rnn_llm_architecture.capacity_012 import SEEDS
from prototypes.rnn_llm_architecture.experiment_013_report import compare

KEYS = [(i, d) for i in SEEDS for d in SEEDS]


def cells(outcomes, wv):
    return {k: {"outcome": o, "learning_onset_step": None if o == "plateau_only" else 1000,
                "eval": {"64": {"whole_varied": w}}} for k, o, w in zip(KEYS, outcomes, wv)}


def test_outperform_comparable_and_inconclusive():
    good = cells(["success"] * 4 + ["partial"] * 5, [1.0] * 4 + [.3] * 5)
    bad = cells(["plateau_only"] * 9, [0.0] * 9)
    assert compare({"X": good, "Y": bad}, "X", "Y")["verdict"] == "X outperforms Y"
    assert compare({"X": bad, "Y": good}, "X", "Y")["verdict"] == "Y outperforms X"
    assert compare({"X": good, "Y": good}, "X", "Y")["verdict"] == "comparable"
    # many better cells but small accuracy gap -> not "outperforms"; learned counts differ by >1 -> inconclusive
    small = cells(["partial"] * 5 + ["plateau_only"] * 4, [.05] * 5 + [0.0] * 4)
    r = compare({"X": small, "Y": bad}, "X", "Y")
    assert r["x_higher_class_cells"] == 5 and r["verdict"] == "inconclusive"
    assert compare({"X": good, "Y": {}}, "X", "Y") == {"complete": False}
