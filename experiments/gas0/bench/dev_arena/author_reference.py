"""Deterministically author the dev-only staged benchmark and reference patches.

This file is outside starter/ and is never copied to agent workspaces.
"""
from __future__ import annotations

import difflib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STARTER = ROOT / "starter"
STAGES = ROOT / "stages"
REFERENCE = ROOT / "reference"


def change(files, name, old, new):
    text = files[name]
    if text.count(old) != 1:
        raise AssertionError((name, old, text.count(old)))
    files[name] = text.replace(old, new)


def patch(before, after):
    chunks = []
    for name in sorted(set(before) | set(after)):
        old = before.get(name, "").splitlines(keepends=True)
        new = after.get(name, "").splitlines(keepends=True)
        if old == new:
            continue
        chunks.extend(difflib.unified_diff(old, new, fromfile=f"a/{name}" if name in before else "/dev/null",
                                           tofile=f"b/{name}" if name in after else "/dev/null"))
    return "".join(chunks)


def write_patch(path: Path, contents: str):
    # git apply requires LF context matching the LF source files on Windows.
    path.write_bytes(contents.encode("utf-8"))


def put(stage, where, name, contents):
    target = STAGES / f"s{stage}" / where / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(contents.rstrip() + "\n")


def main():
    if STAGES.exists():
        shutil.rmtree(STAGES)
    if REFERENCE.exists():
        shutil.rmtree(REFERENCE)
    REFERENCE.mkdir()
    files = {str(p.relative_to(STARTER)).replace("\\", "/"): p.read_text()
             for p in STARTER.rglob("*.py")}
    previous = files.copy()
    write_patch(REFERENCE / "s1.patch", "")
    put(1, "", "request.md", """Inspect this project. Do not edit code. Answer as JSON in
declare_stage_done(summary), with keys q1..q8: q1 module defining World; q2
function constructing seeded walls; q3 save format version; q4 emitted event
name when an actor dies; q5 function choosing enemy actions; q6 function that
computes shortest grid paths; q7 bag default capacity; q8 module rendering HUD
strings. Give exact names (module paths and function names) and integer values.""")

    # S2: shield and a text-only designer decision about poison lethality.
    change(files, "arena/model.py", '    glyph: str\n    alive: bool = True',
           '    glyph: str\n    shield: int = 0\n    alive: bool = True')
    change(files, "arena/model.py", '        self.alive = self.hp > 0\n\n    def move_to',
           '        self.alive = self.hp > 0\n        self.shield = max(0, self.shield)\n\n    def move_to')
    change(files, "arena/model.py", '''    def receive(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("negative damage")
        dealt = min(self.hp, amount)
        self.hp -= dealt
        self.alive = self.hp > 0
        return dealt
''', '''    def receive(self, amount: int, kind: str = "physical") -> int:
        if amount < 0:
            raise ValueError("negative damage")
        if kind != "poison":
            absorbed = min(self.shield, amount)
            self.shield -= absorbed
            amount -= absorbed
        dealt = min(self.hp, amount)
        self.hp -= dealt
        self.alive = self.hp > 0
        return dealt
''')
    change(files, "arena/combat.py", '            damage = actor.receive(1)',
           '            damage = actor.receive(1 if actor.hp > 1 else 0, "poison")')
    # Starter test intentionally states old behavior and is superseded at S2.
    put(2, "", "supersedes.json", json.dumps(["tests/test_starter_poison.py"], indent=2))
    put(2, "visible", "test_stage2.py", """# req: R2.1
from arena.model import Actor, Point

def test_shield_absorbs_direct_hit():
    a = Actor('a', Point(1,1), 5, 5, 1, 'p', '@', shield=2)
    assert a.receive(2) == 0
    assert (a.hp, a.shield) == (5, 0)
""")
    put(2, "hidden", "test_stage2_direct.py", """# req: R2.1
from arena.model import Actor, Point

def test_shield_direct_damage():
    a = Actor('a', Point(1,1), 5, 5, 1, 'p', '@', shield=1)
    assert a.receive(3, 'piercing') == 2
    assert (a.hp, a.shield) == (3, 0)
""")
    put(2, "hidden", "test_stage2_poison.py", """# req: R2.2
from arena.model import Actor, Point
from arena.combat import apply_status, tick_status
from arena.mapgen import bordered_world

# req: R2.2 (text-only decision)
def test_poison_never_kills_or_uses_shield():
    world = bordered_world(7,7)
    a = Actor('a', Point(1,1), 1, 5, 1, 'p', '@', shield=3)
    world.add_actor(a)
    apply_status(world, a, 'poison', 2)
    tick_status(world, a)
    assert a.hp == 1 and a.shield == 3 and a.alive
""")
    put(2, "", "request.md", """Add a shield value to actors. Physical direct
damage consumes shield before HP, while poison bypasses shield. Designer
decision R2.2: poison must never reduce HP below 1; preserve it in future
changes. Visible tests cover direct hits, and you should remember the decision.
""")
    write_patch(REFERENCE / "s2.patch", patch(previous, files))
    previous = files.copy()

    # S3: shield tonic interacts with S2; antidote deliberately deferred.
    change(files, "arena/inventory.py", '''    if item.kind != "potion":
        bag.add(item)
        raise ValueError("item is not usable")
    healed = actor.heal(item.power)
    world.events.append(Event("heal", actor.actor_id, amount=healed))
    return healed
''', '''    if item.kind == "shield_tonic":
        old = actor.shield
        actor.shield = min(5, actor.shield + item.power)
        gained = actor.shield - old
        world.events.append(Event("shield", actor.actor_id, amount=gained))
        return gained
    if item.kind != "potion":
        bag.add(item)
        raise ValueError("item is not usable")
    healed = actor.heal(item.power)
    world.events.append(Event("heal", actor.actor_id, amount=healed))
    return healed
''')
    put(3, "visible", "test_stage3.py", """# req: R3.1
from arena.inventory import Bag, use
from arena.model import Actor, Item, Point
from arena.mapgen import bordered_world

def test_shield_tonic_consumed():
    world = bordered_world(7,7)
    actor = Actor('a', Point(1,1), 5, 5, 1, 'p', '@', shield=1)
    bag = Bag(items=[Item('s', 'shield_tonic', 2)])
    assert use(world, actor, bag, 's') == 2
    assert actor.shield == 3 and bag.items == []
""")
    put(3, "hidden", "test_stage3.py", """# req: R3.1
from arena.inventory import Bag, use
from arena.model import Actor, Item, Point
from arena.mapgen import bordered_world

# req: R3.2 (text-only decision)
def test_tonic_capped_at_five():
    world = bordered_world(7,7)
    actor = Actor('a', Point(1,1), 5, 5, 1, 'p', '@', shield=4)
    bag = Bag(items=[Item('s', 'shield_tonic', 9)])
    assert use(world, actor, bag, 's') == 1
    assert actor.shield == 5

def test_tonic_does_not_heal():
    world = bordered_world(7,7)
    actor = Actor('a', Point(1,1), 2, 5, 1, 'p', '@')
    bag = Bag(items=[Item('s', 'shield_tonic', 2)])
    use(world, actor, bag, 's')
    assert actor.hp == 2 and actor.shield == 2
""")
    put(3, "hidden", "test_stage3_deferred.py", """# req: R3.3 (text-only deferred item)
import pytest
from arena.inventory import Bag, use
from arena.mapgen import bordered_world
from arena.model import Actor, Item, Point

def test_antidote_still_deferred():
    w=bordered_world(7,7); a=Actor('a',Point(1,1),3,5,1,'p','@')
    a.statuses['poison']=2
    bag=Bag(items=[Item('ant','antidote')])
    with pytest.raises(ValueError):
        use(w,a,bag,'ant')
    assert a.statuses['poison']==2 and bag.find('antidote')
""")
    put(3, "", "request.md", """Add a shield_tonic inventory item that increases
the existing shield and is consumed on use. Designer decision R3.2: total shield
is capped at 5 and the tonic does not heal HP. Deferred item R3.3: later, add
an antidote that removes poison without healing or granting shield. Do not
implement R3.3 yet; a later stage will request that deferred item.
""")
    write_patch(REFERENCE / "s3.patch", patch(previous, files))
    previous = files.copy()

    # S4: an injected path-collision regression in stable starter code.
    bugged = files.copy()
    change(bugged, "arena/model.py", '        return self.in_bounds(p) and p not in self.walls',
           '        return self.in_bounds(p)')
    (STAGES / "s4").mkdir(exist_ok=True)
    write_patch(STAGES / "s4" / "bug.patch", patch(files, bugged))
    write_patch(REFERENCE / "s4.patch", patch(bugged, files))
    put(4, "visible", "test_stage4.py", """# req: R4.1
from arena.mapgen import bordered_world
from arena.model import Point

def test_wall_collision_regression_after_patch():
    w=bordered_world(7,7); w.walls.add(Point(2,2))
    assert not w.walkable(Point(2,2))
""")
    put(4, "hidden", "test_stage4.py", """# req: R4.1
from arena.mapgen import bordered_world
from arena.model import Point
from arena.path import shortest_path

def test_paths_do_not_cross_interior_walls():
    w=bordered_world(7,7); w.walls.add(Point(2,1))
    assert Point(2,1) not in shortest_path(w,Point(1,1),Point(3,1))
""")
    put(4, "", "request.md", """An injected defect makes the headless pathfinder
route through walls. The visible regression test demonstrates the symptom.
Find and fix the root cause without breaking earlier mechanics.
""")
    previous = files.copy()

    # S5: typed piercing damage revises the S2 all-direct-damage assumption.
    change(files, "arena/model.py", '        if kind != "poison":',
           '        if kind not in {"physical", "piercing", "poison"}:\n            raise ValueError("unknown damage type")\n        if kind == "physical":')
    change(files, "arena/combat.py", 'def strike(world: World, attacker: Actor, defender: Actor, dice: Dice) -> int:',
           'def strike(world: World, attacker: Actor, defender: Actor, dice: Dice, kind: str = "physical") -> int:')
    change(files, "arena/combat.py", '    dealt = defender.receive(amount)\n    world.events.append(Event("hit", attacker.actor_id, defender.actor_id, dealt))',
           '    dealt = defender.receive(amount, kind)\n    world.events.append(Event("hit", attacker.actor_id, defender.actor_id, dealt, kind))')
    put(5, "", "supersedes.json", json.dumps(["tests/hidden_2/test_stage2_direct.py"], indent=2))
    put(5, "visible", "test_stage5.py", """# req: R5.1
from arena.model import Actor, Point

def test_piercing_bypasses_shield():
    a = Actor('a', Point(1,1), 4, 4, 1, 'p', '@', shield=3)
    assert a.receive(2, 'piercing') == 2
    assert a.hp == 2 and a.shield == 3
""")
    put(5, "hidden", "test_stage5.py", """# req: R5.1
from arena.combat import strike
from arena.mapgen import bordered_world
from arena.model import Actor, Point
from arena.rng import Dice

def test_piercing_event_and_dependents():
    w = bordered_world(7,7)
    a = Actor('a', Point(1,1), 5, 5, 2, 'p', '@')
    b = Actor('b', Point(2,1), 5, 5, 1, 'e', 'e', shield=5)
    w.add_actor(a); w.add_actor(b)
    assert strike(w,a,b,Dice(1), 'piercing') > 0
    assert b.shield == 5 and w.events[-1].detail == 'piercing'

""")
    put(5, "", "request.md", """Modify the earlier shield mechanic: attacks now
have a damage type. Physical attacks use shield; piercing attacks bypass it;
poison retains its old nonlethal, shield-bypassing rule. Propagate the type
through combat events and any dependent path. The stage-2 broad direct-damage
probe is superseded by this specification.
""")
    write_patch(REFERENCE / "s5.patch", patch(previous, files))
    previous = files.copy()

    # S6: global monotonic event identifiers, including later stages.
    change(files, "arena/model.py", '''    detail: str = ""
''', '''    detail: str = ""
    seq: int = 0
''')
    change(files, "arena/model.py", '''    turn: int = 0
    events: list[Event] = field(default_factory=list)
''', '''    turn: int = 0
    event_seq: int = 0
    events: list[Event] = field(default_factory=list)
''')
    change(files, "arena/model.py", '''    def clear_events(self):
''', '''    def emit(self, event: Event):
        self.event_seq += 1
        event.seq = self.event_seq
        self.events.append(event)

    def clear_events(self):
''')
    change(files, "arena/save.py", '''        "turn": world.turn,
        "events": [vars(event) for event in world.events],
''', '''        "turn": world.turn,
        "event_seq": world.event_seq,
        "events": [vars(event) for event in world.events],
''')
    change(files, "arena/save.py", '''    world.events = [Event(**event) for event in data["events"]]
    return world, bags
''', '''    world.events = [Event(**event) for event in data["events"]]
    world.event_seq = max(data.get("event_seq", 0),
                          max((event.seq for event in world.events), default=0))
    return world, bags
''')
    for name in ["arena/combat.py", "arena/inventory.py", "arena/game.py"]:
        files[name] = files[name].replace("world.events.append(", "world.emit(")
        files[name] = files[name].replace("self.world.events.append(", "self.world.emit(")
    put(6, "visible", "test_stage6.py", """# req: R6.1
from arena.mapgen import bordered_world
from arena.model import Event

def test_event_sequence():
    w = bordered_world(7,7)
    w.emit(Event('a','hero')); w.emit(Event('b','hero'))
    assert [e.seq for e in w.events] == [1,2]
""")
    put(6, "hidden", "test_stage6.py", """# req: R6.1
from arena import Arena
from arena.mapgen import bordered_world
from arena.model import Event, Point

def test_generated_events_monotone():
    g = Arena(1,bordered_world(7,7))
    g.add_player(); g.add_enemy('rat', Point(2,1), hp=1)
    g.player_move('hero',1,0)
    assert [e.seq for e in g.world.events] == list(range(1,len(g.world.events)+1))

def test_sequence_persists_after_event_clear():
    w=bordered_world(7,7)
    w.emit(Event('a','hero')); w.clear_events(); w.emit(Event('b','hero'))
    assert w.events[-1].seq == 2
""")
    put(6, "", "static_checks.py", """# req: R6.1
import ast
from pathlib import Path

def test_no_raw_event_append_outside_world():
    root = Path(__file__).resolve().parents[1] / 'arena'
    for path in root.glob('*.py'):
        if path.name == 'model.py':
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert not (node.func.attr == 'append' and
                            isinstance(node.func.value, ast.Attribute) and
                            node.func.value.attr == 'events'), str(path)
""")
    put(6, "", "request.md", """New global constraint R6.1: every game event,
from every mechanic, must receive a unique monotonically increasing sequence
number when appended. Keep this constraint in stages 7 and 8. Use one shared
World event-emission path; do not manually append game events in subsystems.
""")
    write_patch(REFERENCE / "s6.patch", patch(previous, files))
    previous = files.copy()

    # S7: scripted antidote crash and completion of S3's deferred request.
    put(7, "", "supersedes.json", json.dumps(["tests/hidden_3/test_stage3_deferred.py"], indent=2))
    put(7, "", "scenario.py", """from arena.inventory import Bag, use
from arena.mapgen import bordered_world
from arena.model import Actor, Item, Point
world = bordered_world(7,7)
actor = Actor('hero', Point(1,1), 5, 5, 1, 'p', '@')
actor.statuses['poison'] = 3
bag = Bag(items=[Item('ant', 'antidote', 0)])
use(world, actor, bag, 'ant')
assert 'poison' not in actor.statuses
""")
    change(files, "arena/inventory.py", '''    if item.kind == "shield_tonic":
''', '''    if item.kind == "antidote":
        removed = int(actor.statuses.pop("poison", None) is not None)
        world.emit(Event("cure", actor.actor_id, amount=removed))
        return removed
    if item.kind == "shield_tonic":
''')
    put(7, "visible", "test_stage7.py", """# req: R7.1
from arena.inventory import Bag, use
from arena.mapgen import bordered_world
from arena.model import Actor, Item, Point

def test_antidote_stops_poison():
    w=bordered_world(7,7); a=Actor('a',Point(1,1),2,5,1,'p','@')
    a.statuses['poison']=2
    bag=Bag(items=[Item('ant','antidote')])
    use(w,a,bag,'ant')
    assert not a.statuses and not bag.items
""")
    put(7, "hidden", "test_stage7.py", """# req: R7.1 and deferred R3.3
from arena.inventory import Bag, use
from arena.mapgen import bordered_world
from arena.model import Actor, Item, Point

def test_antidote_does_not_heal_or_grant_shield():
    w=bordered_world(7,7); a=Actor('a',Point(1,1),2,5,1,'p','@',shield=1)
    a.statuses['poison']=3
    bag=Bag(items=[Item('ant','antidote')])
    use(w,a,bag,'ant')
    assert (a.hp,a.shield)==(2,1) and 'poison' not in a.statuses

def test_antidote_event_has_sequence():
    w=bordered_world(7,7); a=Actor('a',Point(1,1),2,5,1,'p','@')
    a.statuses['poison']=3
    bag=Bag(items=[Item('ant','antidote')])
    use(w,a,bag,'ant')
    assert w.events[-1].seq == 1
""")
    put(7, "", "request.md", """A headless playtest crashes when the hero
uses a newly found ant item; run the stage7 scenario and diagnose the root
cause. Also complete the item explicitly deferred at stage 3. Preserve all
earlier designer decisions and the global event constraint.
""")
    write_patch(REFERENCE / "s7.patch", patch(previous, files))
    previous = files.copy()

    # S8: persistent shields and backward-compatible version-1 saves.
    change(files, "arena/save.py", '            "glyph": a.glyph, "statuses": a.statuses,',
           '            "glyph": a.glyph, "statuses": a.statuses, "shield": a.shield,')
    change(files, "arena/save.py", '''        actor.statuses = dict(row["statuses"])
''', '''        actor.statuses = dict(row["statuses"])
        actor.shield = max(0, int(row.get("shield", 0)))
''')
    put(8, "visible", "test_stage8.py", """# req: R8.1
from arena import Arena
from arena.mapgen import bordered_world
from arena.save import dumps, loads

def test_save_shield_roundtrip():
    g=Arena(1,bordered_world(7,7)); a=g.add_player(); a.shield=4
    world,_=loads(dumps(g.world,g.bags))
    assert world.actors['hero'].shield==4
""")
    put(8, "hidden", "test_stage8.py", """# req: R8.1
import json
from arena import Arena
from arena.mapgen import bordered_world
from arena.save import dumps, loads

def test_old_save_defaults_to_zero_shield():
    g=Arena(1,bordered_world(7,7)); g.add_player().shield=4
    data=json.loads(dumps(g.world,g.bags))
    assert data['actors'][0]['shield']==4
    for actor in data['actors']:
        actor.pop('shield',None)
    world,_=loads(json.dumps(data))
    assert world.actors['hero'].shield==0

def test_shield_and_antidote_items_integrate():
    g=Arena(1,bordered_world(7,7)); a=g.add_player(); a.shield=3
    from arena.model import Item
    g.bags['hero'].add(Item('ant','antidote'))
    world,bags=loads(dumps(g.world,g.bags))
    assert world.actors['hero'].shield==3
    assert bags['hero'].find('antidote').item_id=='ant'
""")
    put(8, "", "request.md", """Complete cross-system integration: save and
load every player state introduced in the earlier stages, including shield,
while preserving compatibility with older version-1 saves that omitted it.
Inventory items and the event sequence must still survive round-trip.
""")
    write_patch(REFERENCE / "s8.patch", patch(previous, files))

    # Probe IDs use the names observed by pytest after hidden overlay.
    probes = [{"introduced": 1, "retired": 2, "tests": [f"Q{i}" for i in range(1,9)],
               "text_only": False, "requirement": "R1.1"}]
    definitions = [
        (2, "R2.1", ["test_shield_direct_damage"], False, 5),
        (2, "R2.2", ["test_poison_never_kills_or_uses_shield"], True, None),
        (3, "R3.1", ["test_tonic_does_not_heal"], False, None),
        (3, "R3.2", ["test_tonic_capped_at_five"], True, None),
        (3, "R3.3", ["test_antidote_still_deferred"], True, 7),
        (4, "R4.1", ["test_paths_do_not_cross_interior_walls"], False, None),
        (5, "R5.1", ["test_piercing_event_and_dependents"], False, None),
        (6, "R6.1", ["test_generated_events_monotone", "test_sequence_persists_after_event_clear"], False, None),
        (7, "R3.3", ["test_antidote_does_not_heal_or_grant_shield"], True, None),
        (7, "R7.1", ["test_antidote_event_has_sequence"], False, None),
        (8, "R8.1", ["test_old_save_defaults_to_zero_shield", "test_shield_and_antidote_items_integrate"], False, None),
    ]
    for introduced, rid, names, text_only, retired in definitions:
        basename = ("test_stage2_direct.py" if rid == "R2.1" else
                    "test_stage2_poison.py" if rid == "R2.2" else
                    "test_stage3_deferred.py" if rid == "R3.3" and introduced == 3 else
                    f"test_stage{introduced}.py")
        ids = [f"tests/hidden_{introduced}/{basename}::{name}" for name in names]
        probes.append({"introduced": introduced, "retired": retired,
                       "tests": ids, "text_only": text_only, "requirement": rid})
    (ROOT / "manifest.json").write_text(json.dumps({
        "project": "dev_arena", "kind": "development", "stages": 8,
        "orientation_answers": {"q1": "arena.model", "q2": "arena.mapgen.generate",
            "q3": 1, "q4": "death", "q5": "arena.ai.choose_action",
            "q6": "arena.path.shortest_path", "q7": 6, "q8": "arena.hud"},
        "probes": probes,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
