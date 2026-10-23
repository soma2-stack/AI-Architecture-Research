"""CPU tests for the read-only Experiment 009 table and decision renderer."""
from pathlib import Path

from prototypes.rnn_llm_architecture import experiment_009_report as rep

REPORTS = Path(rep.__file__).resolve().parent / "reports"


def test_report_renders_archived_pilot_and_hosted_lines():
    pilot = rep.load(REPORTS / "experiment_009_exploratory" / "pilot_seed29_two_slot.json")
    text = rep.render(pilot)
    assert "### Preregistered decisions" in text and "`protected_w32`" in text
    hosted = rep.load_hosted(REPORTS / "experiment_009_hosted_lines.jsonl")
    assert len(hosted) == 75 and all(len(k) == 3 for k in hosted)
    assert "Hosted GitHub Actions replication" in rep.render(pilot, hosted)


def test_committed_results_reproduce_committed_tables():
    report = rep.load(REPORTS / "experiment_009_results.json")
    hosted = rep.load_hosted(REPORTS / "experiment_009_hosted_lines.jsonl")
    assert report["status"] == "complete" and len(report["runs"]) == 75
    assert rep.render(report, hosted) == (REPORTS / "experiment_009_tables.md").read_text()
