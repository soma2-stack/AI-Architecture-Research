from budgeter.goals import add_goal, contribute
from budgeter.model import Transaction
from budgeter.summary import monthly_summary

def test_refund_reduces_actual_category_spend():
    rows=[Transaction("a","2026-04-04","-40","travel"),
          Transaction("b","2026-04-08","15","travel")]
    report=monthly_summary(rows,"2026-04")
    assert report["categories"]["travel"] == -25
    assert report["expenses"] == -40 and report["income"] == 15

def test_goal_contribution_does_not_change_transaction_report():
    rows=[Transaction("a","2026-04-04","-4","food")]
    goal=add_goal([],"g","Reserve","12"); contribute(goal,"5")
    assert monthly_summary(rows,"2026-04")["net"] == -4
