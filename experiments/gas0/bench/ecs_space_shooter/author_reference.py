"""Generate eight staged reference patches for the ECS shooter benchmark."""

from __future__ import annotations

import difflib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STARTER = ROOT / "starter"
STAGES = ROOT / "stages"
REFERENCE = ROOT / "reference"


def snapshot():
    return {
        path.relative_to(STARTER).as_posix(): path.read_text(encoding="utf-8")
        for path in STARTER.rglob("*.py")
        if "__pycache__" not in path.parts
    }


def diff(before, after):
    result = []
    for name in sorted(set(before) | set(after)):
        left = before.get(name, "").splitlines(keepends=True)
        right = after.get(name, "").splitlines(keepends=True)
        if left != right:
            result.extend(difflib.unified_diff(
                left, right,
                fromfile=f"a/{name}" if name in before else "/dev/null",
                tofile=f"b/{name}" if name in after else "/dev/null"))
    return "".join(result).encode("utf-8")


def change(state, path, old, new):
    if state[path].count(old) != 1:
        raise AssertionError((path, old, state[path].count(old)))
    state[path] = state[path].replace(old, new)


def put(stage, folder, name, body):
    target = STAGES / f"s{stage}" / folder / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body.strip() + "\n", encoding="utf-8")


def emit(stage, before, after, request, visible, hidden,
         visible_name=None, hidden_name=None):
    (REFERENCE / f"s{stage}.patch").write_bytes(diff(before, after))
    put(stage, "", "request.md", request)
    put(stage, "visible", visible_name or f"test_ecs_stage{stage}.py", visible)
    put(stage, "hidden", hidden_name or f"test_ecs_stage{stage}.py", hidden)


