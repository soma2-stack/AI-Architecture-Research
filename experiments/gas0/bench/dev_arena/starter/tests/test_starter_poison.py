from arena.combat import apply_status, tick_status
from arena.mapgen import bordered_world
from arena.model import Actor, Point


def test_poison_can_kill_at_starter():
    world = bordered_world(7, 7)
    hero = Actor("hero", Point(1, 1), 1, 10, 2, "player", "@")
    world.add_actor(hero)
    apply_status(world, hero, "poison", 1)
    tick_status(world, hero)
    assert not hero.alive
