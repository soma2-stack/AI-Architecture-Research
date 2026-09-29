from arena import Arena
from arena.inventory import Bag
from arena.mapgen import bordered_world, generate
from arena.model import Item, Point
from arena.path import shortest_path
from arena.save import dumps, loads


def test_seeded_world():
    assert generate(4).walls == generate(4).walls


def test_world_border():
    world = bordered_world(7, 7)
    assert not world.walkable(Point(0, 2))
    assert world.walkable(Point(1, 2))


def test_path():
    world = bordered_world(7, 7)
    path = shortest_path(world, Point(1, 1), Point(4, 4))
    assert path[0] == Point(1, 1) and path[-1] == Point(4, 4)


def test_move():
    game = Arena(1, bordered_world(7, 7))
    hero = game.add_player()
    assert game.player_move("hero", 1, 0)
    assert hero.pos == Point(2, 1)


def test_combat_death_event():
    game = Arena(1, bordered_world(7, 7))
    game.add_player()
    game.add_enemy("rat", Point(2, 1), hp=1)
    game.player_move("hero", 1, 0)
    assert [e.name for e in game.world.events] == ["hit", "death"]


def test_inventory():
    bag = Bag(1)
    bag.add(Item("p", "potion", 2))
    assert bag.find("potion").item_id == "p"
    assert bag.remove("p").power == 2


def test_save_round_trip():
    game = Arena(1, bordered_world(7, 7))
    game.add_player()
    restored, bags = loads(dumps(game.world, game.bags))
    assert restored.actors["hero"].hp == 10
    assert bags["hero"].capacity == 6
