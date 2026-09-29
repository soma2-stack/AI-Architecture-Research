"""Generate staged reference patches and tests for the deck-builder project."""

from __future__ import annotations

import ast
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


def change(state, name, old, new):
    if state[name].count(old) != 1:
        raise AssertionError((name, old, state[name].count(old)))
    state[name] = state[name].replace(old, new)


def put(stage, folder, name, body):
    path = STAGES / f"s{stage}" / folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")


def emit(stage, before, after, request, visible, hidden, visible_name=None, hidden_name=None):
    (REFERENCE / f"s{stage}.patch").write_bytes(diff(before, after))
    put(stage, "", "request.md", request)
    put(stage, "visible", visible_name or f"test_deck_stage{stage}.py", visible)
    put(stage, "hidden", hidden_name or f"test_deck_stage{stage}.py", hidden)


def main():
    for folder in (STAGES, REFERENCE):
        if folder.exists():
            shutil.rmtree(folder)
    STAGES.mkdir()
    REFERENCE.mkdir()
    state = snapshot()
    put(1, "", "request.md", """Do not edit. Inspect the deck-builder project and return JSON q1 through
q8: q1 Card type; q2 Deck type; q3 card play function; q4 draw helper; q5 enemy
attack function; q6 turn-advance function; q7 save function; q8 terminal-state
predicate. Use exact identifiers.""")
    (REFERENCE / "s1.patch").write_bytes(b"")
    put(1, "visible", "test_deck_stage1.py", "def test_orientation_stage_is_read_only():\n    assert True")
    put(1, "hidden", "test_deck_stage1.py", "def test_orientation_has_no_feature_delta():\n    assert True")
    previous = state.copy()

    # S2: block is cleared after the enemy's action.
    change(state, "deckgame/combat.py",
           "    suffered = incoming - absorbed\n    battle.hp = max(0, battle.hp - suffered)\n",
           "    suffered = incoming - absorbed\n    battle.hp = max(0, battle.hp - suffered)\n")
    change(state, "deckgame/combat.py",
           "    suffered = enemy_attack(battle)\n    battle.turn += 1\n",
           "    suffered = enemy_attack(battle)\n    battle.block = 0\n    battle.turn += 1\n")
    emit(2, previous, state,
         """Make block last only through the current enemy turn. Resolve the
enemy's attack using existing block, then clear any remaining block before the
next player turn. Do not change HP or energy rules.""",
         """from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_unused_block_clears_after_enemy_turn():
    battle = create_battle([], intent=1)
    battle.block = 5
    end_enemy_turn(battle)
    assert battle.hp == 30
    assert battle.block == 0
""",
         """from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_only_current_block_absorbs_attack():
    battle = create_battle([], hp=10, intent=4)
    battle.block = 2
    assert end_enemy_turn(battle) == 2
    assert battle.hp == 8 and battle.block == 0

def test_next_turn_does_not_inherit_old_block():
    battle = create_battle([], intent=3)
    battle.block = 9
    end_enemy_turn(battle)
    assert battle.block == 0
""")
    previous = state.copy()

    # S3: poison ticks before the enemy attack; reward choice is deferred.
    change(state, "deckgame/model.py",
           "    events: list[dict] = field(default_factory=list)\n",
           "    events: list[dict] = field(default_factory=list)\n    poison: int = 0\n")
    state["deckgame/status.py"] = """def apply_poison(battle, amount):
    battle.poison = max(0, battle.poison + int(amount))
    return battle.poison

def tick_poison(battle):
    amount = max(0, int(battle.poison))
    if amount == 0 or battle.enemy_hp <= 0:
        return 0
    dealt = min(amount, battle.enemy_hp)
    battle.enemy_hp -= dealt
    battle.poison = max(0, battle.poison - 1)
    battle.events.append({"kind": "poison", "amount": dealt})
    return dealt

def poison_summary(battle):
    return {"amount": battle.poison, "active": battle.poison > 0}
"""
    change(state, "deckgame/combat.py",
           "def end_enemy_turn(battle):\n    \"\"\"Resolve enemy action and start the next player turn.\"\"\"\n    suffered = enemy_attack(battle)\n",
           "def end_enemy_turn(battle):\n    \"\"\"Resolve enemy action and start the next player turn.\"\"\"\n"
           "    from .status import tick_poison\n    tick_poison(battle)\n    suffered = enemy_attack(battle)\n")
    emit(3, previous, state,
         """Add persistent poison that deals its current amount at the beginning
of the enemy phase, then loses one stack even if the enemy survives. Poison
cannot deal more than the enemy's remaining HP. Designer decision D3.1: a
future reward offer is deterministic for a run and contains three distinct
choices. Defer reward offers until Stage 7.""",
         """from deckgame.game import create_battle
from deckgame.status import apply_poison, tick_poison

def test_poison_ticks_and_loses_one_stack():
    battle = create_battle([], enemy_hp=8)
    apply_poison(battle, 3)
    assert tick_poison(battle) == 3
    assert battle.enemy_hp == 5 and battle.poison == 2
""",
         """from deckgame.game import create_battle
from deckgame.status import apply_poison, tick_poison

def test_poison_is_capped_by_remaining_health():
    battle = create_battle([], enemy_hp=2)
    apply_poison(battle, 5)
    assert tick_poison(battle) == 2
    assert battle.enemy_hp == 0 and battle.poison == 4

def test_poison_does_not_damage_defeated_enemy():
    battle = create_battle([], enemy_hp=0)
    apply_poison(battle, 2)
    assert tick_poison(battle) == 0

def test_poison_stack_is_nonnegative():
    battle = create_battle([])
    assert apply_poison(battle, -4) == 0
""")
    put(3, "hidden", "test_deck_poison_timing.py",
        """from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_poison_ticks_before_enemy_attack_in_original_timing():
    battle = create_battle([], enemy_hp=20, intent=5)
    battle.poison = 1
    end_enemy_turn(battle)
    assert [event["kind"] for event in battle.events][-2:] == ["poison", "enemy_attack"]
""")
    put(3, "hidden", "test_deck_reward_deferred.py",
        """def test_reward_offer_is_deferred():
    import deckgame.rewards as rewards
    assert not hasattr(rewards, "offer_rewards")
""")
    put(3, "", "supersedes.json", "[]")
    previous = state.copy()

    # S4 injects duplicate-card corruption only when recycling beside exhaust.
    bugged = state.copy()
    change(bugged, "deckgame/piles.py",
           "    deck.draw_pile.extend(deck.discard_pile)\n",
           "    deck.draw_pile.extend(deck.discard_pile + deck.exhaust_pile)\n")
    (STAGES / "s4").mkdir(parents=True, exist_ok=True)
    (STAGES / "s4" / "bug.patch").write_bytes(diff(state, bugged))
    emit(4, bugged, state,
         """A reshuffle can put an already exhausted card back into the draw
pile, duplicating its use. Find and fix the reshuffle regression while keeping
the ordinary discard-to-draw order stable.""",
         """from deckgame.model import Card, Deck
from deckgame.piles import recycle_discard

def test_recycle_moves_discard_without_copying_exhaust():
    used = Card("used", "Used", 1)
    fresh = Card("fresh", "Fresh", 1)
    deck = Deck(discard_pile=[fresh], exhaust_pile=[used])
    assert recycle_discard(deck) == 1
    assert deck.draw_pile == [fresh]
    assert deck.exhaust_pile == [used]
""",
         """from deckgame.model import Card, Deck
from deckgame.piles import count_cards, recycle_discard

def test_recycle_never_reintroduces_exhausted_card():
    exhausted = Card("gone", "Gone", 1)
    remaining = Card("kept", "Kept", 1)
    deck = Deck(discard_pile=[remaining], exhaust_pile=[exhausted])
    before = count_cards(deck)
    recycle_discard(deck)
    assert count_cards(deck) == before
    assert [card.card_id for card in deck.draw_pile] == ["kept"]
    assert [card.card_id for card in deck.exhaust_pile] == ["gone"]
""")
    previous = state.copy()

    # S5 moves poison from before the enemy action to after it.
    change(state, "deckgame/combat.py",
           "    from .status import tick_poison\n    tick_poison(battle)\n    suffered = enemy_attack(battle)\n",
           "    from .status import tick_poison\n    suffered = enemy_attack(battle)\n    tick_poison(battle)\n")
    emit(5, previous, state,
         """Change poison timing so the enemy completes its attack before poison
ticks. Keep the same stack decay and damage cap. Retire the old timing contract;
all other poison and block behavior remains in force.""",
         """from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_enemy_action_precedes_poison_tick():
    battle = create_battle([], hp=10, enemy_hp=20, intent=4)
    battle.poison = 2
    end_enemy_turn(battle)
    assert battle.hp == 6
    assert [event["kind"] for event in battle.events][-2:] == ["enemy_attack", "poison"]
""",
         """from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_poison_tick_follows_attack_and_keeps_stack_rule():
    battle = create_battle([], hp=10, enemy_hp=20, intent=3)
    battle.poison = 2
    end_enemy_turn(battle)
    assert battle.hp == 7 and battle.poison == 1
    assert [event["kind"] for event in battle.events][-2:] == ["enemy_attack", "poison"]
""")
    put(5, "", "supersedes.json", json.dumps(["tests/hidden_3/test_deck_poison_timing.py"]))
    previous = state.copy()

    # S6 gives every battle an independent seeded random stream.
    state["deckgame/rng.py"] = """import random

class RunRNG:
    def __init__(self, seed=0):
        self._random = random.Random(int(seed))
    def shuffle(self, values):
        self._random.shuffle(values)
    def sample(self, values, count):
        return self._random.sample(list(values), int(count))
    def getstate(self):
        return self._random.getstate()
    def setstate(self, state):
        self._random.setstate(state)
"""
    change(state, "deckgame/model.py",
           "    poison: int = 0\n",
           "    poison: int = 0\n    seed: int = 0\n    rng: object = field(default=None, repr=False)\n    reward_offer: list[Card] = field(default_factory=list)\n")
    change(state, "deckgame/game.py",
           "def create_battle(cards=None, hp=30, enemy_hp=20, intent=5):",
           "def create_battle(cards=None, hp=30, enemy_hp=20, intent=5, seed=0):")
    change(state, "deckgame/game.py",
           "    initial = list(starter_cards() if cards is None else cards)\n    return Battle(",
           "    from .rng import RunRNG\n    initial = list(starter_cards() if cards is None else cards)\n"
           "    seed = int(seed)\n    return Battle(")
    change(state, "deckgame/game.py",
           "        deck=Deck(draw_pile=initial),\n",
           "        deck=Deck(draw_pile=initial), seed=seed, rng=RunRNG(seed),\n")
    emit(6, previous, state,
         """Add a per-battle RNG initialized from a run seed. A battle's shuffle
and reward decisions must not use or mutate process-global randomness. Equal
seeds replay equally; independent battle instances have isolated streams.""",
         """from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.rng import RunRNG

def test_run_rng_is_repeatable():
    first, second = RunRNG(44), RunRNG(44)
    a = [Card(str(i), str(i), 1) for i in range(5)]
    b = list(a)
    first.shuffle(a)
    second.shuffle(b)
    assert [card.card_id for card in a] == [card.card_id for card in b]
""",
         """from deckgame.rng import RunRNG
from deckgame.model import Card

def test_rng_instances_have_independent_replay():
    a, b, c = RunRNG(5), RunRNG(5), RunRNG(5)
    values = list(range(10))
    assert a.sample(values, 4) == b.sample(values, 4) == c.sample(values, 4)

def test_sampling_is_without_replacement():
    result = RunRNG(7).sample([Card(str(i), str(i), 1) for i in range(8)], 5)
    assert len({card.card_id for card in result}) == 5

def test_battle_instances_own_seeded_streams():
    from deckgame.game import create_battle
    a, b = create_battle([], seed=33), create_battle([], seed=33)
    values = [Card(str(i), str(i), 1) for i in range(6)]
    assert a.rng.sample(values, 3) == b.rng.sample(values, 3)
""")
    put(6, "", "static_checks.py",
        """import ast
from pathlib import Path

def test_global_random_import_is_confined_to_rng_module():
    package = Path(__file__).parents[1] / "deckgame"
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
""")
    previous = state.copy()

    # S7 repairs the exhausted-deck status crash and implements deferred offers.
    previous = state.copy()
    change(state, "deckgame/render.py",
           "def next_card_label(battle):\n"
           "    \"\"\"Preview the next draw; empty-deck handling is added at Stage 7.\"\"\"\n"
           "    return battle.deck.draw_pile[0].name\n",
           "def next_card_label(battle):\n"
           "    \"\"\"Preview the next draw; empty-deck handling is added at Stage 7.\"\"\"\n"
           "    if not battle.deck.draw_pile:\n        return 'No cards'\n"
           "    return battle.deck.draw_pile[0].name\n")
    change(state, "deckgame/rng.py",
           "    def getstate(self):\n",
           "    def choice(self, values):\n        return self._random.choice(tuple(values))\n\n"
           "    def getstate(self):\n")
    state["deckgame/rewards.py"] += """

def offer_rewards(battle, cards):
    if battle.rng is None:
        from .rng import RunRNG
        battle.rng = RunRNG(battle.seed)
    unique = {}
    for card in cards:
        unique.setdefault(card.card_id, card)
    pool = list(unique.values())
    if len(pool) < 3:
        raise ValueError("at least three distinct rewards are required")
    battle.reward_offer = battle.rng.sample(pool, 3)
    return list(battle.reward_offer)

def choose_reward(battle, card_id):
    chosen = next((card for card in battle.reward_offer if card.card_id == card_id), None)
    if chosen is None:
        raise ValueError("reward is not in the current offer")
    from .piles import add_card
    add_card(battle.deck, chosen)
    battle.reward_offer.clear()
    return chosen
"""
    emit(7, previous, state,
         """After the draw pile and discard pile are both empty, the status
panel crashes. Make the empty preview safe. Add a run reward offer and let the
player claim one available reward; reject choices that were not offered.""",
         """from deckgame.game import create_battle
from deckgame.render import next_card_label
from deckgame.rewards import choose_reward, offer_rewards
from deckgame.model import Card

def test_empty_draw_preview_is_safe():
    assert next_card_label(create_battle([])) == "No cards"

def test_claimed_reward_enters_deck():
    battle = create_battle([])
    offer = offer_rewards(battle, [Card(str(i), str(i), 1) for i in range(5)])
    selected = choose_reward(battle, offer[0].card_id)
    assert selected in battle.deck.draw_pile
""",
         """from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.rewards import choose_reward, offer_rewards

def test_offer_has_frozen_count_and_distinct_ids():
    battle = create_battle([])
    cards = [Card(str(i), str(i), 1) for i in range(6)]
    offer = offer_rewards(battle, cards)
    assert len(offer) == 3
    assert len({card.card_id for card in offer}) == 3

def test_offer_is_repeatable_for_same_seed():
    cards = [Card(str(i), str(i), 1) for i in range(6)]
    a, b = create_battle([]), create_battle([])
    a.seed = b.seed = 21
    assert [x.card_id for x in offer_rewards(a, cards)] == [x.card_id for x in offer_rewards(b, cards)]

def test_unoffered_reward_cannot_be_chosen():
    battle = create_battle([])
    offer_rewards(battle, [Card(str(i), str(i), 1) for i in range(4)])
    try:
        choose_reward(battle, "missing")
    except ValueError:
        pass
    else:
        raise AssertionError("unoffered reward was accepted")
""")
    put(7, "hidden", "test_deck_reward_deferred_stage7.py",
        """from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.rewards import offer_rewards

def test_deferred_reward_rule_is_enforced():
    battle = create_battle([])
    cards = [Card(str(i), str(i), 1) for i in range(5)]
    offer = offer_rewards(battle, cards)
    assert len(offer) == 3 and len({card.card_id for card in offer}) == 3
""")
    put(7, "", "supersedes.json", json.dumps(["tests/hidden_3/test_deck_reward_deferred.py"]))
    put(7, "", "scenario.py",
        """from deckgame.game import create_battle
from deckgame.render import next_card_label

battle = create_battle([])
print(next_card_label(battle))
""")
    previous = state.copy()

    # S8 persists zones, statuses, seed, offers, and RNG continuation.
    change(state, "deckgame/save.py",
           '        "turn": battle.turn,\n',
           '        "turn": battle.turn,\n        "poison": battle.poison,\n'
           '        "seed": battle.seed,\n'
           '        "rng_state": repr(battle.rng.getstate()) if battle.rng else None,\n'
           '        "offer": [card_row(card) for card in battle.reward_offer],\n')
    change(state, "deckgame/save.py",
           '    return Battle(data["hp"], data["max_hp"], data["block"], data["energy"],\n'
           '                  data["enemy_hp"], data["enemy_intent"], data["turn"], deck)\n',
           '    battle = Battle(data["hp"], data["max_hp"], data["block"], data["energy"],\n'
           '                    data["enemy_hp"], data["enemy_intent"], data["turn"], deck,\n'
           '                    poison=data.get("poison", 0), seed=data.get("seed", 0))\n'
           '    from .model import Card\n'
           '    battle.reward_offer = [Card(row["id"], row["name"], row["cost"], row["damage"],\n'
           '                                row["block"], row["kind"]) for row in data.get("offer", [])]\n'
           '    if data.get("rng_state") is not None:\n'
           '        import ast\n        from .rng import RunRNG\n'
           '        battle.rng = RunRNG(battle.seed)\n'
           '        battle.rng.setstate(ast.literal_eval(data["rng_state"]))\n'
           '    return battle\n')
    emit(8, previous, state,
         """Add a deterministic save/load round trip for combat. Preserve all
card zones, current combat values, poison, selected offer, and random-stream
continuation. Existing old-format payloads may use defaults for new fields.""",
         """from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.save import load_battle, save_battle

def test_round_trip_preserves_piles_and_poison():
    battle = create_battle([Card("x", "X", 1)], hp=17)
    battle.poison = 2
    restored = load_battle(save_battle(battle))
    assert restored.hp == 17 and restored.poison == 2
    assert restored.deck.draw_pile[0].card_id == "x"
""",
         """from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.rewards import offer_rewards
from deckgame.save import load_battle, save_battle

def test_round_trip_preserves_random_continuation():
    battle = create_battle([])
    battle.seed = 19
    cards = [Card(str(i), str(i), 1) for i in range(6)]
    offer_rewards(battle, cards)
    payload = save_battle(battle)
    expected = [card.card_id for card in offer_rewards(battle, cards)]
    restored = load_battle(payload)
    assert [card.card_id for card in offer_rewards(restored, cards)] == expected

def test_round_trip_preserves_poison_and_reward_offer():
    battle = create_battle([])
    battle.poison = 4
    cards = [Card(str(i), str(i), 1) for i in range(5)]
    offer_rewards(battle, cards)
    restored = load_battle(save_battle(battle))
    assert restored.poison == 4
    assert [card.card_id for card in restored.reward_offer] == [card.card_id for card in battle.reward_offer]
""")
    put(8, "", "supersedes.json", "[]")

    probes = [
        {"introduced": 1, "retired": 2, "tests": [f"Q{i}" for i in range(1, 9)],
         "text_only": False, "requirement": "R1.1"},
        {"introduced": 2, "retired": None,
         "tests": ["tests/hidden_2/test_deck_stage2.py::test_next_turn_does_not_inherit_old_block"],
         "text_only": False, "requirement": "R2.1"},
        {"introduced": 3, "retired": None,
         "tests": ["tests/hidden_3/test_deck_stage3.py::test_poison_is_capped_by_remaining_health",
                   "tests/hidden_3/test_deck_stage3.py::test_poison_does_not_damage_defeated_enemy"],
         "text_only": False, "requirement": "R3.1"},
        {"introduced": 3, "retired": 5,
         "tests": ["tests/hidden_3/test_deck_poison_timing.py::test_poison_ticks_before_enemy_attack_in_original_timing"],
         "text_only": False, "requirement": "R3.2"},
        {"introduced": 3, "retired": 7,
         "tests": ["tests/hidden_3/test_deck_reward_deferred.py::test_reward_offer_is_deferred"],
         "text_only": True, "requirement": "D3.1"},
        {"introduced": 4, "retired": None,
         "tests": ["tests/hidden_4/test_deck_stage4.py::test_recycle_never_reintroduces_exhausted_card"],
         "text_only": False, "requirement": "R4.1"},
        {"introduced": 5, "retired": None,
         "tests": ["tests/hidden_5/test_deck_stage5.py::test_poison_tick_follows_attack_and_keeps_stack_rule"],
         "text_only": False, "requirement": "R5.1"},
        {"introduced": 6, "retired": None,
         "tests": ["tests/hidden_6/test_deck_stage6.py::test_rng_instances_have_independent_replay",
                   "tests/hidden_6/test_deck_stage6.py::test_sampling_is_without_replacement"],
         "text_only": False, "requirement": "G6.1"},
        {"introduced": 7, "retired": None,
         "tests": ["tests/hidden_7/test_deck_stage7.py::test_offer_has_frozen_count_and_distinct_ids",
                   "tests/hidden_7/test_deck_stage7.py::test_offer_is_repeatable_for_same_seed",
                   "tests/hidden_7/test_deck_reward_deferred_stage7.py::test_deferred_reward_rule_is_enforced"],
         "text_only": False, "requirement": "D3.1"},
        {"introduced": 8, "retired": None,
         "tests": ["tests/hidden_8/test_deck_stage8.py::test_round_trip_preserves_random_continuation",
                   "tests/hidden_8/test_deck_stage8.py::test_round_trip_preserves_poison_and_reward_offer"],
         "text_only": False, "requirement": "R8.1"},
    ]
    manifest = {
        "project": "deck_builder",
        "kind": "evaluation",
        "stages": 8,
        "orientation_answers": {
            "q1": "deckgame.model.Card",
            "q2": "deckgame.model.Deck",
            "q3": "deckgame.combat.play_card",
            "q4": "deckgame.piles.draw_card",
            "q5": "deckgame.combat.enemy_attack",
            "q6": "deckgame.turns.advance_turn",
            "q7": "deckgame.save.save_battle",
            "q8": "deckgame.model.is_terminal",
        },
        "probes": probes,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("wrote deck-builder stages and reference patches")


if __name__ == "__main__":
    main()
