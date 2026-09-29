from arena.inventory import Bag, use
from arena.mapgen import bordered_world
from arena.model import Actor, Item, Point
world = bordered_world(7,7)
actor = Actor('hero', Point(1,1), 5, 5, 1, 'p', '@')
actor.statuses['poison'] = 3
bag = Bag(items=[Item('ant', 'antidote', 0)])
use(world, actor, bag, 'ant')
assert 'poison' not in actor.statuses
