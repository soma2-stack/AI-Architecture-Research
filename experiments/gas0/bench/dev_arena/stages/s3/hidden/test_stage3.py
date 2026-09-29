# req: R3.1
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
