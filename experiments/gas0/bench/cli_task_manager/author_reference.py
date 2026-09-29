"""Author eight deterministic stages for the CLI task-manager benchmark."""
from __future__ import annotations
import difflib, json, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent; STARTER=ROOT/"starter"
STAGES=ROOT/"stages"; REFERENCE=ROOT/"reference"

def snapshot():
    return {p.relative_to(STARTER).as_posix():p.read_text(encoding="utf-8")
            for p in STARTER.rglob("*.py") if "__pycache__" not in p.parts}
def diff(before,after):
    out=[]
    for name in sorted(set(before)|set(after)):
        old=before.get(name,"").splitlines(keepends=True); new=after.get(name,"").splitlines(keepends=True)
        if old!=new:
            out.extend(difflib.unified_diff(old,new,fromfile=f"a/{name}" if name in before else "/dev/null",
                tofile=f"b/{name}" if name in after else "/dev/null"))
    return "".join(out)
def put(stage,folder,name,body):
    path=STAGES/f"s{stage}"/folder/name; path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(body.strip()+"\n",encoding="utf-8")
def replace(state,name,old,new):
    if state[name].count(old)!=1: raise AssertionError((name,old,state[name].count(old)))
    state[name]=state[name].replace(old,new)
def write_patch(stage,before,after):
    (REFERENCE/f"s{stage}.patch").write_bytes(diff(before,after).encode("utf-8"))

