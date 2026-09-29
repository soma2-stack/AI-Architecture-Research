from budgeter.goals import add_goal, contribute, goal_report
from budgeter.errors import ValidationError

def test_goal_progress_and_completion():
    goals=[]; goal=add_goal(goals,"g1","Trip","100")
    assert contribute(goal,"35") == 65
    assert goal_report(goals)[0]["complete"] is False
    contribute(goal,"65")
    assert goal_report(goals)[0]["complete"] is True

def test_duplicate_goal_rejected():
    import pytest
    goals=[]; add_goal(goals,"g1","Trip","10")
    with pytest.raises(ValidationError): add_goal(goals,"g1","Other","20")
