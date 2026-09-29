# req: R3.1
from arena.inventory import Bag, use
from arena.model import Actor, Item, Point
from arena.mapgen import bordered_world

def test_shield_tonic_consumed():
    world = bordered_world(7,7)
    actor = Actor('a', Point(1,1), 5, 5, 1, 'p', '@', shield=1)
    bag = Bag(items=[Item('s', 'shield_tonic', 2)])
    assert use(world, actor, bag, 's') == 2
    assert actor.shield == 3 and bag.items == []