def main():
    for path in (STAGES,REFERENCE):
        if path.exists(): shutil.rmtree(path)
    REFERENCE.mkdir(parents=True); state=snapshot(); files=state.copy()
    (REFERENCE/"s1.patch").write_bytes(b"")
    put(1,"","request.md","""Do not edit. Inspect the task manager and return JSON with exactly q1 through q8: q1 the Task record; q2 the completion field; q3 tag normalization; q4 strict date parser; q5 task-list entry point; q6 persistence schema version; q7 command dispatcher; q8 the text formatter. Use exact names and values.""")

    # Stage 2: the default open-task filter must compose with tag filtering.
    tests="tests/test_tasks.py"
    replace(state,tests,'list_tasks(sample())','list_tasks(sample(),include_done=True)')
    replace(state,"tests/test_storage_cli.py",'assert "[x] t1" in dispatch(store,["list"])',
        'assert dispatch(store,["list"])=="(no tasks)"')
    query="taskapp/query.py"
    replace(state,query,'def list_tasks(tasks, tag=None, include_done=True):','def list_tasks(tasks, tag=None, include_done=False):')
    put(2,"","request.md","""Change task listing so completed tasks are hidden by default, including when a tag filter is present. Add an explicit `include_done` option to show them. Keep ordering stable and preserve all other filters.""")
    put(2,"visible","test_stage2.py","""from taskapp.model import Task
from taskapp.query import list_tasks

def test_default_hides_completed_tasks():
    rows=[Task("a","A",completed=True),Task("b","B")]
    assert [task.task_id for task in list_tasks(rows)]==["b"]

def test_explicit_flag_restores_completed_rows():
    rows=[Task("a","A",completed=True),Task("b","B")]
    assert [task.task_id for task in list_tasks(rows,include_done=True)]==["b","a"]
""")
    put(2,"hidden","test_stage2.py","""from taskapp.model import Task
from taskapp.query import list_tasks

def test_tag_filter_does_not_reintroduce_completed_tasks():
    rows=[Task("a","A",completed=True,tags=("work",)),Task("b","B",tags=("work",))]
    assert [task.task_id for task in list_tasks(rows,tag="work")]==["b"]

def test_explicit_tag_query_can_show_done_rows():
    rows=[Task("a","A",completed=True,tags=("work",))]
    assert [task.task_id for task in list_tasks(rows,tag="work",include_done=True)]==["a"]

""")
    put(2,"hidden","test_stage2_legacy.py","""def test_legacy_boolean_save_contract():
    from taskapp.store import TaskStore
    from taskapp.model import Task
    store=TaskStore("unused"); store.add(Task("a","A",completed=True))
    assert store.payload()["tasks"][0]["completed"] is True
""")
    put(2,"","supersedes.json","[]")
    write_patch(2,files,state); files=state.copy()

    # Stage 3: named projects and deterministic overdue-first project ordering.
    model="taskapp/model.py"
    replace(state,model,'    due_date: str | None = None\n','    due_date: str | None = None\n    project_id: str | None = None\n')
    replace(state,model,'                "tags": list(self.tags), "due_date": self.due_date}\n',
        '                "tags": list(self.tags), "due_date": self.due_date,\n'
        '                "project_id": self.project_id}\n')
    replace(state,model,'                   tags=tuple(row.get("tags", ())), due_date=row.get("due_date"))\n',
        '                   tags=tuple(row.get("tags", ())), due_date=row.get("due_date"),\n'
        '                   project_id=row.get("project_id"))\n')
    store="taskapp/store.py"
    replace(state,store,'        self.preferences = {"hide_done": False}\n',
        '        self.preferences = {"hide_done": False}\n        self.projects = {}\n')
    replace(state,store,'                "preferences": dict(self.preferences)}\n',
        '                "preferences": dict(self.preferences),\n                "projects": dict(sorted(self.projects.items()))}\n')
    replace(state,store,'        store.preferences = dict(data.get("preferences", {}))\n',
        '        store.preferences = dict(data.get("preferences", {}))\n'
        '        store.projects = dict(data.get("projects", {}))\n')
    state["taskapp/projects.py"]='''"""Named-project registry and deterministic project task ordering."""
from dataclasses import dataclass
from .errors import MissingProject, ValidationError
from .dates import is_overdue, date_sort_key

@dataclass(frozen=True)
class Project:
    project_id: str
    name: str

    def __post_init__(self):
        if not self.project_id.strip() or not self.name.strip():
            raise ValidationError("project id and name are required")

class ProjectRegistry:
    def __init__(self, projects=None):
        self.projects={row.project_id:row for row in (projects or [])}
    def add(self, project_id, name):
        if project_id in self.projects: raise ValidationError("duplicate project id")
        row=Project(project_id,name); self.projects[project_id]=row; return row
    def require(self, project_id):
        try: return self.projects[project_id]
        except KeyError as exc: raise MissingProject(project_id) from exc
    def payload(self):
        return {key:row.name for key,row in sorted(self.projects.items())}
    @classmethod
    def from_payload(cls, data):
        return cls([Project(key,value) for key,value in data.items()])

def project_tasks(tasks, project_id, today):
    selected=[task for task in tasks if task.project_id==project_id]
    return sorted(selected,key=lambda task:(task.completed,
        0 if is_overdue(task.due_date,today) else 1,
        date_sort_key(task.due_date),task.task_id))

def assign_project(task, registry, project_id):
    registry.require(project_id); task.project_id=project_id; return task
'''
    put(3,"","request.md","""Add named projects and assign tasks to them. Within a project, list open overdue tasks first; within each group sort by due date and then task ID. Designer decision D3.1: a task due today is not overdue. Defer bulk-complete with undo; do not implement it yet.""")
    put(3,"visible","test_stage3.py","""from taskapp.model import Task
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
""")
    put(3,"hidden","test_stage3.py","""from taskapp.model import Task
from taskapp.projects import ProjectRegistry, project_tasks
from taskapp.store import TaskStore

def test_tie_breaker_is_due_date_then_task_id():
    registry=ProjectRegistry(); registry.add("p","P")
    rows=[Task("z","Z",due_date="2025-12-31",project_id="p"),
          Task("a","A",due_date="2025-12-31",project_id="p")]
    assert [r.task_id for r in project_tasks(rows,"p","2026-01-01")] == ["a","z"]

def test_projects_round_trip_with_task_association(tmp_path):
    store=TaskStore(tmp_path/"tasks.json"); store.projects={"p":"Home"}
    store.add(Task("a","A",project_id="p")); store.save()
    loaded=TaskStore.load(store.path)
    assert loaded.projects=={"p":"Home"}
    assert loaded.tasks[0].project_id=="p"
""")
    put(3,"hidden","test_bulk_deferred.py","""def test_bulk_complete_with_undo_is_deferred():
    from taskapp import commands
    assert not hasattr(commands,"bulk_complete_with_undo")
""")
    put(3,"","supersedes.json","[]")
    write_patch(3,files,state); files=state.copy()

    # Stage 4 isolates the due-date regression to project-linked tasks added in S3.
    old='def include_due_date(row):\n    """Central serialization choice, kept explicit for schema changes."""\n    return True\n'
    injected=old.replace('return True','return not bool(row.get("project_id"))')
    before_bug=state.copy(); replace(state,store,old,injected); bugged=state.copy()
    (STAGES/"s4").mkdir(parents=True,exist_ok=True)
    (STAGES/"s4"/"bug.patch").write_bytes(diff(before_bug,bugged).encode("utf-8"))
    put(4,"","request.md","""Users report that saving and reopening a project-linked task silently removes its due date. Diagnose the regression and repair persistence without changing project association, ordering, or task status.""")
    put(4,"visible","test_stage4.py","""from taskapp.model import Task
from taskapp.store import TaskStore

def test_due_date_survives_save_and_reload(tmp_path):
    store=TaskStore(tmp_path/"tasks.json"); store.add(Task("a","A",due_date="2026-02-03",project_id="p"))
    store.save(); assert TaskStore.load(store.path).tasks[0].due_date=="2026-02-03"
""")
    put(4,"hidden","test_stage4.py","""from taskapp.model import Task
from taskapp.store import TaskStore

def test_due_date_and_tags_both_survive_persistence(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.add(Task("a","A",tags=("work",),due_date="2026-02-03",project_id="p"))
    store.save(); row=TaskStore.load(store.path).tasks[0]
    assert row.due_date=="2026-02-03" and row.tags==("work",)
""")
    put(4,"","supersedes.json","[]")
    fixed=state.copy(); replace(fixed,store,injected,old); write_patch(4,state,fixed)
    state=fixed; files=state.copy()

    # Stage 5 replaces the Boolean persistence field with a status enum.
    state[model]='''"""Validated tasks with a migrated open/done status."""
from __future__ import annotations
from dataclasses import dataclass
from .dates import parse_date
from .errors import ValidationError

STATUSES={"open","in_progress","done"}

@dataclass(init=False)
class Task:
    task_id: str
    title: str
    description: str
    status: str
    tags: tuple[str,...]
    due_date: str | None
    project_id: str | None
    def __init__(self,task_id,title,description="",completed=False,tags=(),due_date=None,
                 project_id=None,status=None):
        self.task_id=str(task_id).strip(); self.title=" ".join(str(title).split())
        self.description=str(description).strip(); self.tags=normalize_tags(tags)
        self.due_date=parse_date(due_date) if due_date else None
        self.project_id=project_id
        self.status=status or ("done" if completed else "open")
        if not self.task_id or not self.title: raise ValidationError("task id and title are required")
        if self.status not in STATUSES: raise ValidationError("invalid task status")
    @property
    def completed(self): return self.status=="done"
    @completed.setter
    def completed(self,value): self.status="done" if value else "open"
    def to_dict(self):
        return {"task_id":self.task_id,"title":self.title,"description":self.description,
                "status":self.status,"tags":list(self.tags),"due_date":self.due_date,
                "project_id":self.project_id}
    @classmethod
    def from_dict(cls,row):
        return cls(task_id=row["task_id"],title=row["title"],description=row.get("description",""),
                   tags=tuple(row.get("tags",())),due_date=row.get("due_date"),
                   project_id=row.get("project_id"),status=row.get("status"),
                   completed=row.get("completed",False))

def normalize_tags(values):
    result=[]
    for value in values or ():
        tag=" ".join(str(value).split()).casefold()
        if tag and tag not in result: result.append(tag)
    return tuple(sorted(result))

def task_identity(task): return task.task_id
def task_label(task):
    marker="x" if task.completed else " "
    return f"[{marker}] {task.task_id}: {task.title}"
'''
    replace(state,store,'    VERSION = 1','    VERSION = 2')
    replace(state,store,'        if data.get("version") != cls.VERSION:\n','        if data.get("version") not in {1, cls.VERSION}:\n')
    put(5,"","request.md","""Replace the persisted Boolean completion field with `status` values `open`, `in_progress`, and `done`. Migrate version-1 Boolean saves on load; preserve completion commands and ensure new saves contain status rather than completed.""")
    put(5,"visible","test_stage5.py","""from taskapp.model import Task
from taskapp.store import TaskStore

def test_status_enum_and_compatibility_property():
    row=Task("a","A"); assert row.status=="open"
    row.completed=True; assert row.status=="done" and row.completed

def test_new_payload_uses_status_not_boolean():
    store=TaskStore("unused"); store.add(Task("a","A",completed=True))
    row=store.payload()["tasks"][0]
    assert row["status"]=="done" and "completed" not in row
""")
    put(5,"hidden","test_stage5.py","""from taskapp.store import TaskStore

def test_v1_migration_preserves_done_and_open_tasks(tmp_path):
    old={"version":1,"tasks":[{"task_id":"a","title":"A","completed":True},
                                 {"task_id":"b","title":"B","completed":False}]}
    store=TaskStore.from_payload(tmp_path/"old.json",old)
    assert [(row.task_id,row.status) for row in store.tasks]==[("a","done"),("b","open")]
    store.save(); assert all("status" in row for row in store.payload()["tasks"])

def test_in_progress_is_not_reported_complete():
    from taskapp.model import Task
    row=Task("a","A",status="in_progress")
    assert row.completed is False
""")
    put(5,"","supersedes.json",json.dumps(["tests/hidden_2/test_stage2_legacy.py"]))
    # Retire only the old schema assertion; retain the tag-filter probes.
    state["taskapp/store.py"]=state["taskapp/store.py"].replace('"version": self.VERSION,','"version": self.VERSION,')
    write_patch(5,files,state); files=state.copy()

    # Stage 6: atomic save is the persistent global storage invariant.
    state["taskapp/atomic.py"]='''"""Crash-safe replacement for small JSON state files."""
import os
from pathlib import Path

def atomic_write_text(path,text):
    destination=Path(path); destination.parent.mkdir(parents=True,exist_ok=True)
    temporary=destination.with_name(destination.name+".tmp")
    try:
        temporary.write_text(text,encoding="utf-8")
        os.replace(temporary,destination)
    finally:
        if temporary.exists(): temporary.unlink()
'''
    replace(state,store,'import json\n','import json\nfrom .atomic import atomic_write_text\n')
    replace(state,store,'            self.path.write_text(json.dumps(self.payload(), sort_keys=True, indent=2),\n                                 encoding="utf-8")',
        '            atomic_write_text(self.path, json.dumps(self.payload(), sort_keys=True, indent=2))')
    put(6,"","request.md","""Persistent global constraint G6.1: task-state saves must use an atomic same-directory replacement, so an interrupted write cannot leave a truncated JSON file. Preserve this invariant for task, project, preference, and later undo state.""")
    put(6,"","static_checks.py","""import ast
from pathlib import Path

def test_persistent_store_uses_atomic_replacement():
    root=Path(__file__).resolve().parents[1]/"taskapp"
    tree=ast.parse((root/"store.py").read_text(encoding="utf-8"))
    calls={node.func.id for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Name)}
    assert "atomic_write_text" in calls
    assert "write_text" not in calls
""")
    put(6,"visible","test_stage6.py","""from taskapp.atomic import atomic_write_text

def test_atomic_writer_replaces_complete_content(tmp_path):
    path=tmp_path/"state.json"; path.write_text("old")
    atomic_write_text(path,"new")
    assert path.read_text()=="new" and not path.with_name("state.json.tmp").exists()
""")
    put(6,"hidden","test_stage6.py","""from taskapp.atomic import atomic_write_text

def test_atomic_writer_creates_parent_and_keeps_utf8(tmp_path):
    path=tmp_path/"nested"/"state.json"
    atomic_write_text(path,'{"title":"café"}')
    assert path.read_text(encoding="utf-8")=='{"title":"café"}'
""")
    put(6,"","supersedes.json","[]")
    write_patch(6,files,state); files=state.copy()

    # Stage 7 fixes old saves without a projects field and adds deferred undo.
    replace(state,store,'        store.projects = dict(data.get("projects", {}))\n',
        '        store.projects = dict(data.get("projects") or {})\n')
    state["taskapp/commands.py"]+='''\n\ndef bulk_complete_with_undo(tasks, task_ids):\n    """Complete a batch and return an undo token that restores each prior state."""\n    wanted=set(task_ids); selected=[task for task in tasks if task.task_id in wanted]\n    if len(selected)!=len(wanted): raise MissingTask("one or more tasks do not exist")\n    prior=[(task,task.completed) for task in selected]\n    for task,_ in prior: task.completed=True\n    return prior\n\ndef undo_bulk_complete(token):\n    for task,was_completed in token: task.completed=was_completed\n    return len(token)\n'''
    put(7,"","scenario.py","""from taskapp.store import TaskStore
legacy={"version":1,"tasks":[{"task_id":"a","title":"Old"}],"preferences":{},"projects":None}
store=TaskStore.from_payload("unused",legacy)
assert store.projects=={}
""")
    put(7,"","request.md","""The supplied save crashes because its optional projects collection is null. Diagnose the load failure and preserve compatibility with older saves that omit the collection. Also implement the bulk-complete/undo behavior deferred in Stage 3; undo must restore each task's prior completion state and original list order.""")
    put(7,"visible","test_stage7.py","""from taskapp.commands import bulk_complete_with_undo, undo_bulk_complete
from taskapp.model import Task

def test_bulk_completion_undo_restores_mixed_prior_state():
    rows=[Task("a","A"),Task("b","B",completed=True)]
    token=bulk_complete_with_undo(rows,["a","b"])
    assert all(row.completed for row in rows)
    assert undo_bulk_complete(token)==2
    assert [row.completed for row in rows]==[False,True]
""")
    put(7,"hidden","test_stage7.py","""from taskapp.commands import bulk_complete_with_undo, undo_bulk_complete
from taskapp.model import Task
from taskapp.store import TaskStore

def test_legacy_save_missing_or_null_projects_loads_empty_registry():
    payload={"version":1,"tasks":[],"preferences":{},"projects":None}
    assert TaskStore.from_payload("unused",payload).projects=={}

def test_bulk_undo_does_not_reorder_or_change_unselected_tasks():
    rows=[Task("a","A"),Task("b","B",completed=True),Task("c","C")]
    token=bulk_complete_with_undo(rows,["c","a"])
    undo_bulk_complete(token)
    assert [row.task_id for row in rows]==["a","b","c"]
    assert [row.completed for row in rows]==[False,True,False]
""")
    put(7,"hidden","test_bulk_deferred_stage7.py","""from taskapp.commands import bulk_complete_with_undo, undo_bulk_complete
from taskapp.model import Task

def test_deferred_bulk_undo_now_restores_completion_state():
    rows=[Task("a","A"),Task("b","B",completed=True)]
    token=bulk_complete_with_undo(rows,["a","b"])
    undo_bulk_complete(token)
    assert [row.completed for row in rows]==[False,True]
""")
    put(7,"","supersedes.json",json.dumps(["tests/hidden_3/test_bulk_deferred.py"]))
    write_patch(7,files,state); files=state.copy()

    # Stage 8 wires project, due date, tags, status and undo through CLI.
    cli="taskapp/cli.py"
    replace(state,cli,'from .query import list_tasks\n','from .query import list_tasks\nfrom .projects import ProjectRegistry, assign_project, project_tasks\nfrom .commands import bulk_complete_with_undo, undo_bulk_complete\n')
    replace(state,cli,'    commands.add_parser("list")\n',
        '    listing=commands.add_parser("list")\n'
        '    listing.add_argument("--tag"); listing.add_argument("--project"); listing.add_argument("--today",default="2026-01-01"); listing.add_argument("--include-done",action="store_true")\n'
        '    project=commands.add_parser("project"); project.add_argument("id"); project.add_argument("name")\n'
        '    bulk=commands.add_parser("bulk-done"); bulk.add_argument("ids",nargs="+")\n'
        '    commands.add_parser("undo")\n')
    replace(state,cli,'    args = parser.parse_args(argv)\n',
        '    args = parser.parse_args(argv)\n'
        '    if not hasattr(store,"_undo_token"): store._undo_token=None\n')
    replace(state,cli,'        if args.command == "list":\n'
        '            return format_tasks(list_tasks(store.tasks))\n',
        '        if args.command == "project":\n'
        '            if args.id in store.projects: return "error: duplicate project id"\n'
        '            store.projects[args.id]=args.name; store.save(); return args.id\n'
        '        if args.command == "bulk-done":\n'
        '            store._undo_token=bulk_complete_with_undo(store.tasks,args.ids); store.save(); return "done"\n'
        '        if args.command == "undo":\n'
        '            if store._undo_token is None: return "error: no batch to undo"\n'
        '            undo_bulk_complete(store._undo_token); store._undo_token=None; store.save(); return "undone"\n'
        '        if args.command == "list":\n'
        '            rows=list_tasks(store.tasks,tag=args.tag,include_done=args.include_done)\n'
        '            if args.project: rows=project_tasks(rows,args.project,args.today)\n'
        '            return format_tasks(rows,args.today)\n')
    put(8,"","request.md","""Integrate projects, tags, due dates, status, bulk completion, and undo into the CLI and persisted state. Add project creation and filtered listing; due-date ordering must remain deterministic. Round-trip and report must preserve all fields and must not mark unrelated tasks complete.""")
    put(8,"visible","test_stage8.py","""from taskapp.cli import dispatch
from taskapp.model import Task
from taskapp.store import TaskStore

def test_project_command_and_project_listing(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.projects={}
    store.add(Task("a","A",tags=("work",),due_date="2025-12-30",project_id="p"))
    assert dispatch(store,["project","p","Work"])=="p"
    assert "a: A" in dispatch(store,["list","--project","p","--tag","work"])

def test_cli_bulk_done_and_undo(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.add(Task("a","A"))
    assert dispatch(store,["bulk-done","a"])=="done"
    assert store.tasks[0].completed
    assert dispatch(store,["undo"])=="undone" and not store.tasks[0].completed
""")
    put(8,"hidden","test_stage8.py","""from taskapp.cli import dispatch
from taskapp.model import Task
from taskapp.store import TaskStore

def test_all_fields_survive_integrated_save_load(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.projects={"p":"Work"}
    store.add(Task("a","Review",tags=("work",),due_date="2026-04-05",project_id="p",status="in_progress"))
    store.save(); loaded=TaskStore.load(store.path)
    row=loaded.tasks[0]
    assert (row.tags,row.due_date,row.project_id,row.status)==(("work",),"2026-04-05","p","in_progress")

def test_tag_filter_and_project_sort_compose_without_extra_tasks(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.projects={"p":"P"}
    store.add(Task("a","Late",tags=("work",),due_date="2026-03-01",project_id="p"))
    store.add(Task("b","Other",tags=("home",),due_date="2026-02-01",project_id="p"))
    output=dispatch(store,["list","--tag","work","--project","p","--today","2026-03-02"])
    assert "a: Late" in output and "b: Other" not in output
""")
    put(8,"","supersedes.json","[]")
    write_patch(8,files,state)

    manifest={"project":"cli_task_manager","kind":"evaluation","stages":8,
      "orientation_answers":{"q1":"taskapp.model.Task","q2":"Task.completed","q3":"taskapp.model.normalize_tags","q4":"taskapp.dates.parse_date","q5":"taskapp.query.list_tasks","q6":1,"q7":"taskapp.cli.dispatch","q8":"taskapp.formatting.format_tasks"},
      "probes":[
       {"introduced":1,"retired":2,"tests":[f"Q{i}" for i in range(1,9)],"text_only":False,"requirement":"R1.1"},
       {"introduced":2,"retired":None,"tests":["tests/hidden_2/test_stage2.py::test_tag_filter_does_not_reintroduce_completed_tasks"],"text_only":False,"requirement":"R2.1"},
       {"introduced":2,"retired":5,"tests":["tests/hidden_2/test_stage2_legacy.py::test_legacy_boolean_save_contract"],"text_only":True,"requirement":"R2.2"},
       {"introduced":3,"retired":None,"tests":["tests/hidden_3/test_stage3.py::test_tie_breaker_is_due_date_then_task_id","tests/hidden_3/test_stage3.py::test_projects_round_trip_with_task_association"],"text_only":False,"requirement":"R3.1"},
       {"introduced":3,"retired":7,"tests":["tests/hidden_3/test_bulk_deferred.py::test_bulk_complete_with_undo_is_deferred"],"text_only":True,"requirement":"R3.2"},
       {"introduced":4,"retired":None,"tests":["tests/hidden_4/test_stage4.py::test_due_date_and_tags_both_survive_persistence"],"text_only":False,"requirement":"R4.1"},
       {"introduced":5,"retired":None,"tests":["tests/hidden_5/test_stage5.py::test_v1_migration_preserves_done_and_open_tasks","tests/hidden_5/test_stage5.py::test_in_progress_is_not_reported_complete"],"text_only":False,"requirement":"R5.1"},
       {"introduced":6,"retired":None,"tests":["tests/hidden_6/test_stage6.py::test_atomic_writer_creates_parent_and_keeps_utf8"],"text_only":False,"requirement":"G6.1"},
       {"introduced":7,"retired":None,"tests":["tests/hidden_7/test_stage7.py::test_legacy_save_missing_or_null_projects_loads_empty_registry","tests/hidden_7/test_stage7.py::test_bulk_undo_does_not_reorder_or_change_unselected_tasks","tests/hidden_7/test_bulk_deferred_stage7.py::test_deferred_bulk_undo_now_restores_completion_state"],"text_only":False,"requirement":"R3.2"},
       {"introduced":8,"retired":None,"tests":["tests/hidden_8/test_stage8.py::test_tag_filter_and_project_sort_compose_without_extra_tasks"],"text_only":False,"requirement":"R8.1"}]}
    (ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