def main():
    for folder in (STAGES, REFERENCE):
        if folder.exists():
            shutil.rmtree(folder)
    STAGES.mkdir()
    REFERENCE.mkdir()
    state = snapshot()
    put(1, "", "request.md", """Do not edit. Inspect the ECS shooter and return JSON q1 through q8:
q1 Entity; q2 World; q3 entity allocator; q4 collision event; q5 spatial query;
q6 projectile spawn; q7 fixed update; q8 world save function. Use exact
identifiers.""")
    (REFERENCE / "s1.patch").write_bytes(b"")
    put(1, "visible", "test_ecs_stage1.py", "def test_orientation_is_read_only():\n    assert True")
    put(1, "hidden", "test_ecs_stage1.py", "def test_stage_one_preserves_starter():\n    assert True")
    previous = state.copy()

    # S2: direct hits consume shields before health.
    change(state, "spaceecs/model.py",
           '    faction: str = "neutral"\n    alive: bool = True\n',
           '    faction: str = "neutral"\n    alive: bool = True\n    shield: int = 0\n')
    change(state, "spaceecs/model.py",
           '    if any(entity.hp < 0 for entity in world.entities.values()):\n        raise ValueError("health is nonnegative")\n',
           '    if any(entity.hp < 0 or entity.shield < 0 for entity in world.entities.values()):\n'
           '        raise ValueError("health and shield are nonnegative")\n')
    change(state, "spaceecs/combat.py",
           "    absorbed = 0\n    dealt = min(entity.hp, incoming)\n",
           "    absorbed = min(entity.shield, incoming)\n    entity.shield -= absorbed\n"
           "    dealt = min(entity.hp, incoming - absorbed)\n")
    emit(2, previous, state,
         """Add shield to entities. A direct hit consumes shield before health;
excess damage carries into health. Keep HP at zero after lethal damage, and
leave entities without shield unchanged.""",
         """from spaceecs.combat import apply_damage
from spaceecs.ids import spawn_enemy
from spaceecs.model import World

def test_shield_absorbs_damage_before_health():
    world = World()
    enemy = spawn_enemy(world, 0, 0, hp=7)
    enemy.shield = 3
    assert apply_damage(world, enemy.entity_id, 2) == 2
    assert enemy.shield == 1 and enemy.hp == 7
""",
         """from spaceecs.combat import apply_damage
from spaceecs.ids import spawn_enemy
from spaceecs.model import World

def test_excess_hit_spills_from_shield_to_health():
    world = World()
    enemy = spawn_enemy(world, 0, 0, hp=7)
    enemy.shield = 2
    assert apply_damage(world, enemy.entity_id, 5) == 5
    assert enemy.shield == 0 and enemy.hp == 4

def test_no_shield_preserves_direct_damage():
    world = World()
    enemy = spawn_enemy(world, 0, 0, hp=7)
    assert apply_damage(world, enemy.entity_id, 3) == 3
    assert enemy.hp == 4
""")
    previous = state.copy()

    # S3: collision output has stable ID order; piercing is deferred.
    change(state, "spaceecs/collision.py",
           "    return events\n\n\ndef event_payload",
           "    return sorted(events, key=lambda event: (event.projectile_id, event.target_id))\n\n\ndef event_payload")
    emit(3, previous, state,
         """Make equal-tick collision event ordering independent of component
table insertion order. Sort by projectile ID and then target entity ID. Decide
that a future piercing projectile may affect multiple targets; defer piercing
until Stage 7.""",
         """from spaceecs.collision import detect_all_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import spawn_projectile

def test_collision_events_are_sorted_by_ids():
    world = World()
    owner = spawn_player(world, 0, 0)
    first = spawn_enemy(world, 2, 0)
    second = spawn_enemy(world, 2, 0)
    shot = spawn_projectile(world, owner.entity_id, 2, 0, 0, 0)
    world.entities = {second.entity_id: second, owner.entity_id: owner,
                      first.entity_id: first, shot.entity_id: world.entities[shot.entity_id]}
    events = detect_all_hits(world)
    assert [event.target_id for event in events] == sorted([first.entity_id, second.entity_id])
""",
         """from spaceecs.collision import detect_all_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import spawn_projectile

def test_target_ties_ignore_component_table_order():
    world = World()
    owner = spawn_player(world)
    first = spawn_enemy(world, 1, 0)
    second = spawn_enemy(world, 1, 0)
    shot = spawn_projectile(world, owner.entity_id, 1, 0, 0, 0)
    world.entities = {second.entity_id: second, first.entity_id: first,
                      owner.entity_id: owner, shot.entity_id: world.entities[shot.entity_id]}
    events = detect_all_hits(world)
    assert [event.target_id for event in events] == [first.entity_id, second.entity_id]
""")
    put(3, "hidden", "test_ecs_stage3_all_hits.py",
        """from spaceecs.collision import detect_all_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import spawn_projectile

def test_point_collision_reports_all_overlapping_targets():
    world = World()
    owner = spawn_player(world)
    a = spawn_enemy(world, 2, 0)
    b = spawn_enemy(world, 2, 0)
    spawn_projectile(world, owner.entity_id, 2, 0, 0, 0, radius=0.5)
    projectile = next(iter(world.projectiles.values()))
    world.entities = {b.entity_id: b, a.entity_id: a,
                      owner.entity_id: owner,
                      projectile.entity_id: world.entities[projectile.entity_id]}
    events = detect_all_hits(world)
    assert [event.target_id for event in events] == sorted([a.entity_id, b.entity_id])
""")
    put(3, "hidden", "test_ecs_piercing_deferred.py",
        """import importlib.util

def test_piercing_is_deferred():
    assert importlib.util.find_spec("spaceecs.piercing") is None
""")
    put(3, "", "supersedes.json", "[]")
    previous = state.copy()

    # S4 injects a broad-query high-cell omission, not exercised by earlier tests.
    bugged = state.copy()
    change(bugged, "spaceecs/spatial.py",
           "    high_x = floor((float(x) + radius) / size)\n",
           "    high_x = floor((float(x) + radius) / size) - int(float(radius) >= 1.0)\n")
    (STAGES / "s4").mkdir(parents=True, exist_ok=True)
    (STAGES / "s4" / "bug.patch").write_bytes(diff(state, bugged))
    emit(4, bugged, state,
         """A wide spatial query misses entities that lie in its upper boundary
cell. Diagnose the cell-range regression and restore inclusive broad-phase
coverage without changing exact distance filtering.""",
         """from spaceecs.ids import spawn_enemy
from spaceecs.model import World
from spaceecs.spatial import build_grid, nearby

def test_wide_query_includes_upper_boundary_cell():
    world = World()
    target = spawn_enemy(world, 2.0, 0.0)
    grid = build_grid([target])
    assert [e.entity_id for e in nearby(grid, 0.9, 0.0, 1.2)] == [target.entity_id]
""",
         """from spaceecs.ids import spawn_enemy
from spaceecs.model import World
from spaceecs.spatial import build_grid, nearby

def test_wide_query_keeps_exact_max_cell():
    world = World()
    target = spawn_enemy(world, 2.0, 0.0)
    grid = build_grid([target])
    assert target in nearby(grid, 0.9, 0.0, 1.2)
""")
    previous = state.copy()

    # S5 replaces endpoint collision with earliest swept hit; multiple hits retire.
    change(state, "spaceecs/collision.py",
           "def detect_projectile_hits(world, projectile_id):\n",
           "def segment_hit_time(projectile, entity):\n"
           "    dx = projectile.x - projectile.previous_x\n"
           "    dy = projectile.y - projectile.previous_y\n"
           "    length_sq = dx * dx + dy * dy\n"
           "    if length_sq == 0:\n        return 0.0 if overlap(projectile, entity) else None\n"
           "    t = ((entity.x - projectile.previous_x) * dx + "
           "(entity.y - projectile.previous_y) * dy) / length_sq\n"
           "    t = max(0.0, min(1.0, t))\n"
           "    px = projectile.previous_x + t * dx\n"
           "    py = projectile.previous_y + t * dy\n"
           "    return t if distance(px, py, entity.x, entity.y) <= projectile.radius else None\n\n"
           "def detect_projectile_hits(world, projectile_id):\n")
    change(state, "spaceecs/collision.py",
           "        if overlap(projectile, entity):\n"
           "            events.append(CollisionEvent(projectile.entity_id, entity.entity_id))\n"
           "    return events\n",
           "        hit_time = segment_hit_time(projectile, entity)\n"
           "        if hit_time is not None:\n"
           "            events.append(CollisionEvent(projectile.entity_id, entity.entity_id, hit_time))\n"
           "    events.sort(key=lambda event: (event.time, event.target_id))\n"
           "    return events[:1]\n")
    emit(5, previous, state,
         """Replace endpoint-only projectile collision with swept collision
along the segment from previous to current position. Choose the earliest hit;
break equal-time ties by target ID. Retire the former all-overlap point-hit
contract.""",
         """from spaceecs.collision import detect_projectile_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import move_projectile, spawn_projectile

def test_fast_projectile_cannot_skip_crossed_target():
    world = World()
    owner = spawn_player(world, 0, 0)
    target = spawn_enemy(world, 2, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 4, 0, radius=0.2)
    move_projectile(shot)
    assert detect_projectile_hits(world, shot.entity_id)[0].target_id == target.entity_id
""",
         """from spaceecs.collision import detect_projectile_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import move_projectile, spawn_projectile

def test_nearest_swept_target_wins():
    world = World()
    owner = spawn_player(world)
    near = spawn_enemy(world, 1, 0)
    spawn_enemy(world, 3, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 4, 0, radius=0.2)
    move_projectile(shot)
    events = detect_projectile_hits(world, shot.entity_id)
    assert len(events) == 1 and events[0].target_id == near.entity_id
    assert events[0].time < 0.5

def test_equal_time_swept_hit_uses_target_id():
    world = World()
    owner = spawn_player(world)
    first = spawn_enemy(world, 2, 0)
    second = spawn_enemy(world, 2, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 4, 0, radius=0.2)
    move_projectile(shot)
    assert detect_projectile_hits(world, shot.entity_id)[0].target_id == min(first.entity_id, second.entity_id)
""")
    put(5, "", "supersedes.json", json.dumps([
        "tests/hidden_3/test_ecs_stage3_all_hits.py",
        "tests/hidden_3/test_ecs_stage3.py",
        "tests/test_ecs_stage3.py",
    ]))
    previous = state.copy()

    # S6 removes ID reuse; IDs increase monotonically for a world's lifetime.
    change(state, "spaceecs/model.py",
           "    free_ids: list[int] = field(default_factory=list)\n", "")
    change(state, "spaceecs/model.py",
           "    if world.free_ids:\n"
           "        entity_id = min(world.free_ids)\n"
           "        world.free_ids.remove(entity_id)\n"
           "    else:\n"
           "        entity_id = world.next_entity_id\n"
           "        world.next_entity_id += 1\n",
           "    entity_id = world.next_entity_id\n    world.next_entity_id += 1\n")
    change(state, "spaceecs/model.py",
           "    if entity is not None:\n        entity.alive = False\n        world.free_ids.append(entity_id)\n",
           "    if entity is not None:\n        entity.alive = False\n")
    change(state, "spaceecs/model.py",
           "    if set(world.entities).intersection(world.free_ids):\n"
           "        raise ValueError(\"live identifiers cannot also be free\")\n", "")
    change(state, "spaceecs/ids.py",
           "def smallest_free_id(world):\n    return min(world.free_ids) if world.free_ids else None\n\n\n", "")
    emit(6, previous, state,
         """Entity identifiers must increase monotonically for the lifetime of
each World and must never be reused after removal. Keep identifier allocation
world-local. Add a static guard against reintroducing a free-list allocator.""",
         """from spaceecs.ids import spawn_enemy
from spaceecs.model import World, remove_entity

def test_removed_ids_are_not_reused():
    world = World()
    first = spawn_enemy(world, 0, 0)
    remove_entity(world, first.entity_id)
    second = spawn_enemy(world, 0, 0)
    assert second.entity_id > first.entity_id
""",
         """from spaceecs.ids import spawn_enemy
from spaceecs.model import World, remove_entity

def test_ids_strictly_increase_across_removal():
    world = World()
    ids = []
    for index in range(4):
        entity = spawn_enemy(world, index, 0)
        ids.append(entity.entity_id)
        if index % 2 == 0:
            remove_entity(world, entity.entity_id)
    later = spawn_enemy(world, 5, 0)
    assert ids == sorted(set(ids))
    assert later.entity_id > max(ids)
""")
    put(6, "", "static_checks.py",
        """import ast
from pathlib import Path

def test_allocator_has_no_free_list_reuse():
    package = Path(__file__).parents[1] / "spaceecs"
    tree = ast.parse((package / "model.py").read_text())
    reused = [node for node in ast.walk(tree)
              if isinstance(node, ast.Attribute) and node.attr == "free_ids"]
    assert reused == []
    source = (package / "model.py").read_text()
    allocator = source.split("def create_entity", 1)[1].split("def remove_entity", 1)[0]
    assert "next_entity_id" in allocator
""")
    previous = state.copy()

    # S7 tolerates stale collision references and adds deferred piercing.
    change(state, "spaceecs/model.py",
           "    radius: float = 0.25\n",
           "    radius: float = 0.25\n    piercing: bool = False\n")
    change(state, "spaceecs/combat.py",
           "        target_id = event.target_id\n"
           "        world.entities[target_id]\n"
           "        projectile = world.projectiles[event.projectile_id]\n"
           "        results.append(apply_damage(world, target_id, projectile.damage,\n"
           "                                    projectile.owner_id))\n",
           "        target_id = event.target_id\n"
           "        projectile = world.projectiles.get(event.projectile_id)\n"
           "        if projectile is None or target_id not in world.entities:\n"
           "            continue\n"
           "        results.append(apply_damage(world, target_id, projectile.damage,\n"
           "                                    projectile.owner_id))\n")
    state["spaceecs/piercing.py"] = """from .combat import apply_damage

MAX_PIERCING_TARGETS = 3

def enable_piercing(projectile):
    projectile.piercing = True
    return projectile

def resolve_piercing(world, projectile_id, events):
    projectile = world.projectiles.get(int(projectile_id))
    if projectile is None or not projectile.piercing:
        return []
    seen = set()
    applied = []
    ordered = sorted(events, key=lambda event: (event.time, event.target_id))
    for event in ordered:
        if event.projectile_id != projectile.entity_id:
            continue
        if event.target_id in seen or event.target_id not in world.entities:
            continue
        if len(seen) >= MAX_PIERCING_TARGETS:
            break
        seen.add(event.target_id)
        applied.append(apply_damage(
            world, event.target_id, projectile.damage, projectile.owner_id))
    return applied
"""
    emit(7, previous, state,
         """A projectile may retain collision events for an entity that was
removed earlier in the same update. Make event resolution tolerate stale
references. Implement the deferred piercing behavior for piercing projectiles;
unrelated entities and repeated contacts must not be damaged twice.""",
         """from spaceecs.collision import CollisionEvent
from spaceecs.combat import resolve_events
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World, remove_entity
from spaceecs.projectiles import spawn_projectile

def test_stale_collision_target_is_ignored():
    world = World()
    owner = spawn_player(world)
    target = spawn_enemy(world, 1, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 1, 0)
    remove_entity(world, target.entity_id)
    assert resolve_events(world, [CollisionEvent(shot.entity_id, target.entity_id)]) == []
""",
         """from spaceecs.collision import CollisionEvent
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.piercing import enable_piercing, resolve_piercing
from spaceecs.projectiles import spawn_projectile

def test_piercing_hits_at_most_three_distinct_live_targets():
    world = World()
    owner = spawn_player(world)
    targets = [spawn_enemy(world, i, 0, hp=5) for i in range(5)]
    shot = enable_piercing(spawn_projectile(world, owner.entity_id, 0, 0, 1, 0, damage=1))
    events = [CollisionEvent(shot.entity_id, item.entity_id, index / 10)
              for index, item in enumerate(targets)]
    events.insert(1, CollisionEvent(shot.entity_id, targets[0].entity_id, 0.15))
    resolve_piercing(world, shot.entity_id, events)
    assert [item.hp for item in targets] == [4, 4, 4, 5, 5]

def test_stale_and_duplicate_ids_do_not_use_hit_budget():
    from spaceecs.model import remove_entity
    world = World()
    owner = spawn_player(world)
    targets = [spawn_enemy(world, i, 0, hp=5) for i in range(4)]
    shot = enable_piercing(spawn_projectile(world, owner.entity_id, 0, 0, 1, 0))
    remove_entity(world, targets[0].entity_id)
    events = [CollisionEvent(shot.entity_id, targets[0].entity_id, 0.0)]
    events += [CollisionEvent(shot.entity_id, item.entity_id, i / 10)
               for i, item in enumerate(targets[1:], 1)]
    resolve_piercing(world, shot.entity_id, events)
    assert [item.hp for item in targets[1:]] == [4, 4, 4]

def test_resolve_event_skips_removed_target():
    from spaceecs.combat import resolve_events
    from spaceecs.model import remove_entity
    world = World()
    owner = spawn_player(world)
    target = spawn_enemy(world, 1, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 1, 0)
    remove_entity(world, target.entity_id)
    assert resolve_events(world, [CollisionEvent(shot.entity_id, target.entity_id)]) == []
""",
         hidden_name="test_ecs_stage7_audit.py")
    put(7, "hidden", "test_ecs_piercing_deferred_stage7.py",
        """from spaceecs.collision import CollisionEvent
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.piercing import enable_piercing, resolve_piercing
from spaceecs.projectiles import spawn_projectile

def test_deferred_piercing_limit_is_enforced():
    world = World()
    owner = spawn_player(world)
    targets = [spawn_enemy(world, i, 0, hp=5) for i in range(5)]
    shot = enable_piercing(spawn_projectile(world, owner.entity_id, 0, 0, 1, 0))
    events = [CollisionEvent(shot.entity_id, e.entity_id, i) for i, e in enumerate(targets)]
    resolve_piercing(world, shot.entity_id, events)
    assert [e.hp for e in targets] == [4, 4, 4, 5, 5]
""")
    put(7, "", "supersedes.json", json.dumps(["tests/hidden_3/test_ecs_piercing_deferred.py"]))
    put(7, "", "scenario.py",
        """from spaceecs.collision import CollisionEvent
from spaceecs.combat import resolve_events
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World, remove_entity
from spaceecs.projectiles import spawn_projectile

world = World()
owner = spawn_player(world)
enemy = spawn_enemy(world, 1, 0)
shot = spawn_projectile(world, owner.entity_id, 0, 0, 1, 0)
remove_entity(world, enemy.entity_id)
print(resolve_events(world, [CollisionEvent(shot.entity_id, enemy.entity_id)]))
""")
    previous = state.copy()

    # S8 preserves entities, shields, projectiles, and allocator continuation.
    change(state, "spaceecs/save.py",
           '"faction": e.faction, "alive": e.alive}',
           '"faction": e.faction, "alive": e.alive, "shield": e.shield}')
    change(state, "spaceecs/save.py",
           '            row["faction"], row["alive"])\n',
           '            row["faction"], row["alive"], row.get("shield", 0))\n')
    change(state, "spaceecs/save.py",
           '"damage": p.damage, "radius": p.radius}',
           '"damage": p.damage, "radius": p.radius, "piercing": p.piercing}')
    change(state, "spaceecs/save.py",
           '            row["vx"], row["vy"], row["damage"], row["radius"])\n',
           '            row["vx"], row["vy"], row["damage"], row["radius"],\n'
           '            row.get("piercing", False))\n')
    emit(8, previous, state,
         """Add deterministic world save/load. Preserve shield, projectile
motion endpoints and piercing state, events, tick, and the next entity ID.
Old core payloads may load with defaults for fields introduced later.""",
         """from spaceecs.ids import spawn_enemy
from spaceecs.model import World
from spaceecs.save import load_world, save_world

def test_world_round_trip_preserves_core_state():
    world = World(tick_count=7)
    enemy = spawn_enemy(world, 2, 3, hp=6)
    restored = load_world(save_world(world))
    assert restored.tick_count == 7
    assert restored.entities[enemy.entity_id].hp == 6
""",
         """from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.piercing import enable_piercing
from spaceecs.projectiles import spawn_projectile
from spaceecs.save import load_world, save_world

def test_round_trip_preserves_shield_and_piercing():
    world = World(tick_count=4)
    owner = spawn_player(world)
    enemy = spawn_enemy(world, 2, 0)
    enemy.shield = 4
    shot = enable_piercing(spawn_projectile(world, owner.entity_id, 1, 0, 2, 0))
    restored = load_world(save_world(world))
    assert restored.entities[enemy.entity_id].shield == 4
    assert restored.projectiles[shot.entity_id].piercing

def test_next_identifier_survives_round_trip():
    world = World()
    spawn_enemy(world, 0, 0)
    restored = load_world(save_world(world))
    next_entity = spawn_enemy(restored, 1, 0)
    assert next_entity.entity_id == world.next_entity_id
""")
    put(8, "", "supersedes.json", "[]")

    manifest = {
        "project": "ecs_space_shooter",
        "kind": "evaluation",
        "stages": 8,
        "orientation_answers": {
            "q1": "spaceecs.model.Entity",
            "q2": "spaceecs.model.World",
            "q3": "spaceecs.model.create_entity",
            "q4": "spaceecs.collision.CollisionEvent",
            "q5": "spaceecs.spatial.nearby",
            "q6": "spaceecs.projectiles.spawn_projectile",
            "q7": "spaceecs.game.tick",
            "q8": "spaceecs.save.save_world",
        },
        "probes": [
            {"introduced": 1, "retired": 2, "tests": [f"Q{i}" for i in range(1, 9)],
             "text_only": False, "requirement": "R1.1"},
            {"introduced": 2, "retired": None,
             "tests": ["tests/hidden_2/test_ecs_stage2.py::test_excess_hit_spills_from_shield_to_health"],
             "text_only": False, "requirement": "R2.1"},
            {"introduced": 3, "retired": 5,
             "tests": ["tests/hidden_3/test_ecs_stage3.py::test_target_ties_ignore_component_table_order"],
             "text_only": False, "requirement": "R3.1"},
            {"introduced": 3, "retired": 7,
             "tests": ["tests/hidden_3/test_ecs_piercing_deferred.py::test_piercing_is_deferred"],
             "text_only": True, "requirement": "D3.1"},
            {"introduced": 4, "retired": None,
             "tests": ["tests/hidden_4/test_ecs_stage4.py::test_wide_query_keeps_exact_max_cell"],
             "text_only": False, "requirement": "R4.1"},
            {"introduced": 5, "retired": None,
             "tests": ["tests/hidden_5/test_ecs_stage5.py::test_nearest_swept_target_wins",
                       "tests/hidden_5/test_ecs_stage5.py::test_equal_time_swept_hit_uses_target_id"],
             "text_only": False, "requirement": "R5.1"},
            {"introduced": 3, "retired": 5,
             "tests": ["tests/hidden_3/test_ecs_stage3_all_hits.py::test_point_collision_reports_all_overlapping_targets"],
             "text_only": False, "requirement": "R3.3"},
            {"introduced": 6, "retired": None,
             "tests": ["tests/hidden_6/test_ecs_stage6.py::test_ids_strictly_increase_across_removal"],
             "text_only": False, "requirement": "G6.1"},
            {"introduced": 7, "retired": None,
             "tests": ["tests/hidden_7/test_ecs_stage7_audit.py::test_resolve_event_skips_removed_target",
                       "tests/hidden_7/test_ecs_piercing_deferred_stage7.py::test_deferred_piercing_limit_is_enforced"],
             "text_only": False, "requirement": "D3.1"},
            {"introduced": 8, "retired": None,
             "tests": ["tests/hidden_8/test_ecs_stage8.py::test_round_trip_preserves_shield_and_piercing"],
             "text_only": False, "requirement": "R8.1"},
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("wrote ECS space-shooter stages and reference patches")


if __name__ == "__main__":
    main()
