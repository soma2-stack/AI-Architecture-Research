"""Generate frozen staged tests and cumulative reference patches."""

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


def unified(before, after):
    result = []
    for name in sorted(set(before) | set(after)):
        left = before.get(name, "").splitlines(keepends=True)
        right = after.get(name, "").splitlines(keepends=True)
        if left != right:
            result.extend(
                difflib.unified_diff(
                    left,
                    right,
                    fromfile=f"a/{name}" if name in before else "/dev/null",
                    tofile=f"b/{name}" if name in after else "/dev/null",
                )
            )
    return "".join(result).encode("utf-8")


def change(state, name, old, new):
    if state[name].count(old) != 1:
        raise AssertionError((name, old, state[name].count(old)))
    state[name] = state[name].replace(old, new)


def put(stage, folder, name, body):
    path = STAGES / f"s{stage}" / folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")


def save_patch(stage, before, after):
    (REFERENCE / f"s{stage}.patch").write_bytes(unified(before, after))


def emit_stage(stage, before, after, request, visible, hidden):
    save_patch(stage, before, after)
    put(stage, "", "request.md", request)
    put(stage, "visible", f"test_tower_stage{stage}.py", visible)
    put(stage, "hidden", f"test_tower_stage{stage}.py", hidden)


def main():
    for folder in (STAGES, REFERENCE):
        if folder.exists():
            shutil.rmtree(folder)
    STAGES.mkdir()
    REFERENCE.mkdir()
    state = snapshot()
    put(
        1,
        "",
        "request.md",
        """Do not edit. Inspect the tower-defense project and return JSON with q1
through q8: q1 Tower type; q2 Enemy type; q3 target selector; q4 attack
resolver; q5 wave spawn function; q6 path length; q7 Game tick function; q8
save function. Use exact identifiers.""",
    )
    (REFERENCE / "s1.patch").write_bytes(b"")
    put(1, "visible", "test_tower_stage1.py", "def test_stage_one_is_orientation_only():\n    assert True")
    put(1, "hidden", "test_tower_stage1.py", "def test_stage_one_has_no_hidden_behavior_change():\n    assert True")
    previous = state.copy()

    # Stage 2: slow status affects movement, while the old selector remains.
    change(
        state,
        "td/model.py",
        '    kind: str = "basic"\n',
        '    kind: str = "basic"\n    slow_ticks: int = 0\n',
    )
    state["td/slow.py"] = """from .model import Event

def apply_slow(game, enemy, ticks=2):
    enemy.slow_ticks = max(getattr(enemy, "slow_ticks", 0), int(ticks))
    game.events.append(Event(game.tick_count, "slow", "slow_tower", enemy.enemy_id, enemy.slow_ticks))
    return enemy.slow_ticks

def tick_slow(enemy):
    active = getattr(enemy, "slow_ticks", 0) > 0
    if active:
        enemy.slow_ticks -= 1
    return active
"""
    change(
        state,
        "td/pathing.py",
        "    for enemy in game.enemies:\n        if advance_enemy(enemy, distance):",
        "    from .slow import tick_slow\n    for enemy in game.enemies:\n        if enemy.alive and tick_slow(enemy):\n            continue\n        if advance_enemy(enemy, distance):",
    )
    put(
        2,
        "",
        "request.md",
        """Add a slow tower effect. A slow hit sets the enemy's duration to at least
two ticks; while slowed, path progress does not advance and duration decreases
once per game tick. A later slow refresh may extend duration but never shorten
it. Basic tower behavior remains unchanged.""",
    )
    emit_stage(
        2,
        previous,
        state,
        (STAGES / "s2" / "request.md").read_text(),
        """from td.model import Enemy, Game
from td.pathing import move_enemies
from td.slow import apply_slow

def test_slow_prevents_one_movement_step():
    game = Game(enemies=[Enemy("e", 4, 5, 5)])
    apply_slow(game, game.enemies[0], 2)
    assert move_enemies(game) == []
    assert game.enemies[0].progress == 4
""",
        """from td.model import Enemy, Game
from td.pathing import move_enemies
from td.slow import apply_slow

def test_slow_duration_expires_then_movement_resumes():
    game = Game(enemies=[Enemy("e", 1, 5, 5)])
    apply_slow(game, game.enemies[0], 2)
    move_enemies(game)
    move_enemies(game)
    assert game.enemies[0].progress == 1
    assert game.enemies[0].slow_ticks == 0
    move_enemies(game)
    assert game.enemies[0].progress == 2

def test_refresh_never_shortens_duration():
    enemy = Enemy("e", 1, 5, 5, slow_ticks=4)
    assert apply_slow(Game(enemies=[enemy]), enemy, 2) == 4
""",
    )
    put(
        2,
        "hidden",
        "test_tower_stage2_legacy.py",
        """from td.model import Enemy, Game, Tower
from td.targeting import choose_target

def test_legacy_selector_uses_stable_identifier_order():
    game = Game(enemies=[Enemy("b", 1, 5, 5), Enemy("a", 1, 5, 5)])
    assert choose_target(Tower("t", 1, 0), game).enemy_id == "a"
""",
    )
    put(2, "", "supersedes.json", "[]")
    previous = state.copy()

    # Stage 3: armor reduction plus deferred sell-refund decision.
    change(
        state,
        "td/model.py",
        "    slow_ticks: int = 0\n",
        "    slow_ticks: int = 0\n    armor: int = 0\n",
    )
    change(
        state,
        "td/combat.py",
        "    dealt = min(enemy.hp, amount)\n",
        "    amount = max(0, amount - max(0, int(getattr(enemy, 'armor', 0))))\n"
        "    dealt = min(enemy.hp, amount)\n",
    )
    emit_stage(
        3,
        previous,
        state,
        """Add armor to enemies. Direct tower damage is reduced by armor and never
becomes negative; unarmored enemies behave as before. Designer decision D3.1:
when a tower is sold in a later stage, refund 75% of its purchase cost rounded
down. Defer selling until Stage 7; do not implement it now.""",
        """from td.combat import fire_tower
from td.model import Enemy, Game, Tower

def test_armor_reduces_damage():
    enemy = Enemy("e", 1, 8, 8, armor=1)
    assert fire_tower(Game(enemies=[enemy]), Tower("t", 1, 0, damage=3)) == ("e", 2)
    assert enemy.hp == 6
""",
        """from td.combat import fire_tower
from td.model import Enemy, Game, Tower

def test_armor_cannot_heal_or_create_negative_damage():
    enemy = Enemy("e", 1, 5, 5, armor=9)
    assert fire_tower(Game(enemies=[enemy]), Tower("t", 1, 0, damage=2)) == ("e", 0)
    assert enemy.hp == 5

def test_unarmored_tower_damage_is_unchanged():
    enemy = Enemy("e", 1, 5, 5)
    assert fire_tower(Game(enemies=[enemy]), Tower("t", 1, 0, damage=2)) == ("e", 2)
    assert enemy.hp == 3
""",
    )
    put(
        3,
        "hidden",
        "test_tower_sell_deferred.py",
        """def test_tower_selling_is_deferred():
    import td.economy as economy
    assert not hasattr(economy, "sell_tower")
""",
    )
    put(3, "", "supersedes.json", "[]")
    previous = state.copy()

    # Stage 4 isolates a cooldown regression to the armored-enemy path added in S3.
    bugged = state.copy()
    change(
        bugged,
        "td/combat.py",
        "    tower.cooldown_left = tower.cooldown\n",
        "    armor_delay = max(0, int(getattr(target, 'armor', 0)))\n"
        "    tower.cooldown_left = tower.cooldown + armor_delay\n",
    )
    (STAGES / "s4").mkdir(parents=True, exist_ok=True)
    (STAGES / "s4" / "bug.patch").write_bytes(unified(state, bugged))
    emit_stage(
        4,
        bugged,
        state,
        """After the armor change, towers wait too long between shots at armored
enemies. Diagnose and correct the cooldown regression without changing damage,
target selection, or armor behavior.""",
        """from td.combat import fire_tower
from td.model import Enemy, Game, Tower

def test_configured_cooldown_is_set_after_a_hit():
    tower = Tower("t", 1, 0, cooldown=2)
    fire_tower(Game(enemies=[Enemy("e", 1, 9, 9, armor=1)]), tower)
    assert tower.cooldown_left == 2
""",
        """from td.combat import fire_tower
from td.model import Enemy, Game, Tower

def test_attack_becomes_ready_after_exact_wait():
    game = Game(enemies=[Enemy("e", 1, 20, 20, armor=1)])
    tower = Tower("t", 1, 0, damage=2, cooldown=2)
    fire_tower(game, tower)
    fire_tower(game, tower)
    fire_tower(game, tower)
    assert tower.cooldown_left == 0
    assert fire_tower(game, tower) == ("e", 1)
""",
    )
    previous = state.copy()

    # Stage 5 supersedes first-spawned selection with furthest-path targeting.
    change(
        state,
        "td/targeting.py",
        "    return min(candidates, key=lambda enemy: (enemy.enemy_id, enemy.progress))\n",
        "    furthest = max(enemy.progress for enemy in candidates)\n"
        "    return min((enemy for enemy in candidates if enemy.progress == furthest),\n"
        "               key=lambda enemy: enemy.enemy_id)\n",
    )
    put(
        5,
        "",
        "request.md",
        """Change target priority to the enemy furthest along the path (greatest
progress). Break equal-progress ties by ascending enemy ID. Keep range checks,
armor, cooldown, and damage semantics unchanged.""",
    )
    put(
        5,
        "visible",
        "test_tower_stage5.py",
        """from td.model import Enemy, Game, Tower
from td.targeting import choose_target

def test_target_is_furthest_along_path():
    game = Game(enemies=[Enemy("near", 2, 5, 5), Enemy("far", 8, 5, 5)])
    assert choose_target(Tower("t", 0, 0, radius=10), game).enemy_id == "far"
""",
    )
    put(
        5,
        "hidden",
        "test_tower_stage5.py",
        """from td.model import Enemy, Game, Tower
from td.targeting import choose_target

def test_furthest_progress_precedes_lexical_identifier():
    game = Game(enemies=[Enemy("a-near", 2, 5, 5), Enemy("z-far", 8, 5, 5)])
    assert choose_target(Tower("t", 0, 0, radius=10), game).enemy_id == "z-far"

def test_progress_tie_uses_ascending_id():
    game = Game(enemies=[Enemy("z", 8, 5, 5), Enemy("a", 8, 5, 5)])
    assert choose_target(Tower("t", 0, 0, radius=10), game).enemy_id == "a"

def test_out_of_range_furthest_enemy_is_ignored():
    game = Game(enemies=[Enemy("near", 2, 5, 5), Enemy("far", 9, 5, 5)])
    assert choose_target(Tower("t", 0, 0, radius=4), game).enemy_id == "near"
""",
    )
    put(
        5,
        "",
        "supersedes.json",
        json.dumps(["tests/test_targeting_legacy.py"]),
    )
    save_patch(5, previous, state)
    previous = state.copy()

    # Stage 6 routes all procedural variation through a per-game RNG.
    state["td/rng.py"] = """import random

class GameRNG:
    def __init__(self, seed=0):
        self._random = random.Random(int(seed))

    def randint(self, low, high):
        return self._random.randint(int(low), int(high))

    def choice(self, values):
        values = tuple(values)
        if not values:
            raise ValueError("cannot choose from an empty sequence")
        return self._random.choice(values)

    def getstate(self):
        return self._random.getstate()

    def setstate(self, state):
        self._random.setstate(state)
"""
    change(state, "td/model.py", "    wave: int = 0\n", "    wave: int = 0\n    seed: int = 0\n    rng: object = field(default=None, repr=False)\n")
    change(state, "td/pathing.py", "def spawn_wave(game, wave_number, count=3):", "def spawn_wave(game, wave_number, count=3):")
    change(
        state,
        "td/pathing.py",
        "    created = []\n    for index in range(max(0, int(count))):\n        hp = 4 + wave_number\n",
        "    if game.rng is None:\n        from .rng import GameRNG\n        game.rng = GameRNG(game.seed)\n"
        "    created = []\n    for index in range(max(0, int(count))):\n"
        "        hp = 4 + wave_number + game.rng.randint(0, 2)\n",
    )
    emit_stage(
        6,
        previous,
        state,
        """Route each randomized wave attribute through a seed-owned RNG attached
to its Game. Equal seeds replay identically; distinct Game instances must not
share state. Do not import or call module-global random outside td/rng.py.""",
        """from td.model import Game
from td.pathing import spawn_wave

def test_equal_seeds_replay_wave_health():
    first, second = Game(seed=8), Game(seed=8)
    assert [e.hp for e in spawn_wave(first, 1, 5)] == [e.hp for e in spawn_wave(second, 1, 5)]
""",
        """from td.model import Game
from td.pathing import spawn_wave

def test_rng_streams_are_owned_by_game():
    a, b, c = Game(seed=2), Game(seed=2), Game(seed=2)
    out_a = [e.hp for e in spawn_wave(a, 1, 4)]
    out_b = [e.hp for e in spawn_wave(b, 1, 4)]
    out_c = [e.hp for e in spawn_wave(c, 1, 4)]
    assert out_a == out_b == out_c

def test_distinct_seed_changes_generated_wave():
    a, b = Game(seed=1), Game(seed=9)
    assert [e.hp for e in spawn_wave(a, 1, 8)] != [e.hp for e in spawn_wave(b, 1, 8)]
""",
    )
    put(
        6,
        "",
        "static_checks.py",
        """import ast
from pathlib import Path

def test_random_module_is_confined_to_rng():
    package = Path(__file__).parents[1] / "td"
    offenders = []
    for path in package.glob("*.py"):
        if path.name == "rng.py":
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(alias.name == "random" for alias in node.names):
                offenders.append(path.name)
            if isinstance(node, ast.ImportFrom) and node.module == "random":
                offenders.append(path.name)
    assert offenders == []
""",
    )
    put(6, "", "supersedes.json", "[]")
    previous = state.copy()

    # Stage 7 fixes the known empty summary edge and implements the deferred sale.
    change(
        state,
        "td/game.py",
        "    most_advanced = max(enemy.progress for enemy in enemies)\n",
        "    most_advanced = max((enemy.progress for enemy in enemies), default=0)\n",
    )
    change(
        state,
        "td/economy.py",
        "def refund(game, amount):\n",
        "def sell_tower(game, tower_id):\n"
        "    tower = tower_by_id(game, tower_id)\n"
        "    if tower is None:\n        return 0\n"
        "    amount = int(tower.cost * 0.75)\n"
        "    game.towers.remove(tower)\n"
        "    game.money += amount\n"
        "    return amount\n\n"
        "def refund(game, amount):\n",
    )
    emit_stage(
        7,
        previous,
        state,
        """After the final enemy is defeated, the status screen crashes. Make
the empty-enemy summary safe. Add a sell action that removes an installed
tower immediately and credits its refund.""",
        """from td.economy import sell_tower
from td.game import summary
from td.model import Enemy, Game, Tower

def test_empty_enemy_summary_is_safe():
    game = Game(enemies=[Enemy("last", 20, 0, 5, alive=False)])
    assert summary(game)["enemies"] == 0
    assert summary(game)["furthest"] == 0

def test_selling_removes_tower_and_credits_refund():
    game = Game(money=0, towers=[Tower("t", 0, 0, cost=20)])
    assert sell_tower(game, "t") == 15
    assert game.money == 15 and game.towers == []
""",
        """from td.economy import sell_tower
from td.game import summary
from td.model import Enemy, Game, Tower

def test_summary_handles_final_defeat():
    game = Game(enemies=[Enemy("last", 20, 0, 5, alive=False)])
    assert summary(game)["furthest"] == 0

def test_sale_refund_rounds_down_and_unknown_id_is_noop():
    game = Game(money=2, towers=[Tower("t", 0, 0, cost=13)])
    assert sell_tower(game, "t") == 9 and game.money == 11
    assert sell_tower(game, "missing") == 0 and game.money == 11
""",
    )
    put(
        7,
        "hidden",
        "test_tower_stage7_deferred.py",
        """from td.economy import sell_tower
from td.model import Game, Tower

def test_deferred_sell_decision_uses_floor_of_three_quarters():
    game = Game(money=0, towers=[Tower("old", 0, 0, cost=11)])
    assert sell_tower(game, "old") == 8
    assert game.money == 8
""",
    )
    put(
        7,
        "",
        "scenario.py",
        """from td.game import summary
from td.model import Enemy, Game

game = Game(enemies=[Enemy("last", 20, 0, 5, alive=False)])
print(summary(game)["enemies"])
""",
    )
    put(
        7,
        "",
        "supersedes.json",
        json.dumps(["tests/hidden_3/test_tower_sell_deferred.py"]),
    )
    previous = state.copy()

    # Stage 8 persists the entire state, including the RNG continuation.
    change(
        state,
        "td/save.py",
        '        "wave": game.wave,\n',
        '        "wave": game.wave,\n        "seed": game.seed,\n'
        '        "rng_state": repr(game.rng.getstate()) if game.rng else None,\n',
    )
    change(
        state,
        "td/save.py",
        '        wave=data["wave"],\n',
        '        wave=data["wave"], seed=data.get("seed", 0),\n',
    )
    change(
        state,
        "td/save.py",
        '                "kind": enemy.kind,\n',
        '                "kind": enemy.kind,\n                "slow_ticks": enemy.slow_ticks,\n'
        '                "armor": enemy.armor,\n',
    )
    change(
        state,
        "td/save.py",
        '            row["kind"],\n',
        '            row["kind"],\n            row.get("slow_ticks", 0), row.get("armor", 0),\n',
    )
    change(
        state,
        "td/save.py",
        "    return game\n\n\ndef validate_payload",
        "    if data.get('rng_state') is not None:\n"
        "        import ast\n        from .rng import GameRNG\n"
        "        game.rng = GameRNG(game.seed)\n"
        "        game.rng.setstate(ast.literal_eval(data['rng_state']))\n"
        "    return game\n\n\ndef validate_payload",
    )
    emit_stage(
        8,
        previous,
        state,
        """Add save/load for an in-progress game. Preserve resources, wave, tick,
tower cooldowns, enemy health/progress/slow/armor, and the next RNG result.
Keep the plain-data schema deterministic and reject incomplete payloads.""",
        """from td.model import Enemy, Game, Tower
from td.save import load_game, save_game

def test_round_trip_preserves_game_state():
    game = Game(lives=7, money=13, seed=5,
                enemies=[Enemy("e", 4, 2, 5, armor=1)],
                towers=[Tower("t", 1, 0, cooldown_left=1)])
    restored = load_game(save_game(game))
    assert restored.lives == 7 and restored.money == 13
    assert restored.enemies[0].armor == 1
    assert restored.towers[0].cooldown_left == 1
""",
        """from td.model import Game
from td.pathing import spawn_wave
from td.save import load_game, save_game

def test_round_trip_preserves_rng_continuation():
    game = Game(seed=7)
    spawn_wave(game, 1, 2)
    payload = save_game(game)
    expected = [enemy.hp for enemy in spawn_wave(game, 2, 4)]
    restored = load_game(payload)
    assert [enemy.hp for enemy in spawn_wave(restored, 2, 4)] == expected

def test_save_preserves_later_stage_enemy_state():
    from td.model import Enemy
    game = Game(enemies=[Enemy("e", 2, 5, 8, slow_ticks=2, armor=1)])
    restored = load_game(save_game(game))
    assert restored.enemies[0].slow_ticks == 2
    assert restored.enemies[0].armor == 1
""",
    )
    put(8, "", "supersedes.json", "[]")

    # Write the final reference tree back to starter-relative snapshots only in
    # the patch files; participant workspaces always begin from the true starter.
    manifest = {
        "project": "tower_defense",
        "kind": "evaluation",
        "stages": 8,
        "orientation_answers": {
            "q1": "td.model.Tower",
            "q2": "td.model.Enemy",
            "q3": "td.targeting.choose_target",
            "q4": "td.combat.resolve_attacks",
            "q5": "td.pathing.spawn_wave",
            "q6": 20,
            "q7": "td.game.tick",
            "q8": "td.save.save_game",
        },
        "probes": [
            {"introduced": 1, "retired": 2, "tests": [f"Q{i}" for i in range(1, 9)],
             "text_only": False, "requirement": "R1.1"},
            {"introduced": 2, "retired": None,
             "tests": ["tests/hidden_2/test_tower_stage2.py::test_slow_duration_expires_then_movement_resumes",
                       "tests/hidden_2/test_tower_stage2.py::test_refresh_never_shortens_duration"],
             "text_only": False, "requirement": "R2.1"},
            {"introduced": 3, "retired": None,
             "tests": ["tests/hidden_3/test_tower_stage3.py::test_armor_cannot_heal_or_create_negative_damage"],
             "text_only": False, "requirement": "R3.1"},
            {"introduced": 3, "retired": 7,
             "tests": ["tests/hidden_3/test_tower_sell_deferred.py::test_tower_selling_is_deferred"],
             "text_only": True, "requirement": "D3.1"},
            {"introduced": 4, "retired": None,
             "tests": ["tests/hidden_4/test_tower_stage4.py::test_attack_becomes_ready_after_exact_wait"],
             "text_only": False, "requirement": "R4.1"},
            {"introduced": 5, "retired": None,
             "tests": ["tests/hidden_5/test_tower_stage5.py::test_furthest_progress_precedes_lexical_identifier"],
             "text_only": False, "requirement": "R5.1"},
            {"introduced": 6, "retired": None,
             "tests": ["tests/hidden_6/test_tower_stage6.py::test_rng_streams_are_owned_by_game",
                       "tests/hidden_6/test_tower_stage6.py::test_distinct_seed_changes_generated_wave"],
             "text_only": False, "requirement": "G6.1"},
            {"introduced": 7, "retired": None,
             "tests": ["tests/hidden_7/test_tower_stage7.py::test_summary_handles_final_defeat",
                       "tests/hidden_7/test_tower_stage7.py::test_sale_refund_rounds_down_and_unknown_id_is_noop",
                       "tests/hidden_7/test_tower_stage7_deferred.py::test_deferred_sell_decision_uses_floor_of_three_quarters"],
             "text_only": False, "requirement": "D3.1"},
            {"introduced": 8, "retired": None,
             "tests": ["tests/hidden_8/test_tower_stage8.py::test_round_trip_preserves_rng_continuation",
                       "tests/hidden_8/test_tower_stage8.py::test_save_preserves_later_stage_enemy_state"],
             "text_only": False, "requirement": "R8.1"},
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("wrote tower-defense stages and reference patches")


if __name__ == "__main__":
    main()
