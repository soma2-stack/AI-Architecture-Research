"""Harness-owned typed project ledger. Only C4 accepts gate status writes."""
from __future__ import annotations

import json
import re
from pathlib import Path

STATUSES = {"OPEN", "CLAIMED", "VERIFIED", "REGRESSED", "SUPERSEDED"}
KINDS = {"feature", "decision", "constraint", "deferred"}


class Ledger:
    def __init__(self, path: Path, coupled: bool):
        self.path = Path(path)
        self.coupled = coupled
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {
            "requirements": [], "tasks": [], "failures": [], "checkpoint": None,
            "event": 0,
        }

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, sort_keys=True) + "\n")

    def _event(self):
        self.data["event"] += 1
        return self.data["event"]

    def _req(self, rid):
        return next(r for r in self.data["requirements"] if r["id"] == rid)

    def add(self, kind: str, text: str, stage: int):
        if kind not in KINDS or not text.strip():
            raise ValueError("invalid requirement")
        rid = f"R{stage}.{1 + sum(r['stage'] == stage for r in self.data['requirements'])}"
        self.data["requirements"].append({
            "id": rid, "stage": stage, "kind": kind, "text": text,
            "status": "OPEN", "tests": [], "symbols": [],
            "superseded_by": None, "updated_event": self._event(),
            "note": "",
        })
        self.save()
        return rid

    def link(self, rid: str, tests: list[str], symbols: list[str]):
        req = self._req(rid)
        req["tests"] = sorted(set(req["tests"]) | set(tests))
        req["symbols"] = sorted(set(req["symbols"]) | set(symbols))
        req["updated_event"] = self._event()
        self.save()

    def set_status(self, rid: str, status: str, source="model", superseded_by=None):
        if status not in STATUSES:
            raise ValueError("invalid status")
        if source == "model" and self.coupled and status not in {"CLAIMED", "SUPERSEDED"}:
            raise PermissionError("VERIFIED and REGRESSED are set automatically from visible-test "
                                  "results; use CLAIMED or SUPERSEDED")
        if source == "gate" and not self.coupled:
            raise PermissionError("uncoupled ledger cannot receive gate writes")
        req = self._req(rid)
        req["status"] = status
        req["superseded_by"] = superseded_by
        req["updated_event"] = self._event()
        self.save()

    def note(self, rid: str, text: str):
        if len(text) > 200:
            raise ValueError("note exceeds 200 characters")
        req = self._req(rid)
        req["note"] = text
        req["updated_event"] = self._event()
        self.save()

    def task_add(self, rid: str, text: str, stage: int):
        self._req(rid)
        tid = f"T{len(self.data['tasks']) + 1}"
        self.data["tasks"].append({"id": tid, "req": rid, "text": text,
                                   "state": "todo", "stage": stage})
        self._event()
        self.save()
        return tid

    def task_update(self, tid: str, state: str):
        if state not in {"todo", "doing", "done"}:
            raise ValueError("invalid task state")
        next(t for t in self.data["tasks"] if t["id"] == tid)["state"] = state
        self._event()
        self.save()

    def gate_event(self, passed: set[str], failed: dict[str, str],
                   symbols: list[str], diff: str, checkpoint=None, rolled_back=False):
        """Apply one gate result. On a rollback the failing edit is gone and the workspace is back
        at a green checkpoint, so statuses are not downgraded (the failure record keeps the lesson)."""
        if not self.coupled:
            raise PermissionError("gate event requires coupling")
        event = self._event()
        for req in self.data["requirements"]:
            linked = set(req["tests"])
            if req["status"] == "SUPERSEDED" or not linked:
                continue
            if linked & failed.keys() and req["status"] == "VERIFIED" and not rolled_back:
                req["status"] = "REGRESSED"
                req["updated_event"] = event
            elif linked <= passed and checkpoint and req["status"] in {"OPEN", "CLAIMED", "REGRESSED"}:
                req["status"] = "VERIFIED"
                req["updated_event"] = event
        for test, message in failed.items():
            old = next((f for f in self.data["failures"] if f["test"] == test and not f["resolved"]), None)
            if old:
                old["count"] += 1
                old["event"] = event
            else:
                self.data["failures"].append({
                    "id": f"X{len(self.data['failures']) + 1}", "event": event,
                    "test": test, "req_ids": [r["id"] for r in self.data["requirements"] if test in r["tests"]],
                    "tb_symbols": symbols, "reverted_diff": diff,
                    "message_head": message[:300], "count": 1, "resolved": False,
                })
        for failure in self.data["failures"]:
            if failure["test"] in passed:
                failure["resolved"] = True
        if checkpoint:
            self.data["checkpoint"] = checkpoint
        self.save()

    def sync_test_tags(self, workspace: Path, test_ids: set[str]):
        """Associate visible pytest nodes with `# req:` comments or `@pytest.mark.req(...)` marks.

        A tag applies only to the next top-level definition (comments or decorators directly above
        it, or an inline comment on its `def` line); any top-level def/class consumes pending tags."""
        if not self.coupled:
            return
        for file in (Path(workspace) / "tests").rglob("test_*.py"):
            rel = file.relative_to(workspace).as_posix()
            pending = set()
            for line in file.read_text().splitlines():
                comment = re.search(r"#\s*req:\s*([^#]+)", line)
                if comment:
                    pending |= set(re.findall(r"R\d+\.\d+", comment.group(1)))
                mark = re.search(r"@pytest\.mark\.req\(([^)]*)\)", line)
                if mark:
                    pending |= set(re.findall(r"R\d+\.\d+", mark.group(1)))
                definition = re.match(r"(?:async\s+)?(def|class)\s+(\w+)", line)
                if not definition:
                    continue
                test = f"{rel}::{definition.group(2)}"
                if definition.group(1) == "def" and definition.group(2).startswith("test_") \
                        and test in test_ids:
                    for rid in pending:
                        try:
                            req = self._req(rid)
                        except StopIteration:
                            continue
                        if test not in req["tests"]:
                            req["tests"].append(test)
                pending = set()
        self.save()

    def view(self, edit_scope: set[str], token_count, budget=1536):
        reqs = self.data["requirements"]
        lines = []
        for r in reqs:
            if r["status"] == "REGRESSED":
                lines.append(f"REGRESSED {r['id']}: {r['text']}")
        for r in reqs:
            if r["status"] in {"OPEN", "CLAIMED"} and not r["tests"]:
                lines.append(f"UNPROTECTED {r['id']}: {r['text']}")
        for r in reqs:
            if r["status"] != "SUPERSEDED" and r["kind"] in {"decision", "constraint"}:
                lines.append(f"{r['kind'].upper()} {r['id']} [{r['status']}]: {r['text']}")
            elif r["kind"] == "deferred" and r["status"] in {"OPEN", "CLAIMED"} and r["tests"]:
                # unfinished deferred work stays visible after tests are linked
                lines.append(f"DEFERRED {r['id']} [{r['status']}]: {r['text']}")
        modules = {Path(s).with_suffix("").as_posix().replace("/", ".")
                   for s in edit_scope if s.endswith(".py")}
        for f in self.data["failures"]:
            in_scope = any(sym == m or sym.startswith(m + ".") for sym in f["tb_symbols"] for m in modules)
            if not f["resolved"] and (in_scope or any(s in f["reverted_diff"] for s in edit_scope)):
                lines.append(f"FAILURE {f['id']} x{f['count']} {f['test']}: {f['message_head']}")
        for t in self.data["tasks"]:
            if t["state"] != "done":
                lines.append(f"TASK {t['id']} {t['state']}: {t['text']}")
        ids = [r["id"] for r in reqs if r["status"] == "VERIFIED"]
        if ids:
            lines.append("VERIFIED: " + ", ".join(ids))
        return "\n".join(lines[:_fit(lines, token_count, budget)])


def _fit(lines, token_count, budget):
    """Largest k such that the first k lines fit the budget; same result as adding lines one at a
    time until the first overflow (token counts are non-decreasing in k), but O(log n) tokenizer
    calls instead of O(n)."""
    if not lines or token_count("\n".join(lines)) <= budget:
        return len(lines)
    lo, hi = 0, len(lines) - 1  # lines[:lo] fits; lines[:hi + 1] does not
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if token_count("\n".join(lines[:mid])) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo
