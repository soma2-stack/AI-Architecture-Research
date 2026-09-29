from taskapp.model import Task
from taskapp.projects import ProjectRegistry, assign_project, project_tasks

def test_project_assignment_and_overdue_first():
    projects=ProjectRegistry(); projects.add("p","Home")
    rows=[Task("b","Later",due_date="2026-01-04"),Task("a","Overdue",due_date="2025-12-31")]
    for row in rows: assign_project(row,projects,"p")
    assert [row.task_id for row in project_tasks(rows,"p","2026-01-01")]==["a","b"]

def test_due_today_is_not_overdue():
    projects=ProjectRegistry(); projects.add("p","Home")
    row=Task("a","Today",due_date="2026-01-01"); assign_project(row,projects,"p")
    assert project_tasks([row],"p","2026-01-01")==[row]
