# req: R7.1 and deferred R3.3
from arena.inventory import Bag, use
from arena.mapgen import bordered_world
from arena.model import Actor, Item, Point

def test_antidote_does_not_heal_or_grant_shield():
    w=bordered_world(7,7); a=Actor('a',Point(1,1),2,5,1,'p','@',shield=1)
    a.statuses['poison']=3
    bag=Bag(items=[Item('ant','antidote')])
    use(w,a,bag,'ant')
    assert (a.hp,a.shield)==(2,1) and 'poison' not in a.statuses

def test_antidote_event_has_sequence():
    w=bordered_world(7,7); a=Actor('a',Point(1,1),2,5,1,'p','@')
    a.statuses['poison']=3
    bag=Bag(items=[Item('ant','antidote')])
    use(w,a,bag,'ant')
    assert w.events[-1].seq == 1
