from td.combat import fire_tower
from td.economy import place_tower
from td.model import Enemy, Game


def test_tower_purchase_deducts_cost():
    game = Game(money=20)
    tower = place_tower(game, "t", 1, 0, 10)
    assert game.money == 10
    assert tower.cost == 10


def test_attack_applies_damage_and_cooldown():
    game = Game(enemies=[Enemy("e", 1, 5, 5)])
    tower = place_tower(game, "t", 1, 0, 0)
    assert fire_tower(game, tower) == ("e", 2)
    assert tower.cooldown_left == 2
    assert game.enemies[0].hp == 3


def test_tower_without_target_remains_ready():
    from td.model import Tower

    game = Game()
    tower = Tower("t", 0, 0)
    assert fire_tower(game, tower) is None
    assert tower.cooldown_left == 0


def test_purchase_is_atomic_when_funds_are_low():
    game = Game(money=2)
    try:
        place_tower(game, "t", 1, 0, 5)
    except ValueError:
        pass
    else:
        raise AssertionError("purchase unexpectedly succeeded")
    assert game.money == 2 and game.towers == []


def test_path_and_range_boundary():
    from td.geometry import in_range

    assert in_range(0, 0, 3, 4, 5)
    assert not in_range(0, 0, 4, 4, 5)
