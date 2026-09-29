# req: R7.1
from arena.inventory import Bag, use
from arena.mapgen import bordered_world
from arena.model import Actor, Item, Point

def test_antidote_stops_poison():
    w=bordered_world(7,7); a=Actor('a',Point(1,1),2,5,1,'p','@')
    a.statuses['poison']=2
    bag=Bag(items=[Item('ant','antidote')])
    use(w,a,bag,'ant')
    assert not a.statuses and not bag.items
