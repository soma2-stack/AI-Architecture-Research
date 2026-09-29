# req: R2.2
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
