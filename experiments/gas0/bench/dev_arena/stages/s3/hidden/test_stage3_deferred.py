# req: R3.3 (text-only deferred item)
import pytest
from arena.inventory import Bag, use
from arena.mapgen import bordered_world
from arena.model import Actor, Item, Point

def test_antidote_still_deferred():
    w=bordered_world(7,7); a=Actor('a',Point(1,1),3,5,1,'p','@')
    a.statuses['poison']=2
    bag=Bag(items=[Item('ant','antidote')])
    with pytest.raises(ValueError):
        use(w,a,bag,'ant')
    assert a.statuses['poison']==2 and bag.find('antidote')
