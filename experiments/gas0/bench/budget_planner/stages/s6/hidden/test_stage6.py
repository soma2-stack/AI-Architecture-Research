from budgeter.budgets import CategoryBudgets
from budgeter.goals import add_goal, contribute

def test_budget_and_goal_state_use_integer_cents():
    budgets=CategoryBudgets(); budgets.set_limit("food","2026-01","1.25")
    assert budgets.payload()["food|2026-01"]==125
    goal=add_goal([],"g","Reserve","2.00")
    contribute(goal,"0.30")
    assert goal.target_cents==200 and goal.saved_cents==30
