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
            raise PermissionError("C4 reserves VERIFIED/REGRESSED for gate events")
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
                   symbols: list[str], diff: str, checkpoint=None):
        if not self.coupled:
            raise PermissionError("gate event requires coupling")
        event = self._event()
        for req in self.data["requirements"]:
            linked = set(req["tests"])
            if req["status"] == "SUPERSEDED" or not linked:
                continue
            if linked & failed.keys() and req["status"] == "VERIFIED":
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
        """Associate visible pytest nodes with preceding # req comments or marks."""
        if not self.coupled:
            return
        for file in (Path(workspace) / "tests").rglob("test_*.py"):
            rel = file.relative_to(workspace).as_posix()
            current = set()
            decorators = set()
            for line in file.read_text().splitlines():
                comment = re.search(r"#\s*req:\s*([^#]+)", line)
                if comment:
                    current = set(re.findall(r"R\d+\.\d+", comment.group(1)))
                mark = re.search(r"@pytest\.mark\.req\(['\"](R\d+\.\d+)['\"]\)", line)
                if mark:
                    decorators.add(mark.group(1))
                function = re.match(r"def\s+(test_\w+)\s*\(", line)
                if function:
                    test = f"{rel}::{function.group(1)}"
                    if test in test_ids:
                        for rid in current | decorators:
                            try:
                                req = self._req(rid)
                            except StopIteration:
                                continue
                            if test not in req["tests"]:
                                req["tests"].append(test)
                    decorators.clear()
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
        for f in self.data["failures"]:
            if not f["resolved"] and (set(f["tb_symbols"]) & edit_scope or
                                      any(s in f["reverted_diff"] for s in edit_scope)):
                lines.append(f"FAILURE {f['id']} x{f['count']} {f['test']}: {f['message_head']}")
        for t in self.data["tasks"]:
            if t["state"] != "done":
                lines.append(f"TASK {t['id']} {t['state']}: {t['text']}")
        ids = [r["id"] for r in reqs if r["status"] == "VERIFIED"]
        if ids:
            lines.append("VERIFIED: " + ", ".join(ids))
        out = []
        for line in lines:
            candidate = "\n".join(out + [line])
            if token_count(candidate) > budget:
                break
            out.append(line)
        return "\n".join(out)
