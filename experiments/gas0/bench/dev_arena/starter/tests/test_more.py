from arena import Arena
from arena.combat import apply_status, tick_status
from arena.hud import map_lines, render, status_line
from arena.inventory import Bag, pickup, use
from arena.mapgen import bordered_world, connected, generate
from arena.model import Actor, Item, Point
from arena.path import shortest_path, visible
from arena.rng import Dice
from arena.save import dumps, loads


def test_point_shift_and_distance():
    p = Point(2, 3)
    assert p.shift(-1, 2) == Point(1, 5)
    assert p.manhattan(Point(5, 1)) == 5


def test_point_neighbors_are_cardinal():
    neighbors = set(Point(3, 3).neighbors4())
    assert neighbors == {Point(3, 2), Point(4, 3), Point(3, 4), Point(2, 3)}


def test_world_rejects_occupied_spawn():
    world = bordered_world(7, 7)
    world.add_actor(Actor("a", Point(1, 1), 2, 2, 1, "p", "@"))
    try:
        world.add_actor(Actor("b", Point(1, 1), 2, 2, 1, "e", "e"))
    except ValueError:
        pass
    else:
        raise AssertionError("occupied spawn was accepted")


def test_world_rejects_blocked_item():
    world = bordered_world(7, 7)
    try:
        world.add_item(Point(0, 0), Item("x", "potion", 1))
    except ValueError:
        pass
    else:
        raise AssertionError("wall item was accepted")


def test_generator_has_path():
    world = generate(11)
    assert connected(world, Point(1, 1), Point(world.width - 2, world.height - 2))


def test_path_obeys_wall():
    world = bordered_world(7, 7)
    world.walls.add(Point(2, 1))
    path = shortest_path(world, Point(1, 1), Point(3, 1))
    assert Point(2, 1) not in path and len(path) == 5


def test_visibility_radius_zero():
    world = bordered_world(7, 7)
    assert visible(world, Point(2, 2), 0) == {Point(2, 2)}


def test_dice_reproducible():
    a, b = Dice(3), Dice(3)
    assert [a.randint(1, 9) for _ in range(10)] == [b.randint(1, 9) for _ in range(10)]


def test_dice_state_restore():
    dice = Dice(4)
    state = dice.getstate()
    first = dice.randint(1, 100)
    dice.setstate(state)
    assert dice.randint(1, 100) == first


def test_bag_capacity():
    bag = Bag(capacity=1)
    bag.add(Item("a", "potion", 2))
    assert not bag.has_space()


def test_pickup_one_item():
    world = bordered_world(7, 7)
    hero = Actor("hero", Point(1, 1), 4, 4, 1, "p", "@")
    world.add_actor(hero)
    world.add_item(hero.pos, Item("p", "potion", 2))
    bag = Bag()
    assert pickup(world, hero, bag).item_id == "p"
    assert not world.items.get(hero.pos)


def test_potion_heals_no_more_than_max():
    world = bordered_world(7, 7)
    hero = Actor("hero", Point(1, 1), 3, 5, 1, "p", "@")
    bag = Bag(items=[Item("p", "potion", 9)])
    assert use(world, hero, bag, "p") == 2
    assert hero.hp == 5


def test_status_expires():
    world = bordered_world(7, 7)
    hero = Actor("hero", Point(1, 1), 5, 5, 1, "p", "@")
    apply_status(world, hero, "slow", 1)
    tick_status(world, hero)
    assert "slow" not in hero.statuses


def test_hud_pure_render():
    game = Arena(1, bordered_world(7, 7))
    game.add_player()
    assert len(map_lines(game.world, "hero")) == 7
    assert "HP 10/10" in status_line(game.world, "hero")
    assert "@" in render(game.world, "hero")


def test_save_is_deterministic():
    game = Arena(1, bordered_world(7, 7))
    game.add_player()
    text = dumps(game.world, game.bags)
    world, bags = loads(text)
    assert dumps(world, bags) == text


def test_enemy_moves_toward_player():
    game = Arena(1, bordered_world(7, 7))
    game.add_player()
    enemy = game.add_enemy("rat", Point(3, 1))
    game.enemy_turn()
    assert enemy.pos == Point(2, 1)
